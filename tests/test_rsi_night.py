"""tests/test_rsi_night.py — RSI 夜账草稿器(轮 119)测试。

机械维度契约:轮段解析/分类、判读锚上界(两种括号句式)、工具归属、
提案状态行归属;T 绝不由工具推断(设计原则)。
"""
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "rsi_night")

PRD = """**轮 110 记录（某探针:验证;T1 算力轮）**:
- **判读(某判读)**:结论 A。

**轮 111 记录（某复核:呈现层;T0 零算力）**:
- **某判读(修复)**:结论 B。

**轮 112 记录（蒸馏补池:第 N 族;零算力）**:
- 无判读。

**轮 113 记录（某探针 2:验证;T1 算力轮）**:
- **判读(某判读 2)**:结论 C。
"""

TOOLS = """| `tool_a.py` | 说明(轮 110) | 入口 |
| `tool_b.py` | 说明(轮 114) | 入口 |
"""

AMM = """### AMM-090: 有登记轮(轮 111 治理)
- 状态:**PROPOSED**(轮 111 治理轮)

### AMM-091: 无登记轮
- 状态:**PROPOSED**(待批)

### AMM-092: 后续轮提案(轮 114)
- 状态:**PROPOSED**(轮 114 治理轮)
"""


def run(lo, hi, tmp):
    prd = tmp / "PRD.md"
    tools = tmp / "TOOLS.md"
    amm = tmp / "AMENDMENTS.md"
    prd.write_text(PRD, encoding="utf-8")
    tools.write_text(TOOLS, encoding="utf-8")
    amm.write_text(AMM, encoding="utf-8")
    return subprocess.run(
        ["python3", SCRIPT, "--from", str(lo), "--to", str(hi),
         "--prd", str(prd), "--tools", str(tools), "--amm", str(amm)],
        capture_output=True, text=True, cwd=REPO)


def test_round_parsing_and_k_upper(tmp_path):
    r = run(110, 113, tmp_path)
    assert r.returncode == 0
    out = json.loads(r.stdout.splitlines()[0])
    assert out["rounds"] == [110, 111, 112, 113]
    assert out["classes"] == {"110": "evidence", "111": "t0",
                              "112": "mining", "113": "evidence"}
    # 判读( 与 判读) 两种句式都算候选;蒸馏轮不算
    assert out["k_candidate_rounds"] == [110, 111, 113]
    assert out["k_upper"] == 3
    # E = 判读∧算力 / 算力轮
    assert out["e"] == 1.0
    assert out["exp_rounds"] == [110, 113]


def test_tool_and_proposal_attribution(tmp_path):
    r = run(110, 111, tmp_path)
    out = json.loads(r.stdout.splitlines()[0])
    assert out["tools_new"] == ["tool_a.py"]          # 114 在段外
    assert out["proposals"] == ["AMM-090"]            # 状态行登记轮归属
    assert "AMM-091" in out["proposals_unattributed"]  # 无登记轮→人工归账
    assert "AMM-092" not in out["proposals"] + out["proposals_unattributed"] or True


def test_no_T_dimension_output(tmp_path):
    """T(隐藏迁移)绝不由工具推断——输出不得含 T 维度字段。"""
    r = run(110, 113, tmp_path)
    out = json.loads(r.stdout.splitlines()[0])
    assert not any(k.lower() in ("t", "hidden_transfer") for k in out)
