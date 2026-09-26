#!/usr/bin/env bash
# stop_gate — ZCode Stop hook:会话内连续性闸(AMM-020;可选层,仅 ZCode 生效)
# 语义(AMM-034 v7 对齐,轮 293):模型想结束回合时触发——
#       若 队列非空 + mode=ON + 锁新鲜 + state=RUNNING
#       ⇒ exit 2 请求继续(ZCode 上限 3 次/会话);否则 exit 0 放行。
#       v7 状态机=RUNNING|PARKED|BLOCKED-HUMAN(IDLE 废除):仅 RUNNING
#       拦截续跑;PARKED(唯一非手动自停态,快照收束)与 BLOCKED-HUMAN
#       (宪法留人)均放行——v6 遗留正则 (IDLE|BLOCKED-HUMAN) 漏掉
#       PARKED 会把合法收束误拦最多 3 次。
# 安装(工作区 .zcode/config.json,需 hooks.enabled:true):
#   {"hooks":{"enabled":true,"events":{"Stop":[{"hooks":[{"type":"command",
#     "command":"bash scripts/stop_gate.sh"}]}]}}}
# 注意: 上线前先小会话试跑一次,核对 ZCode 对 Stop+exit 2 的实际续跑行为。
set -euo pipefail
cd "$(dirname "$0")/.."

grep -q "^mode: ON" docs/loop/GOALS.md || exit 0          # 总开关关 ⇒ 放行
grep -qE "^state: (PARKED|BLOCKED-HUMAN)" docs/loop/GOALS.md && exit 0  # PARKED 真停滞收束/宪法留人 ⇒ 放行(v7)

# 锁新鲜(<100min)= 有活马拉松才拦;无锁说明本来就不在马拉松里,放行
[[ -f .loop-lock ]] || exit 0
[[ -n $(find .loop-lock -mmin -100) ]] || exit 0

# 队列非空(goal_queue 块内存在 - id: 条目)⇒ 还有活,请求继续
if sed -n '/```yaml/,/```/p' docs/loop/GOALS.md | grep -q -- "- id:"; then
  echo "队列非空且马拉松存活:按 GOAL-PROMPT 连续执行下一心跳(AMM-018/020),不得以等待触发为由结束。"
  exit 2
fi
exit 0
