"""tests/test_loop_closer.py — 合轮收尾器测试(轮 838)。

覆盖三面:红即中止的顺序语义/全绿摘要/判单门 round 接线。
全部用假 runner 注入 rc 序列,零真实门禁执行(快)。
"""
import importlib.util
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CLOSER = ROOT / "scripts" / "loop_closer"
_spec = importlib.util.spec_from_file_location(
    "loop_closer", _CLOSER,
    loader=SourceFileLoader("loop_closer", str(_CLOSER)))
lc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lc)


def _fake_runner(rc_seq):
    """按调用次序回放 rc;记录每次 argv 供断言。"""
    calls = []
    it = iter(rc_seq)

    def run(argv):
        calls.append(argv)
        try:
            return next(it), ""
        except StopIteration:
            raise AssertionError("红门后不应继续跑后续门")
    return run, calls


def test_green_all_four_in_order(capsys):
    run, calls = _fake_runner([0, 0, 0, 0])
    rc, results = lc.run_gates(838, runner=run)
    assert rc == 0
    assert len(calls) == 4
    assert [n for n, _ in results] == [
        "direction_gate", "pytest", "audit_results", "goal_check_audit"]
    assert all(r == 0 for _, r in results)
    out = capsys.readouterr().out
    assert "CLOSER-GREEN" in out and "round=838" in out


def test_red_aborts_at_first_red_and_skips_later_gates(capsys):
    run, calls = _fake_runner([0, 1])  # 判单绿, pytest 红
    rc, results = lc.run_gates(838, runner=run)
    assert rc == 1
    assert len(calls) == 2                     # audit_results/goal_check_audit 未跑
    assert "-m" in calls[1] and "pytest" in calls[1]
    out = capsys.readouterr().out
    assert "CLOSER-ABORT" in out and "pytest" in out


def test_round_wired_into_direction_gate_args():
    gates = lc.build_gates(838)
    name, argv = gates[0]
    assert name == "direction_gate"
    assert "--check-round" in argv and "838" in argv
    assert len(gates) == 4
