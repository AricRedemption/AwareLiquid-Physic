"""goal_check 路由器仪表焊点测试(AMM-013:DEBT-FIRST/MINING-FROZEN)。"""
import os
import re
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

QUEUE_FOLDED = """goal_queue:
- id: Y
    track: engineering
    goal: 折叠标量目标
    done_condition: 永不达成
    check_cmd: >-
      test -f nowhere.txt
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
LEDGER_CLOUD_ONLY = "| D-5 | 全量训练 | y | T3 | ~480min 云跑 | open | 80 | 40 |\n"


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


def test_queue_empty_carries_amm028_gates(tmp_path):
    """AMM-028(轮 227):QUEUE-EMPTY 输出必须携带价值出口门提示——
    决策耦合声明/配方族关闭/回灌门/3-seed/弱题录,每心跳强制可见。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    r = run(tmp_path)
    assert r.returncode == 2
    assert "[AMM-028 门]" in r.stdout
    assert "决策耦合声明" in r.stdout
    assert "配方族默认关闭" in r.stdout
    assert "3-seed" in r.stdout


def test_cloud_only_debt_does_not_block(tmp_path):
    """AMM-014:纯云档(C-debt)欠账 ⇒ 不触发 DEBT-FIRST,队列正常路由。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_CLOUD_ONLY, QUEUE_ONE)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout
    assert "DEBT-FIRST" not in r.stdout


def test_not_achieved_routes_normally_after_debt_cleared(tmp_path):
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ONE)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout


def test_folded_scalar_check_cmd_never_executed(tmp_path):
    """轮 108 回归:check_cmd 用 YAML 折叠标量 `>-` 时,单行解析器把 ">-"
    截成命令本体,shell 将 ">-" 解释为重定向——静默创建名为 "-" 的空文件
    且 exit 0 ⇒ 假 ACHIEVED 误弹(轮 62 空命令防护的变体)。必须拒绝执行
    并按未达成路由,且不得留下 "-" 文件。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_FOLDED)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout
    assert not (tmp_path / "-").exists()
    # 队列不得被误弹
    assert "goal_queue:" in (tmp_path / "docs" / "loop" / "GOALS.md").read_text()


def test_gauge_real_repo_matches_ledger_state():
    """真实仓库一致性:路由裁决必须与台账实况相符(状态驱动,不钉死)。"""
    ledger = (REPO / "docs" / "loop" / "DEBT-LEDGER.md").read_text()
    has_open_debt = bool(
        re.search(r"(?m)^\| *D-\d.*?\|\s*\*{0,2}open(?:\(|\s|\*|\|)", ledger))
    r = subprocess.run([str(GOAL_CHECK)], capture_output=True, text=True, cwd=REPO)
    if has_open_debt:
        assert r.returncode == 4 and "DEBT-FIRST" in r.stdout
    else:
        assert r.returncode != 4 and "DEBT-FIRST" not in r.stdout
    (REPO / ".loop-lock").unlink(missing_ok=True)  # 设计会话清理心跳,防阻塞下个马拉松


QUEUE_PENDING_MIXED = """goal_queue:
- id: P1
    track: frontier
  goal: 已完成待合并
    done_condition: 已判读
    check_cmd: "false"
    status: pr-pending(PR#1)
- id: A2
    track: engineering
  goal: 可行动目标
    done_condition: 某条件
    check_cmd: "false"
"""

QUEUE_PENDING_PASS = """goal_queue:
- id: P1
    track: frontier
  goal: 已完成且已合并
    done_condition: 已判读
    check_cmd: "true"
    status: pr-pending(PR#1)
- id: A2
    track: engineering
  goal: 可行动目标
    done_condition: 某条件
    check_cmd: "false"
"""

QUEUE_ALL_PENDING = """goal_queue:
- id: P1
    track: frontier
  goal: 待合并一
    done_condition: 已判读
    check_cmd: "false"
    status: pr-pending(PR#1)
- id: P2
    track: frontier
  goal: 待合并二
    done_condition: 已判读
    check_cmd: "false"
    status: pr-pending(PR#2)
"""


def test_pr_pending_skipped_to_next_actionable(tmp_path):
    """AMM-026 回归:pr-pending 条目永不迭代(防重跑探针),路由机械跳到
    下一条可行动目标——恢复由状态驱动,不再依赖 GOALS 散文注记。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_PENDING_MIXED)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout
    assert "[A2]" in r.stdout and "[P1]" not in r.stdout.split("VERDICT")[-1]


def test_pr_pending_passing_pops_normally(tmp_path):
    """合并落地(check_cmd 过)后,pr-pending 条目照常弹出且保留 status 字段。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_PENDING_PASS)
    r = run(tmp_path)
    assert r.returncode == 0 and "ACHIEVED" in r.stdout and "P1" in r.stdout
    goals = (tmp_path / "docs" / "loop" / "GOALS.md").read_text()
    assert "id: A2" in goals and "status: pr-pending(PR#1)" not in goals


def test_all_pr_pending_falls_through_to_gauge(tmp_path):
    """全部条目 pr-pending 且未合并 ⇒ 状态驱动跳过后按队列空走仪表路由
    (EXP 健康时 QUEUE-EMPTY=蒸馏/证据,而非对已完目标空转迭代)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ALL_PENDING)
    r = run(tmp_path)
    assert r.returncode == 2 and "QUEUE-EMPTY" in r.stdout
    assert r.stdout.count("[skip]") == 2
