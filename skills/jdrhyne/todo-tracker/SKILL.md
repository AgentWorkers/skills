---
name: todo-tracker
description: 这是一个用于跨会话跟踪任务的持久性待办事项列表（TODO scratch pad）。当用户执行以下操作时，该功能会被触发：添加任务到待办列表（"add to TODO"）、查看待办事项列表（"what's on the TODO"）、标记任务已完成（"mark X done"）、显示待办事项列表（"show TODO list"）或删除任务（"remove from TODO"），同时也会在系统心跳（heartbeat）事件发生时检查是否有过期的待办事项并提醒用户。
---

# 待办事项追踪器（TODO Tracker）

在工作区中维护一个持续的 `TODO.md` 文件，用于记录待办事项。

## 文件位置

`TODO.md` 文件位于工作区的根目录下（例如：`/Users/nuthome/nuri-bot/TODO.md`）

## 命令

### 查看待办事项
当用户询问：“有哪些待办事项？”、“显示待办事项列表”或“有哪些未完成的任务？”时：
```bash
cat TODO.md
```
此时，需要按照优先级对待办事项进行汇总显示。

### 添加待办事项
当用户输入：“将 X 添加到待办事项列表中”或“TODO: X”时：
```bash
bash skills/todo-tracker/scripts/todo.sh add "<priority>" "<item>"
```
待办事项的优先级分为：`高`（high）、`中`（medium）和`低`（low）（默认为中等优先级）。

示例：
```bash
bash skills/todo-tracker/scripts/todo.sh add high "Ingest low-code docs"
bash skills/todo-tracker/scripts/todo.sh add medium "Set up Zendesk escalation"
bash skills/todo-tracker/scripts/todo.sh add low "Add user memory feature"
```

### 标记待办事项为已完成
当用户输入：“将 X 标记为已完成”或“X 已完成”时：
```bash
bash skills/todo-tracker/scripts/todo.sh done "<item-pattern>"
```
系统会将该待办事项移动到 “✅ 已完成”（Done）部分，并记录完成日期。

### 删除待办事项
当用户输入：“从待办事项列表中删除 X”时：
```bash
bash skills/todo-tracker/scripts/todo.sh remove "<item-pattern>"
```

### 按优先级排序显示待办事项
```bash
bash skills/todo-tracker/scripts/todo.sh list high
bash skills/todo-tracker/scripts/todo.sh list medium
bash skills/todo-tracker/scripts/todo.sh list low
```

## 心跳检测（Heartbeat Integration）

在系统进行心跳检测时，会执行以下操作：
1. 统计高优先级的待办事项数量。
2. 检查哪些待办事项已经超过 7 天未被处理。
3. 如果存在未处理的待办事项，会在心跳检测响应中包含相应的简要说明。

示例心跳检测流程：
```bash
bash skills/todo-tracker/scripts/todo.sh summary
```

## `TODO.md` 的格式要求
```markdown
# TODO - Nuri Scratch Pad

*Last updated: 2026-01-17*

## 🔴 High Priority
- [ ] Item one (added: 2026-01-17)
- [ ] Item two (added: 2026-01-15) ⚠️ STALE

## 🟡 Medium Priority
- [ ] Item three (added: 2026-01-17)

## 🟢 Nice to Have
- [ ] Item four (added: 2026-01-17)

## ✅ Done
- [x] Completed item (done: 2026-01-17)
```

## 显示待办事项时的响应格式
```
📋 **TODO List** (3 items)

🔴 **High Priority** (1)
• Ingest low-code docs

🟡 **Medium Priority** (1)  
• Zendesk escalation from Discord

🟢 **Nice to Have** (1)
• User conversation memory

⚠️ 1 item is stale (>7 days old)
```