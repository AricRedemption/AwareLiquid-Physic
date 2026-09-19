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
  下一心跳(执行会话):队列空→goal_check 路由(gauge 已修复,EXP=0.8
  真值,预期 QUEUE-EMPTY ⇒ 蒸馏补池):选与既有 22 query 族零重叠的
  新族,按 PLAYBOOK 检索三连(综述/机制直击/对照式第三槽)执行;条目
  强制 AMM-015 溯源硬标准(作者+年份当场核验,带?不过夜)+ [坐标]/
  [行动] 分流;方向类当轮入队(check_cmd 双锚)。备选:整改面消化
  (scan §9.1/§11.1/§19.3 三条 B 级题录,scan-traceability-audit.md §7)。
  注意:P3 已终收口(轮 97,M2 headroom 关闭),条件性登记五条全终态
  (E2 失效/R1b 未触发/R1c 判负/R1d 失效/轮72 留档)——蒸馏条目不得
  重开已收口线;若连续 2 蒸馏轮无行动类产出 ⇒ 评估收口(S1)。每轮
  PRD §19 判读+PLAYBOOK ≥1 条回写+原子提交 push。
done_condition: >-
  欠账优先:D_count=0 前心跳只清欠/验收,不扩池;恢复队列后每轮 goal_check
  路由;收口按 AMM-007 判据 S1-S4 任一满足即 state: IDLE(写收尾+RSI 入账,
  保留重入口:结果回传/用户指令/新欠账)。
blocked_on: >-
  1) D-2 依赖环境(chronos/timesfm 安装+权重下载,执行会话处置);2) D4 GPU
  去向;3) origin/master 合入顺序(PR#1 CLEAN 可合);4) N1 正式英文稿是否启动。
next_trigger_hint: goal_check → 蒸馏补池(新 query 族)/ 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/loop/DEBT-LEDGER.md(欠账
  台账,清欠顺序与指标);docs/loop/AMENDMENTS.md(AMM-007/008/009);
  docs/scan-conditioning.md §8-22(文献坐标;轮 61/63/65/73/75/77/79/81/83/85/87
  蒸馏);docs/dh-dissipation-design.md(轮 74);docs/koopman-bridge.md(轮 76);
  docs/spectral-bias-naming.md(轮 78);docs/eval-norms-vpt.md(轮 80);
  docs/tsfm-baseline-protocol.md(轮 82);docs/uq-audit.md(轮 84);
  docs/structure-injection-vs-discovery.md(轮 86);docs/grad-path-audit.md(轮 93);
  docs/scan-traceability-audit.md(轮 94 溯源审计)
updated: 2026-09-20 06:25 (轮 97:**台账消化+工具修复轮**——① gauge
  窗口 bug 修复:rounds[-10:] 文件序取尾遇上 PRD §19 分层布局,窗口
  实际取到最老轮 ⇒ EXP 恒 0、MINING-FROZEN 每心跳误报(良性方向潜伏);
  改按头部轮号排序取窗口+WIN_PAT 扩 ID 型头,6 测试含分层回归,修复后
  EXP=0.8 报警清空;② **P3 终收口正式入档**:四路处方全负+机制解释完备
  ⇒ M2 系统辨识链路 headroom 关闭,N1 定位锚结构性质轴+硬约束边界
  声明;③ 条件性登记五条全终态(E2 失效/R1b 未触发/R1c 判负/R1d 失效
  [与轮 95 预注册冲突取后者]/轮 72 留档);④ 本会话被误报路由的两轮
  (94/96)产出独立有效,判定不改写;下一心跳蒸馏补池(新 query 族,
  AMM-015 硬标准);判读见 PRD §19 "轮 97 判读")
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue: []
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空 ⇒ 按 goal_check 路由(蒸馏/证据轮/清欠,以路由器裁决为准)。
**条件性重入口(唯一源=scan §12.3 四路分流表;此处只存状态,不复制逻辑)**:
E2 已失效(轮 90:R1 判负 ⇒ 推断侧方向关闭);R1b/R1c 已字面触发=
**队列候选**,待队列空时按 §12.3 裁决是否入队;R1d 先决=SB-NAMING
对账成立。AMM-021 等效清点:B1 路由行为不变(本块在 yaml 外,路由器
不解析)/B2 候选裁决时机保留/B3 E2 失效判定保留/B4 R1d 先决保留。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
