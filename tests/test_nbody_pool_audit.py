"""tests/test_nbody_pool_audit.py — NBODY-POOL-AUDIT (round 118) checks.

Jacobian exactness on a linear toy map (central differences must recover
the analytic matrix), summary/full_obs shape contract, and a tiny
end-to-end smoke (schema only, round-84 rule).
"""
import importlib.util
import json
import os
import sys

import torch

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load():
    spec = importlib.util.spec_from_file_location(
        "nbody_pool_audit",
        os.path.join(ROOT, "benchmarks", "nbody_pool_audit.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_jacobian_recovers_linear_map():
    mod = _load()
    # float64: at eps=1e-4 the float32 ulp would dominate the difference
    # quotient (round-110 lesson — limit/derivative probes need double)
    a = torch.tensor([[1.0, 2.0], [3.0, 4.0], [0.5, -1.0]],
                     dtype=torch.float64)
    mass = torch.tensor([1.0, 1.2], dtype=torch.float64)
    j = mod.jacobian(lambda m: a @ m, mass, eps=1e-4)
    assert torch.allclose(j, a, atol=1e-6), \
        "central differences must recover the analytic Jacobian"


def test_summary_shapes_and_pool_semantics():
    mod = _load()
    t, n, d = 6, 4, 2
    qs = torch.arange(t * n * d, dtype=torch.float32).reshape(t, n, d)
    vs = torch.ones(t, n, d)
    s = mod.summary(qs, vs, t_obs=6)
    f = mod.full_obs(qs, vs, t_obs=6)
    assert s.shape == (6 * 2 * d,) and f.shape == (6 * n * 2 * d,)
    # pooled channel = unweighted mean over nodes (model.py:241 semantics);
    # the first d entries are the first timestep's node-mean (x, y)
    assert torch.allclose(s[:d], qs.mean(dim=1)[0])


def test_probe_cli_smoke(tmp_path):
    mod = _load()
    sys.argv = [sys.argv[0], "--n_base", "1", "--eps", "0.05",
                "--out_dir", str(tmp_path)]
    mod.main()
    with open(os.path.join(tmp_path, "nbody_pool_audit.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    assert "retention_trace_ratio" in res
    assert len(res["retention_per_mass"]) == 4
    assert set(res["criteria"]) == {"c1_pipeline_failed",
                                    "c2_annihilation_recurred",
                                    "c3_pooled_above_full"}
    assert res["deterministic_resim"] is True
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
