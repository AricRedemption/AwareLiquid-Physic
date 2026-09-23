"""
benchmarks/r1d_mode_scan.py — R1D-MODE-SCAN (round 122): the SB-NAMING
falsifiable prophecy, per-ctx-mode extraction scan.

Preregistered in PRD §19 round 122 BEFORE execution (round 78 registered the
prophecy and its negative branch): IF the spectral-bias naming holds, the
per-mode EXTRACTION QUALITY of the liquid operator's inferred context
degrades MONOTONICALLY with mode ordinal — low-order modes are extracted
well, high-order modes poorly. Flat / anti-monotone => the naming is
downgraded to a weak hypothesis, R1d is withdrawn, and the §12.3 fourth
route is deleted (mechanically, as preregistered in round 78).

Protocol = args copied verbatim from the e1_final product (same pool, same
seed 0, same 300-step semigroup training — same generation as the oracle
0.0148 record), 1 training seed (screening tier; the registered 3-seed
final stays PARKED per AMM-024).

Primary metric (prophecy-bearing): per-ctx-coordinate normalized extraction
error e_j = RMSE(pred_j - true_j) / std(true_j) from the field_context_probe
linear readout convention (fit on the first eval half, scored on the second).
Statistic: Spearman rho between mode ordinal (1..4, sin coordinates 0,2,4,6)
and e_j. cos coordinates are family-degenerate (sin-only truth, std ~ 0) and
are reported raw but never ranked.

Scope qualifier (preregistered): the truth family's amplitude decays as 1/m
(datasets._smooth_field), so frequency and amplitude are entangled — the
normalization removes the amplitude scale, but observation SNR still varies
with amplitude; that is part of what extraction quality means on this family.

Secondary metric (recorded, NOT gate-bearing — same confound): per-mode
functional attribution Delta_m = MSE(all-inferred ctx) - MSE(hybrid ctx with
only mode m's sin coordinate set to the oracle value), plus the total
oracle-recoverable gap.

Results JSON follows the audit schema: top-level "results" key required.
meta carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import os
import sys
from types import SimpleNamespace

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_wave_1d_inhomogeneous  # noqa: E402
from awareliquid_physics.observability import (  # noqa: E402
    rollout_mse_stderr, run_metadata)
from benchmarks.field_eval import (  # noqa: E402
    make_models, oracle_ctx_matrix, train_semigroup)


def spearman_rho(x, y):
    """Spearman rank correlation with average ranks (no scipy). Ties get the
    average rank; with n=4 ordinals there are no ties in x."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx = sum(rx) / len(rx)
    my = sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx)
           * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den > 0 else 0.0


def rollout_mse_with_ctx(model, qs, ps, ctx, t_obs, eval_k):
    """evaluate()'s convention with an EXPLICIT context: free-running rollout
    from the prefix end, q+p point-mean MSE against truth."""
    model.eval()
    q_obs, p_obs = qs[:, :t_obs], ps[:, :t_obs]
    q0, p0 = q_obs[:, -1], p_obs[:, -1]
    with torch.enable_grad():
        qs_pred, ps_pred = model.rollout(q0, p0, ctx, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2, 3)
    p_true = ps[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2, 3)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    return mse, rollout_mse_stderr(qs_pred, q_true, ps_pred, p_true)


def per_mode_extraction(model, qs, ps, coeffs, t_obs):
    """field_context_probe's linear-readout convention, kept per-COORDINATE:
    fit ctx->coeffs on the first eval half, score on the second.
    Returns per-coordinate raw corr and normalized error
    e_j = RMSE(pred_j - true_j) / std(true_j)."""
    model.eval()
    n = qs.shape[0]
    with torch.enable_grad():
        _, _, ctx = model(qs[:, :t_obs], ps[:, :t_obs], 1)
    ctx = ctx.detach().reshape(n, -1).cpu()
    y = coeffs.detach().reshape(n, -1).cpu()
    n_half = n // 2
    xa = torch.cat([ctx[:n_half], torch.ones(n_half, 1)], dim=1)
    xb = torch.cat([ctx[n_half:], torch.ones(n - n_half, 1)], dim=1)
    sol = torch.linalg.lstsq(xa, y[:n_half]).solution
    y_hat = xb @ sol
    y_true = y[n_half:]
    out = []
    for j in range(y_true.shape[1]):
        c = torch.corrcoef(torch.stack([y_hat[:, j], y_true[:, j]]))[0, 1]
        std = y_true[:, j].std().item()
        e = ((y_hat[:, j] - y_true[:, j]) ** 2).mean().sqrt().item() \
            / std if std > 1e-6 else float("nan")
        out.append({"coord": j, "corr": (c.item() if torch.isfinite(c)
                                         else float("nan")),
                    "err_normalized": e, "target_std": std})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    # --- protocol copied verbatim from e1_final product args ---
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--gen_steps", type=int, default=120)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=80)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--c_eval", type=float, default=1.0)
    ap.add_argument("--c_var", type=float, default=0.5)
    ap.add_argument("--n_nodes", type=int, default=32)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--modes", type=int, default=12)
    ap.add_argument("--width", type=int, default=32)
    ap.add_argument("--fno_depth", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--reflect_pad", type=int, default=8)
    ap.add_argument("--train_steps", type=int, default=300)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    # --- mode-scan gates (preregistered three-tier, n=4 rank granularity) ---
    ap.add_argument("--rho_pass", type=float, default=0.6,
                    help="preregistered PASS threshold: rho >= this supports "
                         "the prophecy at screening tier")
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/r1d_mode_scan")
    args = ap.parse_args()

    g = torch.Generator(device=args.device).manual_seed(args.seed)
    n = args.n_train + args.n_eval
    qs, ps, cfields = gen_wave_1d_inhomogeneous(
        n, args.gen_steps, args.dt, args.n_nodes,
        c_mean=args.c_eval, c_var=args.c_var, generator=g,
        device=args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    print(f"R1D-MODE-SCAN | inhomogeneous N={args.n_nodes} "
          f"c(x)={args.c_eval}+/-{args.c_var} steps={args.train_steps} "
          f"seed {args.seed} (e1_final protocol, 1-seed screening)",
          flush=True)

    model_args = SimpleNamespace(
        d_model=args.d_model, context_dim=args.context_dim, n_scales=4,
        modes=args.modes, width=args.width, fno_depth=args.fno_depth,
        hidden=args.hidden, dt=args.dt, reflect_pad=args.reflect_pad,
        pool="mean", device=args.device)
    liquid, _static = make_models(model_args, args.seed)
    floss = train_semigroup(liquid, qs[tr], ps[tr], args.t_obs, args.k_train,
                            args.train_steps, args.lr, args.batch, args.seed,
                            lr_decay=args.lr_decay)
    print(f"  [liquid] train_loss {floss:.4e}", flush=True)

    coeffs = oracle_ctx_matrix(cfields, args.context_dim,
                               scale=args.c_var).cpu()
    per_coord = per_mode_extraction(liquid, qs[ev], ps[ev], coeffs[ev],
                                    args.t_obs)

    # sin coordinates 0,2,4,6 <-> modes 1..4 (oracle_ctx_matrix interleaves
    # [sin1, cos1, sin2, cos2, ...]); cos coords are family-degenerate
    # (sin-only truth) — reported raw, never ranked.
    sin_modes, sin_errs = [], []
    for m in range(args.context_dim // 2):
        coord = per_coord[2 * m]
        sin_modes.append(m + 1)
        sin_errs.append(coord["err_normalized"])
    rho = spearman_rho(sin_modes, sin_errs)
    print("  per-sin-mode normalized extraction error:", flush=True)
    for m, e in zip(sin_modes, sin_errs):
        print(f"    mode {m}: e={e:.4f}", flush=True)
    print(f"  Spearman rho(ordinal, err) = {rho:+.3f}", flush=True)

    # Secondary (NOT gate-bearing): per-mode functional attribution.
    model_eval = qs[ev]
    model_eval_p = ps[ev]
    liquid.eval()
    with torch.enable_grad():
        _, _, ctx_inf = liquid(model_eval[:, :args.t_obs],
                               model_eval_p[:, :args.t_obs], 1)
    ctx_inf = ctx_inf.detach()
    ctx_orc = oracle_ctx_matrix(cfields[ev], args.context_dim,
                                scale=args.c_var).to(ctx_inf.device)
    mse_inf, se_inf = rollout_mse_with_ctx(liquid, model_eval, model_eval_p,
                                           ctx_inf, args.t_obs, args.eval_k)
    mse_orc, _ = rollout_mse_with_ctx(liquid, model_eval, model_eval_p,
                                      ctx_orc, args.t_obs, args.eval_k)
    attributions = {}
    for m in range(args.context_dim // 2):
        coord = 2 * m
        ctx_h = ctx_inf.clone()
        ctx_h[:, coord] = ctx_orc[:, coord]
        mse_h, _ = rollout_mse_with_ctx(liquid, model_eval, model_eval_p,
                                        ctx_h, args.t_obs, args.eval_k)
        attributions[f"mode_{m + 1}"] = mse_inf - mse_h
        print(f"    attribution mode {m + 1}: {mse_inf - mse_h:+.4e}",
              flush=True)
    print(f"  MSE all-inferred {mse_inf:.4e} | all-oracle {mse_orc:.4e} "
          f"(recoverable gap {mse_inf - mse_orc:+.4e})", flush=True)

    # Preregistered three-tier gate (PRD §19 round 122) — mechanical.
    criteria = {
        "c1_prophecy_flat": rho <= 0.0,
        "c2_weak_trend": 0.0 < rho < args.rho_pass,
    }
    if criteria["c1_prophecy_flat"]:
        verdict = "NEGATIVE"
    elif criteria["c2_weak_trend"]:
        verdict = "WEAK"
    else:
        verdict = "PASS"
    results = {
        "per_coordinate": per_coord,
        "sin_mode_ordinals": sin_modes,
        "sin_mode_err_normalized": sin_errs,
        "spearman_rho_ordinal_vs_err": rho,
        "attribution_per_mode": attributions,
        "mse_all_inferred": mse_inf,
        "mse_all_oracle": mse_orc,
        "mse_all_inferred_stderr": se_inf,
        "train_loss": floss,
        "criteria": criteria,
        "gates": {"rho_pass": args.rho_pass},
        "verdict_semantics": "PASS=rho>=gate prophecy supported at screening; "
                             "NEGATIVE=rho<=0 preregistered negative branch "
                             "(naming downgraded, R1d withdrawn, route 4 "
                             "deleted); WEAK=middle, parked 3-seed final "
                             "adjudicates",
    }
    print(f"\nR1D-MODE-SCAN verdict {verdict} | rho {rho:+.3f} "
          f"| criteria {criteria}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "r1d_mode_scan.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "r1d_mode_scan",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
