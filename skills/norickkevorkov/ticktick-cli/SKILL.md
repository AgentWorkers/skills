---
name: ticktick
description: 通过 OAuth2 认证、批量操作以及速率限制管理功能，从命令行界面来管理 TickTick 的任务和项目。
---

# TickTick CLI 技能

通过命令行管理 TickTick 任务和项目。

## 设置

### 1. 注册 TickTick 开发者应用

1. 访问 [TickTick 开发者中心](https://developer.ticktick.com/manage)
2. 创建一个新的应用
3. 将重定向 URI 设置为 `http://localhost:8080`
4. 记下您的 `Client ID` 和 `Client Secret`

### 2. 验证身份

```bash
# Set credentials and start OAuth flow
bun run scripts/ticktick.ts auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

# Check authentication status
bun run scripts/ticktick.ts auth --status

# Logout (clear tokens, keep credentials)
bun run scripts/ticktick.ts auth --logout
```

### 无头/手动身份验证

```bash
# Use manual mode on headless servers
bun run scripts/ticktick.ts auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --manual
```

此操作会生成一个授权 URL。在浏览器中打开该 URL，批准访问权限后，复制完整的重定向 URL（格式如下：`http://localhost:8080/?code=XXXXX&state=STATE`），然后将其粘贴回 CLI 中。

CLI 会自动在浏览器中打开页面以完成身份验证。验证通过后，授权令牌会被存储在 `~/.clawdbot/credentials/ticktick-cli/config.json` 文件中。

## 命令

### 列出任务

```bash
# List all tasks
bun run scripts/ticktick.ts tasks

# List tasks from a specific project
bun run scripts/ticktick.ts tasks --list "Work"

# Filter by status
bun run scripts/ticktick.ts tasks --status pending
bun run scripts/ticktick.ts tasks --status completed

# JSON output
bun run scripts/ticktick.ts tasks --json
```

### 创建任务

```bash
# Basic task creation
bun run scripts/ticktick.ts task "Buy groceries" --list "Personal"

# With description and priority
bun run scripts/ticktick.ts task "Review PR" --list "Work" --content "Check the new auth changes" --priority high

# With due date
bun run scripts/ticktick.ts task "Submit report" --list "Work" --due tomorrow
bun run scripts/ticktick.ts task "Plan vacation" --list "Personal" --due "in 7 days"
bun run scripts/ticktick.ts task "Meeting" --list "Work" --due "2024-12-25"

# With tags
bun run scripts/ticktick.ts task "Research" --list "Work" --tag research important
```

### 更新任务

```bash
# Update by task name or ID
bun run scripts/ticktick.ts task "Buy groceries" --update --priority medium
bun run scripts/ticktick.ts task "abc123" --update --due tomorrow --content "Updated notes"

# Limit search to specific project
bun run scripts/ticktick.ts task "Review PR" --update --list "Work" --priority low
```

### 完成任务

```bash
# Mark task as complete
bun run scripts/ticktick.ts complete "Buy groceries"

# Complete with project filter
bun run scripts/ticktick.ts complete "Review PR" --list "Work"
```

### 放弃任务

```bash
# Mark task as won't do
bun run scripts/ticktick.ts abandon "Old task"

# Abandon with project filter
bun run scripts/ticktick.ts abandon "Obsolete item" --list "Do"
```

### 批量放弃任务（多个任务）

```bash
# Abandon multiple tasks in a single API call
bun run scripts/ticktick.ts batch-abandon <taskId1> <taskId2> <taskId3>

# With JSON output
bun run scripts/ticktick.ts batch-abandon abc123def456... xyz789... --json
```

注意：`batch-abandon` 命令需要任务 ID（24 位的十六进制字符串），而非任务名称。请先使用 `tasks --json` 命令获取任务 ID。

### 列出项目

```bash
# List all projects
bun run scripts/ticktick.ts lists

# JSON output
bun run scripts/ticktick.ts lists --json
```

### 创建项目

```bash
# Create new project
bun run scripts/ticktick.ts list "New Project"

# With color
bun run scripts/ticktick.ts list "Work Tasks" --color "#FF5733"
```

### 更新项目

```bash
# Rename project
bun run scripts/ticktick.ts list "Old Name" --update --name "New Name"

# Change color
bun run scripts/ticktick.ts list "Work" --update --color "#00FF00"
```

## 选项参考

### 优先级级别
- `none` - 无优先级（默认值）
- `low` - 低优先级
- `medium` - 中等优先级
- `high` - 高优先级

### 截止日期格式
- `today` - 今天到期
- `tomorrow` - 明天到期
- `in N days` - N 天后到期（例如：“in 3 days”）
- `next monday` - 下一个工作日到期
- ISO 日期格式 - `YYYY-MM-DD` 或完整的 ISO 格式

### 全局选项
- `--json` - 以 JSON 格式输出结果（适用于脚本编写）
- `--help` - 显示任意命令的帮助信息

## 代理使用提示

当将此技能作为 AI 代理使用时，请注意以下事项：

1. **始终使用 `--json` 标志** 以获得机器可读的输出结果。
2. **先使用 `lists --json` 命令列出所有项目，以获取有效的项目 ID**。
3. **尽可能使用项目 ID 而不是项目名称，以确保操作的准确性**。
4. **在完成任务前检查任务状态，以避免错误**。

示例代理工作流程：
```bash
# 1. Get available projects
bun run scripts/ticktick.ts lists --json

# 2. Create a task in a specific project
bun run scripts/ticktick.ts task "Agent task" --list "PROJECT_ID" --priority high --json

# 3. Later, mark it complete
bun run scripts/ticktick.ts complete "Agent task" --list "PROJECT_ID" --json
```

## 配置

授权令牌存储在 `~/.clawdbot/credentials/ticktick-cli/config.json` 文件中：
```json
{
  "clientId": "YOUR_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET",
  "accessToken": "...",
  "refreshToken": "...",
  "tokenExpiry": 1234567890000,
  "redirectUri": "http://localhost:8080"
}
```

注意：凭证以明文形式存储。CLI 会尝试将文件的权限设置为 700/600；请将此文件视为敏感文件。

CLI 会在令牌过期时自动刷新它们。

## 故障排除

### 出现 “未授权” 错误
运行 `bun run scripts/ticktick.ts auth` 命令进行身份验证。

### 出现 “项目未找到” 错误
使用 `bun run scripts/ticktick.ts lists` 命令查看可用项目及其 ID。

### 出现 “任务未找到” 错误
- 确保任务标题完全匹配（不区分大小写）。
- 尝试使用任务 ID 进行操作。
- 使用 `--list` 命令将搜索范围缩小到特定项目。

### 令牌过期错误
CLI 应该会自动刷新令牌。如果问题仍然存在，请再次运行 `bun run scripts/ticktick.ts auth` 命令。

## API 说明

此 CLI 使用的是 [TickTick Open API v1](https://developer.ticktick.com/api)。

### 限制
- **每分钟 100 次请求**
- **每 5 分钟 300 次请求**

由于 CLI 在执行某些操作（如列出项目以查找任务）时需要多次调用 API，因此批量操作可能会很快达到请求限制。

### 批量操作端点
CLI 支持 TickTick 的批量操作端点：
```
POST https://api.ticktick.com/open/v1/batch/task
{
  "add": [...],    // CreateTaskInput[]
  "update": [...], // UpdateTaskInput[]
  "delete": [...]  // { taskId, projectId }[]
}
```
可以使用 `batch-abandon` 命令一次性放弃多个任务。批量 API 方法也可用于程序化操作。

### 其他限制
- 每个项目最多支持 500 个任务。
- 一些高级功能（如专注时间、习惯设置）不支持通过 API 进行操作。