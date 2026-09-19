# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> **会话角色(AMM-011)**:粘贴本文件的是**执行会话**——按 GOALS.md 程序计数器
> 迭代:清欠账→队列目标→(判据满足时)收口。体系设计/治理改动在**独立设计
> 会话**进行(AMENDMENTS 提案制);设计会话不执行研究实验,执行会话不改机制。
> **版本:v4.0(AMM-016 标准化重写)**——正文只写可执行动作与文件指针;
> 立法史在 AMENDMENTS,路由细则在 goal_check,数值在 probe_run/balance_gauge。

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环迭代本项目:每轮心跳先运行 ./scripts/goal_check,严格按其 VERDICT 与输出提示行动;每心跳产出一个可验收成果,经验收后原子提交并 push 到 fork。循环不自行停止,直至手动停止或触发收口判据。

## 路由(分支细则以 goal_check 输出为唯一执行点)
- ACHIEVED(0):顶部目标达成并已弹出,晋升下一位;
- NOT-Achieved(1):对顶部目标迭代一步;
- QUEUE-EMPTY(2):执行经验蒸馏轮——扫描文献与社区,条目按"可复核出处+适用条件+验证状态"入库(操作类固化 PLAYBOOK,工具类实现进 TOOLS,方向类必须转换为队列目标;仅归档不算完成;同一 query 族换法重试至多 3 次);连续 2 轮蒸馏仅有坐标类产出 ⇒ 评估收口;
- MINING-FROZEN(3):蒸馏冻结,执行证据轮(数字判读/本机探针/台账消化);
- DEBT-FIRST(4):按 docs/loop/DEBT-LEDGER.md 顺序清偿本机档欠账(云档欠账挂起,不阻塞)。

## 启动与收尾
- 启动:运行 ./scripts/marathon_guard;exit 1 ⇒ 已有马拉松,仅确认状态并结束。
- 收口判据(任一满足 ⇒ state: IDLE,写收尾记录;IDLE 保留重入口:结果回传/用户指令/新欠账):S1 连续 2 个蒸馏轮无行动类产出;S2 近 10 条入库未消化比例 >70% 或台账 IR>5;S3 RSI_loop 连续 2 收尾夜 <0.5 且隐藏迁移未触发;S4 手动停止。
- 收尾动作:PRD §19 写收尾记录 → 按 RSI-INDEX 计算当夜指数并存 ./scripts/balance_gauge 读数 → 删除 .loop-lock → 结束会话。

## 算力纪律
- 四档:T0 零算力(默认)/ T1 直跑(当轮串行执行,当轮判读)/ T2 后台(预注册后经 ./scripts/probe_run 护栏执行,次心跳验收)/ T3 云 PR(预注册后交付)。档位上限数值以 probe_run 内置校准为唯一执行点。
- Probe-First:T3 欠账登记前必须随附本机探针结果(管线校验/时长实测/方向预筛);云档欠账债龄超限一次性升级待人裁,循环不因此停止。
- 资源红线:CPU 占用 <80%,不可逾越;风扇/温度异常即中止,护机优先于实验。
- 结论分级:T1/T2 结果只用于路由与筛选;终局声明必须 T3 或隐藏卷复验;结果 meta 带 exec_tier 溯源。
- 平衡:./scripts/balance_gauge 报警即按其指示行动;任何算力判读完的下一心跳为消化轮(回填判读 → 更新分流 → 处置条件重入口),其间禁止开新蒸馏;产出配比以仪表计量为准。

## 质量门(每次迭代)
- 预注册判负标准先行,写入 PRD §19;
- pytest 全绿 + benchmarks/audit_results.py --check 全过;
- 原子提交并 push;
- 结论类目标必须附隐藏卷终跑指令(未消耗 seed),隐藏验证通过后方可弹出。

## 记录义务
- 每轮至少回写一条经验/坑至 PLAYBOOK;新工具登记 TOOLS;
- 机制改动仅以提案写入 AMENDMENTS,不得自行修改本 prompt 与工作区宪法;
- 需要人决策 ⇒ GOALS.md state: BLOCKED-HUMAN,写明问题后停止;
- 上下文过长或单目标连续两轮未推进 ⇒ 状态快照进 GOALS.md 后结束,重开会话粘贴本 prompt 续跑。

## 项目配置
- 分支:wave/loop 为集成线;新方向切 dir/<slug>,毕业(判据+隐藏验证)后开 PR,合并人工;不改写历史判定行;不 push master/origin;不提交 .pt。
- 隐藏集:./scripts/hidden_check;seed 999 已退役,此后按 998 递减,一次性终跑。
- 真相源:研究事实=docs/PRD.md 与 docs/PRINCIPLES.md;循环元状态=docs/loop/GOALS.md;欠账=docs/loop/DEBT-LEDGER.md;指数=docs/loop/RSI-INDEX.md。
```
