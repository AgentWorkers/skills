---
name: omnifocus
description: 通过 Omni Automation 管理 OmniFocus 的任务、项目和文件夹。该工具可用于任务管理、待办事项列表的创建与维护、项目跟踪、GTD（Getting Things Done）工作流程的实现、任务的添加/完成/编辑、截止日期的设置、标签的管理以及重复性任务的设置。请确保您的 macOS 系统上已安装了 OmniFocus。
---

# OmniFocus

通过 JXA（JavaScript for Automation）来控制 OmniFocus。

## 前提条件

- 安装了 OmniFocus 3 或 4 的 macOS 系统。
- OmniFocus 必须正在运行（或者会自动启动）。

## 快速参考

```bash
# Run via the wrapper script
./scripts/of <command> [args...]

# Or directly
osascript -l JavaScript ./scripts/omnifocus.js <command> [args...]
```

## 命令

### 列出/查询

| 命令 | 描述 |
|---------|-------------|
| `inbox` | 列出收件箱中的任务 |
| `folders` | 列出所有文件夹 |
| `projects [folder]` | 列出项目（可选地按文件夹过滤） |
| `tasks <project>` | 列出某个项目中的任务 |
| `tags` | 列出所有标签 |
| `today` | 当天到期的任务或逾期任务 |
| `flagged` | 被标记为未完成的任务 |
| `search <query>` | 按名称搜索任务 |
| `info <taskId>` | 查看任务的详细信息 |

### 创建

| 命令 | 描述 |
|---------|-------------|
| `add <name> [project]` | 将任务添加到收件箱或项目中 |
| `newproject <name> [folder]` | 创建新项目 |
| `newfolder <name>` | 创建顶级文件夹 |
| `newtag <name>` | 创建或获取标签 |

### 修改

| 命令 | 描述 |
|---------|-------------|
| `complete <taskId>` | 将任务标记为已完成 |
| `uncomplete <taskId>` | 将任务标记为未完成 |
| `delete <taskId>` | 永久删除任务 |
| `rename <taskId> <name>` | 重命名任务 |
| `note <taskId> <text>` | 为任务添加备注 |
| `setnote <taskId> <text>` | 更改任务的备注 |
| `defer <taskId> <date>` | 设置任务的延迟完成日期（格式：YYYY-MM-DD） |
| `due <taskId> <date>` | 设置任务的截止日期 |
| `flag <taskId> [true\|false]` | 设置任务的标记状态 |
| `tag <taskId> <tag>` | 为任务添加标签（如果标签不存在则创建） |
| `untag <taskId> <tag>` | 从任务中移除标签 |
| `move <taskId> <project>` | 将任务移动到另一个项目 |

### 重复执行

```bash
# repeat <taskId> <method> <interval> <unit>
of repeat abc123 fixed 1 weeks
of repeat abc123 due-after-completion 2 days
of repeat abc123 defer-after-completion 1 months
of unrepeat abc123
```

可选参数：`fixed`, `due-after-completion`, `defer-after-completion`  
时间单位：`days`, `weeks`, `months`, `years`

## 输出格式

所有命令返回 JSON 格式的数据。成功响应包含 `"success": true`；错误响应包含 `"error": "message"`。

```json
{
  "success": true,
  "task": {
    "id": "abc123",
    "name": "Task name",
    "note": "Notes here",
    "flagged": false,
    "completed": false,
    "deferDate": "2026-01-30",
    "dueDate": "2026-02-01",
    "project": "Project Name",
    "tags": ["tag1", "tag2"],
    "repeat": {"method": "fixed", "rule": "RRULE:FREQ=WEEKLY;INTERVAL=1"}
  }
}
```

## 示例

```bash
# Add task to inbox
of add "Buy groceries"

# Add task to specific project
of add "Review docs" "Work Projects"

# Set due date and flag
of due abc123 2026-02-01
of flag abc123 true

# Add tags
of tag abc123 "urgent"
of tag abc123 "home"

# Create recurring task
of add "Weekly review" "Habits"
of repeat xyz789 fixed 1 weeks

# Search and complete
of search "groceries"
of complete abc123

# Get today's tasks
of today
```

## 注意事项

- 任务 ID 是 OmniFocus 内部使用的唯一标识符（会在所有任务响应中返回）。
- 日期使用 ISO 格式（YYYY-MM-DD）。
- 项目和文件夹名称区分大小写。
- 使用 `tag` 命令时，如果标签不存在，系统会自动创建该标签。
- 所有输出均为 JSON 格式，便于解析。

## 技术细节

此技能主要使用 JavaScript for Automation (JXA) 来执行各种操作；对于标签和重复执行操作，由于 JXA 在处理 OmniFocus API 时存在类型转换问题，因此会使用 AppleScript 作为备用方案。

这种混合使用的方法具有以下优点：
- 输出为 JSON 格式，便于数据解析。
- 对标签名称中的特殊字符进行了有效的转义处理。
- 提供了清晰的错误处理信息。

**首次使用提示：** OmniFocus 可能会提示是否允许自动化访问。请在系统设置 > 隐私与安全 > 自动化中启用该功能。