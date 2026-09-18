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

## Sources

- [UFNO-FiLM: Feature-Modulated UFNO (arXiv 2025)](https://arxiv.org)
- [Feature-wise transformations (Distill 2018, FiLM)](https://distill.pub)
- [HyperFNO (NeurIPS ML4PS)](https://ml4physicalsciences.github.io)
- [FNO: Fourier Neural Operator for Parametric PDEs (OpenReview)](https://openreview.net)
- [Mehta et al., Modulated Periodic Activations (ICCV 2021)](https://arxiv.org/abs/2104.03912)
- [HyPINO: Multi-Physics Neural Operators via HyperPINNs (arXiv 2025)](https://arxiv.org)
- [CPNO: Physics-informed Chebyshev polynomial neural operator](https://www.sciencedirect.com)
