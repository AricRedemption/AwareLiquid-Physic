"""tests/test_escape_door_teven_probe.py — ESC-DOOR-TEVEN (round 120) checks.

Structural mechanism assertions (zero training) + an end-to-end smoke of
the probe CLI at tiny settings (smoke-grade: validates schema and shapes
only, NOT result magnitudes — round-84 product-generation rule).
float64 for the identity/exactness assertions: float32 flips the
flip-retrace error below its own ulp floor (round-110 lesson).
"""
import importlib.util
import json
import os
import sys

import torch
from torch import nn

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from awareliquid_physics.hamiltonian import (HamiltonianHead, _energy_mlp)


def _load_probe_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "escape_door_teven_probe",
        os.path.join(root, "benchmarks", "escape_door_teven_probe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _AsymmetricKinetic(nn.Module):
    """even base + a linear (odd) term — a T that is deliberately NOT even,
    used to prove the even constraint is a real restriction (non-vacuous)."""

    def __init__(self, base: nn.Module, eps: float = 0.1):
        super().__init__()
        self.base, self.eps = base, eps

    def forward(self, p: torch.Tensor) -> torch.Tensor:
        return self.base(p * p) + self.eps * p


def test_teven_gradient_is_odd_and_free_t_is_not():
    """Force-level statement of the round-66 identity (assert at the gradient
    of T, not at tiny-dt step differences): the even parameterization's
    dT/dp is exactly odd, the free MLP's is not — the restriction the R1b
    escape buys is real, not vacuous."""
    mod = _load_probe_module()
    torch.manual_seed(0)
    p = torch.tensor([[0.7], [-0.7], [1.3]], dtype=torch.float64)

    even_head = HamiltonianHead(dim=1, hidden_dim=16, depth=1).double()
    even_head.T = mod.EvenKineticMLP(_energy_mlp(1, 16, 1)).double()
    g_plus = even_head.dT_dp(p)
    g_minus = even_head.dT_dp(-p)
    assert torch.allclose(g_plus, -g_minus, atol=1e-12), \
        "even parameterization: dT/dp must be exactly odd"

    free_head = HamiltonianHead(dim=1, hidden_dim=16, depth=1).double()
    assert not torch.allclose(free_head.dT_dp(p), -free_head.dT_dp(-p),
                              atol=1e-6), \
        "free MLP(p) T is generically non-even (that is the door row's point)"

    asym_head = HamiltonianHead(dim=1, hidden_dim=16, depth=1).double()
    asym_head.T = _AsymmetricKinetic(_energy_mlp(1, 16, 1)).double()
    assert not torch.allclose(asym_head.dT_dp(p), -asym_head.dT_dp(-p),
                              atol=1e-6)


def test_teven_roundtrip_closes_and_asymmetric_does_not():
    """The round-66 identity end to end: velocity-Verlet on a T-even head
    retraces the flip protocol at the float64 floor REGARDLESS of fit
    quality (random init, zero training); adding any odd part to T breaks
    closure at a measurable magnitude."""
    mod = _load_probe_module()
    torch.manual_seed(0)
    q0 = torch.tensor([[0.4]], dtype=torch.float64)
    p0 = torch.tensor([[0.9]], dtype=torch.float64)
    dt, k = 0.1, 50

    def roundtrip(head):
        with torch.enable_grad():
            qs_fwd, ps_fwd = head.rollout(q0, p0, k, dt)
            qs_back, ps_back = head.rollout(qs_fwd[-1], -ps_fwd[-1], k, dt)
        return ((qs_back[-1] - q0) ** 2).item() \
            + ((ps_back[-1] + p0) ** 2).item()

    even_head = HamiltonianHead(dim=1, hidden_dim=16, depth=1).double()
    even_head.T = mod.EvenKineticMLP(_energy_mlp(1, 16, 1)).double()
    err_even = roundtrip(even_head)
    assert err_even < 1e-20, \
        f"T-even head must close at the float64 floor, got {err_even:.3e}"

    asym_head = HamiltonianHead(dim=1, hidden_dim=16, depth=1).double()
    asym_head.T = _AsymmetricKinetic(_energy_mlp(1, 16, 1)).double()
    err_asym = roundtrip(asym_head)
    assert err_asym > 1e-8, \
        f"an odd part in T must break flip-retrace closure, got {err_asym:.3e}"


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), both arms, roundtrip keys,
    criteria block ①-⑤, gates, exec_tier meta passthrough."""
    mod = _load_probe_module()

    sys.argv = [sys.argv[0],
                "--n_train", "16", "--n_eval", "8", "--gen_steps", "24",
                "--train_steps", "30", "--curve_every", "10",
                "--eval_k", "12",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "escape_door_teven.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    for arm in ("arm_A_free_T", "arm_B_teven"):
        assert arm in res
        for key in ("rollout_mse", "rollout_mse_stderr", "energy_drift_max",
                    "params", "train_loss", "roundtrip_k50", "roundtrip_k100",
                    "roundtrip_k200"):
            assert key in res[arm], f"{arm}.{key} missing"
    assert res["arm_A_free_T"]["params"] == res["arm_B_teven"]["params"], \
        "equal-budget contract: both arms must have identical param counts"
    assert res["roundtrip_ratio_A_over_B"] > 0
    assert set(res["criteria"]) == {"c1_necessity_weak", "c2_no_cost_violated",
                                    "c3_symplectic_lost_B",
                                    "c4_symplectic_lost_A",
                                    "c5_teven_not_at_floor"}
    assert res["gates"]["gate_at_rt_k"] == 200
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
    for arm in ("arm_A_free_T", "arm_B_teven"):
        assert len(out["loss_curves"][arm]) >= 2
