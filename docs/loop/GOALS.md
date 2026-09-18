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
  D5-EXPOSURE(轮 61 入队,源:经验蒸馏轮 61 扫描 §8):判读
  prefix/semigroup 训练循环的输入构造与自回归滚出评测口径的一致性
  (exposure gap 是否存在;文献坐标 Brandstetter 2022 pushforward)。
  零算力目标:代码判读 + 报告 + 视结论预注册协议。
current_action: >-
  运行 ./scripts/goal_check 并按其 VERDICT 继续:ACHIEVED → 顶部目标已
  弹出并晋升下一位,对新目标执行其首个迭代步;NOT-Achieved → 对当前
  顶部目标迭代一步(未达成不停)。每轮心跳先校验,再干活。
  队列非空(D5-EXPOSURE,轮 61 补池),不再空转。
  外部触发仍然有效:R1/R2 云结果回传(机械验收 §12.3 判据)→ E2
  条件性重入口视 ρ_CB′;或用户"继续"。
done_condition: >-
  D5 判读报告(gap 定性 + 证据行号)入 PRD §19;gap 存在则 pushforward
  变体协议预注册(判负标准/seeds/命令/时长)+ 云欠账登记;pytest 全绿
  + audit --check 全过 + 原子提交 push。
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35+ 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: 用户粘贴最新 GOAL-PROMPT.md(启动器已按用户指令删除,无自动触发) / 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/scan-conditioning.md §8
  (文献坐标;轮 61 蒸馏);updated 见下
updated: 2026-09-19 05:2x (轮 62:D5-EXPOSURE 判读完成——exposure gap
  不存在,pushforward 不适用,证据入 PRD §19 轮 62;引用清单入 scan §8.5;
  goal_check 空 check_cmd 假阳性坑修复+回写。D5 待下轮 goal_check 弹出)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
  - id: D5-EXPOSURE
    track: engineering
    goal: >-
      滚出口径一致性判读:prefix/semigroup 训练循环输入构造(真值前缀
      vs 模型自预测)与自回归滚出评测口径对比,定性 exposure gap。
      零算力(代码判读+文档);文献坐标 scan-conditioning.md §8
      (pushforward/SRNN/exposure-bias 谱系)。
    done_condition: >-
      判读报告入 PRD §19(逐路径证据:训练输入来源行号 + 评测输入
      来源行号 + gap 定性结论);gap 存在 ⇒ pushforward 变体协议预注册
      (动机/判负标准/seeds/完整命令/冒烟校准时长)入 PRD §19 并登记
      云欠账;gap 不存在 ⇒ 评测口径辩护段落入 PRD §19 + Related Work
      引用清单(scan §8.3/8.4)入 scan 档案。pytest 全绿 + audit
      --check 全过 + 原子提交 push fork wave/loop。
    check_cmd: grep -q "D5-EXPOSURE 判读" docs/PRD.md 2>/dev/null
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
