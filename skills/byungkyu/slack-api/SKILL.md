---
name: slack
description: >
  **Slack API集成与托管式OAuth**  
  支持通过OAuth身份验证与Slack进行交互，实现发送消息、管理频道、搜索对话以及操作Slack工作空间等功能。当用户需要发布消息、查看频道列表、获取用户信息或自动化Slack工作流程时，可利用此技能。对于其他第三方应用程序，建议使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Slack

您可以使用受管理的 OAuth 认证来访问 Slack API。该 API 允许您发送消息、管理频道、列出用户以及自动化 Slack 工作流程。

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

您可以在 `https://ctrl.maton.ai` 管理您的 Slack OAuth 连接。

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

---

## API 参考

### 认证

#### 认证测试

```bash
GET /slack/api/auth.test
```

返回当前用户和团队信息。

---

### 消息

#### 发送消息

```bash
POST /slack/api/chat.postMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "text": "Hello, world!"
}
```

支持使用 Markdown 格式：

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

#### 回复帖子

```bash
POST /slack/api/chat.postMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "thread_ts": "1234567890.123456",
  "text": "This is a reply in a thread"
}
```

#### 更新消息

```bash
POST /slack/api/chat.update
Content-Type: application/json

{
  "channel": "C0123456789",
  "ts": "1234567890.123456",
  "text": "Updated message"
}
```

#### 删除消息

```bash
POST /slack/api/chat.delete
Content-Type: application/json

{
  "channel": "C0123456789",
  "ts": "1234567890.123456"
}
```

#### 安排消息发送

```bash
POST /slack/api/chat.scheduleMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "text": "Scheduled message",
  "post_at": 1734567890
}
```

#### 列出已安排的消息

```bash
GET /slack/api/chat.scheduledMessages.list
```

#### 删除已安排的消息

```bash
POST /slack/api/chat.deleteScheduledMessage
Content-Type: application/json

{
  "channel": "C0123456789",
  "scheduled_message_id": "Q1234567890"
}
```

#### 获取消息的永久链接

```bash
GET /slack/api/chat.getPermalink?channel=C0123456789&message_ts=1234567890.123456
```

---

### 对话（频道）

#### 列出频道

```bash
GET /slack/api/conversations.list?types=public_channel,private_channel&limit=100
```

类型：`public_channel`（公共频道）、`private_channel`（私人频道）、`im`（直接消息）、`mpim`（群组直接消息）

#### 获取频道信息

```bash
GET /slack/api/conversations.info?channel=C0123456789
```

#### 获取频道历史记录

```bash
GET /slack/api/conversations.history?channel=C0123456789&limit=100
```

可指定时间范围：

```bash
GET /slack/api/conversations.history?channel=C0123456789&oldest=1234567890&latest=1234567899
```

#### 获取帖子回复

```bash
GET /slack/api/conversations.replies?channel=C0123456789&ts=1234567890.123456
```

#### 获取频道成员

```bash
GET /slack/api/conversations.members?channel=C0123456789&limit=100
```

#### 创建频道

```bash
POST /slack/api/conversations.create
Content-Type: application/json

{
  "name": "new-channel-name",
  "is_private": false
}
```

#### 加入频道

```bash
POST /slack/api/conversations.join
Content-Type: application/json

{
  "channel": "C0123456789"
}
```

#### 离开频道

```bash
POST /slack/api/conversations.leave
Content-Type: application/json

{
  "channel": "C0123456789"
}
```

#### 归档频道

```bash
POST /slack/api/conversations.archive
Content-Type: application/json

{
  "channel": "C0123456789"
}
```

#### 解压频道

```bash
POST /slack/api/conversations.unarchive
Content-Type: application/json

{
  "channel": "C0123456789"
}
```

#### 重命名频道

```bash
POST /slack/api/conversations.rename
Content-Type: application/json

{
  "channel": "C0123456789",
  "name": "new-name"
}
```

#### 设置频道主题

```bash
POST /slack/api/conversations.setTopic
Content-Type: application/json

{
  "channel": "C0123456789",
  "topic": "Channel topic here"
}
```

#### 设置频道用途

```bash
POST /slack/api/conversations.setPurpose
Content-Type: application/json

{
  "channel": "C0123456789",
  "purpose": "Channel purpose here"
}
```

#### 邀请用户加入频道

```bash
POST /slack/api/conversations.invite
Content-Type: application/json

{
  "channel": "C0123456789",
  "users": "U0123456789,U9876543210"
}
```

#### 将用户踢出频道

```bash
POST /slack/api/conversations.kick
Content-Type: application/json

{
  "channel": "C0123456789",
  "user": "U0123456789"
}
```

#### 标记消息为已读

```bash
POST /slack/api/conversations.mark
Content-Type: application/json

{
  "channel": "C0123456789",
  "ts": "1234567890.123456"
}
```

---

### 直接消息

#### 打开直接消息对话

```bash
POST /slack/api/conversations.open
Content-Type: application/json

{
  "users": "U0123456789"
}
```

#### 群组直接消息：

```bash
POST /slack/api/conversations.open
Content-Type: application/json

{
  "users": "U0123456789,U9876543210"
}
```

#### 列出直接消息频道

```bash
GET /slack/api/conversations.list?types=im
```

#### 列出群组直接消息频道

```bash
GET /slack/api/conversations.list?types=mpim
```

#### 我的对话记录

```bash
GET /slack/api/users.conversations?limit=100
```

---

### 用户

#### 列出用户

```bash
GET /slack/api/users.list?limit=100
```

#### 获取用户信息

```bash
GET /slack/api/users.info?user=U0123456789
```

#### 获取用户在线状态

```bash
GET /slack/api/users.getPresence?user=U0123456789
```

#### 设置用户在线状态

```bash
POST /slack/api/users.setPresence
Content-Type: application/json

{
  "presence": "away"
}
```

#### 通过电子邮件查找用户

```bash
GET /slack/api/users.lookupByEmail?email=user@example.com
```

---

### 反应

#### 添加反应

```bash
POST /slack/api/reactions.add
Content-Type: application/json

{
  "channel": "C0123456789",
  "name": "thumbsup",
  "timestamp": "1234567890.123456"
}
```

#### 删除反应

```bash
POST /slack/api/reactions.remove
Content-Type: application/json

{
  "channel": "C0123456789",
  "name": "thumbsup",
  "timestamp": "1234567890.123456"
}
```

#### 获取消息上的反应

```bash
GET /slack/api/reactions.get?channel=C0123456789&timestamp=1234567890.123456
```

#### 列出我的反应记录

```bash
GET /slack/api/reactions.list?limit=100
```

---

### 星标

#### 列出被星标的消息

```bash
GET /slack/api/stars.list?limit=100
```

#### 给消息添加星标

```bash
POST /slack/api/stars.add
Content-Type: application/json

{
  "channel": "C0123456789",
  "timestamp": "1234567890.123456"
}
```

#### 移除星标

```bash
POST /slack/api/stars.remove
Content-Type: application/json

{
  "channel": "C0123456789",
  "timestamp": "1234567890.123456"
}
```

---

### 机器人

#### 获取机器人信息

```bash
GET /slack/api/bots.info?bot=B0123456789
```

---

### 文件

#### 上传文件

```bash
POST /slack/api/files.upload
Content-Type: multipart/form-data

channels=C0123456789
content=file content here
filename=example.txt
title=Example File
```

#### 上传文件（版本 2：获取上传 URL）

```bash
GET /slack/api/files.getUploadURLExternal?filename=example.txt&length=1024
```

#### 完成文件上传

```bash
POST /slack/api/files.completeUploadExternal
Content-Type: application/json

{
  "files": [{"id": "F0123456789", "title": "My File"}],
  "channel_id": "C0123456789"
}
```

#### 删除文件

```bash
POST /slack/api/files.delete
Content-Type: application/json

{
  "file": "F0123456789"
}
```

#### 获取文件信息

```bash
GET /slack/api/files.info?file=F0123456789
```

---

### 搜索

#### 搜索消息

```bash
GET /slack/api/search.messages?query=keyword
```

---

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
const result = await response.json();
console.log(result);
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
print(response.json())
```

---

## 注意事项

- 频道 ID：`C`（公共频道）、`G`（私人/群组频道）、`D`（直接消息）
- 用户 ID 以 `U` 开头，机器人 ID 以 `B` 开头，团队 ID 以 `T` 开头
- 消息时间戳（`ts`）是唯一的标识符
- 使用 `mrkdwn` 格式来支持 Slack 的 Markdown 格式
- 帖子回复会使用 `thread_ts` 来引用父消息
- 基于游标的分页：使用 `response_metadata.next_cursor` 来获取下一页数据

### Shell 命令使用说明

- **重要提示：** 当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免glob解析问题。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）可能在某些 Shell 环境中无法正确解析，这可能导致 “Invalid API key” 错误。

## 错误处理

| 状态码 | 错误含义 |
|--------|---------|
| 400 | 未建立 Slack 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次请求） |
| 4xx/5xx | 来自 Slack API 的传递错误 |

**缺少权限范围错误：** 如果遇到 `missing_scope` 错误，请联系 [Maton 支持团队](mailto:support@maton.ai) 以申请额外的权限范围。

### 故障排除：API 密钥问题

1. 确保 `MATON_API_KEY` 环境变量已设置：

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `slack` 开头。例如：
  - 正确格式：`https://gateway.maton.ai/slack/api/chat.postMessage`
  - 错误格式：`https://gateway.maton.ai/api/chat.postMessage`

## 资源

- [Slack API 方法](https://api.slack.com/methods)
- [Web API 参考文档](https://api.slack.com/web)
- [Block Kit 参考文档](https://api.slack.com/reference/block-kit)
- [消息格式化指南](https://api.slack.com/reference/surfaces/formatting)
- [速率限制](https://api.slack.com/docs/rate-limits)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)