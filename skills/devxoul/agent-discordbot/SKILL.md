---
name: agent-discordbot
description: 使用机器人令牌与 Discord 服务器进行交互：发送消息、读取频道内容、管理用户反应（如点赞、反对等操作）
version: 1.8.1
allowed-tools: Bash(agent-discordbot:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-discordbot
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-discordbot]
---
# Agent DiscordBot

这是一个TypeScript命令行工具（CLI），它允许AI代理和人类使用Bot令牌与Discord服务器进行交互。与`agent-discord`不同，`agent-discordbot`使用标准的Discord Bot令牌来进行服务器端集成以及持续集成/持续部署（CI/CD）操作。

## 快速入门

```bash
# Set your bot token
agent-discordbot auth set your-bot-token

# Verify authentication
agent-discordbot auth status

# Send a message
agent-discordbot message send 1234567890123456789 "Hello from bot!"

# List channels
agent-discordbot channel list
```

## 认证

### Bot令牌设置

`agent-discordbot`使用你在Discord开发者门户中创建的Bot令牌：

```bash
# Set bot token (validates against Discord API before saving)
agent-discordbot auth set your-bot-token

# Set with a custom bot identifier
agent-discordbot auth set your-bot-token --bot deploy --name "Deploy Bot"

# Check auth status
agent-discordbot auth status

# Clear stored credentials
agent-discordbot auth clear
```

### 获取Bot令牌

1. 访问[discord.com/developers/applications](https://discord.com/developers/applications)。
2. 点击“新建应用”，为其命名并完成创建流程。
3. 转到左侧导航栏中的“Bot”选项。
4. 点击“重置令牌”（如果令牌仍然可见，则选择“复制”）。
5. 复制令牌并妥善保存。

### 邀请Bot加入服务器

创建应用后：

1. 转到左侧导航栏中的“OAuth2” > “URL生成器”。
2. 在“权限范围”中选择“bot”。
3. 在“Bot权限”中选择Bot所需的权限（如发送消息、读取消息历史记录等）。
4. 复制生成的URL并在浏览器中打开它。
5. 选择目标服务器并完成授权。

### 消息内容权限

在100个或更多服务器上运行的Bot需要经过验证（达到75个服务器后即可申请验证），经过验证的Bot必须申请“消息内容”权限。要启用此权限，请执行以下操作：

1. 访问[discord.com/developers/applications](https://discord.com/developers/applications)。
2. 选择你的应用。
3. 转到左侧导航栏中的“Bot”选项。
4. 在“特权网关权限”中启用“消息内容”权限。
5. 保存更改。

如果没有启用此权限，经过验证的Bot收到的`content`字段将为空（私信和提及消息除外）。

### 多Bot管理

你可以存储多个Bot令牌并在不同命令之间切换：

```bash
# Add multiple bots
agent-discordbot auth set deploy-bot-token --bot deploy --name "Deploy Bot"
agent-discordbot auth set alert-bot-token --bot alert --name "Alert Bot"

# List all stored bots
agent-discordbot auth list

# Switch active bot
agent-discordbot auth use deploy

# Use a specific bot for one command (without switching)
agent-discordbot message send 1234567890123456789 "Alert!" --bot alert

# Remove a stored bot
agent-discordbot auth remove deploy
```

在所有命令中，都可以使用`--bot <id>`标志来指定当前使用的Bot。

## 命令

### 认证相关命令

```bash
# Set bot token
agent-discordbot auth set <token>
agent-discordbot auth set <token> --bot deploy --name "Deploy Bot"

# Check auth status
agent-discordbot auth status

# Clear all credentials
agent-discordbot auth clear

# List stored bots
agent-discordbot auth list

# Switch active bot
agent-discordbot auth use <bot-id>

# Remove a stored bot
agent-discordbot auth remove <bot-id>
```

### 服务器相关命令

```bash
# List servers the bot is in
agent-discordbot server list

# Show current server
agent-discordbot server current

# Switch active server
agent-discordbot server switch <server-id>

# Get server info
agent-discordbot server info <server-id>
```

### 消息相关命令

```bash
# Send a message
agent-discordbot message send <channel-id> <content>
agent-discordbot message send 1234567890123456789 "Hello world"

# List messages
agent-discordbot message list <channel-id>
agent-discordbot message list 1234567890123456789 --limit 50

# Get a single message by ID
agent-discordbot message get <channel-id> <message-id>

# Get thread replies
agent-discordbot message replies <channel-id> <message-id>
agent-discordbot message replies 1234567890123456789 9876543210987654321 --limit 50

# Update a message (bot's own messages only)
agent-discordbot message update <channel-id> <message-id> <new-content>

# Delete a message (bot's own messages only)
agent-discordbot message delete <channel-id> <message-id> --force
```

### 频道相关命令

```bash
# List channels in current server
agent-discordbot channel list

# Get channel info
agent-discordbot channel info <channel-id>
agent-discordbot channel info 1234567890123456789
```

### 用户相关命令

```bash
# List server members
agent-discordbot user list
agent-discordbot user list --limit 50

# Get user info
agent-discordbot user info <user-id>
```

### 反应相关命令

```bash
# Add reaction (use emoji name without colons)
agent-discordbot reaction add <channel-id> <message-id> <emoji>
agent-discordbot reaction add 1234567890123456789 9876543210987654321 thumbsup

# Remove reaction
agent-discordbot reaction remove <channel-id> <message-id> <emoji>
```

### 文件相关命令

```bash
# Upload file to a channel
agent-discordbot file upload <channel-id> <path>
agent-discordbot file upload 1234567890123456789 ./report.pdf

# List files in channel
agent-discordbot file list <channel-id>
```

### 线程相关命令

```bash
# Create a thread from a message
agent-discordbot thread create <channel-id> <name>
agent-discordbot thread create 1234567890123456789 "Discussion" --auto-archive-duration 1440

# Archive a thread
agent-discordbot thread archive <thread-id>
```

### 快照命令

该命令可获取AI代理的服务器状态信息：

```bash
# Full snapshot of current server
agent-discordbot snapshot

# Filtered snapshots
agent-discordbot snapshot --channels-only
agent-discordbot snapshot --users-only

# Limit messages per channel
agent-discordbot snapshot --limit 10
```

返回的JSON内容包括：
- 服务器元数据（id、名称）
- 频道信息（id、名称、类型、主题）
- 最新消息（id、内容、发送者、时间戳）
- 服务器成员信息（id、用户名、全局名称）

## 输出格式

### JSON格式（默认）

所有命令默认以JSON格式输出，便于AI代理处理：

```json
{
  "id": "1234567890123456789",
  "content": "Hello world",
  "author": "bot-username",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 人类可读格式

使用`--pretty`标志可获取格式化的输出：

```bash
agent-discordbot channel list --pretty
```

## 全局选项

| 选项 | 描述 |
|--------|-------------|
| `--pretty` | 以人类可读的格式输出结果 |
| `--bot <id>` | 为该命令指定特定的Bot |
| `--server <id>` | 为该命令指定特定的服务器 |

## 常见使用模式

有关AI代理的典型工作流程，请参阅`references/common-patterns.md`。

## 模板

在`templates/`目录中可以找到可执行的示例脚本：
- `post-message.sh`：发送带有错误处理的消息
- `monitor-channel.sh`：监控频道中的新消息
- `server-summary.sh`：生成服务器摘要

## 错误处理

所有命令都会返回统一的错误格式：

```json
{
  "error": "No credentials. Run \"auth set\" first."
}
```

常见错误：
- `missing_token`：未配置凭证
- `invalid_token`：令牌无效或已过期
- `Missing Access`：Bot没有执行该操作的权限
- `Unknown Channel`：频道ID无效
- `Missing Permissions`：Bot的角色没有所需的权限

## 配置

凭证存储位置：`~/.config/agent-messenger/discordbot-credentials.json`

文件权限设置为0600（仅允许所有者读写）。

## 与`agent-discord`的主要区别

| 特性 | agent-discord | agent-discordbot |
|---------|--------------|------------------|
| 令牌类型 | 用户令牌 | Bot令牌 |
| 令牌来源 | 从桌面应用自动提取 | 需要在开发者门户中手动获取 |
| 消息搜索 | 支持 | 不支持 |
| 私信 | 支持 | 不支持 |
| 提及消息 | 支持 | 不支持 |
| 查看/删除好友/笔记 | 支持 | 不支持 |
| 编辑/删除消息 | 可编辑/删除任何消息 | 仅能编辑/删除Bot自己的消息 |
| 上传文件 | 支持 | 支持 |
| 快照功能 | 支持 | 支持 |
| 适合CI/CD集成 | 需要使用桌面应用 | 只需设置令牌即可 |

## 限制

- 不支持实时事件/网关连接
- 不支持语音频道
- 不支持服务器管理（创建/删除频道、角色）
- 不支持斜杠命令（/命令）
- 不支持Webhook
- 不支持消息搜索
- 不支持私信或好友管理
- Bot只能编辑/删除自己的消息
- Bot必须被邀请加入服务器并具有相应的权限
- 经过验证的Bot（在100个或更多服务器上运行的Bot）需要“消息内容”权限
- 仅支持纯文本消息（版本1不支持嵌入内容）

## 故障排除

### “agent-discordbot: command not found”

请注意，`agent-discordbot`并非npm包的名称。实际的npm包名为`agent-messenger`。

如果全局安装了`agent-messenger`包，可以直接使用`agent-discordbot`：

```bash
agent-discordbot message send 1234567890123456789 "Hello"
```

如果未安装该包，请使用`bunx agent-messenger discordbot`：

```bash
bunx agent-messenger discordbot message send 1234567890123456789 "Hello"
```

**切勿运行`bunx agent-discordbot`**——这可能会导致错误或安装错误的包，因为`agent-discordbot`并非npm包的名称。

### Bot无法在大型服务器上读取消息

需要在开发者门户中启用“消息内容”权限：

1. 访问[discord.com/developers/applications](https://discord.com/developers/applications)。
2. 选择你的应用 > “Bot”。
3. 在“特权网关权限”中启用“消息内容”权限。
4. 保存更改。

这是经过验证的Bot（在100个或更多服务器上运行的Bot）必须完成的步骤。

### 出现“Missing Access”或“Missing Permissions”错误

可能是Bot的角色在该频道中没有所需的权限：

1. 检查服务器设置中的Bot角色权限。
2. 检查频道特定的权限设置。
3. 确保Bot能够查看和发送目标频道中的消息。

### 出现“Unknown Channel”错误

可能是频道ID无效，或者Bot没有访问权限。可以使用`channel list`命令查找有效的频道ID。

### 令牌过期或无效

Bot令牌不会自动过期，但可以手动重置：

1. 访问[discord.com/developers/applications](https://discord.com/developers/applications)。
2. 选择你的应用 > “Bot” > “重置令牌”。
3. 复制新的令牌。
4. 运行`agent-discordbot auth set <新令牌>`。

## 参考资料

- [认证指南](references/authentication.md)
- [常见使用模式](references/common-patterns.md)