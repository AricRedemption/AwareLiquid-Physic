"""tests/test_amp_extrap_probe.py — AMP-EXTRAP (round 216) checks.

Relative-calibre classifier semantics (pure) + an end-to-end CLI smoke
at tiny settings (smoke-grade: schema and shapes only, NOT magnitudes —
round-84 rule) + the scale=1 watchdog (round-181 rule: scaled generator
must be bit-identical to the original at scale=1).
"""
import importlib.util
import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "amp_extrap_probe",
        os.path.join(root, "benchmarks", "amp_extrap_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verdict_preregistered_branches():
    """Negative branch on divergence; ROBUST below gate; DEGRADES at or
    above."""
    mod = _load_module()
    v, d = mod.classify_amp([float("nan"), 1.0])
    assert v == "AMPEX_UNRESOLVABLE" and "negative branch" in d["reason"]
    v, d = mod.classify_amp([1.0, 1.2, 1.5])
    assert v == "AMPEX_ROBUST" and "robust" in d["criterion"]
    v, d = mod.classify_amp([1.0, 2.0, 5.0])
    assert v == "AMPEX_DEGRADES" and d["rel_comp"] >= 3.0


def test_scaled_generator_bit_identical_at_scale_1():
    """Watchdog (round-181 rule): the scaled generator at scale=1 must be
    bit-identical to the original gen_spring (same seed)."""
    mod = _load_module()
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "m1_gen", os.path.join(root, "benchmarks", "m1_semigroup_eval.py"))
    m1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m1)
    g1 = torch.Generator().manual_seed(0)
    g2 = torch.Generator().manual_seed(0)
    a = m1.gen_spring(8, 40, 0.1, 1, 0.7, 1.8, g1)
    b = mod.gen_spring_scaled(8, 40, 0.1, 0.7, 1.8, g2, scale=1.0)
    for x, y in zip(a[:2], b[:2]):
        assert torch.equal(x, y), "scale=1 must reproduce the original"


def test_amp_extrap_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), all scale arms, criteria,
    verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--n_eval", "4", "--gen_steps", "41",
                "--t_obs", "6", "--k_train", "4", "--eval_k", "10",
                "--hidden", "8", "--d_model", "8",
                "--train_steps", "4", "--scales", "1,2",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "amp_extrap.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert len(res["arms"]) == 2
    for arm in res["arms"].values():
        assert math.isfinite(arm["rollout_mse"])
        assert math.isfinite(arm["rel_mse"])
    assert res["verdict"] in ("AMPEX_UNRESOLVABLE", "AMPEX_ROBUST",
                              "AMPEX_DEGRADES")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
