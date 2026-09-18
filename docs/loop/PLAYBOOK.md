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
- 对循环自身程序的改进 = 提案制,写 `AMENDMENTS.md`,未经用户批准不得
  自行更改 cron 提示词或本 playbook 的"惯例"节(坑清单可直接追加)。
