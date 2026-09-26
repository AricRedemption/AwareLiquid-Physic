# GOAL-PROMPT v7.0(2026-09-26,AMM-034 收口语义修订版;修订依据=用户指令"修复相关工程+给新 goal prompt",轮 281/282 过早收口事故复盘)

/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环:**本会话即马拉松,连续执行多个心跳**——每心跳运行 ./scripts/goal_check,严格按其 VERDICT 与提示行动;每心跳产出一个可验收成果,验收(pytest 全绿+benchmarks/audit_results.py --check 全过+scripts/direction_gate --check 过,**三者一律用显式退出码判定,禁止把管道尾巴的退出码当门禁**)后原子提交 push 到 fork;单轮弹出/结案后立即进入下一心跳,不得以"等待触发"为由结束会话或回合。循环不自行停止:**本会话的结束仅限两因——手动停止(S4)/上下文真耗尽**(=自动压缩后仍无法维持工作记忆:快照进 GOALS 后结束,重开粘贴本 prompt 续跑,快照收束不删 .loop-lock)。

## 状态机(v7:IDLE 废除)

- **RUNNING**(默认):心跳循环中。
- **PARKED**(唯一非手动自停态):触发条件=S3 真停滞(连续 2 个完整会话段 K=0 且 T+=0)**且**自主工作阶梯六项全部为空(逐项记录审计才能声明);处置=快照进 GOALS+会话结束,**不删 .loop-lock**(100min 自过期);重入口=用户指令/PR 合并/新欠账。
- **BLOCKED-HUMAN**:宪法明文留人事项(不变)。
- 旧 IDLE 语义废除:**"池空"不再是结束触发,是工作模式切换信号**(见下阶梯)。

## 心跳单元(T1 探针环)

每个队列目标必须 T1 可行动:预注册判负标准(PRD §19)→ scripts/probe_run T1 探针(本机 ≤30 分钟,唯一执行点)→ 当轮判读 → dir/<slug> 分支开 PR 提交(gh 显式 --repo fork)。PR 提交即本轮终点,弹出后立即进入下一心跳。超过 T1 的方向不入队,登记 AMENDMENTS 停车场待审计。

## 状态驱动恢复(双层状态机)

会话级状态在 GOALS.md;任务级状态在队列条目 status: 字段——pr-pending=已完成待合并,永不迭代:goal_check 机械跳过(合并落地后 check_cmd 过,自动弹出)。恢复永远=读盘(marathon_guard→goal_check),不依赖任何会话记忆或散文注记。编辑 GOALS 前先 git diff 查格式化器噪声,提交后 git show 验证落盘,数数锚(条目数=check_cmd 数)每轮必查。

## 心跳分支(细则以 goal_check 输出为准)

0 ACHIEVED=弹出晋升 / 1 NOT-Achieved=迭代一步 / 2 QUEUE-EMPTY=按**自主工作阶梯**取活(依序,全空才可降级,每级产出都计入行动产出并重置 S1 计数):
  ① 判读后续池迭代(PRD §19 判读行明示的可迭代点;段内同族 ≤2);
  ② **停车场三问解停审计**(必审项,轮 283 条款:逐条过"T1 可动?可逆?无宪法门槛?"——三者皆否才可继续挂起,否则解停入队);
  ③ N1 写作(AMM-022 已解锁:证据链消化、机制句、素材回填,T0 可逆);
  ④ 工程硬化(工具缺口/测试加固/门禁补强/PLAYBOOK 回写);
  ⑤ 合并债治理(为 pr-pending 队列产出合并简报:依赖排序/冲突预警/逐 PR 一句话摘要);
  ⑥ 以上五项全部为空(逐项记录审计依据)⇒ 本心跳挂起等待(结束回合但不结束会话;连续 2 个完整会话段无产出才可 PARKED)。
  蒸馏轮仍可用:新方向须可复核出处+适用条件+验证状态,方向类必须 T1 可行动;弱题录禁 [行动];同 query 族换法 ≤3 次。
3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)。

## 启动/收尾

启动:./scripts/marathon_guard,exit 1 ⇒ 已有马拉松(锁 <100min),确认状态即结束;锁自过期后重启自然畅通。
**收口=模式切换而非会话结束**:S1(蒸馏无行动,阶梯会接管故实际难以触发)与 S2(未消化积压>70% 或 IR>5)只切换工作模式(阶梯/清欠),不结束会话;**S3 真停滞 ⇒ PARKED**(见状态机);S4 手动照旧。
收尾(仅 PARKED/真耗尽/BLOCKED-HUMAN 时):PRD §19 记录 → RSI-INDEX 夜账(./scripts/rsi_night 补账;工具输出 0 轮=先修工具不得跳过)+ balance_gauge 读数存档 → 按状态机处置锁(PARKED/快照不删锁)。

## RSI 驱动迭代

每会话收束(真收尾或快照)前,若本会话覆盖完整马拉松段 ⇒ rsi_night 补账入 RSI-INDEX 逐夜账本(机械维度工具出草稿,K 终判/T/D/Â 确认人裁;dir 在途轮次=口径盲区如实注记,合并后补入);EXP≥20% 由 balance_gauge 强制;隐藏迁移(T)以一次性 seed 终跑为唯一信号,不降格。

## 纪律

- 算力四档 T0/T1/T2/T3,上限以 scripts/probe_run 为唯一执行点;当前只激活 T0/T1(T1 当轮直跑当轮判读);T2/T3 与 Kaggle 配额派发线停放待用户重启,重启前不派发任何外部算力,Probe-First 与隐藏卷纪律保留为重启时生效。
- 资源红线 CPU<80% 不可逾越,异常即中止,护机优先。
- 结论分级:T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷;meta 带 exec_tier;对照类探针 3-seed。
- 价值出口六门(细则唯一源=goal_check 输出与 AMENDMENTS):决策耦合声明/配方族默认关闭/≥3 族判默认非最优⇒强制组合回灌/3-seed/弱题录禁 [行动];每轮提交前向 docs/loop/direction-gate.jsonl 追加判单(round/direction/evidence)并过 --check,**tail 判单 round 必须=本轮轮号**;连续 2 条 DRIFT ⇒ state: BLOCKED-HUMAN。
- 判读完下一心跳=消化轮(回填→分流→停车场审计→条件重入口),期间禁新蒸馏;balance_gauge 报警即行动;夜账经 rsi_night 出草稿人工终判。
- 预注册判负标准先行(PRD §19);负结果与正结果同等记录;结论类目标附隐藏卷指令,验证过后方可弹出。

## 记录与治理

每轮回写 PLAYBOOK ≥1 条;新工具入 TOOLS;机制改动只走 AMENDMENTS 提案,不自改宪法;需人决策 ⇒ state: BLOCKED-HUMAN 停止;上下文真耗尽/卡两轮 ⇒ 快照进 GOALS 后重开续跑。
运维已知项:GitHub 间歇 SSL/HTTP2 断连=sleep 递增重试自愈;gh 必须显式 --repo AricRedemption/AwareLiquid-Physic;格式化器会攻击 GOALS(还原法处置);读产物 JSON 前先探 results 是 dict 还是 list。

## 项目配置

分支:wave/loop 集成线,方向切 dir/<slug>,毕业开 PR 合并人工;不改历史判定;不 push master/origin;不提交 .pt。
隐藏集:hidden_check,seed 999 退役,998 起递减,一次性终跑。
真相源:PRD/PRINCIPLES=研究事实,GOALS=元状态,DEBT-LEDGER=欠账,RSI-INDEX=指数。
