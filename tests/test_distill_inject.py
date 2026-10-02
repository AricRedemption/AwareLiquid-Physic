"""distill_inject 测试(轮 864;经验检索注入器)。"""
import importlib.machinery
import importlib.util
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
_SPEC = importlib.util.spec_from_loader(
    "distill_inject",
    importlib.machinery.SourceFileLoader("distill_inject", str(_SCRIPTS / "distill_inject")),
)
distill_inject = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(distill_inject)


def _make_root(tmp_path):
    (tmp_path / "docs/loop").mkdir(parents=True)
    (tmp_path / "docs/loop/PLAYBOOK.md").write_text(
        "- **管道吞退出码(2026-10-02 轮 807)**:pytest 管道尾吞退出码家族。\n"
        "- **watch 节流(2026-10-02 轮 832)**:守望拍事件时钟禁分钟级固定拍。\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/loop/REGISTRY.md").write_text(
        "- TSFM-KD | state=reference | gate=none | src=x | 蒸馏题录\n"
        "- SOME-CAND | state=candidate | gate=none | src=y | 候选写作轴\n",
        encoding="utf-8",
    )
    return tmp_path


def test_hit_playbook_and_registry(tmp_path):
    root = _make_root(tmp_path)
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "distill_inject"),
         "--root", str(root), "--query", "退出码 管道 蒸馏"],
        capture_output=True, text=True,
    )
    assert rc.returncode == 0
    assert "管道吞退出码" in rc.stdout and "TSFM-KD" in rc.stdout


def test_zero_hit_reports_honestly(tmp_path):
    root = _make_root(tmp_path)
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "distill_inject"),
         "--root", str(root), "--query", "完全不相关的词组"],
        capture_output=True, text=True,
    )
    assert rc.returncode == 1
    assert "零命中" in rc.stdout and "退化" in rc.stdout
    assert rc.stdout.count("| 退化]") == 2, "零命中须退化输出池尾 2 条(不限源)"


def test_top_limits_results(tmp_path):
    root = _make_root(tmp_path)
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "distill_inject"),
         "--root", str(root), "--query", "蒸馏 管道 节流", "--top", "1"],
        capture_output=True, text=True,
    )
    assert rc.returncode == 0
    assert rc.stdout.count("[PLAYBOOK") == 1, "--top=1 须只注入 1 条"


def test_empty_pool_exits_two(tmp_path):
    (tmp_path / "docs/loop").mkdir(parents=True)
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "distill_inject"),
         "--root", str(tmp_path), "--query", "任何词"],
        capture_output=True, text=True,
    )
    assert rc.returncode == 2
