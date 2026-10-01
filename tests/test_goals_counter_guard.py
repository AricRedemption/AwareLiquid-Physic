"""tests/test_goals_counter_guard.py — GOALS 计数器详文块家规守护(轮 838)。

家规(AMM-046 大道至简,轮 109 splice 机制):GOALS current_action 只保
最近 3 轮详文,更早轮压入段史摘要(逐轮详文唯一源=git log+RSI 夜账行)。
本测试把家规机械化:详文块行首 pattern `^  轮 <数字> ` 计数 ≤3——
段史摘要头统一用 **段史摘要(轮 N-M;…)** 格式,不落本 pattern。
提交前此测试红=忘压最旧详文,先 splice 再提交。
"""
import re
from pathlib import Path

GOALS = Path(__file__).resolve().parents[1] / "docs" / "loop" / "GOALS.md"
DETAIL_BLOCK = re.compile(r"(?m)^  轮 \d+ ")


def test_detail_blocks_within_family_rule_of_three():
    src = GOALS.read_text(encoding="utf-8")
    blocks = DETAIL_BLOCK.findall(src)
    assert len(blocks) <= 3, (
        f"GOALS 计数器详文块 {len(blocks)} 个,超家规'最近 3 轮'"
        f"(AMM-046/轮 109):先把最旧一轮压入段史摘要再提交"
    )
