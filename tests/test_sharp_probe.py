"""tests/test_sharp_probe.py — SHARP-PROBE (round 154) checks.

Preregistered verdict semantics (pure, synthetic Hessian via quadratic
model) + an end-to-end CLI smoke at tiny settings (smoke-grade: schema
and shapes only, NOT magnitudes — round-84 rule).
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
        "sharp_probe", os.path.join(root, "benchmarks", "sharp_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """UNRESOLVABLE on non-convergence; EOS/BELOW/ABOVE by the
    lambda*lr window; trend semantics recorded."""
    mod = _load_module()
    # non-convergence at any checkpoint => negative branch
    v, d = mod.classify_sharp([10.0, 20.0], [True, False])
    assert v == "SHARP_UNRESOLVABLE"
    assert "did not converge" in d["reason"]
    # EOS window
    v, d = mod.classify_sharp([0.5, 2.1, 8.0], [True, True, True])
    assert v == "SHARP_EOS"
    assert 1 in d["eos_checkpoints"]
    # below classical regime
    v, d = mod.classify_sharp([0.3, 1.2, 1.4], [True] * 3)
    assert v == "SHARP_BELOW"
    # deep unstable
    v, d = mod.classify_sharp([4.0, 9.0], [True] * 2)
    assert v == "SHARP_ABOVE"


def test_classifier_thresholds_are_preregistered():
    """The EOS window constants must match the preregistration
    (threshold 2 +/- 50%)."""
    mod = _load_module()
    assert mod.EOS_LO == 1.5 and mod.EOS_HI == 3.0
    assert mod.CONV_GATE == 0.10 and mod.POWER_ITERS == 20


def test_sharp_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), checkpoints, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_loss_batch", "4",
                "--gen_steps", "40", "--t_obs", "10", "--k_train", "4",
                "--hidden", "8", "--d_model", "8",
                "--power_iters", "5", "--checkpoints", "0,2",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "sharp_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert [r["checkpoint_steps"] for r in res["checkpoints"]] == [0, 2]
    for r in res["checkpoints"]:
        assert math.isfinite(r["lambda_max"])
        assert math.isfinite(r["lambda_lr"])
    assert res["verdict"] in ("SHARP_UNRESOLVABLE", "SHARP_EOS",
                              "SHARP_BELOW", "SHARP_ABOVE")
    assert res["trend_reading"] in ("rising", "falling", "flat")
    assert "Adam" in res["adam_caveat"]
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
