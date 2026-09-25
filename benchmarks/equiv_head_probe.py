"""
benchmarks/equiv_head_probe.py — EQUIV-HEAD (round 249): homogeneous
kinetic-energy injection A/B, 3 seeds, on the M1 spring family (E1
calibre).

Preregistered in PRD §19 round 248 BEFORE execution (AMM-027 distill
routing, scan family 54: the round-244 AMP-ATTR verdict measured the
house dynamics head breaking the exact scaling equivariance of the
linear oscillator — head-equivariance error 1.362/2.838 at s=2/4 —
and the deconstructing-HNN literature coordinates the hard-structure
response). For the 1-dim spring the kinetic energy is PHYSICALLY KNOWN:
T = ½ Σ p². Arm B injects it analytically (dV/dq from a learned
V_θ(q|ctx), dT/dp = p exact), removing the T-MLP as a source of
homogeneity violation; arm A is the house default (T,V free MLPs).

Arms: A = house default head; B = AnalyticTHead (subclass, dT_dp = p,
energy = V only). Both trained on the standard scale=1 pool, 2000
steps, house prefix train (sentinel: A seed 0 eval = 3.5581917762756348
bit-for-bit). B carries the now-unused T-MLP parameters (receive no
gradient; capacity note recorded).

Dual readings:
  in-dist — house evaluate at eval_k=100 on the canonical pool;
            ratio = mean_MSE_B / mean_MSE_A (AMM-028 gate-3 3-seed).
  scale   — round-216 amplitude-extrapolation caliber: held-out pools
            with initial conditions scaled by s ∈ {2, 4} (local
            gen_spring_scaled, verbatim round-216 math), rel_mse =
            MSE / mean(true²), rel_comp = rel(s=4)/rel(s=1) per arm.

Mechanical verdict (preregistered, 3-seed):
  EQUIV_ARM_DIVERGED (negative) — any reading non-finite or rollout
      > 1e6
  EQUIV_RESOLVED   — 0.95 <= ratio <= 1.05 AND median rel_comp_B < 3
      (round-216 gate): homogeneous injection = free equivariance;
      decision = architecture-line candidate (escape-door-style [B]
      upgrade)
  EQUIV_TRADEOFF   — ratio < 0.95 or > 1.05 (B materially better or
      worse in-distribution): recorded trade-off, decision = limitation
      documentation either way
  EQUIV_ATTRIB     — 0.95 <= ratio <= 1.05 but rel_comp_B >= 3:
      the equivariance gap is not in T; attribution redirects to V or
      the integrator

Decision coupling (AMM-028 gate-1): the three non-negative outcomes
route the architecture line differently (candidate upgrade / limitation
record / attribution redirect). Family boundary: scan family 54 round
1 — distinct from the R1b T-even line (time-reversal symmetry) and
from the escape-door validation line (this injects a NEW structure).
Wording clause r242: no foreign queue-anchor literals. Results JSON
follows the audit schema (top-level "results" key); meta carries
exec_tier from probe_run.
"""

import argparse
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.hamiltonian import HamiltonianHead  # noqa: E402
from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

NORM_CAP = 1e6      # preregistered: divergence threshold
LO_GATE = 0.95      # preregistered: in-dist parity band
HI_GATE = 1.05
REL_GATE = 3.0      # preregistered: round-216 rel_comp gate
SEEDS = (0, 1, 2)
SENTINEL = 3.5581917762756348  # house default arm A seed 0


class AnalyticTHead(HamiltonianHead):
    """T(p) = ½ Σ p² analytic (exact for the unit-mass spring);
    V(q|ctx) stays learned. dT_dp = p by construction, so the T side of
    the integrator is exactly scaling-equivariant. The inherited T-MLP
    parameters stay in the module but receive no gradient."""

    def dT_dp(self, p):
        return p

    def energy(self, q, p, context=None):
        lead = q.shape[:-1]
        qf = q.reshape(-1, q.shape[-1])
        if context is not None:
            k = qf.shape[0] // context.shape[0]
            v_in = torch.cat([qf, context.repeat(k, 1)], dim=-1)
        else:
            v_in = qf
        return self.V(v_in).squeeze(-1).reshape(lead)


def gen_spring_scaled(n_traj, steps, dt, omega_lo, omega_hi, g, scale,
                      device="cpu"):
    """Verbatim round-216 math: q0/p0 drawn from N(0, scale)."""
    omega = omega_lo + (omega_hi - omega_lo) * torch.rand(
        n_traj, generator=g, device=device)
    q0 = torch.randn(n_traj, 1, generator=g, device=device) * scale
    p0 = torch.randn(n_traj, 1, generator=g, device=device) * scale
    t = torch.arange(steps + 1, dtype=torch.float32, device=device) * dt
    wt = omega.view(-1, 1) * t.view(1, -1)
    c, s = torch.cos(wt).unsqueeze(-1), torch.sin(wt).unsqueeze(-1)
    w = omega.view(-1, 1, 1)
    qs = q0.unsqueeze(1) * c + (p0.unsqueeze(1) / w) * s
    ps = -q0.unsqueeze(1) * w * s + p0.unsqueeze(1) * c
    return qs, ps, omega


def rel_mse_scaled(model, qs, ps, t_obs, eval_k, dt):
    """Round-216 caliber: rollout MSE over mean true signal energy."""
    model.eval()
    q_obs = qs[:, :t_obs]
    p_obs = ps[:, :t_obs]
    fut = slice(t_obs - 1, t_obs + eval_k)
    q_true = qs[:, fut].permute(1, 0, 2)
    p_true = ps[:, fut].permute(1, 0, 2)
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    mse = ((qs_pred - q_true) ** 2 + (ps_pred - p_true) ** 2).mean().item()
    signal = (q_true ** 2 + p_true ** 2).mean().item()
    rel = mse / max(signal, 1e-30)
    return {"mse": mse, "rel_mse": rel,
            "finite": bool(math.isfinite(mse) and math.isfinite(rel)
                           and mse <= NORM_CAP)}


def median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def classify_equiv(mses_a, mses_b, comps_a, comps_b,
                   lo_gate: float = LO_GATE, hi_gate: float = HI_GATE,
                   rel_gate: float = REL_GATE):
    """Preregistered round-248 verdict (pure, test-pinned).

    mses_*: in-dist rollout MSE per seed; comps_*: rel_comp (s4/s1)
    per seed. Verdict on the 3-seed mean ratio and the median rel_comp.
    """
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > NORM_CAP:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "EQUIV_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} (mse={m:.3e})"}
    mean_a = sum(mses_a) / len(mses_a)
    mean_b = sum(mses_b) / len(mses_b)
    ratio = mean_b / max(mean_a, 1e-30)
    med_ca = median(comps_a)
    med_cb = median(comps_b)
    stats = {"ratio": ratio, "mean_A": mean_a, "mean_B": mean_b,
             "mses_A": mses_a, "mses_B": mses_b,
             "rel_comp_A": comps_a, "rel_comp_B": comps_b,
             "rel_comp_median_A": med_ca, "rel_comp_median_B": med_cb,
             "consistent": sum(1 for a, b in zip(mses_a, mses_b)
                               if b < a)}
    if lo_gate <= ratio <= hi_gate and med_cb < rel_gate:
        verdict = "EQUIV_RESOLVED"
        stats["decision"] = ("homogeneous injection = free equivariance: "
                             "in-dist parity and scale extrapolation "
                             "repaired; architecture-line candidate "
                             "(escape-door-style [B] upgrade)")
    elif not (lo_gate <= ratio <= hi_gate):
        verdict = "EQUIV_TRADEOFF"
        stats["decision"] = ("in-distribution materially changed by the "
                             "analytic T: recorded trade-off (hard "
                             "structure vs fit)")
    else:
        verdict = "EQUIV_ATTRIB"
        stats["decision"] = ("in-dist parity but extrapolation not "
                             "repaired: the equivariance gap is not in "
                             "T; attribution redirects to V or the "
                             "integrator")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--scales", default="1,2,4")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/equiv_head")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    scales = [float(x) for x in args.scales.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    scale_pools = {}
    for s in scales:
        gs = torch.Generator().manual_seed(0)
        qs_s, ps_s, _ = gen_spring_scaled(args.n_eval, args.gen_steps,
                                          args.dt, args.omega_lo,
                                          args.omega_hi, gs, scale=s,
                                          device=args.device)
        scale_pools[s] = (qs_s, ps_s)
    print(f"EQUIV-HEAD | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} A=default vs B=analyticT "
          f"(seeds {seeds}; in-dist+scale rel_comp; round-248 "
          f"preregistration)", flush=True)

    arms = {"A": {"mses": [], "comps": []},
            "B": {"mses": [], "comps": []}}
    for seed in seeds:
        for tag, analytic_t in (("A", False), ("B", True)):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            if analytic_t:
                model.ham = AnalyticTHead(
                    1, hidden_dim=args.hidden, depth=2,
                    context_dim=args.context_dim)
            train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                         args.train_steps, args.lr, args.batch, seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            rels = {}
            for s in scales:
                qs_s, ps_s = scale_pools[s]
                r = rel_mse_scaled(model, qs_s, ps_s, args.t_obs,
                                   args.eval_k, args.dt)
                rels[s] = r["rel_mse"]
            comp = rels[scales[-1]] / max(rels[1.0], 1e-30)
            arms[tag]["mses"].append(res["rollout_mse"])
            arms[tag]["comps"].append(comp)
            print(f"  [arm {tag} seed {seed}] MSE "
                  f"{res['rollout_mse']:.4e} | rel_comp "
                  f"{comp:.3f}", flush=True)

    verdict, detail = classify_equiv(arms["A"]["mses"], arms["B"]["mses"],
                                     arms["A"]["comps"],
                                     arms["B"]["comps"])
    sentinels = {"A_seed0": {"expected": SENTINEL,
                             "actual": arms["A"]["mses"][0],
                             "bitwise_match":
                                 arms["A"]["mses"][0] == SENTINEL}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "EQUIV_ARM_DIVERGED",
                     "c_resolved": verdict == "EQUIV_RESOLVED",
                     "c_tradeoff": verdict == "EQUIV_TRADEOFF",
                     "c_attrib": verdict == "EQUIV_ATTRIB"},
        "gates": {"lo_gate": LO_GATE, "hi_gate": HI_GATE,
                  "rel_gate": REL_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "scales": scales},
        "anchor": "A seed 0 = 3.5582 (house default sentinel, rounds "
                  "175/191/223/226 + RECIPE + r237-r246 probes)"},
    print(f"\nEQUIV-HEAD verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinel={sentinels['A_seed0']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "equiv_head.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "equiv_head_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
