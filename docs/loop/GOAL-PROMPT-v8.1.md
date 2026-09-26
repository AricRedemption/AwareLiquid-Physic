# GOAL-PROMPT v8.1(2026-09-27,AMM-036 挂起语义修正版;修订依据=用户第七次质询"为什么迭代一轮就停止"+轮 409 事故复盘;相对 v8.0 仅改挂起/回合语义与启动诊断,其余逐字保留)

/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环,本会话即马拉松。**心跳节奏:有活连跑,无活按冷却语义收束**——每心跳运行 ./scripts/goal_check,严格按其 VERDICT 与提示行动。**产出心跳**(队列弹出/判读/写作/硬化/简报/蒸馏有行动)必须产出可验收成果:pytest 全绿+benchmarks/audit_results.py --check 全过+scripts/direction_gate --check 过(一律显式退出码判定,禁把管道尾巴退出码当门禁),原子提交 push 到 fork;产出心跳完成后立即进入下一心跳。**挂起心跳**(见阶梯⑥)的产出=阶梯空审计记录(写入 GOALS,可验收),同样过门禁提交,提交后**立即继续下一心跳**。

## 会话与回合(AMM-036 铁律:回合永不主动结束)

- **马拉松会话的回合永不主动结束**——本宿主环境"回合终止=会话终止"且无自动唤醒,故任何心跳(含挂起心跳)完成后必须在同一回合内立即运行下一心跳,直至触发下方三种合法收束之一。
- 会话收束仅三因:
  1. 手动停止(S4);
  2. 上下文真耗尽(自动压缩后仍无法维持工作记忆:快照进 GOALS 后结束,重开粘贴本 prompt 续跑,快照收束不删 .loop-lock);
  3. **PARKED 处置完成**(见状态机:RSI 补账+快照+PRD §19 记录齐备后允许收束,.loop-lock 不删自过期)。
- 挂起不是停止,是冷却:空审计心跳与产出心跳一样在回合内连跑;挂起计数(见状态机)只防零产出空转,不改变回合连续性。

## 状态机(v8.1:IDLE 已废除;挂起有冷却上限)

- **RUNNING**(默认):心跳循环中。
- **PARKED**(唯一非手动自停态):触发条件=**同一会话内阶梯⑥连续 3 次空审计**(零产出心跳,计数连续累加,任何产出心跳清零)——这是"连续 2 个完整会话段无产出"的机械可判定替身(AMM-035);或 S3-v2 夜账判据(连续 2 个完整马拉松段全口径 K=0 且 T+=0,v3 口径见 RSI-INDEX)。处置=PRD §19 记录+rsi_night --include-dir 补账+快照进 GOALS,处置完成后允许会话收束,**不删 .loop-lock**(100min 自过期);重入口=用户指令/PR 合并/新欠账/停车场与算力重启,一句话即重启。
- **BLOCKED-HUMAN**:宪法明文留人事项(不变)。

## 心跳单元(T1 探针环)

每个队列目标必须 T1 可行动:预注册判负标准(PRD §19)→ scripts/probe_run T1 探针(本机 ≤30 分钟,唯一执行点)→ 当轮判读 → dir/<slug> 分支开 PR 提交(gh 显式 --repo fork)。**PR 提交即本轮终点**——pr-pending=躺在 PR 区,循环对合并零关注/零催促/零待办登记(AMM-035 条款 3):合并落地与否不影响循环运行,goal_check 在合并落地后经 check_cmd 自动弹出,这是唯一联动;**blocked_on 清单禁列 PR 项**。超过 T1 的方向不入队,登记 AMENDMENTS 停车场待审计。

## 状态驱动恢复(双层状态机)

会话级状态在 GOALS.md;任务级状态在队列条目 status 字段。恢复永远=读盘(marathon_guard→goal_check),不依赖任何会话记忆或散文注记。编辑 GOALS 前先 git diff 查格式化器噪声,提交后 git show 验证落盘,数数锚(条目数=check_cmd 数,./scripts/goal_check --audit)每轮必查。

## 心跳分支(细则以 goal_check 输出为准)

0 ACHIEVED=弹出晋升 / 1 NOT-Achieved=迭代一步 / 2 QUEUE-EMPTY=按**自主工作阶梯**取活(依序;每级产出都计入行动产出并重置挂起计数):
  ① 判读后续池迭代(PRD §19 判读行明示的可迭代点;段内同族 ≤2);
  ② 停车场三问解停审计(必审项:逐条过"T1 可动?可逆?无宪法门槛?"——三者皆否才可继续挂起,否则解停入队;审计本身=产出,逐项记录依据入 GOALS);
  ③ N1 写作(AMM-022 已解锁:证据链消化、机制句、素材回填,T0 可逆);
  ④ 工程硬化(工具缺口/测试加固/门禁补强/PLAYBOOK 回写);
  ⑤ 合并债治理(仅初次或 PR 状态变化时产出简报;无变化则该项=空);
  ⑥ 以上五项全部为空(逐项记录审计依据入 GOALS)⇒ **挂起心跳**:更新 GOALS 挂起计数、过门禁提交,**然后立即继续下一心跳**(回合内连跑,绝不结束回合——AMM-036);**计数满 3 ⇒ 转 PARKED** 并完成处置(不再无限挂起)。
  蒸馏轮仍可用(QUEUE-EMPTY 时):新方向须可复核出处+适用条件+验证状态,方向类必须 T1 可行动;弱题录禁 [行动];同 query 族换法 ≤3 次。
3 MINING-FROZEN=证据轮 / 4 DEBT-FIRST=清偿本机档欠账(云档不阻塞)。

## 启动/收尾

启动:./scripts/marathon_guard——exit 0 直接开跑;exit 1(BUSY)先看 guard 诊断输出:若打印 **STALE-HINT**(锁龄 ≥30min 且锁创建后零提交=活会话心跳为分钟级提交节奏),按 PLAYBOOK『死锁残留接管协议』核实证据清单(锁龄 <100min 且 ≥30min/锁 mtime≈最后提交 epoch/≈.git/index mtime/无存活心跳会话),全满足才接管(date +%s > .loop-lock 后立即 goal_check),缺一即让位;锁自过期后重启自然畅通。
收口=模式切换而非会话结束:S1(蒸馏无 [行动])与 S2(未消化积压>70% 或 IR>5)只切换工作模式(蒸馏降温/清欠优先),不结束会话;S4 手动照旧。
**RSI 入账时机(AMM-035):段完成即入账,不等会话收束**——每累计约 10 个产出心跳、或转 PARKED、或上下文收束前,跑 ./scripts/rsi_night --from N --to M --include-dir 补账入 RSI-INDEX(机械维度工具出草稿,K 终判/T/D/Â 确认人裁;dir 在途轮次已由 v3 全口径纳入,合并后转正)。

## RSI 体系(v3 全口径,AMM-035)

指标定义唯一源=docs/loop/RSI-INDEX.md。要点:夜账用 **--include-dir 全口径**(dir 在途判读行并入,source 标注,合并后转正)——主线口径 K 恒 0 已实证为结构性失真,禁再作为停滞或汇报依据;T(隐藏迁移)以一次性 seed 终跑为唯一信号,不降格;EXP≥20% 由 balance_gauge 强制。

## 纪律

- 算力四档 T0/T1/T2/T3,上限以 scripts/probe_run 为唯一执行点;当前只激活 T0/T1(T1 当轮直跑当轮判读);T2/T3 与 Kaggle 配额派发线停放待用户重启,重启前不派发任何外部算力,Probe-First 与隐藏卷纪律保留为重启时生效。
- 资源红线 CPU<80% 不可逾越,异常即中止,护机优先。
- 结论分级:T1/T2 只解锁路由与筛选,终局声明须 T3 或隐藏卷;meta 带 exec_tier;对照类探针 3-seed。
- 价值出口六门(细则唯一源=goal_check 输出与 AMENDMENTS):决策耦合声明/配方族默认关闭/≥3 族判默认非最优⇒强制组合回灌/3-seed/弱题录禁 [行动];每轮提交前向 docs/loop/direction-gate.jsonl 追加判单(round/direction/evidence)并过 --check-round 本轮轮号;连续 2 条 DRIFT ⇒ state: BLOCKED-HUMAN。
- 判读完下一心跳=消化轮(回填→分流→停车场审计→条件重入口),期间禁新蒸馏;balance_gauge 报警即行动。
- 预注册判负标准先行(PRD §19);负结果与正结果同等记录;结论类目标附隐藏卷指令,验证过后方可弹出。

## 记录与治理

产出轮回写 PLAYBOOK ≥1 条;新工具入 TOOLS;机制改动只走 AMENDMENTS 提案,不自改宪法;需人决策 ⇒ state: BLOCKED-HUMAN 停止;上下文真耗尽/卡两轮 ⇒ 快照进 GOALS 后重开续跑。
运维已知项:GitHub 间歇 SSL/HTTP2 断连=sleep 递增重试自愈(长断网=后台退避重试+循环继续本地心跳);gh 必须显式 --repo AricRedemption/AwareLiquid-Physic;格式化器会攻击 GOALS(还原法处置);读产物 JSON 前先探 results 是 dict 还是 list;死锁残留误让位=按 guard STALE-HINT 与 PLAYBOOK 接管协议处置(AMM-036 配套,勿盲目白等 100min)。

## 项目配置

分支:wave/loop 集成线,方向切 dir/<slug>,毕业开 PR 合并人工;不改历史判定;不 push master/origin;不提交 .pt。
隐藏集:hidden_check,seed 999 退役,998 起递减,一次性终跑。
真相源:PRD/PRINCIPLES=研究事实,GOALS=元状态,DEBT-LEDGER=欠账,RSI-INDEX=指数。
