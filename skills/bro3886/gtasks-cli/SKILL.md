---
name: gtasks-cli
description: 通过命令行管理 Google 任务：查看、创建、更新和删除任务以及任务列表。当用户需要与 Google 任务进行交互、管理待办事项、创建任务列表、标记任务为已完成或检查其 Google 任务状态时，可以使用此方法。
license: MIT
compatibility: Requires gtasks CLI tool to be installed and authenticated
metadata:
  author: BRO3886
  version: "1.0"
allowed-tools: Bash(gtasks:*)
---

# Google Tasks CLI 技能

此技能允许您使用 `gtasks` CLI 工具直接从命令行管理 Google 任务。

## 先决条件

在使用任何命令之前，请确保满足以下要求：

### 1. 安装 gtasks

检查系统中是否已安装 gtasks：

```bash
# Cross-platform check (works on macOS, Linux, Windows Git Bash)
gtasks --version 2>/dev/null || gtasks.exe --version 2>/dev/null || echo "gtasks not found"

# Or use which/where commands
# macOS/Linux:
which gtasks

# Windows (Command Prompt):
where gtasks

# Windows (PowerShell):
Get-Command gtasks
```

**如果未安装 gtasks：**

1. 从 [GitHub Releases](https://github.com/BRO3886/gtasks/releases) 下载适用于您系统的二进制文件。
2. 安装它：
   - **macOS/Linux**：将其移至 `/usr/local/bin` 或添加到 PATH 环境变量中。
   - **Windows**：将其添加到 PATH 环境变量中的某个文件夹中。
3. 验证安装：`gtasks --version`

**重要提示（针对代理）：** 在尝试使用 gtasks 之前，请务必检查其是否已安装。如果找不到该命令，请告知用户并提供安装说明。

### 2. 环境变量

将 Google OAuth2 凭据设置为环境变量：

```bash
export GTASKS_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GTASKS_CLIENT_SECRET="your-client-secret"
```

**获取凭据的方法：**
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)。
2. 创建一个新的项目或选择一个现有的项目。
3. 启用 Google Tasks API。
4. 创建 OAuth2 凭据（应用程序类型：“Web 应用程序”）。
5. 添加授权的回调 URI：
   - `http://localhost:8080/callback`
   - `http://localhost:8081/callback`
   - `http://localhost:8082/callback`
   - `http://localhost:9090/callback`
   - `http://localhost:9091/callback`

**为了永久设置**，将这些 URI 添加到您的 shell 配置文件（如 `~/.bashrc`、`~/.zshrc` 等）中：

```bash
echo 'export GTASKS_CLIENT_ID="your-client-id"' >> ~/.bashrc
echo 'export GTASKS_CLIENT_SECRET="your-client-secret"' >> ~/.bashrc
source ~/.bashrc
```

### 2. 认证

设置环境变量后，使用 Google 进行认证：

```bash
gtasks login
```

这将打开一个浏览器窗口进行 OAuth2 认证。认证生成的令牌将存储在 `~/.gtasks/token.json` 文件中。

## 核心概念

- **任务列表**：用于存储任务的容器（例如 “工作”、“个人”、“购物”）。
- **任务**：任务列表中的单个待办事项。
- **任务属性**：标题（必填）、备注/描述（可选）、截止日期（可选）、状态（待办/已完成）。

## 命令结构

所有命令都遵循以下模式：
```
gtasks [command] [subcommand] [flags] [arguments]
```

## 认证

### 登录
```bash
gtasks login
```
打开浏览器窗口进行 Google OAuth2 认证。在使用其他命令之前必须先完成此步骤。

### 注销
```bash
gtasks logout
```
从 `~/.gtasks/token.json` 中删除存储的凭据。

## 任务列表管理

### 查看所有任务列表
```bash
gtasks tasklists view
```
显示所有任务列表，并附带编号索引。

**输出示例：**
```
[1] My Tasks
[2] Work
[3] Personal
```

### 创建任务列表
```bash
gtasks tasklists add -t "Work Projects"
gtasks tasklists add --title "Shopping List"
```
使用指定的标题创建一个新的任务列表。

**标志参数：**
- `-t, --title`：任务列表的标题（必填）。

### 删除任务列表
```bash
gtasks tasklists rm
```
通过交互式提示选择要删除的任务列表。

### 更新任务列表标题
```bash
gtasks tasklists update -t "New Title"
```
通过交互式提示选择任务列表并更新其标题。

**标志参数：**
- `-t, --title`：任务列表的新标题（必填）。

## 任务管理

所有任务命令都可以选择性地使用 `-l` 标志来指定任务列表。如果省略此标志，系统会提示您选择任务列表。

### 查看任务

**基本视图：**
```bash
gtasks tasks view
gtasks tasks view -l "Work"
```

**包含已完成的任务：**
```bash
gtasks tasks view --include-completed
gtasks tasks view -i
```

**仅显示已完成的任务：**
```bash
gtasks tasks view --completed
```

**对任务进行排序：**
```bash
gtasks tasks view --sort=due        # Sort by due date
gtasks tasks view --sort=title      # Sort by title
gtasks tasks view --sort=position   # Sort by position (default)
```

**输出格式：**
```bash
gtasks tasks view --format=table    # Table format (default)
gtasks tasks view --format=json     # JSON output
gtasks tasks view --format=csv      # CSV output
```

**表格输出示例：**
```
Tasks in Work:
No  Title              Description         Status     Due
1   Finish report      Q4 analysis         pending    25 December 2024
2   Team meeting       Weekly sync         pending    -
3   Code review        PR #123            completed  20 December 2024
```

**JSON 输出示例：**
```json
[
  {
    "number": 1,
    "title": "Finish report",
    "description": "Q4 analysis",
    "status": "pending",
    "due": "2024-12-25"
  }
]
```

### 创建任务

**交互式模式：**
```bash
gtasks tasks add
gtasks tasks add -l "Work"
```
提示用户输入任务标题、备注和截止日期。

**标志模式：**
```bash
gtasks tasks add -t "Buy groceries"
gtasks tasks add -t "Finish report" -n "Q4 analysis" -d "2024-12-25"
gtasks tasks add -t "Call dentist" -d "tomorrow"
gtasks tasks add -t "Team meeting" -d "Dec 25"
```

**标志参数：**
- `-t, --title`：任务标题（非交互式模式必填）。
- `-n, --note`：任务备注/描述（可选）。
- `-d, --due`：截止日期（可选，支持多种格式）。

**日期格式示例：**
日期解析器支持多种格式：
- `2024-12-25`（ISO 格式）
- `Dec 25, 2024`
- `December 25`
- `tomorrow`
- `next Friday`
- `12/25/2024`

有关所有支持的格式，请参阅 [dateparse 示例](https://github.com/araddon/dateparse#extended-example)。

### 将任务标记为已完成

**通过任务编号：**
```bash
gtasks tasks done 1
gtasks tasks done 3 -l "Work"
```

**交互式模式：**
```bash
gtasks tasks done
gtasks tasks done -l "Personal"
```
提示用户从列表中选择要标记为已完成的任务。

### 删除任务

**通过任务编号：**
```bash
gtasks tasks rm 2
gtasks tasks rm 1 -l "Shopping"
```

**交互式模式：**
```bash
gtasks tasks rm
gtasks tasks rm -l "Work"
```
提示用户选择要删除的任务。

### 查看任务详情

**通过任务编号：**
```bash
gtasks tasks info 1
gtasks tasks info 3 -l "Work"
```

**交互式模式：**
```bash
gtasks tasks info
gtasks tasks info -l "Personal"
```

**输出示例：**
```
Task: Finish report
Status: Needs action
Due: 25 December 2024
Notes: Complete Q4 analysis and submit to manager

Links:
  - https://docs.google.com/document/d/...

View in Google Tasks: https://tasks.google.com/...
```

## 常见工作流程

### 快速创建任务
当用户说 “在我的工作列表中添加一个任务” 时：
```bash
gtasks tasks add -l "Work" -t "Task title"
```

### 查看今天的任务
```bash
gtasks tasks view --sort=due
```

### 完成多个任务
```bash
gtasks tasks done -l "Work"
# Interactive prompt appears, select task
gtasks tasks done -l "Work"
# Repeat as needed
```

### 查看所有列表中的任务
可以多次运行查看命令来查看每个列表中的任务，或者先列出所有任务列表：
```bash
gtasks tasklists view
gtasks tasks view -l "Work"
gtasks tasks view -l "Personal"
```

### 导出任务
```bash
gtasks tasks view --format=json > tasks.json
gtasks tasks view --format=csv > tasks.csv
```

## 最佳实践

1. **始终先检查认证状态**：如果命令因认证错误而失败，请运行 `gtasks login`。
2. **在自动化脚本中使用任务列表标志**：在编写脚本或用户指定列表名称时，使用 `-l` 标志以避免交互式提示。
3. **利用灵活的日期解析功能**：`--due` 标志支持自然语言日期格式，如 “tomorrow”、“next week” 等。
4. **选择合适的输出格式**：
   - 表格格式适合人类阅读。
   - JSON 格式适用于与其他工具集成或解析。
   - CSV 格式适用于导入到电子表格中。
5. **任务编号是临时生成的**：任务编号会在任务添加、完成或删除后发生变化。请务必先查看列表以获取当前编号。
6. **优雅地处理不存在的列表**：如果用户指定了不存在的列表名称，命令会报错。请使用 `gtasks tasklists view` 先验证列表名称。

## 错误处理

常见错误及解决方法：

- **“无法获取服务”** 或 **认证错误**：
  - 首先确保环境变量已设置：`echo $GTASKS_CLIENT_ID`。
  - 如果环境变量未设置，请将其导出（参见先决条件部分），然后运行 `gtasks login` 进行认证。
- **“任务列表名称错误”**：指定的列表名称不存在。使用 `gtasks tasklists view` 查看可用的列表。
- **“任务编号错误”**：任务编号无效。使用 `gtasks tasks view` 查看当前的任务编号。
- **“日期格式不正确”**：日期字符串无法解析。请使用格式如 “2024-12-25”、“tomorrow” 或 “Dec 25”。

## 示例

### 示例 1：创建购物列表并添加项目
```bash
gtasks tasklists add -t "Shopping"
gtasks tasks add -l "Shopping" -t "Milk"
gtasks tasks add -l "Shopping" -t "Bread"
gtasks tasks add -l "Shopping" -t "Eggs"
```

### 示例 2：查看并完成工作任务
```bash
gtasks tasks view -l "Work" --sort=due
gtasks tasks done 1 -l "Work"
```

### 示例 3：创建带有截止日期的任务
```bash
gtasks tasks add -l "Work" -t "Submit proposal" -n "Include budget and timeline" -d "next Friday"
```

### 示例 4：导出已完成的任务
```bash
gtasks tasks view --completed --format=json -l "Work" > completed_work.json
```

## 代理使用提示

### 在运行任何命令之前

1. **先检查 gtasks 是否已安装**：
   ```bash
   # Try to run gtasks version check
   gtasks --version 2>/dev/null || gtasks.exe --version 2>/dev/null
   ```
   如果未安装，请告知用户并提供先决条件部分中的安装说明。
2. **验证环境变量是否已设置**：
   ```bash
   # Check if variables exist (macOS/Linux)
   [ -n "$GTASKS_CLIENT_ID" ] && echo "GTASKS_CLIENT_ID is set" || echo "GTASKS_CLIENT_ID is not set"
   [ -n "$GTASKS_CLIENT_SECRET" ] && echo "GTASKS_CLIENT_SECRET is set" || echo "GTASKS_CLIENT_SECRET is not set"

   # Windows PowerShell
   if ($env:GTASKS_CLIENT_ID) { "GTASKS_CLIENT_ID is set" } else { "GTASKS_CLIENT_ID is not set" }
   if ($env:GTASKS_CLIENT_SECRET) { "GTASKS_CLIENT_SECRET is set" } else { "GTASKS_CLIENT_SECRET is not set" }
   ```

3. **检查认证状态**：
   ```bash
   gtasks tasklists view &>/dev/null && echo "Authenticated" || echo "Not authenticated - run 'gtasks login'"
   ```

### 通用提示

- 当用户提到 “任务” 但没有指定工具时，询问他们是否想使用 Google Tasks。
- 如果用户询问他们的任务，请先运行 `gtasks tasklists view` 查看可用的列表。
- 如果用户没有指定任务列表，请始终确认要使用哪个列表。
- 在创建带有日期的任务时，建议使用明确的日期格式（YYYY-MM-DD），以提高清晰度。
- 请记住任务编号是从 1 开始计数的，并会在任务修改后发生变化。
- 如果命令需要交互式操作，但在非交互式模式下运行，请使用标志参数提供所有必要的信息。