"""n1_fig_d1g 测试(轮 873 硬化拍;tmp_path 假 JSON 仓外运行=轮 405 条款,不碰真仓)"""
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "n1_fig_d1g",
    Path(__file__).resolve().parent.parent / "scripts" / "n1_fig_d1g.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

ARMS = mod.ARMS


def _fake_json(path, arms=ARMS):
    """最小 4 臂 JSON:profile 剖面形状自控(prefix 臂 bin2 深凹陷)。"""
    import json

    edges = list(range(0, 161, 10))
    results = {}
    for arm in arms:
        base = [1.0] * 16
        if arm.startswith("prefix"):
            base[2] = 0.4
        results[arm] = {
            "bin_edges_t": edges,
            "profile_mean": base,
            **{f"profile_seed{i}": list(base) for i in range(3)},
        }
    doc = {"args": {}, "meta": {"git_sha": "test", "device": "cpu"}, "results": results}
    path.write_text(json.dumps(doc))
    return path


def test_load_missing_arm_asserts(tmp_path):
    p = _fake_json(tmp_path / "d.json", arms=ARMS[:2])
    with pytest.raises(AssertionError, match="缺臂"):
        mod.load(p)


def test_build_checks_bin2_ratio(tmp_path):
    d = mod.load(_fake_json(tmp_path / "d.json"))
    fig, checks = mod.build(d)
    assert len(checks) == 4
    # prefix 臂 bin2=0.4,其余 bin=1 ⇒ bin-2/mean = 0.4/0.9625 ≈ 0.4156
    pre = [c for c in checks if c.startswith("prefix_n32")]
    assert pre and "0.416" in pre[0]
    # all2all 全 1 ⇒ bin-2/mean = 1.000
    a2a = [c for c in checks if c.startswith("all2all_n32")]
    assert a2a and "1.000" in a2a[0]
    import matplotlib

    matplotlib.pyplot.close(fig)


def test_build_uniform_arm_flat(tmp_path):
    d = mod.load(_fake_json(tmp_path / "d.json"))
    _, checks = mod.build(d)
    for c in checks:
        assert "min_bin=" in c
