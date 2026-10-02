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
