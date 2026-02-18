---
name: whatsapp-ultimate
version: 1.9.0
description: "**OpenClaw代理的完整WhatsApp集成功能：**  
- 支持发送消息、媒体文件、投票、贴纸、语音笔记以及各种表情反应。  
- 支持通过全文搜索（SQLite + FTS5）查询聊天历史记录。  
- 可下载并转录语音消息。  
- 支持导入导出的聊天数据。  
- 全部聊天记录可重新同步。  
**新增功能：**  
🤔↔🧐 **“Thinking Heartbeat”**：一种交替显示的反应指示器（约1秒更新一次），同时具备监控功能（当系统卡顿时会显示为“冻结”状态）。  
- 所有来自管理员的语音消息可绕过预设的前缀过滤规则。  
- 该集成完全基于Bailey框架实现，无需使用Docker或任何外部工具，可与OpenClaw内置的WhatsApp通道无缝协作。"
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
      - thinking-indicator
      - progress-indicator
      - typing-indicator
      - voice-messages
      - baileys
---
# WhatsApp Ultimate

**通过您的AI代理发送消息、媒体文件、进行投票、录制语音笔记，以及管理群组——所有这些功能一应俱全。** **您可以即时搜索整个WhatsApp聊天记录。**

这是OpenClaw中最完整的WhatsApp集成技能。它支持原生Baileys集成，无需Docker、CLI工具或外部服务，只需连接即可使用。

---

## 先决条件

- 已配置WhatsApp通道的OpenClaw
- 通过二维码链接WhatsApp账户（`openclaw whatsapp login`）

---

## 功能概览

| 功能类别          | 具体功能                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **消息发送**        | 文本、媒体文件、投票、贴纸、语音笔记、GIF图片                                                                                   |
| **互动**          | 回复/引用、编辑、取消发送                                                                                   |
| **群组管理**        | 创建群组、重命名群组、设置群组图标、编辑群组描述、管理群组成员、邀请新成员                                                                                   |
| **群组进度显示**      | 显示群组消息处理中的“🤔”提示（表示消息正在处理中）                                                                                   |
| **媒体文件特殊处理**    | 群组中的语音/媒体消息可绕过前缀过滤                                                                                   |
| **聊天记录**        | 使用持久化的SQLite数据库存储聊天记录，支持FTS5全文本搜索，可导入历史聊天记录文件                                                                                   |
| **数据同步**        | 通过重新链接实现聊天记录的完整同步，支持自动备份和恢复                                                                                   |

**总计：24项独立功能 + 可搜索的聊天记录**

---

## 🤔 消息处理中的“🤔”提示（进度指示器）

**问题：** 链接WhatsApp的设备（如Baileys、Web API）无法在群组聊天中显示“正在输入...”的提示。这是WhatsApp服务器端的限制——虽然协议正确地发送了`chatstate` XML节点，但WhatsApp服务器不会将输入提示显示给群组成员。该问题已在[Baileys #866](https://github.com/WhiskeySockets/Baileys/issues/866)中得到确认。**

**解决方案：** 当代理开始处理消息时，会立即在原始消息上显示“🤔”提示。回复准备好后，该提示会自动消失。这为用户提供了即时的视觉反馈，让他们知道代理正在工作，无需再担心消息是否已被接收。

**工作原理：**
1. 消息到达 → 代理在原始消息上显示“🤔”提示（瞬间完成，耗时<100毫秒）
2. 代理处理消息（使用工具、进行API调用等）
3. 回复发送 → “🤔”提示自动消失

**适用场景：** 群组 ✅ | 私人消息 ✅ | 所有聊天类型

这是**唯一一个**解决了“输入提示不可见”问题的WhatsApp集成方案。其他WhatsApp集成方案在代理处理消息时，用户会看到长时间的沉默。

---

## 群组所有者的语音/媒体文件特殊处理

现在，机器人所有者的语音消息和媒体文件可以绕过群组中的`triggerPrefix`过滤规则。之前，如果群组中发送的语音笔记前缀为“Jarvis”，则该消息会被忽略（因为音频文件无法携带文本前缀）。现在，这些消息会自动被转发给代理。

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

**重要提示：** 使用OGG/Opus格式发送语音笔记。MP3格式可能无法正常播放

### 发送GIF图片
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```

**注意：** 需先将GIF图片转换为MP4格式（WhatsApp要求如此）：
```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4 -y
```

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

### 编辑消息（仅限自己的消息）
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

### 提升成员为群组管理员
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降低成员为群组管理员
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

返回链接：`https://chat.whatsapp.com/XXXXX`

### 撤销群组邀请链接
```
message action=revokeInviteCode channel=whatsapp groupJid="123456789@g.us"
```

### 获取群组信息
```
message action=getGroupInfo channel=whatsapp groupJid="123456789@g.us"
```

返回信息包括：群组名称、描述、成员列表、管理员列表及创建日期

---

## 访问控制

### 私人消息政策

在`openclaw.json`中配置谁可以给您的代理发送私人消息：

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

| 政策            | 行为                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `"open"`          | 任何人都可以发送私人消息                                                                                   |
| `"allowlist"`       | 只有`allowFrom`列表中的号码才能发送私人消息                                                                                   |
| `"pairing"`        | 未知发送者会收到配对代码提示                                                                                   |
| `"disabled"`        | 不接受任何私人消息                                                                                   |

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

| 政策            | 行为                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `"open"`          | 会回复群组中的提及消息                                                                                   |
| `"allowlist"`       | 只有`groupAllowFrom`列表中的发送者才能发送消息                                                                                   |
| `"disabled"`        | 忽略所有群组消息                                                                                   |

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

允许您与自己发送消息（即“自我聊天”），以便与代理进行互动

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
- 您（作为群组所有者）使用该前缀发送的任何私人消息

### 消息前缀（用于标识发送者）

```json
{
  "channels": {
    "whatsapp": {
      "messagePrefix": "🤖"
    }
  }
}
```

代理发出的所有消息都会加上这个前缀。建议使用表情符号（如🤖），以便接收者能立即知道是谁在发送消息——尤其是在群组聊天或代理使用您的个人号码发送消息时。

---

## JID格式

WhatsApp内部使用JID（Jabber ID）：

| 类型            | 格式                                                                                          | 示例                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 个人用户         | `<number>@s.whatsapp.net`     | `34612345678@s.whatsapp.net`     |
| 群组用户         | `<id>@g.us`         | `123456789012345678@g.us`         |

当使用`to=`与电话号码关联时，OpenClaw会自动将其转换为JID格式。

---

## 提示

### 查找群组名称

聊天记录数据库中`chat_name`字段可能为`NULL`。要获取群组的显示名称，可以使用以下方法：

```
message action=getGroupInfo channel=whatsapp target="<group-jid>"
```

返回信息包括：群组名称、描述以及所有成员的列表（包括管理员角色）。

**与人类交流时，请始终使用群组名称——JID仅用于内部识别。**

### 语音笔记

请始终使用OGG/Opus格式录制语音笔记：

```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

### 贴纸转换

将图片转换为WebP格式的贴纸：

```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

### 私人消息的优化设置（推荐）

WhatsApp适用于小屏幕设备。只需发送**最终回复**——不要发送工具操作信息、中间状态或调试输出。输入提示（三个点）已经足够作为处理进度反馈。

**在OpenClaw配置中关闭详细输出：**

```json
{
  "agents": {
    "defaults": {
      "verboseDefault": "off"
    }
  }
}
```

这样可以防止`[openclaw] 🛠️ Exec: ...`、`[openclaw] 📖 Read`等消息在聊天中重复显示。

**语音回复中应包含文字记录**：当用户发送语音消息时，回复中应包含文字记录，以便接收者确认消息内容。

### 避免滥用

WhatsApp有反垃圾邮件机制。请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与您联系的人发送消息

### 消息ID

要回复、编辑或取消发送消息，您需要消息的ID。接收到的消息中包含消息ID；您发送的消息的响应中也包含消息ID。

---

## 何时使用此技能

当您的代理需要执行以下操作时，可以使用`whatsapp-ultimate`技能：
- 通过WhatsApp发送文本、图片、视频、文档或语音笔记
- 在群组聊天中创建和管理投票
- 用表情符号回复消息、引用消息、编辑或取消发送消息
- 创建群组、管理成员、获取群组邀请链接
- 根据关键词、发送者或日期搜索过去的WhatsApp聊天记录
- 导入并索引WhatsApp聊天记录文件（.txt格式）
- 获取群组元数据（名称、描述、成员列表）
- 自动生成群组聊天记录的每日摘要

## 与其他技能的比较

| 功能                        | whatsapp-ultimate                                                         | wacli                       | whatsapp-business       |
| ------------------------------- | ------------------------------------------------------------------------- | --------------------------- | ----------------------- |
| 原生集成              | ✅ （无需任何外部依赖）                                                                 | ❌ 需要Go CLI二进制文件            | ❌ 需要外部API和密钥         |
| 发送文本                        | ✅                                                                 | ✅                                                                 | ✅                                                                 |
| 发送媒体文件                      | ✅                                                                 | ✅ （仅支持特定文件格式）                         | ✅                                                                 |
| 进行投票                        | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 使用贴纸                        | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 录制语音笔记                     | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 发送GIF图片                        | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 添加回复表情                    | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 回复/引用消息                    | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 编辑消息                        | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 取消发送/删除消息                    | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 群组管理                        | ✅ （包括创建、重命名、设置图标、描述、管理成员、邀请新成员） | ❌                                                                 | ❌                                                                 |
| 获取群组信息/元数据                   | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 双向聊天                        | ✅                                                                 | ❌                                                                 | ✅ （支持Webhook）                                                                 |
| 查看聊天记录（SQLite + FTS5）            | ✅                                                                 | ✅                                                                 | ❌                                                                 |
| 导入聊天记录文件                   | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 支持个人WhatsApp账户               | ✅                                                                 | ✅                                                                 | ❌ （仅限企业账户）                                                                 |
| 外部依赖                      | **无**                                                                 | 需要Go二进制文件及Maton API密钥         | 需要API密钥和账户                         |

---

## 消息记录与搜索（v1.2.0+）

OpenClaw现在将所有WhatsApp消息存储在本地SQLite数据库中，并支持全文本搜索（FTS5格式）。这样您再也不会丢失任何聊天记录。

### 工作原理

- **实时捕获**：每条新消息都会自动保存
- **历史记录导入**：可以从WhatsApp聊天记录文件批量导入消息
- **全文本搜索**：可以根据内容、发送者或聊天记录内容搜索任何消息

### 搜索聊天记录

可以使用`whatsapp_history`工具（该工具会自动应用于您的代理）：

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

### 导入历史记录

WhatsApp不通过API提供无限量的历史记录。要获取旧消息，请按照以下步骤操作：
1. **从手机导出聊天记录**：进入设置 → 聊天记录 → 导出聊天记录 → 选择“不包含媒体文件”
2. **将导出的.txt文件保存在可访问的位置**
3. **导入聊天记录**：
```
whatsapp_history action=import path="/path/to/exports"
```

或者，您可以导入单个聊天记录：

```
whatsapp_history action=import path="/path/to/chat.txt" chatName="Family Group"
```

### 数据库位置

数据库使用WAL模式的SQLite文件，支持并发访问。

### 使用场景示例

- “我之前跟Sarah说了关于会议什么？”
- “找出所有提到‘截止日期’的消息”
- “向工作群组展示我最近发的消息”
- “John什么时候提到季度报告的？”

代理可以通过搜索您的完整WhatsApp聊天记录来回答这些问题。

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

代理会自动读取昨天的聊天记录，并在早上生成摘要，无需人工操作。

---

## 下载和转录语音消息（v1.3.0+）

聊天记录数据库会将语音消息的原始数据（包括媒体文件）存储在`raw_json`字段中。这意味着您可以下载并解密任何语音消息、图片或视频文件——即使是来自群组聊天的消息。

### 工作原理

WhatsApp会对媒体文件使用唯一的密钥进行加密。该密钥存储在消息的原始数据中，Baileys会负责解密操作。

### 下载语音消息

1. 使用`whatsapp_history`工具找到对应的消息ID：
```
whatsapp_history action=search chat="GROUP_JID" sender="PersonName" limit=10
```

查找类型为“voice”或“audio”的消息。
2. 使用Node.js脚本下载音频文件（脚本需从OpenClaw源代码目录运行）：
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

其他类型的媒体文件下载方法类似，只需修改相应的字段和内容类型：

| 媒体类型        | 原始数据字段            | 对应的存储字段            |
| -------------- | ---------------------- | --------------------------- |
| 语音/音频       | `audioMessage`        | `"audio"`            |
| 图片           | `imageMessage`        | `"image"`            |
| 视频           | `videoMessage`        | `"video"`            |
| 文档           | `documentMessage`       | `"document"`          |
| 贴纸           | `stickerMessage`        | `"sticker"`          |

### 重要提示

- **媒体文件的URL是临时的**：请尽快下载，否则Baileys会尝试重新请求（这需要保持socket连接处于活跃状态）。
- **建议保持WhatsApp连接**：如果媒体文件的URL已过期，Baileys需要通过socket来获取新的URL。
- **数据库路径**：`~/.openclaw/data/whatsapp-history.db`
- **所需文件**：下载脚本需要`@whiskeysockets/baileys`和`better-sqlite3`库，这两个文件都位于OpenClaw的源代码目录中。

### 使用场景示例

- 转录群组聊天中的语音消息
- 保存群组中分享的重要图片/文档
- 生成语音聊天记录的文本版本
- 分析您不懂的语言的语音消息（Whisper支持99种语言）

---

## 完整聊天记录同步（v1.5.0+）

您可以将整个WhatsApp聊天记录（数月或数年的消息）同步到本地数据库。这需要重新连接您的WhatsApp设备，触发WhatsApp的初始同步操作（类似于首次连接设备时的同步过程）。

### 原因

Baileys中的按需获取聊天记录的功能（`fetchMessageHistory`）存在问题（详见[Issue #1934](https://github.com/WhiskeySockets/Baileys/issues/1934)。因此，只能通过初始设备连接来获取旧消息。此功能可自动完成整个同步过程。

### 工作原理

### 设置步骤

1. 将`whatsapp-resync`插件安装到`~/.openclaw/extensions/whatsapp-resync/`目录。
2. 在`openclaw.json`配置文件中添加相关设置：
```json
{
  "plugins": [{ "name": "whatsapp-resync", "path": "~/.openclaw/extensions/whatsapp-resync" }]
}
```

3. 重启OpenClaw代理。

### API端点

| 端点                        | 方法                  | 描述                                                                                          |
| ------------------------------ | ---------------------- | --------------------------------------------------------------------------- |
| `/api/whatsapp/resync`         | POST    | 触发同步操作：备份认证信息、清除缓存数据、关闭监听器                                                                 |
| `/api/whatsapp/resync/restore` | POST    | 从备份中恢复数据（在出现问题时使用）                                                                 |

### 触发同步操作

```bash
curl -X POST http://localhost:3120/api/whatsapp/resync
```

### 完成同步操作

1. 打开Webchat界面 → 选择“Channels”选项卡 → 用手机扫描二维码
2. 在手机上进入WhatsApp设置 → 选择“Linked Devices” → 选择您的设备
3. 扫描二维码
4. 等待同步完成（根据聊天记录的数量，可能需要1-5分钟）

### 验证同步结果

```
whatsapp_history action=stats
```

成功的同步操作通常会下载数千条消息（可能涵盖数月或数年的记录）。

### 从备份中恢复数据

如果系统出现故障，可以恢复之前的认证状态：

```bash
# Restore latest backup
curl -X POST http://localhost:3120/api/whatsapp/resync/restore

# Restore specific backup
curl -X POST http://localhost:3120/api/whatsapp/resync/restore \
  -H 'Content-Type: application/json' \
  -d '{"backupDir": "/path/to/backup"}'
```

### 安全性

- **自动备份**：在删除数据前会备份认证信息
- **无数据丢失**：仅清除认证状态；现有消息会保留在数据库中
- **恢复操作简单**：只需一键即可恢复到之前的状态
- **不影响WhatsApp账户**：仅恢复连接状态，不会影响账户本身的数据

### 实际测试结果

在测试中，一次同步操作恢复了：
- 17,609条消息（之前仅恢复3,242条）
- 1,229个聊天记录
- 4,077个联系人
- 涉及**3年多的聊天记录**（最远可追溯到2022年9月）

---

## 离线消息恢复（v1.6.0+）

当OpenClaw代理断开连接（重启、崩溃等）时，期间发送的消息不会丢失——这些消息会被WhatsApp保存并在重新连接时自动传输。OpenClaw会自动恢复这些消息。

### 工作原理

1. 代理重新连接到WhatsApp服务器
2. WhatsApp会将丢失的消息作为“append”类型的事件发送
3. OpenClaw会检查每条消息的时间戳，判断是否在恢复窗口范围内（默认窗口时间为6小时）
4. 在窗口范围内的消息会按照正常流程处理
5. 超出窗口时间的消息会被标记为已读取状态，但不会被处理

### 注意事项

- **代理断开连接几分钟或几小时？** 所有消息都会自动恢复
- **自我聊天消息**（代理与自己发送的消息）也会被恢复
- **访问控制仍然有效**：未经授权的发送者仍会被过滤
- **消息不会重复处理**：避免重复处理相同的消息

### 配置设置

恢复窗口的默认时间为6小时。您可以通过`offlineRecoveryMs`参数进行调整。将其设置为0可完全禁用恢复功能。

### 智能恢复机制

恢复的消息会标记为`[OFFLINE RECOVERY]`，以便代理知道这些消息来自恢复队列。系统会先读取所有恢复的消息，然后提供以下提示：
- “我在离线期间，您发送了X条消息”
- “您是否希望我继续处理Z条消息？”

这样可以避免重复操作、处理过时的请求，以及避免逐条处理恢复的消息带来的混乱。

### 提示

- 如果代理有定时重启计划（例如更新），请确保重启时间较短——恢复窗口内的消息都会被恢复
- 恢复窗口设置较为宽松；大多数代理中断时间较短（通常以秒或分钟计）
- 超出窗口时间的消息仍会保存在数据库中，可通过`whatsapp_history`功能查询

---

## 语音笔记的转录和处理

现在，语音笔记在处理流程中享有优先权。语音笔记在处理前会被转录，因此`triggerPrefix`规则可以正常应用于语音消息。

### 工作原理

1. 下载并保存音频文件到`~/.openclaw/media/inbound/`
2. 使用配置的音频转录工具（默认使用OpenAI的Whisper）进行转录
3. 检查转录后的文本是否以`triggerPrefix`开头（例如“Jarvis”）
4. 如果匹配，则将转录后的文本替换原始的`<media:audio>`字段，并将其传递给代理

### 配置设置

在`openclaw.json`中启用音频转录功能：

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true
      }
    }
  }
}
```

### 前缀匹配规则

`triggerPrefix`规则同样适用于语音消息：
- “Jarvis, what time is it?” → 会触发转录
- “Hey Jarvis, what time is it?” → 不会触发转录
- “Tell Jarvis to...” → 也不会触发转录

### 防止重复处理

机器人发送的语音回复（通过TTS生成）会根据消息ID进行过滤，从而避免机器人回复自己的语音消息。

---

## 金属音效的语音回复

现在，机器人可以使用本地的TTS引擎（`sherpa-onnx`）生成带有金属音效的语音回复。无需使用云服务，且无延迟。

### 设置步骤

1. 安装`sherpa-onnx` TTS引擎：
   ```bash
   sudo install sherpa-onnx-tts
   ```
2. 创建`jarvis-wa-tts`脚本：
   ```bash
   chmod +x ~/.local/bin/jarvis-wa-tts
   ```
3. 在代理中启用该脚本：
   ```bash
   chmod +x ~/.local/bin/jarvis-wa-tts
   ```

### 在代理中的使用方式

### 效果调整

- **速度**：提高2倍
- **音调**：提升5%
- **音效处理**：添加金属音效
- **回声效果**：设置15毫秒的延迟
- **均衡器**：提升高频音段200Hz

---

## 故障排除

### 家人/朋友发送的消息无法到达代理

**问题**：您已将某人添加到`groupAllowFrom`列表中，但他们发送的私人消息无法被代理接收。

**解决方法**：同时将该人添加到`allowFrom`列表中。`groupAllowFrom`列表仅控制群组内的消息发送，不控制私人消息的发送。

```json
{
  "allowFrom": ["+34612345678", "+14155551234"],
  "groupAllowFrom": ["+34612345678", "+14155551234"]
}
```

### 无法区分私人消息中的发送者

**问题**：私人消息中的所有消息都显示相同的发送者号码。

**原因**：在OpenClaw 2026.2.1版本之前，私人消息中显示的是发送者的`chat ID`（即电话号码），而非实际发送者的名称。

**解决方法**：升级到最新版本的OpenClaw。现在代理可以正确区分您发送的消息和对方发送的消息。

### 语音笔记在WhatsApp中无法播放

**问题**：虽然成功上传了音频文件，但无法播放。

**解决方法**：请使用OGG/Opus格式的音频文件，并在发送时设置`asVoice=true`参数。

---

## 架构说明

**WhatsApp Ultimate**完全依赖OpenClaw的内部功能，无需任何外部服务或Docker、CLI工具。所有功能都通过直接协议集成实现。

---

## 致谢

该技能由**Oscar Serra**开发，Claude（Anthropic团队）提供了协助。

**这是一个让WhatsApp功能恢复正常使用的技能。**

---

## 许可证

MIT许可证——属于OpenClaw项目的一部分

---

## 链接

- OpenClaw分支：https://github.com/globalcaos/clawdbot-moltbot-openclaw
- Baileys：https://github.com/WhiskeySockets/Baileys
- ClawHub：https://clawhub.com