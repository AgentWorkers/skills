---
name: autonomy-windowed
version: 1.0.0
description: 时间窗口化的自主任务队列：自主执行仅在特定的时间窗口内进行（例如，UTC时间上午8点至晚上8点），而cron作业则在夜间运行。这种机制通过时间来区分不同的任务类型：白天执行自主任务，夜间执行维护任务。当您需要可预测的工作计划、受控的令牌预算，以及明确区分自主执行任务与计划维护任务时，可以使用这种方案。
metadata:
  openclaw:
    emoji: "⏰"
    category: productivity
---
# 窗口化自主运行模式

在**特定时间窗口**内，将你的代理从被动响应模式转变为自主工作模式。

---

## 概念

代理仅在**预定义的时间窗口**内自主运行。在窗口之外，代理仅回复 `HEARTBEAT_OK`。当自主运行模式被禁用时，Cron 作业会在夜间自动执行。

```
🌙 Overnight (10 PM - 8 AM UTC):  Autonomy OFF
☀️ Daytime (8 AM - 10 PM UTC):   Autonomy ON
```

**明确的分工：**白天处理队列中的任务，夜间进行系统维护

---

## 工作原理

### 1. 时间窗口

在 `tasks/QUEUE.md` 中定义活跃的时间窗口：

```markdown
## ⏰ Autonomy Windows

- 🌙 Overnight: 20:00 - 08:00 UTC → Autonomy OFF
- ☀️ Daytime: 08:00 - 20:00 UTC → Autonomy ON
```

### 2. 心跳机制

**在活跃时间窗口内：**
```
Heartbeat → Check urgent → No → Read QUEUE → Pick task → Work 15-30 min → Update QUEUE → Log
```

**在非活跃时间窗口内：**
```
Heartbeat → Check urgent → No → Reply "HEARTBEAT_OK" → Sleep
```

**紧急任务优先处理：**
```
Heartbeat → Check urgent → YES → Work immediately (even outside window)
```

### 3. 窗口切换

**窗口开启（上午8:00）：**
- 启用自主运行模式
- 开始从队列中获取任务
- 在 `tasks/MODE_HISTORY.md` 中记录：“窗口已开启”

**窗口关闭（晚上8:00）：**
- 关闭自主运行模式
- 如果有正在进行中的任务，则完成它们
- 在 `tasks/MODE_HISTORY.md` 中记录窗口关闭的状态
- 切换到待机模式（仅发送 `HEARTBEAT_OK`）

---

## 时间表示例

| 时间 | 活动 | 运行模式 |
|------|----------|------|
| 00:00 | GitHub 备份（Cron作业） | 夜间执行（无自主运行） |
| 02:00 | 心跳检查 | 待机模式（发送 `HEARTBEAT_OK`） |
| 03:00 | 临时文件清理（Cron作业） | 夜间执行（无自主运行） |
| 08:00 | 窗口开启 | ✅ 启用自主运行 |
| 09:00 | 处理任务 | 自主运行模式 |
| 12:00 | GitHub 备份（Cron作业） | 自主运行模式（暂停备份） |
| 14:00 | 处理任务 | 自主运行模式 |
| 20:00 | 窗口关闭 | ✌ 关闭自主运行模式 |
| 23:00 | 日常操作 + 内存管理（Cron作业） | 夜间执行（无自主运行） |

---

## 队列结构

```markdown
# Task Queue

## ⏰ Autonomy Windows
- 🌙 Overnight: 20:00 - 08:00 UTC → Autonomy OFF
- ☀️ Daytime: 08:00 - 20:00 UTC → Autonomy ON

---

## 🔴 Ready (can be picked up during windows)
- [ ] @priority:high [Task description]
- [ ] @priority:medium [Task description]

## 🟡 In Progress
- [ ] @agent: @priority:high [Task description]
  - Started: 2026-02-16 14:00 UTC

## 🔵 Blocked
- [ ] @priority:medium [Task] (needs: [what's blocking])

## ✅ Done Today
- [x] @agent: @priority:high [Task]
  - Completed: 2026-02-16 14:25 UTC

## 💡 Ideas
- [Idea for future work]
```

---

## 优先级系统

优先级决定了任务在窗口内的选择顺序：

| 优先级 | 使用时机 | 选择规则 |
|----------|-------------|-----------|
| `@priority:urgent` | 时间敏感，截止时间小于6小时 | 优先处理，即使不在窗口内也优先执行 |
| `@priority:high` | 重要任务，截止时间在24小时内 | 在窗口内优先处理 |
| `@priority:medium` | 一般重要任务 | 在窗口内次优处理 |
| `@priority:low` | 可选任务 | 在窗口内最后处理 |

---

## 窗口类型

### 全天窗口（默认）

**活跃时间：** 上午8:00 - 下午8:00（12小时）

**适用场景：**
- 你在这些时间段内有空
- 任务不紧急
- 希望工作时间有规律

**心跳频率：** 每2小时一次（每天6次）

### 扩展窗口

**活跃时间：** 上午6:00 - 下午10:00（16小时）

**适用场景：**
- 需要更长的工作时间
- 你的工作时间不固定

**心跳频率：** 每2小时一次（每天8次）

### 有限窗口

**活跃时间：** 上午10:00 - 下午6:00（8小时）

**适用场景：**
- 需要控制任务执行频率
- 你的工作时间有限

**心跳频率：** 每2-3小时一次（每天3-4次）

---

## 令牌预算

**建议：** 每天4-6次任务，每次任务消耗约5-10K令牌，总计每天20-60K令牌

**任务执行策略：**

| 窗口类型 | 每天任务次数 | 每次任务消耗令牌数 | 时间安排 |
|------------|--------------|--------|----------|
| 全天窗口（12小时） | 6次 | 30-60K令牌 | 每2小时一次 |
| 扩展窗口（16小时） | 8次 | 40-80K令牌 | 每2小时一次 |
| 有限窗口（8小时） | 4次 | 20-40K令牌 | 每2-3小时一次 |

**停止使用的条件：**
- 窗口关闭（基于时间）
- 令牌剩余量少于5K
- 队列为空
- 你需要处理紧急的人类请求

---

## 紧急任务优先处理

**定义：** 无法等待窗口开启的任务

**使用 `@priority:urgent` 标签将其添加到队列：**
```markdown
## 🔴 Ready
- [ ] @priority:urgent Emergency: [task description]
```

**处理方式：**
- 即刻开始执行，无论是否在窗口内
- 优先处理紧急任务，之后再检查窗口状态

---

## 窗口关闭时的处理流程

**如果在任务进行中窗口关闭：**

1. 检查任务进度：
   - 如果已完成超过80% → 完成任务
   - 如果完成度低于80% → 保存进度，将任务状态改为“进行中”，然后停止

2. 保存任务状态：
```markdown
## 🟡 In Progress
- [ ] @agent: @priority:high [Task description]
  - Started: 2026-02-16 19:30 UTC
  - Progress at window close: Completed X section, need to do Y
  - Resume: 2026-02-17 08:00 UTC (next window)
```

3. 在 `tasks/MODE_HISTORY.md` 中记录窗口关闭的状态：
```markdown
## [2026-02-16 20:00 UTC] Window Closed
Status: Task in progress (60% complete)
Action: Saved state, will resume in next window
```

---

## 运行模式历史记录

文件：`tasks/MODE_HISTORY.md`

```markdown
# Window Mode Transitions

## [2026-02-16 08:00 UTC] Window Opened
Mode: Daytime window
Queue state: 3 tasks ready
Expected sessions: 6

## [2026-02-16 20:00 UTC] Window Closed
Mode: Overnight (standby)
Sessions completed: 5
Tasks completed: 4
Tasks remaining: 1 (in progress, resume tomorrow)

## [2026-02-17 08:00 UTC] Window Opened
Mode: Daytime window
Resumed task in progress
```

---

## 与Cron作业的协调

**白天（自主运行模式开启时：**
- 轻量级Cron作业（如Ollama监控、磁盘检查）可以正常运行，不会与自主运行模式冲突
- 重负载Cron作业（如备份）会在执行期间暂停自主运行模式

**夜间（自主运行模式关闭时：**
- 所有Cron作业都可以自由执行
- 不会有自主运行模式与Cron作业的冲突

**Cron作业时间表：**

| 时间 | 作业名称 | 运行模式 |
|------|----------|---------------|
| 每5分钟 | Ollama监控 | 任何模式（影响较小） |
| 每小时 | 磁盘检查 | 任何模式（影响较小） |
| 00:00 | GitHub 备份 | 关闭（夜间执行） |
| 03:00 | 临时文件清理 | 关闭（夜间执行） |
| 08:00 | 窗口开启 | 启用自主运行模式 |
| 12:00 | GitHub 备份 | 启用自主运行模式（备份期间暂停） |
| 14:00 | 日常操作 + 内存管理 | 启用自主运行模式（期间暂停） |
| 20:00 | 窗口关闭 | 关闭自主运行模式（夜间执行） |
| 23:00 | 日常操作 + 内存管理 | 关闭自主运行模式（夜间执行） |

---

## 与GOALS.md的集成

将队列任务与代理的长期目标（**赚钱**）关联起来：

**在 `GOALS.md` 中添加相关任务链接：**
```markdown
- [ ] @priority:high Competitor pricing analysis (GOAL: monetization strategy)
- [ ] @priority:medium Write sales email template (GOAL: improve conversion)
```

**在窗口内朝向目标努力：**
- 在窗口开始时进行研究性任务（获取新信息）
- 在窗口中期进行写作任务 |
- 在窗口结束时进行任务回顾 |

---

## 学习成果的整合

完成任务后，将学习成果添加到 `.learnings/` 文件中：

```markdown
## [LRN-20260216-001] task-completion
Task: [Task description]

Completed during: Daytime window (14:00-14:25 UTC)
Tokens used: 8K

Key findings: [summarize]
```

---

## 日常工作流程

### 窗口开启（上午8:00）

1. 检查队列中是否有关于 🔴 的任务
2. 选择优先级最高的任务
3. 工作15-30分钟
4. 更新任务状态（改为“进行中”或“已完成”）

### 在窗口内（上午9:00 - 下午8:00）

1. 每2小时发送一次心跳信号，检查队列
2. 处理下一个优先级最高的任务
3. 完成任务后更新队列状态
4. 将任务进度记录到 `memory/[today].md` 文件中

### 窗口关闭（晚上8:00）

1. 检查是否有正在进行中的任务
2. 如果有：保存进度或完成任务
3. 将任务状态改为“已完成”或“进行中”
4. 在 `tasks/MODE_HISTORY.md` 中记录状态变化
5. 切换到待机模式（仅发送 `HEARTBEAT_OK`）

### 夜间（晚上8:00 - 上午8:00）

1. 每次心跳信号时仅检查紧急任务
2. 如果没有紧急任务：发送 `HEARTBEAT_OK`
3. 允许Cron作业自由执行
4. 不进行自主任务

---

## 任务输出格式

```markdown
## Task: [Title]

**Completed during:** [Window type] [Time range]
**Duration:** X minutes
**Tokens:** YK

### Work Done
[Describe what was accomplished]

### Output
[Attach output file or content]

### Next Steps
[What to do next - add to Ideas if task spawns follow-up]
```

---

## 随时间逐步优化

**逐步优化策略：**

这种模式允许代理**逐渐承担更多工作**：

**第1-2周：**
- 保守使用：每天4次任务，使用有限的时间窗口
- 监控运行效果，调整时间表

**第3-4周：**
- 扩大任务量：每天6次任务，根据需要扩展时间窗口
- 向队列中添加更多类型的任务

**第2个月：**
- 根据代理的实际时间和最高效率时段优化时间窗口
- 根据学习到的经验进行调整

**关键点：** 从小处开始，根据反馈和效果逐步扩展

---

## 适用场景

**何时使用此技能：**
- 当你需要**规律的工作时间表**时
- 当你希望代理在**特定时间段**内自主运行时
- 当任务**不紧急**（可以等待窗口开启）时
- 当你希望**明确区分自主运行模式和系统维护时间**时
- 当你愿意**逐步改进**运行模式时（从小处开始，逐步扩展）

---

**不适用场景**

**何时不使用此技能：**
- 当你需要**全天候自主运行**时 → 使用基于任务类型的过滤机制
- 当任务**高度时间敏感**时 → 使用紧急任务优先处理机制或其他方法
- 当你需要根据**任务类型**而不是时间来安排任务时 → 使用基于任务类型的自主运行模式
- 当你在**非标准工作时间**需要代理运行时 → 根据实际情况调整时间窗口

---

## 快速参考

**默认时间窗口：** 上午8:00 - 下午8:00（可调整）
**任务执行频率：** 在窗口内每2-3小时一次
**优先级顺序：** `紧急`（优先处理）→ `高优先级` → `中等优先级` → `低优先级`
**队列文件位置：** `tasks/QUEUE.md`

---

*请参阅 `templates/QUEUE.md` 以获取完整的模板结构*