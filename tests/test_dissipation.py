"""DH-DESIGN (round 74) — Rayleigh dissipation slot probes (no training).

判据 A (bitwise default-off): a default-off head must be indistinguishable
from the pre-extension conservative leapfrog — no new parameters, and its
step outputs bitwise-equal to the inlined conservative kick-drift-kick.

判据 B (dissipation actually dissipates):
  B1: exact quadratic H with R = (gamma/2) p^2 pushed through the SAME
      splitting as the head (damping force in both kicks) against the
      analytic decay H(t) = H0 * exp(-gamma t) — monotone within O(dt^2)
      and log-decay rate ~= gamma.
  B2: head-level structural monotonicity — random smooth T,V, gamma frozen
      to a constant via the PSD net's bias: H non-increasing beyond
      splitting error and substantially decayed over the rollout.

Deterministic (seeds pinned), CPU, seconds. Design rationale:
docs/dh-dissipation-design.md; preregistered criteria: PRD §19 round 73.
"""

import math

import torch
import torch.nn as nn

from awareliquid_physics.hamiltonian import HamiltonianHead


def _manual_conservative_step(head, q, p, dt, context=None):
    """The pre-extension velocity-Verlet body, inlined (bitwise reference)."""
    p_half = p - 0.5 * dt * head.dV_dq(q, context)
    q_next = q + dt * head.dT_dp(p_half)
    p_next = p_half - 0.5 * dt * head.dV_dq(q_next, context)
    return q_next, p_next


def test_a_default_off_bitwise_equivalence():
    torch.manual_seed(0)
    head = HamiltonianHead(2, hidden_dim=16, depth=2)
    assert head.rayleigh is False
    # No new parameters on the default path: every state-dict key belongs to
    # T or V (the damping net G exists only when rayleigh=True).
    assert not any(k.startswith("G.") for k in head.state_dict())

    torch.manual_seed(1)
    q0, p0 = torch.randn(3, 2), torch.randn(3, 2)
    q, p = q0.clone(), p0.clone()
    with torch.enable_grad():
        for _ in range(16):
            q, p = head.step(q, p, dt=0.05)
        qm, pm = q0, p0
        for _ in range(16):
            qm, pm = _manual_conservative_step(head, qm, pm, dt=0.05)
    assert torch.equal(q, qm) and torch.equal(p, pm)

    # Same-seed default vs explicit rayleigh=False constructions are identical
    # module-for-module (the flag adds nothing when off).
    torch.manual_seed(0)
    head2 = HamiltonianHead(2, hidden_dim=16, depth=2, rayleigh=False)
    for (k1, v1), (k2, v2) in zip(head.state_dict().items(),
                                  head2.state_dict().items()):
        assert k1 == k2 and torch.equal(v1, v2)


def test_b1_closed_form_damped_oscillator():
    # Exact quadratics: T = p^2/2, V = q^2/2, R = (gamma/2) p^2. The splitting
    # below mirrors head.step(rayleigh=True): damping force -gamma*p in both
    # kicks. Analytic reference for the continuous damped dynamics:
    # H(t) = H0 * exp(-gamma t).
    gamma, dt, steps = 0.3, 0.005, 4000
    q = torch.tensor([1.0])
    p = torch.tensor([0.0])
    h0 = float(0.5 * (q * q + p * p))
    hs = [h0]
    for _ in range(steps):
        p_half = p - 0.5 * dt * (q + gamma * p)
        q = q + dt * p_half
        p = p_half - 0.5 * dt * (q + gamma * p_half)
        hs.append(float(0.5 * (q * q + p * p)))
    h = torch.tensor(hs)

    # Monotone within O(dt^2) splitting error (no spurious growth).
    assert float((h[1:] - h[:-1]).max()) <= 1e-3 * h0
    # Log-decay rate ~= gamma (least squares on log H vs t).
    t = torch.arange(len(hs), dtype=torch.float64) * dt
    log_h = torch.log(h.to(torch.float64))
    tm = t.mean()
    slope = float(((t - tm) * (log_h - log_h.mean())).sum()
                  / ((t - tm) ** 2).sum())
    assert abs(slope + gamma) / gamma < 0.05


def _rollout_energy(head, q0, p0, steps, dt):
    with torch.enable_grad():
        qs, ps = head.rollout(q0, p0, steps=steps, dt=dt)
    return head.energy(qs, ps).detach()


def test_b2_head_damping_monotone_by_construction():
    torch.manual_seed(0)
    head = HamiltonianHead(2, hidden_dim=16, depth=2, rayleigh=True)
    assert any(k.startswith("G.") for k in head.state_dict())
    torch.manual_seed(3)
    q0 = torch.randn(4, 2) * 0.5
    p0 = torch.randn(4, 2) * 0.5

    def frozen_gamma_head(bias: float) -> HamiltonianHead:
        """Same head with G's weights zeroed and softplus(bias) as gamma."""
        h = HamiltonianHead(2, hidden_dim=16, depth=2, rayleigh=True)
        h.load_state_dict(head.state_dict())
        with torch.no_grad():
            for m in h.G:
                if isinstance(m, nn.Linear):
                    m.weight.zero_()
                    m.bias.zero_()
            h.G[-1].bias.fill_(bias)
        return h.eval()

    h_coarse = _rollout_energy(frozen_gamma_head(math.log(math.expm1(0.8))),
                               q0, p0, steps=600, dt=0.02)
    h_fine = _rollout_energy(frozen_gamma_head(math.log(math.expm1(0.8))),
                             q0, p0, steps=1200, dt=0.01)
    h_control = _rollout_energy(frozen_gamma_head(-20.0),  # softplus ~ 0
                                q0, p0, steps=600, dt=0.02)
    h0_max = float(h_coarse[0].max())

    # Monotone decay: NO stepwise energy increase at either resolution
    # (round-74 measured max step diff -1.8e-5 (dt=0.02) / -9.1e-6 (dt=0.01)).
    d_coarse = h_coarse[1:] - h_coarse[:-1]
    d_fine = h_fine[1:] - h_fine[:-1]
    assert float(d_coarse.max()) <= 0.0
    assert float(d_fine.max()) <= 0.0
    # If any positive injection ever appears (other seeds/futures), it must
    # stay below HALF the physical per-step decay gamma*H*dt — splitting
    # artifacts cannot swamp the dissipation they model.
    assert float(d_coarse.max()) <= 0.5 * 0.8 * h0_max * 0.02
    # Decay is ATTRIBUTABLE to the damping channel: per-item energy drops
    # below 0.7*H0 under gamma=0.8 (round-74 measured 0.187..0.633) while the
    # gamma~0 control conserves H0 within 1% (symplectic bounded drift).
    assert (h_coarse[-1] < 0.7 * h_coarse[0]).all()
    assert ((h_control[-1] - h_control[0]).abs()
            <= 0.01 * h_control[0]).all()
    # Endpoint consistency across dt (scheme converged, not dt luck).
    assert (h_coarse[-1] - h_fine[-1]).abs().max() <= 0.05 * h0_max
