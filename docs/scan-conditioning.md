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
