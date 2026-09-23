"""
benchmarks/map_vs_flow.py — MAP-VS-FLOW (round 129): does the trained head
learn a vector field H or just the dt=0.1 flow map?

Preregistered in PRD §19 round 129 BEFORE execution. The house trains its
Hamiltonian heads on (t, t+dt=0.1) trajectory pairs only; many distinct H
share the same dt=0.1 velocity-Verlet map, so "learned H(q,p)" is
under-determined off the training map. This probe measures the trained
head's dt-transfer: roll out the SAME trained H at dt in {0.05, 0.1, 0.2}
over the SAME physical horizon T=10 (round-104 fixed-horizon rule) and
compare against analytically generated truth at each dt.

  FLOW_LIKE   MSE(dt=0.05)/MSE(dt=0.1) <= 2 and 1-step local-error
              log-log slope in [1.2, 2.8] — the head transfers across dt
              (vector-field object, VV local error O(dt^2)).
  MAP_LIKE    ratio >= 10 — cross-dt collapse (the head pinned the dt=0.1
              map only); N1 wording downgrades to a dt=0.1 map object.
  MIXED       in between — recorded honestly.

Native reference arm: the same architecture trained at dt=0.05 (floor for
the dt=0.05 evaluation). Family: single-frequency spring (omega=1.0) so the
bare autonomous head is in its fit regime (round-120 control-arm lesson;
the heterogeneous-band pool puts bare heads on a family-bias floor).

Results JSON follows the audit schema: top-level "results" key required.
meta carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.hamiltonian import HamiltonianHead  # noqa: E402
from awareliquid_physics.observability import (  # noqa: E402
    rollout_mse_stderr, run_metadata)
from benchmarks.m1_semigroup_eval import gen_spring  # noqa: E402


def train_head(head, qs, ps, dt, steps, lr, batch, seed, curve_every=2000):
    """1-step supervised MSE on random (t0, t0+1) pairs (round-110/120
    training form; escape-door series convention)."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(head.parameters(), lr=lr)
    N, S = qs.shape[0], qs.shape[1]
    head.train()
    loss = float("nan")
    curve = []
    for i in range(steps):
        bi = torch.randint(0, N, (batch,), generator=g)
        t0 = int(torch.randint(0, S - 2, (1,), generator=g).item())
        q, p = qs[bi, t0], ps[bi, t0]
        q_next, p_next = head.step(q, p, dt)
        loss = (q_next - qs[bi, t0 + 1]).pow(2).mean() \
             + (p_next - ps[bi, t0 + 1]).pow(2).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if curve_every and ((i + 1) % curve_every == 0 or i == 0):
            curve.append({"step": i + 1, "loss": loss.item()})
    return loss.item(), curve


def eval_at_dt(head, dt, eval_k, n_eval, seed, n_nodes_dim=1):
    """Fresh analytic truth at this dt; k-step rollout MSE (q+p point-mean)
    + 1-step local MSE of the head against the dt-specific truth map."""
    g = torch.Generator().manual_seed(1000 + seed + int(round(1 / dt)))
    qs, ps, _om = gen_spring(n_eval, eval_k, dt, n_nodes_dim, 1.0, 1.0, g)
    head.eval()
    q0, p0 = qs[:, 0], ps[:, 0]
    with torch.enable_grad():
        qs_pred, ps_pred = head.rollout(q0, p0, eval_k, dt)
        q1_pred, p1_pred = head.step(qs[:, 0], ps[:, 0], dt)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs.permute(1, 0, 2)
    p_true = ps.permute(1, 0, 2)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    local = ((q1_pred - qs[:, 1]).pow(2).mean()
             + (p1_pred - ps[:, 1]).pow(2).mean()).item()
    return {"k": eval_k, "horizon_T": eval_k * dt, "rollout_mse": mse,
            "rollout_mse_stderr": rollout_mse_stderr(qs_pred, q_true,
                                                     ps_pred, p_true),
            "one_step_mse": local}


def loglog_slope(points):
    """Ordinary least squares slope of log(y) vs log(x)."""
    xs = [math.log(x) for x, _ in points]
    ys = [math.log(y) for _, y in points]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = sum((a - mx) ** 2 for a in xs)
    return num / den if den > 0 else float("nan")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--gen_steps", type=int, default=200)
    ap.add_argument("--omega", type=float, default=1.0,
                    help="single-frequency control family (round-120 lesson)")
    ap.add_argument("--dim", type=int, default=1)
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--train_steps", type=int, default=10000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dt_train", type=float, default=0.1)
    ap.add_argument("--dts_eval", type=float, nargs="+",
                    default=[0.05, 0.1, 0.2])
    ap.add_argument("--horizon_T", type=float, default=10.0,
                    help="fixed physical horizon (round-104 rule)")
    ap.add_argument("--ratio_flow_gate", type=float, default=2.0,
                    help="preregistered: ratio <= this is the flow side")
    ap.add_argument("--ratio_map_gate", type=float, default=10.0,
                    help="preregistered: ratio >= this is the map side")
    ap.add_argument("--slope_lo", type=float, default=1.2)
    ap.add_argument("--slope_hi", type=float, default=2.8)
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/map_vs_flow")
    args = ap.parse_args()

    print(f"MAP-VS-FLOW | spring omega={args.omega} train_dt={args.dt_train} "
          f"steps={args.train_steps} horizon T={args.horizon_T} "
          f"(single-frequency control family, seed {args.seed}, "
          f"1-seed screening)", flush=True)

    # primary arm: train at dt_train
    g = torch.Generator().manual_seed(args.seed)
    qs_tr, ps_tr, _ = gen_spring(args.n_train, args.gen_steps, args.dt_train,
                                 args.dim, args.omega, args.omega, g)
    torch.manual_seed(args.seed)
    head_main = HamiltonianHead(dim=args.dim, hidden_dim=args.hidden,
                                depth=args.depth, context_dim=0)
    loss_main, curve_main = train_head(head_main, qs_tr, ps_tr, args.dt_train,
                                       args.train_steps, args.lr, args.batch,
                                       args.seed)
    print(f"  [trained @dt={args.dt_train}] train_loss {loss_main:.3e}",
          flush=True)

    # native reference arm: same architecture/budget at half dt
    g2 = torch.Generator().manual_seed(args.seed)
    qs_ref, ps_ref, _ = gen_spring(args.n_train, args.gen_steps,
                                   args.dt_train / 2, args.dim, args.omega,
                                   args.omega, g2)
    torch.manual_seed(args.seed)
    head_ref = HamiltonianHead(dim=args.dim, hidden_dim=args.hidden,
                               depth=args.depth, context_dim=0)
    loss_ref, curve_ref = train_head(head_ref, qs_ref, ps_ref,
                                     args.dt_train / 2, args.train_steps,
                                     args.lr, args.batch, args.seed)
    print(f"  [native  @dt={args.dt_train / 2}] train_loss {loss_ref:.3e}",
          flush=True)

    sweep = {}
    for dt in args.dts_eval:
        k = max(int(round(args.horizon_T / dt)), 1)
        sweep[f"dt{dt}"] = {"main": eval_at_dt(head_main, dt, k,
                                               args.n_eval, args.seed,
                                               args.dim),
                            "native_dt_half": eval_at_dt(head_ref, dt, k,
                                                         args.n_eval,
                                                         args.seed, args.dim)}
        m = sweep[f"dt{dt}"]
        print(f"  dt={dt} (k={k}, T={k * dt:.1f}): main "
              f"{m['main']['rollout_mse']:.3e} | 1-step "
              f"{m['main']['one_step_mse']:.3e} | native-ref "
              f"{m['native_dt_half']['rollout_mse']:.3e}", flush=True)

    mse_005 = sweep[f"dt{args.dts_eval[0]}"]["main"]["rollout_mse"]
    mse_01 = sweep[f"dt{args.dt_train}"]["main"]["rollout_mse"]
    ratio = mse_005 / mse_01
    slope = loglog_slope([(dt, sweep[f"dt{dt}"]["main"]["one_step_mse"])
                          for dt in args.dts_eval])
    print(f"  cross-dt ratio MSE(0.05)/MSE(0.1) = {ratio:.3f} "
          f"| 1-step log-log slope = {slope:+.3f}", flush=True)

    criteria = {
        "c_map_like": ratio >= args.ratio_map_gate,
        "c_flow_like": (ratio <= args.ratio_flow_gate)
                       and (args.slope_lo <= slope <= args.slope_hi),
    }
    if criteria["c_map_like"]:
        verdict = "MAP_LIKE"
    elif criteria["c_flow_like"]:
        verdict = "FLOW_LIKE"
    else:
        verdict = "MIXED"
    results = {
        "sweep": sweep,
        "cross_dt_ratio_005_over_01": ratio,
        "one_step_loglog_slope": slope,
        "train_loss_main": loss_main,
        "train_loss_native_ref": loss_ref,
        "criteria": criteria,
        "gates": {"ratio_flow_gate": args.ratio_flow_gate,
                  "ratio_map_gate": args.ratio_map_gate,
                  "slope_band": [args.slope_lo, args.slope_hi],
                  "horizon_T": args.horizon_T},
        "verdict_semantics": "FLOW_LIKE=ratio<=flow_gate and slope in band "
                             "(vector-field object transfers); MAP_LIKE="
                             "ratio>=map_gate (cross-dt collapse, N1 wording "
                             "downgrades to dt-map object); MIXED=recorded",
    }
    print(f"\nMAP-VS-FLOW verdict {verdict} | ratio {ratio:.3f} "
          f"| slope {slope:+.3f} | criteria {criteria}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "map_vs_flow.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "map_vs_flow",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results, "loss_curves": {
                       "main": curve_main, "native_ref": curve_ref}}, f,
                  indent=2)


if __name__ == "__main__":
    main()
