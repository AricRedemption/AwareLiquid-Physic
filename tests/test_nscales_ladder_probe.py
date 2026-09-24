"""tests/test_nscales_ladder_probe.py — NSCALES-LADDER (round 197)
checks.

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
        "nscales_ladder_probe",
        os.path.join(root, "benchmarks", "nscales_ladder_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on divergence; unresolved below spread gate;
    resolved reports best n_scales and direction."""
    mod = _load_module()
    vals = [1, 2, 4, 8]
    v, d = mod.classify_nscales(vals, [float("nan"), 1.0, 1.0, 1.0])
    assert v == "NSCALES_UNRESOLVABLE" and "unusable" in d["reason"]
    v, d = mod.classify_nscales(vals, [1.0, 1.02, 1.01, 1.03])
    assert v == "NSCALES_UNRESOLVABLE" and "default sufficient" in d["criterion"]
    v, d = mod.classify_nscales(vals, [2.0, 1.5, 1.2, 1.0])
    assert v == "NSCALES_RESOLVED" and d["best_n_scales"] == 8
    v, d = mod.classify_nscales(vals, [1.0, 1.5, 2.5, 4.0])
    assert v == "NSCALES_RESOLVED" and "fewer scales" in d["direction"]
    v, d = mod.classify_nscales(vals, [1.6, 1.2, 1.5, 1.4])
    assert v == "NSCALES_RESOLVED" and "interior optimum" in d["direction"]


def test_gate_constants_preregistered():
    mod = _load_module()
    assert mod.SPREAD_GATE == 1.05 and mod.NORM_CAP == 1e6
    assert mod.LADDER == (1, 2, 4, 8)


def test_nscales_ladder_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), all arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--n_scales_list", "1,2",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "nscales_ladder.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert len(res["arms"]) == 2
    for arm in res["arms"].values():
        assert math.isfinite(arm["rollout_mse"])
        assert arm["params"] > 0
    assert res["verdict"] in ("NSCALES_UNRESOLVABLE", "NSCALES_RESOLVED")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
