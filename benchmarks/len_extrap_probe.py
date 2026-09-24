"""
benchmarks/len_extrap_probe.py — LEN-EXTRAP (round 170): rollout
generalization BEYOND the training physical window.

Preregistered in PRD §19 round 170 BEFORE execution. Scan §41 (Zhu et al.
ICML 2022 IMDE: learned maps carry dt-specific correction terms whose
validity outside the training window is untested; Li et al. arXiv:2511.
06609 long-horizon error accumulation): the house default trains on
160-step trajectories (16 s physical window) and evaluates at k=100
(10 s) — behaviour beyond 16 s has never been measured.

Design: train the E1-calibre prefix model (hidden64, omega in
[0.7,1.8], 2000 steps) on the standard 160-step pool; then generate a
FRESH 601-step (60 s) pool with the same omega distribution and roll
out each held-out trajectory ONCE for 600 steps, building the per-step
MSE profile. Segments (preregistered):
  interpolated  T in [5, 10] s   (inside the training window)
  extrapolated  T in [20, 30] s  (1.25-1.875x beyond the window)
  edge window   T in [16, 20] s; tail window T in [10, 16] s
comp = mean per-step MSE(extrapolated)/mean(per-step MSE, interpolated).

Mechanical verdict (preregistered):
  LEN_DIVERGENT (negative)  — rollout non-finite or q-norm > 1e6
      (extrapolation collapse is itself information, recorded as such)
  LEN_ROBUST      — comp < 3
  LEN_WINDOW_EDGE — comp >= 3 AND edge/tail window jump >= 3x
  LEN_GRADUAL     — comp >= 3 without the boundary jump

1-seed screening tier; multi-seed finals PARKED per AMM-024. Results
JSON follows the audit schema (top-level "results" key); meta carries
exec_tier passthrough from probe_run.
"""

import argparse
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.liquid_physics_eval import (  # noqa: E402
    train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

COMP_GATE = 3.0    # preregistered: extrapolated/interpolated per-step ratio
EDGE_GATE = 3.0    # preregistered: boundary-window jump for WINDOW_EDGE
NORM_CAP = 1e6     # preregistered: divergence threshold
WINDOW_STEPS = 160  # house default training trajectory length (16 s at dt=0.1)
DT = 0.1


def per_step_mse(qs_pred: torch.Tensor, ps_pred: torch.Tensor,
                 q_true: torch.Tensor, p_true: torch.Tensor):
    """Per-step (k,) MSE profile. qs_pred: (k+1, B, dim); true same."""
    return ((qs_pred - q_true) ** 2).mean(dim=(1, 2)) \
         + ((ps_pred - p_true) ** 2).mean(dim=(1, 2))


def classify_len(comp: float, edge_jump: float,
                 comp_gate: float = COMP_GATE,
                 edge_gate: float = EDGE_GATE):
    """Preregistered round-170 verdict (pure, test-pinned)."""
    if not math.isfinite(comp) or comp < 0:
        return "LEN_DIVERGENT", {
            "reason": f"comp={comp} non-finite or negative: preregistered "
                      f"negative branch"}
    if comp < comp_gate:
        return "LEN_ROBUST", {
            "comp": comp,
            "criterion": f"comp {comp:.2f} < {comp_gate}: extrapolated "
                         f"per-step error comparable to interpolated — "
                         f"smooth extrapolation"}
    if edge_jump >= edge_gate:
        return "LEN_WINDOW_EDGE", {
            "comp": comp, "edge_jump": edge_jump,
            "criterion": f"comp {comp:.2f} >= {comp_gate} with boundary "
                         f"jump {edge_jump:.1f}x: training-window edge "
                         f"effect (IMDE correction-term failure)"}
    return "LEN_GRADUAL", {
        "comp": comp, "edge_jump": edge_jump,
        "criterion": f"comp {comp:.2f} >= {comp_gate} without boundary "
                     f"jump: gradual error accumulation"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--eval_steps", type=int, default=601,
                    help="fresh-pool trajectory length (60 s at dt=0.1)")
    ap.add_argument("--rollout_k", type=int, default=600)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/len_extrap")
    args = ap.parse_args()

    # training pool: house default 160-step trajectories (16 s window)
    g = torch.Generator().manual_seed(args.seed)
    qs_tr, ps_tr, _ = gen_spring(args.n_train, WINDOW_STEPS, DT, 1,
                                 args.omega_lo, args.omega_hi, g,
                                 device=args.device)
    # fresh evaluation pool: SAME omega distribution, 60 s trajectories
    g = torch.Generator().manual_seed(args.seed)
    qs_ev, ps_ev, om_ev = gen_spring(args.n_eval, args.eval_steps, DT, 1,
                                     args.omega_lo, args.omega_hi, g,
                                     device=args.device)
    print(f"LEN-EXTRAP | omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} train window {WINDOW_STEPS} steps "
          f"(16 s) | eval {args.eval_steps} steps (60 s), rollout k="
          f"{args.rollout_k} (seed {args.seed}, 1-seed screening)",
          flush=True)

    torch.manual_seed(args.seed)
    model = LiquidHamiltonianModel(
        1, d_model=args.d_model, context_dim=args.context_dim,
        n_scales=args.n_scales, hidden_dim=args.hidden, depth=2, dt=DT)
    train_prefix(model, qs_tr, ps_tr, args.t_obs, args.k_train,
                 args.train_steps, args.lr, args.batch, args.seed)

    model.eval()
    q_obs = qs_ev[:, :args.t_obs]
    p_obs = ps_ev[:, :args.t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, args.rollout_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs_ev[:, :args.rollout_k + 1].permute(1, 0, 2)
    p_true = ps_ev[:, :args.rollout_k + 1].permute(1, 0, 2)
    profile = per_step_mse(qs_pred, ps_pred, q_true, p_true)  # (k+1,)
    qnorm = qs_pred.norm().item()

    # energy-drift diagnostic (§41.2 statistic preservation): predicted
    # trajectory energy vs its own initial value, per step, true omega
    kin = 0.5 * (ps_pred ** 2).sum(-1)                       # (k+1, B)
    r = qs_pred.norm(dim=-1)
    pot = 0.5 * 100.0 * (r - 1.0) ** 2 + om_ev.T            # gravity g*y
    E = kin + pot                                            # (k+1, B)
    e_scale = E.abs().mean().clamp_min(1e-6)
    energy_drift = ((E - E[:1]) / e_scale).max().item()

    def seg(a, b):  # seconds inclusive -> step slice (k index = T/dt)
        return profile[int(a / DT):int(b / DT) + 1].mean().item()

    interp = seg(5, 10)
    extrap = seg(20, 30)
    tail = seg(10, 16)
    edge = seg(16, 20)
    comp = extrap / max(interp, 1e-30)
    edge_jump = edge / max(tail, 1e-30)
    print(f"  per-step MSE: interp[5,10]s {interp:.4e} | "
          f"extrap[20,30]s {extrap:.4e} | comp {comp:.2f} | "
          f"edge/tail jump {edge_jump:.2f} | E-drift {energy_drift:.2f}",
          flush=True)

    verdict, detail = classify_len(comp, edge_jump)
    results = {
        "per_step_profile_head": profile[:21].tolist(),
        "segments": {"interp_5_10s": interp, "extrap_20_30s": extrap,
                     "tail_10_16s": tail, "edge_16_20s": edge},
        "comp": comp, "edge_jump": edge_jump,
        "rollout_qnorm": qnorm,
        "energy_drift_max": energy_drift,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_divergent": verdict == "LEN_DIVERGENT",
            "c_robust": verdict == "LEN_ROBUST",
            "c_window_edge": verdict == "LEN_WINDOW_EDGE",
            "c_gradual": verdict == "LEN_GRADUAL"},
        "gates": {"comp_gate": COMP_GATE, "edge_gate": EDGE_GATE,
                  "norm_cap": NORM_CAP},
        "window_note": f"training window = {WINDOW_STEPS} steps = "
                       f"{WINDOW_STEPS * DT:.0f} s; extrapolated segment "
                       f"lies 1.25-1.875x beyond it",
    }
    print(f"\nLEN-EXTRAP verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "len_extrap.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "len_extrap_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
