---
name: discord-server-ctrl
description: 完成Discord服务器的全面管理功能，涵盖从A到Z的所有方面：频道/角色/成员管理、自动审核机制（AutoMod）、Webhook集成、模板设计、审计日志记录、定时事件调度，以及通过命令行界面（CLI）实现的对服务器的全面控制。
---

# Discord 服务器管理员（专业版）

这是一套完整的企业级 Discord 服务器管理工具，涵盖了服务器管理员所需的所有功能——从基本的管理功能到自动审核（AutoMod）、Webhook、模板、审计日志等高级功能。

---

## 🚀 快速入门

```bash
# Set your bot token
export DISCORD_BOT_TOKEN="your-bot-token"

# Make script executable
chmod +x discord-admin.sh

# View all commands
./discord-admin.sh --help
```

---

## 📋 命令参考

### 1. 服务器智能功能

```bash
# Full server overview
./discord-admin.sh server-info <guildId>

# Server vanity URL (if enabled)
./discord-admin.sh vanity-get <guildId>

# Set vanity URL (requires DISCOVERABLE + boosts)
./discord-admin.sh vanity-set <guildId> <code>

# Server template operations
./discord-admin.sh template-list <guildId>         # List templates
./discord-admin.sh template-create <guildId> <name>  # Create template
./discord-admin.sh template-use <code>             # Create server from template
```

### 2. 频道管理（所有类型）

```bash
# List ALL channels (organized by category)
./discord-admin.sh channel-list <guildId>

# Create channels
./discord-admin.sh channel-create <guildId> <name> text                    # Text
./discord-admin.sh channel-create <guildId> <name> voice                    # Voice
./discord-admin.sh channel-create <guildId> <name> category                # Category
./discord-admin.sh channel-create <guildId> <name> forum                   # Forum
./discord-admin.sh channel-create <guildId> <name> stage                   # Stage
./discord-admin.sh channel-create <guildId> <name> announcements           # Announcement

# Edit channel (all settings)
./discord-admin.sh channel-edit <guildId> <channelId> name:<newName> topic:<topic>
./discord-admin.sh channel-edit <guildId> <channelId> nsfw:true rateLimit:60

# Channel permissions
./discord-admin.sh channel-perms <guildId> <channelId>                      # View perms
./discord-admin.sh channel-perms-set <guildId> <channelId> <roleId> allow:<perms> deny:<perms>
./discord-admin.sh channel-perms-overwrite <guildId> <channelId> <targetId> <type:role|user> allow:<perms> deny:<perms>

# Delete channel
./discord-admin.sh channel-delete <guildId> <channelId>

# Bulk operations
./discord-admin.sh channel-prune <guildId> <days:7>                         # Delete unused channels
```

### 3. 角色管理（高级）

```bash
# List all roles with hierarchy
./discord-admin.sh role-list <guildId>

# Create role with full permissions
./discord-admin.sh role-create <guildId> <name> color:#FF5500 permissions:ADMINISTRATOR
./discord-admin.sh role-create <guildId> <name> permissions:MANAGE_CHANNELS,KICK_MEMBERS,BAN_MEMBERS

# Edit role
./discord-admin.sh role-edit <guildId> <roleId> name:<name> color:<hex>
./discord-admin.sh role-edit <guildId> <roleId> hoist:true mentionable:true
./discord-admin.sh role-edit <guildId> <roleId> permissions:+MANAGE_MESSAGES,-ADMINISTRATOR

# Position management (hierarchy matters!)
./discord-admin.sh role-position <guildId> <roleId> <newPosition>

# Delete role
./discord-admin.sh role-delete <guildId> <roleId>

# Bulk role operations
./discord-admin.sh role-assign-bulk <guildId> <roleId> <userId1,userId2,...>
./discord-admin.sh role-remove-bulk <guildId> <roleId> <userId1,userId2,...>

# Role permission constants (comma-separated):
# ADMINISTRATOR, VIEW_AUDIT_LOG, VIEW_GUILD_INSIGHTS, MANAGE_GUILD, MANAGE_ROLES, MANAGE_CHANNELS, KICK_MEMBERS, BAN_MEMBERS, CREATE_INSTANT_INVITE, CHANGE_NICKNAME, MANAGE_NICKNAMES, MANAGE_EMOJIS, MANAGE_WEBHOOKS, MANAGE_GUILD_EXPRESSIONS, USE_APPLICATION_COMMANDS, MANAGE_EVENTS, MODERATE_MEMBERS
```

### 4. 成员管理

```bash
# Member info
./discord-admin.sh member-info <guildId> <userId>

# Nickname management
./discord-admin.sh member-nick <guildId> <userId> <nickname>
./discord-admin.sh member-nick-reset <guildId> <userId>

# Timeout (mute) - Discord native
./discord-admin.sh member-timeout <guildId> <userId> <duration:60s|1h|1d|7d>
./discord-admin.sh member-untimeout <guildId> <userId>

# Kick
./discord-admin.sh member-kick <guildId> <userId> [reason]

# Ban (with options)
./discord-admin.sh member-ban <guildId> <userId> [reason] [deleteMessageDays:0-7]
./discord-admin.sh member-ban-temp <guildId> <userId> <duration:7d> [reason]

# Unban
./discord-admin.sh member-unban <guildId> <userId> [reason]

# Bulk moderation
./discord-admin.sh ban-list <guildId>                                   # List all bans
./discord-admin.sh kick-bulk <guildId> <userId1,userId2,...> [reason]
./discord-admin.sh ban-bulk <guildId> <userId1,userId2,...> [reason]

# Avatar management
./discord-admin.sh member-avatar-set <guildId> <userId> <imageUrl>
```

### 5. 自动审核（Pro 版本）

```bash
# List AutoMod rules
./discord-admin.sh automod-list <guildId>

# Create AutoMod rule
./discord-admin.sh automod-create <guildId> <name> \
    keyword:badword,spam,scam \
    presets:SLUR,SEXUAL,PROFANITY \
    actions:BLOCK_MESSAGE,ALERT, timeout:60s

# Keyword filters
./discord-admin.sh automod-keyword <guildId> <ruleName> add:badword,offensive
./discord-admin.sh automod-keyword <guildId> <ruleName> remove:badword
./discord-admin.sh automod-keyword <guildId> <ruleName> clear:true

# Preset filters (Discord-provided)
./discord-admin.sh automod-preset <guildId> <ruleName> SLUR,SEXUAL,PROFANITY,VIOLENCE

# Regex patterns
./discord-admin.sh automod-regex <guildId> <ruleName> pattern:'(?i)(https?://\S+)'

# Block lists
./discord-admin.sh automod-blocklist <guildId> <ruleName> add:custom_blocklist_name

# Actions configuration
./discord-admin.sh automod-actions <guildId> <ruleName> \
    ALERT \
    BLOCK_MESSAGE \
    timeout:60s \
    timeoutDuration:300 \
    channelId:123456789

# Edit/delete rules
./discord-admin.sh automod-edit <guildId> <ruleId> enabled:false
./discord-admin.sh automod-delete <guildId> <ruleId>
```

### 6. 消息管理

```bash
# Send messages
./discord-admin.sh msg-send <channelId> <content>
./discord-admin.sh msg-embed <channelId> '{"title":"Hello","description":"World","color":65280}'

# Send with attachments
./discord-admin.sh msg-send-file <channelId> <filePath> [message]

# Edit messages
./discord-admin.sh msg-edit <channelId> <messageId> <newContent>

# Delete messages
./discord-admin.sh msg-delete <channelId> <messageId>
./discord-admin.sh msg-delete-bulk <channelId> <messageId1,messageId2,...>
./discord-admin.sh msg-delete-range <channelId> <beforeMessageId> [limit:100]

# Bulk delete (14-day limit)
./discord-admin.sh msg-prune <channelId> [days:7]

# Search messages
./discord-admin.sh msg-search <guildId> <query> [channelId]
./discord-admin.sh msg-search-user <guildId> <userId> [limit:100]

# Pin/Unpin
./discord-admin.sh msg-pin <channelId> <messageId>
./discord-admin.sh msg-unpin <channelId> <messageId>
./discord-admin.sh msg-pins <channelId>

# Get message history
./discord-admin.sh msg-history <channelId> [limit:100]
```

### 7. Webhook（高级）

```bash
# List webhooks
./discord-admin.sh webhook-list <guildId> [channelId]
./discord-admin.sh webhook-list <guildId> <channelId>

# Create webhook
./discord-admin.sh webhook-create <channelId> <name> [avatarUrl]

# Get webhook info
./discord-admin.sh webhook-info <webhookId>

# Edit webhook
./discord-admin.sh webhook-edit <webhookId> name:<name> channel:<channelId>
./discord-admin.sh webhook-edit <webhookId> avatar:<imageUrl>

# Execute webhook (send as webhook)
./discord-admin.sh webhook-execute <webhookId> <content>
./discord-admin.sh webhook-execute <webhookId> <content> username:<customName> avatar:<customAvatar>
./discord-admin.sh webhook-execute <webhookId> <content> tts:true
./discord-admin.sh webhook-execute <webhookId> embed:'{"title":"Embed","description":"内容"}'

# Delete webhook
./discord-admin.sh webhook-delete <webhookId>
```

### 8. 表情符号与贴纸

```bash
# List emojis
./discord-admin.sh emoji-list <guildId>

# Create emoji (from URL or base64)
./discord-admin.sh emoji-create <guildId> <name> <imageUrl>
./discord-admin.sh emoji-create <guildId> <name> <base64Data>

# Delete emoji
./discord-admin.sh emoji-delete <guildId> <emojiId>

# Modify emoji
./discord-admin.sh emoji-edit <guildId> <emojiId> <newName>

# List stickers
./discord-admin.sh sticker-list <guildId>

# Create sticker
./discord-admin.sh sticker-create <guildId> <name> <tag> <imageUrl>

# Edit sticker
./discord-admin.sh sticker-edit <guildId> <stickerId> name:<name> tags:<tags>

# Delete sticker
./discord-admin.sh sticker-delete <guildId> <stickerId>
```

### 9. 音效库（测试版）

```bash
# List soundboard sounds
./discord-admin.sh soundboard-list <guildId>

# Play sound (triggers in voice channel)
./discord-admin.sh soundboard-play <guildId> <soundId> [volume:100]

# Default sounds
./discord-admin.sh soundboard-defaults <guildId>
```

### 10. 定时事件

```bash
# List events
./discord-admin.sh event-list <guildId>

# Create event
./discord-admin.sh event-create <guildId> <name> <description> <startTime> endTime:<endTime> channel:<channelId>
./discord-admin.sh event-create <guildId> "Gaming Night" "Join us!" 2024-12-31T20:00:00Z channel:123456789 entityType:VOICE

# Event types: VOICE, STAGE_INSTANCE, EXTERNAL

# Edit event
./discord-admin.sh event-edit <guildId> <eventId> name:<name> description:<desc>
./discord-admin.sh event-edit <guildId> <eventId> status:SCHEDULED|ACTIVE|COMPLETED|CANCELED

# Delete event
./discord-admin.sh event-delete <guildId> <eventId>
```

### 11. 邀请功能

```bash
# List invites
./discord-admin.sh invite-list <guildId>

# Create invite
./discord-admin.sh invite-create <channelId> [maxUses:0] [maxAge:86400] [temporary:true]
./discord-admin.sh invite-create <channelId> maxUses:100 maxAge:3600 unique:true

# Get invite info
./discord-admin.sh invite-info <inviteCode>

# Delete invite
./discord-admin.sh invite-delete <guildId> <inviteCode>

# Vanity URL (server setting)
./discord-admin.sh vanity-get <guildId>
./discord-admin.sh vanity-set <guildId> <code>
```

### 12. 审计日志

```bash
# Get audit logs
./discord-admin.sh audit-logs <guildId> [limit:100]
./discord-admin.sh audit-logs <guildId> user:<userId>
./discord-admin.sh audit-logs <guildId> action:CHANNEL_CREATE,BAN,KICK

# Audit action types:
# GUILD_UPDATE, CHANNEL_CREATE, CHANNEL_UPDATE, CHANNEL_DELETE, CHANNEL_OVERWRITE_CREATE, CHANNEL_OVERWRITE_UPDATE, CHANNEL_OVERWRITE_DELETE, MEMBER_KICK, MEMBER_PRUNE, BAN_ADD, BAN_REMOVE, MEMBER_UPDATE, MEMBER_ROLE_UPDATE, ROLE_CREATE, ROLE_UPDATE, ROLE_DELETE, INVITE_CREATE, INVITE_UPDATE, INVITE_DELETE, WEBHOOK_CREATE, WEBHOOK_UPDATE, WEBHOOK_DELETE, EMOJI_CREATE, EMOJI_UPDATE, EMOJI_DELETE, MESSAGE_DELETE, MESSAGE_BULK_DELETE, MESSAGE_PIN, MESSAGE_UNPIN, STAGE_INSTANCE_CREATE, STAGE_INSTANCE_UPDATE, STAGE_INSTANCE_DELETE, THREAD_CREATE, THREAD_UPDATE, THREAD_DELETE
```

### 13. 主题帖管理

```bash
# List threads
./discord-admin.sh thread-list <guildId>
./discord-admin.sh thread-list <channelId>

# Create thread
./discord-admin.sh thread-create <channelId> <name> <messageId> [autoArchive:1440]
./discord-admin.sh thread-create <channelId> <name> autoArchive:4320

# Edit thread
./discord-admin.sh thread-edit <threadId> name:<name> archived:true
./discord-admin.sh thread-edit <threadId> locked:true autoArchive:10080

# Delete thread
./discord-admin.sh thread-delete <threadId>

# Join/Leave thread
./discord-admin.sh thread-join <threadId>
./discord-admin.sh thread-leave <threadId>
```

### 14. 舞台频道

```bash
# Create stage instance
./discord-admin.sh stage-create <channelId> [topic:"Open Mic"]

# Edit stage
./discord-admin.sh stage-edit <channelId> topic:<topic> privacyLevel:GUILD_ONLY
./discord-admin.sh stage-edit <channelId> scheduledStart:<ISO8601>

# Close stage
./discord-admin.sh stage-close <channelId>
```

### 15. 集成管理

```bash
# List integrations (bots, apps)
./discord-admin.sh integration-list <guildId>

# Integration operations
./discord-admin.sh integration-sync <guildId> <integrationId>
./discord-admin.sh integration-delete <guildId> <integrationId>
```

### 16. 公会设置

```bash
# Edit server settings
./discord-admin.sh guild-edit <guildId> name:<newName>
./discord-admin.sh guild-edit <guildId> icon:<imageUrl>
./discord-admin.sh guild-edit <guildId> splash:<imageUrl>
./discord-admin.sh guild-edit <guildId> region:<voiceRegion>
./discord-admin.sh guild-edit <guildId> afkChannel:<channelId> afkTimeout:900
./discord-admin.sh guild-edit <guildId> systemChannel:<channelId> notifications:ALL_MESSAGES
./discord-admin.sh guild-edit <guildId> explicitContentFilter:ALL_MEMBERS
./discord-admin.sh guild-edit <guildId> mfaLevel:ELEVATED
./discord-admin.sh guild-edit <guildId> verificationLevel:HIGH
./discord-admin.sh guild-edit <guildId> defaultNotifications:ALL_MESSAGES

# Community features
./discord-admin.sh guild-enable-community <guildId>
./discord-admin.sh guild-disable-community <guildId>

# Server merge/transfer
./discord-admin.sh guild-transfer <guildId> <newOwnerId>
```

### 17. 小工具管理

```bash
# Widget settings
./discord-admin.sh widget-get <guildId>
./discord-admin.sh widget-edit <guildId> enabled:true channel:<channelId>
```

### 18. 管理日志

```bash
# Setup moderation log
./discord-admin.sh modlog-set <guildId> <channelId>
./discord-admin.sh modlog-get <guildId>
./discord-admin.sh modlog-disable <guildId>

# Configuration
./discord-admin.sh modlog-config <guildId> \
    kicks:true \
    bans:true \
    messages:true \
    nickname:true \
    roles:true \
    invites:true
```

### 19. 批量操作

```bash
# Mass ban
./discord-admin.sh mass-ban <guildId> <userIdsFileOrComma> [reason]

# Mass kick
./discord-admin.sh mass-kick <guildId> <userIdsFileOrComma> [reason]

# Mass role assignment
./discord-admin.sh mass-role <guildId> <roleId> <userIdsFileOrComma>

# Channel sync (copy permissions)
./discord-admin.sh channel-sync-perms <sourceChannelId> <targetChannelId>

# Role sync (copy all settings)
./discord-admin.sh role-clone <guildId> <roleId> <newName>
```

### 20. 模板操作

```bash
# Templates
./discord-admin.sh template-list <guildId>
./discord-admin.sh template-create <guildId> <name> [description]
./discord-admin.sh template-sync <guildId> <templateCode>
./discord-admin.sh template-delete <guildId> <templateId>

# Create server from template
./discord-admin.sh template-use <templateCode> <newServerName>
```

---

## ⚙️ 配置

### 环境变量

```bash
export DISCORD_BOT_TOKEN="your-bot-token"
export DISCORD_GUILD_ID="default-guild-id"
export DISCORD_DEFAULT_TIMEOUT=60        # API timeout in seconds
export DISCORD_MAX_RETRIES=3             # Retry on rate limit
export DISCORD_OUTPUT_FORMAT="json"      # json, pretty, minimal
```

### 所需权限

**选项 A：管理员权限（最简单）**
- 需要：`ADMINISTRATOR` 权限

**选项 B：细粒度权限**
```
MANAGE_CHANNELS
MANAGE_ROLES
KICK_MEMBERS
BAN_MEMBERS
MANAGE_MESSAGES
MANAGE_GUILD
VIEW_AUDIT_LOG
MANAGE_EMOJIS
MANAGE_WEBHOOKS
MANAGE_GUILD_EXPRESSIONS
MANAGE_EVENTS
MODERATE_MEMBERS
```

### 速率限制

该脚本会自动处理 Discord 的速率限制规则：
- 每个频道每秒最多发送 1 条消息
- 其他操作每 10 秒最多执行 50 次
- 遇到 429 错误时采用指数级重试机制
- 支持全局速率限制检测

---

## 📊 示例

### 完整的服务器设置流程

```bash
#!/bin/bash
# Setup a new community server from scratch

GUILD="123456789"
TOKEN="your-token"

# 1. Create roles
./discord-admin.sh role-create $GUILD "Admin" color:#FF0000 permissions:ADMINISTRATOR
./discord-admin.sh role-create $GUILD "Moderator" color:#FFA500 permissions:KICK_MEMBERS,BAN_MEMBERS,MANAGE_MESSAGES
./discord-admin.sh role-create $GUILD "Member" color:#00FF00 permissions:CREATE_INSTANT_INVITE

# 2. Create channels
./discord-admin.sh channel-create $GUILD "general" text
./discord-admin.sh channel-create $GUILD "announcements" announcements
./discord-admin.sh channel-create $GUILD "Voice Channels" category

# 3. Setup AutoMod
./discord-admin.sh automod-create $GUILD "Anti-Spam" keyword:scam,free,nitro actions:BLOCK_MESSAGE,ALERT

# 4. Create invite
INVITE=$(./discord-admin.sh invite-create 123456789 maxUses:100 unique:true | jq -r '.code')
echo "Server invite: discord.gg/$INVITE"

# 5. Setup mod log
./discord-admin.sh modlog-set $GUILD 987654321
```

### 日常管理例程

```bash
#!/bin/bash
# Daily server maintenance

GUILD="123456789"
TOKEN="your-token"

# Check audit logs for suspicious activity
./discord-admin.sh audit-logs $GUILD action:BAN_ADD --format pretty

# Check mod log
./discord-admin.sh audit-logs $GUILD user:BOT_USER_ID --format pretty

# List recent bans
./discord-admin.sh audit-logs $GUILD action:BAN_ADD limit:50 --format pretty

# Prune old inactive members
./discord-admin.sh member-prune $GUILD 30

# Check for spammers
./discord-admin.sh automod-list $GUILD
```

---

## 🔧 故障排除

### 常见错误及解决方法

| 错误代码 | 解决方案 |
|---------|-------------------------|
| `401: 未经授权` | 请检查你的机器人令牌是否有效 |
| `403: 禁止访问` | 机器人缺乏所需权限 |
| `404: 未找到` | 通道/公会/角色 ID 无效 |
| `429: 请求过多` | 请稍等，脚本会自动处理 |
| `50013: 权限不足` | 机器人的角色权限低于目标角色 |
| `50001: 无访问权限` | 机器人无法访问该频道 |

### 调试模式

```bash
./discord-admin.sh --debug <command>
```

---

## 📝 注意事项

- **14 天限制**：批量删除操作仅适用于过去 14 天内的消息。
- **角色层级**：机器人的角色必须高于目标角色。
- **操作权限**：某些操作需要服务器所有者的权限。
- **自定义链接（Vanity URLs）**：需要启用 `DISCOVERABLE` 功能并提升机器人权限。
- **模板**：仅限具有 `MANAGE_GUILD` 权限的用户使用。
- **审计日志**：仅机器人具有 `VIEW_AUDIT_LOG` 权限时才能查看，日志保留期限为 90 天。

---

## 🤖 支持的 API 端点

- 公会与公会成员
- 频道与主题帖
- 角色与权限
- 消息与反应
- 自动审核规则
- Webhook
- 邀请功能与自定义链接
- 公会模板
- 表情符号与贴纸
- 公会定时事件
- 音效库
- 审计日志
- 集成功能
- 公会小工具
- 应用程序命令（部分功能）