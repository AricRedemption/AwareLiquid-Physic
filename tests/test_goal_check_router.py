"""goal_check 路由器仪表焊点测试(AMM-013:DEBT-FIRST/MINING-FROZEN)。"""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GOAL_CHECK = REPO / "scripts" / "goal_check"
GAUGE = REPO / "scripts" / "balance_gauge"

GOALS_TPL = """
```yaml
{queue}
```
"""

QUEUE_ONE = """goal_queue:
- id: X
    track: engineering
    goal: 某目标
    done_condition: 某条件
    check_cmd: "false"
"""

QUEUE_EMPTY = "goal_queue: []"


def make_repo(tmp, prd_rounds, ledger_rows, queue):
    (tmp / "scripts").mkdir()
    (tmp / "docs" / "loop").mkdir(parents=True)
    shutil.copy(GOAL_CHECK, tmp / "scripts" / "goal_check")
    shutil.copy(GAUGE, tmp / "scripts" / "balance_gauge")
    (tmp / "docs" / "PRD.md").write_text(prd_rounds, encoding="utf-8")
    ledger = ("## 台账\n\n| id | 目标 | 锚 | 档位 | 预计 | 状态 | 轮 | 龄 |\n"
              "|---|---|---|---|---|---|---|---|\n" + ledger_rows)
    (tmp / "docs" / "loop" / "DEBT-LEDGER.md").write_text(ledger, encoding="utf-8")
    (tmp / "docs" / "loop" / "GOALS.md").write_text(
        GOALS_TPL.format(queue=queue), encoding="utf-8")


def run(tmp):
    return subprocess.run([str(tmp / "scripts" / "goal_check")],
                          capture_output=True, text=True, cwd=tmp)


def rounds(spec):
    return "".join(f"**轮 {900+i} 记录（{kind};{tag}）**:\n-\n"
                   for i, (kind, tag) in enumerate(spec))


EVIDENCE6 = rounds([("X 判读", "算力轮")] * 6)
MINING10 = rounds([("蒸馏补池:族", "零算力")] * 10)

LEDGER_OPEN = ("| D-2 | x | y | T1 | ~15min 推理 | open | 82 | 5 |\n"
               "| D-4 | x | y | T2 | ~58min(可拆) | open | 56 | 31 |\n")
LEDGER_ALL_CLOSED = "| D-1 | x | y | T1 | 实测 | **closed(判负)** | 84 | 0 |\n"


def test_debt_first_overrides_queue(tmp_path):
    make_repo(tmp_path, EVIDENCE6, LEDGER_OPEN, QUEUE_ONE)
    r = run(tmp_path)
    assert r.returncode == 4 and "DEBT-FIRST" in r.stdout
    assert "D-2" in r.stdout and "D-4" in r.stdout


def test_mining_frozen_on_low_exp(tmp_path):
    make_repo(tmp_path, MINING10, LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    r = run(tmp_path)
    assert r.returncode == 3 and "MINING-FROZEN" in r.stdout


def test_queue_empty_normal_when_exp_healthy(tmp_path):
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    r = run(tmp_path)
    assert r.returncode == 2 and "QUEUE-EMPTY" in r.stdout


def test_not_achieved_routes_normally_after_debt_cleared(tmp_path):
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ONE)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout


def test_gauge_real_repo_debt_first():
    """真实仓库当前状态:3 笔 open 欠账 ⇒ 必须路由 DEBT-FIRST。"""
    r = subprocess.run([str(GOAL_CHECK)], capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 4 and "DEBT-FIRST" in r.stdout
    (REPO / ".loop-lock").unlink(missing_ok=True)  # 设计会话清理心跳,防阻塞下个马拉松
