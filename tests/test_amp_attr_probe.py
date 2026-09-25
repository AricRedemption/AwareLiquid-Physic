"""Tests for AMP-ATTR (round 244) preregistered verdict."""

import math

import torch

from benchmarks.amp_attr_probe import (
    SENTINEL,
    classify_ampattr,
    ctx_invariance,
    head_equivariance,
    median,
)


def test_ok_and_attribution_rule():
    verdict, d = classify_ampattr(
        {2: {"median": 0.1}, 4: {"median": 0.2}},
        {2: {"value": 0.5}, 4: {"value": 0.9}})
    assert verdict == "AMPATTR_OK"
    assert "head" in d["attribution_rule"]


def test_unresolvable_on_nonfinite():
    verdict, d = classify_ampattr(
        {2: {"median": float("nan")}, 4: {"median": 0.1}},
        {2: {"value": 0.5}, 4: {"value": 0.9}})
    assert verdict == "AMPATTR_UNRESOLVABLE"
    assert "ctx" in d["reason"]
    verdict, d = classify_ampattr(
        {2: {"median": 0.1}, 4: {"median": 0.1}},
        {2: {"value": float("inf")}, 4: {"value": 0.9}})
    assert verdict == "AMPATTR_UNRESOLVABLE"
    assert "head" in d["reason"]


def test_sentinel_value():
    assert SENTINEL == 3.5581917762756348


def test_median_odd_even():
    assert median([3.0, 1.0, 2.0]) == 2.0
    assert median([4.0, 1.0, 2.0, 3.0]) == 2.5


def test_ctx_invariance_perfect_and_broken():
    # an identity "inference head" returns the prefix mean: scaling the
    # prefix scales the output => diff = |s-1| (non-invariant), while
    # a constant head is exactly invariant. Both computed on toy tensors
    # through the real caliber function via a stub model.
    class ConstHead:
        def infer_context(self, q, p):
            return torch.ones(q.shape[0], 3)

    class ScaleHead:
        def infer_context(self, q, p):
            return q.mean(dim=(1, 2)).unsqueeze(1).repeat(1, 3)

    qs = torch.randn(16, 24, 1)
    ps = torch.randn(16, 24, 1)
    r_const = ctx_invariance(ConstHead(), qs, ps, 24, 2)
    assert r_const["median"] < 1e-7
    r_scale = ctx_invariance(ScaleHead(), qs, ps, 24, 2)
    assert abs(r_scale["median"] - 1.0) < 1e-6


def test_head_equivariance_linear_vs_affine():
    # linear map x -> A x is equivariant under input scaling iff
    # homogeneous; adding a constant bias breaks it. Stub rollout
    # through the real caliber function.
    class LinearRoll:
        def infer_context(self, q, p):
            return torch.ones(q.shape[0], 1)

        def rollout(self, q0, p0, ctx, k):
            qs = q0.unsqueeze(0) * (1 + 0.01 * torch.arange(
                k + 1, dtype=q0.dtype).view(-1, 1, 1))
            ps = p0.unsqueeze(0) * (1 + 0.01 * torch.arange(
                k + 1, dtype=p0.dtype).view(-1, 1, 1))
            return qs, ps

    class BiasedRoll(LinearRoll):
        def rollout(self, q0, p0, ctx, k):
            qs, ps = super().rollout(q0, p0, ctx, k)
            return qs + 1.0, ps + 1.0

    qs = torch.randn(16, 24, 1)
    ps = torch.randn(16, 24, 1)
    r_lin = head_equivariance(LinearRoll(), qs, ps, 24, 10, 2)
    assert r_lin["value"] < 1e-6
    r_bia = head_equivariance(BiasedRoll(), qs, ps, 24, 10, 2)
    assert r_bia["value"] > 0.05
