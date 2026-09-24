"""
benchmarks/spectral_dt_probe.py — SPECTRAL-DT (round 162): the omega x dt
interaction matrix on single-frequency spring pools.

Preregistered in PRD §19 round 162 BEFORE execution. Scan §39 (Fridovich-
Keil NeurIPS 2022 frequency-as-operational-variable; Kiessling AAAI 2022
computable-definition grid coupling; Bartolucci 2023 aliasing): does the
HIGH-frequency arm degrade super-proportionally at COARSE training dt
(spectral-bias x Nyquist interaction), or do omega and dt act
independently?

Design: single-frequency pools (gen_spring with omega_lo=omega_hi, the
round-120 control-arm method) on a 3x3 grid — omega in {1,2,4} x
training dt in {0.05,0.1,0.2}, prefix hidden64 2000 steps each. Eval =
fixed PHYSICAL horizon T=10 (k = 10/dt) rollout MSE on held-out
trajectories (E1 calibre, ctx-inferred omega). omega*dt in [0.05,0.8]
with per-cell Nyquist status annotated (the §39.2 "cannot learn" vs
"cannot measure" trap).

Mechanical verdict (preregistered):
  INTERACTION_UNRESOLVABLE (negative) — |R4-R1|/max(R1,1) < 0.20, where
      R_omega = mse(omega, dt=0.2)/mse(omega, dt=0.05).
  INTERACTION_RESOLVED — R4 exceeds R1 by >= 20%.
  Cell failure (non-finite/divergent rollout > 1e6) takes precedence as
  the negative branch.

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
    evaluate, train as train_prefix)
from benchmarks.sample_efficiency_eval import gen_spring  # noqa: E402

INTERACTION_GATE = 0.20  # preregistered: relative excess of R4 over R1
DIVERGENCE_CAP = 1e6     # preregistered: cell failure threshold


def classify_interaction(cells, r_hi: float, r_lo: float,
                         gate: float = INTERACTION_GATE,
                         cap: float = DIVERGENCE_CAP):
    """Preregistered round-162 verdict (pure, test-pinned). cells =
    list of (omega, dt, mse) tuples."""
    for omega, dt, mse in cells:
        if not math.isfinite(mse) or mse > cap:
            return "CELL_FAILURE", {
                "reason": f"cell omega={omega} dt={dt} mse={mse:.3e} "
                          f"non-finite or > {cap:.0e} (preregistered "
                          f"negative branch)"}
    excess = (r_hi - r_lo) / max(r_lo, 1.0)
    if excess >= gate:
        return "INTERACTION_RESOLVED", {
            "r_hi": r_hi, "r_lo": r_lo, "excess": excess,
            "criterion": f"high-frequency coarse/fine ratio exceeds low-"
                         f"frequency ratio by {excess:.1%} >= {gate:.0%}: "
                         f"omega-dt interaction resolvable"}
    return "INTERACTION_UNRESOLVABLE", {
        "r_hi": r_hi, "r_lo": r_lo, "excess": excess,
        "criterion": f"interaction excess {excess:.1%} < {gate:.0%}: "
                     f"omega-dt interaction not resolvable (frequency "
                     f"main effect may still hold; this verdict is about "
                     f"the interaction only)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=128)
    ap.add_argument("--gen_steps", type=int, default=301,
                    help="truth length; must cover t_obs + T/dt_max + 1 "
                         "(finest dt => largest k)")
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--train_steps", type=int, default=2000)
    ap.add_argument("--horizon_T", type=float, default=10.0,
                    help="fixed physical horizon; k = T/dt")
    ap.add_argument("--omegas", default="1.0,2.0,4.0")
    ap.add_argument("--dts", default="0.05,0.1,0.2")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/spectral_dt")
    args = ap.parse_args()
    omegas = [float(x) for x in args.omegas.split(",")]
    dts = [float(x) for x in args.dts.split(",")]

    print(f"SPECTRAL-DT | omega{omegas} x dt{dts}, T={args.horizon_T} "
          f"physical horizon, prefix {args.train_steps} steps "
          f"(seed {args.seed}, 1-seed screening)", flush=True)

    cells = []
    for omega in omegas:
        for dt in dts:
            g = torch.Generator().manual_seed(args.seed)
            pool_qs, pool_ps, pool_om = gen_spring(
                args.n_train + args.n_eval, args.gen_steps, dt, 1,
                omega, omega, g, device=args.device)
            tr, ev = slice(0, args.n_train), slice(args.n_train, None)
            torch.manual_seed(args.seed)
            model = LiquidHamiltonianModel(
                1, d_model=args.d_model, context_dim=args.context_dim,
                n_scales=args.n_scales, hidden_dim=args.hidden, depth=2,
                dt=dt)
            train_prefix(model, pool_qs[tr], pool_ps[tr], args.t_obs,
                         args.k_train, args.train_steps, args.lr,
                         args.batch, args.seed)
            k_eval = int(round(args.horizon_T / dt))
            res = evaluate(model, pool_qs[ev], pool_ps[ev],
                           pool_om[ev], args.t_obs, k_eval, dt)
            mse = res["rollout_mse"]
            nyq = omega * dt / 2.0
            cells.append({"omega": omega, "dt": dt, "k_eval": k_eval,
                          "rollout_mse": mse,
                          "omega_dt": omega * dt,
                          "nyquist_fraction": nyq})
            print(f"  [omega {omega:.1f} dt {dt:.2f}] k={k_eval:>3} "
                  f"rollout MSE {mse:.4e} | omega*dt {omega * dt:.2f} "
                  f"(Nyq frac {nyq:.2f})", flush=True)

    by = {(c["omega"], c["dt"]): c["rollout_mse"] for c in cells}
    dt_coarse, dt_fine = max(dts), min(dts)
    r_omega = {o: by[(o, dt_coarse)] / max(by[(o, dt_fine)], 1e-30)
               for o in omegas}
    r_hi, r_lo = r_omega[4.0], r_omega[1.0]

    verdict, detail = classify_interaction(
        [(c["omega"], c["dt"], c["rollout_mse"]) for c in cells],
        r_hi, r_lo)
    results = {
        "cells": cells,
        "ratios": {"r_omega4": r_hi, "r_omega1": r_lo},
        "verdict": verdict,
        "verdict_detail": detail,
        "criteria": {
            "c_cell_failure": verdict == "CELL_FAILURE",
            "c_interaction": verdict == "INTERACTION_RESOLVED",
            "c_unresolvable": verdict == "INTERACTION_UNRESOLVABLE"},
        "gates": {"interaction_gate": INTERACTION_GATE,
                  "divergence_cap": DIVERGENCE_CAP},
    }
    print(f"\nSPECTRAL-DT verdict {verdict} | "
          f"{detail.get('criterion', detail.get('reason', ''))}",
          flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "spectral_dt.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "spectral_dt_probe",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
