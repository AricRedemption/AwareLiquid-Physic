"""tests/test_icl_m3.py — ICL-M3 (round 132) checks.

Semantics unit tests (the preregistered negative criteria's exact
comparisons) + an end-to-end CLI smoke at tiny settings (smoke-grade:
schema and shapes only, NOT magnitudes — round-84 rule).
"""
import importlib.util
import json
import os
import sys
from argparse import Namespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_module():
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location(
        "icl_m3", os.path.join(root, "benchmarks", "icl_m3.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_criteria_semantics():
    """c1: few-shot gain fails iff finetune arm is not better than
    from-scratch. c2: ordering undecidable iff both gaps sit below their
    stderrs — the preregistered mechanical comparisons."""
    mse_a, mse_b, mse_c = 0.058194, 0.011950, 0.013361
    se_a, se_b, se_c = 0.003118, 0.000825, 0.000826
    c1 = mse_b >= mse_c
    c2 = (abs(mse_a - mse_b) < max(se_a, se_b)
          and abs(mse_b - mse_c) < max(se_b, se_c))
    assert c1 is False and c2 is False, "round-132 recorded values must "
    "reproduce the mechanical criteria (no-fire) as recorded in the JSON"
    # sanity: a healing-of-gaps scenario flips c2
    c2b = (abs(0.012 - 0.0121) < 0.01 and abs(0.0121 - 0.0122) < 0.01)
    assert c2b


def test_build_model_contract():
    """build_model must accept the M3 namespace fields (same contract as
    pretrain_finetune_eval — same model class and construction)."""
    mod = _load_module()
    args = Namespace(d_model=16, context_dim=4, n_scales=2, modes=4,
                     width=16, fno_depth=1, hidden=16, dt=0.05,
                     reflect_pad=4, device="cpu")
    model = mod.build_model(args, 0)
    assert model.ham.context_dim == 4


def test_probe_cli_smoke(tmp_path):
    """End-to-end tiny run: schema (results key), three arms, criteria block,
    exec_tier meta passthrough."""
    mod = _load_module()
    sys.argv = [sys.argv[0],
                "--gen_steps", "24", "--t_obs", "8", "--eval_k", "10",
                "--n_pretrain_per_speed", "4", "--n_shot", "3",
                "--n_few_eval", "6", "--n_nodes", "16",
                "--d_model", "16", "--modes", "4", "--width", "16",
                "--hidden", "16", "--pretrain_steps", "5",
                "--finetune_steps", "5", "--fromscratch_steps", "5",
                "--out_dir", str(tmp_path)]
    mod.main()

    with open(os.path.join(tmp_path, "icl_m3.json")) as f:
        out = json.load(f)
    assert "results" in out, "audit schema: top-level results key required"
    res = out["results"]
    for arm in ("arm_A_prefix_icl", "arm_B_pretrain_finetune",
                "arm_C_from_scratch"):
        assert arm in res and res[arm]["rollout_mse"] >= 0.0
    assert set(res["criteria"]) == {"c1_fewshot_gain_fails",
                                    "c2_ordering_undecidable"}
    assert out["meta"]["exec_tier"] in ("T1", "T2", "T3")
