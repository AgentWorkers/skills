---
name: evogo
description: 通过 Evolution API Go v3 完成 WhatsApp 自动化操作：实例、消息（文本/媒体/投票/轮播）、群组、联系人、聊天记录、社区、新闻通讯以及实时 Webhook 功能
metadata:
  openclaw:
    requires:
      bins: []
    env:
      EVOGO_API_URL: "Evolution API base URL (e.g., http://localhost:8080 or https://api.yourdomain.com)"
      EVOGO_GLOBAL_KEY: "Global API key for admin operations (instance management)"
      EVOGO_INSTANCE: "Default instance name"
      EVOGO_API_KEY: "Instance-specific token for messaging operations"
---

# evoGo - Evolution API Go v3

通过 Evolution API Go v3 完成 WhatsApp 自动化操作。支持发送消息、管理群组、自动化对话以及集成 Webhook 功能。

---

## 🚀 快速入门

### 1. 设置环境变量

```json5
{
  env: {
    EVOGO_API_URL: "http://localhost:8080",        // Your API URL
    EVOGO_GLOBAL_KEY: "your-global-admin-key",     // Admin key (instance mgmt)
    EVOGO_INSTANCE: "my-bot",                      // Instance name
    EVOGO_API_KEY: "your-instance-token"           // Instance token (messaging)
  }
}
```

### 2. 创建实例并连接

```bash
# Create instance
curl -X POST "$EVOGO_API_URL/instance/create" \
  -H "apikey: $EVOGO_GLOBAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-bot",
    "token": "my-secret-token",
    "qrcode": true
  }'

# Connect & get QR code
curl -X POST "$EVOGO_API_URL/instance/connect" \
  -H "apikey: $EVOGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"number": ""}'
```

扫描 `qrcode.base64` 中返回的 QR 码。

### 3. 发送第一条消息

```bash
curl -X POST "$EVOGO_API_URL/send/text" \
  -H "apikey: $EVOGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "text": "Hello from evoGo! 🚀"
  }'
```

---

## 🔐 认证

Evolution API 提供两种认证方式：

| 类型 | 头部字段 | 用途 |
|------|--------|-------|
| **全局 API 密钥** | `apikey: xxx` | 管理员：创建/删除实例、查看日志 |
| **实例令牌** | `apikey: xxx` | 发送消息、管理群组、操作联系人 |

可以通过环境变量设置或直接在请求头部传递 API 密钥。

---

## 📦 核心概念

### 手机号码格式

| 场景 | 格式 | 例子 |
|---------|--------|---------|
| **发送消息** | 国际格式（不含 +） | `5511999999999` |
| **群组成员** | JID 格式 | `5511999999999@s.whatsapp.net` |
| **群组** | 群组 JID | `120363123456789012@g.us` |
| **新闻通讯** | 新闻通讯 JID | `120363123456789012@newsletter` |

### 消息延迟

通过设置 `delay`（毫秒）来避免达到 WhatsApp 的发送速率限制：

```json
{
  "number": "5511999999999",
  "text": "Message with delay",
  "delay": 2000
}
```

---

## 🎯 功能参考

### 📱 实例管理

#### 创建实例
```bash
POST /instance/create
Header: apikey: $EVOGO_GLOBAL_KEY

{
  "name": "bot-name",
  "token": "secret-token",
  "qrcode": true,
  "advancedSettings": {
    "rejectCalls": false,
    "groupsIgnore": false,
    "alwaysOnline": true,
    "readMessages": true,
    "readStatus": true,
    "syncFullHistory": true
  }
}
```

**高级设置：**
- `rejectCalls` - 自动拒绝来电
- `groupsIgnore` - 忽略群组消息
- `alwaysOnline` - 始终保持在线状态
- `readMessages` - 自动将消息标记为已读
- `readStatus` - 自动将状态标记为已查看
- `syncFullHistory` - 同步完整聊天记录

#### 连接 / 获取 QR 码
```bash
POST /instance/connect
GET  /instance/qr
Header: apikey: $EVOGO_API_KEY

{"number": ""}  # Leave empty for QR, or phone number for pairing
```

#### 连接状态
```bash
GET /instance/status
Header: apikey: $EVOGO_API_KEY
```

返回值：`connected`、`connecting`、`disconnected`

#### 列出所有实例
```bash
GET /instance/all
Header: apikey: $EVOGO_GLOBAL_KEY
```

#### 删除实例
```bash
DELETE /instance/delete/{instance}
Header: apikey: $EVOGO_GLOBAL_KEY
```

#### 强制重新连接
```bash
POST /instance/forcereconnect/{instance}
Header: apikey: $EVOGO_GLOBAL_KEY

{"number": "5511999999999"}
```

#### 日志
```bash
GET /instance/logs/{instance}?start_date=2026-01-01&end_date=2026-02-10&level=info&limit=100
Header: apikey: $EVOGO_GLOBAL_KEY
```

**日志级别：** `info`、`warn`、`error`、`debug`

---

### 💬 发送消息

#### 文本消息
```bash
POST /send/text

{
  "number": "5511999999999",
  "text": "Hello World!",
  "delay": 1000,
  "mentionsEveryOne": false,
  "mentioned": ["5511888888888@s.whatsapp.net"]
}
```

#### 媒体文件（URL）
```bash
POST /send/media

{
  "number": "5511999999999",
  "url": "https://example.com/photo.jpg",
  "type": "image",
  "caption": "Check this out!",
  "filename": "photo.jpg"
}
```

**支持的媒体类型：**
- `image` - JPG、PNG、GIF、WEBP
- `video` - MP4、AVI、MOV、MKV
- `audio` - MP3、OGG、WAV（作为语音消息发送）
- `document` - PDF、DOC、DOCX、XLS、XLSX、PPT、TXT、ZIP
- `ptv` - 圆形视频（Instagram 风格）

#### 媒体文件上传
```bash
POST /send/media
Content-Type: multipart/form-data

number=5511999999999
type=image
file=@/path/to/file.jpg
caption=Photo caption
filename=custom-name.jpg
```

#### 投票
```bash
POST /send/poll

{
  "number": "5511999999999",
  "question": "Best language?",
  "options": ["JavaScript", "Python", "Go", "Rust"],
  "selectableCount": 1
}
```

**获取投票结果：**
```bash
GET /polls/{messageId}/results
```

#### 贴纸
```bash
POST /send/sticker

{
  "number": "5511999999999",
  "sticker": "https://example.com/sticker.webp"
}
```

系统会自动将图片转换为 WebP 格式。

#### 位置信息
```bash
POST /send/location

{
  "number": "5511999999999",
  "latitude": -23.550520,
  "longitude": -46.633308,
  "name": "Avenida Paulista",
  "address": "Av. Paulista, São Paulo - SP"
}
```

#### 联系人信息
```bash
POST /send/contact

{
  "number": "5511999999999",
  "vcard": {
    "fullName": "João Silva",
    "phone": "5511988888888",
    "organization": "Company XYZ",
    "email": "joao@example.com"
  }
}
```

#### 信息轮播
```bash
POST /send/carousel

{
  "number": "5511999999999",
  "body": "Main carousel text",
  "footer": "Footer text",
  "cards": [
    {
      "header": {
        "title": "Card 1",
        "subtitle": "Subtitle",
        "imageUrl": "https://example.com/img1.jpg"
      },
      "body": {"text": "Card description"},
      "footer": "Card footer",
      "buttons": [
        {
          "displayText": "Click Me",
          "id": "btn1",
          "type": "REPLY"
        }
      ]
    }
  ]
}
```

**按钮类型：**
- `REPLY` - 回复
- `URL` - 打开链接
- `CALL` - 发起通话
- `COPY` - 复制文本

---

### 📨 消息操作

#### 回复消息
```bash
POST /message/react

{
  "number": "5511999999999",
  "reaction": "👍",
  "id": "MESSAGE_ID",
  "fromMe": false,
  "participant": "5511888888888@s.whatsapp.net"  # Required in groups
}
```

**回复表情：** `👍`、`❤️`、`😂`、`😮`、`😢`、`🙏` 或 `"remove"`

#### 输入/录音指示器
```bash
POST /message/presence

{
  "number": "5511999999999",
  "state": "composing",
  "isAudio": false
}
```

**状态：**
- `composing` + `isAudio: false` → “正在输入…”
- `composing` + `isAudio: true` → “正在录音…”
- `paused` → 停止录音指示器

#### 标记为已读
```bash
POST /message/markread

{
  "number": "5511999999999",
  "id": ["MESSAGE_ID_1", "MESSAGE_ID_2"]
}
```

#### 下载媒体文件
```bash
POST /message/downloadmedia

{
  "message": {}  # Full message object from webhook
}
```

返回媒体文件的 Base64 编码内容。

#### 编辑消息
```bash
POST /message/edit

{
  "chat": "5511999999999@s.whatsapp.net",
  "messageId": "MESSAGE_ID",
  "message": "Edited text"
}
```

**限制：**
- 仅支持文本消息
- 仅限发送者自己的消息
- 消息发送有 15 分钟的时间限制

#### 删除消息
```bash
POST /message/delete

{
  "chat": "5511999999999@s.whatsapp.net",
  "messageId": "MESSAGE_ID"
}
```

**限制：**
- 仅限发送者自己的消息
- 消息删除有 48 小时的时间限制

#### 获取消息状态
```bash
POST /message/status

{
  "id": "MESSAGE_ID"
}
```

返回消息的送达/已读状态。

---

### 👥 群组管理

#### 列出群组
```bash
GET /group/list        # Basic info (JID + name)
GET /group/myall       # Full info (participants, settings, etc)
```

#### 获取群组信息
```bash
POST /group/info

{
  "groupJid": "120363123456789012@g.us"
}
```

#### 创建群组
```bash
POST /group/create

{
  "groupName": "My Team",
  "participants": [
    "5511999999999@s.whatsapp.net",
    "5511888888888@s.whatsapp.net"
  ]
}
```

**要求：**
- 名称：最多 25 个字符
- 最少 1 名成员

#### 管理成员
```bash
POST /group/participant

{
  "groupJid": "120363123456789012@g.us",
  "action": "add",
  "participants": ["5511999999999@s.whatsapp.net"]
}
```

**操作：**
- `add` - 添加成员
- `remove` - 删除成员
- `promote` - 提升成员为管理员
- `demote` - 降级成员为普通成员

#### 更新群组设置
```bash
POST /group/settings

{
  "groupJid": "120363123456789012@g.us",
  "action": "announcement"
}
```

**设置：**
- `announcement` / `not_announcement` - 只有管理员可以发送消息
- `locked` / `unlocked` - 只有管理员可以编辑群组信息
- `approval_on` / `approval_off` - 加入群组需要审批
- `admin_add` / `all_member_add` - 可以添加成员的用户

#### 获取群组邀请链接
```bash
POST /group/invitelink

{
  "groupJid": "120363123456789012@g.us",
  "reset": false
}
```

设置 `reset: true` 可以撤销旧链接并生成新链接。

#### 加入群组
```bash
POST /group/join

{
  "code": "https://chat.whatsapp.com/XXXXXX"
}
```

可以接受完整链接或仅接受群组代码。

#### 离开群组
```bash
POST /group/leave

{
  "groupJid": "120363123456789012@g.us"
}
```

#### 管理加入请求
```bash
# Get pending requests
POST /group/requests
{
  "groupJid": "120363123456789012@g.us"
}

# Approve/Reject
POST /group/requests/action
{
  "groupJid": "120363123456789012@g.us",
  "action": "approve",
  "participants": ["5511999999999@s.whatsapp.net"]
}
```

**操作：** `approve`、`reject`

#### 更新群组元数据
```bash
# Set photo
POST /group/photo
{
  "groupJid": "120363123456789012@g.us",
  "image": "https://example.com/photo.jpg"
}

# Set name
POST /group/name
{
  "groupJid": "120363123456789012@g.us",
  "name": "New Group Name"
}

# Set description
POST /group/description
{
  "groupJid": "120363123456789012@g.us",
  "description": "New description"
}
```

---

### 💬 聊天管理

#### 固定/取消固定聊天记录
```bash
POST /chat/pin
POST /chat/unpin

{
  "chat": "5511999999999@s.whatsapp.net"
}
```

#### 归档/取消归档聊天记录
```bash
POST /chat/archive
POST /chat/unarchive

{
  "chat": "5511999999999@s.whatsapp.net"
}
```

#### 静音/取消静音聊天记录
```bash
POST /chat/mute
POST /chat/unmute

{
  "chat": "5511999999999@s.whatsapp.net"
}
```

#### 同步聊天记录
```bash
POST /chat/history-sync-request
```

请求同步完整聊天记录（可能需要一些时间）。

---

### 👤 用户与个人资料

#### 获取用户信息
```bash
POST /user/info

{
  "number": ["5511999999999", "5511888888888"],
  "formatJid": true
}
```

返回用户状态、个人资料图片、验证标志等信息。

#### 检查 WhatsApp 注册情况
```bash
POST /user/check

{
  "number": ["5511999999999", "5511888888888"]
}
```

返回每个电话号码的 `isInWhatsapp`（true/false）状态。

#### 获取个人资料图片
```bash
POST /user/avatar

{
  "number": "5511999999999",
  "preview": false
}
```

**预览选项：**
- `false` - 全分辨率
- `true` - 低分辨率预览

#### 获取联系人信息
```bash
GET /user/contacts
```

列出所有保存的联系人。

#### 隐私设置
```bash
# Get privacy settings
GET /user/privacy

# Set privacy settings
POST /user/privacy
{
  "groupAdd": "all",
  "lastSeen": "contacts",
  "status": "all",
  "profile": "all",
  "readReceipts": "all",
  "callAdd": "all",
  "online": "match_last_seen"
}
```

**选项：** `all`、`contacts`、`contact_blacklist`、`none`、`match_last_seen`（仅显示在线联系人）

#### 阻止/解除阻止联系人
```bash
POST /user/block
POST /user/unblock

{
  "number": "5511999999999"
}

# Get block list
GET /user/blocklist
```

#### 更新个人资料
```bash
# Set profile picture
POST /user/profilePicture
{
  "image": "https://example.com/photo.jpg"
}

# Set profile name
POST /user/profileName
{
  "name": "My Name"
}

# Set status/about
POST /user/profileStatus
{
  "status": "My custom status"
}
```

**限制：**
- 名称：最多 25 个字符
- 状态：最多 139 个字符

---

### 🏷️ 标签

#### 添加标签
```bash
# To chat
POST /label/chat
{
  "jid": "5511999999999@s.whatsapp.net",
  "labelId": "1"
}

# To message
POST /label/message
{
  "jid": "5511999999999@s.whatsapp.net",
  "labelId": "1",
  "messageId": "MESSAGE_ID"
}
```

#### 删除标签
```bash
POST /unlabel/chat
POST /unlabel/message

{
  "jid": "5511999999999@s.whatsapp.net",
  "labelId": "1",
  "messageId": "MESSAGE_ID"  # Only for /unlabel/message
}
```

#### 编辑标签
```bash
POST /label/edit

{
  "labelId": "1",
  "name": "New Label Name"
}
```

#### 列出标签
```bash
GET /label
```

---

### 🏘️ 社区

#### 创建社区
```bash
POST /community/create

{
  "communityName": "My Community",
  "description": "Optional description"
}
```

#### 添加/删除群组
```bash
POST /community/add
{
  "communityJID": "120363123456789012@g.us",
  "groupJID": ["120363111111111111@g.us"]
}

POST /community/remove
{
  "communityJID": "120363123456789012@g.us",
  "groupJID": ["120363111111111111@g.us"]
}
```

---

### 📢 新闻通讯（频道）

#### 创建新闻通讯
```bash
POST /newsletter/create

{
  "name": "My Channel",
  "description": "Optional description"
}
```

#### 列出新闻通讯
```bash
GET /newsletter/list
```

#### 获取新闻通讯信息
```bash
POST /newsletter/info

{
  "jid": "120363123456789012@newsletter"
}
```

#### 订阅新闻通讯
```bash
POST /newsletter/subscribe

{
  "jid": "120363123456789012@newsletter"
}
```

#### 获取新闻通讯消息
```bash
POST /newsletter/messages

{
  "jid": "120363123456789012@newsletter",
  "limit": 50
}
```

#### 获取邀请链接信息
```bash
POST /newsletter/link

{
  "key": "INVITE_KEY"
}
```

---

### 📞 呼叫管理

#### 拒绝来电
```bash
POST /call/reject

# Webhook payload from call event
```

可以使用 Webhook 自动化功能来自动拒绝来电。

---

## 🎬 常见工作流程

### 向多个联系人广播消息
```bash
for number in 5511999999999 5511888888888 5511777777777; do
  curl -X POST "$EVOGO_API_URL/send/text" \
    -H "apikey: $EVOGO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"number\": \"$number\",
      \"text\": \"Broadcast message\",
      \"delay\": 2000
    }"
done
```

### 向群组发送带有提及信息的图片
```bash
curl -X POST "$EVOGO_API_URL/send/media" \
  -H "apikey: $EVOGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "120363123456789012@g.us",
    "url": "https://example.com/report.jpg",
    "type": "image",
    "caption": "Report ready! @5511999999999 please review",
    "mentionedJid": ["5511999999999@s.whatsapp.net"]
  }'
```

### 自动创建群组并发送欢迎消息
```bash
# 1. Create group
GROUP_JID=$(curl -s -X POST "$EVOGO_API_URL/group/create" \
  -H "apikey: $EVOGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "groupName": "Team Alpha",
    "participants": ["5511999999999@s.whatsapp.net"]
  }' | jq -r '.groupJid')

# 2. Send welcome message
curl -X POST "$EVOGO_API_URL/send/text" \
  -H "apikey: $EVOGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"number\": \"$GROUP_JID\",
    \"text\": \"Welcome to Team Alpha! 🎉\"
  }"
```

### 检查多个电话号码
```bash
curl -X POST "$EVOGO_API_URL/user/check" \
  -H "apikey: $EVOGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "number": [
      "5511999999999",
      "5511888888888",
      "5511777777777"
    ]
  }'
```

---

## ⚠️ 速率限制与最佳实践

### 消息发送延迟

始终在消息之间添加延迟：
```json
{"delay": 2000}  // 2 seconds
```

**推荐：**
- 单条消息之间间隔 1-2 秒
- 批量发送之间间隔 3-5 秒
- 出现错误时采用指数级退避策略

### 错误处理

**HTTP 状态码：**
- `200` - 成功
- `400` - 请求错误（检查参数）
- `401` - 未经授权（检查 API 密钥）
- `404` - 未找到（实例/资源不存在）
- `500` - 服务器错误

**常见问题：**

| 错误 | 解决方案 |
|-------|----------|
| 实例未连接 | 运行 `POST /instance/connect` |
| 手机号码格式错误 | 使用国际格式（不含 +）：`5511999999999` |
| 消息未发送 | 查看 `GET /instance/status` |
- 群组操作失败 | 确认用户具有管理员权限（仅限管理员操作）

---

## 🔗 Webhook

配置 Webhook 以接收实时事件：
- 消息接收
- 消息发送
- 连接状态
- 群组更新
- 来电接收
- 以及其他事件...

使用 `POST /webhook/set` 端点来配置 Webhook URL（详情请参考 Postman 文档）。

---

## 🧪 故障排除

### 实例无法连接
```bash
# 1. Check if instance exists
GET /instance/all

# 2. Force reconnect
POST /instance/forcereconnect/{instance}

# 3. Check logs
GET /instance/logs/{instance}?level=error
```

### 消息无法发送
1. 检查连接状态：`GET /instance/status`
2. 确认电话号码格式（不含 `+` 或空格）
3. 确保接收方安装了 WhatsApp
4. 确认 API 密钥正确

### 群组操作失败
1. 确认用户具有管理员权限（仅限管理员操作）
2. 确认群组 JID 格式：`xxxxx@g.us`
3. 确保成员使用正确的格式：`number@s.whatsapp.net`

---

## 📚 资源

- **Evolution API Go**：https://github.com/EvolutionAPI/evolution-api
- **WhatsApp Business API**：https://developers.facebook.com/docs/whatsapp
- **JID 格式指南**：用户使用 `number@s.whatsapp.net`，群组使用 `xxxxx@g.us`

---

## 🆕 已知限制

**（v3.0 版本）不可用的功能：**
- `/send/button` - 交互式按钮（已被 WhatsApp 废弃）
- `/send/list` - 交互式列表（已被 WhatsApp 废弃）

这些接口虽然存在，但由于 WhatsApp API 的更新，目前无法使用。

---

## 💡 提示

1. **操作前务必检查状态**  
2. **设置延迟** 以避免达到发送速率限制（至少 1-2 秒）  
3. **安全地存储令牌**，将其保存在环境变量中  
4. **处理断开连接** 时自动重新连接  
5. **发送前验证电话号码**  
6. **使用 Webhook** 处理实时事件  
7. **查看日志** 以进行故障排查  
8. **在批量操作前先在小范围内测试**

**evoGo** 通过 Evolution API Go v3 简化了 WhatsApp 的自动化操作。如需高级功能，请查看完整的 Postman 文档或 API 文档。