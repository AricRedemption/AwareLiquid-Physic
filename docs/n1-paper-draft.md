# N1 Paper Draft v0(轮 107 起草;T0 零算力)

> **治理注记(中文,投稿前删除)**:本稿为循环自主起草的 v0 初稿
> (AMM-022 提案授权范围:初稿/迭代可自主,终稿/投稿/venue/署名待人决)。
> 所有数字严格取自 `docs/n1-asset-index.md`(溯源:条目级主锚 100% A 级,
> docs/scan-traceability-audit.md);索引未覆盖的细节以 `[v0-TODO]` 显式
> 留缺,不编造。轮 285 起每个引用数字回溯**产物 JSON 字段**复算一次
> (轮 111 条款);判读行散文聚合值与产物字段不符时以产物为准(轮 285
> 对账抓出两处,见溯源 footer 注记),历史判定行不改。证据分级见附录 A:`[A]`=构造保证(闭式)、`[B]`=本机
> T1/T2 实测(确定性可复现)、`[C]`=终局声明待 T3 或隐藏卷(998 起一次性;
> 轮 812 已按预注册把 998 一次性消耗并退役，下一档 997，见附录 A 台账)。
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

On a noise-free spring benchmark (q+p rollout MSE at k=100 for the
structural arms; q-only for the reference rows), a closed-form liquid base
with the Hamiltonian head reaches the structural-arm operating point
(5.006±0.76 vs 11.58±4.37 for the all2all counterpart at n32) [B], while
zero-shot foundation models sit at 1.229±0.11 (Chronos) and 0.167±0.09
(TimesFM) [B, cross-category reference under a three-declaration fairness
protocol] and classical system identification (LSQ-ω̂ / STLSQ) reaches
2.7e-6 — a near-oracle *upper reference* that bounds what any learned
approach can meaningfully claim in this regime [B]. On the field-
reconstruction task (M2) we further close the headroom: the exact-oracle
context bound there is 0.0148 rollout MSE vs 0.0204 for the static arm —
a 27% headroom that end-to-end inference does not reach [B] — and the
mechanism is an exchange identity: on periodic grids the mean-pooled
aggregation layer *exactly annihilates* the medium field c(x) (total
retention 8.6e-11), rather than an empirical observation [B]; four repair
prescriptions were tested and all judged negative. On the head-structure
axis we measure what the free function form costs and where it pays: a
degree-matched homogeneous potential — partially surrendering functional
freedom — dominates the free-form default head on both error axes (−34%
in-distribution, −49% extrapolation median) at every horizon tested,
while the boundary is measured, not asserted: the wrong homogeneity
degree pays 7.56×, the advantage is a full-data phenomenon (parity at
n=64), and it does not stack with training-recipe gains [B]. We position
the contribution on the structure-property axis with
explicit hard-constraint boundary declarations, and we catalogue failure
modes with pre-registered escape hatches (dissipation slot, T-even
relaxation, nonseparable head). Finally we report what our own
pre-registered one-shot held-out protocol does to our strongest
training-recipe result: the five-axis composite gain of 10.7% (ratio 0.893,
direction-consistent on all three visible seeds) reverses to a 43.8%
degradation on unseen seed 998 (ratio 1.438), so the recipe benefit is
declared visible-set-scoped and the composite is not promoted to the
default configuration — the second time in this study that a one-shot
hidden-set run caught a visible-set overfit (precedent: seed 999 flipped
the prefix advantage by +29%). The same composite is also budget-limited:
at 8000 training steps instead of 2000 its sign reverses as well (ratio
1.116), so every recipe statement below carries its domain — training
budget, rollout horizon, and seed set.

[Resolved round 111 (digestion audit, PRD §19 "BASELINE-SCOPE 判读"):
same-table presentation holds for the five M1 spring rows on the k=100
ladder, with the metric split made explicit per row (q-only vs q+p) and
uncertainty added; the oracle row was mis-attributed to the spring
benchmark — it is the M2 field-task oracle (round 51 do-not-rerun clause)
and now lives in the M2 mechanism claim only.]

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
   (judged negative), closing the M2 headroom [B]. (iii) The
   **head-structure axis**: a degree-matched homogeneous potential
   (analytic T, radial homogeneous V) dominates the free-form default
   head on both error axes and all horizons tested [B]; the boundary is
   the degree axis (degree-matched ≈3500× over free V on a quartic pool;
   the mis-set degree pays 7.56×), the advantage vanishes in the
   small-sample regime, and composition with the training recipe is
   sub-additive (either-or adoption) [B].
4. **Honest baselining.** Cross-category references (TSFM zero-shot) under
   a three-declaration fairness protocol; classical identification as a
   near-oracle *upper reference*; oracle-context bound 0.0148 on the M2
   field task as the interface ceiling [B] (task attribution audited
   round 111).

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

**Enforcing versus discovering structure.** Within the Hamiltonian line,
a precedent group enforces known symmetries by construction — symmetry
control via cyclic coordinates (SCNN), Lie-algebra symmetry detection,
manifold-constrained Hamiltonian/Lagrangian networks (CHNN/CLNN;
Celledoni et al.) [scan §64.2] — the same layered-injection stance we
take at the head (Sec. 3). Polyakov's generalized homogeneous ANN is a
dedicated approximator for homogeneous function classes [B-adjacent
literature coordinate, scan §64.1], independent precedent that the
homogeneity degree is a real interface parameter (our Sec. 6 boundary
measurement agrees). When the structure is *unknown*, meta-learning is
the measured middle path — Noether Networks report discovered conservation
losses matching hand-coded ones [scan §64.3]; our claim is confined to
the known-structure case, where the hard construction beats the free
form on both axes.

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

**Head-structure axis.** Alongside the free-form default we measure a
structured head: analytic T(p) = ½Σp² and a radial homogeneous potential
V(q; c) = ‖q‖^{2k}·s_θ(0, c), whose one structural parameter k is
matched to the true homogeneity of the potential (k = 1 for the quadratic
spring, k = 2 for a quartic pool). The direction channel is removed
(zeroed input), which makes V's continuity at q = 0 hold *by
construction* — the pathology of the naive homogeneous parameterization
was direction-feature discontinuity (sign flips of q̂ at q = 0), not
homogeneity itself [B, PRD §19 round 268]. Sec. 6 measures what this
partial surrender of functional freedom costs and what it buys.

**Integrator.** Fixed-step velocity Verlet; the kick receives force terms
as +dt/2·F (ṗ = −∇qH + F) [implementation pitfall registered: sign flips
become anti-damping and are caught by a monotonicity probe, not by the
preregistered gate]. No adaptive stepping (Sec. 4).

**Training.** Semigroup and prefix loops (DP form). Gradients: unrolled
BPTT is the exact gradient with O(k) memory; at k_train = 8 the footprint
is 2.94→47 MB across k = 8/32/128 with measured slope 1.0000
(saved-tensors-hooks accounting) — zero memory pressure at operating
points [B, GRAD-PATH probe].

**What is learned.** A head trained at dt = 0.1 transfers across the
scanned dt multiples at fixed physical horizon: cross-dt ratio 0.895
(≤ 2 gate) and 1-step log-log slope 1.995 = O(dt²) — two independent
axes agreeing that the learned object is the vector field, not a
dt-mapping [B, PRD §19 round 129; PR#6 pending merge]. The qualifier
"within the scanned dt multiples" attaches to every "learned H" claim
in this paper; notably, the native reference arms trained at the
evaluation grids perform 13–16× worse (0.046–0.049 vs 0.0030–0.0034),
so the training dt is itself a conditional variable.

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
4. **Training-grid resolution (measured boundary of the fixed-step
   defense).** On a single-frequency pool (ω ∈ {1, 2, 4} × dt ∈
   {0.05, 0.1, 0.2}, nine cells, fixed physical horizon), the
   coarse/fine degradation ratio at the highest frequency (24.2)
   exceeds the low-frequency ratio (0.05) by 2410% (pre-registered gate
   20%): frequency–grid interaction is real and concentrated in the
   single near-Nyquist cell (ω·dt = 0.8) — there the model cannot
   *learn* (training grid insufficient), not merely fails to be
   *measured* [B, PRD §19 round 162; PR#17 pending merge]. Practical
   safe domain ω·dt ≲ 0.4; cross-dt consistency claims (round 130) are
   conditional on grid resolution.

## 5 Experiments

**Protocol.** Same-pool comparisons; cross-pool results reported as
geometric means [G2]. Rollout error at the eval_ks ladder (composite-error
backing); VPT as a supplementary lens only (separation holds in a narrow
θ-window — downgraded to presentation norm, not a new verdict). Noise-free
simulation throughout (scope declaration, limitation 1). Infrastructure
disclosure: every experiment is a single-machine deterministic CPU run
(Apple M2 Max, macOS; per-experiment wall-clock in the minutes range), and
each archived result JSON carries meta(git_sha, device, timestamp)
provenance. Hidden-set
discipline: seed 999 retired after it caught a visible-set reversal
(prefix advantage flipped +29% on held-out); consumption is one-shot per
seed, descending from 998 — **no [C]-tier terminal claims are made in this
draft**. (Round 812 update: 998 has since been consumed by a pre-registered
one-shot migration check of the recipe-composition result and is retired —
ladder descends to 997; the reversal that check returned is reported in
Sec. 5 and Limitation 4f, and the draft still asserts no [C]-tier headline.)

| Row | Result (k=100 rollout MSE) | Metric | Uncertainty | Tier | Protocol / pointer |
|---|---|---|---|---|---|
| Classical LSQ-ω̂ / STLSQ (upper reference) | 2.7e-6 (ω̂ err 0.069%) | q-only | deterministic estimator, 768-traj pool (no seed axis) | [B] | classic-baseline-protocol.md |
| TSFM Chronos (zero-shot, q-only) | 1.229 | q-only | ±0.11 (3 data-pool seeds) | [B] | tsfm-baseline-protocol.md, three declarations |
| TSFM TimesFM (zero-shot) | 0.167 | q-only | ±0.09 (3 data-pool seeds) | [B] | D-2 addendum, round 92 |
| Structural arm prefix (n32) | 5.006 | q+p | ±0.76 (3 training seeds, traj stderr) | [B] | d1b same-pool |
| Structural arm all2all (n32) | 11.58 | q+p | ±4.37 (3 training seeds, traj stderr) | [B] | d1b same-pool |

Same-table scope (round 111 audit): all five rows are the M1 spring
family, noise-free, evaluated at k=100. The metric column is load-bearing:
q+p adds the momentum term, so structural-arm magnitudes carry ≈2x the
q-only scale by construction — cross-metric comparisons are within-row
only. The M2 field-task oracle bound (0.0148, do-not-rerun clause round 51)
is *not* same-table compatible (different task/dynamics) and is cited only
in the M2 mechanism claim.

**Reading.** Classical identification at 2.7e-6 is a *reference ceiling*,
not a competitor: in a noise-free linear regime the parametric method
should win, and it bounds what any learned claim can mean here [three
declarations]. TSFM zero-shot numbers are cross-category references under
pretraining-breadth vs small-sample-structure disparity. The structural
arm comparison (prefix vs all2all) is the in-family ablation axis.
[Resolved round 111: 结构臂与 TSFM/oracle 同表复核完成——M1 五行同表成立
(口径列+uncertainty 列已补);oracle 行经查属 M2 场任务,移出本表归 M2
机制句;判读锚 PRD §19 "BASELINE-SCOPE 判读"。]

**UQ.** Ensemble spread exists but is not calibration: coverage@95 measured
1.6% / 0 / 0 across seeds (D-1 judged negative — overconfidence direction);
seed-ensembles are mini deep-ensembles, not posterior coverage. Claims
capped at L2 (training-variance) tier.

**Training-regime audit ladder.** A pre-registered single-axis ladder
audits the default training configuration, one axis per probe, each with
a mechanical gate (spread ≥ 1.05 for resolvability ladders; ratio gates
for A/B probes); every number below is read off the result artifact
[ B, screening tier — 1-seed unless marked 3-seed; unlocks routing and
screening only, no terminal claims ]:

| Axis | Verdict | Artifact-verified reading |
|---|---|---|
| gradient noise scale | GNS_RESOLVED_TREND | B_simple 11.9 → 83.1 (peak at 1k steps), max/min ≈ 7.0; noise-dominated regime at batch 64 |
| sharpness | SHARP_BELOW | all λ_max·lr < 1.5 (classical stable regime throughout) |
| window repetition | REP_UNRESOLVABLE | rollout metric \|diff\| 1.6% < 5% gate (observation-caliber caveat) |
| dt curriculum | CURRICULUM_BENEFICIAL | curriculum better by 33.8% under constrained budget |
| curriculum order | ORDER_MATTERS | positive 0.42 vs reverse 5.91 (reverse 93% worse) |
| length extrapolation | LEN_ROBUST | rel. comp 0.88 beyond the training window; robust to 8–10× (0.78 extended) |
| pool width | WIDTH_COST | wide pool same-distribution penalty ratio 37.5 (caliber split; cross-pool numbers not comparable) |
| optimizer | OPT_SGD_BETTER | SGD-momentum generalizes 8.6% better; Adam's training advantage does not transfer |
| weight decay | WD_RESOLVED | interior optimum wd = 1e-4 (spread 1.18; default 0 not optimal) |
| depth | DEPTH_RESOLVED | monotonic to depth 4 (spread 1.94; default 2 not optimal) |
| depth × width | MATRIX_RESOLVED | main effects additive in log space (interaction ln 0.011) |
| training span | KSPAN_RESOLVED | interior best k_train = 4 (spread 1.9; default 8 not optimal) |
| scale count | NSCALES_RESOLVED | interior best n_scales = 2 (spread 1.56; default 4 not optimal) |
| lr schedule shape | LRDECAY_RESOLVED | interior best decay 0.999 (spread 1.18) |
| batch × lr scaling | SCALING_BROKEN | both pre-registered rules broken (linear 33%, sqrt 21%) |
| tail averaging | SWA_HARMFUL | tail average 8.0% worse (cross-basin averaging reading) |
| lr warmup | WARMUP_3S_BENEFICIAL | 3-seed ratio 0.856 but 1/3 seed consistency (seed-0-driven; the 44.2% single-seed reading downgraded to directional) |
| amplitude extrapolation | AMPEX_DEGRADES | rel. comp 4.08 ≥ 3 gate (linear invariance not inherited) |
| observation window | DEC_TRAIN_HARMFUL | t8 training at fixed-t24 eval 5.6× worse, 0/3 (evaluation-caliber artifact, dissolved) |
| context capacity | CTX2_REVERSED | ctx_dim = 1 ratio 1.11 at 3 seeds (reversal); axis stays at default 8 |
| recipe composition | RECIPE_SYNERGIC | single-axis optima compose to −10.7%, 3/3 consistent |
| trajectory length | GENLEN_CONFIRMED | 7th recipe-axis candidate upgraded to recommended, medium confidence (in-sample 2.96 → 2.70 seed-0-driven; out-of-sample new seeds {3,4,5}: direction 2/3, ratio 0.8738 = −12.6%, seed-4 split 0.045 marginal) |
| training-amount curve | SMOOTH_ASYMPTOTE (judged negative) | rollout-MSE curve smooth (max adjacent-step ratio 1.42 ≪ 3× gate); grokking naming not applicable in this regime |
| recipe composition × held-out seed | RECIPE_MIGRATION_REVERSED | one-shot seed 998: default 2.4269 vs five-axis composite 3.4910, ratio 1.438 — the visible-set 0.893 direction flips (hidden-set tier, migration judgment only) |
| recipe composition × horizon | HORIZON_ROBUST | ratio 0.893 / 0.834 / 0.825 at k = 100 / 200 / 400, direction-consistent 3/3 at each (the gain *grows* with horizon; composite arm's seed spread falls 1.54 → 1.03) |
| recipe composition × training budget | RECIPE_BUDGET_REVERSED | same arms at 8000 steps, 3 seeds: ratio 1.1157 (mean_A 2.3886 vs mean_B 2.6649), direction consistency 3/3 → 1/3, composite spread 1.727; no 8000-step historical sentinel (caliber caveat, kept honest) |

The ladder's decision logic is the point, not any single row: at least
three axes judge the default configuration non-optimal, which under the
value-exit rules forces a composition check rather than per-axis backfill
— the composition probe returned −10.7% (3/3), and the head-structure
axis (Sec. 6) then closed the question with an either-or result. Two
honest notes: the artifact of the curriculum-order probe carries the
mechanical branch label CURRICULUM_HARMFUL for the same data the
judgment named ORDER_MATTERS (reverse arm 93% worse — two descriptions,
one dataset); and warmup's 3-seed confirmation is consistency-1/3, so
its recipe candidacy carries a confidence annotation rather than a clean
win.

Axis-attribution follow-ups (rounds 434/440, PR#58/#59 pending merge)
sharpen the composition row: leave-one-out at 3 seeds shows depth
(removal degrades 18.9%, 3/3) and warmup (9.2%, 2/3) carry the composite,
while lr-decay/weight-decay/k-train are individually neutral — yet a
direct 3-seed comparison against a two-axis reduced composite fails the
trimming gate (ratio 1.062), and the reduced arm's per-seed spread (1.79
vs 1.54) indicates the neutral axes contribute training stability rather
than mean improvement. External mechanism studies point the same way —
warmup acts as implicit down-scaling of early updates (Kosson et al.,
NeurIPS 2024) and weight decay as the actual cross-width stabilizer
(Kosson et al., ICLR 2026) — though at GPT-pretraining scale, so we cite
them as mechanism-level concordance, not transfer evidence. The five-axis
composite therefore stands as the back-propagation candidate on a
four-probe evidence chain (composition, horizon robustness, LOO,
reduction), with the recipe-against-head interaction resolved separately
by the either-or result above.

**Hidden-set migration check of the composite (seed 998, one-shot;
round 812).** That candidate was then submitted to a pre-registered
held-out test before any further use: same probe, same pool and budget
(gen_spring, n_train 256 / n_eval 128, gen_steps 160, eval_k 100, dt 0.1,
ω ∈ [0.7, 1.8], t_obs 24, 2000 training steps), A = house default vs B =
the five-axis composite, run at unseen seed 998 exactly once. Decision
bands were frozen before execution (ratio < 0.95 = migration holds;
0.95–1.0 = direction kept, magnitude decays; ≥ 1.05 = reversal), and the
environment was anchored first by re-running seed 0 bitwise (A = 3.5582,
B = 3.3910 — identical to the visible-set run). The artifact fields read
A = 2.4269, B = 3.4910 → **ratio 1.438, RECIPE_MIGRATION_REVERSED** (the
probe's mechanical branch label is RECIPE_ANTAGONISTIC): the 10.7%
visible-set gain does not migrate, it inverts into a 43.8% degradation.
Both arms move relative to their visible-set means (default 2.43 below
2.96, composite 3.49 above 2.64), so the flip is not a common-mode shift
of the pool. Consequences, in the order the pre-registration permits: (i)
the five-axis composite is **not** promoted to the default configuration —
the recipe claim is scoped to "gain real on the visible seed set", and the
back-fill proposals built on it are closed out on this migration result;
(ii) no axis is blamed — attributing the reversal to a specific axis would
use a consumed held-out seed as a tuning signal, which the hidden-set
protocol forbids, so the conflict attribution is parked; (iii) with the
budget probe this closes the recipe family at six probes (composition,
horizon, leave-one-out, reduction, budget, migration). Methodologically
this is the second time a one-shot held-out run caught a visible-set
overfit in this study (seed 999 flipped the prefix advantage by +29%), and
it sits in the same lineage as the seed-0-driven dissolutions above
(warmup's 3-seed consistency of 1/3, the ctx-capacity reversal, the mixed
trajectory-length direction): at this scale, multi-seed agreement inside
one visible pool is a screening result, not a transfer result. Honest
boundary: a single hidden seed is one point, so the reading is used as a
migration signal and a scope annotation only — never as a terminal
headline, and never as evidence for a different recipe.

**Two more domain limits: horizon and budget (rounds 252/460).** The
composite's gain is not a scalar either. Same arms, three rollout
horizons (k = 100 / 200 / 400, three seeds, a second pool for the long
horizon): ratio 0.893 / 0.834 / 0.825 with direction consistency 3/3 at
each horizon, and the composite arm's seed spread contracting 1.54 → 1.03
— the benefit *grows* with horizon and buys stability as well as mean
error at long rollout (HORIZON_ROBUST, PR#45 pending merge). Same arms,
8000 training steps instead of 2000: ratio **1.1157** (mean_A 2.3886 vs
mean_B 2.6649), direction consistency falls 3/3 → 1/3, composite spread
1.727 — the gain reverses in the budget domain (RECIPE_BUDGET_REVERSED,
PR#60 pending merge), because the per-axis optima that make up the
composite were located at the 2000-step operating point and longer
training walks past them. Two caveats stay attached to that reading: the
8000-step regime has no historical bitwise sentinel of its own, so it is a
within-run paired comparison rather than an anchored one; and it is a
visible-seed-set measurement, so it carries the same seed-scope annotation
as the migration check above. Read jointly, the three probes fence one
claim from three sides: the five-axis composition is real **at a 2000-step
training budget, on the visible seed set, and it helps most where the
rollout horizon is long**; outside that box it is not merely weaker but of
opposite sign (budget) or opposite direction (held-out seed). Every recipe
recommendation in this paper therefore ships with its domain, and the
back-fill proposals built on the composite were scoped this way instead of
adopted as defaults. The reversal itself is an instance of a documented
phenomenon class rather than a house quirk: data-recipe rankings measured
at small compute are known to flip at larger scales (Goyal, Maini, Lipton
& Raghunathan, CVPR 2024 — data curation cannot be compute-agnostic), and
small-proxy-protocol rankings are documented as unreliable guides for
fully tuned large-scale runs (Wang et al., arXiv:2512.24503, ICLR 2026)
[B; both are LLM pre-training data-curation results — an analogous
phenomenon class for our synthetic-dynamics recipes, not a direct
replication].

Evaluation-protocol robustness (round 408 update): recomputing the same
weights at fp64 instead of the fp32 house caliber — both heads, both
anchor calibers (k=100 on the house pool, k=400 on the long-horizon
pool), three readouts (rollout MSE, final and max energy drift) — moves
every reading by at most 2.3e-6 relative, four orders of magnitude below
the 1.10 stability gate (ANCHOR-PRECISION, PRD §19 round 406, PR#57
pending merge; bitwise sentinels A=3.5582/B=2.0024 re-verified). The
pool-composition axis, by contrast, swings single-readout anchors by
1.3-1.9x (POOL-BITS, round 275, PR#53 pending merge). Evaluation
variance in this regime is therefore dominated by pool composition, not
floating-point precision — the basis on which the anchor protocol
requires per-anchor multi-variant spread annotations but no precision
variants. Scoped to single-machine deterministic CPU inference; the
multi-hardware/multi-precision serving regime is a different operating
point (scan §65, Yuan et al. 2025). Independently, a recent comparative
study across chaotic-system surrogate architectures reports that
integrator-like updates yield lower bias and perturbation amplification
and stabler long-horizon rollouts (Biswas, arXiv:2605.24868, 2026
preprint, scan §66.1) — external corroboration, under a shared
training protocol, of the structure-preserving thesis this paper
defends by construction.

## 6 Mechanism Analysis

**Inference gap (M1).** Why does the amortized context underuse the
available information? Chain, in evidence order: (i) the observation
window carries a t³-growing information budget with no plateau — the
window is not the bottleneck [B, D6]; (ii) capacity is not the bottleneck:
+46% parameters produce zero effect [B, E3]; (iii) the bottleneck is
optimization: gradient starvation at 3.97e-3 [B, E4a; Gradient Starvation
naming], with the amortization gap [Cremer et al., ICML 2018] as the named
frame. A spectral-bias candidate naming passed the four-question audit
with a pre-registered falsifiable prophecy; the prophecy test (per-mode
extraction scan, 1-seed T1 screening, PRD §19 round 122; PR#4) found no
decodable per-mode signal — flat — so it is carried only as a downgraded
weak hypothesis. We keep the full naming→prophecy→test→downgrade chain
visible as the falsification discipline this paper claims.

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

**Distribution shift separates the two stages.** Out-of-band ω pools
(training band ω ∈ [0.7, 1.8]; evaluation in / low-out / high-out bands)
decouple the two stages the architecture splits [B, PRD §19 round 115;
PR#2 pending merge]: the structural arm stays *absolutely dominant in
every band* — 0.77 / 7.53 / 2.65 vs the static counterpart's 2.33 /
9.76 / 5.90 (rollout MSE, ±stderr in the artifact) — while linear
decodability of ω from the inferred context code collapses to noise
level out-of-band (corr 0.38 in-band → −0.01 / 0.01 out-of-band). Two
honest qualifications: what breaks first under shift is the *inference*
stage, not the conserving rollout; and in relative terms the structural
arm's own low-band degradation ratio (9.8×) exceeds the static arm's
(4.2×) — absolute dominance and relative degradation point in opposite
directions here, so both axes are reported (the artifact's pre-registered
criterion "structure amplifies OOD risk" evaluates false).

**Few-shot adaptation lands in the same place.** On an unseen spring
task (c = 1.5, outside the pretraining corpus {0.8, 1.0, 1.2}), three
adaptation modes order strictly — pretrain-then-finetune 1.20e-2 <
from-scratch 1.34e-2 < amortized zero-shot prefix 5.82e-2 rollout MSE:
implicit in-context adaptation pays 4.9× over gradient fine-tuning
[B, PRD §19 round 132; PR#7 pending merge]. An interpolation control
(c = 1.1, inside the corpus) tightens the arms to near-parity (1.21e-2
/ 0.97e-2 / 1.03e-2; the zero-shot/fine-tune gap falls 4.9× → 1.25×)
— the gap is an extrapolation effect, not an adaptation-mechanism
deficit [B, round 134; PR#8 pending merge]: the out-of-distribution
weakness that the band-shift paragraph shows at the ω level reappears
at the task level.

**The two sides were paid for separately first (rounds 249/261).** Before
the chain that follows attributed the complete construction, two paired
probes injected one side at a time on the same pool, budget and 3-seed
protocol, and the two sides buy different things:

- **Analytic T alone** (`T = ½Σp²` with `dT/dp = p`, V still free) beats
  the free kinetic MLP in-distribution in 3/3 seeds — ratio 0.8604152214
  (2.9612487952 → 2.5479035378, −14.0%) — and degrades amplitude
  extrapolation at every seed (rel. comp 5.607083149 / 9.071356650 /
  11.128190930 against the default's 3.334158179 / 2.523428448 /
  3.489056819; medians 9.071 vs 3.334). On a task whose kinetic energy is
  known analytically the free T-MLP is pure variance in-distribution,
  while the analytic form delivers no extrapolation benefit: the
  amplitude gap is not in T [B, PRD §19 round 249; artifact
  `benchmarks/physics_out_v02/equiv_head/equiv_head.json`, git_sha
  11e32aa, sentinel default-arm seed0 3.5581917763 bitwise].
- **Homogeneous V alone** (both arms on the same analytic T; free V vs
  strictly degree-2 `V = ‖q‖²·s_θ(q̂, ctx)`) returns the mechanical
  verdict VHOM_NULL with 0/3 consistency, because the homogeneous arm is
  training-catastrophic in 2/3 seeds (2456.613037 and 701.840576 against
  2.778663874 / 2.555983782). The seed that does train carries the
  mechanism signal: rel. comp 1.442855937 at in-distribution parity
  (2.384193897 vs 2.309062958) — near-perfect scale-equivariant recovery
  where the identical non-homogeneous construction reads 9.071356650 at
  the same seed. The registered reading was revised from "V is not the
  carrier" to "the V-side benefit is real and blocked by parameterization
  training stability" (direction-normalized-input pathology, parked as a
  stability study) [B, round 261; artifact
  `benchmarks/physics_out_v02/v_hom/v_hom.json`, git_sha 5215a97,
  sentinel = the round-249 analytic-T arm re-anchored bitwise at
  2.7786638737].

Read against each other, neither single side is the construction the chain
measures. The T side buys in-distribution accuracy and costs
extrapolation; the V side buys extrapolation recovery only when it
survives training. The dominance reported next belongs to the conjunction
— analytic T, homogeneous V, and the direction-channel repair that makes
the latter trainable — which is why the replacement candidate is
registered as the complete head (AMM-033) and no single-side adoption
claim is made anywhere in this draft.

**Closing the third question: which channel carries the rest (round 244).**
With T ruled out as the extrapolation carrier and V's homogeneity shown
to be the right-but-unstable lever, the pre-registered AMP-ATTR
decomposition asked where the amplitude bias actually sits on the *house
default* head. Two channels are separated by construction: holding the
context fixed and comparing `rollout(s·s₀)` against `s·rollout(s₀)`
isolates the dynamics head's scale-equivariance violation, while
`ctx(s·prefix)` against `ctx(prefix)` isolates the inference channel's
non-invariance; for a linear system both ideals are zero. The head
channel is the larger carrier — median relative equivariance error
1.3622821050 at s = 2 and 2.8378283895 at s = 4, against context
non-invariance 0.4166634232 and 1.2239125967 — and the ordering holds in
3/3 seeds at both scale factors. This upgrades the mechanism sentence
from "the inference and potential channels jointly carry the nonlinear
bias" to a measured share: the head carries the larger part, the context
a smaller but not negligible one. Three qualifications travel with the
number. It is a *share*, not an exclusivity claim — both channels are
O(1) against the ideal zero, so neither is exempt; the probe is
report-type by pre-registration (relative RMS calibers, no fail gate, the
residual-spectral precedent), so no threshold was crossed to call the head
primary; and the gap narrows with scale (the context channel grows ×2.94
from s = 2 to s = 4 against the head's ×2.08; at the largest seed/scale
combination they read 1.8711150885 and 2.9164962155), so the shares are
quoted per scale factor rather than collapsed into one ratio. The
attribution is also anchored to the construction it describes: this
probe's training arm reproduces the default head's per-seed rollout MSEs
bitwise — 3.5581917763, 2.6058924198, 2.7196621895, the same three values
as round 249's default arm — which is what licenses reading it as a
property of the head that the chain below then repairs [B, PRD §19 round
244; artifact `benchmarks/physics_out_v02/amp_attr/amp_attr.json`, git_sha
b1fd910, exec_tier T1].

**Head structure (M1) — what the free function form costs.** A
seven-probe chain (same-pool paired arms, 3 seeds, every cell carrying a
bitwise cross-run anchor) measures the structured head of Sec. 3 against
the free-form default [B; PRD §19 rounds 268–279, verdict rows on the
dir branches pending merge via PRs #49–#55 — all numbers below
re-verified against the result artifacts]:

- **Repair.** The naive homogeneous parameterization is
  training-catastrophic (2/3 seeds). Zeroing the direction channel
  repairs it — 0/3 catastrophic, mean rollout MSE 1.949 vs the free-V
  baseline 2.548 (≈23% in-distribution gain at equal budget) — and
  unlocks the extrapolation benefit in 3/3 seeds (median rel. comp
  1.705 < gate 3; the un-repaired construction delivered it in 1/3).
- **Dominance.** The complete construction beats the house default head
  on both axes in 3/3 seeds: in-distribution ratio 0.658 (−34%),
  extrapolation median −49% (1.705 vs 3.334). It is registered as the
  default-M1 replacement candidate (proposal AMM-033; implementation
  rides the PR merge).
- **The boundary is the degree axis.** On a quartic pool
  (H = p²/2 + q⁴/4), the degree-matched homogeneous V reaches 4.4e-5
  rollout MSE vs 0.157 for free V (≈3500×, near-perfect recovery with
  conservation intact), while the mis-set quadratic form pays 7.56×
  (1.184). The free function form is not free — it is insurance against
  a mis-specified degree, and the premium is measurable.
- **Robustness.** The candidate dominates at every horizon tested
  (k ∈ {100, 400, 1000}): MSE ratio 0.62 / 0.82 / 0.87 and energy-drift
  ratio 0.16 / 0.17 / 0.30, its drift stable at ≈0.14 across horizons.
- **Absorbed composition.** A 2×2 grid (training recipe {off, on} ×
  head {default, candidate}; three cells anchored bitwise to historical
  runs) is sub-additive: candidate head alone 1.949 < +recipe 2.241 <
  recipe alone 2.645 < default 2.961. The recipe absorbs the head's
  gain; adoption is either-or, not stacked. Scope note: the recipe arm in
  this grid is the visible-set five-axis composite, whose own gain does
  not migrate to held-out seed 998 (Sec. 5, Limitation 4f) — the grid is
  therefore a within-visible-pool interaction statement, not a claim
  about the interaction under an unseen pool draw. The recipe arm is also
  budget-scoped: the composite it uses reverses at 8000 training steps
  (Sec. 5, Limitation 4f), so the "recipe off/on" axis of this grid is
  defined at the 2000-step operating point.
- **Negative results, kept.** At n = 64 training trajectories the
  advantage vanishes (ratio 0.99) and one grid unit diverges (candidate
  arm, n = 128, seed 0; 1/18 units) — the dominance is a full-data
  (n = 256) phenomenon. And under bit-level pool perturbation (same
  draws, tensor length 160/300/600/1100) the cross-run anchors of
  *both* heads are fragile (median spread 1.86 default vs 1.29
  candidate, both above the 1.10 stability gate): anchor reproducibility
  needs a multi-variant protocol, registered into the anchor-reset plan.

The chain's shape is the claim: a structural injection at the head pays
where its single parameter (the degree) is matched to the true
functional form, and every direction in which it does not pay is
measured and reported in the same breath.

## 7 Honest Limitations

1. **Noise-free simulation.** All results are in the noise-free regime
   (code-audit confirmed); no noisy-domain claim is made.
2. **UQ ceiling.** Uncertainty is L2 (training variance) at best;
   coverage is not achieved (1.6%/0/0); no posterior claim.
3. **M2 closed.** Field-reconstruction headroom is closed with an
   all-negative evidence chain; we do not promise it back.
4. **Conservation ≠ time-reversal.** T-symmetry is an independent
   property (T-non-even finding); the R1b relaxation path exists as a
   conditional registration. The T-even hatch is locally validated
   [B, 1-seed screening; PRD §19 round 120]: on the spring family (equal
   budget, same pool) the free-T head's flip-and-retrace closure degrades
   with horizon (5.6e-3 at k=200, q+p口径) while the T-even-parameterized
   head stays at the float floor (5.8e-12) REGARDLESS of fit quality — a
   9.7e8x gap; a single-frequency control puts both arms in the fit
   regime and shows the even constraint costs nothing in-distribution
   (B/A forward 0.078, i.e. a 12.8x gain). Multi-seed finals remain
   parked.
4b. **Seed-level sign instability of the prefix advantage.** The
   prefix-over-all2all advantage reverses for ~1/3 of seeds; located by a
   diagnostic probe [B, 1-seed x 8, PRD §19 round 126; PR#5]: flips are
   heterogeneous — majority basin-stable at 2x budget with comparable
   training losses (equivalent-solution signature; sign-symmetry basins,
   Lubana et al. ICML 2023), minority transient. Reported as a property of
   the training axis, not averaged away.
4c. **Two-timescale boundary (budget-attributed).** On the elastic
   pendulum family (10x timescale separation, directly representable by
   the separable head) trained at an analytically resolving dt, the fast
   mode is captured — short-horizon rel MSE 0.26% at 4x budget vs the 1%
   gate (3.2% and failing at the round-137 budget) — while the
   slow-exchange envelope over T=40 (~6.4 slow periods) stays above its
   10% gate: 22% at 4x budget, a 5.4x improvement from the 122%
   baseline but not through the gate. Two-arm attribution
   (hidden128+40k vs hidden64+40k, shared pool/gates/seed) classifies
   this BUDGET_DOMINANT — an optimization limit, not a structural floor
   (§33.2 stiffness signature rejected); capacity contributes a factor
   2 on the slow axis (0.224 vs 0.439) as a secondary effect [B, 1-seed
   screening; PRD §19 rounds 137/143; PR#9/#10]. Scope: the structure-by-
   construction claims cover single-timescale families; two-timescale
   long-horizon slow exchange is not usable in this training regime,
   and the budget needed to bring the slow axis through its gate is
   untested (parked as a T2/T3 direction). Multi-seed finals remain
   parked.
4d. **Head-structure scope (homogeneous family).** The Sec. 6 dominance
   chain is a house-scale, spring-family, full-data result: at n = 64
   training trajectories the advantage is absent (ratio 0.99, 1/18 grid
   units diverged in the candidate arm) [B, PRD §19 round 277], so the
   benefit scope is annotated conservatively — no small-sample or
   cross-potential extrapolation (degree matching is per-family by
   construction). Cross-run anchor reproducibility under pool
   perturbation is fragile for both heads (round 275); the anchor-reset
   plan adopts a multi-variant spread-annotated protocol. The
   default-head replacement itself is a registered proposal awaiting PR
   merge (AMM-033), not an applied change; multi-seed finals remain
   parked.
   *Addendum (round 818, single-side attribution):* the two structural
   sides were also measured separately (Sec. 6, rounds 249/261), and that
   evidence tightens the scope rather than loosening it — analytic T alone
   worsens amplitude extrapolation in 3/3 seeds, and homogeneous V alone
   trains in only 1/3. The homogeneous-V stability blocker
   (direction-normalized input, parked as a T2 stability study) is
   therefore a live prerequisite of the candidate, not a cosmetic
   parameterization detail; no single-side variant is proposed for
   adoption.
4e. **Band-limited context inference.** Context inference claims are
   in-band claims: trained on ω ∈ [0.7, 1.8], out-of-band rollout
   degrades up to 9.8× on the relative axis even though the structural
   arm remains absolutely dominant in every band — and on that same
   relative axis the structural arm's degradation (9.8×) *exceeds* the
   static control's (4.2×), so dominance and degradation-ratio point
   in opposite directions and both are reported; linear decodability
   of ω from the context code is noise-level out-of-band [B, PRD §19
   round 115; PR#2 pending merge]. No out-of-band inference claim is
   made.
4f. **Recipe-composition gain is visible-set-scoped (held-out reversal
   measured).** The strongest training-recipe result in this paper — the
   five-axis composite, −10.7% rollout MSE with all three visible seeds
   agreeing (ratio 0.893) — was submitted to a pre-registered one-shot
   held-out run at unseen seed 998 and reversed: default 2.4269 vs
   composite 3.4910, ratio 1.438 (RECIPE_MIGRATION_REVERSED; probe's
   mechanical label RECIPE_ANTAGONISTIC). Consequences as registered: the
   composite is not promoted to the default configuration; the reversal
   is reported as a migration judgment only, with axis-level conflict
   attribution deliberately parked, because tuning on a consumed hidden
   seed would destroy the very held-out that made the check meaningful;
   and the recipe evidence family is closed at six probes. What this
   limitation does *not* say: it does not retract the per-axis
   measurements (depth, warmup, weight decay, lr-decay, k_train all keep
   their own artifact-verified verdicts) and it does not touch the
   head-structure result, whose dominance is a different axis and was
   measured at 3 seeds against a different baseline [B, PRD §19 rounds
   268–279]. Read together with the seed-999 prefix reversal (Limitation
   4b), the honest generalization is structural: at house scale, seed-axis
   transfer is the dominant unmodeled variance source for *training-recipe
   and comparison* claims, and cross-seed agreement within one visible
   pool is screening evidence — a scope annotation this draft now carries
   on every recipe row. Multi-seed held-out replication of the migration
   check is a compute-gated direction (T2/T3, parked), not an assertion
   here. The same scope discipline now covers the other two domains of
   that gain: it *grows* with rollout horizon (ratio 0.893 / 0.834 / 0.825
   at k = 100 / 200 / 400, direction-consistent 3/3 at each) but reverses
   in the training-budget domain (8000 steps instead of 2000: ratio
   1.1157, direction consistency 3/3 → 1/3, composite seed spread 1.727,
   and no historical bitwise sentinel at that budget — a within-run paired
   reading). The recipe claims in this paper are therefore a three-sided
   domain statement — 2000-step budget × visible seed set ×
   horizon-robustness — not a default-configuration recommendation. The
   reversal phenomenon class itself is externally corroborated: recipe
   rankings flipping across compute scales is documented in LLM
   pre-training data curation (Goyal et al., CVPR 2024; Wang et al.,
   arXiv:2512.24503, ICLR 2026) [B; analogous phenomenon class, different
   domain — synthetic-dynamics recipes here, data curation there].
4g. **Channel-attribution shares are report-only.** The Sec. 6 statement
   that the dynamics head carries the larger share of the amplitude
   extrapolation bias (1.362 / 2.838 vs context 0.417 / 1.224 at
   s = 2 / 4) comes from a probe pre-registered as *report-type*: the
   calibers are relative RMS values with no pass/fail gate, the primary
   carrier is decided by which channel is larger, and both channels sit
   at O(1) against the ideal of zero. So the reading licenses
   "head-first, context-secondary" and forbids "the context channel is
   clean" — and it is a 3-seed T1 measurement on the house default head
   at house scale, not a decomposition of the repaired candidate head
   (whose scale covariance is by construction enforced on the V side and
   was measured only through the outcome axis, rel. comp). Multi-seed
   held-out replication of the decomposition is compute-gated and parked
   with the other T2/T3 directions [B, PRD §19 round 244; artifact
   `benchmarks/physics_out_v02/amp_attr/amp_attr.json`].
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
architecture cannot do. We also let the held-out protocol judge our own
strongest training-recipe result and printed the answer rather than the
wish: the five-axis composite's 10.7% gain reversed on unseen seed 998
(ratio 0.893 → 1.438), so the recipe stays scoped to the visible seed set
and the default configuration is not changed on its behalf. That check is
the third piece of audit apparatus in this paper, after pre-registered
gates and artifact-level re-verification of every quoted number. Future
work menu: discovery-lineage upstream
(SINDy / AI Poincaré / LieGAN) to propose the injected structure;
noise-injection line; SSM control baselines (pre-registered per the TSFM
precedent when scheduled); shadow-Hamiltonian monitoring upgrade (Skeel
reading); post-hoc symbolization; P-CfC gating; higher-order composition
for long horizons; multi-seed held-out replication of the recipe-family
migration check (compute-gated, T2/T3).

## Appendix A: Claim Tier Ledger

| Tier | Meaning | Items in this draft |
|---|---|---|
| [A] | By construction (closed form) | conservation at integrator level; mean-field identity (algebraic) |
| [B] | Local T1/T2 measurement, deterministic CPU, reproducible | all tables/orders/drifts above |
| [C] | Terminal claim — requires T3 or hidden-set (998, one-shot) | **none asserted**; required for: any noisy-domain claim, chaos-domain conservation, cross-domain transfer, final headline numbers. Addendum (round 812): the recipe-composition migration check was run one-shot at 998 and returned *negative on transfer* (0.893 → 1.438); the draft uses it as a scope annotation on the recipe rows, not as an asserted [C]-tier headline |

Hidden-set ledger: 999 consumed (round 44; H1 ✓ mechanism migrated / H2 ✗
advantage reversed — the reversal that anchored the discipline), 998
retained. [v0-TODO: 终稿前如需 [C] 级声明,预注册 998 一次性终跑清单。]
*Ledger updated round 814:* 998 is no longer retained — it was consumed as
scheduled by RECIPE-MIGRATION (pre-registered bands frozen before
execution, seed-0 bitwise re-anchor first, one-shot by construction;
artifact `benchmarks/physics_out_v02/hidden_final/recipe_synthesis.json`,
meta `exec_tier=T1`, `git_sha=354c134`) and 998 is retired; the descending
held-out ladder now starts at **997**. Both consumed seeds produced the
same class of finding — a visible-set comparison failing to migrate (999:
prefix advantage +29% reversed; 998: recipe composite −10.7% reversed to
+43.8%) — which is why every recipe/comparison row above carries its
seed-set scope inline. The outstanding [v0-TODO] is narrowed accordingly:
if a [C]-tier claim is ever wanted, it must be pre-registered against 997
or later with a fresh one-shot budget, and the recipe-composition line is
closed without such a claim.

---

*Draft provenance: round 107, T0, assets from docs/n1-asset-index.md
(25-family distillation, traceability 100% A-grade entry-level); all
pointers resolve into docs/scan-conditioning.md, docs/PRD.md §19, and the
protocol documents listed per row. Updated round 110: escape-hatch
nonseparable validation added to Limitations 5 (T1 probe, PRD §19).
Updated round 120: T-even escape-hatch validation added to Limitations 4
(T1 probe + single-frequency control, PRD §19). Updated round 123:
spectral-bias naming downgraded to weak hypothesis in Mechanism Analysis
(prophecy test NEGATIVE, PR#4, PRD §19 round 122). Updated round 127:
seed-level sign instability added to Limitations 4b (diagnostic probe,
PR#5, PRD §19 round 126). Updated round 130: dt-transfer qualifier for
the "learned H" claim (FLOW_LIKE, PR#6, PRD §19 round 129). Updated
round 144: two-timescale boundary added to Limitations 4c WITH budget
attribution (FASTSLOW-PROBE round 137 + FASTSLOW-2 round 143, PR#9/#10,
PRD §19) — a round-137 provenance note pre-announced this entry as
"round 138" but the Limitations body had been left to a digest round
that was redirected; the dangling announcement is fixed here per the
round-111 carrier-layer rule (announcement and body now agree). Updated
round 285: head-structure axis chain added (Abstract, Contribution
3(iii), Sec. 3 head-structure axis, Sec. 6 head-structure subsection,
Limitations 4d) from PRD §19 rounds 268–279 dir-branch verdict rows
(PR#49–#55, pending merge) plus round 283 SPEC3 closure of the residual
line (PR#56, AMM-031 downgraded to reference-only); per the round-111
rule every number was re-verified against the result artifacts, which
caught two prose-arithmetic slips in the dir-branch verdict rows (round
268 "mean 1.957" — artifact mean 1.949; round 273 default-head drift
"[0.294, 1.626, 0.313]" — artifact per-horizon means [0.93, 0.82,
0.48]); this draft cites artifact-verified fields, history rows are not
rewritten, and correction notes ride the merge. Updated round 286:
distribution-shift separation added (Sec. 6 paragraph + Limitations
4e) from the ω out-of-band extrapolation asset (PRD §19 round 115,
PR#2 pending merge; numbers re-verified against the result artifact) —
an asset-index entry registered since round 115 that no prior writing
round had absorbed; the writing-round gap scan (asset-index entries vs
draft coverage) is now part of the ladder's N1 line. Updated round 287:
training-grid resolution clause added to Sec. 4 item 4 (SPECTRAL-DT,
PRD §19 round 162, PR#17 pending merge; 2410% interaction excess
re-verified against the artifact) — the write-in promised by that
round's verdict row. Updated round 288: training-regime audit ladder
added to Sec. 5 (22 axes, every reading extracted from its result
artifact; label divergence on the curriculum-order probe recorded
in-table); the ladder is the evidence base for the forced-composition
rule (≥3 axes judge the default non-optimal → composition probe
−10.7% → either-or head result). Updated round 289: few-shot
adaptation paragraph added to Sec. 6 (ICL-M3 round 132 + interpolation
control round 134, PRs #7/#8 pending merge; three-arm orderings
re-verified against the artifacts) and the training-amount negative
result added as a ladder row (grok_curve SMOOTH_ASYMPTOTE, max ratio
1.42). Updated round 290: the round-130 provenance line below claimed a
dt-transfer qualifier that the body did not actually carry (the
round-144 dangling-announcement pattern, caught by the round-286 gap
scan); the body now carries it — Sec. 3 "What is learned" (MAP-VS-FLOW,
PRD §19 round 129, PR#6 pending merge; cross-dt ratio 0.895 / slope
1.995 and the native-reference 13–16× reading re-verified against the
artifact) — and announcement and body agree. Updated round 297:
Related Work "Enforcing versus discovering structure" paragraph added
from scan §64 (Polyakov homogeneous ANN / symmetry-enforcement
precedent group SCNN–Dierkes–CHNN–Celledoni / Noether Networks as the
unknown-structure middle path); the paper's head-structure claim is
confined to the known-structure case, matching Sec. 6's measured
boundary. Updated round 408: Sec. 5 evaluation-protocol robustness
paragraph added from ANCHOR-PRECISION round 406 (precision axis
<=2.3e-6 vs pool-composition axis 1.3-1.9x; both artifacts
re-verified; scoped to single-machine deterministic CPU inference).
Updated round 414: the Sec. 5 robustness paragraph gains the Biswas
2026 comparative-study corroboration (scan §66.1, verified preprint).
Updated round 444: the Sec. 5 recipe-ladder paragraph gains the
axis-attribution follow-ups (LOO rounds 434 + direct reduction
comparison round 440, PRs #58/#59 pending merge; five-axis candidate
upheld on a four-probe chain) and the Kosson et al. mechanism-level
corroboration (scan §68, NeurIPS 2024 / ICLR 2026, scope-annotated).
Updated round 814 (queue entry N1-HIDDEN-REV; first beat of a new
iteration, distillation gate cleared): the seed-998 hidden migration check
is absorbed into the Abstract, Sec. 5 (ladder row + a "Hidden-set
migration check of the composite" paragraph), Sec. 6 (scope note on the
absorbed-composition bullet), Limitation 4f, Sec. 8 (conclusion sentence +
a compute-gated future-work item) and Appendix A ([C] row addendum +
hidden-set ledger: 998 consumed and retired, next held-out seed 997) —
source = PRD §19 round 812; per the round-111 rule every quoted reading
was re-verified against the result artifacts rather than the prose, i.e.
visible set `benchmarks/physics_out_v02/recipe_synthesis/recipe_synthesis.json`
(ratio 0.8931607635, mean_A 2.9612487952, mean_B 2.6448712349, direction
3/3, A seed0 3.5581917762 = house sentinel) and hidden set
`benchmarks/physics_out_v02/hidden_final/recipe_synthesis.json` (A
2.4269325733, B 3.4910252094, ratio 1.4384516685, mechanical verdict
RECIPE_ANTAGONISTIC, meta git_sha 354c134 / exec_tier T1); no existing
draft content was removed — all additions are additive and the two
now-stale pointers ("998 retained", the 998 [v0-TODO]) are corrected by
appended addenda rather than deletion. Updated round 816 (queue entry
N1-RECIPE-SCOPE, second writing iteration of this segment; distillation
gate cleared with pool items only — PLAYBOOK 轮 111 artifact-field
recompute + 轮 465 same-domain cross-check + scan §72.2 pre-registration):
the composite's two remaining domain limits are absorbed (Abstract budget
clause, Sec. 5 two new ladder rows + a "Two more domain limits: horizon
and budget" paragraph, Sec. 6 absorbed-composition budget qualifier,
Limitation 4f three-sided domain statement), readings taken from the
artifacts rather than the prose — `benchmarks/physics_out_v02/recipe_horizon/recipe_horizon.json`
(HORIZON_ROBUST, ratios 0.8931607635 / 0.8339268819 / 0.8247211326 at
k = 100/200/400, direction 3/3 per horizon, spread_B 1.5377 → 1.0346,
git_sha 1a4af63) and `benchmarks/physics_out_v02/recipe_budget/recipe_budget.json`
(RECIPE_BUDGET_REVERSED, ratio 1.1156959228, mean_A 2.3885671298,
mean_B 2.6649146080, direction_consistency 1/3, spread_B 1.7274477275,
train_steps 8000, exec_tier T1, git_sha 239c54b); asset-index entry 4e
registered in the same heartbeat per the round-814 rule; nothing removed.*

*Updated round 818 (queue entry N1-HEAD-SIDES, third writing iteration of
this segment; distillation gate cleared with pool items only — PLAYBOOK
轮 111 artifact-field recompute + 轮 465 same-domain cross-check + scan
§72.2): the two single-side head-structure injections are absorbed as
attribution boundaries for the Sec. 6 dominance claim (new Sec. 6
paragraph "The two sides were paid for separately first" + Limitations 4d
addendum), readings taken from the artifacts —
`benchmarks/physics_out_v02/equiv_head/equiv_head.json` (EQUIV_TRADEOFF,
ratio 0.8604152214, mean_A 2.9612487952 / mean_B 2.5479035378,
rel_comp_B 5.607083149 / 9.071356650 / 11.128190930 vs rel_comp_A
3.334158179 / 2.523428448 / 3.489056819, consistent 3, git_sha 11e32aa)
and `benchmarks/physics_out_v02/v_hom/v_hom.json` (VHOM_NULL, consistent
0, mses_B 2456.613037 / 2.384193897 / 701.840576, rel_comp_B seed1
1.442855937 against rel_comp_A seed1 9.071356650, sentinel
A_seed0_round249B bitwise true at 2.7786638737, git_sha 5215a97);
asset-index entry 4f registered in the same heartbeat. Nothing removed.*

*Updated round 820 (queue entry N1-AMPATTR-SHARE, fourth writing
iteration of this segment; distillation gate cleared with pool items only
— PLAYBOOK 轮 111 artifact-field recompute + 轮 819 三判口径[该读数即由
宽池清点浮出] + scan §72.2 report-type 预注册披露): the third attribution
question is closed with measured shares (new Sec. 6 paragraph "Closing the
third question: which channel carries the rest" + new Limitations 4g),
readings taken from the artifact —
`benchmarks/physics_out_v02/amp_attr/amp_attr.json` (AMPATTR_OK,
primary_carrier head, head-equivariance medians 1.3622821050 /
2.8378283895 at s = 2/4 vs context non-invariance 0.4166634232 /
1.2239125967, ordering 3/3 seeds at both scales, per-seed head values
1.3622821050 / 1.6007063861 / 1.0203475843 and context medians
0.4166634232 / 0.3900730759 / 0.5502080023 at s = 2, training-arm per-seed
rollout MSE 3.5581917763 / 2.6058924198 / 2.7196621895 bitwise equal to
round 249's default arm, caliber "relative RMS, report-only", git_sha
b1fd910, exec_tier T1); asset-index entry 4g registered in the same
heartbeat. Nothing removed.*
