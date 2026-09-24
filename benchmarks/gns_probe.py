"""
benchmarks/gns_probe.py — GNS-PROBE (round 149): closed-form gradient-noise
scale estimate on the M1 spring family.

Preregistered in PRD §19 round 149 BEFORE execution. Scan §36 (McCandlish
et al. 2018, arXiv:1812.06162) defines the gradient noise scale
B_noise = tr(G)/|ḡ|² — the batch size at which linear speedup from
averaging breaks down. This probe estimates the one-sample-flavour
B_simple with N=32 random batch-64 gradients at three training-progress
checkpoints (0 / 1000 / 4000 steps of the standard prefix loop), using
the SAME loss construction as training (random-window rollout MSE).

First-order estimator (McCandlish §2 flavour): the per-batch gradient
g_i has covariance G/b, so tr(G) ≈ b/(N-1) · Σ_i |g_i − ĝ|² and
    B_simple = tr(G) / |ĝ|².

Preregistered mechanical verdict:
  GNS_UNRESOLVABLE (negative branch) — any checkpoint has |ĝ|² < 1e-16
      (zero mean gradient: the ratio diverges and carries no meaning)
      or a non-finite B_simple.
  GNS_RESOLVED_TREND — max/min B_simple across checkpoints >= 3x
      (trend reportable: growing/shrinking, cf. the "grows during
      training" prediction).
  GNS_FLAT — max/min < 3x: trend not resolvable (recorded as such),
      but the magnitude reading stands (where batch=64 sits).

1-seed screening tier; multi-seed finals PARKED per AMM-024. Results
JSON follows the audit schema (top-level "results" key); meta carries
exec_tier passthrough from probe_run.
"""

import argparse
import json
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

GRAD_SAMPLES = 32       # preregistered: N random batch gradients per checkpoint
ZERO_GNORM_FLOOR = 1e-16  # preregistered: |ĝ|² below this => ratio meaningless
TREND_GATE = 3.0        # preregistered: max/min across checkpoints for a trend


def sample_grads(model, qs, ps, t_obs, k_train, batch, n_samples, seed):
    """N gradients of the training loss (same window construction as
    train_prefix) at random batch-64 slices, flattened to (N, P)."""
    g = torch.Generator().manual_seed(seed)
    N, S = qs.shape[0], qs.shape[1]
    model.train()
    grads = []
    for _ in range(n_samples):
        bi = torch.randint(0, N, (batch,), generator=g)
        t0 = torch.randint(0, S - t_obs - k_train, (1,), generator=g).item()
        q_obs = qs[bi, t0:t0 + t_obs]
        p_obs = ps[bi, t0:t0 + t_obs]
        fut = slice(t0 + t_obs - 1, t0 + t_obs + k_train)
        q_true = qs[bi, fut]
        p_true = ps[bi, fut]
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k_train)
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        model.zero_grad(set_to_none=True)
        loss.backward()
        flat = torch.cat([p.grad.detach().reshape(-1)
                          for p in model.parameters()
                          if p.grad is not None])
        grads.append(flat)
    model.zero_grad(set_to_none=True)
    return torch.stack(grads)


def b_simple(grads: torch.Tensor, batch: int):
    """Preregistered first-order estimator (pure, test-pinned).

    tr(G) ≈ b/(N-1) · Σ_i |g_i − ĝ|² ;  B_simple = tr(G)/|ĝ|².
    Returns (b_simple, gnorm_sq, tr_G); gnorm_sq is returned so the
    caller can apply the zero-gradient preregistered guard."""
    gbar = grads.mean(0)
    dev = grads - gbar
    n = grads.shape[0]
    gnorm_sq = gbar.pow(2).sum().item()
    tr_g = batch / (n - 1) * dev.pow(2).sum().item()
    bs = tr_g / gnorm_sq if gnorm_sq > 0 else float("inf")
    return bs, gnorm_sq, tr_g


def classify_gns(checkpoints, gnorm_sqs, b_simples,
                 zero_floor: float = ZERO_GNORM_FLOOR,
                 trend_gate: float = TREND_GATE):
    """Preregistered round-149 verdict (pure, test-pinned)."""
    for c, gn in zip(checkpoints, gnorm_sqs):
        if gn < zero_floor:
            return "GNS_UNRESOLVABLE", {
                "reason": f"checkpoint {c} has |ĝ|² < {zero_floor}: "
                          f"mean gradient vanished, ratio carries no "
                          f"meaning (preregistered negative branch)"}
    if not all(bs > 0 and bs == bs and bs != float("inf")
               and bs != float("-inf") for bs in b_simples):
        return "GNS_UNRESOLVABLE", {
            "reason": "non-finite B_simple at some checkpoint "
                      "(preregistered negative branch)"}
    ratio = max(b_simples) / max(min(b_simples), 1e-30)
    regime = ("linear-speedup (signal-dominated)" if min(b_simples) >= 64
              else "noise-dominated")
    if ratio >= trend_gate:
        trend = "growing" if b_simples[-1] > b_simples[0] else "shrinking"
        return "GNS_RESOLVED_TREND", {
            "trend": trend, "max_min_ratio": ratio,
            "regime_at_64": regime,
            "criterion": f"max/min B_simple >= {trend_gate}"}
    return "GNS_FLAT", {
        "max_min_ratio": ratio, "regime_at_64": regime,
        "criterion": f"max/min B_simple < {trend_gate}: trend not "
                     f"resolvable at screening tier; magnitude reading "
                     f"stands"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
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
    ap.add_argument("--grad_samples", type=int, default=GRAD_SAMPLES)
    ap.add_argument("--checkpoints", default="0,1000,4000")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/gns_probe")
    ap.add_argument("--out_name", default="gns_probe.json",
                    help="round-151 (GNS-PROBE-2) writes its own filename "
                         "on the stacked branch; v1 default unchanged")
    args = ap.parse_args()
    checkpoints = sorted(int(c) for c in args.checkpoints.split(","))

    g = torch.Generator().manual_seed(args.seed)
    pool_qs, pool_ps, _ = gen_spring(args.n_train, args.gen_steps,
                                     args.dt, 1, args.omega_lo,
                                     args.omega_hi, g, device=args.device)
    print(f"GNS-PROBE | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} batch={args.batch} N={args.grad_samples} "
          f"checkpoints={checkpoints} (seed {args.seed}, 1-seed screening)",
          flush=True)

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
        grads = sample_grads(model, pool_qs, pool_ps, args.t_obs,
                             args.k_train, args.batch, args.grad_samples,
                             args.seed)
        bs, gnorm_sq, tr_g = b_simple(grads, args.batch)
        rows.append({"checkpoint_steps": ck, "b_simple": bs,
                     "gnorm_sq": gnorm_sq, "tr_g": tr_g})
        print(f"  [ckpt {ck:>5}] B_simple {bs:.3e} | |ĝ|² {gnorm_sq:.3e} "
              f"| tr(G) {tr_g:.3e}", flush=True)

    verdict, detail = classify_gns([r["checkpoint_steps"] for r in rows],
                                   [r["gnorm_sq"] for r in rows],
                                   [r["b_simple"] for r in rows])
    results = {
        "checkpoints": rows,
        "batch": args.batch,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "GNS_UNRESOLVABLE",
            "c_trend_resolved": verdict == "GNS_RESOLVED_TREND",
            "c_flat_trend_only": verdict == "GNS_FLAT"},
        "gates": {"zero_gnorm_floor": ZERO_GNORM_FLOOR,
                  "trend_gate": TREND_GATE},
    }
    print(f"\nGNS-PROBE verdict {verdict} | {detail.get('criterion', '')}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, args.out_name), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "gns_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
