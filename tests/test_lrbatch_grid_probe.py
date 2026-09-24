"""tests/test_lrbatch_grid_probe.py — LRBATCH-GRID (round 205) checks.

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
        "lrbatch_grid_probe",
        os.path.join(root, "benchmarks", "lrbatch_grid_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on divergence; rule identification by the
    5% equivalence gate on each preregistered pair."""
    mod = _load_module()
    cells = {(16, 3e-3): 1.0, (64, 3e-3): 1.1, (64, 6e-3): 1.08,
             (16, 1.2e-2): 1.05, (64, 1.2e-2): 1.0}
    v, d = mod.classify_scaling(cells,
                                linear_pair=((16, 3e-3), (64, 1.2e-2)),
                                sqrt_pair=((16, 3e-3), (64, 6e-3)))
    assert v in ("LINEAR_RULE", "SQRT_RULE", "SCALING_BROKEN",
                 "LRBATCH_UNRESOLVABLE")
    # divergence at any cell => negative branch
    bad = dict(cells)
    bad[(16, 3e-3)] = float("nan")
    v, d = mod.classify_scaling(bad,
                                linear_pair=((16, 3e-3), (64, 1.2e-2)),
                                sqrt_pair=((16, 3e-3), (64, 6e-3)))
    assert v == "LRBATCH_UNRESOLVABLE"


def test_classifier_rule_directions():
    """ LINEAR vs SQRT identification on clean synthetic cells."""
    mod = _load_module()
    # linear pair matches (within 5%), sqrt pair differs (>=5%)
    cells = {(16, 3e-3): 1.00, (64, 1.2e-2): 1.02, (64, 6e-3): 1.30}
    v, d = mod.classify_scaling(cells,
                                linear_pair=((16, 3e-3), (64, 1.2e-2)),
                                sqrt_pair=((16, 3e-3), (64, 6e-3)))
    assert v == "LINEAR_RULE", v
    # sqrt pair matches instead
    cells2 = {(16, 3e-3): 1.00, (64, 1.2e-2): 1.40, (64, 6e-3): 1.02}
    v, d = mod.classify_scaling(cells2,
                                linear_pair=((16, 3e-3), (64, 1.2e-2)),
                                sqrt_pair=((16, 3e-3), (64, 6e-3)))
    assert v == "SQRT_RULE"


def test_lrbatch_grid_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), all cells, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "lrbatch_grid.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert len(res["cells"]) == 5
    for c in res["cells"].values():
        assert math.isfinite(c["rollout_mse"])
    assert res["verdict"] in ("LRBATCH_UNRESOLVABLE", "SCALING_BROKEN",
                              "LINEAR_RULE", "SQRT_RULE")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
