---
name: todo-management
description: 这是一个基于工作空间的 SQLite 待办事项管理器（文件路径：./todo.db），支持分组功能以及任务状态的管理（待办/进行中/已完成/跳过）。用户可以通过 {baseDir}/scripts/todo.sh 脚本来添加、列出、编辑、移动和删除待办事项，同时还可以管理各个分组。
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["sqlite3"]}}}
user-invocable: true
---

# 待办事项管理

## 该功能的作用
该功能使用一个与每个工作空间关联的 SQLite 数据库来存储待办事项：
- 默认数据库文件：`./todo.db`
- 可自定义数据库文件路径：`TODO_DB=/path/to/todo.db`

所有对待办事项的修改都必须通过命令行界面（CLI）来完成：
`bash {baseDir}/scripts/todo.sh ...`

## 待办事项的状态
- `pending`（默认状态）
- `in_progress`（进行中）
- `done`（已完成）
- `skipped`（跳过）

默认情况下，系统会隐藏已完成和被跳过的待办事项，除非用户使用 `--all` 或 `--status=...` 参数来显示所有状态。

---

# 不可妥协的规则

## 1) 绝对禁止文件写入
- 禁止创建或修改任何文件（例如 `todos.md`、笔记文件或 Markdown 格式的文件）。
- 禁止输出类似 `todos.md (...)` 这样的文件内容。
- 所有待办事项的状态信息仅保存在 `todo.db` 数据库中，并通过 `todo.sh` 脚本进行更新。

## 2) 除非用户明确要求，否则不得显示待办事项列表
- 如果用户没有请求“显示/列出/打印我的待办事项”，则不得显示待办事项列表。
- 在完成任何操作后，系统仅输出一条简短的确认信息。

## 3) 回复信息要尽可能简洁
- 操作成功后，回复信息应仅包含一行，字数不超过 5 个词（请根据用户的语言进行翻译）。
- 除非用户明确要求，否则不要包含项目符号列表、表格、代码块或工具输出。

允许使用的确认信息（英文示例；根据需要翻译）：
- “已完成。”
- “已添加。”
- “已更新。”
- “已删除。”
- “已移动。”
- “已重命名。”
- “已清除。”
- “已添加到列表中。”

## 4) 处理模糊请求的情况（这是规则 2 的唯一例外）
- 如果用户请求执行某个操作但没有提供具体的任务 ID（例如：“删除‘买牛奶’这个任务”）：
  1) 运行 `entry list` 命令（可选参数 `--group=...` 可用于按组显示待办事项）
  2) 显示操作结果（以表格形式）
  3) 询问用户希望针对哪个任务 ID 进行操作

只有在用户没有明确要求的情况下，才能显示待办事项列表。

## 5) 安全地处理批量删除操作
- 使用 `group remove "X"` 命令时，待办事项会被移动到“收件箱”（Inbox）文件夹中。
- 只有在用户明确选择删除待办事项时，才会实际删除它们：
  - 提示用户：“是否将待办事项移动到‘收件箱’（默认操作）或直接删除它们？”
  - 仅在用户确认后，才使用 `--delete-entries` 参数来删除待办事项。

---

# 可用的命令（请严格使用以下命令）

### 添加待办事项
- `bash {baseDir}/scripts/todo.sh entry create "Buy milk"`
- `bash {baseDir}/scripts/todo.sh entry create "Ship feature X" --group="Work" --status=in_progress`

### 查看待办事项列表
- `bash {baseDir}/scripts/todo.sh entry list` （仅在用户请求时显示）
- `bash {baseDir}/scripts/todo.sh entry list --group="Work"`
- `bash {baseDir}/scripts/todo.sh entry list --all`
- `bash {baseDir}/scripts/todo.sh entry list --status=done`

### 显示特定待办事项的详细信息
- `bash {baseDir}/scripts/todo.sh entry show 12`

### 修改待办事项的详细信息
- `bash {baseDir}/scripts/todo.sh entry edit 12 "Buy oat milk instead"`

### 移动待办事项
- `bash {baseDir}/scripts/todo.sh entry move 12 --group="Inbox"`

### 更改待办事项的状态
- `bash {baseDir}/scripts/todo.sh entry status 12 --status=done`
- `bash {baseDir}/scripts/todo.sh entry status 12 --status=skipped`

### 删除待办事项
- `bash {baseDir}/scripts/todo.sh entry remove 12`

### 创建/列出待办事项组
- `bash {baseDir}/scripts/todo.sh group create "Work"`
- `bash {baseDir}/scripts/todo.sh group list`

### 重命名待办事项组
- `bash {baseDir}/scripts/todo.sh group rename "Work" "Work (Project A)`
- `bash {baseDir}/scripts/todo.sh group edit "Work" "Work (Project A)"

### 删除待办事项组
- 默认操作：将组中的所有待办事项移动到“收件箱”：
  - `bash {baseDir}/scripts/todo.sh group remove "Work"`
- 如果用户希望同时删除组中的所有待办事项：
  - `bash {baseDir}/scripts/todo.sh group remove "Work" --delete-entries`

---

# “清除待办事项列表”的操作流程
- 首先运行 `entry list --all` 命令获取待办事项的 ID（不要显示结果）。
- 使用 `entry remove ID` 命令逐一删除这些待办事项。
- 回复用户：“待办事项列表已清除。”

- 如果用户随后请求查看待办事项列表，再运行 `entry list` 命令并显示列表内容。

---

# 对话示例（预期行为）
用户：“我需要去买牛奶，把它添加到待办事项列表中。”
助手：“已添加。”

用户：“哦，我还需要打扫房间。”
助手：“已添加到列表中。”

用户：“显示我的待办事项。”
助手：（显示待办事项列表）

用户：“删除‘买牛奶’这个任务。”
助手：（列出所有相关的待办事项，询问用户需要删除的具体任务 ID，确认后执行删除操作）