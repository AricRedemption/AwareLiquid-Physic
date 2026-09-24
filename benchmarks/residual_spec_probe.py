"""
benchmarks/residual_spec_probe.py — RESIDUAL-SPEC (round 219): spectral
diagnosis of the rollout residual on the M1 spring family.

Preregistered in PRD §19 round 219 BEFORE execution. Scan §51: scalar
MSE hides the FREQUENCY STRUCTURE of the error — a spectral breakdown
directly indicates the error mechanism (phase drift = peak broadening
around the true frequency; amplitude error = peak height mismatch;
nonlinearity = harmonics; noise = broadband floor).

This is a DIAGNOSTIC round (no pass/fail gate): train the default
configuration (prefix hidden64 ctx=8, 2000 steps, E1 pool), roll out
k=200 on 128 held-out trajectories, average the per-trajectory FFT
power spectrum of the residual, and report:
  * dominant residual peak location vs the true-frequency band
    (omega in [0.7, 1.8] -> f in [0.11, 0.29] cycles/step at dt=0.1)
  * high-frequency energy ratio (energy above 2 x omega_max = 3.6
    cycles/step, over total residual energy)
  * spectral profile classification (peaked / broadband)

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
from benchmarks.liquid_physics_eval import train as train_prefix  # noqa: E402
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402

NORM_CAP = 1e6  # preregistered: divergence threshold
DT = 0.1


def residual_spectrum(model, qs, ps, t_obs, k):
    """Mean FFT power spectrum of the rollout residual (q+p combined),
    plus the residual time series stats. Returns (spectrum, freqs,
    finite, qnorm)."""
    model.eval()
    q_obs = qs[:, :t_obs]
    p_obs = ps[:, :t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    fut = slice(t_obs - 1, t_obs + k)
    q_true = qs[:, fut].permute(1, 0, 2)
    p_true = ps[:, fut].permute(1, 0, 2)
    resid_q = (qs_pred - q_true)          # (k+1, B, dim)
    resid_p = (ps_pred - p_true)
    resid = torch.cat([resid_q, resid_p], dim=-1)   # (k+1, B, 2*dim)
    qnorm = qs_pred.norm().item()
    # mean power spectrum across trajectories/dims
    spec = torch.fft.rfft(resid, dim=0).abs() ** 2   # (k//2+1, B, 2dim)
    spec = spec.mean(dim=(1, 2))
    freqs = torch.fft.rfftfreq(resid.shape[0], d=DT)
    finite = bool(torch.isfinite(spec).all())
    return spec.numpy().tolist(), freqs.numpy().tolist(), finite, qnorm


def spectral_readings(freqs, spec, omega_hi, dt):
    """Preregistered readings: dominant peak, high-frequency energy
    ratio (> 2 x omega_max band), and a peaked-vs-broadband call.
    Frequencies are in cycles/step (= omega * dt / 2pi for the truth)."""
    total = sum(spec)
    hf_cut = 2.0 * omega_hi * dt / (2 * math.pi)
    hf = sum(s for f, s in zip(freqs, spec) if f > hf_cut)
    hf_ratio = hf / max(total, 1e-30)
    peak_i = max(range(len(spec)), key=lambda i: spec[i])
    width = [s for f, s in zip(freqs, spec)
             if abs(f - freqs[peak_i]) <= 0.05]
    peak_frac = sum(width) / max(total, 1e-30)
    shape = "PEAKED" if peak_frac >= 0.5 else "BROADBAND"
    return {"dominant_peak_freq": freqs[peak_i],
            "hf_ratio": hf_ratio,
            "peak_frac": peak_frac,
            "shape": shape,
            "hf_cut": hf_cut}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=301,
                    help="must cover t_obs + rollout_k + 1 (round-162 "
                         "lesson)")
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
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
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/residual_spec")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    qs, ps, _ = gen_spring(args.n_train + args.n_eval, args.gen_steps,
                           args.dt, 1, args.omega_lo, args.omega_hi, g,
                           device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"RESIDUAL-SPEC | M1 spring omega[{args.omega_lo},"
          f"{args.omega_hi}] hidden={args.hidden} steps={args.train_steps} "
          f"rollout k={args.rollout_k} (seed {args.seed}, 1-seed "
          f"screening)", flush=True)

    torch.manual_seed(args.seed)
    model = LiquidHamiltonianModel(
        1, d_model=args.d_model, context_dim=args.context_dim,
        n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
        dt=args.dt)
    train_prefix(model, qs[tr], ps[tr], args.t_obs, args.k_train,
                 args.train_steps, args.lr, args.batch, args.seed)

    spec, freqs, finite, qnorm = residual_spectrum(
        model, qs[ev], ps[ev], args.t_obs, args.rollout_k)

    if not finite or qnorm > NORM_CAP:
        results = {
            "verdict": "RESIDUAL_UNRESOLVABLE",
            "verdict_detail": {"reason": "residual spectrum non-finite "
                                         "or q-norm above cap: preregistered "
                                         "negative branch"},
            "criteria": {"c_unresolvable": True},
            "gates": {"norm_cap": NORM_CAP},
        }
        print("\nRESIDUAL-SPEC verdict RESIDUAL_UNRESOLVABLE", flush=True)
    else:
        readings = spectral_readings(freqs, spec, args.omega_hi, args.dt)
        verdict = "RESIDUAL_PROFILED"
        results = {
            "spectrum_freqs": freqs,
            "spectrum_power": spec,
            "rollout_qnorm": qnorm,
            "verdict": verdict,
            "verdict_detail": {
                "readings": readings,
                "criterion": "diagnostic round: spectral readings reported "
                             "(no pass/fail gate per preregistration)"},
            "criteria": {"c_profiled": True},
            "gates": {"norm_cap": NORM_CAP},
        }
        print(f"\nRESIDUAL-SPEC verdict {verdict} | peak "
              f"{readings['dominant_peak_freq']:.3f} cyc/step | "
              f"hf_ratio {readings['hf_ratio']:.3f} | shape "
              f"{readings['shape']}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "residual_spec.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "residual_spec_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
