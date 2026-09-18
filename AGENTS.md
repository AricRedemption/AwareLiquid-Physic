# AGENTS.md — AwareLiquid-Physic 工作区宪法

> 本文件为**前缀缓存友好设计:默认冻结**。这里只放跨会话稳定的规则与指针;
> 演化内容一律放 `docs/loop/`(GOALS.md 状态机、PLAYBOOK 坑清单、
> AMENDMENTS 提案)。修改本文件属重大变更,走 AMENDMENTS 提案并尽量少改。

物理结构写进架构的连续时序模型:liquid (LTC) 基座推断 context →
哈密顿头硬约束辛可比滚出(能量守恒由构造保证)。事实来源 `docs/PRD.md`,
原则台账 `docs/PRINCIPLES.md`,循环治理 `docs/loop/`。

## 会话入口(任何人/任何触发器)

1. 读 `docs/loop/GOALS.md`(程序计数器):按 `current_action` 继续;
   完成后把 GOALS.md 推进到下一状态,与产物一起原子提交 push。
2. 开场必读 `docs/loop/PLAYBOOK.md`(操作坑,同一坑不踩第二次)与
   `docs/loop/TOOLS.md`(工具索引,先复用后新写);新坑/新工具当场回写。
3. 研究事实只认 `docs/PRD.md` 与 `docs/PRINCIPLES.md`;循环元状态只认
   `docs/loop/GOALS.md`。不要在别处复制真相。

## 铁律(任何入口都适用)

- 分支模型(AMM-003/005):`wave/loop` = 集成线;**每个新方向自它切
  `dir/<slug>` 分支单因子迭代,毕业(判据+隐藏验证过)开 PR,合并人工**。
  `master`/`origin`/他人分支与 worktree 只读。
- 永不:改写 PRD/台账历史判定行(新证据只能新增)、合并或关闭 PR、
  push master/origin、force push、改写历史、提交 `.pt`、
  未经批准修改 cron 提示词(提案走 `docs/loop/AMENDMENTS.md`)。
- 验收门:预注册判负标准先行;pytest 全绿 + `benchmarks/audit_results.py
  --check` 全过;结果 JSON 带 `meta(git_sha,device,ts)` 溯源。
- 本机(M2 Max)只跑预计 ≤1h 任务;隐藏集(seed 999 已退役,后续 998 递减)
  一次性终跑,结论只做迁移判定。

## 度量

收尾轮按 `docs/loop/RSI-INDEX.md` 计算当夜指数入账(K/E/T/D/T+/A)。
