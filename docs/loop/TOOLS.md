# LOOP TOOLS — 诊断与实验工具索引(先复用,后新写;新工具必回写)

> 每件工具:一句话用途 + 入口。全部 CPU、确定性、带溯源 JSON 输出。

| 工具 | 用途 | 入口 |
|---|---|---|
| `sample_efficiency_eval.py` | 样本数-vs-MSE 双曲线(两训练循环对照) | `--sizes --n_seeds --eval_ks --probe_context --start_probe --start_mix --two_stage --adaptive_sampling` |
| `start_time_sweep.py` | 1 步误差按起点时刻剖面(D1g 机制证据) | `--out_dir d1g_sweep` |
| `identifiability_probe.py` | 弹簧族隐藏 ω 的观测窗 Fisher 信息 J(ω) | 即跑即出,秒级 |
| `field_identifiability_probe.py` | M2 场 c(x) 的谱域 Fisher(逐 cos 模式) | 即跑即出,秒级 |
| `plot_profiles.py` | 论文主图:D1g 四剖面板(start-time × MSE,训练窗阴影) | `--sweep JSON --out PNG`;依赖 `plots` extras(`uv pip install -e ".[plots]"`) |
| `field_eval.py` | M2 场任务 liquid vs static + resolution | `--train_loop {semigroup,prefix}` |
| `audit_results.py` | 结果 JSON 溯源 schema 审计(--check 为提交门) | `--check [目录]` |
| `m1_semigroup_eval.py` | 半群 vs prefix 主对照(gen_spring 出处) | — |
| `energy_drift_eval.py` | P0-3 守恒漂移对照 | — |

## 已知产物目录(结果本地留存,数字见 PRD §19)

`d1_small_n` `d1b_eval_depth` `d1c_start_probe` `d1d_start_mix`
`d1f_two_stage` `d1g_sweep` `n2_adaptive` `d2_m2_loop/{sg,prefix}`
`d3_window/{tobs8,tobs24}` `d3_identifiability` `d3_field_identifiability`
`physics_out_v02`(第九波 canonical,勿覆盖)
