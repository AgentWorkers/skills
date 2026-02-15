---
name: google-meet
description: |
  Google Meet API integration with managed OAuth. Create meeting spaces, list conference records, and manage meeting participants. Use this skill when users want to interact with Google Meet. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Meet

您可以使用托管的 OAuth 认证来访问 Google Meet API。该 API 允许您创建和管理会议空间、列出会议记录以及检索参与者信息。

## 快速入门

```bash
# Create a meeting space
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-meet/v2/spaces', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-meet/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Meet API 端点路径。该网关会将请求代理到 `meet.googleapis.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-meet&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-meet'}).encode()
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
    "app": "google-meet",
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

如果您有多个 Google Meet 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-meet/v2/spaces', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 会议空间

#### 创建会议空间

```bash
POST /google-meet/v2/spaces
Content-Type: application/json

{}
```

**响应：**
```json
{
  "name": "spaces/abc123",
  "meetingUri": "https://meet.google.com/abc-defg-hij",
  "meetingCode": "abc-defg-hij",
  "config": {
    "accessType": "OPEN",
    "entryPointAccess": "ALL"
  }
}
```

#### 获取会议空间信息

```bash
GET /google-meet/v2/spaces/{spaceId}
```

#### 更新会议空间信息

```bash
PATCH /google-meet/v2/spaces/{spaceId}
Content-Type: application/json

{
  "config": {
    "accessType": "TRUSTED"
  }
}
```

#### 结束活动会议

```bash
POST /google-meet/v2/spaces/{spaceId}:endActiveConference
```

### 会议记录

#### 列出会议记录

```bash
GET /google-meet/v2/conferenceRecords
```

支持过滤：

```bash
GET /google-meet/v2/conferenceRecords?filter=space.name="spaces/abc123"
```

#### 获取会议记录信息

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}
```

### 参与者

#### 列出参与者

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/participants
```

#### 获取参与者信息

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/participants/{participantId}
```

### 参与者的会议会话

#### 列出参与者的会议会话

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/participants/{participantId}/participantSessions
```

### 录像

#### 列出录像文件

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/recordings
```

#### 获取录像文件信息

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/recordings/{recordingId}
```

### 文本记录

#### 列出文本记录

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/transcripts
```

#### 获取文本记录信息

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/transcripts/{transcriptId}
```

#### 列出文本记录条目

```bash
GET /google-meet/v2/conferenceRecords/{conferenceRecordId}/transcripts/{transcriptId}/entries
```

## 代码示例

### JavaScript

```javascript
// Create a meeting space
const response = await fetch(
  'https://gateway.maton.ai/google-meet/v2/spaces',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({})
  }
);

const space = await response.json();
console.log(`Meeting URL: ${space.meetingUri}`);
```

### Python

```python
import os
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
}

# Create a meeting space
response = requests.post(
    'https://gateway.maton.ai/google-meet/v2/spaces',
    headers=headers,
    json={}
)
space = response.json()
print(f"Meeting URL: {space['meetingUri']}")
```

## 注意事项

- 会议空间是可重复使用的永久性会议室。
- 会议记录会在会议开始时创建，并用于追踪会议历史。
- 访问权限类型包括：`OPEN`（任何人都可以访问）、`TRUSTED`（仅限组织成员）和 `RESTRICTED`（仅限受邀人员）。
- 录像和文本记录功能需要启用 Google Workspace 的录像功能。
- **重要提示：** 当使用 `curl` 命令时，如果 URL 中包含方括号，请使用 `curl -g` 以避免全局解析问题。
- **重要提示：** 在将 `curl` 的输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google Meet 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Google Meet API 的传递错误 |

### 故障排除：无效的 API 密钥

**当收到 “无效 API 密钥” 错误时，请务必按照以下步骤操作，再判断是否存在问题：**

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

1. 确保您的 URL 路径以 `google-meet` 开头。例如：
   - 正确的路径：`https://gateway.maton.ai/google-meet/v2/spaces`
   - 错误的路径：`https://gateway.maton.ai/meet/v2/spaces`

## 资源

- [Google Meet API 概述](https://developers.google.com/meet/api/reference/rest)
- [会议空间](https://developers.google.com/meet/api/reference/rest/v2/spaces)
- [会议记录](https://developers.google.com/meet/api/reference/rest/v2/conferenceRecords)
- [参与者](https://developers.google.com/meet/api/reference/rest/v2/conferenceRecords.participants)
- [录像](https://developers.google.com/meet/api/reference/rest/v2/conferenceRecords.recordings)
- [文本记录](https://developers.google.com/meet/api/reference/rest/v2/conferenceRecords.transcripts)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)