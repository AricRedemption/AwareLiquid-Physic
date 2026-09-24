"""tests/test_opt_compare_probe.py — OPT-COMPARE (round 178) checks.

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
        "opt_compare_probe",
        os.path.join(root, "benchmarks", "opt_compare_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Divergence/negative branch first (lr-budget mismatch, not an
    optimizer verdict); unresolved within gate; SGD/Adam directions."""
    mod = _load_module()
    v, d = mod.classify_opt(float("nan"), 1.0)
    assert v == "OPT_UNRESOLVABLE" and "lr-budget" in d["reason"]
    v, d = mod.classify_opt(1.0, 1e8)
    assert v == "OPT_UNRESOLVABLE"
    v, d = mod.classify_opt(1.02, 1.00)
    assert v == "OPT_UNRESOLVABLE" and "no single winner" in d["criterion"]
    v, d = mod.classify_opt(1.40, 1.00)
    assert v == "OPT_SGD_BETTER" and d["diff"] >= 0.05
    v, d = mod.classify_opt(0.80, 1.00)
    assert v == "OPT_ADAM_BETTER" and d["diff"] <= -0.05


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.DIFF_GATE == 0.05 and mod.NORM_CAP == 1e6


def test_opt_compare_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "opt_compare.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert set(res["arms"]) == {"ADAM", "SGDM"}
    for arm in res["arms"].values():
        assert math.isfinite(arm["rollout_mse"])
        assert math.isfinite(arm["train_loss"])
    assert res["verdict"] in ("OPT_UNRESOLVABLE", "OPT_SGD_BETTER",
                              "OPT_ADAM_BETTER")
    assert "tuning" in res["limit_note"] or "tuned" in res["limit_note"]
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
