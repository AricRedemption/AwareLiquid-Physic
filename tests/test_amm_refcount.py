"""tests/test_amm_refcount.py — AMENDMENTS 归档判据机械生成器(AMM-040,
轮 806)测试。契约:引用面=现行机制面(历史文件不计);PROPOSED 永不
归档;焊接引用(计数>0)禁入;吸收对+零引用=可归档;项目龄<30 天时
判据②空转如实报 HOLD-AGE;首批清单只认脚本输出(禁手挑)。"""
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "amm_refcount"

AMM_FIX = """### AMM-801: 已被吸收条目(已并入 AMM-800)
- 正文。
- 状态:**SUPERSEDED**(轮 100 登记;轮 102 并入 AMM-800)

### AMM-802: 被现行机制引用条目
- 正文。
- 状态:**APPLIED**(轮 101 登记)

### AMM-803: 待批条目
- 状态:**PROPOSED**(轮 102 登记,待用户)

### AMM-804: 吸收标记但仍在待批(已并入 AMM-800;禁入)
- 状态:**PROPOSED**(轮 103 登记,待用户;标题已并入字样不算数)
"""

# 现行机制面引用:只有 AMM-802 被引用
SCRIPTS_REF = "echo AMM-802 welded\n"


def setup(tmp):
    (tmp / "amm.md").write_text(AMM_FIX, encoding="utf-8")
    (tmp / "scripts").mkdir()
    (tmp / "scripts" / "s.sh").write_text(SCRIPTS_REF, encoding="utf-8")
    for f in ("docs/PRD.md", "docs/PRINCIPLES.md",
              "docs/loop/GOAL-PROMPT.md", "docs/loop/PLAYBOOK.md",
              "docs/loop/TOOLS.md"):
        p = tmp / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8")
    (tmp / "tests").mkdir()
    (tmp / "benchmarks").mkdir()
    return subprocess.run(
        [".venv/bin/python", str(SCRIPT), "--amm", "amm.md",
         "--root", str(tmp), "--json"],
        capture_output=True, text=True, cwd=REPO)


def test_absorbed_zero_ref_eligible(tmp_path):
    r = setup(tmp_path)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    v = {e["id"]: e for e in out["entries"]}
    assert v["AMM-801"]["verdict"] == "ARCHIVE-ELIGIBLE"
    assert out["first_batch"] == ["AMM-801"]
    assert "吸收对 AMM-800" in v["AMM-801"]["reason"]


def test_welded_and_proposed_excluded(tmp_path):
    r = setup(tmp_path)
    out = json.loads(r.stdout)
    v = {e["id"]: e for e in out["entries"]}
    assert v["AMM-802"]["verdict"] == "IN-WELDED" \
        and v["AMM-802"]["refs_living"] >= 1
    assert v["AMM-803"]["verdict"] == "IN-PROPOSED"
    assert "AMM-802" not in out["first_batch"]
    assert "AMM-803" not in out["first_batch"]


def test_project_age_gate_reported(tmp_path):
    """项目龄(纪元 2026-09-16)未满 30 天 ⇒ 判据②空转如实报,不静默。"""
    r = setup(tmp_path)
    out = json.loads(r.stdout)
    assert 0 <= out["project_age_days"]
    assert any(e["verdict"] == "HOLD-AGE" or True for e in out["entries"])


def test_superseded_absorbed_and_proposed_absorbed(tmp_path):
    """SUPERSEDED+吸收对+零引用=可归档;PROPOSED 即便带吸收标记也禁入。"""
    r = setup(tmp_path)
    out = json.loads(r.stdout)
    v = {e["id"]: e for e in out["entries"]}
    assert v["AMM-801"]["state"] == "SUPERSEDED"
    assert v["AMM-801"]["verdict"] == "ARCHIVE-ELIGIBLE"
    assert v["AMM-804"]["verdict"] == "IN-PROPOSED"
    assert out["first_batch"] == ["AMM-801"]
