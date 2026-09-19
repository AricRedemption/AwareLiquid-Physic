# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE
mode: ON                  # AMM-003 迭代总开关(./scripts/iteration start|stop)
iteration_window: 全天候(00:00-24:00 永动模式,2026-09-19 用户改定;总开关 mode=ON/OFF)
current_goal: >-
  治理轮 2+对齐修正(2026-09-19 15:09,设计会话):AMM-010(T1 放宽 ≤30min
  当轮直跑 + Probe-First 大训练准入)+ AMM-011(设计/执行会话角色分离)+
  AMM-012(训练↔方向平衡:EXP≥30%/WIP≤2/消化耦合)落地;D-1 UQ 校准已
  结案判负(coverage 1.6%/0/0,过度自信方向,N1 上限 L2 坐实,判读见 PRD
  §19 "D-1 判读")。台账 D_count=3。对齐修正 5 处:DEBT-LEDGER 清偿顺序
  T1 化/TOOLS probe_run 行 T1≤30/本文件时间戳实测化/AMM-008 核数以实测
  为准(8核→4线程)/GOAL-PROMPT"算力目标一生"段 v3.1 化(该段已于 v4.0
  重写时并入"算力纪律"节,此为历史日志)。
  治理轮 3(2026-09-19 17:29,设计会话终审):AMM-013 仪表强制化落地
  (goal_check 焊入 DEBT-FIRST/MINING-FROZEN 硬出口+台账指标自动化,真实
  仓库验证路由正确);AMM-014 欠账分级提案 PROPOSED 待批(云债不阻塞循环);
  GOAL-PROMPT 终审修正 5 处(资源护栏去机型数值+80%绝对红线入文/吞吐优先
  与 AMM-012 对齐/平衡阈值收归 gauge/收尾清单补 B+EXP 计量/隐藏卷条款
  去 PR 专属措辞)。
current_action: >-
  下一心跳(执行会话):队首 **R1C-AGG**(聚合轴修复,T1 当轮直跑):按
  PRD §19 轮 95 预注册执行——① model.py 池化参数化(--pool {mean,attn},
  默认 mean 逐位等价+回归测试);② tests/test_context_pool.py;③ attn 臂
  field_eval --oracle_ctx 3 seeds 对照(mean 基线 0.020004/oracle 0.014834
  勿重跑);④ probe_run T1 护栏(实测基线 ~8min,预计 ≤15min);⑤ 判读按
  预注册判负标准(corr<0.5 或几何比>0.95 ⇒ 判负,四路全负触发 P3 终收口
  证据完备)。机制背景:聚合层均值场恒等式——c(x) 信息在 mean-pool 处
  精确湮灭(retention 8.6e-11),attn 聚合是四路处方最后一路。每轮 PRD
  §19 判读+PLAYBOOK ≥1 条回写+原子提交 push。整改面随轮消化:scan
  §9.1/§11.1/§19.3 三条 B 级题录(docs/scan-traceability-audit.md §7)。
done_condition: >-
  欠账优先:D_count=0 前心跳只清欠/验收,不扩池;恢复队列后每轮 goal_check
  路由;收口按 AMM-007 判据 S1-S4 任一满足即 state: IDLE(写收尾+RSI 入账,
  保留重入口:结果回传/用户指令/新欠账)。
blocked_on: >-
  1) D-2 依赖环境(chronos/timesfm 安装+权重下载,执行会话处置);2) D4 GPU
  去向;3) origin/master 合入顺序(PR#1 CLEAN 可合);4) N1 正式英文稿是否启动。
next_trigger_hint: goal_check → R1C-AGG / 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/loop/DEBT-LEDGER.md(欠账
  台账,清欠顺序与指标);docs/loop/AMENDMENTS.md(AMM-007/008/009);
  docs/scan-conditioning.md §8-22(文献坐标;轮 61/63/65/73/75/77/79/81/83/85/87
  蒸馏);docs/dh-dissipation-design.md(轮 74);docs/koopman-bridge.md(轮 76);
  docs/spectral-bias-naming.md(轮 78);docs/eval-norms-vpt.md(轮 80);
  docs/tsfm-baseline-protocol.md(轮 82);docs/uq-audit.md(轮 84);
  docs/structure-injection-vs-discovery.md(轮 86);docs/grad-path-audit.md(轮 93);
  docs/scan-traceability-audit.md(轮 94 溯源审计)
updated: 2026-09-20 03:40 (轮 95:**MINING-FROZEN 证据轮,R1C-AGG 裁决
  入队**——① R1b/R1c 裁决点机械执行:corr 0.058≈0 ⇒ §12.3 第一路触发,
  R1c 入队(R1b/E2/R1d 维持条件性登记);② 机制发现:**聚合层均值场
  恒等式**——周期网格 accel 空间均值恒为零 ⇒ mean-pool 后编码器输入
  与介质 c 严格无关(T_obs×N 观测坍缩为 2 标量),探针实测 c 信息保留
  8.6e-11=精确零,回溯统一解释 E1/E3/D-3 三轮"信息没进来";oracle
  缺口 −26% 仍在 ⇒ 湮灭点在观测→ctx 之间,attn 聚合=最后一路处方;
  ③ 轮 72 复验条件处置(前提未兑现,弱信号留档);④ 判负标准预注册:
  attn 判负 ⇒ 四路全负,P3 终收口证据完备;3 新测试+probe_run 级 T0
  探针,判读见 PRD §19 "轮 95 判读")
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
- id: R1C-AGG
    track: engineering
    goal: 聚合轴修复(轮 95 裁决入队,scan §12.3 第一路):model.py 池化参数化(--pool {mean,attn},默认 mean 逐位等价)+ attn 臂 E1 式对照 3 seeds vs mean 基线(轮 51 B 臂勿重跑)vs oracle(勿重跑);机制背景=聚合层均值场恒等式(c 信息精确湮灭,retention 8.6e-11,PRD §19 轮 95)
    done_condition: tests/test_context_pool.py 落地+attn 臂判读写入 PRD §19("R1C-AGG 判读"锚);判负标准已预注册(corr<0.5 或几何比>0.95 ⇒ 四路全负触发 P3 终收口证据完备)
    check_cmd: grep -q "R1C-AGG 判读" docs/PRD.md && test -f tests/test_context_pool.py
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空 ⇒ 按 goal_check 路由(蒸馏/证据轮/清欠,以路由器裁决为准)。
**条件性重入口(唯一源=scan §12.3 四路分流表;此处只存状态,不复制逻辑)**:
E2 已失效(轮 90:R1 判负 ⇒ 推断侧方向关闭);R1b/R1c 已字面触发=
**队列候选**,待队列空时按 §12.3 裁决是否入队;R1d 先决=SB-NAMING
对账成立。AMM-021 等效清点:B1 路由行为不变(本块在 yaml 外,路由器
不解析)/B2 候选裁决时机保留/B3 E2 失效判定保留/B4 R1d 先决保留。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
