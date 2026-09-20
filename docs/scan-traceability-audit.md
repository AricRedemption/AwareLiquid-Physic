# SCAN-AUDIT — 入库条目溯源审计报告(轮 94,2026-09-20;T0 零算力)

> 预注册:PRD §19 "轮 88 治理轮"(判负标准①②③先于执行钉死;AMM-015)。
> 审计对象:`docs/scan-conditioning.md` §1-22 全部入库条目 + 衍生文档缺证性
> 声明全库降档扫。方法:读文档 + 检索复核(本轮 14 次 web 检索,逐条定位
> 精确题录),零训练零实验。执行会话:马拉松轮 94。

## 1. 评级规则(先于评级钉死,对应 AMM-015 溯源硬标准)

- **A 题录可复核**:条目主锚含可唯一定位题录——arXiv ID / DOI /
  OpenReview forum ID / (作者 + 会议或期刊 + 年份) 任一形式,第三方可凭
  条目本身定位精确文献记录。
- **B 仅域名根**:主锚只有域名根/聚合站链接(ResearchGate/EmergentMind/
  alphaxiv 裸链等),或缺作者或缺年份——不能唯一定位。
- **C 缺出处**:条目无任何可定位信息。
- 单元:条目级(主锚判定),二级出处缺陷以注记登记不降主级;派生文档
  (N1 素材)的引用继承 scan 主表,不重复计单元。

## 2. 审计范围与条目计数

`scan-conditioning.md` §1-22 共 **54 条**入库条目,其中 **4 条内部
[行动]协议条目**(19.4/20.4/21.4/22.4,出处=本仓工具路径+PRD 预注册锚,
不经外部题录复核,**单独列于 §5,不计入复核率分母**),**外部文献条目
50 条**(§5 HyPINO/CPNO 按 2 条计;轮 88 估计"约 49"按 §5 合 1 计,两
口径差 1,本审计取 50 分母)。

## 3. 逐条溯源等级表(50 条外部条目)

标记:❶=事实错误当轮修订(判负③);升级=本轮检索复核后 B→A。

| § | 条目 | 主锚(入库时) | 修前 | 修订动作 | 修后 |
|---|---|---|---|---|---|
| 1 | UFNO-FiLM | 标题+年月,arXiv 根链,无作者 | B | 升级:Abdellatif et al. 2025(Heriot-Watt;arXiv ID 待补,二级注记) | A |
| 2 | HyperFNO | Alesiani+ML4PS,缺年份 | B | 升级:NeurIPS ML4PS **2022** workshop,全文 PDF 路径 | A |
| 3 | FNO | Li et al., ICLR 2021 | A | — | A |
| 4 | Mehta 调制 | arXiv:2104.03912 | A | — | A |
| 5a | HyPINO | NeurIPS 2025 无作者 | B | 升级:Bischof et al.(ETH Zurich), NeurIPS 2025 | A |
| 5b | CPNO | "2024"+ScienceDirect 根 | B | **❶年份误记修正 2024→2026**:Biao Chen et al., arXiv:2602.01737 | A |
| 6.1 | Gradient Starvation | Pezeshki et al., NeurIPS 2021+官方仓 | A | — | A |
| 6.2 | E2C | Watter et al., NeurIPS 2015 | A | — | A |
| 6.3 | DVBF | Karl et al., ICLR 2017 | A | — | A |
| 7 | CNO/RPB/PDEBench/Well | Raonic 无 venue/年 | B | 升级主锚:Raonic et al., CNO/RPB(arXiv 2022,ETH 2023 修订版,~331 引);The Well 无作者→二级整改注记 | A |
| 8.1 | Pushforward | arXiv:2202.03376 | A | — | A |
| 8.2 | 低幅局限 | 全路径 PDF+题名,作者记"Havrilla et al.?" | A(误记) | **❶作者误记修正**:实为 PDE-Refiner——Lippe, Veeling, Perdikaris, Turner, Brandstetter, arXiv:2308.05732 | A |
| 8.3 | SRNN | arXiv:1909.13334 | A | — | A |
| 8.4 | Exposure 谱系 | Bengio 2015+Lamb 2016 精确 | A | — | A |
| 9.1 | PE | ScienceDirect 根,无作者无题名 | B | **留 B**(整改登记:补经典教材题录+HAL 预印本作者) | B |
| 9.2 | Concurrent Learning | Chowdhary & Johnson CDC 2010 | A | — | A |
| 9.3 | OED | Rojas et al. 2007+题名 | A | — | A |
| 10.1 | TR-Sym ODE | 无作者无年,proceedings 根 | B | 升级:Huh, Kang, Chun, Kim & Kim(KAIST), NeurIPS 2021, arXiv:2007.11362 | A |
| 10.2 | Noether 硬/软 | Noether's Razor, NeurIPS 2024 | A | — | A |
| 11.1 | 谱混叠 | 三链全聚合根(RG/EmergentMind/arXiv 根) | B | **留 B**(整改登记:证据轮逐条补 ID/作者) | B |
| 11.2 | 分辨率边界 | ResearchSquare 根无作者 | B | 升级:Resolution-Invariant Fluid Dynamics Modeling(Research Square rs-8218223, 2025-11,全文路径) | A |
| 12.1 | Amortization gap | Cremer et al., ICML 2018 全路径 | A | — | A |
| 12.2 | NP/ANP | Kim et al., ICLR 2019+Garnelo 2018 | A | — | A |
| 13.1 | CfC 闭式 | Hasani et al., Nature MI 2022+官方仓 | A | — | A |
| 13.2 | CfC 活跃度 | Urrea et al., MDPI 2024 | A | — | A |
| 14.1 | 无噪边界 | arXiv:2312.00301+2504.18076 | A | — | A |
| 15.1 | D-HNN | arXiv:2201.10085+官方仓 | A | — | A |
| 15.2 | Port-HNN | Desai PRE 2021+Roth forum ID | A | — | A |
| 15.3 | 耗散×辛边界 | APS DOI+Müller 2023 | A | — | A |
| 16.1 | Deep-OSG | Chen et al., JCP 2023 | A | — | A |
| 16.2 | Koopman 综述 | Brunton et al., SIAM Rev 2022 | A | — | A |
| 16.3 | HNK 混合 | Zhang 2024+Wang 2024 | A | — | A |
| 17.1 | F-Principle | Rahaman et al., ICML 2019 | A | — | A |
| 17.2 | PINN 谱偏置 | arXiv:2602.19265 全路径 | A | — | A |
| 17.3 | 处方谱系 | Khodakarami et al. 2025(OSTI) | A | — | A |
| 18.1 | VPT | Vlachas et al., PRS-A 2018 | A | — | A |
| 18.2 | 复合误差 | arXiv:2203.09637+forum ID | A | — | A |
| 18.3 | Lyapunov 边界 | alphaxiv 裸链,无作者 | B | 升级:Learning Chaos in a Linear Way = Cheng, arXiv:2503.14702;RF-HNN = Choi et al., arXiv:2607.28977 | A |
| 19.1 | TSFM 范式 | "arXiv 2025-04"无作者 | B | 升级:Jain et al.(Dell), arXiv:2504.04011 | A |
| 19.2 | DYN 层 | Brachet et al., OpenReview 缺年 | B | 升级:Brachet, Richard & Hudelot, **ECAI 2025**(DBLP conf/ecai/BrachetRH25) | A |
| 19.3 | 天气宏观轴 | ScienceDirect 2026 综述无作者 | B | **留 B**(整改登记:蒸馏轮补作者/DOI) | B |
| 20.1 | UQ 分类 | He et al. 2023+Schmid et al. 2025 | A | — | A |
| 20.2 | DE vs BNN | arXiv:2509.19180+全路径 PDF | A | — | A |
| 20.3 | 校准规范 | Marx 2025(author+year+题名) | A | — | A |
| 21.1 | AI Poincaré | Liu et al., PR 2021 | A | — | A |
| 21.2 | LieGAN | ICML 2023(轮 88 修订),精确 ID 待补 | B | **升级并销轮 88 待办**:Yang et al., "Generative Adversarial Symmetry Discovery", ICML 2023, **arXiv:2302.00236** | A |
| 21.3 | 硬编码权衡 | SIAM DOI+SD 全路径 pii | A | — | A |
| 22.1 | DP 训练 | Um et al., NeurIPS 2020 | A | — | A |
| 22.2 | 辛伴随 | Matsubara et al., arXiv 根,缺 ID | B | 升级:NeurIPS 2021 版 arXiv:2102.08532;IEEE 扩展版(~21 引与本条吻合) | A |
| 22.3 | 前向≠反向 | SymODEN/Hamiltonian Matching 均无题录细节 | B | 升级:SymODEN = Zhong, Datta, Kolter, Kiziltan & Pappas, ICLR 2020;Hamiltonian Matching = Canizares et al., NeurReps **Workshop** @ NeurIPS 2024(venue 修正);Pascanu = arXiv:1211.5063 | A |

## 4. 内部 [行动] 协议条目(4 条,不计复核率)

| § | 条目 | 出处性质 | 可复核性 |
|---|---|---|---|
| 19.4 | TSFM-BASELINE 协议 | 本仓 docs/tsfm-baseline-protocol.md+PRD §19 轮 81 预注册 | 内部可复核(已结案 D-2) |
| 20.4 | UQ-AUDIT | 本仓 probabilistic_eval.py+PRD §19 轮 83 预注册 | 内部可复核(已结案 D-1) |
| 21.4 | SD-POS | 本仓 docs/structure-injection-vs-discovery.md+轮 85 预注册 | 内部可复核(轮 86 结案) |
| 22.4 | GRAD-PATH | 本仓 grad_path_probe.py+PRD §19 轮 87 预注册 | 内部可复核(轮 93 结案) |

## 5. 题录可复核率(判负①②判据数字)

- **修前**:34/50 = **68.0%**
- **修后**(本轮 13 条检索复核升级后):47/50 = **94.0%**
- 剩余 B:§9.1(PE 经典无题录)、§11.1(三条聚合根链)、§19.3(天气综述
  无作者)——整改计划见 §7。

## 6. 修订清单(本轮全部写回动作)

### 6.1 事实错误修正(判负③触发:当轮修订+PLAYBOOK 回写)

1. **§8.2 作者误记**:"Havrilla et al.?" → 实为 **PDE-Refiner(Lippe, Veeling,
   Perdikaris, Turner & Brandstetter, NeurIPS 2023, arXiv:2308.05732)**;
   原条目全路径 PDF 链接与题名无误,作者名错。判据影响:无(内容映射
   "pushforward 低幅局限"不依赖作者)。
2. **§5b CPNO 年份误记**:"CPNO(2024)" → **arXiv:2602.01737(2026-02 预印,
   Biao Chen et al.)**;检索一致定年 2026,未见 2024 版。
3. **§21.2 LieGAN 待办销账**(轮 88 抓出的既成错误,本轮补齐精确记录):
   Yang et al., ICML 2023, arXiv:2302.00236。

### 6.2 题录升级(B→A,13 条)

§1(Abdellatif 2025)、§2(ML4PS 2022)、§5a(Bischof/NeurIPS 2025)、
§5b(见 6.1)、§7(Raonic/CNO-RPB)、§10.1(Huh/NeurIPS 2021)、
§11.2(rs-8218223)、§18.3(2503.14702+2607.28977)、§19.1(2504.04011)、
§19.2(ECAI 2025)、§21.2(见 6.1)、§22.2(2102.08532+IEEE 扩展)、
§22.3(ICLR 2020+NeurReps 2024+1211.5063)。全部以
"SCAN-AUDIT 修订(轮 94)"注记写回 scan-conditioning.md 就地,原文不改写。

### 6.3 缺证性声明降档扫(AMM-015 第二款,全库)

| 位置 | 原文(最强断言) | 处置 |
|---|---|---|
| scan §7【验证状态】行 | "规范空白:已验证(检索侧)" | **降档修订**:"检索未见(非证真空白)"——轮 88 只降了内容行,状态行漏网,本轮补 |
| scan §3 | "无同类工作直接研究" | 就地注记降档:"当前 query 族下未检索到同类(轮 43 检索口径)" |
| scan §6.1 | "硬约束物理架构上首次机械测量" | 就地注记降档:"据当前检索未见先例——非证真首创" |
| scan §7 蒸馏结论 2 | "完整协议无成文先例" | 就地注记降档:"当前 query 族下未检索到成文先例" |
| docs/d1-start-state-mismatch.md:102 | "no prior work on training-loop curricula…" | 就地降档:"no prior work **found in our retrieval**…"+"appears to be the first"保留其既有 hedge |
| docs/PRD.md:454(轮 42 前后) | "无人做硬约束架构的训练循环课程" | **PRD 历史判定行不改写**;登记本表,N1 引用该结论时按降档口径表述 |
| docs/PRD.md:584(轮 59) | "极少成文——公认空白" | 同上(轮 88 已在 scan §7 内容行降档,PRD 历史行保留原貌,本表留痕) |

其余 grep 命中(首个 k 档/唯一变量/唯一挡路/首次扫描等)均为内部技术或
过程陈述,非文献存在性断言,不降档。

### 6.4 二级出处缺陷注记(不降主级,整改随 §7)

§7 The Well 无作者;§8.4 DySI 缺 venue;§9.2 Parikh 缺 venue/年;§9.3
Busetto 缺年;§10.1 TS-IDM 缺年;§10.2 Neural Mechanics 缺作者;§13.2
"2025 综述"未具名;§14.1 IFAC/IEEE 未具名;§15.2 Hernández 缺 venue;
§16.1 OSG-Net 无作者;§17.1 F-Principle overview 缺年;§17.3 Fourier
features 未具名(宜引 Tancik et al. 2020);§19.1 MDPI 2025 无作者;§19.2
ACM 审计线+NeurIPS 合成数据未具名;§1 arXiv ID 待补;§5a arXiv ID 待补。

## 7. 整改计划(剩余 B 级与二级缺陷)

- **§9.1**:自适应控制 PE 经典教材题录(如 Slotine & Li 1991 教材线)+
  HAL 2023 线性情形预印本作者——下一蒸馏轮 1 次检索可清。
- **§11.1**:三条聚合根链(RG/EmergentMind/arXiv 根)逐条换精确 ID——
  该组条目语义是"社区共识实践",下一次云回传证据轮按需补。
- **§19.3**:天气域系统综述补作者/DOI——N1 introduction 动笔前补。
- **§6.4 二级缺陷**:不阻塞主级复核率,随对应条目被 N1 实际引用时补齐
  (引用驱动,防为补而补)。

### 7.1 整改回填状态(轮 101 更新)

- **§9.1 → A(已清偿)**:Slotine & Li,"Applied Nonlinear Control",
  Prentice Hall 1991(PE §8.31);线性情形改锚 Green & Moore,Systems
  & Control Letters, 1986(原 HAL 链接未能钉住作者,弃用)。
- **§11.1 → A(部分,1 断言降格)**:两条聚合链升级为档内精确锚交叉
  引用(§17.3 Khodakarami HFS 2025 / §17.1 Xu et al. 2025);EmergentMind
  "混叠误差不随训练数据规模消失"原始论文未能定位 ⇒ 该断言降格为
  "未复核",不得以强断言引用;其余主张由精确锚支撑。
- **§19.3 → A(已清偿)**:Waqas et al. 2026 系统综述(ScienceDirect,
  作者+年+题名;DOI 卷期随引用补)。
- **修后题录可复核率:50/50 = 100%**(B 级清零;§6.4 二级缺陷清单
  维持引用驱动消化;§11.1 一条降格断言引用前必须补原始出处)。

## 8. IR 首算(轮 88 预注册交付物;DEBT-LEDGER 指标行同步)

- 分子:**2** = 未消化 [行动] 条目(R1b/R1c 条件性重入口——R1 判负字面
  触发,GOALS 轮 90 注记列为队列候选非欠账,待路由裁决;10/10 队列型
  [行动] 目标 D5/D6/DH/KM/SB/EVAL/TSFM/UQ/SD/GRAD 全部结案消化)。
- 分母:**6** = 近 10 轮(84-93)实验类判读:D-1、D-2、D-2 追记(TimesFM
  臂)、D-3、D-4、GRAD-PATH。
- **IR = 2/6 ≈ 0.33**(若按 GOALS 口径排除条件性登记则 0/6=0;取保守
  上界 0.33)——远低于报警线 5,**无 S2 触发**。DEBT-LEDGER"待首算
  (≈1.2 人工估)"同步替换为本实测口径。

## 9. 判负标准对账(PRD §19 轮 88 预注册)

- **① 修后可复核率 <80%?否**——94.0% ≥ 80%,蒸馏管线**不降速**。
- **② 修后 ≥95%?否**(94.0%<95%)——不满足"仅登记结论"条件;整改面
  (3 条 B + 二级缺陷)按 §7 计划登记,随后续轮消化。
- **③ 新题录事实错误?是,2 处**(§8.2 作者、§5b CPNO 年份)——已当轮
  修订(6.1),PLAYBOOK 无对应坑,已回写"作者/年份未核即入库"坑。

## 10. 结论

入库管线溯源面经一轮全库对账后达到 **94% 可复核**(修前 68%),两处
既成事实错误修正、三处缺证性漏网降档、轮 88 遗留待办(LieGAN 精确
题录)销账。挖掘管线维持现行速度(判负①未触发),整改面登记不阻塞。
AMM-015 入库硬标准(题录当场核验+缺证性降档)继续有效;本轮新坑
(带?题录不得过夜、降档扫连状态行一起扫)已回写 PLAYBOOK。
