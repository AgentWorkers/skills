---
name: sprint-os
description: "这是一个专为AI代理设计的5分钟快速操作系统。其执行周期为：评估（ASSESS）→ 计划（PLAN）→ 确定范围（SCOPE）→ 执行（EXECUTE）→ 测量（MEASURE）→ 适应（ADAPT）→ 记录（LOG）→ 进行下一步（NEXT）。该系统支持可选的Convex集成功能，用于跟踪执行过程、收集指标数据以及消除内容重复。"
requiredEnv:
  - CONVEX_SPRINT_URL  # optional — Convex HTTP API endpoint for sprint logging
permissions:
  - network: Makes HTTP requests to Convex endpoint (optional) and any resources needed for sprint work
  - filesystem: Reads/writes sprint logs to working directory
source:
  url: https://github.com/Batsirai/carson-skills
  author: Carson Jarvis (@CarsonJarvisAI)
  github: https://github.com/Batsirai/carson-skills
  verified: true
security:
  note: The Convex endpoint URL is safe to store in env. No credentials are embedded in the skill itself.
---
# Sprint OS — 5分钟冲刺操作系统

Sprint OS专为可立即投入使用的AI代理设计。每次冲刺都会产生一个可交付的成果（而非计划或总结），这是一个实实在在的成果。

---

## 什么是Sprint OS

Sprint OS是一种适用于需要保持高效执行状态的AI代理（以及人类）的操作系统。你将按照连续的5分钟冲刺模式进行工作。每个冲刺都遵循相同的8步循环流程，并且所有操作都会被记录下来。没有任何任务会被批量处理、被忽视或丢失。

**何时使用Sprint OS：**
- 当用户要求代理“以冲刺模式运行”或“使用Sprint OS”时；
- 在开始新项目或工作会话时，需要结构化的管理方式；
- 需要自主执行任务并跟踪工作进度时；
- 希望将工作记录到Convex后端系统以便进行跟踪和去重时。

---

## 施冲刺循环

每次冲刺都严格遵循以下步骤：

### 1. 评估（ASSESS）
> 当前的状态是什么？与目标结果之间还有多大的差距？

- 阅读当前的任务列表、相关文件以及最近的冲刺日志；
- 明确当前的工作进展；
- 确定差距：当前状态与目标结果之间还缺少什么？

### 2. 规划（PLAN）
> 现在可以采取的最具成效的行动是什么？

- 选择本次冲刺要完成的一项任务；
- 应用优先级排序规则（见下文）；
- 不要同时处理多项任务。

### 3. 确定任务范围（SCOPE）
> 在5分钟内完成任务。

- 明确本次冲刺要产生的具体成果；
- 如果无法在5分钟内完成，将其拆分为更小的冲刺任务；
- 每次冲刺都必须有具体的成果。

### 4. 执行（EXECUTE）
> 开始执行任务并产生相应的成果。
- 全神贯注于任务成果的完成，避免任务范围扩大；
- 如果发现任务范围设定错误，立即停止、重新调整任务范围后再继续。

### 5. 测量（MEASURE）
> 这项任务是否推动了目标的实现？有哪些变化？

- 说明具体的成果；
- 指出相关的指标及其变化情况；
- 诚实地记录：是“已完成”、“部分完成”还是“受阻”。

### 6. 适应（ADAPT）
> 重新调整优先级，放弃那些无法推进的任务。
- 根据结果，确定下一次冲刺的重点；
- 如果连续3次冲刺都没有取得任何进展，应立即调整工作方向；
- 绝不要在无效的方法上继续浪费时间。

### 7. 记录（LOG）
> 将冲刺日志记录到指定的文件中（格式见下文），并根据需要将日志发送到Convex后端系统。

### 8. 开始下一次冲刺（NEXT）
> 立即开始下一次冲刺。

不允许出现任何延误；反思时间不得超过30秒。保持工作势头是关键。

---

## 施冲刺规则
- 每次冲刺都必须产生一个可交付的成果；
- 如果任务耗时超过5分钟，应将其拆分为更小的冲刺；
- 不要提前规划超过3次的冲刺内容；
- 优先考虑推进工作的进度，而非追求完美；
- 每次冲刺都必须与具体的目标成果相关联；
- 如果遇到阻碍，记录阻碍因素并直接进入下一次冲刺，切勿空闲等待。

---

## 优先级排序规则

在每次冲刺开始前，问自己：
> “如果我只能在接下来的5分钟内完成一件事来接近目标，那会是什么？”

1. **修复问题** → 首先解决正在造成损失（金钱或信任）的问题；
2. **优化现有流程** → 在尝试新方法之前，先优化现有的高效流程；
3. **测试新方法** → 通过小规模实验寻找新的突破点；
4. **建设基础设施** → 只有在前三项工作顺利进行时，才进行基础设施的建设。

---

## 转变策略的触发条件

当出现以下情况时，应立即停止当前的工作方向并进行调整：
- 连续3次冲刺都没有取得任何进展 → 更改工作方向或方法；
- 某个工作流程的效率开始下降 → 减少资源投入，尝试其他方案；
- 出现意外的成功（如病毒式传播、媒体报道、客户推荐等） → 立即抓住机会；
- 客户反馈表明需要调整策略 → 将相关任务提至冲刺优先级列表的顶端。

---

## 施冲刺日志格式

在`sprint-log.md`文件中为每次冲刺记录一条日志条目：

```markdown
## Sprint [N] — [YYYY-MM-DD HH:MM]

**Project:** [project name]
**Workstream:** [marketing / development / content / research / etc.]
**Task:** [what you did]
**Artifact:** [what was produced — link or one-line description]
**Metric:** [what moved, or "no movement"]
**Status:** completed | partial | blocked
**Blocker:** [only if blocked — what's stopping you]
**Next sprint:** [what comes next]
```

---

## Convex集成（可选）

如果设置了`CONVEX_SPRINT_URL`，请将每次冲刺的日志发送到该HTTP端点。这可以实现以下功能：
- 跨会话查看冲刺历史记录；
- 分析工作流程的效率；
- 去重处理相关内容；
- 跟踪指标变化趋势。

### 设置方法
1. 在`scripts/convex-setup.md`中部署Convex后端服务；
2. 将`CONVEX_SPRINT_URL`设置为Convex后端的URL（例如：`https://your-deployment.convex.site`）；
3. 每次冲刺结束后，系统会自动将日志记录到后端。

### 可用端点
| 方法 | 路径 | 功能 |
|--------|------|---------|
| POST | `/sprints/log` | 记录完成的冲刺 |
| GET | `/sprints/recent?project=X&limit=N` | 查看最近的冲刺历史记录 |
| GET | `/sprints/stats?project=X&days=N` | 查看工作流程的效率分析 |
| POST | `/metrics/record` | 记录指标数据 |
| GET | `/metrics/latest?metric=X` | 获取当前指标值 |
| GET | `/metrics/trend?metric=X&days=N` | 查看指标的变化趋势 |
| POST | `/content/log` | 记录内容的创建情况 |
| GET | `/content/search?query=X` | 检查内容是否重复 |

### 日志记录脚本

使用`scripts/log-sprint.sh`脚本进行快速的命令行日志记录：

```bash
./scripts/log-sprint.sh \
  --project "my-project" \
  --workstream "development" \
  --task "Fix checkout redirect bug" \
  --artifact "PR #42 opened" \
  --metric "checkout CVR: TBD pending deploy" \
  --status "completed"
```

---

## 日常工作流程

### 早晨
- 阅读当前的任务列表；
- 评估所有任务的进展情况；
- 确定当天的首要任务；
- 开始第一次冲刺。

### 持续工作
- 连续进行5分钟的冲刺；
- 记录每次冲刺的详细情况（包括文件和Convex系统的日志）；
- 对于需要大量计算的工作，可以启动辅助代理；
- 每次冲刺之间休息时间不超过30秒。

### 每天结束时
- 完成冲刺日志的记录；
- 更新任务列表，反映任务的完成情况；
- 确定第二天的首要任务；
- 如果配置了Convex系统，运行`scripts/log-sprint.sh --daily-summary`命令。

### 每周五
- 回顾：哪些工作流程的效果最好？
- 哪些冲刺被浪费了？原因是什么？
- 识别最大的瓶颈；
- 为下周重新安排任务优先级。

---

## 报告格式

### 日常状态报告
```
📊 DAY [X] — [DATE]
SPRINTS: [completed today] | TOP WIN: [best result]
BLOCKER: [biggest obstacle]
METRICS: [key metric] → [current value]
TOMORROW: [1–2 sentences]
```

### 周度总结
```
📈 WEEK [X] — [DATE RANGE]
SPRINTS: [total] (by workstream breakdown)
WINS: [top 3 with metrics]
MISSES: [top 3 with root cause]
LESSONS: [top 3]
NEXT WEEK: [top 3 priorities]
ESCALATIONS: [decisions needed from human]
```

---

## 使用示例
```
# Start sprint operating mode
"Enter sprint mode. My project is [X]. Target outcome: [Y]."

# Run a sprint
"Run sprint on: write 3 email subject line variants for the welcome sequence."

# Review recent sprints
"Show my sprint log for today."

# Weekly review
"Generate weekly sprint review."

# With Convex logging
"Log sprint: task=wrote homepage copy, artifact=homepage-v2.md, metric=awaiting test, status=completed"
```

---

## 文件结构
```
sprint-os/
├── SKILL.md                    ← This file
├── README.md                   ← Human-readable overview
└── scripts/
    ├── log-sprint.sh           ← CLI sprint logger (Convex optional)
    └── convex-setup.md         ← Instructions for Convex backend setup
```

---

*Sprint OS v1.0 — 2026年2月*
*作者：Carson Jarvis (@CarsonJarvisAI)*