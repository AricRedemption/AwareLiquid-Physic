"""ladder_scan 测试(轮 843,AMM-049 实施面)。

用临时根目录造假仓面,四级扫描各一用例+全空一用例。
"""
import importlib.util
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
_SPEC = importlib.util.spec_from_loader(
    "ladder_scan",
    importlib.machinery.SourceFileLoader("ladder_scan", str(_SCRIPTS / "ladder_scan")),
)
ladder_scan = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ladder_scan)


def _make_root(tmp_path: Path) -> Path:
    (tmp_path / "docs/loop").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "docs/loop/GOALS.md").write_text("state: RUNNING\n", encoding="utf-8")
    (tmp_path / "scripts/goal_check").write_text("#!/bin/sh\n", encoding="utf-8")
    (tmp_path / "docs/loop/DEBT-LEDGER.md").write_text("", encoding="utf-8")
    (tmp_path / "docs/loop/TOOLS.md").write_text("见 `goal_check` 条目\n", encoding="utf-8")
    (tmp_path / "tests/test_goal_check_router.py").write_text("", encoding="utf-8")
    (tmp_path / "docs/loop/PLAYBOOK.md").write_text("", encoding="utf-8")
    return tmp_path


def test_all_levels_empty_reports_zero(tmp_path):
    root = _make_root(tmp_path)
    l1 = ladder_scan.scan_l1_writing(root)
    l2 = ladder_scan.scan_l2_parking(root)
    l3 = ladder_scan.scan_l3_hardening(root)
    assert l1 == [] and l2 == [] and l3 == []


def test_l1_detects_weak_coupling_and_l2_parking(tmp_path):
    root = _make_root(tmp_path)
    (root / "docs/loop/DEBT-LEDGER.md").write_text(
        "- 弱耦合欠账: N1-FOO 写作轴(在册)\n- 已结: closed 条目\n", encoding="utf-8"
    )
    (root / "docs/scan-demo.md").write_text(
        "- 【参照】停车场条目: UQ 升级处方(解停=T2/T3 重启)\n", encoding="utf-8"
    )
    l1 = ladder_scan.scan_l1_writing(root)
    l2 = ladder_scan.scan_l2_parking(root)
    assert any("弱耦合欠账" in r for r in l1)
    assert not any("closed 条目" in r for r in l1)
    assert any("停车场条目" in r for r in l2)


def test_l3_detects_untested_and_unlisted_scripts(tmp_path):
    root = _make_root(tmp_path)
    (root / "scripts/orphan_tool").write_text("#!/bin/sh\n", encoding="utf-8")
    (root / "scripts/listed_tool").write_text("#!/bin/sh\n", encoding="utf-8")
    (root / "docs/loop/TOOLS.md").write_text("见 `listed_tool` 条目\n", encoding="utf-8")
    rows = ladder_scan.scan_l3_hardening(root)
    assert any("orphan_tool" in r and "无对应" in r for r in rows)
    assert any("orphan_tool" in r and "未入" in r for r in rows)
    assert not any("listed_tool" in r and "未入" in r for r in rows)


def test_cli_runs_and_exits_zero(tmp_path):
    root = _make_root(tmp_path)
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "ladder_scan"), "--root", str(root)],
        capture_output=True, text=True,
    )
    assert rc.returncode == 0
    assert "LADDER-SCAN" in rc.stdout
    assert "TOTAL leads" in rc.stdout


def test_cli_missing_root_exits_two(tmp_path):
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "ladder_scan"), "--root", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert rc.returncode == 2


def test_l3_exempt_marker_suppresses_untested_report(tmp_path):
    root = _make_root(tmp_path)
    (root / "scripts/waived_tool").write_text("#!/bin/sh\n", encoding="utf-8")
    (root / "docs/loop/TOOLS.md").write_text(
        "见 `goal_check` 条目\n| `waived_tool` | 一次性终跑器(无单测豁免: 终跑信号 T 唯一性) | — |\n",
        encoding="utf-8",
    )
    rows = ladder_scan.scan_l3_hardening(root)
    assert not any("waived_tool" in r and "无对应" in r for r in rows)
    assert not any("waived_tool" in r and "未入" in r for r in rows)


def test_registry_structured_l1_l2(tmp_path):
    root = _make_root(tmp_path)
    (root / "docs/loop/REGISTRY.md").write_text(
        dedent("""
        # REGISTRY
        ## 写作轴(L1)
        - A1 | state=candidate | gate=none | src=x | 真候选
        - A2 | state=gated | gate=compute | src=y | 算力门控
        - A3 | state=closed | gate=none | src=z | 已处置
        ## 停车场(L2)
        - P1 | state=gated | gate=human | src=w | 人决项
        """),
        encoding="utf-8",
    )
    l1 = ladder_scan.scan_l1_writing(root)
    l2 = ladder_scan.scan_l2_parking(root)
    assert l1[0][0] == "REGISTRY" and l2[0][0] == "REGISTRY"
    _, _, c1 = l1[0]
    assert c1 == {"candidate": 1, "gated": 1, "closed": 1}
    _, _, c2 = l2[0]
    assert c2 == {"gated": 1}


def test_l4_beat_distance(tmp_path):
    root = _make_root(tmp_path)
    (root / "docs/loop/direction-gate.jsonl").write_text(
        '{"round": 850}\n{"round": 855}\n', encoding="utf-8"
    )
    (root / "docs/loop/RSI-INDEX.md").write_text(
        "| 36 | ... | 入账(轮 846)段 |\n| 37 | ... | 入账(轮 850)段 |\n",
        encoding="utf-8",
    )
    rows, _ = ladder_scan.scan_l4_distill(root)
    assert any("节拍距 N=5" in r for r in rows)
    assert not any("N≥10" in r for r in rows)
    (root / "docs/loop/direction-gate.jsonl").write_text('{"round": 861}\n', encoding="utf-8")
    rows, _ = ladder_scan.scan_l4_distill(root)
    assert any("节拍距 N=11" in r and "强制节拍检查" in r for r in rows)
