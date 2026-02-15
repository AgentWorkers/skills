---
name: ttt
description: 通过 ttt CLI 管理 TinyTalkingTodos 列表及其项目
metadata: {"openclaw": {"emoji": "✅", "requires": {"bins": ["ttt"]}, "homepage": "https://tinytalkingtodos.com"}}
---

# TinyTalkingTodos CLI

使用 `ttt` 从命令行管理待办事项列表及其内容。该 CLI 与 TinyTalkingTodos 实时同步。

## 安装

```bash
npm install -g @ojschwa/ttt-cli
```

或为了开发目的进行本地安装：

```bash
cd /path/to/talking-todo/ttt-cli
npm install
npm run build
npm link
```

使用 `ttt --help` 进行验证。

## 认证

在使用 CLI 之前，用户必须先进行身份验证：

```bash
# Check auth status
ttt auth status

# Login via browser (opens OAuth flow)
ttt auth login

# Logout
ttt auth logout

# Export credentials as env vars (for scripts)
ttt auth export
```

## 列表管理

### 显示所有列表

```bash
ttt list ls
```

输出格式（简洁、节省令牌）：
```
Today [2/5]
Groceries [0/3]
Work Tasks [1/4]
```

对于结构化数据：
```bash
ttt list ls --json
```

### 获取列表详情

```bash
ttt list get "Groceries"
# or by ID
ttt list get list-abc123
```

### 创建新列表

```bash
ttt list create "Weekend Plans"
ttt list create "Shopping" --icon "🛒" --color "#FF6B6B"
```

选项：
- `--color <hex>` - 列表背景颜色
- `--icon <emoji>` - 列表图标
- `--type <type>` - 列表类型

### 更新列表

```bash
ttt list update "Groceries" --name "Shopping List"
ttt list update "Shopping List" --icon "🛒" --color "#00FF00"
```

选项：
- `--name <name>` - 新列表名称
- `--color <hex>` - 列表背景颜色
- `--icon <emoji>` - 列表图标
- `--type <type>` - 列表类型

### 删除列表

```bash
ttt list delete "Old List"
ttt list rm "Old List"  # alias

# Force delete even if list has todos
ttt list delete "Old List" --force
```

## 待办事项操作

### 显示列表中的所有待办事项

```bash
ttt todo ls --list "Groceries"
```

输出格式（简洁）：
```
Groceries [1/4]
✓ Milk id:todo-abc123
○ Bread id:todo-def456
○ Eggs id:todo-ghi789
○ Butter id:todo-jkl012
```

JSON 格式输出：
```bash
ttt todo ls --list "Groceries" --json
```

### 添加待办事项

基本用法：
```bash
ttt todo add "Buy avocados" --list "Groceries"
```

带选项的用法：
```bash
ttt todo add "Doctor appointment" --list "Health" \
  --date 2026-02-15 \
  --time 14:30 \
  --notes "Bring insurance card"

ttt todo add "Try new pasta place" --list "Restaurants" \
  --url "https://example.com/restaurant" \
  --street-address "123 Main St" \
  --rating 4

ttt todo add "Tomatoes" --list "Groceries" \
  --amount 2.50 \
  --category "Produce" \
  --emoji "🍅"
```

所有 `--list` 选项的示例：
| 选项 | 描述 | 示例 |
|--------|-------------|---------|
| `--notes <text>` | 额外备注 | `--notes "organic preferred"` |
| `--date <YYYY-MM-DD>` | 截止日期 | `--date 2026-02-15` |
| `--time <HH:MM>` | 截止时间 | `--time 14:30` |
| `--url <url>` | 关联链接 | `--url "https://..."` |
| `--emoji <emoji>` | 待办事项图标 | `--emoji "🎉"` |
| `--email <email>` | 关联邮箱 | `--email "contact@..."` |
| `--street-address <addr>` | 位置信息 | `--street-address "123 Main"` |
| `--number <n>` | 数值字段 | `--number 5` |
| `--amount <n>` | 金额/价格 | `--amount 12.99` |
| `--rating <1-5>` | 星级评分 | `--rating 4` |
| `--type <A-E>` | 待办事项类型 | `--type A` |
| `--category <name>` | 分类 | `--category "Urgent"` |

### 将待办事项标记为已完成

```bash
ttt todo done todo-abc123
```

在简洁的输出格式中，待办事项的 ID 会以 `id:` 的形式显示。

### 将待办事项标记为未完成

```bash
ttt todo undone todo-abc123
```

### 更新待办事项

```bash
ttt todo update todo-abc123 --text "New text"
ttt todo update todo-abc123 --category "Urgent" --date 2026-02-15
ttt todo update todo-abc123 --done   # mark as done
ttt todo update todo-abc123 --not-done  # mark as not done
```

选项：
- `--text <text>` - 新待办事项内容
- `--notes`, `--date`, `--time`, `--url`, `--emoji`, `--email`, `--street-address`
- `--number`, `--amount`, `--rating`, `--type`, `--category`
- `--done` / `--not-done` - 切换完成状态

### 删除待办事项

```bash
ttt todo delete todo-abc123
# or use alias
ttt todo rm todo-abc123
```

## 批量添加待办事项

使用 JSON 格式一次性添加多个待办事项：

```bash
ttt todo batch-add --list "Groceries" --items '[
  {"text": "Milk"},
  {"text": "Eggs", "fields": {"category": "Dairy"}},
  {"text": "Bread", "fields": {"amount": 3.50}}
]'
```

每个待办事项项都需要提供 `text`，并可选择性地提供其他字段。

### 批量更新待办事项

一次性更新多个待办事项：

```bash
ttt todo batch-update --items '[
  {"id": "todo-abc123", "fields": {"done": true}},
  {"id": "todo-def456", "fields": {"text": "Updated text", "category": "Urgent"}}
]'
```

每个待办事项项都需要提供 `id` 和需要更新的字段。

## 撤销操作

所有修改操作都会被记录下来，并可以撤销：

```bash
# Undo the last operation
ttt undo

# Undo the last 3 operations
ttt undo 3

# View undo history
ttt history
ttt history --limit 20
ttt history --json
```

撤销操作支持以下操作：添加/删除/更新待办事项、批量添加/更新、标记为已完成/未完成、创建/更新列表。

## 守护进程（性能优化）

守护进程会保持一个持久的 WebSocket 连接，以加快命令执行速度：

```bash
# Start daemon (auto-starts on first command if not running)
ttt daemon start

# Check status
ttt daemon status

# Stop daemon
ttt daemon stop
```

如果 30 分钟内没有活动，守护进程会自动关闭。

## 最佳实践

1. **在向用户显示列表时使用简洁的输出格式**（默认设置）——这样可以节省令牌资源。
2. **在需要解析数据或提取特定字段时使用 `--json` 选项**。
3. **为了便于阅读，可以通过名称引用列表；为了确保准确性，可以通过 ID 引用列表**。
4. **在操作前检查认证状态**，以防登录状态不确定。
5. **从简洁的输出格式中提取待办事项的 ID（格式：`id:<todo-id>`）以便进行更新操作。
6. **在添加或更新多个待办事项时使用批量操作**——这比单独调用更高效。
7. **如果操作有误，请使用撤销功能`ttt undo`来恢复之前的操作状态**。

## 示例工作流程

### 向购物清单中添加项目
```bash
ttt todo add "Milk" --list "Groceries" --category "Dairy"
ttt todo add "Bread" --list "Groceries" --category "Bakery"
ttt todo add "Apples" --list "Groceries" --amount 3.50 --category "Produce"
```

### 检查并完成任务
```bash
# View todos
ttt todo ls --list "Today"

# Mark one done (using ID from output)
ttt todo done todo-xyz789
```

### 创建包含待办事项的新列表
```bash
ttt list create "Weekend Trip" --icon "🏕️"
ttt todo add "Pack tent" --list "Weekend Trip"
ttt todo add "Check weather" --list "Weekend Trip" --url "https://weather.com"
ttt todo add "Gas up car" --list "Weekend Trip"
```

### 高效批量添加项目
```bash
ttt todo batch-add --list "Party Supplies" --items '[
  {"text": "Balloons", "fields": {"category": "Decorations"}},
  {"text": "Cake", "fields": {"category": "Food", "amount": 45.00}},
  {"text": "Plates", "fields": {"category": "Supplies", "number": 20}},
  {"text": "Candles", "fields": {"category": "Decorations"}}
]'
```

### 将多个项目标记为已完成
```bash
ttt todo batch-update --items '[
  {"id": "todo-abc", "fields": {"done": true}},
  {"id": "todo-def", "fields": {"done": true}},
  {"id": "todo-ghi", "fields": {"done": true}}
]'
```

### 撤销错误操作
```bash
# Accidentally deleted something? Undo it
ttt undo

# Made several mistakes? Undo multiple
ttt undo 3
```