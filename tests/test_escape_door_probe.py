"""tests/test_escape_door_probe.py — ESC-DOOR-VAB (round 110) checks.

Structural mechanism assertions (zero training) + an end-to-end smoke of
the probe CLI at tiny settings (smoke-grade: validates schema and shapes
only, NOT result magnitudes — round-84 product-generation rule).
"""
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.datasets import gen_magnetic
from awareliquid_physics.hamiltonian import (HamiltonianHead,
                                             NonseparableHamiltonianHead)


def test_separable_force_is_p_independent_and_nonseparable_is_not():
    """Mechanism core, stated at the exact granularity that is true (cf.
    round-66 lesson: decompose the premises of a structural property): a
    separable H's momentum FORCE dV/dq is q-only, so the instantaneous
    dp/dt its integrator can express at fixed q is a single p-free vector
    (Verlet's composed Δp/dt converges to it as dt→0; the finite-step
    p-dependence enters only via q_next at O(dt)). The Nonseparable head's
    C coupling has EXPLICIT p dependence (dC/dp), so its dp/dt moves with
    p at O(1) — that is the Lorentz-rotation capacity the escape door buys."""
    torch.manual_seed(0)
    sep = HamiltonianHead(dim=2, hidden_dim=16, depth=1, context_dim=0)
    nonsep = NonseparableHamiltonianHead(dim=2, hidden_dim=16, depth=1,
                                         iters=2)
    # float64: at dt=1e-5 the true Δp (~1e-7) sits below float32's ulp near
    # p~0.5 (6e-8) — the limit probe would measure rounding noise, not force.
    sep, nonsep = sep.double(), nonsep.double()
    q = torch.tensor([[0.3, -0.7]], dtype=torch.float64)
    p1 = torch.tensor([[0.5, 0.5]], dtype=torch.float64)
    p2 = torch.tensor([[1.5, -0.5]], dtype=torch.float64)
    dt = 1e-5

    # separable: instantaneous dp/dt is p-free (p-dependence only O(dt) via
    # q_next; at dt=1e-5 it is below the 1e-6 atol)
    v1 = (sep.step(q, p1, dt)[1] - p1) / dt
    v2 = (sep.step(q, p2, dt)[1] - p2) / dt
    assert torch.allclose(v1, v2, atol=1e-6), \
        "separable dp/dt at fixed q must be p-free"

    # nonseparable: dp/dt carries explicit p dependence (C coupling)
    w1 = (nonsep.step(q, p1, dt)[1] - p1) / dt
    w2 = (nonsep.step(q, p2, dt)[1] - p2) / dt
    assert not torch.allclose(w1, w2, atol=1e-6), \
        "C-coupled dp/dt should move with p"


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, ratio,
    criteria block, exec_tier meta passthrough."""
    import importlib.util

    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "escape_door_probe",
        os.path.join(root, "benchmarks", "escape_door_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    sys.argv = [sys.argv[0],
                "--n_train", "16", "--n_eval", "8", "--gen_steps", "24",
                "--train_steps", "30", "--curve_every", "10",
                "--eval_k", "12", "--iters", "2",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "escape_door_probe.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    for arm in ("arm_A_separable", "arm_B_nonseparable"):
        assert arm in res
        for key in ("rollout_mse", "rollout_mse_stderr", "energy_drift_max",
                    "params", "train_loss"):
            assert key in res[arm]
    assert "ratio_A_over_B" in res and res["ratio_A_over_B"] > 0
    assert set(res["criteria"]) == {"c1_door_not_open", "c2_necessity_weak",
                                    "c3_symplectic_lost_B",
                                    "c4_symplectic_lost_A"}
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
    for arm in ("arm_A_separable", "arm_B_nonseparable"):
        assert len(out["loss_curves"][arm]) >= 2
