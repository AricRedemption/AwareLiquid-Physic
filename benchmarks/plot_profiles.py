"""Paper main-figure generator (wave-10 N1): the 4-profile start-time panel.

Reads d1g_sweep/start_time_sweep.json (D1g) and renders the four 1-step
error profiles (prefix/all2all x n=32/64) with the training-start region
shaded — the D1g verdict figure referenced by docs/d1-start-state-mismatch.md
§7. Also emits the two-night ledger numbers as a caption sidecar.

Usage:
    python benchmarks/plot_profiles.py [--sweep JSON] [--out PNG]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sweep",
                    default="benchmarks/physics_out_v02/d1g_sweep/start_time_sweep.json")
    ap.add_argument("--out", default="docs/assets/d1g-profile-panel.png")
    args = ap.parse_args()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with open(args.sweep) as f:
        d = json.load(f)
    edges = d["results"]["prefix_n64"]["bin_edges_t"]
    centers = [(edges[i] + edges[i + 1]) / 2 for i in range(len(edges) - 1)]
    t_obs = d["args"]["t_obs"]
    k_train = d["args"]["k_train"]

    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
    panels = [("prefix_n32", "prefix, n=32"), ("all2all_n32", "all2all, n=32"),
              ("prefix_n64", "prefix, n=64"), ("all2all_n64", "all2all, n=64")]
    for ax, (key, label) in zip(axes.flat, panels):
        p = d["results"][key]["profile_mean"]
        ax.axvspan(edges[0], t_obs + k_train, color="0.85", zorder=0,
                   label="prefix training window")
        ax.plot(centers, p, marker="o", ms=3, lw=1.2, color="C0")
        ax.set_title(label, fontsize=10)
        ax.set_ylabel("1-step rollout MSE", fontsize=8)
        ax.tick_params(labelsize=8)
    axes.flat[0].legend(fontsize=7, frameon=False)
    for ax in axes[1]:
        ax.set_xlabel("rollout start time $t_0$ (steps)", fontsize=8)
    fig.suptitle("D1g: one-step error vs rollout start time "
                 "(3-seed mean; shaded = prefix training window)",
                 fontsize=11)
    fig.tight_layout()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    fig.savefig(args.out, dpi=200)
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
