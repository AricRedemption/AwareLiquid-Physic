# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE
mode: ON                  # AMM-003 迭代总开关(./scripts/iteration start|stop)
iteration_window: 全天候(00:00-24:00 永动模式,2026-09-19 用户改定;总开关 mode=ON/OFF)
current_goal: >-
  治理轮 2+对齐修正(2026-09-19 15:09,设计会话):AMM-010(T1 放宽 ≤30min
  当轮直跑 + Probe-First 大训练准入)+ AMM-011(设计/执行会话角色分离)+
  AMM-012(训练↔方向平衡:EXP≥30%/WIP≤2/消化耦合)落地;D-1 UQ 校准已
  结案判负(coverage 1.6%/0/0,过度自信方向,N1 上限 L2 坐实,判读见 PRD
  §19 "D-1 判读")。台账 D_count=3。对齐修正 5 处:DEBT-LEDGER 清偿顺序
  T1 化/TOOLS probe_run 行 T1≤30/本文件时间戳实测化/AMM-008 核数以实测
  为准(8核→4线程)/GOAL-PROMPT"算力目标一生"段 v3.1 化(该段已于 v4.0
  重写时并入"算力纪律"节,此为历史日志)。
  治理轮 3(2026-09-19 17:29,设计会话终审):AMM-013 仪表强制化落地
  (goal_check 焊入 DEBT-FIRST/MINING-FROZEN 硬出口+台账指标自动化,真实
  仓库验证路由正确);AMM-014 欠账分级提案 PROPOSED 待批(云债不阻塞循环);
  GOAL-PROMPT 终审修正 5 处(资源护栏去机型数值+80%绝对红线入文/吞吐优先
  与 AMM-012 对齐/平衡阈值收归 gauge/收尾清单补 B+EXP 计量/隐藏卷条款
  去 PR 专属措辞)。
current_action: >-
  下一心跳(执行会话,AMM-011 角色下所有执行归你):按 DEBT-LEDGER 顺序
  清欠——D-4 R2 视距扫描(T2 后台,可拆 3×~20min 逐档跑:K=8/16/32,
  完整命令 docs/pr-d2-r1r2-cloud.md §2;注意 k=8 档须逐位复现 e1_final
  A/B 臂作管线校验,不复现即停)。[D-3 已结案(轮 90 判负:辅助辨识在
  硬约束架构失效,E2 重入口失效,998 未消耗);D-2 余项=TimesFM 臂权重
  受限挂起(~/.cache/timesfm/torch_model.ckpt 断点续传中,到位则先 T1
  补跑 --models timesfm --timesfm_path <path> ~10min)]
  ——每笔 PRD §19 判读(锚"<id> 判读")+台账置 closed+digest_rate 更新;
  R2 判读走 scan §12.3 视距轴判据;清零后恢复 GRAD-PATH(队首)。
done_condition: >-
  欠账优先:D_count=0 前心跳只清欠/验收,不扩池;恢复队列后每轮 goal_check
  路由;收口按 AMM-007 判据 S1-S4 任一满足即 state: IDLE(写收尾+RSI 入账,
  保留重入口:结果回传/用户指令/新欠账)。
blocked_on: >-
  1) D-2 依赖环境(chronos/timesfm 安装+权重下载,执行会话处置);2) D4 GPU
  去向;3) origin/master 合入顺序(PR#1 CLEAN 可合);4) N1 正式英文稿是否启动。
next_trigger_hint: goal_check → 清欠 D-2…D-4 / GRAD-PATH / 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/loop/DEBT-LEDGER.md(欠账
  台账,清欠顺序与指标);docs/loop/AMENDMENTS.md(AMM-007/008/009);
  docs/scan-conditioning.md §8-22(文献坐标;轮 61/63/65/73/75/77/79/81/83/85/87
  蒸馏);docs/dh-dissipation-design.md(轮 74);docs/koopman-bridge.md(轮 76);
  docs/spectral-bias-naming.md(轮 78);docs/eval-norms-vpt.md(轮 80);
  docs/tsfm-baseline-protocol.md(轮 82);docs/uq-audit.md(轮 84);
  docs/structure-injection-vs-discovery.md(轮 86)
updated: 2026-09-19 23:45 (轮 90:D-3 R1 主跑 T1 清偿判负(0.019938 vs
  0.020004=0.9967,corr 0.058<0.2——辅助辨识在硬约束架构失效,负判据双
  条件成立;998 未消耗;E2 重入口失效,R1b/R1c 条件字面触发列候选);
  判读入 PRD §19;台账 D-3 closed,digest 2/4;下一心跳 D-4 R2 K=8 档起)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
- id: GRAD-PATH
    track: engineering
    goal: 滚出训练梯度路径审计轮(create_graph 梯度路径语义审计+内存/梯度范数冒烟探针 k=8/32/128+辛伴随升级草案;判负标准 PRD §19 轮 87;探针零训练)
    done_condition: docs/grad-path-audit.md 落地(梯度路径语义审计+探针数字+辛伴随草案)+判读写入 PRD §19
    check_cmd: grep -q "GRAD-PATH 判读" docs/PRD.md && test -f docs/grad-path-audit.md
- id: SCAN-AUDIT
    track: frontier
    goal: 溯源审计轮(T0,AMM-015):scan §1-22 约 49 条入库逐条判溯源等级(题录可复核/仅域名根/缺出处三档)+已知错题录修订(LieGAN 年份)+缺证性声明全库降档扫("公认空白"类→"当前 query 族下未检索到");判负标准 PRD §19 轮 88 治理轮
    done_condition: docs/scan-traceability-audit.md 落地(逐条溯源等级表+修订清单+题录可复核率)+判读写入 PRD §19
    check_cmd: grep -q "SCAN-AUDIT 判读" docs/PRD.md && test -f docs/scan-traceability-audit.md
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空 ⇒ 按 goal_check 路由(蒸馏/证据轮/清欠,以路由器裁决为准)。
**E2 条件性重入口(不入队,防路由器空转)**:若 E3 修复推断后
ρ_CB′ 仍 ≥0.9(接口重成第一嫌疑),把 E2(concat/hyper,设计文档 §6
原闸门)追加回队尾。
**(轮 90 注记:D-3 R1 判负 ⇒ 按 PR 包 §3.4 预注册,E2 条件性重入口
失效——推断侧方向关闭;R1b/R1c 重入口条件字面触发,列为队列候选
非欠账,待 D_count=0 队列恢复后按路由裁决。)**
**R1b 条件性重入口(轮 65 登记,轮 66 修订,不入队)**:若 R1 云结果
回传判负(辅助辨识损失未兑现 oracle 缺口收敛),把 R1b 追加回队尾——
先决条件已判明:当前 T 非偶 ⇒ 回程一致性需先补结构(硬:T 偶参数化;
软:一致性损失,PRD §19 轮 66),真物理归纳偏置(动能偶),判负标准
届时预注册(scan §10.3)。
**R1c 条件性重入口(轮 68 登记,不入队)**:R1 判负且 ctx 探针仍 ≈0
(信息没进来)⇒ R1c(attention/可学习聚合替代节点 mean-pool,代码
前提已定位 model.py 编码管线;scan §12.2)。三路分流判读逻辑见
scan §12.3。
**R1d 条件性重入口(轮 77 登记,不入队)**:R1 判负且 R1b/R1c 均未
兑现缺口收敛 ⇒ 表征轴第四路(ctx/q 的 Fourier 特征重参数化/高频
缩放,反制谱偏置;scan §17.3,§12.3 已追加)。先决条件:SB-NAMING
命名对账成立;判负标准届时预注册。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
