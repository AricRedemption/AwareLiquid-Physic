"""tests/test_warmup_probe.py — WARMUP-PROBE (round 212) checks.

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
        "warmup_probe",
        os.path.join(root, "benchmarks", "warmup_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on divergence; unresolved within gate; warmup
    beneficial/harmful directions."""
    mod = _load_module()
    v, d = mod.classify_warmup(float("nan"), 1.0)
    assert v == "WARMUP_UNRESOLVABLE" and "negative branch" in d["reason"]
    v, d = mod.classify_warmup(1.02, 1.00)
    assert v == "WARMUP_UNRESOLVABLE"
    assert "not resolvable" in d["criterion"]
    v, d = mod.classify_warmup(1.40, 1.00)
    assert v == "WARMUP_BENEFICIAL" and d["diff"] >= 0.05
    v, d = mod.classify_warmup(0.90, 1.10)
    assert v == "WARMUP_HARMFUL" and d["diff"] <= -0.05


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.DIFF_GATE == 0.05 and mod.NORM_CAP == 1e6
    assert mod.WARMUP_STEPS == 200


def test_warmup_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--warmup_steps", "1",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "warmup_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert math.isfinite(res["arms"]["A_constant"])
    assert math.isfinite(res["arms"]["B_warmup"])
    assert res["verdict"] in ("WARMUP_UNRESOLVABLE", "WARMUP_BENEFICIAL",
                              "WARMUP_HARMFUL")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
