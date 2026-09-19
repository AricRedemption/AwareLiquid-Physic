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
  轮 77(2026-09-19 13:10):队列空→蒸馏补池第 17 族(谱偏置/频率
  原理族,scan §17,3 坐标+1 行动入库);E1 缺口获机制命名候选
  (低频优先优化动力学),R1d 表征轴登记为分流表第四路(§12.3 追加);
  SB-NAMING 已入队并预注册(PRD §19 轮 77)。R1/R2 云回传仍待。
current_action: >-
  下一心跳先跑 ./scripts/goal_check 路由:SB-NAMING(NOT-Achieved 预期)
  ⇒ 对其迭代一轮:docs/spectral-bias-naming.md 机制命名对账文档
  (四层证据链 + R1d 预注册草案),判负标准 PRD §19 轮 77;若 R1/R2
  云结果到达,优先机械验收(scan §12.3 四路分流)。
done_condition: >-
  队列非空时永不停——每轮 goal_check 路由;队列空则蒸馏补池,
  循环不自行停止。
blocked_on: >-
  1) R1/R2 云结果回传(欠账 ~70min);2) D4 GPU 去向;3) origin/master
  合入顺序(PR#1 CLEAN 可合);4) N1 正式英文稿是否启动。
next_trigger_hint: goal_check → SB-NAMING / R1/R2 云结果回传 / 用户"继续"
pointer: docs/PRD.md §19(判读报告落点);docs/scan-conditioning.md §8-17
  (文献坐标;轮 61/63/65/73/75/77 蒸馏);docs/dh-dissipation-design.md
  (轮 74);docs/koopman-bridge.md(轮 76)
updated: 2026-09-19 13:12 (轮 77 蒸馏补池:谱偏置族 3+1 入库 scan §17;
  R1d 第四路登记;SB-NAMING 入队+预注册;R1/R2 仍外部阻塞)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
- id: SB-NAMING
    track: frontier
    goal: E1 缺口的谱偏置机制命名对账文档(四层证据链+R1d 预注册草案;判负标准 PRD §19 轮 77;纯写作)
    done_condition: docs/spectral-bias-naming.md 落地(命名假设+四层证据链逐层对账+R1d 预注册草案)+判读写入 PRD §19
    check_cmd: grep -q "SB-NAMING 判读" docs/PRD.md && test -f docs/spectral-bias-naming.md
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空才允许空转/扫描补池。
**E2 条件性重入口(不入队,防路由器空转)**:若 E3 修复推断后
ρ_CB′ 仍 ≥0.9(接口重成第一嫌疑),把 E2(concat/hyper,设计文档 §6
原闸门)追加回队尾。
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
