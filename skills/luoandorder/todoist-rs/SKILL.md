---
name: todoist
description: 管理 Todoist 任务。当用户提到 “todoist”、“我的任务”、“任务列表”、“添加任务”、“完成任务” 或希望与他们的 Todoist 账户进行交互时，请使用此功能。
homepage: https://github.com/LuoAndOrder/todoist-rs
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":["td"]},"install":[{"id":"brew","kind":"brew","formula":"LuoAndOrder/tap/todoist-cli","bins":["td"],"label":"Install todoist-cli via Homebrew"}]}}
---

# Todoist 集成

通过 `td` CLI（todoist-rs）来管理任务。

## 安装

```bash
brew install LuoAndOrder/tap/todoist-cli
```

或者通过 Cargo 安装：`cargo install todoist-cli-rs`

## 同步行为

- **自动同步**：`add`、`done`、`edit`、`delete` 操作会直接触发 API 请求进行同步
- **读取数据时使用缓存**：`list`、`today`、`show` 操作会从本地缓存中读取数据
- **需要时手动同步**：使用 `--sync` 标志或 `td sync` 命令来获取最新数据

```bash
td sync              # Incremental sync (fast)
td sync --full       # Full rebuild if cache seems off
```

## 常用操作

### 列出任务

```bash
# Today's agenda (includes overdue)
td today --sync

# Today only (no overdue)
td today --no-overdue

# All tasks
td list --sync

# By project
td list -p "Inbox" --sync
td list -p "Work" --sync

# High priority
td list -f "p1 | p2" --sync

# By label
td list -l "urgent" --sync

# Complex filters
td list -f "today & p1" --sync
td list -f "(today | overdue) & !@waiting_on" --sync
```

### 添加任务

- **快速添加（使用自然语言）**：
```bash
td quick "Buy milk tomorrow @errands #Personal"
td quick "Review PR tomorrow" --note "Check the auth changes carefully"
```

- **结构化添加**：
```bash
td add "Task content" \
  -p "Inbox" \
  -P 2 \
  -d "today" \
  -l "urgent"

# With description
td add "Prepare quarterly report" -P 1 -d "friday" \
  --description "Include sales metrics and customer feedback summary"
```

**可选参数**：
- `-P, --priority` - 优先级（1 表示最高优先级，4 表示最低优先级，默认值）
- `-p, --project` - 项目名称
- `-d, --due` - 截止日期（格式为 "today"、"tomorrow"、"2026-01-30"、"next monday"）
- `-l, --label` - 任务标签（可多次使用）
- `--description` - 任务描述/备注（显示在任务标题下方）
- `--section` - 任务所属的项目部分
- `--parent` - 父任务 ID（用于创建子任务）

### 完成任务

```bash
td done <task-id>
td done <id1> <id2> <id3>              # Multiple at once
td done <id> --all-occurrences         # End recurring task permanently
```

### 修改任务

```bash
td edit <task-id> -c "New content"
td edit <task-id> --description "Additional notes here"
td edit <task-id> -P 1
td edit <task-id> -d "tomorrow"
td edit <task-id> --add-label "urgent"
td edit <task-id> --remove-label "next"
td edit <task-id> --no-due             # Remove due date
td edit <task-id> --section "Next Actions"
td edit <task-id> -p "Work"            # Move to different project
```

**编辑选项**：
- `-c, --content` - 更新任务标题
- `--description` - 更新任务描述/备注
- `-P, --priority` - 更改优先级（1-4）
- `-d, --due` - 更改截止日期
- `--no-due` - 删除截止日期
- `-l, --label` - 更改或删除任务标签
- `--add-label` - 添加新标签
- `--remove-label` - 删除标签
- `--project` - 将任务移动到其他项目
- `--section` - 将任务移动到项目内的其他部分

### 显示任务详情

```bash
td show <task-id>
td show <task-id> --comments
```

### 删除任务

```bash
td delete <task-id>
```

### 重新打开已完成的任务

```bash
td reopen <task-id>
```

## 项目与标签管理

```bash
# Projects
td projects                            # List all
td projects add "New Project"
td projects show <id>

# Labels
td labels                              # List all
td labels add "urgent"
```

## 过滤语法

使用 `-f/--filter` 进行过滤：
- `|` 表示 OR 关系：`today | overdue`
- `&` 表示 AND 关系：`@next & #Personal`
- 括号：`(today | overdue) & p1`
- 否定操作：`!@waiting_on`
- 优先级：`p1`、`p2`、`p3`、`p4`
- 日期：`today`、`tomorrow`、`overdue`、`no date`、`7 days`

## 工作流程建议

1. **晨间检查**：`td today --sync`
2. **快速添加任务**：`td quick "thing to do"`
3. **查看待办事项**：`td list -f "@next" --sync`
4. **查看待处理任务**：`td list -f "@waiting_on" --sync`
5. **每日总结**：`td today`（缓存已更新，无需再次同步）