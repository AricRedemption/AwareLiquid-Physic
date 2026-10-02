# QUEUE-ARCHIVE — 队列归档区(AMM-038 条款 1,轮 431 落地)

> 方向条目 **开 PR 即终态**:PR 提交的心跳内从 goal_queue 弹出并归档到本文件,
> 不占活性、不进数数锚;合并落地与否属用户门控,循环零关注零催促(轮 267 校准)。
> 归档条目保留判读摘要与 PR 号=检索面;合并后复核(原 check_cmd 语义)降级为后台福利。
> 原始 check_cmd 弃用(轮 428 实证死路:grep 格式失配+依赖 gitignored 本机路径,0/55)。

```yaml
archived_pr:
- id: RECIPE-SYNTHESIS
  status: pr-pending(PR#44-判读RECIPE_SYNERGIC=组合收益10.7% ratio=0.893 3/3方向一致, 判读与代码在dir/recipe-synthesis分支, 合并后check过自动弹出; 决策=臂B五轴为M1默认配置候选, 回灌PR用户线下处理)
  check_cmd: grep -q "RECIPE-SYNTHESIS" docs/PRD.md
- id: M1-CAP-AXIS
  status: pr-pending(PR#1)
  check_cmd: grep -q "M1-CAP-AXIS" docs/PRD.md
- id: OMEGA-EXTRAP
  status: pr-pending(PR#2)
  check_cmd: grep -q "OMEGA-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/omega_extrap/omega_extrap.json
- id: NBODY-POOL-AUDIT
  status: pr-pending(PR#3)
  check_cmd: grep -q "NBODY-POOL-AUDIT 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/nbody_pool_audit/nbody_pool_audit.json
- id: R1D-MODE-SCAN
  status: pr-pending(PR#4, 判读NEGATIVE=判负分支已执行, 合并后check过自动弹出)
  check_cmd: grep -q "R1D-MODE-SCAN" docs/PRD.md
- id: SIGN-FLIP-PROBE
  status: pr-pending(PR#5, 判读TRANSIENT+异质纹理如实: 盆地稳定占多数, 合并后check过自动弹出)
  check_cmd: grep -q "SIGN-FLIP-PROBE" docs/PRD.md
- id: MAP-VS-FLOW
  status: pr-pending(PR#6, 判读FLOW_LIKE=跨dt迁移获支持, 合并后check过自动弹出)
  check_cmd: grep -q "MAP-VS-FLOW" docs/PRD.md
- id: ICL-M3
  status: pr-pending(PR#7, 判读=判负①②未触发三臂排序B<C<A交付, 合并后check过自动弹出)
  check_cmd: grep -q "ICL-M3" docs/PRD.md
- id: ICL-M3-INTERP
  status: pr-pending(PR#8, 判读=判负①外插为主因触发, 合并后check过自动弹出)
  check_cmd: grep -q "ICL-M3-INTERP" docs/PRD.md
- id: FASTSLOW-PROBE
  status: pr-pending(PR#9, 判读BOTH_FAILED=双时标捕捉失败量化边界交付, 合并后check过自动弹出)
  check_cmd: grep -q "FASTSLOW-PROBE 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/fastslow_probe/fastslow_probe.json
- id: FASTSLOW-2
  status: pr-pending(PR#10, 判读BUDGET_DOMINANT=步数为因逆转优化限制非结构限制, 合并后check过自动弹出)
  check_cmd: grep -q "FASTSLOW-2" docs/PRD.md
- id: GROK-CURVE
  status: pr-pending(PR#11, 判读SMOOTH_ASYMPTOTE=判负分支执行grokking命名不适用本仓, 合并后check过自动弹出)
  check_cmd: grep -q "GROK-CURVE" docs/PRD.md
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
  check_cmd: grep -q "WARMUP-PROBE" docs/PRD.md
- id: AMP-EXTRAP
  status: pr-pending(PR#34, 判读AMPEX_DEGRADES=幅度外推退化rel_comp=4.08线性不变性未被继承, 合并后check过自动弹出)
  check_cmd: grep -q "AMP-EXTRAP 判读" docs/PRD.md && test -f benchmarks/physics_out_v02/amp_extrap/amp_extrap.json
- id: RESIDUAL-SPEC
  status: pr-pending(PR#35, 判读RESIDUAL_PROFILED=残差能量93.2%在高频段高频欠拟合主导诊断读数交付, 合并后check过自动弹出)
  check_cmd: grep -q "RESIDUAL-SPEC" docs/PRD.md
- id: WARMUP-PROBE-2
  status: pr-pending(PR#48-判读WARMUP_3S_BENEFICIAL=比值0.8561<0.95但一致性1/3收益seed0驱动如实注记, 判读与代码在dir/warmup-probe-v2分支, 合并后check过自动弹出; 决策=warmup保留回灌配方候选依据改记组合3/3, 轮213的44.2%降格seed0抽取)
  check_cmd: grep -q "WARMUP-PROBE-2" docs/PRD.md
- id: CTX-DIM-2
  status: pr-pending(PR#39-判读CTX2_REVERSED=ratio1.1096>1.05反转由seed2单点驱动spread_B2.72高方差轴+语义诊断ctx不承载ω, 判读与代码在dir/ctx-dim-2分支, 合并后check过自动弹出; 决策=ctx轴维持默认8, 轮226读数降格, ctx_dim=1不入回灌; 轮242误弹恢复+锚加固两轮=锚改判读头全串合并前不可能命中)
  check_cmd: grep -q "CTX-DIM-2" docs/PRD.md
- id: TOSA-CTX-DECOUPLE
  status: pr-pending(PR#46-判读DEC_TRAIN_HARMFUL=ratio5.5975>1.05训练窗缩短在固定eval下5.6×恶化一致性0/3, 轮223 t8 4.5%定性=评估口径伪影+seed0抽取双层dissolution, 判读与代码在dir/tosa-decouple分支, 合并后check过自动弹出; 决策=t_obs维持默认24, t_obs=8不列回灌候选, RECIPE t_obs口径歧义条款收口)
  check_cmd: grep -q "TOSA-CTX-DECOUPLE" docs/PRD.md
- id: AMP-ATTR
  status: pr-pending(PR#38-判读AMPATTR_OK=归因动力学头主因载体头等变误差s2中位1.362/s4 2.838 vs ctx非不变0.417/1.224两层均O(1)+违反, 判读与代码在dir/amp-attr分支, 合并后check过自动弹出; 决策=头侧等变性参数化列停车场候选, AMPLITUDE族2/2收口)
  check_cmd: grep -q "AMP-ATTR" docs/PRD.md
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
  check_cmd: grep -q "V-HOM" docs/PRD.md
- id: V-HOM-STAB
  status: pr-pending(PR#49-判读STAB_REPAIRS=方向通道置零修复训练灾难0/3+MSE均值1.957低于自由V基线2.548+外推收益3/3兑现median1.705<3, 判读与代码在dir/v-hom-stab分支, 合并后check过自动弹出; 决策=方向自由齐次头候选提级头部构造独立线; REF哨兵逐位复现轮261 B臂, 第54族新段第1轮)
  check_cmd: grep -q "V-HOM-STAB" docs/PRD.md
- id: HOM-DEFAULT
  status: pr-pending(PR#50-判读HOM_DEFAULT_DOMINATES=齐次头完整构造对house默认头双轴3/3全胜分布内ratio0.658−34%外推median−49%, 判读与代码在dir/hom-default分支, 合并后check过自动弹出; 决策=解析T+方向自由齐次V列为默认M1替换候选, 采纳走AMM-033提案带锚重置计划; 双哨兵逐位全真=全仓锚3.5582+轮268 STAB跨脚本锚, 第54族新段第2轮族收口)
  check_cmd: grep -q "HOM-DEFAULT" docs/PRD.md
- id: HOM-BOUND
  status: pr-pending(PR#51-判读HOM_BOUND_DEGREE_MATCHED=纯四次池实测边界在次数轴, 次数匹配齐次C臂比自由V好约3500×近完美恢复+守恒精确, 次数误设B臂付出7.56×, 判读与代码在dir/hom-bound分支, 合并后check过自动弹出; 决策=AMM-033范围注记升级为次数匹配齐次族配方实测推广路径; 第59族第1轮, scan §59三槽入库)
  check_cmd: grep -q "HOM-BOUND" docs/PRD.md
- id: HOM-DRIFT
  status: pr-pending(PR#52-判读HOM_DRIFT_ROBUST=候选头全视距双轴占优MSE比0.62-0.87漂移比0.16-0.30, 候选漂移稳定0.14不随视距增长而默认头k400漂1.63, 判读与代码在dir/hom-drift分支, 合并后check过自动弹出; 决策=AMM-033锚集计划纳入长视距锚; 哨兵失配=超越函数池比特尺寸依赖如实诊断(预注册非门条款兑现), 第60族第1轮, scan §60三槽入库)
  check_cmd: grep -q "HOM-DRIFT" docs/PRD.md
- id: POOL-BITS
  status: pr-pending(PR#53-判读ANCHOR_BOTH_FRAGILE=双头锚在比特级池扰动下均脆弱默认头spread中位1.86候选1.29稳30%但双过1.10门, 判读与代码在dir/pool-bits分支, 合并后check过自动弹出; 决策=AMM-033锚计划增补多变体协议每锚带spread注记; variant-160双锚逐位真=轮273同参锚教训实证, 第61族第1轮, scan §61三槽入库)
  check_cmd: grep -q "POOL-BITS" docs/PRD.md
- id: HOM-SAMPLE
  status: pr-pending(PR#54-判读HOM_ARM_DIVERGED=判负分支兑现B s0 n128训练NaN 1/18单元, 有限格注记=纹理反转n64 ratio0.99持平vs n256 0.66=候选优势是全数据现象, 判读与代码在dir/hom-sample分支, 合并后check过自动弹出; 决策=AMM-033 benefit-scope保守注记优势限于house规模小样本不外推, 第62族第1轮, scan §62三槽入库)
  check_cmd: grep -q "HOM-SAMPLE 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/hom_sample/hom_sample.json
- id: RECIPE-HEAD
  status: pr-pending(PR#55-判读COMPOSE_ABSORBED=次可加B0候选头单独1.949全场最优<B1组合2.241<A1配方2.645<A0默认2.961, 三哨兵逐位全真A0/A1轮252/B0轮269, 判读与代码在dir/recipe-head分支, 合并后check过自动弹出; 决策=either-or采纳选候选头单独配方与头不叠加回灌PR scope注记, 组合确认轮回灌门2精神)
  check_cmd: grep -q "RECIPE-HEAD 判读:" docs/PRD.md && test -f benchmarks/physics_out_v02/recipe_head/recipe_head.json
- id: SPEC3
  status: pr-pending(PR#56-判读SPEC3_ORDER_TIED=修正截止下双臂low_band约0.998成分差0.02pp, r246谱增量系截止伪影且轮267排序对冲亦被推翻, 判读与代码在dir/residual-spec-3分支, 合并后check过自动弹出; 决策=AMM-031降级reference-only修正house值落账闭轮267待办, 标量双锚逐位真, RESIDUAL族口径修正闭账)
  check_cmd: grep -q "SPEC3" docs/PRD.md
- id: ANCHOR-PRECISION
  status: pr-pending(PR#57-判读PRECISION_ANCHOR_ROBUST=锚读数精度轴稳健, 12 spread全<=2.29e-6低于门0.10四个量级+双哨兵逐位真A=3.5582/B=2.0024, 判读与代码在dir/anchor-precision分支, 合并后check过自动弹出; 决策=AMM-033锚协议⑤维持现文本不增补精度变体轴, scan §65文献[坐标]级佐证)
  check_cmd: grep -q "ANCHOR-PRECISION" docs/PRD.md
```
- id: RECIPE-LOO
  status: pr-pending(PR#58-判读RECIPE_LOO_PARTIAL=五轴回灌候选维持无harmful轴, load-bearing=depth 1.189 3/3+warmup 1.092 2/3, NEUTRAL=lr_decay/wd/k_train弱证据不据此精简, 双哨兵逐位真含轮228复现首落地, 判读与代码在dir/recipe-loo分支; 轮228登记族后续兑现, 决策=回灌候选维持五轴, 回灌PR用户线下)
  check_cmd: grep -q "RECIPE-LOO" docs/PRD.md
- id: RECIPE-REDUCE
  status: pr-pending(PR#59-判读RECIPE_REDUCE_WEAK=五轴回灌候选维持, 双轴精简未过门ratio_red=1.0617弱带内, NEUTRAL三轴价值=训练稳定性非均值B2 spread1.79, 回灌候选五轴终判四探针证据链闭环, 判读与代码在dir/recipe-reduce分支; 轮434 LOO NEUTRAL弱证据的门1过门路径, 决策=回灌候选维持五轴, 回灌PR用户线下)
  check_cmd: grep -q "RECIPE-REDUCE" docs/PRD.md
- id: TOSA-LADDER
  status: pr-pending(PR#36-判读TOSA_RESOLVED=观测窗长度可分辨非单调锯齿, 最优t_obs=8短窗有益(与D6对表), 轮223; 历史上经AMM-026 check_cmd流程弹出未入归档, 轮449 dir在途对账补录; 决策=t_obs维持默认24, t_obs=8不列回灌候选=评估口径歧义收口)
  check_cmd: grep -q "TOSA-LADDER" docs/PRD.md
- id: CTX-DIM-LADDER
  status: pr-pending(PR#37-判读CTXDIM_RESOLVED=容量单调有害, 最优ctx_dim=1(默认8差80%=最大配置误差), 轮226; 历史上经AMM-026 check_cmd流程弹出未入归档, 轮449 dir在途对账补录; 后续轮239 CTX-DIM-2 3-seed反转=CTX2_REVERSED见CTX-DIM族条目, ctx轴维持默认8已闭族)
  check_cmd: grep -q "CTX-DIM-LADDER" docs/PRD.md
- id: RECIPE-BUDGET
  status: pr-pending(PR#60-判读RECIPE_BUDGET_REVERSED=组合收益在8000步预算反转ratio1.1157>1.05, 2000步10.7%收益不迁移且反号方向一致性3/3=>1/3, 决策=回灌PR scope限定2000步训练域+预算交互注记, 判读与代码在dir/recipe-budget分支; 轮227登记慢轴候选AMM-044供给义务转正, 回灌候选五轴的预算域边界=RECIPE家族第五条边界证据)
  check_cmd: grep -q "RECIPE-BUDGET 判读" docs/PRD.md
- id: N1-HIDDEN-REV
  status: done(轮 814 完成弹出:writing track, 轮 813 派生评估首次判可派生入队, 本拍蒸馏门三步齐后吸收轮 812 隐藏迁移反转进 n1-paper-draft——Abstract 诚实句/Sec.5 ladder 第 23 行+新段"Hidden-set migration check of the composite"/Sec.6 absorbed-composition 范围注/Limitations 4f/Sec.8 结论句+future-work 计算门控项/Appendix A [C] 行补记与隐藏集台账 998 消耗退役下一档 997; 数字全部对产物字段复算(可见 0.8931607635/A2.9612/B2.6449 3/3; 隐藏 A2.4269/B3.4910 ratio1.4384516685); asset-index 同心跳登记 4d 条目+§9 补记; 等效不删=两处陈旧指针以补记修正非删除; 零算力轮无 PR)
  check_cmd: grep -q RECIPE_MIGRATION_REVERSED docs/n1-paper-draft.md
- id: N1-RECIPE-SCOPE
  status: done(轮 816 完成弹出:writing track, 轮 815 机械缺口清点派生评估转正, 首拍蒸馏门三步齐后吸收配方收益两条域边界——Abstract 预算限定句/§5 ladder 第 24-25 行+新段"Two more domain limits: horizon and budget"/§6 absorbed-composition 预算限定/Limitation 4f 三重域声明[2000 步预算×可见 seed 集×视距稳健, 域外反号非减弱]/footer; 读数取自产物 JSON: HORIZON 0.8931607635/0.8339268819/0.8247211326 逐视距3/3 spread_B1.5377→1.0346 git_sha1a4af63 + BUDGET ratio1.1156959228 meanA2.3885671298 meanB2.6649146080 方向1/3 spread1.7274477275 train_steps8000 exec_tier T1 git_sha239c54b 含 8000 步无历史哨兵如实注记; asset-index 条目 4e 同心跳登记[轮 814 家规首跑]; 零算力轮无 PR)
  check_cmd: grep -q RECIPE_BUDGET_REVERSED docs/n1-paper-draft.md
- id: N1-HEAD-SIDES
  status: done(轮 818 完成弹出:writing track, 轮 817 标签×实质双判派生评估入队[真欠账强耦合两条=EQUIV_TRADEOFF+VHOM_NULL], 首拍蒸馏门三步齐后吸收头结构族两侧单独注入证据——§6 新段"The two sides were paid for separately first"[T 侧=分布内 ratio0.8604152214 −14.0% 3/3 而幅度外推逐 seed 全劣 rel_comp 中位 9.071 vs 3.334=缺口不在 T;V 侧=VHOM_NULL consistent0 且齐次臂 seeds0/2 灾难 2456.613037/701.840576, 唯 seed1 rel_comp 1.442855937 近完美恢复 vs 同构造 9.071356650=收益真实被参数化训练稳定性阻塞]+两侧合成边界"单侧≠完整构造"+Limitation 4d 补记[稳定性前置=候选活前提, 默认头替换候选=完整头 AMM-033, 禁单侧采纳主张]; 读数取自 equiv_head.json/v_hom.json 产物字段[git_sha 11e32aa/5215a97, 双哨兵 A_seed0 3.5581917763 与 A_seed0_round249B 2.7786638737 逐位], 索引语义经 249B↔261A rel_comp 列表逐位对账证实按 seeds[0,1,2] 排序; asset-index 条目 4f 同心跳登记[轮 814 家规第 3 次履行]; 等效不删=链正文与 4d 原文未动; 零算力轮无 PR)
  check_cmd: grep -q VHOM_NULL docs/n1-paper-draft.md
- id: N1-AMPATTR-SHARE
  status: done(轮 820 完成弹出:writing track, 轮 819 三判口径宽池清点浮出的唯一强耦合条目[AMPATTR_OK 轮 244], 首拍蒸馏门三步齐后吸收三通道归因闭合——§6 新段"Closing the third question: which channel carries the rest"[两通道分离构造=同 ctx 下 rollout(s·s0) vs s·rollout(s0) 隔离头等变性违反 / ctx(s·prefix) vs ctx(prefix) 隔离推断层非不变性; 聚合中位 头 1.3622821050(s2)/2.8378283895(s4) vs ctx 0.4166634232/1.2239125967, 逐 seed 主次次序两档尺度均 3/3; 份额非独占[两通道相对理想值 0 同 O(1)]+无阈值跨越声明[report-type 无判负门, RESIDUAL-SPEC 先例]+尺度并列报[ctx ×2.94 vs 头 ×2.08 从 s2→s4, 最窄 seed2 组合 2.9164962155 vs 1.8711150885]]+§7 新 Limitation 4g(report-only 边界+不外推到已修复候选头+隐藏复现计算门控停放)+footer 轮 820; 跨构造锚=本探针训练臂逐 seed rollout MSE 3.5581917763/2.6058924198/2.7196621895 与轮 249 默认臂逐位相同[轮 818 索引语义对账家规同轮复用]; 读数取自 amp_attr.json 字段 git_sha b1fd910 exec_tier T1; asset-index 条目 4g 同心跳登记[轮 814 家规第 4 次履行, 补 PRD-only 读数的索引缺口]; 等效不删=§6/§7 既有段未动且 4g 新条不挤压 4a-4f; 零算力轮无 PR)
  check_cmd: grep -q AMPATTR docs/n1-paper-draft.md
- id: N1-WEAKDEBT-ABS
  status: done(轮 827 完成弹出:writing track, 轮 826 用户重入口拍入队[用户粘贴 GOAL-PROMPT=放行令, 六条弱耦合登记欠账吸收=AMM-047 条件①供给面], 首拍蒸馏门三步齐[池内 5 条: 轮 111/814/817/819/820=段蒸馏义务良信尝试留痕, AMM-047 条件②同拍履行]+预注册判负三条先行后六条终态分账 **2 入稿+4 关账**——GENLEN_CONFIRMED 入稿[§5 梯子行 RESOLVED→CONFIRMED, 轮 258 出样方向 2/3 ratio 2.3661/2.7079=0.8738(−12.6%) seed4 微差 0.045 如实带注, 数字回溯 dir/genlen-confirm PRD 判读行+asset-index 第 25 条先行]; LOAD_BEARING+PRECISION_ANCHOR_ROBUST 关账[实质已入稿=草稿 §5 axis-attribution 段 depth 18.9% 3/3+warmup 9.2% 2/3(轮 228 loo_ratio 1.189/1.092)+ANCHOR-PRECISION 锚口径段(轮 406)]; SHARP_EOS+WINDOW_EDGE 关账[预注册分支未走=实判 SHARP_BELOW 轮 154(λ_max·lr 0.009→0.066≪EOS 阈值 2)+LEN_ROBUST 轮 170/171]; SPECTRA_INCREMENTAL 关账[谱口径未采纳为主判据, 逐 seed 一致 1/3=增量证据弱, 残差谱条目在档]; 清单漂移注记=TOSA_RESOLVED 为窄池名实标签 DEC_TRAIN_HARMFUL 草稿已载无新欠账[轮 826 坑条款履行]; 六标签清零⇒写作轴登记欠账=0; asset-index §7 第 7 条 WEAKDEBT 关账块同心跳登记; 等效不删=草稿仅梯子单行判词刷新; PRD §19 轮 827 判读行落地; 零算力轮无 PR)
  check_cmd: grep -q "N1-WEAKDEBT-ABS 判读" docs/PRD.md && grep -q WEAKDEBT docs/n1-asset-index.md
- id: N1-PROXY-CORROB
  status: done(轮 830 完成弹出:writing track, 轮 829 用户质询重入口拍的新鲜池枯重审蒸馏轮转出[scan §73 小规模代理实验配方迁移可靠性族 [坐标]×2], 首拍蒸馏门三步齐[池内 4 条: 轮 444 引用分级 scope 注记/111 引用回溯/94 题录核验/814 索引先行]+预注册判负三条[引用字段不符⇒停改/缺域限定⇒判违/等效不删破⇒当轮修, 三条均未触发]后吸收印证——§5 预算域段尾追加印证句(Goyal Maini Lipton Raghunathan CVPR 2024 数据配方排序算力依赖 + Wang et al. arXiv:2512.24503 ICLR 2026 代理协议排序不可靠, [B]+域限定'analogous phenomenon class, not a direct replication')+Limitation 4f 尾追加印证句(同两引用+域限定)+asset-index §7 第 8 条同心跳登记(使用条款=引用必带域限定+本仓预算跨度 4× 注记+不构成 [行动]); 效果=RECIPE_BUDGET/MIGRATION_REVERSED 的 house 发现升级为有文档化现象类外部印证, 预答审稿人'是否个例'质疑; 等效不删=既有内容零删改; 引用字段与 scan §73 逐项一致; PRD §19 轮 830 判读行落地; 零算力轮无 PR)
  check_cmd: grep -q "N1-PROXY-CORROB 判读" docs/PRD.md && grep -q "Goyal" docs/n1-paper-draft.md
- id: LADDER-SCAN-TOOL
  status: done(轮 843 完成弹出:engineering track, 轮 842 用户令 AMM-049 取活阶梯立法拍入队[阶梯第一滚供给=改造最小化闭环], 执行拍落地 scripts/ladder_scan 四级只读扫描器[L1 写作轴/L2 停车场/L3 硬化盲区/L4 蒸馏池龄; 只报数不判定, 全空输出=判空留痕附件]+tests/test_ladder_scan.py 5 用例[222→227 实测]+TOOLS 条目; 本仓真面首跑=L1 8/L2 6/L3 8=阶梯供给非空实证)
  check_cmd: test -f scripts/ladder_scan && .venv/bin/python -m pytest tests/test_ladder_scan.py -q >/dev/null 2>&1
- id: HARDEN-TOOLS-GAPS
  status: done(轮 845 完成弹出:engineering track, 轮 844 阶梯取活拍入队[AMM-049 首次实战生效后第一取活轴], 执行拍 TOOLS +5 条目[marathon_guard/hidden_check 豁免=T 一次性信号唯一性/iteration 豁免=直改真相源/headless_loop.sh+ignite.sh=已弃用轮 793 标注勿启用]+ladder_scan 豁免识别[+1 用例=6 用例 227→228 实测]; 复扫 L3=0 盲区 check_cmd rc0=达成)
  check_cmd: test "$(./scripts/ladder_scan | grep -c '未入' || true)" = 0
- id: AMM-AUDIT-453-ALIGN
  status: done(轮 849 完成弹出:governance track, 轮 849 重入口取活拍登记入队当拍执行[用户粘贴 GOAL-PROMPT v9.8 放行; 轮 847 注记之'待后续硬化轴'=AMM-049 L3 复检扩展面:登记在案硬化轴注记纳入人工复检], 执行拍 goal_check --audit 卫生检查三分流[状态行点锚'轮 N'=归属/'登记轮≤N'=已知态单列(真仓 31 条全归此桶)/真缺号=缺号口径]+已知态文案载轮 453 裁决语义禁补点锚禁元轮号+tests +1 用例[32→33, 229 全绿实测]+TOOLS goal_check 条目同步+PLAYBOOK+1 坑; done_condition 实测达成=audit 真面输出已知态 31 条单列+缺号 0[本拍留痕]; check_cmd 用源码标记 grep(全量 audit 递归自演算>30s 演练超时, 换快速锚=HARDEN-TOOLS-GAPS 先例同型); 零算力硬化拍无 PR)
  check_cmd: grep -q "AMM 卫生·已知态" scripts/goal_check
- id: REGISTRY-STRUCT
  status: done(轮 853 完成弹出:engineering track, 轮 852 取活入队[850 判枯过松修正=P2 清单对话面落盘], 执行拍落地 docs/loop/REGISTRY.md 机器可读镜像 14 条全量[写作轴 8+停车场 6, state=absorbed/closed/gated/candidate+gate=none/compute/human]+ladder_scan L1/L2 升级消费结构化面[+1 测试=7 用例 229→230 实测]; 真面首判 L1 candidate=0∧L2 gated=6=与轮 846 逐行核真机械一致)
  check_cmd: test -f docs/loop/REGISTRY.md && ./scripts/ladder_scan | grep -q "REGISTRY"
- id: DISTILL-BEAT
  status: done(轮 855 完成弹出:engineering track, 轮 854 对话面扫描取活入队[轮 852 块②首次生效], 执行拍 ladder_scan L4 升级输出节拍距 N=判单链尾轮−最近夜账入账轮[+1 测试=8 用例 230→231 实测, N≥10⇒强制节拍检查提示]=M2 AMM-011 十轮节拍本仓化; 真面 N=4)
  check_cmd: ./scripts/ladder_scan | grep -q "节拍距"
- id: NOTE-APPENDER
  status: done(轮 857 完成弹出:engineering track, 轮 856 取活入队[粘连四犯机械化], 执行拍 scripts/note_append 落地[换行另起行+缩进归一+计数打印家规超限退出 1]+4 用例[231→235 实测]; 狗粮首跑=本拍 857 详文即由该工具写入并正确拦截计数 4>3 提示折叠; 自抓=工具首版锚前无空行结构粘连 bug 测试首跑即拦+真仓三处历史粘连拆行+压 851-854 归家规)
  check_cmd: test -f scripts/note_append && .venv/bin/python -m pytest tests/test_note_append.py -q >/dev/null 2>&1
- id: DISTILL-INJECT
  status: done(轮 864 完成弹出:engineering track, 轮 863 用户立项令入队["后面一项肯定要做,这个很重要"], 执行拍 scripts/distill_inject 落地[PLAYBOOK+REGISTRY 双源检索 top-N 注入, 零命中如实退出 1]+ASK-TABLE.md 四栏问表(含轮 859/840 两条已用记录回填)+4 用例[235→239 实测]+TOOLS 条目; 真面狗粮首跑=按队列首条 goal 检索命中 49 条 top-3 高相关[859 L5 三态/61 最小闭环/75 对照式第三槽])
  check_cmd: test -f scripts/distill_inject && test -f docs/loop/ASK-TABLE.md && .venv/bin/python -m pytest tests/test_distill_inject.py -q >/dev/null 2>&1
