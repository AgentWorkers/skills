---
name: ms-todo-sync
description: >
  A CLI skill to manage Microsoft To Do tasks via Microsoft Graph API.
  Supports listing, creating, completing, deleting, searching tasks and lists,
  viewing overdue/today/pending tasks, and exporting data.
metadata:
  version: 1.0.2
  author: xiaoski@qq.com
  license: MIT License
  tags: [productivity, task-management, microsoft-todo, cli]
  category: productivity
---

# ms-todo-sync

这是一个基于Microsoft Graph API的命令行客户端，用于通过Microsoft To Do管理任务和列表。

## 前提条件

1. 必须安装Python 3.9或更高版本。
2. 必须安装`uv`（Python包管理器）。可以通过`pip install uv`来安装，或访问https://docs.astral.sh/uv/获取更多信息。
3. **工作目录**：所有命令必须从这个技能文件（即SKILL.md所在的目录）的根目录下执行。
4. **网络访问**：需要互联网连接才能访问Microsoft Graph API的端点。
5. **身份验证**：首次使用时需要通过浏览器进行交互式登录。请参阅[身份验证](#authentication)部分。
   - **令牌缓存**：`~/.mstodo_token_cache.json`（在会话间保持持久性，会自动刷新）
   - **设备代码流缓存**：`~/.mstodo_device_flow.json`（临时文件）

## 安装与设置

### 首次设置

在首次使用此技能之前，需要先安装依赖项：

```bash
# Navigate to skill directory
cd <path-to-ms-todo-sync>

# Install dependencies using uv (recommended - creates isolated environment)
uv sync

# Alternative: Install dependencies with pip (uses global/active Python environment)
pip install -r requirements.txt
```

**依赖项：**
- 需要`msal`（Microsoft身份验证库）和`requests`
- 在`requirements.txt`中列出
- `uv`会创建一个隔离的虚拟环境以避免依赖冲突

### 环境验证

安装完成后，验证设置是否正确：

```bash
# Check if uv can find the script
uv run scripts/ms-todo-sync.py --help

# Expected: Command help text should be displayed
```

**故障排除：**
- 如果出现“uv: command not found”的错误，请安装`uv`：`pip install uv`
- 如果找不到Python，请从https://python.org下载并安装Python 3.9或更高版本
- 如果脚本在执行过程中出现导入错误，请确保所有依赖项都已安装：`uv sync`或`pip install -r requirements.txt`

### 安全说明

- 该工具通过Microsoft的`msal`库使用官方的Microsoft Graph API
- 所有代码都是纯Python（.py文件），易于阅读和审计
- 令牌存储在本地文件`~/.mstodo_token_cache.json`中
- 所有API请求都直接发送到Microsoft的端点

## 命令参考

所有命令都遵循以下格式：

```
uv run scripts/ms-todo-sync.py [GLOBAL_OPTIONS] <command> [COMMAND_OPTIONS]
```

### 全局选项

| 选项 | 描述 |
|--------|-------------|
| `-v, --verbose` | 显示详细信息（ID、日期、备注）。**必须放在子命令之前** |
| `--debug` | 启用调试模式，以显示API请求和响应。有助于故障排除。**必须放在子命令之前** |

> ⚠️ **常见错误**：全局选项必须放在子命令之前。
> - ✅ `uv run scripts/ms-todo-sync.py -v lists`
> - ✅ `uv run scripts/ms-todo-sync.py --debug add "Task"`
> - ❌ `uv run scripts/ms-todo-sync.py lists -v`

---

### 身份验证

身份验证采用两步设备代码流机制，适用于非交互式/代理环境。

#### `login get` — 获取验证码

```bash
uv run scripts/ms-todo-sync.py login get
```

**输出示例：**
```
✓ Verification code generated

Please visit the following link to log in:
https://microsoft.com/devicelogin

Enter verification code: ABC123XYZ

Verify with command: ms-todo-sync.py login verify
```

**代理行为**：向用户展示URL和验证码。等待用户确认完成浏览器登录后再继续操作。

#### `login verify` — 完成登录

```bash
uv run scripts/ms-todo-sync.py login verify
```

**成功输出：**
```
✓ Authentication successful! Login information saved, you will be logged in automatically next time.
```

**失败输出：**
```
✗ Authentication failed: <error description>
```

> ⚠️ 此命令会阻塞，直到Microsoft的服务器确认用户已完成浏览器身份验证。在用户确认完成登录之前，请勿运行此命令。

**退出代码**：成功时为0，失败时为1。

#### `logout` — 清除保存的登录信息

```bash
uv run scripts/ms-todo-sync.py logout
```

仅当用户明确要求切换账户或清除登录信息时使用。通常情况下，令牌会被缓存，登录是自动完成的。

---

### 列表管理

#### `lists` — 列出所有任务列表

```bash
uv run scripts/ms-todo-sync.py lists
uv run scripts/ms-todo-sync.py -v lists  # with IDs and dates
```

**输出示例：**
```
📋 Task Lists (3 total):

1. Tasks
2. Work
3. Shopping
```

#### `create-list` — 创建新列表

```bash
uv run scripts/ms-todo-sync.py create-list "<name>"
```

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `name` | 是 | 新列表的名称 |

输出：`✓ 列表创建成功：<name>`

#### `delete-list` — 删除列表

```bash
uv run scripts/ms-todo-sync.py delete-list "<name>" [-y]
```

| 参数/选项 | 必需 | 描述 |
|-----------------|----------|-------------|
| `name` | 是 | 要删除的列表名称 |
| `-y, --yes` | 否 | 跳过确认提示 |

> ⚠️ 这是一个破坏性操作。如果不使用`-y`，命令会提示用户确认。在删除重要列表之前，请先询问用户。

输出：`✓ 列表删除成功：<name>`

---

### 任务操作

#### `add` — 添加新任务

```bash
uv run scripts/ms-todo-sync.py add "<title>" [options]
```

| 选项 | 必需 | 默认值 | 描述 |
|--------|----------|---------|-------------|
| `title` | 是 | — | 任务标题 |
| `-l, --list` | 否 | （默认列表） | 目标列表名称。如果未指定，将使用用户的默认列表。 |
| `-p, --priority` | 否 | `normal` | 优先级：`low`、`normal`、`high` |
| `-d, --due` | 否 | — | 截止日期。支持从现在起的天数（如`3`或`3d`）或日期（如`2026-02-15`）。**注意**：仅支持日期，不支持时间。 |
| `-r, --reminder` | 否 | — | 提醒时间。格式：`3h`（小时）、`2d`（天）、`2026-02-15 14:30`（日期+时间，需要加引号）、`2026-02-15T14:30:00`（ISO格式）、`2026-02-15`（仅日期，默认为09:00）。 |
| `-R, --recurrence` | 否 | — | 重复模式。格式：`daily`（每天）、`weekdays`（周一至周五）、`weekly`（每周）、`monthly`（每月）。间隔示例：`daily:2`（每2天）、`weekly:3`（每3周）、`monthly:2`（每2个月）。**注意**：会自动设置开始日期。 |
| `-D, --description` | 否 | — | 任务描述/备注 |
| `-t, --tags` | 否 | — | 逗号分隔的标签（例如，“work,urgent”） |

**行为**：如果指定的列表不存在，系统会自动创建该列表。

**输出示例：**
```
✓ List created: Work
✓ Task added: Complete report
```

#### `complete` — 将任务标记为已完成

```bash
uv run scripts/ms-todo-sync.py complete "<title>" [-l "<list>"]
```

| 选项 | 必需 | 默认值 | 描述 |
|--------|----------|---------|-------------|
| `title` | 是 | — | 任务标题 |
| `-l, --list` | 否 | （默认列表） | 任务所在的列表名称。如果未指定，将使用用户的默认列表。 |

输出：`✓ 任务已完成：<title>`

#### `delete` — 删除任务

```bash
uv run scripts/ms-todo-sync.py delete "<title>" [-l "<list>"] [-y]
```

| 选项 | 必需 | 默认值 | 描述 |
|--------|----------|---------|-------------|
| `title` | 是 | — | 任务标题 |
| `-l, --list` | 否 | （默认列表） | 列表名称。如果未指定，将使用用户的默认列表。 |
| `-y, --yes` | 否 | — | 跳过确认提示 |

> ⚠️ 这是一个破坏性操作。如果不使用`-y`，命令会提示用户确认。在常规清理或用户明确表示同意删除时，可以使用`-y`来避免阻塞。

输出：`✓ 任务删除成功：<title>`

---

### 任务视图

#### `tasks` — 列出特定列表中的任务

```bash
uv run scripts/ms-todo-sync.py tasks "<list>" [-a]
```

| 选项 | 必需 | 默认值 | 描述 |
|--------|----------|---------|-------------|
| `list` | 是 | — | 列表名称 |
| `-a, --all` | 否 | — | 包括已完成的任务（默认：仅显示未完成的任务） |

**输出示例：**
```
📋 Tasks in list "Work" (2 total):

1. [In Progress] Write documentation ⭐
2. [In Progress] Review PR
```

#### `pending` — 查看所有列表中未完成的任务

```bash
uv run scripts/ms-todo-sync.py pending [-g]
```

| 选项 | 必需 | 描述 |
|--------|----------|-------------|
| `-g, --group` | 否 | 按列表分组结果 |

**使用`-g`时的输出示例：**
```
📋 All incomplete tasks (3 total):

📂 Work:
  [In Progress] Write documentation ⭐
  [In Progress] Review PR

📂 Shopping:
  [In Progress] Buy groceries
```

#### `today` — 查看今天到期的任务

```bash
uv run scripts/ms-todo-sync.py today
```

列出今天到期的未完成任务。如果没有找到到期任务，输出：`📅 今天没有到期的任务`。

#### `overdue` — 查看逾期任务

```bash
uv run scripts/ms-todo-sync.py overdue
```

**输出示例：**
```
⚠️  Overdue tasks (1 total):

[In Progress] Submit report ⭐
   List: Work
   Overdue: 3 days
```

#### `detail` — 查看任务详细信息

```bash
uv run scripts/ms-todo-sync.py detail "<title>" [-l "<list>"]
```

| 选项 | 必需 | 默认值 | 描述 |
|--------|----------|---------|-------------|
| `title` | 是 | — | 任务标题（支持**部分/模糊匹配**） |
| `-l, --list` | 否 | （默认列表） | 列表名称。如果未指定，将使用用户的默认列表。 |

当有多个匹配项时，返回最近修改的**未完成**任务。如果所有匹配项都已完成，则返回最近修改的已完成任务。

#### `search` — 按关键词搜索任务

```bash
uv run scripts/ms-todo-sync.py search "<keyword>"
```

在所有列表中搜索任务标题和备注（不区分大小写）。

**输出示例：**
```
🔍 Search results (1 found):

[In Progress] Write documentation ⭐
   List: Work
```

#### `stats` — 任务统计信息

```bash
uv run scripts/ms-todo-sync.py stats
```

**输出示例：**
```
📊 Task Statistics:

  Total lists: 3
  Total tasks: 15
  Completed: 10
  Pending: 5
  High priority: 2
  Overdue: 1

  Completion rate: 66.7%
```

#### `export` — 将所有任务导出为JSON

```bash
uv run scripts/ms-todo-sync.py export [-o "<filename>"]
```

| 选项 | 必需 | 默认值 | 描述 |
|--------|----------|---------|-------------|
| `-o, --output` | 否 | `todo_export.json` | 输出文件路径 |

输出：`✓ 任务已导出至：<filename>`

---

## 错误处理

### 错误代码

| 代码 | 含义 |
|------|---------|
| `0` | 成功 |
| `1` | 失败（未登录、API错误、参数无效等） |

### 常见错误信息

| 错误 | 原因 | 解决方案 |
|-------|-------|------------|
| `❌ 未登录` | 未缓存令牌或令牌过期 | 先运行`login get`，然后运行`login verify` |
| `ModuleNotFoundError: 未找到名为'msal'的模块` | 依赖项未安装 | 运行`uv sync`或`pip install -r requirements.txt` |
| `❌ 列表未找到：<name>` | 指定的列表不存在 | 使用`lists`命令检查列表名称 |
| `❌ 任务未找到：<name>` | 未找到具有指定标题的任务 | 使用`tasks`或`search`命令检查任务标题 |
| `❌ 错误：<message>` | API或网络错误 | 重试；检查网络连接；使用`--debug`获取详细信息 |

---

## 代理使用指南

### 关键规则

1. **工作目录**：在运行命令之前，务必使用`cd`进入包含此SKILL.md文件的目录。
2. **依赖项安装**：首次使用或遇到导入错误时，运行`uv sync`以确保所有依赖项都已安装。
3. **任务列表管理**：
   - 添加任务时：
     - 首先运行`lists`查看可用的任务列表
     - 如果用户未指定列表，任务将添加到他们的**默认列表**（`wellknownListName: "defaultList"`）
     - 智能地将任务分类到相应的列表中（例如，“Work”、“Personal”、“Shopping”）
     - 如果用户指定了上下文（工作、家庭、购物等），使用或创建相应的列表
     - 如果列表不存在，系统会自动创建，因此请使用有意义的列表名称
4. **破坏性操作**：对于`delete`和`delete-list`命令：
     - 这些命令默认会提示用户确认（会导致阻塞）
     - 仅在以下情况下使用`-y`标志跳过确认：
       - 用户明确要求不进行确认
       - 删除操作意图明确且已通过对话确认
     - 如果有疑问，请先询问用户确认
5. **全局选项的位置**：`-v`和`--debug`必须放在子命令之前。
6. **不要自动重试`login verify`：此命令会阻塞，等待用户完成浏览器操作。只有在用户确认后才能调用它。
7. **先检查登录状态**：在执行任何任务操作之前，先运行一个简单的命令（如`lists`）来验证身份。优雅地处理“未登录”的错误。

### 代理的推荐工作流程

```
1. cd <skill_directory>
2. uv sync                                       # Ensure dependencies are installed (first time or after updates)
3. uv run scripts/ms-todo-sync.py lists          # Test auth & see available lists
   → If fails with exit code 1 ("Not logged in"):
     a. uv run scripts/ms-todo-sync.py login get  # Get code
     b. Present URL + code to user
     c. Wait for user confirmation
     d. uv run scripts/ms-todo-sync.py login verify
4. When adding tasks:
   → Analyze task context from user's description
   → Choose or create appropriate list name:
     - Work-related → "Work" list
     - Personal errands → "Personal" list  
     - Shopping items → "Shopping" list
     - Project-specific → Use project name as list
   → Add task with appropriate list via `-l` option
5. Verify results (e.g., list tasks after adding)
```

**任务分类示例：**
- “购买牛奶” → 添加到购物列表（或使用默认列表）
- “准备会议报告” → 添加到工作列表
- “预约牙医” → 添加到个人列表（或使用默认列表）
- “审查认证服务的PR” → 添加到工作或项目特定列表

**注意**：如果没有指定列表，任务将添加到用户的默认Microsoft To Do列表中。

### 任务标题匹配

- `complete`和`delete`操作要求**完全匹配任务标题**。
- `detail`和`search`操作支持**部分/模糊关键词匹配**（不区分大小写）。
- 如果有疑问，先使用`search`找到准确的标题，然后再使用相应的命令。

### 默认列表行为

当未指定`-l`选项时，工具会使用用户的默认Microsoft To Do列表（通常是“Tasks”）。要指定特定列表，请使用`-l`选项。

---

## 快速示例

```bash
# Check existing lists first
uv run scripts/ms-todo-sync.py lists

# Add task to specific list (list auto-created if needed)
uv run scripts/ms-todo-sync.py add "Report" -l "Work" -p high -d 3 -D "Q4 financials"

# Add task to default list (no -l option)
uv run scripts/ms-todo-sync.py add "Buy milk"

# Add task with reminder in 2 hours
uv run scripts/ms-todo-sync.py add "Call client" -r 2h

# Add task with specific reminder date and time
uv run scripts/ms-todo-sync.py add "Meeting" -d 2026-03-15 -r "2026-03-15 14:30"

# Add recurring tasks
uv run scripts/ms-todo-sync.py add "Daily standup" -l "Work" -R daily -d 7
uv run scripts/ms-todo-sync.py add "Weekly review" -R weekly -d 2026-02-17
uv run scripts/ms-todo-sync.py add "Gym" -R weekdays -l "Personal"  
uv run scripts/ms-todo-sync.py add "Monthly report" -R monthly -p high -d 30

# Search then complete (use exact title from search results)
uv run scripts/ms-todo-sync.py search "report"
uv run scripts/ms-todo-sync.py complete "Report" -l "Work"

# Delete (use -y only when user intent is clear)
uv run scripts/ms-todo-sync.py delete "Old task" -y

# Views
uv run scripts/ms-todo-sync.py -v pending -g          # all pending, grouped
uv run scripts/ms-todo-sync.py -v detail "report"      # task detail with fuzzy match
uv run scripts/ms-todo-sync.py export -o "backup.json"  # export all
```