"""Tests for RECIPE-HEAD (round 279) preregistered verdict."""

import math

import torch

from benchmarks.recipe_head_probe import (
    A0_ANCHOR,
    A1_ANCHOR,
    B0_ANCHOR,
    RECIPE,
    classify_compose,
)


def test_synergic():
    verdict, d = classify_compose([3.5, 3.4, 3.6], [3.3, 3.2, 3.4],
                                  [2.0, 1.6, 2.2], [1.5, 1.4, 1.6])
    assert verdict == "COMPOSE_SYNERGIC"
    assert "joint default" in d["decision"]


def test_absorbed():
    verdict, d = classify_compose([3.5, 3.4, 3.6], [2.0, 1.6, 2.2],
                                  [2.0, 1.6, 2.2], [1.95, 1.95, 2.0])
    assert verdict == "COMPOSE_ABSORBED"
    assert "either-or" in d["decision"]


def test_conflict():
    verdict, d = classify_compose([3.5, 3.4, 3.6], [2.0, 1.6, 2.2],
                                  [2.0, 1.6, 2.2], [2.6, 2.7, 2.65])
    assert verdict == "COMPOSE_CONFLICT"
    assert "recipe + default head" in d["decision"]


def test_divergence_checked_first():
    verdict, d = classify_compose([3.5, math.inf, 3.6], [3.3, 3.2, 3.4],
                                  [2.0, 1.6, 2.2], [1.5, 1.4, 1.6])
    assert verdict == "HOM_ARM_DIVERGED"
    assert "cell A0" in d["reason"]


def test_declared_anchors_and_recipe():
    assert A0_ANCHOR == 3.5581917762756348
    assert A1_ANCHOR == 3.3909592628479004
    assert B0_ANCHOR == 2.0023648738861084
    assert RECIPE == {"depth": 4, "lr_decay": 0.999,
                      "weight_decay": 1e-4, "warmup_steps": 200,
                      "k_train": 4}


def test_candidate_head_constructs_depth4():
    from benchmarks.v_hom_stab_probe import HomVStabHead
    head = HomVStabHead(1, hidden_dim=8, depth=4, context_dim=2)
    q = torch.randn(4, 1, requires_grad=True)
    ctx = torch.randn(4, 2)
    e = head.energy(q, p=torch.randn(4, 1), context=ctx)
    e.sum().backward()
    assert q.grad is not None
