#!/usr/bin/env bash
# headless_loop.sh — AMM-002: GOALS.md 驱动的连续循环监督进程
#
# 模式:wake fresh + state file(aicell/极简循环派)。每个心跳检查
# docs/loop/GOALS.md 的 state:RUNNING 则以 headless 方式重启一轮
# (新会话,按 AGENTS.md 自动加载的规程继续 current_action,28 分钟盒),
# 完成后冷却;IDLE/BLOCKED-HUMAN 退避;窗口外(23:00–09:00 之外)睡眠。
#
# 启用(需先停用 cron 心跳避免双跑,见 AMM-002):
#   ZCODE_CMD="<headless 调用,如: zcode -p>" \
#     nohup ./scripts/headless_loop.sh >> /tmp/alp_loop.log 2>&1 &
# 停止:pkill -f headless_loop.sh
set -u

REPO="$(cd "$(dirname "$0")/.." && pwd)"
ZCODE_CMD="${ZCODE_CMD:-}"           # headless 调用命令(用户侧填实际二进制/flag)
ROUND_PROMPT="夜间心跳轮:按工作区 AGENTS.md 与 docs/loop/GOALS.md 的 current_action 继续,28 分钟时间盒,完成后推进 GOALS.md 并原子提交 push。"

cd "$REPO"
window_ok() { local h; h=$(date +%H); [ "$h" = "23" ] || { [ "$h" -ge 0 ] && [ "$h" -le 8 ]; }; }
state()     { sed -n 's/^state: *//p' docs/loop/GOALS.md | head -1; }

echo "[$(date '+%F %T')] supervisor start (repo=$REPO)"
while true; do
  if ! window_ok; then
    echo "[$(date '+%F %T')] outside window (23:00-09:00), sleep 600s"
    sleep 600
    continue
  fi
  git fetch --all --prune -q   # origin/master 有新合入时,轮内规程会自行 merge
  st="$(state)"
  case "$st" in
    RUNNING)
      if [ -z "$ZCODE_CMD" ]; then
        echo "[$(date '+%F %T')] ZCODE_CMD 未设置,无法 spawn headless 轮;sleep 1800s"
        sleep 1800
        continue
      fi
      echo "[$(date '+%F %T')] spawn round"
      "$ZCODE_CMD" "$ROUND_PROMPT"
      echo "[$(date '+%F %T')] round exit=$?; cooldown 120s"
      sleep 120
      ;;
    IDLE|BLOCKED-HUMAN)
      echo "[$(date '+%F %T')] state=$st, backoff 1800s"
      sleep 1800
      ;;
    *)
      echo "[$(date '+%F %T')] state unparsable ('$st'), sleep 600s"
      sleep 600
      ;;
  esac
done
