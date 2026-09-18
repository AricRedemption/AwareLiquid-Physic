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
  N1 论文骨架已达 done_condition(Related Work 全文+表 1+主图引用+产物索引,
  无占位);打包阶段完成。当前转入"等裁定+轻维护"阶段。
current_action: >-
  运行 ./scripts/goal_check 并按其 VERDICT 继续:ACHIEVED → 顶部目标已
  弹出并晋升下一位,对新目标执行其首个迭代步;NOT-Achieved → 对当前
  顶部目标迭代一步(未达成不停)。每轮心跳先校验,再干活。
done_condition: >-
  队列空时进入文献扫描补队列;队列非空时永不停——每轮 goal_check 路由。
blocked_on: >-
  1) D4 GPU 去向;2) origin/master 合入顺序(PR#1 CLEAN 可合, wave/loop
  领先 35+ 提交);3) N1 正式英文稿是否启动。
next_trigger_hint: cron 30min 心跳(先 goal_check 路由) / 用户"继续" / SessionStart
pointer: docs/PRD.md §19(轮 44 隐藏集终跑为最新关键记录)
updated: 2026-09-19 00:58 (goal_queue + 校验路由器上线)
```

## goal_queue(双轨交替:engineering / frontier;顶部为当前目标)

```yaml
goal_queue:
  - id: G1
    track: engineering
    goal: D2 场任务结果图表化进论文附录(主图脚本扩场任务消融 panel)
    done_condition: docs/assets/ 存在 d2-loop-ablation 图,且骨架文档附录节引用它
    check_cmd: test -f docs/assets/d2-loop-ablation.png && grep -q "d2-loop-ablation" docs/d1-start-state-mismatch.md
  - id: G2
    track: frontier
    goal: 半群 k100 优势的跨 seed 稳健性量化(轮 44 反转的后续,≥5 seeds)
    done_condition: physics_out_v02/k100_seed_scan/k100_scan.json 含 ≥5 个 seed 的 k100 比值与符号统计
    check_cmd: python3 -c "import json,sys; d=json.load(open('benchmarks/physics_out_v02/k100_seed_scan/k100_scan.json')); sys.exit(0 if len(d['results']['seeds'])>=5 else 1)"
  - id: G3
    track: engineering
    goal: hidden 终跑一键化(scripts/hidden_check,自动登记消耗表)
    done_condition: scripts/hidden_check 可执行且能跑标准 4 臂隐藏终跑
    check_cmd: test -x scripts/hidden_check
  - id: G4
    track: frontier
    goal: M2 context→势能映射容量瓶颈实验设计(P4 候选,设计文档)
    done_condition: docs/d2-capacity-design.md 存在且含预注册协议段
    check_cmd: grep -q "预注册" docs/d2-capacity-design.md 2>/dev/null
```

队列规则:goal_check 判 ACHIEVED 时弹出顶部并晋升下一位;两轨交替
养成交付节奏;新方向(文献扫描/用户指定)追加到队尾并标 track。
队列空才允许空转/扫描补池。

## 推进规则

1. current_action 完成且验收过 → 写入 next_action,`updated` 戳更新,
   与产物同一原子提交;
2. 出现需要人的决策 → `state: BLOCKED-HUMAN` + `blocked_on` 写明问题,
   循环在收尾轮汇总,不自行决策;
3. 目标本身要变(罕见)→ 走 `AMENDMENTS.md` 提案制,不改本文件语义。
