---
name: whatsapp-ultimate
version: 1.4.0
version: 3.6.0
description: "WhatsApp skill with a 3-rule security gate. Your agent speaks only when spoken to — in the right chat, by the right person."
metadata:
  openclaw:
    emoji: "📱"
    requires:
      channels: ["whatsapp"]
---

# WhatsApp Ultimate

**WhatsApp 的所有功能，你的 AI 代理也能实现。**

本文档记录了通过 OpenClaw 的原生通道集成可使用的所有 WhatsApp 功能。无需外部 Docker 服务，也无需 CLI 包装器——只需通过 Baileys 直接使用 WhatsApp Web 协议即可。

---

## 先决条件

- 已配置 WhatsApp 通道的 OpenClaw
- 通过 QR 码链接了 WhatsApp 账户（`openclaw whatsapp login`）

---

## 功能概览

| 类别 | 功能 |
|----------|----------|
| **消息发送** | 文本、媒体文件、投票、贴纸、语音笔记、GIF 图片 |
| **互动** | 回应、回复/引用、编辑、取消发送 |
| **群组** | 创建群组、重命名群组、设置群组图标、编辑群组描述、管理群组成员、邀请成员 |

**总计：22 个独立操作**

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
支持的格式：JPG、PNG、GIF、MP4、PDF、DOC 等。

### 发送投票
```
message action=poll channel=whatsapp to="+34612345678" pollQuestion="What time?" pollOption=["3pm", "4pm", "5pm"]
```

### 发送贴纸
```
message action=sticker channel=whatsapp to="+34612345678" filePath=/path/to/sticker.webp
```
贴纸必须是 WebP 格式，理想尺寸为 512x512 像素。

### 发送语音笔记
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```
**重要提示：** 使用 OGG/Opus 格式的语音笔记。MP3 格式可能无法在 WhatsApp 中正常播放。

### 发送 GIF 图片
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```
请先将 GIF 图片转换为 MP4 格式（WhatsApp 要求如此）：
```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4 -y
```

---

## 互动

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

### 编辑消息（仅限自己发送的消息）
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

### 提升群组管理员权限
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降低群组管理员权限
```
message action=demoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 离开群组
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

### 获取群组信息
```
message action=getGroupInfo channel=whatsapp groupJid="123456789@g.us"
```
返回内容：群组名称、描述、成员列表、管理员信息、创建日期。

---

## JID 格式

WhatsApp 内部使用 JID（Jabber ID）：

| 类型 | 格式 | 例子 |
|------|--------|---------|
| 个人 | `<数字>@s.whatsapp.net` | `34612345678@s.whatsapp.net` |
| 群组 | `<id>@g.us` | `123456789012345678@g.us` |

当使用 `to=` 与电话号码关联时，OpenClaw 会自动将其转换为 JID 格式。

---

## 提示

### 语音笔记
始终使用 OGG/Opus 格式：
```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

### 贴纸
将图片转换为 WebP 格式的贴纸：
```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

### 回复消息（ackMessage）
收到新消息时发送即时文本消息——该功能在消息传递到模型进行处理之前触发：
```json
{
  "channels": {
    "whatsapp": {
      "ackMessage": {
        "text": "⚡",
        "direct": true,
        "group": "never"
      }
    }
  }
}
```
| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `text` | 字符串 | `""` | 要发送的文本（为空表示禁用） |
| `direct` | 布尔值 | `true` | 在私信中发送 |
| `group` | `"always"` / `"mentions"` / `"never"` | `"never"` | 在群组消息中发送 |

这与 `ackReaction`（发送表情符号）不同。`ackMessage` 会发送一条独立的消息提示——即使在 WhatsApp Web 中看不到表情符号时也能显示。

### 速率限制
WhatsApp 有反垃圾信息机制。请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与你联系的人发送消息

### 消息 ID
要回复、编辑或取消发送消息，你需要消息的 ID。收到的消息中包含该 ID；你发送的消息也会附带 ID。

---

## 与其他功能的比较

| 功能 | WhatsApp Ultimate | wacli | whatsapp-automation | gif-whatsapp |
|---------|-------------------|-------|---------------------|--------------|
| 原生集成 | ✅ | ❌（CLI） | ❌（Docker） | N/A |
| 发送文本 | ✅ | ✅ | ❌ | ❌ |
| 发送媒体文件 | ✅ | ✅ | ❌ | ❌ |
| 投票 | ✅ | ❌ | ❌ | ❌ |
| 贴纸 | ✅ | ❌ | ❌ | ❌ |
| 语音笔记 | ✅ | ❌ | ❌ | ❌ |
| GIF 图片 | ✅ | ❌ | ❌ | ✅ |
| 回应 | ✅ | ❌ | ❌ | ❌ |
| 回复/引用 | ✅ | ❌ | ❌ | ❌ |
| 编辑 | ✅ | ❌ | ❌ | ❌ |
| 取消发送 | ✅ | ❌ | ❌ | ❌ |
| 创建群组 | ✅ | ❌ | ❌ | ❌ |
| 群组管理 | ✅（全面支持） | ❌ | ❌ | ❌ |
| 接收消息 | ✅ | ✅ | ✅ | ❌ |
| 双向聊天 | ✅ | ❌ | ❌ | ❌ |
| 外部依赖 | 无 | 需 Go 二进制文件 | 需 Docker 和 WAHA | 需 ffmpeg |

---

## 媒体文件下载（从聊天记录中）

可以从 WhatsApp 的聊天记录中下载图片、视频、文档和音频文件。使用 Baileys 的 `downloadContentFromMessage` 函数，并从 `raw_json` 中获取媒体文件的键——无需保持活跃的连接。

### 列出最近发送的媒体文件
```bash
cd ~/src/tinkerclaw && npx tsx src/whatsapp-history/download-media.ts --list-media [--since YYYY-MM-DD] [--chat <jid|name>] [--limit N]
```

### 按消息 ID 下载文件
```bash
cd ~/src/tinkerclaw && npx tsx src/whatsapp-history/download-media.ts --id <messageId> [--out <directory>]
```
默认输出路径：`~/.openclaw/workspace/data/wa-media/<messageId>.<ext>`

### 注意：
- WhatsApp 服务器上的媒体文件链接大约两周后会失效，请尽快下载。
- 支持下载的文件类型：图片、视频、文档、音频、贴纸、语音笔记。
- 系统会自动根据文件的 MIME 类型判断文件格式。
- `messages` 表中的 `raw_json` 列必须包含原始的 Baileys 协议数据（仅适用于实时捕获的消息，不包括导入的.txt 文件）。

---

### 3.5.1 版本更新

- **新增功能：** 从聊天记录中下载媒体文件——`download-media.ts` 脚本可以从存储的 `raw_json` 中提取媒体文件的键，并直接从 WhatsApp 的 CDN 下载/解压文件，无需保持活跃的连接。

### 3.5.0 版本更新

- **新增功能：** `ackMessage**——在消息到达时立即发送可配置的文本消息（例如 ⚡），在模型处理之前触发。该功能与 `ackReaction`（发送表情符号）的触发速度相同，有助于在 WhatsApp Web 中区分机器人的回复和用户的消息（因为机器人回复可能不会显示表情符号）。

### 3.4.0 版本更新

- **修复问题：** 聊天搜索现在可以识别 LID/JID 别名——通过聊天名称搜索时，可以找到使用 `@lid` 或 `@s.whatsapp.net` 格式的消息。
- **新增功能：** `resolveChatJids()` 函数可以关联聊天记录、联系人和消息表，以查找指定聊天的所有 JID 别名。
- **改进：** 如果无法解析 JID，系统会回退到原有的搜索方式，避免功能失效。

### 3.0.0 版本更新

**无需外部服务，无需 Docker，也无需 CLI 工具。直接使用 WhatsApp 的原生协议进行集成。**

---

## 许可证

MIT 许可证——属于 OpenClaw 项目的一部分。

## 适用工具

- [outlook-hack](https://clawhub.com/globalcaos/outlook-hack) —— 与 Outlook 集成：读取所有聊天记录，可起草回复，但不会自动发送消息。
- [teams-hack](https://clawhub.com/globalcaos/teams-hack) —— 与 Teams 集成，采用相同的浏览器中继机制。
- [agent-superpowers](https://clawhub.com/globalcaos/agent-superpowers) —— 用于管理这些聊天通道的代理程序。

👉 **访问项目仓库：https://github.com/globalcaos/tinkerclaw**

**欢迎克隆、修改或根据需要进一步开发这个项目。**