"""
benchmarks/nbody_pool_audit.py — NBODY-POOL-AUDIT (round 118, dir/nbody-pool-audit).

Preregistered in PRD §19 round 118 BEFORE execution: close round-95's stated
boundary ("NBody particle pooling unaudited") — does the mean-pooled node
channel of LiquidNBodyModel.infer_context preserve identifiable information
about the hidden per-particle mass field?

CODE AUDIT (prereg half 1, T0): infer_context = shared Linear over nodes
then x.mean(dim=2). Mean commutes with the shared linear, so the ctx input
is the per-timestep UNWEIGHTED mean position/velocity (a CoM-like summary,
4xD numbers per step) — a structural N→4xD squeeze. Unlike the M2 grid
telescoping (exact annihilation, 8.6e-11) there is NO exact-zero identity
here (momentum conservation + mass-independent wall reflections make the
CoM nearly mass-free, but the unweighted-mean vs mass-weighted-CoM gap
carries second-order mass information).

EMPIRICAL PROBE (prereg half 2, training-free and DECISIVE): data-level
Fisher port of field_identifiability_probe --meanpool. Central-difference
Jacobians of (a) the full observed prefix and (b) the pooled CoM-like
summary w.r.t. each mass, simulated by the zero-parameter engine.
retention = trace(J_p^T J_p) / trace(J_f^T J_f). By the data-processing
inequality NO trained decoder can extract more mass information from ctx
than Fisher_pooled — the probe bounds the channel capacity directly.

Negative criteria ①-③ are preregistered in PRD §19. Results JSON follows
the audit schema; meta carries exec_tier passthrough from probe_run.
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_nbody
from awareliquid_physics.observability import run_metadata
from awareliquid_physics.physics_ops import (integrate_verlet,
                                             reflect_in_box,
                                             resolve_sphere_collisions)

T_OBS = 24
DT = 0.05
N_PART = 4
D = 2
STEPS = 160


def simulate(pos0, vel0, mass, steps=STEPS, dt=DT, radius=0.1,
             restitution=0.9, softening=0.05, G=1.0, box=2.0):
    """Same integration loop as gen_nbody (house engine, compute don't
    memorise) — returns (qs, vs) with (steps+1, N, D)."""
    pos, vel = pos0.clone(), vel0.clone()
    pos, vel = reflect_in_box(pos, vel, -box, box)

    def accel_fn(p):
        return pairwise_gravity_local(p, mass, G=G, softening=softening)

    a = accel_fn(pos)
    qs, vs = [pos.clone()], [vel.clone()]
    for _ in range(steps):
        pos, vel, a = integrate_verlet(pos, vel, accel_fn, dt, accel=a)
        vel = resolve_sphere_collisions(pos, vel, radius=radius, mass=mass,
                                        restitution=restitution)
        pos, vel = reflect_in_box(pos, vel, -box, box)
        qs.append(pos.clone())
        vs.append(vel.clone())
    return torch.stack(qs), torch.stack(vs)          # (steps+1, N, D)


def pairwise_gravity_local(positions, mass, *, G=1.0, softening=0.05):
    """Local copy of the pairwise gravity kernel (physics_ops.pairwise_gravity
    signature) kept import-light: N small here, O(N^2) direct loop."""
    n = positions.shape[0]
    acc = torch.zeros_like(positions)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = positions[j] - positions[i]
            r2 = (d * d).sum() + softening * softening
            acc[i] += G * mass[j] * d / (r2 * r2.sqrt())
    return acc


def summary(qs, vs, t_obs=T_OBS):
    """Pooled channel input: per-step unweighted mean over particles
    (model.py:241 x.mean(dim=2)), flattened over the t_obs window."""
    return torch.cat([qs[:t_obs].mean(dim=1).reshape(-1),
                      vs[:t_obs].mean(dim=1).reshape(-1)])


def full_obs(qs, vs, t_obs=T_OBS):
    return torch.cat([qs[:t_obs].reshape(-1), vs[:t_obs].reshape(-1)])


def jacobian(sim_fn, mass, eps=0.01):
    """Central-difference Jacobian of a scalar-to-vector map w.r.t. each
    mass component."""
    s0 = sim_fn(mass)
    cols = []
    for i in range(mass.shape[0]):
        mp = mass.clone()
        mp[i] += eps
        mm = mass.clone()
        mm[i] -= eps
        cols.append((sim_fn(mp) - sim_fn(mm)) / (2 * eps))
    return torch.stack(cols, dim=1)                  # (dim_out, N)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_base", type=int, default=8)
    ap.add_argument("--eps", type=float, default=0.01)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/nbody_pool_audit")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, vs, masses = gen_nbody(args.n_base, STEPS, DT, N_PART, D,
                               generator=g)
    print(f"NBODY-POOL-AUDIT | N={N_PART} D={D} t_obs={T_OBS} "
          f"bases={args.n_base} eps={args.eps}", flush=True)

    fisher_pooled = torch.zeros(N_PART, N_PART)
    fisher_full = torch.zeros(N_PART, N_PART)
    finite = True
    for b in range(args.n_base):
        pos0, vel0 = qs[b, 0], vs[b, 0]

        def sim_pooled(m):
            q, v = simulate(pos0, vel0, m)
            return summary(q, v)

        def sim_full(m):
            q, v = simulate(pos0, vel0, m)
            return full_obs(q, v)

        jp = jacobian(sim_pooled, masses[b], args.eps)
        jf = jacobian(sim_full, masses[b], args.eps)
        finite = finite and bool(torch.isfinite(jp).all()) \
            and bool(torch.isfinite(jf).all())
        fisher_pooled += jp.T @ jp
        fisher_full += jf.T @ jf
        print(f"  [base {b}] |J_p| {jp.norm():.3e} |J_f| {jf.norm():.3e}",
              flush=True)

    # determinism self-check (pipeline sanity, prereg ①)
    q1, v1 = simulate(qs[0, 0], vs[0, 0], masses[0])
    q2, v2 = simulate(qs[0, 0], vs[0, 0], masses[0])
    deterministic = bool(torch.equal(q1, q2) and torch.equal(v1, v2))

    tp, tf = fisher_pooled.trace().item(), fisher_full.trace().item()
    retention = tp / tf if tf > 0 else float("nan")
    per_mass = (torch.diag(fisher_pooled)
                / torch.diag(fisher_full).clamp_min(1e-30)).tolist()
    results = {"retention_trace_ratio": retention,
               "fisher_pooled_trace": tp, "fisher_full_trace": tf,
               "retention_per_mass": per_mass,
               "finite_jacobians": finite,
               "deterministic_resim": deterministic}
    results["criteria"] = {
        "c1_pipeline_failed": bool(not finite or not deterministic
                                   or tf <= 0 or tp < 0),
        "c2_annihilation_recurred": bool(retention < 1e-3),
        "c3_pooled_above_full": bool(retention > 1.0),
    }
    verdict = "PASS" if not any(results["criteria"].values()) else "NEGATIVE"
    print(f"\nNBODY-POOL-AUDIT verdict {verdict} | retention "
          f"{retention:.4e} (per-mass {['%.2e' % x for x in per_mass]}) "
          f"| criteria {results['criteria']}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "nbody_pool_audit.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "nbody_pool_audit", "device": "cpu",
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
