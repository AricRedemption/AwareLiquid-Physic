"""tests/test_r1d_mode_scan.py — R1D-MODE-SCAN (round 122) checks.

Statistics unit tests (spearman/normalized-error semantics — the round-122
judgment hinges on their meaning) + an end-to-end CLI smoke at tiny settings
(smoke-grade: schema and shapes only, NOT magnitudes — round-84 rule).
"""
import importlib.util
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "r1d_mode_scan",
        os.path.join(root, "benchmarks", "r1d_mode_scan.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_spearman_rank_semantics():
    """The gate statistic must mean what the preregistration says: perfect
    monotone increase = +1, decrease = -1, and NEAR-TIED inputs must NOT
    fabricate a strong ranking (the round-122 reading: rho over noise-level
    e values carries no direction information)."""
    mod = _load_module()
    assert mod.spearman_rho([1, 2, 3, 4], [10, 20, 30, 40]) == 1.0
    assert mod.spearman_rho([1, 2, 3, 4], [40, 30, 20, 10]) == -1.0
    # near-tied values differing by <5% must land mid-scale, not at the poles
    near_tied = [1.184, 1.176, 1.052, 0.968]
    rho = mod.spearman_rho([1, 2, 3, 4], near_tied)
    assert -1.0 <= rho <= 1.0
    assert mod.spearman_rho([1, 2, 3, 4], [1.0, 1.0, 1.0, 1.0]) == 0.0, \
        "all-tied inputs have zero rank spread => rho defined as 0"


def test_normalized_error_semantics():
    """e_j = RMSE(pred - true)/std(true): perfect decoding ~ 0, predicting
    the mean ~ 1, anti-correlated garbage > 1 — the scale the judgment
    reads ('no extraction signal' = all e ~ 1)."""
    mod = _load_module()
    torch.manual_seed(0)
    y = torch.randn(64, 1) * 3.0 + 5.0
    perfect = y.clone()
    mean_pred = torch.zeros_like(y) + y.mean()
    garbage = y.mean() + torch.randn(64, 1) * y.std()
    anti = y.mean() - 2.0 * (y - y.mean())

    def err(pred, true):
        return ((pred - true) ** 2).mean().sqrt().item() / true.std().item()

    assert err(perfect, y) < 1e-6
    # torch.std is the n-1 sample std while RMSE uses n => exactly
    # sqrt((n-1)/n); the ~1 semantics is what matters, not the last ulp
    assert abs(err(mean_pred, y) - (63 / 64) ** 0.5) < 1e-6
    assert err(garbage, y) > 0.9
    assert err(anti, y) > 1.9


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), per-coordinate table,
    criteria block, verdict field, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "16", "--n_eval", "8", "--gen_steps", "48",
                "--t_obs", "12", "--eval_k", "16", "--n_nodes", "16",
                "--train_steps", "5", "--batch", "8", "--d_model", "16",
                "--modes", "4", "--width", "16", "--hidden", "16",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "r1d_mode_scan.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert len(res["per_coordinate"]) == 8
    assert res["sin_mode_ordinals"] == [1, 2, 3, 4]
    assert len(res["sin_mode_err_normalized"]) == 4
    assert -1.0 <= res["spearman_rho_ordinal_vs_err"] <= 1.0
    assert set(res["criteria"]) == {"c1_prophecy_flat", "c2_weak_trend"}
    assert res["mse_all_inferred"] >= 0.0 and res["mse_all_oracle"] >= 0.0
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
