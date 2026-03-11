---
name: todo
description: |
  **macOS Only** - Manage macOS Reminders app via AppleScript.
  Full-featured reminder management: add, list, complete, delete, search, create lists, and more.
  
  **Note: This skill is macOS-only**, requiring the native Reminders app.
  
  Use cases:
  - Create reminders with due dates and priorities
  - List reminders from specific lists or incomplete ones
  - Mark reminders as complete/uncomplete
  - Delete reminders
  - Search reminders by title or content
  - Create new reminder lists
  - View today's due reminders
---

# 待办事项列表（Mac）

## ⚠️ 系统要求

本功能仅适用于 macOS，需要使用原生的 Reminders 应用程序。在非 Mac 系统上无法使用。

## 功能概述

本功能通过 AppleScript 与 macOS 的 Reminders 应用程序进行交互，支持完整的待办事项管理流程：

| 功能 | 命令                |
|---------|-------------------|
| 添加待办事项 | `todo add`           |
| 查看待办事项列表 | `todo list`          |
| 标记为已完成 | `todo complete`        |
| 取消标记为已完成 | `todo uncomplete`       |
| 删除待办事项 | `todo delete`          |
| 搜索待办事项 | `todo search`         |
| 创建待办事项列表 | `todo create-list`       |
| 查看今日待办事项 | `todo today`         |

## 使用方法

所有操作均通过 `scripts/todo.sh` 脚本执行：

```bash
./scripts/todo.sh <action> [args...]
```

### 1. 添加待办事项

```bash
# Basic usage
./scripts/todo.sh add "title" "notes" "date" "list" "priority" "recur"

# Example: Simple reminder
./scripts/todo.sh add "Buy milk" "" "" "" 0 ""

# Example: With due date
./scripts/todo.sh add "Submit report" "Q4 summary" "2025-02-10 14:00" "" 1 ""

# Example: Add to specific list
./scripts/todo.sh add "Buy eggs" "Buy 12" "" "Shopping" 5 ""

# Example: High priority + list + date
./scripts/todo.sh add "Important meeting" "Client call" "2025-02-05 10:00" "Work" 1 ""
```

**优先级等级：**
- `0` = 无优先级
- `1` = 高（🔴）
- `5` = 中等（🟡）
- `9` = 低（🔵）

### 2. 查看待办事项列表

```bash
# List incomplete reminders from default list
./scripts/todo.sh list

# List from specific list
./scripts/todo.sh list "Shopping"

# Include completed reminders
./scripts/todo.sh list "" true

# List all from specific list (including completed)
./scripts/todo.sh list "Work" true
```

### 3. 标记为已完成/未完成

```bash
# Mark complete (supports fuzzy matching)
./scripts/todo.sh complete "Buy milk"

# Unmark complete
./scripts/todo.sh uncomplete "Buy milk"
```

### 4. 删除待办事项

```bash
# Delete reminder (supports fuzzy matching)
./scripts/todo.sh delete "Buy milk"
```

⚠️ 删除操作是不可逆的，请谨慎使用。

### 5. 搜索待办事项

```bash
# Search by keyword in title or content
./scripts/todo.sh search "meeting"
```

### 6. 管理待办事项列表

```bash
# View all lists with stats
./scripts/todo.sh lists

# Create new list
./scripts/todo.sh create-list "Study Plan"
```

### 7. 查看今日的待办事项

```bash
# View today's incomplete due reminders
./scripts/todo.sh today
```

## 完整的使用流程示例

```bash
# 1. Create a work list
./scripts/todo.sh create-list "Work"

# 2. Add work tasks
./scripts/todo.sh add "Finish Q4 report" "Compile data" "2025-02-05 17:00" "Work" 1 ""
./scripts/todo.sh add "Reply to client email" "" "" "Work" 5 ""
./scripts/todo.sh add "Team weekly" "Prepare slides" "2025-02-06 10:00" "Work" 1 ""

# 3. View work list
./scripts/todo.sh list "Work"

# 4. Complete a task
./scripts/todo.sh complete "Reply to client email"

# 5. Check today's todos
./scripts/todo.sh today
```

## 用户交互提示

当用户需要管理待办事项时：
1. **明确用户需求** - 询问用户想要执行的具体操作（添加、查看、完成等）。
2. **提供快捷方式** - 对于常见的操作（如“提醒我……”），可以直接使用 `todo add` 命令。
3. **显示操作结果** - 显示操作结果和当前待办事项列表的状态。
4. **支持模糊匹配** - 在完成、删除或搜索时支持模糊匹配。

## 注意事项：
1. **日期格式** - 支持自然格式，如 “2025-02-05”、“2025年2月5日” 或 “明天”。
2. **模糊匹配** - 在完成、删除或搜索时，输入部分内容即可匹配到相关待办事项，无需输入完整标题。
3. **权限** - 首次运行时，macOS 可能会请求权限以控制 Reminders 应用程序，请点击 “允许”。
4. **同步** - 所有更改会同步到 iCloud，并在其他 Apple 设备上显示。
5. **重复性待办事项** - 由于 AppleScript 的限制，复杂的重复性设置需要手动在应用程序中进行配置。