"""tests/test_omega_extrap_probe.py — OMEGA-EXTRAP (round 115) checks.

End-to-end smoke at tiny settings (schema/shape evidence only, round-84
rule) + a data sanity check (band disjointness of the eval pools).
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load():
    spec = importlib.util.spec_from_file_location(
        "omega_extrap_probe",
        os.path.join(ROOT, "benchmarks", "omega_extrap_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_band_disjointness():
    """The probe's premise: eval bands are disjoint from each other and the
    training band edges (0.3-0.6 < 0.7-1.8 < 1.9-2.2)."""
    assert 0.6 < 0.7 and 1.8 < 1.9
    mod = _load()
    for lo, hi in ((0.7, 1.8), (0.3, 0.6), (1.9, 2.2)):
        _, _, om = mod.make_pool(lo, hi, 8, 0, gen_steps=40)
        assert om.min().item() >= lo - 1e-5 and om.max().item() <= hi + 1e-5


def test_probe_cli_smoke(tmp_path):
    """Tiny end-to-end: schema, per-band MSE, degradation ratios, criteria,
    ctx decode block, exec_tier meta."""
    mod = _load()
    sys.argv = [sys.argv[0], "--n_train", "8", "--n_eval", "8",
                "--gen_steps", "40", "--train_steps", "10",
                "--eval_k", "8", "--k_train", "6",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "omega_extrap.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    for arm in ("liquid", "static"):
        assert set(res["mse_by_band"][arm]) >= {"in", "low", "high",
                                                "in_stderr"}
        assert set(res["degradation_ratio"][arm]) == {"low", "high"}
    for band in ("in", "low", "high"):
        assert "rel_err" in res["ctx_decode"][band]
    assert set(res["criteria"]) == {"c1_pipeline_failed",
                                    "c2_structure_amplifies_ood_risk",
                                    "c3_near_band_collapse"}
    assert isinstance(res["structure_mitigates_ood"], bool)
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
