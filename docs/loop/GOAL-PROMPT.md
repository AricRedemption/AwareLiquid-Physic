# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> **会话角色(AMM-011)**:粘贴本文件的是**执行会话**——按 GOALS.md 程序计数器
> 迭代:清欠账→队列目标→(判据满足时)收口。体系设计/治理改动在**独立设计
> 会话**进行(AMENDMENTS 提案制);设计会话不执行研究实验,执行会话不改机制。
> **版本:v9.3(目标达成检测驱动:blocked-human 目标族每轮实跑 check_cmd
> 做达成检测+全阻机械等待态 BLOCKED-HUMAN——等待=状态迁移非心跳轮询;
> v9.2 长跑结构修复条款全部保留)**——
> 正文只写可执行动作与文件指针;立法史在 AMENDMENTS,路由细则在 goal_check,
> 数值在 probe_run/balance_gauge。v8.x 系列交付副本全部作废,以本文件为唯一正本。

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环:**本会话即马拉松,连续执行多个心跳**。每心跳=./scripts/goal_check→按 VERDICT 行动→门禁(pytest 全绿+benchmarks/audit_results.py --check 全过+scripts/direction_gate --check-round 本轮+./scripts/goal_check --audit,一律显式退出码判定)→原子提交 push fork→**立即下一心跳,回合永不主动结束**(本宿主回合终止=会话终止),不得以"等待触发"为由结束;**停止权外置:结束会话仅两源——用户显式停止令/宿主硬限(截断或预算),及 goal_check 全阻机械等待态(可行动 0+用户门控目标全未达成+派生评估判否 ⇒ 置 BLOCKED-HUMAN 休息,重入口即恢复)**,代理无自宣收束权;上下文过长(将尽)时代理唯一合法动作=程序计数器瘦身快照进 GOALS(不删 .loop-lock)后继续心跳直到宿主实际截断,重开粘贴续跑;PARKED(跨段 S3)=状态标注非收束理由;BLOCKED-HUMAN=机械等待态(置态判据=goal_check exit 6+派生评估判否双机械留痕,等待=状态迁移,禁以心跳轮询当监听器)。

## 心跳语义(机械定义;细则唯一源=GOALS.md 语义注记+goal_check 输出)
**研究拍与簿记拍分离**:研究心跳=队列弹出/判读行/写作/蒸馏 [行动];簿记心跳(夜账/对账/索引/瘦身/简报)仅段尾或 ≥15 产出心跳触发,禁自造簿记凑产出。SUPPLY-EMPTY(队列空)=**供给故障信号,非合法稳态**:唯一合法动作=①检查最近判读行可否派生新轴(判"否"须引闭族/闭轴证据,池枯判定每段重审)②不可派生⇒逐目标达成检测处置:goal_check 对 blocked-human 条目每轮实跑 check_cmd(用户裁定落盘/凭证就位⇒弹出按重入口行动);全阻 ⇒ 派生评估判否后置 state: BLOCKED-HUMAN 休息(机械等待态,禁以心跳轮询当监听器),重入口(用户一句话/新欠账/停车场与算力重启/新会话入口)⇒RUNNING 续跑。

## 心跳分支(细则以 goal_check 输出为准)
0 弹出晋升 / 1 迭代一步 / 2 SUPPLY-EMPTY=供给故障处理:①判读行派生评估(目标供给义务)②派生可行⇒新轴入队执行 ③不可派生⇒逐目标达成检测处置(见心跳语义);蒸馏轮可用(可复核出处+适用条件+验证状态,方向类须 T1 可行动,弱题录禁 [行动],同 query 族换法 ≤3),每段至少一次良信尝试拒绝留痕;判读完下一心跳=消化轮禁新蒸馏。/ 3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)/ 6 ALL-BLOCKED-HUMAN=全目标用户门控未达成:先派生评估(判否须引闭族/闭轴证据留痕,池枯每唤醒重审)⇒判否⇒置 state BLOCKED-HUMAN+原子提交+会话休息(夜账欠段则先段尾入账);达成检测每轮实跑,任一 check 过⇒弹出按重入口行动。

## 状态与恢复
会话级 state 在 GOALS.md(RUNNING/PARKED=跨段 S3 判定/BLOCKED-HUMAN=状态标注);任务级在队列 status 字段:方向条目**开 PR 即终态**=同一心跳弹出归档(QUEUE-ARCHIVE.md),合并与算力=用户门控零催促,blocked_on 禁列 PR 项;用户一句话重入口优先级最高(先答质询再续跑,同拍完成);恢复=读盘(marathon_guard→goal_check),不依赖会话记忆或散文注记;段记录三数=队列迭代数/研究拍/簿记拍(每段必记)。

## 纪律(研究面细则唯一源=AGENTS.md/PLAYBOOK/AMENDMENTS,渐进披露按需读盘)
算力四档以 scripts/probe_run 为唯一执行点,当前激活 T0/T1,T2/T3/隐藏卷停放待用户重启,Probe-First 保留;资源红线 CPU<80% 不可逾越;结论分级=T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷,meta 带 exec_tier,对照类探针 3-seed;预注册判负标准先行(PRD §19);每轮提交前 direction-gate 判单(round/direction/evidence)并过 --check,连续 2 条 DRIFT⇒BLOCKED-HUMAN;balance_gauge 报警即行动;S1/S2=模式切换非收束。
每轮回写 PLAYBOOK≥1 条;新工具入 TOOLS;机制改动走 AMENDMENTS 提案,不自改本 prompt 与宪法;分支 wave/loop,方向切 dir/<slug>,不 push master/origin,不提交 .pt;隐藏集 hidden_check,seed 999 退役 998 递减一次性终跑;真相源=PRD/PRINCIPLES(研究)/GOALS(元状态)/DEBT-LEDGER(欠账)/RSI-INDEX(指数)。
RSI:夜账入账=段尾或 ≥15 产出心跳(二者取晚),转 PARKED 前必入账,跑 ./scripts/rsi_night --from N --to M --include-dir,工具出草稿 K/T/D/Â 人裁终判;夜账 v3 全口径(dir 在途并入),主线口径 K 恒 0 禁作停滞依据;T 以一次性 seed 终跑为唯一信号不降格;EXP≥20% 由 balance_gauge 强制。
```
