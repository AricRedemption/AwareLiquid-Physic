"""tests/test_residual_spec_probe.py — RESIDUAL-SPEC (round 219) checks.

Diagnostic-round semantics (no pass/fail gate; readings are the
deliverable) + an end-to-end CLI smoke at tiny settings (smoke-grade:
schema and shapes only, NOT magnitudes — round-84 rule).
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
        "residual_spec_probe",
        os.path.join(root, "benchmarks", "residual_spec_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.NORM_CAP == 1e6 and mod.DT == 0.1


def test_residual_spec_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), spectrum arrays,
    diagnostic-round verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--rollout_k", "20",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "residual_spec.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert res["verdict"] in ("RESIDUAL_PROFILED", "RESIDUAL_UNRESOLVABLE")
    if res["verdict"] == "RESIDUAL_PROFILED":
        assert "dominant_peak_freq" in res["verdict_detail"]["readings"]
        assert len(res["spectrum_freqs"]) > 0
        assert len(res["spectrum_power"]) == len(res["spectrum_freqs"])
    assert res["criteria"].get("c_profiled") is True or \
        res["criteria"].get("c_unresolvable") is True
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
