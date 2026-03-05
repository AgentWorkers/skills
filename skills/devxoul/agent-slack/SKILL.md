---
name: agent-slack
description: 与 Slack 工作区交互：发送消息、阅读频道内容、管理回复（Reaction）
version: 1.10.0
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

这是一个TypeScript命令行工具（CLI），它允许AI代理和人类通过简单的命令接口与Slack工作区进行交互。该工具支持从Slack桌面应用中自动提取访问令牌，并支持多工作区功能。

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

首次使用时，系统会自动从Slack桌面应用中提取认证凭据。无需手动设置——只需运行任意命令，认证过程将在后台默默完成。

在macOS系统中，系统可能会首次提示您输入Keychain密码（用于解密Slack存储的令牌）。此提示仅出现一次。

### 多工作区支持

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

## 命令

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

### 通道相关命令

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

### 活动相关命令

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

### 通道部分相关命令

```bash
# List channel sections (sidebar organization)
agent-slack sections list
agent-slack sections list --pretty
```

### 快照命令

该命令可获取AI代理所需的工作区完整状态：

```bash
# Full snapshot
agent-slack snapshot

# Filtered snapshots
agent-slack snapshot --channels-only
agent-slack snapshot --users-only

# Limit messages per channel
agent-slack snapshot --limit 10
```

返回的JSON数据包含：
- 工作区元数据
- 通道信息（id、名称、主题、用途）
- 最新消息（时间戳、文本内容、发送者、通道名称）
- 用户信息（id、名称、个人资料）

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

使用`--pretty`标志可获取格式化后的输出：

```bash
agent-slack channel list --pretty
```

## 常见使用模式

有关AI代理的典型工作流程，请参阅`references/common-patterns.md`。

## 模板

请查看`templates/`目录中的可执行示例：
- `post-message.sh`：发送消息并处理错误
- `monitor-channel.sh`：监控通道中的新消息
- `workspace-summary.sh`：生成工作区摘要

## 错误处理

所有命令返回统一的错误格式：

```json
{
  "error": "No workspace authenticated. Run: agent-slack auth extract"
}
```

常见错误：
- `NO_WORKSPACE`：未找到可认证的工作区（自动提取失败，请参阅“故障排除”部分）
- `SLACK_API_ERROR`：Slack API返回错误
- `RATE_LIMIT`：达到Slack的请求速率限制（系统会自动重试）

## 配置

认证凭据存储路径：`~/.config/agent-messenger/slack-credentials.json`

文件权限设置：0600（仅允许所有者读写）

## 限制

- 不支持实时事件/Socket模式
- 不支持通道管理（创建/归档通道）
- 不支持工作区管理操作
- 不支持发送定时消息
- 不支持用户在线状态显示功能
- 仅支持纯文本消息（版本1不支持消息格式化）

## 故障排除

### 认证失败或未找到工作区

通常情况下，认证凭据会自动提取。如果自动提取失败，可以手动运行命令并查看调试信息：

```bash
agent-slack auth extract --debug
```

常见原因：
- 未安装Slack桌面应用或未登录
- 在macOS系统中，Keychain访问被拒绝（请重新运行命令并批准权限请求）
- 通过其他方式安装了Slack（导致存储路径不同）

### “agent-slack”命令未找到

**“agent-slack”并非npm包的名称。** 实际的npm包名为`agent-messenger`。

如果该包已全局安装，可以直接使用`agent-slack`命令：

```bash
agent-slack message list general
```

如果该包未安装，请使用`bunx agent-messenger slack`（注意：需要使用`slack`子命令，而非`agent-slack`）：

```bash
bunx agent-messenger slack message list general
```

**切勿运行`bunx agent-slack`**——npm上确实存在一个名为`agent-slack`的独立包，但它会安装错误的包（且命令不同）。

## 参考资料

- [认证指南](references/authentication.md)
- [常见使用模式](references/common-patterns.md)