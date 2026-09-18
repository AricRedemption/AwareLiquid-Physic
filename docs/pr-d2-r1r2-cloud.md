# PR 交付包:D2-CAPACITY R1/R2 云算力执行(G4-PR,2026-09-19)

> 本文档即 PR 正文:云算力执行者照跑命令、回传产物即可。全部命令 CPU
> 可跑,预计总时长 **~70 分钟**(R1 ~12 min + R2 ~58 min)。
> 协议预注册:`docs/d2-capacity-design.md` §12(先于本包钉死)。
> 算力闸门 v2 登记:本机禁止训练,故交付云执行;欠账见 PRD §19 轮 54/57。

## 0. 背景一段(为什么跑)

M2 场任务上,liquid 端到端增益 ≈0,但三臂分解证明:任务需要辨识
(oracle ctx −27%)、接口送得到(同一 FiLM)、而 liquid 的推断 ctx 对
真系数**零可读出信息**(线性与 MLP 探针皆 ≈0),容量翻两番无效,梯度
饥饿被机械证实(推断路径/头梯度比 3.97e-3)。**R1** 验证"给推断路径
一条直接梯度(辅助辨识损失)能否解锁端到端增益";**R2** 验证"单步
目标的信息价值是否随训练视距(k_train)增长"(视距-增益曲线)。
先例线:E2C/DVBF(潜码监督)/ Gradient Starvation(现象理论),
见 `docs/scan-conditioning.md` §6。

## 1. R1:辅助辨识损失(主候选)

```bash
# 主判据跑(3 seeds, ~9 min CPU)
python benchmarks/field_eval.py --inhomogeneous --oracle_ctx \
  --arms liquid_operator --aux_identify_weight 1.0 \
  --n_seeds 3 --seed 0 \
  --out_dir benchmarks/physics_out_v02/d2_capacity/r1_aux

# 隐藏卷(一次性,seed 998 未消耗, ~3 min CPU)
python benchmarks/field_eval.py --inhomogeneous --oracle_ctx \
  --arms liquid_operator --aux_identify_weight 1.0 \
  --n_seeds 1 --seed 998 \
  --out_dir benchmarks/physics_out_v02/d2_capacity/r1_aux_hidden998
```

- **基线(已测,勿重跑)**:B(无辅助)geo 0.020004;C(oracle 上界)
  0.014834;B 臂线性探针 corr ≈0.014。见 PRD §19 轮 51。
- **判据(预注册 §12.3,先钉死)**:
  - **正**:`r1_aux` 的 rollout MSE 几何均值 ≤ 0.85 × 0.020004(即降
    ≥15%)且其 `ctx_probe.corr_mean` ≥ 0.5,两条件同时;
  - **负**:MSE 几何比 >0.95(变化 <5%)且 corr < 0.2 → 辅助辨识在
    硬约束架构上失效(与 VAE-land 的差异即新发现),推断侧方向关闭;
  - **中间**:如实记录,不加扫描。
- **隐藏卷验收(61fc5da 规)**:主结论为正时,998 单卷须同判据方向
  (MSE ≤ 0.85 × 同 seed 的 B 臂基线不存在——998 无配对 B;改用绝对
  判据:998 的 MSE ≤ 0.0170(=B 均值 ×0.85)且 corr ≥ 0.5)→ 通过才
  毕业;失败则结论降级为"仅 seeds 0-2 成立"。

## 2. R2:k_train 视距扫描(次候选)

```bash
# 三个视距档,各 2 臂 × 3 seeds(每条 ~18-25 min CPU,云上无单命令限制)
for K in 8 16 32; do
  python benchmarks/field_eval.py --inhomogeneous \
    --train_loop semigroup --arms liquid_operator,static_operator \
    --k_train $K --n_seeds 3 --seed 0 \
    --out_dir benchmarks/physics_out_v02/d2_capacity/r2_k$K
done
```

- **判据(预注册 §12.3)**:liquid/static 的 rollout MSE 几何比随
  k_train 单调走阔且 k=32 处 ≤ 0.85(走阔 ≥1.5x 相对 k=8 的 0.979
  基线)→ 视距轴成立(信息价值随深度付账,长 span 训练自带辨识压力);
  非单调或 k=32 仍 >0.95 → 记负。
- 注:k=8 档应逐位复现 e1_final 的 A/B 臂(同 RNG),作为管线校验;
  若不复现,立即停止并在回传中注明。

## 3. 回传与验收协议

1. 产物 = 各 `--out_dir` 下的 JSON(field_eval.json / grad_starvation.json);
   `meta.git_sha` 须指向含 R1 代码的提交(≥ fa8c8d6),`audit_results.py
   --check` 全过;
2. 回传 JSON 与运行日志(若云环境允许),数字由循环侧抄录 PRD §19 并
   按上述判据机械验收;
3. 模型权重不入库(惯例);`.pt` 永不入库(铁律)。
4. 判定入档后:正 → R1 毕业弹出,论文 §5 叙事链补"处方生效"段;
   负 → 如实记负,推断侧方向关闭,E2 条件性重入口失效,P3 终收口
   候选"M2 系统辨识链路无可达增益"。

## 4. 欠账登记(算力闸门 v2)

| 项 | 预计(CPU) | 状态 |
|---|---|---|
| R1 主跑 3 seeds | ~9 min | 欠:待云执行 |
| R1 隐藏卷 998 | ~3 min | 欠:待云执行(主结论正后) |
| R2 三档 ×2 臂 ×3 seeds | ~58 min | 欠:待云执行 |
| 合计 | **~70 min** | PR 交付,循环不阻塞等待 |
