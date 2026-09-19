"""GOAL-PROMPT 承重句不变式测试(AMM-019 措辞回归门禁)。

背景: v4.0/v4.1 标准化重写删掉"中途不停"一句,执行会话解读为
"一会话=一心跳",轮 93 后停止(AMM-018 修复)。本测试把 prompt 的
承重语义固化为门禁——pytest 全绿是既有提交门,任何改写 GOAL-PROMPT
的提交若丢掉承重句,在提交前即被拦截,而非在马拉松现场爆发。
新增/改写承重句时同步更新本表(每次变更须留痕于 AMENDMENTS)。
"""

import re
from pathlib import Path

PROMPT = Path(__file__).resolve().parents[1] / "docs" / "loop" / "GOAL-PROMPT.md"

# 不变式名 → 正则标记。名 = 它保护的行为,不是它的字面。
INVARIANTS = {
    "会话连续性(轮93回归:禁一会话一心跳)": r"连续执行多个心跳",
    "禁等待触发式停机": r"不得以.{0,4}等待触发.{0,8}结束",
    "合法停点含上下文过长(快照兜底)": r"上下文过长",
    "防双跑守卫": r"marathon_guard",
    "心跳路由器": r"goal_check",
    "算力四档": r"T3",
    "档位数值唯一执行点": r"唯一执行点",
    "Probe-First 大训练准入": r"Probe-First",
    "资源红线(用户绝对命令)": r"80%",
    "结论分级(T1/T2 不支撑终局)": r"终局声明",
    "算力溯源字段": r"exec_tier",
    "平衡仪表报警即行动": r"balance_gauge",
    "判读完强制消化轮": r"消化轮",
    "预注册判负标准先行": r"判负标准",
    "双门验收": r"audit_results",
    "隐藏卷复验": r"隐藏卷",
    "每轮回写 PLAYBOOK": r"PLAYBOOK",
    "机制改动走提案制": r"AMENDMENTS",
    "人决即停": r"BLOCKED-HUMAN",
    "快照续跑": r"快照",
    "方向分支纪律": r"dir/<slug>",
    "推送边界(不碰 master/origin)": r"master/origin",
    "不提交权重": r"\.pt",
    "隐藏集规约(999 退役)": r"999",
    "收口判据 S1-S4": r"S1",
    "欠账台账指针": r"DEBT-LEDGER",
    "程序计数器指针": r"GOALS\.md",
}


def prompt_text() -> str:
    src = PROMPT.read_text(encoding="utf-8")
    start = src.index("```text") + len("```text")
    end = src.index("```", start)
    return src[start:end]


def test_text_block_exists():
    assert "```text" in PROMPT.read_text(encoding="utf-8"), "GOAL-PROMPT 缺少粘贴块"


def test_all_invariants_present():
    text = prompt_text()
    missing = [name for name, pat in INVARIANTS.items() if not re.search(pat, text)]
    assert not missing, f"承重句丢失(措辞回归): {missing}"


def test_no_colloquial_rationale_in_text_block():
    """正文零 AMM 出处引用(立法史归 AMENDMENTS,v4.0 立的规矩)。"""
    assert not re.search(r"AMM-\d+", prompt_text()), "粘贴块内出现修正案编号"
