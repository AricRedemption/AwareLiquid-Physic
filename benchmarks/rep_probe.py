"""
benchmarks/rep_probe.py — REP-PROBE (round 159): window-repetition-rate
contrast on the M1 spring semigroup regime.

Preregistered in PRD §19 round 159 BEFORE execution. Scan §38 (Muennighoff
NeurIPS 2023 value decay; Fu et al. arXiv:2305.13230): does HOW windows
are consumed matter? Two arms, same 4000-step budget, same everything:

  A — WITH-replacement resampling: train_semigroup verbatim (the house
      default; a window pair can repeat arbitrarily).
  B — WITHOUT-replacement epoch sweeps: all unique (traj, t0) pairs
      shuffled and consumed in order (each pair at most once per epoch,
      reshuffled when exhausted, ~7.8 epochs over 4000 steps).

The B loop is verbatim-identical to A except the start-time selection
(round-149 loss-calibre rule). Eval = same held-out 128 trajectories,
k100 rollout MSE (liquid evaluate calibre).

Mechanical verdict (preregistered): diff = (A-B)/max(A,B);
  REP_UNRESOLVABLE (negative)  — |diff| < 5%
  REP_REPETITION_HARMFUL       — diff >= +5%   (A worse)
  REP_REPETITION_HELPFUL       — diff <= -5%   (A better)

1-seed screening tier; multi-seed finals PARKED per AMM-024. Results JSON
follows the audit schema (top-level "results" key); meta carries
exec_tier passthrough from probe_run.
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from awareliquid_physics.train import train_semigroup  # noqa: E402
from benchmarks.liquid_physics_eval import (  # noqa: E402
    evaluate, rollout_mse_loss)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

DIFF_GATE = 0.05  # preregistered: |diff| below this => unresolved


def train_sweep(model, qs, ps, t_obs, k_train, steps, lr, batch, seed):
    """Arm B: without-replacement epoch sweeps — verbatim-identical to
    train_semigroup except start pairs are drawn from a shuffled deck of
    ALL unique (traj, t0) pairs (reshuffled when exhausted)."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    n_traj, S = qs.shape[0], qs.shape[1]
    pairs = [(i, t) for i in range(n_traj)
             for t in range(t_obs, S - k_train)]
    deck = []
    model.train()
    loss = torch.tensor(float("nan"))
    for step_i in range(steps):
        if len(deck) < batch:
            perm = torch.randperm(len(pairs), generator=g)
            deck = [pairs[j] for j in perm.tolist()]
        bi_list = [deck.pop() for _ in range(batch)]
        bi = torch.tensor([b for b, _ in bi_list])
        t0 = torch.tensor([t for _, t in bi_list])
        q_obs = qs[bi, :t_obs]
        p_obs = ps[bi, :t_obs]
        with torch.enable_grad():
            ctx = model.infer_context(q_obs, p_obs)
            q0 = qs[bi, t0]
            p0 = ps[bi, t0]
            qs_pred, ps_pred = model.rollout(q0, p0, ctx, k_train)
            # (B, k+1, dim) — rollout_mse_loss transposes internally
            # (prefix-train convention; no extra permute here)
            q_true = qs[bi[:, None], t0[:, None] + torch.arange(k_train + 1)]
            p_true = ps[bi[:, None], t0[:, None] + torch.arange(k_train + 1)]
            loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step_i % 500 == 0:
            print(f"    [sweep {step_i:>5}] loss {loss.item():.3e}",
                  flush=True)
    return loss.item()


def classify_rep(mse_a: float, mse_b: float, gate: float = DIFF_GATE):
    """Preregistered round-159 verdict (pure, test-pinned)."""
    diff = (mse_a - mse_b) / max(mse_a, mse_b, 1e-30)
    if abs(diff) < gate:
        return "REP_UNRESOLVABLE", {
            "diff": diff,
            "criterion": f"|diff| < {gate}: repetition rate not "
                         f"resolvable by the rollout metric (record "
                         f"observation-calibre caveat per §38.3)"}
    if diff > 0:
        return "REP_REPETITION_HARMFUL", {
            "diff": diff,
            "criterion": f"A (with replacement) worse by {diff:.1%}: "
                         f"repetition rate past the value-decay region"}
    return "REP_REPETITION_HELPFUL", {
        "diff": diff,
        "criterion": f"A (with replacement) better by {abs(diff):.1%}: "
                     f"random resampling acts as more diverse updates"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
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
    ap.add_argument("--train_steps", type=int, default=4000)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/rep_probe")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    pool_qs, pool_ps, pool_om = gen_spring(
        args.n_train + args.n_eval, args.gen_steps, args.dt, 1,
        args.omega_lo, args.omega_hi, g, device=args.device)
    ev = slice(args.n_train, None)
    omega_ev = pool_om[ev]
    print(f"REP-PROBE | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} semigroup steps={args.train_steps} "
          f"arms=A(with-replacement)/B(sweep) (seed {args.seed}, 1-seed "
          f"screening)", flush=True)

    arms = {}
    for name in ("A", "B"):
        torch.manual_seed(args.seed)
        model = LiquidHamiltonianModel(1, d_model=args.d_model,
                                       context_dim=args.context_dim,
                                       n_scales=args.n_scales,
                                       hidden_dim=args.hidden, depth=2,
                                       dt=args.dt)
        if name == "A":
            loss = train_semigroup(model, pool_qs[:args.n_train],
                                   pool_ps[:args.n_train], args.t_obs,
                                   args.k_train, args.train_steps,
                                   args.lr, args.batch, args.seed)
        else:
            loss = train_sweep(model, pool_qs[:args.n_train],
                               pool_ps[:args.n_train], args.t_obs,
                               args.k_train, args.train_steps,
                               args.lr, args.batch, args.seed)
        res = evaluate(model, pool_qs[ev], pool_ps[ev], omega_ev,
                       args.t_obs, args.eval_k, args.dt)
        res["train_loss"] = loss
        arms[name] = res
        print(f"  [{name}] rollout MSE {res['rollout_mse']:.4e} "
              f"| train_loss {loss:.3e}", flush=True)

    verdict, detail = classify_rep(arms["A"]["rollout_mse"],
                                   arms["B"]["rollout_mse"])
    results = {
        "arms": arms,
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "REP_UNRESOLVABLE",
            "c_harmful": verdict == "REP_REPETITION_HARMFUL",
            "c_helpful": verdict == "REP_REPETITION_HELPFUL"},
        "gates": {"diff_gate": DIFF_GATE},
    }
    print(f"\nREP-PROBE verdict {verdict} | {detail.get('criterion')}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "rep_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "rep_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
