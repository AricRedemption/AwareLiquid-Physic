# PR-BRIEFING.md — 合并债简报(轮 294 产出,阶梯⑤合并债治理)

> 用途:56 个在途 PR 的人工合并操作手册。逐 PR 判读详情唯一源=
> `GOALS.md` goal_queue 各条目 status 字段(AMM-021 不复制);
> 本文件只承载合并顺序、冲突解法与族分组速览。
> 产出后每次批量合并前后各跑一次 `./scripts/goal_check`(自动弹出)。

## 1. 盘点(2026-09-26 实测,gh --repo AricRedemption/AwareLiquid-Physic)

- **56 个 open PR**(#1-#56),全部 `dir/<slug>` → `wave/loop`,fork 上。
- 54 条有 GOALS 队列条目(pr-pending,合并落地后 check_cmd 过自动弹出);
  2 条无队列条目:**#36 tosa-ladder / #37 ctx-dim-ladder**(轮 223/226
  早期梯,判读已被 #46/#39 后续 3-seed 探针取代,合并只为判读行归档)。
- GitHub mergeable 实测:55 个 UNKNOWN(积压未计算,非阻塞),
  **#56 CONFLICTING/DIRTY**(唯一实测冲突;base 早于轮 284,
  wave/loop 在其切出后前进了十个提交)。
- 分支拓扑实测:全部分支自 wave/loop **独立平行切出**(领先 merge-base
  +1~+4 提交,无堆叠)⇒ 探针代码零相互依赖,合并顺序不影响正确性。

## 2. 推荐合并顺序

**按 PR 号升序(#1→#56)**=轮次时间序。理由:①无代码依赖,升序只
为 PRD §19 判读行按轮号落位、队列按序自动弹出;②每合并一个,先点
**Update branch**(=git merge wave/loop,正常推分支,无 force)→按
§3 规则解冲突→mergeable 转 clean→合并。

## 3. 冲突预警与逐文件解法(实测依据)

| 文件 | 解法 | 依据 |
|---|---|---|
| `docs/loop/GOALS.md` | **取 ours**(wave/loop 现行) | 现行队列是全量权威(54 条全带 PR 号);dir 版本=历史子集 |
| `docs/loop/direction-gate.jsonl` | **取 ours** | 已逐条核验:dir 轮次判单(268-283)全部已在 wave/loop(50 行) |
| `docs/loop/PLAYBOOK.md` | **联合**:ours + theirs 独有坑条目 | 实测 dir 分支有 wave/loop 缺失条目(如轮 279"2×2 次可加"条款);逐条补入,勿整文件覆盖 |
| `docs/PRD.md` | **双侧保留** | theirs 带来 dir 轮次 §19 判读行(=队列自动弹出锚+N1 引用依据);按轮号排序,**永不删行** |
| `benchmarks/` + `tests/` | **取 theirs** | 探针代码与测试,wave/loop 无此代码 |

## 4. 族分组速览(详情一律看 GOALS 队列条目)

| 族 | PR | 一句话 |
|---|---|---|
| 早期机制探针 | #1 #2 #3 #4 | 容量轴/ω 带外/NBody 聚合/R1d 判负(轮 113-122) |
| 学习动态与迁移 | #5 #6 #7 #8 #9 #10 #11 | 符号反转/dt 迁移/少样本三臂/双时标/grokking 判负(轮 126-146) |
| 训练动态审计 | #12 #13 #14 #15 #16 #17 #18 #19 #20 #21 | GNS/sharp/重复率/网格解析度/dt 课程/长度外推(轮 149-172) |
| 配置梯 | #22-#34 | 池宽/优化器/wd/深度/跨度/尺度/调度/SWA/warmup/幅度外推(轮 175-216) |
| 残差谱链 | #35 #45 #56 | 三轮口径演进,终局=ORDER_TIED+AMM-031 降级 reference-only(轮 219/246/283) |
| 早期观测/容量梯 | #36 #37 | 已被 #46/#39 取代,合并归档 |
| 3-seed 确认与归因 | #38 #39 #40 #41 #42 #43 #44 #46 #48 | 归因/容量反转/轨迹长度/视距/配方组合(轮 227-255) |
| 齐次头链 | #47 #49 #50 #51 #52 #53 #54 #55 | 七探针证据链,终局=either-or 采纳+AMM-033 默认头替换提案(轮 261-279) |

## 5. 合并后动作

1. 每批合并后跑 `./scripts/goal_check`:对应队列条目 check_cmd 过即自动
   弹出(AMM-026 状态驱动);弹出后队列条目数下降属预期(--audit 数数
   锚随实况变化,以实跑为准)。
2. 全部合并完:队列清空;PRD §19 含轮 113-283 全部判读行;
   `n1-paper-draft.md` 溯源 footer 的"pending merge"注记全部兑现。
3. **AMM-033(默认头替换)实施=合并后新段首消化轮**(提案条款),
   循环自决排程,无需用户指令。

## 6. 增量更新(轮 412,2026-09-27,⑤合并债条款=PR 状态变化时产出)

- **PR#57 新开**(dir/anchor-precision → wave/loop):ANCHOR-PRECISION
  判读 PRECISION_ANCHOR_ROBUST(第 65 族第 1 轮,锚读数精度轴稳健,
  决策=AMM-033 锚协议⑤维持现文本)。**在途 PR 总数 56→57**;有队列
  条目者 54→55(ANCHOR-PRECISION 条目已入 GOALS 队尾)。
- **堆叠依赖注记**:dir/anchor-precision 自 dir/pool-bits 切出(齐次
  头线先例),含 PR#53 全部提交——先合并 PR#53 则 PR#57 diff 自动
  缩减为本族两文件(probe+tests)+判读行;反之 PR#57 先合并亦无冲突
  (超集包含)。
- 判读详情唯一源不变=GOALS 队列条目 status 字段(AMM-021)。
