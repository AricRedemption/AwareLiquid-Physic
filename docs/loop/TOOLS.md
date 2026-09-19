# LOOP TOOLS — 诊断与实验工具索引(先复用,后新写;新工具必回写)

> 每件工具:一句话用途 + 入口。全部 CPU、确定性、带溯源 JSON 输出。

| 工具 | 用途 | 入口 |
|---|---|---|
| `sample_efficiency_eval.py` | 样本数-vs-MSE 双曲线(两训练循环对照) | `--sizes --n_seeds --eval_ks --probe_context --start_probe --start_mix --two_stage --adaptive_sampling` |
| `start_time_sweep.py` | 1 步误差按起点时刻剖面(D1g 机制证据) | `--out_dir d1g_sweep` |
| `identifiability_probe.py` | 弹簧族隐藏 ω 的观测窗 Fisher 信息 J(ω) | 即跑即出,秒级;轮 69 起 `--window_scan` 扫窗口轴(J/CRB/平台判定,D6 协议工具化,产物 `d6_window_scan/`) |
| `tests/test_dissipation.py` | 耗散槽位探针组(轮 74):判据 A 默认关逐位等价 / B1 闭式阻尼振子解析对照(斜率−0.301 vs −0.3) / B2 头级严格单调+γ≈0 归因对照 | `.venv/bin/python -m pytest tests/test_dissipation.py`(秒级) |
| `plot_profiles.py` | 论文主图:D1g 四剖面板(start-time × MSE,训练窗阴影) | `--sweep JSON --out PNG`;依赖 `plots` extras(`uv pip install -e ".[plots]"`) |
| `field_identifiability_probe.py` | M2 场 c(x) 的谱域 Fisher(逐 cos 模式) | 即跑即出,秒级 |
| `goal_check` | **目标校验路由器**(每轮心跳第一步):验 goal_queue 顶部 done_condition,达成自动弹出晋升 | `./scripts/goal_check`;退出码 0=达成已弹出 / 1=未达成继续迭代 / 2=队列空 |
| `probe_run` | **本机探针训练资源护栏**(AMM-008 闸门 v3):档位/时长校验(T1≤15/T2≤60,T3 拒绝)+ 线程=⌊0.6×逻辑核⌋ + nice 15 + 溯源行(stderr 可抄进结果 meta) | `./scripts/probe_run T1\|T2 <est_min> -- <cmd>`;`--dry-run` 只打印不执行;测试 `tests/test_probe_run.py` |
| `probabilistic_eval.py` | 概率预测 + **校准检验**(D-1,coverage95/z 矩,`calibration_stats` 函数;--context_dim 1 = ω 后验忠实实例化) | `probe_run T1 -- ... probabilistic_eval.py --train_steps 500 --context_dim 1 --seed N --out_dir ...`;测试 `tests/test_calibration_stats.py` |
| `plot_profiles.py` | 论文主图:D1g 四剖面板(start-time × MSE,训练窗阴影) | `--sweep JSON --out PNG`;依赖 `plots` extras(`uv pip install -e ".[plots]"`) |
| `field_eval.py` | M2 场任务 liquid vs static + resolution | `--train_loop {semigroup,prefix}` |
| `field_eval.py` | M2 场任务 liquid vs static + resolution | `--train_loop {semigroup,prefix}`;G4-E1 起:`--oracle_ctx`(三臂上界分解+线性/MLP 双探针)、`--arms`(选臂子集,算力闸门合规) |
| `oracle_ctx_matrix` / `OracleOperatorWrapper` / `field_context_probe` / `mlp_context_probe` | D2-CAPACITY 工具组:真 c(x) 8 系数投影、前缀指纹查表注入、线性/非线性可读出探针 | `benchmarks/field_eval.py`;测试 `tests/test_oracle_ctx.py` |
| `audit_results.py` | 结果 JSON 溯源 schema 审计(--check 为提交门) | `--check [目录]` |
| `m1_semigroup_eval.py` | 半群 vs prefix 主对照(gen_spring 出处) | — |
| `energy_drift_eval.py` | P0-3 守恒漂移对照 | — |

## 已知产物目录(结果本地留存,数字见 PRD §19)

`d1_small_n` `d1b_eval_depth` `d1c_start_probe` `d1d_start_mix`
`d1f_two_stage` `d1g_sweep` `n2_adaptive` `d2_m2_loop/{sg,prefix}`
`d3_window/{tobs8,tobs24}` `d3_identifiability` `d3_field_identifiability`
`physics_out_v02`(第九波 canonical,勿覆盖)
