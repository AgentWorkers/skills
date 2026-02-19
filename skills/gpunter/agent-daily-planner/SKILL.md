# 代理每日计划器 📋

这是一个专为 AI 代理设计的结构化每日计划与执行跟踪系统，帮助您整理任务、追踪已完成的工作，并在会话之间保持责任清晰。

## 该工具的必要性

代理在会话之间可能会丢失上下文。如果没有计划系统，您会浪费时间重新适应环境，而无法专注于实际工作。这个工具能帮助您建立一种可复制的每日工作流程，确保工作在会话之间持续进行。

## 命令

### `/plan today`
根据以下信息生成当天的计划：
- 昨天未完成的任务
- 来自 `memory/projects.json` 的活跃项目（如果存在）
- `MEMORY.md` 中记录的任何阻碍因素或截止日期

创建/更新 `memory/YYYY-MM-DD.md` 文件，文件采用结构化模板：

```markdown
# YYYY-MM-DD - Daily Plan

## Priority Tasks (Must Do)
- [ ] Task 1 — [project] — deadline/context
- [ ] Task 2 — [project] — deadline/context

## Stretch Goals (If Time)
- [ ] Task 3
- [ ] Task 4

## Blockers
- Blocker 1 — who can unblock this?

## Shipped Today
_(fill as you complete tasks)_

## Notes
_(learnings, decisions, context for future sessions)_
```

### `/plan review`
查看当天的进度：
- 统计已完成与未完成的任务数量
- 识别逾期项目
- 计算完成率
- 提出需要延续到明天的任务

### `/plan ship <描述>`
记录您已完成的工作，并添加到当天的“今日已完成”部分，同时附上时间戳。
示例：`/plan ship "在 ClawHub 上发布了 skill-auditor"`

### `/plan block <描述> [负责人]`
记录一个阻碍因素。可选地标记需要解决该问题的人。
示例：`/plan block "Post Bridge SSL 出现故障" George`

### `/plan week`
从每日日志中生成每周总结：
- 完成的总任务数量
- 完成率趋势
- 收入事件（如果有的话）
- 重要的决策
- 已解决/未解决的阻碍因素

### `/plan standup`
生成一个简短的每日站会报告格式：
```
Yesterday: [completed tasks]
Today: [planned tasks]
Blockers: [current blockers]
```

### `/plan priorities <任务1> <任务2> ...`
设置当天的优先级任务。这会覆盖“优先任务”部分的内容。

### `/plan carry`
将昨天未完成的任务延续到今天的计划中。

## 文件结构

该计划器与您的现有记忆系统协同工作：
```
memory/
  YYYY-MM-DD.md    — Daily logs (one per day)
  projects.json    — Active projects (optional)
  weekly/
    YYYY-Wxx.md    — Weekly summaries
```

## 集成

该工具可以与其他工具一起使用，不会修改它不管理的文件。它读取以下文件：
- `MEMORY.md` — 用于获取上下文和持续记录
- `memory/projects.json` — 用于跟踪活跃项目
- 前一天的 `memory/YYYY-MM-DD.md` — 用于延续任务

## 使用建议

1. 每次会话开始时运行 `/plan today`
2. 每完成一项工作后运行 `/plan ship`（以记录进度）
3. 会话结束前运行 `/plan review`
4. 每周日/周一使用 `/plan week` 进行总结
5. 站会报告格式非常适合向团队成员更新进度

## 作者
- CLAW-1 (@Claw_00001)
- 发布者：Gpunter（在 ClawHub 上）

## 版本
1.0.0

## 标签
生产力、计划、任务、每日日志、责任、工作流程、组织