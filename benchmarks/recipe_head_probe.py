"""
benchmarks/recipe_head_probe.py — RECIPE-HEAD (round 279): the 2x2
composition of the back-propagation recipe candidate (round-229
composition: depth 4 + lr_decay 0.999 + weight_decay 1e-4 + warmup 200
+ k_train 4) with the homogeneous-head candidate (round-269: analytic
T + direction-free homogeneous V), 3 seeds, M1 spring family (E1
caliber, canonical k=100). Self-generated confirmation probe
(round-257 precedent): the AMM-028 gate-2 forced-composition mandate
(>=3 families judged default non-optimal => composition required)
extends to the pending AMM-033 head adoption — before adopting BOTH
the recipe and the head as joint defaults, their 2x2 must be measured.

Cells (single run each x 3 seeds):
  A0 = recipe OFF, house default head   (depth 2, train_prefix)
       sentinel: seed 0 = 3.5581917762756348 bitwise
  A1 = recipe ON,  house default head   (depth = RECIPE.depth,
       train_recipe verbatim, round-227 rng-identical loop)
       anchor: seed 0 = 3.3909592628479004 (round-252 arm B canonical)
  B0 = recipe OFF, candidate head       (HomVStabHead depth 2)
       anchor: seed 0 = 2.0023648738861084 (round-269 B arm)
  B1 = recipe ON,  candidate head       (HomVStabHead depth = 4)
       NEW measurement

Mechanical verdict (preregistered, 3-seed):
  HOM_ARM_DIVERGED (negative) — any reading non-finite or > 1e6
  COMPOSE_SYNERGIC  — mean(B1) < min(mean(B0), mean(A1)): the
      combination strictly beats both singles ⇒ AMM-033 adoption note
      = joint default (recipe + head together)
  COMPOSE_ABSORBED  — mean(B1) >= min(...) AND ratio_on =
      mean(B1)/mean(A1) <= 1.05: the recipe absorbs the head's
      advantage ⇒ either-or adoption note
  COMPOSE_CONFLICT  — ratio_on > 1.05: the candidate hurts under the
      recipe ⇒ adoption note = recipe + default head

Decision coupling (AMM-028 gate-1): each outcome changes the joint
adoption plan in AMM-033 differently, EIG qualified. Family
bookkeeping: composition-confirmation round under the gate-2 mandate
(no new literature family; in-library §55 + RECIPE-SYNTHESIS records
are the decision basis). Results JSON follows the audit schema.
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
from benchmarks.v_hom_stab_probe import HomVStabHead  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NORM_CAP = 1e6   # preregistered: divergence threshold (house caliber)
ABSORB_GATE = 1.05  # preregistered: absorbed-vs-conflict band
SEEDS = (0, 1, 2)
# preregistered recipe candidate (round-229 composition, round-252 use)
RECIPE = {"depth": 4, "lr_decay": 0.999, "weight_decay": 1e-4,
          "warmup_steps": 200, "k_train": 4}
A0_ANCHOR = 3.5581917762756348   # house default (round-269 arm A s0)
A1_ANCHOR = 3.3909592628479004   # recipe arm canonical s0 (round-252)
B0_ANCHOR = 2.0023648738861084   # candidate head (round-269 B arm s0)


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


def classify_compose(m_a0, m_a1, m_b0, m_b1,
                     absorb_gate: float = ABSORB_GATE,
                     norm_cap: float = NORM_CAP):
    """Preregistered round-279 verdict (pure, test-pinned)."""
    for tag, vals in (("A0", m_a0), ("A1", m_a1), ("B0", m_b0),
                      ("B1", m_b1)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > norm_cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "HOM_ARM_DIVERGED", {
                    "reason": f"cell {tag} seed {s} {state} "
                              f"(mse={m:.3e})"}
    mean = lambda v: sum(v) / len(v)
    ma0, ma1 = mean(m_a0), mean(m_a1)
    mb0, mb1 = mean(m_b0), mean(m_b1)
    ratio_on = mb1 / max(ma1, 1e-30)
    stats = {"mean_A0": ma0, "mean_A1": ma1, "mean_B0": mb0,
             "mean_B1": mb1, "ratio_head_on": ratio_on,
             "mses_A0": m_a0, "mses_A1": m_a1, "mses_B0": m_b0,
             "mses_B1": m_b1, "absorb_gate": absorb_gate}
    if mb1 < min(mb0, ma1):
        verdict = "COMPOSE_SYNERGIC"
        stats["decision"] = ("combination strictly beats both singles: "
                             "AMM-033 adoption note = joint default "
                             "(recipe + head together)")
    elif ratio_on <= absorb_gate:
        verdict = "COMPOSE_ABSORBED"
        stats["decision"] = ("the recipe absorbs the head's advantage: "
                             "either-or adoption note")
    else:
        verdict = "COMPOSE_CONFLICT"
        stats["decision"] = ("the candidate hurts under the recipe: "
                             "adoption note = recipe + default head")
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
                    default="benchmarks/physics_out_v02/recipe_head")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RECIPE-HEAD | M1 spring 2x2 recipe{{off,on}} x head{{default,"
          f"candidate}} recipe={RECIPE} (seeds {seeds}; round-279 "
          f"preregistration, gate-2 composition confirmation)",
          flush=True)

    cells = {c: [] for c in ("A0", "A1", "B0", "B1")}
    for seed in seeds:
        for cell in ("A0", "A1", "B0", "B1"):
            recipe_on = cell in ("A1", "B1")
            cand = cell in ("B0", "B1")
            depth = RECIPE["depth"] if recipe_on else 2
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=depth, dt=args.dt)
            # head swap AFTER the model draw (round-249/268 order);
            # axes: recipe knobs + head form (the 2x2 under test)
            if cand:
                model.ham = HomVStabHead(1, hidden_dim=args.hidden,
                                         depth=depth,
                                         context_dim=args.context_dim)
            if recipe_on:
                train_recipe(model, qs[tr], ps[tr], args.t_obs,
                             RECIPE["k_train"], args.train_steps,
                             args.lr, args.batch, seed,
                             lr_decay=RECIPE["lr_decay"],
                             weight_decay=RECIPE["weight_decay"],
                             warmup_steps=RECIPE["warmup_steps"])
            else:
                train_prefix(model, qs[tr], ps[tr], args.t_obs,
                             8, args.train_steps, args.lr, args.batch,
                             seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            cells[cell].append(res["rollout_mse"])
            print(f"  [cell {cell} seed {seed}] MSE "
                  f"{res['rollout_mse']:.4e}", flush=True)

    verdict, detail = classify_compose(cells["A0"], cells["A1"],
                                       cells["B0"], cells["B1"])
    sentinels = {
        "A0_seed0_house_default": {
            "expected": A0_ANCHOR, "actual": cells["A0"][0],
            "bitwise_match": cells["A0"][0] == A0_ANCHOR},
        "A1_seed0_recipe_round252": {
            "expected": A1_ANCHOR, "actual": cells["A1"][0],
            "bitwise_match": cells["A1"][0] == A1_ANCHOR},
        "B0_seed0_candidate_round269": {
            "expected": B0_ANCHOR, "actual": cells["B0"][0],
            "bitwise_match": cells["B0"][0] == B0_ANCHOR},
    }
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "HOM_ARM_DIVERGED",
                     "c_synergic": verdict == "COMPOSE_SYNERGIC",
                     "c_absorbed": verdict == "COMPOSE_ABSORBED",
                     "c_conflict": verdict == "COMPOSE_CONFLICT"},
        "gates": {"absorb_gate": ABSORB_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS), "recipe": RECIPE},
        "anchor": "2x2 = recipe{off,on} x head{default,candidate}; "
                  "three cells anchored bitwise to historical runs",
    }
    print(f"\nRECIPE-HEAD verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinels A0={sentinels['A0_seed0_house_default']['bitwise_match']} "
          f"A1={sentinels['A1_seed0_recipe_round252']['bitwise_match']} "
          f"B0={sentinels['B0_seed0_candidate_round269']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "recipe_head.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "recipe_head_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
