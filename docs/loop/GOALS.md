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
  D2-CAPACITY 线已全链交付云(PR 包+欠账登记);骨架 §6/产物索引已刷新,
  k100 audit 欠账清偿。当前:DISTILL-2 报告规范蒸馏(喂 N1 写作),随后
  轻维护至 08:30 收尾轮。
current_action: >-
  运行 ./scripts/goal_check 并按其 VERDICT 继续:ACHIEVED → 顶部目标已
  弹出并晋升下一位,对新目标执行其首个迭代步;NOT-Achieved → 对当前
  顶部目标迭代一步(未达成不停)。每轮心跳先校验,再干活。
  当前顶部 DISTILL-2:隐藏集/多种子报告规范扫描,≥1 条入库;
  完成后队列空,轻维护等待 08:30 收尾轮与云结果回传。
done_condition: >-
  队列空时进入文献扫描补队列;队列非空时永不停——每轮 goal_check 路由。
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35+ 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: 夜间马拉松(23:00 启动,自循环至 09:00) / 用户"继续" / 兑底心跳(3h)
pointer: docs/PRD.md §19(轮 55 记录为最新;设计 docs/d2-capacity-design.md §12)
updated: 2026-09-19 05:50 (N1-OQ 入档;DISTILL-2 顶部)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
- id: N1-OQ
    track: frontier
    goal: 论文骨架 §6 Open questions 刷新(容量已闭→推断侧开放问题与 R1/R2 判据入册)+ 产物索引补 D2-CAPACITY 链 + 清偿 k100_seed_scan audit 欠账
    done_condition: 骨架 §6 含推断侧开放问题且 audit k100_seed_scan 全过并记入 PRD
    check_cmd: grep -q "R1 (auxiliary identification loss)" docs/d1-start-state-mismatch.md 2>/dev/null
- id: DISTILL-2
    track: frontier
    goal: 经验蒸馏轮 2——神经 PDE/物理网络的隐藏集与多种子报告规范(直接喂 N1 §5/§6 的写作),≥1 条入库
    done_condition: docs/scan-conditioning.md 或骨架新增 ≥1 条带出处的报告规范条目
    check_cmd: grep -q "报告规范" docs/scan-conditioning.md 2>/dev/null
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
