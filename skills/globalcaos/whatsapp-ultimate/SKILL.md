---
name: whatsapp-ultimate
version: 3.5.1
description: "这是一个基于 WhatsApp 的技能（skill），它采用了三重安全验证机制。该技能的代理（agent）仅在以下条件下才会响应用户：  
1. 用户在正确的聊天频道中发送消息；  
2. 发消息的用户是被授权与该技能交互的人；  
3. 用户的请求符合预设的规则或条件。  
换句话说，这个技能会确保只有经过身份验证的用户才能与它进行交互，从而保护系统的安全性和隐私性。"
metadata:
  openclaw:
    emoji: "📱"
    requires:
      channels: ["whatsapp"]
---
# WhatsApp Ultimate

**WhatsApp 的所有功能，你的 AI 代理也能实现。**

本文档记录了通过 OpenClaw 的原生通道集成可使用的所有 WhatsApp 功能。无需外部 Docker 服务，也无需 CLI 包装器——只需直接使用 Baileys 协议与 WhatsApp Web 进行交互。

---

## 先决条件

- 已配置 WhatsApp 通道的 OpenClaw
- 通过二维码链接 WhatsApp 账户（`openclaw whatsapp login`）

---

## 功能概述

| 功能类别 | 具体功能 |
|----------|----------|
| **消息发送** | 文本、媒体文件、投票、贴纸、语音笔记、GIF 图片 |
| **互动** | 回应、回复/引用、编辑、取消发送 |
| **群组管理** | 创建群组、重命名群组、设置群组图标、编辑群组描述、管理群组成员、邀请新成员 |

**总计：22 项独立功能**

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
支持的格式：JPG、PNG、GIF、MP4、PDF、DOC 等

### 发送投票
```
message action=poll channel=whatsapp to="+34612345678" pollQuestion="What time?" pollOption=["3pm", "4pm", "5pm"]
```

### 发送贴纸
```
message action=sticker channel=whatsapp to="+34612345678" filePath=/path/to/sticker.webp
```
贴纸格式必须为 WebP，建议尺寸为 512x512 像素

### 发送语音笔记
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```
**注意：** 使用 OGG/Opus 格式的语音笔记。MP3 格式可能无法正常播放

### 发送 GIF 图片
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/animation.mp4 gifPlayback=true
```
发送前请先将 GIF 图片转换为 MP4 格式（WhatsApp 要求如此）：
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

### 提升成员为管理员
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降级成员为普通用户
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

### 获取群组信息
```
message action=getGroupInfo channel=whatsapp groupJid="123456789@g.us"
```
返回信息包括：群组名称、描述、成员列表及管理员信息、创建日期

---

## JID 格式

WhatsApp 内部使用 JID（Jabber ID）：

| 类型 | 格式 | 例子 |
|------|--------|---------|
| 个人账户 | `<数字>@s.whatsapp.net` | `34612345678@s.whatsapp.net` |
| 群组 | `<id>@g.us` | `123456789012345678@g.us` |

使用 `to=` 与电话号码关联时，OpenClaw 会自动将其转换为 JID 格式。

---

## 使用技巧

### 语音笔记
请务必使用 OGG/Opus 格式：
```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

### 贴纸
请将图片转换为 WebP 格式的贴纸：
```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

### 回复消息
收到新消息时，会立即发送一条确认消息——该消息在模型处理之前在网关层被发送：
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
| `text` | 字符串 | `""` | 要发送的确认消息（空值表示禁用） |
| `direct` | 布尔值 | `true` | 是否在私信中发送 |
| `group` | `"always"` / `"mentions"` / `"never"` | 是否在群组聊天中发送 |

这与 `ackReaction`（发送表情符号）不同：`ackMessage` 会发送一条独立的消息，即使在群组聊天中看不到表情符号时也能显示。

### 避免违规行为
WhatsApp 有反垃圾信息机制，请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与你联系的人发送消息

### 消息 ID
要回复、编辑或取消发送消息，需要知道消息的 ID。收到的消息中包含该 ID；自己发送的消息的响应中也包含 ID。

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
| 回应/引用 | ✅ | ❌ | ❌ | ❌ |
| 编辑消息 | ✅ | ❌ | ❌ | ❌ |
| 取消发送 | ✅ | ❌ | ❌ | ❌ |
| 创建群组 | ✅ | ❌ | ❌ | ❌ |
| 群组管理 | ✅（全面支持） | ❌ | ❌ | ❌ |
| 接收消息 | ✅ | ✅ | ✅ | ❌ |
| 双向聊天 | ✅ | ❌ | ❌ | ❌ |
| 外部依赖 | 无 | 需 Go 语言和 Docker | 需 Docker 以及 WAHA 库 | 需 ffmpeg 工具 |

---

### 3.5.0 版本更新

- **新增功能：** `ackMessage`——在收到新消息时立即发送可配置的确认消息（例如 ⚡），在模型处理之前触发。发送速度与 `ackReaction`（表情符号）相同，有助于在 WhatsApp Web 中区分机器人的回复和用户的消息（尤其是当表情符号不可见时）。

### 3.4.0 版本更新

- **修复问题：** 聊天搜索现在可以识别 LID/JID 别名；通过聊天名称搜索时，会找到使用 `@lid` 和 `@s.whatsapp.net` 格式的消息。
- **新增功能：** `resolveChatJids()` 函数可以跨聊天记录、联系人和消息表查找指定聊天的所有 JID 别名。
- **改进：** 如果无法解析 JID，搜索会恢复到原有的 LIKE 搜索方式，避免功能退化。

### 3.0.0 版本更新

**特点：**
- 无需外部服务，无需 Docker，无需 CLI 工具，直接使用 WhatsApp 的原生协议进行集成。

---

## 许可证

MIT 许可证——属于 OpenClaw 项目的一部分

---

## 链接

- OpenClaw：https://github.com/openclaw/openclaw
- Baileys：https://github.com/WhiskeySockets/Baileys
- ClawHub：https://clawhub.com