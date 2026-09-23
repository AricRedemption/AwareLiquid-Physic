# LOOP TOOLS — 诊断与实验工具索引(先复用,后新写;新工具必回写)

> 每件工具:一句话用途 + 入口。全部 CPU、确定性、带溯源 JSON 输出。

| 工具 | 用途 | 入口 |
|---|---|---|
| `sample_efficiency_eval.py` | 样本数-vs-MSE 双曲线(两训练循环对照) | `--sizes --n_seeds --eval_ks --probe_context --start_probe --start_mix --two_stage --adaptive_sampling` |
| `start_time_sweep.py` | 1 步误差按起点时刻剖面(D1g 机制证据) | `--out_dir d1g_sweep` |
| `identifiability_probe.py` | 弹簧族隐藏 ω 的观测窗 Fisher 信息 J(ω) | 即跑即出,秒级;轮 69 起 `--window_scan` 扫窗口轴(J/CRB/平台判定,D6 协议工具化,产物 `d6_window_scan/`) |
| `tests/test_dissipation.py` | 耗散槽位探针组(轮 74):判据 A 默认关逐位等价 / B1 闭式阻尼振子解析对照(斜率−0.301 vs −0.3) / B2 头级严格单调+γ≈0 归因对照 | `.venv/bin/python -m pytest tests/test_dissipation.py`(秒级) |
| `plot_profiles.py` | 论文主图:D1g 四剖面板(start-time × MSE,训练窗阴影) | `--sweep JSON --out PNG`;依赖 `plots` extras(`uv pip install -e ".[plots]"`) |
| `field_identifiability_probe.py` | M2 场 c(x) 的谱域 Fisher(逐 cos 模式);轮 95 起 `--meanpool` 对照臂:空间均值池化的 Fisher 谱+逐模式保留率(聚合层信息湮灭实证,均值场恒等式:total retention 8.6e-11) | 即跑即出,秒级;测试 `tests/test_field_meanpool_probe.py` |
| `goal_check` | **目标校验路由器**(每轮心跳第一步;AMM-013 起内置仪表闸):DEBT-FIRST/队列路由/MINING-FROZEN 自动裁决 | `./scripts/goal_check`;退出码 0=ACHIEVED 已弹出 / 1=NOT-Achieved / 2=QUEUE-EMPTY / 3=MINING-FROZEN 补证据轮 / 4=DEBT-FIRST 先清欠 |
| `probe_run` | **本机探针训练资源护栏**(AMM-008+010 闸门 v3.1):档位/时长校验(上限数值以脚本内置为唯一执行点)+ 线程=⌊0.6×逻辑核⌋ + nice 15 + PROBE_TIER/EST 溯源透传(stderr 可抄进结果 meta) | `./scripts/probe_run T1\|T2 <est_min> -- <cmd>`;`--dry-run` 只打印不执行;测试 `tests/test_probe_run.py` |
| `balance_gauge` | **平衡仪表计量器**(AMM-012/014):PRD §19 轮记录头自动分类(mining/evidence/t0)+GOALS 队列 WIP+台账欠账分账(L/C),算 EXP 占比与报警线;数值自动计算不手工维护 | `./scripts/balance_gauge [--window 10]`;测试 `tests/test_balance_gauge.py` |
| `stop_gate.sh` | **Stop hook 会话连续性闸**(AMM-020,Desktop 主引擎):模型想结束时查 队列非空+mode=ON+锁新鲜+state≠IDLE 四闸 ⇒ exit 2 请求继续(ZCode 上限 3 次/会话);配置在 `.zcode/config.json` | 随会话自动触发;`bash scripts/stop_gate.sh` 可手动试闸(无马拉松时预期 exit 0) |
| `ignite.sh` | **跨 Agent 点火器**(AMM-020,Ralph 式,**沉睡未激活**):锁新鲜/mode=OFF/IDLE 三查不点火,否则按 agent-cmd.conf 喂 GOAL-PROMPT;驱动=机器级 crontab | `docs/loop/agent-cmd.conf` 填一行 headless 命令模板后可用;仅将来 CLI 场景 |
| `probabilistic_eval.py` | 概率预测 + **校准检验**(D-1,coverage95/z 矩,`calibration_stats` 函数;--context_dim 1 = ω 后验忠实实例化) | `probe_run T1 -- ... probabilistic_eval.py --train_steps 500 --context_dim 1 --seed N --out_dir ...`;测试 `tests/test_calibration_stats.py` |
| `tsfm_baseline_eval.py` | D-2 TSFM 零样本参考基线(Chronos/TimesFM on M1 q(t) 外推 k=100,同池 d1b 尾 128,q-only 口径,3 seeds,逐池 JSONL 断点续跑;公平性三声明入 meta) | `probe_run T1 20 -- ... tsfm_baseline_eval.py --models chronos,timesfm --timesfm_path <ckpt>`;依赖 `chronos-forecasting`+`timesfm[torch]`(venv,不在 lock);测试 `tests/test_tsfm_baseline.py` |
| `plot_profiles.py` | 论文主图:D1g 四剖面板(start-time × MSE,训练窗阴影) | `--sweep JSON --out PNG`;依赖 `plots` extras(`uv pip install -e ".[plots]"`) |
| `field_eval.py` | M2 场任务 liquid vs static + resolution | `--train_loop {semigroup,prefix}` |
| `field_eval.py` | M2 场任务 liquid vs static + resolution | `--train_loop {semigroup,prefix}`;G4-E1 起:`--oracle_ctx`(三臂上界分解+线性/MLP 双探针)、`--arms`(选臂子集,算力闸门合规) |
| `oracle_ctx_matrix` / `OracleOperatorWrapper` / `field_context_probe` / `mlp_context_probe` | D2-CAPACITY 工具组:真 c(x) 8 系数投影、前缀指纹查表注入、线性/非线性可读出探针 | `benchmarks/field_eval.py`;测试 `tests/test_oracle_ctx.py` |
| `grad_path_probe.py` | **GRAD-PATH 梯度路径探针**(轮 93,零训练):k=8/32/128 展开图内存(saved_tensors_hooks pack 口径)/节点数/逐组梯度范数标度+eval 对照(params_with_grad 语义锚),判负阈值钉在代码内(MEM_SLOPE_OK/GNORM_RATIO_BOUNDS),M1/M2 两头,seed 0 逐位复现 | `probe_run T1 5 -- .venv/bin/python benchmarks/grad_path_probe.py --heads m1,m2 --ks 8 32 128 --out_dir grad_path_probe`;测试 `tests/test_grad_path_probe.py` |
| `classic_baseline_eval.py` | **经典系统辨识基线两臂**(轮 99,CLASSIC-BASELINE):LSQ-ω̂(中心差分+过原点线性 LS)与自实现 STLSQ(多项式库,零依赖)on M1 同池 768 轨,解析 (A,B) 边界态+Verlet k100 滚出;无噪线性域近 oracle 级(2.7e-6),三声明协议 docs/classic-baseline-protocol.md | `probe_run T1 5 -- .venv/bin/python benchmarks/classic_baseline_eval.py`(秒级);测试 `tests/test_classic_baseline.py` |
| `verlet_order_probe.py` | **Verlet 观测阶数探针**(轮 104,VERLET-ORDER;09-22 收尾补登记——入库时漏登 TOOLS):固定视距 T=10、dt 四档,energy drift 与 q RMSE 双轴 log2 收敛阶,判负带 p̂∈[1.8,2.2] 预注册在代码内;口径:点均精度以 RMSE 轴为准(MSE 平方量观测阶翻倍,raw MSE 留参照),最粗对预渐近混叠排除规则入 docstring;结果 2.021/1.999 双轴确认 2 阶(N1 methods 素材) | `probe_run T1 5 -- .venv/bin/python benchmarks/verlet_order_probe.py`(零训练,秒级);测试 `tests/test_verlet_order_probe.py` |
| `escape_door_probe.py` | **逃生门#3 A/B 验证探针**(轮 110,ESC-DOOR-VAB):磁族同池同预算双臂——可分 HamiltonianHead+Verlet vs NonseparableHamiltonianHead+隐式中点,"门该开时才开"必要性对比;预注册判负①-④钉在代码内(ratio_gate 2×/drift_gate 0.10 房史校准),实测比值 60669× PASS,逃生门清单 [C]→[B];1-seed 筛查口径 | `probe_run T1 5 -- .venv/bin/python benchmarks/escape_door_probe.py`(~1min 实测);测试 `tests/test_escape_door_probe.py`(结构断言用 float64——小 dt 极限在 float32 被 ulp 吞) |
| `kaggle_quota_check.py` | **Kaggle GPU 余量读数**(轮 108,AMM-023 用户指令):best-effort 读 UI 同款配额端点(非官方,诚实注记入 docstring),结构化失败码 0=ok/3=NO_CREDS/4=DEP_MISSING/5=READ_FAILED;TIERS 常量=余量→派发档位唯一源(NO_READ/PROBE_ONLY/SHORT_RUN/FULL_RUN/MULTI_RUN),**仅 status=ok 驱动派发** | `.venv/bin/python scripts/kaggle_quota_check.py`(--creds 默认 ~/.kaggle/kaggle.json,用户放凭证=材料非决策);协议 `docs/kaggle-quota-protocol.md`;测试 `tests/test_kaggle_quota_check.py`(全离线) |
| `audit_results.py` | 结果 JSON 溯源 schema 审计(--check 为提交门) | `--check [目录]` |
| `m1_semigroup_eval.py` | 半群 vs prefix 主对照(gen_spring 出处) | — |
| `energy_drift_eval.py` | P0-3 守恒漂移对照 | — |

## 已知产物目录(结果本地留存,数字见 PRD §19)

`d1_small_n` `d1b_eval_depth` `d1c_start_probe` `d1d_start_mix`
`d1f_two_stage` `d1g_sweep` `n2_adaptive` `d2_m2_loop/{sg,prefix}`
`d3_window/{tobs8,tobs24}` `d3_identifiability` `d3_field_identifiability`
`tsfm_baseline`(轮 89,D-2)
`physics_out_v02`(第九波 canonical,勿覆盖)
