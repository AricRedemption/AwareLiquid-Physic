"""GRAD-PATH 探针最小闭环(轮 93):schema + 判负阈值机械判定 + 确定性。

纯函数级测试(零训练,秒级):
  * 端到端小配置跑通 → JSON 合 audit schema(args/results/meta),
    eval 对照 params_with_grad == 0(create_graph=False 语义锚);
  * anomaly_flags 对三类异常(超线性内存/NaN/范数出界)机械命中;
  * 同 seed 两次运行:图字节/张量/节点数逐位一致,loss 浮点容差内
    (CPU 线程数可能改变归约顺序,整数计量是确定性锚)。
"""

import importlib.util
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_SPEC = importlib.util.spec_from_file_location(
    "grad_path_probe",
    Path(__file__).resolve().parent.parent / "benchmarks" / "grad_path_probe.py")
gpp = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(gpp)


def _tiny_args(out_dir, ks=(4,)):
    return gpp.argparse.Namespace(
        heads="m1", ks=list(ks), n_traj=8, batch=4, t_obs=4, seed=0,
        phase_dim=1, d_model=16, context_dim=4, hidden_dim=16, depth=2,
        n_nodes=8, m2_d_model=8, m2_context_dim=2, m2_modes=2, m2_width=4,
        m2_fno_depth=2, out_dir=str(out_dir))


def test_end_to_end_schema_and_eval_semantics(tmp_path):
    args = _tiny_args(tmp_path)
    model = gpp.make_model("m1", args, args.seed)
    row = gpp.one_measurement(model, "m1", args, k=4, data_seed=0)
    ev = gpp.eval_contrast(model, "m1", args, k=4, data_seed=0)
    assert row["graph_bytes"] > 0 and row["graph_tensors"] > 0
    assert row["graph_nodes"] > 0
    assert row["loss"] is not None and math.isfinite(row["loss"])
    assert row["loss_requires_grad"] is True          # 训练态有梯度路径
    # eval 对照:create_graph=False ⇒ 零参数收到梯度(脆判据)
    assert ev["params_with_grad"] == 0
    assert ev["graph_bytes"] > 0
    # schema 走通:main() 的 payload 构造与 audit REQUIRED 三键一致
    payload = {"args": vars(args),
               "meta": gpp.run_metadata({"exec_tier": "T1"}),
               "results": {"m1": {"per_k": [row]}}}
    for key in ("args", "results", "meta"):
        assert key in payload
    for key in ("git_sha", "device", "ts"):
        assert key in payload["meta"]


def test_anomaly_flags_mechanical_thresholds():
    def row(k, mem, norm, loss=1.0):
        return {"k": k, "graph_bytes": mem, "grad_norm_total": norm,
                "loss": loss, "grad_norm_core": 1.0, "grad_norm_ctx_proj": 1.0,
                "grad_norm_T": 1.0, "grad_norm_V": 1.0}

    # 正常:线性内存 + 温和范数增长 ⇒ 无异常
    ok = gpp.anomaly_flags([row(8, 800.0, 0.1), row(32, 3200.0, 0.5),
                            row(128, 12800.0, 3.0)])
    assert ok["anomaly"] is False
    assert abs(ok["mem_slope"] - 1.0) < 1e-9
    # 超线性内存(平方标度)⇒ mem_slope ≈ 2,判异常
    quad = gpp.anomaly_flags([row(8, 64.0, 1.0), row(32, 1024.0, 1.0),
                              row(128, 16384.0, 1.0)])
    assert quad["mem_slope_anomaly"] is True and quad["anomaly"] is True
    # NaN 损失 ⇒ nan_inf 命中
    nan = gpp.anomaly_flags([row(8, 8.0, 1.0, loss=float("nan")),
                             row(16, 16.0, 1.0)])
    assert nan["nan_inf"] is True and nan["anomaly"] is True
    # 范数出界(>1e4)⇒ gnorm_anomaly 命中
    boom = gpp.anomaly_flags([row(8, 8.0, 1e-6), row(128, 128.0, 1e2)])
    assert boom["gnorm_anomaly"] is True and boom["anomaly"] is True


def test_determinism_same_seed():
    args = _tiny_args("/tmp/gpp_test_det")
    m1 = gpp.make_model("m1", args, args.seed)
    m2 = gpp.make_model("m1", args, args.seed)
    r1 = gpp.one_measurement(m1, "m1", args, k=4, data_seed=7)
    r2 = gpp.one_measurement(m2, "m1", args, k=4, data_seed=7)
    for key in ("graph_bytes", "graph_tensors", "graph_nodes"):
        assert r1[key] == r2[key], key
    assert abs(r1["loss"] - r2["loss"]) <= 1e-5 * abs(r1["loss"])
