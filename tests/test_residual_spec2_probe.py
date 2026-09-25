"""Tests for RESIDUAL-SPEC-2 (round 246) preregistered verdict."""

import math

from benchmarks.residual_spec2_probe import (
    SENTINEL_HF,
    SENTINEL_MSE,
    classify_spectra,
    median,
)


def test_redundant_when_orderings_agree():
    verdict, d = classify_spectra([1.0, 1.0, 1.0], [0.9, 0.9, 0.9],
                                  [0.1, 0.1, 0.1], [0.3, 0.3, 0.3])
    assert verdict == "SPECTRA_REDUNDANT"
    assert d["order_agreement"] == "3/3"
    assert "rejected" in d["decision"]


def test_incremental_when_orderings_disagree():
    # B wins scalar (lower MSE) but A wins composition (higher low-band)
    verdict, d = classify_spectra([1.0, 1.0, 1.0], [0.9, 0.9, 0.9],
                                  [0.3, 0.3, 0.3], [0.1, 0.1, 0.1])
    assert verdict == "SPECTRA_INCREMENTAL"
    assert d["order_agreement"] == "0/3"
    assert "AMENDMENTS" in d["decision"]


def test_majority_agreement_is_redundant():
    # agree on 2 of 3 seeds + aggregate agree => REDUNDANT
    verdict, _ = classify_spectra([1.0, 1.0, 1.0], [0.9, 0.9, 1.2],
                                  [0.1, 0.1, 0.3], [0.3, 0.3, 0.2])
    assert verdict == "SPECTRA_REDUNDANT"


def test_divergence_checked_before_ratio():
    verdict, d = classify_spectra([1.0, math.inf, 1.0], [0.9, 0.9, 0.9],
                                  [0.1, 0.1, 0.1], [0.3, 0.3, 0.3])
    assert verdict == "SPECTRA_ARM_DIVERGED"
    assert "seed 1" in d["reason"]
    verdict, d = classify_spectra([1.0, 1.0, 1.0], [0.9, 0.9, 0.9],
                                  [0.1, 0.1, 0.1], [float("nan"), 0.3, 0.3])
    assert verdict == "SPECTRA_ARM_DIVERGED"
    assert "spectral" in d["reason"]


def test_sentinels():
    assert SENTINEL_MSE == 3.5581917762756348
    assert SENTINEL_HF == 0.9324550504166047


def test_median():
    assert median([1.0, 2.0, 3.0]) == 2.0
    assert median([1.0, 2.0, 3.0, 4.0]) == 2.5
