# N1 复现性审计报告(轮 869;N1-REPRO-AUDIT 队列条目交付物)

> 审计对象=`docs/n1-paper-draft.md`(v0,轮 869 时点 HEAD 4648559 后工作区版)。
> 审计框架=AAAI-26 Reproducibility Checklist 披露面(算力基础设施/seed/
> 数据统计与划分/代码可用性/预注册与口径注记)+ LTSF taxonomy 评估批判
> (arXiv 2026-08 "Time-Series Forecasting Must Adopt Taxonomy-Specific
> Evaluation")对表。零算力 T1 写作轴;本报告自洽(数字/行号取自草稿本拍
> 实读,不引用本地-only 产物)。

审计结论: 2 缺口发现, 1 条本拍已修入稿(G2), 1 条注记待用户门控(G1);
数据/seed/预注册/评估口径四面披露达标, LTSF taxonomy 对表无冲突——
草稿披露面达投稿就绪级(待 G1 用户决策与 venue 人决后闭合)。

## 逐面审计

| 面 | AAAI-26 清单要求 | 草稿现状(证据) | 判定 |
|---|---|---|---|
| 算力基础设施 | CPU/GPU 型号、内存、OS、运行时披露 | 原稿仅 "single-machine deterministic CPU"(§5/§7/AppA 三处),无设备/OS/运行时 | **G2 缺口→本拍已修**:§5 Protocol 段补 Apple M2 Max(CPU-only)/macOS/单实验分钟级 wall-clock/meta(git_sha,device,timestamp) 溯源一句(事实性,与 AGENTS.md 本机口径及 PRD 轮 92/18 运行时记录 4.6min/3min/7min29s 一致) |
| seed 与运行次数 | 运行次数、seed、误差棒 | 3-seed±stderr 行内披露(§5 表 Uncertainty 列)、隐藏卷 999/998 一次性协议全文(AppA ledger)、每 recipe 行 seed-set scope 行内标注(轮 812/814 后) | 达标 |
| 数据统计与划分 | 数据集统计、划分、规模 | M1 spring family、768-traj pool、n∈{64,128,256} 训练规模、k=100 评估、q-only vs q+p 口径列、noise-free scope 声明(§5);积分器/dt=0.1/Verlet(§3) | 达标 |
| 预注册与口径注记 | 预注册、口径偏离如实注记 | 预注册判负标准纪律全文(§5 Protocol)、口径偏离注记先例(轮 13/111 审计行在稿)、[A]/[B]/[C] 分级 ledger(AppA) | 达标 |
| 代码/产物可用性 | 代码与数据可用性声明 | 草稿仅以内部协议文档文件名作 pointer(classic-baseline-protocol.md 等),无面向读者的可用性声明 | **G1 缺口→注记待用户**:发布承诺属用户门控决策(禁代理代决"code will be released");处置=留待 venue 人决同拍由用户裁(与 AMM-034-N1-TODO 门控项合并处置),本拍不入稿 |
| LTSF taxonomy 对表 | 评估方案与任务 taxonomy 匹配 | 草稿已按 taxonomy 分列(q-only vs q+p 口径列、eval_ks 阶梯、同表 scope 轮 111 审计行、TSFM 定位为 cross-category reference 而非同轴竞品)——与该批判的核心主张(禁跨 taxonomy 直接比 MSE)一致,无冲突;是否引用该文入 Related Work=venue 人决后定(REGISTRY LTSF-TAXONOMY-EVAL, state=reference) | 对表通过,零缺口 |

## 判负标准履行(预注册,轮 868 队列条目)

- 判负=审计发现披露缺口未处置即未达成 → 实测:G2 已修入稿、G1 已注记
  处置路径(用户门控)、G3 面(数据/seed/预注册)无缺口——**判负标准未触发,
  迭代达成**。
- 决策耦合履行(轮 868 预注册):发现披露缺口⇒改稿(G2 已改);零缺口面⇒
  投稿就绪确认(本报告结论行)。

## 遗留(不阻塞本条目 done)

- G1 代码可用性声明=用户门控(合并入 AMM-034-N1-TODO 的 venue/发布人决)。
- 题录引用决策(CONS-Q-EVAL/LTSF-TAXONOMY-EVAL 是否入 Related Work)=
  venue 人决后,REGISTRY 题录节留痕在案。
