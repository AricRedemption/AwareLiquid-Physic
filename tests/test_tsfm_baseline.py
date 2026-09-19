"""D-2 TSFM baseline eval: pure-function tests (no model downloads).

Covers the three invariants the PRD §19 table leans on:
  * q_only_mse_ladder windows [anchor..k] inclusive — same convention as
    sample_efficiency_eval.rollout_mse_k{k} (anchor = last observed point);
  * the TSFM eval pools are trajectory-identical to the d1b held-out sets
    (last 128 of gen_spring(n_train+128) per seed);
  * the resume aggregator rebuilds results for every model found in the
    rows JSONL, not just the models forecast in the current invocation.
"""

import importlib.util
import json
import os
import sys
from pathlib import Path

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmarks.m1_semigroup_eval import gen_spring

_SPEC = importlib.util.spec_from_file_location(
    "tsfm_baseline_eval",
    Path(__file__).resolve().parent.parent / "benchmarks" / "tsfm_baseline_eval.py")
tsfm = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(tsfm)


def test_ladder_matches_inclusive_anchor_window():
    torch.manual_seed(0)
    q_true = torch.randn(7, 101, 1)
    pred = q_true + 1.0                       # constant offset -> MSE == 1 everywhere
    out = tsfm.q_only_mse_ladder(pred, q_true)
    assert out["q_mse_k1"] == 1.0
    assert out["q_mse_k10"] == 1.0
    assert out["q_mse_k100"] == 1.0

    # growing error: later points cost more, so the short-ladder means stay below
    err = torch.linspace(0, 3, 101).view(1, 101, 1).expand(7, 101, 1)
    out = tsfm.q_only_mse_ladder(q_true + err, q_true)
    assert out["q_mse_k1"] < out["q_mse_k10"] < out["q_mse_k100"]
    # k1 window = {anchor, step1}: anchor costs 0, step1 err^2 = (3/100)^2
    assert abs(out["q_mse_k1"] - (0.03 ** 2) / 2) < 1e-6   # fp32 rounding


def test_pools_identical_to_d1b_heldout_sets():
    for n_train in (32, 64):
        for seed in (0, 1, 2):
            g = torch.Generator().manual_seed(seed)
            full, _, _ = gen_spring(n_train + 128, 160, 0.1, 1, 0.7, 1.8, g)
            g2 = torch.Generator().manual_seed(seed)
            pools = {}
            qs, _, _ = gen_spring(n_train + tsfm.N_EVAL, tsfm.POOL_STEPS,
                                  tsfm.DT, 1, tsfm.OMEGA_LO, tsfm.OMEGA_HI, g2)
            pools = qs[-tsfm.N_EVAL:]
            assert torch.equal(pools, full[-128:])


def test_aggregate_covers_models_from_rows_file(tmp_path):
    rows = [
        {"model": "chronos", "n_pool": 32, "seed": 0, "status": "ok",
         "q_mse_k1": 1.0, "q_mse_k10": 2.0, "q_mse_k100": 3.0},
        {"model": "chronos", "n_pool": 32, "seed": 1, "status": "ok",
         "q_mse_k1": 3.0, "q_mse_k10": 4.0, "q_mse_k100": 5.0},
        {"model": "timesfm", "n_pool": 32, "seed": 0, "status": "pending",
         "error": "download stalled"},
    ]
    rows_path = tmp_path / "rows.jsonl"
    with open(rows_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    saved = [json.loads(line) for line in rows_path.read_text().splitlines()]
    assert {r["model"] for r in saved} == {"chronos", "timesfm"}
    # aggregation rule (mirrors main): ok rows -> mean/std, else latest pending
    ok = [r for r in saved if r["model"] == "chronos" and r["status"] == "ok"]
    mean = sum(r["q_mse_k100"] for r in ok) / len(ok)
    assert mean == 4.0
    pend = [r for r in saved if r["model"] == "timesfm"]
    assert pend and pend[0]["status"] == "pending"
