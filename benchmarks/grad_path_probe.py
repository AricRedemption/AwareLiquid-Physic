"""grad_path_probe.py — GRAD-PATH 零训练梯度路径冒烟探针(轮 93)。

审计 train_semigroup 展开式 BPTT(create_graph=self.training 路线)的
图内存与梯度范数随滚出视距 k 的标度。合成张量、固定 seed、**零训练**
(无优化器、无参数更新),每个 k 一次前向+一次反向。

每个 (head, k) 记录:
  * graph_bytes / graph_tensors — 滚出前向期间 autograd 为 backward 保存的
    张量总字节/个数(saved_tensors_hooks pack 钩子,图驻留内存的精确量,
    CPU 上比 RSS 峰值干净);eval 模式(create_graph=False)对照记录同指标,
    验证 eval 侧场求值为图外常数。
  * graph_nodes — 从 loss.grad_fn 可达的唯一 autograd 节点数
    (create_graph=True 的内层 grad 展平进外层图,节点数即图规模)。
  * fwd_s / bwd_s — 前向/反向墙钟。
  * grad_norm_{core,ctx_proj,T,V} — 各参数组 L2 范数;
    grad_norm_ctx — ||dL/dctx||(ctx.retain_grad,E4a 弱假说的审计入口,
    只记录不下结论);loss — rollout MSE 值。

判负标准①的操作化(先于运行钉进代码,PRD §19 轮 87 预注册的机制化):
任一 (a) NaN/Inf;(b) 内存标度指数 mem_slope 出 [0.7, 1.3](展开式 BPTT
必须近线性,超线性=图构建异常);(c) 梯度范数比 ||g||(k_max)/||g||(k_min)
< 1e-4(消失)或 > 1e4(爆炸)——任一命中即 anomaly=true,如实入档并
登记风险项。

用法::

    .venv/bin/python benchmarks/grad_path_probe.py \
        --heads m1,m2 --ks 8 32 128 --out_dir grad_path_probe
    # 结果写 benchmarks/<out_dir>/grad_path_probe.json;数字抄 PRD §19。
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import torch

from awareliquid_physics.model import (LiquidHamiltonianModel,
                                       LiquidOperatorHamiltonianModel)
from awareliquid_physics.observability import run_metadata
from awareliquid_physics.train import rollout_mse_loss

# 判负标准①的操作化阈值(轮 93 预声明,运行前钉死;改动须新轮预注册)
MEM_SLOPE_OK = (0.7, 1.3)          # 图内存 ~ k 线性的对数斜率容差
GNORM_RATIO_BOUNDS = (1e-4, 1e4)   # 消失/爆炸检查,作用于两端 k 的总范数比


class _GraphMeter:
    """pack 钩子累计 backward 保存的张量字节/个数。

    语义(如实注记):pack 在每次 save-for-backward 时触发——训练态
    (create_graph=True)这些张量驻留到 loss.backward() 才释放,故总量
    ≈ 展开图驻留内存;eval 态(内层 create_graph=False)保存量只服务
    内层 grad 调用自身的 backward,每次调用后即释放,故 eval 侧计量是
    瞬时保存**体积**而非驻留量。同一 save 事件被两个节点共享存储时会
    重复计字节——对标度(随 k 的斜率)无影响,绝对值有上界性偏差,
    引用绝对值时按"pack 事件总量"口径。"""

    def __init__(self):
        self.bytes = 0
        self.count = 0

    def pack(self, t):
        if isinstance(t, torch.Tensor):
            self.bytes += t.numel() * t.element_size()
            self.count += 1
        return t

    def unpack(self, t):
        return t


def count_graph_nodes(loss: torch.Tensor) -> int:
    """从 loss.grad_fn 可达的唯一 autograd 节点数(内层 create_graph=True
    的 backward 算子已展平在外层图中,一并计入)。"""
    seen: set[int] = set()
    stack = [loss.grad_fn]
    while stack:
        fn = stack.pop()
        if fn is None or id(fn) in seen:
            continue
        seen.add(id(fn))
        for nxt, _ in fn.next_functions:
            stack.append(nxt)
    return len(seen)


def _param_group_norms(model: torch.nn.Module) -> dict:
    groups = {"core": model.core, "ctx_proj": model.context_proj}
    if hasattr(model.ham, "T"):
        groups["T"] = model.ham.T
    if hasattr(model.ham, "V"):
        groups["V"] = model.ham.V
    out = {}
    for name, mod in groups.items():
        sq = 0.0
        for p in mod.parameters():
            if p.grad is not None:
                sq += float(p.grad.pow(2).sum())
        out[name] = math.sqrt(sq)
    return out


def _finite(x: float) -> float | None:
    return x if math.isfinite(x) else None


def make_model(head: str, args, seed: int) -> torch.nn.Module:
    torch.manual_seed(seed)
    if head == "m1":
        return LiquidHamiltonianModel(
            phase_dim=args.phase_dim, d_model=args.d_model,
            context_dim=args.context_dim, hidden_dim=args.hidden_dim,
            depth=args.depth)
    if head == "m2":
        return LiquidOperatorHamiltonianModel(
            phase_dim=args.phase_dim, d_model=args.m2_d_model,
            context_dim=args.m2_context_dim, modes=args.m2_modes,
            width=args.m2_width, fno_depth=args.m2_fno_depth,
            hidden_dim=args.hidden_dim, t_depth=args.depth)
    raise ValueError(f"unknown head {head!r} (m1|m2)")


def synthetic_batch(head: str, args, n_traj: int, S: int, seed: int):
    g = torch.Generator().manual_seed(seed)
    shape = (n_traj, S, args.phase_dim) if head == "m1" else \
        (n_traj, S, args.n_nodes, args.phase_dim)
    return torch.randn(*shape, generator=g), torch.randn(*shape, generator=g)


def one_measurement(model: torch.nn.Module, head: str, args, k: int,
                    data_seed: int) -> dict:
    """零训练一次前向+反向:合成批、固定 seed,训练态展开滚出。
    返回该 (head, k) 的全部指标(不更新任何参数)。"""
    torch.manual_seed(args.seed)          # 模型无关的批独立性由 data_seed 控制
    n_traj = args.n_traj
    S = args.t_obs + k + 2                # t0 ∈ [t_obs, S-k):合法起点充足
    qs, ps = synthetic_batch(head, args, n_traj, S, data_seed)
    g = torch.Generator().manual_seed(args.seed)
    bi = torch.randint(0, n_traj, (args.batch,), generator=g)
    t0 = torch.randint(args.t_obs, S - k, (args.batch,), generator=g)

    model.train()
    with torch.enable_grad():             # 场是 autograd 梯度,no_grad 会杀滚出
        q_obs, p_obs = qs[bi, :args.t_obs], ps[bi, :args.t_obs]
        ctx = model.infer_context(q_obs, p_obs)
        ctx.retain_grad()                 # E4a 入口:||dL/dctx|| 只记录不判读
        q0, p0 = qs[bi, t0], ps[bi, t0]

        meter = _GraphMeter()
        t_fwd = time.perf_counter()
        with torch.autograd.graph.saved_tensors_hooks(meter.pack, meter.unpack):
            qs_pred, ps_pred = model.rollout(q0, p0, ctx, k)
        t_fwd = time.perf_counter() - t_fwd

        q_true = qs[bi[:, None], t0[:, None] + torch.arange(k + 1)]
        p_true = ps[bi[:, None], t0[:, None] + torch.arange(k + 1)]
        q_true = q_true.permute(1, 0, *range(2, q_true.dim()))
        p_true = p_true.permute(1, 0, *range(2, p_true.dim()))
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        nodes = count_graph_nodes(loss)

        t_bwd = time.perf_counter()
        loss.backward()
        t_bwd = time.perf_counter() - t_bwd

        norms = _param_group_norms(model)
        ctx_grad = ctx.grad
        row = {
            "k": k,
            "graph_bytes": meter.bytes,
            "graph_tensors": meter.count,
            "graph_nodes": nodes,
            "fwd_s": t_fwd,
            "bwd_s": t_bwd,
            "loss": _finite(float(loss.detach())),
            "loss_requires_grad": bool(loss.requires_grad),
            "grad_norm_ctx": _finite(float(ctx_grad.norm())) if ctx_grad is not None else None,
        }
        row.update({f"grad_norm_{n}": _finite(v) for n, v in norms.items()})
        row["grad_norm_total"] = _finite(
            math.sqrt(sum(v * v for v in norms.values() if math.isfinite(v))
                      + (float(ctx_grad.norm()) ** 2
                         if ctx_grad is not None and math.isfinite(float(ctx_grad.norm()))
                         else 0.0)))
    model.zero_grad(set_to_none=True)
    return row


def eval_contrast(model: torch.nn.Module, head: str, args, k: int,
                  data_seed: int) -> dict:
    """eval 模式对照:create_graph=False ⇒ 内层场求值应为图外常数,
    滚出链不挂外向图(saved bytes 应远小于训练态,链 requires_grad=False)。"""
    S = args.t_obs + k + 2
    qs, ps = synthetic_batch(head, args, args.n_traj, S, data_seed)
    g = torch.Generator().manual_seed(args.seed)
    bi = torch.randint(0, args.n_traj, (args.batch,), generator=g)
    t0 = torch.randint(args.t_obs, S - k, (args.batch,), generator=g)
    model.eval()
    meter = _GraphMeter()
    with torch.enable_grad():             # 内层 autograd.grad 需要 grad 模式
        ctx = model.infer_context(qs[bi, :args.t_obs], ps[bi, :args.t_obs])
        with torch.autograd.graph.saved_tensors_hooks(meter.pack, meter.unpack):
            qs_pred, ps_pred = model.rollout(qs[bi, t0], ps[bi, t0], ctx, k)
        q_true = qs[bi[:, None], t0[:, None] + torch.arange(k + 1)]
        p_true = ps[bi[:, None], t0[:, None] + torch.arange(k + 1)]
        q_true = q_true.permute(1, 0, *range(2, q_true.dim()))
        p_true = p_true.permute(1, 0, *range(2, p_true.dim()))
        loss = rollout_mse_loss(qs_pred, ps_pred, q_true, p_true)
        loss.backward()
    # create_graph=False 的脆判据:backward 后**没有任何参数**收到梯度
    # (场是图外常数;梯度只会流入被 _grad 原地 requires_grad_(True) 改标
    # 的 q0/p0 数据叶子)。loss.requires_grad 在 eval 也为 True——叶子
    # 改标所致,故它不是判据,params_with_grad 才是(eval 应为 0)。
    n_pg = sum(1 for p in model.parameters() if p.grad is not None
               and float(p.grad.abs().sum()) > 0)
    model.zero_grad(set_to_none=True)
    return {"graph_bytes": meter.bytes, "graph_tensors": meter.count,
            "params_with_grad": int(n_pg),
            "loss_requires_grad": bool(loss.requires_grad)}


def _loglog_slope(xs, ys) -> float:
    lxs = [math.log(x) for x in xs]
    lys = [math.log(y) for y in ys]
    n = len(xs)
    mx, my = sum(lxs) / n, sum(lys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(lxs, lys))
    den = sum((x - mx) ** 2 for x in lxs)
    return num / den


def anomaly_flags(per_k: list[dict]) -> dict:
    """判负标准①的机械判定(阈值 MEM_SLOPE_OK / GNORM_RATIO_BOUNDS)。"""
    ks = [r["k"] for r in per_k]
    mems = [r["graph_bytes"] for r in per_k]
    norms = [r.get("grad_norm_total") for r in per_k]
    nan_inf = any(
        r["loss"] is None or not math.isfinite(r["loss"])
        or any(r.get(f"grad_norm_{g}") is None
               for g in ("core", "ctx_proj", "T", "V"))
        for r in per_k)
    slope = _loglog_slope(ks, mems) if all(m > 0 for m in mems) else float("nan")
    mem_anom = not (MEM_SLOPE_OK[0] <= slope <= MEM_SLOPE_OK[1])
    ratio = None
    gnorm_anom = False
    if all(v is not None for v in norms) and norms[0] > 0:
        ratio = norms[-1] / norms[0]
        gnorm_anom = not (GNORM_RATIO_BOUNDS[0] <= ratio <= GNORM_RATIO_BOUNDS[1])
    return {"nan_inf": bool(nan_inf), "mem_slope": _finite(slope),
            "mem_slope_anomaly": bool(mem_anom),
            "gnorm_ratio_kmax_kmin": _finite(ratio) if ratio is not None else None,
            "gnorm_anomaly": bool(gnorm_anom),
            "anomaly": bool(nan_inf or mem_anom or gnorm_anom)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--heads", default="m1,m2")
    ap.add_argument("--ks", type=int, nargs="+", default=[8, 32, 128])
    ap.add_argument("--n_traj", type=int, default=64)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--t_obs", type=int, default=16)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--phase_dim", type=int, default=1)
    ap.add_argument("--d_model", type=int, default=64)
    ap.add_argument("--context_dim", type=int, default=16)
    ap.add_argument("--hidden_dim", type=int, default=64)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--n_nodes", type=int, default=16)
    ap.add_argument("--m2_d_model", type=int, default=32)
    ap.add_argument("--m2_context_dim", type=int, default=4)
    ap.add_argument("--m2_modes", type=int, default=6)
    ap.add_argument("--m2_width", type=int, default=16)
    ap.add_argument("--m2_fno_depth", type=int, default=4)
    ap.add_argument("--out_dir", default="grad_path_probe")
    args = ap.parse_args()

    out_dir = Path(__file__).resolve().parent / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    results: dict = {}
    for head in [h.strip() for h in args.heads.split(",") if h.strip()]:
        model = make_model(head, args, args.seed)
        rows = [one_measurement(model, head, args, k,
                                data_seed=args.seed * 1000 + ki)
                for ki, k in enumerate(args.ks)]
        flags = anomaly_flags(rows)
        # eval 对照只跑最小/最大 k 两档(对照语义与 k 无关)
        ev = {str(k): eval_contrast(model, head, args, k,
                                    data_seed=args.seed * 1000 + i)
              for i, k in enumerate((args.ks[0], args.ks[-1]))}
        results[head] = {"per_k": rows, "negative_criteria": flags,
                         "eval_contrast": ev}
        del model

    payload = {
        "args": vars(args),
        "meta": run_metadata({"exec_tier": "T1", "probe": "grad_path_probe",
                              "zero_training": True}),
        "results": results,
    }
    out = out_dir / "grad_path_probe.json"
    out.write_text(json.dumps(payload, indent=2))
    heads_summary = {h: {"anomaly": results[h]["negative_criteria"]["anomaly"],
                         "mem_slope": results[h]["negative_criteria"]["mem_slope"],
                         "gnorm_ratio": results[h]["negative_criteria"]["gnorm_ratio_kmax_kmin"]}
                     for h in results}
    print(json.dumps({"out": str(out), "summary": heads_summary}, indent=2))


if __name__ == "__main__":
    main()
