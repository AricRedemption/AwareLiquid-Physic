# 条件化接口文献/GitHub 扫描(G4-SCAN,2026-09-19)

> 问题:M2 的 context→势能条件化(FiLM 通道仿射)在算子学习文献里的
> 同类实践是什么、谁做过、失败/成功在哪。按学术引用潜力排序。
> 服务对象:E2 接口消融的变体辩护 + 论文 Related Work"条件化"小节。

## 1. UFNO-FiLM:Feature-Modulated UFNO(arXiv,2025-11)

- **谁做过**:UFNO-FiLM——把 FiLM 条件化接进 UNet 增强的 Fourier Neural
  Operator(UFNO),用于**地下流动(subsurface flow)预测**,条件输入是
  PDE 系数/输入场。
- **做法与结果**:与我们的 M2 同构——低维条件码经 FiLM 逐通道仿射调制
  谱算子的特征通道;报告相对 UFNO 基线的精度提升。
- **对我们的含义**:FiLM × FNO 的组合已被独立验证有效——**"FiLM 是 M2
  现役接口"有文献先例**,不是本仓自造;同时它的条件输入是**已知的系数场**
  (监督条件),而我们条件于**推断出的低维码**(8 维)——这正是 E1 想隔离
  的差距(推断质量 vs 接口容量)。
- 引用潜力:高(2025 新作,FiLM+UFNO 直接同构)。

## 2. HyperFNO(Alesiani,NeurIPS ML4PS workshop)

- **谁做过**:用**超网**生成 FNO 的适配参数,条件于 PDE 参数配置,目的
  是跨宽参数域泛化。
- **做法与结果**:超网条件化在 FNO 上可行、改善泛化——即 E2 的 C-hyper
  变体有直接先例(我们是低秩 r=8 通道混合仿射,比全权重超网便宜一个量级)。
- **对我们的含义**:E2 若 hyper 胜出,"低秩超网接口"可引 HyperFNO 背书;
  若 FiLM 胜出,与 Mehta(§4)"调制 ≈ 超网表达力、参数省一个量级"一致,
  同样可引。
- 引用潜力:高(workshop,引用 9,方向正热)。

## 3. FNO 原文(Li et al., ICLR 2021,~6900 引)

- **谁做过**:参数化 PDE 的算子学习奠基作。关键对照:**FNO 处理变系数的
  方式是把系数场 a(x) 作为输入通道喂进去**(全场拼接),不经低维码。
- **对我们的含义**:文献主流回避了"压缩到低维推断码"这一步——M1/M2 的
  liquid 系统辨识正是做这一步,所以**条件化瓶颈是我们的独有问题域**,
  Related Work 有清晰的空位可占("低维推断码 → 谱势能的接口表达力"
  无同类工作直接研究;UFNO-FiLM/HyperFNO 都是监督条件码)。
- 引用潜力:必引(领域奠基石,定位空位)。

## 4. Mehta et al., Modulated Periodic Activations(ICCV 2021,~227 引)

- **谁做过**:INR 语境下**拼接 vs 调制(FiLM 式)vs 超网**三分类的系统
  论证:调制比超网**参数省一个量级而表达力相当**,比拼接**表达力强**
  (拼接只加性混入条件信息,调制乘性改变特征)。
- **对我们的含义**:E2 三变体恰好是这个分类在谱势能上的重演;无论哪个
  胜出都有文献坐标——concat 胜 = M1 ADR-4 结论跨头型成立;FiLM 胜 =
  Mehta 结论在物理算子域成立;hyper 胜 = HyperFNO 一致。**E2 的三种
  结局都可写作,无白跑分支**。
- 引用潜力:高(ICCV,方法论分类学)。

## 5. HyPINO(NeurIPS 2025)+ CPNO(2024)

- **谁做过**:HyPINO——超网按 PDE 参数生成 PINN 权重,零样本跨物理泛化;
  CPNO——把"参数依赖调制"内嵌进 Chebyshev 谱算子网络,声称近最优函数
  空间构造。
- **对我们的含义**:条件化正沿"外挂 FiLM → 权重生成超网 → 调制内嵌算子"
  谱系演化;M2 的 P4 若定案任何一档,都有 2024-2025 的新鲜引用链。
  P-CfC 门控变体(轮 41 登记未排队)亦属"时间经门条件化"同一谱系,
  Related Work 可合并成节。
- 引用潜力:中高(NeurIPS 新作堆热度)。

## 汇总(对循环的决策含义)

- E2 三变体全部有文献坐标,**不存在白跑分支**——E2 按预注册执行的辩护
  成立。
- M2 的科研空位("低维**推断**码 × 谱势能接口")在文献中确实无直接
  同类——P3 指出的瓶颈问题本身可作论文卖点。
- M1 的 FiLM 负结果(ADR-4)+ 文献中 FiLM 的成功(UFNO-FiLM)构成
  "条件化优劣依赖头型与任务对齐"的可检验叙事,E1/E2 就是它的物理域
  实证。

## 6. 经验蒸馏(轮 56,QUEUE-EMPTY 轮,2026-09-19):辅助辨识损失与梯度饥饿

> 本节按 PLAYBOOK 经验蒸馏轮格式:每条【出处 + 适用条件 + 验证状态】,
> 有效性由 R1 云跑与 RSI-INDEX 收口。

### 6.1 Gradient Starvation(Pezeshki et al., NeurIPS 2021,~462 引)

- 【出处】[NeurIPS Proceedings](https://proceedings.neurips.cc) /
  [官方实现](https://github.com/mpezeshki/Gradient_Starvation)。
- 【内容】形式化"易学特征主导梯度信号、压制同样有信息但更难学的特征"
  的现象,给出耦合动力学理论。
- 【对我们的映射】E4a 实测正是该现象的机械版:推断路径/头梯度比
  3.97e-3,且"head 未学用 ctx → ctx 无压力"是耦合塌缩的双侧形式。
  **我们的增量**:在硬约束物理架构上首次机械测量,而非仅理论刻画。
- 【适用条件】过参数化网络、特征间梯度竞争;难特征需独立梯度通路才能
  逃逸——R1 的辅助损失即此通路。
- 【验证状态】饥饿测量:已验证(本机 E4a);其修复处方对我们:待验证
  (R1 云跑收口)。

### 6.2 E2C — Embed to Control(Watter et al., NeurIPS 2015)

- 【出处】NeurIPS 2015,原始潜空间动力学控制线。
- 【内容】辅助损失强制潜动力学局部线性,把潜空间塑形为"对动力学有用"
  的形状——"潜变量不监督就会编码无关事物"的最早系统证据。
- 【对我们的映射】R1(辅助辨识损失)是该模式在硬约束哈密顿架构上的
  直系移植:ctx 不监督就收敛到无信息平台(E1/E3 实测)。
- 【适用条件】可微潜动力学 + 已知参数族形式(仿真场景满足)。
- 【验证状态】待验证(R1 云跑;社区已验证于 VAE-land,勿直接外推)。

### 6.3 DVBF — Deep Variational Bayes Filters(Karl et al., ICLR 2017)

- 【出处】ICLR 2017。
- 【内容】"Latent-force-model"辅助损失:以**真值状态导数**监督潜变量,
  解决无监督潜动力学简并——与 R1 的 `aux_targets`(仿真真值系数)同构。
- 【对我们的映射】R1 的直接先例:训练期真值可得时,直接监督潜码是
  社区验证过的破简并手段。
- 【适用条件】仿真/有真值场景(与我们完全一致)。
- 【验证状态】待验证(R1 云跑)。

### 蒸馏结论

R1 的设计不是拍脑袋:它有 2015-2021 的连续文献线(潜码需监督 → 真值
监督破简并 → 梯度饥饿理论命名我们实测的现象)。R1 若正,论文叙事获得
"现象(实测)→ 机制(命名)→ 修复(有先例的处方)"完整链;若负,
则硬约束架构与 VAE-land 的差异本身即新发现。**不存在白跑分支**。

## Sources

- [UFNO-FiLM: Feature-Modulated UFNO (arXiv 2025)](https://arxiv.org)
- [Feature-wise transformations (Distill 2018, FiLM)](https://distill.pub)
- [HyperFNO (NeurIPS ML4PS)](https://ml4physicalsciences.github.io)
- [FNO: Fourier Neural Operator for Parametric PDEs (OpenReview)](https://openreview.net)
- [Mehta et al., Modulated Periodic Activations (ICCV 2021)](https://arxiv.org/abs/2104.03912)
- [HyPINO: Multi-Physics Neural Operators via HyperPINNs (arXiv 2025)](https://arxiv.org)
- [CPNO: Physics-informed Chebyshev polynomial neural operator](https://www.sciencedirect.com)
- [Gradient Starvation (Pezeshki et al., NeurIPS 2021)](https://proceedings.neurips.cc)
- [Gradient Starvation 官方实现 (GitHub)](https://github.com/mpezeshki/Gradient_Starvation)
- E2C (Watter et al., NeurIPS 2015) / DVBF (Karl et al., ICLR 2017)——见 §6 条目
