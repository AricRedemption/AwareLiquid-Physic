"""balance_gauge 计量器测试(AMM-012 EXP 占比 + WIP)。"""
import json
import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "balance_gauge")

PRD = """
**轮 90 记录（蒸馏补池:第 25 族;零算力）**:
x

**轮 89 判读（SOMETHING 判读:探针实跑;算力轮）**:
y

**轮 88 判读（WRITING 判读:纯写作;零算力）**:
z

**D-1 判读（UQ 校准;算力轮）**:
w

**轮 87 记录（蒸馏补池:第 22 族;零算力）**:
v
"""

GOALS_Q = """
```yaml
goal_queue:
- id: A
    track: engineering
- id: B
    track: frontier
```
"""

GOALS_EMPTY = """
```yaml
goal_queue: []
```
"""


def run_with(tmp_path, prd, goals):
    p, g = tmp_path / "p.md", tmp_path / "g.md"
    p.write_text(prd), g.write_text(goals)
    r = subprocess.run([sys.executable, SCRIPT, "--prd", str(p), "--goals", str(g)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_classification_and_ratio(tmp_path):
    out = run_with(tmp_path, PRD, GOALS_Q)
    assert out["window"] == 5
    assert out["evidence"] == 2      # 轮89 算力轮 + D-1 算力轮
    assert out["mining"] == 2        # 轮90 + 轮87
    assert out["t0"] == 1            # 轮88 零算力写作
    assert abs(out["exp_ratio"] - 0.4) < 1e-9
    assert out["wip"] == 2
    assert out["alarms"] == []


def test_wip_over_limit_alarms(tmp_path):
    g = GOALS_Q.replace("- id: B", "- id: B\n- id: C\n- id: D")
    out = run_with(tmp_path, PRD, g)
    assert out["wip"] == 4
    assert any("WIP" in a for a in out["alarms"])


def test_exp_below_20_alarms(tmp_path):
    prd = PRD + "".join(
        f"**轮 {60+i} 记录（蒸馏补池:族;零算力）**:\n-\n" for i in range(8))
    out = run_with(tmp_path, prd, GOALS_EMPTY)
    assert out["mining"] == 9      # 窗口10 = 蒸馏×9(轮87+60..67) + 证据×1(D-1)
    assert out["exp_ratio"] < 0.20
    assert any("冻结蒸馏" in a for a in out["alarms"])


def test_empty_window_no_crash(tmp_path):
    out = run_with(tmp_path, "no rounds here", GOALS_EMPTY)
    assert out["window"] == 0 and out["exp_ratio"] is None and out["wip"] == 0
