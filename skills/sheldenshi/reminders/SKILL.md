---
name: reminders
description: 搜索、创建、修改和删除 macOS 的提醒事项。主动使用这些功能——当用户请求接收提醒、提及某个任务或待办事项，或者想要查看即将到期的提醒时，都可以及时响应。
---

# macOS 提醒事项管理

通过 `reminders` 脚本来管理 macOS 的提醒事项。返回 JSON 格式的数据。该脚本不依赖任何外部库，仅使用 macOS 自带的工具。

## 何时使用此功能

建议 **主动** 使用此功能，而不仅仅是在用户明确请求时：

- 当用户说 “提醒我……” 时，创建一个带有到期时间的提醒事项。
- 当用户提到某项任务或待办事项时，创建提醒事项或搜索现有的提醒事项。
- 当用户询问 “我需要做什么？” 时，列出即将到期或未完成的提醒事项。
- 当用户表示 “我已经完成了 X” 时，将相应的提醒事项标记为已完成。
- 当用户请求查询、添加、修改或删除提醒事项时。

## 命令使用方法

所有命令都使用位于 `references/` 目录中的 `reminders` 脚本。请根据当前 SKILL.md 文件的路径来执行相应的命令：

```bash
REMINDERS="$(dirname "<path-to-this-SKILL.md>")/references/reminders.sh"
```

首次运行时，macOS 会请求允许访问提醒事项功能——请点击 “允许”。

## 命令列表

### 列出所有提醒事项列表

```bash
$REMINDERS lists
```

显示所有提醒事项列表，并统计已完成和未完成的提醒事项数量。

### 显示具体提醒事项

```bash
$REMINDERS ls [<list-name>] [--all]
```

列出所有提醒事项。默认情况下仅显示未完成的提醒事项。如果未指定列表名称，则会显示所有列表中的提醒事项。

| 标志 | 描述 |
|------|-------------|
| `--all` | 包括已完成的提醒事项 |

### 搜索提醒事项

```bash
$REMINDERS search <query> [--all]
$REMINDERS <query>                   # search is the default command
```

根据名称和备注在所有列表中搜索提醒事项。默认情况下，搜索结果中不会包含已完成的提醒事项。

### 添加提醒事项

```bash
$REMINDERS add --name <text> [--list <name>] [--due <datetime>] [--remind <datetime>] [--notes <text>] [--priority high|medium|low] [--flagged]
```

必须提供 `--name` 参数。如果省略 `--list` 参数，系统会使用默认的提醒事项列表。如果提供了 `--due` 参数但未提供 `--remind` 参数，系统会将该提醒事项的到期时间设置为当前时间。

**日期必须使用 ISO 8601 格式（例如：2025-02-15T10:00:00）**。在调用命令之前，请将相对日期（例如 “明天上午 9 点”）转换为绝对的 ISO 8601 格式。

```bash
$REMINDERS add --name "Buy milk"
$REMINDERS add --name "Call dentist" --due 2025-02-15T09:00:00 --priority high
$REMINDERS add --name "Pick up package" --list "Errands" --notes "At the post office"
```

### 将提醒事项标记为已完成

```bash
$REMINDERS complete <query> [--list <name>]
```

将提醒事项标记为已完成。系统会搜索未完成的提醒事项并根据名称进行匹配。如果找到多个匹配项，会列出所有匹配项。

### 修改提醒事项

```bash
$REMINDERS edit <query> [--list <name>] [options]
```

根据名称查找提醒事项并进行修改。如果找到多个匹配项，会列出所有匹配项。

| 选项 | 描述 |
|--------|-------------|
| `--list <名称>` | 将搜索范围限制在指定的列表内 |
| `--name <文本>` | 设置新的名称 |
| `--due <日期时间>` | 设置到期时间（使用 `--clear` 可删除该选项） |
| `--remind <日期时间>` | 设置提醒时间（使用 `--clear` 可删除该选项） |
| `--notes <文本>` | 设置备注（使用 `--clear` 可删除该选项） |
| `--priority <优先级>` | 设置优先级（高、中、低、无） |
| `--flagged` | 设置标记（使用 `--clear` 可删除该选项） |
| `--unflagged` | 取消标记（使用 `--clear` 可删除该选项） |
| `--uncomplete` | 将提醒事项标记为未完成（使用 `--clear` 可删除该选项） |

### 删除提醒事项

```bash
$REMINDERS delete <query> [--list <name>] [--yes]
```

根据名称查找并删除提醒事项。除非提供了 `--yes` 参数，否则系统会提示用户确认删除操作。建议始终使用 `--yes` 以跳过确认步骤。

### 创建新的提醒事项列表

```bash
$REMINDERS add-list --name <text>
```

创建一个新的提醒事项列表。

## 输出结果

所有命令都会返回 JSON 格式的数据：

```json
// lists
[
  { "name": "Reminders", "count": 12, "incomplete": 5 },
  { "name": "Shopping", "count": 3, "incomplete": 2 }
]

// ls, search
[
  {
    "name": "Buy milk",
    "body": "Get whole milk",
    "completed": false,
    "dueDate": "2025-02-15T10:00:00.000Z",
    "remindMeDate": "2025-02-15T10:00:00.000Z",
    "completionDate": null,
    "priority": "high",
    "flagged": false,
    "list": "Shopping"
  }
]

// add
{ "created": true, "name": "Buy milk", "list": "Shopping", ... }

// complete, edit
{ "updated": true, "name": "Buy milk", "completed": true, "list": "Shopping", ... }

// delete
{ "deleted": true, "name": "Buy milk", "list": "Shopping" }

// add-list
{ "created": true, "name": "Projects" }
```

## 工作流程

### 主动服务行为：

- 当用户说 “提醒我……” 时，立即创建提醒事项。系统会从上下文中解析到期时间（例如：“明天早上” 被解析为 “次日上午 9:00”），并确认创建的内容。
- 当用户在对话中提到需要完成某项任务时，主动提出创建提醒事项或直接完成任务。
- 当用户表示 “我已经完成了 X” 或 “我完成了 X” 时，系统会搜索相应的提醒事项并将其标记为已完成，并确认具体完成了哪些任务。
- 当用户询问 “我的列表里有什么？” 时，系统会列出所有未完成的提醒事项。如果提醒事项较多，系统会按列表进行分类显示。