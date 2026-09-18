# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE
mode: ON                  # AMM-003 迭代总开关(./scripts/iteration start|stop)
iteration_window: 周一至五 23:00-09:00(夜间cron);周六 09:00-23:00(全天候)
current_goal: >-
  N1 论文骨架已达 done_condition(Related Work 全文+表 1+主图引用+产物索引,
  无占位);打包阶段完成。当前转入"等裁定+轻维护"阶段。
current_action: >-
  空转等待:08:30 收尾轮做第三夜 RSI 首算;可做的小项仅剩
  (a) D2 图表化进附录 (b) N1 正式英文稿(需用户启动)。
done_condition: >-
  骨架文档无 TODO 占位;引用的每个数字可溯源到 physics_out_v02 产物或
  PRD §19;主图 docs/assets/d1g-profile-panel.png 已被正文引用。✓ 已达成
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: cron 30min 心跳(空转确认) / 用户"继续" / SessionStart
pointer: docs/PRD.md §19(轮 44 隐藏集终跑为最新关键记录)
updated: 2026-09-19 00:47 (iteration start)
```

## 状态机

- `RUNNING`:按 current_action 执行(夜间心跳或用户驱动均可)。
- `BLOCKED-HUMAN`:current_action 需要用户裁定(如 D4 GPU、PR 合入),
  此时空转触发只确认状态不改内容。
- `IDLE`:白昼/无动作,仅等待触发。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
