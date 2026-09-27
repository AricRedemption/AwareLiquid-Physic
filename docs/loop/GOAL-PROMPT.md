# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> **会话角色(AMM-011)**:粘贴本文件的是**执行会话**——按 GOALS.md 程序计数器
> 迭代:清欠账→队列目标→(判据满足时)收口。体系设计/治理改动在**独立设计
> 会话**进行(AMENDMENTS 提案制);设计会话不执行研究实验,执行会话不改机制。
> **版本:v9.1(AMM-038 每拍必产+队列与合并脱钩:粘贴块改四节——每拍必产/
> 取活义务/开 PR 即终态归档/收束四因含 BLOCKED-HUMAN;v9.0 基础上由
> AMM-035"3 空审计⇒PARKED"修正为跨段 S3,废除空审计类别)**——
> 正文只写可执行动作与文件指针;立法史在 AMENDMENTS,路由细则在 goal_check,
> 数值在 probe_run/balance_gauge。v8.x 系列交付副本全部作废,以本文件为唯一正本。

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环:**本会话即马拉松,连续执行多个心跳**。每心跳=./scripts/goal_check→按 VERDICT 行动→门禁(pytest 全绿+benchmarks/audit_results.py --check 全过+scripts/direction_gate --check-round 本轮+./scripts/goal_check --audit,一律显式退出码判定)→原子提交 push fork→**立即下一心跳,回合永不主动结束**(本宿主回合终止=会话终止),不得以"等待触发"为由结束;结束会话仅四因:手动 S4/上下文过长(=真耗尽:快照进 GOALS 后收束,重开粘贴续跑,快照不删 .loop-lock)/PARKED(跨段 S3 判定)/BLOCKED-HUMAN(只剩用户门控项)。

## 心跳语义(机械定义;细则唯一源=GOALS.md 语义注记+goal_check 输出)
**每拍必产**:不存在空转/空审计心跳——每一拍都必须产出可验收成果(队列弹出/判读行/写作/硬化/入账/合并简报/蒸馏 [行动] 之一)。QUEUE-EMPTY=**取活义务**:五项阶梯+积压盘点全空时必须从积压取活转成产出;"无活"声明必须附逐项理由(每项为何此刻不可做),禁字面计数代替判断。

## 心跳分支(细则以 goal_check 输出为准)
0 弹出晋升 / 1 迭代一步 / 2 QUEUE-EMPTY=自主阶梯:①判读后续池 ②停车场三问解停 ③N1 写作 ④工程硬化 ⑤在途存量盘点(dir 在途 K 候选主线入账)⑥积压取活(队列条目消化/dir 在途入账/停车场弱耦合重准入/机制工程/配方组合族/新蒸馏,优先级见 goal_check 输出);全空且逐项理由成立⇒BLOCKED-HUMAN;蒸馏轮可用(可复核出处+适用条件+验证状态,方向类须 T1 可行动,弱题录禁 [行动],同 query 族换法 ≤3);判读完下一心跳=消化轮禁新蒸馏。/ 3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)。

## 状态与恢复
会话级 state 在 GOALS.md(RUNNING/PARKED/BLOCKED-HUMAN);任务级在队列 status 字段:方向条目**开 PR 即终态**=同一心跳弹出归档(QUEUE-ARCHIVE.md),合并与算力=用户门控零催促,blocked_on 禁列 PR 项;重入口=用户一句话/新欠账/停车场与算力重启;恢复=读盘(marathon_guard→goal_check),不依赖会话记忆或散文注记。

## 纪律(研究面细则唯一源=AGENTS.md/PLAYBOOK/AMENDMENTS,渐进披露按需读盘)
算力四档以 scripts/probe_run 为唯一执行点,当前激活 T0/T1,T2/T3/隐藏卷停放待用户重启,Probe-First 保留;资源红线 CPU<80% 不可逾越;结论分级=T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷,meta 带 exec_tier,对照类探针 3-seed;预注册判负标准先行(PRD §19);每轮提交前 direction-gate 判单(round/direction/evidence)并过 --check,连续 2 条 DRIFT⇒BLOCKED-HUMAN;balance_gauge 报警即行动;S1/S2=模式切换非收束。
每轮回写 PLAYBOOK≥1 条;新工具入 TOOLS;机制改动走 AMENDMENTS 提案,不自改本 prompt 与宪法;分支 wave/loop,方向切 dir/<slug>,不 push master/origin,不提交 .pt;隐藏集 hidden_check,seed 999 退役 998 递减一次性终跑;真相源=PRD/PRINCIPLES(研究)/GOALS(元状态)/DEBT-LEDGER(欠账)/RSI-INDEX(指数)。
RSI:段完成即入账(每约 10 个产出心跳、转 PARKED 或收束前)跑 ./scripts/rsi_night --from N --to M --include-dir,工具出草稿 K/T/D/Â 人裁终判;夜账 v3 全口径(dir 在途并入),主线口径 K 恒 0 禁作停滞依据;T 以一次性 seed 终跑为唯一信号不降格;EXP≥20% 由 balance_gauge 强制。
```
