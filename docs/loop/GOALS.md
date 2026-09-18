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
  夜 4 收口(轮 61-72):队列空,蒸馏补池 ×6(18 条入库,scan §8-14)+
  零算力判读 ×5(D5 口径辩护/D6 信息预算/T 非偶机制发现/无噪确认/超分
  反向弱信号)+ 工具 +2;RSI 夜 4 行已入账(≈0.45,T̂ 未触发保守计 0)。
  剩余工作全外部阻塞:R1/R2 云回传(欠账 ~70min,分流表 scan §12.3 就绪)。
current_action: >-
  收尾完成,循环待触发。下一触发:R1/R2 云结果回传(机械验收 PR §3 +
  三路分流 §12.3)→ 按失败模式路由 R1b/R1c/E2 条件入口;或用户"继续"
  (先跑 ./scripts/goal_check 路由,队列空则按 PLAYBOOK 蒸馏轮闭环补池)。
done_condition: >-
  条件入口路由表就绪(scan §12.3);队列非空时永不停——每轮 goal_check 路由。
blocked_on: >-
  1) R1/R2 云结果回传(欠账 ~70min);2) D4 GPU 去向;3) origin/master
  合入顺序(PR#1 CLEAN 可合);4) N1 正式英文稿是否启动。
next_trigger_hint: R1/R2 云结果回传 / 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/scan-conditioning.md §8-10
  (文献坐标;轮 61/63/65 蒸馏);updated 见下
updated: 2026-09-19 07:2x (夜 4 收尾:RSI 入账 0.45;条件入口路由表就绪;
  .loop-lock 已删;待云回传或用户触发)
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
**R1c 条件性重入口(轮 68 登记,不入队)**:R1 判负且 ctx 探针仍 ≈0
(信息没进来)⇒ R1c(attention/可学习聚合替代节点 mean-pool,代码
前提已定位 model.py 编码管线;scan §12.2)。三路分流判读逻辑见
scan §12.3。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
