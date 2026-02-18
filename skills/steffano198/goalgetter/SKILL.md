---
name: goalgetter
description: "通过简单的 Markdown 文件来管理任务和目标。可以创建、跟踪并完成任务和目标，并支持任务完成的进度记录（即“连击”功能）。数据存储在 `~/.openclaw/goalgetter/` 目录中。支持的触发命令包括：`add task`（添加任务）、`new goal`（添加目标）、`task done`（任务完成）、`show tasks`（显示任务列表）、`goal streak`（查看目标完成进度）以及 `complete task`（完成特定任务）。"
author: DevSef
version: 1.0.0
tags: [tasks, goals, productivity, habits, streaks, markdown]
---
# Goal Getter - 使用 Markdown 追踪任务和目标

这是一个简单的任务和目标跟踪工具，完全基于纯 Markdown 文件实现，无需任何外部依赖。

## 数据存储位置

默认路径：`~/.openclaw/goalgetter/`

文件结构：
- `tasks.md`：待办事项列表
- `goals.md`：目标跟踪记录（包括完成进度）
- `done/`：已完成任务的存档文件夹

## 命令

### 任务管理

**添加任务：**
```bash
echo "- [ ] $TEXT" >> ~/.openclaw/goalgetter/tasks.md
```

**完成任务：**
```bash
# Read tasks.md, find task, move to done/TIMESTAMP.md, mark complete
```

**查看任务列表：**
```bash
cat ~/.openclaw/goalgetter/tasks.md
```

### 目标管理

**添加目标：**
```bash
echo "## $GOAL_NAME" >> ~/.openclaw/goalgetter/goals.md
echo "- streak: 0" >> ~/.openclaw/goalgetter/goals.md
echo "- created: $DATE" >> ~/.openclaw/goalgetter/goals.md
echo "- log:" >> ~/.openclaw/goalgetter/goals.md
```

**标记目标为已完成：**
```bash
# Read goals.md, increment streak, add date to log
```

**查看目标完成进度：**
```bash
# Read goals.md and display each goal with current streak
```

## 文件格式

### tasks.md
```markdown
# Tasks

- [ ] Buy groceries
- [x] Call dentist
- [ ] Finish SAAS research
```

### goals.md
```markdown
# Goals

## Meditation
- streak: 5
- created: 2026-01-15
- log:
  - 2026-01-15
  - 2026-01-16
  - 2026-01-17
  - 2026-01-18
  - 2026-01-19

## Exercise
- streak: 2
- created: 2026-02-01
- log:
  - 2026-02-15
  - 2026-02-16
```

## 使用示例

| 用户操作 | 动作 |
|-----------|--------|
| “添加任务：完成报告” | 将任务添加到 tasks.md 文件中 |
| “查看我的任务” | 查看 tasks.md 文件中的所有任务 |
| “完成任务：完成报告” | 将任务标记为已完成，并移至 done/ 文件夹 |
| “新增目标：冥想” | 将目标添加到 goals.md 文件中 |
| “完成了冥想” | 更新目标完成进度，并记录日期 |
| “查看目标的完成进度” | 显示该目标的完成进度 |
| “我的冥想目标进展如何？” | 查看该目标的完成进度 |

## 注意事项：

- 如果目录 `~/.openclaw/goalgetter/` 不存在，请先创建它。
- 请使用 ISO 格式（YYYY-MM-DD）来记录日期，以确保数据的一致性。
- 修改文件前，请使用 `read` 工具查看当前文件内容。
- 使用 `write` 工具来更新文件内容。