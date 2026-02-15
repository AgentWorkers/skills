---
name: whatsapp-ultimate
version: 1.8.1
description: "**OpenClaw代理的完整WhatsApp集成功能：**  
- 支持发送消息、媒体文件、投票、贴纸、语音笔记以及各种表情（reaction）和回复。  
- 支持使用全文搜索功能（SQLite + FTS5）查询聊天记录。  
- 可下载并转录语音消息。  
- 支持导入导出的聊天数据。  
- 全部聊天记录可重新同步。  

**新功能：**  
- **“思考中”表情（Thinking Reaction）**：在群组聊天中显示用户正在思考的进度指示器（这是对WhatsApp在链接设备上显示的错误打字提示的临时解决方案）。  
- **所有者语音消息**：所有者发送的语音消息会绕过前缀过滤规则。  

**优势：**  
- 100%原生集成，无需使用Docker或任何外部工具。  
- 可与OpenClaw内置的WhatsApp通道同时使用。  

**主要功能说明：**  
- **消息发送**：支持发送各种类型的数据（文本、图片、视频、音频等）。  
- **媒体文件**：支持上传和接收多媒体文件。  
- **投票**：允许用户在聊天中发起投票并查看结果。  
- **贴纸**：支持使用WhatsApp内置的贴纸功能。  
- **语音笔记**：支持录制和分享语音消息。  
- **表情（Reaction）**：提供丰富的表情选项，增强聊天互动性。  
- **聊天历史搜索**：支持通过全文搜索快速查找聊天记录。  
- **数据同步**：所有聊天数据均可自动同步到本地和云端。  

**技术实现：**  
- 使用SQLite和FTS5（Full-Text Search）技术实现高效的全文搜索功能。  
- 支持跨设备同步聊天记录。  
- 通过原生Bailey库处理语音消息，确保低延迟和高可靠性。  

**适用场景：**  
- 适用于需要集成WhatsApp功能的自动化系统或聊天机器人。  

**更多信息：**  
- 详情请参阅[OpenClaw官方文档](https://docs.openclaw.io/)。"
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

**通过您的AI代理发送消息、媒体文件、进行投票、录制语音笔记，以及管理群组——所有这些功能都无需离开您的设备。**您可以即时搜索整个WhatsApp聊天记录。

这是OpenClaw中最全面的WhatsApp集成技能。它支持原生Baileys集成，无需使用Docker、CLI工具或外部服务，只需连接即可开始使用。

---

## 先决条件

- 已配置WhatsApp通道的OpenClaw
- 通过二维码将WhatsApp账户关联到OpenClaw（使用`openclaw whatsapp login`命令）

---

## 功能概览

| 功能类别          | 具体功能                                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **消息发送**        | 支持文本、媒体文件、投票、贴纸、语音笔记和GIF文件发送                                                                                   |
| **互动**          | 支持回复/引用消息、编辑或取消发送消息                                                                                   |
| **群组管理**        | 创建群组、重命名群组、设置群组图标和描述、管理群组成员、任命管理员以及生成群组邀请链接         |
| **进度显示**        | 在群组聊天中显示“🤔”进度指示器（表示消息正在处理中）                                                                                   |
| **媒体文件过滤**      | 群组中的语音/媒体消息可绕过预设的前缀过滤                                                                                   |
| **聊天记录**        | 使用持久化的SQLite数据库存储聊天记录，支持FTS5全文本搜索；支持导入聊天记录文件           |
| **数据同步**        | 可通过重新连接实现聊天记录的完全同步；支持自动备份和恢复                                                                                   |

**总计：24项独立功能 + 可搜索的聊天记录**

---

## 🤔 进度指示器（“🤔 Thinking Reaction”）

**问题：** 链接WhatsApp设备的应用程序（如Baileys、Web API）无法在群组聊天中显示“正在输入...”的提示。这是WhatsApp服务器端的限制——协议正确地发送了`chatstate` XML节点，但WhatsApp服务器不会将输入状态传递给群组成员。该问题已在[Baileys #866](https://github.com/WhiskeySockets/Baileys/issues/866)中得到确认。

**解决方案：** 当代理开始处理消息时，会立即在原始消息上显示“🤔”提示。回复准备好后，该提示会自动消失。这为用户提供了即时的视觉反馈，让他们知道代理正在工作，而无需猜测消息是否已成功发送。

**工作原理：**
1. 消息到达 → 代理在原始消息上显示“🤔”提示（耗时<100毫秒）
2. 代理处理消息（使用工具、进行计算或调用API等）
3. 回复发送 → “🤔”提示自动消失

**适用范围：** 群组聊天 ✅ | 私人消息 ✅ | 所有类型的聊天

这是**唯一一个**解决了“输入提示不可见”问题的WhatsApp集成方案。其他WhatsApp集成方案在代理处理消息时，用户会看到长时间的沉默。

---

## 群组所有者的语音/媒体文件过滤

现在，机器人所有者的语音消息和媒体文件可以绕过群组中的`triggerPrefix`过滤规则。例如，如果群组中发送的语音笔记前缀为“Jarvis”，系统之前会忽略该消息。现在，这些消息会自动被转发给代理。

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

支持的格式：JPG、PNG、GIF、MP4、PDF、DOC等

### 发送投票
```
message action=poll channel=whatsapp to="+34612345678" pollQuestion="What time?" pollOption=["3pm", "4pm", "5pm"]
```

### 发送贴纸
```
message action=sticker channel=whatsapp to="+34612345678" filePath=/path/to/sticker.webp
```

贴纸格式必须为WebP，推荐尺寸为512x512像素

### 发送语音笔记
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```

**重要提示：** 使用OGG/Opus格式发送语音笔记。MP3格式可能无法正常播放

### 发送GIF文件
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```

**注意：** 需先将GIF文件转换为MP4格式（WhatsApp要求如此）：
```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4 -y
```

---

## 互动功能

### 添加反应表情
```
message action=react channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123" emoji="🚀"
```

### 删除反应表情
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

### 删除群组成员
```
message action=removeParticipant channel=whatsapp groupId="123456789@g.us" participant="+34612345678"
```

### 提升成员为管理员
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降级成员为普通成员
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

返回信息包括：群组名称、描述、成员列表和管理员列表

---

## 访问控制

### 私人消息政策

在`openclaw.json`中配置谁可以发送私人消息：

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
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `"open"`          | 任何人都可以发送私人消息                                                                                   |
| `"allowlist"`       | 只有`allowFrom`列表中的号码才能发送私人消息                                                                                   |
| `"pairing"`        | 未知发件人会收到配对代码提示                                                                                   |
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
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `"open"`          | 回应群组中的提及消息                                                                                   |
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

允许您与自己进行聊天（“Note to Self”模式），以便与代理互动

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

---

## JID格式

WhatsApp内部使用JID（Jabber IDs）：

| 类型            | 格式                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 个人用户         | `<数字>@s.whatsapp.net`                                                                                   |
| 群组用户         | `<id>@g.us`                                                                                   |

当使用`to=`与电话号码关联时，OpenClaw会自动将电话号码转换为JID格式。

---

## 提示

### 查找群组名称

聊天记录数据库中`chat_name`字段可能为`NULL`。要获取群组的显示名称，可以使用以下方法：

```
message action=getGroupInfo channel=whatsapp target="<group-jid>"
```

返回信息包括：群组名称、描述以及包含管理员角色的完整成员列表。

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

### 优化私人消息显示（推荐配置）

WhatsApp适用于小屏幕设备。只需发送**最终回复**，避免发送工具操作信息、中间状态或调试输出。建议在OpenClaw配置中关闭详细日志显示：
```json
{
  "agents": {
    "defaults": {
      "verboseDefault": "off"
    }
  }
}
```

这样可以防止`[openclaw] 🛠️ Exec: ...`、`[openclaw] 📖 Read`等日志信息在聊天中重复显示。

**语音回复中应包含文字记录**：当用户发送语音消息时，回复中应包含文字转录内容，以便对方确认消息内容。

### 避免违规行为

WhatsApp有反垃圾邮件机制。请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与您联系过的人发送消息

### 消息ID

要回复、编辑或取消发送消息，您需要知道消息的ID。接收到的消息中包含消息ID；您发送的消息的响应中也包含消息ID。

---

## 何时使用此技能

当您的代理需要执行以下操作时，可以使用`whatsapp-ultimate`技能：
- 通过WhatsApp发送文本、图片、视频、文档或语音笔记
- 在群组聊天中创建和管理投票
- 用表情符号回复消息、引用或编辑/取消发送消息
- 创建群组、管理群组成员、获取群组邀请链接
- 根据关键词、发送者或日期搜索过去的WhatsApp聊天记录
- 导入并索引WhatsApp聊天记录文件（.txt格式）
- 获取群组元数据（名称、描述、成员列表）
- 自动生成群组聊天活动的每日摘要

## 与其他技能的比较

| 功能                | whatsapp-ultimate                                                                 | wacli                                                                 | whatsapp-business                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 原生集成            | ✅（无需任何外部依赖）                                                                 | ❌（需要Go CLI二进制文件或外部API密钥）                                                                 |
| 发送文本            | ✅                                                                 | ✅                                                                 | ✅                                                                 |
| 发送媒体文件          | ✅                                                                 | ✅（仅支持特定文件格式）                                                                 | ✅                                                                 |
| 进行投票            | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 使用贴纸              | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 录制语音笔记          | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 支持GIF文件          | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 添加反应表情          | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 回复/引用消息          | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 编辑消息            | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 取消发送/删除消息        | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 群组管理            | ✅（包括创建、重命名、设置图标、描述、管理成员、任命管理员等）                                                                 | ❌                                                                 | ❌                                                                 |
| 获取群组信息          | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 双向聊天            | ✅                                                                 | ❌                                                                 | ✅（需要Webhook接口）                                                                 |
| 查看聊天记录          | ✅（使用SQLite和FTS5技术）                                                                 | ✅                                                                 | ❌                                                                 |
| 导入聊天记录文件        | ✅                                                                 | ❌                                                                 | ❌                                                                 |
| 支持个人WhatsApp账户     | ✅                                                                 | ✅（仅限企业版）                                                                 | ❌                                                                 |
| 外部依赖            | **无**                                                                 | ✅（需要Go二进制文件和Maton API密钥）                                                                 |

---

## 消息记录与搜索（v1.2.0及以上版本）

OpenClaw现在将所有WhatsApp消息存储在本地SQLite数据库中，并支持全文本搜索（FTS5算法）。这样您再也不会丢失任何聊天记录。

### 工作原理

- **实时捕获**：每条新消息都会自动保存
- **历史记录导入**：可以从WhatsApp聊天记录文件中批量导入消息
- **全文本搜索**：可以根据内容、发送者或聊天记录类型搜索任何消息

### 搜索聊天记录

可以使用`whatsapp_history`工具（该工具会自动集成到您的代理中）：

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

WhatsApp并未通过API提供无限量的历史记录。要获取旧消息，请按照以下步骤操作：
1. 从手机设置中导出聊天记录
2. 将导出的.txt文件保存在可访问的位置
3. 使用````
whatsapp_history action=import path="/path/to/exports"
````命令导入这些文件

### 数据库位置

聊天记录存储在采用WAL模式的SQLite数据库中，支持并发访问。

### 使用场景示例

- “我之前跟Sarah说了关于会议什么？”
- “找到所有提到‘deadline’的消息”
- “向工作群组展示我最近发送的消息”
- “John什么时候提到季度报告的？”

代理可以通过搜索您的完整WhatsApp聊天记录来回答这些问题。

### 自动生成每日摘要（基于Cron任务）

您可以设置每日Cron任务，让代理自动汇总群组中的活跃聊天记录：

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

代理会在每天启动时自动读取昨天的聊天记录，并生成每日摘要，无需人工操作。

---

## 下载与转录语音消息（v1.3.0及以上版本）

聊天记录数据库会存储原始的语音消息数据（包括媒体文件的相关信息）。这意味着您可以下载并解密任何语音消息、图片或视频文件——即使这些消息来自群组聊天或其他人发送的文件。

### 工作原理

- 使用`whatsapp_history`命令查找语音消息的ID：
  ```
whatsapp_history action=search chat="GROUP_JID" sender="PersonName" limit=10
```

  查找类型为“voice”或“audio”的消息
- 使用Node.js脚本下载音频文件（需要在OpenClaw源代码目录中运行）
- 使用`Whisper`或其他语音转文字工具进行转录：
  ```bash
ffmpeg -i /tmp/voice-msg.ogg -ar 16000 -ac 1 /tmp/voice-msg.wav -y
whisper /tmp/voice-msg.wav --model base --language es --output_format txt --output_dir /tmp/
cat /tmp/voice-msg.txt
```

### 下载其他类型的媒体文件

其他类型的媒体文件下载规则类似，只需根据对应的字段和内容类型进行操作：

| 媒体类型            | 对应的Proto字段            | 内容类型                                                                                   |
| --------------------------- | ----------------------------- | ------------------------------------------------------------------------- |
| 语音/音频           | `audioMessage`           | `"audio"`                                                                                   |
| 图片               | `imageMessage`           | `"image"`                                                                                   |
| 视频               | `videoMessage`           | `"video"`                                                                                   |
| 文档               | `documentMessage`          | `"document"`                                                                                   |
| 贴纸               | `stickerMessage`          | `"sticker"`                                                                                   |

### 重要提示

- **媒体文件链接的有效期**：WhatsApp提供的媒体文件链接是临时的。请尽快下载，否则Baileys会尝试重新请求链接（这需要保持socket连接激活）。
- **建议保持WhatsApp连接状态**：如果媒体文件链接失效，Baileys需要通过socket重新请求链接。保持WhatsApp连接状态可确保下载成功。
- **数据库路径**：`~/.openclaw/data/whatsapp-history.db`
- **所需文件**：下载脚本需要`@whiskeysockets/baileys`和`better-sqlite3`库，这两个文件都包含在OpenClaw的源代码目录中。

### 使用场景示例

- 转录群组聊天中的语音消息
- 保存群组中分享的重要图片/文档
- 生成语音聊天记录的文字版本
- 分析您不熟悉语言的语音消息（Whisper支持99种语言）

---

## 完整聊天记录同步（v1.5.0及以上版本）

您可以将数月甚至数年的WhatsApp聊天记录同步到本地数据库。该功能通过重新连接您的WhatsApp设备来触发同步操作（类似于首次连接设备时的同步过程）。

### 原因

Baileys中的按需获取聊天记录的功能（`fetchMessageHistory`）存在问题（详见[Issue #1934](https://github.com/WhiskeySockets/Baileys/issues/1934)）。因此，只能通过初始设备连接来获取旧消息。此功能可自动完成整个同步过程。

### 工作原理

- 安装`whatsapp-resync`插件：
  1. 将插件复制到`~/.openclaw/extensions/whatsapp-resync/`
  2. 在`openclaw.json`配置文件中添加相关设置：
  ```json
{
  "plugins": [{ "name": "whatsapp-resync", "path": "~/.openclaw/extensions/whatsapp-resync" }]
}
```

- 启动代理后，可以通过以下API端点触发同步操作：
  - `/api/whatsapp/resync`（POST请求）：备份认证信息、清除缓存数据、关闭监听器
  - `/api/whatsapp/resync/restore`（POST请求）：在出现问题时从备份中恢复数据

### 触发同步操作

```bash
curl -X POST http://localhost:3120/api/whatsapp/resync
```

### 完成同步过程

- 打开Webchat界面，选择“Channels”选项卡，然后用手机扫描二维码
- 在手机上进入WhatsApp设置，选择“Linked Devices”，然后扫描二维码
- 等待同步完成（根据聊天记录数量，同步时间可能为1-5分钟）

### 验证同步结果

同步成功后，通常会下载大量消息（可能涵盖数月甚至数年的聊天记录）。

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

### 安全性措施

- **自动备份**：在删除数据前会备份认证信息
- **无数据丢失**：仅清除认证状态；现有消息会保留在数据库中
- **一键恢复**：可以轻松恢复到之前的状态
- **非破坏性操作**：您的WhatsApp账户不会受到影响；仅恢复与设备关联的聊天记录

### 实际应用效果

在测试中，一次同步操作可恢复：
- 17,609条消息（之前仅恢复3,242条）
- 1,229个聊天记录
- 4,077个联系人
- 涉及**3年以上的聊天记录**（最远可恢复到2022年9月的记录）

---

## 离线消息恢复（v1.6.0及以上版本）

当代理连接中断（重启、崩溃等）时，期间发送的消息不会丢失。OpenClaw会自动恢复这些消息：

- 代理重新连接WhatsApp后，会以“append”类型的事件形式恢复这些消息
- OpenClaw会检查每条消息的时间戳，确保消息在指定时间窗口内发送（默认时间窗口为6小时）
- 在指定时间窗口内的消息会通过正常的访问控制流程进行处理
- 超出时间窗口的消息会被标记为已读，但不会被再次处理

### 注意事项

- **配置选项**：可以通过`offlineRecoveryMs`参数调整恢复窗口的时间。设置为0可完全禁用恢复功能
- 恢复窗口默认设置为6小时；如果需要，可以将其调整为更短的时间
- 恢复的消息会标记为“[OFFLINE RECOVERY]”，以便代理知道这些消息是离线期间发送的
- 恢复操作会先读取所有恢复的消息，然后提供摘要信息
- 之后会询问用户是否继续处理这些消息，避免重复操作或处理过时的请求

### 配置建议

- 如果代理有定时重启计划（例如更新），请确保重启时间较短（通常在6小时内）
- 恢复窗口设置较宽泛；大多数情况下，代理中断时间较短（通常在几秒到几分钟内）
- 超出时间窗口的消息仍会保存在数据库中，可以通过`whatsapp_history`命令查询

## 语音笔记的转录与前缀匹配（v1.7.0及以上版本）

现在，语音笔记在处理流程中享有与文本消息相同的优先级。语音笔记在发送前会被自动转录，因此`triggerPrefix`规则同样适用于语音消息。

### 工作原理

- 音频文件会被下载并保存到`~/.openclaw/media/inbound/`目录
- 使用配置的音频转录工具（默认使用OpenAI的Whisper）进行转录
- 转录后的文本会与`triggerPrefix`进行匹配（例如，前缀必须以“Jarvis”开头）
- 如果前缀匹配，转录后的文本会替换原始的`<media:audio>`字段，并进入代理的处理流程

### 配置说明

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

语音消息也遵循与文本消息相同的`triggerPrefix`规则：
- “Jarvis, what time is it?” → 会触发转录
- “Hey Jarvis, what time is it?” → 不会触发转录
- “Tell Jarvis to...” → 也不会触发转录

### 防止重复处理

机器人发送的语音回复（通过TTS生成）会通过消息ID进行识别，并在处理过程中被自动过滤掉。这可以防止机器人响应自己的语音消息。

---

## 金属音效的语音回复（v1.7.0及以上版本）

现在，机器人可以使用本地TTS引擎（`sherpa-onnx`）生成具有金属音效的语音回复。这种方式无需使用云服务，也不会产生延迟。

### 设置步骤

- 安装`sherpa-onnx` TTS引擎
- 创建`jarvis-wa-tts`脚本
- 使脚本可执行：`chmod +x ~/.local/bin/jarvis-wa-tts`

### 在代理中使用

```bash
# Generate voice note
jarvis-wa-tts "Hello sir, systems nominal." /tmp/reply.ogg

# Send as WhatsApp voice note
message action=send channel=whatsapp target="+1234567890" filePath=/tmp/reply.ogg asVoice=true
```

### 效果设置

- **速度提升**：2倍（`vits-length-scale=0.5`）
- **音调调整**：提高5%
- **音效处理**：添加金属音效
- **回声处理**：设置15毫秒的延迟效果
- **均衡器设置**：提升高频音段200Hz并增强音量6dB

---

## 常见问题与解决方法

### 家人/朋友发送的消息无法到达代理

**问题**：虽然将某人添加到了`groupAllowFrom`列表中，但他们发送的私人消息无法被代理接收。

**解决方法**：同时将该人添加到`allowFrom`列表中。`groupAllowFrom`列表仅控制群组内的消息发送，不控制私人消息的发送。

```json
{
  "allowFrom": ["+34612345678", "+14155551234"],
  "groupAllowFrom": ["+34612345678", "+14155551234"]
}
```

### 无法区分私人消息中的发送者

**问题**：私人消息中的所有消息都显示相同的发送者号码。

**原因**：在OpenClaw 2026.2.1版本之前，私人消息中显示的是聊天ID（对方的电话号码），而非实际发送者的号码。

**解决方法**：升级到最新版本的OpenClaw。现在代理可以正确区分您发送的消息和对方发送的消息。

### 语音笔记在WhatsApp中无法播放

**问题**：虽然成功上传了音频文件，但无法播放。

**解决方法**：请使用OGG/Opus格式录制语音笔记，并在发送时设置`asVoice=true`参数。

---

## 架构说明

- 该技能完全不依赖任何外部服务或Docker，也不需要使用CLI工具，直接通过WhatsApp的原始协议进行集成。

---

## 致谢

该技能由Oscar Serra开发，Claude（Anthropic团队）提供了协助。

“这个技能终于让WhatsApp实现了应有的功能。”

---

## 许可证

该技能基于MIT许可证发布，是OpenClaw项目的一部分。

---

## 链接

- OpenClaw分支仓库：https://github.com/globalcaos/clawdbot-moltbot-openclaw
- Baileys项目：https://github.com/WhiskeySockets/Baileys
- ClawHub平台：https://clawhub.com