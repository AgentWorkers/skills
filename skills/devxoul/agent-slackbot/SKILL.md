---
name: agent-slackbot
description: 使用机器人令牌与 Slack 工作区进行交互：发送消息、查看频道内容、管理用户反应（如点赞、反对等操作）。
version: 1.10.5
allowed-tools: Bash(agent-slackbot:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-slackbot
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-slackbot]
---
# Agent SlackBot

这是一个基于TypeScript的命令行工具（CLI），它允许AI代理和人类使用Slack机器人令牌（xoxb-）与Slack工作区进行交互。与agent-slack不同，agent-slackbot从桌面应用程序中提取用户令牌，而agent-slackbot使用标准的Slack机器人令牌来进行服务器端集成以及持续集成/持续部署（CI/CD）操作。

## 快速入门

```bash
# Set your bot token
agent-slackbot auth set xoxb-your-bot-token

# Or set with a custom bot identifier for multi-bot setups
agent-slackbot auth set xoxb-your-bot-token --bot deploy --name "Deploy Bot"

# Verify authentication
agent-slackbot auth status

# Send a message
agent-slackbot message send C0ACZKTDDC0 "Hello from bot!"

# List channels
agent-slackbot channel list
```

## 认证

### 机器人令牌设置

agent-slackbot使用从Slack应用程序配置中获取的Slack机器人令牌（xoxb-）：

```bash
# Set bot token (validates against Slack API before saving)
agent-slackbot auth set xoxb-your-bot-token

# Set with a custom bot identifier
agent-slackbot auth set xoxb-your-bot-token --bot deploy --name "Deploy Bot"

# Check auth status
agent-slackbot auth status

# Clear stored credentials
agent-slackbot auth clear
```

### 多机器人管理

您可以存储多个机器人令牌并在它们之间切换：

```bash
# Add multiple bots
agent-slackbot auth set xoxb-deploy-token --bot deploy --name "Deploy Bot"
agent-slackbot auth set xoxb-alert-token --bot alert --name "Alert Bot"

# List all stored bots
agent-slackbot auth list

# Switch active bot
agent-slackbot auth use deploy

# Use a specific bot for one command (without switching)
agent-slackbot message send C0ACZKTDDC0 "Alert!" --bot alert

# Remove a stored bot
agent-slackbot auth remove deploy

# Disambiguate bots with same ID across workspaces
agent-slackbot auth use T123456/deploy
```

在所有命令中，都可以使用`--bot <id>`标志来指定在单次调用时使用的机器人。

### 获取机器人令牌

1. 访问[api.slack.com/apps](https://api.slack.com/apps)。
2. 创建一个新的应用程序（或选择现有的应用程序）。
3. 转到**OAuth & Permissions**页面。
4. 添加所需的机器人令牌权限范围（见下文）。
5. 将应用程序安装到工作区。
6. 复制**Bot User OAuth Token**（以`xoxb-`开头）。

### 所需的机器人令牌权限范围

| 权限范围 | 用途 |
|-------|----------|
| `chat:write` | 发送消息 |
| `channels:history` | 读取公共频道消息 |
| `channels:read` | 列出公共频道 |
| `channels:join` | 加入公共频道 |
| `groups:history` | 读取私有频道消息 |
| `groups:read` | 列出私有频道 |
| `users:read` | 列出用户 |
| `users:read.email` | 读取用户电子邮件地址 |
| `reactions:write` | 添加/删除反应 |
| `reactions:read` | 列出反应 |

### 环境变量（CI/CD）

对于持续集成/持续部署管道，请设置这些环境变量，而不是使用`auth set`：

```bash
export E2E_SLACKBOT_TOKEN=xoxb-your-bot-token
export E2E_SLACKBOT_WORKSPACE_ID=T123456
export E2E_SLACKBOT_WORKSPACE_NAME="My Workspace"
```

## 内存管理

该工具会维护一个名为`~/.config/agent-messenger/MEMORY.md`的文件作为跨会话的持久化内存。这个文件由工具本身管理——CLI不会读取或写入该文件。您可以使用`Read`和`Write`工具来管理这个内存文件。

### 读取内存

在**每个任务开始时**，使用`Read`工具读取`~/.config/agent-messenger/MEMORY.md`文件，以加载之前发现的工作区ID、频道ID、用户ID和偏好设置。

- 如果文件还不存在，没关系——可以直接继续操作，并在首次有需要存储的信息时创建它。
- 如果无法读取文件（权限问题或目录缺失），也可以继续操作，但不要出现错误。

### 写入内存

在发现有用信息后，使用`Write`工具更新`~/.config/agent-messenger/MEMORY.md`文件。需要写入的情况包括：
- 发现工作区ID时（来自`auth status`）
- 发现频道ID和名称时（来自`channel list`等）
- 发现用户ID和名称时（来自`user list`等）
- 用户提供了别名或偏好设置时（例如：“将此机器人称为‘alerts bot’”，“我的主要工作区是X”）
- 设置机器人标识符时（来自`auth list`）

写入时，请包含**整个文件内容**——`Write`工具会覆盖整个文件。

### 应该存储的内容

- 带有名称的工作区ID
- 带有名称和用途的频道ID
- 带有显示名称的用户ID
- 机器人标识符及其用途
- 用户提供的别名（例如：“alerts bot”，“deploys channel”）
- 用户在交互过程中表达的任何偏好设置

### 不应该存储的内容

切勿存储机器人令牌、凭据或任何敏感数据。切勿存储完整的消息内容（仅存储ID和频道上下文）。也不要存储文件上传的内容。

### 处理过时数据

如果存储的ID导致错误（例如频道找不到或用户找不到），请将其从`MEMORY.md`文件中删除。不要盲目信任存储的数据——当发现异常时请进行验证。如果数据可能已经过时，建议重新获取信息。

### 格式/示例

```markdown
# Agent Messenger Memory

## Slack Workspaces (Bot)

- `T0ABC1234` — Acme Corp

## Bots (Acme Corp)

- `deploy` — Deploy Bot (active)
- `alert` — Alert Bot

## Channels (Acme Corp)

- `C012ABC` — #general (company-wide announcements)
- `C034DEF` — #engineering (team discussion)
- `C056GHI` — #deploys (CI/CD notifications)

## Users (Acme Corp)

- `U0ABC123` — Alice (engineering lead)
- `U0DEF456` — Bob (backend)

## Aliases

- "deploys" → `C056GHI` (#deploys in Acme Corp)

## Notes

- Deploy Bot is used for CI/CD notifications
- Alert Bot is used for error monitoring
```

> 内存功能可以让您避免重复调用`channel list`和`auth list`命令。如果您在之前的会话中已经知道某个ID，可以直接使用它。

## 命令

### 消息命令

```bash
# Send a message
agent-slackbot message send <channel> <text>
agent-slackbot message send C0ACZKTDDC0 "Hello world"

# Send a threaded reply
agent-slackbot message send C0ACZKTDDC0 "Reply" --thread <ts>

# List messages
agent-slackbot message list <channel>
agent-slackbot message list C0ACZKTDDC0 --limit 50

# Get a single message by timestamp
agent-slackbot message get <channel> <ts>

# Get thread replies (includes parent message)
agent-slackbot message replies <channel> <thread_ts>
agent-slackbot message replies C0ACZKTDDC0 1234567890.123456 --limit 50

# Update a message (bot's own messages only)
agent-slackbot message update <channel> <ts> <new-text>

# Delete a message (bot's own messages only)
agent-slackbot message delete <channel> <ts> --force
```

### 频道命令

```bash
# List channels the bot can see
agent-slackbot channel list
agent-slackbot channel list --limit 50

# Get channel info
agent-slackbot channel info <channel>
agent-slackbot channel info C0ACZKTDDC0
```

### 用户命令

```bash
# List users
agent-slackbot user list
agent-slackbot user list --limit 50

# Get user info
agent-slackbot user info <user-id>
```

### 反应命令

```bash
# Add reaction
agent-slackbot reaction add <channel> <ts> <emoji>
agent-slackbot reaction add C0ACZKTDDC0 1234567890.123456 thumbsup

# Remove reaction
agent-slackbot reaction remove <channel> <ts> <emoji>
```

## 输出格式

### JSON（默认）

所有命令默认输出JSON格式，以便AI程序进行处理：

```json
{
  "ts": "1234567890.123456",
  "channel": "C0ACZKTDDC0",
  "text": "Hello world"
}
```

### 人类可读格式

使用`--pretty`标志可以获得格式化的输出：

```bash
agent-slackbot channel list --pretty
```

## 常见工作流程

有关典型的AI代理工作流程，请参阅`references/common-patterns.md`。

## 模板

请查看`templates/`目录中的可执行示例：
- `post-message.sh` - 发送消息并处理错误
- `monitor-channel.sh` - 监控频道中的新消息
- `workspace-summary.sh` - 生成工作区摘要

## 错误处理

所有命令都会返回一致的错误格式：

```json
{
  "error": "No credentials. Run \"auth set\" first."
}
```

常见错误：
- `missing_token`：未配置凭据
- `invalid_token_type`：令牌不是机器人令牌（必须以xoxb-开头）
- `not_in_channel`：机器人需要先加入该频道
- `slack_webapi_rate_limited_error`：达到请求速率限制（会自动重试）

## 配置

凭据存储在：`~/.config/agent-messenger/slackbot-credentials.json`文件中

文件权限设置为0600（仅允许所有者读写）。

## 与agent-slack的主要区别

| 特性 | agent-slack | agent-slackbot |
|---------|------------|----------------|
| 令牌类型 | 用户令牌（xoxc-） | 机器人令牌（xoxb-） |
| 令牌来源 | 从桌面应用程序自动提取 | 从Slack应用程序配置中手动获取 |
| 消息搜索 | 支持 | 不支持（需要用户令牌） |
| 文件操作 | 支持 | 不支持 |
| 频道快照 | 支持 | 不支持 |
| 编辑/删除消息 | 可以编辑/删除任何消息 | 仅能编辑/删除机器人自己的消息 |
| 工作区管理 | 支持多工作区 | 支持多机器人和多工作区 |
| 适合CI/CD | 需要使用桌面应用程序 | 支持（只需设置令牌即可） |

## 限制

- 不支持实时事件/Socket模式
- 不支持消息搜索（需要用户令牌权限）
- 不支持文件上传/下载
- 不支持工作区快照
- 机器人只能编辑/删除自己的消息
- 机器人必须被邀请才能加入私有频道
- 不支持定时发送消息
- 仅支持纯文本消息（不支持格式化）

## 故障排除

### `agent-slackbot: command not found`

**`agent-slackbot`并不是npm包的名称。**正确的npm包名称是`agent-messenger`。

如果全局安装了`agent-messenger`，可以直接使用`agent-slackbot`：

```bash
agent-slackbot message send general "Hello"
```

如果未安装该包，请使用`bunx agent-messenger slackbot`：

```bash
bunx agent-messenger slackbot message send general "Hello"
```

**切勿运行`bunx agent-slackbot`**——这可能会导致错误或安装错误的包，因为`agent-slackbot`并不是正确的npm包名称。

## 参考资料

- [认证指南](references/authentication.md)
- [常见工作流程](references/common-patterns.md)