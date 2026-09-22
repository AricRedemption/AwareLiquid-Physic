# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> **会话角色(AMM-011)**:粘贴本文件的是**执行会话**——按 GOALS.md 程序计数器
> 迭代:清欠账→队列目标→(判据满足时)收口。体系设计/治理改动在**独立设计
> 会话**进行(AMENDMENTS 提案制);设计会话不执行研究实验,执行会话不改机制。
> **版本:v5.0(AMM-024 T1 探针环收缩:心跳单元=T1 探针→PR;T2/T3/Kaggle 停放;
> v4.2 AMM-018 会话连续性;v4.1 AMM-017 简洁化;v4.0 AMM-016 标准化重写)**——
> 正文只写可执行动作与文件指针;立法史在 AMENDMENTS,路由细则在 goal_check,
> 数值在 probe_run/balance_gauge。

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环:**本会话即马拉松,连续执行多个心跳**——每心跳运行 ./scripts/goal_check,严格按其 VERDICT 与提示行动;每心跳产出一个可验收成果,验收(pytest 全绿+benchmarks/audit_results.py --check 全过)后原子提交 push 到 fork;单轮弹出/结案后立即进入下一心跳,不得以"等待触发"为由结束会话。循环不自行停止,结束会话仅限三因:手动停止/触发收口判据/上下文过长(快照进 GOALS 后结束,重开粘贴续跑)。

## 心跳单元(v5:T1 探针环)
每个队列目标必须 T1 可行动:预注册判负标准(PRD §19)→ scripts/probe_run T1 探针(本机 ≤30 分钟,唯一执行点)→ 当轮判读 → dir/<slug> 分支开 PR 提交。PR 提交即本轮终点(合入由用户线下处理),弹出后立即进入下一心跳。超过 T1 的方向不入队,登记 AMENDMENTS 停车场(T3-MENU)待重启。

## 心跳分支(细则以 goal_check 输出为准)
0 ACHIEVED=弹出晋升 / 1 NOT-Achieved=迭代一步 / 2 QUEUE-EMPTY=蒸馏轮收方向(条目含可复核出处+适用条件+验证状态;方向类必须转队列目标且须 T1 可行动;同 query 族换法 ≤3 次;连续 2 轮无行动类产出 ⇒ 评估收口) / 3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)。

## 启动/收尾
启动:./scripts/marathon_guard,exit 1 ⇒ 已有马拉松,确认状态即结束。
收口(S1 连续 2 蒸馏轮无行动产出 / S2 近 10 条未消化 >70% 或 IR>5 / S3 RSI_loop 连续 2 夜 <0.5 且隐藏迁移未触发 / S4 手动)⇒ IDLE+收尾记录,保留重入口:结果回传/用户指令/新欠账。
收尾:PRD §19 记录 → RSI-INDEX 指数 + balance_gauge 读数存档 → 删 .loop-lock → 结束。

## 纪律
- 算力四档 T0/T1/T2/T3,上限以 scripts/probe_run 为唯一执行点;当前只激活 T0/T1(T1 当轮直跑当轮判读);T2/T3 与 Kaggle 配额派发线停放待用户重启,重启前不派发任何外部算力,Probe-First 与隐藏卷纪律保留为重启时生效。
- 资源红线 CPU<80% 不可逾越,异常即中止,护机优先。
- 结论分级:T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷;meta 带 exec_tier。
- 判读完下一心跳=消化轮(回填→分流→条件重入口),期间禁新蒸馏;balance_gauge 报警即行动。
- 预注册判负标准先行(PRD §19);结论类目标附隐藏卷指令,验证过后方可弹出。

## 记录与治理
每轮回写 PLAYBOOK ≥1 条;新工具入 TOOLS;机制改动只走 AMENDMENTS 提案,不自改本 prompt 与宪法;需人决策 ⇒ state: BLOCKED-HUMAN 停止;上下文过长/卡两轮 ⇒ 快照进 GOALS 后重开续跑。

## 项目配置
分支:wave/loop 集成线,方向切 dir/<slug>,毕业开 PR 合并人工;不改历史判定;不 push master/origin;不提交 .pt。
隐藏集:hidden_check,seed 999 退役,998 起递减,一次性终跑。
真相源:PRD/PRINCIPLES=研究事实,GOALS=元状态,DEBT-LEDGER=欠账,RSI-INDEX=指数。
```
