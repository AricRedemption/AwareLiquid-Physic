"""tests/test_fastslow_probe.py — FASTSLOW-PROBE (round 137) checks.

Physics/unit-semantics tests (truth generator energy sanity, gate
classification) + an end-to-end CLI smoke at tiny settings (smoke-grade:
schema and shapes only, NOT magnitudes — round-84 rule).
"""
import importlib.util
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "fastslow_probe",
        os.path.join(root, "benchmarks", "fastslow_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_truth_generator_energy_and_rest_length():
    """Elastic-pendulum truth: VV energy drift must be tiny over a short
    run, and the spring must stay stretched near L0 (the fast mode's
    operating point) — the family the head is asked to fit."""
    mod = _load_module()
    qs, ps = mod.gen_pendulum(8, 300, 0.02, seed=0)
    E = mod.true_energy(qs, ps)                    # (8, 301)
    e_scale = E.abs().mean().clamp_min(1e-6)
    drift = ((E - E[:, :1]).abs() / e_scale).max()
    assert drift.item() < 0.05, f"VV truth drifted {drift.item():.3f}"
    norm = qs.norm(dim=-1)
    assert (norm > 0.3).all() and (norm < 3.0).all(), "spring left sanity"
    assert torch.isfinite(qs).all() and torch.isfinite(ps).all()


def test_gate_classification_semantics():
    """The four-way verdict must follow the preregistered gate table."""
    gate_fast, gate_long = 0.01, 0.1

    def verdict(ef, el):
        fast_ok, long_ok = ef <= gate_fast, el <= gate_long
        if fast_ok and long_ok:
            return "BOTH_CAPTURED"
        if fast_ok:
            return "FAST_ONLY"
        if long_ok:
            return "SLOW_ONLY"
        return "BOTH_FAILED"

    assert verdict(0.005, 0.05) == "BOTH_CAPTURED"
    assert verdict(0.005, 1.2) == "FAST_ONLY"
    assert verdict(0.5, 0.05) == "SLOW_ONLY"
    assert verdict(0.0316, 1.2166) == "BOTH_FAILED"


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), axes, criteria, verdict,
    exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "101",
                "--train_steps", "10", "--k_fast", "20", "--k_long", "50",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "fastslow_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert "axis_A_fast" in res and "axis_B_long" in res
    assert "axis_C_stiffness_documentation" in res
    assert set(res["criteria"]) == {"c_fast_not_captured", "c_slow_lost"}
    assert res["verdict"] in ("BOTH_CAPTURED", "FAST_ONLY", "SLOW_ONLY",
                              "BOTH_FAILED")
    assert math.isfinite(res["true_energy_drift_max_long"])
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
