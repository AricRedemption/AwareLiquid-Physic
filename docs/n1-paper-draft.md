# N1 Paper Draft v0(轮 107 起草;T0 零算力)

> **治理注记(中文,投稿前删除)**:本稿为循环自主起草的 v0 初稿
> (AMM-022 提案授权范围:初稿/迭代可自主,终稿/投稿/venue/署名待人决)。
> 所有数字严格取自 `docs/n1-asset-index.md`(溯源:条目级主锚 100% A 级,
> docs/scan-traceability-audit.md);索引未覆盖的细节以 `[v0-TODO]` 显式
> 留缺,不编造。轮 285 起每个引用数字回溯**产物 JSON 字段**复算一次
> (轮 111 条款);判读行散文聚合值与产物字段不符时以产物为准(轮 285
> 对账抓出两处,见溯源 footer 注记),历史判定行不改。证据分级见附录 A:`[A]`=构造保证(闭式)、`[B]`=本机
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
relaxation, nonseparable head).

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
simulation throughout (scope declaration, limitation 1). Hidden-set
discipline: seed 999 retired after it caught a visible-set reversal
(prefix advantage flipped +29% on held-out); consumption is one-shot per
seed, descending from 998 — **no [C]-tier terminal claims are made in this
draft**.

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
| trajectory length | GENLEN_RESOLVED | 7th recipe-axis candidate (2.96 → 2.70; per-seed direction mixed, seed-0-driven) |

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
  gain; adoption is either-or, not stacked.
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
−10.7% → either-or head result).*
