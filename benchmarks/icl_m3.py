"""
benchmarks/icl_m3.py — ICL-M3 (round 132): three-arm few-shot adaptation
contrast on the M3 wave-family task.

Preregistered in PRD §19 round 132 BEFORE execution. Scan §32.3 (Nagabandi
et al., ICLR 2018: GrBAL gradient-style vs ReBAL recurrence-style implicit
adaptation) supplies the contrast language; scan §32.2 names the house's
prefix-amortized inference as implicit in-context adaptation.

  arm A  PREFIX (implicit ICL): liquid model trained on the mixed-speed
         corpus {0.8, 1.0, 1.2}, NO finetune — evaluated zero-shot on the
         unseen speed c=1.5 (the prefix IS the prompt).
  arm B  PRETRAIN+FINETUNE (GrBAL-style gradient adaptation): identical
         pretrain, then finetune on n_shot=20 trajectories of c=1.5.
  arm C  FROM SCRATCH: same architecture trained from scratch on the same
         n_shot trajectories (the few-shot baseline; M3 PRD P1-2 target).

Protocol mirrors the M3 script defaults verbatim (the existing M3 product is
a 5-step smoke — round-84 generation rule: this probe delivers the first
real numbers). 1-seed screening tier; multi-seed finals PARKED per AMM-024.

Preregistered negative criteria: c1 few-shot gain fails (B >= C); c2 ordering
undecidable (|A-B| and |B-C| both below their stderrs). Otherwise the
three-way ordering IS the deliverable (GrBAL/ReBAL reading).

Results JSON follows the audit schema: top-level "results" key required.
meta carries exec_tier passthrough from probe_run (PROBE_TIER env).
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_wave_1d  # noqa: E402
from awareliquid_physics.model import LiquidOperatorHamiltonianModel  # noqa: E402
from awareliquid_physics.observability import (  # noqa: E402
    rollout_mse_stderr, run_metadata)
from awareliquid_physics.train import (  # noqa: E402
    finetune, train_pretrain, train_semigroup)


def build_model(args, seed):
    torch.manual_seed(seed)
    return LiquidOperatorHamiltonianModel(
        phase_dim=1, d_model=args.d_model, context_dim=args.context_dim,
        n_scales=args.n_scales, modes=args.modes, width=args.width,
        fno_depth=args.fno_depth, hidden_dim=args.hidden, t_depth=2,
        dt=args.dt, core_dt=1.0, reflect_pad=args.reflect_pad).to(args.device)


def evaluate(model, qs, ps, t_obs, eval_k):
    model.eval()
    q_obs, p_obs = qs[:, :t_obs], ps[:, :t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2, 3)
    p_true = ps[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2, 3)
    mse = ((qs_pred - q_true).pow(2).mean()
           + (ps_pred - p_true).pow(2).mean()).item()
    return mse, rollout_mse_stderr(qs_pred, q_true, ps_pred, p_true)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gen_steps", type=int, default=100)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=60)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--n_nodes", type=int, default=32)
    ap.add_argument("--n_pretrain_per_speed", type=int, default=96)
    ap.add_argument("--n_shot", type=int, default=20)
    ap.add_argument("--n_few_eval", type=int, default=64)
    ap.add_argument("--c_target", type=float, default=1.5)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--modes", type=int, default=12)
    ap.add_argument("--width", type=int, default=32)
    ap.add_argument("--fno_depth", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--reflect_pad", type=int, default=8)
    ap.add_argument("--pretrain_steps", type=int, default=300)
    ap.add_argument("--finetune_steps", type=int, default=200)
    ap.add_argument("--fromscratch_steps", type=int, default=400)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0)
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out_dir",
                    default="benchmarks/physics_out_v02/icl_m3")
    args = ap.parse_args()

    print(f"ICL-M3 | target speed c={args.c_target} (unseen); "
          f"n_shot={args.n_shot}; pretrain {args.pretrain_steps}/finetune "
          f"{args.finetune_steps}/scratch {args.fromscratch_steps} steps "
          f"(M3 protocol mirror, seed {args.seed}, 1-seed screening)",
          flush=True)

    families = []
    for i, c in enumerate((0.8, 1.0, 1.2)):
        qs, ps = gen_wave_1d(args.n_pretrain_per_speed, args.gen_steps,
                             args.dt, args.n_nodes, c,
                             torch.Generator(device=args.device).manual_seed(
                                 args.seed + i),
                             device=args.device)
        families.append((qs, ps))

    qs_t, ps_t = gen_wave_1d(args.n_shot + args.n_few_eval, args.gen_steps,
                             args.dt, args.n_nodes, args.c_target,
                             torch.Generator(device=args.device).manual_seed(
                                 args.seed + 100),
                             device=args.device)
    qs_few, ps_few = qs_t[:args.n_shot], ps_t[:args.n_shot]
    qs_ev, ps_ev = qs_t[args.n_shot:], ps_t[args.n_shot:]

    # arm A: mixed pretrain, NO finetune — zero-shot prefix (implicit ICL)
    model_a = build_model(args, args.seed)
    loss_a = train_pretrain(model_a, families, args.t_obs, args.k_train,
                            args.pretrain_steps, args.lr, args.batch,
                            args.seed, lr_decay=args.lr_decay)
    mse_a, se_a = evaluate(model_a, qs_ev, ps_ev, args.t_obs, args.eval_k)
    print(f"  [A prefix/ICL  ] rollout_mse {mse_a:.4e} "
          f"(pretrain_loss {loss_a:.3e})", flush=True)

    # arm B: same pretrain + finetune on n_shot (GrBAL-style)
    model_b = build_model(args, args.seed)
    lp = train_pretrain(model_b, families, args.t_obs, args.k_train,
                        args.pretrain_steps, args.lr, args.batch, args.seed,
                        lr_decay=args.lr_decay)
    lf = finetune(model_b, qs_few, ps_few, args.t_obs, args.k_train,
                  args.finetune_steps, args.lr, args.batch, args.seed + 1,
                  lr_decay=args.lr_decay)
    mse_b, se_b = evaluate(model_b, qs_ev, ps_ev, args.t_obs, args.eval_k)
    print(f"  [B pretrain+ft ] rollout_mse {mse_b:.4e} "
          f"(pretrain {lp:.3e}, finetune {lf:.3e})", flush=True)

    # arm C: from scratch on the same n_shot trajectories
    model_c = build_model(args, args.seed)
    lc = train_semigroup(model_c, qs_few, ps_few, args.t_obs, args.k_train,
                         args.fromscratch_steps, args.lr, args.batch,
                         args.seed, lr_decay=args.lr_decay)
    mse_c, se_c = evaluate(model_c, qs_ev, ps_ev, args.t_obs, args.eval_k)
    print(f"  [C from-scratch] rollout_mse {mse_c:.4e} "
          f"(train_loss {lc:.3e})", flush=True)

    # Preregistered negative criteria (PRD §19 round 132) — mechanical.
    criteria = {
        "c1_fewshot_gain_fails": mse_b >= mse_c,
        "c2_ordering_undecidable": (abs(mse_a - mse_b) < max(se_a, se_b)
                                    and abs(mse_b - mse_c) < max(se_b, se_c)),
    }
    results = {
        "arm_A_prefix_icl": {"rollout_mse": mse_a, "stderr": se_a,
                             "train_loss": loss_a},
        "arm_B_pretrain_finetune": {"rollout_mse": mse_b, "stderr": se_b,
                                    "pretrain_loss": lp, "finetune_loss": lf},
        "arm_C_from_scratch": {"rollout_mse": mse_c, "stderr": se_c,
                               "train_loss": lc},
        "fewshot_gain_direction_holds": bool(mse_b < mse_c),
        "criteria": criteria,
        "verdict_semantics": "ordering A/B/C is the deliverable; c1 fires if "
                             "finetune is not better than from-scratch "
                             "(few-shot gain direction fails); c2 fires if "
                             "the orderings are within stderr (undecidable)",
    }
    print(f"\nICL-M3 | A {mse_a:.4e} | B {mse_b:.4e} | C {mse_c:.4e} "
          f"| criteria {criteria}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "icl_m3.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({
                       "benchmark": "icl_m3",
                       "device": args.device,
                       "exec_tier": os.environ.get("PROBE_TIER", "T1"),
                       "probe_est_min": os.environ.get("PROBE_EST_MIN", "")}),
                   "results": results}, f, indent=2)


if __name__ == "__main__":
    main()
