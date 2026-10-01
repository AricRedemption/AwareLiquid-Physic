#!/usr/bin/env python3
"""reflection_mine — 复盘候选挖掘器(AMM-041,轮 806;手动调用,
默认不在任何心跳路由内)。消费盘上已有的四类信号源,输出**复盘候选
清单**(每项带信号出处+建议动作类型);禁自动写 PLAYBOOK/AMENDMENTS/
prompt——修订权全留人(工具本身不改任何文件)。

信号源:
  ① 判单 jsonl 连续 DRIFT ≥2(direction_gate BLOCKED-HUMAN 触发器的先导
     弱信号);
  ② 夜账覆盖缺口:git 历史里 [from,to] 段存在心跳轮提交,而 PRD §19
     段记录数为 0(rsi_night 口径)=夜账断档(夜 11 断喂 91 轮家族);
  ③ PLAYBOOK 同坑复发:同坑条目(标题前缀归并)含 ≥2 个不同轮号;
  ④ goal_check --audit 机制异常行(AUDIT FAIL/执行异常)。

每次调用打印扫描范围+逐源命中数(非零断言面:某源 0 命中即显式报 0,
防本工具自身静默失效——家族根因的对症条款)。
用法:python3 scripts/reflection_mine.py --from 141 --to 229
                [--jsonl ... --playbook ... --audit-file ...(测试注入面)]
"""
import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROUND_IN_COMMIT = re.compile(r"wave\d+-轮(\d+)")
ENTRY_TITLE = re.compile(r"^- \*\*([^*]{4,40})")
# 出处轮号链:轮 22/92/283、轮 524/558→559 等斜杠/箭头链全收
ROUND_CHAIN = re.compile(r"轮\s*((?:\d+\s*[/→]?\s*)+)")


def sig_drift(jsonl_path):
    """①连续 DRIFT ≥2。"""
    runs, cur = [], 0
    last_round = None
    for line in Path(jsonl_path).read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("direction") == "DRIFT":
            cur += 1
            last_round = rec.get("round", last_round)
        else:
            if cur >= 2:
                runs.append(last_round)
            cur = 0
    if cur >= 2:
        runs.append(last_round)
    return [{"signal": "drift-run", "last_round": r,
             "出处": f"direction-gate.jsonl 连续 DRIFT≥2(止于轮 {r})",
             "建议动作": "BLOCKED-HUMAN 升级复核/漂移归因复盘"}
            for r in runs]


def sig_ledger_gap(lo, hi, repo, prd):
    """②夜账覆盖缺口:有心跳提交而无 §19 段记录。"""
    log = subprocess.run(["git", "-C", repo, "log", "--format=%s"],
                         capture_output=True, text=True).stdout
    commits = sorted({int(m) for m in ROUND_IN_COMMIT.findall(log)
                      if lo <= int(m) <= hi})
    r = subprocess.run([sys.executable, f"{repo}/scripts/rsi_night",
                        "--from", str(lo), "--to", str(hi),
                        "--prd", str(prd)],
                       capture_output=True, text=True)
    try:
        covered = json.loads(r.stdout.splitlines()[0])["rounds"]
    except Exception:
        covered = []
    if commits and not covered:
        return [{"signal": "ledger-gap",
                 "出处": f"轮 {lo}-{hi}:git 心跳提交 {len(commits)} 轮 vs "
                         f"§19 段记录 0 轮(夜 11 断喂家族)",
                 "建议动作": "夜账补账+断喂根因复盘(工具静默失效家族)"}]
    return []


def sig_playbook_recur(playbook):
    """③同坑复发:标题前缀归并,≥2 不同轮号。"""
    groups = defaultdict(set)
    title = None
    for line in Path(playbook).read_text(encoding="utf-8").splitlines():
        m = ENTRY_TITLE.match(line)
        if m:
            title = re.sub(r"[(:：].*$", "", m.group(1)).strip()[:16]
            continue
        if title:
            for chain in ROUND_CHAIN.findall(line):
                for rr in re.findall(r"\d+", chain):
                    groups[title].add(int(rr))
            title = None
    return [{"signal": "pit-recurrence", "pit": t,
             "rounds": sorted(rs),
             "出处": f"PLAYBOOK 同坑条目'{t}…'跨轮 {sorted(rs)}",
             "建议动作": "同坑第二次复发⇒机制级修复候选(非追加条目)"}
            for t, rs in groups.items() if len(rs) >= 2]


def sig_audit(repo, audit_file):
    """④goal_check --audit 机制异常(AUDIT FAIL 整块+执行异常行)。"""
    if audit_file:
        lines = Path(audit_file).read_text(encoding="utf-8").splitlines()
    else:
        lines = subprocess.run([f"{repo}/scripts/goal_check", "--audit"],
                               capture_output=True, text=True).stdout.splitlines()
    out = []
    for i, l in enumerate(lines):
        if "AUDIT FAIL" in l:
            block = " ⏎ ".join(x.strip() for x in lines[i:i + 4])
            out.append({"signal": "audit-anomaly",
                        "出处": f"goal_check --audit:{block[:160]}",
                        "建议动作": "队列完整性修复(禁提交态)"})
        elif "执行异常" in l:
            out.append({"signal": "audit-anomaly", "出处": f"audit:{l[:120]}",
                        "建议动作": "check_cmd 命令体修复"})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="lo", type=int, required=True)
    ap.add_argument("--to", dest="hi", type=int, required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--prd", default="docs/PRD.md")
    ap.add_argument("--jsonl", default="docs/loop/direction-gate.jsonl")
    ap.add_argument("--playbook", default="docs/loop/PLAYBOOK.md")
    ap.add_argument("--audit-file", default=None,
                    help="测试注入:预采集的 audit 输出文件(缺省=实跑)")
    args = ap.parse_args()
    repo = str(Path(args.repo).resolve())

    cands = []
    sources = {}
    for name, fn in (
            ("①drift", lambda: sig_drift(args.jsonl)),
            ("②ledger-gap", lambda: sig_ledger_gap(args.lo, args.hi,
                                                   repo, args.prd)),
            ("③pit-recurrence", lambda: sig_playbook_recur(args.playbook)),
            ("④audit", lambda: sig_audit(repo, args.audit_file))):
        try:
            hits = fn()
        except Exception as e:            # 信号源自身故障=显式报告非静默
            hits = [{"signal": "source-error", "出处": f"{name}:{e}",
                     "建议动作": "先修信号源(本工具失效面)"}]
        sources[name] = len(hits)
        cands.extend(hits)

    print(f"[reflection_mine] 扫描范围 轮 {args.lo}-{args.hi};"
          f"逐源命中={sources}(零命中如实报 0,非零断言面)")
    for c in cands:
        print(f"  [候选] {c['signal']}: {c['出处']} ⇒ {c['建议动作']}")
    print(f"[done] 候选 {len(cands)} 条——仅草稿,人裁门槛,"
          f"本工具未写任何文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
