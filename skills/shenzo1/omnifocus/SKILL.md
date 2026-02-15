---
name: omnifocus
description: "通过 JavaScript for Automation (JXA) 脚本来管理 OmniFocus 任务。当用户要求 Clawdbot 与 OmniFocus 进行交互时，可以使用这些脚本执行以下操作：  
(1) 将任务添加到收件箱；  
(2) 列出或搜索任务（包括收件箱中的任务、已完成的任务、已标记的任务、过期的任务以及即将到期的任务）；  
(3) 完成任务；  
(4) 更新任务属性（如备注、截止日期和标记）；  
(5) 获取 OmniFocus 的统计信息；  
(6) 报告任务状态；  
(7) 根据用户的查询在 OmniFocus 中执行相应操作。"
---

# OmniFocus 任务管理

通过 JavaScript for Automation (JXA) 脚本自动化 OmniFocus 的任务管理。

## 快速入门

所有脚本都位于 `scripts/` 目录中，并使用 JXA。运行方式如下：

```bash
osascript -l JavaScript scripts/<script-name>.js [args]
```

**核心脚本：**
- `add_task.js` - 向收件箱添加任务
- `list_tasks.js` - 使用过滤器列出任务
- `search_tasks.js` - 按关键词搜索任务
- `complete_task.js` - 根据名称完成任务
- `update_task.js` - 更新任务属性
- `get_stats.js` - 获取 OmniFocus 统计信息

## 核心操作

### 添加任务

```bash
osascript -l JavaScript scripts/add_task.js "Task name" ["Note"] ["YYYY-MM-DD"]
```

**示例：**
```bash
osascript -l JavaScript scripts/add_task.js "Buy groceries"
osascript -l JavaScript scripts/add_task.js "Review doc" "Check sections 1-3"
osascript -l JavaScript scripts/add_task.js "Submit report" "Q1" "2026-01-31"
```

**返回值：** 任务 ID

### 列出任务

```bash
osascript -l JavaScript scripts/list_tasks.js [filter] [limit]
```

**过滤器：**
- `inbox` - 收件箱中的任务
- `available` - 可用的（未阻塞）任务（默认）
- `flagged` - 被标记的任务
- `due-soon` - 3 天内到期的任务
- `overdue` - 过期的任务
- `all` - 所有未完成的任务

**返回值：** 包含任务详细信息的 JSON 数组（名称、ID、备注、截止日期、是否被标记、项目、标签）

### 搜索任务

```bash
osascript -l JavaScript scripts/search_tasks.js "keyword" [limit]
```

搜索任务名称和备注。搜索不区分大小写。

**返回值：** 匹配任务的 JSON 数组

### 完成任务

**首先在收件箱中搜索，然后在所有任务中搜索。** 完成第一个匹配到的任务。

### 更新任务

```bash
osascript -l JavaScript scripts/update_task.js "Task name" [--note "text"] [--due "YYYY-MM-DD"] [--flag true/false]
```

**示例：**
```bash
osascript -l JavaScript scripts/update_task.js "Review" --note "Added notes"
osascript -l JavaScript scripts/update_task.js "Submit" --due "2026-02-01"
osascript -l JavaScript scripts/update_task.js "Important" --flag true
```

### 获取统计信息

```bash
osascript -l JavaScript scripts/get_stats.js
```

**返回值：** 包含以下统计信息的 JSON：**
- 总任务数、未完成任务数、收件箱中的任务数
- 被标记的任务数、过期的任务数、3 天内到期的任务数
- 可用的任务数、被阻塞的任务数

## 使用指南

### 回应用户查询时

1. 在执行操作之前先列出任务以确认目标
2. 解析 JSON 输出以便进行结构化处理
3. 以用户友好的格式呈现结果（而不是原始 JSON）
4. 在完成任务或修改任务之前确认操作
5. 优雅地处理错误（例如任务未找到等）

### 常见模式

**每日回顾：**
```bash
# Statistics overview
osascript -l JavaScript scripts/get_stats.js

# What needs attention
osascript -l JavaScript scripts/list_tasks.js overdue
osascript -l JavaScript scripts/list_tasks.js due-soon
```

**任务查询：**
```bash
# "What's in my inbox?"
osascript -l JavaScript scripts/list_tasks.js inbox

# "What are my next actions?"
osascript -l JavaScript scripts/list_tasks.js available 10

# "Show my flagged tasks"
osascript -l JavaScript scripts/list_tasks.js flagged
```

**任务管理：**
```bash
# "Add a task to call John"
osascript -l JavaScript scripts/add_task.js "Call John"

# "Find tasks about the project"
osascript -l JavaScript scripts/search_tasks.js "project"

# "Mark 'Buy milk' as complete"
osascript -l JavaScript scripts/complete_task.js "Buy milk"

# "Flag the review task"
osascript -l JavaScript scripts/update_task.js "Review" --flag true
```

### 结果处理

脚本返回结构化数据的 JSON。在向用户展示结果时：
1. 解析 JSON
2. 清晰地格式化结果
3. 总结计数和关键信息
4. 突出显示紧急项（过期的、3 天内到期的任务）

**示例响应格式：**
```
Found 3 overdue tasks:
• Submit Q1 report (due Jan 20)
• Review contract (due Jan 23)
• Call vendor (due Jan 24)

And 5 tasks due in the next 3 days:
• [list tasks]

Would you like me to flag or update any of these?
```

### 错误处理

常见错误：
- **任务未找到** - 重新检查名称或先进行搜索
- **没有任务** - 明确报告空结果
- **日期格式无效** - 使用 YYYY-MM-DD 格式
- **OmniFocus 未运行** - 脚本需要 OmniFocus 运行

### 多步骤操作

**先查找再执行：**
```bash
# 1. Search for task
RESULTS=$(osascript -l JavaScript scripts/search_tasks.js "meeting")

# 2. Parse and identify target task name

# 3. Complete the task
osascript -l JavaScript scripts/complete_task.js "Team meeting notes"
```

## 技术参考

有关详细的 API 信息和高级用法，请参阅：
- **JXA API 参考：** `references/jxa-api.md` - 对象模型和方法
- **自动化指南：** `references/automation-guide.md` - 详细的脚本文档和工作流程

在以下情况下请阅读这些文件：
- 构建复杂查询时
- 理解 OmniFocus 数据模型时
- 实现自定义工作流程时
- 调试脚本时

## 要求

- macOS
- 安装并运行 OmniFocus
- 脚本具有执行权限（chmod +x）

## 注意事项

- 脚本使用 JXA（JavaScript for Automation），而不是 AppleScript
- 任务匹配对名称是区分大小写的，但对搜索内容是不区分大小写的
- 日期格式：YYYY-MM-DD（ISO 8601）
- 所有操作都在默认的 OmniFocus 文档上执行
- 除了添加、完成和更新操作外，脚本都是只读安全的