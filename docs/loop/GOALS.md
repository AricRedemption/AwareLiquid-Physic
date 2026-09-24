# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE(轮 141 用户质询重入,见 updated)
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
next_trigger_hint: goal_check → 十条全 pr-pending(PR#1-#10)机械跳过 ⇒ QUEUE-EMPTY 仪表路由(判读轮后消化轮优先:回填 N1 时标条款量化升级/分流/条件重入口,禁新蒸馏;后续池=慢轴到门预算归因属停车场 T2/T3 待用户重启,无 T1 可迭代点)/ 用户指令 / 停车场重启
pointer: docs/PRD.md §19(判读报告落点);docs/loop/DEBT-LEDGER.md(欠账
  台账,清欠顺序与指标);docs/loop/AMENDMENTS.md(AMM-007/008/009);
  docs/scan-conditioning.md §8-22(文献坐标;轮 61/63/65/73/75/77/79/81/83/85/87
  蒸馏);docs/dh-dissipation-design.md(轮 74);docs/koopman-bridge.md(轮 76);
  docs/spectral-bias-naming.md(轮 78);docs/eval-norms-vpt.md(轮 80);
  docs/tsfm-baseline-protocol.md(轮 82);docs/uq-audit.md(轮 84);
  docs/structure-injection-vs-discovery.md(轮 86);docs/grad-path-audit.md(轮 93);
  docs/scan-traceability-audit.md(轮 94 溯源审计)

updated: 2026-09-24 (**轮 149:GNS-PROBE 判读 GNS_RESOLVED_TREND,dir/
  gns-probe PR#12 即终点**——goal_check NOT-Achieved⇒T1 探针环心跳;
  预注册先于执行钉死(M1 弹簧同池 hidden64 prefix 循环 batch=64,
  3 个训练进度 checkpoint×N=32 子批梯度,一阶估计 B_simple,机械
  三值判据);实跑 ~3min≤est8(轮 146 同循环实测标度=跨循环教训的
  正确应用):B_simple 0 步=11.89→1000 步=83.11→4000 步=60.39
  (max/min=6.99≥3⇒growing,与 McCandlish 预言方向一致);量级定位
  如实拆解=早期噪声主导区/训练后 **batch=64 恰在线性加速临界附近**;
  对轮 126 噪声侧读数=早期 B_noise≪64⇒种子噪声实现可导向不同解
  盆地,与符号反转观察一致(一致性支持非因果,1-seed 筛查);判负
  未触发;**格式化器第五袭(同轮 146 变体:缩进重排+GNS-PROBE 整条
  被删)checkout HEAD 还原,12=12+12 ID 核对**;160 测试(157+3)
  +audit 全绿;队列十二条全 pr-pending。下一心跳=goal_check 裁决——
  判读轮后消化轮优先(回填资产索引 GNS 条目/分流/条件重入口,禁新
  蒸馏))

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
- id: R1D-MODE-SCAN
  track: frontier
  goal: R1d逐ctx模式提取质量扫描——SB-NAMING可证伪预言检验(scan§17.3+轮78预言: 提取质量随模式序数单调变差=谱偏置命名, 平坦=判负⇒命名降级+第四路删除; 复用--oracle_ctx三臂框架逐模式分解, T1筛查级1-seed, 注册的3-seed终局协议维持停车场)
  done_condition: PRD §19有"R1D-MODE-SCAN 判读"锚且benchmarks/physics_out_v02/r1d_mode_scan/r1d_mode_scan.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "R1D-MODE-SCAN 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/r1d_mode_scan/r1d_mode_scan.json
  status: pr-pending(PR#4, 判读NEGATIVE=判负分支已执行, 合并后check过自动弹出)
- id: SIGN-FLIP-PROBE
  track: engineering
  goal: 半群符号反转异常定位——轮113记录开放问题(符号反转1/3全容量点恒定)的机制探针: 跨seed扫描追踪符号统计与稳定性(3-seed T1诊断级, 多seed终局维持停车场), 与sign-symmetry盆地机制对账(scan§30.3: tanh奇激活符号对称盆地=机制性不同解)
  done_condition: PRD §19有"SIGN-FLIP-PROBE 判读"锚且benchmarks/physics_out_v02/sign_flip_probe/sign_flip_probe.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "SIGN-FLIP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/sign_flip_probe/sign_flip_probe.json
  status: pr-pending(PR#5, 判读TRANSIENT+异质纹理如实: 盆地稳定占多数, 合并后check过自动弹出)
- id: MAP-VS-FLOW
  track: engineering
  goal: 学习对象dt迁移探针——M1头在dt=0.1训练后于dt∈{0.05,0.1,0.2}评估1-step局部误差与k100 MSE(scan§31: 学到H向量场则跨dt一致O(dt²), 学到dt映射则O(1)崩塌; N1"学到H(q,p)"声明的范围限定检验, verdict=FLOW_LIKE/MAP_LIKE机械二值, 判负=跨dt崩塌⇒N1措辞降级为映射对象)
  done_condition: PRD §19有"MAP-VS-FLOW 判读"锚且benchmarks/physics_out_v02/map_vs_flow/map_vs_flow.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "MAP-VS-FLOW 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/map_vs_flow/map_vs_flow.json
  status: pr-pending(PR#6, 判读FLOW_LIKE=跨dt迁移获支持, 合并后check过自动弹出)
- id: ICL-M3
  track: engineering
  goal: 少样本适配三臂对照——M3 wave族同任务(c=1.5未见)上前缀摊销(liquid标准) vs 梯度微调(pretrain+finetune, M3臂) vs 从头n-shot(M3对照)三臂T1对照(scan§32.3 GrBAL/ReBAL对照语言: 梯度式vs隐式适配; 判读=三臂k100 MSE排序与少样本增益方向, N1迁移线定位)
  done_condition: PRD §19有"ICL-M3 判读"锚且benchmarks/physics_out_v02/icl_m3/icl_m3.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "ICL-M3 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/icl_m3/icl_m3.json
  status: pr-pending(PR#7, 判读=判负①②未触发三臂排序B<C<A交付, 合并后check过自动弹出)
- id: ICL-M3-INTERP
  track: engineering
  goal: 少样本适配内插对照——ICL-M3三臂原样但c_target=1.1(语料{0.8,1.0,1.2}内=内插任务, 剥离轮132判读的外插混杂: 隐式ICL与梯度适配差距中适配能力与OOD外插各占多少, 内插版A臂应显著改善若仍落后则适配能力为真因)
  done_condition: PRD §19有"ICL-M3-INTERP 判读"锚且benchmarks/physics_out_v02/icl_m3_interp/icl_m3_interp.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "ICL-M3-INTERP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/icl_m3_interp/icl_m3_interp.json
  status: pr-pending(PR#8, 判读=判负①外插为主因触发, 合并后check过自动弹出)
- id: FASTSLOW-PROBE
  track: frontier
  goal: 弹性摆快慢双时标探针——probe-local弹性摆族(dim=2可分H: 快弹簧模态ω_s+慢摆动模态ω_p, VV真值), 头在解析dt训练后测快模态捕捉与长视距T≫1/ω_p慢交换保持(scan§33: 时标上限=架构×dt联合性质, 失效模式=刚性签名; 判读=双时标同时捕捉与否+失效模式分类, N1时标条款路由)
  done_condition: PRD §19有"FASTSLOW-PROBE 判读"锚且benchmarks/physics_out_v02/fastslow_probe/fastslow_probe.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "FASTSLOW-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/fastslow_probe/fastslow_probe.json
  status: pr-pending(PR#9, 判读BOTH_FAILED=双时标捕捉失败量化边界交付, 合并后check过自动弹出)
- id: FASTSLOW-2
  track: frontier
  goal: 双时标失败归因探针——FASTSLOW-PROBE(BOTH_FAILED)的容量/训练量归因: hidden128+40000步(4×容量与预算)下BOTH_FAILED是否逆转, 逆转=优化限制(加大即愈), 不变=数据/时标结构限制(§33.2刚性签名, N1时标条款措辞升级为结构性); 附加轴hidden64同预算对照(分离容量与步数贡献)
  done_condition: PRD §19有"FASTSLOW-2 判读"锚且benchmarks/physics_out_v02/fastslow_probe_v2/fastslow_probe_v2.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "FASTSLOW-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/fastslow_probe_v2/fastslow_probe_v2.json
  status: pr-pending(PR#10, 判读BUDGET_DOMINANT=步数为因逆转优化限制非结构限制, 合并后check过自动弹出)
- id: GROK-CURVE
  track: engineering
  goal: 训练量-泛化函数形状探针——M1弹簧held-out族hidden64步数阶梯{2500,5000,10000,20000,40000}逐点k100 rollout rel MSE曲线(log-log), 判读=平滑渐近(轮143 BUDGET_DOMINANT单模式拟合叙事)vs 突变转折(grokking型延迟泛化, §35 Davies双速度统一); 判负=曲线平滑无突变⇒grokking命名不适用本仓训练体制只留渐近记录(scan§35; 载体=泛化动力学轴grokking族第1轮, 非fastslow载体段内预算不动; 1-seed筛查多seed终局=停车场)
  done_condition: PRD §19有"GROK-CURVE 判读"锚且benchmarks/physics_out_v02/grok_curve/grok_curve.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "GROK-CURVE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/grok_curve/grok_curve.json
  status: pr-pending(PR#11, 判读SMOOTH_ASYMPTOTE=判负分支执行grokking命名不适用本仓, 合并后check过自动弹出)
- id: GNS-PROBE
  track: engineering
  goal: 梯度噪声尺度闭式估计探针——M1弹簧同池hidden64三个训练进度checkpoint(0/1000/4000步短训)各采N=32个batch-64随机子批梯度, B_simple谱+跨进度趋势(对照McCandlish"B_noise随训练增长"预言, scan§36), 判读=batch=64相对B_noise位置(噪声主导区/线性加速区)+为轮126种子敏感性提供优化噪声读数; 判负=B_simple全失效或无可分辨结构⇒本仓体制GNS不可分辨(batch阶梯对照转停车场登记)
  done_condition: PRD §19有"GNS-PROBE 判读"锚且benchmarks/physics_out_v02/gns_probe/gns_probe.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "GNS-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/gns_probe/gns_probe.json
  status: pr-pending(PR#12, 判读GNS_RESOLVED_TREND=梯度噪声尺度增长~7×判负未触发, 合并后check过自动弹出)
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空 ⇒ 按 goal_check 路由(蒸馏/证据轮/清欠,以路由器裁决为准)。
**在途 PR 注记(备份说明,AMM-026 起非承载)**:任务级恢复已由队列
`status: pr-pending` 字段机械承载(goal_check 状态驱动跳过/弹出,回归
测试在位)——本注记仅作人类可读备份:PR#1=M1-CAP-AXIS、PR#2=OMEGA-
EXTRAP、PR#3=NBODY-POOL-AUDIT,均判读 PASS 待合并,合并后自动弹出。
**条件性重入口(唯一源=scan §12.3 四路分流表;此处只存状态,不复制逻辑)**:
E2 已失效(轮 90:R1 判负 ⇒ 推断侧方向关闭);R1b 分支前提不满足 ⇒
轮 95 裁决不触发,维持条件性登记(轮 120 门#2 [B] 实证属架构层证据,
非修复路线触发);R1c 已闭环(R1C-AGG 轮 96 判负,入 P3 四路全负链);
R1d 已撤回(轮 122 R1D-MODE-SCAN 判读 NEGATIVE,轮 78 预注册判负分支
机械执行:谱偏置命名降级弱假设留档+第四路删除;判读在 PR#4,合并后
以 PRD §19 为准)。§12.3 分流表现存三路(R1/R1b/R1c)全部终态,
条件重入口清零。AMM-021 等效清点:B1 路由行为不变/B2 候选裁决时机
已消费(轮 121 入队→轮 122 判读)/B3 E2 失效判定保留/B4 R1d 先决
已消费。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
