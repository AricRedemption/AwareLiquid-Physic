"""tests/test_rep_probe.py — REP-PROBE (round 159) checks.

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
        "rep_probe", os.path.join(root, "benchmarks", "rep_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_classifier_preregistered_branches():
    """|diff| < 5% => UNRESOLVABLE (negative branch); A worse by >=5%
    => HARMFUL; A better by >=5% => HELPFUL."""
    mod = _load_module()
    v, d = mod.classify_rep(1.00, 1.03)
    assert v == "REP_UNRESOLVABLE"
    assert "not resolvable" in d["criterion"]
    v, d = mod.classify_rep(1.20, 1.00)
    assert v == "REP_REPETITION_HARMFUL"
    assert d["diff"] >= mod.DIFF_GATE
    v, d = mod.classify_rep(0.90, 1.10)
    assert v == "REP_REPETITION_HELPFUL"
    assert d["diff"] <= -mod.DIFF_GATE


def test_classifier_symmetry_boundary():
    """Exactly-at-gate values must resolve (>= / <=), and the diff sign
    convention must be (A-B)/max(A,B)."""
    mod = _load_module()
    v, d = mod.classify_rep(1.05, 1.00)          # diff = +5/105 ≈ 4.8% < 5%
    assert v == "REP_UNRESOLVABLE"
    v, d = mod.classify_rep(2.00, 1.00)          # diff = +50%
    assert v == "REP_REPETITION_HARMFUL" and d["diff"] > 0
    v, d = mod.classify_rep(1.00, 2.00)          # diff = -50%
    assert v == "REP_REPETITION_HELPFUL" and d["diff"] < 0


def test_rep_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "40",
                "--t_obs", "10", "--k_train", "4", "--eval_k", "20",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "6", "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "rep_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert set(res["arms"]) == {"A", "B"}
    for arm in res["arms"].values():
        assert math.isfinite(arm["rollout_mse"])
        assert math.isfinite(arm["train_loss"])
    assert res["verdict"] in ("REP_UNRESOLVABLE", "REP_REPETITION_HARMFUL",
                              "REP_REPETITION_HELPFUL")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
