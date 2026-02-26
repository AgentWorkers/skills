---
name: whatsapp-ultimate
version: 3.5.0
description: "WhatsApp技能：具备三重安全防护机制。该智能助手仅在以下条件下才会响应用户指令：  
1. 用户位于正确的聊天频道中；  
2. 发出指令的人是该助手被授权服务的用户；  
3. 用户使用的指令符合预设的规则或语法规范。  
该助手会严格遵循这些安全规则，确保只有经过授权的用户才能与其进行有效沟通。"
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
- 通过二维码链接 WhatsApp 账户（`openclaw whatsapp login`）

---

## 功能概述

| 类别 | 功能 |
|----------|----------|
| **消息传递** | 文本、媒体文件、投票、贴纸、语音笔记、GIF 图片 |
| **互动** | 互动表情、回复/引用、编辑、取消发送 |
| **群组** | 创建群组、重命名群组、设置群组图标、添加/删除成员、设置管理员权限、生成群组邀请链接 |

**总共 22 项独立功能**

---

## 消息传递

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
贴纸必须为 WebP 格式，建议尺寸为 512x512 像素

### 发送语音笔记
```
message action=send channel=whatsapp to="+34612345678" filePath=/path/to/audio.ogg asVoice=true
```
**重要提示：** 使用 OGG/Opus 格式的语音笔记。MP3 格式可能无法在 WhatsApp 中正常播放

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

### 添加互动表情
```
message action=react channel=whatsapp chatJid="34612345678@s.whatsapp.net" messageId="ABC123" emoji="🚀"
```

### 删除互动表情
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

### 删除群组成员
```
message action=removeParticipant channel=whatsapp groupId="123456789@g.us" participant="+34612345678"
```

### 提升成员为管理员
```
message action=promoteParticipant channel=whatsapp groupJid="123456789@g.us" participants=["+34612345678"]
```

### 降低成员为普通成员
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
返回内容：群组名称、描述、成员列表、管理员信息、创建日期

---

## JID 格式

WhatsApp 内部使用 JID（Jabber ID）：

| 类型 | 格式 | 例子 |
|------|--------|---------|
| 个人用户 | `<数字>@s.whatsapp.net` | `34612345678@s.whatsapp.net` |
| 群组 | `<id>@g.us` | `123456789012345678@g.us` |

当使用 `to=` 与电话号码关联时，OpenClaw 会自动将其转换为 JID 格式。

---

## 提示

### 语音笔记
请始终使用 OGG/Opus 格式：
```bash
ffmpeg -i input.wav -c:a libopus -b:a 64k output.ogg
```

### 贴纸
请将图片转换为 WebP 格式的贴纸：
```bash
ffmpeg -i input.png -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000" output.webp
```

### 回复消息
当收到新消息时，会立即发送一条文本消息——该消息在模型处理之前就在网关层被发送：
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
| `text` | 字符串 | `""` | 要发送的文本（空值表示禁用） |
| `direct` | 布尔值 | `true` | 是否在私信中发送 |
| `group` | `"always"` / `"mentions"` / `"never"` | 是否在群组聊天中发送 |

这与 `ackReaction`（发送表情符号）不同：`ackMessage` 会发送一条独立的消息气泡——即使在群组聊天中看不到互动表情时，这条消息也会显示。

### 发送频率限制
WhatsApp 有反垃圾邮件机制。请避免：
- 向大量联系人批量发送消息
- 迅速连续发送消息
- 向未先与你联系过的联系人发送消息

### 消息 ID
要回复、编辑或取消发送消息，你需要消息的 ID。收到的消息中包含该 ID；你发送的消息的响应中也包含该 ID。

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
| 互动表情 | ✅ | ❌ | ❌ | ❌ |
| 回复/引用 | ✅ | ❌ | ❌ | ❌ |
| 编辑消息 | ✅ | ❌ | ❌ | ❌ |
| 取消发送 | ✅ | ❌ | ❌ | ❌ |
| 创建群组 | ✅ | ❌ | ❌ | ❌ |
| 群组管理 | ✅（全部功能） | ❌ | ❌ | ❌ |
| 接收消息 | ✅ | ✅ | ✅ | ❌ |
| 双向聊天 | ✅ | ❌ | ❌ | ❌ |
| 外部依赖 | 无 | 需 Go 语言和二进制文件 | 需 Docker 与 WAHA 工具 | 需 ffmpeg |

---

### 3.5.0 版本更新

- **新增功能：** `ackMessage`——在收到新消息时立即发送可配置的文本消息（例如 ⚡），在模型处理之前触发。发送速度与 `ackReaction`（表情符号）相同。这有助于在 WhatsApp Web 中区分人工回复和机器人回复（因为互动表情可能无法显示）。

### 3.4.0 版本更新

- **修复问题：** 聊天搜索现在可以解析 LID/JID 别名——通过聊天名称搜索时，可以找到使用 `@lid` 和 `@s.whatsapp.net` 格式的消息
- **新增功能：** `resolveChatJids()` 函数可以查询聊天记录、联系人和消息表，以找到指定聊天的所有 JID 别名
- **改进：** 如果无法解析 JID，搜索会回退到原始的 LIKE 搜索方式，以避免功能退化

### 3.0.0 版本更新

**特点：**
- 无需外部服务，无需 Docker，无需 CLI 工具，直接使用协议集成

---

## 许可证

MIT 许可证——属于 OpenClaw 项目的一部分

---

## 链接

- OpenClaw：https://github.com/openclaw/openclaw
- Baileys：https://github.com/WhiskeySockets/Baileys
- ClawHub：https://clawhub.com