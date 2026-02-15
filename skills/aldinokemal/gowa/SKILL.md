---
name: gowa
description: 通过 GOWA（Go WhatsApp Web Multi-Device）REST API 与 WhatsApp 进行交互，以实现自动化操作。支持发送带有“@everyone”提及的消息、图片、文档，以及进行群组管理等功能。在生产环境中，请始终使用 REST 模式（http://localhost:3000）。
user-invocable: true
command-dispatch: model
---

# GOWA - 通过 REST API 实现 WhatsApp 自动化

使用 GOWA（Go WhatsApp Web Multi-Device）REST API 与 WhatsApp 进行交互，以完成自动化任务。

## 安装与设置

GOWA 可在以下地址获取：https://github.com/aldinokemal/go-whatsapp-web-multidevice

### 下载

访问 [发布页面](https://github.com/aldinokemal/go-whatsapp-web-multidevice/releases)，下载适合您操作系统和架构的 zip 文件。  
发布文件的命名格式为：`whatsapp_version_OS_arch.zip`  
支持的平台：`linux` (amd64/arm64/386)、`darwin` (amd64/arm64)、`windows` (amd64/386)

### 运行 REST 服务器

```bash
./gowa rest
```

服务器默认运行在 `http://localhost:3000` 上。

### 登录（首次使用）

在浏览器中打开 `http://localhost:3000`，使用手机上的 WhatsApp 扫描 QR 码以关联设备。

## 生产环境设置

**GOWA 以 REST 模式运行：**
- 基本 URL：`http://localhost:3000`
- GOWA 会自动连接到数据库中存储的设备——单设备设置时不需要 `X-Device-Id` 头部信息。

**⚠️ 重要提示：** 仅使用 REST API（端口 3000），切勿使用 MCP 模式——所有调度器和自动化功能都依赖于 REST API。

## 快速示例

### 幽灵提及（@ 符号不显示）
```bash
curl -X POST http://localhost:3000/send/message \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "120363040656010581@g.us",
    "message": "Important announcement",
    "mentions": ["@everyone"]
  }'
```

### 发送文本消息
```bash
curl -X POST http://localhost:3000/send/message \
  -H "Content-Type: application/json" \
  -d '{"phone": "628123456789", "message": "Hello!"}'
```

### 发送图片
```bash
curl -X POST http://localhost:3000/send/image \
  -F "phone=628xxx" \
  -F "caption=Photo" \
  -F "image=@/path/to/image.jpg"
```

### 检查状态
```bash
curl http://localhost:3000/app/status | jq .
```

## 完整的 API 操作

### 消息

**发送带有幽灵提及的文本消息：**
- 端点：`POST /send/message`
- 请求体：`{"phone": "group@g.us", "message": "text", "mentions": ["@everyone"]}`  
- `@everyone` 会提及所有成员，且消息文本中不会显示 @ 符号 ✅

**回复消息：**
- 请求体：`{"phone": "...", "message": "...", "reply_message_id": "msg_id"}`

**发送临时消息（86400 秒后自动消失）：**
- 请求体：`{"phone": "...", "message": "...", "duration": 86400}`

**转发消息：**
- 请求体：`{"phone": "...", "message": "...", "is_forwarded": true}`

### 媒体文件

**发送图片：**
- 端点：`POST /send/image`
- 请求参数：`phone`、`caption`、`image`（文件路径）、`compress`（布尔值）

**发送文档：**
- 端点：`POST /send/file`
- 请求参数：`phone`、`caption`、`file`（文件路径）

**发送视频：**
- 端点：`POST /send/video`
- 请求参数：`phone`、`caption`、`video`（文件路径）、`compress`（布尔值）

**发送音频：**
- 端点：`POST /send/audio`
- 请求参数：`phone`、`audio`（音频文件路径）

**发送贴纸：**
- 端点：`POST /send/sticker`
- 请求参数：`phone`、`sticker`（贴纸文件路径，会自动转换为 WebP 格式）

**发送联系人信息：**
- 端点：`POST /send/contact`
- 请求体：`{"phone": "...", "contact_name": "...", "contact_phone": "..."}`

**发送位置信息：**
- 端点：`POST /send/location`
- 请求体：`{"phone": "...", "latitude": 0.0, "longitude": 0.0}`

**发送链接：**
- 端点：`POST /send/link`
- 请求体：`{"phone": "...", "link": "...", "caption": "..."}`

**发送投票：**
- 端点：`POST /send/poll`
- 请求体：`{"phone": "...", "question": "...", "options": ["A", "B"]}`

### 连接与状态

**获取状态：**
- `GET /app/status`
- 返回值：`{"is_connected": true, "is_logged_in": true}`

**重新连接：**
- `GET /app/reconnect`

**登出：**
- `GET /app/logout`

**获取 QR 码（用于登录）：**
- `GET /app/login`
- 返回值：PNG 格式的 QR 码图片

**使用配对码登录：**
- `GET /app/login-with-code?phone=628xxx`

### 组群

**列出我的群组：**
- `GET /user/my/groups`
- 返回值：`{"results: {data: [...]}}` —— 群组信息存储在 `.results.data` 中  
- 示例：`curl ... | jq '.results.data[] | {Name, JID, Members: .Participants | length}'`
- 最多可列出 500 个群组（受 WhatsApp 协议限制）

**获取群组信息：**
- `GET /group/info?group_jid=xxx@g.us`

**创建群组：**
- `POST /group`
- 请求体：`{"name": "群组名称", "participants": ["628xxx@s.whatsapp.net"]`

**获取群组成员：**
- `GET /group/participants?group_jid=xxx@g.us`

**添加成员：**
- `POST /group/participants`
- 请求体：`{"group_jid": "...", "participants": ["628xxx@s.whatsapp.net"]`

**移除成员：**
- `POST /group/participants/remove`
- 请求体：`{"group_jid": "...", "participants": ["628xxx@s.whatsapp.net"]`

**提升成员为管理员：**
- `POST /group/participants/promote`
- 请求体：`{"group_jid": "...", "participants": ["628xxx@s.whatsapp.net"]`

**降级成员为普通成员：**
- `POST /group/participants/demote`
- 请求体：`{"group_jid": "...", "participants": ["628xxx@s.whatsapp.net"]`

**离开群组：**
- `POST /group/leave`
- 请求体：`{"group_jid": "..."`

**设置群组图片：**
- `POST /group/photo`
- 请求参数：`group_jid`、`photo`（图片文件路径）

**设置群组名称：**
- `POST /group/name`
- 请求体：`{"group_jid": "...", "name": "..."`

**设置群组描述：**
- `POST /group/topic`
- 请求体：`{"group_jid": "...", "topic": "..."`

**获取群组邀请链接：**
- `GET /group/invite-link?group_jid=xxx@g.us`

**通过链接加入群组：**
- `POST /group/join-with-link`
- 请求体：`{"link": "https://chat.whatsapp.com/..."}`

### 联系人与聊天记录

**列出联系人：**
- `GET /user/my/contacts`

**获取聊天记录：**
- `GET /chats`

**获取用户信息：**
- `GET /user/info?phone=628xxx`

**检查用户是否存在：**
- `GET /user/check?phone=628xxx`

### 消息操作

**撤销/删除消息：**
- `POST /message/{message_id}/revoke`

**对消息做出反应：**
- `POST /message/{message_id}/reaction`
- 请求体：`{"emoji": "👍`）

**编辑消息：**
- `POST /message/{message_id}/update`
- 请求体：`{"message": "编辑后的文本"}`

**标记消息为已读：**
- `POST /message/{message_id}/read`

**将消息标记为星标：**
- `POST /message/{message_id}/star`

**下载媒体文件：**
- `GET /message/{message_id}/download`

## 手机号码格式

- **用户 JID：** `628123456789@s.whatsapp.net`
- **群组 JID：** `120363040656010581@g.us`
- **仅包含电话号码：** `628123456789`（不包含 + 符号）

## 幽灵提及功能

**工作原理：**
- 在 `/send/message` 请求中使用 `{"mentions": ["@everyone"]`  
- 所有群组成员都会收到通知  
- 消息文本中不会显示 @ 符号（实现真正的“幽灵提及”效果）  
- 已经过测试并确认可用 ✅

**调度器示例：**
```bash
curl -s -X POST http://localhost:3000/send/message \
  -H 'Content-Type: application/json' \
  -d '{"phone": "120363040656010581@g.us", "message": "Reminder text", "mentions": ["@everyone"]}' | jq .
```

## API 参考文档

完整的 OpenAPI 3.0 规范请参考：
- OpenAPI 文档：https://raw.githubusercontent.com/aldinokemal/go-whatsapp-web-multidevice/refs/heads/main/docs/openapi.yaml  
- GitHub 项目：https://github.com/aldinokemal/go-whatsapp-web-multidevice

## 注意事项：

- 发送前会自动压缩图片和视频  
- 图片会自动转换为 WebP 格式以适应贴纸显示  
- 最多可查询 500 个群组（受 WhatsApp 协议限制）  
- 所有媒体文件可通过文件上传或 URL 发送  
- 支持设置消息的可见时长（临时消息）  
- 多设备支持（通过 `X-Device-Id` 头部信息实现）  
- 由 @aldinokemal 开发：https://github.com/aldinokemal/go-whatsapp-web-multidevice