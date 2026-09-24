"""
benchmarks/sharp_probe.py — SHARP-PROBE (round 154): sharpness-trajectory
probe on the M1 spring family.

Preregistered in PRD §19 round 154 BEFORE execution. Scan §37 (Cohen et
al. ICLR 2021 edge of stability, arXiv:2103.00065; Kalra et al. NeurIPS
2023 warmup mechanisms): training tends to run with the sharpness
(lambda_max of the loss Hessian) at ~2/learning-rate. This probe measures
lambda_max at checkpoints {0, 200, 500, 1000, 2000} of the standard
prefix training, via power iteration on Hessian-vector products (double
backward autograd) of the FIXED large-batch full-window loss (EOS
full-batch flavour: 128 trajectories, fixed window t0=0).

Mechanical verdict (preregistered):
  SHARP_UNRESOLVABLE — power iteration fails to converge (relative change
      of the Rayleigh quotient over the last 3 iterations > 10%) at any
      checkpoint, or lambda_max non-finite.
  SHARP_EOS   — lambda_max * lr in [1.5, 3] (threshold 2 +/- 50%).
  SHARP_BELOW — all lambda_max * lr < 1.5 (classical stable regime).
  SHARP_ABOVE — all lambda_max * lr > 3.
Trend reading (not gate-bearing): lambda_max direction across checkpoints
(rising / falling / flat), cf. EOS "rise and hover" vs warmup "early
high, then fall". Adam caveat recorded throughout (criterion derived for
GD).

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

from benchmarks.liquid_physics_eval import (  # noqa: E402
    rollout_mse_loss, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402
from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402

POWER_ITERS = 20       # preregistered: power-iteration steps per checkpoint
CONV_GATE = 0.10       # preregistered: last-3 relative change for convergence
EOS_LO, EOS_HI = 1.5, 3.0  # preregistered: lambda_max * lr window (2 +/- 50%)


def fixed_loss(model, qs, ps, t_obs, k_train, n_batch, t0=0):
    """Fixed large-batch full-window loss (the EOS full-batch flavour)."""
    q_obs = qs[:n_batch, t0:t0 + t_obs]
    p_obs = ps[:n_batch, t0:t0 + t_obs]
    fut = slice(t0 + t_obs - 1, t0 + t_obs + k_train)
    q_true = qs[:n_batch, fut]
    p_true = ps[:n_batch, fut]
    qs_pred, ps_pred, _ = model(q_obs, p_obs, k_train)
    return rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)


def lambda_max(model, qs, ps, t_obs, k_train, n_batch, iters, seed):
    """Power iteration for the largest Hessian eigenvalue via double
    backward. Returns (lam, converged, rel_change_last3)."""
    params = [p for p in model.parameters() if p.requires_grad]
    loss = fixed_loss(model, qs, ps, t_obs, k_train, n_batch)
    grads = torch.autograd.grad(loss, params, create_graph=True,
                                allow_unused=True)
    flat_g = torch.cat([(g.reshape(-1) if g is not None
                         else torch.zeros(p.numel(), device=next(
                             model.parameters()).device))
                        for g, p in zip(grads, params)])

    g_gen = torch.Generator().manual_seed(seed)
    v = torch.randn(flat_g.shape[0], generator=g_gen)
    v = v / v.norm()

    rays = []
    hv_fn = None
    for _ in range(iters):
        hv_grads = torch.autograd.grad(flat_g @ v, params,
                                       retain_graph=True, allow_unused=True)
        hv = torch.cat([(h.reshape(-1) if h is not None
                         else torch.zeros(p.numel(), device=flat_g.device))
                        for h, p in zip(hv_grads, params)])
        new_v = hv / hv.norm().clamp_min(1e-20)
        ray = (v @ hv).item()          # v^T H v
        rays.append(ray)
        v = new_v
        hv_fn = hv.norm().item()
    lam = rays[-1]
    tail = rays[-4:]
    denom = max(abs(tail[-1]), 1e-30)
    rel = max(abs(tail[i] - tail[i + 1]) / denom for i in range(len(tail) - 1))
    converged = math.isfinite(lam) and rel <= CONV_GATE and hv_fn > 0
    return lam, converged, rel


def classify_sharp(ratios, convs, eos_lo=EOS_LO, eos_hi=EOS_HI):
    """Preregistered round-154 verdict (pure, test-pinned). ratios =
    lambda_max * lr per checkpoint; convs = convergence flags."""
    if not all(convs):
        return "SHARP_UNRESOLVABLE", {
            "reason": "power iteration did not converge at some checkpoint "
                      "(preregistered negative branch)"}
    in_eos = [r for r in ratios if eos_lo <= r <= eos_hi]
    if in_eos:
        return "SHARP_EOS", {
            "eos_checkpoints": [i for i, r in enumerate(ratios)
                                if eos_lo <= r <= eos_hi],
            "criterion": f"lambda_max*lr in [{eos_lo},{eos_hi}] "
                         f"(threshold 2 +/- 50%) at >= 1 checkpoint"}
    if max(ratios) < eos_lo:
        return "SHARP_BELOW", {
            "criterion": f"all lambda_max*lr < {eos_lo}: classical "
                         f"stable regime"}
    return "SHARP_ABOVE", {
        "criterion": f"all lambda_max*lr > {eos_hi}: deep unstable "
                     f"regime"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_loss_batch", type=int, default=128,
                    help="fixed batch for the full-batch-flavour loss")
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--power_iters", type=int, default=POWER_ITERS)
    ap.add_argument("--checkpoints", default="0,200,500,1000,2000")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/sharp_probe")
    args = ap.parse_args()
    checkpoints = sorted(int(c) for c in args.checkpoints.split(","))

    g = torch.Generator().manual_seed(args.seed)
    pool_qs, pool_ps, _ = gen_spring(args.n_train, args.gen_steps,
                                     args.dt, 1, args.omega_lo,
                                     args.omega_hi, g, device=args.device)
    print(f"SHARP-PROBE | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} lr={args.lr} (Adam) checkpoints="
          f"{checkpoints} (seed {args.seed}, 1-seed screening; Adam caveat: "
          f"EOS criterion derived for GD)", flush=True)

    torch.manual_seed(args.seed)
    model = LiquidHamiltonianModel(1, d_model=args.d_model,
                                   context_dim=args.context_dim,
                                   n_scales=args.n_scales,
                                   hidden_dim=args.hidden, depth=2,
                                   dt=args.dt)

    rows = []
    trained = 0
    for ck in checkpoints:
        if ck > trained:
            train_prefix(model, pool_qs, pool_ps, args.t_obs, args.k_train,
                         ck - trained, args.lr, args.batch, args.seed)
            trained = ck
        lam, conv, rel = lambda_max(model, pool_qs, pool_ps, args.t_obs,
                                    args.k_train, args.n_loss_batch,
                                    args.power_iters, args.seed)
        ratio = lam * args.lr
        rows.append({"checkpoint_steps": ck, "lambda_max": lam,
                     "lambda_lr": ratio, "converged": conv,
                     "rel_change_last3": rel})
        print(f"  [ckpt {ck:>5}] lambda_max {lam:.4e} | lam*lr {ratio:.3f} "
              f"| converged {conv} (rel {rel:.2e})", flush=True)

    verdict, detail = classify_sharp([r["lambda_lr"] for r in rows],
                                     [r["converged"] for r in rows])
    lams = [r["lambda_max"] for r in rows]
    hi, lo = max(lams), min(lams)
    trend = ("rising" if hi / max(lo, 1e-30) >= 1.5 and lams[-1] > lams[0]
             else "falling" if lams[-1] < lams[0] else "flat")
    results = {
        "checkpoints": rows,
        "lr": args.lr,
        "verdict": verdict,
        "verdict_detail": detail,
        "trend_reading": trend,
        "criteria": {
            "c_unresolvable": verdict == "SHARP_UNRESOLVABLE",
            "c_eos": verdict == "SHARP_EOS",
            "c_below": verdict == "SHARP_BELOW",
            "c_above": verdict == "SHARP_ABOVE"},
        "gates": {"eos_lo": EOS_LO, "eos_hi": EOS_HI,
                  "conv_gate": CONV_GATE},
        "adam_caveat": "EOS threshold derived for full-batch GD; Adam "
                       "readings interpreted by magnitude only",
    }
    print(f"\nSHARP-PROBE verdict {verdict} | trend {trend} | "
          f"{detail.get('criterion', detail.get('reason', ''))}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "sharp_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "sharp_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
