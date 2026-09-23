# N1 素材索引(轮 105 消化轮;T0 零算力)

> 用途:25 族蒸馏 + 审计 + 探针产出的 N1 可用资产一步取用索引。
> N1 正式英文稿启动属用户决策(GOALS blocked_on 4);启动时按本表
> 逐节取材,出处溯源状态见 docs/scan-traceability-audit.md(条目级
> 主锚 100% A 级,轮 101)。

## 1. 定位三轴表( introduction / Related Work 主表)

三轴模板(轮 76 koopman-bridge):**线性化在哪 / 结构保证在哪 / 情境通道在哪**。五线对照:

| 线 | 线性化 | 结构保证 | 情境通道 | 指针 |
|---|---|---|---|---|
| 本仓 | 无(状态空间) | 哈密顿+辛,守恒由构造 | 观测前缀→ctx 推断 | — |
| Koopman | 可观空间全局线性 | 无能量结构 | 无 | §16.2(Brunton SIAM Rev 2022)/§16.3 HNK 混合线 |
| TSFM | 无 | 无 | 裸序列零样本 | §19(范式/交锋/天气宏观轴)+D-2 实测 |
| SSM(S4/Mamba) | 状态空间线性 | 无物理守恒 | 无 | §24.1(HiPPO 与 ODE 基座同源=盟友) |
| NODE/CDE | 无 | 无 | CDE 部分有(path) | §24.2(SUBNET-CT 盟友实证) |

一句话定位(各线):互补谱系非排名;结构化优势有盟友实证(SUBNET-CT
ICLR 2023);评审"为何不用 X"逐线有现成答案。

## 2. 基座小节(Related Work/Methods)

- CfC 闭式基座:Hasani et al., Nature MI 2022(§13.1)+活跃度证据
  (§13.2 Urrea MDPI 2024);诚实 scope:闭式近似层未分离(§13.1
  limitation 注记)。
- DP 训练范式:Um et al., NeurIPS 2020(§22.1)——本仓 train_semigroup/
  prefix 即 DP 形态,方法节奠基引用。

## 3. 条件化小节(Related Work"条件化")

UFNO-FiLM(§1,Abdellatif 2025)/HyperFNO(§2,ML4PS 2022)/FNO 全场
拼接对照(§3)/Mehta 调制分类学(§4)/HyPINO+CPNO(§5)——"低维推断码×
谱势能接口"空位声明(轮 101 整改后降档口径:"当前 query 族下未检索到
同类")。E2 接口消融三变体的文献坐标齐(§1-5 汇总节)。

## 4. 机制链章(Discussion/Mechanism)

E1 推断缺口叙事链(坐标按证据顺序):D6 信息预算(t³ 无平台,层 1 非瓶颈)
→ E3 容量否定(+46% 参数零效应)→ E4a 梯度饥饿(3.97e-3,§6.1 Gradient
Starvation 命名)→ 谱偏置候选(§17,SB-NAMING 文档四问对账)→
amortization gap 命名(§12.1 Cremer ICML 2018)。
**M2 附加(轮 95 机制发现)**:聚合层均值场恒等式——c(x) 信息在
mean-pool 处精确湮灭(8.6e-11),attn 修复判负(轮 96)⇒ P3 终收口
(轮 97):M2 链路 headroom 关闭,N1 定位锚结构性质轴+硬约束边界声明。

## 5. Methods 三件套(Methods/实现辩护)

1. **阶数**:Verlet 观测阶 2.021(能量)/1.999(RMSE)双轴确认
   (VERLET-ORDER 判读,轮 104);平方指标阶翻倍坑已注记。
2. **理论**:影子哈密顿/后向误差分析(Hairer-Lubich-Wanner 2006;
   §25.2)——漂移有界定理级;hω≈0.18(0.1×1.8)远在界内。
3. **步长策略**:固定步长辩护(§25.3;自适应换误差丢结构)。
另:半群训练先例 SRNN(§8.3)/Deep-OSG(§16.1);PE 量化(§9.1)/
并发学习(§9.2);梯度方案三分(§22.2:展开=精确梯度,O(k) 内存,
k_train=8 实测零压力——GRAD-PATH 轮 93 实测背书 2.94→47MB 线性斜率
1.0000)。

## 6. 实验基线表(Experiments)

| 基线行 | 数字锚 | 协议/三声明 |
|---|---|---|
| TSFM(Chronos) | k100 1.229±0.11(q-only) | D-2 判读+tsfm-baseline-protocol.md |
| TSFM(TimesFM) | k100 0.167±0.09 | D-2 轮 92 追记 |
| 经典 LSQ-ω̂/STLSQ | k100 2.7e-6(上界参照) | classic-baseline-protocol.md(轮 99) |
| 结构臂 prefix/all2all | 5.006/11.58(n32) | d1b 同池 |
| oracle 上界 | 0.0148 | 轮 51 勿重跑条款 |

评估口径:eval_ks 阶梯(§18.2 复合误差背书)/VPT 补充口径(§18.1+
eval-norms-vpt.md,轮 80 窄窗降格注记)/暴露偏差辩护(§8.5 D5 判读)/
Lyapunov 边界声明(§18.3:守恒可积域,未验证混沌域)。

## 7. 诚实边界/limitation 清单(Limitations)

1. 无噪仿真(§14.1,轮 71 代码判读)——范围声明 noise-free sim。
2. UQ 上限 L2 训练方差(D-1 判负:coverage 1.6%/0/0);种子=迷你 DE
   (§20.2,不可称后验覆盖)。
3. M2 headroom 关闭(P3 终收口,轮 97)——四路处方全负证据链。
4. T 非偶(轮 66):守恒与时间反演是独立性质;R1b 未触发终态。
5. 硬约束失败模式与逃生门(§21.3+轮 86 文档):耗散槽位/Nonseparable
   头/MLP 平滑未解。**Nonseparable 门已本机实证(轮 110 ESC-DOOR-VAB,
   [B] 级,1-seed T1 筛查口径)**:磁族同池同预算 A/B——可分臂 k100
   MSE 1.449e-01(饱和于解析偏置地板 ~5e-5 量级)vs 非可分臂
   2.388e-06,比值 60669×,双臂自身 H 漂移 ≤2e-06,"门该开时才开"
   成立;多 seed 终局=停车场。
6. 闭式近似层未分离(§13.1);混沌域未验证(§18.3)。

## 8. 守恒与结构哲学(Discussion)

硬/软二分(§10.2 Noether's Razor 对照)/分层注入哲学(轮 86
structure-injection-vs-discovery.md)/发现谱系上游(SINDy §23.1、
AI Poincaré §21.1)/"注入是可撤销赌注清单"表述。

## 9. 报告规范(Experiments/附录)

RSI-Exam 哲学(§7,降档口径)+隐藏集实践(轮 44 反转抓取,seed 999
退役/998 递减)+跨 pool 几何均值(G2)+校准判据(§20.3:有 spread
≠ 校准)。

## 10. future work 菜单(Discussion 结尾)

结构发现谱系上游(§21.1/§23.1)/噪声注入线(§14)/SSM 对照基线
(§24.3,届时按 TSFM 先例预注册)/shadow-Hamiltonian 诊断升级(§25.2
Skeel 法)/训练后符号化(§23.3 Fronk & Petzold)/P-CfC 门控(§13.2)/
高阶组合升级(§25.1 Yoshida,长视距时)。

## 11. 待用户决策

- N1 正式英文稿是否启动(blocked_on 4)。
- origin/master PR#1 合入顺序(blocked_on 3)。
- D4 GPU 通道去向(blocked_on 2)。
