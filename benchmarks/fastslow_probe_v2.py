"""
benchmarks/fastslow_probe_v2.py — FASTSLOW-2 (round 143): capacity/budget
attribution of the round-137 BOTH_FAILED.

Preregistered in PRD §19 round 143 BEFORE execution. Round 137 (hidden64 +
10k steps) classified BOTH_FAILED on the elastic pendulum (fast gate 1% /
slow gate 10%). This probe answers: optimization limit (more capacity /
budget fixes it) or data/timescale structural limit (§33.2)?

Two arms, same family / dt=0.02 / seed 0 / pool / gates (1-seed screening):
  MAIN — hidden128 + 40000 steps (4x parameters x 4x budget vs round 137)
  H64  — hidden64  + 40000 steps (4x budget, capacity unchanged)

Mechanical attribution (preregistered):
  MAIN still BOTH_FAILED          => STRUCTURAL (N1 wording upgraded)
  MAIN reversed + H64 BOTH_FAILED => CAPACITY_NEEDED (capacity was the cause)
  MAIN reversed + H64 reversed    => BUDGET_DOMINANT (steps were the cause)

Reuses the round-137 family/truth/training/eval functions verbatim; arms
share one truth pool. Results JSON follows the audit schema (top-level
"results" key); meta carries exec_tier passthrough from probe_run.
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastslow_probe import (  # noqa: E402
    gen_pendulum, rollout_mse_rel, train_head, true_energy)

from awareliquid_physics.hamiltonian import HamiltonianHead  # noqa: E402
from awareliquid_physics.observability import run_metadata  # noqa: E402


def verdict_four_way(fast_rel: float, long_rel: float,
                     gate_fast: float, gate_long: float) -> str:
    """Preregistered gate table (round 137): mechanical four-way verdict."""
    fast_ok, long_ok = fast_rel <= gate_fast, long_rel <= gate_long
    if fast_ok and long_ok:
        return "BOTH_CAPTURED"
    if fast_ok:
        return "FAST_ONLY"
    if long_ok:
        return "SLOW_ONLY"
    return "BOTH_FAILED"


def classify_attribution(main_verdict: str, h64_verdict: str) -> str:
    """Preregistered round-143 attribution table (pure, test-pinned)."""
    if main_verdict == "BOTH_FAILED":
        return "STRUCTURAL"
    if h64_verdict == "BOTH_FAILED":
        return "CAPACITY_NEEDED"
    return "BUDGET_DOMINANT"


ATTRIBUTION_SEMANTICS = {
    "STRUCTURAL":
        "MAIN still BOTH_FAILED at 4x capacity x 4x budget => data/timescale "
        "structural limit (§33.2); N1 timescale clause wording upgraded to "
        "structural; H64 arm is failure texture only",
    "CAPACITY_NEEDED":
        "MAIN reversed but H64 (same 4x budget, original capacity) still "
        "BOTH_FAILED => capacity was the binding constraint (optimization "
        "limit); N1 clause keeps scope-limited wording",
    "BUDGET_DOMINANT":
        "MAIN and H64 both reversed => training budget (steps) was the "
        "binding constraint, capacity secondary (optimization limit); N1 "
        "clause keeps scope-limited wording",
}


def eval_arm(head, qs, ps, qs_l, ps_l, dt, k_fast, k_long, dt_coarse,
             gate_fast, gate_long):
    """Round-137 axes A/B/C + energy drift for one trained head."""
    qs_f = qs[:, :k_fast + 1].contiguous()
    ps_f = ps[:, :k_fast + 1].contiguous()
    e_fast = rollout_mse_rel(head, qs_f, ps_f, dt, k_fast, dt)
    e_long = rollout_mse_rel(head, qs_l, ps_l, dt, k_long, dt)

    head.eval()
    with torch.enable_grad():
        qs_p2, ps_p2 = head.rollout(qs_l[:, 0], ps_l[:, 0], k_long, dt)
    E = true_energy(qs_p2.detach(), ps_p2.detach())
    e_scale = E.abs().mean().clamp_min(1e-6)
    drift_true = ((E - E[0]).abs() / e_scale).max().item()

    with torch.enable_grad():
        qs_c, ps_c = head.rollout(qs_l[:, 0], ps_l[:, 0],
                                  int(2 / dt_coarse), dt_coarse)
    blowup = bool(not torch.isfinite(qs_c).all()
                  or qs_c.norm() > 1e3 * qs_l[:, :qs_c.shape[0] + 1]
                  .norm().clamp_min(1e-6))

    verdict = verdict_four_way(e_fast["mse_rel_to_signal"],
                               e_long["mse_rel_to_signal"],
                               gate_fast, gate_long)
    return {
        "verdict": verdict,
        "criteria": {
            "c_fast_not_captured":
                e_fast["mse_rel_to_signal"] > gate_fast,
            "c_slow_lost": e_long["mse_rel_to_signal"] > gate_long},
        "axis_A_fast": e_fast,
        "axis_B_long": e_long,
        "true_energy_drift_max_long": drift_true,
        "axis_C_stiffness_documentation": {
            "dt_coarse": dt_coarse,
            "finite": bool(torch.isfinite(qs_c).all().item()),
            "blowup": blowup},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--dt", type=float, default=0.02)
    ap.add_argument("--gen_steps", type=int, default=2001)
    ap.add_argument("--k_fast", type=int, default=100)
    ap.add_argument("--k_long", type=int, default=2000)
    ap.add_argument("--dt_coarse", type=float, default=0.5)
    ap.add_argument("--hidden_main", type=int, default=128)
    ap.add_argument("--hidden_h64", type=int, default=64)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--train_steps", type=int, default=40000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gate_fast", type=float, default=0.01)
    ap.add_argument("--gate_long", type=float, default=0.1)
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/fastslow_probe_v2")
    args = ap.parse_args()

    qs, ps = gen_pendulum(args.n_train + args.n_eval, args.gen_steps,
                          args.dt, args.seed, args.device)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)
    qs_l = qs[ev].contiguous()
    ps_l = ps[ev].contiguous()
    print(f"FASTSLOW-2 | elastic pendulum omega_s=10 omega_p≈1 "
          f"dt={args.dt} steps={args.train_steps} "
          f"arms=hidden{args.hidden_main}+hidden{args.hidden_h64} "
          f"(seed {args.seed}, 1-seed screening)", flush=True)

    arms = {}
    for name, hidden in (("MAIN", args.hidden_main),
                         ("H64", args.hidden_h64)):
        torch.manual_seed(args.seed)
        head = HamiltonianHead(dim=2, hidden_dim=hidden,
                               depth=args.depth, context_dim=0)
        loss = train_head(head, qs[tr], ps[tr], args.dt, args.train_steps,
                          args.lr, args.batch, args.seed)
        print(f"  [{name} hidden{hidden}] train_loss {loss:.3e}", flush=True)
        res = eval_arm(head, qs[ev], ps[ev], qs_l, ps_l,
                       args.dt, args.k_fast, args.k_long, args.dt_coarse,
                       args.gate_fast, args.gate_long)
        res["train_loss"] = loss
        res["hidden"] = hidden
        res["train_steps"] = args.train_steps
        arms[name] = res
        print(f"  [{name}] A rel {res['axis_A_fast']['mse_rel_to_signal']:.4f}"
              f" | B rel {res['axis_B_long']['mse_rel_to_signal']:.4f}"
              f" | E-drift {res['true_energy_drift_max_long']:.3f}"
              f" | verdict {res['verdict']}", flush=True)

    attribution = classify_attribution(arms["MAIN"]["verdict"],
                                       arms["H64"]["verdict"])
    results = {
        "arms": arms,
        "attribution": attribution,
        "attribution_semantics": ATTRIBUTION_SEMANTICS[attribution],
        "n1_wording_route": ("STRUCTURAL_UPGRADE" if attribution ==
                             "STRUCTURAL" else "SCOPE_LIMITED_KEPT"),
        "gates": {"gate_fast": args.gate_fast, "gate_long": args.gate_long},
    }
    print(f"\nFASTSLOW-2 attribution {attribution}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "fastslow_probe_v2.json"),
              "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "fastslow_probe_v2",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN",
                                                       "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
