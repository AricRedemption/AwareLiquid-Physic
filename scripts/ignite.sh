#!/usr/bin/env bash
# ignite — 跨 Agent 点火器(AMM-020;Ralph 式,机器级 cron/launchd 驱动,与具体
# Agent 软件解耦)。语义: 锁新鲜(<100min)=马拉松活着 ⇒ 退出;否则用
# docs/loop/agent-cmd.conf 里配置的命令把 GOAL-PROMPT 正文喂给任意 agent CLI。
#
# agent-cmd.conf 格式(一行模板,{PROMPT} 占位符会被替换为 prompt 正文):
#   zcode -p {PROMPT}
#   claude -p {PROMPT}
#   codex exec {PROMPT}
#
# 安装(机器级,独立于任何 Agent 软件,macOS launchd 例:每 30 分钟):
#   crontab: */30 * * * * /Users/aricredemption/Projects/AwareLiquid-Physic/scripts/ignite.sh >> /tmp/ignite.log 2>&1
set -uo pipefail
cd "$(dirname "$0")/.."
LOG=/tmp/ignite.log

CONF=docs/loop/agent-cmd.conf
[[ -f $CONF ]] || { echo "$(date '+%F %T') 未配置 $CONF(AGENT_CMD 模板)" >> $LOG; exit 1; }

# 有活马拉松(锁龄<100min)⇒ 不点火
if [[ -f .loop-lock ]] && [[ -n $(find .loop-lock -mmin -100 2>/dev/null) ]]; then
  exit 0
fi
# 停机条件:mode=OFF 或 state=PARKED/BLOCKED-HUMAN ⇒ 不点火(AMM-034 v7,轮 295 对齐;原 IDLE 已废除)
grep -q "^mode: ON" docs/loop/GOALS.md || { echo "$(date '+%F %T') mode=OFF,不点火" >> $LOG; exit 0; }
grep -qE "^state: (PARKED|BLOCKED-HUMAN)" docs/loop/GOALS.md && { echo "$(date '+%F %T') 真停滞收束/等人,不点火" >> $LOG; exit 0; }

CMD=$(head -1 "$CONF")
PROMPT=$(sed -n '/^```text$/,/^```$/p' docs/loop/GOAL-PROMPT.md | sed '1d;$d')
CMD=${CMD/\{PROMPT\}/$PROMPT}

echo "$(date '+%F %T') 点火: $CMD" >> $LOG
eval "$CMD" >> $LOG 2>&1
RC=$?
echo "$(date '+%F %T') 会话结束 exit=$RC" >> $LOG
exit 0
