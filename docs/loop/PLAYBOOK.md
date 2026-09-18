# LOOP PLAYBOOK — 操作坑与惯例(每轮开场必读,新坑必回写)

> ACE 式演化手册(wave-10 轮 43 落地,2026-09-18)。本文件是循环的**操作记忆**:
> 每轮开场先读;踩到新坑当场回写(一行:坑 → 解法 → 出处轮次);惯例一旦写入
> 即为约束。目标:同一个坑不踩第二次。

## 坑清单(每条都真实付出过代价)

- **`torch.linspace(...).long()` 浮点舍入会越过终点**(轮 22):候选起点
  越过 `S−k_train−1` 导致训练目标索引越界。→ 任何 linspace 取整后必须
  `.clamp(max=合法上界)`;派生量先确认 `steps+1` 语义。
- **`gen_spring` 返回 `steps+1` 个时刻**(轮 22):S 的推导处处可能差一,
  配对比较前先 `S = tensor.shape[1]` 实取,不要用生成参数回推。
- **管道尾命令吞退出码**(轮 22):`pytest -q | tail -1 && 下一步` 中
  pytest 失败也会继续(退出码取自 tail)。→ 门禁链写 `pytest -q && ...`
  或单独跑 pytest 不接管道。
- **`no_grad` 杀死 symplectic rollout**(轮 2):哈密顿头 `dV_dq` 内部用
  autograd,eval 前向必须 `torch.enable_grad()` 包裹(参考
  `eval_rollout_mse`),输出再 detach。
- **测试 Namespace 与脚本 argparse 漂移**(轮 13/14/22 三次):给
  `run_one` 加每个新 flag 后,`tests/test_eval_ks_ladder.py` 的 `_args`
  必须同步(已有 keep-in-sync 注释);AttributeError 就是这个。
- **结果目录 `benchmarks/physics_out_v02` 是 gitignored**(轮 2 起):
  结果 JSON 只留本地 + audit,数字必须抄进 PRD 记录,路径仅作本地索引。
- **新产物用子目录隔离**(轮 2 起):绝不覆盖 canonical 产物
  (如第九波 `sample_efficiency_p11.json`);脚本若固定写文件名,用
  `--out_dir 子目录` 隔离。
- **screening 与判定分离**:1 seed 只做闸门/校准,结论必须 3 seeds +
  预注册判据;口径偏离(如用了 k100 而非 k1)必须如实注记(轮 13)。
- **配对基线要看 pool**:同 pool seed 才可逐 seed 配对;`max(sizes)` 不同
  ⇒ pool 不同 ⇒ 只能指示性对比(轮 14 教训)。
- **field_eval 单 seed 全流程 ~7 分钟**:全量拆轮必须预声明(轮 7)。
- **后台长命令**:run_in_background + TaskOutput 轮询;脚本内 `time` 计时
  校准时长(轮 8 起)。
- **策略热更新竞态**(轮 51-52,2026-09-19 夜):用户会在会话运行中途往
  PLAYBOOK/GOAL-PROMPT 提交新规(本夜算力闸门 v1→v2 两次热更);E3 两跑在
  v2 落地后启动,违规(如实入档轮 53,不改写轮 52 判定行)。→ 解法:每次
  心跳启动任何执行类工作前,先 `git log --oneline -3 docs/loop/PLAYBOOK.md
  docs/loop/GOAL-PROMPT.md` 复查规则新鲜度再动手。(出处:轮 51-52;适用
  条件:多会话同仓;验证状态:已验证——本夜三次热更全部命中。)
- **训练循环不传轨迹索引 → 前缀字节指纹查表**(轮 51):需要给模型注入
  每轨迹潜变量(oracle ctx)但 train_semigroup/prefix 只喂 gather 切片时,
  以 t_obs 前缀 `numpy().tobytes()` 为键建行号表,零侵入训练循环;表外
  轨迹回退语义默认值(常数场→零投影即正确 oracle)。(出处:轮 51
  `OracleOperatorWrapper`;适用条件:批 = 母张量精确 gather、轨迹不重复
  生成;验证状态:已验证——A/B 臂与 D2 逐位复现。)
- **1-seed 筛查两连中**(轮 51/52,被验证有效的做法):E1 筛查 ρ 0.730/
  0.719 → 终判 0.726/0.742 同判定;E3 冒烟双探针 ≈0 → 终判同。筛查闸门
  实践有效,保持。(出处:轮 51/52;验证状态:已验证,n=2。)
- **新基准脚本的结果 JSON 顶层必须有 `results` 键**(轮 55):audit_results
  的 schema 硬要求,探针类脚本裸写 summary/per_batch 会被 --check 拒
  (付过 1 cycle)。→ 载荷包一层 `"results": {...}`,args/meta 顶层照旧。
  (出处:轮 55 grad_starvation_probe;验证状态:已验证。)
- **`ctx.retain_grad()` 量激活级梯度**(轮 55):对非叶张量 ctx(推断头
  输出)先 retain_grad 再进 rollout,backward 后 ctx.grad 即 ∂L/∂ctx;
  oracle 对照用 `row.clone().requires_grad_(True)` 叶张量解耦推断图。
  (出处:轮 55 grad_starvation_probe;验证状态:已验证。)

- **经验蒸馏轮最小闭环(轮 61,被验证有效的做法)**:补池时先 grep
  档案既有 query 族(PRD §19 轮 45/60 清单 + scan 档案节标题),本轮
  选**零重叠族**;3 次检索(每族 1 次)即可收口 ≥1 条入库,全轮非算力
  <15 分钟。方向类条目**当轮**追加 GOALS 队尾(写清 done_condition 可
  验证判据),防"档案写了、循环忘了"——队列恢复非空,下轮 goal_check
  自动路由。(出处:轮 61;验证状态:已验证——D5-EXPOSURE 即按此产出。)

- **goal_check 空 check_cmd ⇒ 假阳性 ACHIEVED 误弹**(轮 62,实付 1
  cycle):路由器对队首目标跑 `subprocess.call(check_cmd, shell=True)`,
  入队时漏写 check_cmd ⇒ 空命令退出码 0 ⇒ 刚入队未干活的目标被判达成
  弹出吞掉。→ ① 防线已修:goal_check 空 check_cmd 按未达成路由;
  ② 入队模板必须带轻量验收锚(grep 式 check_cmd,如 `grep -q "锚"
  docs/PRD.md`);③ 误弹后恢复:目标回写队首,在提交信息注明"误弹恢复"。
  (出处:轮 61 入队/轮 62 发现;适用条件:一切经 goal_check 的入队;
  验证状态:已验证——修复后 NOT-Achieved 路由正确。)

- **入新目标前先查工具/产物覆盖面**(轮 63,被验证有效的做法):蒸馏轮
  想入方向类目标时,先 grep 现有 TOOLS 工具与 benchmarks/ 产物目录
  (如 d3_* 已有 tobs8/tobs24 对照),确认新目标是**增量**(连续图谱/
  新框架)而非重复;check_cmd 锚写目标 ID 特异串(如 "D6-INFO-BUDGET
  判读"),不写会过早命中的泛词。(出处:轮 62 假阳性教训的推广;
  验证状态:已验证——D6 入队前查得 fisher_j 闭式已存在,目标即改为
  "图谱+分解"增量定位。)

- **闭式工具的图谱化复用**(轮 64,被验证有效的做法):已有一维/单点
  判据的秒级闭式工具(如 fisher_j)不必重写——沿未扫过的轴(窗口长度)
  做网格扫描 + 与已知渐近律(t³)对照,即可把单点结论升级为图谱级判读
  (无平台判定 + CRB 换算),全轮零算力 <10 分钟。数字抄 PRD,JSON 留
  gitignored 目录。(出处:轮 64;验证状态:已验证——D6 即按此交付。)

## 惯例(已固化的流程约束)

- **算力闸门(2026-09-19,AricRedemption 定策,硬规则)**:任何实验动手前,
  预注册必须含**实测校准的预计总时长**(用冒烟实测推算,不许拍脑袋);
  预计 **>1 小时**的任务**禁止本地执行**——正确动作:① 把协议+可执行产物
  (脚本/参数/判据)做成 PR 交付(云算力或他人执行),② 在 PRD 登记云算力
  欠账,③ 循环立即换下一方向,不阻塞不硬跑。单条命令预计 >25 分钟同样
  拆分或转 PR。探针/分析/判读/文档不受限。
- 预注册先行:判负标准写进 PRD 再动手;负结果与正结果同等记录。
- 验收门:pytest 全绿 + `audit_results.py --check` 全过才可提交。
- 原子提交:协议+代码+结果+台账+波次记录同一 commit,推 fork。
- 先读 `TOOLS.md` 复用既有工具,再考虑新写;新工具写完回写 TOOLS。
- **单马拉松约定(2026-09-19)**:同一时间只允许一个马拉松会话。任何马拉松
  启动前先看 `docs/loop/GOALS.md` 的 updated——距今 <100 分钟 ⇒ 已有活
  会话,本次启动转为"仅确认状态并结束"。防 CPU 互抢与文件竞态。
- **经验蒸馏轮(QUEUE-EMPTY 时执行,2026-09-19 制度化)**:社区/论文扫描
  找有效经验,每条入库必须含【出处链接+适用条件+验证状态(待验证/已验证/
  不适用)】并分流:操作类→PLAYBOOK 本节;工具类→实现后进 TOOLS;方向类
  →GOALS 队尾。本轮交付=≥1 条入库条目或 ≥1 个新目标,否则不算完成——
  防止变成无限读论文。社区说有效 ≠ 对我们有效,有效性由后续循环与
  RSI-INDEX 的 K/E 变化收口。
- 对循环自身程序的改进 = 提案制,写 `AMENDMENTS.md`,未经用户批准不得
  自行更改 cron 提示词或本 playbook 的"惯例"节(坑清单可直接追加)。
