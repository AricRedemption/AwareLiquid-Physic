"""tests/test_dt_curriculum_probe.py — DT-CURRICULUM (round 165) checks.

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
        "dt_curriculum_probe",
        os.path.join(root, "benchmarks", "dt_curriculum_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_classifier_preregistered_branches():
    """Divergence takes precedence; |diff| < 5% => UNRESOLVABLE;
    A worse by >=5% => BENEFICIAL; A better by >=5% => HARMFUL."""
    mod = _load_module()
    v, d = mod.classify_curriculum(float("inf"), 1.0)
    assert v == "CURRICULUM_UNRESOLVABLE"
    assert "diverged" in d["reason"]
    v, d = mod.classify_curriculum(1.02, 1.00)
    assert v == "CURRICULUM_UNRESOLVABLE"
    assert "strong baseline" in d["criterion"]
    v, d = mod.classify_curriculum(1.30, 1.00)
    assert v == "CURRICULUM_BENEFICIAL"
    assert d["diff"] >= 0.05
    v, d = mod.classify_curriculum(0.90, 1.10)
    assert v == "CURRICULUM_HARMFUL"
    assert d["diff"] <= -0.05


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.DIFF_GATE == 0.05 and mod.DIVERGENCE_CAP == 1e6


def test_dt_curriculum_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--steps_fine", "4", "--steps_coarse", "2",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "dt_curriculum.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert set(res["arms"]) == {"A", "B"}
    for arm in res["arms"].values():
        assert math.isfinite(arm["rollout_mse"])
    assert res["verdict"] in ("CURRICULUM_UNRESOLVABLE",
                              "CURRICULUM_BENEFICIAL",
                              "CURRICULUM_HARMFUL")
    assert "Adam" in res["optimizer_note"]
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
