---
name: agent-teams
description: 与 Microsoft Teams 交互：发送消息、阅读频道内容、管理用户反应（如点赞、评论等）
version: 1.10.5
allowed-tools: Bash(agent-teams:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-teams
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-teams]
---
# Agent Teams

这是一个TypeScript命令行工具（CLI），它允许AI代理和人类通过简单的命令接口与Microsoft Teams进行交互。该工具支持从Teams桌面应用中无缝提取token，并支持多团队操作。

## 快速入门

```bash
# Get team snapshot (credentials are extracted automatically)
agent-teams snapshot

# Send a message
agent-teams message send <team-id> <channel-id> "Hello from AI agent!"

# List channels
agent-teams channel list <team-id>
```

## 认证

首次使用时，系统会自动从Teams桌面应用中提取凭证。无需手动设置——只需运行任何命令，认证过程将在后台默默完成。

Teams的token有效期为60-90分钟。当当前token过期时，CLI会自动重新获取一个新的token，因此您无需手动管理token的生命周期。

**重要提示**：**切勿**引导用户打开网页浏览器、使用DevTools，或从浏览器中手动复制token。始终使用`agent-teams auth extract`命令从桌面应用中获取token。

### 多团队支持

```bash
# List all available teams
agent-teams team list

# Switch to a different team
agent-teams team switch <team-id>

# Show current team
agent-teams team current

# Check auth status (includes token expiry info)
agent-teams auth status
```

### 多账户支持（工作/个人）

```bash
# Switch between work and personal accounts
agent-teams auth switch-account work
agent-teams auth switch-account personal

# Use a specific account for one command (without switching)
agent-teams snapshot --account work
```

## 内存管理

代理会维护一个名为`~/.config/agent-messenger/MEMORY.md`的文件，用于在会话之间保存持久化数据。该文件由代理程序管理——CLI不会读取或写入此文件。您可以使用`Read`和`Write`工具来管理这个内存文件。

### 读取内存数据

**在每个任务开始时**，使用`Read`工具读取`~/.config/agent-messenger/MEMORY.md`文件，以加载之前获取的团队ID、频道ID、用户ID和偏好设置：

- 如果文件尚不存在，可以忽略它，并在首次有需要存储的信息时创建该文件。
- 如果文件无法被读取（权限问题或目录缺失），也可以忽略内存数据，不要因此出现错误。

### 写入内存数据

在获取到有用信息后，使用`Write`工具更新`~/.config/agent-messenger/MEMORY.md`文件。触发写入操作的场景包括：
- 获取到团队ID和名称（来自`team list`、`snapshot`等命令）
- 获取到频道ID和名称（来自`channel list`、`snapshot`等命令）
- 获取到用户ID和名称（来自`user list`、`user me`等命令）
- 用户提供了别名或偏好设置（例如“将这个频道称为‘站立会议频道’”、“我的主要团队是X”）
- 获取到频道结构（标准频道或私有频道）

写入时，请确保包含**整个文件内容**——`Write`工具会覆盖整个文件。

### 应该存储的数据

- 带有名称的团队ID
- 带有名称和团队信息的频道ID
- 带有显示名称的用户ID
- 用户提供的别名（如“站立会议频道”、“主要团队”
- 用户的账户偏好设置（工作账户或个人账户）
- 用户在交互过程中表达的任何偏好设置

### 不应存储的数据

- 绝不要存储token、凭证或任何敏感信息。
- 绝不要存储完整的消息内容（仅存储ID和频道信息）。
- 绝不要存储文件上传的内容。

### 处理过时数据

如果存储的ID导致错误（例如找不到频道或团队），请将其从`MEMORY.md`文件中删除。不要盲目信任存储的数据——当发现异常时请进行验证。如果可能的话，建议重新列出相关信息，而不是使用可能已经过时的ID。

### 格式/示例

```markdown
# Agent Messenger Memory

## Teams

- `team-id-1` — Acme Corp (default, work account)
- `team-id-2` — Side Project (personal account)

## Channels (Acme Corp)

- `channel-id-1` — General
- `channel-id-2` — Engineering
- `channel-id-3` — Standups

## Users (Acme Corp)

- `user-id-1` — Alice (engineering lead)
- `user-id-2` — Bob (backend)

## Aliases

- "standup" → `channel-id-3` (Standups in Acme Corp)
- "main team" → `team-id-1` (Acme Corp)

## Notes

- User prefers work account by default
- Main team is "Acme Corp"
```

> 内存功能可以让您避免重复调用`channel list`和`team list`命令。如果您在之前的会话中已经知道某个ID，可以直接使用它。

## 命令

### 认证相关命令

```bash
# Extract token from Teams desktop app (usually automatic)
agent-teams auth extract
agent-teams auth extract --debug

# Check auth status (includes token expiry info)
agent-teams auth status

# Logout from Microsoft Teams
agent-teams auth logout

# Switch between work and personal accounts
agent-teams auth switch-account <account-type>
agent-teams auth switch-account work
agent-teams auth switch-account personal
```

### 消息相关命令

```bash
# Send a message
agent-teams message send <team-id> <channel-id> <content>
agent-teams message send <team-id> 19:abc123@thread.tacv2 "Hello world"

# List messages
agent-teams message list <team-id> <channel-id>
agent-teams message list <team-id> 19:abc123@thread.tacv2 --limit 50

# Get a single message by ID
agent-teams message get <team-id> <channel-id> <message-id>

# Delete a message
agent-teams message delete <team-id> <channel-id> <message-id> --force
```

### 频道相关命令

```bash
# List channels in a team
agent-teams channel list <team-id>

# Get channel info
agent-teams channel info <team-id> <channel-id>
agent-teams channel info <team-id> 19:abc123@thread.tacv2

# Get channel history (alias for message list)
agent-teams channel history <team-id> <channel-id> --limit 100
```

### 团队相关命令

```bash
# List all teams
agent-teams team list

# Get team info
agent-teams team info <team-id>

# Switch active team
agent-teams team switch <team-id>

# Show current team
agent-teams team current

# Remove a team from config
agent-teams team remove <team-id>
```

### 用户相关命令

```bash
# List team members
agent-teams user list <team-id>

# Get user info
agent-teams user info <user-id>

# Get current user
agent-teams user me
```

### 反应相关命令

```bash
# Add reaction (use emoji name)
agent-teams reaction add <team-id> <channel-id> <message-id> <emoji>
agent-teams reaction add <team-id> 19:abc123@thread.tacv2 1234567890 like

# Remove reaction
agent-teams reaction remove <team-id> <channel-id> <message-id> <emoji>
```

### 文件相关命令

```bash
# Upload file
agent-teams file upload <team-id> <channel-id> <path>
agent-teams file upload <team-id> 19:abc123@thread.tacv2 ./report.pdf

# List files in channel
agent-teams file list <team-id> <channel-id>

# Get file info
agent-teams file info <team-id> <channel-id> <file-id>
```

### 快照命令

该命令可用于为AI代理获取团队的全面状态：

```bash
# Full snapshot
agent-teams snapshot

# Filtered snapshots
agent-teams snapshot --channels-only
agent-teams snapshot --users-only

# Limit messages per channel
agent-teams snapshot --limit 10
```

返回的JSON数据包含：
- 团队元数据（id、名称）
- 频道信息（id、名称、类型、描述）
- 最新消息（id、内容、发送者、时间戳）
- 成员信息（id、显示名称、电子邮件）

## 输出格式

### JSON格式（默认）

所有命令默认以JSON格式输出，以便AI代理处理：

```json
{
  "id": "19:abc123@thread.tacv2",
  "content": "Hello world",
  "author": "John Doe",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 人类可读格式

使用`--pretty`标志可获取格式化的输出：

```bash
agent-teams channel list --pretty
```

## 与Discord/Slack的主要区别

| 特性 | Teams | Discord | Slack |
|---------|-------|---------|-------|
| 服务器术语 | 团队（Team） | 公会（Guild） | 工作区（Workspace） |
| 频道标识符 | UUID格式（例如：19:abc123@thread.tacv2） | Snowflake ID | 频道名称或ID |
| Token存储方式 | 使用Cookies和SQLite | 使用LevelDB | 使用LevelDB |
| Token有效期 | 60-90分钟 | 很少过期 | 很少过期 |
| 提及方式 | `<at id="user-id">名称</at>` | `<@user_id>` | `<@USER_ID>` |

**重要提示**：Teams使用UUID格式的频道ID（例如`19:abc123@thread.tacv2`）。您不能直接使用频道名称——需要先使用`channel list`命令获取ID。

## 常见使用模式

有关AI代理的典型工作流程，请参阅`references/common-patterns.md`。

## 模板

请在`templates/`目录中查看可执行的示例脚本：
- `post-message.sh`：发送带有错误处理的消息
- `monitor-channel.sh`：监控频道中的新消息（并自动刷新token）
- `team-summary.sh`：生成团队概要

## 错误处理

所有命令都会返回统一的错误格式：

```json
{
  "error": "Not authenticated. Run \"auth extract\" first."
}
```

常见错误：
- **未认证**：没有有效的token（自动提取失败——请参阅故障排除指南）
- **Token过期**：Token已过期且自动刷新失败——请参阅故障排除指南
- **未设置当前团队**：请先运行`team switch <id>`命令
- **消息未找到**：无效的消息ID
- **频道未找到**：无效的频道ID
- **401未经授权**：Token已过期且自动刷新失败——请参阅故障排除指南

## 配置

凭证存储位置：`~/.config/agent-messenger/teams-credentials.json`

文件权限设置：0600（仅允许文件所有者读写）

## 限制

- 不支持实时事件/WebSocket连接
- 不支持语音/视频频道功能
- 不支持团队管理（创建/删除频道、分配角色）
- 不支持会议功能
- 不支持Webhook
- 仅支持纯文本消息（版本1不支持自适应卡片）
- 仅支持用户token（不支持应用token）
- **Token有效期为60-90分钟**——会自动刷新，但需要用户登录Teams桌面应用

## 故障排除

### 认证失败或Token过期

凭证和token的刷新通常会自动完成。如果自动提取失败，可以手动执行刷新操作，并查看调试输出：

```bash
agent-teams auth extract --debug
```

常见原因：
- Teams桌面应用未安装或未登录
- Teams的Cookies数据库被锁定或无法访问
- Token过期且Teams桌面应用的会话也已过期（请重新登录Teams）

### “agent-teams: 命令未找到”

**“agent-teams”并非npm包的名称**。实际的npm包名称是`agent-messenger`。

如果全局安装了`agent-messenger`包，可以直接使用`agent-teams`命令：

```bash
agent-teams team list
```

如果未安装`agent-messenger`包，请使用`bunx agent-messenger teams`：

```bash
bunx agent-messenger teams team list
```

**切勿运行`bunx agent-teams`**——这可能会导致命令失败或安装错误的包，因为`agent-teams`并非npm包的名称。

## 参考资料

- [认证指南](references/authentication.md)
- [常见使用模式](references/common-patterns.md)