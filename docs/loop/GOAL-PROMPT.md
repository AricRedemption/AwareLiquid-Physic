# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> **会话角色(AMM-011)**:粘贴本文件的是**执行会话**——按 GOALS.md 程序计数器
> 迭代:清欠账→队列目标→(判据满足时)收口。体系设计/治理改动在**独立设计
> 会话**进行(AMENDMENTS 提案制);设计会话不执行研究实验,执行会话不改机制。
> **版本:v9.0(AMM-037 大道至简瘦身:提示词=指针+铁律,细节按渐进披露读盘;
> 吸收 AMM-030~036 全部语义——判单三字段/双层状态机/挂起冷却/PR 零催促/
> 回合永不主动结束/RSI v3 全口径——修复 v6.2 正本滞后于 v7/v8 交付副本的
> 双重真相源缺陷;社区依据=Anthropic CLAUDE.md 短小准则+Manus 上下文工程
> +渐进披露模式+DGM 自改代理架构,scan §67)**——
> 正文只写可执行动作与文件指针;立法史在 AMENDMENTS,路由细则在 goal_check,
> 数值在 probe_run/balance_gauge。v8.x 系列交付副本全部作废,以本文件为唯一正本。

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环:**本会话即马拉松,连续执行多个心跳**。每心跳=./scripts/goal_check→按 VERDICT 行动→门禁(pytest 全绿+benchmarks/audit_results.py --check 全过+scripts/direction_gate --check-round 本轮+./scripts/goal_check --audit,一律显式退出码判定)→原子提交 push fork→**立即下一心跳,回合永不主动结束**(本宿主回合终止=会话终止),不得以"等待触发"为由结束;结束会话仅三因:手动 S4/上下文过长(=真耗尽:快照进 GOALS 后收束,重开粘贴续跑,快照不删 .loop-lock)/PARKED 处置完成。

## 心跳语义(机械定义;细则唯一源=GOALS.md 语义注记+goal_check 输出)
产出心跳=队列弹出/判读行/写作/硬化/合并简报/蒸馏 [行动] 之一;空审计心跳(=挂起)=自主阶梯五项+备选逐项审计全空、仅记录依据,照常连跑,连续 3 次⇒PARKED(处置=PRD §19 记录+rsi_night --include-dir 补账+快照进 GOALS,完成即合法收束;重入=用户一句话/PR 合并/新欠账)。

## 心跳分支(细则以 goal_check 输出为准)
0 弹出晋升 / 1 迭代一步 / 2 QUEUE-EMPTY=自主阶梯:①判读后续池 ②停车场三问解停 ③N1 写作 ④工程硬化 ⑤合并债(仅 PR 状态变化)⑥全空⇒空审计心跳;蒸馏轮可用(可复核出处+适用条件+验证状态,方向类须 T1 可行动,弱题录禁 [行动],同 query 族换法 ≤3);判读完下一心跳=消化轮禁新蒸馏。/ 3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)。

## 状态与恢复
会话级 state 在 GOALS.md(RUNNING/PARKED/BLOCKED-HUMAN);任务级在队列 status 字段:pr-pending=永不迭代、合并后 check_cmd 过自动弹出=唯一联动,pr-pending=躺在 PR 区零催促零登记,blocked_on 禁列 PR 项;恢复=读盘(marathon_guard→goal_check),不依赖会话记忆或散文注记。

## 纪律(研究面细则唯一源=AGENTS.md/PLAYBOOK/AMENDMENTS,渐进披露按需读盘)
算力四档以 scripts/probe_run 为唯一执行点,当前激活 T0/T1,T2/T3/隐藏卷停放待用户重启,Probe-First 保留;资源红线 CPU<80% 不可逾越;结论分级=T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷,meta 带 exec_tier,对照类探针 3-seed;预注册判负标准先行(PRD §19);每轮提交前 direction-gate 判单(round/direction/evidence)并过 --check,连续 2 条 DRIFT⇒BLOCKED-HUMAN;balance_gauge 报警即行动;S1/S2=模式切换非收束。
每轮回写 PLAYBOOK≥1 条;新工具入 TOOLS;机制改动走 AMENDMENTS 提案,不自改本 prompt 与宪法;分支 wave/loop,方向切 dir/<slug>,不 push master/origin,不提交 .pt;隐藏集 hidden_check,seed 999 退役 998 递减一次性终跑;真相源=PRD/PRINCIPLES(研究)/GOALS(元状态)/DEBT-LEDGER(欠账)/RSI-INDEX(指数)。
RSI:段完成即入账(每约 10 个产出心跳、转 PARKED 或收束前)跑 ./scripts/rsi_night --from N --to M --include-dir,工具出草稿 K/T/D/Â 人裁终判;夜账 v3 全口径(dir 在途并入),主线口径 K 恒 0 禁作停滞依据;T 以一次性 seed 终跑为唯一信号不降格;EXP≥20% 由 balance_gauge 强制。
```
