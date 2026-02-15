---
name: whatsapp-ultimate
version: 1.3.0
description: "您可以通过您的AI代理发送WhatsApp消息、媒体文件、进行投票、使用贴纸、录制语音笔记、发送表情反应以及管理群组。支持通过全文搜索（基于SQLite和FTS5技术）来查找消息历史记录。该功能还支持导入WhatsApp聊天记录的导出文件。同时，它具备与Bailey框架的原生集成能力——无需任何外部依赖，也无需使用Docker或CLI工具。这是OpenClaw平台中最完善的WhatsApp相关功能模块。"
homepage: https://github.com/openclaw/openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
metadata:
  openclaw:
    emoji: "📱"
    requires:
      channels: ["whatsapp"]
    tags:
      - whatsapp
      - messaging
      - chat
      - voice-notes
      - group-management
      - message-history
      - search
      - media
      - polls
      - stickers
      - reactions
      - baileys
---

# WhatsApp Ultimate

**通过您的人工智能助手发送消息、媒体文件、进行投票、发送语音笔记，以及管理群组——所有这些功能都无需离开您的应用程序。**您可以即时搜索整个WhatsApp聊天记录。

这是OpenClaw中最全面的WhatsApp功能插件。它支持与Baileys的原生集成，无需使用Docker、CLI工具或外部服务，只需连接即可开始使用。

---

## 先决条件

- 已配置WhatsApp通道的OpenClaw
- 通过二维码链接您的WhatsApp账户（`openclaw whatsapp login`）

---

## 功能概览

| 功能类别 | 具体功能 |
|----------|----------|
| **消息发送** | 文本、媒体文件、投票、贴纸、语音笔记、GIF图片 |
| **互动** | 回应、回复/引用、编辑、取消发送 |
| **群组管理** | 创建群组、重命名群组、设置群组图标、编辑群组描述、管理群组成员、任命管理员、生成群组邀请链接 |
| **聊天记录** | 使用SQLite数据库持久化存储聊天记录，支持FTS5全文搜索，可导入历史聊天记录文件 |

**总计：22项独立功能 + 可搜索的聊天记录**

---

## 消息发送

### 发送文本
```
message action=send channel=whatsapp to="+34612345678" message="Hello!"
```

### 发送媒体文件（图片/视频/文档）
```
message action=send channel=whatsapp to="+34612345678" message="Check this out" filePath=/path/to/image.jpg
```
支持的文件格式：JPG、PNG、GIF、MP4、PDF、DOC等

### 发送投票
```
message action=poll channel=whatsapp to="+34612345678" pollQuestion="What time?" pollOption=["3pm", "4pm", "5pm"]
```

### 发送贴纸
```
message action=sticker channel=whatsapp to="+34612345678" filePath=/path/to/sticker.webp
```
贴纸格式必须为WebP，建议尺寸为512x512像素

### 发送语音笔记
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```
**重要提示：**请使用OGG/Opus格式的语音文件，因为MP3格式可能无法在WhatsApp中正常播放

### 发送GIF图片
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```
发送前请将GIF图片转换为MP4格式（WhatsApp要求）

---

## 互动功能

### 添加回复表情
```
message action=react channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123" emoji="🚀"
```

### 删除回复表情
```
message action=react channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123" remove=true
```

### 回复/引用消息
```
message action=reply channel=whatsapp to="34612345678@s.whatsapp.net" replyTo="QUOTED_MSG_ID" message="Replying to this!"
```

### 编辑自己的消息
```
message action=edit channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123" message="Updated text"
```

### 取消发送/删除消息
```
message action=unsend channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123"
```

---

## 群组管理

### 创建群组
```
message action=group-create channel=whatsapp name="Project Team" participants=["+34612345678", "+34687654321"]
```

### 重命名群组
```
message action=renameGroup channel=whatsapp groupId="123456789@g.us" name="New Name"
```

### 设置群组图标
```
message action=setGroupIcon channel=whatsapp groupId="123456789@g.us" filePath=/path/to/icon.jpg
```

### 设置群组描述
```
message action=setGroupDescription channel=whatsapp groupJid="123456789@g.us" description="Team chat for Q1 project"
```

### 添加群组成员
```
message action=addParticipant channel=whatsapp groupId="123456789@g.us" participant="+34612345678"
```

### 移除群组成员
```
message action=removeParticipant channel=whatsapp groupId="123456789@g.us" participant="+34612345678"
```

### 提升某人为群组管理员
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降低某人的管理员权限
```
message action=demoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 退出群组
```
message action=leaveGroup channel=whatsapp groupId="123456789@g.us"
```

### 获取群组邀请链接
```
message action=getInviteCode channel=whatsapp groupJid="123456789@g.us"
```
返回格式：`https://chat.whatsapp.com/XXXXX`

### 取消群组邀请链接
```
message action=revokeInviteCode channel=whatsapp groupJid="123456789@g.us"
```

### 查看群组信息
```
message action=getGroupInfo channel=whatsapp groupJid="123456789@g.us"
```
返回信息包括：群组名称、描述、成员列表及管理员信息

---

## 访问控制

### 私信策略
您可以通过`openclaw.json`文件配置谁可以给您的助手发送私信：

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+34612345678", "+14155551234"],
      "triggerPrefix": "Jarvis"
    }
  }
}
```

| 策略 | 行为 |
|--------|----------|
| `"open"` | 任何人都可以发送私信 |
| `"allowlist"` | 只有`allowFrom`列表中的号码才能发送私信 |
| `"pairing"` | 未知发件人会收到配对代码提示 |
| `"disabled"` | 不接受任何私信 |

### 群组消息策略
```json
{
  "channels": {
    "whatsapp": {
      "groupPolicy": "open",
      "groupAllowFrom": ["+34612345678", "+14155551234"]
    }
  }
}
```

| 策略 | 行为 |
|--------|----------|
| `"open"` | 回复群组内的所有消息 |
| `"allowlist"` | 只有`groupAllowFrom`列表中的号码才能发送消息 |
| `"disabled"` | 忽略所有群组消息 |

### 自我聊天模式
```json
{
  "channels": {
    "whatsapp": {
      "selfChatMode": true
    }
  }
}
```
允许您与自己发送消息（即“自我聊天”），从而与助手进行互动

### 触发前缀
```json
{
  "channels": {
    "whatsapp": {
      "triggerPrefix": "Jarvis"
    }
  }
}
```
消息必须以该前缀开头才能触发助手的响应。该前缀适用于：
- 自我聊天
- 允许的私信
- 您自己发送的私信

---

## JID格式

WhatsApp内部使用JID（Jabber ID）进行通信：

| 类型 | 格式 | 例子 |
|------|--------|---------|
| 个人用户 | `<数字>@s.whatsapp.net` | `34612345678@s.whatsapp.net` |
| 群组 | `<id>@g.us` | `123456789012345678@g.us` |

当使用`to=`与电话号码通信时，OpenClaw会自动将其转换为JID格式。

---

## 使用提示

### 查找群组名称
聊天记录数据库中`chat_name`字段可能显示为`NULL`。要获取群组的显示名称，请使用以下命令：
```
message action=getGroupInfo channel=whatsapp target="<group-jid>"
```
返回信息包括：群组名称、描述及所有成员的列表（包括管理员角色）。

**与人类交流时，请始终使用群组的显示名称——JID仅用于系统内部识别**

### 语音笔记
请务必使用OGG/Opus格式的语音文件：

```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

### 贴纸
请将图片转换为WebP格式的贴纸：

```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

### 使用限制

WhatsApp有防垃圾信息机制。请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与您联系的联系人发送消息

### 消息ID
要回复、编辑或取消发送消息，您需要知道消息的ID。接收到的消息中会包含消息ID；您发送的消息的响应中也会包含该ID。

---

## 适用场景

当您的助手需要执行以下操作时，可以使用`whatsapp-ultimate`插件：
- 通过WhatsApp发送文本、图片、视频、文档或语音笔记
- 在群组聊天中创建和管理投票
- 用表情符号回复消息、引用或编辑/取消发送消息
- 创建群组、管理成员、生成群组邀请链接
- 根据关键词、发送者或日期搜索过去的WhatsApp聊天记录
- 导入并索引WhatsApp聊天记录文件（.txt格式）
- 获取群组元数据（名称、描述、成员列表）
- 自动生成群组聊天活动的每日摘要

## 与其他插件的比较

| 功能 | whatsapp-ultimate | wacli | whatsapp-business |
|---------|-------------------|-------|-------------------|
| 原生集成 | ✅ | ❌ | 需要安装Go CLI工具 |
| 发送文本 | ✅ | ✅ | ✅ |
| 发送媒体文件 | ✅ | ✅ | ✅（需使用特定模板） |
| 投票 | ✅ | ❌ | ❌ |
| 贴纸 | ✅ | ❌ | ❌ |
| 语音笔记 | ✅ | ❌ | ❌ |
| GIF图片 | ✅ | ❌ | ❌ |
| 回应/引用 | ✅ | ❌ | ❌ |
| 编辑消息 | ✅ | ❌ | ❌ |
| 取消发送/删除 | ✅ | ❌ | ❌ |
| 群组管理 | ✅（包括创建、重命名、设置图标、编辑描述、管理成员、任命管理员） | ❌ | ❌ |
| 群组信息/元数据 | ✅ | ❌ | ❌ |
| 双向聊天 | ✅ | ❌ | ✅（需要Webhook） |
| 消息记录（SQLite + FTS5） | ✅ | ✅ | ❌ |
| 导入聊天记录文件 | ✅ | ❌ | ❌ |
| 个人WhatsApp账户 | ✅ | ✅ | （仅限企业版） |
| 外部依赖 | **无** | 需要安装Go CLI工具 | 需要Maton API密钥和账户 |

---

## 消息记录与搜索（v1.2.0及以上版本）

OpenClaw现在将所有WhatsApp消息存储在本地SQLite数据库中，并支持全文搜索（FTS5格式），确保您不会丢失任何聊天记录。

### 工作原理

- **实时捕获**：每条新消息都会自动保存
- **历史记录导入**：可以从WhatsApp聊天记录文件批量导入聊天记录
- **全文搜索**：可以根据内容、发送者或聊天记录内容快速查找任何消息

### 搜索聊天记录

您可以使用`whatsapp_history`工具（该工具会自动集成到您的助手中）进行搜索：

```
# Search by keyword
whatsapp_history action=search query="meeting tomorrow"

# Filter by chat
whatsapp_history action=search chat="Family Group" limit=50

# Find what you said
whatsapp_history action=search fromMe=true query="I promised"

# Filter by sender
whatsapp_history action=search sender="John" limit=20

# Date range
whatsapp_history action=search since="2026-01-01" until="2026-02-01"

# Database stats
whatsapp_history action=stats
```

### 导入历史聊天记录

WhatsApp的API不提供无限量的历史聊天记录。要获取旧消息，请按照以下步骤操作：
1. **从手机端导出聊天记录**：进入设置 → 聊天记录 → 导出聊天记录（选择“不包含媒体文件”选项）
2. **将导出的.txt文件保存到可访问的位置**
3. **导入聊天记录**：
```
whatsapp_history action=import path="/path/to/exports"
```

您也可以导入单个聊天记录：

```
whatsapp_history action=import path="/path/to/chat.txt" chatName="Family Group"
```

### 数据库位置

聊天记录存储在采用WAL模式的SQLite数据库中，支持并发访问。

### 使用示例

- “我之前跟Sarah说了关于会议的什么？”
- “查找所有提到‘截止日期’的消息”
- “向工作群组展示我最近发送的消息”
- “John什么时候提到季度报告的？”

您的助手可以通过搜索完整的WhatsApp聊天记录来回答这些问题。

### 自动化每日摘要（通过Cron任务）

您可以设置每日Cron任务，自动总结群组的活跃聊天记录：

```json
{
  "name": "whatsapp-group-summary",
  "schedule": { "kind": "cron", "expr": "30 5 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Search yesterday's WhatsApp messages using whatsapp_history. For groups with 20+ messages, generate a summary with key topics and action items. Send via message tool to the target group."
  }
}
```

助手会自动读取昨天的聊天记录，并在早晨为您提供摘要，无需您手动操作。

---

## 常见问题及解决方法

### 家人/朋友的私信无法送达助手
**问题**：您已将某人添加到`groupAllowFrom`列表中，但他们发送的私信无法送达助手。

**解决方法**：也将该人添加到`allowFrom`列表中。`groupAllowFrom`列表仅控制群组内的消息访问权限，不控制私信发送。

```json
{
  "allowFrom": ["+34612345678", "+14155551234"],
  "groupAllowFrom": ["+34612345678", "+14155551234"]
}
```

### 无法区分私信中的消息发送者
**问题**：私信对话中的所有消息都显示相同的电话号码。

**原因**：在OpenClaw 2026.2.1版本之前，私信中显示的是对方的电话号码（即“chat ID”），而非实际发送者信息。

**解决方法**：请更新到最新版本的OpenClaw。现在助手可以正确区分您发送的消息和对方发送的消息。

### 语音笔记在WhatsApp中无法播放
**问题**：虽然音频文件已发送，但在WhatsApp中显示为无法播放。

**解决方法**：请使用OGG/Opus格式的音频文件，并在发送时设置`asVoice=true`参数。

---

## 架构特点

**特点**：
- 无需依赖任何外部服务或Docker
- 无需使用CLI工具
- 直接通过协议与WhatsApp进行集成

---

## 创作者与贡献者

该插件由Oscar Serra开发，Claude（Anthropic团队）提供了技术支持。

“这个插件让WhatsApp终于能够按照预期的方式正常使用了。”

---

## 许可证

遵循MIT许可证，属于OpenClaw项目的一部分。

---

## 链接

- OpenClaw插件仓库：https://github.com/globalcaos/clawdbot-moltbot-openclaw
- Baileys库：https://github.com/WhiskeySockets/Baileys
- ClawHub平台：https://clawhub.com