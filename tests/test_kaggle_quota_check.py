"""KAGGLE-QUOTA 工具测试(轮 108,AMM-023):档位映射边界 + 结构化降级路径。

全部离线:映射与降级直接调模块函数/子进程,不触网、不依赖 kaggle 包。
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "scripts" / "kaggle_quota_check.py"

spec = importlib.util.spec_from_file_location("kqc", TOOL)
kqc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kqc)


def test_tier_boundaries():
    # 边界值逐档核对(数值唯一活在工具 TIERS,测试钉的是边界行为)
    assert kqc.tier_for(None) == "NO_READ"
    assert kqc.tier_for(0.0) == "PROBE_ONLY"
    assert kqc.tier_for(1.99) == "PROBE_ONLY"
    assert kqc.tier_for(2.0) == "SHORT_RUN"
    assert kqc.tier_for(7.99) == "SHORT_RUN"
    assert kqc.tier_for(8.0) == "FULL_RUN"
    assert kqc.tier_for(19.99) == "FULL_RUN"
    assert kqc.tier_for(20.0) == "MULTI_RUN"
    assert kqc.tier_for(30.0) == "MULTI_RUN"


def test_read_quota_injected_poster():
    ok = lambda creds, url: 5.5  # noqa: E731
    assert kqc.read_quota_hours({"username": "u", "key": "k"}, poster=ok) == 5.5
    assert kqc.read_quota_hours({"username": "u", "key": "k"},
                                poster=lambda c, u: None) is None


def _run_with_creds(tmp_path: Path, creds: dict | None) -> subprocess.CompletedProcess:
    args = [sys.executable, str(TOOL), "--creds", str(tmp_path / "kaggle.json")]
    if creds is not None:
        (tmp_path / "kaggle.json").write_text(json.dumps(creds))
    return subprocess.run(args, capture_output=True, text=True)


def test_no_creds_structured_refusal(tmp_path):
    r = _run_with_creds(tmp_path, None)
    assert r.returncode == 3
    body = json.loads(r.stdout)
    assert body["status"] == "KAGGLE_NO_CREDS"
    assert body["tier"] == "NO_READ" and body["gpu_hours_remaining"] is None
    assert body["meta"]["ts"] and body["meta"]["note"]


def test_malformed_creds_is_no_creds(tmp_path):
    (tmp_path / "kaggle.json").write_text("{not json")
    r = _run_with_creds(tmp_path, None)
    assert r.returncode == 3
    assert json.loads(r.stdout)["status"] == "KAGGLE_NO_CREDS"


def test_incomplete_creds_is_no_creds(tmp_path):
    r = _run_with_creds(tmp_path, {"username": "u"})  # 缺 key
    assert r.returncode == 3
