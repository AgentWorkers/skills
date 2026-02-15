---
name: task-tracker
description: "个人任务管理，包括每日站会和每周回顾。适用场景如下：  
(1) 用户提到“每日站会”或询问自己当前的任务安排；  
(2) 用户提到“每周回顾”或询问上周的工作进展；  
(3) 用户希望添加、更新或完成任务；  
(4) 用户询问任务执行中遇到的障碍或截止日期；  
(5) 用户分享会议记录并希望从中提取相关任务信息；  
(6) 用户询问“本周需要完成的任务”或其他类似问题。"
homepage: https://github.com/kesslerio/task-tracker-clawdbot-skill
metadata: {"clawdbot":{"emoji":"📋","requires":{"files":["~/clawd/memory/work/TASKS.md"]},"install":[{"id":"init","kind":"script","script":"python3 scripts/init.py","label":"Initialize TASKS.md from template"}]}}
---

```html
<div align="center">

![任务跟踪器](https://img.shields.io/badge/Task_Tracker-ClawdbotSkill-blue?style=for-the-badge&logo=checklist)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square&logo=python)
![状态](https://img.shields.io/badge/Status-Production-green?style=flat-square)
![问题](https://img.shields.io/badge/Issues-0-black?style=flat-square)
![最后更新时间](https://img.shields.io/badge/Last_Updated-Jan_2026-orange?style=flat-square)

**个人任务管理工具，支持每日站会和每周回顾**

[主页](https://github.com/kesslerio/task-tracker-clawdbot-skill) • [功能介绍](#what-this-skill-does) • [命令参考](#commands-reference)

</div>
```

---

# 任务跟踪器

这是一个用于个人任务管理的工具，支持每日站会和每周回顾。它可以跟踪工作任务、显示优先级以及管理任务中的阻碍因素。

---

## 功能介绍

1. **列出任务**：按优先级、状态或截止日期筛选任务列表。
2. **每日站会**：显示当天的首要任务、阻碍因素以及已完成的任务。
3. **每周回顾**：总结上周的工作，归档已完成的任务，并规划本周的任务。
4. **添加任务**：创建新的任务，设置优先级和截止日期。
5. **完成任务**：将任务标记为已完成。
6. **从会议记录中提取任务**：从会议笔记中提取需要处理的任务。

---

## 文件结构

```
~/clawd/memory/work/
├── TASKS.md              # Active tasks (source of truth)
├── ARCHIVE-2026-Q1.md    # Completed tasks by quarter
└── WORKFLOW.md           # Workflow documentation
```

**TASKS.md 文件格式：**
```markdown
# Work Tasks

## 🔴 High Priority (This Week)
- [ ] **Set up Apollo.io** — Access for Lilla
  - Due: ASAP
  - Blocks: Lilla (podcast outreach)

## 🟡 Medium Priority (This Week)
- [ ] **Review newsletter concept** — Figma design
  - Due: Before Feb 1

## ✅ Done
- [x] **Set up team calendar** — Shared Google Calendar
```

---

## 快速入门

### 查看任务
```bash
python3 ~/clawd/skills/task-tracker/scripts/tasks.py list
```

### 每日站会
```bash
python3 ~/clawd/skills/task-tracker/scripts/standup.py
```

### 每周回顾
```bash
python3 ~/clawd/skills/task-tracker/scripts/weekly_review.py
```

---

## 命令参考

### 列出任务
```bash
# All tasks
tasks.py list

# Only high priority
tasks.py list --priority high

# Only blocked
tasks.py list --status blocked

# Due today or this week
tasks.py list --due today
tasks.py list --due this-week
```

### 添加任务
```bash
# Simple
tasks.py add "Draft project proposal"

# With details
tasks.py add "Draft project proposal" \
  --priority high \
  --due "Before Mar 15" \
  --blocks "Sarah (client review)"
```

### 完成任务
```bash
tasks.py done "proposal"  # Fuzzy match - finds "Draft project proposal"
```

### 显示阻碍因素
```bash
tasks.py blockers              # All blocking tasks
tasks.py blockers --person sarah  # Only blocking Sarah
```

### 从会议记录中提取任务
```bash
extract_tasks.py --from-text "Meeting: discuss Q1 planning, Sarah to own budget review"
# Outputs: tasks.py add "Discuss Q1 planning" --priority medium
#          tasks.py add "Sarah to own budget review" --owner sarah
```

---

## 优先级等级

| 图标 | 含义 | 使用场景 |
|------|---------|-------------|
| 🔴 **高** | 关键任务，具有截止日期，会阻碍其他任务的进展 | 影响收入，可能阻碍团队进度 |
| 🟡 **中** | 重要但不紧急 | 需要审核、提供反馈或进行规划 |
| 🟢 **低** | 需要监控或委托他人处理 | 等待他人回复或属于待办事项 |

---

## 状态管理流程

```
Todo → In Progress → Done
      ↳ Blocked (waiting on external)
      ↳ Waiting (delegated, monitoring)
```

---

## 自动化设置（Cron 任务）

| 任务 | 执行时间 | 执行内容 |
|-----|------|------|
| 每日站会 | 工作日 8:30 AM | 将站会内容发布到 Telegram 日志群组 |
| 每周回顾 | 星期一 9:00 AM | 发布每周回顾总结，并归档已完成的任务 |

---

## 自然语言指令

| 指令 | 功能 |
|---------|-----------|
| "daily standup" | 运行 standup.py，将站会内容发布到日志群组 |
| "weekly review" | 运行 weekly_review.py，发布每周回顾总结 |
| "what's on my plate?" | 列出所有任务 |
| "what's blocking Lilla?" | 显示阻碍 Lilla 的任务 |
| "mark IMCAS done" | 将指定的任务标记为已完成 |
| "what's due this week?" | 列出本周到期的任务 |
| "add task: X" | 向 TASKS.md 文件中添加任务 X |
| "extract tasks from: [notes]" | 从会议笔记中提取任务信息 |

---

## 使用示例

**晨间检查：**
```
$ python3 scripts/standup.py

📋 Daily Standup — Tuesday, January 21

🎯 #1 Priority: Complete project proposal draft
   ↳ Blocking: Sarah (client review)

⏰ Due Today:
  • Complete project proposal draft
  • Schedule team sync

🔴 High Priority:
  • Review Q1 budget (due: Before Mar 15)
  • Draft blog post (due: ASAP)

✅ Recently Completed:
  • Set up shared calendar
  • Update team documentation
```

**添加任务：**
```
$ python3 scripts/tasks.py add "Draft blog post" --priority high --due ASAP

✅ Added task: Draft blog post
```

**从会议记录中提取任务：**
```
$ python3 scripts/extract_tasks.py --from-text "Meeting: Sarah needs budget review, create project timeline"

# Extracted 2 task(s) from meeting notes
# Run these commands to add them:

tasks.py add "Budget review for Sarah" --priority high
tasks.py add "Create project timeline" --priority medium
```

---

## 集成方式

- **Telegram 日志群组**：自动发布站会和回顾总结。
- **Obsidian**：将每日站会内容记录到 `01-Daily/YYYY-MM-DD.md` 文件中。
- **MEMORY.md**：在每周回顾中展示常见的阻碍因素和重复出现的任务。
- **Cron 任务**：自动执行每日站会和每周回顾。

---

## 常见问题及解决方法

**“任务文件未找到”**
- 确保 `TASKS.md` 文件存在于 `~/clawd/memory/work/TASKS.md` 路径下。
- 检查文件格式是否正确（使用 `- [ ]` 标记复选框，文件开头是否有 `## 🔴` 标签）。
- 运行 `tasks.py list` 命令进行调试。

**日期解析问题**
- 支持的日期格式包括：`ASAP`、`YYYY-MM-DD`、`Before Mar 15`、`Before product launch`。
- `check_due_date()` 函数可以处理这些日期格式。

---

## 相关文件

| 文件 | 用途 |
|------|---------|
| `scripts/tasks.py` | 主要命令行工具：用于列出任务、添加任务、标记任务完成状态或归档任务 |
| `scripts/standup.py` | 生成每日站会内容的脚本 |
| `scripts/weekly_review.py` | 生成每周回顾内容的脚本 |
| `scripts/extract_tasks.py` | 从会议记录中提取任务信息的脚本 |
| `scripts/utils.py` | 公共辅助工具 |
| `scripts/init.py` | 从模板创建新的 TASKS.md 文件 |
| `references/task-format.md` | 任务格式规范文档 |
| `assets/templates/TASKS.md` | 新任务文件的模板格式 |
```