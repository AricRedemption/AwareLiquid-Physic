# N1 Paper Draft v0(轮 107 起草;T0 零算力)

> **治理注记(中文,投稿前删除)**:本稿为循环自主起草的 v0 初稿
> (AMM-022 提案授权范围:初稿/迭代可自主,终稿/投稿/venue/署名待人决)。
> 所有数字严格取自 `docs/n1-asset-index.md`(溯源:条目级主锚 100% A 级,
> docs/scan-traceability-audit.md);索引未覆盖的细节以 `[v0-TODO]` 显式
> 留缺,不编造。证据分级见附录 A:`[A]`=构造保证(闭式)、`[B]`=本机
> T1/T2 实测(确定性可复现)、`[C]`=终局声明待 T3 或隐藏卷(998 起一次性)。
> 本稿**不含任何 [C] 级终局断言**——按结论分级纪律,T1/T2 只解锁路由
> 与筛选。

---

# Structure by Construction: Liquid Context Inference with
# Hamiltonian-Constrained Symplectic Rollout for Physical System Identification

[v0-TODO: title alternatives; venue 未定(人决项)]

## Abstract

Physical structure should live in the architecture, not in the loss. We
study a continuous-time model that splits the two jobs a physical forecaster
must do: (i) *inferring the context* of an observed trajectory, and (ii)
*integrating it forward* under a conservable dynamics. A closed-form liquid
(LTC) base [B, CfC; Hasani et al., Nature MI 2022] infers a low-dimensional
context code from the observation prefix; a Hamiltonian head consumes the
code as a potential-energy interface and is rolled out with a fixed-step
velocity Verlet integrator, so energy conservation is guaranteed *by
construction* at the integrator level [A] and verified numerically [B]:
observed convergence orders 2.021 (energy drift) and 1.999 (rollout RMSE)
confirm the theoretical second order, with the shadow-Hamiltonian drift
parameter hω ≈ 0.18 far inside the backward-error-analysis bound
[Hairer–Lubich–Wanner 2006].

On a noise-free spring benchmark the exact-oracle context upper bound is
0.0148 rollout MSE at k=100 [B]; a closed-form liquid base with the
Hamiltonian head reaches the structural-arm operating point (5.006 vs 11.58
for the all2all counterpart at n32) [B], while zero-shot foundation models
sit at 1.229±0.11 (Chronos) and 0.167±0.09 (TimesFM) [B, cross-category
reference under a three-declaration fairness protocol] and classical
system identification (LSQ-ω̂ / STLSQ) reaches 2.7e-6 — a near-oracle
*upper reference* that bounds what any learned approach can meaningfully
claim in this regime [B]. We further close the field-reconstruction (M2)
headroom with a mechanism result: on periodic grids the mean-pooled
aggregation layer *exactly annihilates* the medium field c(x) (total
retention 8.6e-11), by an exchange identity rather than an empirical
observation [B]; four repair prescriptions were tested and all judged
negative. We position the contribution on the structure-property axis with
explicit hard-constraint boundary declarations, and we catalogue failure
modes with pre-registered escape hatches (dissipation slot, T-even
relaxation, nonseparable head).

[v0-TODO: abstract 数字口径复核——TSFM/结构臂是否同一 eval_ks 阶梯同表
可比;若否,按三声明协议拆表。]

## 1 Introduction

Small-sample physical system identification faces a split: black-box
sequence models amortize broad priors but carry no dynamics structure;
classical identification is sample-efficient but brittle to unmodeled
coordinates. We propose to hard-inject only what is *structural* — the
existence of a Hamiltonian and a symplectic integrator — while leaving the
*functional form* (the potential/kinetic landscape) free, and letting a
liquid continuous-time base infer the instance-specific context from data.

**Contributions.**

1. **Architecture.** A two-stage continuous-time model: liquid (LTC) base
   → low-dim context code → Hamiltonian head (H = T(p) + V(q; c)) rolled
   out by fixed-step velocity Verlet. Conservation by construction [A];
   layered-injection philosophy: hard at the conservation-law layer, free
   at the function-form layer — every injection ships with a registered
   escape hatch (Sec. 7).
2. **Integrator accountability.** Observed order 2.021 / 1.999 on the two
   error axes [B], a shadow-Hamiltonian drift budget hω ≈ 0.18 well inside
   the theoretical bound [B, theory anchor: Hairer–Lubich–Wanner 2006],
   and a fixed-step defense (adaptive stepping trades error for structure).
3. **Mechanism results.** (i) The inference-gap chain: information budget
   is not the bottleneck (t³ budget growth, no plateau [B]); capacity is
   not the bottleneck (+46% parameters, zero effect [B]); gradient
   starvation is (3.97e-3 [B], Gradient Starvation naming), with spectral
   bias and amortization-gap candidates named under a four-question
   audit [B]. (ii) The **mean-field identity**: on periodic grids,
   mean-pooling commutes with the shared operator and the spatial mean of
   the acceleration field vanishes term-by-term — c(x) information is
   *exactly* annihilated at the aggregation layer (total retention 8.6e-11
   [B]); attention repair opens the channel yet remains budget-limited
   (judged negative), closing the M2 headroom [B].
4. **Honest baselining.** Cross-category references (TSFM zero-shot) under
   a three-declaration fairness protocol; classical identification as a
   near-oracle *upper reference*; oracle-context bound 0.0148 as the
   interface ceiling [B].

## 2 Related Work

Five lineages, three axes (where is the linearization / where is the
structural guarantee / where is the contextual channel):

| Line | Linearization | Structural guarantee | Contextual channel |
|---|---|---|---|
| **Ours** | none (state space) | Hamiltonian + symplectic, conservation by construction | observed prefix → inferred ctx code |
| Koopman | global linear in observable space | none (no energy structure) | none |
| TSFM | none | none | bare sequence, zero-shot |
| SSM (S4/Mamba) | linear state space | none (no physical conservation) | none |
| NODE / CDE | none | none | CDE partially (path) |

**Positioning.** These are complementary lineages, not a ranking. HiPPO's
continuous-time foundation is an ally of our ODE base [S4 line]; structured
state-space identification outperforming black-box NODEs is ally evidence
for structure [SUBNET-CT, ICLR 2023]. The conditioning interface (low-dim
inferred code × spectral-potential interface) was **not retrieved under
current query families** [degraded claim per AMM-015 — an existence claim
is only as strong as its search]; FiLM-style conditioning (UFNO-FiLM),
HyperNetwork conditioning (HyperFNO), full-field concatenation (FNO), and
modulation taxonomies are the nearest neighbors.

**Base and training paradigm.** Closed-form liquid base: CfC [Hasani et
al., Nature MI 2022] — honest scope: the closed-form approximation layer
is not disentangled (limitation 6). Training paradigm: semigroup/prefix
training is a deep-print (DP) form [Um et al., NeurIPS 2020]; semigroup
training precedent SRNN; deep operator splitting Deep-OSG. Prediction-error
quantification anchor: Green & Moore (1986); concurrent learning as the
data-side counterpart.

## 3 Method

**Liquid base.** A closed-form continuous-time liquid network (CfC) reads
the observation prefix and produces a context code c ∈ R^d (d small;
`--context_dim 1` = ω-faithful instantiation in the spring family).

**Hamiltonian head.** c enters as a potential-energy interface:
H(q, p; c) = T(p) + V(q; c), with T, V realized as MLPs (function-form
layer left free by design).

**Integrator.** Fixed-step velocity Verlet; the kick receives force terms
as +dt/2·F (ṗ = −∇qH + F) [implementation pitfall registered: sign flips
become anti-damping and are caught by a monotonicity probe, not by the
preregistered gate]. No adaptive stepping (Sec. 4).

**Training.** Semigroup and prefix loops (DP form). Gradients: unrolled
BPTT is the exact gradient with O(k) memory; at k_train = 8 the footprint
is 2.94→47 MB across k = 8/32/128 with measured slope 1.0000
(saved-tensors-hooks accounting) — zero memory pressure at operating
points [B, GRAD-PATH probe].

**Escape hatches (registered per-injection).** conservation → dissipation
slot (γ); T-even assumption → R1b relaxation (never triggered, terminal);
separability → nonseparable head (available, unused); MLP smoothness →
unresolved, recorded as a limitation.

## 4 Integrator Accountability (Methods defense)

Three-piece defense for the methods section:

1. **Order (measured).** Fixed horizon T=10, dt ∈ {0.2, 0.1, 0.05, 0.025}
   (k = T/dt — horizon held fixed, else horizon shrinkage contaminates the
   order). Energy-drift axis: observed order 2.021 (asymptotic pairs
   2.13/2.03/2.01, all in-band); pointwise RMSE axis: 1.999 (2.00 ×3).
   The raw-MSE axis reads 4.00 — a *squared* metric doubles the observed
   order of the underlying second-order accuracy; pointwise claims use
   the RMSE axis [B, VERLET-ORDER preregistered pass band p̂ ∈ [1.8, 2.2]].
2. **Theory (bound).** Backward error analysis: the modified (shadow)
   Hamiltonian is exactly conserved to O(h^2); the drift of the true H is
   bounded over exponentially long times. Our operating point hω ≈ 0.18
   (dt=0.1 × ω=1.8) is far inside the regime where the bound is
   meaningful [Hairer–Lubich–Wanner, Springer 2006].
3. **Step-size policy.** Fixed step. Adaptive integrators trade structure
   for error: step-size adaptivity breaks the symplectic map, and the
   measured drift is our contract, not an adaptive re-negotiation.
   (Higher-order composition is available — Yoshida — but deferred:
   conservation is carried by measurement, and hω ≈ 0.18 leaves orders of
   magnitude before integrator error approaches learning error.)

## 5 Experiments

**Protocol.** Same-pool comparisons; cross-pool results reported as
geometric means [G2]. Rollout error at the eval_ks ladder (composite-error
backing); VPT as a supplementary lens only (separation holds in a narrow
θ-window — downgraded to presentation norm, not a new verdict). Noise-free
simulation throughout (scope declaration, limitation 1). Hidden-set
discipline: seed 999 retired after it caught a visible-set reversal
(prefix advantage flipped +29% on held-out); consumption is one-shot per
seed, descending from 998 — **no [C]-tier terminal claims are made in this
draft**.

| Row | Result (k=100 rollout MSE unless noted) | Tier | Protocol / pointer |
|---|---|---|---|
| Oracle context (upper bound) | 0.0148 | [B] | do-not-rerun clause, round 51 |
| Classical LSQ-ω̂ / STLSQ (upper reference) | 2.7e-6 (ω̂ err 0.069%) | [B] | classic-baseline-protocol.md |
| TSFM Chronos (zero-shot, q-only) | 1.229 ± 0.11 | [B] | tsfm-baseline-protocol.md, three declarations |
| TSFM TimesFM (zero-shot) | 0.167 ± 0.09 | [B] | D-2 addendum, round 92 |
| Structural arm prefix (n32) | 5.006 | [B] | d1b same-pool |
| Structural arm all2all (n32) | 11.58 | [B] | d1b same-pool |

**Reading.** Classical identification at 2.7e-6 is a *reference ceiling*,
not a competitor: in a noise-free linear regime the parametric method
should win, and it bounds what any learned claim can mean here [three
declarations]. TSFM zero-shot numbers are cross-category references under
pretraining-breadth vs small-sample-structure disparity. The structural
arm comparison (prefix vs all2all) is the in-family ablation axis.
[v0-TODO: 结构臂与 TSFM/oracle 是否同一评估协议同表呈现,复核后定稿;
 uncertainty 列(d1b stderr)待补。]

**UQ.** Ensemble spread exists but is not calibration: coverage@95 measured
1.6% / 0 / 0 across seeds (D-1 judged negative — overconfidence direction);
seed-ensembles are mini deep-ensembles, not posterior coverage. Claims
capped at L2 (training-variance) tier.

## 6 Mechanism Analysis

**Inference gap (M1).** Why does the amortized context underuse the
available information? Chain, in evidence order: (i) the observation
window carries a t³-growing information budget with no plateau — the
window is not the bottleneck [B, D6]; (ii) capacity is not the bottleneck:
+46% parameters produce zero effect [B, E3]; (iii) the bottleneck is
optimization: gradient starvation at 3.97e-3 [B, E4a; Gradient Starvation
naming], with spectral bias (four-question naming audit, scope-narrowed)
and the amortization gap [Cremer et al., ICML 2018] as the named frame.

**Field reconstruction (M2) — a closed result.** On periodic grids with a
shared linear operator, mean-pooling commutes with the operator, and the
spatial mean of the acceleration field cancels term-by-term to exactly
zero: the mean-field rollout is strictly uniform and independent of the
medium c(x). The aggregation layer therefore annihilates c(x) *by
identity*, measured at total retention 8.6e-11 [B]. Attention pooling
opens the channel (zero-init equivalence anchor: first forward bitwise
equals mean-pool) yet the standard budget still cannot extract the field —
repair judged negative; with four prescriptions all negative (supervised
R1, horizon R2, interface E2, attention R1c), the M2 headroom is **closed**
[P3]. N1 therefore claims the *structure-property* axis and states the
hard-constraint boundary explicitly; the oracle gap (−26%) is an
interface-reachable upper bound, not a reachable gain.

## 7 Honest Limitations

1. **Noise-free simulation.** All results are in the noise-free regime
   (code-audit confirmed); no noisy-domain claim is made.
2. **UQ ceiling.** Uncertainty is L2 (training variance) at best;
   coverage is not achieved (1.6%/0/0); no posterior claim.
3. **M2 closed.** Field-reconstruction headroom is closed with an
   all-negative evidence chain; we do not promise it back.
4. **Conservation ≠ time-reversal.** T-symmetry is an independent
   property (T-non-even finding); the R1b relaxation path exists and was
   never needed.
5. **Hard-constraint failure modes** carry registered escape hatches
   (dissipation slot / nonseparable head / T-even relaxation); MLP
   smoothness failure mode remains unsolved and is recorded as such —
   injection is a revocable bet list, not dogma. The nonseparable hatch
   is locally validated [B, 1-seed screening]: on the magnetic family
   (equal budget, same pool) the separable head saturates at its analytic
   bias floor while the nonseparable head reaches 2.4e-06 rollout MSE — a
   60669x gap with both arms' architectural conservation intact (PRD §19
   round 110); multi-seed finals remain parked.
6. **Closed-form base layer not disentangled** (CfC approximation vs
   full LTC dynamics); **chaotic domain not verified** (conservation
   claims restricted to the integrable regime; Lyapunov-boundary
   declaration).

## 8 Conclusion and Future Work

We argued for structure by construction at the conservation-law layer with
free function forms, delivered the integrator accountability that makes
the hard constraint auditable, closed the field-reconstruction headroom
with an identity rather than an excuse, and catalogued what the
architecture cannot do. Future work menu: discovery-lineage upstream
(SINDy / AI Poincaré / LieGAN) to propose the injected structure;
noise-injection line; SSM control baselines (pre-registered per the TSFM
precedent when scheduled); shadow-Hamiltonian monitoring upgrade (Skeel
reading); post-hoc symbolization; P-CfC gating; higher-order composition
for long horizons.

## Appendix A: Claim Tier Ledger

| Tier | Meaning | Items in this draft |
|---|---|---|
| [A] | By construction (closed form) | conservation at integrator level; mean-field identity (algebraic) |
| [B] | Local T1/T2 measurement, deterministic CPU, reproducible | all tables/orders/drifts above |
| [C] | Terminal claim — requires T3 or hidden-set (998, one-shot) | **none asserted**; required for: any noisy-domain claim, chaos-domain conservation, cross-domain transfer, final headline numbers |

Hidden-set ledger: 999 consumed (round 44; H1 ✓ mechanism migrated / H2 ✗
advantage reversed — the reversal that anchored the discipline), 998
retained. [v0-TODO: 终稿前如需 [C] 级声明,预注册 998 一次性终跑清单。]

---

*Draft provenance: round 107, T0, assets from docs/n1-asset-index.md
(25-family distillation, traceability 100% A-grade entry-level); all
pointers resolve into docs/scan-conditioning.md, docs/PRD.md §19, and the
protocol documents listed per row. Updated round 110: escape-hatch
nonseparable validation added to Limitations 5 (T1 probe, PRD §19).*
