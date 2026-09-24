"""
benchmarks/wsa_probe.py — WSA-PROBE (round 209): tail weight-averaging
(SWA-style) contrast on the M1 spring family.

Preregistered in PRD §19 round 209 BEFORE execution. Scan §50: SWA
(Izmailov arXiv:1803.05407) averages weights along the tail of the SGD
trajectory — lands in wider optima, generalizes better; EMA (Morales-
Brotons 2024) is a different-but-related solution point. This probe
trains the E1-calibre prefix model for 2000 steps (constant lr, house
default), snapshots the last 10 checkpoints (every 100 steps), and
contrasts:

  A — LAST checkpoint rollout MSE
  B — uniform average of the tail-10 snapshots, rollout MSE

Both evaluated on the same held-out 128 trajectories at k=100. The head
has no BatchNorm (LayerNorm-style uses activations, not sliding stats),
so naive weight averaging is safe here (recorded).

Mechanical verdict (preregistered): diff = (A-B)/max(A,B);
  WSA_UNRESOLVABLE (negative) — any arm non-finite/divergent (>1e6)
  SWA_BENEFICIAL — diff >= +5%  (averaging helps)
  WSA_HARMFUL    — diff <= -5%  (averaging hurts, recorded as such)
  (|diff| < 5% falls through as "averaging not resolvable at screening
  tier" — reported inside detail; verdict field stays WSA_UNRESOLVABLE
  per the preregistered two-branch table)

1-seed screening tier; multi-seed finals PARKED per AMM-024. Results
JSON follows the audit schema (top-level "results" key); meta carries
exec_tier passthrough from probe_run.
"""

import argparse
import copy
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from awareliquid_physics.model import LiquidHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402
from benchmarks.liquid_physics_eval import evaluate  # noqa: E402
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

DIFF_GATE = 0.05  # preregistered: |diff| below this => unresolved
NORM_CAP = 1e6    # preregistered: divergence threshold
SNAP_EVERY = 100  # preregistered: checkpoint snapshot interval
N_SNAPS = 10      # preregistered: tail snapshots to average


def classify_wsa(mse_last: float, mse_avg: float,
                 gate: float = DIFF_GATE, cap: float = NORM_CAP):
    """Preregistered round-209 verdict (pure, test-pinned)."""
    for name, m in (("last", mse_last), ("avg", mse_avg)):
        if not math.isfinite(m) or m > cap:
            state = "non-finite" if not math.isfinite(m) else "diverged"
            return "WSA_UNRESOLVABLE", {
                "reason": f"{name} arm {state} (mse={m:.3e}): preregistered "
                          f"negative branch"}
    diff = (mse_last - mse_avg) / max(mse_last, mse_avg, 1e-30)
    if abs(diff) < gate:
        return "WSA_UNRESOLVABLE", {
            "diff": diff,
            "criterion": f"|diff| < {gate:.0%}: tail averaging not "
                         f"resolvable (trajectory variance already low, "
                         f"recorded as such)"}
    if diff > 0:
        return "SWA_BENEFICIAL", {
            "diff": diff,
            "criterion": f"tail average better by {diff:.1%}: averaging "
                         f"gain at zero inference cost"}
    return "SWA_HARMFUL", {
        "diff": diff,
        "criterion": f"tail average worse by {abs(diff):.1%}: recorded "
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
    ap.add_argument("--snap_every", type=int, default=SNAP_EVERY)
    ap.add_argument("--n_snaps", type=int, default=N_SNAPS)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/wsa_probe")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"WSA-PROBE | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} tail avg over "
          f"last {args.n_snaps} snapshots (every {args.snap_every}) "
          f"(seed {args.seed}, 1-seed screening)", flush=True)

    # injected training loop (round-149 loss-calibre rule) with tail
    # snapshots: train once, snapshotting every snap_every steps inside
    # the tail window [tail_start, train_steps]
    from benchmarks.liquid_physics_eval import rollout_mse_loss
    torch.manual_seed(args.seed)
    model = LiquidHamiltonianModel(
        1, d_model=args.d_model, context_dim=args.context_dim,
        n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
        dt=args.dt)
    g2 = torch.Generator().manual_seed(args.seed)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    N, S = qs.shape[0], qs.shape[1]
    model.train()
    snaps = []
    tail_start = args.train_steps - args.n_snaps * args.snap_every
    for step_i in range(args.train_steps):
        bi = torch.randint(0, N, (args.batch,), generator=g2)
        t0 = torch.randint(0, S - args.t_obs - args.k_train, (1,),
                           generator=g2).item()
        q_obs = qs[bi, t0:t0 + args.t_obs]
        p_obs = ps[bi, t0:t0 + args.t_obs]
        fut = slice(t0 + args.t_obs - 1, t0 + args.t_obs + args.k_train)
        q_true = qs[bi, fut]
        p_true = ps[bi, fut]
        qs_pred, ps_pred, _ = model(q_obs, p_obs, args.k_train)
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if (step_i + 1) >= tail_start \
                and (step_i + 1 - tail_start) % args.snap_every == 0:
            snaps.append(copy.deepcopy(model.state_dict()))
    snaps.append(copy.deepcopy(model.state_dict()))  # final step

    avg_sd = {k: torch.stack([sd[k].float() for sd in snaps])
              .mean(0) for k in snaps[0]}
    last_sd = snaps[-1]

    model.eval()
    mses = {}
    for name, sd in (("LAST", last_sd), ("AVG", avg_sd)):
        model.load_state_dict(sd)
        res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                       args.eval_k, args.dt)
        mses[name] = res["rollout_mse"]
        print(f"  [{name}] rollout MSE {res['rollout_mse']:.4e}",
              flush=True)

    verdict, detail = classify_wsa(mses["LAST"], mses["AVG"])
    results = {
        "mse_last": mses["LAST"],
        "mse_avg": mses["AVG"],
        "n_snapshots": len(snaps),
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_unresolvable": verdict == "WSA_UNRESOLVABLE",
            "c_beneficial": verdict == "SWA_BENEFICIAL",
            "c_harmful": verdict == "SWA_HARMFUL"},
        "gates": {"diff_gate": DIFF_GATE, "norm_cap": NORM_CAP},
    }
    print(f"\nWSA-PROBE verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "wsa_probe.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "wsa_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
