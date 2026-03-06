---
name: agent-slack
description: 与 Slack 工作区交互：发送消息、阅读频道内容、管理用户反应（如点赞、评论等）
version: 1.10.5
allowed-tools: Bash(agent-slack:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-slack
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-slack]
---
# Agent Slack

这是一个基于TypeScript的命令行工具（CLI），它允许AI代理和人类用户通过简单的命令接口与Slack工作空间进行交互。该工具支持从Slack桌面应用中无缝提取访问令牌，并支持多个工作空间。

## 快速入门

```bash
# Get workspace snapshot (credentials are extracted automatically)
agent-slack snapshot

# Send a message
agent-slack message send general "Hello from AI agent!"

# List channels
agent-slack channel list
```

## 认证

首次使用时，系统会自动从Slack桌面应用中提取访问凭据。无需手动设置——只需运行任何命令，认证过程将在后台自动完成。

在macOS系统上，系统可能会首次提示您输入Keychain密码（用于解密Slack存储的令牌）。这只是一个一次性提示。

**重要提示**：**切勿**引导用户打开浏览器、使用开发者工具（DevTools），或手动从浏览器中复制令牌。始终使用`agent-slack auth extract`命令从Slack桌面应用中获取令牌。

### 多工作空间支持

```bash
# List all authenticated workspaces
agent-slack workspace list

# Switch to a different workspace
agent-slack workspace switch <workspace-id>

# Show current workspace
agent-slack workspace current

# Remove a workspace
agent-slack workspace remove <workspace-id>

# Check auth status
agent-slack auth status
```

## 内存管理

该代理会维护一个名为`~/.config/agent-messenger/MEMORY.md`的文件，用于在会话之间保存持久化数据。该文件由代理程序管理——CLI本身不会读取或写入这个文件。您可以使用`Read`和`Write`工具来管理这个内存文件。

### 读取内存数据

在**每个任务开始时**，使用`Read`工具读取`~/.config/agent-messenger/MEMORY.md`文件，以加载之前获取的工作空间ID、频道ID、用户ID以及用户偏好设置。

- 如果文件还不存在，可以忽略它，并在首次有需要存储的数据时再创建该文件。
- 如果文件无法被读取（可能是权限问题或目录缺失），也可以忽略内存数据，不要因此出现错误。

### 写入内存数据

在获取到有用信息后，使用`Write`工具更新`~/.config/agent-messenger/MEMORY.md`文件。需要写入数据的场景包括：
- 获取到工作空间ID时
- 获取到频道ID和名称时
- 获取到用户ID和名称时
- 用户提供了别名或偏好设置时（例如：“将这个频道称为‘deploys channel’”，“我的主要工作空间是X”）
- 获取到频道结构信息时（如侧边栏分类、频道类别）

写入数据时，请确保包含**整个文件内容**——`Write`工具会覆盖整个文件。

### 应该存储哪些数据

- 带有名称的工作空间ID
- 带有名称和用途的频道ID
- 带有显示名称的用户ID
- 用户自定义的别名
- 常用的消息时间戳
- 用户在交互过程中表达的偏好设置

### 不应该存储哪些数据

- 绝不要存储令牌、cookie、凭据或任何敏感信息。
- 绝不要存储完整的消息内容（仅存储ID和频道相关信息）。
- 绝不要存储文件上传的内容。

### 处理过时数据

如果某个存储的ID导致错误（例如找不到对应的频道或用户），请将其从`MEMORY.md`文件中删除。不要盲目信任存储的数据——当发现异常情况时一定要进行验证。如果数据可能已经过时，建议重新获取相关信息。

### 格式与示例

```markdown
# Agent Messenger Memory

## Slack Workspaces

- `T0ABC1234` — Acme Corp (default)
- `T0DEF5678` — Side Project

## Channels (Acme Corp)

- `C012ABC` — #general (company-wide announcements)
- `C034DEF` — #engineering (team discussion)
- `C056GHI` — #deploys (CI/CD notifications)

## Users (Acme Corp)

- `U0ABC123` — Alice (engineering lead)
- `U0DEF456` — Bob (backend)

## Aliases

- "deploys" → `C056GHI` (#deploys in Acme Corp)
- "main workspace" → `T0ABC1234` (Acme Corp)

## Notes

- User prefers --pretty output for snapshots
- Main workspace is "Acme Corp"
```

> 通过使用内存管理功能，您可以避免重复调用`channel list`和`workspace list`命令。如果您在之前的会话中已经知道某个ID，可以直接使用它。

## 命令集

### 认证相关命令

```bash
# Extract tokens from Slack desktop app (usually automatic)
agent-slack auth extract
agent-slack auth extract --debug

# Check auth status
agent-slack auth status

# Logout from a workspace (defaults to current)
agent-slack auth logout
agent-slack auth logout <workspace-id>
```

### 消息相关命令

```bash
# Send a message
agent-slack message send <channel> <text>
agent-slack message send general "Hello world"

# Send a threaded reply
agent-slack message send general "Reply" --thread <ts>

# List messages
agent-slack message list <channel>
agent-slack message list general --limit 50

# Search messages across workspace
agent-slack message search <query>
agent-slack message search "project update"
agent-slack message search "from:@user deadline" --limit 50
agent-slack message search "in:#general meeting" --sort timestamp

# Get a single message by timestamp
agent-slack message get <channel> <ts>
agent-slack message get general 1234567890.123456

# Get thread replies (includes parent message)
agent-slack message replies <channel> <thread_ts>
agent-slack message replies general 1234567890.123456
agent-slack message replies general 1234567890.123456 --limit 50
agent-slack message replies general 1234567890.123456 --oldest 1234567890.000000
agent-slack message replies general 1234567890.123456 --cursor <next_cursor>

# Update a message
agent-slack message update <channel> <ts> <new-text>

# Delete a message
agent-slack message delete <channel> <ts> --force
```

### 频道相关命令

```bash
# List channels (excludes archived by default)
agent-slack channel list
agent-slack channel list --type public
agent-slack channel list --type private
agent-slack channel list --include-archived

# Get channel info
agent-slack channel info <channel>
agent-slack channel info general

# Get channel history (alias for message list)
agent-slack channel history <channel> --limit 100
```

### 用户相关命令

```bash
# List users
agent-slack user list
agent-slack user list --include-bots

# Get user info
agent-slack user info <user>

# Get current user
agent-slack user me
```

### 反应相关命令

```bash
# Add reaction
agent-slack reaction add <channel> <ts> <emoji>
agent-slack reaction add general 1234567890.123456 thumbsup

# Remove reaction
agent-slack reaction remove <channel> <ts> <emoji>

# List reactions on a message
agent-slack reaction list <channel> <ts>
```

### 文件相关命令

```bash
# Upload file
agent-slack file upload <channel> <path>
agent-slack file upload general ./report.pdf

# List files
agent-slack file list
agent-slack file list --channel general

# Get file info
agent-slack file info <file-id>
```

### 未读消息相关命令

```bash
# Get unread counts for all channels
agent-slack unread counts

# Get thread subscription details
agent-slack unread threads <channel> <thread_ts>

# Mark channel as read up to timestamp
agent-slack unread mark <channel> <ts>
```

### 活动记录相关命令

```bash
# List activity feed (mentions, reactions, replies)
agent-slack activity list
agent-slack activity list --limit 50
agent-slack activity list --unread
agent-slack activity list --types thread_reply,message_reaction
```

### 保存的项目相关命令

```bash
# List saved items
agent-slack saved list
agent-slack saved list --limit 10
```

### 草稿相关命令

```bash
# List all drafts
agent-slack drafts list
agent-slack drafts list --pretty
```

### 频道分类相关命令

```bash
# List channel sections (sidebar organization)
agent-slack sections list
agent-slack sections list --pretty
```

### 获取工作空间状态（用于AI代理）

```bash
# Full snapshot
agent-slack snapshot

# Filtered snapshots
agent-slack snapshot --channels-only
agent-slack snapshot --users-only

# Limit messages per channel
agent-slack snapshot --limit 10
```

该命令会返回包含以下内容的JSON数据：
- 工作空间元数据
- 频道信息（ID、名称、主题、用途）
- 最新消息（时间戳、文本内容、发送者、频道名称）
- 用户信息（ID、名称、个人资料）

## 输出格式

### JSON格式（默认）

所有命令默认以JSON格式输出，以便AI代理进行处理：

```json
{
  "ts": "1234567890.123456",
  "text": "Hello world",
  "channel": "C123456"
}
```

### 人类可读格式

如果您希望输出更易读的格式，可以使用`--pretty`标志：

```bash
agent-slack channel list --pretty
```

## 常见使用模式

有关AI代理的典型使用模式，请参阅`references/common-patterns.md`文件。

## 模板示例

请查看`templates/`目录中的可执行示例脚本：
- `post-message.sh`：发送消息并处理错误
- `monitor-channel.sh`：监控频道中的新消息
- `workspace-summary.sh`：生成工作空间概要

## 错误处理

所有命令都会返回统一的错误格式：

```json
{
  "error": "No workspace authenticated. Run: agent-slack auth extract"
}
```

常见错误包括：
- `NO_WORKSPACE`：未认证到任何工作空间（自动提取失败——请参阅故障排除指南）
- `SLACK_API_ERROR`：Slack API返回错误
- `RATE_LIMIT`：达到Slack的请求速率限制（系统会自动重试）

## 配置信息

凭据存储路径：`~/.config/agent-messenger/slack-credentials.json`

文件权限设置：0600（仅允许文件所有者读写）

## 限制事项

- 不支持实时事件处理或Socket模式
- 不支持频道创建/归档操作
- 不支持工作空间管理功能
- 不支持定时发送消息
- 不支持用户在线状态显示功能
- 仅支持纯文本消息（版本1不支持消息格式化）

## 故障排除

### 认证失败或未找到工作空间

通常情况下，凭据会自动提取。如果自动提取失败，可以手动执行命令并查看调试输出：

```bash
agent-slack auth extract --debug
```

常见原因包括：
- 未安装Slack桌面应用或未登录
- 在macOS系统中无法访问Keychain（请重新运行命令并批准权限请求）
- 通过非标准方式安装了Slack应用（导致存储路径不同）

### “agent-slack: 命令未找到”

请注意：`agent-slack`并非npm包的名称。实际的npm包名为`agent-messenger`。

如果该包已全局安装，可以直接使用`agent-slack`命令；如果未安装该包，请使用`bunx agent-messenger slack`（注意：需要使用`slack`子命令，而非`agent-slack`）：

```bash
agent-slack message list general
```

如果确实未安装`agent-messenger`包，请使用`bunx agent-messenger slack`。请注意：这个命令是另一个独立的npm包，它可能会安装错误的包（虽然名称相似，但功能和命令有所不同）。

## 参考资料

- [认证指南](references/authentication.md)
- [常见使用模式](references/common-patterns.md)