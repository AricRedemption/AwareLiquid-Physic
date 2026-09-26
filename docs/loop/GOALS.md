# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE(轮 267 分工校准后恢复,见 updated)
mode: ON                  # AMM-003 迭代总开关(./scripts/iteration start|stop)
iteration_window: 全天候(00:00-24:00 永动模式,2026-09-19 用户改定;总开关 mode=ON/OFF)
current_goal: >-
  v5.2 六门体系下的 T1 探针环:队列目标逐个探针-判读-PR(细则与立法史
  唯一源=AMENDMENTS/goal_check/probe_run,本文件不复述)。
current_action: >-
  v5.2(AMM-029 方向门禁生效):六门=AMM-028 五门+方向判单门,细则
  唯一源=AMENDMENTS+goal_check 输出(每心跳必见)。轮 279 蒸馏轮
  =自生成组合确认(轮 257 先例,回灌门 2 精神):RECIPE×HEAD 2×2
  判读 COMPOSE_ABSORBED=次可加,候选头单独 1.949 全场最优,配方
  吸收头优势(PR#55;三哨兵逐位全真)=**either-or 采纳:默认替换
  选候选头单独,回灌配方与头不叠加**。下一心跳=消化轮(AMM-033
  either-or 注记回填+分流),期间禁新蒸馏;消化后 ⇒ 蒸馏轮,S1
  要求 [行动](AMM-028 门 1)。

blocked_on: >-
  1) PR 合入=用户线下;2) 停车场重启(N1 v1+/T2/T3/Kaggle/隐藏卷)
  待用户指令;3) Kaggle 凭证=激活材料不阻塞。
next_trigger_hint: goal_check ⇒ QUEUE-EMPTY ⇒ 消化轮(AMM-033 either-or 注记回填+分流,禁新蒸馏);消化后 ⇒ 蒸馏轮(新方向须声明决策耦合;配方族默认关闭;无 [行动] 则 S1 累计);用户指令 / 停车场重启 / PR 合并(合并落地触发 AMM-033 实施排程)随时重入

pointer: docs/PRD.md §19(判读落点);docs/loop/{AMENDMENTS,
  DEBT-LEDGER,PLAYBOOK,TOOLS,RSI-INDEX}.md;docs/scan-conditioning.md
  (蒸馏唯一源);docs/n1-asset-index.md(N1 素材)。
updated: 2026-09-26 (**轮 268-269:新马拉松段前两轮,齐次头线
  连续双胜**)——用户重贴 GOAL-PROMPT 重启马拉松(新段,族额度
  重置);轮 65 条款条件入口兑现:V-HOM-STAB(幅度-方向解耦稳定
  化,预注册机制细化=1-D detach 无操作/病理在方向特征不连续,先于
  执行落盘)判读 STAB_REPAIRS=方向通道置零修复训练灾难(0/3,MSE
  均值 1.957<自由 V 基线 2.548)+外推收益 3/3 兑现,REF 逐位复现
  轮 261 B 臂,PR#49;池盘点入队迭代 HOM-DEFAULT(齐次头完整构造
  vs house 默认头)判读 HOM_DEFAULT_DOMINATES=双轴 3/3 全胜(分布
  内 ratio 0.658 −34%/外推 median −49%),双哨兵逐位全真(全仓锚
  3.5582+轮 268 STAB 跨脚本锚),PR#50;**决策=解析 T+方向自由齐次
  V 列为默认 M1 替换候选**;第 54 族新段 2/2 收口;193/201 测试+
  audit 99 全绿。轮 270 消化轮=AMM-033 提案登记(锚重置计划+实施
  自决排程)+分流干净。轮 271 蒸馏轮=第 59 族入库(scan §59 三槽)
  +HOM-BOUND 判读 HOM_BOUND_DEGREE_MATCHED(次数匹配齐次 V 近
  完美恢复,误设付出 7.56×,PR#51)=AMM-033 范围注记升级为次数
  匹配齐次族配方实测推广路径;202 测试+audit 99 全绿。轮 272
  消化轮=AMM-033 范围注记实测化修订(k 泛化=停车场注记)+分流
  干净。轮 273 蒸馏轮=第 60 族入库(scan §60 三槽)+HOM-DRIFT
  判读 HOM_DRIFT_ROBUST(候选头全视距双轴占优,PR#52;哨兵失配
  =超越函数池比特尺寸依赖如实诊断)=AMM-033 锚集计划纳入长视距
  锚;201 测试+audit 99 全绿。轮 274 消化轮=AMM-033 锚重置计划
  增补长视距维度条款+分流干净。轮 275 蒸馏轮=第 61 族入库(scan
  §61 三槽)+POOL-BITS 判读 ANCHOR_BOTH_FRAGILE(默认头 spread
  中位 1.86/候选 1.29 稳 30% 但双过门,PR#53;variant-160 双锚
  逐位真)=AMM-033 锚计划增补多变体协议;200 测试+audit 99 全绿。
  轮 276 消化轮=AMM-033 锚计划⑤条多变体协议回填+分流干净。轮
  277 蒸馏轮=第 62 族入库(scan §62 三槽)+HOM-SAMPLE 判读
  HOM_ARM_DIVERGED=判负兑现(B s0 n128 NaN;纹理反转=候选优势是
  全数据现象,PR#54)=AMM-033 benefit-scope 保守注记;201 测试+
  audit 99 全绿。轮 278 消化轮=AMM-033 benefit-scope 保守注记
  回填+分流干净;齐次头线 T1 级六轴全测 harvested。轮 279 蒸馏
  轮=组合确认 RECIPE×HEAD 2×2 判读 COMPOSE_ABSORBED(次可加,候
  选头单独全场最优,PR#55;三哨兵逐位真)=AMM-033 either-or 采纳
  注记;199 测试+audit 99 全绿;队列五十三条全 pr-pending。


## goal_queue(顶部为当前目标)

```yaml
goal_queue:
- id: RECIPE-SYNTHESIS
  status: pr-pending(PR#44-判读RECIPE_SYNERGIC=组合收益10.7% ratio=0.893 3/3方向一致, 判读与代码在dir/recipe-synthesis分支, 合并后check过自动弹出; 决策=臂B五轴为M1默认配置候选, 回灌PR用户线下处理)
  check_cmd: grep -q "RECIPE-SYNTHESIS 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/recipe_synthesis/recipe_synthesis.json
- id: M1-CAP-AXIS
  status: pr-pending(PR#1)
  check_cmd: grep -q "M1-CAP-AXIS 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/m1_cap_axis/m1_cap_axis.json
- id: OMEGA-EXTRAP
  status: pr-pending(PR#2)
  check_cmd: grep -q "OMEGA-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/omega_extrap/omega_extrap.json
- id: NBODY-POOL-AUDIT
  status: pr-pending(PR#3)
  check_cmd: grep -q "NBODY-POOL-AUDIT 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/nbody_pool_audit/nbody_pool_audit.json
- id: R1D-MODE-SCAN
  status: pr-pending(PR#4, 判读NEGATIVE=判负分支已执行, 合并后check过自动弹出)
  check_cmd: grep -q "R1D-MODE-SCAN 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/r1d_mode_scan/r1d_mode_scan.json
- id: SIGN-FLIP-PROBE
  status: pr-pending(PR#5, 判读TRANSIENT+异质纹理如实: 盆地稳定占多数, 合并后check过自动弹出)
  check_cmd: grep -q "SIGN-FLIP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/sign_flip_probe/sign_flip_probe.json
- id: MAP-VS-FLOW
  status: pr-pending(PR#6, 判读FLOW_LIKE=跨dt迁移获支持, 合并后check过自动弹出)
  check_cmd: grep -q "MAP-VS-FLOW 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/map_vs_flow/map_vs_flow.json
- id: ICL-M3
  status: pr-pending(PR#7, 判读=判负①②未触发三臂排序B<C<A交付, 合并后check过自动弹出)
  check_cmd: grep -q "ICL-M3 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/icl_m3/icl_m3.json
- id: ICL-M3-INTERP
  status: pr-pending(PR#8, 判读=判负①外插为主因触发, 合并后check过自动弹出)
  check_cmd: grep -q "ICL-M3-INTERP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/icl_m3_interp/icl_m3_interp.json
- id: FASTSLOW-PROBE
  status: pr-pending(PR#9, 判读BOTH_FAILED=双时标捕捉失败量化边界交付, 合并后check过自动弹出)
  check_cmd: grep -q "FASTSLOW-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/fastslow_probe/fastslow_probe.json
- id: FASTSLOW-2
  status: pr-pending(PR#10, 判读BUDGET_DOMINANT=步数为因逆转优化限制非结构限制, 合并后check过自动弹出)
  check_cmd: grep -q "FASTSLOW-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/fastslow_probe_v2/fastslow_probe_v2.json
- id: GROK-CURVE
  status: pr-pending(PR#11, 判读SMOOTH_ASYMPTOTE=判负分支执行grokking命名不适用本仓, 合并后check过自动弹出)
  check_cmd: grep -q "GROK-CURVE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/grok_curve/grok_curve.json
- id: GNS-PROBE
  status: pr-pending(PR#12, 判读GNS_RESOLVED_TREND=梯度噪声尺度增长~7×判负未触发, 合并后check过自动弹出)
  check_cmd: grep -q "GNS-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/gns_probe/gns_probe.json
- id: GNS-PROBE-2
  status: pr-pending(PR#13, 判读GNS_RESOLVED_TREND=1k峰值后回落batch=64长训练体制重回噪声主导侧, 合并后check过自动弹出)
  check_cmd: grep -q "GNS-PROBE-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/gns_probe_v2/gns_probe_v2.json
- id: SHARP-PROBE
  status: pr-pending(PR#14, 判读SHARP_BELOW=本仓训练不在EOS轮146反弹EOS解释排除, 合并后check过自动弹出)
  check_cmd: grep -q "SHARP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/sharp_probe/sharp_probe.json
- id: SHARP-PROBE-2
  status: pr-pending(PR#15, 判读SHARP_BELOW维持=训练全程10k步深度稳定区体制定性收口, 合并后check过自动弹出)
  check_cmd: grep -q "SHARP-PROBE-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/sharp_probe_v2/sharp_probe_v2.json
- id: REP-PROBE
  status: pr-pending(PR#16, 判读REP_UNRESOLVABLE=窗口重复率rollout口径不可分辨判负分支执行, 合并后check过自动弹出)
  check_cmd: grep -q "REP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/rep_probe/rep_probe.json
- id: SPECTRAL-DT
  status: pr-pending(PR#17, 判读INTERACTION_RESOLVED=高频粗dt超比例恶化+2410%训练网格解析度条款入N1, 合并后check过自动弹出)
  check_cmd: grep -q "SPECTRAL-DT 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/spectral_dt/spectral_dt.json
- id: DT-CURRICULUM
  status: pr-pending(PR#18, 判读CURRICULUM_BENEFICIAL=受限预算下dt课程有益33.8%组合收益, 合并后check过自动弹出)
  check_cmd: grep -q "DT-CURRICULUM 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/dt_curriculum/dt_curriculum.json
- id: DT-CURRICULUM-2
  status: pr-pending(PR#19, 判读ORDER_MATTERS=顺序为因正课程0.4225vs逆课程5.9056覆盖假说被否, 合并后check过自动弹出)
  check_cmd: grep -q "DT-CURRICULUM-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/dt_curriculum_v2/dt_curriculum_v2.json
- id: LEN-EXTRAP
  status: pr-pending(PR#20, 判读LEN_ROBUST=训练窗外1.25-1.875×平缓延续无边界效应comp=0.88, 合并后check过自动弹出)
  check_cmd: grep -q "LEN-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/len_extrap/len_extrap.json
- id: LEN-EXTRAP-2
  status: pr-pending(PR#21, 判读LEN_ROBUST维持=相对化与绝对一致守恒体系无增量区分度稳健域延伸至窗外8-10×, 合并后check过自动弹出)
  check_cmd: grep -q "LEN-EXTRAP-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/len_extrap_v2/len_extrap_v2.json
- id: POOL-WIDTH
  status: pr-pending(PR#22, 判读WIDTH_COST=池宽度巨大同分布精度代价ratio=37.5口径拆解跨池数字不可比, 合并后check过自动弹出)
  check_cmd: grep -q "POOL-WIDTH 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/pool_width/pool_width.json
- id: OPT-COMPARE
  status: pr-pending(PR#23待建-网络断连推送欠账, 判读OPT_SGD_BETTER=SGD-m泛化好8.6%Adam训练优势不传递, dir/opt-compare 6580473+5080a07已推)
  check_cmd: grep -q "OPT-COMPARE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/opt_compare/opt_compare.json
- id: WD-LADDER
  status: pr-pending(PR#24, 判读WD_RESOLVED=强度可分辨最优wd=1e-4内点默认wd=0差17.6%, 合并后check过自动弹出)
  check_cmd: grep -q "WD-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/wd_ladder/wd_ladder.json
- id: DEPTH-LADDER
  status: pr-pending(PR#25, 判读DEPTH_RESOLVED=深度单调有益末端最优depth=4默认非最优, 合并后check过自动弹出)
  check_cmd: grep -q "DEPTH-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/depth_ladder/depth_ladder.json
- id: DEPTH-WIDTH
  status: pr-pending(PR#26, 判读MATRIX_RESOLVED=深度宽度主效应独立可加交互ln0.011, 合并后check过自动弹出)
  check_cmd: grep -q "DEPTH-WIDTH 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/depth_width/depth_width.json
- id: KSPAN-LADDER
  status: pr-pending(PR#27, 判读KSPAN_RESOLVED=跨度可分辨最优k_train=4比默认8好47%非单调如实注记, 合并后check过自动弹出)
  check_cmd: grep -q "KSPAN-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/kspan_ladder/kspan_ladder.json
- id: KSPAN-LADDER-2
  status: pr-pending(PR#28, 判读KSPAN_RESOLVED=首端补探真最优k_train=4内点确认, 合并后check过自动弹出)
  check_cmd: grep -q "KSPAN-LADDER-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/kspan_ladder_v2/kspan_ladder_v2.json
- id: NSCALES-LADDER
  status: pr-pending(PR#29, 判读NSCALES_RESOLVED=内点最优n_scales=2默认4差45.8%参数量混杂排除, 合并后check过自动弹出)
  check_cmd: grep -q "NSCALES-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/nscales_ladder/nscales_ladder.json
- id: LRDECAY-LADDER
  status: pr-pending(PR#30, 判读LRDECAY_RESOLVED=调度形状可分辨最优lr_decay=0.999内点恒定lr差17.9%, 合并后check过自动弹出)
  check_cmd: grep -q "LRDECAY-LADDER 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/lrdecay_ladder/lrdecay_ladder.json
- id: LRBATCH-GRID
  status: pr-pending(PR#31, 判读SCALING_BROKEN=两条缩放规则均打破batch×lr需联合调优, 合并后check过自动弹出)
  check_cmd: grep -q "LRBATCH-GRID 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/lrbatch_grid/lrbatch_grid.json
- id: WSA-PROBE
  status: pr-pending(PR#32, 判读SWA_HARMFUL=尾段平均有害8.0%与SWA文献相反跨盆地平均解读, 合并后check过自动弹出)
  check_cmd: grep -q "WSA-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/wsa_probe/wsa_probe.json
- id: WARMUP-PROBE
  status: pr-pending(PR#33, 判读WARMUP_BENEFICIAL=warmup有益44.2%与§37.2方向一致轮194预测张力显性化, 合并后check过自动弹出)
  check_cmd: grep -q "WARMUP-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/warmup_probe/warmup_probe.json
- id: AMP-EXTRAP
  status: pr-pending(PR#34, 判读AMPEX_DEGRADES=幅度外推退化rel_comp=4.08线性不变性未被继承, 合并后check过自动弹出)
  check_cmd: grep -q "AMP-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/amp_extrap/amp_extrap.json
- id: RESIDUAL-SPEC
  status: pr-pending(PR#35, 判读RESIDUAL_PROFILED=残差能量93.2%在高频段高频欠拟合主导诊断读数交付, 合并后check过自动弹出)
  check_cmd: grep -q "RESIDUAL-SPEC 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/residual_spec/residual_spec.json
- id: WARMUP-PROBE-2
  status: pr-pending(PR#48-判读WARMUP_3S_BENEFICIAL=比值0.8561<0.95但一致性1/3收益seed0驱动如实注记, 判读与代码在dir/warmup-probe-v2分支, 合并后check过自动弹出; 决策=warmup保留回灌配方候选依据改记组合3/3, 轮213的44.2%降格seed0抽取)
  check_cmd: grep -q "WARMUP-PROBE-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/warmup_probe_v2/warmup_probe_v2.json
- id: CTX-DIM-2
  status: pr-pending(PR#39-判读CTX2_REVERSED=ratio1.1096>1.05反转由seed2单点驱动spread_B2.72高方差轴+语义诊断ctx不承载ω, 判读与代码在dir/ctx-dim-2分支, 合并后check过自动弹出; 决策=ctx轴维持默认8, 轮226读数降格, ctx_dim=1不入回灌; 轮242误弹恢复+锚加固两轮=锚改判读头全串合并前不可能命中)
  check_cmd: grep -q "CTX-DIM-2 判读:CTX2_REVERSED" docs/PRD.md && test -f benchmarks/physics_out_v02/ctx_dim_2/ctx_dim_2.json
- id: TOSA-CTX-DECOUPLE
  status: pr-pending(PR#46-判读DEC_TRAIN_HARMFUL=ratio5.5975>1.05训练窗缩短在固定eval下5.6×恶化一致性0/3, 轮223 t8 4.5%定性=评估口径伪影+seed0抽取双层dissolution, 判读与代码在dir/tosa-decouple分支, 合并后check过自动弹出; 决策=t_obs维持默认24, t_obs=8不列回灌候选, RECIPE t_obs口径歧义条款收口)
  check_cmd: grep -q "TOSA-CTX-DECOUPLE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/tosa_decouple/tosa_decouple.json
- id: AMP-ATTR
  status: pr-pending(PR#38-判读AMPATTR_OK=归因动力学头主因载体头等变误差s2中位1.362/s4 2.838 vs ctx非不变0.417/1.224两层均O(1)+违反, 判读与代码在dir/amp-attr分支, 合并后check过自动弹出; 决策=头侧等变性参数化列停车场候选, AMPLITUDE族2/2收口)
  check_cmd: grep -q "AMP-ATTR 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/amp_attr/amp_attr.json
- id: RESIDUAL-SPEC-2
  status: pr-pending(PR#45-判读SPECTRA_INCREMENTAL=逐seed排序一致1/3+聚合同向双口径k4均优, 判读与代码在dir/residual-spec-2分支, 合并后check过自动弹出; 决策=谱指标候选house次级口径走AMM-031提案PROPOSED待用户, RESIDUAL族2/2收口; 轮252根因修订=gen_steps不改数据值真因训练t0范围)
  check_cmd: grep -q "RESIDUAL-SPEC-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/residual_spec_2/residual_spec_2.json
- id: EQUIV-HEAD
  status: pr-pending(PR#40-判读EQUIV_TRADEOFF=解析T分布内3/3全赢均值-14%但外推rel_comp中位9.07vs3.33恶化, 判读与代码在dir/equiv-head分支, 合并后check过自动弹出; 决策=解析动能spring配置候选走独立线+归因重定向V与ctx通道, 第54族段内1/2)
  check_cmd: grep -q "EQUIV-HEAD 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/equiv_head/equiv_head.json
- id: RECIPE-HORIZON
  status: pr-pending(PR#43-判读HORIZON_ROBUST=ratio0.893/0.834/0.825随视距增强逐视距3/3一致回灌scope确认, 判读与代码在dir/recipe-horizon分支, 合并后check过自动弹出; 决策=回灌PR scope确认k100-400稳健增强, 附轮246根因修订)
  check_cmd: grep -q "RECIPE-HORIZON 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/recipe_horizon/recipe_horizon.json
- id: GENLEN-PROBE
  status: pr-pending(PR#42-判读GENLEN_RESOLVED=means2.961/2.836/2.699spread1.097best450但逐seed方向混合seed0主导高方差, 判读与代码在dir/genlen-probe分支, 合并后check过自动弹出; 决策=house训练轨迹长度=配置候选带置信标回灌第7轴候选, 301臂跨脚本复现轮246)
  check_cmd: grep -q "GENLEN-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/genlen_probe/genlen_probe.json
- id: GENLEN-CONFIRM
  status: pr-pending(PR#41-判读GENLEN_CONFIRMED=出样方向2/3稳健ratio0.8738与轮255量级一致第7轴候选升级建议采纳置信中, 判读与代码在dir/genlen-confirm分支, 合并后check过自动弹出; 决策=采纳实施架构变更走独立线用户, 第56族段内2/2收口)
  check_cmd: grep -q "GENLEN-CONFIRM 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/genlen_confirm/genlen_confirm.json
- id: V-HOM
  status: pr-pending(PR#47-判读VHOM_NULL+seed1强机制信号=齐次V外推修复收益真实seed1 rel_comp1.443近完美恢复但训练不稳定瓶颈, 判读与代码在dir/v-hom分支, 合并后check过自动弹出; 决策=齐次V构造保留候选前置训练稳定性研究项T2停车场, 第54族2/2收口)
  check_cmd: grep -q "V-HOM 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/v_hom/v_hom.json
- id: V-HOM-STAB
  status: pr-pending(PR#49-判读STAB_REPAIRS=方向通道置零修复训练灾难0/3+MSE均值1.957低于自由V基线2.548+外推收益3/3兑现median1.705<3, 判读与代码在dir/v-hom-stab分支, 合并后check过自动弹出; 决策=方向自由齐次头候选提级头部构造独立线; REF哨兵逐位复现轮261 B臂, 第54族新段第1轮)
  check_cmd: grep -q "V-HOM-STAB 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/v_hom_stab/v_hom_stab.json
- id: HOM-DEFAULT
  status: pr-pending(PR#50-判读HOM_DEFAULT_DOMINATES=齐次头完整构造对house默认头双轴3/3全胜分布内ratio0.658−34%外推median−49%, 判读与代码在dir/hom-default分支, 合并后check过自动弹出; 决策=解析T+方向自由齐次V列为默认M1替换候选, 采纳走AMM-033提案带锚重置计划; 双哨兵逐位全真=全仓锚3.5582+轮268 STAB跨脚本锚, 第54族新段第2轮族收口)
  check_cmd: grep -q "HOM-DEFAULT 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/hom_default/hom_default.json
- id: HOM-BOUND
  status: pr-pending(PR#51-判读HOM_BOUND_DEGREE_MATCHED=纯四次池实测边界在次数轴, 次数匹配齐次C臂比自由V好约3500×近完美恢复+守恒精确, 次数误设B臂付出7.56×, 判读与代码在dir/hom-bound分支, 合并后check过自动弹出; 决策=AMM-033范围注记升级为次数匹配齐次族配方实测推广路径; 第59族第1轮, scan §59三槽入库)
  check_cmd: grep -q "HOM-BOUND 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/hom_bound/hom_bound.json
- id: HOM-DRIFT
  status: pr-pending(PR#52-判读HOM_DRIFT_ROBUST=候选头全视距双轴占优MSE比0.62-0.87漂移比0.16-0.30, 候选漂移稳定0.14不随视距增长而默认头k400漂1.63, 判读与代码在dir/hom-drift分支, 合并后check过自动弹出; 决策=AMM-033锚集计划纳入长视距锚; 哨兵失配=超越函数池比特尺寸依赖如实诊断(预注册非门条款兑现), 第60族第1轮, scan §60三槽入库)
  check_cmd: grep -q "HOM-DRIFT 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/hom_drift/hom_drift.json
- id: POOL-BITS
  status: pr-pending(PR#53-判读ANCHOR_BOTH_FRAGILE=双头锚在比特级池扰动下均脆弱默认头spread中位1.86候选1.29稳30%但双过1.10门, 判读与代码在dir/pool-bits分支, 合并后check过自动弹出; 决策=AMM-033锚计划增补多变体协议每锚带spread注记; variant-160双锚逐位真=轮273同参锚教训实证, 第61族第1轮, scan §61三槽入库)
  check_cmd: grep -q "POOL-BITS 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/pool_bits/pool_bits.json
- id: HOM-SAMPLE
  status: pr-pending(PR#54-判读HOM_ARM_DIVERGED=判负分支兑现B s0 n128训练NaN 1/18单元, 有限格注记=纹理反转n64 ratio0.99持平vs n256 0.66=候选优势是全数据现象, 判读与代码在dir/hom-sample分支, 合并后check过自动弹出; 决策=AMM-033 benefit-scope保守注记优势限于house规模小样本不外推, 第62族第1轮, scan §62三槽入库)
  check_cmd: grep -q "HOM-SAMPLE 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/hom_sample/hom_sample.json
- id: RECIPE-HEAD
  status: pr-pending(PR#55-判读COMPOSE_ABSORBED=次可加B0候选头单独1.949全场最优<B1组合2.241<A1配方2.645<A0默认2.961, 三哨兵逐位全真A0/A1轮252/B0轮269, 判读与代码在dir/recipe-head分支, 合并后check过自动弹出; 决策=either-or采纳选候选头单独配方与头不叠加回灌PR scope注记, 组合确认轮回灌门2精神)
  check_cmd: grep -q "RECIPE-HEAD 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/recipe_head/recipe_head.json
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;新方向(文献扫描/用户指定)追加到队尾;队列空⇒按 goal_check 路由(先盘判读后续池)。
**PR 号勘误(轮 266)**:gh 裸命令默认查 origin(上游),fork 上 48 PR 全部真实 OPEN(轮 236-264 各 PR 实号已按 gh pr list 勘误;历史行不改);RECIPE-SYNTHESIS=PR#44。
**条件性重入口(轮 65 条款)**:V-HOM-STAB(第 54 族第 3 轮,幅度-方向解耦稳定化,scan §57)=触发新马拉松段(族额度重置)即入队;**已于轮 268 兑现**(新段第 1 轮入队执行,STAB_REPAIRS,PR#49 在途;后续迭代点=齐次头实现确认探针走判读后续池)。
**价值出口六门**:细则唯一源=AMENDMENTS+goal_check 输出(每心跳必见),此处不复制——入队带决策耦合声明/配方族默认关闭/≥3 族判默认非最优⇒强制组合回灌/3-seed/弱题录禁 [行动]/判单+direction_gate 提交门。研究内容唯一源=PRD §19。
