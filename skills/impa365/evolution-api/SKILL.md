---
name: evolution-api-v2
description: 通过 Evolution API v2.3 完成 WhatsApp 自动化操作：支持实例、消息（文本/媒体/投票/列表/按钮/状态）、群组、标签、聊天机器人（Typebot/OpenAI/Dify/Flowise/N8N/EvoAI）、Webhook、代理服务器、S3 存储以及与 Chatwoot 的集成。
metadata:
  openclaw:
    requires:
      bins: []
    env:
      EVO_API_URL: "Evolution API base URL (e.g., http://localhost:8080 or https://api.yourdomain.com)"
      EVO_GLOBAL_KEY: "Global API key for admin operations (instance management)"
      EVO_INSTANCE: "Default instance name"
      EVO_API_KEY: "Instance-specific API key for messaging operations"
---

# Evolution API v2.3

通过Evolution API v2.3实现完整的WhatsApp自动化功能。您可以发送消息、管理群组、集成聊天机器人（如Typebot、OpenAI、Dify、Flowise、N8N、Evo AI）、配置Webhook，并与Chatwoot进行连接。

---

## 快速入门

### 1. 设置环境变量

```json5
{
  env: {
    EVO_API_URL: "http://localhost:8080",       // Your API URL
    EVO_GLOBAL_KEY: "your-global-admin-key",    // Admin key (instance mgmt)
    EVO_INSTANCE: "my-bot",                     // Instance name
    EVO_API_KEY: "your-instance-token"          // Instance token (messaging)
  }
}
```

### 2. 创建实例并连接

```bash
# Create instance (supports Baileys, Business, or Evolution integration)
curl -X POST "$EVO_API_URL/instance/create" \
  -H "apikey: $EVO_GLOBAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "my-bot",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'

# Connect & get QR code
curl -X GET "$EVO_API_URL/instance/connect/$EVO_INSTANCE" \
  -H "apikey: $EVO_API_KEY"
```

扫描`base64`字段中返回的二维码。或者使用`?number=5511999999999`作为配对码。

### 3. 发送第一条消息

```bash
curl -X POST "$EVO_API_URL/message/sendText/$EVO_INSTANCE" \
  -H "apikey: $EVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5511999999999",
    "text": "Hello from Evolution API v2! 🚀"
  }'
```

---

## 认证

Evolution API提供两种认证级别：

| 认证类型 | 头部字段 | 用途 |
|--------|---------|-------|
| **全局API密钥** | `apikey: $EVO_GLOBAL_KEY` | 管理员：创建/删除实例、获取所有信息 |
| **实例API密钥** | `apikey: $EVO_API_KEY` | 发送消息、管理群组、聊天、个人资料、标签 |

所有实例端点的路径模式为：`/{resource}/{action}/{instanceName}`

---

## 核心概念

### 手机号码格式

| 使用场景 | 格式 | 示例 |
|---------|--------|---------|
| **发送消息** | 国家代码 + 电话号码 | `5511999999999` |
| **群组JID** | 群组ID | `999999999999999999@g.us` |
| **用户JID** | 电话号码 + 后缀 | `5511999999999@s.whatsapp.net` |

### 集成类型

| 值 | 描述 |
|-------|-------------|
| `WHATSAPP-BAILEYS` | 非官方版本（默认，支持全部功能） |
| `WHATSAPP-BUSINESS` | 官方Cloud API |
| `EVOLUTION` | Evolution专用通道 |

### 消息延迟

通过添加`delay`参数（单位：毫秒）来避免达到发送速率限制：

```json
{ "delay": 1200 }
```

---

## 功能参考

### 实例管理

#### 创建实例
```bash
POST /instance/create
Header: apikey: $EVO_GLOBAL_KEY

{
  "instanceName": "my-bot",
  "qrcode": true,
  "integration": "WHATSAPP-BAILEYS",
  // Optional
  "token": "custom-api-key",
  "number": "5511999999999",
  // Settings (optional)
  "rejectCall": false,
  "msgCall": "",
  "groupsIgnore": false,
  "alwaysOnline": false,
  "readMessages": false,
  "readStatus": false,
  "syncFullHistory": false,
  // Proxy (optional)
  "proxyHost": "",
  "proxyPort": "",
  "proxyProtocol": "",
  "proxyUsername": "",
  "proxyPassword": ""
}
```

**创建时可选配置：**
- **内联Webhook**：```json
{
  "webhook": {
    "url": "https://webhook.site/your-id",
    "byEvents": false,
    "base64": true,
    "headers": {
      "autorization": "Bearer TOKEN"
    },
    "events": ["MESSAGES_UPSERT", "CONNECTION_UPDATE"]
  }
}
```
- **内联RabbitMQ / SQS**：```json
{
  "rabbitmq": { "enabled": true, "events": ["MESSAGES_UPSERT"] },
  "sqs": { "enabled": true, "events": ["MESSAGES_UPSERT"] }
}
```
- **内联Chatwoot**：```json
{
  "chatwootAccountId": "1",
  "chatwootToken": "TOKEN",
  "chatwootUrl": "https://chatwoot.com",
  "chatwootSignMsg": true,
  "chatwootReopenConversation": true,
  "chatwootConversationPending": false,
  "chatwootImportContacts": true,
  "chatwootNameInbox": "evolution",
  "chatwootMergeBrazilContacts": true,
  "chatwootImportMessages": true,
  "chatwootDaysLimitImportMessages": 3
}
```

#### 获取实例信息
```bash
GET /instance/fetchInstances
Header: apikey: $EVO_GLOBAL_KEY

# Optional query params:
# ?instanceName=my-bot
# ?instanceId=INSTANCE_ID
```

#### 通过二维码连接实例
```bash
GET /instance/connect/{instance}
Header: apikey: $EVO_API_KEY

# Optional: ?number=5511999999999 (for pairing code)
```

#### 检查实例连接状态
```bash
GET /instance/connectionState/{instance}
Header: apikey: $EVO_API_KEY
```

#### 重启实例
```bash
POST /instance/restart/{instance}
Header: apikey: $EVO_API_KEY
```

#### 设置用户在线状态
```bash
POST /instance/setPresence/{instance}
Header: apikey: $EVO_API_KEY

{ "presence": "available" }
```
**可选状态：** `available`（在线），`unavailable`（离线）

#### 退出实例
```bash
DELETE /instance/logout/{instance}
Header: apikey: $EVO_API_KEY
```

#### 删除实例
```bash
DELETE /instance/delete/{instance}
Header: apikey: $EVO_GLOBAL_KEY
```

---

### 设置

#### 配置设置
```bash
POST /settings/set/{instance}
Header: apikey: $EVO_API_KEY

{
  "rejectCall": true,
  "msgCall": "I do not accept calls",
  "groupsIgnore": false,
  "alwaysOnline": true,
  "readMessages": false,
  "syncFullHistory": false,
  "readStatus": false
}
```

#### 查看设置
```bash
GET /settings/find/{instance}
Header: apikey: $EVO_API_KEY
```

---

### 代理设置

#### 设置代理
```bash
POST /proxy/set/{instance}
Header: apikey: $EVO_API_KEY

{
  "enabled": true,
  "host": "0.0.0.0",
  "port": "8000",
  "protocol": "http",
  "username": "user",
  "password": "pass"
}
```

#### 查找代理信息
```bash
GET /proxy/find/{instance}
Header: apikey: $EVO_API_KEY
```

---

### 发送消息

#### 发送文本消息
```bash
POST /message/sendText/{instance}

{
  "number": "5511999999999",
  "text": "Hello World!"
  // Options:
  // "delay": 1200,
  // "linkPreview": false,
  // "mentionsEveryOne": false,
  // "mentioned": ["5511888888888"],
  // "quoted": { "key": { "id": "MESSAGE_ID" }, "message": { "conversation": "quoted text" } }
}
```

#### 发送媒体文件（URL）
```bash
POST /message/sendMedia/{instance}

{
  "number": "5511999999999",
  "mediatype": "image",
  "mimetype": "image/png",
  "caption": "Caption text",
  "media": "https://example.com/photo.jpg",
  "fileName": "photo.png"
  // Options: delay, quoted, mentionsEveryOne, mentioned
}
```

**支持的媒体类型：** `image`（图片）、`video`（视频）、`document`（文档）

#### 上传媒体文件
```bash
POST /message/sendMedia/{instance}
Content-Type: multipart/form-data

# Use form-data with file field
```

#### 发送PTV（圆形视频）
```bash
POST /message/sendPtv/{instance}

{
  "number": "5511999999999",
  "video": "https://example.com/video.mp4"
  // Options: delay, quoted, mentionsEveryOne, mentioned
}
```

支持通过表单数据上传文件。

#### 发送语音消息
```bash
POST /message/sendWhatsAppAudio/{instance}

{
  "number": "5511999999999",
  "audio": "https://example.com/audio.mp3"
  // Options: delay, quoted, encoding (true/false)
}
```

#### 发送状态/故事
```bash
POST /message/sendStatus/{instance}

{
  "type": "text",
  "content": "My status update!",
  "backgroundColor": "#008000",
  "font": 1,
  "allContacts": false,
  "statusJidList": ["5511999999999@s.whatsapp.net"]
}
```

**状态/故事类型：** `text`（文本）、`image`（图片）、`video`（视频）、`audio`（音频）  
**文本字体：** `1`（SERIF）、`2`（NORICAN_REGULAR）、`3`（BRYNDAN_WRITE）、`4`（BEBASNEUE_REGULAR）、`5`（OSWALD_HEAVY）  
对于图片/视频，使用`content`作为URL，`caption`作为文字描述。

#### 发送贴纸
```bash
POST /message/sendSticker/{instance}

{
  "number": "5511999999999",
  "sticker": "https://example.com/sticker.webp"
  // Options: delay, quoted
}
```

#### 发送位置信息
```bash
POST /message/sendLocation/{instance}

{
  "number": "5511999999999",
  "name": "Bora Bora",
  "address": "French Polynesia",
  "latitude": -16.505538,
  "longitude": -151.742277
  // Options: delay, quoted
}
```

#### 发送联系人信息（vCard）
```bash
POST /message/sendContact/{instance}

{
  "number": "5511999999999",
  "contact": [
    {
      "fullName": "Contact Name",
      "wuid": "559999999999",
      "phoneNumber": "+55 99 9 9999-9999",
      "organization": "Company",
      "email": "email@example.com",
      "url": "https://example.com"
    }
  ]
}
```

可以一次性发送多个联系人信息。

#### 发送反应表情
```bash
POST /message/sendReaction/{instance}

{
  "key": {
    "remoteJid": "5511999999999@s.whatsapp.net",
    "fromMe": true,
    "id": "BAE5A75CB0F39712"
  },
  "reaction": "🚀"
}
```

将`reaction`设置为`""`可取消发送反应表情。

#### 发送投票
```bash
POST /message/sendPoll/{instance}

{
  "number": "5511999999999",
  "name": "What is your favorite color?",
  "selectableCount": 1,
  "values": ["Red", "Blue", "Green"]
  // Options: delay, quoted
}
```

#### 发送列表信息
```bash
POST /message/sendList/{instance}

{
  "number": "5511999999999",
  "title": "List Title",
  "description": "Choose an option",
  "buttonText": "Click Here",
  "footerText": "Footer text",
  "sections": [
    {
      "title": "Section 1",
      "rows": [
        {
          "title": "Option A",
          "description": "Description of option A",
          "rowId": "opt_a"
        },
        {
          "title": "Option B",
          "description": "Description of option B",
          "rowId": "opt_b"
        }
      ]
    }
  ]
  // Options: delay, quoted
}
```

#### 发送按钮
```bash
POST /message/sendButtons/{instance}

{
  "number": "5511999999999",
  "title": "Button Title",
  "description": "Button Description",
  "footer": "Footer Text",
  "buttons": [
    { "type": "reply", "displayText": "Reply", "id": "btn_1" },
    { "type": "copy", "displayText": "Copy Code", "copyCode": "ABC123" },
    { "type": "url", "displayText": "Open Link", "url": "https://example.com" },
    { "type": "call", "displayText": "Call Us", "phoneNumber": "5511999999999" },
    { "type": "pix", "currency": "BRL", "name": "John Doe", "keyType": "random", "key": "uuid-key" }
  ]
  // Options: delay, quoted
}
```

**按钮类型：** `reply`（回复）、`copy`（复制）、`url`（链接）、`call`（呼叫）、`pix`（图片链接）  
**Pix键值类型：** `phone`（电话号码）、`email`（电子邮件地址）、`cpf`（加拿大法人身份证号）、`random`（随机）

---

### 聊天操作

#### 检查WhatsApp号码是否可用
```bash
POST /chat/whatsappNumbers/{instance}

{
  "numbers": [
    "55911111111",
    "55922222222",
    "55933333333"
  ]
}
```

#### 阅读消息（标记为已读）
```bash
POST /chat/markMessageAsRead/{instance}

{
  "readMessages": [
    {
      "remoteJid": "5511999999999@s.whatsapp.net",
      "fromMe": false,
      "id": "MESSAGE_ID"
    }
  ]
}
```

#### 归档聊天记录
```bash
POST /chat/archiveChat/{instance}

{
  "lastMessage": {
    "key": {
      "remoteJid": "5511999999999@s.whatsapp.net",
      "fromMe": false,
      "id": "MESSAGE_ID"
    }
  },
  "chat": "5511999999999@s.whatsapp.net",
  "archive": true
}
```

将`archive`设置为`false`可取消归档。

#### 将聊天记录标记为未读
```bash
POST /chat/markChatUnread/{instance}

{
  "lastMessage": {
    "key": {
      "remoteJid": "5511999999999@s.whatsapp.net",
      "fromMe": false,
      "id": "MESSAGE_ID"
    }
  },
  "chat": "5511999999999@s.whatsapp.net"
}
```

#### 删除消息
```bash
DELETE /chat/deleteMessageForEveryone/{instance}

{
  "id": "MESSAGE_ID",
  "remoteJid": "5511999999999@s.whatsapp.net",
  "fromMe": true,
  "participant": "participant_jid"
}
```

#### 更新消息内容
```bash
POST /chat/updateMessage/{instance}

{
  "number": "5511999999999",
  "key": {
    "remoteJid": "5511999999999@s.whatsapp.net",
    "fromMe": true,
    "id": "MESSAGE_ID"
  },
  "text": "new edited message"
}
```

#### 设置发送状态（输入中）
```bash
POST /chat/sendPresence/{instance}

{
  "number": "5511999999999",
  "delay": 1200,
  "presence": "composing"
}
```

**状态选项：** `composing`（输入中）、`recording`（正在录制）、`paused`（暂停）

#### 更新消息块状态
```bash
POST /message/updateBlockStatus/{instance}

{
  "number": "5511999999999",
  "status": "block"
}
```

**状态选项：** `block`（屏蔽）、`unblock`（解封）

#### 获取个人资料图片
```bash
POST /chat/fetchProfilePictureUrl/{instance}

{ "number": "5511999999999" }
```

#### 从媒体消息中提取Base64编码
```bash
POST /chat/getBase64FromMediaMessage/{instance}

{
  "message": {
    "key": { "id": "MESSAGE_ID" }
  },
  "convertToMp4": false
}
```

从接收到的媒体文件中提取Base64编码。将`convertToMp4`设置为`true`可获取MP4格式文件（而非OGG格式）。

#### 查找联系人
```bash
POST /chat/findContacts/{instance}

{
  "where": {
    "id": "5511999999999"
  }
}
```

省略`id`参数可列出所有联系人。

#### 查找消息
```bash
POST /chat/findMessages/{instance}

{
  "where": {
    "key": {
      "remoteJid": "5511999999999"
    }
  },
  "page": 1,
  "offset": 10
}
```

#### 查找状态消息
```bash
POST /chat/findStatusMessage/{instance}

{
  "where": {
    "remoteJid": "5511999999999@s.whatsapp.net",
    "id": "MESSAGE_ID"
  },
  "page": 1,
  "offset": 10
}
```

#### 查找聊天记录
```bash
POST /chat/findChats/{instance}
```

---

### 呼叫功能

#### 模拟电话呼叫
```bash
POST /call/offer/{instance}

{
  "number": "5511999999999",
  "isVideo": false,
  "callDuration": 3
}
```

模拟向指定号码发起电话呼叫。`callDuration`参数以秒为单位。

---

### 标签管理

#### 查找标签
```bash
GET /label/findLabels/{instance}
```

#### 添加/删除标签
```bash
POST /label/handleLabel/{instance}

{
  "number": "5511999999999",
  "labelId": "label_id_here",
  "action": "add"
}
```

**操作选项：** `add`（添加）、`remove`（删除）

---

### 个人资料设置

#### 获取企业资料
```bash
POST /chat/fetchBusinessProfile/{instance}

{ "number": "5511999999999" }
```

#### 获取个人资料信息
```bash
POST /chat/fetchProfile/{instance}

{ "number": "5511999999999" }
```

#### 更新个人资料名称
```bash
POST /chat/updateProfileName/{instance}

{ "name": "My Bot Name" }
```

#### 更新个人资料状态
```bash
POST /chat/updateProfileStatus/{instance}

{ "status": "Available 24/7" }
```

#### 更新个人资料图片
```bash
POST /chat/updateProfilePicture/{instance}

{ "picture": "https://example.com/avatar.jpg" }
```

#### 删除个人资料图片
```bash
DELETE /chat/removeProfilePicture/{instance}
```

#### 获取隐私设置
```bash
GET /chat/fetchPrivacySettings/{instance}
```

#### 更新隐私设置
```bash
POST /chat/updatePrivacySettings/{instance}

{
  "readreceipts": "all",
  "profile": "all",
  "status": "contacts",
  "online": "all",
  "last": "contacts",
  "groupadd": "none"
}
```

**隐私设置选项：**
- `readreceipts`：`all`（全部显示）、`none`（不显示）
- `profile`：`all`（全部显示）、`contacts`（仅显示联系人）、`contact_blacklist`（仅显示黑名单联系人）
- `status`：`all`（全部显示）、`contacts`（仅显示联系人）、`contact_blacklist`（仅显示黑名单联系人）
- `online`：`all`（全部显示）、`match_last_seen`（仅显示最后联系时间）
- `last`：`all`（全部显示）、`contacts`（仅显示联系人）、`contact_blacklist`（仅显示黑名单联系人）
- `groupadd`：`all`（全部显示）、`contacts`（仅显示联系人）、`contact_blacklist`（仅显示黑名单联系人）

---

### 群组管理

#### 创建群组
```bash
POST /group/create/{instance}

{
  "subject": "Group Name",
  "description": "Group description (optional)",
  "participants": [
    "5531900000000",
    "5531900000000"
  ]
}
```

#### 更新群组图片
```bash
POST /group/updateGroupPicture/{instance}?groupJid={groupJid}

{ "image": "https://example.com/group-photo.png" }
```

#### 更新群组名称
```bash
POST /group/updateGroupSubject/{instance}?groupJid={groupJid}

{ "subject": "New Group Name" }
```

#### 更新群组描述
```bash
POST /group/updateGroupDescription/{instance}?groupJid={groupJid}

{ "description": "New group description" }
```

#### 获取群组邀请码
```bash
GET /group/inviteCode/{instance}?groupJid={groupJid}
```

#### 取消群组邀请
```bash
POST /group/revokeInviteCode/{instance}?groupJid={groupJid}
```

#### 发送群组邀请链接
```bash
POST /group/sendInvite/{instance}

{
  "groupJid": "999999999@g.us",
  "description": "Join my WhatsApp group:",
  "numbers": ["5511999999999"]
}
```

#### 通过邀请码查找群组
```bash
GET /group/inviteInfo/{instance}?inviteCode={inviteCode}
```

#### 通过JID查找群组
```bash
GET /group/findGroupInfos/{instance}?groupJid={groupJid}
```

#### 查找所有群组
```bash
GET /group/fetchAllGroups/{instance}
# Optional: ?getParticipants=true
```

#### 查找群组成员
```bash
GET /group/participants/{instance}?groupJid={groupJid}
```

#### 更新群组成员
```bash
POST /group/updateParticipant/{instance}?groupJid={groupJid}

{
  "action": "add",
  "participants": ["5511999999999"]
}
```

**操作选项：** `add`（添加成员）、`remove`（删除成员）、`promote`（提升成员权限）、`demote`（降低成员权限）

#### 更新群组设置
```bash
POST /group/updateSetting/{instance}?groupJid={groupJid}

{ "action": "announcement" }
```

**设置选项：**
- `announcement`：仅管理员可发送消息 |
- `not_announcement`：所有成员均可发送消息 |
- `locked`：仅管理员可编辑群组信息 |
- `unlocked`：所有成员均可编辑群组信息

#### 设置消息自动消失功能
```bash
POST /group/toggleEphemeral/{instance}?groupJid={groupJid}

{ "expiration": 86400 }
```

**消息消失时间（秒）：**
- `0`：不启用 |
- `86400`：24小时 |
- `604800`：7天 |
- `7776000`：90天 |

#### 退出群组
```bash
DELETE /group/leaveGroup/{instance}?groupJid={groupJid}
```

---

### 集成 - 事件通知

#### Webhook
```bash
# Set Webhook
POST /webhook/set/{instance}

{
  "webhook": {
    "enabled": true,
    "url": "https://webhook.site/your-id",
    "headers": {
      "autorization": "Bearer TOKEN",
      "Content-Type": "application/json"
    },
    "byEvents": false,
    "base64": false,
    "events": [
      "APPLICATION_STARTUP",
      "QRCODE_UPDATED",
      "MESSAGES_UPSERT",
      "MESSAGES_UPDATE",
      "MESSAGES_DELETE",
      "SEND_MESSAGE",
      "CONTACTS_UPDATE",
      "PRESENCE_UPDATE",
      "CHATS_UPDATE",
      "CHATS_DELETE",
      "GROUPS_UPSERT",
      "GROUP_UPDATE",
      "GROUP_PARTICIPANTS_UPDATE",
      "CONNECTION_UPDATE",
      "LABELS_EDIT",
      "LABELS_ASSOCIATION",
      "CALL",
      "TYPEBOT_START",
      "TYPEBOT_CHANGE_STATUS"
    ]
  }
}

# Find Webhook
GET /webhook/find/{instance}
```

**关键参数：**
- `byEvents`：如果设置为`true`，则按事件类型发送通知到不同URL |
- `base64`：如果设置为`true`，媒体文件将以Base64编码的形式包含在请求体中

#### WebSocket
```bash
POST /websocket/set/{instance}

{
  "websocket": {
    "enabled": true,
    "events": ["MESSAGES_UPSERT", "CONNECTION_UPDATE"]
  }
}

GET /websocket/find/{instance}
```

#### RabbitMQ
```bash
POST /rabbitmq/set/{instance}

{
  "rabbitmq": {
    "enabled": true,
    "events": ["MESSAGES_UPSERT", "CONNECTION_UPDATE"]
  }
}

GET /rabbitmq/find/{instance}
```

#### SQS（Amazon）
```bash
POST /sqs/set/{instance}

{
  "sqs": {
    "enabled": true,
    "events": ["MESSAGES_UPSERT", "CONNECTION_UPDATE"]
  }
}

GET /sqs/find/{instance}
```

#### NATS
```bash
POST /nats/set/{instance}
GET /nats/find/{instance}
```
与SQS/RabbitMQ使用相同的请求体结构。

#### Pusher
```bash
POST /pusher/set/{instance}
GET /pusher/find/{instance}
```
与SQS/RabbitMQ使用相同的请求体结构。

**支持的事件类型（所有传输方式）：**
`APPLICATION_STARTUP`、`QRCODE_updated`、`MESSAGES_SET`、`MESSAGES_UPSERT`、`MESSAGES_UPDATE`、`MESSAGES_DELETE`、`SEND_MESSAGE`、`CONTACTS_SET`、`CONTACTS_UPSERT`、`CONTACTS_UPDATE`、`PRESENCE_UPDATE`、`CHATS_SET`、`CHATS_UPSERT`、`CHATS_UPDATE`、`CHATS_DELETE`、`GROUPS_UPSERT`、`GROUP_UPDATE`、`GROUP_PARTICIPANTS_UPDATE`、`CONNECTION_UPDATE`、`LABELS_EDIT`、`LABELS_ASSOCIATION`、`CALL`、`TYPEBOT_START`、`TYPEBOT_CHANGE_STATUS`

---

### 集成 - 聊天机器人

所有聊天机器人的集成都遵循相同的模式，包括配置设置、会话管理、CRUD操作和触发器配置。

**通用触发器选项（所有聊天机器人）：**
```json
{
  "triggerType": "keyword",
  "triggerOperator": "equals",
  "triggerValue": "hello",
  "expire": 20,
  "keywordFinish": "#SAIR",
  "delayMessage": 1000,
  "unknownMessage": "Message not recognized",
  "listeningFromMe": false,
  "stopBotFromMe": false,
  "keepOpen": false,
  "debounceTime": 10,
  "ignoreJids": []
}
```

| 参数 | 描述 |
|-------|-------------|
| `triggerType` | `all`（每条消息触发）或`keyword`（匹配特定关键词触发） |
| `triggerOperator` | `contains`（包含）、`equals`（等于）、`startsWith`（以...开头）、`endsWith`（以...结尾）、`regex`（正则表达式匹配） |
| `triggerValue` | 需要匹配的关键词/模式 |
| `expire` | 会话超时时间（分钟） |
| `keywordFinish` | 用于结束机器人会话的关键词 |
| `delayMessage` | 消息发送间隔（毫秒） |
| `unknownMessage` | 未识别输入时的响应内容 |
| `listeningFromMe` | 处理来自您的消息 |
| `stopBotFromMe` | 当您发送消息时暂停机器人 |
| `keepOpen` | 会话结束后保持连接状态 |
| `debounceTime` | 消息发送的延迟间隔（秒） |
| `ignoreJids` | 需要忽略的JID列表（例如`"@g.us"`表示忽略群组消息）

#### Chatwoot
```bash
# Set Chatwoot
POST /chatwoot/set/{instance}

{
  "enabled": true,
  "accountId": "1",
  "token": "CHATWOOT_TOKEN",
  "url": "https://chatwoot.yourdomain.com",
  "signMsg": true,
  "reopenConversation": true,
  "conversationPending": false,
  "nameInbox": "evolution",
  "mergeBrazilContacts": true,
  "importContacts": true,
  "importMessages": true,
  "daysLimitImportMessages": 2,
  "signDelimiter": "\n",
  "autoCreate": true,
  "organization": "BOT",
  "logo": "https://example.com/logo.png",
  "ignoreJids": ["@g.us"]
}

# Find Chatwoot
GET /chatwoot/find/{instance}
```

#### Typebot
```bash
# Create Typebot
POST /typebot/create/{instance}

{
  "enabled": true,
  "url": "https://typebot.yourdomain.com",
  "typebot": "my-typebot-flow-id",
  "triggerType": "keyword",
  "triggerOperator": "regex",
  "triggerValue": "^atend.*",
  "expire": 20,
  "keywordFinish": "#SAIR",
  "delayMessage": 1000,
  "unknownMessage": "Message not recognized",
  "listeningFromMe": false,
  "stopBotFromMe": false,
  "keepOpen": false,
  "debounceTime": 10
}

# Find/Fetch/Update/Delete
GET  /typebot/find/{instance}
GET  /typebot/fetch/{typebotId}/{instance}
PUT  /typebot/update/{typebotId}/{instance}
DELETE /typebot/delete/{typebotId}/{instance}

# Start Typebot manually
POST /typebot/start/{instance}

{
  "url": "https://typebot.yourdomain.com",
  "typebot": "flow-id",
  "remoteJid": "5511999999999@s.whatsapp.net",
  "startSession": false,
  "variables": [
    { "name": "pushName", "value": "User Name" }
  ]
}

# Change session status
POST /typebot/changeStatus/{instance}
{ "remoteJid": "5511999999999@s.whatsapp.net", "status": "closed" }

# Fetch sessions
GET /typebot/fetchSessions/{typebotId}/{instance}

# Default settings
POST /typebot/settings/{instance}
GET  /typebot/fetchSettings/{instance}

{
  "expire": 20,
  "keywordFinish": "#SAIR",
  "delayMessage": 1000,
  "unknownMessage": "Not recognized",
  "listeningFromMe": false,
  "stopBotFromMe": false,
  "keepOpen": false,
  "debounceTime": 10,
  "ignoreJids": [],
  "typebotIdFallback": "fallback-typebot-id"
}
```

**会话状态：** `opened`（打开）、`paused`（暂停）、`closed`（关闭）

#### OpenAI
```bash
# Set Credentials
POST /openai/creds/{instance}
{ "name": "apikey", "apiKey": "sk-proj-..." }

GET /openai/creds/{instance}
DELETE /openai/creds/{openaiCredsId}/{instance}

# Create Bot (Assistant or Chat Completion)
POST /openai/create/{instance}

{
  "enabled": true,
  "openaiCredsId": "creds-id",
  "botType": "assistant",
  // For assistants:
  "assistantId": "asst_XXXXX",
  "functionUrl": "https://n8n.site.com",
  // For chatCompletion:
  "model": "gpt-4o",
  "systemMessages": ["You are a helpful assistant."],
  "assistantMessages": ["Hello, how can I help?"],
  "userMessages": ["Hello!"],
  "maxTokens": 300,
  // Trigger options...
  "triggerType": "keyword",
  "triggerOperator": "equals",
  "triggerValue": "ai"
}

# Find/Fetch/Update/Delete
GET  /openai/find/{instance}
GET  /openai/fetch/{openaiBotId}/{instance}
PUT  /openai/update/{openaiBotId}/{instance}
DELETE /openai/delete/{openaiBotId}/{instance}

# Session management
POST /openai/changeStatus/{instance}
GET  /openai/fetchSessions/{openaiBotId}/{instance}

# Default settings
POST /openai/settings/{instance}
GET  /openai/fetchSettings/{instance}
```

**机器人类型：** `assistant`（助手）、`chatCompletion`（聊天完成）

#### Dify
```bash
POST /dify/create/{instance}

{
  "enabled": true,
  "botType": "chatBot",
  "apiUrl": "http://dify.site.com/v1",
  "apiKey": "app-123456",
  // Trigger options...
}

GET  /dify/find/{instance}
GET  /dify/fetch/{difyId}/{instance}
PUT  /dify/update/{difyId}/{instance}
DELETE /dify/delete/{difyId}/{instance}

POST /dify/changeStatus/{instance}
GET  /dify/fetchSessions/{difyId}/{instance}

POST /dify/settings/{instance}
GET  /dify/fetchSettings/{instance}
```

**Dify机器人类型：** `chatBot`（聊天机器人）、`textGenerator`（文本生成器）、`agent`（代理）、`workflow`（工作流）

#### Flowise
```bash
POST /flowise/create/{instance}

{
  "enabled": true,
  "apiUrl": "http://flowise.site.com/v1",
  "apiKey": "app-123456",
  // Trigger options...
}

GET  /flowise/find/{instance}
GET  /flowise/fetch/{flowiseId}/{instance}
PUT  /flowise/update/{flowiseId}/{instance}
DELETE /flowise/delete/{flowiseId}/{instance}

POST /flowise/changeStatus/{instance}
GET  /flowise/fetchSessions/{flowiseId}/{instance}

POST /flowise/settings/{instance}
GET  /flowise/fetchSettings/{instance}
```

#### N8N
```bash
POST /n8n/create/{instance}

{
  "enabled": true,
  "apiUrl": "http://n8n.site.com/v1",
  "apiKey": "app-123456",
  // Trigger options...
}

GET  /n8n/find/{instance}
GET  /n8n/fetch/{n8nId}/{instance}
PUT  /n8n/update/{n8nId}/{instance}
DELETE /n8n/delete/{n8nId}/{instance}

POST /n8n/changeStatus/{instance}
GET  /n8n/fetchSessions/{n8nId}/{instance}

POST /n8n/settings/{instance}
GET  /n8n/fetchSettings/{instance}
```

#### Evolution Bot
```bash
POST /evolutionBot/create/{instance}

{
  "enabled": true,
  "apiUrl": "http://api.site.com/v1",
  "apiKey": "app-123456",
  // Trigger options...
}

GET  /evolutionBot/find/{instance}
GET  /evolutionBot/fetch/{evolutionBotId}/{instance}
PUT  /evolutionBot/update/{evolutionBotId}/{instance}
DELETE /evolutionBot/delete/{evolutionBotId}/{instance}

POST /evolutionBot/changeStatus/{instance}
GET  /evolutionBot/fetchSessions/{evolutionBotId}/{instance}

POST /evolutionBot/settings/{instance}
GET  /evolutionBot/fetchSettings/{instance}
```

#### Evo AI
```bash
POST /evoai/create/{instance}

{
  "enabled": true,
  "apiUrl": "http://evoai.site.com/v1",
  "apiKey": "app-123456",
  // Trigger options...
}

GET  /evoai/find/{instance}
GET  /evoai/fetch/{evoaiId}/{instance}
PUT  /evoai/update/{evoaiId}/{instance}
DELETE /evoai/delete/{evoaiId}/{instance}

POST /evoai/changeStatus/{instance}
GET  /evoai/fetchSessions/{evoaiId}/{instance}

POST /evoai/settings/{instance}
GET  /evoai/fetchSettings/{instance}
```

---

### 集成 - WhatsApp Business Cloud API

#### 发送模板消息
```bash
POST /message/sendTemplate/{instance}

{
  "number": "5511999999999",
  "name": "hello_world",
  "language": "en_US",
  "components": [
    {
      "type": "body",
      "parameters": [
        { "type": "text", "text": "John" },
        { "type": "text", "text": "email@email.com" }
      ]
    },
    {
      "type": "button",
      "sub_type": "URL",
      "index": "1",
      "parameters": [
        { "type": "text", "text": "/reset-password/1234" }
      ]
    }
  ]
}
```

#### 创建模板
```bash
POST /template/create/{instance}

{
  "name": "my_template",
  "category": "MARKETING",
  "allowCategoryChange": false,
  "language": "en_US",
  "components": [
    {
      "type": "BODY",
      "text": "Thank you {{1}}! Confirmation: {{2}}",
      "example": {
        "body_text": [["John", "860198-230332"]]
      }
    },
    {
      "type": "BUTTONS",
      "buttons": [
        { "type": "QUICK_REPLY", "text": "Unsubscribe" },
        { "type": "URL", "text": "Support", "url": "https://example.com" }
      ]
    }
  ]
}
```

**模板分类：** `AUTHENTICATION`（认证）、`MARKETING`（营销）、`UTILITY`（实用工具）

#### 查找模板
```bash
GET /template/find/{instance}
```

#### Evolution Channel Webhook
```bash
POST /webhook/evolution

{
  "numberId": "5511999999999",
  "key": {
    "remoteJid": "5511888888888",
    "fromMe": false,
    "id": "ABC1234"
  },
  "pushName": "Contact Name",
  "message": {
    "conversation": "Hello"
  },
  "messageType": "conversation"
}
```

**消息类型：** `conversation`（普通消息）、`imageMessage`（图片消息）、`videoMessage`（视频消息）、`documentMessage`（文档消息）

---

### 存储（S3/MinIO）

#### 获取媒体文件
```bash
POST /s3/getMedia/{instance}

{
  "id": "media-id",
  "type": "image",
  "messageId": "MESSAGE_ID"
}
```

#### 获取媒体文件的URL
```bash
POST /s3/getMediaUrl/{instance}

{
  "id": "media-id"
}
```

---

### 系统信息

#### 获取API版本和系统详情
```bash
GET /
```

#### 获取指标数据
```bash
GET /metrics
Authorization: Basic (METRICS_USER:password)
```

---

## 常用工作流程

### 广播消息
```bash
for number in 5511999999999 5511888888888 5511777777777; do
  curl -X POST "$EVO_API_URL/message/sendText/$EVO_INSTANCE" \
    -H "apikey: $EVO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"number\": \"$number\",
      \"text\": \"Broadcast message!\",
      \"delay\": 2000
    }"
done
```

### 自动创建群组并配置聊天机器人
```bash
# 1. Create group
curl -X POST "$EVO_API_URL/group/create/$EVO_INSTANCE" \
  -H "apikey: $EVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Support Group",
    "participants": ["5511999999999"]
  }'

# 2. Attach Typebot for auto-response
curl -X POST "$EVO_API_URL/typebot/create/$EVO_INSTANCE" \
  -H "apikey: $EVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "url": "https://typebot.yourdomain.com",
    "typebot": "support-flow-id",
    "triggerType": "all"
  }'
```

### 完整的实例设置（包括实例、Webhook和Chatwoot）
```bash
# 1. Create instance with webhook inline
curl -X POST "$EVO_API_URL/instance/create" \
  -H "apikey: $EVO_GLOBAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "support-bot",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS",
    "webhook": {
      "url": "https://n8n.yourdomain.com/webhook/evo",
      "byEvents": false,
      "base64": false,
      "events": ["MESSAGES_UPSERT", "CONNECTION_UPDATE"]
    }
  }'

# 2. Connect
curl -X GET "$EVO_API_URL/instance/connect/support-bot" \
  -H "apikey: $EVO_API_KEY"

# 3. Configure Chatwoot
curl -X POST "$EVO_API_URL/chatwoot/set/support-bot" \
  -H "apikey: $EVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "accountId": "1",
    "token": "CHATWOOT_TOKEN",
    "url": "https://chatwoot.yourdomain.com",
    "signMsg": true,
    "importContacts": true,
    "importMessages": true,
    "autoCreate": true,
    "nameInbox": "support-bot"
  }'
```

### 发送消息前检查号码是否可用
```bash
# 1. Validate numbers
curl -X POST "$EVO_API_URL/chat/whatsappNumbers/$EVO_INSTANCE" \
  -H "apikey: $EVO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "numbers": ["5511999999999", "5511888888888"] }'

# 2. Send only to valid numbers
```

---

## 发送速率限制与最佳实践

### 消息发送间隔

始终在消息之间添加延迟：
```json
{ "delay": 1200 }
```

**推荐设置：**
- 单条消息之间间隔1-2秒 |
- 批量发送之间间隔3-5秒 |
- 出现错误时采用指数级退避策略

### 错误处理

| 状态码 | 含义 |
|--------|---------|
| `200` | 成功 |
| `400` | 请求错误（检查请求参数） |
| `401` | 未经授权（检查API密钥） |
| `404` | 未找到资源 |
| `500` | 服务器错误 |

### 常见问题及解决方法

| 问题 | 解决方案 |
|-------|----------|
| 实例无法连接 | 运行`GET /instance/connect/{instance}`命令 |
| 手机号码格式错误 | 使用不带`+`的国家代码，例如`5511999999999` |
| 消息无法发送 | 检查`GET /instance/connectionState/{instance}`命令 |
| 群组操作失败 | 确认您具有管理员权限 |
| 媒体文件提取失败 | 确保已启用MongoDB或文件存储功能 |
| Chatwoot同步失败 | 检查token和URL，确认`importMessages`参数已设置 |

---

## 故障排除

### 实例无法连接
```bash
# 1. Check instances
GET /instance/fetchInstances

# 2. Restart instance
POST /instance/restart/{instance}

# 3. Reconnect
GET /instance/connect/{instance}
```

### 聊天机器人无响应
1. 确认聊天机器人已启用：运行`GET /{botType}/find/{instance}`命令 |
2. 检查触发器是否与接收到的消息匹配 |
3. 检查会话状态：运行`GET /{botType}/fetchSessions/{botId}/{instance}`命令 |
4. 重置会话状态：运行`POST /{botType}/changeStatus/{instance}`，并将`status`设置为`closed` |

### 消息无法送达
1. 检查连接状态：运行`GET /instance/connectionState/{instance}`命令 |
2. 确认电话号码格式正确（不含`+`符号且无空格） |
3. 确认接收方已安装WhatsApp |
4. 检查Webhook是否收到发送状态通知

---

## v2与v3（Evolution Go）的差异

| 特性 | v2.3 | v3（Go） |
|---------|------|---------|
| **编程语言** | Node.js/TypeScript | Go |
| **API端点** | `/message/sendText/{instance}` | `/send/text` |
| **支持的聊天机器人集成** | 7种（Typebot、OpenAI、Dify、Flowise、N8N、EvolutionBot、EvoAI） | 减少 |
| **Chatwoot集成方式** | 内置集成 | 作为独立服务 |
| **事件通知方式** | 6种（Webhook、WebSocket、RabbitMQ、SQS、NATS、Pusher） | 减少 |
| **列表和按钮功能** | 支持 | 已弃用 |
| **PTV（圆形视频）** | 支持 | 支持 |
| **状态/故事功能** | 支持 | 支持 |
| **模板功能** | 通过Business Cloud API实现 | 通过Business Cloud API实现 |
| **S3存储** | 内置支持 | 需单独配置 |

---

## 资源链接

- **Evolution API**：https://github.com/EvolutionAPI/evolution-api |
- **文档**：https://doc.evolution-api.com |
- **Chatwoot**：https://www.chatwoot.com |
- **Typebot**：https://typebot.io |
- **WhatsApp Business API**：https://developers.facebook.com/docs/whatsapp |

---

## 使用建议

1. **操作前务必检查连接状态** |
2. **使用延迟机制**以避免达到发送速率限制（每条消息之间至少间隔1.2秒） |
3. **将API密钥存储在环境变量中，切勿硬编码** |
4. **使用Webhook的`CONNECTION_UPDATE`事件处理连接断开情况** |
5. **在批量发送前使用`whatsappNumbers`函数验证电话号码格式** |
6. **在聊天机器人中设置`debounceTime`以控制消息发送频率** |
7. **在聊天机器人中设置`ignoreJids: ["@g.us"]`以忽略群组消息** |
8. **在切换触发器类型时，先使用`triggerType: "keyword"`进行测试** |
9. **监控会话状态**：过期会话可能导致聊天机器人停止响应 |
10. **使用Chatwoot实现人工干预功能**