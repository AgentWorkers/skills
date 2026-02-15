---
name: slack
description: |
  Slack API integration with managed OAuth. Send messages, manage channels, search conversations, and interact with Slack workspaces. Use this skill when users want to post messages, list channels, get user info, or automate Slack workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Slack

您可以使用托管的 OAuth 认证来访问 Slack API。该 API 允许您发送消息、管理频道、列出用户以及自动化 Slack 工作流程。

## 快速入门

```bash
# Post a message to a channel
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456789', 'text': 'Hello from Maton!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/slack/{method}
```

该网关会将请求代理到 `slack.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Slack OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=slack&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'slack'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "slack",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

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

如果您有多个 Slack 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456789', 'text': 'Hello!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 发送消息

```bash
POST /slack/api/chat.postMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "text": "Hello, world!"
}
```

**使用 Markdown 格式发送消息：**

```bash
POST /slack/api/chat.postMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "blocks": [
    {"type": "section", "text": {"type": "mrkdwn", "text": "*Bold* and _italic_"}}
  ]
}
```

### 回复帖子

```bash
POST /slack/api/chat.postMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "thread_ts": "1234567890.123456",
  "text": "This is a reply in a thread"
}
```

### 更新消息

```bash
POST /slack/api/chat.update
Content-Type: application/json

{
  "channel": "C0123456789",
  "ts": "1234567890.123456",
  "text": "Updated message"
}
```

### 删除消息

```bash
POST /slack/api/chat.delete
Content-Type: application/json

{
  "channel": "C0123456789",
  "ts": "1234567890.123456"
}
```

### 列出频道

```bash
GET /slack/api/conversations.list?types=public_channel,private_channel
```

### 获取频道信息

```bash
GET /slack/api/conversations.info?channel=C0123456789
```

### 获取频道成员

```bash
GET /slack/api/conversations.members?channel=C0123456789&limit=100
```

### 列出频道中的消息

```bash
GET /slack/api/conversations.history?channel=C0123456789&limit=100
```

### 获取帖子回复

```bash
GET /slack/api/conversations.replies?channel=C0123456789&ts=1234567890.123456
```

### 列出用户

```bash
GET /slack/api/users.list
```

### 获取用户信息

```bash
GET /slack/api/users.info?user=U0123456789
```

### 搜索消息

```bash
GET /slack/api/search.messages?query=keyword
```

### 打开私信对话

```bash
POST /slack/api/conversations.open
Content-Type: application/json

{
  "users": "U0123456789"
}
```

### 添加表情反应

```bash
POST /slack/api/reactions.add
Content-Type: application/json

{
  "channel": "C0123456789",
  "name": "thumbsup",
  "timestamp": "1234567890.123456"
}
```

### 上传文件

```bash
POST /slack/api/files.upload
Content-Type: multipart/form-data

channels=C0123456789
content=file content here
filename=example.txt
```

### 验证 API 密钥

获取当前用户和团队信息：

```bash
GET /slack/api/auth.test
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/slack/api/chat.postMessage', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({ channel: 'C0123456', text: 'Hello!' })
});
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/slack/api/chat.postMessage',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'channel': 'C0123456', 'text': 'Hello!'}
)
```

## 注意事项

- 频道 ID 以 `C`（公共频道）、`G`（私有/组频道）或 `D`（私信）开头。
- 用户 ID 以 `U` 开头，团队 ID 以 `T` 开头。
- 消息时间戳（`ts`）用作唯一标识符。
- 使用 `mrkdwn` 格式进行 Slack 特色的 Markdown 格式化。
- 帖子回复使用 `thread_ts` 来引用父消息。
- **重要提示：** 当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 选项来禁用全局解析。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析，这可能导致 “无效的 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Slack 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次请求） |
| 4xx/5xx | 来自 Slack API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `slack` 开头。例如：
   - 正确：`https://gateway.maton.ai/slack/api/chat.postMessage`
   - 错误：`https://gateway.maton.ai/api/chat.postMessage`

## 资源

- [Slack API 概述](https://api.slack.com/apis)
- [发送消息](https://api.slack.com/methods/chat.postMessage)
- [更新消息](https://api.slack.com/methods/chat.update)
- [删除消息](https://api.slack.com/methods/chat.delete)
- [列出频道](https://api.slack.com/methods/conversations.list)
- [频道历史记录](https://api.slack.com/methods/conversations.history)
- [帖子回复](https://api.slack.com/methods/conversations.replies)
- [列出用户](https://api.slack.com/methods/users.list)
- [获取用户信息](https://api.slack.com/methods/users.info)
- [搜索消息](https://api.slack.com/methods/search.messages)
- [Block Kit 参考](https://api.slack.com/reference/block-kit)
- [LLM 参考](https://docs.slack.dev/llms.txt)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)