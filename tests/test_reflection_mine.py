"""tests/test_reflection_mine.py — 复盘候选挖掘器(AMM-041,轮 806)测试。
契约:四类信号源命中→候选草稿;零命中显式报 0;工具不写任何文件;
修订权留人(输出仅为草稿)。"""
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "reflection_mine.py"

JSONL_DRIFT = "\n".join(
    json.dumps({"round": r, "direction": d, "evidence": "x"}, ensure_ascii=False)
    for r, d in [(1, "ALIGNED"), (2, "DRIFT"), (3, "DRIFT"), (4, "ALIGNED"),
                 (5, "DRIFT"), (6, "DRIFT"), (7, "DRIFT")]) + "\n"

JSONL_CLEAN = "\n".join(
    json.dumps({"round": r, "direction": "ALIGNED", "evidence": "x"},
               ensure_ascii=False) for r in range(1, 5)) + "\n"

PLAYBOOK_RECURRED = """# PLAYBOOK

- **管道尾巴吞退出码(轮 22,被咬过)**:内容。
  (出处:轮 22/92/283;适用条件:x。)
- **监察结论禁止预写(轮 524,坑)**:内容。
  (出处:轮 524/558→559 修正;适用条件:y。)
- **单发坑(轮 999,坑)**:只有一轮。
  (出处:轮 999;适用条件:z。)
"""

PLAYBOOK_CLEAN = """# PLAYBOOK

- **单发坑甲(轮 1,坑)**:
  (出处:轮 1。)
- **单发坑乙(轮 2,坑)**:
  (出处:轮 2。)
"""


def run_mine(tmp, jsonl_text, playbook_text, audit_text=None):
    (tmp / "j.jsonl").write_text(jsonl_text, encoding="utf-8")
    (tmp / "p.md").write_text(playbook_text, encoding="utf-8")
    (tmp / "PRD.md").write_text("", encoding="utf-8")
    cmd = [".venv/bin/python", str(SCRIPT), "--from", "1", "--to", "2",
           "--repo", str(REPO), "--prd", str(tmp / "PRD.md"),
           "--jsonl", str(tmp / "j.jsonl"),
           "--playbook", str(tmp / "p.md")]
    if audit_text is not None:
        (tmp / "a.out").write_text(audit_text, encoding="utf-8")
        cmd += ["--audit-file", str(tmp / "a.out")]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)


def test_drift_run_detected(tmp_path):
    r = run_mine(tmp_path, JSONL_DRIFT, PLAYBOOK_CLEAN,
                 "AUDIT OK: 条目 0=0\n")
    assert r.returncode == 0
    assert "drift-run" in r.stdout and "止于轮 3" in r.stdout \
        and "止于轮 7" in r.stdout
    assert "逐源命中" in r.stdout          # 非零断言面:逐源计数显式可见


def test_pit_recurrence_detected(tmp_path):
    r = run_mine(tmp_path, JSONL_CLEAN, PLAYBOOK_RECURRED,
                 "AUDIT OK: 条目 0=0\n")
    assert "pit-recurrence" in r.stdout
    assert "管道尾巴吞退出码" in r.stdout and "监察结论禁止预写" in r.stdout
    assert "单发坑" not in r.stdout        # 单轮坑不误报


def test_audit_anomaly_and_zero_surface(tmp_path):
    r = run_mine(tmp_path, JSONL_CLEAN, PLAYBOOK_CLEAN,
                 "AUDIT FAIL:队列完整性问题(禁提交):\n  - [X] check_cmd 缺失\n")
    assert "audit-anomaly" in r.stdout and "check_cmd 缺失" in r.stdout
    # 零命中的源如实报 0(防静默失效)
    assert "'①drift': 0" in r.stdout


def test_tool_writes_nothing(tmp_path):
    """宪法条款:工具不改任何文件——只读信号源,输出草稿。"""
    run_mine(tmp_path, JSONL_CLEAN, PLAYBOOK_CLEAN, "AUDIT OK\n")  # 先造 fixtures
    import subprocess as sp
    before = {p.name: p.stat().st_mtime_ns for p in tmp_path.iterdir()}
    cmd = [".venv/bin/python", str(SCRIPT), "--from", "1", "--to", "2",
           "--repo", str(REPO), "--prd", str(tmp_path / "PRD.md"),
           "--jsonl", str(tmp_path / "j.jsonl"),
           "--playbook", str(tmp_path / "p.md"),
           "--audit-file", str(tmp_path / "a.out")]
    r = sp.run(cmd, capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0
    after = {p.name: p.stat().st_mtime_ns for p in tmp_path.iterdir()}
    assert before == after
