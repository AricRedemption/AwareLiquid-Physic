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
  D6-INFO-BUDGET(轮 63 入队,源:经验蒸馏轮 63 扫描 §9):信息预算
  分解——J(ω; t_obs) 图谱平台判定 + E1 缺口进"窗口 Fisher 上界 vs
  oracle 可读出 vs 实际推断"框架。零算力(闭式 Fisher 扫描+判读+文档)。
current_action: >-
  运行 ./scripts/goal_check 并按其 VERDICT 继续:ACHIEVED → 顶部目标已
  弹出并晋升下一位,对新目标执行其首个迭代步;NOT-Achieved → 对当前
  顶部目标迭代一步(未达成不停)。每轮心跳先校验,再干活。
  队列非空(D6-INFO-BUDGET,轮 63 补池)。
  外部触发仍然有效:R1/R2 云结果回传(机械验收 §12.3 判据)→ E2
  条件性重入口视 ρ_CB′;或用户"继续"。
done_condition: >-
  D6 判读记录(J 图谱平台判定+信息预算分解)入 PRD §19;pytest 全绿
  + audit --check 全过 + 原子提交 push。
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35+ 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: 用户粘贴最新 GOAL-PROMPT.md(启动器已按用户指令删除,无自动触发) / 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/scan-conditioning.md §8-10
  (文献坐标;轮 61/63/65 蒸馏);updated 见下
updated: 2026-09-19 06:0x (轮 66 零算力深化:R1b 前提判读——T 非偶 ⇒
  回程不一致(实测 4.6e-1 vs 偶 T 对照 1.2e-7),docstring 过度声明修订,
  R1b 语义升级为真物理归纳偏置(PRD §19 轮 66)。队列空,下一触发:
  R1/R2 云回传 / 蒸馏 / 用户停)
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
**R1b 条件性重入口(轮 65 登记,轮 66 修订,不入队)**:若 R1 云结果
回传判负(辅助辨识损失未兑现 oracle 缺口收敛),把 R1b 追加回队尾——
先决条件已判明:当前 T 非偶 ⇒ 回程一致性需先补结构(硬:T 偶参数化;
软:一致性损失,PRD §19 轮 66),真物理归纳偏置(动能偶),判负标准
届时预注册(scan §10.3)。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
