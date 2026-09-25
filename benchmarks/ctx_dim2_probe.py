"""
benchmarks/ctx_dim2_probe.py — CTX-DIM-2 (round 239): 3-seed ctx_dim
1-vs-8 confirmation + omega-semantic recalibration diagnostic on the
M1 spring family (E1 calibre).

Preregistered in PRD §19 round 238 BEFORE execution (AMM-027 pool
routing: the round-226 CTX-DIM-LADDER verdict line named the ctx_dim
follow-up — "派发协议字段=ctx_dim 候选(多参数族需重标定=族后续候选
1/2)" — and the round-227 RECIPE entry held ctx_dim=1 out of the
composite pending inference-semantic recalibration). Round 226 (1-seed)
found ctx_dim=1 optimal by 80% over the default 8 — the largest
detected configuration error; this round upgrades that contrast to the
AMM-028 gate-3 3-seed protocol and adds a report-only semantic
diagnostic.

Mechanical verdict (preregistered, 3-seed mean ratio r = mean_B/mean_A,
arm A = ctx_dim 8 default, arm B = ctx_dim 1):
  CTX_ARM_DIVERGED (negative) — any arm/seed non-finite or rollout
      > 1e6: that arm unusable, recorded as such
  CTX2_CONFIRM   — r < 0.95: ctx_dim=1 advantage confirmed at 3-seed
  CTX2_UNRESOLVED — 0.95 <= r <= 1.05: round-226 single-seed 80%
      reading downgraded (presentation-layer revision at merge time)
  CTX2_REVERSED  — r > 1.05: reversal recorded as such

Semantic diagnostic (report-only, RESIDUAL-SPEC precedent — no fail
gate): after training, infer ctx from the true prefix of each held-out
trajectory (k=1 forward, third return) and measure how faithfully the
context carries the true omega: per channel |Pearson| between
ctx[:, c] and omega across the 128 held-out trajectories (arm B has
one channel; arm A reports the max over its 8 channels), plus a
closed-form linear readout R^2 predicting omega from the ctx vector.
Median + IQR across the 3 seeds recorded per arm. Statistic
refinement vs the round-238 wording ("逐轨 Pearson 相关") is
caliber-noted: per-trajectory pairs are single points, so correlation
runs across trajectories within a seed — honestly recorded here and
in the verdict line. High correlation => omega-faithful (recalibration
concern lifted, recipe annotation upgraded); low => semantic carrier
is not omega (concern stands, parked annotation).

The verdict line carries per-seed values, direction-consistency count
(# seeds with B < A) and per-arm seed spread (AMM-028 gate-3).
Cross-validation anchors: arm A seed 0 = 3.5581917762756348 (house
default, rounds 175/191/223/226 + RECIPE-SYNTHESIS) and arm B seed 0 =
1.9746309518814087 (round-226 ctx_dim=1 arm), both bit-for-bit.
Parameter-count note carries over from round 226 (ctx8 12694 vs ctx1
11903: -6.2% params, interference not capacity mechanism per §53.1).
Family boundary: CTX-DIM family in-segment round 2 of 2 — family
closes after this. Results JSON follows the audit schema (top-level
"results" key); meta carries exec_tier passthrough from probe_run.
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

NORM_CAP = 1e6      # preregistered: divergence threshold
CONFIRM_GATE = 0.95  # preregistered: ratio < gate => ctx1 confirmed
REVERSE_GATE = 1.05  # preregistered: ratio > gate => reversal
SEEDS = (0, 1, 2)    # preregistered: AMM-028 gate-3 3-seed minimum
SENTINEL_A = 3.5581917762756348   # house default ctx8 arm A seed 0
SENTINEL_B = 1.9746309518814087   # round-226 ctx_dim=1 arm seed 0


def train_ctx(model, qs, ps, t_obs, k_train, steps, lr, batch, seed):
    """House prefix loop, verbatim rng consumption (sentinel clause
    r181): constant lr 3e-3, batch 64, k_train 8, 2000 steps."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
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
    return loss.item()


def infer_ctx(model, qs, ps, t_obs):
    """Third forward return = inferred context per held-out trajectory
    (prefix-only, k=1; enable_grad keeps the symplectic-head internals
    live per the round-2 playbook pitfall)."""
    model.eval()
    q_obs = qs[:, :t_obs]; p_obs = ps[:, :t_obs]
    with torch.enable_grad():
        _, _, ctx = model(q_obs, p_obs, 1)
    return ctx.detach()


def omega_semantic(ctx, omega):
    """Per-channel |Pearson| between ctx channel and omega across
    trajectories + closed-form linear readout R^2 (all channels)."""
    c = ctx.float()
    w = omega.float()
    cc = c - c.mean(0, keepdim=True)
    ww = w - w.mean()
    num = (cc * ww.unsqueeze(1)).sum(0)
    den = torch.sqrt((cc ** 2).sum(0) * (ww ** 2).sum() + 1e-30)
    corr_c = (num / den).abs()
    # closed-form least squares omega ~ [1, ctx]: R^2 on the same data
    X = torch.cat([torch.ones(len(c), 1), c], dim=1)
    beta = torch.linalg.lstsq(X, w.unsqueeze(1)).solution
    resid = w.unsqueeze(1) - X @ beta
    ss_res = (resid ** 2).sum()
    ss_tot = (ww ** 2).sum() + 1e-30
    r2 = (1 - ss_res / ss_tot).item()
    return {"corr_per_channel": [v for v in corr_c.tolist()],
            "max_abs_corr": max(corr_c.tolist()),
            "linear_readout_r2": r2}


def median_iqr(vals):
    s = sorted(vals)
    n = len(s)
    med = s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])
    q1 = s[max(0, n // 4)]
    q3 = s[min(n - 1, (3 * n) // 4)]
    return {"median": med, "iqr": q3 - q1, "values": vals}


def classify_ctx2(mses_a, mses_b,
                  confirm_gate: float = CONFIRM_GATE,
                  reverse_gate: float = REVERSE_GATE,
                  cap: float = NORM_CAP):
    """Preregistered round-238 verdict (pure, test-pinned)."""
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(SEEDS, vals):
            if not math.isfinite(m) or m > cap:
                state = "non-finite" if not math.isfinite(m) else "diverged"
                return "CTX_ARM_DIVERGED", {
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
    if ratio < confirm_gate:
        verdict = "CTX2_CONFIRM"
        stats["decision"] = ("ctx_dim=1 advantage confirmed at 3-seed; "
                             "round-226 upgrade stands")
    elif ratio <= reverse_gate:
        verdict = "CTX2_UNRESOLVED"
        stats["decision"] = ("ctx contrast not robust at 3-seed: "
                             "round-226 single-seed 80% reading "
                             "downgraded (presentation-layer revision "
                             "at merge time)")
    else:
        verdict = "CTX2_REVERSED"
        stats["decision"] = ("ctx reversal at 3-seed: round-226 "
                             "reading reversed, ctx axis stays at "
                             "default 8")
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
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/ctx_dim_2")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"CTX-DIM-2 | M1 spring omega[{args.omega_lo},{args.omega_hi}] "
          f"hidden={args.hidden} steps={args.train_steps} "
          f"A=ctx8(default) vs B=ctx1 (seeds {seeds}, AMM-028 g3 "
          f"3-seed + omega-semantic diagnostic; round-238 "
          f"preregistration)", flush=True)

    arms = {"A": [], "B": []}
    sem = {"A": [], "B": []}
    for seed in seeds:
        for tag, cd in (("A", 8), ("B", 1)):
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=cd,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            train_ctx(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                      args.train_steps, args.lr, args.batch, seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            arms[tag].append(res["rollout_mse"])
            s = omega_semantic(infer_ctx(model, qs[ev], ps[ev],
                                         args.t_obs), om[ev])
            sem[tag].append(s)
            print(f"  [arm {tag} seed {seed}] rollout MSE "
                  f"{res['rollout_mse']:.4e} | omega-corr "
                  f"{s['max_abs_corr']:.3f} r2 "
                  f"{s['linear_readout_r2']:.3f}", flush=True)

    verdict, detail = classify_ctx2(arms["A"], arms["B"])
    semantic = {
        "caliber_note": ("per-channel |Pearson| across held-out "
                         "trajectories within each seed; median+IQR "
                         "across seeds; arm A reports max over 8 "
                         "channels; report-only, no fail gate"),
        "A_ctx8": {"max_abs_corr": median_iqr(
                       [s["max_abs_corr"] for s in sem["A"]]),
                   "linear_readout_r2": median_iqr(
                       [s["linear_readout_r2"] for s in sem["A"]])},
        "B_ctx1": {"max_abs_corr": median_iqr(
                       [s["max_abs_corr"] for s in sem["B"]]),
                   "linear_readout_r2": median_iqr(
                       [s["linear_readout_r2"] for s in sem["B"]])},
        "per_seed": sem}
    sentinels = {
        "arm_A_seed0": {"expected": SENTINEL_A,
                        "actual": arms["A"][0],
                        "bitwise_match": arms["A"][0] == SENTINEL_A},
        "arm_B_seed0": {"expected": SENTINEL_B,
                        "actual": arms["B"][0],
                        "bitwise_match": arms["B"][0] == SENTINEL_B}}
    results = {
        "arms": {"A_ctx8": arms["A"], "B_ctx1": arms["B"]},
        "verdict": verdict,
        "verdict_detail": detail,
        "omega_semantic": semantic,
        "sentinels": sentinels,
        "criteria": {
            "c_diverged": verdict == "CTX_ARM_DIVERGED",
            "c_confirm": verdict == "CTX2_CONFIRM",
            "c_unresolved": verdict == "CTX2_UNRESOLVED",
            "c_reversed": verdict == "CTX2_REVERSED"},
        "gates": {"confirm_gate": CONFIRM_GATE,
                  "reverse_gate": REVERSE_GATE, "norm_cap": NORM_CAP,
                  "seeds": list(SEEDS)},
        "anchor": "arm A seed 0 = 3.5582 (house default sentinel) + "
                  "arm B seed 0 = 1.9746 (round-226 ctx_dim=1 arm)"},
    print(f"\nCTX-DIM-2 verdict {verdict} | "
          f"{detail.get('decision', detail.get('reason', ''))} | "
          f"sentinels A={sentinels['arm_A_seed0']['bitwise_match']} "
          f"B={sentinels['arm_B_seed0']['bitwise_match']} | "
          f"omega-corr B median="
          f"{semantic['B_ctx1']['max_abs_corr']['median']:.3f}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "ctx_dim_2.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "ctx_dim2_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
