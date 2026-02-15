---
name: claude-team
description: 通过 `iTerm2` 和 `claude-team MCP` 服务器来协调多个 Claude Code 工作进程。使用 `git worktrees` 创建新的工作进程，分配相关任务（如 “beads issues”），监控开发进度，并协调各个进程的并行开发工作。
homepage: https://github.com/Martian-Engineering/claude-team
metadata: {"clawdbot":{"emoji":"👥","os":["darwin"],"requires":{"bins":["mcporter"]}}}
---

# Claude Team

Claude Team 是一个 MCP（Mission Control Panel）服务器，允许您通过 iTerm2 创建和管理 Claude Code 会话团队。每个工作者都有自己的终端窗口、可选的 Git 工作区（worktree），并且可以分配任务（beads issues）。

## 为什么使用 Claude Team？

- **并行性**：将任务分配给多个工作者同时执行
- **上下文隔离**：每个工作者都有独立的上下文，确保协调者的上下文保持清晰
- **可视性**：您可以实时查看、中断或接管 Claude Code 会话
- **Git 工作区**：每个工作者都可以拥有独立的工作分支

## ⚠️ 重要规则

**切勿直接修改代码。**务必通过创建新的工作者来执行代码修改。这样可以保持上下文的清晰，并确保正确的 Git 工作流程。

## 先决条件

- 安装了 macOS 并启用了 iTerm2（已启用 Python API：偏好设置 → 通用 → Magic → 启用 Python API）
- 在 `~/.claude.json` 中配置了 claude-team MCP 服务器

## 通过 mcporter 使用

所有工具都通过 `mcporter call claude-team.<tool>` 来调用：

```bash
mcporter call claude-team.list_workers
mcporter call claude-team.spawn_workers workers='[{"project_path":"/path/to/repo","bead":"cp-123"}]'
```

## 核心工具

### spawn_workers

创建新的 Claude Code 工作者会话。

```bash
mcporter call claude-team.spawn_workers \
  workers='[{
    "project_path": "/path/to/repo",
    "bead": "cp-123",
    "annotation": "Fix auth bug",
    "use_worktree": true,
    "skip_permissions": true
  }]' \
  layout="auto"
```

**工作者配置字段：**
- `project_path`：必填。仓库路径或 "auto"（使用 CLAUDE_TEAMPROJECT_DIR）
- `bead`：可选的任务 ID — 工作者将按照任务流程执行
- `annotation`：任务描述（显示在徽章上，用于分支名称）
- `prompt`：附加指令（如果没有任务，则作为工作者的默认任务）
- `use_worktree`：创建独立的 Git 工作区（默认：true）
- `skip_permissions`：是否跳过权限检查（默认：false）
- `name`：可选的工作者名称（否则会自动从主题列表中选择）

**布局选项：**
- `"auto"`：重用现有的 Claude Team 窗口，并根据可用空间进行布局
- `"new"`：始终创建新的窗口（1-4 个工作者以网格布局显示）

### list_workers

查看所有被管理的工作者：

```bash
mcporter call claude-team.list_workers
mcporter call claude-team.list_workers status_filter="ready"
```

状态值：`spawning`、`ready`、`busy`、`closed`

### message_workers

向一个或多个工作者发送消息：

```bash
mcporter call claude-team.message_workers \
  session_ids='["Groucho"]' \
  message="Please also add unit tests" \
  wait_mode="none"
```

**wait_mode 选项：**
- `"none"`：发送后立即忽略（默认）
- `"any"`：任何工作者空闲时返回结果
- `"all"`：所有工作者空闲时返回结果

### check_idle_workers / wait_idle_workers

检查或等待工作者完成任务：

```bash
# Quick poll
mcporter call claude-team.check_idle_workers session_ids='["Groucho","Harpo"]'

# Blocking wait
mcporter call claude-team.wait_idle_workers \
  session_ids='["Groucho","Harpo"]' \
  mode="all" \
  timeout=600
```

### read_worker_logs

获取对话记录：

```bash
mcporter call claude-team.read_worker_logs \
  session_id="Groucho" \
  pages=2
```

### examine_worker

获取详细状态信息，包括对话统计：

```bash
mcporter call claude-team.examine_worker session_id="Groucho"
```

### close_workers

任务完成后终止工作者：

```bash
mcporter call claude-team.close_workers session_ids='["Groucho","Harpo"]'
```

⚠️ **工作区清理**：使用工作区的工作者会将更改提交到临时分支。关闭后：
1. 查看工作者分支上的提交记录
2. 将更改合并到持久分支
3. 删除分支：`git branch -D <branch-name>`

### bd_help

任务相关命令的快速参考：

```bash
mcporter call claude-team.bd_help
```

## 工作者识别

工作者可以通过以下方式识别：
- **内部 ID**：简短的十六进制字符串（例如 `3962c5c4`）
- **终端 ID**：`iterm:UUID` 格式
- **工作者名称**：易于理解的名称（例如 `Groucho`、`Aragorn`）

## 工作流程：分配任务

```bash
# 1. Spawn worker with a bead assignment
mcporter call claude-team.spawn_workers \
  workers='[{
    "project_path": "/Users/phaedrus/Projects/myrepo",
    "bead": "proj-abc",
    "annotation": "Implement config schemas",
    "use_worktree": true,
    "skip_permissions": true
  }]'

# 2. Worker automatically:
#    - Creates worktree with branch named after bead
#    - Runs `bd show proj-abc` to understand the task
#    - Marks issue in_progress
#    - Implements the work
#    - Closes the issue
#    - Commits with issue reference

# 3. Monitor progress
mcporter call claude-team.check_idle_workers session_ids='["Groucho"]'
mcporter call claude-team.read_worker_logs session_id="Groucho"

# 4. When done, close and merge
mcporter call claude-team.close_workers session_ids='["Groucho"]'
# Then: git merge or cherry-pick from worker's branch
```

## 并行任务分配流程

```bash
# Spawn multiple workers for parallel tasks
mcporter call claude-team.spawn_workers \
  workers='[
    {"project_path": "auto", "bead": "cp-123", "annotation": "Auth module"},
    {"project_path": "auto", "bead": "cp-124", "annotation": "API routes"},
    {"project_path": "auto", "bead": "cp-125", "annotation": "Unit tests"}
  ]' \
  layout="new"

# Wait for all to complete
mcporter call claude-team.wait_idle_workers \
  session_ids='["Groucho","Harpo","Chico"]' \
  mode="all"

# Review and close
mcporter call claude-team.close_workers \
  session_ids='["Groucho","Harpo","Chico"]'
```

## 最佳实践

1. **使用任务 ID**：为工作者分配任务 ID，以便他们按照正确的流程执行任务
2. **使用工作区**：保持工作独立性，支持并行提交
3. **启用权限检查**：工作者需要设置 `skip_permissions: true` 才能写入文件
4. **监控而非微观管理**：让工作者完成任务后再进行审查
5. **谨慎合并**：在合并到主分支之前先查看工作者的分支
6. **关闭工作者**：任务完成后务必关闭工作者，以清理工作区

## HTTP 模式（可流式传输）

为了实现持久化的服务器运行，Claude Team 可以作为 HTTP 服务器运行。这样可以确保 MCP 服务器持续运行并保持数据持久化，避免重启时的数据丢失。

### 启动 HTTP 服务器

直接运行 Claude Team 的 HTTP 服务器：

```bash
# From the claude-team directory
uv run python -m claude_team_mcp --http --port 8766

# Or specify the directory explicitly
uv run --directory /path/to/claude-team python -m claude_team_mcp --http --port 8766
```

若希望登录时自动启动服务器，请使用 launchd（详见下面的“launchd 自动启动”部分）。

### mcporter.json 配置

HTTP 服务器启动后，需要配置 mcporter 以连接到该服务器。创建 `~/.mcporter/mcporter.json` 文件：

```json
{
  "mcpServers": {
    "claude-team": {
      "transport": "streamable-http",
      "url": "http://127.0.0.1:8766/mcp",
      "lifecycle": "keep-alive"
    }
  }
}
```

## HTTP 模式的优势

- **数据持久化**：工作者的状态信息在多次调用 CLI 时仍然保留
- **响应更快**：每次调用时无需重新启动 Python 环境
- **外部访问**：可以通过 cron 作业、脚本或其他工具访问服务器
- **会话恢复**：即使协调者断开连接，服务器也能记录会话状态

### 从 Claude Code 连接

更新您的 `.mcp.json` 文件以使用 HTTP 传输方式：

```json
{
  "mcpServers": {
    "claude-team": {
      "transport": "streamable-http",
      "url": "http://127.0.0.1:8766/mcp"
    }
  }
}
```

## launchd 自动启动

要实现登录时自动启动 Claude Team 服务器，请使用捆绑的设置脚本。

### 快速设置

从技能的 assets 目录运行设置脚本：

```bash
# From the skill directory
./assets/setup.sh

# Or specify a custom claude-team location
CLAUDE_TEAM_DIR=/path/to/claude-team ./assets/setup.sh
```

### 设置脚本的功能

设置脚本会：
1. 检测您的 `uv` 安装路径
2. 在 `~/.claude-team/logs/` 创建日志目录
3. 从 `assets/com.claude-team.plist.template` 生成 launchd plist 文件
4. 将其安装到 `~/Library/LaunchAgents/com.claude-team.plist`
5. 加载服务以立即启动

plist 文件使用 `uv run` 命令在端口 8766 上启动 HTTP 服务器，并配置为支持 iTerm2 的 Python API（Aqua 会话类型）。

### 服务管理

```bash
# Stop the service
launchctl unload ~/Library/LaunchAgents/com.claude-team.plist

# Restart (re-run setup)
./assets/setup.sh

# Check if running
launchctl list | grep claude-team

# View logs
tail -f ~/.claude-team/logs/stdout.log
tail -f ~/.claude-team/logs/stderr.log
```

### launchd 故障排除

```bash
# Check for load errors
launchctl print gui/$UID/com.claude-team

# Force restart
launchctl kickstart -k gui/$UID/com.claude-team

# Remove and reload (if plist changed)
launchctl bootout gui/$UID/com.claude-team
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.claude-team.plist
```

## Cron 集成

Claude Team 支持通过 cron 作业来监控和通知工作者的状态。

### 工作者状态文件

Claude Team 会将工作者的状态信息写入 `~/.claude-team/memory/worker-tracking.json` 文件：

```json
{
  "workers": {
    "Groucho": {
      "session_id": "3962c5c4",
      "bead": "cp-123",
      "annotation": "Fix auth bug",
      "status": "busy",
      "project_path": "/Users/phaedrus/Projects/myrepo",
      "started_at": "2025-01-05T10:30:00Z",
      "last_activity": "2025-01-05T11:45:00Z"
    },
    "Harpo": {
      "session_id": "a1b2c3d4",
      "bead": "cp-124",
      "annotation": "Add API routes",
      "status": "idle",
      "project_path": "/Users/phaedrus/Projects/myrepo",
      "started_at": "2025-01-05T10:30:00Z",
      "last_activity": "2025-01-05T11:50:00Z",
      "completed_at": "2025-01-05T11:50:00Z"
    }
  },
  "last_updated": "2025-01-05T11:50:00Z"
}
```

### 监控完成的 cron 作业

创建一个监控脚本 `~/.claude-team/scripts/check_workers.sh`：

```bash
#!/bin/bash
# Check for completed workers and send notifications

TRACKING_FILE="$HOME/.claude-team/memory/worker-tracking.json"
NOTIFIED_FILE="$HOME/.claude-team/memory/notified-workers.json"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID}"

# Exit if tracking file doesn't exist
[ -f "$TRACKING_FILE" ] || exit 0

# Initialize notified file if needed
[ -f "$NOTIFIED_FILE" ] || echo '{"notified":[]}' > "$NOTIFIED_FILE"

# Find idle workers that haven't been notified
IDLE_WORKERS=$(jq -r '
  .workers | to_entries[] |
  select(.value.status == "idle") |
  .key
' "$TRACKING_FILE")

for worker in $IDLE_WORKERS; do
  # Check if already notified
  ALREADY_NOTIFIED=$(jq -r --arg w "$worker" '.notified | index($w) != null' "$NOTIFIED_FILE")

  if [ "$ALREADY_NOTIFIED" = "false" ]; then
    # Get worker details
    BEAD=$(jq -r --arg w "$worker" '.workers[$w].bead // "no-bead"' "$TRACKING_FILE")
    ANNOTATION=$(jq -r --arg w "$worker" '.workers[$w].annotation // "no annotation"' "$TRACKING_FILE")

    # Send Telegram notification
    MESSAGE="🤖 Worker *${worker}* completed
📋 Bead: \`${BEAD}\`
📝 ${ANNOTATION}"

    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d chat_id="$TELEGRAM_CHAT_ID" \
      -d text="$MESSAGE" \
      -d parse_mode="Markdown" > /dev/null

    # Mark as notified
    jq --arg w "$worker" '.notified += [$w]' "$NOTIFIED_FILE" > "${NOTIFIED_FILE}.tmp"
    mv "${NOTIFIED_FILE}.tmp" "$NOTIFIED_FILE"
  fi
done
```

使其可执行：

```bash
chmod +x ~/.claude-team/scripts/check-workers.sh
```

### 添加到 crontab

将脚本添加到 crontab 中（使用 `crontab -e`）：

```cron
# Check claude-team workers every 2 minutes
*/2 * * * * TELEGRAM_BOT_TOKEN="your-bot-token" TELEGRAM_CHAT_ID="your-chat-id" ~/.claude-team/scripts/check-workers.sh
```

### 环境设置

在您的 shell 配置文件（`~/.zshrc`）中设置 Telegram 凭据：

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_CHAT_ID="-1001234567890"
```

### 替代方案：使用 clawdbot 发送通知

如果您已经配置了 clawdbot，也可以通过它来发送通知：

```bash
# In check-workers.sh, replace the curl command with:
clawdbot send --to "$TELEGRAM_CHAT_ID" --message "$MESSAGE" --provider telegram
```

### 清除通知记录

在启动新的工作者批次时，清除已通知的列表：

```bash
echo '{"notified":[]}' > ~/.claude-team/memory/notified-workers.json
```