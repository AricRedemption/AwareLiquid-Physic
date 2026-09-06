"""Integration test: run a real benchmark CLI end-to-end (tiny params) and
audit its result JSON through the provenance schema.

This is the executable form of the eval-type acceptance bar in
docs/DELIVERABLE_TYPES.md: a benchmark run is only shippable if its output
carries a valid `meta` block. time_eval is the cheapest single-model benchmark
(~2 s at these settings, forced to CPU for hermeticity).
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:  # benchmarks/ is not a package
    sys.path.insert(0, str(ROOT))

from benchmarks.audit_results import audit_one  # noqa: E402


@pytest.mark.integration
def test_time_eval_end_to_end_produces_auditable_result(tmp_path):
    out_dir = tmp_path / "integration_out"
    cmd = [
        sys.executable, "benchmarks/time_eval.py",
        "--n_train", "16", "--n_eval", "8", "--gen_steps", "60",
        "--train_steps", "10", "--eval_k", "20", "--batch", "8",
        "--hidden", "8", "--device", "cpu",
        "--out_dir", str(out_dir),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, f"benchmark failed:\n{proc.stderr[-2000:]}"

    result_path = out_dir / "time_eval.json"
    assert result_path.exists()
    doc = json.loads(result_path.read_text())

    # Provenance schema (the whole point of the observability port)
    report = audit_one(result_path)
    assert report["issues"] == []
    assert report["git_sha"] not in (None, "unknown")
    assert report["device"] == "cpu"

    # Per-trajectory stderr sits next to the mean; the mean itself is a number
    metrics = report["metrics"]
    assert isinstance(metrics["rollout_mse"], float)
    assert isinstance(metrics["rollout_mse_stderr"], float)
    assert metrics["params"] > 0
