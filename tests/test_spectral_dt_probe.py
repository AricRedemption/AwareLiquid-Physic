"""tests/test_spectral_dt_probe.py — SPECTRAL-DT (round 162) checks.

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
        "spectral_dt_probe",
        os.path.join(root, "benchmarks", "spectral_dt_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Cell failure takes precedence; interaction by the >=20% excess of
    the high-frequency ratio over the low-frequency ratio; otherwise
    unresolved (frequency main effect may still hold — noted)."""
    mod = _load_module()
    cells = [(1.0, 0.05, 1.0), (1.0, 0.2, 1.5),
             (4.0, 0.05, 2.0), (4.0, 0.2, 10.0)]
    # R1 = 1.5, R4 = 5.0 => excess = (5-1.5)/1.5 ≈ 233% >= 20%
    v, d = mod.classify_interaction(cells, 5.0, 1.5)
    assert v == "INTERACTION_RESOLVED"
    assert d["excess"] >= 0.20
    # flat ratios => unresolved, with the interaction-only caveat
    v, d = mod.classify_interaction(cells, 1.6, 1.5)
    assert v == "INTERACTION_UNRESOLVABLE"
    assert "interaction only" in d["criterion"]
    # cell failure takes precedence over everything
    bad = cells + [(2.0, 0.1, 1e7)]
    v, d = mod.classify_interaction(bad, 5.0, 1.5)
    assert v == "CELL_FAILURE"
    assert "negative branch" in d["reason"]


def test_ratios_need_real_interaction_not_main_effect():
    """A uniform main effect (both frequencies scale identically with dt)
    must NOT count as interaction."""
    mod = _load_module()
    v, _ = mod.classify_interaction([], 3.0, 3.0)   # R4 == R1 exactly
    assert v == "INTERACTION_UNRESOLVABLE"


def test_spectral_dt_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), 8 cells (2x2),
    criteria, verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4",
                "--omegas", "1.0,4.0", "--dts", "0.05,0.1",
                "--horizon_T", "1.0",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "spectral_dt.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert len(res["cells"]) == 4
    for c in res["cells"]:
        assert math.isfinite(c["rollout_mse"])
        assert "nyquist_fraction" in c
    assert res["verdict"] in ("CELL_FAILURE", "INTERACTION_RESOLVED",
                              "INTERACTION_UNRESOLVABLE")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
