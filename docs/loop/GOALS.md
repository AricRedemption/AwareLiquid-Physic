# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 本文件是项目的 goal prompt 本体:任何会话(人/cron/hook)打开工作区,
> 读这里 → 执行 `current_action` → 完成后推进状态并原子提交。
> 规则:一次只有一个 `current_action`;完成条件必须可验证;详情指针指向
> PRD §19,不在本文件复制研究内容。更新本文件 = 推进程序计数器。

```yaml
state: RUNNING            # RUNNING | BLOCKED-HUMAN | IDLE
mode: ON                  # AMM-003 迭代总开关(./scripts/iteration start|stop)
iteration_window: 周一至五 23:00-09:00(夜间cron);周六 09:00-23:00(全天候)
current_goal: >-
  D2-CAPACITY 轮:E1 已判定(E1-c 推断瓶颈:oracle ctx 经同一 FiLM 接口
  兑现 27% 增益而 liquid 推断 ctx 探针≈0)。当前 E3 推断侧容量阶梯
  (d_model 96/192 × 3 seeds + MLP 探针,设计文档 §10 预注册)。
current_action: >-
  运行 ./scripts/goal_check 并按其 VERDICT 继续:ACHIEVED → 顶部目标已
  弹出并晋升下一位,对新目标执行其首个迭代步;NOT-Achieved → 对当前
  顶部目标迭代一步(未达成不停)。每轮心跳先校验,再干活。
  当前顶部 G4-E3:先冒烟校准 d96 单 seed 实测时长(算力闸门),再逐臂
  分命令跑 d96/d192(3 seeds,各 ≤25 min),按 §10 判定入档。
done_condition: >-
  队列空时进入文献扫描补队列;队列非空时永不停——每轮 goal_check 路由。
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35+ 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: 夜间马拉松(23:00 启动,自循环至 09:00) / 用户"继续" / 兑底心跳(3h)
pointer: docs/PRD.md §19(轮 51 记录为最新;设计 docs/d2-capacity-design.md §10)
updated: 2026-09-19 03:10 (E1 判定 E1-c 入档,E2 降权出队,E3 预注册补池;算力闸门遵行)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
- id: G4-E1
    track: engineering
    goal: D2-CAPACITY E1 实装+筛查(OracleOperator+模式投影+线性探针+测试,1-seed 三臂筛查)
    done_condition: field_eval 支持 --oracle_ctx,三臂筛查 JSON 落 d2_capacity/e1_screen 且 pytest 全绿
    check_cmd: test -f benchmarks/physics_out_v02/d2_capacity/e1_screen/field_eval.json
- id: G4-SCAN
    track: frontier
    goal: 条件化接口文献/GitHub 扫描(FiLM/hypernet/concat 在 FNO 与 PDE 基础模型的条件化实践,谁做过、失败在哪)
    done_condition: docs/scan-conditioning.md 存在且含至少 3 项相关工作注记
    check_cmd: test -f docs/scan-conditioning.md
- id: G4-E3
    track: engineering
    goal: D2-CAPACITY E3 推断侧容量阶梯(d_model∈{96,192}×3 seeds+MLP 探针,按设计文档 §10 预注册判定)
    done_condition: e3_d96 与 e3_d192 结果 JSON 落 d2_capacity/ 且判定入 PRD §19
    check_cmd: test -f benchmarks/physics_out_v02/d2_capacity/e3_d96/field_eval.json -a -f benchmarks/physics_out_v02/d2_capacity/e3_d192/field_eval.json
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空才允许空转/扫描补池。
**E2 条件性重入口(不入队,防路由器空转)**:若 E3 修复推断后
ρ_CB′ 仍 ≥0.9(接口重成第一嫌疑),把 E2(concat/hyper,设计文档 §6
原闸门)追加回队尾。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
