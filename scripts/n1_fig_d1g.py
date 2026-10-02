#!/usr/bin/env python
"""n1_fig_d1g — N1 论文主图:D1g 起点剖面四板(轮 872,N1-MAIN-FIGURE)

数据源=benchmarks/physics_out_v02/d1g_sweep/start_time_sweep.json(本地已归档
产物,meta git_sha=a9be910 device=cpu;轮 18 判定行"论文主图候选")。
数字纪律(轮 111):图中呈现的一切读数须与本 JSON 逐位一致;核对留痕入轮记录
(RSI/git)。PRD 轮 18 的 std/mean 口径(0.22-0.23/0.08-0.10)以 seed 离散口径
未能复现→本图不含该读数(诚实边界,不编造)。

用法:.venv/bin/python scripts/n1_fig_d1g.py [--json PATH] [--out PATH]
输出:docs/n1-figs/fig1_d1g_profile.png(2×2 四板归一化剖面)
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent
DEFAULT_JSON = REPO / "benchmarks" / "physics_out_v02" / "d1g_sweep" / "start_time_sweep.json"
DEFAULT_OUT = REPO / "docs" / "n1-figs" / "fig1_d1g_profile.png"
ARMS = ["prefix_n32", "prefix_n64", "all2all_n32", "all2all_n64"]


def load(path):
    d = json.loads(Path(path).read_text())
    for arm in ARMS:
        assert arm in d["results"], f"缺臂 {arm}(禁硬造,如实留缺)"
    return d


def build(d):
    """返回 (fig, checks);checks=逐位核对留痕(打印供轮记录引用)。"""
    res = d["results"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.4), sharex=True)
    checks = []
    for ax, arm in zip(axes.flat, ARMS):
        r = res[arm]
        edges = r["bin_edges_t"]
        centers = [(edges[i] + edges[i + 1]) / 2 for i in range(len(edges) - 1)]
        pm = r["profile_mean"]
        mu = statistics.mean(pm)
        rel = [v / mu for v in pm]
        seeds = [r[f"profile_seed{i}"] for i in range(3)]
        seed_rel = [[sv / statistics.mean(sp) for sv in sp] for sp in seeds]
        lo = [min(sr[b] for sr in seed_rel) for b in range(len(pm))]
        hi = [max(sr[b] for sr in seed_rel) for b in range(len(pm))]
        ax.fill_between(centers, lo, hi, alpha=0.25, color="C0", label="3-seed range")
        ax.plot(centers, rel, "o-", ms=3.5, lw=1.4, color="C0")
        dip = pm[2] / mu
        label = "prefix" if arm.startswith("prefix") else "all2all"
        n = arm.split("_")[1].lstrip("n")
        ax.set_title(f"{label}, n={n} (bin-2/mean = {dip:.3f})", fontsize=10)
        checks.append(f"{arm}: bin-2/mean={dip:.3f} min_bin={min(range(len(pm)), key=lambda i: pm[i])}")
        ax.axhline(1.0, ls=":", lw=0.8, color="gray")
        ax.set_ylabel("relative 1-step error (profile mean = 1)", fontsize=8)
        ax.tick_params(labelsize=8)
    for ax in axes[1]:
        ax.set_xlabel("training start-time bin center $t$", fontsize=9)
    axes.flat[0].legend(fontsize=7, loc="upper right")
    fig.suptitle(
        "D1g start-time sweep: prefix collapses at its sole training start (bin 2), all2all stays flat",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    return fig, checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=DEFAULT_JSON)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    d = load(args.json)
    fig, checks = build(d)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=200)
    print(f"FIG written: {args.out}")
    meta = d.get("meta", {})
    print(f"source meta: git_sha={meta.get('git_sha')} device={meta.get('device')} ts={meta.get('ts')}")
    for c in checks:
        print("check:", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
