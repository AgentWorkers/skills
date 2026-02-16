---
name: autonomy-type-based
version: 1.0.0
description: 基于类型的自主任务队列系统。该系统根据任务类型（研究、写作、分析、维护）对任务进行分类，仅让自动化系统处理能够创造价值的任务，而使用 cron 工具来处理维护任务。当您希望针对特定类型的任务实现自动化处理、最大化代币（token）的使用效率，并明确区分自动化工作与计划维护任务之间的职责时，可以使用该系统。
metadata:
  openclaw:
    emoji: "🏷️"
    category: productivity
---
# 基于类型的自主性

将你的代理从反应式系统转变为在**特定任务类型**上具备自主执行能力的系统。

---

## 概念

该代理会从 `tasks/QUEUE.md` 中获取任务，但**仅执行带有特定类型标签的任务**：

```
📚 Research  → ✅ Autonomy works on these
✍️ Writing   → ✅ Autonomy works on these
🔍 Analysis  → ✅ Autonomy works on these

🧹 Maintenance → ❌ Autonomy SKIPS these (cron handles)
💾 Backup      → ❌ Autonomy SKIPS these (cron handles)
```

Cron 作业负责处理备份、清理和安全审计等工作；而自主系统则负责研究、写作和分析任务。

---

## 工作原理

### 1. 任务队列结构

`tasks/QUEUE.md` 中的每个任务都带有 `@type:` 标签：

```markdown
## 🔴 Ready

### 📚 Research (@type:research)
- [ ] @priority:high @type:research Competitor pricing for X product
- [ ] @priority:medium @type:research Ollama model alternatives

### ✍️ Writing (@type:writing)
- [ ] @priority:medium @type:writing Blog post on memory systems
- [ ] @priority:low @type:writing Documentation update

### 🔍 Analysis (@type:analysis)
- [ ] @priority:medium @type:analysis Review weekly metrics
- [ ] @priority:low @type:analysis Analyze token patterns

### 🧹 Maintenance (@type:maintenance)
→ Autonomy IGNORES, cron handles
- [ ] @priority:medium @type:maintenance Old log cleanup
```

### 2. 心跳机制（Heartbeat Flow）

**过滤逻辑：**
- 读取所有标记为 “Ready” 的任务
- **仅** 选择 `@type:research` | `@type:writing` | `@type:analysis` 类型的任务
- **跳过** `@type:maintenance` | `@type:backup` | `@type:security` 类型的任务

### 3. 任务完成流程

```
1. Mark task as In Progress: @agent: @type:research [task description]
2. Work on it
3. Move to Done Today with completion notes
4. Log to memory/[today].md
5. Check GOALS.md and .learnings/ for follow-up tasks
```

---

## 任务类型

### 研究 (@type:research)

**定义：** 信息收集、调查、发现

**示例：**
- 竞争对手分析
- API 文档研究
- 技术探索
- 市场调研
- 最佳实践调查

**输出格式：**
```markdown
## Research: [Topic]

### Findings
- Key point 1
- Key point 2

### Sources
- [Source 1](url)
- [Source 2](url)

### Recommendations
- Recommendation 1
- Recommendation 2
```

**后续任务：** 将相关任务添加到 “Ideas” 列表中以待处理：

```markdown
- [Idea: @type:analysis @priority:medium Analyze research findings for X]
```

---

### 写作 (@type:writing)

**定义：** 内容创作、文档编写、沟通

**示例：**
- 博文撰写
- 文档更新
- 电子邮件草稿
- 公告发布
- 教程编写

**输出格式：**
```markdown
# [Title]

[Content]
```

**完成后的处理：**
- 如果是电子邮件：添加到 “Ideas” 列表中，等待审核
- 如果是文档：添加到 “Ideas” 列表中，等待发布
- 如果是公告：添加到 “Ideas” 列表中，等待分发

---

### 分析 (@type:analysis)

**定义：** 数据审查、指标分析、模式识别

**示例：**
- 周度性能评估
- 代币使用情况分析
- 日志分析
- 趋势识别
- 指标仪表盘制作

**输出格式：**
```markdown
## Analysis: [Topic]

### Data Reviewed
- [List of data sources]

### Key Findings
- Finding 1 with metric
- Finding 2 with metric

### Patterns
- Pattern 1
- Pattern 2

### Recommendations
- Action 1
- Action 2
```

**后续任务：** 根据分析结果添加相应的后续任务：

```markdown
- [Idea: @type:writing @priority:medium Write analysis report]
- [Idea: @type:research @priority:low Investigate pattern X further]
```

---

### 维护 (@type:maintenance)

**定义：** 系统维护、整理、常规任务

**处理方式：** 由 Cron 作业处理（非自主系统执行）

**示例：**
- 清理旧日志
- 删除临时文件
- 整理文件
- 归档旧记录

**行为：**
- 自主系统会跳过这些任务
- Cron 作业会在夜间自动执行这些任务
- 如有紧急情况可手动触发，但通常不需要

---

### 备份 (@type:backup)

**定义：** 数据备份、版本控制、同步

**处理方式：** 由 Cron 作业处理（非自主系统执行）

**示例：**
- GitHub 数据备份
- 数据库备份
- 数据同步到云端

**行为：**
- 自主系统会跳过这些任务
- 备份任务每天在 UTC 时间 00:00 和 12:00 自动执行

---

### 安全 (@type:security)

**定义：** 安全检查、审计、漏洞扫描

**处理方式：** 由 Cron 作业处理（非自主系统执行）

**示例：**
- 安全审计
- 权限检查
- 凭据审核

**行为：**
- 自主系统会跳过这些任务
- 安全审计任务每月在月初自动执行

---

## 优先级系统

优先级决定了任务的执行顺序：

| 优先级 | 使用场景 | 选择规则 |
|----------|-------------|-----------|
| `@priority:urgent` | 时间敏感、截止日期在 24 小时内 | 首先执行 |
| `@priority:high` | 重要任务、截止日期在 2-3 天内 | 第二个执行 |
| `priority:medium` | 一般重要性 | 最后执行 |
| `priority:low` | 可选任务、无截止日期 | 最后执行 |

---

## 与 `GOALS.md` 的集成

所有任务都应支持代理的长期目标：**盈利**  

**创建任务时：**
- 查看 `GOALS.md` 中的当前目标
- 将任务与盈利相关的活动关联起来
- 问自己：“这个任务如何帮助代理实现盈利？”

**示例：**

```markdown
### 📚 Research
- [ ] @priority:high @type:research Competitor pricing (GOAL: pricing strategy for new product)
- [ ] @priority:medium @type:research Market fit analysis (GOAL: validate product idea)
```

```markdown
### ✍️ Writing
- [ ] @priority:high @type:writing Sales email template (GOAL: improve conversion)
- [ ] @priority:medium @type:blog Marketing post (GOAL: drive traffic)
```

**任务完成后的处理：**
- 如有必要，将任务完成情况更新到 `GOALS.md` 中
- 将有助于实现目标的后续任务添加到 “Ideas” 列表中

---

## 与 `.learnings/` 的集成

完成任务后，将相关学习内容添加到 `.learnings/` 文件中：

**完成研究任务后：**
```markdown
## [LRN-20260216-001] research-findings
Research: Competitor pricing analysis

Key findings: [summarize]
```

**完成分析任务后：**
```markdown
## [LRN-20260216-002] analysis-insights
Analysis: Token usage patterns

Key insights: [summarize]
```

**解决问题后：**
```markdown
## [ERR-20260216-001] research-issue
Error: API rate limit during research

Fix: [document the fix]
```

---

## 队列管理

### 添加任务

**代理可以直接将任务添加到队列中：**
```markdown
## 🔴 Ready
- [ ] @type:research @priority:high Analyze competitor X pricing
```

**代理在工作过程中发现任务后，会将其添加到 “Ideas” 列表中：**
```markdown
## 💡 Ideas
- [Idea: @type:research @priority:medium Investigate Ollama alternative models]
```

### 更新任务状态

**任务开始时：**
```markdown
## 🟡 In Progress
- [ ] @agent: @type:research @priority:high Competitor pricing analysis
  - Started: 2026-02-16 14:00 UTC
  - Progress: Gathering data
```

**任务完成时：**
```markdown
## ✅ Done Today
- [x] @agent: @type:research @priority:high Competitor pricing analysis
  - Completed: 2026-02-16 14:25 UTC
  - Output: tasks/outputs/competitor-pricing-analysis.md
```

**任务被阻塞时：**
```markdown
## 🔵 Blocked
- [ ] @type:writing @priority:medium Email draft (needs: RA review)
```

### 清理今日已完成的任务**

**每日例行操作（在心跳机制或 Cron 作业执行时）：**
- 将已完成的任务从 “Done Today” 区域移动到 `tasks/archive/`（如果需要保留历史记录）
- 或者直接删除这些任务
- 清空 “Done Today” 区域（显示 “## ✅ Done Today”）

---

## 代币预算

**建议：** 每天使用 4 次任务处理机会，每次使用 3-8K 个代币，总计 12-32K 个代币

**任务处理时间安排：**
| 时间 | 任务类型 | 代币消耗 | 重点任务 |
|------|-----------|--------|-------|
| 上午 9:00 | 研究 | 8-10K | 深度分析 |
| 下午 1:00 | 写作 | 5-7K | 内容创作 |
| 下午 5:00 | 分析 | 3-5K | 数据审查 |
| 下午 9:00 | 学习 | 2-3K | 学习总结 |

**停止使用的条件：**
- 如果当天剩余代币少于 5K
- 如果队列中没有符合要求的任务类型
- 如果代理正在处理其他紧急任务（优先级更高）

---

## 与 Cron 的协调

自主系统和 Cron 作业并行运行，但处理的任务类型不同：

| 系统 | 任务类型 | 安排时间 |
|--------|-----------|----------|
| **自主系统** | 研究、写作、分析 | 随时（由心跳机制驱动） |
| **Cron** | 备份、维护、安全 | 按预定时间（午夜、中午、每天） |

**两者之间没有冲突**——它们处理的任务完全不同。

---

## 何时使用此技能

在以下情况下使用此技能：
- 当你希望代理专注于**能创造价值的任务**（如研究、写作、分析）
- 当你希望**最大化代币使用效率**时
- 当任务类型可以**明确分类**时
- 当你希望**后续扩展任务类型**（例如添加编码、测试等）时
- 当你希望**明确区分自主执行任务和维护任务**时

---

## 何时不使用此技能

在以下情况下不要使用此技能：
- 当你需要持续处理所有类型的任务时 → 使用 `autonomy-windowed` 技能
- 当任务类型不明确或容易混淆时 → 使用更简单的任务管理方式
- 当你需要代理处理维护任务时 → 这些任务应由 Cron 作业完成
- 当你需要固定的工作时间安排时 → 使用基于时间的 `autonomy-windowed` 功能

---

## 快速参考

**自主系统处理的任务类型：** `@type:research` | `@type:writing` | `@type:analysis`
**Cron 作业处理的任务类型：** `@type:maintenance` | `@type:backup` | `@type:security`
**优先级顺序：** `urgent` → `high` → `medium` → `low`
**任务存储位置：** `tasks/QUEUE.md`

---

*请参阅 `templates/QUEUE.md` 以获取完整的模板结构*