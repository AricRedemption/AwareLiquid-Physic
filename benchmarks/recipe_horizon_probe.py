"""
benchmarks/recipe_horizon_probe.py — RECIPE-HORIZON (round 252):
evaluation-horizon robustness of the back-propagation recipe candidate,
3 seeds, on the M1 spring family (E1 calibre).

Preregistered in PRD §19 round 251 BEFORE execution (AMM-027 distill
routing, self-generated scan family 55). All RECIPE evidence (rounds
227/228: composite gain 10.7%, direction 3/3) was measured at the
single k=100 evaluation caliber; whether the gain holds at deployment
horizons is open. Arms: A = house default configuration, B = the
recipe candidate (depth 4 + lr_decay 0.999 + weight_decay 1e-4 +
warmup 200 + k_train 4, round-229 composition, injected composed loop
per the round-181 watchdog clause). Each arm trained 2000 steps x 3
seeds on the canonical pool; each trained model evaluated at THREE
horizons k ∈ {100, 200, 400} on a shared long-horizon held-out pool
(gen_steps=450 to cover t_obs + k + 1, round-162 lesson).

Dual-pool design note (honest, r246 lesson applied): the sentinel
(A seed 0, k=100, canonical gen-160 pool) is only valid on the
canonical data stream — the gen-450 horizon pool is a different
stream, so horizon ratios are computed WITHIN the 450 pool only
(internally consistent across arms and horizons). The preregistered
sentinel stays bitwise-valid; this refinement is recorded in the
round-252 record.

Mechanical verdict (preregistered, 3-seed mean ratio r(k) =
mean_MSE_B(k) / mean_MSE_A(k)):
  HORIZON_ARM_DIVERGED (negative) — any arm/seed/horizon non-finite
      or rollout > 1e6
  HORIZON_ROBUST  — r(k) < 0.95 at ALL horizons: recipe gain is
      horizon-robust; decision = back-propagation PR scope confirmed
  HORIZON_LIMITED — r(400) >= 0.95 (with r(100) < 0.95): gain limited
      to mid horizons; decision = back-propagation PR scope annotated
      "k100-200"
  HORIZON_FRAGILE — r(400) > 1.05: recipe horizon-fragile, recorded
      as such

The verdict line carries per-seed per-horizon values, direction
consistency per horizon, and seed spreads (AMM-028 gate-3).
Cross-validation anchor: A seed 0 at k=100 on the canonical pool =
3.5581917762756348 (house default sentinel). Family boundary: scan
family 55 round 1 — distinct from the KSPAN family (training span)
and from §41.2/§46.1 literature coordinates. Results JSON follows the
audit schema (top-level "results" key); meta carries exec_tier from
probe_run.
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
    evaluate, rollout_mse_loss, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

NORM_CAP = 1e6       # preregistered: divergence threshold
ROBUST_GATE = 0.95   # preregistered: ratio < gate at ALL horizons
FRAGILE_GATE = 1.05  # preregistered: r(400) > gate => fragile
SEEDS = (0, 1, 2)
SENTINEL = 3.5581917762756348  # house default A seed 0, canonical pool

# preregistered recipe candidate (round-229 composition)
RECIPE = {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
          "warmup_steps": 200, "k_train": 4}


def train_recipe(model, qs, ps, t_obs, k_train, steps, lr, batch, seed,
                 lr_decay: float = 1.0, weight_decay: float = 0.0,
                 warmup_steps: int = 0):
    """Composed recipe loop (round-227 verbatim): identical rng
    consumption to the house prefix train; with neutral knobs it is
    the house default bit-for-bit (sentinel clause r181)."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr,
                           weight_decay=weight_decay)

    def lr_fn(t):
        warm = min(1.0, (t + 1) / warmup_steps) if warmup_steps > 0 else 1.0
        return warm * (lr_decay ** t)

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_fn)
    N, S = qs.shape[0], qs.shape[1]
    model.train()
    loss = torch.tensor(float("nan"))
    for _ in range(steps):
        bi = torch.randint(0, N, (batch,), generator=g)
        t0 = torch.randint(0, S - t_obs - k_train, (1,), generator=g).item()
        q_obs = qs[bi, t0:t0 + t_obs]; p_obs = ps[bi, t0:t0 + t_obs]
        fut = slice(t0 + t_obs - 1, t0 + t_obs + k_train)
        q_true = qs[bi, fut]; p_true = ps[bi, fut]
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k_train)
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        sched.step()
    return loss.item()


def median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def classify_horizon(ratios, mses_a_by_k, mses_b_by_k,
                     robust_gate: float = ROBUST_GATE,
                     fragile_gate: float = FRAGILE_GATE,
                     cap: float = NORM_CAP, seeds=SEEDS):
    """Preregistered round-251 verdict (pure, test-pinned).

    ratios: {k: ratio} over 3-seed means; mses_*_by_k: {k: [per-seed]}.
    """
    for k, vals in mses_a_by_k.items():
        for s, m in zip(seeds, vals):
            if not math.isfinite(m) or m > cap:
                return "HORIZON_ARM_DIVERGED", {
                    "reason": f"arm A k={k} seed {s} non-finite/diverged "
                              f"({m:.3e})"}
    for k, vals in mses_b_by_k.items():
        for s, m in zip(seeds, vals):
            if not math.isfinite(m) or m > cap:
                return "HORIZON_ARM_DIVERGED", {
                    "reason": f"arm B k={k} seed {s} non-finite/diverged "
                              f"({m:.3e})"}
    ks = sorted(ratios)
    per_k = {}
    for k in ks:
        ma, mb = mses_a_by_k[k], mses_b_by_k[k]
        agree = sum(1 for a, b in zip(ma, mb) if b < a)
        per_k[k] = {"ratio": ratios[k],
                    "direction_consistency": f"{agree}/{len(ma)}",
                    "seed_spread_B": max(mb) / max(min(mb), 1e-30)}
    stats = {"ratios": ratios, "per_horizon": per_k,
             "mses_A": mses_a_by_k, "mses_B": mses_b_by_k}
    if all(r < robust_gate for r in ratios.values()):
        verdict = "HORIZON_ROBUST"
        stats["decision"] = ("recipe gain horizon-robust: back-propagation "
                             "PR scope confirmed")
    elif ratios[max(ks)] >= fragile_gate:
        verdict = "HORIZON_FRAGILE"
        stats["decision"] = ("recipe horizon-fragile at long horizons: "
                             "recorded as such")
    else:
        verdict = "HORIZON_LIMITED"
        stats["decision"] = ("recipe gain limited to mid horizons: "
                             "back-propagation PR scope annotated "
                             "'k100-200'")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=160)
    ap.add_argument("--horizon_gen_steps", type=int, default=450)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--horizons", default="100,200,400")
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
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/recipe_horizon")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    horizons = sorted(int(x) for x in args.horizons.split(","))

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    gh = torch.Generator().manual_seed(0)
    qs_h, ps_h, om_h = gen_spring(args.n_train + args.n_eval,
                                  args.horizon_gen_steps, args.dt, 1,
                                  args.omega_lo, args.omega_hi, gh,
                                  device=args.device)
    ev_h = slice(args.n_train, None)
    print(f"RECIPE-HORIZON | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} steps={args.train_steps} "
          f"A=default vs B=recipe{RECIPE} horizons={horizons} "
          f"(seeds {seeds}; dual-pool: canonical sentinel + gen-{args.horizon_gen_steps} horizon pool; "
          f"round-251 preregistration)", flush=True)

    mses = {"A": {k: [] for k in horizons},
            "B": {k: [] for k in horizons}}
    canonical = []
    for seed in seeds:
        for tag in ("A", "B"):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=RECIPE["depth"] if tag == "B" else 2, dt=args.dt)
            if tag == "A":
                train_prefix(model, qs[tr], ps[tr], args.t_obs,
                             args.k_train, args.train_steps, args.lr,
                             args.batch, seed)
            else:
                train_recipe(model, qs[tr], ps[tr], args.t_obs,
                             RECIPE["k_train"], args.train_steps,
                             args.lr, args.batch, seed,
                             lr_decay=RECIPE["lr_decay"],
                             weight_decay=RECIPE["weight_decay"],
                             warmup_steps=RECIPE["warmup_steps"])
            # canonical sentinel eval (k=100, gen-160 pool) — arm A only
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            if tag == "A":
                canonical.append(res["rollout_mse"])
            for k in horizons:
                rh = evaluate(model, qs_h[ev_h], ps_h[ev_h], om_h[ev_h],
                              args.t_obs, k, args.dt)
                mses[tag][k].append(rh["rollout_mse"])
            print(f"  [arm {tag} seed {seed}] canonical k100 "
                  f"{res['rollout_mse']:.4e} | horizon "
                  f"{ {k: round(mses[tag][k][-1], 3) for k in horizons} }",
                  flush=True)

    ratios = {k: (sum(mses["B"][k]) / len(seeds))
              / max(sum(mses["A"][k]) / len(seeds), 1e-30)
              for k in horizons}
    verdict, detail = classify_horizon(ratios, mses["A"], mses["B"],
                                       seeds=seeds)
    sentinels = {"A_canonical_k100_seed0": {
        "expected": SENTINEL, "actual": canonical[0],
        "bitwise_match": canonical[0] == SENTINEL}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "recipe": RECIPE,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "HORIZON_ARM_DIVERGED",
                     "c_robust": verdict == "HORIZON_ROBUST",
                     "c_limited": verdict == "HORIZON_LIMITED",
                     "c_fragile": verdict == "HORIZON_FRAGILE"},
        "gates": {"robust_gate": ROBUST_GATE,
                  "fragile_gate": FRAGILE_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(seeds), "horizons": horizons},
        "anchor": "A canonical k100 seed0 = 3.5582 (house default "
                  "sentinel; horizon pool is a separate gen-450 stream, "
                  "ratios computed within-pool)"},
    print(f"\nRECIPE-HORIZON verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"ratios={ {k: round(v, 4) for k, v in ratios.items()} } | "
          f"sentinel={sentinels['A_canonical_k100_seed0']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "recipe_horizon.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "recipe_horizon_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
