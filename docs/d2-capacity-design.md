# D2-CAPACITY — M2 context→势能映射容量瓶颈实验设计(G4/P4,2026-09-19)

> 状态:**设计完成,预注册钉死,实验未跑**。执行入口见 §8 轮次拆分。
> 本文件是 P3 收口(轮 42)指出的"M2 增益瓶颈候选:context→32 节点势能
> 的映射容量/接口"的实验设计,同时兑现 P4 条件化注记(concat vs FiLM vs
> hypernetwork,M2 消融定案进 ADR)。预注册判负标准先行,先于任何运行。

## 1. 背景与证据链

- **D2 基线**(轮 7,`physics_out_v02/d2_m2_loop/`,3 seeds,semigroup 环,
  inhomogeneous c(x) 硬任务):liquid 0.02000±0.00035 vs static 0.02043±0.00033
  ——liquid 仅优 **2.1%**,且 seed 级 std 0.0003 与差距同量级;prefix 环下
  符号反转(static 优 2.0%)。对照 M1 弹簧族的 21%,M2 上 liquid 的增益
  **接近零**。
- **P3 收口**(轮 42,`d3_field_identifiability/`):隐参数族低维(4 模式,
  族谱支撑 89% 在模式 1–4)且 Fisher 谱平坦(动态范围仅 2.5x)——**观测端
  不缺信息,任务良置**。可辨识度解释被否定。
- **残存瓶颈候选**(P3 结论):① context 推断质量(liquid core 是否把
  4 模系数放进 ctx);② context→势能接口的表达力(信息在 ctx 但接口用不出);
  ③ 任务本身无系统辨识 headroom(static 平均介质已够)。
- **M1 先例的边界**:FiLM 在 M1 是负结果(短窗过拟合,rollout 发散 9x,
  ADR-4 保 concat),但 M1 头是逐点 MLP,concat 天然;M2 谱势能下 concat
  依然合法(逐节点广播拼接,平移等变 + 分辨率不变保持)——**M1 结论不可
  外推,这正是 P4 要求 M2 消融的原因**。

## 2. 接口解剖(架构事实)

`LiquidOperatorHamiltonianModel`(field_eval.py,M2 配置):
liquid core(LTC,d_model=48)→ `infer_context` → **ctx ∈ R^8**
(context_dim=8)→ `OperatorPotential`(FNO,width=32,depth=4)逐块 FiLM
条件化。FiLM 是**通道仿射**:每块 `v ← scale(ctx)⊙v + bias(ctx)`,
scale/bias 各为 Linear(8→32),空间维广播。

关键结构事实:**ctx 对势能的全部影响被限制在每块 2×32=64 个标量的均匀
通道调制**;空间变化的 ctx 依赖(真任务恰恰需要:V(q|c)=Σᵢ cᵢ²/2·(Δq)²
的系数逐节点变化)只能靠"均匀 FiLM × 固定谱核"的深层组合间接合成。
真值的 ctx→V 映射是**乘性、空间结构化**的——与 FiLM 的加性均匀调制
**参数化不对齐**。这是容量假设的构造性动机。

对照:M1 的隐藏参数是标量 ω,V(q|ω) 的 ω 依赖是全空间均匀的——FiLM
的均匀调制恰好对齐,M1 尚且输给 concat;M2 的 c(x) 是空间场,不对齐
更严重。

## 3. 三个竞争假设

| 假设 | 内容 | 若真,可观测量 |
|---|---|---|
| H_headroom | 任务不需要逐轨迹辨识,static 已近最优 | oracle ctx 也打不过 static |
| H_cap | 瓶颈在接口表达力(FiLM 参数化不对齐) | 真信息经 FiLM 无增益,但经更强接口有 |
| H_infer | 瓶颈在推断质量(ctx 丢失系数) | oracle 大幅优于 inferred,且探针读不出系数 |

## 4. Oracle context 的精确构造

生成器(`gen_wave_1d_inhomogeneous`):c(x) = c_mean + c_var·Σ_{m=1..4}
a_m·sin(2πmx/N + φ_m),a_m~U(0, 0.5/m),φ_m~U(0, 2π),再 clamp_min(0.2·c_mean)。
由 sin 和角公式,场是 8 个线性系数 {a_m cosφ_m, a_m sinφ_m} 的叠加——
**族恰好 8 维线性,与 context_dim=8 同维**(信息论上无欠充足混淆)。

**Oracle ctx(固定、确定性、零学习)**:对每条轨迹的 c(x)(32 节点)做
正交投影,取归一化系数:

```
α_m = (2/N)·Σᵢ c(xᵢ)·sin(2πmi/N),  β_m = (2/N)·Σᵢ c(xᵢ)·cos(2πmi/N)
ctx_oracle = [α₁,β₁,α₂,β₂,α₃,β₃,α₄,β₄] / c_var
```

该投影在生成族上几乎必然单射(共 8 维恰好张成;clamp 罕见激活,如触发
仅引入轻微非线性,如实注记)。c_mean 项为全族共享常数、零信息,故意排除。
**Oracle 臂从头训练**(C 臂),不做 eval 时换 ctx——避免对已训练 FiLM 的
OOD 污染。

## 5. 预注册协议 E1:三臂上界分解(先跑,最便宜)

- **臂**(同预算 300 steps、semigroup 环、inhomogeneous、3 seeds 0/1/2、
  评估 eval_k=80 / t_obs=24 / n_eval=64,与 D2 完全同配置):
  - **A** = static_operator(ctx=0)——已有,直接复用 D2 数字做先验对照,
    但仍随跑重训(同 seed 同 RNG,应逐字节复现 D2);
  - **B** = liquid_operator(inferred ctx)——同上;
  - **C** = oracle_operator(§4 的 ctx_oracle,其余结构同 liquid 的势能头)
    ——新实装(`field_eval.py --oracle_ctx`,~50 行:OracleOperator 包装 +
    投影 helper + results 键)。
- **附带探针(近零成本)**:对 B 臂 inferred ctx 做**线性读出**→ 8 个
  oracle 系数(移植 `--probe_context` 惯例,轮 6),报逐系数相关系数均值。
- **主终点**:rollout MSE(q,p);种子内先取均值,再跨 seed 取几何均值比:
  **ρ_CA = geo(MSE(C)/MSE(A)),ρ_CB = geo(MSE(C)/MSE(B))**。
  能量漂移为次级指标,只记录不设门。

### E1 判定(先钉死)

| 分支 | 判据 | 结论与动作 |
|---|---|---|
| E1-a | ρ_CA ≥ 0.9 | 真信息经 FiLM 接口无可兑现价值 → 接口容量或 headroom 主嫌疑,**进 E2**(C 臂换接口)定夺 |
| E1-b | ρ_CB ≤ 0.8 且探针均值 ≥ 0.8 | 信息在 ctx 而接口用不出 → **H_cap 主嫌疑**,E2 主攻 |
| E1-c | ρ_CB ≤ 0.8 且探针均值 < 0.5 | 推断丢信息 → **H_infer 主嫌疑**,接口消融降权;登记 liquid core 容量方向(d_model/t_depth)不排队 |
| E1-d | 其余中间带 | 记"部分支持",按较强证据定向,E2 缩为 1 变体 × 3 seeds |
| E1-null | ρ_CA ∈ [0.9,1.1] 且 ρ_CB ∈ [0.8,1.2] | 容量假设在当前预算不可分辨 → 预算升级实验(width×2 单臂)后才有资格关闭方向 |

诚实注记:探针线性读出失败 ≠ 信息不在(可能非线性编码);故 H_infer 判定
**必须联用 ρ_CB**,不单凭探针。

## 6. 预注册协议 E2:接口消融(P4 三选一定案)

**触发**:E1 完成后无条件执行(E1-a 分支下它是分辨"接口 vs headroom"的
唯一手段;E1-b 下它是定案手段)。

- **变体**(均作用于 C 臂 oracle ctx,与 E1 的 C-FiLM 同 seed 同预算对比,
  C-FiLM 不重训):
  - **C-concat**:lift 改 Linear(dim+context_dim → width),ctx 广播拼接
    为额外输入通道(+288 参数)。M1 ADR-4 胜者的谱势能移植。
  - **C-hyper**:低秩通道混合超网——每块 ctx → Linear(8→512) → 重排为
    32×32 低秩(r=8)仿射 W(ctx),v ← W(ctx)v;**通道混合使 ctx 依赖
    严格更富**,逐节点形式保持平移等变(+~18k 参数,总参数 +16%,
    如实注记不严格匹配,预算对齐)。
- **门**:
  - **通过**:最优变体 geo(C′/C_FiLM) ≤ 0.85 → 接口容量瓶颈实锤,
    P4 ADR 提案在 M2 谱势能语境采用该变体;
  - **否定**:全部变体 |ratio−1| < 0.10 → 接口容量非瓶颈 → 按 E1 分支
    收口(E1-a+本条 ⇒ **P3 终收口:M2 系统辨识链路整段无 headroom,
    P4 在 M2 上关闭,负结果入档**);
  - **中间** → 记录,不加扫描。
- **端到端补验**(仅在 E2 通过时):胜出变体换 B 臂(inferred ctx)× 3
  seeds 重训一臂,确认增益在真实推断链路上迁移(ADR 证据完整性;
  ~11 分钟)。

## 7. E3(条件性,不默认执行)

仅当 E2 通过且需要外推时登记:context_dim 剂量响应 {4, 8, 16} × 胜出
变体。预言:族维 8,增益在 ≥8 饱和、4 处退化。当前不排队。

## 8. 成本与轮次拆分(单轮 ≤1h 红线内)

| 轮 | 内容 | 预计 |
|---|---|---|
| E1-impl | OracleOperator + 投影 + 探针 + 测试(~3 例)+ E1 筛查 1 seed | 实装 ~15 min + 跑 ~11 min |
| E1-final | E1 三臂 × 3 seeds 终判 + 判定入档 | ~33 min |
| E2-run | 两变体 × 3 seeds(+条件性端到端臂)+ P4 ADR 草案 | ~22 min(+11 min) |

## 9. 风险与诚实注记

- **训练环轴**:D2 证明训练环翻转 liquid-vs-static 符号;本实验钉
  semigroup(出货配置、D2 胜者)。prefix 环下 static 已占优,是容量问题
  信息量最低的配置,不做。
- **参数量不严格匹配**:concat/hyper 变体参数 +0.3%/+16%,以训练预算
  对齐,注记了事——容量假设本身主张"参数化形状"而非"参数量"是瓶颈。
- **C 臂的 liquid core 缺席**:C 臂不含推断网络,度量的是"真信息 × 接口"
  的上界,不是端到端 liquid 模型——上界不成立则链路更不成立(保守方向
  正确);端到端迁移由 E2 补验步兜住。
- **单 seed 筛查只做闸门**:结论级判定必须 3 seeds + 几何均值(惯例)。
- 产物落 `physics_out_v02/d2_capacity/`,audit --check 过门,模型不入库。
