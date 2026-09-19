# 滚出训练梯度路径审计(GRAD-PATH,轮 93,2026-09-20)

> 预注册:PRD §19 轮 87(交付物/判负标准先于执行钉死);文献坐标:
> scan §22(Um 2020 DP 范式 / Matsubara 辛伴随 / 前向稳定≠反向稳定)。
> 执行:`benchmarks/grad_path_probe.py`,probe_run **T1**(threads=4/8,
> nice=15,实际 ~40s ≪ 5min 估计),零训练(无优化器、无参数更新),
> seed 0 确定性(两次全跑 JSON 逐位一致);产物
> `benchmarks/grad_path_probe/grad_path_probe.json`(gitignored,数字抄本
> 文与 PRD)。**结论分级:T1 探针,只解锁路由与筛选,终局声明须 T3。**

## 摘要

① create_graph 梯度路径语义审计:训练态梯度路径为
`loss → k 步展开滚出链 → 内层 autograd.grad 算子(create_graph=True)→ T/V 参数与 ctx → liquid core`,
backward 实际穿过能量网的**混合偏导算子**(二阶结构);eval 态内层场求值为图外常数(探针以
`params_with_grad==0` 验证)。② 冒烟探针:k=8/32/128 展开图内存**严格线性**
(对数斜率 1.000,M1 2.94→47.0 MB,M2 38.9→622 MB @B=32);梯度总范数随 k
温和指数增长(k128/k8 比 78.7/129.4 ≈ 每步 +3.7~4.1%,远在预声明界内)。
③ **判负标准①②均未触发**;本仓 k_train=8 的展开式 BPTT 选择维持
(精确梯度 + ~MB 级驻留),辛伴随升级草案作为 k↑ 触发条件式云跑候选落档(§5)。

## 1 create_graph 梯度路径语义审计

### 1.1 内层梯度点清单(全部 6 个头,同一模式)

`_grad` 家族全部以 `create_graph=self.training` 调
`torch.autograd.grad(energy.sum(), x)`(hamiltonian.py:179/285/421/498+506/571/673,
另 pairwise_potential.py:112):HamiltonianHead(T/V)、FiLMHamiltonianHead、
OperatorHamiltonianHead(T/V)、TimeConditionedHamiltonianHead(T/V)、
NonseparableHamiltonianHead(T/V/C)、OperatorHamiltonianHead2d、
NBodyHamiltonianHead。**训练/评估的梯度语义开关只有一个:模型的
`self.training` 标志**;头部之外的训练循环(train.py `train_semigroup`、
field_eval 训练段)在 `torch.enable_grad()` 下滚出——因为场本身就是
autograd 梯度,`no_grad` 会杀死滚出(轮 2 坑,PLAYBOOK 在案)。

### 1.2 训练态路径解剖(train_semigroup,k 步展开)

```
loss = MSE(rollout_k(q0,p0|ctx), truth)
  └─ rollout 链:每步 velocity-Verlet = 2×dV_dq + 1×dT_dp(内层 grad,k×3 次)
       └─ 内层 grad 算子(create_graph=True)⇒ backward 穿过"对梯度的导数"
            = 能量网 H 的混合偏导 J^T·v 积(二阶结构,图规模 k×3×网深)
       └─ FiLM/concat 通道 ⇒ ctx ⇒ context_proj ⇒ LiquidCore.encode(前缀编码)
  └─ 数据侧:q0/p0 为 gather 叶子,q_true/p_true 不挂图
```

要点:**(a)** 内层 `create_graph=True` 把内层 backward 的算子**展平进外层图**
(探针节点计数从 loss.grad_fn 可达 577→7177 个,M1 k8→k128)——即反向传播
计算的是 ∂L/∂θ = Σ (∂²H/∂x∂θ) 型项,这正是"可微物理训练"的精确梯度口径
(Um 2020,scan §22.1);**(b)** ctx 通道全程连通(FiLM scale/bias 与 concat
都吃 ctx 梯度,再经 context_proj 回传液基细胞)——轮 90 R1 辅助辨识即借
此通道注入监督。

### 1.3 eval 态语义(已探针验证)

`model.eval()` ⇒ 内层 `create_graph=False` ⇒ 场 g 是**图外常数**:滚出链
不携参数梯度,eval 损失 backward 后**零参数收到梯度**(探针 M1/M2 全档
`params_with_grad=0`)。但两点语义细节值得入档:

1. **`enable_grad` 仍必需**(内层 autograd.grad 自身要求 grad 模式);
2. **`requires_grad` 系标志在 eval 侧会假真**:`_grad` 对数据叶子
   `x.requires_grad_(True)` 是**原地改标**——q0/p0 被改后,滚出输出经这些
   叶子 `requires_grad=True`,`loss.requires_grad` 在 eval 也为 True。
   语义判据必须落在**梯度流终点**(参数是否收到梯度),不能用中间张量的
   requires_grad 标志(新坑,已回写 PLAYBOOK 轮 93)。

### 1.4 eval 态内存语义(对照档)

eval 滚出仍有内层 backward 的**瞬态**保存(每次 grad 调用后即释放):
pack 钩子口径 M1@k128 瞬态体积 20.7 MB ≈ 训练驻留 47.0 MB 的 44%
(M2@k128 267.7 MB vs 622.0 MB ≈ 43%)。即 eval 滚出不是零分配,只是
不驻留——长 rollout 评估的瞬时峰值仍按同阶量级预算。

## 2 冒烟探针:方法与数字

### 2.1 方法

- **图驻留内存**:`torch.autograd.graph.saved_tensors_hooks` pack 钩子累计
  save-for-backward 字节/张量数。口径声明:训练态=驻留至 backward 的量
  (≈展开图内存);eval 态=瞬时保存体积(§1.4);同一存储被两个节点共享
  保存时重复计字节——对标度无影响,绝对值按"pack 事件总量"理解。
  CPU 上这比 RSS 峰值干净(RSS 含解释器/分配器噪声,不可分辨图增量)。
- **图规模**:loss.grad_fn 可达唯一 autograd 节点数(内层展平算子计入)。
- **梯度范数**:backward 后逐参数组 L2(core/context_proj/T/V)+
  `||dL/dctx||`(ctx.retain_grad)。
- **零训练**:合成张量(seed 0),无优化器;判负标准①的操作化阈值
  (**先于运行钉进探针代码**):NaN/Inf;mem_slope∉[0.7,1.3];
  范数比 k_max/k_min 出 [1e-4,1e4]。
- 配置:M1=LiquidHamiltonianModel 默认规模(dim1/d64/ctx16/h64/depth2);
  M2=LiquidOperatorHamiltonianModel 缩减档(N16/modes6/width16/fno4/d32/
  ctx4);两者 B=32,t_obs=16。

### 2.2 数字(k=8/32/128,B=32,probe_run T1,~40s)

| head | k | 图驻留 MB | 保存张量 | 图节点 | fwd ms | bwd ms | ‖g‖总 | ‖g‖ctx | ‖g‖ctx/‖g‖总 |
|---|---|---|---|---|---|---|---|---|---|
| M1 | 8 | 2.94 | 408 | 577 | 16 | 7 | 1.83e-1 | 1.16e-3 | 6.4e-3 |
| M1 | 32 | 11.76 | 1632 | 1897 | 15 | 15 | 3.10e+0 | 5.69e-3 | 1.8e-3 |
| M1 | 128 | 47.05 | 6528 | 7177 | 59 | 48 | 1.44e+1 | 1.81e-2 | 1.3e-3 |
| M2 | 8 | 38.87 | 1784 | 4040 | 66 | 154 | 1.17e-1 | 1.42e-3 | 1.2e-2 |
| M2 | 32 | 155.49 | 7136 | 15656 | 259 | 612 | 9.03e-1 | 3.81e-3 | 4.2e-3 |
| M2 | 128 | 621.95 | 28544 | 62120 | 1049 | 2458 | 1.52e+1 | 2.71e-2 | 1.8e-3 |

### 2.3 判读

- **内存严格线性**:对数斜率 M1=1.0000 / M2=1.0000(2.94→11.76→47.05 MB
  恰 ×4/×16)。每步驻留 M1≈368 KB、M2≈4.86 MB(FNO 保存量大 ~13×)。
  本仓 k_train=8 实际训练驻留:M1 ~3 MB、M2 ~39 MB/批——**展开式 BPTT
  在当前档位零压力**,scan §22.2"k_train=8 无需变更"的文献判断获得本仓
  实测背书。
- **反向温和指数增长(前向稳定≠反向稳定的量化实例)**:‖g‖总
  k128/k8 = ×78.7(M1)/×129.4(M2)⇒ 每步复合 +3.7%/+4.1%。增长主要由
  **T(动能)组驱动**(M1:×107;k8→k128),V 组 ×17.8。方向与 scan §22.3
  坐标一致:辛结构保前向,不自动保反向;伴随动力学含 e^{λk} 型因子。
  在预声明界(1e4)内 ⇒ 判负标准①未触发,但**可证伪外推**(投影非实测):
  若 +3.7~4.1%/步 趋势不变,范数比触界在 k≈250-260 ——即 k_train↑ 到
  ~256 档时应同时预期内存(线性,~百 MB-GB 级)与反向稳定(裁剪/辛伴随)
  两个压力点。诚实注记:本探针为随机初始化网络+高斯合成数据,增长系数
  不等于训练后模型的工作点值;训练后复测列入辛伴随草案的验收前置(§5)。
- **ctx 通道(E4a 审计入口,只记录不下结论)**:k_train=8 工作点上
  ‖dL/dctx‖/‖g‖总 ≈ 0.6%(M1)/1.2%(M2)——绝对量随 k 增长(×15.6/×19),
  但**相对份额随 k 稀释**(T 组增长更快)。与轮 55 E4a 的 ~4e-5 一步压力
  同量级口径不同(彼为 field 模型单批测量),不做直接比较;假说"反向
  灵敏度结构衰减是 ctx 梯度弱的因素之一"在本探针中表现为**相对稀释**,
  k=8 处 ctx 份额并不随视距趋零——弱假说既未证实也未证伪,维持登记。
- **eval 对照**:params_with_grad=0 全档成立(create_graph=False 语义
  锚,§1.3)。
- **判负标准对账**:① 未触发(无 NaN、内存线性、范数在界内)——无需
  登记风险项,但 k≈260 触界投影按"如实入档"原则记录如上;② 未触发
  (k 标度数字齐全)——不降级。

## 3 辛伴随升级草案(k↑ 触发条件式云跑候选)

**触发条件(预注册,任一满足再立项,当前不立项)**:
(a) 任何训练档 k_train ≥ 256;(b) 单批图驻留 > 2 GB;
(c) 训练后模型在目标档复测出现范数出界(复用本探针阈值)或需引入
梯度裁剪才能稳定收敛。

**方案**(scan §22.2,Matsubara et al. Symplectic Adjoint Method):对
velocity-Verlet 的**离散格式**直接构造伴随:前向 `torch.no_grad` 只存
检查点 (q0, p0, ctx)(O(1) 内存),反向解伴随递推——对辛积分器
梯度**精确**(与展开式逐位同义,非 adjoint 法的近似)且内存 O(1),
前向代价 ~1×(无需像 adjoint 法重解正问题,链上状态已存检查点;比
adjoint 的 ~2× 前向代价便宜)。落点:`HamiltonianHead.rollout_adjoint`
+ `train_semigroup(use_adjoint=True)` 开关,默认关(保守路径逐位不变,
仿 rayleigh 槽位先例)。

**验收判据(预注册)**:k=32 上展开式 vs 辛伴随参数梯度余弦相似度
>0.999 且相对 L2 误差 <1e-3;峰值内存 < 2× 单步前向;训练一段
loss 曲线与展开式逐位同量级。**执行档位:T3 云跑候选**(本机 M1/M2
梯度对照探针为前置已备,本档探针即 Probe-First 证据)。

**当前裁决**:k_train=8 现状**不立项**(触发条件全不满足);本节仅为
k↑ 协议预留,不登记云欠账(无触发无欠账)。

## 4 N1 可引用表述(方法节口径)

- 训练范式:可微物理(DP)训练,梯度穿过 k 步辛积分器与液基推断链
  (Um et al. NeurIPS 2020 奠基引用,scan §22.1);
- 梯度精确性:展开式 BPTT 给出离散格式的**精确**梯度(相对 adjoint 法
  的近似梯度),k_train=8 档驻留 ~MB 级(本档探针数字),无需伴随法;
- k↑ 协议:预注册触发条件 + 辛伴随(精确+O(1) 内存)优先于截断/裁剪
  (scan §22.2);反向温和指数增长的量化实例与每步系数入档(§2.3)。

## 5 谱系与边界

- 判负标准两条均未触发 ⇒ GRAD-PATH **结案(通过,无风险项新增;
  k≈260 触界投影为条件式预警,非判定)**。
- 本轮全部数字为 T1 探针级:解锁路由与 N1 方法节表述;不构成任何
  训练后模型工作点的终局声明(该声明属未来云跑/隐藏卷)。
- E4a 弱假说:维持登记、无结论(§2.3);R1b/R1c 候选地位不变。
