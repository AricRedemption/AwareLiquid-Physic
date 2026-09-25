"""Tests for AMM-029 direction gate (round 231): verdict ledger + drift escalation."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

GATE = Path(__file__).resolve().parents[1] / "scripts" / "direction_gate"

VALID = {"round": 231, "direction": "ALIGNED",
         "evidence": "PRD §19 轮 231 判读行 RECIPE_X 数字 3.2",
         "effective_output": "探针判读一行", "next_adjust": "维持"}


def run_gate(*args):
    return subprocess.run([sys.executable, str(GATE), *args],
                          capture_output=True, text=True)


def write_ledger(tmp_path, entries):
    p = tmp_path / "gate.jsonl"
    p.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n"
                         for e in entries))
    return p


def test_missing_file_rejects(tmp_path):
    r = run_gate("--check", "--file", str(tmp_path / "none.jsonl"))
    assert r.returncode == 1 and "判单文件不存在" in r.stderr


def test_bad_json_line_rejects(tmp_path):
    p = tmp_path / "gate.jsonl"
    p.write_text("{not json}\n")
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 1 and "非合法 JSON" in r.stderr


@pytest.mark.parametrize("mutate", [
    lambda e: {k: v for k, v in e.items() if k != "evidence"},
    lambda e: {**e, "direction": "SURE"},
    lambda e: {**e, "evidence": ""},
    lambda e: {**e, "effective_output": "NONE"},
])
def test_invalid_entries_reject(tmp_path, mutate):
    p = write_ledger(tmp_path, [mutate(VALID)])
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 1


def test_valid_aligned_passes(tmp_path):
    p = write_ledger(tmp_path, [VALID])
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 0 and "GATE OK" in r.stdout


def test_uncertain_passes_with_warning(tmp_path):
    p = write_ledger(tmp_path, [{**VALID, "direction": "UNCERTAIN"}])
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 0 and "UNCERTAIN" in r.stdout


def test_single_drift_passes(tmp_path):
    p = write_ledger(tmp_path, [{**VALID, "direction": "DRIFT",
                                 "evidence": "-"}])
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 0


def test_two_consecutive_drifts_escalate(tmp_path):
    drift = lambda r: {"round": r, "direction": "DRIFT", "evidence": "-",
                       "effective_output": "状态机搬运",
                       "next_adjust": "回正轨"}
    p = write_ledger(tmp_path, [VALID, drift(232), drift(233)])
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 3 and "BLOCKED-HUMAN" in r.stdout


def test_drift_streak_broken_by_aligned(tmp_path):
    drift = {"round": 232, "direction": "DRIFT", "evidence": "-",
             "effective_output": "x", "next_adjust": "回正轨"}
    p = write_ledger(tmp_path, [drift, VALID])
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 0


def test_add_rejects_invalid_then_accepts_valid(tmp_path):
    p = tmp_path / "gate.jsonl"
    r = run_gate("--add", json.dumps({**VALID, "direction": "?"}),
                 "--file", str(p))
    assert r.returncode == 1 and not p.exists()
    r = run_gate("--add", json.dumps(VALID), "--file", str(p))
    assert r.returncode == 0 and p.exists()
    r = run_gate("--check", "--file", str(p))
    assert r.returncode == 0
