"""
benchmarks/residual_spec2_probe.py — RESIDUAL-SPEC-2 (round 246):
spectral-metric caliber validation, 3 seeds, on the M1 spring family
(E1 calibre).

Preregistered in PRD §19 round 245 BEFORE execution (AMM-027 pool
routing, last pool item: round 220 flagged "评估口径可补谱域指标" as
the RESIDUAL-family follow-up; extended by the round-241 eval-caliber
fixity clause). Round 219 profiled the default model's rollout residual
(93.2% of energy above the 2x omega_max band, PEAKED) and noted that
scalar MSE is dominated by the high-band residual, masking low-frequency
structural error. This round tests whether a spectral reading adds
DISCRIMINATION beyond scalar MSE, using two arms with a known scalar
contrast: A = default (k_train=8) vs B = k_train=4 (a RECIPE candidate
member, round 191 judged it 47% better at 1 seed).

Dual readings per trained model:
  scalar  — house evaluate at eval_k=100 (comparable to all historical
            numbers; sentinel A seed 0 = 3.5582)
  spectral— round-219 caliber: residual FFT power spectrum at k=200,
            high-frequency ratio above 2 x omega_max (hf_cut 0.0573
            cycles/step); low-band ratio = 1 - hf_ratio.
            Sentinel A seed 0 hf_ratio = 0.9324550504166047 (round-219
            replication).

Mechanical verdict (preregistered, report-type caliber validation):
  SPECTRA_ARM_DIVERGED (negative) — any reading non-finite or rollout
      > 1e6
  SPECTRA_REDUNDANT  — arm ordering agrees between calibers in >= 2/3
      seeds AND in aggregate: the spectral metric carries the same
      information as scalar MSE; caliber extension rejected, axis
      closes
  SPECTRA_INCREMENTAL — orderings disagree (or 2/3 disagree): the
      spectral metric adds composition discrimination scalar MSE lacks;
      candidate as a house secondary criterion (adoption would touch
      the house evaluate() contract => AMENDMENTS proposal, not
      self-merged)

Honest caliber note (carried in the verdict line): hf_ratio measures
error COMPOSITION, not magnitude — a model can have lower total error
yet a worse composition; that disagreement is exactly the increment
being tested. Family boundary: RESIDUAL family in-segment round 2 of 2
— family closes after this. Wording-clause r242: this docstring and
the PRD preregistration avoid writing queue-anchor literals other than
the ones this entry owns. Results JSON follows the audit schema
(top-level "results" key); meta carries exec_tier from probe_run.
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
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

NORM_CAP = 1e6  # preregistered: divergence threshold
SEEDS = (0, 1, 2)
SENTINEL_MSE = 3.5581917762756348        # house default A seed 0
SENTINEL_HF = 0.9324550504166047         # round-219 A seed 0 hf_ratio
DT = 0.1


def residual_hf_ratio(model, qs, ps, t_obs, k, omega_hi, dt):
    """Round-219 caliber: mean FFT power spectrum of the rollout
    residual; energy fraction above 2 x omega_max."""
    model.eval()
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(qs[:, :t_obs], ps[:, :t_obs], k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    fut = slice(t_obs - 1, t_obs + k)
    resid_q = qs_pred - qs[:, fut].permute(1, 0, 2)
    resid_p = ps_pred - ps[:, fut].permute(1, 0, 2)
    resid = torch.cat([resid_q, resid_p], dim=-1)
    spec = torch.fft.rfft(resid, dim=0).abs() ** 2
    spec = spec.mean(dim=(1, 2))
    freqs = torch.fft.rfftfreq(resid.shape[0], d=dt)
    total = spec.sum().item()
    hf_cut = 2.0 * omega_hi * dt / (2 * math.pi)
    hf = spec[freqs > hf_cut].sum().item()
    ratio = hf / max(total, 1e-30)
    peak_i = int(spec.argmax().item())
    return {"hf_ratio": ratio,
            "low_band_ratio": 1.0 - ratio,
            "dominant_peak_freq": freqs[peak_i].item(),
            "finite": bool(math.isfinite(ratio) and math.isfinite(total))}


def median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def classify_spectra(mses_a, mses_b, low_a, low_b,
                     cap: float = NORM_CAP, seeds=SEEDS):
    """Preregistered round-245 verdict (pure, test-pinned).

    mses_*: scalar rollout MSE per seed; low_*: low-band ratio per seed
    (higher = better composition). Orderings agree per seed when the
    same arm wins both calibers; >= 2/3 agreement (and aggregate)
    => REDUNDANT, else INCREMENTAL.
    """
    for tag, vals in (("A", mses_a), ("B", mses_b)):
        for s, m in zip(seeds, vals):
            if not math.isfinite(m) or m > cap:
                return "SPECTRA_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} scalar non-finite/"
                              f"diverged ({m:.3e})"}
    for tag, vals in (("A", low_a), ("B", low_b)):
        for s, v in zip(seeds, vals):
            if not math.isfinite(v):
                return "SPECTRA_ARM_DIVERGED", {
                    "reason": f"arm {tag} seed {s} spectral non-finite"}
    agree = sum(1 for ma, mb, la, lb in zip(mses_a, mses_b, low_a, low_b)
                if (ma < mb) == (la > lb))
    n = len(seeds)
    mean_a = sum(mses_a) / n
    mean_b = sum(mses_b) / n
    low_med_a = median(low_a)
    low_med_b = median(low_b)
    agg_agree = (mean_a < mean_b) == (low_med_a > low_med_b)
    stats = {"mses_A": mses_a, "mses_B": mses_b,
             "low_band_A": low_a, "low_band_B": low_b,
             "order_agreement": f"{agree}/{n}",
             "mean_mse_A": mean_a, "mean_mse_B": mean_b,
             "low_band_median_A": low_med_a,
             "low_band_median_B": low_med_b,
             "aggregate_agree": agg_agree,
             "caliber_note": "hf_ratio measures error COMPOSITION not "
                             "magnitude; disagreement is the increment "
                             "under test"}
    if agree >= 2 and agg_agree:
        verdict = "SPECTRA_REDUNDANT"
        stats["decision"] = ("spectral metric carries the same ordering "
                             "information as scalar MSE: caliber "
                             "extension rejected, axis closes")
    else:
        verdict = "SPECTRA_INCREMENTAL"
        stats["decision"] = ("spectral reading disagrees with scalar "
                             "ordering: composition discrimination beyond "
                             "scalar MSE; candidate as house secondary "
                             "criterion via AMENDMENTS proposal")
    return verdict, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=301)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--eval_k", type=int, default=100)
    ap.add_argument("--rollout_k", type=int, default=200)
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
    ap.add_argument("--train_tobs", default="8,24")
    ap.add_argument("--ktrain_arms", default="8,4")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/residual_spec_2")
    args = ap.parse_args()
    seeds = [int(x) for x in args.seeds.split(",")]
    k_arms = sorted(int(x) for x in args.ktrain_arms.split(","))

    g = torch.Generator().manual_seed(0)
    qs, ps, om = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                            args.dt, 1, args.omega_lo, args.omega_hi, g,
                            device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RESIDUAL-SPEC-2 | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} "
          f"steps={args.train_steps} ktrain_arms={k_arms} "
          f"(seeds {seeds}; scalar+spectral dual caliber; round-245 "
          f"preregistration)", flush=True)

    mses = {k: [] for k in k_arms}
    lows = {k: [] for k in k_arms}
    hfs = {k: [] for k in k_arms}
    for k_train in k_arms:
        for seed in seeds:
            torch.manual_seed(seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden,
                depth=2, dt=args.dt)
            train_prefix(model, qs[tr], ps[tr], args.t_obs, k_train,
                         args.train_steps, args.lr, args.batch, seed)
            res = evaluate(model, qs[ev], ps[ev], om[ev], args.t_obs,
                           args.eval_k, args.dt)
            sp = residual_hf_ratio(model, qs[ev], ps[ev], args.t_obs,
                                   args.rollout_k, args.omega_hi, args.dt)
            mses[k_train].append(res["rollout_mse"])
            lows[k_train].append(sp["low_band_ratio"])
            hfs[k_train].append(sp["hf_ratio"])
            print(f"  [k_train {k_train:>2} seed {seed}] MSE "
                  f"{res['rollout_mse']:.4e} | hf_ratio "
                  f"{sp['hf_ratio']:.4f} | peak "
                  f"{sp['dominant_peak_freq']:.3f}", flush=True)

    verdict, detail = classify_spectra(
        mses[k_arms[0]], mses[k_arms[1]],
        lows[k_arms[0]], lows[k_arms[1]], seeds=seeds)
    sentinels = {
        "A_mse_seed0": {"expected": SENTINEL_MSE,
                        "actual": mses[k_arms[0]][0],
                        "bitwise_match":
                            mses[k_arms[0]][0] == SENTINEL_MSE},
        "A_hf_seed0_round219": {"expected": SENTINEL_HF,
                                "actual": hfs[k_arms[0]][0],
                                "bitwise_match":
                                    hfs[k_arms[0]][0] == SENTINEL_HF}}
    results = {
        "verdict": verdict,
        "verdict_detail": detail,
        "spectral_per_arm": {f"k{k}": {"hf_ratio": hfs[k],
                                       "dominant_peak":
                                           None} for k in k_arms},
        "sentinels": sentinels,
        "criteria": {"c_diverged": verdict == "SPECTRA_ARM_DIVERGED",
                     "c_redundant": verdict == "SPECTRA_REDUNDANT",
                     "c_incremental": verdict == "SPECTRA_INCREMENTAL"},
        "gates": {"norm_cap": NORM_CAP, "seeds": list(seeds),
                  "ktrain_arms": k_arms},
        "anchor": "A (default k8) seed0 MSE = 3.5582 (house sentinel) + "
                  "A seed0 hf_ratio = 0.9325 (round-219 replication)"},
    print(f"\nRESIDUAL-SPEC-2 verdict {verdict} | "
          f"{detail['decision']} | sentinels "
          f"{sentinels['A_mse_seed0']['bitwise_match']}/"
          f"{sentinels['A_hf_seed0_round219']['bitwise_match']}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "residual_spec_2.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "residual_spec2_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
