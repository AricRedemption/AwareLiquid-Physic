# LOOP AMENDMENTS — 循环自改进提案(人工闸门)

> RSI 落地形式:**循环可以提案修改自己的操作程序(cron 提示词/本目录下的
> 惯例),但应用必须经 AricRedemption 批准**。这是 DGM/AlphaEvolve 的
> "经验验证 + 选择"原则在治理层的对应物——提案留存、人工选择。

## 提案格式

```
### AMM-<编号>: <一句话>
- 动机:(哪个坑/哪次低效触发)
- 提案 diff:(改 cron 提示词/PLAYBOOK 惯例节的哪一句,原文→新文)
- 风险与回滚:(可能破坏什么;如何一键回退)
- 状态:PROPOSED / APPROVED / REJECTED / APPLIED
```

### AMM-003: 方向-分支-PR 交付模型 + 周六全天候 + 迭代开关按钮
- 动机(AricRedemption 2026-09-19 对齐结论):① 一个方向一个分支、单因子
  迭代到位(创新性或工程性)后**开 PR 到远程**作为交付单元;新方向开新
  分支新 PR。② 周一至五夜间 cron 照旧;**周六全天候迭代**。③ 要一个
  **开关按钮**:贴 Goal Prompt / 定义时间段 / 随时启停。
- 提案 diff:
  1. GOALS.md 增 `mode`(ON/OFF,迭代总开关)与 `iteration_window`
     (当前生效时段,周六全天候时为 00-24)字段;
  2. 新增 `scripts/iteration`(start/stop/status 按钮:改 GOALS.md 的
     mode/window;start 可贴 goal 文本直接写入 current_action);
  3. **分支纪律修订**:循环获准**开 PR**(origin/master 为目标;合并仍
     人工);方向分支 `dir/<slug>`;排序:先合 PR #1(feat,9 提交)→
     wave/loop 集成 PR → 之后 dir/* 自新 master 切出,保证单方向 PR
     干净;4. 新增周六全天候自动化(每 30 分钟,受 GOALS.md mode
     与 iteration_window 双闸)。
- 风险与回滚:PR 开启是外部可见动作——仅当方向 done_condition 达成才开,
  开前在 PRD 记录;其余回滚同 git。cron 双闸设计与夜间 cron 不冲突
  (周六 23:00 后夜间 cron 接管,白天周六自动化 22:30 最后发后静默)。
- 状态:**APPLIED**(用户对齐原话"迭代到一定程度提交一个 PR 到远程;
  新方向新分支新 PR;周六全天候";Stop-hook 应用内链式留下一轮登记)。
  **待办**:周六全天候自动化(cron `*/30 9-22 * * 6`,提示词=夜间哑触发器
  +mode/window 双闸)因 cron 会话内禁止再建定时任务而挂账——需用户在
  非 cron 会话中一句"建周六自动化"即可完成;未建期间周六由夜间 cron 的
  23:00-09:00 段覆盖。

### AMM-004: 驱动重构——单启动马拉松 + 兑底心跳,退役 30 分钟网格与 supervisor
- 动机(AricRedemption 2026-09-19 对齐):30 分钟网格心跳把驱动搞复杂了;
  目标校验应由 agent 在**一次长会话内自循环**(goal_check 每目标校验,
  未达成不停),外部只需一次启动 + 一条兑底。
- 提案 diff:① 原 30 分钟自动化改造为**夜间马拉松启动器**
  (cron `0 23 * * 1-5`:23:00 启动,会话内循环 goal_check→迭代→推进,
  08:30 写收尾+RSI 入账后自停);② AMM-002 supervisor 脚本退役(文件
  归档保留);③ 周六全天候与兑底心跳由用户在非 cron 会话创建:
  - 周六启动器:cron `0 9 * * 6`,提示词=夜间马拉松版(09:00 启动,
    自循环至 23:00,23:00 写收尾);
  - 兑底心跳:cron `13 */3 * * *`,提示词="读 GOALS.md:若 updated 距今
    >100 分钟且 state=RUNNING 且在迭代窗口内 → 拉起马拉松继续;否则
    确认即结束"。
- 风险与回滚:长会话上下文膨胀 → 马拉松提示词含快照结束条款,兑底心跳
  续命;兑底与马拉松撞车 → 心跳先看 GOALS.md updated 新鲜度(<100 分钟
  = 有活会话,no-op)。回滚 = 恢复 30 分钟 cron 表达式。
- 状态:**APPLIED**(夜间启动器已生效)。**兑底心跳:取消**(2026-09-19,
  AricRedemption 裁定+两夜实证:马拉松会话连续 20+ 轮/29+ 小时零中断,
  断链恢复成本仅"重开会话贴 prompt"30 秒,保险丝复杂度不值)。
  周六启动器:仍待用户建(或手动贴 GOAL-PROMPT.md 启动)。

### AMM-005: 分支模型落地——方向分支 dir/<slug> + 毕业 PR(修复 AMM-003 记录与提示词层的执行缺口)
- 动机:AricRedemption 2026-09-19 指出——AMM-003 记录了"方向-分支-PR"
  模型并标 APPLIED,但 GOAL-PROMPT/AGENTS/cron 的分支规则从未跟着改,
  仍写"只在 wave/loop 写"。记录与执行不一致 = 执行缺口。
- 提案 diff:GOAL-PROMPT/AGENTS/cron 三处分支规则统一为:wave/loop =
  集成线;新方向切 `dir/<slug>` 单因子迭代;毕业(判据+隐藏验证)开 PR
  (dir → 集成线;master 追平后可直开 master),合并人工;新方向新分支新 PR。
- 风险与回滚:多方向并行时分支网会变复杂——约定"同一时间只推进一个
  方向分支"(单马拉松约定自然覆盖)。回滚 = git revert 本提交。
- 状态:**APPLIED**(AricRedemption 当日指出不一致并要求修正,视为批准)

### AMM-002: headless supervisor——GOALS.md 驱动的连续循环引擎
- 动机:cron 是固定 30 分钟网格的心跳,有活时浪费等待、没活时空转;前沿
  headless agent 范式("wake fresh + state file")是**监督进程 + 状态文件**:
  有活(RUNNING)就背靠背跑,没活(IDLE/BLOCKED)退避,窗口外只睡眠——
  驱动与触发彻底解耦。
- 提案 diff:新增 `scripts/headless_loop.sh`(监督进程:窗口检查
  23:00–09:00 → 读 GOALS.md state → RUNNING 则以 `ZCODE_CMD` headless
  重启一轮("按 AGENTS.md 与 GOALS.md current_action 继续",28 分钟盒)→
  冷却 120s;IDLE/BLOCKED 睡 1800s;窗口外睡 600s)。
- 风险与回滚:① 常驻进程占配额(建议仍只在你授权的窗口跑);② headless
  CLI 具体命令需用户填 `ZCODE_CMD`(桌面版二进制不在 PATH);③ 与 cron
  并行会双跑——**启用 supervisor 前应停用 cron**(或反之)。回滚:杀进程
  即可,状态全在 GOALS.md/git。
- 状态:**RETIRED**(AMM-004 驱动重构后退役;脚本归档保留,备胎不再需要——马拉松会话即引擎)

## 规则

1. 循环每轮可追加 PROPOSED 提案,但**不得**自行修改 cron 提示词;
2. AricRedemption 批准后,由用户或下一轮循环应用并改状态为 APPLIED,
   同时在当夜收尾记录留痕;
3. 被拒绝的提案保留原文(REJECTED),不删除——提案史也是研究记录。

## 提案列表

### AMM-001: cron 提示词瘦身为哑触发器,智能迁入 GOALS.md 程序计数器
- 动机:循环规程作为静态大块存在 cron 提示词里,已三次 CronUpdate 迭代,
  越长越锈(提示词被当数据库用);且人开的会话拿不到循环规程。
- 提案 diff:① 新增工作区 `AGENTS.md` 宪法(每个会话自动加载:入口规则、
  铁律、度量指针);② 新增 `docs/loop/GOALS.md` 程序计数器(state/
  current_goal/current_action/done_condition,ACE 式演化状态);③ cron
  提示词缩为"夜间心跳:按 AGENTS.md 与 GOALS.md 执行 current_action,
  推进并原子提交;08:30 收尾轮按 RSI-INDEX 计算指数"。
- 风险与回滚:cron 会话若不自动加载 AGENTS.md 则丢失规程——回滚 = 恢复
  本文件历史版本中的完整提示词(git 可溯);GOALS.md 与 PRD §19 职责
  重叠部分以"元状态 vs 研究记录"划分,不复制真相。
- 状态:**APPLIED**(2026-09-18,AricRedemption 当日明确要求重构 goal
  prompt 为目标驱动循环,视为批准;本轮实施)
