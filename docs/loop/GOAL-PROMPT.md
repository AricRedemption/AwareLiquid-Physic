# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环迭代本项目:每轮先跑 ./scripts/goal_check 校验顶部目标——NOT-Achieved 则对该目标迭代一轮,ACHIEVED 则弹出晋升下一个,QUEUE-EMPTY 则进入**经验蒸馏轮**(社区/论文扫描:找有效经验与前沿方向,每条按"出处+适用条件+验证状态"入库——操作类固化进 PLAYBOOK、工具类实现进 TOOLS、方向类追加 GOALS 队尾;本轮交付=≥1 条入库条目或 ≥1 个新目标);直到我设定的收尾时间为止,中途不停。

迭代纪律:
- 启动自检(防双马拉松,第一优先):先跑 `./scripts/marathon_guard`——exit 1 ⇒ 已有活马拉松(锁龄 <100 分钟),本次转为"仅确认状态并结束";exit 0 ⇒ 放行进入循环体(循环内每轮 goal_check 自动刷新 .loop-lock 存活心跳;收尾时删除它)。绝不并行第二马拉松。
- 算力闸门(硬,每轮动手前必过):本机**不做任何训练/批量评测/长跑类执行——无论预计时长**。凡是"要跑结果"的任务:① 预注册协议(写进 docs/PRD.md §19:动机、判负标准、seeds、完整命令、预计时长);② 把可执行产物(脚本/参数/判据)做成 PR 交付云算力/他人执行;③ 在 PRD §19 登记云算力欠账;④ 立即换下一方向,绝不本地硬跑、绝不为等结果阻塞。
- 本机只允许(<10 分钟/条,每轮算力类合计 <20 分钟):快速探针、数据分析/判读、文献扫描、文档写作、单文件小修、冒烟实测(验证语法与数据形状,不跑完整实验)。
- 吞吐优先:每轮时间预算向"方向迭代"倾斜——一个心跳尽量产出一个非算力型成果(设计文档/探针结论/代码+测试/判读报告)。
- 每次迭代:预注册判负标准先行(写进 docs/PRD.md §19)→ pytest 全绿 + benchmarks/audit_results.py --check 全过 → 原子提交 push 到 fork 的 wave/loop 分支。
- 收尾时间由你决定:粘贴时可以附加说明(如"跑到今晚 23 点收尾");不指定则持续迭代,直到你手动停止(说停/关闭会话)。收尾动作固定:在 PRD §19 写收尾记录,并按 docs/loop/RSI-INDEX.md 计算当夜指数(K/E/T/D/T+/A+复合)入账 → 删除 .loop-lock(如存在)→ 停止本会话。
- 上下文过长或单目标卡住超过两轮:把状态快照进 docs/loop/GOALS.md 后结束本轮;重开新会话粘贴本 prompt 即无缝续跑。
- 需要人决策的事:GOALS.md 的 state 改 BLOCKED-HUMAN 并写明问题,停止。
- 每轮收尾强制回写:至少一条经验/教训/坑到 docs/loop/PLAYBOOK.md(没有坑就写一条被验证有效的做法)——大厂"抓问题→学经验→升级"的最小落地。
- 结论类目标(得出"X 比 Y 好"类定量结论)的交付 PR 必须包含隐藏卷终跑指令(用未消耗 seed 复验主结论);隐藏结果回传并通过判据后,目标才算达成弹出——防被单次抽签骗。
- 新踩的坑回写 docs/loop/PLAYBOOK.md;新工具回写 docs/loop/TOOLS.md;对循环自身的改进提案写 docs/loop/AMENDMENTS.md(不自行改本 prompt 与宪法)。

纪律以工作区 AGENTS.md 为准。分支模型(AMM-003/005):`wave/loop` = 集成线(所有已验证成果汇入);**每个新方向自 wave/loop 切 `dir/<slug>` 分支,单因子迭代到底**——方向 done_condition 达成且判据/隐藏验证通过 → 开 PR(dir/<slug> → 集成线;origin/master 追平后可直接开到 master),合并仍人工;新方向 = 新分支 = 新 PR。不改写历史判定行;不 push master/origin;不提交 .pt;隐藏集终跑用 ./scripts/hidden_check(seed 999 已退役,998 递减)。
纪律以工作区 AGENTS.md 为准。分支模型(AMM-003/005):`wave/loop` = 集成线(所有已验证成果汇入);**每个新方向自 wave/loop 切 `dir/<slug>` 分支,单因子迭代到底**——方向 done_condition 达成且判据/隐藏验证通过 → 开 PR(dir/<slug> → 集成线;origin/master 追平后可直接开到 master),合并仍人工;新方向 = 新分支 = 新 PR。不改写历史判定行;不 push master/origin;不提交 .pt;隐藏集终跑用 ./scripts/hidden_check(seed 999 已退役,998 递减)。
停止规则:只在三种情况停止——① 你设定的收尾时间到(先做收尾动作:PRD §19 收尾记录 + RSI-INDEX 指数入账 + 删除 .loop-lock);② 全部方向 BLOCKED-HUMAN(写明问题);③ 经验蒸馏连续 2 轮、不同 query 族扫描均无产出且无零算力深化目标(附每轮 query 清单,时间用 date 实测)。除此之外:队列非空就迭代,未达成就继续。
```

**需要算力的目标的一生**(详见 PRD §19 各轮协议):发现(本地探针)→ 预注册验收标准(本地文档)→ PR 交付算力(含隐藏卷终跑指令)→ 结果回传 → 机械验收 → 毕业弹出/如实记负。
