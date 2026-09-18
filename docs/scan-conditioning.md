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

## 7. 经验蒸馏 2(轮 59,2026-09-19):隐藏集与多种子报告规范

- 【出处】[CNO / Representative PDE Benchmarks (Raonic et al., ~330 引)](https://openreview.net);
  PDEBench(Takamoto et al., NeurIPS 2022);The Well(2024)。
- 【内容】神经 PDE 评测的标准化努力集中在 **OOD/鲁棒性基准**(RPB、
  PDEBench、The Well);检索证据显示**多种子/隐藏集报告规范极少成文**
  ——公认空白。
- 【对我们的映射】本仓的 RSI-Exam 实践(预注册一次性隐藏集终跑、
  轮 44 首夜即抓可见集过拟合反转、G2 的跨 pool 几何均值报告)恰好落在
  该空白上——**论文 §5 自主循环小节的 novelty 声明有据**:不是我们自说
  自话,是社区规范缺失而我们给出了可执行协议。
- 【适用条件】一切"单次训练+可见集刷分"式结论的论文;对sim2real/
  隐藏参数族任务尤其成立。
- 【验证状态】规范空白:已验证(检索侧);我们的协议有效性:已验证
  (轮 44 真抓到反转)——可直接写进论文。

### 蒸馏结论 2

N1 的 Related Work 已有"自主研究循环"小节;本条给它的 novelty 补上
文献坐标系(现有基准推进 OOD,但预注册+隐藏集+跨 seed 几何报告的
完整协议无成文先例)。写作时引用 CNO-RPB/PDEBench 作为"评测标准化
努力"的最近邻,然后指出隐藏集维度空白。

## 8. 经验蒸馏 3(轮 61,2026-09-19,QUEUE-EMPTY 轮):长时程滚出稳定性与多步训练族

> 新 query 族(与前六族零重叠):pushforward/多步滚出损失、辛积分
> 网络训练、exposure bias 处方谱系。直接服务滚出 MSE 评测口径的辩护
> 与 N1 Related Work。

### 8.1 Pushforward trick 与自回归分布漂移(Brandstetter et al., ICLR 2022)

- 【出处】[Message Passing Neural PDE Solvers (arXiv:2202.03376)](https://arxiv.org/pdf/2202.03376);
  [ICLR blog 重述(2023)](https://iclr-blogposts.github.io/2023/blog/2023/autoregressive-neural-pde-solver)。
- 【内容】诊断:自回归神经求解器**训练吃真值前缀、测试吃自己的预测**
  → 输入分布漂移 → 误差复利,长滚出崩。处方 pushforward trick:训练时
  下一步输入改用模型自身滚出(detach),配合多步/全展开损失。
- 【对我们的映射】我们的评测口径正是自回归滚出 MSE,而训练循环
  (prefix/semigroup)是否暴露于自预测**未系统判读过**——若训练全吃
  真值前缀,则存在与评测口径的结构性 exposure gap,这可能是滚出误差
  的一个未被归因过的来源(D1-D4 均未涉及此因子)。
- 【适用条件】自回归多步预测 + 一步式/短展开训练;对仿真数据同样成立。
- 【验证状态】社区已验证(ICLR 2022 高引);**对我们待验证**——零算力
  代码判读先行(→ D5-EXPOSURE 入队)。

### 8.2 Pushforward 的低幅信息局限(Havrilla et al.?, NeurIPS 2023)

- 【出处】[Achieving Accurate Long Rollouts with Neural PDE Solvers (NeurIPS 2023)](https://papers.neurips.cc/paper_files/paper/2023/file/d529b943af3dba734f8a7d49efcb6d09-Paper-Conference.pdf)。
- 【内容】pushforward 解决输入漂移但**捕捉不了低幅信息**,长程统计
  (谱/能量)仍不准;需时间展开加权/谱修正补足。
- 【对我们的映射】能量守恒由构造保证(硬约束),低幅问题在我们这里
  会表现为**高频细结构糊化而能量统计正常**——若未来滚出判读出现
  "能量对但细节糊",此条即坐标,防止误判为容量问题。
- 【适用条件】长程统计评测的滚出模型;我们暂未到该判读阶段。
- 【验证状态】社区已验证;**对我们暂不适用**,备用注记。

### 8.3 SRNN:辛递归网络(Chen et al., ICLR 2020,~372 引)

- 【出处】[Symplectic Recurrent Neural Networks (arXiv:1909.13334)](https://arxiv.org/abs/1909.13334);
  [官方实现](https://github.com/zhengdao-chen/SRNN)。
- 【内容】神经网络哈密顿量 + leapfrog(Störmer–Verlet)积分器展开 +
  多步 BPTT 训练;展示对噪声哈密顿系统的稳定滚出。
- 【对我们的映射】"哈密顿头 + 辛积分滚出"结构的直系先例——Related
  Work 必引;其多步展开训练与我们滚出损失的对应关系按 D5 判读收口。
- 【适用条件】可微哈密顿参数化 + 可积积分器(与我们一致)。
- 【验证状态】社区已验证;引用:立即可用。

### 8.4 Exposure bias 处方谱系(Bengio 2015 → Professor Forcing 2016 → DySI 2023)

- 【出处】Scheduled Sampling(Bengio et al., NeurIPS 2015);[Professor Forcing (Lamb et al., NeurIPS 2016)](https://papers.nips.cc)——其 T-SNE 证据显示训练后自由滚出与 teacher-forced 两种模式的**隐藏状态动力学**对齐;DySI(Lin et al., 2023, OpenReview)修正 schedule 缺陷。
- 【内容】exposure bias 的三代处方:采样课程 → 对抗对齐动力学 → 模仿损失。
- 【对我们的映射】prefix(teacher-forced)与 semigroup(自回归)双训练
  循环的分歧是 exposure bias 的架构内版本;D5 若量化出 gap,处方可从
  本谱系直接取(pushforward 是 PDE 版 scheduled sampling)。
- 【适用条件】序列/动力学模型的 teacher-forcing 训练。
- 【验证状态】社区已验证;对我们待 D5 判读后适用。

### 蒸馏结论 3

本轮产出一个**零算力深化目标**(已追加 GOALS 队尾):D5-EXPOSURE
——判读训练循环输入构造与滚出评测口径的一致性。两种结局都可写:
gap 存在 → 新归因因子 + 预注册 pushforward 协议(云交付);gap 不存在
→ 评测口径辩护成立 + 8.3/8.4 收进 Related Work。**不存在白跑分支**。

### 8.5 判读回填(轮 62,D5-EXPOSURE 结案)

- **8.1 pushforward:不适用(已判读)**——本仓训练与评测的滚出段
  同为自回归(训练损失直接吃自预测,`train_semigroup` 与两处 eval
  逐路径证据见 PRD §19 轮 62 记录),pushforward 所修的
  teacher-forced→free-running 漂移由构造消除。
- **8.2 低幅局限:不适用(前提同上,备用注记保留)**。
- **8.3 SRNN:引用生效**——Related Work 必引清单已落 PRD §19 轮 62。
- **8.4 exposure-bias 谱系:降为背景引用**(gap 不存在,无修复需求)。
- 辩护价值:全部滚出 MSE 数字(R1/R2/E/D 系列)不受 exposure bias
  混淆,评测口径辩护成立。

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
- [CNO / Representative PDE Benchmarks (OpenReview)](https://openreview.net)——见 §7
