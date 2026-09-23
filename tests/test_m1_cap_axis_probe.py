"""tests/test_m1_cap_axis_probe.py — M1-CAP-AXIS (round 113) checks.

Contract test (base_args mirrors the d1b protocol args the bridge gates
depend on) + an end-to-end smoke at tiny settings (smoke-grade: schema and
shape evidence only — round-84 product-generation rule).
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load():
    spec = importlib.util.spec_from_file_location(
        "m1_cap_axis_probe",
        os.path.join(ROOT, "benchmarks", "m1_cap_axis_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_base_args_mirrors_d1b_contract():
    """The bridge gates (round 113 prereg) are only meaningful if the run
    config matches the d1b artifact args exactly where it claims to."""
    mod = _load()
    a = mod.base_args(48)
    assert (a.context_dim, a.n_scales, a.hidden, a.depth) == (8, 4, 48, 2)
    assert (a.t_obs, a.k_train, a.eval_k, a.train_steps) == (24, 8, 100, 2000)
    assert (a.dt, a.omega_lo, a.omega_hi, a.lr, a.lr_decay, a.batch) == \
        (0.1, 0.7, 1.8, 3e-3, 1.0, 64)
    assert a.two_stage is False and a.start_mix == 0.0
    assert a.adaptive_sampling is False and a.probe_context is True
    assert a.eval_ks_list == []


def test_probe_cli_smoke(tmp_path):
    """Tiny end-to-end: schema (results key), r_by_dmodel, criteria block,
    sign-reversal counts, exec_tier meta."""
    mod = _load()
    sys.argv = [sys.argv[0], "--n_train", "8", "--n_eval", "8",
                "--gen_steps", "40", "--train_steps", "15", "--eval_k", "8",
                "--seeds", "0", "--d_models", "24",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "m1_cap_axis.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert "d24_prefix" in res["by_config"]
    assert "d24_all2all" in res["by_config"]
    r = res["r_by_dmodel"]["24"]
    for key in ("mse_prefix_mean", "mse_all2all_mean", "ratio",
                "per_seed_ratio", "sign_reversals"):
        assert key in r
    assert set(res["criteria"]) == {"c1_bridge_broken",
                                    "c2_low_capacity_artifact",
                                    "c3_training_failed"}
    assert res["sign_reversals_by_dmodel"] == {"24": r["sign_reversals"]}
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
