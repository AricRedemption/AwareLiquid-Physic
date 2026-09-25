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
  v5.2 六门体系下的 T1 探针环:队列目标逐个探针-判读-PR(细则与立法史
  唯一源=AMENDMENTS/goal_check/probe_run,本文件不复述)。
current_action: >-
  v5.2(AMM-029 方向门禁生效):六门=AMM-028 五门+方向判单门,细则
  唯一源=AMENDMENTS+goal_check 输出(每心跳必见)。当前队列 38 条
  (37 pr-pending+CTX-DIM-2 actionable);RECIPE-SYNTHESIS 判
  RECIPE_SYNERGIC(组合收益 10.7% 3-seed)回灌 PR=用户线下;轮 237
  WARMUP-PROBE-2 判 WARMUP_3S_BENEFICIAL(比值 0.8561 但一致性 1/3
  =收益 seed0 驱动,44.2% 降格定性,回灌依据改记组合 3/3)。下一心跳:
  goal_check 路由迭代 CTX-DIM-2(dir/ctx-dim-2 分支 3-seed ctx_dim
  1v8 确认+ω 语义重标定诊断,轮 226 判读行明示族后续=最大配置误差
  的统计升级,决策耦合=回灌配方 ctx 轴去留);池余三条(AMP 线性
  不变性归因/RESIDUAL 谱指标/TOSA 窗长-ctx 解耦)出处已锚定按序留池。
blocked_on: >-
  1) PR 合入=用户线下;2) 停车场重启(N1 v1+/T2/T3/Kaggle/隐藏卷)
  待用户指令;3) Kaggle 凭证=激活材料不阻塞。
next_trigger_hint: goal_check → CTX-DIM-2 actionable(dir/ctx-dim-2 分支 3-seed ctx_dim 1v8 +ω 语义诊断:探针执行→判读→PR,哨兵锚=ctx8 臂 s0 逐位 3.5582+ctx1 臂 s0 逐位 1.9746)→ 判读后消化轮优先(回填资产索引 ctx 条目);池余三条按序(AMP 归因/RESIDUAL 谱指标/TOSA 解耦);蒸馏轮只收"声明了决策耦合"的族/ 用户指令 / 停车场重启
pointer: docs/PRD.md §19(判读落点);docs/loop/{AMENDMENTS,
  DEBT-LEDGER,PLAYBOOK,TOOLS,RSI-INDEX}.md;docs/scan-conditioning.md
  (蒸馏唯一源);docs/n1-asset-index.md(N1 素材)。
updated: 2026-09-25 (**轮 238:消化轮+CTX-DIM-2 入队**)——轮 237
  WARMUP-PROBE-2 判读(WARMUP_3S_BENEFICIAL,比值 0.8561 但一致性
  1/3=收益 seed0 驱动,轮 213 的 44.2% 降格定性,回灌依据改记组合
  3/3)回填资产索引第 18 条;分流 balance_gauge EXP=0.2 无报警/消化
  率 1.0;池盘点非空 ⇒ 同轮入队 CTX-DIM-2(轮 226 判读行明示族后续
  =最大配置误差 ctx_dim 的 3-seed 统计升级+ω 语义重标定诊断,族段内
  第 2 轮达上限);队列三十八条(37 pr-pending+CTX-DIM-2 actionable)。
  下一心跳=goal_check 路由迭代 CTX-DIM-2。

## goal_queue(顶部为当前目标)

```yaml
goal_queue:
- id: RECIPE-SYNTHESIS
  status: pr-pending(PR#38待建-判读RECIPE_SYNERGIC=组合收益10.7% ratio=0.893 3/3方向一致, 判读与代码在dir/recipe-synthesis分支, 合并后check过自动弹出; 决策=臂B五轴为M1默认配置候选, 回灌PR用户线下处理)
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
  status: pr-pending(PR#39待建-判读WARMUP_3S_BENEFICIAL=比值0.8561<0.95但一致性1/3收益seed0驱动如实注记, 判读与代码在dir/warmup-probe-v2分支, 合并后check过自动弹出; 决策=warmup保留回灌配方候选依据改记组合3/3, 轮213的44.2%降格seed0抽取)
  check_cmd: grep -q "WARMUP-PROBE-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/warmup_probe_v2/warmup_probe_v2.json
- id: CTX-DIM-2
  status: actionable
  check_cmd: grep -q "CTX-DIM-2 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/ctx_dim_2/ctx_dim_2.json
```
队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;新方向(文献扫描/用户指定)追加到队尾;队列空⇒按 goal_check 路由(先盘判读后续池)。
**价值出口六门**:细则唯一源=AMENDMENTS+goal_check 输出(每心跳必见),此处不复制——入队带决策耦合声明/配方族默认关闭/≥3 族判默认非最优⇒强制组合回灌/3-seed/弱题录禁 [行动]/判单+direction_gate 提交门。研究内容唯一源=PRD §19。
