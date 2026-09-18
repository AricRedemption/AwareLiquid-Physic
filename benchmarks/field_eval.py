"""
benchmarks/field_eval.py 鈥?v0.2 (M2): the OPERATOR potential on a 1D field.

The coupling experiment for fields: a family of periodic strings (hidden wave
speed c per trajectory), prefix -> symplectic rollout, with a SPECTRAL (FNO)
potential conditioned by the liquid context.

Models:
  liquid_operator  鈥?liquid core system-ID -> FiLM conditions the FNO potential
  static_operator  鈥?same FNO Hamiltonian, context = 0 (no system identification)

Physics metrics only (rollout MSE, energy drift), plus the resolution test:
train at N=32, evaluate zero-shot at N=64/128 (resolution invariance).

Usage:
  python benchmarks/field_eval.py --train_steps 300
"""

import argparse
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_wave_1d, gen_wave_1d_inhomogeneous
from awareliquid_physics.hamiltonian import OperatorHamiltonianHead
from awareliquid_physics.model import LiquidOperatorHamiltonianModel
from awareliquid_physics.train import train_semigroup
from benchmarks.liquid_physics_eval import train as train_prefix
from awareliquid_physics.observability import rollout_mse_stderr, run_metadata


class StaticOperatorWrapper(torch.nn.Module):
    """Operator Hamiltonian with a FIXED zero context 鈥?the 'no system-ID'
    control, matched to the train/rollout interface."""

    def __init__(self, ham: OperatorHamiltonianHead, dt: float):
        super().__init__()
        self.ham = ham
        self.dt = float(dt)

    def infer_context(self, q_obs, p_obs):
        B = q_obs.shape[0]
        return torch.zeros(B, self.ham.context_dim, device=q_obs.device)

    def rollout(self, q0, p0, ctx, steps):
        return self.ham.rollout(q0, p0, steps, self.dt, context=ctx)

    def forward(self, q_obs, p_obs, k):
        ctx = self.infer_context(q_obs, p_obs)
        q0, p0 = q_obs[:, -1], p_obs[:, -1]
        qs, ps = self.rollout(q0, p0, ctx, k)
        return qs, ps, ctx


def oracle_ctx_matrix(cfields, context_dim, scale=1.0):
    """D2-CAPACITY (wave-10 G4-E1, docs/d2-capacity-design.md section 4): the
    fixed zero-learning ORACLE context — the orthogonal projection of the true
    wave-speed field c(x) onto sin/cos Fourier modes 1..context_dim//2,
    normalised by the field amplitude scale.

    The inhomogeneous family IS exactly this span (gen_wave_1d_inhomogeneous
    draws n_modes=4 sine modes), so with the default context_dim=8 the
    projection is injective on the family: perfect system identification,
    information-optimal, nothing learned. Interleaved order [a1,b1,a2,b2,...].

    cfields: (n_traj, N). Returns (n_traj, context_dim)."""
    if context_dim % 2 != 0 or context_dim < 2:
        raise ValueError("context_dim must be even and >= 2 for the oracle")
    n_modes = context_dim // 2
    n, N = cfields.shape
    x = torch.arange(N, dtype=cfields.dtype, device=cfields.device)
    basis = []
    for m in range(1, n_modes + 1):
        basis.append(torch.sin(2.0 * math.pi * m * x / N))
        basis.append(torch.cos(2.0 * math.pi * m * x / N))
    bm = torch.stack(basis)                              # (context_dim, N)
    coeffs = (2.0 / N) * (cfields @ bm.T)                # (n_traj, context_dim)
    s = float(scale) if scale and scale > 0 else 1.0
    return coeffs / s


class OracleOperatorWrapper(torch.nn.Module):
    """D2-CAPACITY C arm (wave-10 G4-E1): the operator Hamiltonian conditioned
    on the ORACLE context — a fixed projection of the true c(x), trained in
    from step zero (never swapped at eval: that would be out-of-distribution
    for a trained FiLM). It upper-bounds what PERFECT system identification
    can express through the conditioning interface, above the liquid core's
    inference quality.

    The training loops sample trajectories by index without telling the model,
    so the wrapper recovers the row by the byte-fingerprint of the t_obs
    prefix (every batch is an exact gather of the qs tensor the wrapper was
    built with). A prefix missing from the table (the homogeneous resolution
    test draws fresh trajectories) gets the constant-medium context: a
    constant field is orthogonal to modes >= 1, so zeros IS its correct
    oracle projection."""

    def __init__(self, ham, dt, qs, t_obs, row_ctx):
        super().__init__()
        self.ham = ham
        self.dt = float(dt)
        self.row_ctx = row_ctx
        self.table = {}
        for i in range(qs.shape[0]):
            key = qs[i, :t_obs].contiguous().numpy().tobytes()
            self.table[key] = i

    def lookup_rows(self, q_obs):
        rows = []
        for b in range(q_obs.shape[0]):
            key = q_obs[b].detach().contiguous().numpy().tobytes()
            rows.append(self.table.get(key, -1))
        return rows

    def infer_context(self, q_obs, p_obs):
        rows = self.lookup_rows(q_obs)
        ctx = torch.zeros(len(rows), self.row_ctx.shape[1],
                          dtype=self.row_ctx.dtype, device=self.row_ctx.device)
        for j, r in enumerate(rows):
            if r >= 0:
                ctx[j] = self.row_ctx[r]
        return ctx

    def rollout(self, q0, p0, ctx, steps):
        return self.ham.rollout(q0, p0, steps, self.dt, context=ctx)

    def forward(self, q_obs, p_obs, k):
        ctx = self.infer_context(q_obs, p_obs)
        q0, p0 = q_obs[:, -1], p_obs[:, -1]
        qs, ps = self.rollout(q0, p0, ctx, k)
        return qs, ps, ctx


def field_context_probe(model, qs, ps, coeffs, t_obs):
    """D2-CAPACITY diagnostic (wave-10 G4-E1): how much of the oracle c(x)
    coefficient vector does the learned context carry? Linear readout
    ctx -> coeffs fitted on the FIRST half of the pool, per-coefficient
    correlation reported on the SECOND half (same convention as
    sample_efficiency_eval.context_probe: a linear probe lower-bounds the
    decodable information without assuming a context layout). NaN
    correlations (degenerate targets) fold to a finite-count annotation."""
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
    return _probe_corr(y_hat, y[n_half:], "ctx_probe")


def _probe_corr(y_hat, y_true, prefix):
    """Per-coefficient Pearson correlation summary, NaN-safe (strict JSON)."""
    corrs = []
    for j in range(y_true.shape[1]):
        c = torch.corrcoef(torch.stack([y_hat[:, j], y_true[:, j]]))[0, 1]
        if torch.isfinite(c):
            corrs.append(c.item())
    if not corrs:
        return {f"{prefix}_corr_mean": 0.0, f"{prefix}_corr_min": 0.0,
                f"{prefix}_n_finite": 0}
    return {f"{prefix}_corr_mean": sum(corrs) / len(corrs),
            f"{prefix}_corr_min": min(corrs),
            f"{prefix}_n_finite": len(corrs)}


def mlp_context_probe(model, qs, ps, coeffs, t_obs, seed,
                      hidden=64, steps=500, lr=1e-2):
    """D2-CAPACITY E3 diagnostic (wave-10 G4, docs/d2-capacity-design.md
    §10): the NONLINEAR companion of field_context_probe — a small MLP
    readout (ctx -> coeffs) closes the 'information present but nonlinearly
    encoded' loophole that a linear probe cannot distinguish from true
    information loss. Trained by Adam on the FIRST half of the pool
    (z-scored by train-half statistics), correlation reported on the held-out
    SECOND half. A probe, not a model: overfitting shows up as a train/test
    gap and is not defended against beyond weight decay + z-scoring."""
    model.eval()
    n = qs.shape[0]
    with torch.enable_grad():
        _, _, ctx = model(qs[:, :t_obs], ps[:, :t_obs], 1)
    ctx = ctx.detach().reshape(n, -1).cpu()
    y = coeffs.detach().reshape(n, -1).cpu()
    n_half = n // 2
    mu = ctx[:n_half].mean(0, keepdim=True)
    sd = ctx[:n_half].std(0, keepdim=True).clamp_min(1e-6)
    xa = (ctx[:n_half] - mu) / sd
    xb = (ctx[n_half:] - mu) / sd
    g = torch.Generator().manual_seed(seed + 2000)
    readout = torch.nn.Sequential(
        torch.nn.Linear(ctx.shape[1], hidden), torch.nn.Tanh(),
        torch.nn.Linear(hidden, hidden), torch.nn.Tanh(),
        torch.nn.Linear(hidden, y.shape[1]))
    opt = torch.optim.Adam(readout.parameters(), lr=lr, weight_decay=1e-4)
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        loss = ((readout(xa) - y[:n_half]) ** 2).mean()
        loss.backward()
        opt.step()
    readout.eval()
    with torch.no_grad():
        y_hat = readout(xb)
    return _probe_corr(y_hat, y[n_half:], "ctx_mlp")


def make_models(args, seed):
    torch.manual_seed(seed)
    liquid = LiquidOperatorHamiltonianModel(
        phase_dim=1, d_model=args.d_model, context_dim=args.context_dim,
        n_scales=args.n_scales, modes=args.modes, width=args.width,
        fno_depth=args.fno_depth, hidden_dim=args.hidden, t_depth=2,
        dt=args.dt, core_dt=1.0, reflect_pad=args.reflect_pad).to(args.device)
    static_ham = OperatorHamiltonianHead(
        dim=1, width=args.width, modes=args.modes, fno_depth=args.fno_depth,
        context_dim=args.context_dim, hidden_dim=args.hidden, t_depth=2,
        reflect_pad=args.reflect_pad).to(args.device)
    static = StaticOperatorWrapper(static_ham, args.dt)
    return liquid, static


def evaluate(model, qs, ps, c_field, t_obs, eval_k, dt):
    """Free-running eval from the prefix: rollout MSE + energy drift. c_field is
    the per-trajectory wave-speed field (n_traj, N) for the energy diagnostic."""
    model.eval()
    q_obs, p_obs = qs[:, :t_obs], ps[:, :t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, ctx = model(q_obs, p_obs, eval_k)
    qs_pred, ps_pred = qs_pred.detach(), ps_pred.detach()
    q_true = qs[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2, 3)
    p_true = ps[:, t_obs - 1: t_obs + eval_k].permute(1, 0, 2, 3)
    mse = ((qs_pred - q_true).pow(2).mean() + (ps_pred - p_true).pow(2).mean()).item()

    def string_energy(q, p):
        dq = q - torch.roll(q, 1, dims=-2)
        c2 = (c_field ** 2).unsqueeze(0).unsqueeze(-1)       # (1, B, N, 1)
        return 0.5 * (p ** 2).sum((-1, -2)) + 0.5 * (c2 * dq ** 2).sum((-1, -2))
    E = string_energy(qs_pred, ps_pred)                      # (k+1, B)
    E0 = E[0].abs().clamp_min(1e-6)
    drift = ((E - E[0]).abs() / E0).max().item()
    return mse, drift, rollout_mse_stderr(qs_pred, q_true, ps_pred, p_true)


def resolution_test(model, args, g):
    """Zero-shot super-resolution: trained at N_train, evaluated at N_test."""
    n_traj, steps = args.n_res_eval, args.gen_steps
    qs, ps = gen_wave_1d(n_traj, steps, args.dt, args.n_res_test, args.c_eval, g,
                         device=args.device)
    qs, ps = qs[:n_traj], ps[:n_traj]
    t_obs, k = args.t_obs, args.eval_k
    model.eval()
    q_obs, p_obs = qs[:, :t_obs], ps[:, :t_obs]
    with torch.enable_grad():
        qs_pred, ps_pred, _ = model(q_obs, p_obs, k)
    qs_pred = qs_pred.detach()
    q_true = qs[:, t_obs - 1: t_obs + k].permute(1, 0, 2, 3)
    mse = (qs_pred - q_true).pow(2).mean().item()
    return mse


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n_train", type=int, default=256)
    ap.add_argument("--n_eval", type=int, default=64)
    ap.add_argument("--gen_steps", type=int, default=120)
    ap.add_argument("--t_obs", type=int, default=24)
    ap.add_argument("--k_train", type=int, default=8)
    ap.add_argument("--eval_k", type=int, default=80)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--c_lo", type=float, default=0.8)
    ap.add_argument("--c_hi", type=float, default=1.6)
    ap.add_argument("--c_eval", type=float, default=1.0)
    ap.add_argument("--c_var", type=float, default=0.5,
                    help="inhomogeneous mode: amplitude of the random c(x) field")
    ap.add_argument("--inhomogeneous", action="store_true",
                    help="wave speed is a random smooth FIELD c(x) per trajectory")
    ap.add_argument("--n_nodes", type=int, default=32)
    ap.add_argument("--n_res_test", type=int, default=64)
    ap.add_argument("--n_res_eval", type=int, default=16)
    ap.add_argument("--d_model", type=int, default=48)
    ap.add_argument("--context_dim", type=int, default=8)
    ap.add_argument("--n_scales", type=int, default=4)
    ap.add_argument("--modes", type=int, default=12)
    ap.add_argument("--width", type=int, default=32)
    ap.add_argument("--fno_depth", type=int, default=4)
    ap.add_argument("--hidden", type=int, default=48)
    ap.add_argument("--reflect_pad", type=int, default=8)
    ap.add_argument("--train_steps", type=int, default=300)
    ap.add_argument("--train_loop", default="semigroup",
                    choices=["semigroup", "prefix"],
                    help="D2 ablation (wave-10 round 7): semigroup (default, "
                         "the shipped behaviour) vs the v0.1 fixed-window "
                         "prefix loop — quantifies P2's claim on M2")
    ap.add_argument("--oracle_ctx", action="store_true",
                    help="D2-CAPACITY E1 (wave-10 G4): add the oracle_operator "
                         "arm — trained with the fixed projection of the true "
                         "c(x) as context (docs/d2-capacity-design.md §4-5) — "
                         "plus the linear context probe on the liquid arm")
    ap.add_argument("--arms", default="",
                    help="comma subset of the enabled arms to RUN (e.g. "
                         "'liquid_operator' for E3 dose runs); empty = all "
                         "enabled arms, the historical behaviour")
    ap.add_argument("--aux_identify_weight", type=float, default=0.0,
                    help="D2-CAPACITY R1 (wave-10 G4, semigroup loop only): "
                         "weight of the auxiliary readout loss from the "
                         "inferred context to the true c(x) coefficients "
                         "(docs/d2-capacity-design.md §12.3); 0.0 = off, "
                         "identical RNG and behaviour")
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--lr_decay", type=float, default=1.0,
                    help="per-step exponential lr decay (1.0 = constant)")
    ap.add_argument("--device", default="cpu", help="cpu | cuda")
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n_seeds", type=int, default=1,
                    help="repeat training across seeds, report mean +/- std")
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02")
    args = ap.parse_args()

    g = torch.Generator(device=args.device).manual_seed(args.seed)
    n = args.n_train + args.n_eval
    if args.inhomogeneous:
        # Hard version: the hidden parameter is a whole spatial FIELD c(x) per
        # trajectory 鈥?a static potential can only approximate an average medium.
        qs, ps, cfields = gen_wave_1d_inhomogeneous(
            n, args.gen_steps, args.dt, args.n_nodes,
            c_mean=args.c_eval, c_var=args.c_var, generator=g,
            device=args.device)
        print(f"field family (INHOMOGENEOUS): N={args.n_nodes} "
              f"c(x) = {args.c_eval} +/- {args.c_var} per trajectory", flush=True)
    else:
        # Family of constant wave speeds: half at c_eval, rest spread over
        # [c_lo, c_hi] 鈥?per-trajectory hidden scalar the context must identify.
        qs, ps = gen_wave_1d(n, args.gen_steps, args.dt, args.n_nodes,
                             c=args.c_eval, generator=g, device=args.device)
        g2 = torch.Generator(device=args.device).manual_seed(args.seed + 1)
        cs = torch.empty(n, device=args.device)
        cs[:n // 2] = args.c_eval
        cs[n // 2:] = args.c_lo + (args.c_hi - args.c_lo) * torch.rand(
            n - n // 2, generator=g2, device=args.device)
        for i in range(n // 2, n):
            qi, pi = gen_wave_1d(1, args.gen_steps, args.dt, args.n_nodes,
                                 c=cs[i].item(), generator=g2, device=args.device)
            qs[i], ps[i] = qi[0], pi[0]
        cfields = cs[:, None].expand(n, args.n_nodes)
        print(f"field family: N={args.n_nodes} c~{{{args.c_lo}..{args.c_hi}}} "
              f"t_obs={args.t_obs} k_train={args.k_train} eval_k={args.eval_k}",
              flush=True)
    tr, ev = slice(0, args.n_train), slice(args.n_train, None)

    arms = ("liquid_operator", "static_operator")
    if args.oracle_ctx:
        arms += ("oracle_operator",)
    if args.arms:
        want = [s.strip() for s in args.arms.split(",") if s.strip()]
        unknown = [w for w in want if w not in arms]
        if unknown:
            raise SystemExit(f"--arms unknown (or flag-absent) arms: "
                             f"{unknown}; available here: {arms}")
        arms = tuple(a for a in arms if a in want)
        if not arms:
            raise SystemExit("--arms selected nothing")
    results = {}
    liquid_trained = None
    probe_corrs = []
    mlp_corrs = []
    for name in arms:
        mses, drifts, mse_ses = [], [], []
        n_par = None
        for s in range(args.n_seeds):
            seed = args.seed + s
            liquid, static = make_models(args, seed)
            if name == "liquid_operator":
                model = liquid
                liquid_trained = model
            elif name == "oracle_operator":
                oham = OperatorHamiltonianHead(
                    dim=1, width=args.width, modes=args.modes,
                    fno_depth=args.fno_depth, context_dim=args.context_dim,
                    hidden_dim=args.hidden, t_depth=2,
                    reflect_pad=args.reflect_pad).to(args.device)
                row_ctx = oracle_ctx_matrix(cfields, args.context_dim,
                                            scale=args.c_var).to(args.device)
                model = OracleOperatorWrapper(oham, args.dt, qs, args.t_obs,
                                              row_ctx)
            else:
                model = static
            if n_par is None:
                n_par = sum(p.numel() for p in model.parameters())
            if args.train_loop == "prefix":
                floss = train_prefix(model, qs[tr], ps[tr], args.t_obs,
                                     args.k_train, args.train_steps, args.lr,
                                     args.batch, seed, lr_decay=args.lr_decay)
            else:
                aux_head = aux_targets = None
                if args.aux_identify_weight > 0.0 and name == "liquid_operator":
                    # D2-CAPACITY R1 (docs/d2-capacity-design.md §12.3):
                    # linear readout inferred-ctx -> true 8 coefficients.
                    aux_head = torch.nn.Linear(args.context_dim,
                                               args.context_dim).to(args.device)
                    aux_targets = oracle_ctx_matrix(cfields, args.context_dim,
                                                    scale=args.c_var).to(args.device)
                floss = train_semigroup(model, qs[tr], ps[tr], args.t_obs,
                                        args.k_train, args.train_steps,
                                        args.lr, args.batch, seed,
                                        lr_decay=args.lr_decay,
                                        aux_head=aux_head,
                                        aux_targets=aux_targets,
                                        aux_identify_weight=args.aux_identify_weight)
            mse, drift, mse_se = evaluate(model, qs[ev], ps[ev], cfields[ev], args.t_obs,
                                          args.eval_k, args.dt)
            if name == "liquid_operator" and args.oracle_ctx:
                coeffs = oracle_ctx_matrix(cfields, args.context_dim,
                                           scale=args.c_var)
                probe = field_context_probe(model, qs[ev], ps[ev],
                                            coeffs[ev], args.t_obs)
                mprobe = mlp_context_probe(model, qs[ev], ps[ev],
                                           coeffs[ev], args.t_obs, seed)
                probe_corrs.append(probe["ctx_probe_corr_mean"])
                mlp_corrs.append(mprobe["ctx_mlp_corr_mean"])
            mses.append(mse)
            drifts.append(drift)
            mse_ses.append(mse_se)
        mse_mean = sum(mses) / len(mses)
        drift_mean = sum(drifts) / len(drifts)
        mse_std = (sum((m - mse_mean) ** 2 for m in mses) / len(mses)) ** 0.5
        drift_std = (sum((d - drift_mean) ** 2 for d in drifts) / len(drifts)) ** 0.5
        results[name] = {"params": n_par, "train_loss": floss,
                         "rollout_mse": mse_mean, "rollout_mse_std": mse_std,
                         "rollout_mse_stderr": sum(mse_ses) / len(mse_ses),
                         "energy_drift_max": drift_mean,
                         "energy_drift_max_std": drift_std,
                         # per-seed traceability (wave-10 round 9 gap): paired
                         # multi-seed judgments need the per-seed values
                         **{f"rollout_mse_seed{i}": m for i, m in enumerate(mses)},
                         **{f"energy_drift_max_seed{i}": d for i, d in enumerate(drifts)}}
        print(f"  [{name:16s}] params {n_par:>6,} | n_seeds {args.n_seeds} | "
              f"rollout_mse {mse_mean:.4e} +/- {mse_std:.2e} | "
              f"energy_drift(max) {drift_mean:.4e} +/- {drift_std:.2e}", flush=True)
        if name == "liquid_operator" and probe_corrs:
            results["ctx_probe"] = {
                "corr_mean": sum(probe_corrs) / len(probe_corrs),
                **{f"corr_mean_seed{i}": c for i, c in enumerate(probe_corrs)}}
        if name == "liquid_operator" and mlp_corrs:
            results["ctx_probe_mlp"] = {
                "corr_mean": sum(mlp_corrs) / len(mlp_corrs),
                **{f"corr_mean_seed{i}": c for i, c in enumerate(mlp_corrs)}}

    # Resolution invariance: the SAME trained model at 2x the node count.
    if "liquid_operator" in results:
        g3 = torch.Generator(device=args.device).manual_seed(args.seed + 2)
        mse_hi = resolution_test(liquid_trained, args, g3)
        results["resolution"] = {"train_N": args.n_nodes, "test_N": args.n_res_test,
                                 "rollout_mse": mse_hi}
        print(f"  [resolution      ] trained N={args.n_nodes} -> eval N="
              f"{args.n_res_test} zero-shot rollout_mse {mse_hi:.4e}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    import json
    with open(os.path.join(args.out_dir, "field_eval.json"), "w") as f:
        json.dump({"args": vars(args), "meta": run_metadata({"benchmark": "field_eval",
                   "device": args.device}), "results": results}, f, indent=2)

    if "liquid_operator" in results and "static_operator" in results:
        lq, st = results["liquid_operator"], results["static_operator"]
        print("\n" + "=" * 70, flush=True)
        print("FIELD + OPERATOR POTENTIAL | does liquid system-ID add value?", flush=True)
        print("=" * 70, flush=True)
        print(f"  rollout MSE:   liquid {lq['rollout_mse']:.3e} | static "
              f"{st['rollout_mse']:.3e}", flush=True)
        print(f"  energy drift:  liquid {lq['energy_drift_max']:.3e} | static "
              f"{st['energy_drift_max']:.3e}", flush=True)
        gap = 1.0 - lq["rollout_mse"] / st["rollout_mse"]
        print(f"  liquid advantage over static: {gap * 100:.1f}% "
              f"(target >= 30%)", flush=True)
    if args.oracle_ctx and "oracle_operator" in results:
        oc = results["oracle_operator"]
        lq = results.get("liquid_operator")
        st = results.get("static_operator")
        parts = [f"  D2-CAPACITY oracle-ctx arm: {oc['rollout_mse']:.3e}"]
        if st:
            parts.append(f"rho_CA {oc['rollout_mse'] / st['rollout_mse']:.3f}")
        if lq:
            parts.append(f"rho_CB {oc['rollout_mse'] / lq['rollout_mse']:.3f}")
        if "ctx_probe" in results:
            parts.append(f"probe {results['ctx_probe']['corr_mean']:.3f}")
        if "ctx_probe_mlp" in results:
            parts.append(f"mlp-probe {results['ctx_probe_mlp']['corr_mean']:.3f}")
        print(" | ".join(parts), flush=True)


if __name__ == "__main__":
    main()
