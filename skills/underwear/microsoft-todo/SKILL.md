---
name: microsoft-todo
description: "通过 `todo` CLI 管理 Microsoft To Do 任务。适用于用户需要添加、查看、完成任务、删除任务、管理子任务（步骤）、添加备注或整理任务列表的场景。"
homepage: https://github.com/underwear/microsoft-todo-cli
metadata:
  {
    "openclaw":
      {
        "emoji": "✅",
        "requires": { "bins": ["todo"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "uv",
              "package": "microsoft-todo-cli",
              "bins": ["todo"],
              "label": "Install microsoft-todo-cli (pip/uv)",
            },
          ],
      },
  }
---

# Microsoft To Do CLI

使用 `todo` 命令管理 Microsoft To Do 中的任务。

## 参考资料

- `references/setup.md`（Azure 应用注册 + OAuth 配置）

## 先决条件

1. 已安装 `todo` CLI（通过 `pip install microsoft-todo-cli` 安装）
2. 已注册 Microsoft Azure 应用（请参阅 `references/setup.md`）
3. 凭据已配置在 `~/.config/microsoft-todo-cli/keys.yml` 文件中
4. 首次运行时需要在浏览器中完成 OAuth 认证流程

## 命令

### 任务（Tasks）

```bash
# List tasks
todo tasks --json                        # Default list
todo tasks Work --json                   # Specific list
todo tasks --due-today --json            # Due today
todo tasks --overdue --json              # Past due
todo tasks --important --json            # High priority
todo tasks --completed --json            # Done tasks
todo tasks --all --json                  # Everything

# Create task
todo new "Task name" --json              # Basic
todo new "Task" -l Work --json           # In specific list
todo new "Task" -d tomorrow --json       # With due date
todo new "Task" -r 2h --json             # With reminder
todo new "Task" -d mon -r 9am --json     # Due Monday, remind 9am
todo new "Task" -I --json                # Important
todo new "Task" -R daily --json          # Recurring daily
todo new "Task" -R weekly:mon,fri --json # Specific days
todo new "Task" -S "Step 1" -S "Step 2" --json  # With subtasks
todo new "Task" -N "Note content" --json      # With note

# Update task
todo update "Task" --title "New" --json
todo update "Task" -d friday -I --json

# Complete/Uncomplete
todo complete "Task" --json
todo complete 0 1 2 --json               # Batch by index
todo uncomplete "Task" --json

# Delete
todo rm "Task" -y --json
```

### 子任务（Subtasks）

```bash
todo new-step "Task" "Step text" --json
todo list-steps "Task" --json
todo complete-step "Task" "Step" --json
todo uncomplete-step "Task" "Step" --json
todo rm-step "Task" 0 --json
```

### 备注（Notes）

```bash
todo note "Task" "Note content"
todo show-note "Task"
todo clear-note "Task"
```

### 列表（Lists）

```bash
todo lists --json
todo new-list "Project X" --json
todo rename-list "Old" "New" --json
todo rm-list "Project X" -y --json
```

## 任务识别（Task Identification）

| 方法           | 稳定性 | 使用场景            |
| ---------------- | --------- | ------------------- |
| `--id "AAMk..."` | 稳定    | 自动化、脚本操作           |
| 索引（`0`, `1`）     | 不稳定  | 仅限交互式操作         |
| 名称（`"Task"`）     | 不稳定  | 名称必须唯一           |

**多步骤操作时使用任务 ID：**

```bash
ID=$(todo new "Task" -l Work --json | jq -r '.id')
todo complete --id "$ID" -l Work --json
```

## 日期和时间格式（Date & Time Formats）

| 类型       | 示例                          |
| -------- | ----------------------------------- |
| 相对时间    | `1h`, `30m`, `2d`, `1h30m`          |
| 时间        | `9:30`, `9am`, `17:00`, `5:30pm`    |
| 天数        | `tomorrow`, `monday`, `fri`         |
| 日期        | `2026-12-31`, `31.12.2026`          |
| 关键词      | `morning` (7:00), `evening` (18:00)     |

## 重复模式（Recurrence Patterns）

| 模式          | 描述                |
| ---------------- | ------------------- |
| 每日（daily）     | 每天                |
| 每周（weekly）     | 每周                |
| 每月（monthly）    | 每月                |
| 每年（yearly）     | 每年                |
| 工作日（weekdays）   | 星期一至周五            |
| 每周：周一、周三、周五（weekly:mon,wed,fri） | 指定工作日            |
| 每隔两天（every 2 days） | 自定义间隔            |

## 别名（Aliases）

| 别名       | 命令                |
| ------------ | ------------------- |
| `t`       | `tasks`            |
| `n`       | `new`              |
| `c`       | `complete`            |
| `d`       | `rm`                |
| `sn`       | `show-note`            |
| `cn`       | `clear-note`            |

## 注意事项

- 所有命令均需使用 `--json` 选项以获取结构化输出
- 使用 `rm` 命令时请务必加上 `-y` 选项以跳过确认步骤
- 使用 `--id` 和 `-l ListName` 可以获取特定列表的任务信息
- 首次运行时系统会自动在浏览器中打开页面进行 OAuth 认证