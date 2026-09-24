"""
benchmarks/warmup_probe.py — WARMUP-PROBE (round 212): lr warmup contrast
on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 212 BEFORE execution. Scan §37.2 (Kalra
NeurIPS 2023: warmup works by letting sharpness fall before larger lr;
§37.4 action face): does lr warmup (linear 0 -> 3e-3 over the first 200
steps, then constant) change rollout generalization vs the constant-lr
house default? Round 194 (SHARP_BELOW) found the house regime is NOT at
the edge of stability — warmup's benefit domain may not trigger here;
this probe tests that prediction directly.

Warmup is injected via a LambdaLR scheduler over the verbatim prefix
loop (round-149 loss-calibre rule).

Mechanical verdict (preregistered): diff = (A-B)/max(A,B);
  WARMUP_UNRESOLVABLE (negative) — any arm diverged (non-finite or
      rollout > 1e6), or |diff| < 5% (warmup not resolvable; consistent
      with round-194 SHARP_BELOW: not at EOS)
  WARMUP_BENEFICIAL — diff >= +5%  (A worse; §37.2 direction)
  WARMUP_HARMFUL    — diff <= -5%  (A better; recorded as such)

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
    rollout_mse_loss)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

DIFF_GATE = 0.05  # preregistered: |diff| below this => unresolved
NORM_CAP = 1e6    # preregistered: divergence threshold
WARMUP_STEPS = 200  # preregistered: warmup phase length


def train_variant(model, qs, ps, t_obs, k_train, steps, lr, batch, seed,
                  warmup_steps: int = 0):
    """Prefix loop verbatim (round-149 loss-calibre rule) with an optional
    linear lr warmup over the first warmup_steps via LambdaLR."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    if warmup_steps > 0:
        sched = torch.optim.lr_scheduler.LambdaLR(
            opt, lambda t: min(1.0, (t + 1) / warmup_steps))
    else:
        sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda t: 1.0)
    N, S = qs.shape[0], qs.shape[1]
    model.train()
    loss = torch.tensor(float("nan"))
    for _ in range(steps):
        bi = torch.randint(0, N, (batch,), generator=g)
        t0 = torch.randint(0, S - t_obs - k_train, (1,), generator=g).item()
        q_obs = qs[bi, t0:t0 + t_obs]
        p_obs = ps[bi, t0:t0 + t_obs]
        fut = slice(t0 + t_obs - 1, t0 + t_obs + k_train)
        q_true = qs[bi, fut]
        p_true = ps[bi, fut]
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k_train)
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        sched.step()
    return loss.item()


def evaluate_rollout(model, qs, ps, k, t_obs):
    """k-step free-running rollout MSE on held-out trajectories."""
    model.eval()
    q_obs = qs[:, :t_obs]
    p_obs = ps[:, :t_obs]
    fut = slice(t_obs - 1, t_obs + k)
    q_true = qs[:, fut].permute(1, 0, 2)   # (k+1, B, dim)
    p_true = ps[:, fut].permute(1, 0, 2)
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    return ((qs_pred - q_true) ** 2 + (ps_pred - p_true) ** 2).mean().item()


def classify_warmup(mse_const: float, mse_warm: float,
                    gate: float = DIFF_GATE, cap: float = NORM_CAP):
    """Preregistered round-212 verdict (pure, test-pinned)."""
    for name, m in (("constant", mse_const), ("warmup", mse_warm)):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "WARMUP_UNRESOLVABLE", {
                "reason": f"{name} arm {state} (mse={m:.3e}): preregistered "
                          f"negative branch"}
    diff = (mse_const - mse_warm) / max(mse_const, mse_warm, 1e-30)
    if abs(diff) < gate:
        return "WARMUP_UNRESOLVABLE", {
            "diff": diff,
            "criterion": f"|diff| < {gate:.0%}: warmup not resolvable "
                         f"(consistent with round-194 SHARP_BELOW: not at "
                         f"EOS, warmup benefit domain may not trigger)"}
    if diff > 0:
        return "WARMUP_BENEFICIAL", {
            "diff": diff,
            "criterion": f"warmup arm better by {diff:.1%}: §37.2 direction"}
    return "WARMUP_HARMFUL", {
        "diff": diff,
        "criterion": f"warmup arm worse by {abs(diff):.1%}: recorded "
                     f"as such"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--omega_lo", type=float, default=0.7)
    ap.add_argument("--omega_hi", type=float, default=1.8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--warmup_steps", type=int, default=WARMUP_STEPS)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/warmup_probe")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    ev = slice(args.n_train, None)
    print(f"WARMUP-PROBE | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} lr={args.lr} A=constant vs "
          f"B=warmup({args.warmup_steps}) (seed {args.seed}, 1-seed "
          f"screening)", flush=True)

    arms = {}
    for name, warm in (("A", 0), ("B", args.warmup_steps)):
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        tr = slice(0, args.n_train)
        train_variant(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                      args.train_steps, args.lr, args.batch, args.seed,
                      warmup_steps=warm)
        mse = evaluate_rollout(model, qs[ev], ps[ev], args.eval_k,
                               args.t_obs)
        arms[name] = mse
        print(f"  [{name}] rollout MSE {mse:.4e}", flush=True)

    verdict, detail = classify_warmup(arms["A"], arms["B"])
    results = {
        "arms": {"A_constant": arms["A"], "B_warmup": arms["B"]},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "WARMUP_UNRESOLVABLE",
            "c_beneficial": verdict == "WARMUP_BENEFICIAL",
            "c_harmful": verdict == "WARMUP_HARMFUL"},
        "gates": {"diff_gate": DIFF_GATE, "norm_cap": NORM_CAP,
                  "warmup_steps": WARMUP_STEPS},
    }
    print(f"\nWARMUP-PROBE verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "warmup_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "warmup_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
