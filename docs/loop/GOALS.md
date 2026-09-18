# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE
current_goal: >-
  把"起点失配"机制研究打包为可评审成果(N1 论文),
  同时保持隐藏集纪律(seed 999 已退役;后续 998 递减)。
current_action: >-
  N1 写作深化:扩写 docs/d1-start-state-mismatch.md 的 Related Work 全文
  (MBRL 分布漂移 / HNN / PINN 两相训练 / CfC 四段已有定位稿),
  并把 D2 表格数字转为正文表 1。完成条件:骨架文档四节全非占位,
  含主图引用与产物索引,pytest/audit 不涉及(纯文档)。
done_condition: >-
  骨架文档无 TODO 占位;引用的每个数字可溯源到 physics_out_v02 产物或
  PRD §19;主图 docs/assets/d1g-profile-panel.png 已被正文引用。
blocked_on: null          # 例: D4 需用户裁定算力通道
next_trigger_hint: cron 30min 心跳 / 用户"继续" / SessionStart
pointer: docs/PRD.md §19(第 43 轮起为第三夜记录)
updated: 2026-09-18 23:58 (wave/loop @ 0385c1a 之后)
```

## 状态机

- `RUNNING`:按 current_action 执行(夜间心跳或用户驱动均可)。
- `BLOCKED-HUMAN`:current_action 需要用户裁定(如 D4 GPU、PR 合入),
  此时空转触发只确认状态不改内容。
- `IDLE`:白昼/无动作,仅等待触发。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
