# Start-State Distribution Mismatch in Semigroup-Trained Hamiltonian Models

> **论文骨架 / 写作底稿**(wave-10 夜间循环 N1 轮产出,2026-09-17)。
> 全部数字可溯源至 `benchmarks/physics_out_v02/` 各产物目录与 PRD §19;
> 相关工作定位基于 2026-09-17 文献扫描(query 清单见 PRD §19 轮 15)。
> 状态:**骨架**——叙事已定,待补图表与 Related Work 全文。

## Abstract(sketch)

Training recurrence-based dynamics models on arbitrary (start, span) pairs
within trajectories — *semigroup training* — dramatically improves
multi-step rollout accuracy in the many-sample regime (61–90% over
fixed-window prefix training, waves 5–7), and we recently confirmed its
sample-efficiency form: it opens accuracy levels the prefix loop never
reaches. In the *small-sample* regime (n<128), however, semigroup training
is *worse* than prefix training. We attribute this disadvantage to a
**start-state distribution mismatch**: semigroup sampling draws rollout
starts from random interior times, while deployment/evaluation rolls out
from the last observed state. Three interventions — pinning starts to the
endpoint, windowed endpoint-neighbourhood mixing, and a two-stage
semigroup→prefix curriculum — all fail to repair the one-step endpoint gap;
the curriculum trades 27% of the large-sample advantage for a partial
small-sample mid-horizon repair. We conclude the advantage and the
disadvantage are **same-sourced**: the any-time-pair property that wins at
scale is what dilutes deployment-start precision, and endpoint precision is
not purchasable by training recipes.

## 1. Setup

- Architecture: liquid (LTC) core infers a context from a t_obs prefix →
  Hamiltonian head H(q,p|ctx) rolled out by a symplectic integrator
  (energy conserved by construction). Task: spring family with hidden
  stiffness ω ∈ [0.7, 1.8] (the home task of liquid system-ID).
- Loops: *prefix* (v0.1: fixed-window, k_train-step rollout from the
  endpoint) vs *all2all* (semigroup: random interior (t_i, t_j) pairs).
  Identical model, optimizer budget, data pools; only the loop differs.
- Artifacts: `sample_efficiency_eval.py` (+ `--probe_context`,
  `--eval_ks`, `--start_probe`, `--two_stage`), CPU-deterministic, all
  result JSONs carry `meta(git_sha, device, ts)` provenance.

## 2. Attribution chain (each step preregistered)

| # | Hypothesis | Probe | Verdict | Artifact |
|---|---|---|---|---|
| D1 | disadvantage = system-ID quality | linear probe ω̂ decode from context | **refuted** — all2all decodes ω *better* (corr 0.34 vs 0.21; rel-err lower in 5/6 pairs) | `d1_small_n/` |
| D1b | disadvantage = eval-horizon mismatch | eval_k ∈ {1,10,100} ladder | **refuted** — gap present at k=1 (6/6 seeds; 1.44–3.27x), non-monotone in depth | `d1b_eval_depth/` |
| D1c | disadvantage = start-state distribution | 1-step MSE from interior true states (all2all's training starts), conditioning fixed | **confirmed** — endpoint→interior ratio shrinks 6/6 seeds, 4/6 reverse (n=32: 3.27x→1.25x; n=64: 1.44x→0.70x) | `d1c_start_probe/` |

## 3. Repair attempts (all preregistered, all honest)

| # | Recipe | Result | Artifact |
|---|---|---|---|
| D1d | pin 50% of starts to the endpoint | endpoint k1 ratio **worse** (3.27→3.76x; 5/6 seed-pairs) — single-time pinning halves sampling diversity | `d1d_start_mix/` |
| D1e | windowed neighbourhood (w=8) | gate failed (n=64 2.09x vs 1.28x line) — same as D1d | (screening, PRD §19 r6) |
| D1f | two-stage curriculum (semigroup 80% → prefix 20%) | **tradeoff**: endpoint k1 still 1.75x; small-n k100 repaired (n=32: 0.66x vs prefix; n=64: 0.90x); large-n k100 advantage −27% vs pure semigroup (still 2.1x vs prefix) | `d1f_two_stage/` |

## 4. Reading

1. The disadvantage is *not* identification quality (the context is *more*
   informative under semigroup training) and *not* horizon mismatch — it is
   the **context→one-step-dynamics map at the deployment start**, a start
   state all2all almost never trains from and prefix always does.
2. Mixing/cannot-fix results indicate the mechanism needs endpoint-
   *neighbourhood diversity in function space*, not endpoint exposure —
   naively reweighting dilutes the diversity that makes semigroup win.
3. Practical guidance: in the small-sample regime either (a) accept prefix
   (its objective is deployment-aligned), or (b) two-stage *if* mid-horizon
   small-sample accuracy matters more than 27% of large-sample advantage.
   Endpoint 1-step precision remains unpurchasable.

## 5. Related work (scan 2026-09-17)

- **MBRL distribution shift**: compounding rollout error from OOD start
  states is the core MBRL pathology; remedies = DAgger-style correction,
  adaptive rollout horizons, uncertainty penalisation. None combined with
  Hamiltonian hard-constraint architectures or system-ID contexts.
- **HNN literature**: no curriculum or start-state-distribution work found
  (Greydanus 2019; Zhong 2021 benchmark; energy-consistent operators 2025).
- **Two-phase PIML**: rich in PINN/PDE-residual soft-constraint land
  (DP-PINN, PIFT); absent for hard-constraint training-loop curricula.
- **CfC** (Hasani et al., Nature MI 2022): closed-form LTC — time-explicit
  form suggests an *analytic* treatment of the start-point mismatch
  (future work).

## 6. Open questions

- Cross-task: does the start-mismatch mechanism transfer to the M2 c(x)
  field family (32-dim hidden parameter)?
- Uncertainty-adaptive start sampling (vs fixed mixing) — untested.
- Analytic start-dependence under CfC-style closed forms.

## Artifact index (commits, wave-10 night 2026-09-16/17)

`d1_small_n` 34f9857→301e19c · `d1b_eval_depth` 5521942 ·
`d1c_start_probe` b54a08a · `d1d_start_mix` fa78fa9 · `d1f_two_stage`
cd57393 · probe/recipe code `--probe_context/--eval_ks/--start_probe/
--start_mix/--two_stage` · branch `wave/loop` (fork)
