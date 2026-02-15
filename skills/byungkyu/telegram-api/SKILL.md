---
name: telegram
description: |
  Telegram Bot API integration with managed authentication. Send messages, manage chats, handle updates, and interact with users through your Telegram bot. Use this skill when users want to send messages, create polls, manage bot commands, or interact with Telegram chats. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Telegram机器人API

您可以使用托管的身份验证来访问Telegram机器人API。通过您的Telegram机器人发送消息、图片、投票、位置等信息。

## 快速入门

```bash
# Get bot info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/telegram/:token/getMe')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/telegram/:token/{method}
```

`:token`占位符会自动替换为从连接配置中获取的机器人令牌。请将`{method}`替换为Telegram机器人API的方法名称（例如：`sendMessage`、`getUpdates`）。

## 身份验证

所有请求都需要在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Telegram机器人连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=telegram&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'telegram'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "e8f5078d-e507-4139-aabe-1615181ea8fc",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T10:37:21.053942Z",
    "last_updated_time": "2026-02-07T10:37:59.881901Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "telegram",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成机器人令牌的配置。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个Telegram连接（多个机器人），请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/telegram/:token/getMe')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'e8f5078d-e507-4139-aabe-1615181ea8fc')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 机器人信息

#### 获取机器人信息

```bash
GET /telegram/:token/getMe
```

返回有关机器人的信息。

**响应：**
```json
{
  "ok": true,
  "result": {
    "id": 8523474253,
    "is_bot": true,
    "first_name": "Maton",
    "username": "maton_bot",
    "can_join_groups": true,
    "can_read_all_group_messages": true,
    "supports_inline_queries": true
  }
}
```

### 获取更新

#### 获取更新（长轮询）

```bash
POST /telegram/:token/getUpdates
Content-Type: application/json

{
  "limit": 100,
  "timeout": 30,
  "offset": 625435210
}
```

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| offset | 整数 | 否 | 要返回的第一个更新ID |
| limit | 整数 | 否 | 更新数量（1-100，默认为100） |
| timeout | 整数 | 否 | 长轮询超时时间（以秒为单位） |
| allowed_updates | 数组 | 否 | 要接收的更新类型 |

#### 获取Webhook信息

```bash
GET /telegram/:token/getWebhookInfo
```

#### 设置Webhook

```bash
POST /telegram/:token/setWebhook
Content-Type: application/json

{
  "url": "https://example.com/webhook",
  "allowed_updates": ["message", "callback_query"],
  "secret_token": "your_secret_token"
}
```

#### 删除Webhook

```bash
POST /telegram/:token/deleteWebhook
Content-Type: application/json

{
  "drop_pending_updates": true
}
```

### 发送消息

#### 发送文本消息

```bash
POST /telegram/:token/sendMessage
Content-Type: application/json

{
  "chat_id": 6442870329,
  "text": "Hello, World!",
  "parse_mode": "HTML"
}
```

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| chat_id | 整数/字符串 | 是 | 目标聊天ID或@用户名 |
| text | 字符串 | 是 | 消息文本（1-4096个字符） |
| parse_mode | 字符串 | 否 | `HTML`、`Markdown`或`MarkdownV2` |
| reply_markup | 对象 | 否 | 回复键盘样式 |
| reply_parameters | 对象 | 否 | 回复特定消息 |

**使用HTML格式：**

```bash
POST /telegram/:token/sendMessage
Content-Type: application/json

{
  "chat_id": 6442870329,
  "text": "<b>Bold</b> and <i>italic</i> with <a href=\"https://example.com\">link</a>",
  "parse_mode": "HTML"
}
```

**使用内联键盘：**

```bash
POST /telegram/:token/sendMessage
Content-Type: application/json

{
  "chat_id": 6442870329,
  "text": "Choose an option:",
  "reply_markup": {
    "inline_keyboard": [
      [
        {"text": "Option 1", "callback_data": "opt1"},
        {"text": "Option 2", "callback_data": "opt2"}
      ],
      [
        {"text": "Visit Website", "url": "https://example.com"}
      ]
    ]
  }
}
```

#### 发送图片

```bash
POST /telegram/:token/sendPhoto
Content-Type: application/json

{
  "chat_id": 6442870329,
  "photo": "https://example.com/image.jpg",
  "caption": "Image caption"
}
```

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| chat_id | 整数/字符串 | 是 | 目标聊天ID |
| photo | 字符串 | 是 | 图片URL或文件ID |
| caption | 字符串 | 否 | 图片说明（0-1024个字符） |
| parse_mode | 字符串 | 否 | 说明解析模式 |

#### 发送文档

```bash
POST /telegram/:token/sendDocument
Content-Type: application/json

{
  "chat_id": 6442870329,
  "document": "https://example.com/file.pdf",
  "caption": "Document caption"
}
```

#### 发送视频

```bash
POST /telegram/:token/sendVideo
Content-Type: application/json

{
  "chat_id": 6442870329,
  "video": "https://example.com/video.mp4",
  "caption": "Video caption"
}
```

#### 发送音频

```bash
POST /telegram/:token/sendAudio
Content-Type: application/json

{
  "chat_id": 6442870329,
  "audio": "https://example.com/audio.mp3",
  "caption": "Audio caption"
}
```

#### 发送位置

```bash
POST /telegram/:token/sendLocation
Content-Type: application/json

{
  "chat_id": 6442870329,
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

#### 发送联系人信息

```bash
POST /telegram/:token/sendContact
Content-Type: application/json

{
  "chat_id": 6442870329,
  "phone_number": "+1234567890",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### 发送投票

```bash
POST /telegram/:token/sendPoll
Content-Type: application/json

{
  "chat_id": 6442870329,
  "question": "What is your favorite color?",
  "options": [
    {"text": "Red"},
    {"text": "Blue"},
    {"text": "Green"}
  ],
  "is_anonymous": false
}
```

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| chat_id | 整数/字符串 | 是 | 目标聊天ID |
| question | 字符串 | 是 | 投票问题（1-300个字符） |
| options | 数组 | 是 | 投票选项（2-10个选项） |
| is_anonymous | 布尔值 | 否 | 是否匿名投票（默认为true） |
| type | 字符串 | 否 | `regular`或`quiz` |
| allows_multiple_answers | 布尔值 | 是否允许多个答案 |
| correct_option_id | 整数 | 否 | 正确答案（用于测验） |

#### 发送骰子结果

```bash
POST /telegram/:token/sendDice
Content-Type: application/json

{
  "chat_id": 6442870329,
  "emoji": "🎲"
}
```

支持的emoji：🎲 🎯 🎳 🏀 ⚽ 🎰

### 编辑消息

#### 编辑消息文本

```bash
POST /telegram/:token/editMessageText
Content-Type: application/json

{
  "chat_id": 6442870329,
  "message_id": 123,
  "text": "Updated message text"
}
```

#### 编辑消息说明

```bash
POST /telegram/:token/editMessageCaption
Content-Type: application/json

{
  "chat_id": 6442870329,
  "message_id": 123,
  "caption": "Updated caption"
}
```

#### 编辑消息回复样式

```bash
POST /telegram/:token/editMessageReplyMarkup
Content-Type: application/json

{
  "chat_id": 6442870329,
  "message_id": 123,
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "New Button", "callback_data": "new"}]
    ]
  }
}
```

#### 删除消息

```bash
POST /telegram/:token/deleteMessage
Content-Type: application/json

{
  "chat_id": 6442870329,
  "message_id": 123
}
```

### 转发与复制

#### 转发消息

```bash
POST /telegram/:token/forwardMessage
Content-Type: application/json

{
  "chat_id": 6442870329,
  "from_chat_id": 6442870329,
  "message_id": 123
}
```

#### 复制消息

```bash
POST /telegram/:token/copyMessage
Content-Type: application/json

{
  "chat_id": 6442870329,
  "from_chat_id": 6442870329,
  "message_id": 123
}
```

### 聊天信息

#### 获取聊天信息

```bash
POST /telegram/:token/getChat
Content-Type: application/json

{
  "chat_id": 6442870329
}
```

#### 获取聊天管理员

```bash
POST /telegram/:token/getChatAdministrators
Content-Type: application/json

{
  "chat_id": -1001234567890
}
```

#### 获取聊天成员数量

```bash
POST /telegram/:token/getChatMemberCount
Content-Type: application/json

{
  "chat_id": -1001234567890
}
```

#### 获取聊天成员

```bash
POST /telegram/:token/getChatMember
Content-Type: application/json

{
  "chat_id": -1001234567890,
  "user_id": 6442870329
}
```

### 机器人命令

#### 设置我的命令

```bash
POST /telegram/:token/setMyCommands
Content-Type: application/json

{
  "commands": [
    {"command": "start", "description": "Start the bot"},
    {"command": "help", "description": "Get help"},
    {"command": "settings", "description": "Open settings"}
  ]
}
```

#### 获取我的命令

```bash
GET /telegram/:token/getMyCommands
```

#### 删除我的命令

```bash
POST /telegram/:token/deleteMyCommands
Content-Type: application/json

{}
```

### 机器人配置

#### 获取我的描述

```bash
GET /telegram/:token/getMyDescription
```

#### 设置我的描述

```bash
POST /telegram/:token/setMyDescription
Content-Type: application/json

{
  "description": "This bot helps you manage tasks."
}
```

#### 设置我的名称

```bash
POST /telegram/:token/setMyName
Content-Type: application/json

{
  "name": "Task Bot"
}
```

### 文件

#### 获取文件

```bash
POST /telegram/:token/getFile
Content-Type: application/json

{
  "file_id": "AgACAgQAAxkDAAM..."
}
```

**响应：**
```json
{
  "ok": true,
  "result": {
    "file_id": "AgACAgQAAxkDAAM...",
    "file_unique_id": "AQAD27ExGysnfVBy",
    "file_size": 7551,
    "file_path": "photos/file_0.jpg"
  }
}
```

从以下地址下载文件：`https://api.telegram.org/file/bot<token>/<file_path>`

### 回调查询

#### 回答回调查询

```bash
POST /telegram/:token/answerCallbackQuery
Content-Type: application/json

{
  "callback_query_id": "12345678901234567",
  "text": "Button clicked!",
  "show_alert": false
}
```

## 代码示例

### JavaScript

```javascript
// Send a message
const response = await fetch(
  'https://gateway.maton.ai/telegram/:token/sendMessage',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      chat_id: 6442870329,
      text: 'Hello from JavaScript!'
    })
  }
);
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

# Send a message
response = requests.post(
    'https://gateway.maton.ai/telegram/:token/sendMessage',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'chat_id': 6442870329,
        'text': 'Hello from Python!'
    }
)
print(response.json())
```

### Python (urllib)

```python
import urllib.request, os, json

data = json.dumps({
    'chat_id': 6442870329,
    'text': 'Hello from Python!'
}).encode()
req = urllib.request.Request(
    'https://gateway.maton.ai/telegram/:token/sendMessage',
    data=data,
    method='POST'
)
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
response = json.load(urllib.request.urlopen(req))
print(json.dumps(response, indent=2))
```

## 响应格式

所有Telegram机器人API的响应都遵循以下格式：

**成功：**
```json
{
  "ok": true,
  "result": { ... }
}
```

**错误：**
```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: chat not found"
}
```

## 注意事项

- `:token`会自动替换为从连接中获取的机器人令牌。
- 私人聊天的聊天ID为整数，群组的聊天ID可以为负数。
- 所有方法都支持GET和POST请求，但带有参数的方法建议使用POST。
- 文本消息的长度限制为4096个字符。
- 说明的长度限制为1024个字符。
- 投票支持2-10个选项。
- 上传文件需要使用multipart/form-data格式（为简化操作，可以使用URL）。
- 重要提示：当将curl的输出传递给`jq`或其他命令时，在某些shell环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少Telegram连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 超过请求频率限制（不同方法的限制不同） |
| 4xx/5xx | 来自Telegram机器人API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了`MATON_API_KEY`环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的URL路径以`telegram`开头。例如：
- 正确：`https://gateway.maton.ai/telegram/:token/sendMessage`
- 错误：`https://gateway.maton.ai/:token/sendMessage`

## 资源

- [Telegram机器人API文档](https://coreTelegram.org/bots/api)
- [可用方法](https://coreTelegram.org/bots/api#available-methods)
- [格式化选项](https://coreTelegram.org/bots/api#formatting-options)
- [内联键盘样式](https://coreTelegram.org/bots/api#inlinekeyboardmarkup)
- [机器人命令](https://coreTelegram.org/bots/api#setmycommands)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)