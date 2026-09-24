"""tests/test_pool_width_probe.py — POOL-WIDTH (round 175) checks.

Preregistered classifier semantics (pure) + an end-to-end CLI smoke at
tiny settings (smoke-grade: schema and shapes only, NOT magnitudes —
round-84 rule).
"""
import importlib.util
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "pool_width_probe",
        os.path.join(root, "benchmarks", "pool_width_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on divergence; unresolved within +/-5% of 1;
    COST above; BENEFIT below."""
    mod = _load_module()
    v, d = mod.classify_width(float("inf"))
    assert v == "WIDTH_UNRESOLVABLE" and "non-finite" in d["reason"]
    v, d = mod.classify_width(1.03)
    assert v == "WIDTH_UNRESOLVABLE" and "Kumar" in d["criterion"]
    v, d = mod.classify_width(1.30)
    assert v == "WIDTH_COST" and d["ratio"] > 1.0
    v, d = mod.classify_width(0.70)
    assert v == "WIDTH_BENEFIT" and d["ratio"] < 1.0


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.WIDTH_GATE == 0.05 and mod.NORM_CAP == 1e6
    assert mod.POOLS == {"A": (0.95, 1.05), "B": (0.7, 1.8)}


def test_pool_width_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, ratio,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "pool_width.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert set(res["arms"]) == {"A", "B"}
    for arm in res["arms"].values():
        assert math.isfinite(arm["rollout_mse"])
    assert math.isfinite(res["ratio"]) and res["ratio"] > 0
    assert res["verdict"] in ("WIDTH_UNRESOLVABLE", "WIDTH_COST",
                              "WIDTH_BENEFIT")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
