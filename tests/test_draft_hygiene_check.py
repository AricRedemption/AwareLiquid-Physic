"""draft_hygiene_check 测试(轮 871;tmp_path 仓外运行=轮 405 坑条款)"""
import importlib.util
import sys
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "draft_hygiene_check",
    Path(__file__).resolve().parent.parent / "scripts" / "draft_hygiene_check.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


GOVERNANCE = "# N1 Paper Draft v0(轮 107 起草)\n> 治理注记(投稿前删除)\n\n## Abstract\n"


def _run(tmp_path, text):
    p = tmp_path / "draft.md"
    p.write_text(text, encoding="utf-8")
    return mod.check(text)


def test_clean_draft_passes(tmp_path):
    v = _run(tmp_path, GOVERNANCE + "All English body text with v0-TODO: title alternatives; venue TBD.\n")
    assert v == []


def test_body_cjk_flagged(tmp_path):
    v = _run(tmp_path, GOVERNANCE + "English line with 中文残留 inside body.\n")
    assert len(v) == 1 and v[0][1] == "cjk"


def test_governance_block_exempt(tmp_path):
    v = _run(tmp_path, "# 草稿标题(中文)\n> 注记(投稿前删除)\n\n## Abstract\nBody only.\n")
    assert v == []


def test_stale_todo_flagged(tmp_path):
    v = _run(tmp_path, GOVERNANCE + "retained. [v0-TODO: pre-register the 998 terminal run.]\n")
    assert len(v) == 1 and v[0][1] == "stale-todo"


def test_stale_todo_reference_flagged(tmp_path):
    v = _run(tmp_path, GOVERNANCE + "The outstanding [v0-TODO] is narrowed accordingly: x.\n")
    assert len(v) == 1 and v[0][1] == "stale-todo"


def test_meta_mention_not_flagged(tmp_path):
    v = _run(tmp_path, GOVERNANCE + "Verified by checker (stale v0-TODO markers = 0).\n")
    assert v == []


def test_allowed_todo_survives(tmp_path):
    v = _run(tmp_path, GOVERNANCE + "[v0-TODO: title alternatives; venue TBD (human)]\n")
    assert v == []
