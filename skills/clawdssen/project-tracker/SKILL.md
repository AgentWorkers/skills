---
name: project-tracker
version: "1.0.0"
description: 多项目跟踪工具，具备状态仪表板、里程碑跟踪功能、停滞项目检测机制、优先级评分系统以及自动生成的每周进度报告。
tags: [project-management, tracker, dashboard, milestones, progress-reports, weekly-review, priority-scoring, stalled-detection, side-projects, portfolio]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 项目跟踪器

在一个地方跟踪所有项目，了解哪些项目正在推进中，哪些项目停滞不前，以及哪些项目应该被终止。

**由 The Agent Ledger 提供** — [theagentledger.com](https://theagentledger.com)

## 设置

创建 `projects/` 目录和 `projects/DASHBOARD.md` 文件：

```markdown
# Project Dashboard

Last updated: [date]

| Project | Status | Priority | Next Action | Due |
|---------|--------|----------|-------------|-----|

## Active Projects
<!-- Agent maintains this section -->

## On Hold
<!-- Paused but not abandoned -->

## Completed
<!-- Archive of finished work -->
```

## 工作原理

### 添加项目

当用户提到一个新的项目时，会创建 `projects/<项目名称>.md` 文件：

```markdown
# Project: [Name]

**Status:** 🟢 Active | 🟡 On Hold | 🔴 Blocked | ✅ Done
**Priority:** P1 (critical) | P2 (important) | P3 (nice-to-have)
**Started:** [date]
**Target:** [deadline or "ongoing"]
**One-liner:** [what this project is in one sentence]

## Milestones

- [ ] Milestone 1 — [description] — [target date]
- [ ] Milestone 2 — [description] — [target date]

## Progress Log

### [date]
- What happened today

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|

## Blockers

- [blocker] → [who/what can unblock it]
```

### 仪表盘更新

在以下情况下更新 `projects/DASHBOARD.md` 文件：
- 项目状态发生变化
- 一个里程碑完成
- 添加了一个新项目
- 在每周的审查过程中

### 停滞项目的检测

如果项目满足以下条件，则被视为**停滞项目**：
- 超过 7 天没有进度记录
- 状态显示为“活跃”，但近期没有里程碑进展
- 存在超过 3 天未解决的障碍因素

在每日简报或心跳检查中标记停滞项目：
> ⚠️ **停滞项目：** [项目名称] — [N] 天内没有更新。继续进行、暂停还是终止？

### 每周审查格式

每周日（或根据需求）生成报告：

```markdown
# Weekly Project Review — [date range]

## Summary
- **Active:** [N] projects
- **Completed this week:** [list]
- **Stalled:** [list]
- **New:** [list]

## Per-Project Status
### [Project Name]
- **Progress:** [what moved]
- **Blockers:** [any]
- **Next week:** [planned actions]

## Recommendations
- [Kill/pause/accelerate suggestions based on patterns]
```

### 优先级评分

当用户同时管理多个项目时，可以使用此工具来帮助确定项目的优先级：

| 评分因素 | 权重 | 分数（1-5） |
|--------|--------|-------------|
| 收入潜力 | 30% | |
| 完成时间 | 20% | |
| 战略一致性 | 25% | |
| 个人精力/兴趣 | 15% | |
| 依赖性（影响其他工作） | 10% | |

**加权得分 = Σ（权重 × 分数）**。得分低于 2.5 的项目被视为需要暂停或终止的候选对象。

## 集成

- **与每日简报集成**：将项目摘要包含在晨间简报中
- **与独立创业者助手集成**：将项目数据导入业务仪表盘
- **与记忆系统集成**：将项目决策记录在每日记忆文件中

## 自定义设置

- **审查频率**：每周（默认）、每两周或每月
- **停滞项目的阈值**：7 天（默认），可根据项目类型进行调整
- **仪表盘格式**：表格（默认）或看板式列表
- **优先级权重**：根据用户的需求调整评分因素

## 故障排除

| 问题 | 解决方法 |
|-------|-----|
| 仪表盘数据不同步 | 重新扫描 `projects/` 目录，并从各个文件重新生成数据 |
| 活动项目过多 | 运行优先级评分，建议暂停或终止排名最低的 30% 的项目 |
| 停滞项目检测过于敏感 | 对于周期较长的项目，提高停滞项目的阈值 |
| 进度记录缺失 | 设置每日提醒以记录项目进展**

---

*免责声明：本工具完全由 AI 生成，未经人工审核。仅用于提供信息和教育用途。使用前请仔细检查所有生成的文件。The Agent Ledger 对使用结果不承担任何责任。请自行承担风险。*

*由 [The Agent Ledger](https://theagentledger.com) 创建 — 一个专注于 AI 的 AI 工具开发者。*