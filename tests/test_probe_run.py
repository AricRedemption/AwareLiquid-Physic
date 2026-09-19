"""probe_run 护栏脚本测试(AMM-008 算力闸门 v3)。"""
import os
import re
import subprocess

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "probe_run")


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def thread_cap():
    return max(1, (os.cpu_count() or 1) * 6 // 10)


def test_dry_run_reports_thread_cap_and_env():
    r = run([SCRIPT, "--dry-run", "T2", "58", "--", "echo", "hi"])
    assert r.returncode == 0, r.stderr
    m = re.search(r"threads=(\d+)/(\d+)", r.stderr)
    assert m, r.stderr
    assert int(m.group(1)) == thread_cap()
    assert int(m.group(1)) <= 0.6 * int(m.group(2)) + 1e-9  # 不越过 60% 核
    assert "nice -n 15" in r.stderr


def test_t1_rejects_over_15min():
    r = run([SCRIPT, "--dry-run", "T1", "16", "--", "echo"])
    assert r.returncode == 3 and "T1" in r.stderr


def test_t2_rejects_over_60min():
    r = run([SCRIPT, "--dry-run", "T2", "61", "--", "echo"])
    assert r.returncode == 3 and "云 PR" in r.stderr


def test_t3_rejected_outright():
    r = run([SCRIPT, "--dry-run", "T3", "90", "--", "echo"])
    assert r.returncode == 3 and "云 PR" in r.stderr


def test_t1_boundary_15_and_t2_boundary_60_pass():
    for tier, est in (("T1", "15"), ("T2", "60")):
        r = run([SCRIPT, "--dry-run", tier, est, "--", "echo"])
        assert r.returncode == 0, (tier, r.stderr)


def test_exec_actually_applies_thread_env(monkeypatch):
    cap = thread_cap()
    code = (
        f"import os;print(os.environ.get('OMP_NUM_THREADS'),"
        f"os.environ.get('VECLIB_MAXIMUM_THREADS'))"
    )
    r = run([SCRIPT, "T1", "1", "--", os.environ.get("PYTHON_BIN", "python3"), "-c", code])
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == [str(cap), str(cap)]


def test_non_numeric_minutes_rejected():
    r = run([SCRIPT, "--dry-run", "T2", "abc", "--", "echo"])
    assert r.returncode == 2


def test_missing_separator_rejected():
    r = run([SCRIPT, "--dry-run", "T2", "30", "echo"])
    assert r.returncode == 2
