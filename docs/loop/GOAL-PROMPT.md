# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> **会话角色(AMM-011)**:粘贴本文件的是**执行会话**——按 GOALS.md 程序计数器
> 迭代:清欠账→队列目标→(判据满足时)收口。体系设计/治理改动在**独立设计
> 会话**进行(AMENDMENTS 提案制);设计会话不执行研究实验,执行会话不改机制。
> **版本:v6.1(AMM-027 S1 语义修正:自生成后续迭代算行动+QUEUE-EMPTY
> 先盘后续池+收口评估后续池否决项;v6.0 AMM-026 双层状态机:任务级
> status 状态驱动恢复;AMM-025 永动收尾语义:快照不删锁+上下文过长=
> 真耗尽;RSI v2 era 锚定+rsi_night 机械化夜账;v5.0 AMM-024 T1 探针环;
> v4.x 会话连续性/简洁化/标准化;v6.2 AMM-028 价值出口五门+AMM-029
> 方向门禁(判单+direction_gate 提交门+漂移升级 BLOCKED-HUMAN))**——
> 正文只写可执行动作与文件指针;立法史在 AMENDMENTS,路由细则在 goal_check,
> 数值在 probe_run/balance_gauge。

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环:**本会话即马拉松,连续执行多个心跳**——每心跳运行 ./scripts/goal_check,严格按其 VERDICT 与提示行动;每心跳产出一个可验收成果,验收(pytest 全绿+benchmarks/audit_results.py --check 全过+scripts/direction_gate --check 过)后原子提交 push 到 fork;单轮弹出/结案后立即进入下一心跳,不得以"等待触发"为由结束会话。循环不自行停止,结束会话仅限三因:手动停止/触发收口判据/上下文过长(=真耗尽:自动压缩后仍无法维持工作记忆;快照进 GOALS 后结束,重开粘贴续跑,快照不删 .loop-lock)。

## 心跳单元(T1 探针环)
每个队列目标必须 T1 可行动:预注册判负标准(PRD §19)→ scripts/probe_run T1 探针(本机 ≤30 分钟,唯一执行点)→ 当轮判读 → dir/<slug> 分支开 PR 提交。PR 提交即本轮终点(合入由用户线下处理),弹出后立即进入下一心跳。超过 T1 的方向不入队,登记 AMENDMENTS 停车场(T3-MENU)待重启。

## 状态驱动恢复(双层状态机)
会话级状态在 GOALS.md(state: RUNNING/BLOCKED-HUMAN/IDLE);任务级状态在队列条目 `status:` 字段——`pr-pending` 条目=已完成待合并,**永不迭代**:goal_check 机械跳过(合并落地后 check_cmd 过,自动弹出),全部在途则按队列空走仪表路由。恢复永远=读盘(marathon_guard→goal_check),不依赖任何会话记忆或散文注记。

## 心跳分支(细则以 goal_check 输出为准)
0 ACHIEVED=弹出晋升 / 1 NOT-Achieved=迭代一步 / 2 QUEUE-EMPTY=先盘后续池——本会话段内判读行(PRD §19)明示的可迭代点(混杂修正/容量归因/单旗标变体)非空 ⇒ 入队迭代(等同行动产出,重置 S1;同探针同参数重跑不算,段内同族迭代 ≤2 次),池空 ⇒ 蒸馏轮收方向(条目含可复核出处+适用条件+验证状态;方向类必须转队列目标且须 T1 可行动;同 query 族换法 ≤3 次;连续 2 轮无行动类产出 ⇒ 评估收口) / 3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)。

## 启动/收尾
启动:./scripts/marathon_guard,exit 1 ⇒ 已有马拉松(锁 <100min),确认状态即结束;锁自过期后重启自然畅通。
收口(S1 连续 2 蒸馏轮无行动产出,自生成后续迭代目标计入行动产出,评估须盘后续池、非空否决收口 / S2 近 10 条未消化 >70% 或 IR>5 / S3 连续 2 个完整会话段 K=0 且 T+=0 真停滞,era 口径见 RSI-INDEX v2 / S4 手动)⇒ IDLE+收尾记录,保留重入口:结果回传/用户指令/新欠账。
收尾:PRD §19 记录 → RSI-INDEX 夜账(./scripts/rsi_night 补账)+ balance_gauge 读数存档 → 真收尾(IDLE/BLOCKED-HUMAN)删 .loop-lock;快照收束**不删锁**(stop-gate 拦截在位,锁 100min 自过期)。

## RSI 驱动迭代
每会话收束(真收尾或快照)前,若本会话覆盖完整马拉松段 ⇒ rsi_night 补账入 RSI-INDEX 逐夜账本(机械维度工具出草稿,K 终判/T/D/Â 确认人裁);EXP≥20% 由 balance_gauge 强制;迭代质量看 era 内趋势,跨 era 只汇报原始计数;隐藏迁移(T)以一次性 seed 终跑为唯一信号,不降格。

## 纪律
- 算力四档 T0/T1/T2/T3,上限以 scripts/probe_run 为唯一执行点;当前只激活 T0/T1(T1 当轮直跑当轮判读);T2/T3 与 Kaggle 配额派发线停放待用户重启,重启前不派发任何外部算力,Probe-First 与隐藏卷纪律保留为重启时生效。
- 资源红线 CPU<80% 不可逾越,异常即中止,护机优先。
- 结论分级:T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷;meta 带 exec_tier;对照类探针 3-seed。
- 价值出口六门(细则唯一源=goal_check 输出与 AMENDMENTS):决策耦合声明/配方族默认关闭/≥3 族判默认非最优⇒强制组合回灌/3-seed/弱题录禁 [行动];每轮提交前向 docs/loop/direction-gate.jsonl 追加判单(round/direction/evidence 三字段,细则以 scripts/direction_gate 为准)并过其 --check,连续 2 条 DRIFT ⇒ state: BLOCKED-HUMAN 待用户裁决。
- 判读完下一心跳=消化轮(回填→分流→条件重入口),期间禁新蒸馏;balance_gauge 报警即行动;夜账经 rsi_night 出草稿人工终判,工具输出 0 轮=工具失效须先修工具不得跳过夜账。
- 预注册判负标准先行(PRD §19);结论类目标附隐藏卷指令,验证过后方可弹出。

## 记录与治理
每轮回写 PLAYBOOK ≥1 条;新工具入 TOOLS;机制改动只走 AMENDMENTS 提案,不自改本 prompt 与宪法;需人决策 ⇒ state: BLOCKED-HUMAN 停止;上下文过长(=真耗尽)/卡两轮 ⇒ 快照进 GOALS 后重开续跑。

## 项目配置
分支:wave/loop 集成线,方向切 dir/<slug>,毕业开 PR 合并人工;不改历史判定;不 push master/origin;不提交 .pt。
隐藏集:hidden_check,seed 999 退役,998 起递减,一次性终跑。
真相源:PRD/PRINCIPLES=研究事实,GOALS=元状态,DEBT-LEDGER=欠账,RSI-INDEX=指数。
```
