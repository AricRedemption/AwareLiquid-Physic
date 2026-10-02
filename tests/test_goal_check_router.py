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
    assert r.returncode == 2 and "SUPPLY-EMPTY" in r.stdout


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
    goals = (REPO / "docs" / "loop" / "GOALS.md").read_text()
    # 轮 871 坑守卫:队列含行动条目(status 非 blocked-human/pr-pending)时,
    # 本用例的真仓 goal_check 会实跑其 check_cmd——达成即消费真供给(弹出)!
    # 轮 405 条款:测试禁碰真仓可变状态;本用例只验 DEBT 路由,防误弹即跳。
    queue_m = re.search(r"goal_queue:\n(.*?)```", goals, re.S)
    if queue_m:
        statuses = re.findall(r"(?m)^\s*status:\s*(.+)$", queue_m.group(1))
        if any("blocked-human" not in s and "pr-pending" not in s for s in statuses):
            pytest.skip("真仓队列含行动条目,防测试消费真供给(轮 871 坑)")
    lock = REPO / ".loop-lock"
    had_lock = lock.exists()
    lock_body = lock.read_text() if had_lock else None
    ledger = (REPO / "docs" / "loop" / "DEBT-LEDGER.md").read_text()
    has_open_debt = bool(
        re.search(r"(?m)^\| *D-\d.*?\|\s*\*{0,2}open(?:\(|\s|\*|\|)", ledger))
    r = subprocess.run([str(GOAL_CHECK)], capture_output=True, text=True, cwd=REPO)
    if has_open_debt:
        assert r.returncode == 4 and "DEBT-FIRST" in r.stdout
    else:
        assert r.returncode != 4 and "DEBT-FIRST" not in r.stdout
    # 锁状态恢复(非无条件删):测试前无锁⇒清;有锁⇒还原内容,保活会话 guard 语义
    if had_lock:
        lock.write_text(lock_body)
    else:
        lock.unlink(missing_ok=True)


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
    assert r.returncode == 2 and "SUPPLY-EMPTY" in r.stdout
    assert r.stdout.count("[skip]") == 2


# --- 轮 292 工程硬化:--audit 队列完整性审计(数数锚机械化) ---

def run_audit(tmp):
    return subprocess.run([str(tmp / "scripts" / "goal_check"), "--audit"],
                          capture_output=True, text=True, cwd=tmp)


def test_audit_healthy_queue_passes(tmp_path):
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ALL_PENDING)
    r = run_audit(tmp_path)
    assert r.returncode == 0 and "AUDIT OK" in r.stdout
    assert "尾条 P2" in r.stdout and "pr-pending 2" in r.stdout


def test_audit_flags_swallowed_check_cmd(tmp_path):
    """轮 136/138/142 吞行坑:check_cmd 整行被删 ⇒ 数数锚不平衡+缺字段,
    手工数数锚机械化后由门禁抓,不再依赖每轮手工 grep。"""
    swallowed = QUEUE_ALL_PENDING.replace('    check_cmd: "false"\n', "")
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, swallowed)
    r = run_audit(tmp_path)
    assert r.returncode == 1 and "AUDIT FAIL" in r.stdout
    assert "数数锚不平衡" in r.stdout and "check_cmd 缺失/空" in r.stdout


def test_audit_flags_folded_scalar(tmp_path):
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_FOLDED)
    r = run_audit(tmp_path)
    assert r.returncode == 1 and "折叠标量残留" in r.stdout


def test_audit_flags_duplicate_id(tmp_path):
    dup = QUEUE_ONE + QUEUE_ONE.replace("id: X", "id: X")  # 同 id 两条
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, dup)
    r = run_audit(tmp_path)
    assert r.returncode == 1 and "重复条目 id: X" in r.stdout


# --- AMM-038(轮 431):开 PR 即终态+取活义务+端到端弹出演练 ---

QUEUE_WITH_ARCHIVED = """goal_queue:
- id: DONE1
    track: engineering
    goal: 已开 PR 归档条目
    done_condition: 无
    check_cmd: "false"
    status: archived-pr(PR#99, 开PR即终态)
- id: LIVE
    track: engineering
    goal: 活跃目标
    done_condition: 某条件
    check_cmd: "false"
"""


def test_archived_pr_skipped_routes_to_live(tmp_path):
    """archived-pr 终态条目零催促跳过,路由到下一条可行动目标(AMM-038 ①)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_WITH_ARCHIVED)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout
    assert "[skip] DONE1" in r.stdout and "archived-pr" in r.stdout
    assert "对 [LIVE]" in r.stdout


def test_queue_empty_carries_supply_fault_semantics(tmp_path):
    """SUPPLY-EMPTY 必须带供给故障语义+停止权外置(AMM-044,轮 459);
    AMM-045(轮 793)后②改为登记 blocked-human+机械等待态,禁最小心跳轮询。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    r = run(tmp_path)
    assert r.returncode == 2 and "SUPPLY-EMPTY" in r.stdout
    assert "供给故障信号" in r.stdout and "禁自造簿记" in r.stdout
    assert "停止权" in r.stdout and "机械等待态" in r.stdout
    assert "禁最小心跳轮询" in r.stdout
    assert "取活义务" not in r.stdout  # AMM-044 废除


def test_audit_reports_end_to_end_rehearsal(tmp_path):
    """--audit 端到端弹出演练:check_cmd 逐条实跑并报告通过率(AMM-038 ⑤)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ALL_PENDING)
    r = run_audit(tmp_path)
    assert r.returncode == 0 and "端到端演练" in r.stdout
    assert "通过 0,未达 2" in r.stdout  # false×2=未达但机制未坏,不判死


AMM_BAD = """### AMM-901: 测试提案甲(PROPOSED)
- 动机:x
- 状态:**PROPOSED**(待用户;无登记轮号)
### AMM-902: 测试提案乙(PROPOSED)
- 动机:y
- 状态:**PROPOSED**(轮 900 登记,待用户)
"""

AMM_GOOD = """### AMM-901: 测试提案甲(PROPOSED)
- 动机:x
- 状态:**PROPOSED**(轮 900 登记,待用户)
"""

AMM_UB = """### AMM-903: 测试提案丙(PROPOSED)
- 动机:z
- 状态:**PROPOSED**(登记轮≤899(git 首入提交窗口机械锚),待用户)
"""


def test_amm_status_line_without_round_is_flagged(tmp_path):
    make_repo(tmp_path, "", LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    (tmp_path / "docs" / "loop" / "AMENDMENTS.md").write_text(AMM_BAD,
                                                         encoding="utf-8")
    out = run_audit(tmp_path).stdout
    assert "AUDIT OK" in out
    assert "[AMM 卫生]1 条提案状态行缺登记轮号(AMM-901)" in out


def test_amm_status_line_with_round_passes_silent(tmp_path):
    make_repo(tmp_path, "", LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    (tmp_path / "docs" / "loop" / "AMENDMENTS.md").write_text(AMM_GOOD,
                                                         encoding="utf-8")
    out = run_audit(tmp_path).stdout
    assert "AUDIT OK" in out
    assert "AMM 卫生" not in out


def test_amm_hygiene_absent_file_no_crash(tmp_path):
    make_repo(tmp_path, "", LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    out = run_audit(tmp_path).stdout
    assert "AUDIT OK" in out


def test_amm_ub_anchor_reported_as_known_state_not_missing(tmp_path):
    """轮 849 对齐轮 453 裁决:'登记轮≤N'上界锚=A 维不可见属设计取舍
    (点锚虚增精度 vs 上界诚实)——单列已知态报告,不计入'缺登记轮号',
    文案禁诱导补点锚(旧文案'状态行补轮 N 登记'与裁决冲突=陷阱面)。"""
    make_repo(tmp_path, "", LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    (tmp_path / "docs" / "loop" / "AMENDMENTS.md").write_text(
        AMM_BAD + AMM_UB, encoding="utf-8")
    out = run_audit(tmp_path).stdout
    assert "AUDIT OK" in out
    assert "[AMM 卫生]1 条提案状态行缺登记轮号(AMM-901)" in out
    assert "[AMM 卫生·已知态]1 条'登记轮≤N'上界锚" in out
    assert "轮 453 裁决设计取舍" in out
    assert "禁补点锚" in out


def test_audit_rehearses_archive_cmds(tmp_path):
    """轮 450 硬化:队列清空后演练并归档条 check_cmd,防空转化
    (队列 0 条时演练面=归档条;broken 命令体仍判死)。"""
    make_repo(tmp_path, "", LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    (tmp_path / "docs" / "loop" / "QUEUE-ARCHIVE.md").write_text(
        "- id: GOOD\n"
        "  status: pr-pending(PR#1)\n"
        '  check_cmd: "true"\n'
        "- id: UNMET2\n"
        "  status: pr-pending(PR#2)\n"
        "  check_cmd: \"grep -q X /nonexistent/&&\"\n",
        encoding="utf-8")
    r = run_audit(tmp_path)
    assert r.returncode == 0  # 未达=状态事实,报告不判死
    assert "(队列 0+归档 2)" in r.stdout and "通过 1,未达 1" in r.stdout


def test_audit_archive_cmds_unmet_is_report_not_fail(tmp_path):
    make_repo(tmp_path, "", LEDGER_ALL_CLOSED, QUEUE_EMPTY)
    (tmp_path / "docs" / "loop" / "QUEUE-ARCHIVE.md").write_text(
        "- id: UNMET\n"
        "  status: pr-pending(PR#1)\n"
        '  check_cmd: "false"\n',
        encoding="utf-8")
    r = run_audit(tmp_path)
    assert r.returncode == 0 and "AUDIT OK" in r.stdout
    assert "通过 0,未达 1" in r.stdout


# --- AMM-045(轮 793):blocked-human 目标族+目标达成检测驱动+机械等待态 ---

QUEUE_BLOCKED_MIXED = """goal_queue:
- id: B1
    track: governance
  goal: 用户裁定目标
    done_condition: 用户裁定落盘
    check_cmd: "false"
    status: blocked-human(用户裁定,零催促)
- id: A2
    track: engineering
  goal: 可行动目标
    done_condition: 某条件
    check_cmd: "false"
"""

QUEUE_ALL_BLOCKED = """goal_queue:
- id: B1
    track: governance
  goal: 用户裁定目标一
    done_condition: 用户裁定一落盘
    check_cmd: "false"
    status: blocked-human(用户裁定,零催促)
- id: B2
    track: compute
  goal: 算力凭证就位
    done_condition: 配额检查 status=ok
    check_cmd: "false"
    status: blocked-human(用户资源门控,零催促)
"""

QUEUE_BLOCKED_PASS = """goal_queue:
- id: B1
    track: governance
  goal: 用户已裁定目标
    done_condition: 用户裁定落盘
    check_cmd: "true"
    status: blocked-human(用户裁定,零催促)
- id: A2
    track: engineering
  goal: 可行动目标
    done_condition: 某条件
    check_cmd: "false"
"""


def test_blocked_human_skipped_routes_to_live(tmp_path):
    """AMM-045:blocked-human 条目零催促跳过迭代(check_cmd 已实跑做达成
    检测),路由到下一条可行动目标——用户门控目标永不自由迭代。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_BLOCKED_MIXED)
    r = run(tmp_path)
    assert r.returncode == 1 and "NOT-Achieved" in r.stdout
    assert "对 [A2]" in r.stdout and "[检测] B1" in r.stdout


def test_all_blocked_human_issues_rest_license(tmp_path):
    """AMM-045 核心:可行动 0+blocked-human 全部未达成 ⇒ exit 6
    ALL-BLOCKED-HUMAN(机械等待态判据),不再是 exit 2 最小心跳轮询——
    等待=状态迁移(BLOCKED-HUMAN),禁以心跳轮询当监听器。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ALL_BLOCKED)
    r = run(tmp_path)
    assert r.returncode == 6 and "ALL-BLOCKED-HUMAN" in r.stdout
    assert "机械等待态" in r.stdout and "BLOCKED-HUMAN" in r.stdout
    assert "[未达成] B1" in r.stdout and "[未达成] B2" in r.stdout
    assert "派生评估" in r.stdout and "禁以心跳轮询" in r.stdout
    # AMM-049(轮 847):exit 6 文案必含取活阶梯指引(单源链第三处,
    # 轮 847 验收抓出实施面漏改——新会话按 goal_check 输出行动不漏阶梯)。
    assert "取活阶梯" in r.stdout and "ladder_scan" in r.stdout
    # AMM-050(轮 859):exit 6 文案必含 L5 蒸馏找方向指引(五级阶梯增量引擎)。
    assert "L5 蒸馏找方向" in r.stdout


def test_all_pr_pending_without_blocked_stays_supply_empty(tmp_path):
    """边界:纯 pr-pending(无 blocked-human)不触发 exit 6——pr-pending=
    循环侧工作已完成的终态,供给问题走 SUPPLY-EMPTY 派生评估,行为不变
    (AMM-038 语义保持,exit 6 仅在存在用户门控决策目标时给出)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ALL_PENDING)
    r = run(tmp_path)
    assert r.returncode == 2 and "SUPPLY-EMPTY" in r.stdout


def test_blocked_human_passing_pops_as_supply_arrival(tmp_path):
    """AMM-045:用户门控目标达成(裁定落盘/凭证就位 ⇒ check_cmd 过)⇒
    照常弹出(exit 0)——供给到达由每轮达成检测机械发现,不依赖散文注记。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_BLOCKED_PASS)
    r = run(tmp_path)
    assert r.returncode == 0 and "ACHIEVED" in r.stdout and "B1" in r.stdout
    goals = (tmp_path / "docs" / "loop" / "GOALS.md").read_text()
    assert "id: A2" in goals and "blocked-human" not in goals


def test_audit_counts_blocked_human(tmp_path):
    """--audit 汇报 blocked-human 条数(数数锚含新目标族,提交门可见)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_ALL_BLOCKED)
    r = run_audit(tmp_path)
    assert r.returncode == 0 and "AUDIT OK" in r.stdout
    assert "blocked-human 2" in r.stdout and "尾条 B2" in r.stdout


# --- AMM-048(轮 832):doing 在途腿+WATCH 路由(exit 7,训练在途≠阻塞) ---
QUEUE_DOING_ONLY = """goal_queue:
- id: L1
    track: engineering
    goal: 长训练腿
    done_condition: 判决文件存在
    check_cmd: "false"
    status: doing(在途腿,训练在途≠阻塞)
"""

QUEUE_DOING_MIXED = """goal_queue:
- id: L1
    track: engineering
    goal: 长训练腿
    done_condition: 判决文件存在
    check_cmd: "false"
    status: doing(在途腿)
- id: T1
    track: compute
    goal: 用户门控算力
    done_condition: 凭证就位
    check_cmd: "false"
    status: blocked-human(用户门控,零催促)
"""

QUEUE_DOING_LIVE_FIRST = """goal_queue:
- id: A1
    track: engineering
    goal: 可行动目标
    done_condition: 某条件
    check_cmd: "false"
- id: L1
    track: engineering
    goal: 长训练腿
    done_condition: 判决文件存在
    check_cmd: "false"
    status: doing(在途腿)
"""

QUEUE_DOING_ACHIEVED = """goal_queue:
- id: L1
    track: engineering
    goal: 长训练腿
    done_condition: 判决文件存在
    check_cmd: "true"
    status: doing(在途腿)
"""


def test_doing_routes_watch_exit7(tmp_path):
    """AMM-048:doing 条目 check_cmd 未达成⇒WATCH 路由(exit 7,训练在途
    ≠阻塞)——不触发迭代一步也不触发 exit 6 全阻。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_DOING_ONLY)
    r = run(tmp_path)
    assert r.returncode == 7 and "VERDICT: WATCH" in r.stdout
    assert "[守望] L1" in r.stdout and "在途跟进拍协议" in r.stdout


def test_doing_with_blocked_still_watch_not_exit6(tmp_path):
    """AMM-048:doing 与 blocked-human 并存⇒exit 7(腿在途≠全阻,
    机械等待的"全阻"前提不成立)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_DOING_MIXED)
    r = run(tmp_path)
    assert r.returncode == 7 and "VERDICT: WATCH" in r.stdout
    assert "[检测] T1" in r.stdout


def test_doing_does_not_shadow_live_entry(tmp_path):
    """AMM-048:可行动条目在前照常 exit 1 迭代——守望不遮蔽活供给。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_DOING_LIVE_FIRST)
    r = run(tmp_path)
    assert r.returncode == 1 and "对 [A1]" in r.stdout


def test_doing_achieved_pops(tmp_path):
    """AMM-048:doing 条目达成(rc=0)⇒照常弹出(腿完成=供给到达机械检测面)。"""
    make_repo(tmp_path, EVIDENCE6, LEDGER_ALL_CLOSED, QUEUE_DOING_ACHIEVED)
    r = run(tmp_path)
    assert r.returncode == 0 and "ACHIEVED" in r.stdout
