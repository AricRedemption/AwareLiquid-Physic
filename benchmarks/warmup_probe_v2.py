"""
benchmarks/warmup_probe_v2.py — WARMUP-PROBE-2 (round 237): 3-seed
single-axis warmup ablation on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 236 BEFORE execution (AMM-027 pool
routing: dir/recipe-synthesis round-228 verdict line named the warmup
attribution as a family follow-up — "组合臂含 warmup 且整体协同,但单轴
贡献不可分离(归因=族后续候选,需 3-seed 单轴消融)"). Same two arms and
calibre as round 212 (A = constant lr 3e-3 house default; B = linear
warmup 0 -> 3e-3 over the first 200 steps, then constant), upgraded
from 1-seed screening to the AMM-028 gate-3 3-seed protocol. The
round-213 single-seed 44.2% contra-expectation reading is the value
under test: RECIPE-SYNTHESIS (round 228, ratio 0.893 with warmup
inside arm B) already suggests the single-seed number does not survive
composition.

Mechanical verdict (preregistered, 3-seed mean ratio r = mean_B/mean_A):
  WARMUP_ARM_DIVERGED (negative) — any arm/seed non-finite or rollout
      > 1e6: that arm unusable, recorded as such
  WARMUP_3S_BENEFICIAL — r < 0.95: warmup benefit confirmed at 3-seed;
      round-213 44.2% downgraded to directional; decision = warmup
      stays in the back-propagation recipe candidate
  WARMUP_3S_UNRESOLVED — 0.95 <= r <= 1.05: benefit not robust;
      round-213 reading downgraded to single-seed noise; decision =
      drop-warmup recommendation for the recipe candidate
  WARMUP_3S_HARMFUL — r > 1.05: reversal recorded as such; decision =
      remove warmup from the recipe candidate (interaction-attribution
      material vs RECIPE_SYNERGIC)

The verdict line must carry per-seed values, direction-consistency
count (# seeds with B < A) and per-arm seed spread (AMM-028 gate-3).
Cross-validation anchor: arm A seed 0 is configurationally identical
to the house default arms of rounds 175/191/223/226 and to the
RECIPE-SYNTHESIS arm A seed 0 (same seed, same rng stream) and must
match 3.5582 bit-for-bit (sentinel clause r181). Family boundary:
WARMUP family in-segment round 2 of 2 — family closes after this.
Results JSON follows the audit schema (top-level "results" key); meta
carries exec_tier passthrough from probe_run.
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
    evaluate, rollout_mse_loss)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

NORM_CAP = 1e6          # preregistered: divergence threshold
BENEFICIAL_GATE = 0.95  # preregistered: ratio < gate => benefit robust
HARM_GATE = 1.05        # preregistered: ratio > gate => reversal
SEEDS = (0, 1, 2)       # preregistered: AMM-028 gate-3 3-seed minimum
WARMUP_STEPS = 200      # preregistered: warmup phase length (round 212)
SENTINEL = 3.5581917762756348  # house default arm A seed 0 (r175/191/
                               # 223/226 + RECIPE-SYNTHESIS arm A s0)


def train_warmup(model, qs, ps, t_obs, k_train, steps, lr, batch, seed,
                 warmup_steps: int = 0):
    """House prefix loop with the warmup knob.

    Identical rng consumption to benchmarks.liquid_physics_eval.train:
    with warmup_steps=0 the lr schedule is constant 1.0 — bit-for-bit
    the house default arm (sentinel clause r181).
    """
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda t: min(1.0, (t + 1) / warmup_steps)
        if warmup_steps > 0 else 1.0)
    N, S = qs.shape[0], qs.shape[1]
    model.train()
    loss = torch.tensor(float("nan"))
    for _ in range(steps):
        bi = torch.randint(0, N, (batch,), generator=g)
        # random window: [t0, t0+t_obs) observed, next k_train predicted
        t0 = torch.randint(0, S - t_obs - k_train, (1,), generator=g).item()
        q_obs = qs[bi, t0:t0 + t_obs]; p_obs = ps[bi, t0:t0 + t_obs]
        fut = slice(t0 + t_obs - 1, t0 + t_obs + k_train)        # incl. last observed
        q_true = qs[bi, fut]; p_true = ps[bi, fut]
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k_train)
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        sched.step()
    return loss.item()


def classify_warmup_3s(mses_a, mses_b,
                       beneficial_gate: float = BENEFICIAL_GATE,
                       harm_gate: float = HARM_GATE,
                       cap: float = NORM_CAP):
    """Preregistered round-236 verdict (pure, test-pinned)."""
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "WARMUP_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} {state} "
                              f"(mse={m:.3e}): arm unusable, "
                              f"recorded as such"}
    mean_a = sum(mses_a) / len(mses_a)
    mean_b = sum(mses_b) / len(mses_b)
    ratio = mean_b / max(mean_a, 1e-30)
    consistent = sum(1 for a, b in zip(mses_a, mses_b) if b < a)
    spread_a = max(mses_a) / max(min(mses_a), 1e-30)
    spread_b = max(mses_b) / max(min(mses_b), 1e-30)
    stats = {"ratio": ratio, "mean_A": mean_a, "mean_B": mean_b,
             "mses_A": mses_a, "mses_B": mses_b,
             "direction_consistency": f"{consistent}/{len(mses_a)}",
             "seed_spread_A": spread_a, "seed_spread_B": spread_b}
    if ratio < beneficial_gate:
        verdict = "WARMUP_3S_BENEFICIAL"
        stats["decision"] = ("warmup benefit confirmed at 3-seed: stays "
                             "in the back-propagation recipe candidate; "
                             "round-213 44.2% downgraded to directional")
    elif ratio <= harm_gate:
        verdict = "WARMUP_3S_UNRESOLVED"
        stats["decision"] = ("warmup benefit not robust at 3-seed: "
                             "drop-warmup recommendation for the recipe "
                             "candidate; round-213 reading downgraded "
                             "to single-seed noise")
    else:
        verdict = "WARMUP_3S_HARMFUL"
        stats["decision"] = ("warmup reversal at 3-seed: remove from "
                             "the recipe candidate (interaction material "
                             "vs RECIPE_SYNERGIC r228)")
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
    ap.add_argument("--warmup_steps", type=int, default=WARMUP_STEPS)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/warmup_probe_v2")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"WARMUP-PROBE-2 | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} A=constant vs "
          f"B=warmup({args.warmup_steps}) (seeds {seeds}, AMM-028 g3 "
          f"3-seed; round-236 preregistration)", flush=True)

    arms = {"A": [], "B": []}
    for seed in seeds:
        for tag, warm in (("A", 0), ("B", args.warmup_steps)):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            train_warmup(model, qs[tr], ps[tr], args.t_obs,
                         args.k_train,
                         args.train_steps, args.lr, args.batch, seed,
                         warmup_steps=warm)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            arms[tag].append(res["rollout_mse"])
            print(f"  [arm {tag} seed {seed}] rollout MSE "
                  f"{res['rollout_mse']:.4e}", flush=True)

    verdict, detail = classify_warmup_3s(arms["A"], arms["B"])
    sentinel = {"expected": SENTINEL, "actual": arms["A"][0],
                "bitwise_match": arms["A"][0] == SENTINEL}
    results = {
        "arms": {"A_constant": arms["A"], "B_warmup": arms["B"]},
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinel_arm_a_seed0": sentinel,
        "criteria": {
            "c_diverged": verdict == "WARMUP_ARM_DIVERGED",
            "c_beneficial": verdict == "WARMUP_3S_BENEFICIAL",
            "c_unresolved": verdict == "WARMUP_3S_UNRESOLVED",
            "c_harmful": verdict == "WARMUP_3S_HARMFUL"},
        "gates": {"beneficial_gate": BENEFICIAL_GATE,
                  "harm_gate": HARM_GATE, "norm_cap": NORM_CAP,
                  "warmup_steps": WARMUP_STEPS,
                  "seeds": list(SEEDS)},
        "anchor": "arm A seed 0 expected 3.5582 (house default, rounds "
                  "175/191/223/226 + RECIPE-SYNTHESIS arm A seed0 "
                  "sentinel)"},
    print(f"\nWARMUP-PROBE-2 verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinel A/s0 match={sentinel['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "warmup_probe_v2.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "warmup_probe_v2",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
