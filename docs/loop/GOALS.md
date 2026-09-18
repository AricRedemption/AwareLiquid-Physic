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
pointer: docs/PRD.md §19(判读报告落点);docs/scan-conditioning.md §8
  (文献坐标;轮 61 蒸馏);updated 见下
updated: 2026-09-19 05:3x (轮 63 经验蒸馏:§9 三条入库(PE/concurrent
  learning/OED,出处+适用条件+验证状态);D6-INFO-BUDGET 零算力目标入队,
  check_cmd 已带)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
  - id: D6-INFO-BUDGET
    track: engineering
    goal: >-
      信息预算分解(零算力):用现有 identifiability_probe.fisher_j 闭式
      扫 J(ω; t_obs) 图谱(ω∈[0.7,1.8] × t_obs 8..48),判定 t_obs=24
      的信息平台位置;把 E1 的 oracle −27% 缺口放进"窗口 Fisher 上界 vs
      oracle 可读出 vs 实际推断"的信息预算框架。文献坐标 scan §9
      (PE/concurrent learning/OED)。
    done_condition: >-
      D6-INFO-BUDGET 判读记录入 PRD §19(J 图谱平台判定 + 数字 + 信息
      预算分解表述,服务 D2-CAPACITY 叙事与 N1);pytest 全绿 + audit
      --check 全过 + 原子提交 push fork wave/loop。
    check_cmd: grep -q "D6-INFO-BUDGET 判读" docs/PRD.md 2>/dev/null
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
