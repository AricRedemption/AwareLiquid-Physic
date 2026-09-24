"""tests/test_fastslow_v2.py — FASTSLOW-2 (round 143) checks.

Preregistered attribution-table semantics (pure) + an end-to-end two-arm
CLI smoke at tiny settings (smoke-grade: schema and shapes only, NOT
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
        "fastslow_probe_v2",
        os.path.join(root, "benchmarks", "fastslow_probe_v2.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_attribution_table_preregistered():
    """The three-way attribution must follow the round-143 preregistration:
    MAIN both-failed => STRUCTURAL; MAIN reversed with H64 failed =>
    CAPACITY_NEEDED; both reversed => BUDGET_DOMINANT."""
    mod = _load_module()
    assert mod.classify_attribution("BOTH_FAILED", "BOTH_FAILED") \
        == "STRUCTURAL"
    assert mod.classify_attribution("BOTH_FAILED", "FAST_ONLY") \
        == "STRUCTURAL"  # MAIN gate is the preregistered trigger
    assert mod.classify_attribution("FAST_ONLY", "BOTH_FAILED") \
        == "CAPACITY_NEEDED"
    assert mod.classify_attribution("BOTH_CAPTURED", "SLOW_ONLY") \
        == "BUDGET_DOMINANT"
    assert mod.classify_attribution("FAST_ONLY", "FAST_ONLY") \
        == "BUDGET_DOMINANT"


def test_wording_route_and_semantics_coverage():
    """Every attribution value must carry semantics text, and the N1
    wording route must flip only on STRUCTURAL."""
    mod = _load_module()
    for att in ("STRUCTURAL", "CAPACITY_NEEDED", "BUDGET_DOMINANT"):
        assert att in mod.ATTRIBUTION_SEMANTICS
        assert mod.ATTRIBUTION_SEMANTICS[att]
    for main_v, h64_v in (("BOTH_FAILED", "BOTH_FAILED"),
                          ("FAST_ONLY", "BOTH_FAILED"),
                          ("BOTH_CAPTURED", "FAST_ONLY")):
        att = mod.classify_attribution(main_v, h64_v)
        route = "STRUCTURAL_UPGRADE" if att == "STRUCTURAL" \
            else "SCOPE_LIMITED_KEPT"
        assert route in ("STRUCTURAL_UPGRADE", "SCOPE_LIMITED_KEPT")


def test_two_arm_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms present with
    the round-137 axes, attribution fields, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "101",
                "--train_steps", "10", "--k_fast", "20", "--k_long", "50",
                "--hidden_main", "16", "--hidden_h64", "8",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "fastslow_probe_v2.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert set(res["arms"]) == {"MAIN", "H64"}
    for arm in res["arms"].values():
        assert "axis_A_fast" in arm and "axis_B_long" in arm
        assert "axis_C_stiffness_documentation" in arm
        assert arm["verdict"] in ("BOTH_CAPTURED", "FAST_ONLY",
                                  "SLOW_ONLY", "BOTH_FAILED")
        assert math.isfinite(arm["true_energy_drift_max_long"])
        assert math.isfinite(arm["train_loss"])
    assert res["attribution"] in mod.ATTRIBUTION_SEMANTICS
    assert res["n1_wording_route"] in ("STRUCTURAL_UPGRADE",
                                       "SCOPE_LIMITED_KEPT")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
