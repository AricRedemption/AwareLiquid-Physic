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
  夜 3 收口(轮 50-60):D2-CAPACITY 全链闭环——E1 推断瓶颈(oracle −27%
  兑现于同一接口 × 双探针≈0)、E3 容量否定、E4a 饥饿确认(3.97e-3)、
  R1/R2 云交付包+欠账 ~70min;RSI 夜 3 行已入账(≈0.66)。队列穷尽,
  剩余工作全部外部阻塞(云回传/人工裁定)。
current_action: >-
  运行 ./scripts/goal_check 并按其 VERDICT 继续:ACHIEVED → 顶部目标已
  弹出并晋升下一位,对新目标执行其首个迭代步;NOT-Achieved → 对当前
  顶部目标迭代一步(未达成不停)。每轮心跳先校验,再干活。
  队列空(穷尽,query 清单见 PRD §19 轮 60 与 scan-conditioning.md)。
  下一触发:按最新 GOAL-PROMPT.md(停止条款 v2)进入经验蒸馏轮补池;
  或 R1/R2 云结果回传(机械验收 §12.3 判据)→ E2 条件性重入口视 ρ_CB′;
  或用户"继续"。
done_condition: >-
  队列空时进入文献扫描补队列;队列非空时永不停——每轮 goal_check 路由。
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35+ 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: 用户粘贴最新 GOAL-PROMPT.md(启动器已按用户指令删除,无自动触发) / 用户"继续"
pointer: docs/PRD.md §19(轮 60 收尾记录;设计 docs/d2-capacity-design.md §12;RSI-INDEX 夜 3 行)
updated: 2026-09-19 04:07 (一致性终检:修正时间戳与失效触发引用;分支模型 AMM-005 已同步)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue: []
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空才允许空转/扫描补池。
**E2 条件性重入口(不入队,防路由器空转)**:若 E3 修复推断后
ρ_CB′ 仍 ≥0.9(接口重成第一嫌疑),把 E2(concat/hyper,设计文档 §6
原闸门)追加回队尾。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
