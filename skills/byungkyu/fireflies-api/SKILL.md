---
name: fireflies
description: |
  Fireflies.ai GraphQL API integration with managed OAuth. Access meeting transcripts, summaries, users, contacts, and AI-powered meeting analysis.
  Use this skill when users want to retrieve meeting transcripts, search conversations, analyze meeting content with AskFred, or manage meeting recordings.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Fireflies

您可以使用托管的 OAuth 认证来访问 Fireflies.ai 的 GraphQL API。该 API 可用于检索会议记录、会议摘要、用户信息、联系人信息以及频道信息，并通过 AskFred 功能利用人工智能对会议内容进行分析。

## 快速入门

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ user { user_id name email is_admin } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/fireflies/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/fireflies/graphql
```

所有请求都会发送到一个统一的 GraphQL 端点。Fireflies 的网关会将请求代理到 `api.fireflies.aigraphql`，并自动插入您的 OAuth 令牌。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Fireflies OAuth 连接。

### 列出所有连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=fireflies&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'fireflies'}).encode()
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
    "connection_id": "a221f04a-6842-4254-ae9a-424bb63ad745",
    "status": "ACTIVE",
    "creation_time": "2026-02-11T00:45:25.802991Z",
    "last_updated_time": "2026-02-11T00:46:04.771700Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "fireflies",
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

如果您有多个 Fireflies 连接，可以使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ user { user_id name email } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/fireflies/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', 'a221f04a-6842-4254-ae9a-424bb63ad745')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果未指定，网关将使用默认的（最旧的）活动连接。

## GraphQL API

Fireflies 使用 GraphQL，这意味着所有请求都是 POST 请求，目标端点为 `/graphql`，请求体需要包含 JSON 格式的查询内容。

### 请求格式

```bash
POST /fireflies/graphql
Content-Type: application/json

{
  "query": "{ ... }",
  "variables": { ... }
}
```

---

## 查询

### 获取当前用户信息

```graphql
{
  user {
    user_id
    name
    email
    is_admin
    num_transcripts
    minutes_consumed
    recent_transcript
    recent_meeting
  }
}
```

**响应：**
```json
{
  "data": {
    "user": {
      "user_id": "01KH5131Z0W4TS7BBSEP66CV6V",
      "name": "John Doe",
      "email": "john@example.com",
      "is_admin": true,
      "num_transcripts": null,
      "minutes_consumed": 0
    }
  }
}
```

### 列出用户信息

```graphql
{
  users {
    user_id
    name
    email
    is_admin
    num_transcripts
    minutes_consumed
  }
}
```

### 列出会议记录

```graphql
{
  transcripts {
    id
    title
    date
    duration
    host_email
    organizer_email
    privacy
    transcript_url
    audio_url
    video_url
    dateString
    calendar_type
    meeting_link
  }
}
```

**带参数的查询（用于过滤）：**

```json
{
  "query": "query($limit: Int, $skip: Int) { transcripts(limit: $limit, skip: $skip) { id title date duration } }",
  "variables": {
    "limit": 10,
    "skip": 0
  }
}
```

### 根据 ID 获取会议记录

```graphql
query($id: String!) {
  transcript(id: $id) {
    id
    title
    date
    duration
    host_email
    privacy
    transcript_url
    audio_url
    summary {
      overview
      short_summary
      action_items
      outline
      keywords
      meeting_type
    }
    sentences {
      text
      speaker_name
      start_time
      end_time
    }
    participants
    speakers {
      name
    }
  }
}
```

### 列出频道信息

```graphql
{
  channels {
    id
    title
    created_at
    updated_at
    is_private
    created_by
  }
}
```

### 根据 ID 获取频道信息

```graphql
query($id: String!) {
  channel(id: $id) {
    id
    title
    created_at
    is_private
    members
  }
}
```

### 列出联系人信息

```graphql
{
  contacts {
    email
    name
    picture
    last_meeting_date
  }
}
```

### 列出用户组信息

```graphql
{
  user_groups {
    id
    name
  }
}
```

### 列出会议中的语音片段（Bites）

```graphql
{
  bites {
    id
    name
    transcript_id
    thumbnail
    preview
    status
    summary
    start_time
    end_time
    media_type
    created_at
  }
}
```

### 根据 ID 获取语音片段

```graphql
query($id: String!) {
  bite(id: $id) {
    id
    name
    transcript_id
    summary
    start_time
    end_time
    captions
  }
}
```

### 列出正在进行的会议

```graphql
{
  active_meetings {
    id
    title
    date
  }
}
```

### 使用 AskFred 功能查询会议内容

**列出会议中的讨论线程：**
```graphql
{
  askfred_threads {
    id
    title
    created_at
  }
}
```

**根据 ID 获取讨论线程：**
```graphql
query($id: String!) {
  askfred_thread(id: $id) {
    id
    title
    messages {
      content
      role
    }
  }
}
```

---

## 更改请求数据（Mutations）

### 上传音频文件

```graphql
mutation($input: AudioUploadInput!) {
  uploadAudio(input: $input) {
    success
    title
    message
  }
}
```

**参数：**
```json
{
  "input": {
    "url": "https://example.com/audio.mp3",
    "title": "Meeting Recording"
  }
}
```

### 删除会议记录

```graphql
mutation($id: String!) {
  deleteTranscript(id: $id) {
    success
    message
  }
}
```

### 更新会议标题

```graphql
mutation($id: String!, $title: String!) {
  updateMeetingTitle(id: $id, title: $title) {
    success
  }
}
```

### 更改会议隐私设置

```graphql
mutation($id: String!, $privacy: String!) {
  updateMeetingPrivacy(id: $id, privacy: $privacy) {
    success
  }
}
```

### 更改会议使用的频道

```graphql
mutation($id: String!, $channelId: String!) {
  updateMeetingChannel(id: $id, channelId: $channelId) {
    success
  }
}
```

### 设置用户角色

```graphql
mutation($userId: String!, $role: String!) {
  setUserRole(userId: $userId, role: $role) {
    success
  }
}
```

### 创建新的语音片段

```graphql
mutation($input: CreateBiteInput!) {
  createBite(input: $input) {
    id
    name
  }
}
```

### 使用 AskFred 功能进行操作

**创建新的讨论线程：**
```graphql
mutation($input: CreateAskFredThreadInput!) {
  createAskFredThread(input: $input) {
    id
    title
  }
}
```

**继续现有讨论线程：**
```graphql
mutation($id: String!, $question: String!) {
  continueAskFredThread(id: $id, question: $question) {
    id
    messages {
      content
      role
    }
  }
}
```

**删除讨论线程：**
```graphql
mutation($id: String!) {
  deleteAskFredThread(id: $id) {
    success
  }
}
```

### 实时会议操作

**更改会议状态（暂停/恢复）：**
```graphql
mutation($id: String!, $state: String!) {
  updateMeetingState(id: $id, state: $state) {
    success
  }
}
```

**创建实时操作项：**
```graphql
mutation($meetingId: String!, $text: String!) {
  createLiveActionItem(meetingId: $meetingId, text: $text) {
    success
  }
}
```

**创建实时语音片段：**
```graphql
mutation($meetingId: String!, $name: String!) {
  createLiveSoundbite(meetingId: $meetingId, name: $name) {
    success
  }
}
```

**将机器人添加到实时会议中：**
```graphql
mutation($meetingLink: String!) {
  addToLiveMeeting(meetingLink: $meetingLink) {
    success
  }
}
```

---

## 代码示例

### JavaScript 示例

```javascript
const query = `{
  user {
    user_id
    name
    email
  }
}`;

const response = await fetch(
  'https://gateway.maton.ai/fireflies/graphql',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  }
);
const data = await response.json();
console.log(data.data.user);
```

### Python 示例

```python
import os
import requests

query = '''
{
  transcripts {
    id
    title
    date
    duration
  }
}
'''

response = requests.post(
    'https://gateway.maton.ai/fireflies/graphql',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'query': query}
)
data = response.json()
for transcript in data['data']['transcripts']:
    print(f"{transcript['title']}: {transcript['duration']}s")
```

## 注意事项：

- Fireflies 使用 GraphQL 而非 REST：所有请求均为 POST 请求，目标端点为 `/graphql`。
- 用户 ID 采用 ULID 格式（例如：`01KH5131Z0W4TS7BBSEP66CV6V`）。
- 时间戳为 Unix 时间戳（以毫秒为单位）。
- 会议记录中的 `summary` 字段包含人工智能生成的内容（如会议概要、操作项、大纲和关键词）。
- AskFred 支持对会议记录进行自然语言查询。
- 免费计划每天允许 50 次 API 请求；商业计划提供更多请求次数。
- 重要提示：所有 GraphQL 查询和更改操作都必须以 `POST` 请求的形式发送，且请求头的 `Content-Type` 必须设置为 `application/json`。
- 重要提示：在将 curl 的输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY`。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | GraphQL 查询无效或未建立连接 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足 |
| 429 | 请求次数达到限制 |
| 500 | 服务器内部错误 |

**GraphQL 错误代码：**
```json
{
  "errors": [
    {
      "message": "Cannot query field \"id\" on type \"User\".",
      "code": "GRAPHQL_VALIDATION_FAILED"
    }
  ]
}
```

### 故障排除：API 密钥相关问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出所有连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称错误

1. 确保您的 URL 路径以 `fireflies` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/firefliesgraphql`
  - 错误的路径：`https://gateway.maton.aigraphql`

## 资源

- [Fireflies API 文档](https://docs.fireflies.ai/)
- [Fireflies GraphQL API 参考文档](https://docs.fireflies.aigraphql-api)
- [Fireflies 开发者计划](https://docs.fireflies.ai/getting-started/developer-program)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 客服](mailto:support@maton.ai)