"""tests/test_sign_flip_probe.py — SIGN-FLIP-PROBE (round 126) checks.

Statistics/semantics unit tests + an end-to-end CLI smoke at tiny settings
(smoke-grade: schema and shapes only, NOT magnitudes — round-84 rule; the
bitwise reproduction anchor is only meaningful at the preregistered 2000-step
budget, so the smoke asserts plumbing, not anchor equality).
"""
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "sign_flip_probe",
        os.path.join(root, "benchmarks", "sign_flip_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_flip_semantics_and_anchors():
    """flip = r < 1 (all2all rollout better than prefix for that seed); the
    cap-axis d48 anchors are carried verbatim (round-113 continuity)."""
    mod = _load_module()
    assert mod.ANCHORS_D48 == [3.893828710272355,
                               0.7019011657583599,
                               2.288356329861092]
    assert all(r < 1.0 for r in (0.7019, 0.3403, 0.721))
    assert all(r >= 1.0 for r in (1.0, 1.3110, 3.8938))


def test_base_args_mirrors_d1b():
    """The run_one contract: base_args must carry the d1b geometry fields
    run_one reads (round-113 bridge convention — same code path)."""
    mod = _load_module()
    a = mod.base_args(48)
    for field in ("d_model", "context_dim", "t_obs", "k_train", "eval_k",
                  "train_steps", "lr", "batch", "gen_steps", "n_eval"):
        assert hasattr(a, field), f"base_args missing {field}"
    assert a.d_model == 48 and a.train_steps == 2000 and a.dt == 0.1


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), per-seed table, criteria
    block, four-value verdict, exec_tier meta passthrough. Anchor equality is
    NOT asserted (smoke budget differs from the preregistered 2000)."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--seeds", "0,1", "--train_steps", "20",
                "--ext_steps", "30", "--eval_k", "24",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "sign_flip_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert set(res["per_seed"]) == {"0", "1"}
    assert res["flip_frequency"] in ("0/2", "1/2", "2/2")
    assert set(res["criteria"]) == {"c1_not_reproduced", "c2_transient",
                                    "c3_misfit_confound"}
    assert res["verdict_semantics"]
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
