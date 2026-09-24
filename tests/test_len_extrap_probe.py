"""tests/test_len_extrap_probe.py — LEN-EXTRAP (round 170) checks.

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
        "len_extrap_probe",
        os.path.join(root, "benchmarks", "len_extrap_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on non-finite/negative comp; ROBUST below gate;
    WINDOW_EDGE requires the boundary jump; otherwise GRADUAL."""
    mod = _load_module()
    v, d = mod.classify_len(float("nan"), 1.0)
    assert v == "LEN_DIVERGENT" and "non-finite" in d["reason"]
    v, d = mod.classify_len(-1.0, 1.0)
    assert v == "LEN_DIVERGENT"
    v, d = mod.classify_len(1.5, 10.0)
    assert v == "LEN_ROBUST" and "smooth extrapolation" in d["criterion"]
    v, d = mod.classify_len(8.0, 4.0)
    assert v == "LEN_WINDOW_EDGE" and d["edge_jump"] >= mod.EDGE_GATE
    v, d = mod.classify_len(8.0, 1.2)
    assert v == "LEN_GRADUAL" and "gradual" in d["criterion"]


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.COMP_GATE == 3.0 and mod.EDGE_GATE == 3.0
    assert mod.NORM_CAP == 1e6 and mod.WINDOW_STEPS == 160


def test_len_extrap_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), segments, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4",
                "--t_obs", "6", "--k_train", "4",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--eval_steps", "301",
                "--rollout_k", "300",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "len_extrap.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert len(res["per_step_profile_head"]) == 21
    for k in ("interp_5_10s", "extrap_20_30s"):
        assert k in res["segments"]
        assert math.isfinite(res["segments"][k])
    assert res["verdict"] in ("LEN_DIVERGENT", "LEN_ROBUST",
                              "LEN_WINDOW_EDGE", "LEN_GRADUAL")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
