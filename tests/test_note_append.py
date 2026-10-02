"""note_append 测试(轮 857;粘连四犯的机械化守护)。"""
import importlib.machinery
import importlib.util
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
_SPEC = importlib.util.spec_from_loader(
    "note_append",
    importlib.machinery.SourceFileLoader("note_append", str(_SCRIPTS / "note_append")),
)
note_append = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(note_append)

GOALS_TMPL = """# GOALS.md — 程序计数器

```yaml
state: RUNNING
```
  轮 900 旧详文行。
  续行。
## 心跳语义注记(锚)

**心跳**=定义。
"""


def _run(tmp_path, text, round_=901):
    p = tmp_path / "GOALS.md"
    p.write_text(GOALS_TMPL, encoding="utf-8")
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "note_append"),
         "--file", str(p), "--round", str(round_), "--text", text],
        capture_output=True, text=True,
    )
    return rc, p.read_text(encoding="utf-8")


def test_appends_on_new_line_with_indent(tmp_path):
    rc, out = _run(tmp_path, "轮 901 新详文首行。\n  续行内容。")
    assert rc.returncode == 0
    assert "\n  轮 901 新详文首行。\n" in out, "详文必须另起行(粘连回归)"
    assert "  续行内容。" in out
    assert out.count("轮 901") == 1
    assert "\n## 心跳语义注记" in out


def test_auto_prefixes_round_and_counts(tmp_path):
    rc, out = _run(tmp_path, "新详文没有轮前缀。")
    assert rc.returncode == 0
    assert "\n  轮 901 新详文没有轮前缀。" in out
    assert "详文块计数=2" in rc.stdout


def test_family_rule_overflow_exits_one(tmp_path):
    p = tmp_path / "GOALS.md"
    p.write_text(GOALS_TMPL, encoding="utf-8")  # 初始计数=1(轮 900)

    def add(r):
        return subprocess.run(
            [sys.executable, str(_SCRIPTS / "note_append"),
             "--file", str(p), "--round", str(r), "--text", f"详文 {r}。"],
            capture_output=True, text=True,
        )

    assert add(902).returncode == 0  # 计数 2
    rc3 = add(903)                   # 计数 3=家规上限
    assert rc3.returncode == 0 and "计数=3" in rc3.stdout
    rc4 = add(904)                   # 计数 4>3⇒退出 1 提示折叠
    assert rc4.returncode == 1, "计数超家规须退出 1 提示折叠"
    assert "计数=4" in rc4.stdout


def test_missing_anchor_exits_two(tmp_path):
    p = tmp_path / "GOALS.md"
    p.write_text("无锚文件", encoding="utf-8")
    rc = subprocess.run(
        [sys.executable, str(_SCRIPTS / "note_append"),
         "--file", str(p), "--round", str(1), "--text", "x"],
        capture_output=True, text=True,
    )
    assert rc.returncode == 2
