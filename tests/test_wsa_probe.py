"""tests/test_wsa_probe.py — WSA-PROBE (round 209) checks.

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
        "wsa_probe", os.path.join(root, "benchmarks", "wsa_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on divergence; unresolved within gate; average
    better/worse directions."""
    mod = _load_module()
    v, d = mod.classify_wsa(float("nan"), 1.0)
    assert v == "WSA_UNRESOLVABLE" and "negative branch" in d["reason"]
    v, d = mod.classify_wsa(1.02, 1.00)
    assert v == "WSA_UNRESOLVABLE"
    assert "not resolvable" in d["criterion"]
    v, d = mod.classify_wsa(1.40, 1.00)
    assert v == "SWA_BENEFICIAL" and d["diff"] >= 0.05
    v, d = mod.classify_wsa(0.90, 1.10)
    assert v == "SWA_HARMFUL" and d["diff"] <= -0.05


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.DIFF_GATE == 0.05 and mod.NORM_CAP == 1e6
    assert mod.SNAP_EVERY == 100 and mod.N_SNAPS == 10


def test_wsa_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "10", "--snap_every", "3",
                "--n_snaps", "3", "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "wsa_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert math.isfinite(res["mse_last"])
    assert math.isfinite(res["mse_avg"])
    assert res["verdict"] in ("WSA_UNRESOLVABLE", "SWA_BENEFICIAL",
                              "SWA_HARMFUL")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
