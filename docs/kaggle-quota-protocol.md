# Kaggle 配额感知训练调度协议(AMM-023;轮 108)

> 用户指令(2026-09-22):"kaggle的训练应该通过api去获取余量去决定训练
> 内容 训练多少"。本协议把这条指令固化为可执行机制;**数值阈值唯一活
> 在 `scripts/kaggle_quota_check.py` 的 TIERS 常量**(通用规则原则,本文
> 只描述档位语义不复述数值)。

## 1. 机制链

```
kaggle_quota_check.py(读余量,结构化失败码)
  → status=ok 才允许查档位(tier_for)
  → 档位 ∩ T3 候选菜单 → 本心跳派发决定
  → 派发仍走 AMM-003/005/008/010 全套纪律(dir/<slug> 分支 + PR 交付
    + Probe-First + DEBT-LEDGER C-debt 登记 + 结果回传 _results/)
```

## 2. 读数语义(诚实边界)

- Kaggle 稳定公开 API(api/v1)**没有配额端点**;工具 best-effort 读
  UI 同款会话端点(非官方,可能变更)。**只有 `status:"ok"` 的读数
  可以驱动派发**;任何失败码(NO_CREDS/DEP_MISSING/READ_FAILED/
  NO_READ)= 本心跳不派发,如实入档。
- 凭证 `~/.kaggle/kaggle.json` 由用户提供(材料供给,非决策);工具
  对凭证只读。

## 3. 档位语义(数值见工具 TIERS)

| tier | 语义 | 允许动作 |
|---|---|---|
| `NO_READ` | 读数失败/无凭证 | **禁止派发**,只登记失败码 |
| `PROBE_ONLY` | 余量很小 | 仅允许 Kaggle 侧冒烟(管线校验/环境验证),不跑任何训练 |
| `SHORT_RUN` | 小余量 | 派发一个预注册 T3 候选的短档(单 seed/小规模) |
| `FULL_RUN` | 中余量 | 派发一个预注册 T3 候选的全档(多 seed 终局) |
| `MULTI_RUN` | 大余量 | 可排队多个候选,周预算内错峰 |

- **预计时长 > 当前余量 ⇒ 自动降档或不派发**(派发前核对候选的
  预注册时长估计与读数,宁小勿爆)。
- 候选菜单 = PRD future work / DEBT-LEDGER 中的 T3 候选(如 SSM 对照
  基线、多 seed 终局、噪声注入线);**每笔派发前该候选的具体 run 规格需
  预注册入 PRD**(判负标准先行),没有预注册规格的候选不派发。

## 4. 派发与回传闭环

1. 派发心跳:读数 ok → 选候选 → PRD 预注册 → 开 dir/<slug> 分支 +
   Kaggle kernel/PR 交付 → DEBT-LEDGER 登记 C-debt(债龄照计);
2. 回传心跳:`_results/` 收 JSON → audit_results --check → PRD §19
   判读 → C-debt 置 closed;
3. 异常即中止:读数骤降/账号异常/配额耗尽 ⇒ 停派发护账号(护机优先
   同款);连续 2 次读数失败 ⇒ 派发线挂起,待用户检查凭证/端点。

## 5. 判负标准(预注册)

- 端点连续 2 个心跳不可读且无凭证补齐 ⇒ 派发线判负挂起(如实入档,
  不硬凑调度);
- 工具读数与 Kaggle 网页显示长期(≥3 次)矛盾 ⇒ 端点语义判失效,
  工具需修,期间禁止派发。
