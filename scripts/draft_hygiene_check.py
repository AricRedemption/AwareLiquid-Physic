#!/usr/bin/env python
"""draft_hygiene_check — N1 草稿终稿卫生机械检查(轮 871,N1-DRAFT-CLEANUP check_cmd)

规则(等效清点单机械化,AMM-021 简化等效铁律的检查面):
  1. 正文级中文残留:治理面(文件头至 `## Abstract` 前)之外的行含 CJK 字符
     ⇒ rc=1(治理注记区自声明"投稿前删除",属设计内豁免)。
  2. stale v0-TODO:仅允许 "title alternatives"(title/venue 人决项)存活;
     方括号 stale 标记形态 `[v0-TODO` 的任何其他出现(含叙述性指涉)⇒ rc=1
     (纯词元叙述如 "v0-TODO markers = 0" 不违禁)。
退出码:0=卫生面干净;1=列出违例行。
用法:.venv/bin/python scripts/draft_hygiene_check.py [--draft PATH]
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DRAFT = REPO / "docs" / "n1-paper-draft.md"
CJK = re.compile(r"[\u4e00-\u9fff]")
ALLOWED_TODO = "title alternatives"


def check(text):
    """返回违例行列表 [(lineno, reason, line)];0 条=干净。"""
    violations = []
    in_governance = True  # 文件头至 ## Abstract 前为治理面
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            in_governance = False
        if in_governance:
            continue
        if CJK.search(line):
            violations.append((i, "cjk", line))
        elif "[v0-TODO" in line and ALLOWED_TODO not in line:
            violations.append((i, "stale-todo", line))
    return violations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", type=Path, default=DEFAULT_DRAFT)
    args = ap.parse_args()
    text = args.draft.read_text(encoding="utf-8")
    violations = check(text)
    if violations:
        print(f"DRAFT-HYGIENE FAIL: {len(violations)} 处违例({args.draft}):")
        for lineno, reason, line in violations:
            print(f"  L{lineno} [{reason}] {line.strip()[:80]}")
        return 1
    print(f"DRAFT-HYGIENE CLEAN: 正文级中文残留=0 且 stale v0-TODO=0({args.draft})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
