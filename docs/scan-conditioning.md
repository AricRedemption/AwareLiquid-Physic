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

## 9. 经验蒸馏 4(轮 63,2026-09-19,QUEUE-EMPTY 轮):可辨识性与激励条件族

> 新 query 族(与前七族零重叠):persistent excitation、最优实验设计、
> concurrent learning。服务对象:E1 推断瓶颈的理论坐标 + Fisher 探针
> 工具的文献命名。

### 9.1 Persistent Excitation(自适应控制经典条件)

- 【出处】 adaptive control 系统辨识经典条件([ScienceDirect 综述](https://www.sciencedirect.com);线性情形 HAL 2023)。
- 【内容】PE 要求输入信号足够" rich "以保证参数收敛;是参数可辨识性
  的标准充分条件,且有"难以检验"的著名缺点(Papusha)。
- 【对我们的映射】`identifiability_probe.py` 的闭式 Fisher J(ω; t_obs)
  正是 PE 的**量化版**:观测窗对 ω 的激励充分度。E1 的叙事可借 PE
  词汇重述——"观测窗信息量(PE 充分度)是 oracle 上界的物理来源,
  推断器损耗是其上的实现缺口"。Related Work 引它可把本仓探针接进
  50 年的控制论文献线。
- 【适用条件】参数辨识场景;对哈密顿参数(ω、场系数)直接适用。
- 【验证状态】社区已验证(经典理论);命名/引用:立即可用。

### 9.2 Concurrent Learning(Chowdhary & Johnson, CDC 2010,~570 引)

- 【出处】Chowdhary & Johnson 2010(CDC/Georgia Tech PhD);finite-time
  扩展 Parikh, Kamalapurkar & Dixon(~265 引);近期 Koopman 统一批在线
  (Mazouchi et al., JMLR 2023)。
- 【内容】用**记录数据复用**(recorded data pairs)替代当前信号持续
  激励,在无 PE 条件下保证参数收敛——破 PE 的主流处方。
- 【对我们的映射】train_semigroup 每步**随机 t0 重采样**(train.py:150)
  本质是并发学习式数据复用:单窗不必持续激励,随机起点批的聚合覆盖
  等效于 PE。这为"训练循环设计"提供理论辩护,也是 E1 判读的背景:
  训练期信息覆盖 ≠ 单窗推断期信息——**推断器只拿一个 t_obs 窗,训练
  拿全轨迹聚合**,这个不对称正是 E1 所测推断瓶颈的另一面表述。
- 【适用条件】可记录历史数据的辨识/自适应控制;与 minibatch 随机
  采样天然相容。
- 【验证状态】社区已验证;对我们的适用判读:已判读(本轮,叙事级)。

### 9.3 最优实验设计 OED(Rojas et al. 2007,~311 引;Fisher 驱动)

- 【出处】[Rojas et al., min-max robust experiment design](https://www.sciencedirect.com)(~311 引);
  Fisher 信息矩阵驱动的最优输入设计(经典教材线);非线性期望信息增益
  ([Busetto et al., ICML](https://icml.cc))。
- 【内容】以 Fisher 信息最大化为准则设计输入/实验条件;鲁棒版对
  最坏情形参数取 min-max。
- 【对我们的映射】仿真仓里我们**控制生成过程**(ω 采样分布、S、t_obs、
  采样密度)——这就是 OED 的决策空间。现有闭式 J(ω; t_obs) 工具可
  零算力产出**可辨识性图谱**(J 随 t_obs 的平台位置),为 E1 的
  "信息预算分解"(窗口 Fisher 上界 vs oracle 可读出 vs 实际推断)提供
  物理上界坐标 → 已追加 D6-INFO-BUDGET(零算力判读目标)。
- 【适用条件】仿真数据可控生成场景(与我们完全一致)。
- 【验证状态】社区已验证;对我们待验证(D6 判读收口)。

### 蒸馏结论 4

本族给 D2-CAPACITY 叙事补上控制论文献线:窗口信息量有名字(PE)、
训练/推断的信息不对称有先例(concurrent learning 的聚合 vs 单窗)、
上界刻画有方法论(OED/Fisher)。产出一个零算力深化目标
D6-INFO-BUDGET(已入队尾):用现有 Fisher 工具把 E1 的 27% 差距
放进"信息预算"框架。两种结局都可写:平台存在 → E1 缺口是纯推断
损耗,叙事收紧;无平台 → 窗口信息仍在增长,oracle 上界解释需修正。
**不存在白跑分支**。

## 10. 经验蒸馏 5(轮 65,2026-09-19,QUEUE-EMPTY 轮):对称性与守恒律正则族

> 新 query 族(与前八族零重叠):时间反演一致性、Noether 式守恒正则。
> 服务对象:R1 之外的独立修复候选 + 架构选型(硬约束)的文献辩护。

### 10.1 时间反演对称一致性损失(Time-Reversal Symmetric ODE Networks, NeurIPS)

- 【出处】[TR-Symmetric ODE Networks (NeurIPS)](https://proceedings.neurips.cc);
  [TS-IDM (Cheng et al., OpenReview)](https://openreview.net);
  [TSDA (Barkley et al., ICML 2024)](https://arxiv.org)。
- 【内容】对时间可逆物理,训练加一致性正则:前向滚出 k 步后动量取反
  再滚 k 步应回到起点;或反向等价的数据增强。正则提升样本效率与 OOD
  泛化,无需额外监督。
- 【对我们的映射】弹簧/波场皆时间可逆,哈密顿头 + Verlet 积分天然
  支持反向滚出(积分器可逆)——一致性损失可零成本实现:
  `L_tr = ||rollout(rollout(s,k), −k) − s||`。**与 R1(辅助辨识损失)
  不同源但同属"给推断路径造梯度"家族**:R1 用真值系数监督,R1b 用
  物理一致性自监督——若 R1 云跑判负,R1b 是独立修复候选(条件性
  登记,见 GOALS 队列规则注记)。
- 【适用条件】时间可逆系统(我们全部任务满足)+ 可逆积分器(满足)。
- 【验证状态】社区已验证;对我们待验证(条件触发后预注册)。

### 10.2 Noether 式守恒:硬约束 vs 软正则二分(2023-2024 谱系)

- 【出处】[Noether's Razor (van der Ouderaa et al., NeurIPS 2024)](https://proceedings.neurips.cc);
  Noether Networks(meta-learned 守恒损失,2024);[Müller et al., SE(3) 精确守恒积分器 (2023, ~33 引)](https://www.sciencedirect.com);
  [Neural Mechanics (ICLR 2021)](https://ai.stanford.edu)(深度学习自身的守恒律,背景)。
- 【内容】守恒律进网络的两条路线:软(meta-learned 正则/学习守恒量)
  vs 硬(架构内建精确守恒)。
- 【对我们的映射】本仓能量守恒走**硬路线**(哈密顿头 + 辛积分,由
  构造保证,P0-3 实测漂移对照)——与 Müller 2023 同路线;N1 架构章
  可用"硬/软二分"定位我们的选型并引软路线作对照。Noether's Razor 的
  学习守恒量可在 M2 用作**诊断探针**(学出的守恒量是否恢复真值能量
  = c(x) 编码质量的独立读数),备用。
- 【适用条件】力学系统+已知守恒结构(硬);守恒量未知场景(软)。
- 【验证状态】社区已验证;架构辩护引用:立即可用。

### 蒸馏结论 5

本轮产出:① R1b 条件性修复候选(时间反演一致性,零监督成本,独立
于 R1 的真值监督路线——R1 判负时仍有处方,降低"R1 白跑"风险);
② N1 架构章的硬/软二分辩护坐标。**方向类按条件性登记**(仿 E2 先例
不入队,防路由器空转);触发条件:R1/R2 云结果回传且判负。

### 10.3 判读回填(轮 66,R1b 可行性)

- **前提判读否决了"零成本"预期**:当前 HamiltonianHead 的 T 是非偶
  MLP,动量翻转回程 1 步即失配(实测见 PRD §19 轮 66)——10.1 的
  "一致性损失可零成本实现"修正为:**先补 T 偶结构(硬参数化)或以
  一致性损失软教偶性,再谈回程一致**。
- 升级:R1b 从"免费正则"变为"真物理归纳偏置"(真系统动能偶)——
  与辨识目标的交互是待验证研究问题,判负标准届时预注册。
- 架构诚实性:能量守恒(无条件)与时间反演对称(T 偶才成立)是两个
  独立性质,docstring 已修订。

## 11. 经验蒸馏 6(轮 67,2026-09-19,QUEUE-EMPTY 轮):神经算子谱实践族

> 新 query 族(与前九族零重叠):谱混叠/谱偏置、分辨率不变性边界。
> 服务对象:M2 FNO 头的实践辩护 + 未来云结果的解读坐标。
> 条目标记:**[坐标]** = 解读用,不触发目标;**[行动]** = 触发目标/协议。
> (轮 67 起,蒸馏条目强制分流标记,防坐标类条目撑大队列。)

### 11.1 谱混叠与不可约误差 [坐标]

- 【出处】FNO 实践综述([ResearchGate 2025](https://www.researchgate.net));
  不可约混叠/人工耗散报告([EmergentMind 2025](https://www.emergentmind.com));
  高频监督缓解谱偏置([arXiv 2025](https://arxiv.org))。
- 【内容】FNO 高频分量混叠进低频产生伪振荡;部分混叠误差**不随训练
  数据规模消失**;缓解靠模态截断纪律、高频监督、渐进谱训练。
- 【对我们的映射】与 §8.2(低幅局限)交叉:若云回传结果显示"能量
  统计对但高频细节糊",**混叠/谱偏置是候选解释**(候选解释清单 +
1:容量——E3 已否定;饥饿——E4a 已确认待 R1;混叠——本条)。
  另:训练/推理网格 Nyquist 一致性是口径纪律(我们评测同网格,无此
  混淆)。
- 【适用条件】谱域算子头(M2 OperatorPotentialHead,n_scales 模)。
- 【验证状态】社区已验证;对我们:待云数据触发解读(条件性)。

### 11.2 分辨率不变性的实证边界 [坐标]

- 【出处】[FNO vs CNN 跨分辨率实证 (Research Square 2025)](https://assets-eu.researchsquare.com);
  [Neural Spectral Methods (ICLR 2024)](https://proceedings.iclr.cc)。
- 【内容】FNO 训练截断外的零样本超分**实证退化**——分辨率不变性
  是"结构上可迁移",不是"精度不变"。
- 【对我们的映射】M2 resolution 对照(d2_m2_loop)若现高分辨率 MSE
  退化:预期内(FNO 文献一致),写论文时引此定调"结构迁移成立、
  精度迁移有界",防评审误读。
- 【适用条件】跨分辨率评测的谱算子。
- 【验证状态】社区已验证;对我们:待解读触发(条件性)。

### 蒸馏结论 6

本轮两条均为 [坐标] 类:不新增目标(云回传前无行动点),但把"高频
糊化"的候选解释清单补全(容量✗/饥饿✓待R1/混叠✓本条),给 R2 判读
预留解读框架。蒸馏轮第 4 次达标(交付 2 条入库)。

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
