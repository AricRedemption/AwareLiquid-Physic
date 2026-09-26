"""stop_gate v7 状态机对齐回归(轮 293,AMM-034)。

v6 遗留正则 `state:(IDLE|BLOCKED-HUMAN)` 在 v7(IDLE 废除,新增 PARKED)下
漏掉 PARKED——合法自停收束会被"队列非空+锁新鲜"误拦最多 3 次。
四状态矩阵:仅 RUNNING 拦截;PARKED/BLOCKED-HUMAN/未知放行。
"""
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
STOP_GATE = REPO / "scripts" / "stop_gate.sh"

GOALS_TPL = """state: {state}            # 注释行
mode: ON                  # AMM-003 迭代总开关

```yaml
goal_queue:
- id: P1
    check_cmd: "false"
    status: pr-pending(PR#1)
```
"""


def make_repo(tmp, state: str, fresh_lock: bool = True):
    (tmp / "docs" / "loop").mkdir(parents=True)
    (tmp / "scripts").mkdir()
    shutil.copy(STOP_GATE, tmp / "scripts" / "stop_gate.sh")
    (tmp / "docs" / "loop" / "GOALS.md").write_text(
        GOALS_TPL.format(state=state), encoding="utf-8")
    if fresh_lock:
        (tmp / ".loop-lock").write_text("0")


def run(tmp):
    return subprocess.run(["bash", str(tmp / "scripts" / "stop_gate.sh")],
                          capture_output=True, text=True, cwd=tmp)


def test_running_with_fresh_lock_and_queue_requests_continue(tmp_path):
    make_repo(tmp_path, "RUNNING")
    r = run(tmp_path)
    assert r.returncode == 2 and "下一心跳" in r.stdout


def test_parked_releases(tmp_path):
    """AMM-034 回归核心:PARKED=唯一非手动自停态,v6 正则漏判会误拦。"""
    make_repo(tmp_path, "PARKED")
    r = run(tmp_path)
    assert r.returncode == 0


def test_blocked_human_releases(tmp_path):
    make_repo(tmp_path, "BLOCKED-HUMAN")
    r = run(tmp_path)
    assert r.returncode == 0


def test_stale_or_missing_lock_releases_even_running(tmp_path):
    make_repo(tmp_path, "RUNNING", fresh_lock=False)
    r = run(tmp_path)
    assert r.returncode == 0


def test_mode_off_releases_even_running(tmp_path):
    make_repo(tmp_path, "RUNNING")
    goals = tmp_path / "docs" / "loop" / "GOALS.md"
    goals.write_text(goals.read_text(encoding="utf-8").replace(
        "mode: ON", "mode: OFF"), encoding="utf-8")
    r = run(tmp_path)
    assert r.returncode == 0
