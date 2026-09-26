"""
benchmarks/hom_bound_probe.py — HOM-BOUND (round 271): the expressivity
boundary of the homogeneous-V constraint, measured on a NEW quartic
oscillator pool (pure degree-4 truth), 3 seeds. Scan family 59
(constraint-expressivity boundary family, round-271 distillation; slot
1 = Dym & Maron ICLR 2021 approximation power of constrained
architectures, slot 2 = Finkelshtein et al. ICML 2022 universal-by-
construction, slot 3 = Chen et al. 2021 arXiv:2102.11923 misspecified-
model readouts).

Why this pool: the round-268/269 candidate V = ‖q‖²·s_θ(0, ctx) is
degree-2 homogeneous — exact for the harmonic pool (AMM-033 evidence
chain) and structurally BIASED for a quartic truth. A pure quartic
oscillator (H = p²/2 + q⁴/4, separable, velocity-Verlet ground truth)
isolates the DEGREE axis of the constraint: three arms share the
analytic T = ½Σp² (round-249 lineage) and differ ONLY in the V form —
  arm A  = V free MLP (universal; reference baseline);
  arm B  = V = ‖q‖²·s_θ(0, ctx)  (degree-2 homogeneous: CANNOT
           represent q⁴/4 — misspecification expected);
  arm C  = V = ‖q‖⁴·s_θ(0, ctx)  (degree-4 homogeneous: represents
           q⁴/4 exactly with s = 1/4 — degree-matched).
All arms keep ctx (per-trajectory energy/phase) inside s via the same
input width (zeroed direction block, no extra parameter draws — the
round-268 construction discipline).

Readings: in-dist rollout MSE (k=100, house evaluate).

Mechanical verdict (preregistered, 3-seed; parity band ±5% = house
round-260 gates):
  HOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  r2 = mean MSE_B / mean MSE_A; r4 = mean MSE_C / mean MSE_A
  HOM_BOUND_DEGREE_MATCHED — r4 < 1.05 AND r2 > 1.05: the boundary is
      the degree axis; a degree-matched homogeneous V is free (or
      better) while the wrong degree pays ⇒ AMM-033 scope note
      upgraded with a measured extension path (degree-matched recipe)
  HOM_BOUND_ALL_TOLERANT — r4 < 1.05 AND r2 <= 1.05: no measurable
      bias even with the wrong degree at this scale ⇒ honest void
  HOM_BOUND_MEASURED — r4 >= 1.05: even the degree-matched constraint
      pays on an anharmonic pool ⇒ boundary real; AMM-033 stays
      strictly spring-line (measured)

Decision coupling (AMM-028 gate-1): each outcome changes the AMM-033
scope annotation differently (measured extension / void / measured
boundary), EIG qualified. Sentinel honesty: NEW pool ⇒ no historical
bitwise anchors exist (round-257 clause) — arm A is the reference
baseline and this run's readings become the pool's future anchors.
Family boundary: scan family 59 round 1. Results JSON follows the
audit schema; meta carries exec_tier.
"""

import argparse
import json
import math
import os
import sys

import torch
import torch.nn as nn

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.equiv_head_probe import AnalyticTHead  # noqa: E402
from benchmarks.liquid_physics_eval import (  # noqa: E402
    rollout_mse_loss, train as train_prefix)
from benchmarks.v_hom_stab_probe import HomVStabHead  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6   # preregistered: divergence threshold (house caliber)
PARITY = 1.05    # preregistered: house parity band (round-260 gate)
SEEDS = (0, 1, 2)


def gen_quartic(n_traj: int, steps: int, dt: float,
                generator: torch.Generator, device: str = "cpu"):
    """Pure quartic oscillator, separable H = p²/2 + q⁴/4 (dim=1).
    Force a(q) = −q³; velocity-Verlet ground truth (house caliber for
    separable systems). Returns (qs, ps), each (n, steps+1, 1)."""
    q0 = torch.randn(n_traj, 1, generator=generator, device=device) * 0.5
    p0 = torch.randn(n_traj, 1, generator=generator, device=device) * 0.5
    qs, ps = [q0.clone()], [p0.clone()]
    q, p = q0.clone(), p0.clone()

    def accel(q_):
        return -(q_ ** 3)

    for _ in range(steps):
        p = p + 0.5 * dt * accel(q)
        q = q + dt * p
        p = p + 0.5 * dt * accel(q)
        qs.append(q.clone())
        ps.append(p.clone())
    return torch.stack(qs, dim=1), torch.stack(ps, dim=1)


class HomPowerV(nn.Module):
    """V(q, ctx) = ‖q‖^(2·deg) · s(0, ctx): degree-`deg` homogeneous
    with the direction channel zeroed (round-268 discipline: input
    width unchanged, no extra parameter draws, q=0 continuity by
    construction). deg=1 reproduces QuadraticDirectionFree; deg=2 is
    degree-4 homogeneous and represents the pure quartic truth
    q⁴/4 exactly with s = 1/4."""

    def __init__(self, inner: nn.Module, dim: int, degree: int):
        super().__init__()
        self.inner = inner
        self.dim = dim
        self.degree = degree

    def forward(self, v_in: torch.Tensor) -> torch.Tensor:
        q = v_in[..., :self.dim]
        nq = q.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        zeros = torch.zeros_like(q)
        feats = torch.cat([zeros, v_in[..., self.dim:]], dim=-1)
        return (nq ** (2 * self.degree)) * self.inner(feats)


class HomPowerHead(AnalyticTHead):
    """Analytic T + degree-`deg` homogeneous direction-free V."""

    def __init__(self, degree: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.V = HomPowerV(self.V, self.dim, degree)


def eval_rollout_mse(model, qs, ps, t_obs, eval_k, dt):
    """House-caliber rollout MSE on the quartic pool. The house
    evaluate() is spring-specific (energy drift and the AMM-031 band
    need a per-trajectory omega); this mirrors its MSE path exactly
    (same prefix slicing + rollout_mse_loss) and adds the quartic
    energy drift H = p²/2 + q⁴/4 as an informational reading."""
    model.eval()
    q_obs = qs[:, :t_obs]
    p_obs = ps[:, :t_obs]
    fut = slice(t_obs - 1, t_obs + eval_k)
    q_true = qs[:, fut]
    p_true = ps[:, fut]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    mse = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true).item()
    e = 0.5 * ps_pred ** 2 + 0.25 * qs_pred ** 4          # (k+1, B, 1)
    e = e.squeeze(-1).mean(-1)                             # (k+1,)
    e0 = e[0].abs().clamp_min(1e-6)
    drift = ((e - e[0]).abs() / e0).mean().item()
    return {"rollout_mse": mse, "quartic_energy_drift_mean": drift}


def classify_hom_bound(mses_a, mses_b, mses_c,
                       parity: float = PARITY,
                       norm_cap: float = NORM_CAP):
    """Preregistered round-271 verdict (pure, test-pinned). A = free V,
    B = degree-2 homogeneous, C = degree-4 homogeneous."""
    for tag, vals in (("A", mses_a), ("B", mses_b), ("C", mses_c)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > norm_cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "HOM_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} (mse={m:.3e})"}
    mean = {k: sum(v) / len(v) for k, v in
            (("A", mses_a), ("B", mses_b), ("C", mses_c))}
    r2 = mean["B"] / max(mean["A"], 1e-30)
    r4 = mean["C"] / max(mean["A"], 1e-30)
    stats = {"parity": parity, "mean_A": mean["A"], "mean_B": mean["B"],
             "mean_C": mean["C"], "r2": r2, "r4": r4,
             "mses_A": mses_a, "mses_B": mses_b, "mses_C": mses_c,
             "consistent_C": sum(1 for a, c in zip(mses_a, mses_c)
                                 if c < a)}
    if r4 < parity and r2 > parity:
        verdict = "HOM_BOUND_DEGREE_MATCHED"
        stats["decision"] = ("boundary is the degree axis: degree-matched "
                             "homogeneous V is free (or better) while the "
                             "wrong degree pays; AMM-033 scope note "
                             "upgraded with a measured extension path")
    elif r4 < parity:
        verdict = "HOM_BOUND_ALL_TOLERANT"
        stats["decision"] = ("no measurable bias even with the wrong "
                             "degree at this scale: honest void")
    else:
        verdict = "HOM_BOUND_MEASURED"
        stats["decision"] = ("even the degree-matched constraint pays on "
                             "an anharmonic pool: boundary real, AMM-033 "
                             "stays strictly spring-line (measured)")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/hom_bound")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps = gen_quartic(args.n_train + args.n_eval, args.gen_steps,
                         args.dt, g, device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"HOM-BOUND | quartic pool H=p²/2+q⁴/4 dt={args.dt} "
          f"hidden={args.hidden} steps={args.train_steps} all-analyticT:"
          f" A=V-free vs B=‖q‖²·s vs C=‖q‖⁴·s (seeds {seeds}; round-271 "
          f"preregistration, scan family 59)", flush=True)

    arms = {k: [] for k in ("A", "B", "C")}
    heads = {"A": lambda: AnalyticTHead(1, hidden_dim=args.hidden,
                                        depth=2,
                                        context_dim=args.context_dim),
             "B": lambda: HomVStabHead(1, hidden_dim=args.hidden,
                                       depth=2,
                                       context_dim=args.context_dim),
             "C": lambda: HomPowerHead(2, 1, hidden_dim=args.hidden,
                                       depth=2,
                                       context_dim=args.context_dim)}
    for seed in seeds:
        for tag in ("A", "B", "C"):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            # head swap AFTER the model draw (round-249/268 construction
            # order); single variable = the V form (all analytic T)
            model.ham = heads[tag]()
            train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                         args.train_steps, args.lr, args.batch, seed)
            res = eval_rollout_mse(model, qs[ev], ps[ev], args.t_obs,
                                   args.eval_k, args.dt)
            arms[tag].append(res["rollout_mse"])
            print(f"  [arm {tag} seed {seed}] MSE "
                  f"{res['rollout_mse']:.4e} | E-drift "
                  f"{res['quartic_energy_drift_mean']:.4f}", flush=True)

    verdict, detail = classify_hom_bound(arms["A"], arms["B"], arms["C"])
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": {"pool": "quartic H=p²/2+q⁴/4 is NEW — no historical "
                              "bitwise anchors (round-257 clause); arm A "
                              "is the reference baseline and this run's "
                              "readings become the pool's future anchors",
                      "anchor_readings": {"A": arms["A"], "B": arms["B"],
                                          "C": arms["C"]}},
        "criteria": {"c_diverged": verdict == "HOM_ARM_DIVERGED",
                     "c_degree_matched":
                         verdict == "HOM_BOUND_DEGREE_MATCHED",
                     "c_all_tolerant": verdict == "HOM_BOUND_ALL_TOLERANT",
                     "c_measured": verdict == "HOM_BOUND_MEASURED"},
        "gates": {"parity": PARITY, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS)},
        "anchor": "all arms analytic T = ½Σp²; single variable = V form "
                  "(free / degree-2 hom / degree-4 hom)",
    }
    print(f"\nHOM-BOUND verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "hom_bound.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "hom_bound_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
