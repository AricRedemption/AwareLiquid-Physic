"""
benchmarks/grad_starvation_probe.py — D2-CAPACITY E4a (wave-10 G4, 2026-09-19).

ZERO-TRAINING gradient probe (docs/d2-capacity-design.md §12.2, gate v2
compliant: no optimizer steps, seconds of runtime). Question: is the
inference path (node_enc + liquid core + context_proj) gradient-starved
relative to the fit path (FNO potential) — i.e. does the one-step loss exert
meaningful pressure on the context at all?

Per batch we measure, on a FRESH model (the early-training regime where
starvation would bite):
  * ||dL/d(inference-path params)||  vs  ||dL/d(head params)||
  * ||dL/d(ctx)|| (activation level, via retain_grad) — the raw pressure the
    loss exerts on the context VALUE
  * oracle control: ctx replaced by the true c(x) projection as a leaf with
    requires_grad — head-side gradient with informed context, and the
    decoupled pressure dL/d(ctx_oracle).

Preregistered reading (PRD §19 round 54): ratio < 1e-2 => starvation
confirmed; ratio >= 0.1 => not starved, failure is later-stage (R1 decides);
in between => record honestly.

Usage: python benchmarks/grad_starvation_probe.py [--out_dir d2_capacity/e4a]
"""

import argparse
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_wave_1d_inhomogeneous
from awareliquid_physics.model import LiquidOperatorHamiltonianModel
from awareliquid_physics.observability import run_metadata
from benchmarks.field_eval import oracle_ctx_matrix


def group_norms(model):
    inf_params = list(model.node_enc.parameters()) + \
        list(model.core.parameters()) + list(model.context_proj.parameters())
    head_params = list(model.ham.parameters())
    return inf_params, head_params


def total_norm(params):
    s = 0.0
    for p in params:
        if p.grad is not None:
            s += p.grad.pow(2).sum().item()
    return s ** 0.5


def one_measurement(model, qs, ps, batch_idx, t_obs, k_train, oracle_rows=None):
    """Forward+backward on ONE batch, no optimizer step. Returns dict of
    gradient norms. oracle_rows: (B, ctx_dim) leaf replacing the inferred
    context when given."""
    bi = torch.tensor(batch_idx)
    q_obs, p_obs = qs[bi, :t_obs], ps[bi, :t_obs]
    t0 = torch.full((len(batch_idx),), t_obs, dtype=torch.long)
    q0, p0 = qs[bi, t0], ps[bi, t0]
    q_true = qs[bi[:, None], t0[:, None] + torch.arange(k_train + 1)]
    p_true = ps[bi[:, None], t0[:, None] + torch.arange(k_train + 1)]
    q_true = q_true.permute(1, 0, 2, 3)
    p_true = p_true.permute(1, 0, 2, 3)

    model.zero_grad(set_to_none=True)
    if oracle_rows is None:
        ctx = model.infer_context(q_obs, p_obs)
        ctx.retain_grad()
    else:
        ctx = oracle_rows.clone().requires_grad_(True)
    qs_pred, ps_pred = model.rollout(q0, p0, ctx, k_train)
    loss = ((qs_pred - q_true) ** 2).mean() + ((ps_pred - p_true) ** 2).mean()
    loss.backward()
    inf_params, head_params = group_norms(model)
    out = {"loss": loss.item(),
           "grad_inf_path": total_norm(inf_params),
           "grad_head": total_norm(head_params),
           "grad_ctx": ctx.grad.norm().item() if ctx.grad is not None else 0.0}
    model.zero_grad(set_to_none=True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_traj", type=int, default=32)
    ap.add_argument("--gen_steps", type=int, default=48)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--n_nodes", type=int, default=32)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--c_mean", type=float, default=1.0)
    ap.add_argument("--c_var", type=float, default=0.5)
    ap.add_argument("--batches", type=int, default=3)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02/d2_capacity/e4a")
    args = ap.parse_args()

    g = torch.Generator().manual_seed(args.seed)
    torch.manual_seed(args.seed)
    qs, ps, cfields = gen_wave_1d_inhomogeneous(
        args.n_traj, args.gen_steps, args.dt, args.n_nodes,
        c_mean=args.c_mean, c_var=args.c_var, generator=g)
    model = LiquidOperatorHamiltonianModel(
        phase_dim=1, d_model=args.d_model, context_dim=args.context_dim,
        dt=args.dt)
    row_ctx = oracle_ctx_matrix(cfields, args.context_dim, scale=args.c_var)

    rg = torch.Generator().manual_seed(args.seed + 1)
    inferred, oracle = [], []
    for _ in range(args.batches):
        bi = torch.randint(0, args.n_traj, (args.batch,),
                           generator=rg).tolist()
        inferred.append(one_measurement(model, qs, ps, bi, args.t_obs,
                                        args.k_train))
        oracle.append(one_measurement(model, qs, ps, bi, args.t_obs,
                                      args.k_train,
                                      oracle_rows=row_ctx[bi]))

    def mean(key, rows):
        return sum(r[key] for r in rows) / len(rows)

    ratio = mean("grad_inf_path", inferred) / max(mean("grad_head", inferred),
                                                  1e-12)
    summary = {
        "grad_ratio_inferred": ratio,
        "grad_ctx_inferred": mean("grad_ctx", inferred),
        "grad_ctx_oracle": mean("grad_ctx", oracle),
        "grad_head_inferred": mean("grad_head", inferred),
        "grad_head_oracle": mean("grad_head", oracle),
        "loss_inferred": mean("loss", inferred),
        "loss_oracle": mean("loss", oracle),
    }
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "grad_starvation.json"), "w") as f:
        json.dump({"args": vars(args),
                   "meta": run_metadata({"benchmark": "grad_starvation_probe",
                                         "device": "cpu"}),
                   "results": {"summary": summary,
                               "per_batch_inferred": inferred,
                               "per_batch_oracle": oracle}}, f, indent=2)

    print(f"E4a gradient-starvation probe (fresh model, {args.batches} batches,"
          f" no optimizer steps)", flush=True)
    print(f"  ||dL/d inf-path|| / ||dL/d head||  = {summary['grad_ratio_inferred']:.3e}"
          f"   (preregistered: <1e-2 starved | >=0.1 not starved)", flush=True)
    print(f"  ||dL/d ctx|| inferred {summary['grad_ctx_inferred']:.3e}"
          f" | oracle-leaf {summary['grad_ctx_oracle']:.3e}", flush=True)
    print(f"  ||dL/d head|| inferred {summary['grad_head_inferred']:.3e}"
          f" | oracle-ctx {summary['grad_head_oracle']:.3e}", flush=True)
    print(f"  1-step loss   inferred {summary['loss_inferred']:.5f}"
          f" | oracle-ctx {summary['loss_oracle']:.5f}", flush=True)


if __name__ == "__main__":
    main()
