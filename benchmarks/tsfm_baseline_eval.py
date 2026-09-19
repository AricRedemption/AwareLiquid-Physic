"""D-2 TSFM-BASELINE — Chronos/TimesFM 零样本参考基线(轮 82 协议;AMM-010 重标 T1 直跑).

Protocol docs/tsfm-baseline-protocol.md (round 82, preregistered):
  * Task: M1 spring q(t) univariate — t_obs=24-step prefix, extrapolate
    k=100 steps; the true p channel does NOT participate (TSFM cannot use
    momentum — that IS the interface axis, protocol §1/§2).
  * Same pool as the existing arms: the d1b three-point artifact
    (sample_efficiency_eval sizes=32,64, out_dir d1b_eval_depth) generated
    its eval set as the LAST 128 of gen_spring(n_train+128, steps=160,
    dt=0.1, ω∈[0.7,1.8]) with torch Generator seeded 0/1/2. This script
    regenerates those exact pools (n_train=32 → 160-traj pool, n_train=64 →
    192-traj pool) so the n32/n64 eval sets are trajectory-identical to the
    prefix/all2all arms they are tabulated against.
  * Metric: q-only rollout MSE, same windowing as eval_rollout_mse — the
    101-point alignment [last observed q, 100 forecast steps] vs
    q_true[t_obs-1 : t_obs+k], MSE averaged over all points incl. the
    (zero-error) anchor; per-k ladder k∈{1,10,100} = mean over the first
    k+1 points, matching rollout_mse_k{k} in the d1b artifact.
  * Fairness (protocol §2, must appear WITH the numbers): data-regime
    mismatch (massive cross-domain pretraining vs n≤512 in-context line),
    category-crossing reference (NOT a same-protocol ranking — TSFM has no
    conservation/symplectic structure), reader-reference use (either
    outcome is informative; no ranking conclusion).
  * Verdict field is deliberately absent here: the preregistered criterion
    is "k100 rollout MSE presented in the same table", judged in PRD §19.

Usage:
    python benchmarks/tsfm_baseline_eval.py                # Chronos (+ TimesFM if importable)
    python benchmarks/tsfm_baseline_eval.py --models chronos
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import torch

from awareliquid_physics.observability import run_metadata
from benchmarks.m1_semigroup_eval import gen_spring

SEEDS = (0, 1, 2)          # d1b convention: seed = base + i, base 0
T_OBS = 24                 # protocol-pinned prefix length
EVAL_KS = (1, 10, 100)     # d1b three-point ladder
K_HORIZON = 100            # protocol-pinned extrapolation horizon
POOL_STEPS = 160           # d1b gen_steps
DT, OMEGA_LO, OMEGA_HI = 0.1, 0.7, 1.8
N_EVAL = 128


def q_only_mse_ladder(pred: torch.Tensor, q_true: torch.Tensor) -> dict:
    """pred/q_true: (n, k+1, 1) aligned at the last observed point.
    Returns per-k q-only MSE (mean over the first k+1 points), matching
    sample_efficiency_eval.eval_rollout_mse's q-part windowing."""
    sq = (pred - q_true).pow(2).flatten(1)          # (n, k+1)
    out = {}
    for k in EVAL_KS:
        out[f"q_mse_k{k}"] = sq[:, : k + 1].mean().item()
    return out


class ChronosArm:
    """Loads the official zero-shot weights ONCE; forecasts the median."""

    def __init__(self, model_name: str, num_samples: int = 10):
        self.err: str | None = None
        self.pipe = None
        self.num_samples = num_samples
        try:
            from chronos import ChronosPipeline
            self.pipe = ChronosPipeline.from_pretrained(
                model_name, device_map="cpu", torch_dtype=torch.float32)
        except Exception as e:                       # noqa: BLE001 — degrade to pending
            self.err = f"{type(e).__name__}: {e}"

    def __call__(self, contexts: torch.Tensor, horizon: int):
        if self.err is not None or self.pipe is None:
            return None, self.err
        try:
            with torch.no_grad():
                # chronos-forecasting 2.x API: positional inputs; returns
                # SAMPLES (n, num_samples, horizon) — take the per-step
                # median as the point forecast. limit_prediction_length
                # default False keeps the k=100 horizon beyond the t5
                # training length (64) legal (warns, by design).
                fcst = self.pipe.predict(contexts, prediction_length=horizon,
                                         num_samples=self.num_samples)
            if fcst.dim() == 3:
                fcst = fcst.median(dim=1).values
            return fcst.float(), None                # median point forecast
        except Exception as e:                       # noqa: BLE001
            return None, f"{type(e).__name__}: {e}"


class TimesFMArm:
    """Best-effort TimesFM arm (protocol names both models): a missing
    environment degrades that column to 'pending', never crashes Chronos."""

    def __init__(self, repo_id: str, local_path: str | None = None):
        self.err: str | None = None
        self.tfm = None
        try:
            import timesfm
            ckpt = (timesfm.TimesFmCheckpoint(path=local_path) if local_path
                    else timesfm.TimesFmCheckpoint(huggingface_repo_id=repo_id))
            self.tfm = timesfm.TimesFm(
                hparams=timesfm.TimesFmHparams(
                    backend="cpu", per_core_batch_size=32, horizon_len=K_HORIZON,
                    context_len=512, input_patch_len=32, output_patch_len=128),
                checkpoint=ckpt)
        except Exception as e:                       # noqa: BLE001
            self.err = f"{type(e).__name__}: {e}"

    def __call__(self, contexts: torch.Tensor, horizon: int):
        if self.err is not None or self.tfm is None:
            return None, self.err
        try:
            outs = []
            for i in range(0, contexts.shape[0], 32):
                batch = [contexts[j].numpy() for j in
                         range(i, min(i + 32, contexts.shape[0]))]
                fcst, _ = self.tfm.forecast(batch)
                outs.append(torch.tensor(np.asarray(fcst), dtype=torch.float32))
            return torch.cat(outs), None
        except Exception as e:                       # noqa: BLE001
            return None, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", default="chronos,timesfm",
                    help="comma subset of {chronos,timesfm}")
    ap.add_argument("--chronos_model", default="amazon/chronos-t5-small")
    ap.add_argument("--timesfm_repo", default="google/timesfm-1.0-200m-pytorch")
    ap.add_argument("--timesfm_path", default=None,
                    help="local torch_model.ckpt path (offline form; skips the "
                         "HF download whose xet etags defeat resume)")
    ap.add_argument("--num_samples", type=int, default=10,
                    help="chronos sample count for the median forecast "
                         "(default 20; 10 halves CPU time, pinned in meta)")
    ap.add_argument("--out_dir", default="benchmarks/physics_out_v02/tsfm_baseline")
    args = ap.parse_args()
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    os.makedirs(args.out_dir, exist_ok=True)
    rows_path = os.path.join(args.out_dir, "tsfm_baseline_rows.jsonl")
    rows = []                                        # per (pool, seed, model)
    if os.path.exists(rows_path):                    # resume: keep finished pools
        with open(rows_path) as f:
            rows = [json.loads(line) for line in f if line.strip()]

    # pools identical to the d1b artifact: last 128 of gen_spring(n_train+128)
    pools = {}
    for n_train in (32, 64):
        for seed in SEEDS:
            g = torch.Generator().manual_seed(seed)
            qs, _, _ = gen_spring(n_train + N_EVAL, POOL_STEPS, DT, 1,
                                  OMEGA_LO, OMEGA_HI, g)
            pools[(n_train, seed)] = qs[-N_EVAL:]    # (128, 161, 1) held-out set

    forecasters = {}
    if "chronos" in models:
        forecasters["chronos"] = ChronosArm(args.chronos_model, args.num_samples)
    if "timesfm" in models:
        forecasters["timesfm"] = TimesFMArm(args.timesfm_repo, args.timesfm_path)

    done = {(r["model"], r["n_pool"], r["seed"]) for r in rows if r["status"] == "ok"}
    rows_file = open(rows_path, "a")
    for name, arm in forecasters.items():
        for (n_train, seed) in sorted(pools):
            if (name, n_train, seed) in done:
                print(f"[{name}] pool n_train={n_train} seed={seed}: cached", flush=True)
                continue
            qs = pools[(n_train, seed)]
            ctx = qs[:, :T_OBS, 0].contiguous()      # (128, 24) univariate q
            q_true = qs[:, T_OBS - 1: T_OBS + K_HORIZON]   # (128, 101, 1)
            fcst, err = arm(ctx, K_HORIZON)
            if fcst is None:
                row = {"model": name, "n_pool": n_train, "seed": seed,
                       "status": "pending", "error": err}
            else:
                pred = torch.cat([qs[:, T_OBS - 1: T_OBS], fcst.unsqueeze(-1)],
                                 dim=1)              # (128, 101, 1) anchored
                row = {"model": name, "n_pool": n_train, "seed": seed,
                       "status": "ok",
                       **q_only_mse_ladder(pred, q_true)}
            rows.append(row)
            rows_file.write(json.dumps(row) + "\n")
            rows_file.flush()
            print(f"[{name}] pool n_train={n_train} seed={seed}: "
                  + (", ".join(f"{k}={row[k]:.4e}" for k in row
                               if k.startswith("q_mse_")) or row.get("status", "")),
                  flush=True)
    rows_file.close()

    # a prior run's transient 'pending' rows must not poison the aggregate:
    # only 'ok' rows count, and a model with zero ok rows re-reports pending
    # from its latest error below.

    # aggregate: mean ± std across seeds (protocol: point estimate + seed
    # interval); covers ALL models present in the rows file so a per-model
    # invocation (resume) still rebuilds the full results table
    results = {}
    for name in ({r["model"] for r in rows} | set(forecasters)):
        for n_train in (32, 64):
            rs = [r for r in rows if r["model"] == name
                  and r["n_pool"] == n_train and r["status"] == "ok"]
            key = f"{name}_n{n_train}"
            if not rs:
                errs = {r.get("error", "?") for r in rows
                        if r["model"] == name and r["n_pool"] == n_train}
                results[key] = {"status": "pending",
                                "error": "; ".join(sorted(errs))[:500]}
                continue
            entry = {"status": "ok",
                     **{f"{m}_mean": sum(r[m] for r in rs) / len(rs)
                        for m in ("q_mse_k1", "q_mse_k10", "q_mse_k100")},
                     **{f"{m}_seed{i}": r[m] for i, r in enumerate(rs)
                        for m in ("q_mse_k1", "q_mse_k10", "q_mse_k100")}}
            for m in ("q_mse_k1", "q_mse_k10", "q_mse_k100"):
                vals = [r[m] for r in rs]
                mean = sum(vals) / len(vals)
                entry[f"{m}_std"] = (sum((v - mean) ** 2 for v in vals)
                                     / (len(vals) - 1)) ** 0.5 if len(vals) > 1 else 0.0
            results[key] = entry

    meta = run_metadata({"benchmark": "tsfm_baseline_eval", "device": "cpu"})
    meta.update({"exec_tier": os.environ.get("PROBE_TIER", "unmanaged"),
                 "tier_est_min": os.environ.get("PROBE_EST_MIN", ""),
                 "chronos_model": args.chronos_model,
                 "timesfm_repo": args.timesfm_repo,
                 "timesfm_path": args.timesfm_path,
                 "num_samples": args.num_samples,
                 "protocol": "docs/tsfm-baseline-protocol.md",
                 "fairness": ["data-regime mismatch (cross-domain pretraining vs "
                              "n<=512 in-context line)",
                              "category-crossing reference, not a ranking "
                              "(no conservation/symplectic structure on TSFM side)",
                              "reader reference; either outcome informative"]})

    def _json_safe(o):
        if isinstance(o, float) and not np.isfinite(o):
            return None
        raise TypeError(o)

    out = os.path.join(args.out_dir, "tsfm_baseline.json")
    with open(out, "w") as f:
        json.dump({"args": vars(args), "meta": meta, "results": results,
                   "rows": rows}, f, indent=2, default=_json_safe)
    print(f"\nwrote {out}", flush=True)
    print("\nTSFM-BASELINE | q-only rollout MSE by k (mean over 3 seeds; "
          "tabulated against d1b q+p arms in PRD §19 — different channel "
          "denominator, protocol §1)", flush=True)
    for key, r in results.items():
        if r.get("status") == "ok":
            print(f"  {key:14s}: k1 {r['q_mse_k1_mean']:.4e}  "
                  f"k10 {r['q_mse_k10_mean']:.4e}  "
                  f"k100 {r['q_mse_k100_mean']:.4e} "
                  f"(±{r['q_mse_k100_std']:.1e})", flush=True)
        else:
            print(f"  {key:14s}: PENDING — {r.get('error', '')[:120]}", flush=True)


if __name__ == "__main__":
    main()
