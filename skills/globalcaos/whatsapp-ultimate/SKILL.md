---
name: whatsapp-ultimate
version: 1.5.0
description: "**OpenClaw代理的完整WhatsApp集成功能：**  
- 支持发送消息、媒体文件、投票、贴纸、语音笔记以及表情符号；  
- 支持发送回复；  
- 具备全文搜索功能（通过SQLite和FTS5技术实现）；  
- 可下载并转录语音消息；  
- 支持导入聊天记录导出文件；  
- 全部聊天记录可自动同步；  
- 内置Bailey库，无需使用Docker或任何外部工具；  
- 与OpenClaw内置的WhatsApp通道无缝集成。"
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
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

**通过您的AI代理发送消息、媒体文件、进行投票、发送语音笔记以及管理群组——所有这些功能均可实现。同时，您可以即时搜索整个WhatsApp聊天记录。**

这是OpenClaw中最完整的WhatsApp功能插件。它支持与Baileys的原生集成，无需使用Docker、CLI工具或外部服务，只需连接即可开始使用。

---

## 先决条件

- 确保已安装OpenClaw，并且已配置WhatsApp通道。
- 通过二维码将您的WhatsApp账户与OpenClaw关联（使用`openclaw whatsapp login`命令）。

---

## 功能概览

| 功能类别 | 具体功能 |
|----------|----------|
| **消息发送** | 文本消息、媒体文件、投票、贴纸、语音笔记、GIF图片 |
| **互动** | 回应、回复/引用、编辑、取消发送 |
| **群组管理** | 创建群组、重命名群组、设置群组图标、编辑群组描述、管理群组成员、任命管理员、生成群组邀请链接 |
| **聊天记录** | 数据存储在本地SQLite数据库中，支持FTS5全文搜索；可导入历史聊天记录文件 |
| **数据同步** | 通过重新连接设备实现聊天记录的完全同步；支持自动备份和恢复 |

**总计：22项独立功能 + 可搜索的聊天记录**

---

## 消息发送

### 发送文本消息
```
message action=send channel=whatsapp to="+34612345678" message="Hello!"
```

### 发送媒体文件（图片/视频/文档）
```
message action=send channel=whatsapp to="+34612345678" message="Check this out" filePath=/path/to/image.jpg
```
支持的文件格式：JPG、PNG、GIF、MP4、PDF、DOC等。

### 发送投票
```
message action=poll channel=whatsapp to="+34612345678" pollQuestion="What time?" pollOption=["3pm", "4pm", "5pm"]
```

### 发送贴纸
```
message action=sticker channel=whatsapp to="+34612345678" filePath=/path/to/sticker.webp
```
贴纸格式必须为WebP，建议尺寸为512x512像素。

### 发送语音笔记
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```
**重要提示：** 请使用OGG/Opus格式发送语音笔记。MP3格式可能无法在WhatsApp中正常播放。

### 发送GIF图片
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```
发送GIF图片前，请先将其转换为MP4格式（WhatsApp要求如此）：
```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4 -y
```

---

## 互动功能

### 添加反应（表情）
```
message action=react channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123" emoji="🚀"
```

### 删除反应
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

### 提升群组成员为管理员
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降低群组成员为普通成员
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

### 撤销群组邀请链接
```
message action=revokeInviteCode channel=whatsapp groupJid="123456789@g.us"
```

### 查看群组信息
```
message action=getGroupInfo channel=whatsapp groupJid="123456789@g.us"
```
返回信息包括：群组名称、描述、成员列表、管理员列表以及创建日期。

---

## 访问控制

### 私人消息政策
您可以在`openclaw.json`文件中配置谁可以给您的代理发送私人消息：

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

| 政策 | 启用效果 |
|--------|----------|
| `"open"` | 任何人都可以发送私人消息 |
| `"allowlist"` | 仅允许`allowFrom`列表中的号码发送私人消息 |
| `"pairing"` | 未知发送者会收到配对代码提示 |
| `"disabled"` | 完全禁止接收私人消息 |

### 群组消息政策
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

| 政策 | 启用效果 |
|--------|----------|
| `"open"` | 会回复群组内的所有提及消息 |
| `"allowlist"` | 仅允许`groupAllowFrom`列表中的号码发送消息 |
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
允许您给自己发送消息（即“自我聊天”），以便与代理进行交互。

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
消息必须以该前缀开头才能触发代理的响应。该前缀适用于：
- 自我聊天
- 允许的私人消息
- 您作为发送者发送的任何私人消息

---

## JID格式

WhatsApp内部使用JID（Jabber ID）进行标识：

| 类型 | 格式 | 例子 |
|------|--------|---------|
| 个人用户 | `<number>@s.whatsapp.net` | `34612345678@s.whatsapp.net` |
| 群组 | `<id>@g.us` | `123456789012345678@g.us` |

当使用`to=`与电话号码交互时，OpenClaw会自动将其转换为JID格式。

---

## 使用提示

### 查找群组名称
聊天记录数据库中`chat_name`字段可能显示为`NULL`。要获取群组的显示名称，请使用以下命令：
```
message action=getGroupInfo channel=whatsapp target="<group-jid>"
```
返回信息包括：群组名称、描述以及所有成员的列表（包括管理员角色）。

**与人类交流时，请始终使用群组的显示名称——JID仅用于内部识别。**

### 语音笔记
请务必使用OGG/Opus格式发送语音笔记：
```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

### 贴纸转换
请将图片转换为WebP格式的贴纸：
```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

### 避免滥用功能

WhatsApp有反垃圾邮件机制。请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与您联系过的人发送消息

### 消息ID
要回复、编辑或取消发送消息，您需要知道消息的ID。接收到的消息中会包含消息ID；您发送的消息也会附带ID。

---

## 适用场景

当您的代理需要执行以下操作时，可以使用`whatsapp-ultimate`插件：
- 通过WhatsApp发送文本、图片、视频或语音笔记
- 在群组聊天中创建和管理员理投票
- 用表情符号回复消息、引用或编辑/取消发送消息
- 创建群组、管理群组成员、生成群组邀请链接
- 根据关键词、发送者或日期搜索过去的聊天记录
- 导入并索引WhatsApp聊天记录文件（.txt格式）
- 获取群组元数据（名称、描述、成员列表）
- 自动生成群组聊天活动的每日摘要

## 与其他插件的比较

| 功能 | whatsapp-ultimate | wacli | whatsapp-business |
|---------|-------------------|-------|-------------------|
| 原生集成 | ✅ | ❌ | 需要Go CLI二进制文件或外部API |
| 发送文本 | ✅ | ✅ | ✅ |
| 发送媒体文件 | ✅ | ✅ | ✅（仅支持模板） |
| 投票 | ✅ | ❌ | ❌ |
| 贴纸 | ✅ | ❌ | ❌ |
| 语音笔记 | ✅ | ❌ | ❌ |
| GIF图片 | ✅ | ❌ | ❌ |
| 回应/引用 | ✅ | ❌ | ❌ |
| 编辑消息 | ✅ | ❌ | ❌ |
| 取消发送/删除 | ✅ | ❌ | ❌ |
| 群组管理 | ✅（包括创建、重命名、设置图标、描述、管理成员、任命管理员等） | ❌ | ❌ |
| 群组信息/元数据 | ✅ | ❌ | ❌ |
| 双向聊天 | ✅ | ❌ | ✅（需要Webhook） |
| 聊天记录（SQLite + FTS5） | ✅ | ✅（支持同步） | ❌ |
| 导入聊天记录文件 | ✅ | ❌ | ❌ |
| 个人WhatsApp账户 | ✅ | ✅ | （仅限企业版） |
| 外部依赖 | **无** | 需要Go二进制文件或Maton API密钥 | 需要API密钥和账户 |

---

## 聊天记录与搜索（v1.2.0+）

OpenClaw现在将所有WhatsApp消息存储在本地SQLite数据库中，并支持全文搜索（FTS5格式）。这样您再也不会丢失任何聊天记录。

### 工作原理

- **实时捕获**：每条新消息都会被自动保存。
- **历史记录导入**：可以从WhatsApp聊天记录文件中批量导入聊天记录。
- **全文搜索**：可以根据内容、发送者或聊天记录内容进行搜索。

### 搜索聊天记录

您可以使用`whatsapp_history`工具（该工具会自动集成到您的代理中）进行搜索：
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

WhatsApp并未通过API提供无限量的历史记录。若要获取旧消息，请按照以下步骤操作：
1. **从手机中导出聊天记录**：进入“设置” → “聊天记录” → “导出聊天记录”（仅导出文本部分）。
2. **将导出的.txt文件保存在可访问的位置**。
3. **导入聊天记录**：
```
whatsapp_history action=import path="/path/to/exports"
```

您也可以单独导入某个群的聊天记录：
```
whatsapp_history action=import path="/path/to/chat.txt" chatName="Family Group"
```

### 数据库位置

聊天记录存储在SQLite数据库中，采用WAL模式以支持并发访问。

### 使用示例

- “我之前跟Sarah提到了会议的相关内容吗？”
- “找到所有包含‘截止日期’的聊天记录”
- “向工作群组展示我最近发送的消息”
- “John什么时候提到季度报告的？”

您的代理可以通过搜索完整的WhatsApp聊天记录来回答这些问题。

### 自动生成每日摘要（通过Cron任务）

您可以设置每日Cron任务来生成群组聊天的摘要：
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

代理会自动读取昨天的聊天记录并生成每日摘要，无需您手动操作。

---

## 下载和转录语音消息（v1.3.0+）

聊天记录数据库会将语音消息的原始数据（包括媒体文件信息）存储在`raw_json`字段中。这意味着您可以下载并解密任何语音消息、图片或视频文件——即使这些消息来自群组聊天或来自其他用户。

### 工作原理

WhatsApp会对媒体文件使用唯一的密钥进行加密。该密钥会存储在消息的原始数据中，Baileys框架会负责解密操作。

### 下载语音消息

1. 使用`whatsapp_history`命令查找相关消息：
```
whatsapp_history action=search chat="GROUP_JID" sender="PersonName" limit=10
```
查找类型为“voice”或“audio”的消息。
2. 使用Node.js脚本下载音频文件（该脚本需要在OpenClaw的源代码目录中运行，以便Baileys框架能够访问这些文件）：
```bash
cd /path/to/openclaw/source && node -e "
const { downloadContentFromMessage } = require('@whiskeysockets/baileys');
const Database = require('better-sqlite3');
const fs = require('fs');
const { pipeline } = require('stream/promises');

async function main() {
  const db = new Database('$HOME/.openclaw/data/whatsapp-history.db', { readonly: true });
  const row = db.prepare('SELECT raw_json FROM messages WHERE id = ?').get('MESSAGE_ID_HERE');
  const msg = JSON.parse(row.raw_json);
  const audioMsg = msg.message.audioMessage;
  const stream = await downloadContentFromMessage(audioMsg, 'audio');
  await pipeline(stream, fs.createWriteStream('/tmp/voice-msg.ogg'));
  console.log('Downloaded!');
}
main().catch(console.error);
"
```

3. 使用Whisper或其他语音转文字工具将音频文件转录为文本：
```bash
ffmpeg -i /tmp/voice-msg.ogg -ar 16000 -ac 1 /tmp/voice-msg.wav -y
whisper /tmp/voice-msg.wav --model base --language es --output_format txt --output_dir /tmp/
cat /tmp/voice-msg.txt
```

### 下载其他类型的媒体文件

不同类型的媒体文件对应的字段和内容类型如下：

| 媒体类型 | 对应的原始数据字段 | 内容类型 |
|------------|-------------|--------------|
| 语音/音频 | `audioMessage` | `"audio"` |
| 图片 | `imageMessage` | `"image"` |
| 视频 | `videoMessage` | `"video"` |
| 文档 | `documentMessage` | `"document"` |
| 贴纸 | `stickerMessage` | `"sticker"` |

### 注意事项

- **媒体文件的URL是临时链接**：请尽快下载媒体文件，否则Baileys框架会尝试重新请求下载（这需要保持网络连接）。
- **建议保持WhatsApp连接状态**：如果媒体文件的URL已过期，Baileys框架需要网络连接来获取新的URL。
- **数据库路径**：`~/.openclaw/data/whatsapp-history.db`
- **开发环境要求**：下载脚本需要`@whiskeysockets/baileys`和`better-sqlite3`库，这两个工具都包含在OpenClaw的源代码目录中。

### 使用示例

- 转录群组聊天中的语音消息
- 保存群组中分享的重要图片或文档
- 生成语音聊天记录的文字版本
- 分析您不懂的语言的语音文件（Whisper支持99种语言）

---

## 完整聊天记录同步（v1.5.0+）

您可以将整个WhatsApp聊天记录（包括数月或数年内的所有消息）同步到本地数据库。该功能通过重新连接您的WhatsApp设备来实现同步，这一过程类似于首次连接设备时的同步操作。

### 原因

Baileys框架中的按需获取聊天记录的功能（`fetchMessageHistory`）存在问题（参见[Issue #1934](https://github.com/WhiskeySockets/Baileys/issues/1934)）。因此，唯一可靠的获取旧消息的方法是通过初始化设备连接来同步数据。此功能可自动完成整个同步过程。

### 设置步骤

1. 安装`whatsapp-resync`插件：
   - 将插件复制到`~/.openclaw/extensions/whatsapp-resync/`目录。
2. 在`openclaw.json`文件中配置相关设置：
   ```json
{
  "plugins": [
    { "name": "whatsapp-resync", "path": "~/.openclaw/extensions/whatsapp-resync" }
  ]
}
```
3. 重启OpenClaw代理。

### API端点

| 端点 | 方法 | 功能 |
|----------|--------|-------------|
| `/api/whatsapp/resync` | POST | 触发同步操作：备份认证信息、清除缓存数据、关闭监听器 |
| `/api/whatsapp/resync/restore` | POST | 在出现问题时从备份中恢复数据 |

### 触发同步操作

```bash
curl -X POST http://localhost:3120/api/whatsapp/resync
```

### 完成同步过程

1. 打开Webchat界面 → 选择“Channels”选项卡 → 用手机扫描二维码。
2. 在手机上进入WhatsApp设置 → 选择“Linked Devices” → 选择要同步的设备。
3. 扫描二维码。
4. 等待同步完成（根据聊天记录的数量，同步可能需要1-5分钟）。

### 验证同步结果

成功同步后，您将看到之前保存的所有聊天记录。

### 备份恢复

如果系统出现故障，您可以恢复之前的认证状态：
```bash
# Restore latest backup
curl -X POST http://localhost:3120/api/whatsapp/resync/restore

# Restore specific backup
curl -X POST http://localhost:3120/api/whatsapp/resync/restore \
  -H 'Content-Type: application/json' \
  -d '{"backupDir": "/path/to/backup"}'
```

### 安全性

- **自动备份**：在删除数据前会备份认证信息。
- **数据安全**：仅清除认证状态，现有聊天记录不会被删除。
- **一键恢复**：可以轻松恢复到之前的状态。
- **不影响现有数据**：您的WhatsApp账户不会受到影响，仅会更新设备关联状态。

### 实际测试结果

在测试中，一次同步操作成功恢复了：
- 17,609条消息（之前仅恢复3,242条）
- 1,229个聊天记录（之前仅恢复57个）
- 4,077个联系人信息
- 涉及**3年以上的聊天记录**（最远可追溯到2022年9月）

---

## 常见问题及解决方法

### 家人或朋友发送的私人消息无法到达代理
**问题**：您已将某人添加到`groupAllowFrom`列表中，但他们发送的私人消息无法被代理接收。

**解决方法**：也将此人添加到`allowFrom`列表中。`groupAllowFrom`列表仅控制群组内的消息发送权限，不影响私人消息的接收。

```json
{
  "allowFrom": ["+34612345678", "+14155551234"],
  "groupAllowFrom": ["+34612345678", "+14155551234"]
}
```

### 私人消息中无法区分消息的发送者
**问题**：私人消息中的所有消息都显示相同的电话号码。

**原因**：在OpenClaw 2026.2.1版本之前，系统会显示发送者的WhatsApp ID（即电话号码），而非实际发送者的名称。

**解决方法**：请更新到最新版本的OpenClaw。现在代理能够正确区分您发送的消息和对方发送的消息。

### 语音笔记无法在WhatsApp中播放
**问题**：虽然成功上传了语音文件，但无法播放。

**解决方法**：请确保使用OGG/Opus格式进行上传，并在发送时设置`asVoice=true`参数。

---

## 架构特点

**无需依赖任何外部服务**：既不需要Docker，也不需要CLI工具，所有功能都通过直接协议实现。

---

## 开发者信息

该插件由Oscar Serra开发，Claude（Anthropic团队成员）提供了技术支持。

**这是一个让WhatsApp功能真正发挥作用的插件。**

---

## 许可证

该插件遵循MIT许可证，属于OpenClaw项目的一部分。

---

## 链接资源

- OpenClaw插件分支：https://github.com/globalcaos/clawdbot-moltbot-openclaw
- Baileys框架：https://github.com/WhiskeySockets/Baileys
- ClawHub平台：https://clawhub.com