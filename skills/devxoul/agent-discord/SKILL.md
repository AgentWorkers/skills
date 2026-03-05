---
name: agent-discord
description: 与 Discord 服务器交互：发送消息、查看频道内容、管理用户反应（如点赞、反对等操作）
version: 1.9.2
allowed-tools: Bash(agent-discord:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-discord
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-discord]
---
# Agent Discord

这是一个基于TypeScript的命令行工具（CLI），它允许AI代理和人类通过简单的命令界面与Discord服务器进行交互。该工具支持从Discord桌面应用中自动提取token，并支持多服务器操作。

## 快速入门

```bash
# Get server snapshot (credentials are extracted automatically)
agent-discord snapshot

# Send a message
agent-discord message send <channel-id> "Hello from AI agent!"

# List channels
agent-discord channel list
```

## 认证

首次使用时，系统会自动从Discord桌面应用中提取认证凭据。无需手动设置——只需运行任何命令，认证过程将在后台默默完成。

在macOS系统上，系统可能会首次提示您输入Keychain密码（用于解密Discord存储的token）。这只是一个一次性提示。

### 多服务器支持

```bash
# List all available servers
agent-discord server list

# Switch to a different server
agent-discord server switch <server-id>

# Show current server
agent-discord server current

# Check auth status
agent-discord auth status
```

## 命令

### 认证相关命令

```bash
# Extract token from Discord desktop app (usually automatic)
agent-discord auth extract
agent-discord auth extract --debug

# Check auth status
agent-discord auth status

# Logout from Discord
agent-discord auth logout
```

### 消息相关命令

```bash
# Send a message
agent-discord message send <channel-id> <content>
agent-discord message send 1234567890123456789 "Hello world"

# List messages
agent-discord message list <channel-id>
agent-discord message list 1234567890123456789 --limit 50

# Get a single message by ID
agent-discord message get <channel-id> <message-id>
agent-discord message get 1234567890123456789 9876543210987654321

# Delete a message
agent-discord message delete <channel-id> <message-id> --force

# Acknowledge/mark a message as read
agent-discord message ack <channel-id> <message-id>

# Search messages in current server
agent-discord message search <query>
agent-discord message search "project update" --limit 10
agent-discord message search "hello" --channel <channel-id> --author <user-id>
```

### 频道相关命令

```bash
# List channels in current server (text channels only)
agent-discord channel list

# Get channel info
agent-discord channel info <channel-id>
agent-discord channel info 1234567890123456789

# Get channel history (alias for message list)
agent-discord channel history <channel-id> --limit 100
```

### 服务器相关命令

```bash
# List all servers
agent-discord server list

# Get server info
agent-discord server info <server-id>

# Switch active server
agent-discord server switch <server-id>

# Show current server
agent-discord server current
```

### 用户相关命令

```bash
# List server members
agent-discord user list

# Get user info
agent-discord user info <user-id>

# Get current user
agent-discord user me
```

### 私信相关命令

```bash
# List DM channels
agent-discord dm list

# Create a DM channel with a user
agent-discord dm create <user-id>
```

### 提及相关命令

```bash
# List recent mentions
agent-discord mention list
agent-discord mention list --limit 50
agent-discord mention list --guild <server-id>
```

### 朋友相关命令

```bash
# List all relationships (friends, blocked, pending requests)
agent-discord friend list
agent-discord friend list --pretty
```

### 备注相关命令

```bash
# Get note for a user
agent-discord note get <user-id>

# Set note for a user
agent-discord note set <user-id> "Note content"
```

### 个人资料相关命令

```bash
# Get detailed user profile
agent-discord profile get <user-id>
```

### 成员相关命令

```bash
# Search guild members
agent-discord member search <guild-id> <query>
agent-discord member search 1234567890123456789 "john" --limit 20
```

### 主题相关命令

```bash
# Create a thread in a channel
agent-discord thread create <channel-id> <name>
agent-discord thread create 1234567890123456789 "Discussion" --auto-archive-duration 1440

# Archive a thread
agent-discord thread archive <thread-id>
```

### 反应相关命令

```bash
# Add reaction (use emoji name without colons)
agent-discord reaction add <channel-id> <message-id> <emoji>
agent-discord reaction add 1234567890123456789 9876543210987654321 thumbsup

# Remove reaction
agent-discord reaction remove <channel-id> <message-id> <emoji>

# List reactions on a message
agent-discord reaction list <channel-id> <message-id>
```

### 文件相关命令

```bash
# Upload file
agent-discord file upload <channel-id> <path>
agent-discord file upload 1234567890123456789 ./report.pdf

# List files in channel
agent-discord file list <channel-id>

# Get file info
agent-discord file info <channel-id> <file-id>
```

### 获取服务器状态（供AI代理使用）

```bash
# Full snapshot
agent-discord snapshot

# Filtered snapshots
agent-discord snapshot --channels-only
agent-discord snapshot --users-only

# Limit messages per channel
agent-discord snapshot --limit 10
```

返回的JSON数据包含：
- 服务器元数据（id, name）
- 频道信息（id, name, type, topic）
- 最新消息（id, content, author, timestamp）
- 成员信息（id, username, global_name）

## 输出格式

### JSON（默认格式）

所有命令默认以JSON格式输出，以便AI代理使用：

```json
{
  "id": "1234567890123456789",
  "content": "Hello world",
  "author": "username",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 人类可读格式

使用`--pretty`标志可获取格式化后的输出：

```bash
agent-discord channel list --pretty
```

## 与Slack的主要区别

| 特性 | Discord | Slack |
|---------|---------|-------|
| 服务器术语 | Server | Workspace |
| 频道标识符 | Snowflake ID | 频道名称或ID |
| 消息标识符 | Snowflake ID | 时间戳（ts） |
| 主题（Thread） | 主题ID字段 | 主题时间戳 |
| 提及（Mention） | `<@user_id>` | `<@USER_ID>` |

**重要提示**：Discord使用Snowflake ID（例如`1234567890123456789`）作为所有标识符。您不能直接使用频道名称——需要先使用`channel list`命令获取频道ID。

## 常见使用模式

请参阅`references/common-patterns.md`以了解AI代理的典型使用模式。

## 模板

请查看`templates/`目录中的示例脚本：
- `post-message.sh`：发送消息并处理错误
- `monitor-channel.sh`：监控频道中的新消息
- `server-summary.sh`：生成服务器摘要

## 错误处理

所有命令都会返回统一的错误格式：

```json
{
  "error": "Not authenticated. Run \"auth extract\" first."
}
```

常见错误：
- **未认证**：无法获取有效token（自动提取失败——请参阅“故障排除”部分）
- **未设置当前服务器**：请先运行`server switch <id>`命令
- **消息未找到**：消息ID无效
- **未知频道**：频道ID无效

## 配置

认证凭据存储在：`~/.config/agent-messenger/discord-credentials.json`文件中

文件权限设置为0600（仅允许文件所有者读写）

## 限制

- 不支持实时事件/网关连接
- 不支持语音频道
- 不支持服务器管理（创建/删除频道、角色）
- 不支持斜杠命令（/命令）
- 不支持Webhook
- 仅支持纯文本消息（版本1不支持消息嵌入）
- 仅支持用户token（不支持机器人token）

## 故障排除

### 认证失败或未找到token

通常情况下，凭据会自动提取。如果自动提取失败，请手动执行命令并查看调试信息：

```bash
agent-discord auth extract --debug
```

常见原因：
- 未安装Discord桌面应用或未登录
- 在macOS系统中被拒绝访问Keychain（重新运行命令并批准权限请求）
- Discord未运行，导致LevelDB文件数据过期

### 错误提示：“agent-discord: command not found”

**“agent-discord”并非npm包的名称。** 正确的npm包名为`agent-messenger`。

如果全局安装了该软件包，可以直接使用`agent-discord`命令：

```bash
agent-discord server list
```

如果未安装该软件包，请使用`bunx agent-messenger discord`：

```bash
bunx agent-messenger discord server list
```

**切勿使用`bunx agent-discord`**——这可能会导致命令执行失败或安装错误的包，因为“agent-discord”并非真正的npm包名称。

## 参考资料

- [认证指南](references/authentication.md)
- [常见使用模式](references/common-patterns.md)