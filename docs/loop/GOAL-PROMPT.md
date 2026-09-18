# GOAL-PROMPT — 自循环马拉松提示词(正本,随 AMENDMENTS 演化)

> 用法:在 AwareLiquid-Physic 工作区**新开一个 ZCode 会话**,整段粘贴。
> 第一行必须是 `/goal` 开头——各家 harness 都认这个前缀作为目标声明。
> 本文件由 AMENDMENTS 提案制维护;改这里的规则 = 改循环自身,走提案。

```text
/goal 按 docs/loop/GOALS.md 的 goal_queue 持续自循环迭代本项目:每轮先跑 ./scripts/goal_check 校验顶部目标——NOT-Achieved 则对该目标迭代一轮,ACHIEVED 则弹出晋升下一个,QUEUE-EMPTY 则文献/GitHub 扫描补池;直到我设定的收尾时间为止,中途不停。

迭代纪律:
- 算力闸门(硬,每轮动手前必过):实验前先冒烟实测校准预计总时长;预计 >1 小时或单命令 >25 分钟禁止本地执行——把协议+可执行产物(脚本/参数/判据)做成 PR 交付云算力/他人执行,在 PRD §19 登记云算力欠账,立即换下一方向。本机只允许:探针/分析/判读/文档/单文件小修 + 冒烟实测。
- 每次迭代:预注册判负标准先行(写进 docs/PRD.md §19)→ 做最便宜实验 → pytest 全绿 + benchmarks/audit_results.py --check 全过 → 原子提交 push 到 fork 的 wave/loop 分支。
- 收尾时间到(我指定,或默认 08:30/23:00):在 PRD §19 写收尾记录,并按 docs/loop/RSI-INDEX.md 计算当夜指数(K/E/T/D/T+/A+复合)入账 → 停止本会话。
- 上下文过长或单目标卡住超过两轮:把状态快照进 docs/loop/GOALS.md 后结束本轮;重开新会话粘贴本 prompt 即无缝续跑。
- 需要人决策的事:GOALS.md 的 state 改 BLOCKED-HUMAN 并写明问题,停止。
- 新踩的坑回写 docs/loop/PLAYBOOK.md;新工具回写 docs/loop/TOOLS.md;对循环自身的改进提案写 docs/loop/AMENDMENTS.md(不自行改本 prompt 与宪法)。

纪律以工作区 AGENTS.md 为准:只在 wave/loop 分支写;不改写历史判定行;不合并 PR;不 push master/origin;不提交 .pt;隐藏集终跑用 ./scripts/hidden_check(seed 999 已退役,998 递减)。
停止条件:队列真穷尽(附扫描 query 清单)或全部 BLOCKED-HUMAN。被中断前,确保最近一轮已原子提交。
```
