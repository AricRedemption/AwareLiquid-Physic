"""
benchmarks/opt_compare_probe.py — OPT-COMPARE (round 178): Adam vs
SGD-momentum on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 178 BEFORE execution. Scan §43: Wilson
NeurIPS 2017 (arXiv:1705.08292) found adaptive methods generalize worse
(MLP/CNN side); Kunstner 2023 found Adam's advantage on transformers is
not noise-driven but geometric — an architecture-dependent pair. The
house default is Adam(lr=3e-3); this probe measures whether SGD-
momentum(lr=0.1, momentum=0.9) differs on rollout generalization under
the same 2000-step budget.

KNOWN LIMIT (preregistered): lr is NOT per-optimizer tuned (Schmidt
ICML 2021: tuning budget is the dominant variable) — a diverging or
non-finite arm maps to OPT_UNRESOLVABLE (lr-budget mismatch), recorded
as such, NOT as an optimizer verdict.

Mechanical verdict (preregistered): diff = (A-B)/max(A,B);
  OPT_UNRESOLVABLE (negative) — any arm loss non-finite or rollout
      > 1e6 (lr-budget mismatch), or |diff| < 5%
      (no single winner, §43.3-consistent)
  OPT_SGD_BETTER  — diff >= +5%  (A worse; adaptive cost, §43.1)
  OPT_ADAM_BETTER — diff <= -5%  (A better; adaptive gain, §43.2)

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

DIFF_GATE = 0.05    # preregistered: |diff| below this => unresolved
NORM_CAP = 1e6      # preregistered: divergence threshold


def train_custom(model, qs, ps, t_obs, k_train, steps, opt, batch, seed):
    """Prefix loop verbatim (round-149 loss-calibre rule) with a
    caller-provided optimizer."""
    g = torch.Generator().manual_seed(seed)
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


def evaluate_rollout(model, qs, ps, k):
    """k-step free-running rollout MSE on held-out trajectories."""
    model.eval()
    q0, p0 = qs[:, 0], ps[:, 0]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(qs[:, :24], ps[:, :24], k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[:, :k + 1].permute(1, 0, 2)
    p_true = ps[:, :k + 1].permute(1, 0, 2)
    return ((qs_pred - q_true) ** 2 + (ps_pred - p_true) ** 2).mean().item()


def classify_opt(mse_adam: float, mse_sgd: float,
                 gate: float = DIFF_GATE, cap: float = NORM_CAP):
    """Preregistered round-178 verdict (pure, test-pinned)."""
    for name, m in (("adam", mse_adam), ("sgd", mse_sgd)):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "OPT_UNRESOLVABLE", {
                "reason": f"{name} arm {state} (mse={m:.3e}): lr-budget "
                          f"mismatch — preregistered negative branch, "
                          f"NOT an optimizer verdict"}
    diff = (mse_adam - mse_sgd) / max(mse_adam, mse_sgd, 1e-30)
    if abs(diff) < gate:
        return "OPT_UNRESOLVABLE", {
            "diff": diff,
            "criterion": f"|diff| < {gate:.0%}: optimizer not resolvable "
                         f"(no single winner, §43.3-consistent)"}
    if diff > 0:
        return "OPT_SGD_BETTER", {
            "diff": diff,
            "criterion": f"SGD-momentum rollout better by {diff:.1%}: "
                         f"adaptive generalization cost (§43.1 direction)"}
    return "OPT_ADAM_BETTER", {
        "diff": diff,
        "criterion": f"Adam rollout better by {abs(diff):.1%}: adaptive "
                     f"gain (§43.2 direction)"}


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
    ap.add_argument("--lr_adam", type=float, default=3e-3)
    ap.add_argument("--lr_sgd", type=float, default=0.1)
    ap.add_argument("--momentum", type=float, default=0.9)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/opt_compare")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, _ = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                           args.dt, 1, args.omega_lo, args.omega_hi, g,
                           device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"OPT-COMPARE | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} "
          f"arms=Adam(lr={args.lr_adam})/SGD-m(lr={args.lr_sgd},"
          f"mom={args.momentum}) (seed {args.seed}, 1-seed screening; "
          f"lr NOT per-optimizer tuned — preregistered limit)",
          flush=True)

    arms = {}
    for name, opt_name in (("ADAM", "adam"), ("SGDM", "sgd")):
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(
            1, d_model=args.d_model, context_dim=args.context_dim,
            n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
            dt=args.dt)
        if opt_name == "adam":
            opt = torch.optim.Adam(model.parameters(), lr=args.lr_adam)
        else:
            opt = torch.optim.SGD(model.parameters(), lr=args.lr_sgd,
                                  momentum=args.momentum)
        loss = train_custom(model, qs[tr], ps[tr], args.t_obs,
                            args.k_train, args.train_steps, opt,
                            args.batch, args.seed)
        mse = evaluate_rollout(model, qs[ev], ps[ev], args.eval_k)
        arms[name] = {"rollout_mse": mse, "train_loss": loss}
        print(f"  [{name}] rollout MSE {mse:.4e} | train_loss {loss:.3e}",
              flush=True)

    verdict, detail = classify_opt(arms["ADAM"]["rollout_mse"],
                                   arms["SGDM"]["rollout_mse"])
    results = {
        "arms": arms,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "OPT_UNRESOLVABLE",
            "c_sgd_better": verdict == "OPT_SGD_BETTER",
            "c_adam_better": verdict == "OPT_ADAM_BETTER"},
        "gates": {"diff_gate": DIFF_GATE, "norm_cap": NORM_CAP},
        "limit_note": "lr NOT per-optimizer tuned (Schmidt 2021: tuning "
                      "budget dominates); results are a constrained "
                      "contrast",
    }
    print(f"\nOPT-COMPARE verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "opt_compare.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "opt_compare_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
