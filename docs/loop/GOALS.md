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

updated: 2026-09-24 (**轮 186:自生成后续迭代入队 DEPTH-WIDTH**——
  goal_check QUEUE-EMPTY⇒先盘后续池:**非空**=轮 185 判读行明示
  "深度×宽度交叉=DEPTH 族后续池候选 1/2"(轮 162 注记的参数量混杂:
  深度收益部分可能是参数量效应,与宽度轴交叉后可分离)⇒入队迭代
  等同行动产出重置 S1;DEPTH-WIDTH=depth{2,4}×d_model{48,96} 四单
  元 2000 步,判读=两轴主效应+交互项;非同参重跑,DEPTH 族段内第
  2 轮达 ≤2 上限之后换方向或入停车场;est 10min;25=25+ID 数数锚
  核对。下一心跳=goal_check 路由迭代 DEPTH-WIDTH)

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
- id: GNS-PROBE-2
  track: engineering
  goal: 梯度噪声尺度进度轴延长迭代——GNS-PROBE同款estimator同判据但checkpoint轴延长{0,1000,4000,10000,20000}步(轮149判读明示后续: >4k步轴未覆盖), 判读=增长趋势是否持续+batch=64是否跨过线性加速临界(完善T2/T3派发batch字段读数); 判负同轮149三值判据(失效/平坦如实登记); GNS族段内第2轮达≤2上限之后必须换方向或入停车场
  done_condition: PRD §19有"GNS-PROBE-2 判读"锚且benchmarks/physics_out_v02/gns_probe_v2/gns_probe_v2.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "GNS-PROBE-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/gns_probe_v2/gns_probe_v2.json
  status: pr-pending(PR#13, 判读GNS_RESOLVED_TREND=1k峰值后回落batch=64长训练体制重回噪声主导侧, 合并后check过自动弹出)
- id: SHARP-PROBE
  track: engineering
  goal: sharpness轨迹探针——M1弹簧同池(E1口径与GNS-PROBE同配置)checkpoint{0,200,500,1000,2000}各估训练loss的λ_max(HVP幂迭代20步双反向), 判读=λ_max·η(lr=3e-3)相对EOS阈值2位置(SHARP_EOS∈[1.5,3]/BELOW/ABOVE)+λ_max随训练走向(对照EOS悬停与warmup早期高后降两预言, scan§37), 判负=幂迭代不收敛(相邻迭代>10%)或非有限⇒本体制sharpness不可分辨; Adam修正面如实注记(判据由GD推导)
  done_condition: PRD §19有"SHARP-PROBE 判读"锚且benchmarks/physics_out_v02/sharp_probe/sharp_probe.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "SHARP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/sharp_probe/sharp_probe.json
  status: pr-pending(PR#14, 判读SHARP_BELOW=本仓训练不在EOS轮146反弹EOS解释排除, 合并后check过自动弹出)
- id: SHARP-PROBE-2
  track: engineering
  goal: sharpness进度轴延长迭代——SHARP-PROBE同款estimator同判据但checkpoint轴延长{0,1000,2000,4000,6000,8000,10000}(轮154判读明示后续: 2000步后是否逼近EOS未测), 判读=λ_max·lr是否持续远低于阈值2或出现逼近/悬停(完善训练体制定性); 判负同轮154(幂迭代不收敛>10%或非有限⇒不可分辨); sharpness族段内第2轮达≤2上限之后必须换方向或入停车场; Adam修正面注记沿用
  done_condition: PRD §19有"SHARP-PROBE-2 判读"锚且benchmarks/physics_out_v02/sharp_probe_v2/sharp_probe_v2.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "SHARP-PROBE-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/sharp_probe_v2/sharp_probe_v2.json
  status: pr-pending(PR#15, 判读SHARP_BELOW维持=训练全程10k步深度稳定区体制定性收口, 合并后check过自动弹出)
- id: REP-PROBE
  track: engineering
  goal: 窗口重复率对照探针——M1弹簧semigroup体制固定4000步预算两臂: A=默认随机窗口重复(train_semigroup原样) vs B=窗口去重(预生成互不重叠(t_i,t_j)对遍历一次), 判读=A/B rollout MSE(k100同held-out): 差<5%⇒重复无害区记录/A差≥5%⇒重复有害/A好≥5%⇒重复有益(scan§38 value decay框架), 判负=两臂差<5%⇒本体制重复率不可分辨如实登记(38.3观测口径限制注记); 族边界=数据重复轴REP族第1轮与§8.4/§35/§30分立
  done_condition: PRD §19有"REP-PROBE 判读"锚且benchmarks/physics_out_v02/rep_probe/rep_probe.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "REP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/rep_probe/rep_probe.json
  status: pr-pending(PR#16, 判读REP_UNRESOLVABLE=窗口重复率rollout口径不可分辨判负分支执行, 合并后check过自动弹出)
- id: SPECTRAL-DT
  track: engineering
  goal: 谱偏置×离散化交叉双因子矩阵探针——单频弹簧池ω∈{1,2,4}×训练dt∈{0.05,0.1,0.2}九单元短训(prefix hidden64 2000步)固定物理视距T=10(k=200/100/50归一)rollout MSE, 判读=交叉交互: 高频ω=4粗dtvs细dt误差增幅超低频同比值≥20%⇒交互可分辨(scan§39; ω·dt∈0.05-0.8逐单元Nyquist状态注记防aliasing/学不到混淆), 判负=交互差<20%⇒不可分辨如实登记或矩阵单元失效; 族边界=频率×网格交叉轴SPECTRAL-DT族第1轮(Rahaman已在§17.1不重复收)
  done_condition: PRD §19有"SPECTRAL-DT 判读"锚且benchmarks/physics_out_v02/spectral_dt/spectral_dt.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "SPECTRAL-DT 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/spectral_dt/spectral_dt.json
  status: pr-pending(PR#17, 判读INTERACTION_RESOLVED=高频粗dt超比例恶化+2410%训练网格解析度条款入N1, 合并后check过自动弹出)
- id: DT-CURRICULUM
  track: engineering
  goal: dt分辨率课程对照探针——单频弹簧池ω=2(轮162中频单元)2000步预算两臂: A=恒定dt=0.05 vs B=dt课程(0.1×1000步→0.05×1000步权重连续), 判读=A/B rollout MSE(k=200 T=10同口径)三分支: 差<5%⇒课程不可分辨(与Wu 2021随机序强基线相容如实记录)/B好≥5%⇒受限预算下课程有益(文献方向一致)/B差≥5%⇒课程有害如实登记(scan§40), 判负=两臂差<5%⇒本体制dt课程不可分辨或臂发散; 族边界=分辨率排序轴DT-CURRICULUM族第1轮与§8.4采样课程/D1f训练循环课程/§39静态矩阵三分
  done_condition: PRD §19有"DT-CURRICULUM 判读"锚且benchmarks/physics_out_v02/dt_curriculum/dt_curriculum.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "DT-CURRICULUM 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/dt_curriculum/dt_curriculum.json
  status: pr-pending(PR#18, 判读CURRICULUM_BENEFICIAL=受限预算下dt课程有益33.8%组合收益, 合并后check过自动弹出)
- id: DT-CURRICULUM-2
  track: engineering
  goal: 课程机制分离迭代——逆课程对照: 同池同预算2000步 A=正课程(0.1×1000→0.05×1000, 轮165同配置) vs B=逆课程(0.05×1000→0.1×1000), 判读=A/B rollout MSE(k=200 T=10): A好≥5%⇒顺序为因(课程语义成立=粗阶段低频结构初始化细阶段)/A≈B(<5%)⇒物理覆盖假说(轮162反向纹理同源)/B好≥5%⇒逆课程更优如实登记; 判负=任一臂发散或diff边界情形不可判; 课程族段内第2轮达≤2上限之后必须换方向或入停车场; Adam状态不继承注记沿用
  done_condition: PRD §19有"DT-CURRICULUM-2 判读"锚且benchmarks/physics_out_v02/dt_curriculum_v2/dt_curriculum_v2.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "DT-CURRICULUM-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/dt_curriculum_v2/dt_curriculum_v2.json
  status: pr-pending(PR#19, 判读ORDER_MATTERS=顺序为因正课程0.4225vs逆课程5.9056覆盖假说被否, 合并后check过自动弹出)
- id: LEN-EXTRAP
  track: engineering
  goal: 训练窗外rollout外推探针——异频池(E1口径)prefix hidden64 2000步训练(160步轨迹=16s物理窗全仓默认), 评估新池gen601步(60s)held-out双轴: 内插段per-step误差(T∈5-10s窗内)vs外推段(T∈20-30s窗外4-14×), comp=外推/内插per-step MSE比三分支: comp<3⇒LEN_ROBUST平缓外推/≥3且16s边界后首窗跳变≥3×⇒LEN_WINDOW_EDGE窗口边界效应(IMDE修正项失效, scan§41)/≥3无边界跳变⇒LEN_GRADUAL渐进累积; 附能量漂移诊断; 判负=评估生成/滚动非有限发散>1e6或comp数值异常; 族边界=物理时长轴LEN-EXTRAP族第1轮与§18.1口径/§31网格/§40排序分立
  done_condition: PRD §19有"LEN-EXTRAP 判读"锚且benchmarks/physics_out_v02/len_extrap/len_extrap.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "LEN-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/len_extrap/len_extrap.json
  status: pr-pending(PR#20, 判读LEN_ROBUST=训练窗外1.25-1.875×平缓延续无边界效应comp=0.88, 合并后check过自动弹出)
- id: LEN-EXTRAP-2
  track: engineering
  goal: 长度外推稳健域延长迭代——同estimator但相对化口径+更长池: per-step MSE除以各时刻信号能量(相对误差剖面, 剥离信号量级演化混杂) + 新池gen1001步(100s)外推段[40,60]s(窗外4-6×)与[80,100]s(8-10×), 判读=相对comp三分支同轮170门(<3 ROBUST/≥3边界跳变WINDOW_EDGE/≥3渐进GRADUAL)+外推倍数延长下稳健域边界定位; 判负=发散或相对化数值异常; 族边界=物理时长轴LEN族第2轮达≤2上限之后换方向或入停车场
  done_condition: PRD §19有"LEN-EXTRAP-2 判读"锚且benchmarks/physics_out_v02/len_extrap_v2/len_extrap_v2.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "LEN-EXTRAP-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/len_extrap_v2/len_extrap_v2.json
  status: pr-pending(PR#21, 判读LEN_ROBUST维持=相对化与绝对一致守恒体系无增量区分度稳健域延伸至窗外8-10×, 合并后check过自动弹出)
- id: POOL-WIDTH
  track: engineering
  goal: 池分布宽度对照探针——M1弹簧2000步prefix两臂: A=窄池ω∈[0.95,1.05](近单频) vs B=宽池ω∈[0.7,1.8](E1默认), 各评估同分布held-out(k100 T=10), 判读=B/A rollout MSE比三分支: ∈[0.95,1.05]⇒宽度不可分辨(Kumar反直觉相容)/ >1.05⇒宽度有代价(§42.3宽池精度下降) / <0.95⇒宽度有收益(传统多样性增益), 判负=口径失效非有限发散; ω·dt网格两臂同; 族边界=训练分布宽度轴POOL-WIDTH族第1轮与§20.2成员多样性/§29后验/§39网格交互分立
  done_condition: PRD §19有"POOL-WIDTH 判读"锚且benchmarks/physics_out_v02/pool_width/pool_width.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "POOL-WIDTH 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/pool_width/pool_width.json
  status: pr-pending(PR#22, 判读WIDTH_COST=池宽度巨大同分布精度代价ratio=37.5口径拆解跨池数字不可比, 合并后check过自动弹出)
- id: OPT-COMPARE
  track: engineering
  goal: 优化器对照探针——异频池(E1口径)prefix hidden64 2000步两臂: A=Adam lr=3e-3(默认) vs B=SGD momentum=0.9 lr=0.1(常用值), 判读=A/B rollout MSE(k100同held-out)三分支: 差<5%⇒优化器不可分辨(§43.3无单胜者相容)/Adam好≥5%⇒自适应有增益(§43.2病态几何方向)/SGD好≥5%⇒自适应泛化代价(§43.1经典方向), 判负=任一臂loss非有限或rollout发散>1e6⇒OPT_UNRESOLVABLE(lr预算未调平受限对照局限如实登记); 族边界=优化器选择轴OPT族第1轮与§36梯度噪声分立
  done_condition: PRD §19有"OPT-COMPARE 判读"锚且benchmarks/physics_out_v02/opt_compare/opt_compare.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "OPT-COMPARE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/opt_compare/opt_compare.json
  status: pr-pending(PR#23待建-网络断连推送欠账, 判读OPT_SGD_BETTER=SGD-m泛化好8.6%Adam训练优势不传递, dir/opt-compare 6580473+5080a07已推)
- id: WD-LADDER
  track: engineering
  goal: weight decay阶梯对照探针——异频池(E1口径)prefix hidden64 2000步三臂: Adam weight_decay∈{0默认,1e-4,1e-2}, 判读=三臂rollout MSE(k100同held-out)spread(max/min): <1.05⇒WD_UNRESOLVABLE强度不可分辨(§44.3增强已够相容)/≥1.05⇒报告最优wd与方向(单调有益/有害/中间最优点), 判负=任一臂发散非有限或spread数值异常; 族边界=正则化强度轴WD族第1轮与§35.2 grokking机制语境/§43.1 AdamW注记分立
  done_condition: PRD §19有"WD-LADDER 判读"锚且benchmarks/physics_out_v02/wd_ladder/wd_ladder.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "WD-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/wd_ladder/wd_ladder.json
  status: pr-pending(PR#24, 判读WD_RESOLVED=强度可分辨最优wd=1e-4内点默认wd=0差17.6%, 合并后check过自动弹出)
- id: DEPTH-LADDER
  track: engineering
  goal: 深度阶梯对照探针——异频池(E1口径)prefix hidden64 2000步三臂: depth∈{1,2,4}(hidden固定参数量随深度近线性增), 判读=三臂rollout MSE(k100同held-out)spread(max/min): <1.05⇒DEPTH_UNRESOLVABLE深度不可分辨(depth=2默认充分)/≥1.05⇒报告最优depth与方向(深度有益/有害/内点), 判负=任一臂发散非有限或spread数值异常; 族边界=深度轴DEPTH族第1轮与§39.1宽度标度/§42池宽度分立
  done_condition: PRD §19有"DEPTH-LADDER 判读"锚且benchmarks/physics_out_v02/depth_ladder/depth_ladder.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "DEPTH-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/depth_ladder/depth_ladder.json
  status: pr-pending(PR#25, 判读DEPTH_RESOLVED=深度单调有益末端最优depth=4默认非最优, 合并后check过自动弹出)
- id: DEPTH-WIDTH
  track: engineering
  goal: 深度×宽度交叉矩阵探针——轮185判读行明示后续: depth∈{2,4}×d_model∈{48,96}四单元2000步prefix(hidden固定), 判读=两轴效应分离(主效应depth/width+交互项: 交互超比例⇒深度收益依赖宽度或反之)与轮162 M1-CAP-AXIS宽度轴数字对表, 判负=任一单元发散非有限或交互不可分辨如实登记; DEPTH族段内第2轮达≤2上限之后换方向或入停车场
  done_condition: PRD §19有"DEPTH-WIDTH 判读"锚且benchmarks/physics_out_v02/depth_width/depth_width.json产物存在, 判负标准执行前预注册
  check_cmd: grep -q "DEPTH-WIDTH 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/depth_width/depth_width.json
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
