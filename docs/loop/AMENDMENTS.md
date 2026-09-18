# LOOP AMENDMENTS — 循环自改进提案(人工闸门)

> RSI 落地形式:**循环可以提案修改自己的操作程序(cron 提示词/本目录下的
> 惯例),但应用必须经 AricRedemption 批准**。这是 DGM/AlphaEvolve 的
> "经验验证 + 选择"原则在治理层的对应物——提案留存、人工选择。

## 提案格式

```
### AMM-<编号>: <一句话>
- 动机:(哪个坑/哪次低效触发)
- 提案 diff:(改 cron 提示词/PLAYBOOK 惯例节的哪一句,原文→新文)
- 风险与回滚:(可能破坏什么;如何一键回退)
- 状态:PROPOSED / APPROVED / REJECTED / APPLIED
```

## 规则

1. 循环每轮可追加 PROPOSED 提案,但**不得**自行修改 cron 提示词;
2. AricRedemption 批准后,由用户或下一轮循环应用并改状态为 APPLIED,
   同时在当夜收尾记录留痕;
3. 被拒绝的提案保留原文(REJECTED),不删除——提案史也是研究记录。

## 提案列表

### AMM-001: cron 提示词瘦身为哑触发器,智能迁入 GOALS.md 程序计数器
- 动机:循环规程作为静态大块存在 cron 提示词里,已三次 CronUpdate 迭代,
  越长越锈(提示词被当数据库用);且人开的会话拿不到循环规程。
- 提案 diff:① 新增工作区 `AGENTS.md` 宪法(每个会话自动加载:入口规则、
  铁律、度量指针);② 新增 `docs/loop/GOALS.md` 程序计数器(state/
  current_goal/current_action/done_condition,ACE 式演化状态);③ cron
  提示词缩为"夜间心跳:按 AGENTS.md 与 GOALS.md 执行 current_action,
  推进并原子提交;08:30 收尾轮按 RSI-INDEX 计算指数"。
- 风险与回滚:cron 会话若不自动加载 AGENTS.md 则丢失规程——回滚 = 恢复
  本文件历史版本中的完整提示词(git 可溯);GOALS.md 与 PRD §19 职责
  重叠部分以"元状态 vs 研究记录"划分,不复制真相。
- 状态:**APPLIED**(2026-09-18,AricRedemption 当日明确要求重构 goal
  prompt 为目标驱动循环,视为批准;本轮实施)
