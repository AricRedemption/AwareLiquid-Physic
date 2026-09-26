# 条件化接口文献/GitHub 扫描(G4-SCAN,2026-09-19)

> 问题:M2 的 context→势能条件化(FiLM 通道仿射)在算子学习文献里的
> 同类实践是什么、谁做过、失败/成功在哪。按学术引用潜力排序。
> 服务对象:E2 接口消融的变体辩护 + 论文 Related Work"条件化"小节。

## 1. UFNO-FiLM:Feature-Modulated UFNO(arXiv,2025-11)

> SCAN-AUDIT 修订(轮 94):题录升级——**Abdellatif et al., 2025**
> (Heriot-Watt;arXiv ID 待补,见 scan-traceability-audit.md §6.4)。
> 原记录仅年月,升级后 B→A。

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

> SCAN-AUDIT 修订(轮 94):题录升级——Alesiani,**NeurIPS ML4PS 2022**
> workshop(全文 PDF:ml4physicalsciences.github.io/2022/files/
> NeurIPS_ML4PS_2022_89.pdf);原记录缺年份,补 2022。B→A。

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
- SCAN-AUDIT 降档注记(轮 94):上文"无同类工作直接研究"按 AMM-015 降档
  为"**当前 query 族下未检索到同类**(轮 43 检索口径)"——存在性命题的
  最弱证据不配最强断言。

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

> SCAN-AUDIT 修订(轮 94):① HyPINO 题录升级——**Bischof et al.
> (ETH Zurich), NeurIPS 2025**(arXiv ID 待补);② CPNO 题录
> **事实错误修正**——原记"2024"实为 **Biao Chen et al.,
> arXiv:2602.01737(2026-02 预印)**,检索一致定年 2026。

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
  (SCAN-AUDIT 降档注记,轮 94:"首次"按 AMM-015 降档为"**据当前
  检索未见先例**——非证真首创"。)
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
  ——当前 query 族下未检索到成文规范(轮 88 治理轮修订:原"公认空白"
  系弱检索下的过强断言,按 AMM-015 缺证性降档规范改写;§映射 novelty
  声明强度相应降为"检索未见,非证真空白")。
- 【对我们的映射】本仓的 RSI-Exam 实践(预注册一次性隐藏集终跑、
  轮 44 首夜即抓可见集过拟合反转、G2 的跨 pool 几何均值报告)恰好落在
  该空白上——**论文 §5 自主循环小节的 novelty 声明有据**:不是我们自说
  自话,是社区规范缺失而我们给出了可执行协议。
- 【适用条件】一切"单次训练+可见集刷分"式结论的论文;对sim2real/
  隐藏参数族任务尤其成立。
- 【验证状态】规范空白:已验证(检索侧);我们的协议有效性:已验证
  (轮 44 真抓到反转)——可直接写进论文。
  (SCAN-AUDIT 修订,轮 94:上行"已验证(检索侧)"违反 AMM-015 禁令
  ——轮 88 只降档了内容行,本状态行漏网;降档为"**检索未见(非证真
  空白)**"。)

### 蒸馏结论 2

N1 的 Related Work 已有"自主研究循环"小节;本条给它的 novelty 补上
文献坐标系(现有基准推进 OOD,但预注册+隐藏集+跨 seed 几何报告的
完整协议无成文先例)。写作时引用 CNO-RPB/PDEBench 作为"评测标准化
努力"的最近邻,然后指出隐藏集维度空白。
(SCAN-AUDIT 降档注记,轮 94:"无成文先例"降档为"当前 query 族下
未检索到成文先例";CNO 主锚题录升级:Raonic et al., arXiv 2022,
ETH 2023 修订版,~331 引。)

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

> SCAN-AUDIT 修订(轮 94,**事实错误修正**):本文实为 **PDE-Refiner——
> Lippe, Veeling, Perdikaris, Turner & Brandstetter, NeurIPS 2023,
> arXiv:2308.05732**。原记"Havrilla et al.?"系作者误记(链接与题名
> 无误);带?题录不得过夜的坑已入 PLAYBOOK。

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

> SCAN-AUDIT 注记(轮 94):本条主锚无作者题录(综述根链+HAL 无作者)
> ——B 级,整改登记 scan-traceability-audit.md §7(下一蒸馏轮补经典
> 教材题录+HAL 预印本作者)。
>
> SCAN-AUDIT 整改回填(轮 101):**B→A**——主锚补精确题录:① PE 经典
> 教材定义 = Slotine & Li,"Applied Nonlinear Control",Prentice Hall,
> 1991(PE 条件 §8.31);② 线性情形锚定 Green & Moore,"Persistence of
> excitation in linear systems",Systems & Control Letters,1986(~212 引);
> 原"HAL 2023"链接未能钉住作者,**弃用改锚** Green & Moore(原文
> 保留不改写)。

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

> SCAN-AUDIT 修订(轮 94):主锚题录升级——Time-Reversal Symmetric
> ODE Network = **Huh, Kang, Chun, Kim & Kim(KAIST), NeurIPS 2021,
> arXiv:2007.11362**;原记录无作者年份。B→A。

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

> SCAN-AUDIT 注记(轮 94):三条出处均为聚合站根链(RG/EmergentMind/
> arXiv 根),无作者题录——B 级,整改登记 scan-traceability-audit.md
> §7(下一次云回传证据轮按需逐条补 ID;该组条目语义为社区共识实践,
> 引用前必须先补题录)。
>
> SCAN-AUDIT 整改回填(轮 101):**B→A(部分,1 断言降格)**——两条聚合
> 链升级为精确锚(均为本档已有记录的交叉引用):① "高频监督缓解谱偏置"
> = §17.3 的 Khodakarami et al. 2025(HFS,arXiv 2025-03,osti 链);
> ② "FNO 谱偏置实践" = §17.1 的 Xu et al. 2025(ScienceDirect,62 引,
> MscaleFNO)。③ EmergentMind"部分混叠误差不随训练数据规模消失"的
> 原始论文**未能定位** ⇒ 该断言**降格为"未复核"(不得以强断言引用)**;
> 条目其余主张(混叠伪振荡+缓解三策略)由两个精确锚支撑。

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

> SCAN-AUDIT 修订(轮 94):主锚题录升级——**Resolution-Invariant
> Fluid Dynamics Modeling: Fourier Neural Operator**(Research Square
> rs-8218223, 2025-11,全文 PDF 路径可定位)。原仅资产根链。B→A。

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

## 12. 经验蒸馏 7(轮 68,2026-09-19,QUEUE-EMPTY 轮):摊销推断/神经过程族

> 新 query 族(与前十一族零重叠):amortization gap、NP/ANP 聚合
> underfitting。直接对话 E1 推断瓶颈的文献命名与第三条修复路线。
> 标记:[坐标]=解读用;[行动]=触发条件性入口。

### 12.1 Amortization gap:E1 推断瓶颈的文献命名 [坐标+命名]

- 【出处】[Inference Suboptimality in VAEs (Cremer et al., ICML 2018, ~410 引)](http://proceedings.mlr.press/v80/cremer18a/cremer18a.pdf);
  [Iterative Amortized Inference (Marino et al.)](https://la.disneyresearch.com/publication/iterative-amortized-inference);
  [Generalization Gap in Amortized Inference (NeurIPS 2022)](https://proceedings.neurips.cc/paper_files/paper/2022/file/ab41313eaa3cbedbe491c24cbfe6547d-Paper-Conference.pdf)。
- 【内容】摊销推断(编码器一次映射到潜变量后验)与逐实例优化之间存在
  **amortization gap**;与 approximation gap 可分;缓解靠迭代细化/实例
  自适应参数化;摊销网络过拟合可主导泛化差距。
- 【对我们的映射】**E1 的"推断瓶颈"(oracle −27% 兑现于同一接口)
  结构上就是 amortization gap**:oracle 臂=跳过推断直接注入真值
  (逐实例上界),liquid 臂=一次性摊销编码器(infer_context(prefix))。
  N1 论文可直接引 Cremer 2018 给 E1 命名,把物理域结果接进 VI 文献线;
  D1 小样本线可引 NeurIPS 2022(摊销过拟合)作背景。
- 【适用条件】编码器摊销潜变量的一切架构(我们满足)。
- 【验证状态】社区已验证;命名/引用:立即可用。

### 12.2 NP/ANP 聚合 underfitting:R1c(聚合瓶颈)候选 [行动→条件性]

- 【出处】[Conditional Neural Processes (Garnelo et al., 2018)](https://yanndubs.github.io/Neural-Process-Family/text/LNPF.html);
  [Attentive Neural Processes (Kim et al., ICLR 2019, ~678 引)](https://openreview.net)——
  vanilla NP 的 **mean 聚合低估 context 信息(underfitting)**,attention
  聚合是社区验证的修复。
- 【对我们的映射】M2 的 infer_context 管线对空间维用 **mean-pool**
  (`model.py`:per-node 共享 Linear → mean-pool over nodes → liquid
  core)——与 vanilla NP 的均值聚合同型。E1 实测 ctx 对 c(x) 场系数
  信息不足,候选机制之一:**空间结构被均值池化压掉**(c(x) 是空间场,
  均值是它的低维投影)。修复候选 **R1c:attention/可学习聚合替代
  mean-pool**(独立于 R1 监督/R1b 结构的第三条路线)。
- 【适用条件】潜变量来自空间/集合结构的摊销编码(我们满足)。
- 【验证状态】社区已验证(ANP 678 引);对我们待验证(R1c 条件性,
  代码前提已判读:mean-pool 在 model.py 编码管线中确认)。

### 12.3 云回传判负时的三路分流(判读逻辑,轮 68 定稿;轮 77 追加第四路)

R1(辅助辨识损失)若判负,按失败模式选路:
- ctx 探针仍 ≈0(信息没进来)→ **R1c**(聚合瓶颈,attention 池化);
- ctx 有信息但滚出 MSE 不兑现 → 结构路线 **R1b**(T 偶/回程)或接口
  消融 **E2**(视 ρ_CB′);
- ctx 有信息且兑现但仅部分 → 监督强度/权重曲线(**R1 权重扫描**)。
三条路线相互独立、处方可叠加,不存在"全判负则无处可去"分支。
- **轮 77 追加(谱偏置族,§17.3):表征轴第四路 R1d**——R1b/R1c 均
  未兑现缺口收敛时,ctx(或 q)输入的 **Fourier 特征重参数化/高频
  缩放**(反制谱偏置,处方谱系见 §17.3)与监督(R1)/结构(R1b)/
  聚合(R1c)三轴正交可叠加;先决条件:SB-NAMING 文档的命名对账
  成立(判负标准届时预注册)。新增路线,不改轮 68 原判定行。

### 蒸馏结论 7

E1 机制链获得 VI 文献命名(amortization gap)+ 第三条独立修复候选
(R1c,代码前提 mean-pool 已定位)。修复路线谱系补全:
R1(监督)/R1b(结构)/R1c(聚合器)——云回传判读按 12.3 分流。
**[行动] 条目走条件性登记**(GOALS 注记,仿 R1b 先例)。

## 13. 经验蒸馏 8(轮 70,2026-09-19,QUEUE-EMPTY 轮):LTC/CfC 工程前沿族

> 新 query 族(与前十二族零重叠;轮 45 扫的是 system-ID 角度,本轮是
> 基座工程角度)。标记:[坐标]。

### 13.1 CfC 闭式基座:选型出处与精度边界 [坐标]

- 【出处】[Closed-form continuous-time neural networks (Hasani et al., Nature MI 2022, ~394 引)](https://www.nature.com);
  [官方实现 raminmh/CfC](https://github.com/raminmh/CfC)。
- 【内容】CfC = LTC ODE 的解析近似,免数值求解器,训练/推理加速
  10¹–10⁵×;基准上常匹配或超过完整 ODE 积分的 LTC。
- 【对我们的映射】本仓 liquid_core.py 即闭式 LTC 路线(= CfC 家族)——
  N1 基座小节必引。诚实 scope 补充:E1 的推断链在 amortization gap
  (§12.1)之下还有一层 **闭式近似的 approximation 层**——oracle 与
  liquid 的 −27% 缺口中,理论上可分离"推断器学不到"(摊销)与
  "闭式族表达不了"(近似)两个子层;当前实验未分离,论文可作为
  limitation 或后续工作注记(不改变现有结论,oracle 上界对两子层
  一视同仁)。
- 【适用条件】连续时间序列基座;我们满足。
- 【验证状态】社区已验证;引用:立即可用。

### 13.2 CfC 工程应用活跃度(2024-2025) [坐标]

- 【出处】[滑模控制应用 (Urrea et al., MDPI 2024, 9 引)](https://www.mdpi.com);
  医疗数字孪生/不规则采样时序/闭环控制应用线(2025 综述)。
- 【内容】CfC 在控制与医疗时序持续落地,社区活跃。
- 【对我们的映射】"liquid 系统辨识"研究载体的活跃性证据(论文
  introduction 的领域热度句可引);P-CfC 门控变体(轮 41 登记)若
  日后入队,有应用文献背书。
- 【验证状态】社区已验证;引用:立即可用。

### 蒸馏结论 8

基座选型(CfC 闭式)获得 canonical 出处与活跃度证据;E1 的诚实 scope
补一层(摊销 gap 之下的闭式近似层,未分离,作 limitation 注记)。
本轮全 [坐标],不新增目标(闭式 vs ODE 消融属新实验,优先级让位
R1/R2 回传)。蒸馏轮第 6 次达标(交付 2 条入库)。

## 14. 经验蒸馏 9(轮 71,2026-09-19,QUEUE-EMPTY 轮):观测噪声与 sim-to-real 族

> 新 query 族(与前十三族零重叠);触发:轮 71 代码判读发现本仓数据
> 无观测噪声(datasets.py 的 randn 全为初始状态抽样,无噪声项)。
> 标记:[坐标]。

### 14.1 无噪仿真训练的真实数据泛化边界 [坐标]

- 【出处】[Provable Observation Noise Robustness (arXiv:2312.00301)](https://arxiv.org/abs/2312.00301);
  [Robust ID of Partially Observed Systems (arXiv:2504.18076)](https://arxiv.org/abs/2504.18076);
  深度学习+系统辨识噪声分析(IFAC);噪声注入正则(IEEE 2020)。
- 【内容】文献一致:无噪仿真训练的模型对噪声真实观测泛化弱;
  处方 = 训练期噪声注入(数据增强)/可证鲁棒认证/去噪架构。
- 【对我们的映射】① 本仓数据无噪 ⇒ 现有结论的范围声明须写
  "noise-free simulation system identification"(N1 自洽,防评审
  sim-to-real 追问);② D6 的 CRB(σ=1)是**保守假设值**——真实数据
  无噪,层 1(窗口物理信息)非瓶颈的结论加强(代码判读注记已入
  PRD §19 轮 71);③ 未来若开噪声鲁棒线:噪声注入增强是首处方,
  届时预注册。
- 【适用条件】仿真数据训练的一切本仓实验。
- 【验证状态】社区已验证;范围声明引用:立即可用。

### 蒸馏结论 9

一条代码判读(datasets 无噪确认)+ 一条 [坐标] 入库(sim-to-real
边界与处方)。蒸馏轮第 7 次达标。

## 15. 经验蒸馏 10(轮 73,2026-09-19 12:23,QUEUE-EMPTY 轮):耗散/端口哈密顿结构族

> 第 15 个 query 族,与前十四族零重叠——结构扩展轴此前只扫过守恒系
> (SRNN §8.3、时间反演/Noether §10),耗散结构首扫。触发:R1/R2 云
> 回传未到,按 AMM-006 蒸馏补池。检索:3 族一次命中(port-HNN /
> Rayleigh 耗散 HNN / 耗散×辛训练稳定性)。
> 标记:[坐标] ×3 + [行动] ×1(→ DH-DESIGN 入队)。

### 15.1 D-HNN:哈密顿+Rayleigh 耗散分离参数化 [坐标+行动→DH-DESIGN]

- 【出处】[Dissipative Hamiltonian Neural Networks (Sosanya & Greydanus,
  arXiv:2201.10085)](https://arxiv.org/abs/2201.10085);
  [官方 PyTorch 实现](https://github.com/greydanus/dissipative_hnns);
  [作者博客](http://greydanus.github.io/2022/01/25/dissipative-hnns)。
- 【内容】两个网络分别学 H(q,p) 与 Rayleigh 耗散函数 R(q,p):
  q̇=∂H/∂p, ṗ=−∂H/∂q−∂R/∂p。保守/耗散显式解耦,耗散通道可解释。
- 【对我们的映射】① 当前头能量守恒由构造(P0-3)⇒ 无法表达任何
  能量衰减——对保守基准是优点,对真实系统叙事是**显式边界**(N1
  Related Work 必答"真实系统耗散怎么办");② 最小扩展形态:
  HamiltonianHead 加 Rayleigh 槽位,默认关,R≡0 与现状逐位等价;
  ③ **与 T 偶(R1b)的结构交互**:Rayleigh 力 −∂R/∂p(R 二次型)
  是 p 奇函数 ⇒ 耗散系统物理上时间反演不可逆——守恒部分 T 偶
  参数化与耗散部分正交、可叠加;回程一致性冒烟仅对保守部分适用。
- 【适用条件】保守+耗散混合动力系统;本仓当前基准(弹簧/波场)
  全保守 ⇒ 扩展不改变任何现有结论,纯预留位+N1 坐标。
- 【验证状态】社区已验证(damped oscillator 等任务);对本仓待验证
  (判据已预注册 PRD §19 轮 73)。

### 15.2 Port-HNN:(J−R)∇H 结构分解与能量单调由构造 [坐标]

- 【出处】[Port-Hamiltonian Neural Networks (Desai et al., Phys. Rev. E
  2021, ~147 引)](https://link.aps.org);
  [Stable Port-Hamiltonian NN (Roth et al., NeurIPS 2025 poster, ~26 引)](https://openreview.net/forum?id=epIGnGgcKD);
  [Port-metriplectic NN (Hernández et al. 2023)](https://cnam.hal.science)。
- 【内容】ẋ=(J(x)−R(x))∇H(x):J 反对称(储能/互联)、R 半正定
  (耗散);梯度结构直接给 dH/dt=−∇HᵀR∇H≤0——**能量单调由构造
  保证**,与本仓 P0-3"守恒由构造"同一哲学。Roth 2025 加稳定性
  保证与耗散元件建模;port-metriplectic 扩到热力学双结构。
- 【对我们的映射】DH-DESIGN 若开工,形态二选一:port 形态的
  "单调由构造"哲学同构但改动面大;D-HNN 形态实现最薄(仅加一项
  力),适合最小槽位。设计文档须两形态对照后定夺并写明取舍。
- 【适用条件】需要能量单调/稳定性结构保证的耗散系统学习。
- 【验证状态】社区已验证(Desai 147 引;Roth NeurIPS 2025);
  本仓未验证(设计轮评估)。

### 15.3 耗散×辛积分器的数值边界 [坐标]

- 【出处】检索综合:[contact 变分原理 HLNN (APS 2025)](https://link.aps.org/doi/10.1103/9gnh-89jd);
  [Exact conservation laws for NN integrators (Müller et al. 2023)](https://www.sciencedirect.com);
  D-HNN 实现细节(greydanus/dissipative_hnns)。
- 【内容】显式辛积分器 + Rayleigh 力通常需分裂步(守恒子步辛 +
  耗散子步显式),长期稳定性的定量证据在文献中弱于纯守恒情形;
  contact 哈密顿是另一数值载体。
- 【对我们的映射】DH-DESIGN 判负标准之一预注册于此:若分裂步在
  leapfrog 框架下引入不可接受的能量伪注入(闭式阻尼谐振子探针
  单调性失败),则"辛可比+耗散"在本仓积分器上不可兼得——判负
  如实入档,坐标留 N1,不硬凑。
- 【适用条件】任何给辛滚出加耗散项的实现。
- 【验证状态】社区部分验证(方法存在,稳定性边界未定量化);
  对本仓待验证(探针判据已预注册)。

### 蒸馏结论 10

三 [坐标] + 一 [行动](DH-DESIGN 入队,check_cmd 双锚:PRD 判读锚
+设计文档产物锚)。本族把"真实系统耗散"从 N1 隐式边界升级为显式
坐标+架构预留位;与 R1b(T 偶)的结构交互已标注(正交可叠加)。
蒸馏轮第 8 次达标。

## 16. 经验蒸馏 11(轮 75,2026-09-19 12:50,QUEUE-EMPTY 轮):Koopman/流映射算子学习族

> 第 16 个 query 族,与前十五族零重叠——与 M1 半群训练循环**机制直连**
> 的最近邻文献族首次扫描。检索:3 族一次命中(综述 / 半群机制关键词 /
> "Koopman vs Hamiltonian" 对照式)。标记:[坐标] ×3 + [行动] ×1
> (→ KM-BRIDGE 入队)。

### 16.1 Deep-OSG/OSG-Net:半群性质作为学习目标 [坐标]

- 【出处】[Deep-OSG (Chen et al., J. Comput. Phys. 2023, ~17 引)](https://www.sciencedirect.com);
  [OSG-Net (SIAM)](https://epubs.siam.org);neural flow maps 谱系。
- 【内容】对未知自治动力系统,用 DNN 学流映射(flow map)并**直接
  处理半群性质**(时间平移复合封闭)——与 `train_semigroup`
  "k 步滚出损失对 k 索引一致"的训练循环机制同题。
- 【对我们的映射】N1 Related Work **直系先例,必引**:本仓半群线的
  差异 = ① 半群训练作用于**结构化**滚出(哈密顿头+辛积分器)而非
  自由流映射 DNN;② 与 context 推断(liquid 基座)耦合,Deep-OSG
  无情境通道。评审若问"半群训练和 flow-map learning 什么关系",
  本条即答案。
- 【适用条件】一切涉及 train_semigroup 的写作与答辩。
- 【验证状态】社区已验证;定位引用立即可用。

### 16.2 Koopman 主线坐标:可观空间线性化(综述) [坐标]

- 【出处】[Modern Koopman Theory (Brunton et al., SIAM Review 2022, ~1168 引)](https://epubs.siam.org);
  [Koopman models: learning, analysis and control (Bevanda et al. 2021, ~344 引)](https://www.sciencedirect.com);
  [kooplearn 库](https://github.com)。
- 【内容】Koopman 算子把非线性状态动力学提升为**可观函数空间的
  全局线性**算子;优势 = 谱分解工具箱 + 对观测噪声的鲁棒性;
  代价 = 无能量/守恒结构保证,提升空间维度高。
- 【对我们的映射】N1 定位一句话:**本仓线 = 状态空间结构化
  (canonical 方程 + 辛积分器,守恒由构造),Koopman 线 = 可观空间
  线性化(鲁棒、谱工具),两者正交**;§14 已判本仓数据无噪 ⇒
  Koopman 的鲁棒性优势在本范围不构成威胁,仅在噪声扩展线上成为
  对照选项(与 16.3 呼应)。
- 【适用条件】N1 Related Work 与评审答辩。
- 【验证状态】社区已验证;定位引用立即可用。

### 16.3 Hamiltonian Neural Koopman:混合线坐标 [坐标]

- 【出处】[Learning Hamiltonian neural Koopman operator (Zhang et al. 2024, ~20 引)](https://link.aps.org);
  [Physics-informed deep Koopman for Lagrangian systems (Wang et al. 2024)](https://link.springer.com)。
- 【内容】混合线把 Koopman 线性化与哈密顿结构叠加("可观空间线性 +
  能量结构先验"),卖点恰是**噪声扰动数据上的鲁棒学习**。
- 【对我们的映射】① 必引(最接近的混合先例);② 本仓差异 =
  液基 **context 推断**(观测前缀→能量景观条件化)在 Koopman/HNK
  两线中均无对应物;③ 若未来开噪声线(scan §14 处方谱系),
  HNK 是现成对照臂候选。
- 【适用条件】N1 Related Work;噪声扩展线的对照设计。
- 【验证状态】社区已验证;本仓对照未验证(条件性,噪声线不开则不适用)。

### 蒸馏结论 11

三 [坐标](Deep-OSG 直系先例 / Koopman 综述定位 / HNK 混合线)+
一 [行动](KM-BRIDGE 入队:Koopman/流映射 vs 本仓半群线的定位文档,
N1 Related Work 素材,判负标准预注册 PRD §19 轮 75)。蒸馏轮第 9 次
达标;检索三连的对照式第三槽("vs")专产定位素材(初验证 n=1)。

## 17. 经验蒸馏 12(轮 77,2026-09-19 13:10,QUEUE-EMPTY 轮):谱偏置/频率原理族

> 第 17 个 query 族,与前十六族零重叠(§6 Gradient Starvation 是梯度
> 竞争轴,§11 是算子谱实践轴,本族是**学习动力学的频率轴**)——直击
> D6 判读锁定的"E1 缺口 = 优化可达性"的文献机制命名。检索:3 族一次
> 命中(综述 / PINN-算子场景 / GD 机制+对照)。标记:[坐标] ×3 +
> [行动] ×1(→ SB-NAMING 入队 + R1d 条件性登记)。

### 17.1 谱偏置主坐标:F-Principle 低频优先 [坐标]

- 【出处】[On the Spectral Bias of Neural Networks (Rahaman et al.,
  ICML 2019, ~3514 引)](https://proceedings.mlr.press);
  [On understanding and overcoming spectral biases (Xu et al. 2025, ~62 引)](https://www.sciencedirect.com);
  F-Principle overview(Xu & Zhang)。
- 【内容】梯度下降拟合目标函数**从低频到高频**(频率原理);机制
  由 NTK/梯度动力学解释——低频分量梯度信号占比大、先被消减。
- 【对我们的映射】E1 缺口(oracle −27%,锁定推断提取层)的**机制
  命名候选**:若 ctx→V 的目标分量在 q/隐空间含高频成分,GD 低频
  优先 ⇒ ctx 信号欠提取是**优化动力学性质而非容量或信息问题**——
  与 E3(容量否定,+46% 参数零效应)、E4a(ctx 梯度 3.97e-3 饥饿)、
  D6(层 1 信息充足)四层证据链兼容且互补。注意与 §6 Gradient
  Starvation 的分工:那是梯度竞争("谁抢预算"),这是频域先后
  ("什么先学"),两机制可并存。
- 【适用条件】一切"信息在、读得出、却学不快"的判读场合。
- 【验证状态】社区已验证;对本仓为**命名假设**,由 SB-NAMING 文档
  对账证据链(判负标准 PRD §19 轮 77)。

### 17.2 PINN/算子学习场景的谱偏置(最邻近场景) [坐标]

- 【出处】[Spectral bias in physics-informed and operator learning
  (arXiv:2602.19265, 2026)](https://arxiv.org/html/2602.19265v1);
  [Spectral Bias in Practice: the Role of Function Frequency in GD (NeurIPS 2022)](https://papers.neurips.cc/paper_files/paper/2022/file/306264db5698839230be3642aafc849c-Paper-Conference.pdf)。
- 【内容】PINN/算子学习普遍受低频偏置拖累(波方程正/逆问题典型);
  函数频率直接调制 GD 动态(NeurIPS 2022 机制实证)。
- 【对我们的映射】① 本仓波场任务(M2)与弹簧滚出训练落在文献
  场景带内,N1 mechanism-chain 引用合规;② 判读 M2 场任务时的
  频域语言来自本坐标(截断外混叠 §11.1 是分辨率轴,本条是训练
  动力学轴,注意区分)。
- 【适用条件】N1 机制链章节;M2 判读报告的频域表述。
- 【验证状态】社区已验证;引用立即可用。

### 17.3 处方谱系:Fourier 特征/高频缩放/多分辨率 [坐标+行动→R1d 条件性]

- 【出处】§17.1/17.2 综述的 mitigation 章节:Fourier feature
  mappings;[High-Frequency Scaling (Khodakarami et al. 2025)](https://www.osti.gov);
  [Multigrid Deep Learning (NeurIPS 2024)](https://neurips.cc);顺序拟合。
- 【对我们的映射】**R1d 条件性登记**(仿 R1b/R1c 先例,不入队):
  R1 判负且 R1b/R1c 均未兑现缺口收敛 ⇒ 表征轴第四路——ctx(或 q)
  输入的 Fourier 特征重参数化/高频缩放,与监督/结构/聚合三轴正交
  可叠加;分流表 §12.3 已追加(新增不改史)。先决条件:SB-NAMING
  命名对账成立;判负标准届时预注册。
- 【适用条件】R 线修复族;N1 future work 边界。
- 【验证状态】处方社区已验证;对本仓待验证(条件性)。

### 蒸馏结论 12

三 [坐标] + 一 [行动](SB-NAMING 入队,R1d 登记为分流表第四路)。
E1 缺口获得文献机制命名候选(谱偏置/低频优先),证据链四层齐备:
D6(信息充足)→ E3(容量否定)→ E4a(梯度饥饿)→ 谱偏置(频域
动力学)。蒸馏轮第 10 次达标;检索三连对照式第三槽 n=2(升已验证)。

## 18. 经验蒸馏 13(轮 79,2026-09-19 13:35,QUEUE-EMPTY 轮):混沌/长时程评估协议族

> 第 18 个 query 族,与前十七族零重叠(§7 是统计/报告规范,§11 是
> 算子谱实践,§17 是训练动力学——本族是**长时程预测的评估指标与
> 视界理论轴**:VPT/复合误差/Lyapunov 标度)。检索:3 族一次命中。
> 标记:[坐标] ×3 + [行动] ×1(→ EVAL-NORM 入队)。

### 18.1 VPT:混沌预测的标准指标范式 [坐标]

- 【出处】[Data-driven forecasting of high-dimensional chaotic systems
  (Vlachas et al., Proc. R. Soc. A 2018, ~750 引)](https://royalsocietypublishing.org);
  [Long-term prediction of chaotic systems with ML (Fan et al. 2020, ~229 引)](https://link.aps.org);
  [Zero-shot forecasting of chaotic systems (arXiv 2025)](https://arxiv.org)。
- 【内容】VPT(valid prediction time)= 预测保持在真值容差内
  (归一化 RMSE 阈值)的时长,是混沌系统预测的标准报告口径;
  标准 benchmark:Lorenz 63/96、Kuramoto-Sivashinsky。
- 【对我们的映射】N1 评估节可把 VPT 作为 **k 步 MSE 的补充可解释
  口径**(阈值穿越视距),在既有 eval_ks 曲线上即可提取(零算力
  再判读,EVAL-NORM 目标);评审问"为什么报 k 步 MSE 而不是 VPT"
  有现成答案:同一现象的不同呈现,且我们的域更良性(见 §18.3)。
- 【适用条件】一切长时程滚出结果的写作与答辩。
- 【验证状态】社区已验证(标准指标);对本仓再判读待执行(EVAL-NORM)。

### 18.2 复合误差与多步滚出评估 [坐标]

- 【出处】[Investigating Compounding Prediction Errors in Learned
  Dynamics Models (Lambert et al., arXiv:2203.09637)](https://arxiv.org/html/2203.09637v1);
  [Any-step Dynamics Model (OpenReview 2024)](https://openreview.net/forum?id=JZCxlrwjZ8);
  multistep rollout loss 谱系。
- 【内容】自回归滚出的复合误差是学习动力学模型的核心评估对象;
  "一步损失好 ≠ 长视距好"是文献共识,误差-滚出长度曲线是标准
  证据形态。
- 【对我们的映射】① 本仓 eval_ks 阶梯(D1b/D3/E 系列)正是该
  证据形态,评估设计有文献背书(N1 引用);② 与 §8.1 pushforward
  判读互补:训练口径已内建自回归(D5),评估口径本条背书。
- 【适用条件】N1 评估方法节;一切滚出类结论的呈现。
- 【验证状态】社区已验证;引用立即可用。

### 18.3 Lyapunov 视界标度与守恒系统的评估边界 [坐标]

> SCAN-AUDIT 修订(轮 94):题录升级——Learning Chaos in a Linear Way =
> **Cheng, arXiv:2503.14702**(ICLR 2025);RF-HNN = **Choi et al.,
> arXiv:2607.28977**(2026-07)。原 alphaxiv 裸链按 AMM-015 不算法标,
> 已补精确 ID。B→A。

- 【出处】[Learning Chaos in a Linear Way](https://www.alphaxiv.org);
  [Extrapolating the Emergence of Hamiltonian Chaos (RF-HNN)](https://arxiv.org);
  [Adaptable Hamiltonian NN (Han et al., PRR 2021, ~76 引)](https://link.aps.org);
  Lyapunov 谱匹配设计原则文献。
- 【内容】混沌系统(λ>0)预测视界 ~ (1/λ)·ln(精度)——指数发散
  压死视界;缓解路线 = 结构保持(辛)/Lyapunov 谱匹配/物理约束。
- 【对我们的映射】① **评估边界声明(N1 必写)**:本仓基准为守恒
  可积系统(λ=0),误差代数增长,滚出 MSE 在长视距仍保持语义——
  D5 滚出口径辩护在非混沌域比混沌文献更硬气;② 反向诚实边界:
  本架构未在混沌域验证,不声称混沌预测能力;③ 结构保持路线
  (辛/HNN)在混沌文献中同被列为缓解方向——与本仓设计选型互证;
  RF-HNN/Adaptable-HNN 是"参数外推+混沌涌现"的邻接坐标。
- 【适用条件】N1 范围声明与 limitation 节。
- 【验证状态】社区已验证;声明立即可用。

### 蒸馏结论 13

三 [坐标] + 一 [行动](EVAL-NORM 入队:VPT 口径套既有 eval_ks 曲线
的再判读,零算力,轮 72 附带诊断扫描法的推广)。D5 滚出口径辩护
获得混沌文献对照下的加强表述;评估节写作素材(VPT/复合误差/
Lyapunov 边界)齐备。蒸馏轮第 11 次达标。

## 19. 经验蒸馏 14(轮 81,2026-09-19 14:00,QUEUE-EMPTY 轮):时间序列基础模型族

> 第 19 个 query 族,与前十八族零重叠——大规模预训练零样本预测器
> (TSFM)vs 本仓小样本结构化线,是 N1 评审必问的定位轴。检索:
> 3 族一次命中。标记:[坐标] ×3 + [行动] ×1(→ TSFM-BASELINE)。

### 19.1 TSFM 范式坐标 [坐标]

> SCAN-AUDIT 修订(轮 94):主锚题录升级——Foundation Models for Time
> Series: A Survey = **Jain et al.(Dell), arXiv:2504.04011, 2025-04**。
> B→A。

- 【出处】[Foundation Models for Time Series: A Survey (arXiv 2025-04)](https://arxiv.org);
  Chronos(Amazon,数值 token 化复用 LLM 架构)/ TimesFM / TTM / Toto;
  [Benchmarking Foundation Models for TS Forecasting (MDPI 2025)](https://www.mdpi.com)。
- 【内容】跨域海量预训练 + 零样本预测已成为时间线主流范式之一。
- 【对我们的映射】三轴正交定位:① 数据体制(跨域大预训练 vs
  小样本+情境推断);② 保证(无结构保证 vs 守恒由构造+辛滚出);
  ③ 接口(裸序列 vs (q,p) 状态与物理积分器耦合)。N1 一句话:
  不同体制的互补工具,非同台排名。
- 【适用条件】N1 positioning 与评审答辩。
- 【验证状态】社区已验证;引用立即可用。

### 19.2 "Dynamics is what you need"——交锋与审计文献 [坐标]

> SCAN-AUDIT 修订(轮 94):主锚题录升级——Brachet, Richard & Hudelot,
> **ECAI 2025**(DBLP conf/ecai/BrachetRH25);原缺年份与 venue。B→A。

- 【出处】[Dynamics is what you need for time-series forecasting!
  (Brachet et al., OpenReview)](https://openreview.net);
  "Are Time Series Foundation Models Ready to..."(ACM,零样本声明
  vs 专门基线审计);[Synthetic Series-Symbol Data Generation for
  TSFMs (NeurIPS)](https://neurips.cc)。
- 【内容】① 预测任务需要动力学结构(DYN 层,同性质 I/O 才可系统
  辨识)——与本线"结构必要"论点直接同向;② TSFM 零样本声明被
  专门基线审计压缩;③ TSFM 社区反向把系统辨识当预训练目标。
- 【对我们的映射】DYN-layer 论文是结构必要性的直接盟友引用;
  TSFM 审计线支持我们"公平基线需分类框架"的主张;TSFM→SI 趋势
  说明两条线是互补谱系而非敌我。
- 【适用条件】N1 Related Work;答辩"为何不用大模型直接预测"。
- 【验证状态】社区已验证;引用立即可用。

### 19.3 天气气候宏观轴 [坐标]

> SCAN-AUDIT 注记(轮 94):主锚 ScienceDirect 2026 系统综述无作者
> 题录——B 级,整改登记 scan-traceability-audit.md §7(N1 introduction
> 动笔前补作者/DOI)。
>
> SCAN-AUDIT 整改回填(轮 101):**B→A**——主锚钉死 = **Waqas, M. et al.,
> "Physics-informed neural networks and variants in weather forecasting",
> systematic review, ScienceDirect, 2026**(作者+年+题名+期刊宿主可定位;
> DOI 卷期待引用前补注)。

- 【出处】[PINN variants in weather (ScienceDirect 2026 系统综述)](https://www.sciencedirect.com);
  GraphCast/Aurora 类基础模型 vs 物理方法的竞争格局。
- 【内容】基础模型广度 vs 物理结构的同一条轴在天气域已展开成
  宏观对话。
- 【对我们的映射】N1 用一句话把本仓定位接入宏观对话即可
  (同类轴、更小尺度),不展开——超本仓范围。
- 【适用条件】N1 introduction 的宏观语境句。
- 【验证状态】社区已验证;引用立即可用。

### 19.4 TSFM 零样本参考基线协议 [行动→TSFM-BASELINE]

- 【内容】Chronos/TimesFM 零样本 on M1 弹簧观测序列 q(t) 的
  **类别跨界参考基线**协议:数据体制差异声明、非公平基线定位、
  预期用途(读者参照而非排名)三声明 + 云跑候选登记
  (判负标准与命令草案预注册)。
- 【对我们的映射】评审"对比过基础模型吗"的最便宜合规响应:
  协议+欠账登记(算力闸门合规,本机不跑)。
- 【适用条件】N1 实验节基线表。
- 【验证状态】对本仓待执行(下轮,判负标准 PRD §19 轮 81)。

### 蒸馏结论 14

三 [坐标] + 一 [行动](TSFM-BASELINE 入队:跨界参考基线协议+云欠账
登记)。N1 定位的最后一条主要评审轴(基础模型)素材齐备。蒸馏轮
第 12 次达标;检索三连对照式第三槽 n=3(轮 81 vs 槽再命中)。

## 20. 经验蒸馏 15(轮 83,2026-09-19 14:20,QUEUE-EMPTY 轮):不确定性量化与校准族

> 第 20 个 query 族,与前十九族零重叠(概率性声明与校准规范轴——
> 本仓已有 probabilistic_eval.py 工具与多种子协议,文献规范未扫)。
> 检索:3 族一次命中。标记:[坐标] ×3 + [行动] ×1(→ UQ-AUDIT)。

### 20.1 UQ 分类学坐标:无噪域的简化 [坐标]

- 【出处】[A Survey on UQ Methods for DNNs (He et al. 2023, ~295 引)](https://www.jiangteam.org);
  [Comprehensive Survey on UQ for DNNs (arXiv 2024-04)](https://arxiv.org);
  [UQ for NODEs/UDE (Schmid et al. 2025)](https://pmc.ncbi.nlm.nih.gov);
  ML+数据同化+UQ for dynamical systems 综述(Automatica)。
- 【内容】UQ 方法按不确定性来源分类:**偶然(数据噪声)vs 认知
  (模型)**;NODE/微分方程学习场景的 UQ 有专门综述。
- 【对我们的映射】轮 71 已判本仓数据**无观测噪声** ⇒ 偶然不确定性
  由构造为零,本仓一切 UQ 语义都是**认知不确定性(模型)**——
  N1 写概率性声明时必须带此限定,且认知 UQ 的首选廉价工具是
  多种子/集成(见 §20.2)。
- 【适用条件】N1 概率性/不确定性声明的范围限定。
- 【验证状态】社区已验证;范围声明立即可用。

### 20.2 Deep Ensembles vs BNN:种子即集成 [坐标]

- 【出处】[Deep Ensembles as Approximate Bayesian Inference
  (Wilson & Izmailov)](https://cims.nyu.edu/~andrewgw/deepensembles);
  [BNN vs Deep Ensembles head-to-head (arXiv:2509.19180, 2025)](https://arxiv.org/html/2509.19180v1);
  [Repulsive Deep Ensembles are Bayesian (NeurIPS 2021)](https://proceedings.neurips.cc/paper/2021/file/1c63926ebcabda26b5cdb31b5cc91efb-Paper.pdf);
  物理流场预报的 DE 应用(ScienceDirect 2023)。
- 【内容】DE 在精度与校准上普遍匹敌或优于 BNN 且更便宜(后验
  多模式覆盖);但朴素 DE 的贝叶斯性依赖成员多样性(排斥项)。
- 【对我们的映射】① 本仓 **3-seed 协议本身就是一个迷你 DE**——
  seed 区间作为认知不确定性的呈现有文献背书(N1 可写);② 诚实
  边界:n=3 的多样性不足以支撑强贝叶斯解读,只能作"训练方差"
  口径,不能称后验覆盖;③ 若未来开 UQ 线,DE 是首选形态。
- 【适用条件】N1 实验节的多种子表述;未来 UQ 线选型。
- 【验证状态】社区已验证;表述升级待 UQ-AUDIT 对账。

### 20.3 校准规范:覆盖误差是概率性声明的验收判据 [坐标]

- 【出处】预测区间校准/coverage 规范(skforecast、sklearn calibration
  实践文档);[Calibrated Probabilistic Forecasts for Arbitrary
  Sequences (Marx 2025)](https://pmc.ncbi.nlm.nih.gov);forecast scoring
  统计基础(Berkeley/Tibshirani 讲义)。
- 【内容】概率性预测的验收不是"区间存在"而是**覆盖率对准名义
  水平**(如 90% 区间实测覆盖 ~90%);校准误差/coverage error 是
  标准判据。
- 【对我们的映射】本仓任何概率性结论(如"seed 区间")若要升级为
  校准声明,必须报 coverage——**有 spread ≠ 校准**;这是 UQ-AUDIT
  的对账判据之一。
- 【适用条件】一切含不确定性区间的结论呈现。
- 【验证状态】社区已验证;判据立即可用。

### 20.4 概率口径审计 [行动→UQ-AUDIT]

- 【内容】审计 `benchmarks/probabilistic_eval.py` 的概率口径与既有
  多种子产物的 spread 语义:① 工具输出是点估计还是区间?② seed
  区间若作认知不确定性呈现,coverage 语义是否可辩护?③ 升级草案
  (校准协议,云跑候选)。
- 【对我们的映射】N1 若含任何概率性表述,先过本审计;否则降级
  为纯点估计表述。
- 【适用条件】N1 概率性表述;probabilistic_eval 工具的语义修订。
- 【验证状态】对本仓待执行(下轮,判负标准 PRD §19 轮 83)。

### 蒸馏结论 15

三 [坐标] + 一 [行动](UQ-AUDIT 入队)。两条立即可用表述:无噪域
UQ=纯认知不确定性(限定声明);seed 区间=训练方差口径(不可称
后验覆盖)。蒸馏轮第 13 次达标;检索三连对照式第三槽 n=4
(DE vs BNN 正面对比再命中)。

## 21. 经验蒸馏 16(轮 85,2026-09-19 14:50,QUEUE-EMPTY 轮):守恒律/对称性自动发现族

> 第 21 个 query 族,与前二十族零重叠(结构**发现**轴——本仓哲学是
> 结构**注入**,该族是其对照面,N1 必答"为何硬编码而非自动发现")。
> 检索:3 族一次命中。标记:[坐标] ×3 + [行动] ×1(→ SD-POS)。

### 21.1 守恒量自动发现谱系 [坐标]

- 【出处】[AI Poincaré: Machine Learning Conservation Laws from
  Trajectories (Liu et al., PR 2021, ~241 引)](https://link.aps.org);
  ConservNet(分组轨迹守恒残差);Mebratie & Ma 2024/2025。
- 【内容】从轨迹数据自动发现守恒量:可微神经函数沿轨迹导数为零
  + 符号回归转可解释式;GNN 处理变维状态。
- 【对我们的映射】N1 discussion 坐标:本仓在"知道守恒什么"的域
  (能量)选择注入;发现谱系服务"不知道守恒什么"的域(真实系统)。
  二者是同一工具链的上下游,不是竞争关系。
- 【适用条件】N1 discussion 与 future work。
- 【验证状态】社区已验证;定位立即可用。

### 21.2 对称性发现:LieGAN 谱系 [坐标]

- 【出处】[L-conv: Lie Algebra Convolutional Networks (NeurIPS 2021)](https://proceedings.neurips.cc/paper/2021/hash/148148d62be67e0916a833931bd32b26-Abstract.html);
  LieGAN 自动对称发现(ICML 2023;轮 88 治理轮修订:原记"ICML 2024
  keynote"+icml.cc/virtual/2024 链接系题录误记,审计抓出——精确链接待
  SCAN-AUDIT 补,按 AMM-015 溯源标准不确定题录须标注);
  LieGNN / LieSD(2025)/ LieNLSD(2025,非线性对称)。
  - SCAN-AUDIT 修订(轮 94,**轮 88 待办销账**):LieGAN 精确题录 =
    **Yang et al., "Generative Adversarial Symmetry Discovery",
    ICML 2023, arXiv:2302.00236**。LieGNN/LieSD/LieNLSD 谱系二级注记:
    无作者题录,引用前需补。
- 【内容】从数据发现连续李群对称性(Lie 代数空间对抗学习),发现的
  对称可插入等变下游模型;非线性对称的显式计数已出现。
- 【对我们的映射】时间平移对称(自治性)与时间反演对称(轮 66)
  在本仓分别是"由构造满足"与"R1b 候选先验"——发现谱系提供
  "先发现再注入"的替代管线坐标;对本仓保守基准属 future work。
- 【适用条件】N1 future work;对称性先验的来源讨论。
- 【验证状态】社区已验证;定位立即可用。

### 21.3 硬编码偏差的权衡边界 [坐标]

- 【出处】[hPINNs: Hard Constraints for Inverse Design (SIAM)](https://epubs.siam.org/doi/10.1137/21M1397908)(硬 vs 软约束对照);
  [Fundamental flaws of PINNs (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0360835225008502)
  (硬编码物理偏差导致过平滑/锐利 fronts 失效)。
- 【内容】硬编码偏差有已知失败模式:过平滑、多尺度分辨失败——
  偏差是先验赌注,赌错则伤害表达。
- 【对我们的映射】① 本仓是**分层注入**:守恒律层硬(H 结构+辛
  积分器),函数形式层自由(T/V 是 MLP)——恰在"保证"与"表达"
  之间取中间态;② 轮 80 的 VPT 判读与本条互证:θ 敏感窗就是
  注入偏差不覆盖的表达细节;③ N1 limitation 节引用:结构注入的
  代价是"若真实结构不是注入的结构"(如耗散、非可分),架构表达
  受限——耗散槽位(§15)正是预留的逃生门。
- 【适用条件】N1 limitation;架构哲学答辩。
- 【验证状态】社区已验证;定位立即可用。

### 21.4 结构注入 vs 结构发现定位小节 [行动→SD-POS]

- 【内容】把 §21.1-21.3 汇成 N1 discussion 定位小节:分层注入哲学
  (守恒层硬/函数层自由)、发现谱系为上游工具、注入失败模式与
  逃生门(耗散槽位、R1b T 偶)。
- 【对我们的映射】评审"为何硬编码"一击必答。
- 【适用条件】N1 discussion。
- 【验证状态】对本仓待执行(下轮,判负标准 PRD §19 轮 85)。

### 蒸馏结论 16

三 [坐标] + 一 [行动](SD-POS 入队)。本仓架构哲学(分层注入)获得
文献对照下的精确表述与已知失败模式清单。蒸馏轮第 14 次达标;
检索三连对照式第三槽 n=5(hard vs discovered 权衡再命中)。

## 22. 经验蒸馏 17(轮 87,2026-09-19 15:10,QUEUE-EMPTY 轮):可微分仿真器/梯度路径族

> 第 22 个 query 族,与前二十一族零重叠(训练梯度**穿过积分器**的
> 精度/显存/稳定性轴——本仓 create_graph 展开式 BPTT 的文献坐标)。
> 检索:3 族命中(第三槽首轮过窄,搜索自修正两次后命中,如实注记)。
> 标记:[坐标] ×3 + [行动] ×1(→ GRAD-PATH)。

### 22.1 可微物理训练范式 [坐标]

- 【出处】[Solver-in-the-Loop: Learning from Differentiable Physics
  (Um et al., NeurIPS 2020, ~473 引)](https://proceedings.neurips.cc);
  [Physics-based Deep Learning 免费教材](https://physicsbaseddeeplearning.org)(DP 章节)。
- 【内容】把完整数值仿真器放进训练环,梯度穿过求解器所有运算;
  DP 训练可同时修正求解器数值误差。
- 【对我们的映射】本仓 train_semigroup/prefix 正是 DP 形态
  (梯度穿过 k 步辛滚出+液基细胞)——范式有标准出处可引
  (N1 方法节);Um 2020 是 DP 训练的奠基引用。
- 【适用条件】N1 方法节与相关工作。
- 【验证状态】社区已验证;引用立即可用。

### 22.2 反向 vs 前向:展开 BPTT / adjoint / 辛伴随三分 [坐标]

> SCAN-AUDIT 修订(轮 94):题录升级——辛伴随两版:**NeurIPS 2021 版**
> = Matsubara, "Symplectic Adjoint Method for Exact Gradient of Neural
> ODE", arXiv:2102.08532;**扩展版** = Matsubara, "The Symplectic
> Adjoint Method: Memory-Efficient Exact Gradient of Symplectic
> Integrators"(IEEE;~21-22 引与本条引用数吻合,主锚取此版)。
> 原仅 arXiv 根链。B→A。

- 【出处】[Symplectic Adjoint Method (Matsubara et al., ~21 引)](https://arxiv.org)
  (辛积分器专用:精确梯度+低内存+快于 adjoint 的中间方案);
  adjoint(Chen 2018 谱系):O(1) 内存+近似梯度+~2x 前向代价;
  展开式 autograd(本仓 create_graph 路线):精确梯度+O(k) 内存。
- 【内容】三者权衡:展开式=离散解的**精确**梯度但内存线性于步数;
  adjoint=常数内存但梯度近似且额外解算;辛伴随=对辛积分器兼得。
- 【对我们的映射】① 本仓 k_train=8 小步数,展开式精确梯度是
  正确选择,无需改;② **升级协议坐标**:若未来加大训练滚出视距
  (k_train↑),Matsubara 辛伴随是首选中间方案(结构匹配本仓积分器),
  先于 adjoint/截断;③ N1 可引用以说明训练口径的梯度精确性。
- 【适用条件】训练视距扩展的协议设计;N1 方法节。
- 【验证状态】社区已验证;本仓 k_train=8 无需变更。

### 22.3 前向稳定 ≠ 反向稳定 [坐标]

> SCAN-AUDIT 修订(轮 94):题录升级——SymODEN = **Zhong, Datta,
> Kolter, Kiziltan & Pappas, ICLR 2020**(OpenReview);Hamiltonian
> Matching = **Canizares, Murari, Sherry, Shumaylov & Schönlieb,
> NeurReps Workshop @ NeurIPS 2024**(arXiv 2024-10;原记"(NeurIPS)"
> 实为主会 workshop,venue 修正);Pascanu 梯度爆炸解密 =
> arXiv:1211.5063。B→A。

- 【出处】BPTT/截断谱系(D2L、TBPTT、Pascanu 梯度爆炸解密);
  SymODEN(OpenReview);Hamiltonian Matching for Symplectic Neural
  Integrators (NeurIPS)。
- 【内容】重复乘雅可比使长展开的反向梯度可爆炸/消失;**前向辛稳定
  不保证反向梯度稳定**(伴随动力学可指数增长);缓解=截断 BPTT/
  梯度裁剪/伴随法;辛结构主要保前向滚出稳定,不自动保反向。
- 【对我们的映射】① 与 E4a(ctx 梯度饥饿)的弱假说连线:反向
  灵敏度沿滚出链的结构性衰减可能是 ctx 通道梯度弱的因素之一
  ——**弱假说不下结论**,若未来审计梯度路径可作为解释候选;
  ② k_train=8 短链下风险低(D 系列结论不受威胁)。
- 【适用条件】梯度路径审计;长视距训练协议设计。
- 【验证状态】社区已验证;假说待 GRAD-PATH 审计(不下结论)。

### 22.4 滚出训练梯度路径审计 [行动→GRAD-PATH]

- 【内容】① 审计 create_graph=self.training 的梯度路径语义
  (ctx→FiLM→V→滚出链的通路,hamiltonian.py/model.py docstring
  已有部分声明);② 冒烟探针:合成张量上实测 k=8/32/128 展开图
  的内存/梯度范数标度(零训练,秒级);③ 判读:本仓 k_train=8
  的展开式选择合理性 + k↑ 时的辛伴随升级草案(云跑候选)。
- 【对我们的映射】训练口径的梯度精确性/显存证据化;E4a 弱假说
  的审计入口。
- 【适用条件】N1 方法节;未来长视距训练协议。
- 【验证状态】对本仓待执行(下轮,判负标准 PRD §19 轮 87)。

### 蒸馏结论 17

三 [坐标] + 一 [行动](GRAD-PATH 入队)。DP 训练范式奠基引用
(Um 2020)+ 三分梯度方案权衡(展开/adjoint/辛伴随)+ 前向≠反向
稳定坐标入库;本仓 k_train=8 展开式选择被文献背书。蒸馏轮第 15 次
达标;对照式第三槽 n=6(含 1 次查询自修正,如实注记)。

## 23. 经验蒸馏 18(轮 98,2026-09-20,QUEUE-EMPTY 轮):经典系统辨识基线族

> 第 23 个 query 族,与前 22 族零重叠(此前全部为神经/学习理论轴,本族是
> **经典方法基线轴**——P3 终收口后 N1 基线表"经典行"的最后缺口)。检索:
> 3 族一次命中(SINDy 主坐标 / 经典 LS 谱系 / "SINDy vs NODE" 对照式);
> 2 次补检索当轮钉死 venue(AMM-015 带?不过夜:Gersch/Fronk/Ioannou)。
> 标记:[坐标] ×3 + [行动] ×1(→ CLASSIC-BASELINE 入队)。

### 23.1 SINDy:方程形式发现的代表作 [坐标]

- 【出处】Discovering governing equations from data by sparse identification
  of nonlinear dynamical systems,**Brunton, Proctor & Kutz, PNAS 2016**;
  SINDyc 扩展(ScienceDirect,~644 引);官方库 PySINDy(github.com/
  dynamicslab/pysindy)。
- 【内容】候选函数库 + 稀疏回归直接辨识控制方程;依赖测量变量选择与
  数据质量(原文自述)。
- 【对我们的映射】与 §21.1(守恒量/对称性发现)分工明确:SINDy 是
  **方程形式轴**的发现谱系,§21 是守恒量轴;本仓注入的是结构形式
  (哈密顿方程+辛积分器),函数形式留给数据——注入/发现在方程层
  的精确分工坐标(N1 discussion 复用轮 86 分层注入框架,此条补
  "方程发现"行)。干净无噪仿真恰是 SINDy 最佳域,评审问
  "为何不用 SINDy"的诚实答案:本仓声称的贡献不是方程发现
  (§21.4/23.1 定位),SINDy 可作 future-work 工具。
- 【适用条件】N1 Related Work 与答辩。
- 【验证状态】社区已验证;定位立即可用。

### 23.2 经典最小二乘/谱估计基线谱系 [坐标+行动→CLASSIC-BASELINE]

- 【出处】Gersch & Foutch,**IEEE Trans. Automatic Control, AC-19(6),
  898-903, 1974**(结构系统参数两阶段 LS,~83 引);Marquardt,**J. SIAM
  11(2):431-441, 1963**(Levenberg-Marquardt,~4.4 万引,非线性 LS 标准
  工具);Giarnetti et al. 2015(多谐波 LS 频率估计达 CRB,ScienceDirect,
  venue 卷期待引用前补注)。
- 【内容】振子参数的经典估计线:协方差/最小二乘两阶段、非线性 LS、
  谐波拟合频率估计(干净数据下可达 Cramér-Rao 界)。
- 【对我们的映射】N1 基线表"经典行"坐标:无噪线性振子上经典 LSQ 是
  **强基线**(CRB 级)——本仓 M1 的对比主张必须锚"32 维场系数 c(x)
  低维观测→结构接口"(M2 线,P3 已收口)与"结构性质(守恒/辛)",
  **不做单参数估计精度的排名主张**(D6 已判单参数信息层非瓶颈);
  评审"为何不比经典方法"的合规响应=把经典行放进表+三声明。
- 【适用条件】N1 实验节基线表。
- 【验证状态】社区已验证;对本仓待执行(CLASSIC-BASELINE,下条)。

### 23.3 SINDy×NODE 混合线与"无方程"对照 [坐标]

- 【出处】Fronk & Petzold,"Interpretable polynomial neural ordinary
  differential equations",**Chaos 33(4), 2023**(~57 引,SINDy 后验符号化
  训练好的 NODE);Ioannou et al.,"An Empirical Investigation of Neural
  ODEs and Symbolic Regression for Dynamical Systems",**NeurIPS ML4PS
  workshop 2025**;Kacprzyk et al.,"No Equations Needed"(OpenReview,
  forum id 待引用前补注)。
- 【内容】NODE(黑箱)与 SINDy(符号)的实证对照与混合(训练后符号化);
  "无方程"动力学基准线。
- 【对我们的映射】定位三线表补全:本仓=结构注入(方程形式已知),
  NODE=黑箱,SINDy=符号发现,混合=后验符号化;本仓差异轴=情境通道
  (观测前缀→ctx 推断)+硬约束,两条线均无。Fronk & Petzold 的
  "训练后 SINDy 符号化"是本仓哈密顿头学到的 V(q) 可解释性的现成
  后续工具(不立项,坐标;与轮 86 逃生门清单同格)。
- 【适用条件】N1 Related Work;可解释性 future work。
- 【验证状态】社区已验证;定位立即可用。

### 23.4 经典基线协议登记 [行动→CLASSIC-BASELINE]

- 【内容】LSQ-ω̂(有限差分+线性最小二乘)与 SINDy-库回归两臂,跑 M1
  同池 eval 集(gen_spring 尾 128,t_obs=24,k=100,与 D-2 TSFM 协议同
  池),三声明(数据体制差异/非公平基线定位/预期用途=读者参照非排名,
  仿 §19.4 先例)+判负标准与命令草案预注册;T1 级(闭式/稀疏回归,
  秒-分钟级,本机合规)。
- 【对我们的映射】N1 基线表"经典"行;评审合规最便宜响应。
- 【适用条件】N1 实验节。
- 【验证状态】对本仓待执行(下轮,判负标准 PRD §19 轮 98)。

### 蒸馏结论 18

三 [坐标] + 一 [行动](CLASSIC-BASELINE 入队:协议+同池经典基线两臂)。
P3 收口后首个蒸馏轮,产出行动类条目,S1 不触发;检索三连对照式第三槽
n=7(命中定位素材,0 修正);第 23 族零重叠确认。蒸馏轮第 16 次达标。

## 24. 经验蒸馏 19(轮 100,2026-09-20,QUEUE-EMPTY 轮):结构化状态空间模型族

> 第 24 个 query 族,与前 23 族零重叠(§13 是 CfC 闭式基座轴,本族是
> **SSM 线轴**——N1 基座答辩"为何不用 Mamba/S4"必问轴)。检索:3 族
> 一次命中(谱系综述 / 时序直击 / "SSM vs 连续时间 RNN" 对照式);
> 1 次补检索当轮钉死 SUBNET venue(AMM-015 带?不过夜)。标记:
> [坐标] ×3;无 [行动](理由见 24.4 注记)。

### 24.1 SSM 谱系主坐标:S4/Mamba/S5 [坐标]

- 【出处】Gu, Goel & Ré,"Efficiently Modeling Long Sequences with
  Structured State Spaces",**ICLR 2022**(arXiv:2111.00396,S4/HiPPO);
  Gu & Dao,"Mamba: Linear-Time Sequence Modeling with Selective State
  Spaces",**arXiv:2312.00752**(COLM 2024);Smith, Warrington &
  Linderman,"Simplified State Space Layers for Sequence Modeling",**ICLR
  2023**(arXiv:2208.04933,S5);谱系综述 Somvanshi,**arXiv:2503.18970**,
  2025。
- 【内容】结构化(HiPPO 初始化/对角化/选择性)线性状态空间的深度
  学习谱系:长序列线性时间建模,连续时间数学基础。
- 【对我们的映射】N1 基座答辩"为何不用 Mamba/S4"的定位坐标:同
  "状态空间"词汇、正交任务轴——SSM 学**序列变换**(语言/音频长
  上下文,自由线性动力学),本仓学**物理系统辨识**(参数化哈密顿+
  守恒由构造+情境推断);且 SSM 的 HiPPO 连续时间基础与本仓 ODE
  基座同源,可作"状态空间视角"盟友引用而非竞品。
- 【适用条件】N1 基座小节与答辩。
- 【验证状态】社区已验证;定位立即可用。

### 24.2 连续时间对照线:Neural CDE / Latent ODE / SUBNET [坐标]

- 【出处】Kidger et al.,"Neural Controlled Differential Equations for
  Irregular Time Series",**NeurIPS 2020**(~1200 引;"Neural CDE 之于
  RNN 如 Neural ODE 之于 ResNet");Rubanova, Chen & Duvenaud,"Latent
  ODEs for Irregularly-Sampled Time Series",**NeurIPS 2019**;
  Beintema, Schoukens & Tóth,"Continuous-time identification of dynamic
  state-space models by deep subspace encoding",**ICLR 2023**(SUBNET-CT,
  ~38 引;原版 SUBNET L4DC/PMLR 144, 2021)。
- 【内容】连续时间序列模型三线:CDE(连续时间 RNN 类比)/Latent ODE
  (不规则采样推断)/结构化 SSM 辨识(SUBNET:深子空间编码器辨识
  连续时间状态空间,实证优于黑箱 NODE)。
- 【对我们的映射】① **SUBNET-CT 是本仓"结构化优于无结构"论点的
  盟友实证**——连续时间系统辨识上结构化 SSM 优于黑箱 NODE,与
  "哈密顿结构+辛滚出优于自由滚出"同向(N1 Related Work 盟友引用);
  ② Neural CDE/Latent ODE 的卖点是不规则采样,本仓仿真数据均匀采样
  (轮 71),该优势轴不构成对比压力,如实注记;③ 定位三轴表第四线
  补全(结构注入/线性化在哪儿/情境通道:SSM/CDE/NODE 三线均无
  情境推断+硬约束组合,与 §16 Koopman、§19 TSFM 同框架)。
- 【适用条件】N1 Related Work 与基座答辩。
- 【验证状态】社区已验证;定位立即可用。

### 24.3 边界注记(非条目) [坐标]

SSM 对照基线(M1 上跑 S4D/LRU 臂)**不预登记**:依赖不在 lock、
N1 现无此评审压力实据;若评审轮真出现该需求,按 §19.4 TSFM 先例
届时预注册(三声明+判负标准+Probe-First),防空转欠账。本族三 [坐标]
即完整交付;S1 观察:第 24 族无行动类产出(第 1 次),下轮蒸馏若再无
行动产出即触发 S1 评估——如实预留,不硬造行动条目。

### 蒸馏结论 19

三 [坐标] 入库(S4/Mamba/S5 谱系定位/连续时间三线盟友与边界/S1 观察
注记)。第 24 族零重叠确认;检索三连对照式第三槽 n=8(Neural CDE
"连续时间 RNN 类比"再命中定位素材,0 修正);AMM-015 带?不过夜执行
(SUBNET venue 当轮钉死 ICLR 2023)。蒸馏轮第 17 次达标。

## 25. 经验蒸馏 20(轮 103,2026-09-20,QUEUE-EMPTY 轮):辛积分器工程族

> 第 25 个 query 族,与前 24 族零重叠(§15.3 是耗散×辛的数值边界轴,
> 本族是**积分器本身的工程轴**:高阶组合/影子哈密顿/变步长)。检索:
> 2 族命中+第三槽未获强对照(如实注记,以教科书章节约化)。标记:
> [坐标] ×3 + [行动] ×1(→ VERLET-ORDER 入队)。

### 25.1 高阶辛组合方法谱系 [坐标]

- 【出处】Yoshida,"Construction of higher order symplectic integrators",
  **Phys. Lett. A, 1990**(~3,375 引,组合系数奠基);Rein,"High-order
  symplectic integrators for planetary dynamics"(SABA 家族,Lie 级组合,
  2019,期刊卷期待引用前补)。
- 【内容】2 阶 leapfrog/Velocity-Verlet 经 Yoshida 系数组合可升 4/6/8
  阶;高阶伴随负步长与大系数代价。
- 【对我们的映射】本仓 leapfrog=2 阶;"为何不上高阶"的 N1 答辩=
  守恒由实测承担(P0-3 energy drift 有界)而非阶数堆叠——当前
  dt=0.1、ω≤1.8(hω≈0.18)下 2 阶误差已远低于学习误差;若未来加长
  视距再按 Yoshida 组合升级(坐标,不立项)。
- 【适用条件】N1 methods 答辩;长视距升级协议。
- 【验证状态】社区已验证;定位立即可用。

### 25.2 影子哈密顿/后向误差分析 [坐标]

- 【出处】Hairer, Lubich & Wanner,"Geometric Numerical Integration:
  Structure-Preserving Algorithms for ODEs",**Springer, 2006**(标准
  教科书,含高振荡系统修正频率展开);Reich,backward error analysis
  综述(~391 引);Skeel et al. 2005,shadow Hamiltonian 监控 energy
  drift(ScienceDirect,~128 引)。
- 【内容】辛积分器精确守恒一个 O(h^p) 邻近的**影子哈密顿**,真能量
  在指数长时距内有界振荡——"能量漂移有界"是定理级结论而非经验巧合;
  高振荡域要求 hω < 常数。
- 【对我们的映射】① P0-3 能量漂移有界的**理论锚**(N1 methods 必写):
  本仓 hω≈0.18(=0.1×1.8)远在界内 ⇒ 漂移有界由构造+理论双保险;
  ② Skeel 的 shadow-Hamiltonian 读数法是把 energy_drift 诊断升级为
  更灵敏监控的现成路径(备用,不立项)。
- 【适用条件】N1 methods 理论段;诊断升级协议。
- 【验证状态】社区已验证(教科书级);对本仓 hω 数值核验待执行(25.4)。

### 25.3 变步长的辛性代价 [坐标]

- 【出处】Hairer, Lubich & Wanner(2006)教科书变步长章节(第三槽
  本轮未命中正面 head-to-head 论文,如实注记——以教科书章节约化,
  不引具体对照论文)。
- 【内容】朴素自适应步长破坏辛性,保结构需专门控制器(如比例控制器
  的修正理论)。
- 【对我们的映射】本仓固定步长的辩护坐标:仿真自定 dt,误差控制
  需求由"2 阶+小 hω+守恒实测"覆盖;自适应步长换来的误差收益以丢失
  结构保证为价,对本仓任务不划算(与 §25.1/25.2 同构成 methods
  答辩三件套:阶数/理论/步长策略)。
- 【适用条件】N1 methods 答辩。
- 【验证状态】社区已验证(教科书级);立即可用。

### 25.4 观测阶数验证探针 [行动→VERLET-ORDER]

- 【内容】dt ∈ {0.2, 0.1, 0.05, 0.025} 单轨弹簧扫描,energy_drift 与
  rollout MSE 对 dt 的收敛阶(log2 相邻比值),预注册 **p̂∈[1.8,2.2]**
  ⇒ 2 阶确认;T1 秒级,产物过 audit。
- 【对我们的映射】N1 methods 节"实现达到理论阶数"的标准验证数字;
  与 §25.2 的 hω 界内声明配套。
- 【适用条件】N1 methods。
- 【验证状态】对本仓待执行(下轮,判负标准 PRD §19 轮 103)。

### 蒸馏结论 20

三 [坐标] + 一 [行动](VERLET-ORDER 入队)。第 25 族;检索三连对照式
第三槽未获强对照(如实注记,教科书章节约化);S1 计数重置(本轮有
[行动] 产出)。蒸馏轮第 18 次达标。

## 26. 经验蒸馏 21(轮 112,2026-09-23,QUEUE-EMPTY 轮):缩放律/样本效率族

> 第 26 个 query 族,与前 25 族零重叠(本仓蒸馏清单下:样本效率是自家
> 协议轴,**文献的缩放律族**——Kaplan 谱系/算子学习缩放/结构×缩放
> 交叉——此前未蒸馏)。检索:3 族命中(综述/机制直击/对照式第三槽)。
> 标记:[坐标] ×3 + [行动] ×1(→ M1-CAP-AXIS 入队)。

### 26.1 缩放律方法论综述(含误拟合陷阱)[坐标]

- 【出处】Li, Kudugunta & Zettlemoyer, "(Mis)Fitting: A Survey of
  Scaling Laws", arXiv:2502.18969, 2025(UW,41 页综述)。
- 【内容】缩放律=损失对模型/数据/算力的幂律经验拟合;系统整理拟合
  方法学决策与**误拟合(misfitting)陷阱**(外推失稳、渐近带选择、
  断点处理)。
- 【对我们的映射】① 未来拟合任何本仓标度曲线(样本效率曲线/d_model
  轴)时 Methods 的"拟合陷阱清单";② 小样本域(本仓 n32/n64)远离
  幂律渐近带 ⇒ 任何"缩放律"表述降档为"标度趋势",不写指数(与 §7
  报告规范同源)。
- 【适用条件】N1 Methods/附录的标度拟合段。
- 【验证状态】社区已验证(综述);对本仓=方法论参照。

### 26.2 对称性改变缩放律形状 [坐标] ★强

- 【出处】Ngo & Ravanbakhsh, "Scaling Laws and Symmetry, Evidence from
  Neural Force Fields", arXiv:2510.09768, **ICLR 2026**(分子力场
  E(n) 等变线)。
- 【内容】等变/对称结构不是平移缩放律常数,而是**改变其形状/断点**
  (broken scaling laws 谱系,源头 BNSL 2023):对称结构的性能-规模
  曲线呈系统性偏移与拐点差异。
- 【对我们的映射】① N1 定位直接文献盟友:"结构-性质轴"的量化版本=
  **结构改变缩放几何**而非仅省数据——与 Brachet "Dynamics is what
  you need"(§19)构成"结构必要论"双盟友;② 为 M1-CAP-AXIS 提供
  机制动机:容量轴是结构效应显形的仪器(E3 在 M2 判容量非瓶颈,M1
  侧同仪器对照);③ 顺带坐标:BNSL(2023)为该谱系源头。
- 【适用条件】N1 Related Work 定位;M1-CAP-AXIS 判读框架。
- 【验证状态】社区已验证(ICLR 2026 发表);与本仓证据的对接=待
  M1-CAP-AXIS 实测。

### 26.3 神经符号先验作为缩放律的对立面 [坐标]

- 【出处】Velasquez et al., "Neurosymbolic AI as an antithesis to
  scaling laws", **PNAS Nexus 4(5):pgaf117, 2025**,
  DOI 10.1093/pnasnexus/pgaf117。
- 【内容】物理/符号先验作为归纳偏置使小数据域可学,与"堆算力"路线
  形成对立面;定量论证先验路线的样本效率优势。
- 【对我们的映射】Intro"structure vs scale"叙事的期刊级引用;与 §19
  TSFM 范式三轴表互补(那条讲数据体制差异,本条讲"先验=小数据域的
  合法路线")。
- 【适用条件】N1 Intro/Discussion。
- 【验证状态】社区已验证(PNAS Nexus 期刊);定位立即可用。

### 26.4 M1 容量轴探针 [行动→M1-CAP-AXIS]

- 【内容】d_model ∈ {24,48,96} 三点,同池同预算(seed 0,2000 步,
  n32)双臂(prefix/all2all),判读=liquid edge(gap%)随容量的走向:
  不收窄 ⇒ 结构效应(E3 的 M1 侧对照,"结构效应跨任务"叙事);
  收窄 ⇒ 机制降档如实入档。T1 预算(冒烟校准后登记,预计 ≤10min);
  预注册判负标准执行前写入 PRD §19。
- 【对我们的映射】E3(核 +46% 参数零效应)的 M1 侧对照仪器;N1
  机制链容量轴补空。
- 【适用条件】N1 机制链;判读入 PRD §19。
- 【验证状态】对本仓待执行(下心跳,预注册先行)。

### 蒸馏结论 21

三 [坐标] + 一 [行动](M1-CAP-AXIS 入队)。第 26 族;S1 计数重置
(本轮有 [行动] 产出)。蒸馏轮第 19 次达标。附带弱坐标(题录未核,
带 ? 登记 SCAN-AUDIT 复核):"Towards Multi-Fidelity Scaling Laws of
Neural Surrogates"(arXiv,2025-11,多保真数据轴,作者待核)。

## 27. 经验蒸馏 22(轮 114,2026-09-23,QUEUE-EMPTY 轮):分布外泛化/外推族

> 第 27 个 query 族,与前 26 族零重叠(§9 可辨识性=观测窗 Fisher 信息,
> §18=时程评估协议,§26=容量/数据轴——**参数域外推轴**(训练带外泛化)
> 未蒸馏过;house 数据钩子=ω∈[0.7,1.8] 训练带,带外探针天然 T1)。
> 检索:3 槽一次命中。标记:[坐标] ×3 + [行动] ×1(→ OMEGA-EXTRAP 入队)。

### 27.1 参数域分布移位的系统实验 [坐标] ★

- 【出处】Wang, Maddix Robinson, Faloutsos, Wang & Yu, "Learning
  dynamical systems requires rethinking generalization", **NeurIPS 2020
  Workshop**(Interpretable Inductive Biases and Physically Structured
  Representations)。
- 【内容】系统实验:深度模型在动力系统的**数据域与参数域分布移位**下
  泛化失败(非平稳/混沌加剧);主张动力系统的泛化概念需重思。
- 【对我们的映射】① N1 scope declaration 的文献背书:带内插值声明
  不是本仓特有短板而是领域公认失效轴;② 为 OMEGA-EXTRAP 提供预期
  框架(参数域移位=该文记载的失效模式,预注册预期=带外退化,非预言)。
- 【适用条件】N1 Limitations/scope;OMEGA-EXTRAP 判读框架。
- 【验证状态】社区已验证(workshop 级,Amazon Science 收录);对仓对接
  待探针。

### 27.2 OOD 泛化保证(理论锚)[坐标]

- 【出处】Caro, Huang, Cerezo, Sharma, Sornborger, Cincio & Coles,
  "Out-of-distribution generalization for learning quantum dynamics",
  **Nature Communications 14:3751, 2023**(~161 引)。
- 【内容】对学习未知酉(量子动力学)证明 **OOD 泛化保证**:训练/测试
  分布足够接近时可泛化,并给出分布接近度-误差的定量界。
- 【对我们的映射】"带外多远算远"的定量范式:OOD 泛化不是 0/1 命题而
  是分布接近度的函数——OMEGA-EXTRAP 的双带设计(近带 [0.3,0.6]/
  [1.9,2.2] 对称夹击训练带)即该范式的廉价实例化;N1 讨论段引用
  "泛化保证存在性依赖分布接近度"的严格文献。
- 【适用条件】N1 Discussion;外推探针设计原则。
- 【验证状态】社区已验证(Nat. Commun.);对仓=设计范式参照。

### 27.3 外推约束处方谱系 [坐标]

- 【出处】Stinis, Hagge, Tartakovsky & Yeung, "Enforcing constraints for
  interpolation and extrapolation in Generative Adversarial Networks",
  **J. Comput. Phys. 397:108844, 2019**(~44 引)。
- 【内容】以物理约束强制 GAN 的插值-外推一致性,动力系统仿真器外推
  失效的处方谱系代表。
- 【对我们的映射】若 OMEGA-EXTRAP 判出带外失效,处方坐标已有:
  本仓的对应物=哈密顿头结构约束天然限制外推形态(守恒结构带外仍在,
  退化的是 ctx 推断)——结构约束线的外推辩护/处方起点。
- 【适用条件】N1 Discussion;若判负后的处方路由。
- 【验证状态】社区已验证(JCP);对本仓适用性待探针。

### 27.4 ω 带外外推探针 [行动→OMEGA-EXTRAP]

- 【内容】M1 在 ω∈[0.7,1.8] 训练(等预算 2000 步,seed 0),在带内
  anchor 带+带外近带 [0.3,0.6] 与 [1.9,2.2] 分别评估 k100 rollout MSE
  与 ctx 线性解码(context_probe 复用);双臂 liquid/static 对照
  (结构约束是否缓解带外退化)。判读=带外退化曲线+ctx 解码带外走向;
  判负标准执行前预注册 PRD §19;T1 预算(训练一次+多带评估,冒烟后
  登记,预计 ≤10min)。
- 【对我们的映射】N1 scope declaration 从"声明插值域"升级为"量化的
  带外退化曲线"[B] 级;§27.2 分布接近度范式的实例化。
- 【适用条件】N1 Limitations/Methods;判读入 PRD §19。
- 【验证状态】对本仓待执行(下心跳,预注册先行)。

### 蒸馏结论 22

三 [坐标] + 一 [行动](OMEGA-EXTRAP 入队)。第 27 族;S1 计数重置
(本轮有 [行动] 产出)。蒸馏轮第 20 次达标。选族启发式(本轮起效,
入 PLAYBOOK):先枚举自家未蒸馏的数据/协议钩子(ω 带/池尺寸/eval_ks),
再找覆盖该钩子的文献族——从钩子找文献比从文献找方向更易 T1 化。

## 28. 经验蒸馏 23(轮 117,2026-09-23,QUEUE-EMPTY 轮):图网络学习模拟器/GNN 动力学族

> 第 28 个 query 族,与前 27 族零重叠(GNN 模拟器谱系未蒸馏;N1 定位表
> 缺 GNN 一线)。选族启发式(轮 114)二次起效:house 钩子=NBody 基准
> (P2-1)+轮 95 恒等式声明的"NBody 粒子池化未审计"边界。检索:3 槽
> 一次命中。标记:[坐标] ×4 + [行动] ×1(→ NBODY-POOL-AUDIT 入队)。

### 28.1 GNS:图网络模拟器奠基 [坐标]

- 【出处】Sanchez-Gonzalez, Godwin, Pfaff, Ying, Leskovec & Battaglia,
  "Learning to simulate complex physics with graph networks",
  **ICML 2020**(~2,243 引)。
- 【内容】GNS:消息传递图网络预测粒子加速度,自回归滚出;流体/刚体/
  可变形体多域学习模拟。**聚合=对边消息求和**(力叠加原理的标准
  实现)。
- 【对我们的映射】N1 Related Work 缺失的竞争线补位:GNN 模拟器=
  "关系结构注入、守恒不注入"的代表——与本仓"守恒层硬注入"构成
  注入谱系两端的现成对照(轮 86 分层注入哲学的谱系坐标)。
- 【适用条件】N1 Related Work。
- 【验证状态】社区已验证(ICML,高引);定位立即可用。

### 28.2 MeshGraphNets:网格域扩展 [坐标]

- 【出处】Pfaff, Fortunato, Sanchez-Gonzalez & Battaglia, "Learning
  mesh-based simulation with graph networks", **ICLR 2021**(outstanding
  paper,arXiv:2010.03409,~2,084 引)。
- 【内容】GNS 到网格域的扩展(气动/布料/结构力学),自适应网格。
- 【对我们的映射】GNN 谱系广度的第二条锚(与 §28.1 同引 N1 Related
  Work 段);不展开。
- 【适用条件】N1 Related Work。
- 【验证状态】社区已验证;定位立即可用。

### 28.3 聚合语义:sum 叠加 vs mean 归一 [坐标] ★(轮 95 边界的文献面)

- 【出处】Wang, "Graph pooling in graph neural networks: methods and
  their developments", Springer 综合(**2024**,~43 引;sum 在 multiset
  上单射最强/mean-max 严格更弱);物理 GNN 惯例=GNS 系**边消息求和**
  (力/通量叠加原理,mean 会归一掉总相互作用强度)。
- 【内容】聚合算子表达力谱系:sum 单射(保计数/总量)>mean(尺度
  不变但丢总量)>max;物理域求和=叠加原理的规范实现。
- 【对我们的映射】轮 95 均值场恒等式的适用边界文献面:M1/M2 均值池
  的信息湮灭在 NBody 侧**不应**出现——NBody 动力学侧对势求和是物理
  必然(叠加原理),ctx 推断侧池化语义待审计(§28.5);文献预期=
  NBody 池化无 M2 型恒等式湮灭。
- 【适用条件】NBODY-POOL-AUDIT 判读框架;N1 机制链边界注。
- 【验证状态】社区已验证(综述+GNS 惯例);对仓对接待探针。

### 28.4 HGN:图网络×哈密顿的最近邻 [坐标] ★

- 【出处】Sanchez-Gonzalez, Bapst, Cranmer & Battaglia, "Hamiltonian
  Graph Networks with ODE Integrators", arXiv:1909.12790, **NeurIPS 2019
  ML4 Physical Sciences workshop**(~236 引)。
- 【内容】图网络学习哈密顿量+可微 ODE 积分器:关系结构+守恒结构+
  数值积分三合一;长滚出优于标准 GNS。
- 【对我们的映射】**本仓 NBody 头(LiquidNBodyModel=ctx 推断+对势+
  Verlet)的最近邻先例**:同一"结构三合一"哲学,差异轴=ctx 通道
  (我们经 liquid 核推断,其无推断层)+头形式(径向对势 vs 自由
  H 网络)。N1 定位表必引:既证明"守恒注入进图网络"路线成立,
  又凸显推断条件化空位仍属本仓。
- 【适用条件】N1 Related Work/定位表。
- 【验证状态】社区已验证(workshop,~236 引);定位立即可用。

### 28.5 NBody 聚合语义审计 [行动→NBODY-POOL-AUDIT]

- 【内容】闭合轮 95 恒等式的声明边界("NBody 粒子池化无网格
  telescoping,未审计如实注记"):①代码审计 model.py 粒子池化的
  聚合算子语义(mean/sum/对势直和);②ctx 信息 Fisher 式探针
  (field_identifiability_probe --meanpool 模式移植),判读=NBody
  ctx 通道信息保留率——文献预期(§28.3)无 M2 型湮灭,若实测相反
  即重大异常如实入档。T1 预算(秒级闭式+代码审计);判负标准执行前
  预注册 PRD §19。
- 【对我们的映射】轮 95 恒等式适用边界的实证闭合;NBody 线首次
  获得与 M1/M2 同规格的机制证据。
- 【适用条件】N1 机制链;判读入 PRD §19。
- 【验证状态】对本仓待执行(下心跳,预注册先行)。

### 蒸馏结论 23

四 [坐标] + 一 [行动](NBODY-POOL-AUDIT 入队)。第 28 族;S1 计数
重置(本轮有 [行动] 产出)。蒸馏轮第 21 次达标。选族启发式(轮 114)
二次起效并升级验证状态(n=2)。

## 29. 经验蒸馏 24(轮 124,2026-09-24,QUEUE-EMPTY 轮):模拟基推断/摊销参数后验族(SBI/NPE)

> 新 query 族(与前 28 族零重叠:grep 全库 SBI/simulation-based/neural
> posterior 无既有坐标——§12.1 amortization gap 是 VAE 优化缺口命名,
> §20 是 UQ 量化方法论,均非"模拟+神经估计做后验"范式本身)。标记:
> [坐标](全部;无 [行动]——见蒸馏结论 24 的 S1 注记)。
> 三槽:① 领域综述 ② 机制直击(SBC/coverage 诊断)③ 对照式
> (摊销 vs MCMC)。题录当场核验(AMM-015)。

### 29.1 SBI 奠基综述 [坐标]

- 【出处】[Cranmer, Brehmer & Louppe, "The frontier of simulation-based inference", PNAS 117(48):30055-30062, 2020,~2,100+ 引](https://www.pnas.org)
- 【内容】似然不可得(only simulators)场景下,以神经估计器(NPE/NRE/
  ALE 谱系)对模拟器参数做后验推断的奠基综述;顺序/摊销两策略分野。
- 【对我们的映射】本仓 ctx 推断=**摊销参数后验**(M1 ω、M2 c(x) 系数
  的 amortized posterior),SBI 是该范式的社区正名与标准工具体系
  (sbi 包);N1 定位可用 SBI 术语锚定 ctx 推断通道(推断=amortized
  system ID),并与 §12.1 amortization gap(优化的缺口)衔接为
  "范式名+缺口名"两层表述。
- 【适用条件】一切 ctx 推断的 N1 定位表述与相关工作章。
- 【验证状态】题录当场核验(卷期页码为检索面记录,引用数标注约数);
  社区已验证;对本仓为定位引用(非新实验方向)。

### 29.2 SBC:摊销校准的标准诊断 [坐标]

- 【出处】[Talts, Betancourt, Simpson, Vehtari & Gelman, "Validating
  Bayesian Inference Algorithms with Simulation-Based Calibration",
  arXiv:1804.06788, 2018](https://arxiv.org/abs/1804.06788)
- 【内容】SBC 原始诊断:后验样本对先验预测抽样的秩应均匀,偏离即校准
  失败;expected coverage 为同族检验(可信区间覆盖率=名义水平)。
- 【对我们的映射】**D-1 判负获得社区标准命名**:coverage 1.6%/0/0
  ≪名义 95%(过度自信)实测即 SBC/coverage 类检验的失败案例;N1 的
  "UQ 表述上限 L2"判定由此可引标准诊断文献支撑(不是私有判据)。
- 【适用条件】一切校准声明、D-1 判读引用、UQ 章表述。
- 【验证状态】题录当场核验;社区已验证;对本仓为诊断命名引用。

### 29.3 ★信任危机:摊销后验的过度自信通病 [坐标]

- 【出处】[Hermans, Begy, Delaunoy, Rozet, Louppe & Weniger, "A Trust
  Crisis In Simulation-Based Inference? Your Bayesian Algorithms Should
  Be Explored More Than Exploited", arXiv:2110.06581, 2021(TMLR 2022),
  ~137 引](https://arxiv.org/abs/2110.06581)
- 【内容】系统实证:当前摊销 SBI 算法普遍产出**过度自信**、计算上
  不忠实/欠精炼(c-2,invalid)的后验近似,提出 expected coverage
  诊断与更充分的训练方案。
- 【对我们的映射】D-1 的失败模式(过度自信方向)是该文献记录的
  **摊销后验已知通病**在本仓的具体实例——N1 UQ 段(L2 上限)的
  定位从"我们的模型过度自信"升级为"摊销后验的已知失效模式,本仓
  有独立诊断数字与上限纪律";同作者 Averting-A-Crisis(TMLR 2021,
  验证式早停)为处方参照。
- 【适用条件】N1 UQ/L2 段、一切摊销推断声明与边界声明。
- 【验证状态】题录当场核验(arXiv ID+作者+TMLR 2022);社区已验证。

### 29.4 可微 expected coverage 正则:校准感知训练处方 [坐标]

- 【出处】[Falkiewicz, Cerqueira, Lefebvre, Koenig, Delaunoy & Louppe,
  "Calibrating Neural Simulation-Based Inference with Differentiable
  Expected Coverage", NeurIPS 2023,~20 引](https://proceedings.neurips.cc)
- 【内容】把 expected coverage 诊断可微化,作为正则进 NPE/NRE 训练
  (校准感知训练)。
- 【对我们的映射】L2→L3(校准区间)升级路径的社区处方=coverage
  正则化训练;登记为**停车场参照坐标**(L3 与云档均在停车场,不触发;
  处方谱系入 §17.3 同位)。
- 【适用条件】停车场重启(T2/T3/Kaggle)时的 UQ 升级处方路由。
- 【验证状态】题录当场核验(NeurIPS 2023);社区已验证;停放不触发。

### 29.5 对照槽:统计学社区综述与摊销可靠性边界 [坐标]

- 【出处】Zammit-Mangion, Sainsbury-Dale & Huser, "Neural Methods for
  Amortized Inference", Annual Review of Statistics and Its Application,
  2025(arXiv 2024-10,~154 引;统计学视角综述,neural Bayes estimation
  与 NPE 二分)。
- 【内容/映射】统计学社区对摊销推断的规范综述:"训练前置换推理速度,
  精度依赖训练覆盖度,诊断(SBC/coverage)必需"——与本仓 ctx=摊销
  估计+D-1 上限纪律互证;对照面:Hermans et al. AALR-MCMC(摊销似然比
  +MCMC 采样,~328 引)代表"摊销换可靠性"混合路线——摊销不是唯一
  精度档,弱坐标:**AALR-MCMC 的 venue/年份检索面记 PMLR 2019 与
  AISTATS 2020 存疑,登记 SCAN-AUDIT 复核**。
- 【适用条件】N1 相关工作章(摊销推断定位与可靠性边界)。
- 【验证状态】综述题录基本核验(年份一致,arXiv ID 不写未核值);
  AALR venue 带 ? 登记 SCAN-AUDIT。

### 蒸馏结论 24

5 [坐标](29.3 ★)+ 0 [行动]。第 29 族;**S1 计数不重置(无
[行动] 产出,累计 1/2——下个蒸馏轮必须产出 [行动] 类条目,否则评估
收口)**。蒸馏轮第 22 次达标(≥1 条入库)。选族按轮 114 启发式
(自家钩子=ctx 推断摊销后验+D-1 过自信判负 → SBI/NPE 族),零重叠
grep 确认;题录当场核验,1 处弱坐标带 ? 登记 SCAN-AUDIT。

## 30. 经验蒸馏 25(轮 125,2026-09-24,QUEUE-EMPTY 轮):训练随机性/损失景观族

> 新 query 族(与前 29 族零重叠:§20.2 引 Wilson & Izmailov 是 UQ/集成
> 理论语境的模式多样性,本族是**优化景观与训练随机性的方法论轴**
> ——模式连接机制/符号-置换对称/种子敏感度测量;§17.1 Rahaman 是
> 函数拟合频率原理,均不同轴)。选族过程留痕:尖锐前沿族首候选因
> 机制引用核心(Rahaman)撞 §17.1 当场放弃(轮 114 启发式的机制核对
> 扩展,n=3)。标记:[坐标]×3 + [行动]×1。三槽:① 景观综述/模式
> 连接 ② 种子敏感度机制 ③ 对照式(对称性盆地 vs 模式连接)。
> 题录当场核验(AMM-015)。

### 30.1 模式连接:不同种子的解由低损失路径相连 [坐标]

- 【出处】[Garipov, Izmailov, Podoprikhin, Vetrov & Wilson, "Loss
  Surfaces, Mode Connectivity, and Fast Ensembling of DNNs", NeurIPS
  2018;平行:Draxler et al., AISTATS 2018](https://arxiv.org/abs/1802.10026)
- 【内容】独立训练(不同种子)的解通常由训练误差不升的简单曲线连接
  (mode connectivity);快照集成由此可行。
- 【对我们的映射】本仓 3-seed 协议=迷你 DE(§20.2)的解-多样性面
  获得景观机制:各 seed 的解若模式连接,则集成多样性=盆地内位置差;
  若不连接(见 30.3 的符号对称盆地),多样性=机制不同的解——这给出
  "seed 间数字分歧是两种性质"的可检验区分。
- 【适用条件】一切多种子数字分歧的解读与 N1 实验章表述。
- 【验证状态】题录当场核验;社区已验证;对本仓为方法论定位引用。

### 30.2 种子敏感度:种子对结论的实质影响 [坐标]

- 【出处】[Schader et al., "Don't let your analysis go to seed: on the
  impact of random seeds", 2024(PMC 收录)](https://pmc.ncbi.nlm.nih.gov)
- 【内容】随机种子对 ML 结论(含因果效应估计)有实质影响,种子敏感性
  应作为结果表述的一部分报告。
- 【对我们的映射】本仓"1-seed 筛查→3-seed 终局"分级纪律的文献面:
  筛查级结论必须带 seed 口径限定词(现行惯例)的做法与该文献的规范
  一致;.seed 敏感异常(轮 113 符号反转)按 30.3 机制对账。
- 【适用条件】一切筛查级数字的表述与 PLAYBOOK 口径条款互证。
- 【验证状态】题录当场核验(标题+年份+PMC 收录);社区已验证。

### 30.3 ★符号对称盆地:机制性不同的解 [坐标]

- 【出处】[Lubana, Dick, Tanaka, "Mechanistic Mode Connectivity",
  ICML 2023,arXiv:2211.08422,~93 引](https://arxiv.org/abs/2211.08422);
  参照:Ainsworth, Hayase & Srinivasa "Git Re-Basin"(ICML 2023);
  Entezari, Sedghi & Saukh 置换不变性立场文(arXiv 2022)
- 【内容】置换对称使解精确等价可连;**符号对称**(奇激活如 tanh 的
  入/出权同翻)诱导**机制上不同**的盆地——不同 seed 落入何盆地由
  架构与训练制度决定;置换对齐后大部分解同一盆地(Git Re-Basin)。
- 【对我们的映射】**轮 113 记录的开放异常(半群符号反转 1/3 全容量
  点恒定)获得机制框架**:tanh 能量网的符号对称盆地=种子落入符号
  翻转的机制性不同解,"全容量点恒定"=盆地归属随容量稳定。异常
  从"复现性疑虑"升级为"符号对称盆地的实例化",可被探针证伪/证实
  (见 [行动])。
- 【适用条件】SIGN-FLIP-PROBE 机制对账;一切 seed 间定性分歧解读。
- 【验证状态】题录当场核验(arXiv ID+PMLR v202+引用数约数);
  社区已验证。

### 蒸馏结论 25

3 [坐标](30.3 ★)+ 1 [行动](SIGN-FLIP-PROBE 入队,engineering)。
第 30 族;**S1 重置(有 [行动] 产出);蒸馏轮第 23 次达标**。选族
启发式 n=3(机制引用核心先 grep 既有族,尖锐前沿族撞 §17.1 当场
放弃);弱坐标:arXiv 2026-01 "Training instability follows
low-dimensional dynamics" 作者未核,带 ? 登记 SCAN-AUDIT。

## 31. 经验蒸馏 26(轮 128,2026-09-24,QUEUE-EMPTY 轮):离散化轴——学习流映射 vs 学习向量场族(BEA/修正方程)

> 新 query 族(与前 30 族零重叠:§10.2 是守恒的硬/软路线、§18 是评估
> 协议、§21 是守恒量发现,均不含"有限 dt 下网络到底学到了什么对象"
> 的离散化迁移轴)。自家钩子:verlet_order_probe(轮 104)测的是**真
> 积分器**的收敛阶,已训练头在非训练 dt 上的行为从未测过;N1 全文
> 以"学到 H(q,p)"为对象语言,该声明的 dt 迁移面是空白。标记:
> [坐标]×3 + [行动]×1。三槽:① BEA/修正方程谱系 ② 求解器依赖机制
> ③ 对照式(跨步长迁移的架构对照)。题录当场核验(AMM-015)。

### 31.1 BEA/修正方程:辛方法长期守恒的经典机制 [坐标]

- 【出处】Reich, S. "Backward error analysis for numerical integrators",
  SIAM J. Numer. Anal., 1999,~391 引;体系:Hairer, Lubich & Wanner,
  _Geometric Numerical Integration_ Ch. X;近期:McLachlan et al.
  (2022/2023,共轭辛方法的修正哈密顿量系统确定)。
- 【内容】辛积分器的数值解是附近"修正方程"的精确解——修正哈密顿量
  H + dt^k H_k 的近守恒是辛方法长期稳定的机制。
- 【对我们的映射】本仓 VV+学习 H 的 O(dt²) 能量误差与长期稳定,
  其解析对象是修正哈密顿量而非 H 本身;N1 的 dt 尺度声明可以
  BEA 语言精确化("辛滚出守恒的是修正 H,学习 H 在有限 dt 的意义
  由 31.2/31.3 的迁移行为界定")。
- 【适用条件】N1 methods/discussion 的 dt 尺度表述。
- 【验证状态】题录当场核验(期刊+年份+引用约数);社区已验证。

### 31.2 ★辛神经网络的修正哈密顿量守恒 [坐标]

- 【出处】[M. David, T. Hudson, P. Wales, "Symplectic Learning for
  Hamiltonian Neural Networks", 2023,~98 引](https://arxiv.org/abs/2404.08816)
- 【内容】证明辛神经网络积分器长期守恒的标量量是**修正哈密顿量**
  (接近但非等于学习 H),BEA 给出保证。
- 【对我们的映射】本仓"能量守恒由构造保证"(P0-3)的精确化:守恒的
  是学习 H 的修正版本;学习 H 与真 H 的差距(辨识误差)与修正项
  (dt² 项)在 N1 中须分列——为 dt 迁移探针([行动])提供读数框架。
  正式 venue 未核(检索面为 CNRS 个人页),带 ? 登记 SCAN-AUDIT。
- 【适用条件】N1 守恒主张的精确化;dt 迁移探针读数框架。
- 【验证状态】题录基本核验(作者/年份/arXiv 检索面一致,venue 存疑)。

### 31.3 训练求解器决定学到的参数:跨步长迁移的架构对照 [坐标]

- 【出处】Coelho et al. "Neural ODE Parameters are Dependent on the
  Training Solver"(OpenReview,年份带 ? 登记 SCAN-AUDIT);对照面:
  Chen, Zhang, Arjovsky & Bottou "Symplectic Recurrent Neural Networks"
  (ICLR 2020,arXiv:1909.13334——明言目标含"训练未经历的时间步长/
  积分器阶的泛化");Jin et al. SympNets(2020)与 PSNN(伪辛网络,
  显式面向未见步长)。
- 【内容】固定步长求解器训练的神经动力学模型学到的是**离散化特定的
  流映射**;跨 dt/求解器迁移需要架构级措施(辛结构/伪辛)或显式的
  多 dt 训练。
- 【对我们的映射】本仓头在固定 dt=0.1 轨迹上训练——"学到 H"还是
  "学到 dt=0.1 映射"未经检验;SRNN/PSNN 的跨步长泛化主张给出
  对照架构面(本仓 VV+T/V 头介于两者:结构辛但 H 由数据定)。
- 【适用条件】MAP-VS-FLOW 探针([行动])的预期行为框架与 N1
  "学到 H"声明的范围限定。
- 【验证状态】SRNN 题录当场核验;Coelho 年份带 ?;社区已验证。

### 蒸馏结论 26

3 [坐标](31.2 ★,1 处 venue 带 ?)+ 1 [行动](MAP-VS-FLOW 入队,
engineering)。第 31 族;**S1 重置(有 [行动] 产出);蒸馏轮第 24 次
达标**。选族启发式 n=3 维持(机制核对通过:§10/§18/§21 均无
BEA/dt 迁移轴)。

## 32. 经验蒸馏 27(轮 131,2026-09-24,QUEUE-EMPTY 轮):少样本适配/跨任务迁移族(in-context 与梯度适配)

> 新 query 族(与前 31 族零重叠:§19 TSFM 是零样本预测器审计、§29 SBI
> 是参数后验推断、§30 是优化景观,均非"少样本适配新动力系统"的机制
> 轴;§14 FiLM 是条件化机制本体)。自家钩子:M3 pretrain_finetune 协议
> 在库(PRD P1-2,Poseidon 同型问题)+ctx 推断的隐式 in-context 本质
> 未被命名。标记:[坐标]×3 + [行动]×1。三槽:① PDE 基础模型少样本
> 微调 ② in-context 算子学习 ③ 对照式(meta vs in-context)。
> 题录当场核验(AMM-015)。

### 32.1 Poseidon:PDE 基础模型的少样本微调范式 [坐标]

- 【出处】[Herde, Raonić et al. (ETH Zurich), "Poseidon: Efficient
  Foundation Models for PDEs", NeurIPS 2024, arXiv:2405.19101](
  https://arxiv.org/abs/2405.19101)
- 【内容】多尺度算子 transformer,6 族 PDE ~400K 轨迹预训练;
  layerwise 高效微调在 ~15 个下游任务(含 OOD)少样本超越基线。
- 【对我们的映射】本仓 M3 协议(pretrain mix {0.8,1.0,1.2}→finetune
  c=1.5 少样本)是 Poseidon 范式的单机微缩;N1 related-work 可引
  该范式为 M3 的社区坐标。
- 【适用条件】M3/迁移线的一切表述与 related-work。
- 【验证状态】题录当场核验(NeurIPS 2024+arXiv ID);社区已验证。

### 32.2 ★ICON 与哈密顿系统的 in-context 学习 [坐标]

- 【出处】[L. Yang et al., "In-context operator learning with data
  prompts for differential equations", 2023, arXiv:2304.07993,~160 引](
  https://arxiv.org/abs/2304.07993);参照:AI-Hamilton(OpenReview,
  哈密顿系统 ICL,作者/年份未核带 ? 登记 SCAN-AUDIT)
- 【内容】ICON 以数据提示在推理时学习新算子(隐式少样本);AI-Hamilton
  将 ICL 直接用于哈密顿系统建模。
- 【对我们的映射】**本仓 ctx 推断=隐式 in-context 适配的实例**:
  前缀轨迹即 prompt,ctx 即对未见 ω/c(x) 的推理时适配——此前该机制
  只有摊销推断命名(§29),ICL 命名补足适配语义面;AI-Hamilton 是
  哈密顿域的直接先例(N1 定位表新增一线)。
- 【适用条件】N1 机制命名与定位表;ctx 推断语义的一切表述。
- 【验证状态】ICON 题录当场核验;AI-Hamilton 弱坐标带 ?。

### 32.3 对照:梯度适配 vs 循环隐式适配 [坐标]

- 【出处】Nagabandi et al. "Learning to Adapt in Dynamic, Real-World
  Environments through Meta-Reinforcement Learning"(ICLR 2018,~950 引;
  GrBAL 梯度式 vs ReBAL 循环式直接对照)
- 【内容】在真实动力系统上直接对比 MAML 式梯度快适配与循环式隐式
  (in-context)适配:循环更廉价在线,梯度式更显式可控。
- 【对我们的映射】本仓两线的规范对照语言:prefix 摊销/ctx 推断=
  ReBAL 型隐式适配,M3 finetune=GrBAL 型梯度适配——M3 与 prefix
  的关系由此获得社区对照先例(§32.1 的 Poseidon 微调亦属梯度侧)。
- 【适用条件】M3/迁移/prefix 线的关系表述。
- 【验证状态】题录当场核验(ICLR 2018+引用约数);社区已验证。

### 蒸馏结论 27

3 [坐标](32.2 ★,AI-Hamilton 弱坐标带 ?)+ 1 [行动](ICL-M3 入队,
engineering)。第 32 族;**S1 重置(有 [行动] 产出);蒸馏轮第 25 次
达标**。选族启发式 n=3 维持(机制核对:M3 在库工具即钩子)。

## 33. 经验蒸馏 28(轮 136,2026-09-24,QUEUE-EMPTY 轮):快慢/多尺度动力系统族

> 新 query 族(与前 32 族零重叠:§18 混沌是长时程评估协议轴、§31 是
> 离散化迁移轴、§13.1 CfC 是工程前沿,均非"单一系统内多时标分离"的
> 机制轴)。自家钩子:本仓全部家族为单时标(弹簧 ω、波场 c、NBody
> 短程)——快慢分离(刚性振荡+慢漂移)从未进入任何实验,N1 的时标
> 适用范围是空白。标记:[坐标]×3 + [行动]×1。三槽:① 快慢架构谱系
> ② 刚性求解机制 ③ 对照式(频域分离失效母题)。题录当场核验
> (AMM-015)。

### 33.1 快慢神经网络:奇异扰动系统的数据驱动建模 [坐标]

- 【出处】Serino & Peitzman(DA Serino), "Fast-Slow Neural Networks for
  Learning Singularly Perturbed Dynamical Systems", arXiv 2024(Johns
  Hopkins,~10 引)
- 【内容】FSNN 显式建模奇异扰动系统的快慢分解(快变量耗散至慢流形),
  数据驱动学习多时标模型。
- 【对我们的映射】本仓家族全部单时标;快慢分离是 N1 时标适用范围的
  未测空白(§18.3 混沌空白的多尺度姊妹空白);FSNN 给出"显式分离"
  的架构对照面。
- 【适用条件】N1 时标范围声明;快慢探针的架构对照。
- 【验证状态】题录当场核验(作者/年份/题名;arXiv ID 检索面未展示
  不写);社区已验证;对本仓为空白定位引用。

### 33.2 刚性神经 ODE 的隐式/层级求解 [坐标]

- 【出处】Fronk & Petzold, "Training stiff neural ordinary differential
  equations with implicit schemes", 2024,~21 引;Liu et al. "Hierarchical
  Deep Learning of Multiscale Differential Equations", 2022,~136 引
- 【内容】刚性(快分量快速变化)使显式求解器训练/评估失效;隐式单步
  与层级时间步进器(hierarchy of time-steppers)是两条处方。
- 【对我们的映射】本仓 VV 为显式积分器:若快时标 ω_fast 使 dt 不解析
  (ω_fast·dt≳O(1)),无论 H 学得多好,显式 VV 都会失效——**时标上限
  是架构×dt 联合性质**,N1 的适用声明须含"dt 解析最快时标"条款;
  层级时间步进=慢变量模型的可选对照架构。
- 【适用条件】N1 时标条款;快慢探针的 dt regime 设计。
- 【验证状态】题录当场核验(作者/年份/引用约数);社区已验证。

### 33.3 ★频域可分 HNN:多时标失效的命名先例 [坐标]

- 【出处】Li et al., "Frequency-Separable Hamiltonian Neural Network",
  arXiv 2026(检索面:摘要明言"HNN 变体常无法捕捉跨多时标的复杂时间
  动力学";细节未核带 ? 登记 SCAN-AUDIT);母题:弹性摆(快弹簧振荡
  ω_s 与慢摆动 ω_p 能量交换,经典两时标系统)
- 【内容】频率分离化为 HNN 的补救架构;弹性摆=快慢双时标的标准母题
  (能量在快慢模态间慢交换)。
- 【对我们的映射】本仓 dim=2 可分头可直接表示弹性摆 H(T(p)+V(r),
  r 为 2D 位置)——**FASTSLOW-PROBE 的载体家族无需新架构**:弹性摆
  上测头能否同时捕捉快模态(dt 解析)与慢交换(T≫1/ω_p 长视距),
  失效模式即 §33.2 的刚性签名。
- 【适用条件】FASTSLOW-PROBE 的载体与预言框架。
- 【验证状态】题录部分核验(标题/作者/年份一致;摘要引语检索面一致;
  细节带 ?);社区已验证。

### 蒸馏结论 28

3 [坐标](33.3 ★,细节带 ?)+ 1 [行动](FASTSLOW-PROBE 入队,
engineering)。第 33 族;**S1 重置(有 [行动] 产出);蒸馏轮第 26 次
达标**。选族启发式 n=3 维持(机制核对:§18 混沌=评估协议轴,§31=
离散化迁移轴,均非多时标机制轴)。

## 34. 经验蒸馏 29(轮 139,2026-09-24,QUEUE-EMPTY 轮):粗粒化/有效动力学族(Mori-Zwanzig 与学习慢变量)

> 新 query 族(与前 33 族零重叠:§33 是多时标**直接拟合**的失效轴,
> 本族是"改学慢变量有效动力学"的**替代建模轴**——Mori-Zwanzig 形式
> 化+学习粗粒化;§28 GNN 是算子架构,§29 是参数后验)。钩子:轮 137
> FASTSLOW 双时标失效的文献处方面——直接拟合失败时,社区的答案是
> 学慢变量。标记:[坐标](全部;无 [行动]——S1 如实累计 1/2)。
> 三槽:① CG-GNN 谱系 ② 有效动力学学习方法 ③ 对照式(直接 vs 约化的
> 权衡)。题录当场核验(AMM-015)。

### 34.1 CG-GNN:图网络粗粒化分子动力学 [坐标]

- 【出处】Husic et al., "Coarse graining molecular dynamics with graph
  neural networks", J. Chem. Phys. 2020,~277 引;近期:Lyu et al.
  (PRR 2023,~39 引,Mori-Zwanzig 形式化的 ML-CG)
- 【内容】GNN 直接从全原子轨迹学习粗粒化映射与力场,访问更大系统与
  更长时间尺度。
- 【对我们的映射】FASTSLOW 失效(直接拟合双时标失败)的文献处方面:
  慢变量有效动力学是替代路线;与 §28 GNN 族衔接(GNN 既做算子也做
  粗粒化映射)。
- 【适用条件】N1 时标局限的"替代路线"表述。
- 【验证状态】题录当场核验(期刊+年份+引用约数);社区已验证。

### 34.2 有效动力学的可解释/自适应学习 [坐标]

- 【出处】"Interpretable learning of effective dynamics (iLED)",
  Proc. R. Soc. A, 2025;Kičić et al., "Adaptive learning of effective
  dynamics for online modeling", 2023
- 【内容】多尺度系统的有效动力学提取与在线预报:可解释化(iLED)与
  自适应窗口(Kičić)两条路线。
- 【对我们的映射】若本仓走慢变量路线,iLED 的可解释性诉求与本仓
  "H 是可读对象"的立场一致;登记为时标局限的处方谱系坐标。
- 【适用条件】停车场重启时多尺度方向的设计参照。
- 【验证状态】题录当场核验(期刊+年份);社区已验证;停放参照。

### 34.3 对照:直接动力学 vs 约化模型的权衡 [坐标]

- 【出处】Loose et al., "Coarse-Graining with Equivariant Neural
  Networks", 2023(明确陈述"accuracy vs efficiency trade-off 是 CG
  建模的中心挑战");综述:Guenza 2025(WIREs)
- 【内容】直接细尺度动力学保真但代价高;粗粒化换效率与长时程,
  依赖 CG 映射保留关键多体相互作用——"何时学约化模型"的三条件
  (算力不可行/只关心宏观量/映射保结构)。
- 【对我们的映射】为轮 137 失效提供解读框架:本仓头在双时标上
  属"直接动力学"路线,其失效触发三条件的第 (a)/(b) 条——时标
  超限时学有效动力学是文献正路;与本仓 §33.2 的时标上限条款互补。
- 【适用条件】N1 时标条款的补充讨论。
- 【验证状态】题录当场核验(作者/年份;期刊部分检索面);社区已验证。

### 蒸馏结论 29

3 [坐标](无 ★,全部为轮 137 失效的处方/框架面)+ 0 [行动]。
第 34 族;**S1 如实累计 1/2(无 [行动];族空间饱和信号——连续两轮
无 [行动] 将触发收口评估)**。蒸馏轮第 27 次达标(≥1 条入库)。
选族启发式 n=3 维持(机制核对:TSFM §19/SINDy §23 两次拦截在案)。

## 35. 经验蒸馏 30(轮 145,2026-09-24,QUEUE-EMPTY 轮):grokking/延迟泛化族(训练时间轴上的泛化涌现)

> 新 query 族(与前 34 族零重叠:§17 谱偏置=跨频率的**学习顺序**轴,
> §26 缩放律=模型/数据/算力的**规模幂律**轴,§30=种子间**解的景观**
> 轴——本族是单模型**训练时间轴**上的记忆→泛化转变动力学,
> grokking/delayed generalization/epoch-wise double descent)。
> 钩子:轮 143 FASTSLOW-2 BUDGET_DOMINANT 的现象形状——1-step 拟合
> 已饱和(train_loss 2.5e-6)而 rollout 泛化随训练量持续改善 5.4×
> ("训练目标上已解决的快模式 vs 评估准则上仍在改善的慢模式"=
> 双速度叙事的实例)。标记:[坐标] ×3(2 ★)+ [行动] ×1。
> 三槽:① 综述面 ② 机制直击 ③ 对照式(与 double descent 的统一)。
> 题录当场核验(AMM-015,4 条全部作者/年份/venue 确认)。

### 35.1 综述面:grokking 是普遍性质而非玩具现象 [坐标]

- 【出处】Bertolotti & Cazzola, "A Survey on Grokking", ACM Computing
  Surveys, accepted 2026-04(米兰大学);Humayun, Balestriero &
  Baraniuk, "Deep Networks Always Grok and Here is Why", ICML 2024,
  arXiv:2402.15555,~82 引
- 【内容】综述面:grokking=训练 loss 达近零后测试性能才延迟改善;
  Humayun 等论证 grokking 不是模块算术玩具特例,而是深度网络训练
  的普遍性质(非线性网络广泛呈现延迟泛化),并给出为何如此的解释。
- 【对我们的映射】为"本仓 rollout 泛化随预算持续改善"提供现象学
  定名:这不是本仓特有怪癖,是训练动力学的标准形状;N1 若讨论
  训练量-泛化关系有标准文献坐标可引。
- 【适用条件】训练量-泛化关系的表述与 Limitations 讨论;多 seed
  终局参照。
- 【验证状态】题录当场核验(ACM CSUR accepted 2026-04 作者确认;
  ICML 2024 + arXiv:2402.15555 作者确认);社区已验证。

### 35.2 机制面:傅里叶算法涌现与 weight decay 驱动的记忆→泛化转变 ★ [坐标]

- 【出处】Nanda et al., "Progress Measures for Grokking via
  Mechanistic Interpretability", ICLR 2023(~1188 引;前身=
  LessWrong/Alignment Forum 2022 "A Mechanistic Interpretability
  Analysis of Grokking");Gromov, "A simple and interpretable model
  of grokking modular arithmetic"(OpenReview,可解析 ansatz)
- 【内容】模块加法 transformer 逆向工程:网络学的是傅里叶表示上的
  trig-identity 算法;grokking 转变=记忆组件被 weight decay 逐渐
  削弱、泛化算法占比上升——**降低 weight decay 只延迟不阻止**
  grokking;progress measures 使泛化进展可定量追踪(转变前就有
  可测信号)。
- 【对我们的映射】轮 143 的"优化限制"叙事获得机制面参照:泛化
  解可以已存在于训练中、只是被记忆解压制——BUDGET_DOMINANT 可能
  是"慢泛化模式与快记忆模式竞争训练量"的表现,而非单纯欠拟合;
  若本仓探针需要区分两者,progress-measure 思路(找泛化的可测
  前导量)是处方。
- 【适用条件】GROK-CURVE 判读设计(见 [行动]);N1 训练动力学
  段落。
- 【验证状态】题录当场核验(ICLR 2023 + 引用约数 + 前身帖确认);
  社区已验证(大量复现)。

### 35.3 对照槽:grokking 与 double descent 的双速度统一 ★ [坐标]

- 【出处】Davies, Langosco & Krueger, "Unifying Grokking and Double
  Descent", arXiv:2303.06173(2023,~82 引;NeurIPS 2022 文献面)
- 【内容】统一框架:两现象同源于**模式学习速度差**——快学习模式
  倾向记忆、慢学习模式倾向泛化;训练体制最终 favors 慢泛化模式时,
  表现为 grokking(时间轴)或 epoch-wise double descent(测试误差
  隆起)。"Grokking, like epoch-wise double descent, occurs when slow
  patterns generalize well and are ultimately favored by the training
  regime, but are preceded by faster-learning patterns"。
- 【对我们的映射】轮 143 钩子的**直接文献对**:"1-step 拟合饱和
  (快模式已解决)而 rollout 泛化仍在改善(慢模式后来居上)"=该
  统一框架的实例形状;BUDGET_DOMINANT 的"加大即愈"在此获得机制
  语义——不是"同一解的渐近收敛"而可能是"泛化解需要更长训练才能
  胜出"。判读可分:若步数阶梯呈现突变转折⇒两模式竞争叙事;若
  平滑渐近⇒单模式渐近拟合叙事(见 [行动] 判负分支)。
- 【适用条件】GROK-CURVE 判读的预注册分支;N1 训练量-泛化讨论。
- 【验证状态】题录当场核验(arXiv:2303.06173 作者/年份/引用确认);
  社区已验证(框架被广泛引用,亦有批评面见 LessWrong QAPR 5——
  非定论,如实注记)。

### 35.4 [行动] GROK-CURVE:训练量-泛化函数形状探针(入队)

- 【出处】本节三坐标的合成行动面;载体=house M1 弹簧族。
- 【内容】M1 弹簧 held-out 族(pool 同 E1 口径)上 hidden64 固定、
  train_steps 阶梯 {2500,5000,10000,20000,40000},逐点 k100 rollout
  rel MSE 曲线(log-log);判读=**平滑渐近**(轮 143 BUDGET_DOMINANT
  趋势外推,单模式拟合叙事)vs **突变转折**(grokking 型延迟泛化,
  §35.3 双模式竞争叙事)。判负=曲线平滑无突变 ⇒ grokking 命名不
  适用本仓训练体制,只保留渐近改善记录(N1 不引入 grokking 表述)。
- 【族边界与护栏】载体与判据均为泛化动力学轴(grokking 族第 1 轮),
  非 fastslow 载体(段内 fastslow 迭代预算 1/2 保留不动);1-seed
  筛查口径,多 seed 终局=停车场。
- 【适用条件】T1 可行动:总步数和 77500 ≈ 2×40k H64 实测(~1min)
  ≈ 3-4min+评估,est 10min 富余。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 30

3 [坐标](2 ★)+ 1 [行动](GROK-CURVE 入队,engineering)。
第 35 族;**S1 重置([行动] 产出)**。蒸馏轮第 28 次达标(≥1 条入库
+新目标)。机制核对:grokking/double descent/delayed generalization
全库 grep 零命中,§17/§26/§30 边界族头声明。选族启发式 n=4(钩子=
轮 143 判读现象形状,文献收割 T1 化)。

## 36. 经验蒸馏 31(轮 148,2026-09-24,QUEUE-EMPTY 轮):梯度噪声/临界 batch size 族(优化噪声与隐式正则化)

> 新 query 族(与前 35 族零重叠:§30 是种子间**解的景观**(模式连接/
> 盆地),本族是**优化噪声本身的可测统计**与 batch/LR 标度——梯度
> 噪声尺度、临界 batch size、大 batch 泛化差)。钩子:全仓 batch=64
> 从未消融,且轮 126 符号反转的种子敏感性(§30)存在"敏感性来自
> 梯度噪声水平"的未检假说——GNS 是该假说的第一个可测代理。
> 标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① 奠基统计量 ② 机制面
> (大 batch 泛化差)③ 对照槽(batch/LR 等价)。题录当场核验(AMM-015,
> 3 条全部 arXiv ID/venue/作者确认)。

### 36.1 奠基统计量:gradient noise scale 预测最大有效 batch ★ [坐标]

- 【出处】McCandlish et al. (OpenAI), "An Empirical Model of
  Large-Batch Training", 2018, arXiv:1812.06162,~474 引;现代复现:
  Allen AI OLMo critical batch size revisit(2025)
- 【内容】定义可测量统计量 **gradient noise scale**(B_noise ∝
  梯度协方差迹/均值梯度范数²),预测最大有效 batch size(B_noise
  之下线性加速,之上收益递减);B_noise 一般随训练进度增长;估计
  只需采样若干小 batch 梯度(B_simple 简化式),**无需长训练**。
- 【对我们的映射】直接 T1 化:house M1 载体上闭式梯度统计(与
  fisher_j/grad_path_probe 同型,秒-分钟级);回答"batch=64 在本
  仓体制的噪声/信号谱何处"——为种子敏感性(§30)提供优化噪声
  水平的第一手读数,也为未来 T2/T3 派发的 batch 选择提供依据。
- 【适用条件】SGD 族优化器(Adam 适用性有修正面,如实注记);
  估计噪声大,1-seed 筛查口径。
- 【验证状态】题录当场核验(arXiv:1812.06162+作者+引用约数);
  社区已验证(OLMo 等现代复现)。

### 36.2 机制面:大 batch→尖锐极小值→泛化差 [坐标]

- 【出处】Keskar et al., "On Large-Batch Training for Deep Learning:
  A Generalization Gap Approach", ICLR 2017, arXiv:1609.04836,
  ~5000 引
- 【内容】大 batch 方法倾向收敛到训练损失的**尖锐极小值**(大正
  曲率),与更差泛化相关;小 batch 的梯度噪声起**隐式正则化**作用,
  偏向平坦极小值。
- 【对我们的映射】若 GNS 探针测得本仓处于小 batch/高噪声区,则
  轮 126 的种子间解差异(符号盆地)有了噪声侧解释通道;若处于大
  batch/低噪声区,prefix 优势的种子稳定性问题另寻解释。为 §30 族
  的机制链补优化噪声一环。
- 【适用条件】§30 种子敏感性判读的机制讨论;N1 训练配置辩护段。
- 【验证状态】题录当场核验(ICLR 2017+arXiv:1609.04836+作者);
  社区已验证(引用量大;尖锐/平坦极小值判据后续有修正文献,如实
  注记非定论)。

### 36.3 对照槽:batch size 与学习率的等价性 [坐标]

- 【出处】Smith et al., "Don't Decay the Learning Rate, Increase the
  Batch Size", ICLR 2018,~1600 引
- 【内容】衰减学习率与增大 batch size 对 SGD 轨迹**经验等价**(两者
  都控制更新中的有效梯度噪声幅度);小 batch+大 LR 的噪声注入有
  隐式正则化收益;线性/平方根 batch-LR 标度规则。
- 【对我们的映射】本仓 lr=3e-3 与 batch=64 从未联合消融;该等价
  性提示:轮 143 的 BUDGET_DOMINANT(步数为因)与 batch/LR 配置
  可能非独立——未来任何算力派发协议(T2/T3)的 batch 选择应带
  GNS 读数,不拍 64。
- 【适用条件】T2/T3 派发协议的 batch/LR 字段;停车场重启时清单。
- 【验证状态】题录当场核验(ICLR 2018+作者);社区已验证(等价性
  在 transformer 时代有偏离报告,如实注记适用边界)。

### 36.4 [行动] GNS-PROBE:梯度噪声尺度闭式估计(入队)

- 【出处】§36.1 B_simple 简化式;载体=house M1 弹簧(E1 口径)。
- 【内容】M1 弹簧同池 hidden64,取 3 个训练进度 checkpoint(0/1000/
  4000 步短训),各采 N=32 个 batch-64 随机子批梯度,闭式估计
  B_simple 谱(均值±离散度)+跨进度趋势;判读=batch=64 相对
  B_noise 的位置(噪声主导区/线性加速区)+B_noise 随进度走向
  (对照 §36.1"随训练增长"预言)。
- 【判负(预注册,执行前钉死进 PRD §19)】=B_simple 估计跨
  checkpoint 全部数值失效(非有限/负)或跨 checkpoint 无可分辨
  结构(全同量级且离散度>均值)⇒ 记"本仓体制 GNS 不可分辨",
  batch=64 合理性改由 batch 阶梯短训对照承担(停车场登记)。
- 【族边界】优化噪声轴(GNS 族第 1 轮);载体与 grokking 族
  (轮 146)分属不同问题轴,fastslow 族段内预算不动。
- 【适用条件】T1 可行动:3 checkpoint×32 梯度采样+两段短训
  ≈2-3min,est 8min 富余;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 31

3 [坐标](1 ★)+ 1 [行动](GNS-PROBE 入队,engineering)。
第 36 族;**S1 重置([行动] 产出)**。蒸馏轮第 29 次达标(≥1 条入库
+新目标)。机制核对:gradient noise/critical batch/sharp minima/
McCandlish 全库 grep 零命中;与 §30(解的景观)分界=优化噪声本身
的可测统计。选族启发式 n=5(钩子=全仓 batch 从未消融+轮 126 种子
敏感性的噪声侧假说)。

## 37. 经验蒸馏 32(轮 153,2026-09-24,QUEUE-EMPTY 轮):曲率动力学/训练稳定性族(sharpness、edge of stability 与 warmup)

> 新 query 族(与前 36 族零重叠:§36 梯度噪声=**采样协方差**轴,
> 本族=损失景观**曲率**(Hessian 最大特征值/sharpness)及其训练中
> 演化——edge of stability、warmup 机制、lazy/rich 初始化体制)。
> 钩子:轮 149 GNS 判读副产品——B_simple 在 0→1k 步暴增 7×(11.9→
> 83.1)=训练早期优化体制剧变;其曲率侧解释(早期 sharpness 演化)
> 未检。标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① 初始化体制理论
> ② 机制直击(warmup/EOS)③ 对照槽(lazy vs rich)。题录当场核验
> (AMM-015,4 条 arXiv ID/venue/作者全部确认)。

### 37.1 初始化体制理论:μP 与跨宽度超参迁移 [坐标]

- 【出处】Yang, Hu et al., "Tensor Programs V: Tuning Large Neural
  Networks via Zero-Shot Hyperparameter Transfer", 2022,
  arXiv:2203.03466,~302 引(microsoft/mup 实现)
- 【内容】μP(maximal update parametrization)=逐层初始化方差与
  学习率标度规则,使激活与更新在宽度缩放下保持 O(1)——特征学习
  跨宽度持续;标准参数化大宽度退化为核行为(NTK)。
- 【对我们的映射】本仓全部探针 hidden∈[8,128]、默认初始化=标准
  参数化;M1-CAP-AXIS(PR#1)的容量轴读数隐含"宽度×初始化"耦合
  未分离——μP 是未来任何容量/宽度声明的方法论坐标(非当前行动,
  方法论登记)。
- 【适用条件】容量轴判读的限定词;宽度缩放声明的方法论引注。
- 【验证状态】题录当场核验(arXiv:2203.03466+作者+引用约数);
  社区已验证(官方实现+多框架复刻)。

### 37.2 机制面:edge of stability 与 warmup 的 sharpness 机制 ★ [坐标]

- 【出处】Cohen et al., "Gradient Descent on Neural Networks Typically
  Occurs at the Edge of Stability", ICLR 2021, arXiv:2103.00065,
  ~611 引;Kalra et al., "Why Warmup the Learning Rate? Underlying
  Mechanisms and Effects", NeurIPS 2023(~121 引)
- 【内容】**EOS**:全批 GD 训练中 sharpness(最大 Hessian 特征值)
  升至并悬停于 ~2/η——训练长期运行在经典凸优化稳定域之外,非单调
  训练损失振荡;**warmup 机制**:早期网络 sharpness 高,小学习率
  等待其自然下降,防止早期 loss spike——warmup 不是迷信是曲率
  动力学。
- 【对我们的映射】轮 149 GNS 钩子(0→1k 步体制剧变)的曲率侧
  检验入口:本仓 lr=3e-3 下若 λ_max·η≈2 ⇒ 本仓训练也运行在 EOS
  (GROK-CURVE 观察的 rollout 非单调反弹可能即 EOS 振荡,轮 146
  判读当时标为"1-seed 噪声面"——本探针提供第二解释通道);Adam
  的 EOS 修正面如实注记(判据由 GD 推导)。
- 【适用条件】SHARP-PROBE 判读设计(见 [行动]);N1 训练动力学
  段。
- 【验证状态】题录当场核验(ICLR 2021+arXiv:2103.00065+作者;
  NeurIPS 2023+作者+引用约数);社区已验证(复现+后续理论
  self-stabilization)。

### 37.3 对照槽:lazy(NTK)与 rich(特征学习)体制 [坐标]

- 【出处】Karkada, "The lazy (NTK) and rich (μP) regimes: A gentle
  tutorial", arXiv 2024(UC Berkeley)
- 【内容】"richness scale"统一插值:lazy/NTK=参数近初始化不动、
  特征固定、优化凸;rich=表示主动演化。初始化标度决定落入哪侧。
- 【对我们的映射】解释 §37.1 的方法论关切:本仓小宽度(hidden 8-128)
  离 lazy 极限远,大概率处于 rich 侧——特征学习在发生,§30 符号
  盆地/轮 126 种子敏感都是 rich 体制的表现;此坐标使 N1 的"我们
  学到的是特征而非核回归"立场有理论语言。
- 【适用条件】N1 立场段的理论语言;§30 机制讨论补充。
- 【验证状态】题录当场核验(arXiv+作者+年份+机构);教程性质
  (非原创研究,如实注记),社区已验证(教学广泛引用)。

### 37.4 [行动] SHARP-PROBE:sharpness 轨迹探针(入队)

- 【出处】§37.2 EOS/warmup 机制的直接检验;载体=house M1 弹簧
  (E1 口径,与 GNS-PROBE 同池同训练配置)。
- 【内容】checkpoint {0,200,500,1000,2000} 各估训练 loss 的
  sharpness λ_max(Hessian-vector product 幂迭代 20 步,双反向
  autograd);判读=λ_max·η(lr=3e-3)相对 EOS 阈值 2 的位置——
  SHARP_EOS(∈[1.5,3])/SHARP_BELOW(<1.5 传统稳定区)/
  SHARP_ABOVE(>3);趋势=λ_max 随训练走向(对照 EOS"升至并悬停"
  与 warmup"早期高后降"两预言)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一 checkpoint 幂迭代
  20 步后相邻迭代相对变化 >10%(不收敛)或 λ_max 非有限 ⇒ 本体制
  sharpness 不可分辨,如实登记;Adam 修正面(判据由 GD 推导)全程
  如实注记。
- **族边界**:曲率轴(sharpness 族第 1 轮)——与 GNS 族(采样噪声
  协方差,149/151 两轮用尽)分属不同统计量;与 §30(解的景观)
  分界=训练中曲率的演化轨迹。
- 【适用条件】T1 可行动:2000 步短训+5 checkpoint×20 幂迭代步
  ≈2-3min,est 8min 富余;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 32

3 [坐标](1 ★)+ 1 [行动](SHARP-PROBE 入队,engineering)。
第 37 族;**S1 重置([行动] 产出)**。蒸馏轮第 30 次达标(≥1 条入库
+新目标)。机制核对:muP/NTK/lazy training/initialization theory 全库
grep 零命中(命中均为本仓实验记录非文献族);与 §36 分界=采样噪声
vs 景观曲率,与 §30 分界=解的差异 vs 曲率演化。选族启发式 n=6
(钩子=轮 149 判读副产品体制剧变读数)。

## 38. 经验蒸馏 33(轮 158,2026-09-24,QUEUE-EMPTY 轮):数据重复/记忆族(epochs、value decay 与记忆-泛化权衡)

> 新 query 族(与前 37 族零重叠:§8.4 exposure bias=训练目标构造轴,
> §35 grokking=泛化涌现时间轴,§30=种子间解差异——本族=**同一数据
> 被重复消费的次数轴**(epochs/窗口重复率)与记忆-泛化权衡)。
> 钩子:semigroup 训练默认随机重采样窗口(256 轨×~128 起点,4000 步
> ×batch64≈8 epoch 等效重复率),"重复率→记忆 vs 泛化"从未检视。
> 标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① 奠基 scaling ② 机制
> 对照 ③ 记忆理论。题录当场核验(AMM-015,3 条 venue/作者/arXiv ID
> 确认)。

### 38.1 奠基 scaling:data-constrained 下的重复价值衰减 ★ [坐标]

- 【出处】Muennighoff et al., "Scaling Data-Constrained Language
  Models", NeurIPS 2023(~644 引;JMLR 2025 扩展版)
- 【内容】data-constrained 体制下重复数据有效但边际价值衰减
  (**value decay**):≤4 epochs 重复≈独特数据,~16 epochs 起收益
  递减明显,过多重复反而变差;扩展 Chinchilla scaling(R*D* 修正)。
- 【对我们的映射】本仓 semigroup 训练的等效重复率(短训 ~8 epoch
  量级)恰在"无害区"边缘——REP-PROBE 的对照设计直接检验该预言的
  本仓版本;R*D* 框架为未来算力派发协议的数据预算字段提供语言。
- 【适用条件】REP-PROBE 判读的参照系;派发协议数据预算字段。
- 【验证状态】题录当场核验(NeurIPS 2023+作者+引用约数);社区已
  验证(被大量后续引用)。

### 38.2 机制对照:token-crisis 下重复 vs 新鲜数据 [坐标]

- 【出处】Fu et al., "To Repeat or Not To Repeat: Insights from
  Scaling LLM under Token-Crisis", 2023, arXiv:2305.13230
- 【内容】数据稀缺(token-crisis)场景下重复 vs 新鲜采样:重复至
  ~4 epochs 几乎等效 fresh;超过后多样性损失主导,收益骤减;
  "Larger Datasets Can Be Repeated More"(ICLR)给出重复容忍度随
  数据集规模增长的比例律。
- 【对我们的映射】本仓池(256 轨)是小数据体制=重复容忍度应较高;
  REP-PROBE 的 A/B 对照(随机重复 vs 窗口去重)即该问题的本仓
  实例化。
- 【适用条件】REP-PROBE 判读的预期方向参照。
- 【验证状态】题录当场核验(arXiv:2305.13230+作者);社区已验证。

### 38.3 记忆理论:记忆与泛化的光滑权衡 [坐标]

- 【出处】Chatterjee, "Learning and Memorization", PMLR(ICML),
  ~92 引
- 【内容】半参数框架:记忆与泛化之间存在**光滑权衡**——适量记忆
  (长尾样本)可助泛化,过度重复以泛化换记忆;记忆是连续变量非
  二元开关。
- 【对我们的映射】REP-PROBE 若测得重复无害(A≈B),不等于"记忆
  不发生"——rollout 泛化指标对记忆不敏感的可能如实注记(观测
  口径限制);理论坐标使判读避免过度声明。
- 【适用条件】REP-PROBE 判读的诚实边界;N1 训练体制讨论。
- 【验证状态】题录当场核验(PMLR+作者+引用约数);社区已验证。

### 38.4 [行动] REP-PROBE:窗口重复率对照(入队)

- 【出处】§38.1/38.2 的本仓实例化;载体=house M1 弹簧 semigroup
  体制。
- 【内容】固定 4000 步预算两臂:A=默认随机窗口重复(train_semigroup
  原样);B=窗口去重(预生成互不重叠 (t_i,t_j) 对遍历一次,每窗口
  最多见 1 次);判读=A/B rollout MSE(k100,同 held-out):A≈B(差
  <5%)⇒ 重复无害区如实记录;A 差于 B ≥5% ⇒ 重复有害(重复率已越
  value-decay 区);A 好于 B ≥5% ⇒ 重复有益(等效更多更新步)。
- 【判负(预注册,执行前钉死进 PRD §19)】=两臂差 <5% ⇒ "本体制
  重复率不可分辨"(38.3 口径限制如实注记);估计污染(窗口总量
  不足 4000)⇒ 判负改登记。
- 【族边界】数据重复轴(REP 族第 1 轮);与 §8.4(训练目标构造)/
  §35(泛化涌现)/§30(种子差异)分立。
- 【适用条件】T1 可行动:2 臂×4000 步 semigroup≈10min+评估,est
  20min;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 33

3 [坐标](1 ★)+ 1 [行动](REP-PROBE 入队,engineering)。
第 38 族;**S1 重置([行动] 产出)**。蒸馏轮第 31 次达标(≥1 条入库
+新目标)。机制核对:repetition/data-constrained/memoriz 全库 grep
零命中;与 §8.4/§35/§30 分界族头声明。选族启发式 n=7(钩子=semigroup
默认重采样体制的未检视面)。

## 39. 经验蒸馏 34(轮 161,2026-09-24,QUEUE-EMPTY 轮):谱偏置×离散化交叉族(频率选择性与训练网格的交互)

> 新 query 族(与前 38 族零重叠:§17 谱偏置=频率学习顺序轴(其核心
> 引用 Rahaman 已在库,本轮不重复收),§31 离散化=dt 迁移轴——本族
> =两者的**交叉**:频率选择性与训练网格 dt 的交互(Nyquist 域、
> aliasing、可计算定义的网格要求)。钩子:§17.3 可证伪预言(R1d
> 判负)与 §31 FLOW_LIKE 判读各自成立,但"低频先学是否依赖训练
> 网格解析度"从未设问——ω×dt 双因子从未交叉实验)。标记:
> [坐标] ×3 + [行动] ×1。三槽:① 泛化中的函数频率 ② 谱偏置的
> 可计算定义(网格耦合)③ 神经算子 aliasing。题录当场核验(AMM-015,
> 3 条全库 grep 零命中;Rahaman 撞 §17.1 已注记不收)。

### 39.1 泛化中的函数频率 [坐标]

- 【出处】Fridovich-Keil et al., "Spectral Bias in Practice: the Role
  of Function Frequency in Generalization", NeurIPS 2022,~70 引
- 【内容】谱偏置的实践面:目标函数频率如何影响泛化——网络先学
  低频(平滑)函数,频率内容随训练渐增;频率是泛化的操作变量
  (不仅是训练动力学现象)。
- 【对我们的映射】为 ω×dt 交叉实验提供"频率=自变量"的设计语言:
  弹簧族 ω 即可控频率,SPECTRAL-DT 探针把 ω 与 dt 同时因子化。
- 【适用条件】SPECTRAL-DT 判读设计;N1 谱偏置段落的泛化面补充。
- 【验证状态】题录当场核验(NeurIPS 2022+作者+引用约数);社区已
  验证。

### 39.2 谱偏置的可计算定义:网格分辨率耦合 [坐标]

- 【出处】Kiessling et al., "A Computable Definition of the Spectral
  Bias", AAAI 2022,~18 引
- 【内容】谱偏置的数值估计要求等距网格"足够细以解析目标函数的快
  振荡"——谱偏置的度量本身与训练网格分辨率耦合;网格不解析高频
  时谱偏置读数定义不良。
- 【对我们的映射】直接给出交叉实验的判读陷阱:粗 dt 下高频(ω·dt
  超 Nyquist)的误差上升可能 aliasing 而非学习顺序——判读需分离
  "学不到"与"测不到"(本仓 ω×dt 矩阵的 ω·dt 值域须注记 Nyquist
  状态)。
- 【适用条件】SPECTRAL-DT 判读的陷阱清单;评测口径纪律(scan §17.2
  Nyquist 一致性注记的深化)。
- 【验证状态】题录当场核验(AAAI 2022+作者+引用约数);社区已验证。

### 39.3 对照槽:神经算子的 aliasing 与离散化失配 [坐标]

- 【出处】Bartolucci et al., "Are Neural Operators Really Neural
  Operators? Frame Theory and Aliasing", 2023,~31 引;Gao et al.,
  "Discretization-invariance? On the generalization of neural
  operators"(OpenReview,~40 引)
- 【内容】神经算子的 aliasing 误差(frame 理论);离散化失配对泛化
  的实证——"discretization-invariance"是渐近性质非自动成立。
- 【对我们的映射】与本仓 §31 FLOW_LIKE(学到向量场则跨 dt 一致)
  衔接:向量场学习路线的跨 dt 一致性是 aliasing 免疫的一种形态;
  ω×dt 矩阵若显示高频×粗 dt 恶化超比例,即是该免疫的边界证据。
- 【适用条件】SPECTRAL-DT 判读的解释框架;§31 的边界细化。
- 【验证状态】题录当场核验(arXiv/OpenReview+作者+引用约数);社区
  已验证。

### 39.4 [行动] SPECTRAL-DT:ω×dt 双因子矩阵探针(入队)

- 【出处】§39.1-39.3 的合成行动面;载体=house M1 弹簧单频池
  (gen_spring ω_lo=ω_hi 可控频率,与轮 120 单频控制臂先例同法)。
- 【内容】ω∈{1.0,2.0,4.0}×dt∈{0.05,0.1,0.2} 9 单元短训(prefix
  hidden64 2000 步),各 k=200/100/50(固定物理视距 T=10 归一口径)
  rollout MSE;判读=交叉交互:高频(ω=4)的相对误差比在粗 dt vs
  细 dt 的增幅是否超过低频(ω=1)同比值(≥20% 差 ⇒ 交互可分辨);
  ω·dt 值域(0.05-0.8)的 Nyquist 状态逐单元注记(§39.2 陷阱)。
- 【判负(预注册,执行前钉死进 PRD §19)】=交互不可分辨(高频增幅
  与低频增幅差 <20%)⇒ 本体制频率-网格交互不可分辨,如实登记
  (§39.1 频率面可能仍在,判读只针对交互项);矩阵单元数值失效
  (非有限/发散)⇒ 判负改登记。
- 【族边界】频率×网格交叉轴(SPECTRAL-DT 族第 1 轮);Rahaman/§17
  已在库不重复;与 §31 分立(交叉非迁移)。
- 【适用条件】T1 可行动:9×2000 步 prefix≈4.5min+9 评估,est
  12min;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 34

3 [坐标]+ 1 [行动](SPECTRAL-DT 入队,engineering)。
第 39 族;**S1 重置([行动] 产出)**。蒸馏轮第 32 次达标(≥1 条入库
+新目标)。机制核对:muP/NTK 之外本轮 Fridovich-Keil/Kiessling/
Bartolucci 全库 grep 零命中;Rahaman 撞 §17.1 已注记不重复收。
选族启发式 n=8(钩子=§17×§31 两大已判读面的交叉缺口)。

## 40. 经验蒸馏 35(轮 164,2026-09-24,QUEUE-EMPTY 轮):课程/多分辨率训练族(dt 分辨率课程与难易排序)

> 新 query 族(与前 39 族零重叠:§8.4 采样课程=曝光偏差处方,D1f
> (轮 13)=训练循环课程(半群→prefix)——本族=**数据/分辨率难易
> 排序**轴(curriculum/anti-curriculum/多分辨率两阶段);与 §39 的
> 分界=§39 是 ω×dt 静态交互矩阵,本族是**训练进程中的排序调度**)。
> 钩子:轮 162 反向纹理双实证(ω=1 粗 dt 反而最好=粗分辨率对低频
> 结构有利;训练 dt 是条件性变量)——"先粗后细"的 dt 课程假说有
> 文献面(Wu 2021:课程恰在受限预算下有益)。标记:[坐标] ×3
> (1 ★)+ [行动] ×1。三槽:① 综述 ② 机制直击(课程何时有效)
> ③ 多分辨率两阶段实例。题录当场核验(AMM-015,3 条 venue/作者/
> arXiv ID 确认)。

### 40.1 综述:课程学习的动机、理论与应用 [坐标]

- 【出处】Wang et al., "A Survey on Curriculum Learning", IEEE TPAMI
  2022,~1495 引;奠基:Bengio et al., "Curriculum Learning", ICML
  2009
- 【内容】课程学习=从易到难的数据排序训练;动机(人类学习类比)、
  理论(损失景观的平滑化)、应用与度量(打分器+排序器两组件)。
- 【对我们的映射】dt 即"难度"的操作化:粗 dt=每步物理时长大、
  单步预测易(轮 162 反向纹理),细 dt=精但难——dt 课程是难度
  排序在物理仿真训练的自然实例。
- 【适用条件】DT-CURRICULUM 设计语言;N1 训练策略讨论。
- 【验证状态】题录当场核验(TPAMI 2022+作者+引用约数);社区已
  验证。

### 40.2 机制面:课程何时有效——受限预算与噪声数据的边界 ★ [坐标]

- 【出处】Wu, Dyer & Neyshabur, "When Do Curricula Work?",
  ICLR 2021, arXiv:2012.03107,~200 引
- 【内容】大规模受控对照:课程(易→难)仅在**受限训练预算**或
  噪声/长尾数据体制下有益;标准全预算下与随机排序无差;anti-
  curriculum(难→易)反而改善泛化与校准;"课程→anti-课程"两段
  调度对 OOD 鲁棒性最佳。
- 【对我们的映射】本仓 T1 探针=2000 步受限预算,恰在文献预言的
  课程有益域——DT-CURRICULUM 的假说检验有明确先验;同时该文警告
  随机排序是强基线,判读三分支(含不可分辨)预先注册防过度声明。
- 【适用条件】DT-CURRICULUM 判读的预期方向与诚实边界。
- 【验证状态】题录当场核验(arXiv:2012.03107+ICLR+作者);社区已
  验证。

### 40.3 对照槽:多分辨率数据两阶段加速 [坐标]

- 【出处】Wang et al., "Using Multi-Resolution Data to Accelerate
  Neural Network Training", Lawrence Berkeley National Laboratory,
  2022(~9 引)
- 【内容】输入/标签预降采样为粗数据集,第一阶段粗分辨率训练、
  第二阶段全分辨率精化——多分辨率两阶段加速的工程实例。
- 【对我们的映射】dt 课程的物理仿真版=先粗 dt(大步长覆盖长物理
  时间)后细 dt(精化);两阶段预算切分语言直接复用。
- 【适用条件】DT-CURRICULUM 的臂设计参照。
- 【验证状态】题录当场核验(机构+作者+年份+引用约数);社区已验证
  (引用较少,如实注记)。

### 40.4 [行动] DT-CURRICULUM:dt 分辨率课程对照(入队)

- 【出处】§40.1-40.3 的合成行动面;载体=house M1 弹簧单频池
  ω=2(轮 162 矩阵中频单元)。
- 【内容】2000 步预算两臂:A=恒定 dt=0.05;B=dt 课程(dt=0.1 训练
  1000 步→dt=0.05 训练 1000 步,权重连续传递);判读=A/B rollout
  MSE(k=200,T=10 同口径)三分支:差<5% ⇒ 课程不可分辨(与 Wu
  "随机序强基线"相容如实记录);B 好 ≥5% ⇒ 受限预算下课程有益
  (文献方向一致);B 差 ≥5% ⇒ 课程有害(如实登记)。
- 【判负(预注册,执行前钉死进 PRD §19)】=两臂差 <5% ⇒ "本体制
  dt 课程不可分辨"(受限预算假说在本仓不成立或预算域不同,如实
  注记);任一臂发散/非有限 ⇒ 判负改登记。
- 【族边界】分辨率排序轴(DT-CURRICULUM 族第 1 轮);与 §8.4(
  采样课程)/D1f(训练循环课程)/§39(静态交互矩阵)三分。
- 【适用条件】T1 可行动:2×2000 步 prefix≈1min+评估,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 35

3 [坐标](1 ★)+ 1 [行动](DT-CURRICULUM 入队,engineering)。
第 40 族;**S1 重置([行动] 产出)**。蒸馏轮第 33 次达标(≥1 条入库
+新目标)。机制核对:curriculum/multi-resolution/progressive 全库
grep 零命中(命中为 §8.4 采样课程语提及与 D1f 训练循环课程,族头
三分声明)。选族启发式 n=9(钩子=轮 162 反向纹理的调度化假说)。

## 41. 经验蒸馏 36(轮 169,2026-09-24,QUEUE-EMPTY 轮):长度外推族(训练窗之外的 rollout 泛化)

> 新 query 族(与前 40 族零重叠:§18.1 VPT=评估口径,§31 dt 迁移=
> 网格轴,§40 dt 课程=排序轴——本族=**物理时长轴**:训练轨迹物理
> 时长(16s)之外的 rollout 泛化,训练窗边界效应/长度外推)。
> 钩子:全仓 gen_steps=160 固定(物理时长 16s)——T>16s 的 rollout
> 从未被训练也从未被评估,训练窗边界之外的本仓行为完全未知。
> 标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① 训练积分误差机制
> ② 长视距误差累积 ③ TSFM=插值器理论面。题录当场核验(AMM-015,
> 3 条 venue/作者/arXiv ID 确认)。

### 41.1 机制面:训练时的数值积分误差(IMDE)★ [坐标]

- 【出处】Zhu, Jin & Tang, "On Numerical Integration in Neural Ordinary
  Equations Based on Inverse Modified Differential Equations", ICML
  2022(PMLR),~57 引
- 【内容】IMDE(逆修正微分方程)框架澄清数值积分误差如何进入
  Neural ODE 训练——学习到的动力学是"真动力+积分器修正项"的
  组合,训练窗内的修正在窗外不再适用。
- 【对我们的映射】本仓 VV 积分器+学习头:训练窗(16s)内学到的
  映射含 dt 特定修正(§31 FLOW_LIKE 已证向量场主导),窗外的
  外推行为=IMDE 语境的未测区;LEN-EXTRAP 的拐点检测直接对应
  "修正项失效边界"。
- 【适用条件】LEN-EXTRAP 判读设计;§31 边界的窗外延伸。
- 【验证状态】题录当场核验(ICML 2022+PMLR+作者);社区已验证。

### 41.2 长视距误差累积与统计量保持 [坐标]

- 【出处】Li et al., "A Weak Penalty Neural ODE for Learning Chaotic
  Dynamics from Noisy Time Series", arXiv:2511.06609(2025-11;
  WP-NODE)
- 【内容】neural ODE 长视距误差累积文献面:短窗训练的模型长
  rollout 时误差累积且丢失不变统计量(PDF 等);WP-NODE 用弱惩罚
  在训练中注入统计量保持。
- 【对我们的映射】本仓 rollout 评估(k100)全在训练窗内;窗外的
  误差累积速率未知——LEN-EXTRAP 的 per-step 误差剖面即该文献
  问题的本仓数据点;统计量保持(能量漂移)为附带诊断。
- 【适用条件】LEN-EXTRAP 判读参照;N1 长视距局限讨论。
- 【验证状态】题录当场核验(arXiv:2511.06609+年份+WP-NODE 术语);
  社区验证程度未知(新文,如实注记)。

### 41.3 对照槽:TSFM=插值器理论面 [坐标]

- 【出处】Karaouli et al., "How Foundational are Foundation Models
  for Time Series Forecasting?", arXiv 2025-10(Univ. Rennes/CNRS/
  Inria;NeurIPS TSFM workshop,~9 引)
- 【内容】时间序列基础模型的零样本能力与其预训练域强绑定——
  更像"已见分布上的插值器"而非真外推器。
- 【对我们的映射】与本仓 §19 TSFM 基线协议呼应的理论面:同网格
  内插(§17.2 纪律)之所以是纪律,因模型本质是插值器——LEN-EXTRAP
  把"插值域边界"从频率轴(§39)延伸到时长轴。基线协议不动
  (§19 在库不重复收)。
- 【适用条件】N1 评测纪律段的理论引注;§19 协议的边界讨论。
- 【验证状态】题录当场核验(arXiv 2025-10+作者+机构);社区验证
  早期(workshop,~9 引,如实注记)。

### 41.4 [行动] LEN-EXTRAP:训练窗外 rollout 外推探针(入队)

- 【出处】§41.1-41.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】prefix hidden64 2000 步训练(gen 160 步轨迹=16s 物理窗,
  全仓默认);评估新池 gen 601 步(60s)held-out 128 轨,双轴:
  内插段 per-step 误差(T∈[5,10]s,窗内)vs 外推段(T∈[20,30]s,
  窗外 4-14×)——comp=外推段/内插段 per-step MSE 比;三分支:
  comp<3 ⇒ LEN_ROBUST(平缓外推);≥3 且 16s 边界后首窗口跳变
  ≥3× ⇒ LEN_WINDOW_EDGE(窗口边界效应,§41.1 修正项失效);
  ≥3 但无边界跳变 ⇒ LEN_GRADUAL(渐进累积,§41.2)。附能量漂移
  诊断(统计量保持,§41.2)。
- 【判负(预注册,执行前钉死进 PRD §19)】=评估轨迹生成/滚动
  非有限或发散(>1e6)⇒ 判负登记(外推崩溃本身是信息,按
  WINDOW_EDGE 分支记录阈值情形);comp 计算数值异常 ⇒ 判负。
- 【族边界】物理时长轴(LEN-EXTRAP 族第 1 轮);与 §18.1(VPT
  口径)/§31(dt 网格)/§40(排序)分立。
- 【适用条件】T1 可行动:2000 步训练+601 步生成+3 视距评估 ≈
  2min,est 8min;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 36

3 [坐标](1 ★)+ 1 [行动](LEN-EXTRAP 入队,engineering)。
第 41 族;**S1 重置([行动] 产出)**。蒸馏轮第 34 次达标(≥1 条入库
+新目标)。机制核对:length extrapolation/length generalization/
long-horizon rollout 全库 grep 零命中;与 §18.1/§31/§40 分立。
选族启发式 n=10(钩子=gen_steps=160 全仓固定的未测窗外)。

## 42. 经验蒸馏 37(轮 174,2026-09-24,QUEUE-EMPTY 轮):任务多样性/池分布宽度族(ctx 推断的训练分布轴)

> 新 query 族(与前 41 族零重叠:§20.2 深度集成=**成员**多样性,
> §29 SBI=参数后验,§39=频率×网格——本族=**训练任务/参数分布的
> 宽度**轴:池分布宽度即 ctx 推断的任务多样性难度)。钩子:全仓
> 异频池 ω∈[0.7,1.8] 固定,分布宽度从未消融;轮 120 单频控制臂
> (E1 同法)与宽池数字并存但从未同口径对照。标记:[坐标] ×3
> (1 ★)+ [行动] ×1。三槽:① 多样性反直觉 ② OOD=插值批判
> ③ 宽窄权衡实例。题录当场核验(AMM-015,3 条 venue/作者确认)。

### 42.1 多样性反直觉:任务多样性不必然提升性能 [坐标]

- 【出处】Kumar et al., "The Effect of Diversity in Meta-Learning",
  AAAI 2023,~21 引
- 【内容】反直觉实证:增加元训练任务多样性**不必然**提升性能——
  任务分布的角色比传统认知更微妙;多样性收益依赖算法与评估分布
  的匹配。
- 【对我们的映射】POOL-WIDTH 的预期方向不应默认"宽=好":宽池
  (E1 默认)对窄池可能持平甚至更差(Kumar 方向)——三分支判读
  预先注册防确认偏误。
- 【适用条件】POOL-WIDTH 判读的预期方向校准。
- 【验证状态】题录当场核验(AAAI 2023+作者+引用约数);社区已
  验证。

### 42.2 OOD=插值批判:分布覆盖与真实外推 ★ [坐标]

- 【出处】Li et al., "Probing out-of-distribution generalization in
  machine learning", Nature 2025,~116 引
- 【内容】多数所谓 OOD 测试实为**插值**(测试点仍在训练分布凸包
  内),导致泛化能力被高估;真外推(分布之外)的可靠判别需要
  分布覆盖的显式刻画。
- 【对我们的映射】本仓异频池评估=同分布插值(§17.2 同网格纪律),
  OMEGA-EXTRAP(PR#2)才是真外推——POOL-WIDTH 补充"分布宽度"
  这一覆盖维度,使插值域的宽度本身成为被测量。
- 【适用条件】评测纪律的理论引注;OMEGA-EXTRAP 判读的边界语境。
- 【验证状态】题录当场核验(Nature 2025+作者+引用约数);社区已
  验证。

### 42.3 宽窄权衡实例:分布过宽损害精度 [坐标]

- 【出处】Zhang et al., "Crafting Training Degradation Distribution
  for the Accuracy-Robustness Tradeoff", ICML 2023,~33 引
- 【内容】训练分布过宽导致精度显著退化(精度-鲁棒性权衡的分布
  面);宽窄选择的权衡结构被显式刻画。
- 【对我们的映射】宽池(多任务)的代价面:ctx 推断在宽分布上
  需要分辨更多类系统=单系统精度可能下降;与 §42.1 合成"多样性
  代价-收益"两维预期。
- 【适用条件】POOL-WIDTH 判读的解释框架。
- 【验证状态】题录当场核验(ICML 2023+PMLR+作者);社区已验证。

### 42.4 [行动] POOL-WIDTH:池分布宽度对照(入队)

- 【出处】§42.1-42.3 的合成行动面;载体=house M1 弹簧(轮 120
  控制臂同法)。
- 【内容】2000 步 prefix hidden64 两臂:A=窄池 ω∈[0.95,1.05]
  (近单频);B=宽池 ω∈[0.7,1.8](E1 默认);各评估同分布
  held-out(k100,T=10);判读=B/A rollout MSE 比三分支:<1.05 ⇒
  宽度不可分辨(§42.1 反直觉方向);>1.05 ⇒ 宽度有代价(宽池
  同分布精度下降,§42.3 方向);<0.95 ⇒ 宽度有收益(多样性增益,
  传统方向)。ω·dt 网格解析两臂同(Nyquist 无关)。
- 【判负(预注册,执行前钉死进 PRD §19)】=两臂评估口径失效
  (非有限/发散)⇒ 判负登记;比值落在 [0.95,1.05] ⇒ 不可分辨
  如实登记(Kumar 相容)。
- 【族边界】训练分布宽度轴(POOL-WIDTH 族第 1 轮);与 §20.2(
  成员多样性)/§29(参数后验)/§39(网格交互)分立。
- 【适用条件】T1 可行动:2×2000 步 prefix≈1min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 37

3 [坐标](1 ★)+ 1 [行动](POOL-WIDTH 入队,engineering)。
第 42 族;**S1 重置([行动] 产出)**。蒸馏轮第 35 次达标(≥1 条入库
+新目标)。机制核对:task diversity/meta-learning 全库 grep 零命中
(命中=§20.2 成员多样性语境,族头声明分立)。选族启发式 n=11
(钩子=池分布宽度从未消融)。

## 43. 经验蒸馏 38(轮 177,2026-09-24,QUEUE-EMPTY 轮):优化器选择族(自适应 vs 动量 SGD 的泛化边界)

> 新 query 族(与前 42 族零重叠:§36 梯度噪声=采样协方差轴(引用过
> Adam 修正面措辞但非优化器对比族),§40 课程=排序轴——本族=
> **优化器本身的选择轴**(自适应逐坐标 vs 动量 SGD 的泛化差异)。
> 钩子:全仓 Adam(lr=3e-3)固定从未对照——优化器是另一未检视的
> 全局超参。标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① 经典批判
> ② 现代修正(transformer 侧 Adam 优势)③ 受控基准。题录当场核验
> (AMM-015,3 条 venue/作者/arXiv ID 确认)。

### 43.1 经典批判:自适应方法泛化更差 ★ [坐标]

- 【出处】Wilson et al., "The Marginal Value of Adaptive Gradient
  Methods in Machine Learning", NeurIPS 2017, arXiv:1705.08292,
  ~1714 引;后续修正:Loshchilov & Hutter AdamW 2019(Adam 泛化差
  距部分源于 weight-decay 实现缺陷)
- 【内容】自适应方法(Adam/AdaGrad/RMSProp)找到的解泛化更差
  (常显著)——即使训练 loss 更好;自适应=隐式偏向不同函数
  (simplicity bias 差异);建议不把自适应方法当默认。
- 【对我们的映射】本仓默认 Adam:若 OPT-COMPARE 显示 SGD-momentum
  泛化更好,训练配置辩护需加"Adam 便利性 vs SGD 泛化"的权衡
  注记;若 Adam 更好/不可分辨,则本体制在该批判范围之外(如实)。
- 【适用条件】OPT-COMPARE 判读的文献先验(方向:vision/MLP 侧
  SGD 占优)。
- 【验证状态】题录当场核验(arXiv:1705.08292+NeurIPS 2017+作者);
  社区已验证(AdamW 部分修正亦如实注记)。

### 43.2 现代修正:transformer 侧 Adam 优势非噪声归因 [坐标]

- 【出处】Kunstner et al., "Noise Is Not the Main Factor Behind the
  Gap Between SGD and Adam", 2023,~152 引
- 【内容】SGD 噪声正则假说被驳:Adam 随 batch 增大优势更明显
  (噪声应更小),gap 持续——SGD 在 transformer 损失几何
  (病态/重尾)上失效,Adam 的逐坐标自适应处理更好。
- 【对我们的映射】架构依赖性的两版文献:MLP/CNN 侧 SGD 常优
  (§43.1),attention/病态几何侧 Adam 常优(本条)——本仓 M1
  基座(LTC 核+MLP 头)落哪侧未测,OPT-COMPARE 即实测。
- 【适用条件】OPT-COMPARE 判读的架构依赖解释面。
- 【验证状态】题录当场核验(作者+年份+引用约数);社区已验证。

### 43.3 受控基准:优化器基准研究 [坐标]

- 【出处】Schmidt, Schneider & Hennig, "Descending through a Crowded
  Valley — Benchmarking Deep Learning Optimizers", ICML 2021
  (~1100 引)
- 【内容】15 优化器×问题的大规模受控基准:无单胜者;Adam 系对
  lr 选择鲁棒;调优预算是最重要变量。
- 【对我们的映射】本仓 lr 未逐优化器调优=受限对照,判负分支
  预注册 lr 失配情形(SGD 发散=lr 预算未调平,非优化器本质)。
- 【适用条件】OPT-COMPARE 的判负分支设计;N1 训练配置辩护。
- 【验证状态】题录当场核验(ICML 2021+作者+引用约数);社区已
  验证。

### 43.4 [行动] OPT-COMPARE:优化器对照探针(入队)

- 【出处】§43.1-43.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 两臂:A=Adam lr=3e-3(默认);
  B=SGD momentum=0.9 lr=0.1(常用值);判读=A/B rollout MSE
  (k100 同 held-out)三分支:差<5% ⇒ 优化器不可分辨(§43.3
  "无单胜者"相容);Adam 好 ≥5% ⇒ 自适应在本体制有增益(§43.2
  方向);SGD 好 ≥5% ⇒ 自适应泛化代价(§43.1 方向)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂 loss 非有限或
  rollout 发散(>1e6)⇒ **OPT_UNRESOLVABLE(lr 预算未调平)如实
  登记**——SGD lr=0.1 未逐点调优是受限对照的已知局限(§43.3);
  差<5% ⇒ 不可分辨如实登记。
- 【族边界】优化器选择轴(OPT 族第 1 轮);与 §36(梯度噪声)/
  §43 内部各条分立。
- 【适用条件】T1 可行动:2×2000 步 prefix≈1min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 38

3 [坐标](1 ★)+ 1 [行动](OPT-COMPARE 入队,engineering)。
第 43 族;**S1 重置([行动] 产出)**。蒸馏轮第 36 次达标(≥1 条入库
+新目标)。机制核对:optimizer/SGD/momentum/adaptive 全库 grep 零
命中(命中=§36 的 Adam 修正面措辞,族头声明分立)。选族启发式
n=12(钩子=Adam 全仓固定从未对照)。

## 44. 经验蒸馏 39(轮 180,2026-09-24,QUEUE-EMPTY 轮):正则化强度族(weight decay 与解耦正则)

> 新 query 族(与前 43 族零重叠:§35.2 weight decay=grokking 机制
> 语境,§43.1 AdamW=一句修正注记——本族=**正则化强度作为训练
> 配置轴**(wd 阶梯×泛化、解耦正则)。钩子:轮 178 判读注记"本仓
> Adam 无 weight-decay(默认 0)"——正则化强度从未消融,AdamW
> 修正直接相关)。标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① AdamW
> 奠基 ② 机制面(wd×lr×噪声)③ 对照(增强可替代显式正则)。
> 题录当场核验(AMM-015,3 条 venue/作者确认)。

### 44.1 AdamW 奠基:解耦 weight decay [坐标]

- 【出处】Loshchilov & Hutter, "Decoupled Weight Decay Regularization",
  ICLR 2019(arXiv 2017),~49000 引(官方实现 loshchil/AdamW-and-SGDW)
- 【内容】Adam 的 L2 正则实现次优——wd 应从梯度更新解耦、直接
  作用于权重并与 lr 调度联动(scale λ'=λ·lr);AdamW 修复后成为
  transformer 训练事实标准。
- 【对我们的映射】本仓 Adam(weight_decay=0 默认)在 AdamW 语义
  下=wd 强度 0 的特例;WD-LADDER 的阶梯即对该特例的消融;若
  wd>0 有益,AdamW 式解耦实现是派发协议字段。
- 【适用条件】WD-LADDER 判读参照;派发协议正则字段。
- 【验证状态】题录当场核验(ICLR 2019+作者+引用约数);社区已
  验证(事实标准)。

### 44.2 机制面:wd×lr×SGD 噪声的隐式正则 ★ [坐标]

- 【出处】"Why Do We Need Weight Decay in Modern Deep Learning?"
  (arXiv 2024-11);Bjorck et al., "Understanding Decoupled and
  Early Weight Decay"(Cornell 2021)
- 【内容】wd 的收益机制不止显式范数惩罚:wd+大 lr 组合维持非消失
  SGD 噪声→隐式正则;解耦 wd 与早/晚 wd 作用不同(lr 联动耦合)。
- 【对我们的映射】与 §36 梯度噪声、轮 178 优化器判读衔接:wd 是
  噪声-正则链的第三变量;若 wd 阶梯改变 rollout,§36/§43 的体制
  定性需加 wd 维度。
- 【适用条件】WD-LADDER 判读解释;训练配置辩护。
- 【验证状态】题录当场核验(arXiv 2024-11;Cornell 2021+作者);
  社区验证中(新文如实注记)。

### 44.3 对照槽:数据增强可替代显式正则 [坐标]

- 【出处】Hernández-García et al., "Do Deep Nets Really Need Weight
  Decay and Dropout?", OpenReview(~45 引)
- 【内容】数据增强 alone 可达到甚至超过 wd+dropout 的泛化;显式
  正则对超参调优敏感。
- 【对我们的映射】本仓正则=零(wd=0/dropout=0/增强=无)——三分支
  判读若显示 wd 无益,与"增强可替代"文献面一致;物理仿真域的
  天然增强(窗口采样,轮 159)=本仓已有的隐式增强,如实注记。
- 【适用条件】WD-LADDER 判读的诚实边界。
- 【验证状态】题录当场核验(OpenReview+作者+引用约数);社区验证
  早期(如实注记)。

### 44.4 [行动] WD-LADDER:weight decay 阶梯对照(入队)

- 【出处】§44.1-44.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 三臂:Adam weight_decay∈
  {0(默认),1e-4,1e-2},其余同;判读=三臂 rollout MSE(k100 同
  held-out)spread(max/min):<1.05 ⇒ WD_UNRESOLVABLE(强度不可
  分辨,§44.3"增强已够"相容);≥1.05 ⇒ 报告最优 wd 与方向
  (单调有益/有害/最优点在中间)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  WD_UNRESOLVABLE(该强度不可用如实登记);spread 计算数值异常
  ⇒ 判负。
- 【族边界】正则化强度轴(WD 族第 1 轮);与 §35.2(grokking 机制
  语境)/§43.1(AdamW 注记)分立。
- 【适用条件】T1 可行动:3×2000 步 prefix≈1.5min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 39

3 [坐标](1 ★)+ 1 [行动](WD-LADDER 入队,engineering)。
第 44 族;**S1 重置([行动] 产出)**。蒸馏轮第 37 次达标(≥1 条入库
+新目标)。机制核对:weight decay/regulariz 全库 grep 命中均为语境
提及(§35.2 grokking 机制/§43.1 AdamW 注记),正则化强度轴未收;
族头声明分界。选族启发式 n=13(钩子=轮 178 判读注记 wd=0)。

## 45. 经验蒸馏 40(轮 184,2026-09-24,QUEUE-EMPTY 轮):深度-容量轴族(depth 消融与哈密顿网络深度先例)

> 新 query 族(与前 44 族零重叠:§39.1 μP=宽度标度方法论,M1-CAP-
> AXIS=宽度轴实验——本族=**深度轴**(depth 消融、深度效率、哈密顿
> 网络深度先例)。钩子:全仓 depth=2 固定从未消融,深度-宽度权衡
> (§39.1 μP 的另一半)从未实验。标记:[坐标] ×3 + [行动] ×1。
> 三槽:① 深度效率理论 ② HNN 深度消融先例 ③ 哈密顿 DNN 稳定性。
> 题录当场核验(AMM-015,3 条 venue/作者/引用约数确认)。

### 45.1 深度效率理论:自然函数近似的深度-宽度权衡 [坐标]

- 【出处】Safran & Shamir, "Depth-Width Tradeoffs in Approximating
  Natural Functions", ICML(PMLR),~240 引
- 【内容】深度分离结果:某些简单自然函数深网络可高效近似,浅网络
  需指数级更宽——深度在组合函数表示上有本质效率优势。
- 【对我们的映射】M1 头(depth=2)是浅网络:若深度是本仓误差的
  限制变量,DEPTH-LADDER(depth 1/2/4)直接可测;与 §39.1 μP
  (宽度标度)构成两轴互补。
- 【适用条件】DEPTH-LADDER 判读参照;M1-CAP-AXIS 的深度面补充。
- 【验证状态】题录当场核验(ICML/PMLR+作者+引用约数);社区已
  验证。

### 45.2 HNN 深度消融先例 [坐标]

- 【出处】Mattheakis et al., "Hamiltonian neural networks for solving
  equations of motion", Phys. Rev. E 2022,~215 引
- 【内容】哈密顿神经网络(HNN)的深度/宽度消融:固定训练点数
  增加层数/神经元改善性能——HNN 族有直接的深度-精度消融先例。
- 【对我们的映射】本仓结构注入头(HamiltonianHead)的深度消融
  与该先例同型;判读可与该文献的"层数-精度"趋势对表。
- 【适用条件】DEPTH-LADDER 判读的文献对照。
- 【验证状态】题录当场核验(Phys. Rev. E 2022+作者+引用约数);
  社区已验证。

### 45.3 哈密顿 DNN 的深度稳定性 [坐标]

- 【出处】Galimberti et al., "A unified framework for Hamiltonian
  deep neural networks", PMLR 2021
- 【内容】哈密顿构造的深网络具边际稳定性(marginal stability),
  数百层不崩(对比常规深网络梯度坍缩),可用更少层数达相当性能。
- 【对我们的映射】理论边界:本仓头是"H 参数化的浅 MLP"非哈密顿
  深网络,但该文献提示"哈密顿结构×深度"的交互空间——DEPTH-
  LADDER 的结果可对照"深度收益是否被结构约束抵消"。
- 【适用条件】DEPTH-LADDER 判读的边界讨论;N1 结构注入哲学段。
- 【验证状态】题录当场核验(PMLR 2021+作者);社区验证早期(如实
  注记)。

### 45.4 [行动] DEPTH-LADDER:深度阶梯对照(入队)

- 【出处】§45.1-45.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 三臂:depth∈{1,2,4}(hidden 固
  定,参数量随深度近线性增);判读=三臂 rollout MSE(k100 同
  held-out)spread(max/min):<1.05 ⇒ DEPTH_UNRESOLVABLE(深度
  不可分辨,depth=2 默认充分);≥1.05 ⇒ 报告最优 depth 与方向
  (深度有益/有害/内点)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  DEPTH_UNRESOLVABLE(该深度不可用登记);spread 数值异常 ⇒ 判负。
- 【族边界】深度轴(DEPTH 族第 1 轮);与 §39.1(宽度标度方法论)/
  §42(池宽度)分立。
- 【适用条件】T1 可行动:3×2000 步 prefix≈1.5min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 40

3 [坐标]+ 1 [行动](DEPTH-LADDER 入队,engineering)。
第 45 族;**S1 重置([行动] 产出)**。蒸馏轮第 38 次达标(≥1 条入库
+新目标)。机制核对:depth scaling/depth-width/哈密顿深度 全库 grep
零命中。选族启发式 n=14(钩子=depth=2 全仓固定从未消融)。

## 46. 经验蒸馏 41(轮 190,2026-09-24,QUEUE-EMPTY 轮):训练展开跨度族(k_train 与 rollout 训练)

> 新 query 族(与前 45 族零重叠:§8.4 exposure bias 三代处方(
> scheduled sampling/对抗对齐/模仿损失)已收——本族=**固定多步
> 展开训练的跨度轴**(k_train 本身的消融)与 rollout 训练稳定性
> 文献(pushforward trick/稳定正则),与 §8.4 的分界=本仓训练
> 循环已固定多步展开,未收的是"跨度多长"这一轴。钩子:k_train=8
> 全仓固定从未消融。标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:
> ① 张力诊断 ② pushforward 原文 ③ 稳定正则。题录当场核验
> (AMM-015;Bengio 2015 scheduled sampling 撞 §8.4 不重复收)。

### 46.1 张力诊断:one-step loss 与长视距部署的失配 [坐标]

- 【出处】Q Li, "Stability-Regularized Residual Neural ODEs: From
  Rollout-Error Contraction Diagnostics to a Train-Time Regularizer",
  MDPI 2026
- 【内容】残差 NODE 用 one-step 预测 loss 训练但以自回归长视距
  部署=训练-部署失配,可小一步误差长视距发散;提出 rollout 误差
  收缩诊断+训练时稳定正则。
- 【对我们的映射】k_train 跨度即"训练-部署失配"的旋钮:k_train
  越大训练越接近部署(长视距),单步成本越高——KSPAN-LADDER 检验
  该旋钮在本仓的敏感度。
- 【适用条件】KSPAN-LADDER 判读参照;训练配置辩护。
- 【验证状态】题录当场核验(MDPI 2026+作者);验证早期(新文,
  如实注记)。

### 46.2 pushforward 原文:自反馈训练的连续系统类比 ★ [坐标]

- 【出处】Brandstetter et al., "Message Passing Neural PDE Solvers",
  ICLR 2023(pushforward trick 原文;后续 DySLIM ICML 2024 给出
  不变测度 loss 与 pushforward 的形式分析)
- 【内容】训练时把模型自身(可能带噪)的输出反馈为下一步输入
  (pushforward trick)——超越 teacher forcing 的确定性版本,
  已成神经 PDE 求解器标准配置;DySLIM 形式化其与不变测度 loss
  的关系。
- 【对我们的映射】本仓 k_train 展开训练的真值均为真值轨迹(
  teacher forcing 式多步),pushforward(自反馈)是未实装的
  处方——k_train 消融若显示跨度敏感,pushforward 是下一步
  处方方向(停车场候选)。
- 【适用条件】KSPAN-LADDER 判读的处方储备;§8.4 谱系的连续版
  补充。
- 【验证状态】题录当场核验(ICLR 2023+作者+venue);社区已验证
  (高引标准配置)。

### 46.3 稳定正则与多步 loss 谱系 [坐标]

- 【出处】多步 rollout loss 综述面(Emergent Mind 2026 条目;
  multiple shooting for Neural ODEs 谱系)
- 【内容】多步 rollout loss(对多步预测误差惩罚)作为训练目标
  的谱系:multiple shooting、自适应跨度、稳定性正则——k_train
  选择的文献选项集。
- 【对我们的映射】为 k_train 消融结果的解释提供选项空间:k_train
  增大若有益=更接近部署;无益=本仓 k=8 已在平台(与 §18.2 复合
  误差背书对表)。
- 【适用条件】KSPAN-LADDER 判读的选项框架。
- 【验证状态】题录可定位(MDPI/Emergent Mind 综述面,精确到
  谱系);验证状态如实注记(综述面非原创研究)。

### 46.4 [行动] KSPAN-LADDER:k_train 跨度阶梯对照(入队)

- 【出处】§46.1-46.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 三臂:k_train∈{4,8,16}(训练
  展开跨度);评估同口径 k100 held-out rollout MSE;判读=三臂
  spread(max/min):<1.05 ⇒ KSPAN_UNRESOLVABLE(跨度不可分辨,
  k=8 默认充分如实登记);≥1.05 ⇒ 报告最优 k_train 与方向。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  KSPAN_UNRESOLVABLE(该跨度不可用登记);spread 数值异常 ⇒ 判负。
- 【族边界】训练展开跨度轴(KSPAN 族第 1 轮);与 §8.4(采样课程
  处方——Bengio 2015 已在库不重复收)/§40(dt 排序)分立。
- 【适用条件】T1 可行动:3×2000 步 prefix≈1.5min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 41

3 [坐标](1 ★)+ 1 [行动](KSPAN-LADDER 入队,engineering)。
第 46 族;**S1 重置([行动] 产出)**。蒸馏轮第 39 次达标(≥1 条入库
+新目标)。机制核对:training span/rollout span/k_train grep 零命中
(Bengio 2015 scheduled sampling 撞 §8.4 已在库不重复收,族头声明)。
选族启发式 n=15(钩子=k_train=8 全仓固定从未消融)。

## 47. 经验蒸馏 42(轮 196,2026-09-24,QUEUE-EMPTY 轮):n_scales 多时间常数尺度族(LTC 核架构超参)

> 新 query 族(与前 46 族零重叠:§36 梯度噪声/§40 课程/§43 优化器=
> 训练面,§45 深度=头 MLP——本族=**LTC 核本身的 n_scales 架构超参**
> (多时间常数尺度数),与 SSM 替代线(停车场②)分立——n_scales 是
> 本仓 CfC 核内部参数非替代架构)。钩子:n_scales=4 全仓固定从未
> 消融。标记:[坐标] ×3(1 ★)+ [行动] ×1。三槽:① 奠基(层级
> timescale)② 多尺度可学习 ③ 固定 vs 可学习对照。题录当场核验
> (AMM-015;CfC=本仓基座出处架构文档已引,不重复收,族头注记)。

### 47.1 奠基:层级 RNN 的多时间尺度 [坐标]

- 【出处】Hihi & Bengio, "Hierarchical Recurrent Neural Networks for
  Long-Term Dependencies", NIPS 1995,~606 引;Chung et al.,
  "Hierarchical Multiscale Recurrent Neural Networks", arXiv/OpenReview
  2016-17,~750 引
- 【内容】长期依赖由长时间尺度变量表示——层级 RNN 各层不同
  timescale(高频细粒度在低层,低频长程在高层);Chung 等让尺度
  可学习,更少参数改善语言建模。
- 【对我们的映射】本仓 CfC 核 n_scales=4 即"多时间常数"架构参数:
  尺度数的消融=该奠基方向的直接实例;NSCALES-LADDER 检验尺度数
  对 rollout 的敏感度。
- 【适用条件】NSCALES-LADDER 判读参照;N1 架构段。
- 【验证状态】题录当场核验(NIPS 1995+作者+引用约数;arXiv/
  OpenReview+作者);社区已验证。

### 47.2 连续时间 RNN 的 timescale 参数化谱系 [坐标]

- 【出处】Hasani et al., Closed-form Continuous-time Neural Networks
  (CfC,~294 引)=**本仓基座出处(架构文档已引,非本族新增)**;
  Yu et al., Continuous Timescale LSTM(2017,~43 引);Heinrich
  et al.(2020)gated/adaptive timescales 对照
- 【内容】连续时间 RNN 的 timescale 参数化谱系:CTR-LSTM 每层多
  timescale 常数;CfC 每神经元学习自己的 τ(液态时间常数);
  gated/adaptive 参数化对照。
- 【对我们的映射】本仓 n_scales=4 的出处语义:4 个离散 timescale
  通道;消融回答"4 是否充分/是否过多"——与 §39 频率轴(ω 外部
  频率)分立:这里是内部记忆时间常数。
- 【适用条件】NSCALES-LADDER 判读解释;N1 架构辩护。
- 【验证状态】题录当场核验(PMC 2017+引用约数;CfC=基座出处);
  社区已验证。

### 47.3 固定 vs 可学习 timescale 的对照 [坐标]

- 【出处】Quax et al., "Adaptive time scales in recurrent neural
  networks", 2020,~35 引(PMC/NIH)
- 【内容】可学习内禀时间参数的 RNN 能否恢复环境过程的 timescale
  谱——固定 vs 自适应(可学习)对照:可学习 timescale 匹配输入
  时间结构,提升记忆保持。
- 【对我们的映射】n_scales 阶梯的判读框架:若尺度数敏感(可分辨)
  ⇒ n_scales 是应调优的架构超参;若不敏感 ⇒ 默认 4 充分(如实
  登记)。
- 【适用条件】NSCALES-LADDER 判读的诚实边界。
- 【验证状态】题录当场核验(PMC/NIH 2020+作者+引用约数);社区
  已验证。

### 47.4 [行动] NSCALES-LADDER:n_scales 尺度数阶梯对照(入队)

- 【出处】§47.1-47.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 四臂:n_scales∈{1,2,4,8}(构造
  参数天然可注入=轮 181 哨兵条款适用);判读=四臂 rollout MSE
  (k100 同 held-out)spread(max/min):<1.05 ⇒ NSCALES_
  UNRESOLVABLE(尺度数不可分辨,n_scales=4 默认充分如实登记);
  ≥1.05 ⇒ 报告最优 n_scales 与方向。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  NSCALES_UNRESOLVABLE(该尺度数不可用登记);spread 数值异常 ⇒
  判负。
- 【族边界】核架构超参轴(NSCALES 族第 1 轮);与 §45(头深度)/
  §39.1(宽度标度)分立;与 SSM 替代线(停车场②)分立。
- 【适用条件】T1 可行动:4×2000 步 prefix≈2min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 42

3 [坐标](1 ★)+ 1 [行动](NSCALES-LADDER 入队,engineering)。
第 47 族;**S1 重置([行动] 产出)**。蒸馏轮第 40 次达标(≥1 条入库
+新目标)。机制核对:n_scales/multi-timescale RNN 全库 grep 零命中
(命中=M2 OperatorPotentialHead 语境提及非族);CfC=基座出处已引
不重复收;与 SSM 替代线分立。选族启发式 n=16(钩子=n_scales=4
全仓固定从未消融)。

## 48. 经验蒸馏 43(轮 200,2026-09-24,QUEUE-EMPTY 轮):LR 调度族(decay 形状与恒定 lr 的过拟合)

> 新 query 族(与前 47 族零重叠:§43 优化器选择=优化器本身,§40
> 课程=数据排序,§36 梯度噪声=采样协方差——本族=**lr 调度形状**
> 轴(恒定 vs 衰减、线性/cosine/指数)。钩子:train.py docstring
> 明言"Constant lr overfits long schedules"且 lr_decay=1.0(恒定)
> 全仓固定从未消融——自带未检验声明。标记:[坐标] ×3(1 ★)+
> [行动] ×1。三槽:① 线性衰减最优实证 ② 理论(near-optimal
> schedules)③ 教科书共识面。题录当场核验(AMM-015,2 条精确
> 作者+arXiv ID 确认,教科书面如实注记)。

### 48.1 线性衰减最优实证(固定预算)★ [坐标]

- 【出处】Defazio, Cutkosky, Mehta, Mishchenko (Khaled), "Optimal
  Linear Decay Learning Rate Schedules and Further Refinements",
  arXiv:2310.07831(2023/2024)
- 【内容】固定训练预算下**线性衰减(到 0)schedule 最优**——10 个
  多样问题的最全面评估;附带 warmup+快衰减的精炼变体。
- 【对我们的映射】本仓 lr_decay=1.0(恒定)恰是该文献的"未衰减"
  基线——LRDECAY-LADDER 的阶梯(1.0/0.999/0.99 指数)直接检验
  恒定 vs 衰减在本仓的差距。
- 【适用条件】LRDECAY-LADDER 判读参照;训练配置辩护。
- 【验证状态】题录当场核验(arXiv:2310.07831+作者);社区已验证。

### 48.2 理论面:near-optimal schedules 的共同特征 [坐标]

- 【出处】Bordelon & Mori, "Theory of Optimal Learning Rate Schedules
  and Scaling Laws", arXiv:2602.04774(2026)
- 【内容】可解模型(power-law random features+SGD)理论:near-
  optimal schedules 共同特征=**warmup 后渐进衰减**;常用 schedule
  族(含 WSD)在该理论上非最优。
- 【对我们的映射】与 §37.2 warmup 机制(EOS/曲率)衔接:调度形状
  有理论最优结构;本仓恒定 lr 若劣于衰减,即该理论的本仓数据点。
- 【适用条件】LRDECAY-LADDER 判读的理论框架。
- 【验证状态】题录当场核验(arXiv:2602.04774+作者);社区验证
  早期(新文,如实注记)。

### 48.3 教科书共识面 [坐标]

- 【出处】Dive into Deep Learning §12.11(Learning Rate Scheduling)
- 【内容】教科书共识:衰减 lr 改善精度且"最令人困惑地"减少过拟合
  ——衰减同时作用于优化与泛化;cosine 为经验鲁棒默认。
- 【对我们的映射】轮 159 REP 判负(train_loss 差 2.5× 未传递泛化)
  的调度维度:train.py 注释的"恒定 lr 过拟合长日程"声明即待检验
  的本仓内部断言(架构文档内部断言进实验检验的实例)。
- 【适用条件】LRDECAY-LADDER 判读的对照面。
- 【验证状态】教科书面(可定位章节;非原创研究如实注记)。

### 48.4 [行动] LRDECAY-LADDER:lr 衰减阶梯对照(入队)

- 【出处】§48.1-48.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 三臂:lr_decay∈{1.0(恒定默认),
  0.999,0.99}(prefix 的 lr_decay 参数天然可注入=轮 181 哨兵条款
  适用);判读=三臂 rollout MSE(k100 同 held-out)spread(max/min):
  <1.05 ⇒ LRDECAY_UNRESOLVABLE(调度形状不可分辨,恒定默认充分
  如实登记);≥1.05 ⇒ 报告最优 decay 与方向。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  LRDECAY_UNRESOLVABLE(该衰减率不可用登记);spread 数值异常 ⇒
  判负。
- 【族边界】lr 调度形状轴(LRDECAY 族第 1 轮);与 §43(优化器
  选择)/§40(数据排序)/§36(采样噪声)分立。
- 【适用条件】T1 可行动:3×2000 步 prefix≈1.5min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 43

3 [坐标](1 ★)+ 1 [行动](LRDECAY-LADDER 入队,engineering)。
第 48 族;**S1 重置([行动] 产出)**。蒸馏轮第 41 次达标(≥1 条入库
+新目标)。机制核对:lr_decay/cosine schedule/lr schedule 全库 grep
零命中(train.py docstring 的内部断言非文献族)。选族启发式 n=17
(钩子=train.py 内部断言"恒定 lr 过拟合长日程"从未检验)。

## 49. 经验蒸馏 44(轮 204,2026-09-24,QUEUE-EMPTY 轮):batch×lr 等价规则的受控检验(§43.3 行动面)

> 本轮不收新族——给 §43.3(§43 已收坐标)补行动面:Smith 等价
> (batch↑≡lr↓)与线性/平方根缩放规则在本仓的受控检验。族=LRBATCH
> 交互检验(§43 行动面,非新族;蒸馏交付=行动面准入)。

### 49.1 [行动] LRBATCH-GRID:batch×lr 缩放规则检验(入队)

- 【出处】§43.3 Smith et al. ICLR 2018 等价性坐标的行动检验;载体=
  house M1 弹簧异频池(E1 口径)。
- 【内容】2000 步 prefix hidden64 四单元 (batch, lr) 网格:{(16,
  3e-3), (64, 3e-3), (16, 1.2e-2), (64, 1.2e-2)}——线性等价对=
  (16,3e-3) vs (64,1.2e-2)(lr∝batch),平方根等价对=(16,3e-3) vs
  (64,6e-3)(lr∝√batch);判读=等价对 rollout MSE(k100 同
  held-out)差:<5% ⇒ 该规则在本仓成立(等价性支持);≥5% ⇒ 该
  规则打破(如实报告哪条更准)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一单元发散/非有限 ⇒
  LRBATCH_UNRESOLVABLE(该 (batch,lr) 组合不可用登记);两等价对均
  <5% ⇒ 等价性成立且无法区分线性/平方根(如实登记)。
- 【族边界】batch×lr 交互轴(LRBATCH 检验,§43 行动面);与 §42
  池宽度/§45 深度分立。
- 【适用条件】T1 可行动:4×2000 步 prefix≈2min,est 10min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 44

1 [行动](LRBATCH-GRID 入队,engineering;§43 行动面补全)。
族扩展记录:第 43 族获行动面(非新族,蒸馏交付=行动准入)。
**S1 重置([行动] 产出)**。蒸馏轮第 42 次达标(行动准入)。
机制核对:batch×lr 交互在本仓未测(§43.3 坐标在库,行动面缺失)。
选族启发式 n=18(钩子=已收坐标的行动面缺口)。

## 50. 经验蒸馏 45(轮 208,2026-09-24,QUEUE-EMPTY 轮):权重平均族(SWA/model soups/EMA)

> 新 query 族(与前 49 族零重叠:§30 模式连接=**解的景观几何**,
> 本族=**权重平均作为训练后处理/训练中技术的实证与机制**(SWA/
> model soups/EMA)——§30 是几何描述,本族是可操作技术及其收益)。
> 钩子:train.py 无任何权重平均;轮 191 k_train 判读显示 rollout 对
> 训练轨迹敏感——尾段平均可能降低轨迹级方差。标记:[坐标] ×3
> (1 ★)+ [行动] ×1。三槽:① SWA 奠基 ② model soups ③ EMA 系统
> 研究。题录当场核验(AMM-015,3 条 arXiv ID/venue/作者确认)。

### 50.1 SWA 奠基:权重平均→更宽最优→更好泛化 ★ [坐标]

- 【出处】Izmailov et al., "Averaging Weights Leads to Wider Optima and
  Better Generalization", 2018, arXiv:1803.05407,~2683 引(PyTorch
  swa_utils 事实标准)
- 【内容】SGD 轨迹尾段的等权平均(SWA)落在更宽更平的最优域中心
  ——泛化更好;与 Fast Geometric Ensembling 相通。
- 【对我们的映射】本仓 rollout 对训练轨迹敏感(轮 191 KSPAN 判读
  k_train=4 最优=轨迹方差可见)——尾段权重平均可能以零推理成本
  降低方差;与本仓 §30 模式连接几何衔接(平均有效的前提=解在同一
  盆地)。
- 【适用条件】WSA-PROBE 判读参照;训练后处理。
- 【验证状态】题录当场核验(arXiv:1803.05407+作者+引用约数);
  社区已验证(PyTorch 标准)。

### 50.2 model soups:共享初始化的微调解在同一盆地 [坐标]

- 【出处】Wortsman et al., "Model soups: averaging weights of multiple
  fine-tuned models improves accuracy without increasing inference
  time", ICML 2022, arXiv:2203.05482,~2160 引
- 【内容】共享预训练初始化、不同超参微调的模型权重可直接平均
  (同盆地)且常提升精度;独立初始化的朴素平均失败。
- 【对我们的映射】§30 种子间解的盆地结构(轮 126 符号盆地)与
  soup 前提对表:同 seed 不同超参的解平均=安全;跨 seed 平均=需
  盆地一致性——为多 seed 终局协议(停车场)提供平均选项。
- 【适用条件】多 seed 终局的平均策略(停车场)。
- 【验证状态】题录当场核验(arXiv:2203.05482+ICML 2022+作者);
  社区已验证。

### 50.3 EMA 系统研究:平均=隐式正则 [坐标]

- 【出处】Morales-Brotons et al., "Exponential Moving Average of
  Weights in Deep Learning", 2024,~240 引
- 【内容】EMA 解与最后迭代解是**不同的解点**(EMA=隐式平均/正则化
  模型);EMA 天然降低梯度噪声,所需 lr 衰减更少;泛化与校准常
  优于最终权重。
- 【对我们的映射】与本仓 §43.1(自适应泛化代价)/§48(LR 调度)
  衔接:EMA 是"不调 lr 衰减而获得部分衰减收益"的正交选项;
  WSA-PROBE 的平均臂即其均匀版。
- 【适用条件】训练后处理选项;派发协议字段。
- 【验证状态】题录当场核验(arXiv 2024+作者+引用约数);社区已
  验证。

### 50.4 [行动] WSA-PROBE:尾段权重平均对照(入队)

- 【出处】§50.1-50.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 训练(注入式循环,轮 181 条款),
  尾段(最后 10 个检查点,每 100 步)均匀权重平均;对照两臂:
  A=最后 checkpoint;B=尾段 10 checkpoint 均匀平均(SWA 式);
  判读=A/B rollout MSE(k100 同 held-out)三分支:差<5% ⇒ 平均
  不可分辨(轨迹方差已低);B 好 ≥5% ⇒ SWA_BENEFICIAL(平均收益
  实证);B 差 ≥5% ⇒ SWA_HARMFUL 如实登记。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  WSA_UNRESOLVABLE 登记。
- 【族边界】权重平均轴(WSA 族第 1 轮);与 §30(景观几何描述)
  分立=可操作技术。
- 【适用条件】T1 可行动:2000 步训练+10 快照评估 ≈2min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 45

3 [坐标](1 ★)+ 1 [行动](WSA-PROBE 入队,engineering)。
第 50 族;**S1 重置([行动] 产出)**。蒸馏轮第 43 次达标(≥1 条入库
+新目标)。机制核对:SWA/model soup/EMA/权重平均 全库 grep 零命中
(命中=systematic review/CTI 弱匹配非族)。选族启发式 n=19(钩子=
权重平均从未试+§30 盆地几何的收益面)。

## 50.1x 补充(轮 213,2026-09-24):§37.2 warmup 坐标的行动面准入

> 本轮不收新族——给 §37.2(Kalra NeurIPS 2023 warmup 机制,已在库)
> 补行动面:lr warmup 对照(WARMUP-PROBE 入队)。族=§37 曲率动力学
> 族的 warmup 行动面(与 §45.4 DEPTH-LADDER 同族行动面模式)。

### 50.2b [行动] WARMUP-PROBE:lr warmup 对照(入队)

- 【出处】§37.2 Kalra 坐标(warmup=等待 sharpness 自然下降)的行动
  检验;载体=house M1 弹簧异频池(E1 口径,与轮 201 LRDECAY 同
  配置)。
- 【内容】2000 步 prefix hidden64 两臂:A=恒定 lr=3e-3(默认);
  B=warmup(前 200 步 lr 从 0 线性升至 3e-3,其后恒定);判读=A/B
  rollout MSE(k100 同 held-out)三分支:差<5% ⇒ warmup 不可分辨
  (与轮 194 SHARP_BELOW 一致:本仓不在 EOS,warmup 预言的收益域
  可能不触发——如实登记)/B 好 ≥5% ⇒ warmup 有益(§37.2 方向);
  B 差 ≥5% ⇒ warmup 有害如实登记。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  WARMUP_UNRESOLVABLE 登记;sharpness 前置读数(可选诊断)非承门。
- 【族边界】warmup 行动面(§37 行动化);与 §48 LRDECAY(衰减形状)
  分立=warmup(上升段)。
- 【适用条件】T1 可行动:2×2000 步 prefix≈1min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论补充(§37 行动面)

1 [行动](WARMUP-PROBE 入队,engineering;§37 行动面补全)。
蒸馏轮第 44 次达标(行动准入)。**S1 重置([行动] 产出)**。

## 50.2x 补充(轮 215,2026-09-24):§42.2 行动面——初始幅度外推对照(AMP-EXTRAP 入队)

> 本轮不收新族——给 §42.2(Li Nature 2025 插值/外推批判框架,已在
> 库)补行动面:分布覆盖维度从 ω 宽度(轮 175)延伸到**初始条件
> 幅度**。M1 弹簧 gen 初始条件 q0,p0~N(0,1)(解析闭式解),幅度
> 缩放=初条件能量缩放(能量∝scale²)——训练于 scale=1,评估于
> scale∈{1,2,4}=插值域内 vs 真外推的直接对照。

### 50.2x-1 [行动] AMP-EXTRAP:初始幅度外推对照(入队)

- 【出处】§42.2 Li 插值/外推框架的行动检验;载体=house M1 弹簧
  (解析闭式 gen,幅度参数化为本地实现+与原版 scale=1 逐位一致
  校验=轮 181 哨兵条款适用)。
- 【内容】训练于 scale=1 标准池(ω∈[0.7,1.8] E1 口径,prefix
  hidden64 ctx=8 2000 步);评估三池 scale∈{1(内插参照),2,4}(
  同 ω 分布同 seed,q0/p0 乘 scale)各 held-out 128 轨 k100 rollout
  MSE;**相对口径必需**(绝对 MSE 随能量平方增,scale=4 的真值
  能量 16×)——rel_mse=rollout MSE/mean(q_true²+p_true²) 逐池归
  一;判读=rel_comp=rel_mse(4)/rel_mse(1):<3 ⇒ AMPEX_ROBUST
  (相对误差平缓=幅度外推鲁棒)/≥3 ⇒ AMPEX_DEGRADES(外推退化,
  §42.2 插值域边界实证);发散/非有限 ⇒ AMPEX_UNRESOLVABLE 判负。
- 【族边界】初条件幅度轴(AMPLITUDE 族第 1 轮);与 §42(ω 宽度)
  分立=覆盖的另一维度。
- 【适用条件】T1 可行动:1×2000 步训练+3 池生成评估 ≈1.5min,
  est 8min;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论补充(§42 行动面)

1 [行动](AMP-EXTRAP 入队,engineering;§42.2 行动面补全)。
蒸馏轮第 45 次达标(行动准入)。**S1 重置([行动] 产出)**。

## 51. 经验蒸馏 47(轮 218,2026-09-24,QUEUE-EMPTY 轮):残差频谱诊断族(rollout 误差的频率结构)

> 新 query 族(与前 51 族零重叠:§17 谱偏置=学习顺序,§39=网格交互
> ——本族=**误差本身的频谱分解**(rollout 残差的 FFT 功率谱:误差
> 集中在基频?倍频?高频?),PIML 标准诊断手法的本仓缺位)。钩子:
> 全仓 rollout 误差只报标量 MSE,误差的频率成分从未分解——谱结构
> 直接指示误差来源(相位误差=基频附近展宽;幅值误差=基频增益偏
> 差;高频噪声=宽谱底)。标记:[坐标] ×3 + [行动] ×1。三槽:①
> 谱诊断方法论 ② 相位 vs 幅值误差分解 ③ 频域评估物理仿真。题录
> 当场核验(AMM-015,可定位综述/论文;弱题录如实带注记)。

### 51.1 谱诊断方法论:PIML 残差谱分析 [坐标]

- 【出处】物理启发残差谱诊断谱系(physics-informed ML 社区标准
  诊断;近期综述面如 "Spectral analysis of learned dynamics" 类
  条目——精确题录待 SCAN-AUDIT 复核,带 ? 登记)
- 【内容】对学习模型的预测残差做 FFT 功率谱:误差的频率定位
  (基频/倍频/宽谱)区分误差机制——相位漂移=谱峰展宽;幅值
  偏差=谱峰高度差;数值噪声=宽谱底。
- 【对我们的映射】本仓 MSE 标量掩盖了误差的谱结构;残差谱分析
  零训练成本(评估-only)且与 §17/§31/§39 三族串联。
- 【适用条件】RESIDUAL-SPEC 判读设计;N1 误差分析段。
- 【验证状态】谱系面(精确题录带 ? 登记 SCAN-AUDIT 复核);诊断
  手法社区通用。

### 51.2 相位 vs 幅值误差分解 [坐标]

- 【出处】谐振子误差分解经典面:相位误差在时域表现为随时间线性
  增长的偏差(固定幅值),幅值误差表现为包络偏差——sin/cos 分解
  可分离两者。
- 【对我们的映射】本仓弹簧 rollout 误差可在相位/幅值轴分解:
  轮 137 的"相位误差累积"表述(§33.2)可量化(相位差 vs 幅值比
  分解)——谱分解是其在频域的对偶。
- 【适用条件】误差机制归因的量化工具。
- 【验证状态】经典信号处理方法(教科书级,方法面无单篇题录,
  如实注记)。

### 51.3 频域评估物理仿真 [坐标]

- 【出处】谱域评估物理仿真的近期实践(FNO 系谱域评估;CNO;
  频域指标文献——精确题录待 SCAN-AUDIT 复核,带 ? 登记)
- 【内容】频域指标(谱差/带宽保持/高频能量比)作为时域 MSE 的
  补充,能区分"低频准高频差"与"整体平移"两类误差。
- 【对我们的映射】本仓评估(MSE 标量)之外的谱指标=评估口径
  扩展候选(§18.1 VPT 补充口径的同型扩展)。
- 【适用条件】评估口径扩展讨论(非当前行动)。
- 【验证状态】综述面(精确题录带 ? 登记 SCAN-AUDIT 复核)。

### 51.4 [行动] RESIDUAL-SPEC:rollout 残差频谱诊断(入队)

- 【出处】§51.1-51.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径,与轮 205 LRBATCH 同配置默认臂)。
- 【内容】默认配置训练(prefix hidden64 ctx=8 2000 步),对
  held-out 128 轨 k=200 rollout 残差(逐轨迹)做 FFT 功率谱平均;
  判读=残差功率谱的频率定位:①误差峰位相对真值基频(ω 附近)
  的位置(基频峰=相位/幅值误差;倍频峰=非线性误差;宽谱=噪声);
  ②高频能量占比(>2×ω 频段能量/总残差能量)。零训练(复用已有
  配置重训 1 次 2000 步+FFT 秒级)。
- 【判负(预注册,执行前钉死进 PRD §19)】=残差序列非有限或谱
  计算数值异常 ⇒ RESIDUAL_UNRESOLVABLE 判负;谱结构判读(峰位/
  占比)为读数报告非门轴(诊断轮,无通过/失败二分——报告即交付,
  谱读数入档)。
- 【族边界】误差频谱结构轴(RESIDUAL-SPEC 族第 1 轮);与 §17
  (学习顺序)/§31(网格)/§39(交互)串联但独立。
- 【适用条件】T1 可行动:1×2000 步训练+FFT 秒级,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 47

3 [坐标]+ 1 [行动](RESIDUAL-SPEC 入队,engineering;诊断轮——
谱读数报告即交付,无通过/失败门)。
第 51 族;**S1 重置([行动] 产出)**。蒸馏轮第 45 次达标(≥1 条入库
+新目标)。机制核对:FFT/残差谱/power spectrum 全库 grep 零命中。
选族启发式 n=20(钩子=误差只报标量 MSE 的谱结构盲区)。

## 52. 经验蒸馏 48(轮 222,2026-09-24,QUEUE-EMPTY 轮):观测窗长度族(训练时 t_obs 消融)

> 新 query 族(与前 51 族零重叠:D6=闭式 Fisher 识别窗口(需要多长
> 窗才能辨识 ω——信息论下界),本族=**训练时观测窗长度对端到端
> rollout 泛化的影响**(含网络对窗的容量利用与推理成本),与 D6
> 的分立=信息下界 vs 训练配置轴。钩子:t_obs=24 全仓固定从未消融。
> 标记:[坐标] ×2 + [行动] ×1。三槽:① 观测窗与可辨识性(D6 对表)
> ② 观测窗作为推理成本维度 ③ 前缀长度 vs 上下文学习。题录当场
> 核验(AMM-015,弱题录带 ? 登记 SCAN-AUDIT 复核)。

### 52.1 观测窗与可辨识性(D6 对表) [坐标]

- 【出处】轮 69 identifiability_probe(D6 窗口扫描,在库工具):
  弹簧 ω 的 Fisher 信息 J(ω) 随观测窗增长——识别窗口下界在库。
- 【对我们的映射】D6 给出"辨识需要多长窗",TOSA-LADDER 给出"训练
  用长窗是否值得"——两者对表:若训练最优 t_obs < D6 辨识下界,
  说明网络可从欠完备观测插补;若 ≥ 下界,与 Fisher 预期一致。
- 【适用条件】TOSA-LADDER 判读的 D6 对表。
- 【验证状态】在库工具与判读(D6 判读行);本族为行动面对接。

### 52.2 观测窗作为推理成本维度 [坐标]

- 【出处】序列模型推理成本与输入长度线性相关(prefix 推理需
  t_obs 步观测;精确题录带 ? 登记 SCAN-AUDIT 复核)
- 【内容】观测窗长度直接决定部署时的观测负担(传感器采样时长)
  与推理成本——t_obs 是精度-部署成本的权衡变量。
- 【对我们的映射】t_obs 消融的工程意义:若短窗(t_obs=12)精度
  持平,部署观测负担减半——派发协议字段(t_obs 候选)。
- 【适用条件】TOSA-LADDER 判读的工程解释;派发协议字段。
- 【验证状态】谱系面(弱题录带 ? 登记 SCAN-AUDIT 复核)。

### 52.3 前缀长度与上下文学习 [坐标]

- 【出处】上下文学习的前缀长度敏感文献(ICL 谱系,精确题录带 ?
  登记 SCAN-AUDIT 复核;与 §32 ICL 族相邻但分立——§32 是任务级
  ICL,本轴是物理观测窗长度)
- 【内容】前缀长度对上下文学习性能的影响非单调(过短信息不足,
  过长稀释注意力)。
- 【对我们的映射】t_obs 消融的非单调可能性预判:过短窗 ctx 推断
  不准,过长窗或稀释——判读报告曲线形状(单调/非单调/平台)。
- 【适用条件】TOSA-LADDER 判读的形状报告框架。
- 【验证状态】谱系面(弱题录带 ? 登记 SCAN-AUDIT 复核)。

### 52.4 [行动] TOSA-LADDER:t_obs 观测窗阶梯对照(入队)

- 【出处】§52.1-52.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 四臂:t_obs∈{8,16,24,48}(其余
  全同,评估同 held-out k100——t_obs 是观测窗,评估仍从 t_obs 起);
  判读=四臂 rollout MSE spread(max/min):<1.05 ⇒ TOSA_UNRESOLVABLE
  (观测窗长度不可分辨,t_obs=24 默认充分如实登记);≥1.05 ⇒ 报告
  最优 t_obs 与曲线形状(单调/非单调/平台)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  TOSA_UNRESOLVABLE(该窗长不可用登记);spread 数值异常 ⇒ 判负。
- 【族边界】训练观测窗轴(TOSA 族第 1 轮);与 D6(闭式 Fisher
  辨识下界)对表分立。
- 【适用条件】T1 可行动:4×2000 步 prefix(t_obs=48 窗更贵约 2×)
  ≈2min,est 10min;1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 48

3 [坐标](含 D6 对表)+ 1 [行动](TOSA-LADDER 入队,engineering)。
第 52 族;**S1 重置([行动] 产出)**。蒸馏轮第 46 次达标(≥1 条入库
+新目标)。机制核对:t_obs 阶梯/观测窗消融 全库 grep 零命中(D6=
闭式 Fisher 分立,族头声明)。选族启发式 n=21(钩子=t_obs=24 全仓
固定从未消融)。

## 53. 经验蒸馏 49(轮 225,2026-09-24,QUEUE-EMPTY 轮):ctx 隐变量容量族(context_dim 消融)

> 新 query 族(与前 52 族零重叠:§14 信息瓶颈未收族(在 PRD 但非
> scan 族),D2/E4a=梯度流实验(非容量宽窄),§29 SBI=参数后验——
> 本族=**ctx 隐变量维度容量轴**(context_dim 消融:过多维度是否
> 有害)。钩子:context_dim=8 全仓固定从未消融。标记:[坐标] ×3
> + [行动] ×1。三槽:① ICL 信息论容量 ② 元学习 ctx 谱系 ③ SBI
> 摘要空间 sufficiency。题录当场核验(AMM-015,Zhou 强题录;弱题
> 录带 ? 登记 SCAN-AUDIT 复核)。

### 53.1 ICL 的信息论容量 [坐标]

- 【出处】Zhou et al., "An Information-Theoretic Approach to
  In-Context Learning", arXiv:2410.05493(2024)
- 【内容】ICL 的信息论分析:有限样本精度作为上下文示例数的函数,
  信息瓶颈视角下上下文容量与噪声/干扰的权衡——容量并非越大越好。
- 【对我们的映射】ctx_dim=8 的消融直接检验"过多维度是否有害"
  (§43.1 泛化代价类比):容量不足=信息丢失(ω 辨识不充分),
  容量过剩=干扰/过参数化。
- 【适用条件】CTX-DIM-LADDER 判读参照。
- 【验证状态】题录当场核验(arXiv:2410.05493+作者);社区已验证。

### 53.2 元学习 ctx 谱系 [坐标]

- 【出处】CAVIA 语境(context adaptation 谱系;"Identifiable
  Latent Dynamics via Meta-Learning of Context" OpenReview,弱题录
  带 ? 登记 SCAN-AUDIT 复核)
- 【内容】元学习的 ctx 维度消融谱系:低维 ctx 强制任务结构进入
  少数自由度(正则化效应);过高维 ctx 容纳虚假自由度。
- 【对我们的映射】本仓 ctx 推断头(d_model→ctx_dim)的维度选择
  有元学习谱系支撑;ω 是 1 维真值隐变量,ctx_dim=8 已远超真值
  自由度——低维臂(ctx_dim 1/2)可能有正则化收益。
- 【适用条件】CTX-DIM-LADDER 判读的解释框架(ω=1 维真值)。
- 【验证状态】弱题录带 ? 登记 SCAN-AUDIT 复核;社区已验证(CAVIA
  谱系)。

### 53.3 SBI 摘要空间 sufficiency [坐标]

- 【出处】BayesFlow/sbi 谱系(embedding net 压缩观测为摘要空间,
  摘要维度决定 sufficiency——过小信息丢失后验有偏,足够大可学
  近似充分统计;sbi docs 谱系,弱题录带 ? 登记 SCAN-AUDIT 复核)
- 【内容】amortized SBI 的 embedding 网络摘要空间维度与后验
  sufficiency 的权衡。
- 【对我们的映射】ctx_dim 与 SBI 摘要空间同构(观测→隐变量摘要);
  本仓 ω=1 维真值 ⇒ 理论充分维度=1,ctx_dim=8 的冗余是否有害
  (过参数化)或无害(线性冗余)即实验问题。
- 【适用条件】CTX-DIM-LADDER 判读的 SBI 对照面。
- 【验证状态】弱题录带 ? 登记 SCAN-AUDIT 复核;谱系已验证。

### 53.4 [行动] CTX-DIM-LADDER:ctx 容量阶梯对照(入队)

- 【出处】§53.1-53.3 的合成行动面;载体=house M1 弹簧异频池
  (E1 口径)。
- 【内容】2000 步 prefix hidden64 四臂:context_dim∈{1,2,4,8}
  (构造参数天然可注入=轮 181 哨兵条款适用);判读=四臂 rollout
  MSE(k100 同 held-out)spread(max/min):<1.05 ⇒ CTXDIM_
  UNRESOLVABLE(容量不可分辨,ctx_dim=8 默认充分如实登记);≥1.05
  ⇒ 报告最优 ctx_dim 与方向(容量有益/有害/内点)。
- 【判负(预注册,执行前钉死进 PRD §19)】=任一臂发散/非有限 ⇒
  CTXDIM_UNRESOLVABLE(该容量不可用登记);spread 数值异常 ⇒ 判负。
- 【族边界】ctx 隐变量容量轴(CTX-DIM 族第 1 轮);与 D2/E4a
  (梯度流问题)分立=容量宽窄;与 SSM 替代线分立。
- 【适用条件】T1 可行动:4×2000 步 prefix≈2min,est 8min;
  1-seed 筛查口径。
- 【验证状态】入队执行;预注册判负标准先于执行钉死(下心跳)。

### 蒸馏结论 49

3 [坐标]+ 1 [行动](CTX-DIM-LADDER 入队,engineering)。
第 53 族;**S1 重置([行动] 产出)**。蒸馏轮第 47 次达标(≥1 条入库
+新目标)。机制核对:context_dim/信息瓶颈/latent capacity 全库
grep 零命中(D2/E4a=梯度流实验记录非族,族头声明分立)。选族启发
式 n=22(钩子=ctx_dim=8 全仓固定从未消融;ω=1 维真值的容量
冗余)。

## 54. 经验蒸馏 50(轮 248,2026-09-25,QUEUE-EMPTY 轮):能量头齐次性/标度等变参数化族

> 新 query 族(与前 53 族零重叠:机制核对 grep 等变/齐次仅命中
> LieGAN 发现谱系(§对称性发现=上游工具线,族头声明分立)与 §26.2
> 对称性改变缩放律形状(缩放律几何,非能量参数化)——本族=**能量头
> 的标度齐次结构注入**(T/V 的齐次参数化 vs 自由 MLP)。钩子:轮 244
> AMP-ATTR 实证动力学头标度齐次性破坏(头等变误差 s2 中位 1.362/s4
> 2.838)。标记:[坐标] ×3 + [行动] ×1。三槽:①物理不变性嵌入谱系
> ②等变哈密顿网络 ③硬结构 vs 软学习对照。题录当场核验(AMM-015:
> Gruver 标题漂移被核验抓出,正题=Deconstructing...;Frezat/Holl
> 全名单未核带 ? 登记 SCAN-AUDIT)。

### 54.1 物理不变性嵌入的湍流建模先例 [坐标]

- 【出处】Frezat et al., "Physical Invariance in Neural Networks for
  Subgrid-Scale Flux Modeling", Physical Review Fluids 6.024607
  (2021,~73 引;全作者名单未核带 ? 登记 SCAN-AUDIT)
- 【内容】把物理不变性(伽利略不变性等)架构性嵌入 NN 次网格通量
  模型,约束下的模型物理一致性提升。
- 【对我们的映射】不变性嵌入在流体建模的成熟先例;本族把它落到
  哈密顿头的标度齐次性(轮 244 实测缺口)。
- 【适用条件】EQUIV-HEAD 判读参照;N1 结构注入哲学的跨域盟友。
- 【验证状态】题录部分核验(首作者+期刊+DOI);社区已验证。

### 54.2 标度不变的物理反演 [坐标]

- 【出处】Holl et al., "Scale-invariant Learning by Physics
  Inversion", NeurIPS 2022(全作者名单未核带 ? 登记 SCAN-AUDIT)
- 【内容】以物理求解器求逆产生对参数化缩放不变的梯度更新
  (PhysGrad 谱系),优化侧实现标度不变。
- 【对我们的映射】优化侧标度不变与本族架构侧齐次注入互补——
  两条获得标度不变性的路径坐标。
- 【适用条件】future work 优化线;非当前行动。
- 【验证状态】题录部分核验(venue+首作者);社区已验证。

### 54.3 李群等变卷积与哈密顿系统 [坐标]

- 【出处】Finzi, Stanton, Izmailov & Wilson, "Generalizing
  Convolutional Neural Networks for Equivariance to Lie Groups on
  Arbitrary Continuous Data", ICML 2020, arXiv:2002.12880(LieConv,
  ~501 引);关联:同组 Gruver et al. ICLR 2022 见 54.4。
- 【内容】任意李群等变的连续数据卷积;应用于哈密顿系统时等变性
  带来线性/角动量的精确守恒。
- 【对我们的映射】等变性⇒精确守恒的定理级联系(动量守恒侧);
  本族的标度齐次性=同一哲学在能量函数齐次结构上的实例。
- 【适用条件】N1 Related Work 等变线引用;EQUIV-HEAD 定位。
- 【验证状态】题录当场核验(arXiv+四作者);社区已验证。

### 54.4 HNN 归纳偏置的解构 [坐标] ★强 + [行动]

- 【出处】★Gruver, Finzi, Stanton & Wilson, "Deconstructing the
  Inductive Biases of Hamiltonian Neural Networks", ICLR 2022
  (spotlight), arXiv:2202.01461(核验注记:检索初稿题名"Inductive
  Biases of..."漂移,当场核验抓出正题=Deconstructing...)
- 【内容】解构 HNN 的各类归纳偏置(能量守恒/辛结构/结构先验)对
  分布内拟合与外推行为的不同贡献——硬结构换外推的谱系坐标。
- 【对我们的映射】轮 244 实测"头标度齐次性破坏"(主因载体)的
  文献对表:硬注入齐次结构是否兑现外推收益=本族行动检验的问题。
- 【适用条件】EQUIV-HEAD 预注册的机制依据。
- 【验证状态】题录当场核验(四作者+venue+arXiv);社区已验证。

### 蒸馏结论

- 【行动】EQUIV-HEAD 入队(engineering,T1):齐次动能注入 A/B——
  A=house 默认(T,V 自由 MLP) vs B=T=½Σp² 解析+V_θ(q) MLP(动能
  解析注入,弹簧族物理已知);异频池 2000 步×3-seed;双读数=分布内
  rollout MSE(k100)+幅度外推 rel_comp(轮 216 口径,scale∈{2,4});
  判读:B 分布内持平(0.95≤ratio≤1.05)且外推修复(rel_comp_B<3)
  ⇒ EQUIV_RESOLVED(齐次注入=免费等变性,架构线候选 escape-door
  式 [B] 升级)/B 分布内劣化>5% ⇒ EQUIV_TRADEOFF(齐次注入有分布内
  代价,如实登记)/外推未修复 ⇒ EQUIV_ATTRIB(缺口不在 T,归因
  V/积分器重定向);判负=发散/非有限;决策耦合=三结果各改变架构线
  路由(候选升级/限制文档/归因重定向);族边界=第 54 族第 1 轮
  (与 R1b T 偶线/escape-door 线分立=T 偶是时间反演,本族是标度
  齐次);est 15min。
- 【坐标】54.1-54.3 解读用,不进队列。
- 【行动·第 2 轮】V-HOM 入队(轮 260,段内 2/2):V 侧齐次参数化
  检验(轮 249 判读行明示外推缺口归因 V+ctx;原轮 249 停车登记经
  人决区三问审计推翻=T1 可动/可逆/无宪法门槛⇒自主,修订如实注
  记)。设计=双臂同 AnalyticT(A=V 自由 MLP vs B=V=q²·s_θ(q|ctx)
  二次齐次)×3-seed,读数=分布内 MSE+rel_comp(轮 216 口径)。


## 55. 经验蒸馏 51(轮 251,2026-09-25,QUEUE-EMPTY 轮):配方视距稳健族(自生成行动面)

> 自生成方向(AMM-027 轮 133 先例,非文献族;与前 54 族零重叠:
> §41.2 长视距误差累积与 §46.1 one-step/长视距失配为文献坐标,
> 本族=**回灌配方的评估视距稳健性验证**——全部回灌证据产生于
> k=100 单一口径)。钩子=RECIPE-SYNTHESIS(轮 227/228)组合收益
> 10.7% 的 scope 声明问题:部署视距≠评测视距时收益是否保持。
> 出处=house 判读行(轮 228/229 RECIPE 判读+轮 241 eval 口径
> 固定性条款)。标记:[行动] ×1,无文献条目(自生成,出处为
> house 产物)。

### 蒸馏结论

- 【行动】RECIPE-HORIZON 入队(engineering,T1):回灌配方候选
  (B=depth4+lrdecay0.999+wd1e-4+warmup200+ktrain4,轮 229 组成)
  vs 默认(A)×3-seed,三视距评估 k∈{100,200,400}(gen_steps=450
  覆盖 t_obs+k+1);判读(3-seed 均值比 ratio(k)=mean_B/mean_A
  逐视距,预注册):全部视距 ratio<0.95 ⇒ HORIZON_ROBUST(回灌收
  益视距稳健,scope 确认)/k400 处 ratio≥0.95 ⇒ HORIZON_LIMITED
  (收益限中视距,回灌 PR scope 注记"k100-200")/B 随 k 恶化更快
  且 k400 ratio>1.05 ⇒ HORIZON_FRAGILE(配方视距脆弱如实登记);
  判负(下心跳预注册落盘后执行)=任一臂任一 seed 任一视距发散
  (非有限或 rollout>1e6);**决策耦合声明(AMM-028 门 1)**=三
  分支各改变回灌 PR 的 scope 声明(确认/限中视距注记/脆弱登记),
  用户合并决策的输入,EIG 合格;哨兵=A@k100 s0=3.5582;族边界=
  第 55 族第 1 轮(与 KSPAN 族分立=训练视距轴,本族=评估视距轴;
  §41.2/§46.1 文献坐标声明分立);est 18min(6×2000 步+3 视距评估)。

## 56. 经验蒸馏 52(轮 254,2026-09-25,QUEUE-EMPTY 轮):训练轨迹长度族(自生成)

> 自生成方向(AMM-027 轮 133 先例)。钩子=轮 252 根因修订的意外
> 实测:residual_spec2 的默认臂在 gen-301 训练池上 rollout 2.9031
> 显著优于 canonical 池的 3.5582(纯起点覆盖差异,同一配置同一
> seed)。机制核对:训练轨迹长度作为训练变量全库未收(D1 系=
> 定长轨迹内起点重分配,LEN-EXTRAP=评估外推,KSPAN=rollout 展开
> 跨度——族头声明分立);关联视距稳定文献扫描(SWAD 平坦极小/
> SPF/APEBench)无决策耦合 [行动](pushforward 已被轮 62 D5 判定
> 不适用;配方打磨违 AMM-028 精神),坐标留档不展开。

### 56.1 训练 t0 值域=轨迹长度的函数 [坐标](house 实测)

- 【出处】house 产物对照:residual_spec2(轮 246)默认臂
  2.9031(gen-301 训练池,t0∈[0,270))vs canonical 3.5582
  (gen-160,t0∈[0,129)),同配置同 seed;轮 252 实证数据值
  first-161 逐位相同(差异纯来自训练 t0 范围)。
- 【内容】训练轨迹长度增大 → t0 抽样值域增大 → 起点覆盖更广 →
  rollout 泛化提升(与 D1g 起点覆盖理论一致的方向)。
- 【对我们的映射】house 训练配置 gen_steps=160 的 t0 值域可能是
  免费的泛化余量;GENLEN 探针直接检验。
- 【适用条件】GENLEN-PROBE 判读参照。
- 【验证状态】house 实测(本轮重验钉死);单点信号如实注记
  (residual_spec2 为口径验证轮的附带读数)。

### 56.2 视距稳定文献坐标 [坐标](留档,无行动)

- 【出处】SWAD "Domain Generalization by Seeking Flat Minima"
  (NeurIPS 2021,~778 引,全名单带 ? 登记 SCAN-AUDIT);
  "Differentiability in Unrolled Training of Neural Physics
  Simulators"(arXiv 2024-10,作者未核带 ?);SPF Stochastic
  PushForward(Zhou et al.,arXiv:2508.18565,2025,首作者核验);
  APEBench(Koehler et al.,NeurIPS 2024 D&B,首作者核验)。
- 【内容】展开训练谱系:pushforward/课程式 rollout 长度调度/随机
  pushforward/系统基准;平坦极小与泛化。
- 【对我们的映射】house 训练已内建自反馈(轮 62 D5:pushforward
  不适用);展开训练课程=配方打磨方向(AMM-028 精神排除);坐标
  留档供 N1 相关工作。
- 【适用条件】N1 相关工作;无当前行动。
- 【验证状态】题录部分核验(带 ? 项登记 SCAN-AUDIT)。

### 蒸馏结论

- 【行动】GENLEN-PROBE 入队(engineering,T1):训练池
  gen_steps∈{160,300,450}×3-seed(canonical 训练切片同前;
  训练 t0 值域随长度增大),评估统一 canonical held-out k100;
  判读(3-seed 均值 spread=max/min,预注册):<1.05 ⇒
  GENLEN_UNRESOLVABLE(起点覆盖饱和如实登记,轮 252 意外读数
  归因为单点噪声)/≥1.05 ⇒ GENLEN_RESOLVED(报告最优训练长度
  与方向+D1g 对表,house 训练轨迹长度=配置决策变量);判负(下
  心跳预注册落盘后执行)=任一臂任一 seed 发散(非有限或
  rollout>1e6);**决策耦合声明(AMM-028 门 1)**=RESOLVED⇒house
  训练轨迹长度=免费配置改进(回灌配方第 7 轴候选,回灌 PR 注记
  升级)/UNRESOLVABLE⇒轮 252 意外读数归因单点噪声+覆盖饱和登记,
  两分支各改变配置决策,EIG 合格;哨兵=160 臂 s0=3.5582(canonical
  训练=历史默认路径);族边界=第 56 族第 1 轮(与 D1 系=定长内
  重分配分立);est 22min(9×2000 步+评估)。

## 57. 经验蒸馏 53(轮 263,2026-09-25,QUEUE-EMPTY 轮):齐次参数化优化稳定族([坐标] 轮)

> 钩子=轮 261 V-HOM 的训练不稳定性(齐次 V 参数化 seeds0/2 训练
> 灾难);族=归一化/齐次网络的优化动力学。机制核对:§36 优化器
> 噪声面/§30 盆地几何为相邻,族头声明分立。本轮=[坐标] 轮,S1
> 累计(无 [行动]:修复探针属第 54 族段内第 3 轮超上限,条件性
> 登记为下一段入口,轮 65 条款)。

### 57.1 幅度-方向解耦 [坐标] ★强

- 【出处】"Improving Neural Network Training by Decoupling the
  Magnitude and Direction", arXiv:2606.25971(作者未核带 ? 登记
  SCAN-AUDIT)
- 【内容】尺度不变损失下权重幅度与方向解耦训练:归一化参数化
  的退化方向是训练不稳定性来源,解耦后稳定。
- 【对我们的映射】V-HOM 的 ‖q‖²·s_θ(q̂) 结构中 s_θ 见方向归一
  输入=权重尺度退化同构;解耦法=V-HOM-STAB 候选的直接处方。
- 【适用条件】V-HOM-STAB(下一段条件入口)机制依据。
- 【验证状态】题录部分核验(arXiv id);社区已验证(方向待复核)。

### 57.2 归一化网络的学习动力学 [坐标]

- 【出处】"Learning Dynamics of Normalized Neural Networks"
  (OpenReview,作者/id 未核带 ? 登记 SCAN-AUDIT)
- 【内容】SGD+权重衰减下归一化网络的训练动力学系统分析,含
  方向归一引发的不稳定条件。
- 【对我们的映射】V-HOM 不稳定的形式化对表坐标。
- 【适用条件】同 57.1。
- 【验证状态】题录弱(带 ?);社区已验证。

### 57.3 高曲率训练发散判据 [坐标]

- 【出处】Zhai et al., ICML 2023(attention entropy collapse;
  venue+首作者核验)
- 【内容】训练发散发生于权重进入高曲率区域的损失几何判据。
- 【对我们的映射】V-HOM seeds0/2 灾难的诊断透镜(高曲率 vs
  方向退化)。
- 【适用条件】诊断工具;非当前行动。
- 【验证状态】题录当场核验(venue+首作者);社区已验证。

### 蒸馏结论

- 【坐标】×3 入库(§57.1-57.3)。
- 【条件性登记(轮 65 条款)】V-HOM-STAB=幅度-方向解耦稳定化的
  齐次 V 探针(第 54 族第 3 轮),触发=新马拉松段(族额度重置),
  入口内容=PRD §19 轮 261 判读行+本节坐标;已登记 GOALS 队列规
  则节。

## 58. 经验蒸馏 54(轮 264,2026-09-25,QUEUE-EMPTY 轮):种子方差感知配置采纳族([坐标] 轮,S1 累计 2/2)

> 钩子=本会话段 5 例高方差轴纹理(轮 239 ctx spread 2.72/轮 255
> genlen 2.34/轮 261 V-HOM 不稳定/WSA 轨迹方差/轮 126 seed 敏感
> 性)的元发现:seed 方差本身是配置采纳的一阶诊断。机制核对:
> 轮 126 种子敏感性已在库(house 实验记录非文献族,声明分立)。

### 58.1 算法配置的陷阱与最佳实践 [坐标] ★强

- 【出处】"Pitfalls and Best Practices in Algorithm Configuration"
  (arXiv 2019,作者未核带 ? 登记 SCAN-AUDIT)
- 【内容】固定单 seed 调参会过调到该 seed,选出的配置换 seed 常失效;
  处方=选择阶段多 seed 评估。
- 【对我们的映射】本会话段 5 例高方差轴(1-seed 强读数被 3-seed 溶
  解)的文献印证;AMM-028 门 3 的社区依据。
- 【适用条件】配置采纳协议参照。
- 【验证状态】题录部分核验(arXiv+年份);社区已验证。

### 58.2 实用 HPO 手册 [坐标]

- 【出处】Feurer et al., "A Practical HPO Cookbook"(作者部分核验
  首作者;venue 未核带 ?)
- 【内容】深度学习评估常用 ~3 seeds 统计上脆弱;建议 seed-aware
  incumbent 选择与 seed 预算化。
- 【对我们的映射】3-seed 门是下限而非充分条件(高方差轴需更多)。
- 【适用条件】判读行置信标注的依据。
- 【验证状态】题录部分核验(首作者);社区已验证。

### 58.3 rliable/IQM 报告标准 [坐标]

- 【出处】Agarwal et al., rliable 谱系(IQM=四分位间均值报告;
  作者/venue 未核带 ? 登记 SCAN-AUDIT)
- 【内容】跨 seed 报告的社区标准:IQM+分层 bootstrap 置信区间,
  替代裸均值。
- 【对我们的映射】house 现行协议(3-seed 均值+方向一致性+spread)
  与社区标准同向;IQM 升级=house 工具契约变更走 AMENDMENTS(非本
  轮行动)。
- 【适用条件】评估协议升级候选(提案制)。
- 【验证状态】题录弱(带 ?);社区标准广泛采用。

### 蒸馏结论

- 【坐标】×3 入库(§58.1-58.3)。
- 【判定】无 [行动]:house 现行协议(AMM-028 门 3)已被本轮文献
  印证为最佳实践同向;IQM 升级=触及 house 工具契约走 AMENDMENTS
  (候选登记,非本轮)。S1 累计 2/2 ⇒ 武装。

## 59. 经验蒸馏 55(轮 271,2026-09-26,QUEUE-EMPTY 蒸馏轮):约束结构表达力边界族([行动] 轮=HOM-BOUND 入队执行)

> 钩子=轮 268/269 齐次头连胜留下的未测边界:AMM-033 提案诚实
> 注记"窄构造(V=‖q‖²·s_θ(0,ctx))对非二次势真值系统性偏倚=
> 已知边界"——该边界是断言不是实测。族=结构约束(等变/齐次/
> 硬约束)架构的近似能力边界。机制核对:§45 深度容量轴
> (Safran & Shamir 深度近似理论)相邻分立(45=深度容量,
> 59=约束结构表达力边界);§54 齐次参数化族=优化稳定性面,
> 族头声明分立(54=训练稳定性,59=表达力/误设边界)。

### 59.1 等变架构的通用性边界 [坐标] ★强

- 【出处】Dym & Maron, "On the Universality of Rotation Equivariant
  Point Cloud Networks", ICLR 2021, arXiv:2010.02449(题录当场
  核验:arXiv id+venue+作者)
- 【内容】约束架构(旋转等变网络)近似能力的首次系统研究:给出
  等变架构通用的充分条件,并刻画表达力/等变性边界。
- 【对我们的映射】齐次 V 约束=约束架构;其"次数匹配才无偏"
  即表达力边界的可测实例;HOM-BOUND 三臂(自由/二次/四次)=
  该边界在玩具标度的直接测量。
- 【适用条件】AMM-033 范围注记的实证依据。
- 【验证状态】题录当场核验;社区已验证(~141 引)。

### 59.2 约束内恢复通用性的构造 [坐标]

- 【出处】Finkelshtein, Ben-Hamu, Maron, Dym, "A Simple and
  Universal Rotation Equivariant Point-cloud Network", ICML 2022
  (PMLR v196,题录当场核验)
- 【内容】在保持等变约束的同时证明性恢复通用性的极简构造。
- 【对我们的映射】"约束+表达力"可以兼得的先例=次数推广假说
  (‖q‖^{2k}·s 族)的文献同构;HOM-BOUND C 臂(deg=4)即
  次数匹配方向的最小实现。
- 【适用条件】同 59.1。
- 【验证状态】题录当场核验;社区已验证。

### 59.3 误设体系的非零损失读数 [坐标]

- 【出处】Chen, Matsubara & Yaguchi, "KAM Theory Meets Statistical
  Learning Theory: Hamiltonian Neural Networks with Non-Zero
  Training Loss", arXiv:2102.11923(2021,题录当场核验:arXiv id
  +标题+作者;venue 未核如实注记)
- 【内容】HNN 非零训练损失的 KAM 理论解读:模型类外真值的
  残差结构可读。
- 【对我们的映射】HOM-BOUND B 臂(次数误设)的 MSE 地板=
  误设偏倚的可读化;判读注记残差结构而非只看比值。
- 【适用条件】同 59.1。
- 【验证状态】题录当场核验(arXiv);venue 未核。

### 蒸馏结论

- 【坐标】×3 入库(§59.1-59.3)。
- 【判定】有 [行动]:HOM-BOUND 入队执行(新 quartic 池三臂
  三分支判读,决策耦合=AMM-033 范围注记三路修订);S1 重置
  ([行动] 产出=自生成后续迭代目标+当轮执行)。蒸馏第 55 次达标。

## Sources

> SCAN-AUDIT 注记(轮 94):本节多处仅域名根链——精确题录以各节内
> "SCAN-AUDIT 修订(轮 94)"注记与 docs/scan-traceability-audit.md
> 等级表为准(修后可复核率 94%,判负标准对账见审计报告 §9)。

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
- [D-HNN (Sosanya & Greydanus, arXiv:2201.10085)](https://arxiv.org/abs/2201.10085)——见 §15.1
- [D-HNN 官方实现 (GitHub)](https://github.com/greydanus/dissipative_hnns)——见 §15.1
- [Port-HNN (Desai et al., Phys. Rev. E 2021)](https://link.aps.org)——见 §15.2
- [Stable Port-Hamiltonian Neural Networks (Roth et al., NeurIPS 2025)](https://openreview.net/forum?id=epIGnGgcKD)——见 §15.2
- [Port-metriplectic NN (Hernández et al. 2023)](https://cnam.hal.science)——见 §15.2
- [Contact Hamiltonian Lagrangian NN (APS)](https://link.aps.org/doi/10.1103/9gnh-89jd)——见 §15.3
- [Deep-OSG (Chen et al., J. Comput. Phys. 2023)](https://www.sciencedirect.com)——见 §16.1
- [OSG-Net (SIAM)](https://epubs.siam.org)——见 §16.1
- [Modern Koopman Theory (Brunton et al., SIAM Review 2022)](https://epubs.siam.org)——见 §16.2
- [Koopman operator dynamical models (Bevanda et al. 2021)](https://www.sciencedirect.com)——见 §16.2
- [Hamiltonian Neural Koopman Operator (Zhang et al. 2024)](https://link.aps.org)——见 §16.3
- [Physics-informed deep Koopman for Lagrangian systems (Wang et al. 2024)](https://link.springer.com)——见 §16.3
- [On the Spectral Bias of Neural Networks (Rahaman et al., ICML 2019)](https://proceedings.mlr.press)——见 §17.1
- [On understanding and overcoming spectral biases (Xu et al. 2025)](https://www.sciencedirect.com)——见 §17.1
- [Spectral bias in physics-informed and operator learning (arXiv:2602.19265)](https://arxiv.org/html/2602.19265v1)——见 §17.2
- [Spectral Bias in Practice (NeurIPS 2022)](https://papers.neurips.cc/paper_files/paper/2022/file/306264db5698839230be3642aafc849c-Paper-Conference.pdf)——见 §17.2
- [High-Frequency Scaling (Khodakarami et al. 2025)](https://www.osti.gov)——见 §17.3
- [Data-driven forecasting of high-dimensional chaotic systems (Vlachas et al. 2018)](https://royalsocietypublishing.org)——见 §18.1
- [Long-term prediction of chaotic systems with ML (Fan et al. 2020)](https://link.aps.org)——见 §18.1
- [Compounding Prediction Errors in Learned Dynamics Models (Lambert et al. 2022)](https://arxiv.org/html/2203.09637v1)——见 §18.2
- [Any-step Dynamics Model (OpenReview 2024)](https://openreview.net/forum?id=JZCxlrwjZ8)——见 §18.2
- [Adaptable Hamiltonian NN (Han et al., PRR 2021)](https://link.aps.org)——见 §18.3
- [Foundation Models for Time Series: A Survey (arXiv 2025)](https://arxiv.org)——见 §19.1
- [Dynamics is what you need for time-series forecasting! (Brachet et al., OpenReview)](https://openreview.net)——见 §19.2
- [PINN variants in weather (ScienceDirect 2026)](https://www.sciencedirect.com)——见 §19.3
- [A Survey on UQ Methods for DNNs (He et al. 2023)](https://www.jiangteam.org)——见 §20.1
- [Deep Ensembles as Approximate Bayesian Inference (Wilson & Izmailov)](https://cims.nyu.edu/~andrewgw/deepensembles)——见 §20.2
- [BNN vs Deep Ensembles (arXiv:2509.19180)](https://arxiv.org/html/2509.19180v1)——见 §20.2
- [Repulsive Deep Ensembles are Bayesian (NeurIPS 2021)](https://proceedings.neurips.cc/paper/2021/file/1c63926ebcabda26b5cdb31b5cc91efb-Paper.pdf)——见 §20.2
- [AI Poincaré (Liu et al., PR 2021)](https://link.aps.org)——见 §21.1
- [L-conv (NeurIPS 2021)](https://proceedings.neurips.cc/paper/2021/hash/148148d62be67e0916a833931bd32b26-Abstract.html)——见 §21.2
- [hPINNs: Hard Constraints (SIAM)](https://epubs.siam.org/doi/10.1137/21M1397908)——见 §21.3
- [Solver-in-the-Loop (Um et al., NeurIPS 2020)](https://proceedings.neurips.cc)——见 §22.1
- [Physics-based Deep Learning (免费教材)](https://physicsbaseddeeplearning.org)——见 §22.1
- [Symplectic Adjoint Method (Matsubara et al.)](https://arxiv.org)——见 §22.2
