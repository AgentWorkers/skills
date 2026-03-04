---
name: discord-bot
description: "**Discord Bot API集成**  
通过Discord的REST API，您可以管理服务器、频道、消息、角色、成员以及Webhook。该功能支持发送消息、调整服务器设置、管理用户、创建频道以及处理角色分配等操作。专为AI代理设计，仅使用Python标准库开发，无需任何额外依赖。适用于Discord服务器管理、机器人自动化、社区运营、消息发送、内容审核以及Webhook集成等场景。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🤖", "requires": {"env": ["DISCORD_BOT_TOKEN"]}, "primaryEnv": "DISCORD_BOT_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🤖 Discord Bot

本 Discord Bot 支持通过 Discord REST API 管理服务器、频道、消息、角色、成员以及 Webhook。

## 主要功能

- **发送消息**：可以向任意频道发送文本消息、嵌入内容或文件。
- **频道管理**：创建、更新或删除频道。
- **服务器信息**：查看服务器的详细信息、设置及统计数据。
- **成员管理**：列出服务器成员，执行踢出或禁言操作，以及分配角色。
- **角色管理**：创建、更新角色并分配给成员。
- **消息操作**：发送、编辑、删除消息，以及对消息添加反应（reaction）。
- **Webhook 管理**：创建并触发 Webhook。
- **线程管理**：创建和管理消息线程。
- **表情管理**：列出并管理自定义表情。
- **审计日志**：查看服务器的审计事件记录。

## 必需条件

| 变量        | 是否必需 | 说明                |
|-------------|---------|-------------------|
| `DISCORD_BOT_TOKEN` | ✅     | Discord Bot 的 API 密钥/令牌         |

## 快速入门

```bash
# List bot's servers
python3 {baseDir}/scripts/discord-bot.py guilds
```

```bash
# Get server details
python3 {baseDir}/scripts/discord-bot.py guild-get 123456789
```

```bash
# List server channels
python3 {baseDir}/scripts/discord-bot.py channels --guild 123456789
```

```bash
# Create a channel
python3 {baseDir}/scripts/discord-bot.py channel-create --guild 123456789 "general-chat" --type text
```

## 命令列表

### `guilds`  
列出机器人管理的所有服务器。

```bash
python3 {baseDir}/scripts/discord-bot.py guilds
```

### `guild-get`  
获取服务器的详细信息。

```bash
python3 {baseDir}/scripts/discord-bot.py guild-get 123456789
```

### `channels`  
列出服务器中的所有频道。

```bash
python3 {baseDir}/scripts/discord-bot.py channels --guild 123456789
```

### `channel-create`  
创建一个新的频道。

```bash
python3 {baseDir}/scripts/discord-bot.py channel-create --guild 123456789 "general-chat" --type text
```

### `channel-update`  
更新现有频道的设置。

```bash
python3 {baseDir}/scripts/discord-bot.py channel-update 987654321 '{"name":"announcements","topic":"Important updates"}'
```

### `send`  
向指定频道发送消息。

```bash
python3 {baseDir}/scripts/discord-bot.py send --channel 987654321 "Hello from the bot!"
```

### `send-embed`  
发送嵌入式消息（包含图片、视频等）。

```bash
python3 {baseDir}/scripts/discord-bot.py send-embed --channel 987654321 '{"title":"Update","description":"New feature released","color":5814783}'
```

### `messages`  
列出频道中的所有消息。

```bash
python3 {baseDir}/scripts/discord-bot.py messages --channel 987654321 --limit 20
```

### `message-edit`  
编辑指定的消息。

```bash
python3 {baseDir}/scripts/discord-bot.py message-edit --channel 987654321 --message 111222333 "Updated text"
```

### `message-delete`  
删除指定的消息。

```bash
python3 {baseDir}/scripts/discord-bot.py message-delete --channel 987654321 --message 111222333
```

### `react`  
为指定消息添加反应（如点赞、踩等）。

```bash
python3 {baseDir}/scripts/discord-bot.py react --channel 987654321 --message 111222333 --emoji 👍
```

### `members`  
列出服务器中的所有成员。

```bash
python3 {baseDir}/scripts/discord-bot.py members --guild 123456789 --limit 50
```

### `roles`  
列出服务器中的所有角色。

```bash
python3 {baseDir}/scripts/discord-bot.py roles --guild 123456789
```

### `role-assign`  
为指定成员分配角色。

```bash
python3 {baseDir}/scripts/discord-bot.py role-assign --guild 123456789 --user 444555666 --role 777888999
```

### `webhooks`  
列出频道中绑定的 Webhook。

```bash
python3 {baseDir}/scripts/discord-bot.py webhooks --channel 987654321
```

## 输出格式

所有命令默认以 JSON 格式输出。若需要可读性更强的输出格式，可使用 `--human` 选项。

```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/discord-bot.py guilds --limit 5

# Human-readable
python3 {baseDir}/scripts/discord-bot.py guilds --limit 5 --human
```

## 脚本参考

| 脚本        | 说明                |
|------------|-------------------|
| `{baseDir}/scripts/discord-bot.py` | 主要的命令行接口（CLI）脚本     |

## 数据处理政策

本技能 **绝不将数据存储在本地**。所有请求都会直接发送到 Discord Bot 的 API，结果会显示在标准输出（stdout）中。你的数据将保存在 Discord Bot 的服务器上。

## 致谢

本技能由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
更多内容请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
本技能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)