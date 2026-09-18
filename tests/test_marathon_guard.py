"""marathon_guard 的最小单元测试(wave-10 轮 50):防双马拉松锁的新鲜度判定。

守卫约定:.loop-lock 位于仓库根;存在且 mtime 距今 <100 分钟 = 让位(exit 1);
不存在或已过期 = 放行(exit 0)。
"""
import os
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
    assert _run() == 0                     # 过期锁 = 放行
    if os.path.exists(LOCK):
        os.remove(LOCK)
