"""tests/test_grok_curve.py — GROK-CURVE (round 146) checks.

Preregistered shape-classifier semantics (pure) + an end-to-end CLI
smoke at tiny settings (smoke-grade: schema and shapes only, NOT
magnitudes — round-84 rule).
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
        "grok_curve", os.path.join(root, "benchmarks", "grok_curve.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_classifier_preregistered_branches():
    """GROKKING_SIGNATURE requires a >=3x adjacent drop AFTER fit
    saturation; otherwise SMOOTH_ASYMPTOTE (the negative branch)."""
    mod = _load_module()
    steps = [2500, 5000, 10000, 20000, 40000]

    # smooth power-law-ish descent, no big drop
    v, d = mod.classify_grok(steps, [1e-2, 6e-3, 4e-3, 2.5e-3, 1.6e-3],
                             [1e-3, 5e-4, 2e-4, 8e-5, 3e-5])
    assert v == "SMOOTH_ASYMPTOTE"
    assert d["max_ratio"] < mod.RATIO_GATE

    # big drop but the fit was NOT saturated at the drop => ordinary
    # convergence, NOT grokking
    v, d = mod.classify_grok(steps, [1e-1, 1e-3, 8e-4, 6e-4, 5e-4],
                             [1e-1, 5e-3, 2e-3, 1e-3, 5e-4])
    assert v == "SMOOTH_ASYMPTOTE"

    # big drop AFTER saturation => grokking signature
    v, d = mod.classify_grok(steps, [1e-2, 9e-3, 8e-3, 2e-3, 5e-4],
                             [5e-5, 3e-5, 2e-5, 1e-5, 5e-6])
    assert v == "GROKKING_SIGNATURE"
    assert d["transition_at_steps"] == 20000
    assert d["drop_ratio"] >= mod.RATIO_GATE


def test_negative_branch_is_explicit():
    """The negative-branch detail must name the preregistered outcome:
    grokking naming not applicable, asymptotic improvement recorded."""
    mod = _load_module()
    v, d = mod.classify_grok([100, 200], [1e-2, 9e-3], [1e-4, 5e-5])
    assert v == "SMOOTH_ASYMPTOTE"
    assert "not applicable" in d["criterion"]


def test_grok_curve_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), ladder points, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "40",
                "--t_obs", "10", "--eval_k", "20",
                "--steps", "2,4", "--hidden", "8", "--d_model", "8",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "grok_curve.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert [pt["steps"] for pt in res["ladder"]] == [2, 4]
    for pt in res["ladder"]:
        assert math.isfinite(pt["rollout_mse"])
        assert math.isfinite(pt["train_loss"])
    assert res["verdict"] in ("SMOOTH_ASYMPTOTE", "GROKKING_SIGNATURE")
    assert set(res["criteria"]) == {"c_smooth_no_transition",
                                    "c_transition_after_saturation"}
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
