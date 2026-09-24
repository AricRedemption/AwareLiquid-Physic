"""tests/test_gns_probe.py — GNS-PROBE (round 149) checks.

Preregistered estimator/verdict semantics on synthetic gradients (pure)
+ an end-to-end CLI smoke at tiny settings (smoke-grade: schema and
shapes only, NOT magnitudes — round-84 rule).
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
        "gns_probe", os.path.join(root, "benchmarks", "gns_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_b_simple_recovers_known_ratio():
    """On synthetic gradients with known noise/signal structure the
    first-order estimator must land in the right regime."""
    mod = _load_module()
    torch.manual_seed(0)
    b = 64
    # signal along e0 with scale s; isotropic noise with scale n/sqrt(P)
    P = 512
    s, n = 10.0, 1.0
    gbar = torch.zeros(P)
    gbar[0] = s
    noise = torch.randn(256, P) * n
    grads = gbar.unsqueeze(0) + noise / b ** 0.5  # batch-averaged noise
    bs, gnorm_sq, tr_g = mod.b_simple(grads, b)
    assert math.isfinite(bs) and bs > 0
    # expected: tr(G) = P * n² ; |ĝ|² = s²  =>  B ≈ P n² / s² = 5.12
    assert 1.0 < bs < 30.0, f"B_simple {bs:.2f} outside coarse window"
    assert gnorm_sq > 0 and tr_g > 0


def test_verdict_preregistered_branches():
    """UNRESOLVABLE on zero-gradient / non-finite; RESOLVED_TREND at
    >=3x spread; FLAT otherwise, with regime reported either way."""
    mod = _load_module()
    # zero mean gradient at a checkpoint => negative branch
    v, d = mod.classify_gns([0, 1000], [1e-20, 1.0], [5.0, 5.0])
    assert v == "GNS_UNRESOLVABLE"
    assert "vanished" in d["reason"] or "non-finite" in d["reason"]
    # non-finite B_simple => negative branch
    v, _ = mod.classify_gns([0, 1000], [1.0, 1.0],
                            [float("inf"), 5.0])
    assert v == "GNS_UNRESOLVABLE"
    # growing trend, >=3x
    v, d = mod.classify_gns([0, 1000, 4000], [1.0, 1.0, 1.0],
                            [2.0, 4.0, 20.0])
    assert v == "GNS_RESOLVED_TREND"
    assert d["trend"] == "growing" and d["max_min_ratio"] >= 3.0
    # flat: magnitude reading stands, regime reported
    v, d = mod.classify_gns([0, 1000, 4000], [1.0, 1.0, 1.0],
                            [10.0, 12.0, 11.0])
    assert v == "GNS_FLAT"
    assert "not resolvable" in d["criterion"]
    assert d["regime_at_64"] in ("linear-speedup (signal-dominated)",
                                 "noise-dominated")


def test_gns_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), checkpoints present,
    criteria, verdict semantics, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "8", "--gen_steps", "40",
                "--t_obs", "10", "--k_train", "4",
                "--hidden", "8", "--d_model", "8",
                "--grad_samples", "4", "--checkpoints", "0,2",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "gns_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert [r["checkpoint_steps"] for r in res["checkpoints"]] == [0, 2]
    for r in res["checkpoints"]:
        assert math.isfinite(r["gnorm_sq"])
        assert math.isfinite(r["tr_g"])
    assert res["verdict"] in ("GNS_UNRESOLVABLE", "GNS_RESOLVED_TREND",
                              "GNS_FLAT")
    assert res["verdict_detail"]["regime_at_64"] in (
        "linear-speedup (signal-dominated)", "noise-dominated")
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
