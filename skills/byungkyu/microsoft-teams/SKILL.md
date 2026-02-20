---
name: microsoft-teams
description: >
  **Microsoft Teams API 集成与托管 OAuth**  
  通过 Microsoft Graph API，您可以管理团队、频道、消息和会议。  
  当用户需要列出团队、创建频道、发送消息、安排会议或访问会议记录和文字记录时，可以使用此功能。  
  对于其他第三方应用程序，请使用 `api-gateway` 功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Microsoft Teams

您可以通过 Microsoft Graph 使用托管的 OAuth 认证来访问 Microsoft Teams API。该 API 允许您管理团队、频道、消息、会议以及查看会议记录和文字记录。

## 快速入门

```bash
# List user's joined teams
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/microsoft-teams/v1.0/me/joinedTeams')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/microsoft-teams/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Microsoft Graph API 端点路径。该网关会将请求代理到 `graph.microsoft.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Microsoft Teams OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=microsoft-teams&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'microsoft-teams'}).encode()
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
    "connection_id": "fb0fdc4a-0b5a-40cf-8b92-3bdae848cde3",
    "status": "ACTIVE",
    "creation_time": "2026-02-17T09:51:21.074601Z",
    "last_updated_time": "2026-02-17T09:51:34.323814Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "microsoft-teams",
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

如果您有多个 Microsoft Teams 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/microsoft-teams/v1.0/me/joinedTeams')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'fb0fdc4a-0b5a-40cf-8b92-3bdae848cde3')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 团队

#### 列出已加入的团队

```bash
GET /microsoft-teams/v1.0/me/joinedTeams
```

**响应：**
```json
{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#teams",
  "@odata.count": 1,
  "value": [
    {
      "id": "b643f103-870d-4f98-a23d-e6f164fae33e",
      "displayName": "carvedai.com",
      "description": null,
      "isArchived": false,
      "tenantId": "cb83c3f9-6d16-4cf3-bd8c-ab16b37932f9"
    }
  ]
}
```

#### 获取团队信息

```bash
GET /microsoft-teams/v1.0/teams/{team-id}
```

### 频道

#### 列出频道

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels
```

**响应：**
```json
{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#teams('...')/channels",
  "@odata.count": 1,
  "value": [
    {
      "id": "19:9fwtZjo3IM0D8bLdQqR-_oMFw1eUDlzWjPfIhNGhVd41@thread.tacv2",
      "createdDateTime": "2026-02-16T20:09:27.254Z",
      "displayName": "General",
      "description": null,
      "email": "carvedai.com473@carvedai.com",
      "membershipType": "standard",
      "isArchived": false
    }
  ]
}
```

#### 列出私有频道

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels?$filter=membershipType eq 'private'
```

#### 获取频道信息

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}
```

#### 创建频道

```bash
POST /microsoft-teams/v1.0/teams/{team-id}/channels
Content-Type: application/json

{
  "displayName": "New Channel",
  "description": "Channel description",
  "membershipType": "standard"
}
```

**响应：**
```json
{
  "id": "19:3b3361df822044558a062bb1a4ac8357@thread.tacv2",
  "createdDateTime": "2026-02-17T20:24:33.9284462Z",
  "displayName": "Maton Test Channel",
  "description": "Channel created by Maton integration test",
  "membershipType": "standard",
  "isArchived": false
}
```

#### 更新频道

```bash
PATCH /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}
Content-Type: application/json

{
  "description": "Updated description"
}
```

成功时返回 `204 No Content`。注意：默认的 “General” 频道无法被更新。

#### 删除频道

```bash
DELETE /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}
```

成功时返回 `204 No Content`。

### 频道成员

#### 列出频道成员

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/members
```

**响应：**
```json
{
  "@odata.count": 1,
  "value": [
    {
      "@odata.type": "#microsoft.graph.aadUserConversationMember",
      "id": "MCMjMiMj...",
      "roles": ["owner"],
      "displayName": "Kevin Kim",
      "userId": "5f56d55b-2ffb-448d-982a-b52547431f71",
      "email": "richard@carvedai.com"
    }
  ]
}
```

### 消息

#### 列出频道消息

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/messages
```

#### 向频道发送消息

```bash
POST /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/messages
Content-Type: application/json

{
  "body": {
    "content": "Hello World"
  }
}
```

**响应：**
```json
{
  "id": "1771359569239",
  "replyToId": null,
  "messageType": "message",
  "createdDateTime": "2026-02-17T20:19:29.239Z",
  "importance": "normal",
  "locale": "en-us",
  "from": {
    "user": {
      "id": "5f56d55b-2ffb-448d-982a-b52547431f71",
      "displayName": "Kevin Kim",
      "userIdentityType": "aadUser",
      "tenantId": "cb83c3f9-6d16-4cf3-bd8c-ab16b37932f9"
    }
  },
  "body": {
    "contentType": "text",
    "content": "Hello World"
  },
  "channelIdentity": {
    "teamId": "b643f103-870d-4f98-a23d-e6f164fae33e",
    "channelId": "19:9fwtZjo3IM0D8bLdQqR-_oMFw1eUDlzWjPfIhNGhVd41@thread.tacv2"
  }
}
```

#### 发送 HTML 消息

```bash
POST /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/messages
Content-Type: application/json

{
  "body": {
    "contentType": "html",
    "content": "<h1>Hello</h1><p>This is <strong>formatted</strong> content.</p>"
  }
}
```

#### 回复消息

```bash
POST /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/messages/{message-id}/replies
Content-Type: application/json

{
  "body": {
    "content": "This is a reply"
  }
}
```

#### 列出消息回复

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/messages/{message-id}/replies
```

#### 编辑消息

```bash
PATCH /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/messages/{message-id}
Content-Type: application/json

{
  "body": {
    "content": "Updated message content"
  }
}
```

成功时返回 `204 No Content`。

### 团队成员

#### 列出团队成员

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/members
```

**响应：**
```json
{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#teams('...')/members",
  "@odata.count": 1,
  "value": [
    {
      "@odata.type": "#microsoft.graph.aadUserConversationMember",
      "id": "MCMjMSMj...",
      "roles": ["owner"],
      "displayName": "Kevin Kim",
      "userId": "5f56d55b-2ffb-448d-982a-b52547431f71",
      "email": "richard@carvedai.com",
      "tenantId": "cb83c3f9-6d16-4cf3-bd8c-ab16b37932f9"
    }
  ]
}
```

### 在线状态

#### 获取用户在线状态

```bash
GET /microsoft-teams/v1.0/me/presence
```

**响应：**
```json
{
  "id": "5f56d55b-2ffb-448d-982a-b52547431f71",
  "availability": "Offline",
  "activity": "Offline",
  "outOfOfficeSettings": {
    "message": null,
    "isOutOfOffice": false
  }
}
```

在线状态值：`Available`、`Busy`、`DoNotDisturb`、`Away`、`Offline`

#### 通过 ID 获取用户在线状态

```bash
GET /microsoft-teams/v1.0/users/{user-id}/presence
```

通过用户的 ID 获取其在线状态信息。

### 标签

#### 列出频道标签

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/channels/{channel-id}/tabs
```

**响应：**
```json
{
  "@odata.count": 2,
  "value": [
    {
      "id": "ee0b3e8b-dfc8-4945-a45d-28ceaf787d92",
      "displayName": "Notes",
      "webUrl": "https://teams.microsoft.com/l/entity/..."
    },
    {
      "id": "3ed5b337-c2c9-4d5d-b7b4-84ff09a8fc1c",
      "displayName": "Files",
      "webUrl": "https://teams.microsoft.com/l/entity/..."
    }
  ]
}
```

### 应用程序

#### 列出已安装的应用程序

```bash
GET /microsoft-teams/v1.0/teams/{team-id}/installedApps
```

### 在线会议

#### 创建会议

```bash
POST /microsoft-teams/v1.0/me/onlineMeetings
Content-Type: application/json

{
  "subject": "Team Sync",
  "startDateTime": "2026-02-18T10:00:00Z",
  "endDateTime": "2026-02-18T11:00:00Z"
}
```

**响应：**
```json
{
  "id": "MSo1ZjU2ZDU1Yi0yZmZi...",
  "subject": "Team Sync",
  "startDateTime": "2026-02-18T10:00:00Z",
  "endDateTime": "2026-02-18T11:00:00Z",
  "joinUrl": "https://teams.microsoft.com/l/meetup-join/...",
  "joinWebUrl": "https://teams.microsoft.com/l/meetup-join/...",
  "meetingCode": "28636743235745",
  "joinMeetingIdSettings": {
    "joinMeetingId": "28636743235745",
    "passcode": "qh37NK9V",
    "isPasscodeRequired": true
  },
  "participants": {
    "organizer": {
      "upn": "richard@carvedai.com",
      "role": "presenter"
    }
  }
}
```

`joinUrl` 可以与参会者共享，以便他们加入会议。

#### 获取会议信息

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}
```

#### 通过 Join URL 查找会议

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings?$filter=JoinWebUrl eq '{encoded-join-url}'
```

注意：Microsoft Graph 需要过滤才能查询会议。如果不通过 `JoinWebUrl` 进行过滤，则无法列出所有会议。

#### 列出日历事件（包括预定的会议）

```bash
GET /microsoft-teams/v1.0/me/calendar/events?$top=10
```

预定的团队会议会以日历事件的形式显示，其中 `isOnlineMeeting` 的值为 `true`。

#### 删除会议

```bash
DELETE /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}
```

成功时返回 `204 No Content`。

#### 创建带参会者的会议

```bash
POST /microsoft-teams/v1.0/me/onlineMeetings
Content-Type: application/json

{
  "subject": "Project Review",
  "startDateTime": "2026-02-18T14:00:00Z",
  "endDateTime": "2026-02-18T15:00:00Z",
  "participants": {
    "attendees": [
      {
        "upn": "attendee@example.com",
        "role": "attendee"
      }
    ]
  }
}
```

#### 列出会议记录

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}/recordings
```

返回会议的记录列表（仅在会议结束且启用了录制功能后可用）。

#### 获取会议记录

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}/recordings/{recording-id}
```

#### 列出会议文字记录

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}/transcripts
```

返回会议的文字记录列表（仅在会议结束且启用了文字记录功能后可用）。

#### 获取会议文字记录

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}/transcripts/{transcript-id}
```

#### 列出出勤报告

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}/attendanceReports
```

返回会议的出勤报告（仅在会议结束后可用）。

#### 获取出勤报告

```bash
GET /microsoft-teams/v1.0/me/onlineMeetings/{meeting-id}/attendanceReports/{report-id}
```

### 聊天

#### 列出用户聊天记录

```bash
GET /microsoft-teams/v1.0/me/chats
```

#### 获取聊天记录

```bash
GET /microsoft-teams/v1.0/chats/{chat-id}
```

#### 列出聊天消息

```bash
GET /microsoft-teams/v1.0/chats/{chat-id}/messages
```

#### 向聊天发送消息

```bash
POST /microsoft-teams/v1.0/chats/{chat-id}/messages
Content-Type: application/json

{
  "body": {
    "content": "Hello in chat"
  }
}
```

## 分页

Microsoft Graph 使用 OData 风格的分页机制，通过 `@odata.nextLink` 实现：

```bash
GET /microsoft-teams/v1.0/me/joinedTeams?$top=10
```

当存在更多结果时，响应中会包含分页链接：

```json
{
  "value": [...],
  "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/joinedTeams?$skiptoken=..."
}
```

使用 `$top` 参数来限制每页显示的结果数量。

## OData 查询参数

- `$top=10` - 限制结果数量
- `$skip=20` - 跳过指定数量的结果
- `$select=id,displayName` - 选择特定的字段
- `$filter=membershipType eq 'private'` - 过滤结果
- `$orderby=displayName` - 对结果进行排序

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/microsoft-teams/v1.0/me/joinedTeams',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/microsoft-teams/v1.0/me/joinedTeams',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### 发送消息示例（Python）

```python
import os
import requests

team_id = "your-team-id"
channel_id = "your-channel-id"

response = requests.post(
    f'https://gateway.maton.ai/microsoft-teams/v1.0/teams/{team_id}/channels/{channel_id}/messages',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'body': {'content': 'Hello from Maton!'}}
)
data = response.json()
```

## 注意事项

- 使用的是 Microsoft Graph API v1.0
- 消息是以认证用户的身份发送的（而非以机器人的身份）——`from.user` 字段显示的是用户的真实身份
- 团队 ID 是 GUID（例如：`b643f103-870d-4f98-a23d-e6f164fae33e`）
- 频道 ID 包含线程后缀（例如：`19:9fwtZjo3IM0D8bLdQqR-_oMFw1eUDlzWjPfIhNGhVd41@thread.tacv2`）
- 消息 ID 是时间戳（例如：`1771359569239`）
- 消息内容类型：`text`（默认）或 `html`
- 频道成员类型：`standard`、`private`、`shared`
- 默认的 “General” 频道无法被更新或删除
- 仅支持使用 `me` 端点来列出已加入的团队（不能使用任意用户 ID）
- 重要提示：当使用 curl 命令时，如果 URL 中包含括号，请使用 `curl -g` 以避免全局解析
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少 Microsoft Teams 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 无权访问请求的资源 |
| 404 | 未找到团队、频道或消息 |
| 429 | 请求被限制（Microsoft Graph 的速率限制） |
| 4xx/5xx | 来自 Microsoft Graph API 的传递错误 |

## 资源

- [Microsoft Teams API 概述](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview)
- [Microsoft Graph API 参考](https://learn.microsoft.com/en-us/graph/api/overview)
- [频道资源](https://learn.microsoft.com/en-us/graph/api/resources/channel)
- [聊天消息资源](https://learn.microsoft.com/en-us/graph/api/resources/chatmessage)
- [团队资源](https://learn.microsoft.com/en-us/graph/api/resources/team)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)