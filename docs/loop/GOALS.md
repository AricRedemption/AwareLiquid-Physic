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
  **v5.0 T1 探针环已生效(AMM-024,2026-09-22 用户裁定)**:心跳单元=
  T1 可行动目标(预注册判负 → probe_run T1 ≤30min → 当轮判读 →
  dir/<slug> PR 提交即终点);超 T1 方向入 AMM-024 停车场(T3-MENU:
  N1 v1+/T2/T3 候选/Kaggle 派发线/隐藏卷,停放待用户重启)。下一心跳:
  队列空 ⇒ 蒸馏轮收方向(只收 T1 可行动),或按 goal_check 裁决。
blocked_on: >-
  1) PR 合入=用户线下处理,非循环阻塞;2) 停车场重启(N1 v1+/T2/T3/
  Kaggle 派发/隐藏卷)均待用户指令;3) Kaggle 凭证=停车场激活材料,
  不阻塞 v5 循环。
next_trigger_hint: goal_check → 队首双 PR(PR#1/#2)待合并则跳过 ⇒ 迭代 NBODY-POOL-AUDIT(dir/<slug>:预注册→probe_run→当轮判读→PR)/ 用户指令 / 停车场重启
pointer: docs/PRD.md §19(判读报告落点);docs/loop/DEBT-LEDGER.md(欠账
  台账,清欠顺序与指标);docs/loop/AMENDMENTS.md(AMM-007/008/009);
  docs/scan-conditioning.md §8-22(文献坐标;轮 61/63/65/73/75/77/79/81/83/85/87
  蒸馏);docs/dh-dissipation-design.md(轮 74);docs/koopman-bridge.md(轮 76);
  docs/spectral-bias-naming.md(轮 78);docs/eval-norms-vpt.md(轮 80);
  docs/tsfm-baseline-protocol.md(轮 82);docs/uq-audit.md(轮 84);
  docs/structure-injection-vs-discovery.md(轮 86);docs/grad-path-audit.md(轮 93);
  docs/scan-traceability-audit.md(轮 94 溯源审计)

updated: 2026-09-24 04:20 (**整体验收轮(轮 119)+状态机正式化**:用户
  验收基准="只贴一个 Goal prompt,结合本机 RSI 体系迭代"——逐条对表结果:
  ①启动/路由/双门/原子提交/快照续跑全链实证过(轮 110-118);②状态机缺口
  已补=队列 status 字段+goal_check 状态驱动跳过(pr-pending 永不迭代)+gauge
  WIP 修正,恢复机械化了(AMM-026 PROPOSED);③RSI 断喂已修=夜 7/8/9 补账
  (0.35/0.33/0.27)——**S3 字面武装(连续 3 夜<0.5),待用户裁定口径修订或
  停车场重启**;④WIP 假报警已消。当前路由=MINING-FROZEN(EXP=0.1)⇒下一
  心跳=证据轮(T1 探针);150 测试+audit 绿;提交=f45d1b8 后续)

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
- id: M1-CAP-AXIS
  track: frontier
  goal: M1容量轴探针——d_model∈{24,48,96}×n32同池同预算(2000步,seed0,prefix/all2all双臂), E3容量否定的M1侧对照, 判读=liquid edge随容量走向
  done_condition: PRD §19有"M1-CAP-AXIS 判读"锚且benchmarks/physics_out_v02/m1_cap_axis/m1_cap_axis.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "M1-CAP-AXIS 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/m1_cap_axis/m1_cap_axis.json
  status: pr-pending(PR#1)
- id: OMEGA-EXTRAP
  track: frontier
  goal: ω带外外推探针——M1于ω∈[0.7,1.8]训练(2000步,seed0), 带内anchor+带外[0.3,0.6]/[1.9,2.2]评估k100 MSE与ctx线性解码, liquid/static双臂(结构约束是否缓解带外退化)
  done_condition: PRD §19有"OMEGA-EXTRAP 判读"锚且benchmarks/physics_out_v02/omega_extrap/omega_extrap.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "OMEGA-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/omega_extrap/omega_extrap.json
  status: pr-pending(PR#2)
- id: NBODY-POOL-AUDIT
  track: engineering
  goal: NBody聚合语义审计——闭合轮95恒等式声明边界(代码审计model.py粒子池化聚合语义+ctx信息Fisher式探针移植, 判读=信息保留率, 文献预期无M2型湮灭scan§28.3)
  done_condition: PRD §19有"NBODY-POOL-AUDIT 判读"锚且benchmarks/physics_out_v02/nbody_pool_audit/nbody_pool_audit.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "NBODY-POOL-AUDIT 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/nbody_pool_audit/nbody_pool_audit.json
  status: pr-pending(PR#3)
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空 ⇒ 按 goal_check 路由(蒸馏/证据轮/清欠,以路由器裁决为准)。
**在途 PR 注记(备份说明,AMM-026 起非承载)**:任务级恢复已由队列
`status: pr-pending` 字段机械承载(goal_check 状态驱动跳过/弹出,回归
测试在位)——本注记仅作人类可读备份:PR#1=M1-CAP-AXIS、PR#2=OMEGA-
EXTRAP、PR#3=NBODY-POOL-AUDIT,均判读 PASS 待合并,合并后自动弹出。
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
