"""G1 (wave-10 round 49): D2 field-loop ablation figure for the paper appendix.

Reads the two D2 artifacts (semigroup/prefix full runs) and renders the
loop x model ablation as a grouped bar chart with per-bar seed scatter —
the "training loop flips the liquid-vs-static sign" figure referenced by
docs/d1-start-state-mismatch.md Appendix A.

Usage:
    python benchmarks/plot_d2_loop.py [--out PNG]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load(path):
    with open(path) as f:
        return json.load(f)["results"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sg", default="benchmarks/physics_out_v02/d2_m2_loop/sg/field_eval.json")
    ap.add_argument("--prefix", default="benchmarks/physics_out_v02/d2_m2_loop/prefix/field_eval.json")
    ap.add_argument("--out", default="docs/assets/d2-loop-ablation.png")
    args = ap.parse_args()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sg = load(args.sg)
    pf = load(args.prefix)
    models = ("liquid_operator", "static_operator")
    labels = ("liquid", "static")
    sg_means = [sg[m]["rollout_mse"] for m in models]
    pf_means = [pf[m]["rollout_mse"] for m in models]
    sg_stds = [sg[m]["rollout_mse_std"] for m in models]
    pf_stds = [pf[m]["rollout_mse_std"] for m in models]

    fig, ax = plt.subplots(figsize=(6, 4))
    x = [0, 1]
    w = 0.35
    ax.bar([i - w / 2 for i in x], sg_means, w, label="semigroup (all2all)",
           color="C0", yerr=sg_stds, capsize=4)
    ax.bar([i + w / 2 for i in x], pf_means, w, label="prefix (v0.1)",
           color="C1", yerr=pf_stds, capsize=4)
    ax.set_xticks(x, labels)
    ax.set_ylabel("rollout MSE (3 seeds, mean; bars=range)")
    ax.set_title("M2 field task: training loop flips the\nliquid-vs-static sign (D2)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    fig.savefig(args.out, dpi=200)
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
