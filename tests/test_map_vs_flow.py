"""tests/test_map_vs_flow.py — MAP-VS-FLOW (round 129) checks.

Statistics unit tests (log-log slope semantics — the gate's corroborating
axis) + an end-to-end CLI smoke at tiny settings (smoke-grade: schema and
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
        "map_vs_flow",
        os.path.join(root, "benchmarks", "map_vs_flow.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_loglog_slope_semantics():
    """The corroborating gate axis: quadratic scaling (VV local error) reads
    ~2, dt-independent (map-like) reads 0."""
    mod = _load_module()
    quad = [(dt, 3.0 * dt ** 2) for dt in (0.05, 0.1, 0.2)]
    assert abs(mod.loglog_slope(quad) - 2.0) < 1e-9
    flat = [(dt, 5e-3) for dt in (0.05, 0.1, 0.2)]
    assert abs(mod.loglog_slope(flat)) < 1e-9
    linear = [(dt, 2.0 * dt) for dt in (0.05, 0.1, 0.2)]
    assert abs(mod.loglog_slope(linear) - 1.0) < 1e-9


def test_eval_at_dt_shapes_and_horizon():
    """eval_at_dt must honor the fixed-horizon contract: k = T/dt per dt
    (round-104 rule) and return the documented metric keys."""
    mod = _load_module()
    from awareliquid_physics.hamiltonian import HamiltonianHead
    torch.manual_seed(0)
    head = HamiltonianHead(dim=1, hidden_dim=8, depth=1, context_dim=0)
    out = mod.eval_at_dt(head, 0.05, 20, 4, seed=0)
    assert out["horizon_T"] == 1.0 and out["k"] == 20
    for key in ("rollout_mse", "one_step_mse", "rollout_mse_stderr"):
        assert key in out and out[key] >= 0.0


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), sweep table, criteria,
    three-value verdict, exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--n_train", "16", "--n_eval", "8", "--gen_steps", "48",
                "--train_steps", "30", "--horizon_T", "2.4",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "map_vs_flow.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    for dt in ("dt0.05", "dt0.1", "dt0.2"):
        assert dt in res["sweep"]
        assert "rollout_mse" in res["sweep"][dt]["main"]
    assert math.isfinite(res["one_step_loglog_slope"])
    assert set(res["criteria"]) == {"c_map_like", "c_flow_like"}
    assert res["verdict_semantics"]
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
