"""marathon_guard 的最小单元测试(wave-10 轮 50):防双马拉松锁的新鲜度判定。

守卫约定:.loop-lock 位于仓库根;存在且 mtime 距今 <100 分钟 = 让位(exit 1);
不存在或已过期 = 放行(exit 0)。
轮 404 加固:BUSY 时输出死锁残留诊断(锁 mtime vs 最后本地提交),
锁龄 ≥1800s 且锁创建后零提交 ⇒ STALE-HINT;退出码语义不变。
"""
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, "scripts", "marathon_guard")
LOCK = os.path.join(ROOT, ".loop-lock")


def _run():
    return subprocess.run([GUARD], capture_output=True, text=True).returncode


def test_no_lock_allows_start():
    if os.path.exists(LOCK):
        os.remove(LOCK)
    assert _run() == 0


def test_fresh_lock_blocks_start():
    with open(LOCK, "w") as f:
        f.write(str(int(time.time())))
    assert _run() == 1
    os.remove(LOCK)
    assert _run() == 0   # 清理后放行


def test_stale_lock_allows_start():
    old = int(time.time()) - 6001          # >100 分钟
    with open(LOCK, "w") as f:
        f.write(str(old))
    os.utime(LOCK, (old, old))             # 回拨 mtime,模拟"久未刷新"
    assert _run() == 0                     # 过期锁 = 放行
    if os.path.exists(LOCK):
        os.remove(LOCK)
    if os.path.exists(LOCK):
        os.remove(LOCK)


def test_busy_prints_diagnostics_without_stale_hint(tmp_path):
    # 刚刷新的锁(<30min):诊断行必出,STALE-HINT 不出(轮 405 修正:
    # 仓外临时目录运行,不碰真仓锁,git 失败⇒commit epoch=0)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    guard = scripts / "marathon_guard"
    shutil.copy2(GUARD, guard)  # copy2 保留可执行位
    lock = tmp_path / ".loop-lock"
    now = int(time.time())
    lock.write_text(str(now))
    os.utime(lock, (now, now))
    p = subprocess.run([str(guard)], capture_output=True, text=True)
    assert p.returncode == 1
    assert "锁 mtime:" in p.stdout
    assert "最后本地提交:" in p.stdout
    assert "STALE-HINT" not in p.stdout


def test_busy_dead_lock_residue_emits_stale_hint(tmp_path):
    # 锁龄 35min(≥1800s 且 <6000s);仓外运行⇒git 取不到提交⇒
    # commit epoch 0 ≤ 锁 epoch ⇒ "锁创建后零提交"条件确定性成立
    # ⇒ STALE-HINT 必出,退出码仍 1(轮 405 修正:不依赖真仓提交时间)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    guard = scripts / "marathon_guard"
    shutil.copy2(GUARD, guard)  # copy2 保留可执行位
    lock = tmp_path / ".loop-lock"
    lock_ts = int(time.time()) - 35 * 60
    lock.write_text(str(lock_ts))
    os.utime(lock, (lock_ts, lock_ts))
    p = subprocess.run([str(guard)], capture_output=True, text=True)
    assert p.returncode == 1
    assert "STALE-HINT" in p.stdout
    assert "死锁残留" in p.stdout
