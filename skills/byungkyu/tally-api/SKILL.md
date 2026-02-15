---
name: tally
description: |
  Tally API integration with managed OAuth. Manage forms, submissions, workspaces, and webhooks.
  Use this skill when users want to create or manage Tally forms, retrieve form submissions, or work with workspaces.
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

# Tally

您可以使用托管的 OAuth 认证来访问 Tally API，从而管理您的 Tally 账户中的表单、提交记录、工作空间和 Webhook。

## 快速入门

```bash
# List your forms
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/tally/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/tally/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Tally API 端点路径。该网关会将请求代理到 `api.tally.so` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头部和 `User Agent` 头部中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
User-Agent: Maton/1.0
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

您可以在 `https://ctrl.maton.ai` 上管理您的 Tally OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=tally&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'tally'}).encode()
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
    "connection_id": "cd54e2b0-f1d0-435e-a97d-f2d6a5c474bf",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T21:00:31.222600Z",
    "last_updated_time": "2026-02-07T21:00:37.821240Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "tally",
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

如果您有多个 Tally 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/tally/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'cd54e2b0-f1d0-435e-a97d-f2d6a5c474bf')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户

#### 获取当前用户

```bash
GET /tally/users/me
```

**响应：**
```json
{
  "id": "w2lBkb",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "organizationId": "n0Ze8Q",
  "subscriptionPlan": "FREE",
  "createdAt": "2026-02-07T20:58:54.000Z",
  "updatedAt": "2026-02-07T22:50:35.000Z"
}
```

### 表单

#### 列出表单

```bash
GET /tally/forms
```

**查询参数：**
- `page` - 页码（默认值：1）
- `limit` - 每页显示的条数（默认值：50）

**响应：**
```json
{
  "items": [
    {
      "id": "GxdRaQ",
      "name": "Contact Form",
      "workspaceId": "3jW9Q1",
      "organizationId": "n0Ze8Q",
      "status": "PUBLISHED",
      "hasDraftBlocks": false,
      "numberOfSubmissions": 42,
      "createdAt": "2026-02-09T08:36:00.000Z",
      "updatedAt": "2026-02-09T08:36:17.000Z",
      "isClosed": false
    }
  ],
  "page": 1,
  "limit": 50,
  "total": 1,
  "hasMore": false
}
```

#### 获取表单信息

```bash
GET /tally/forms/{formId}
```

**响应：**
```json
{
  "id": "GxdRaQ",
  "name": "Contact Form",
  "workspaceId": "3jW9Q1",
  "status": "PUBLISHED",
  "blocks": [
    {
      "uuid": "11111111-1111-1111-1111-111111111111",
      "type": "FORM_TITLE",
      "groupUuid": "22222222-2222-2222-2222-222222222222",
      "groupType": "FORM_TITLE",
      "payload": {}
    },
    {
      "uuid": "33333333-3333-3333-3333-333333333333",
      "type": "INPUT_TEXT",
      "groupUuid": "44444444-4444-4444-4444-444444444444",
      "groupType": "INPUT_TEXT",
      "payload": {}
    }
  ],
  "settings": null
}
```

#### 创建表单

```bash
POST /tally/forms
Content-Type: application/json

{
  "status": "DRAFT",
  "workspaceId": "3jW9Q1",
  "blocks": [
    {
      "type": "FORM_TITLE",
      "uuid": "11111111-1111-1111-1111-111111111111",
      "groupUuid": "22222222-2222-2222-2222-222222222222",
      "groupType": "FORM_TITLE",
      "title": "My Form",
      "payload": {}
    },
    {
      "type": "INPUT_TEXT",
      "uuid": "33333333-3333-3333-3333-333333333333",
      "groupUuid": "44444444-4444-4444-4444-444444444444",
      "groupType": "INPUT_TEXT",
      "title": "Your name",
      "payload": {}
    }
  ]
}
```

**表单类型：**
- `FORM_TITLE` - 表单标题块
- `INPUT_TEXT` - 单行文本输入框
- `INPUT_EMAIL` - 电子邮件输入框
- `INPUT_NUMBER` - 数字输入框
- `INPUT_PHONE_NUMBER` - 电话号码输入框
- `INPUT_DATE` - 日期选择器
- `INPUT_TIME` - 时间选择器
- `INPUT_LINK` - URL 输入框
- `TEXTAREA` - 多行文本输入框
- `MULTIPLE_CHOICE` - 单选按钮
- `CHECKBOXES` - 复选框组
- `DROPDOWN` - 下拉菜单
- `LINEAR_SCALE` - 等级评分
- `RATING` - 星级评分
- `FILE_UPLOAD` - 文件上传框
- `SIGNATURE` - 签名字段
- `PAYMENT` - 支付字段
- `HIDDEN_fields` - 隐藏字段

**注意：** `uuid` 和 `groupUuid` 字段必须是有效的 UUID（GUID）。

#### 更新表单

```bash
PATCH /tally/forms/{formId}
Content-Type: application/json

{
  "name": "Updated Form Name",
  "status": "PUBLISHED"
}
```

**状态值：**
- `DRAFT` - 表单为草稿状态
- `PUBLISHED` - 表单已发布

#### 删除表单

```bash
DELETE /tally/forms/{formId}
```

表单将被移至“回收站”。

### 表单问题

#### 列出问题

```bash
GET /tally/forms/{formId}/questions
```

**响应：**
```json
{
  "questions": [
    {
      "uuid": "33333333-3333-3333-3333-333333333333",
      "type": "INPUT_TEXT",
      "title": "Your name"
    }
  ],
  "hasResponses": true
}
```

### 表单提交

#### 列出提交记录

```bash
GET /tally/forms/{formId}/submissions
```

**查询参数：**
- `page` - 页码（默认值：1）
- `limit` - 每页显示的条数（默认值：50）
- `startDate` - 按开始日期过滤（ISO 8601 格式）
- `endDate` - 按结束日期过滤（ISO 8601 格式）
- `afterId` - 获取此 ID 之后的提交记录（分页查询）

**响应：**
```json
{
  "page": 1,
  "limit": 50,
  "hasMore": false,
  "totalNumberOfSubmissionsPerFilter": {
    "all": 42,
    "completed": 40,
    "partial": 2
  },
  "questions": [
    {
      "uuid": "33333333-3333-3333-3333-333333333333",
      "type": "INPUT_TEXT",
      "title": "Your name"
    }
  ],
  "submissions": [
    {
      "id": "sub123",
      "respondentId": "resp456",
      "formId": "GxdRaQ",
      "createdAt": "2026-02-09T10:00:00.000Z",
      "isCompleted": true,
      "responses": [
        {
          "questionId": "33333333-3333-3333-3333-333333333333",
          "value": "John Doe"
        }
      ]
    }
  ]
}
```

#### 获取提交记录信息

```bash
GET /tally/forms/{formId}/submissions/{submissionId}
```

#### 删除提交记录

```bash
DELETE /tally/forms/{formId}/submissions/{submissionId}
```

### 工作空间

#### 列出工作空间

```bash
GET /tally/workspaces
```

**响应：**
```json
{
  "items": [
    {
      "id": "3jW9Q1",
      "name": "My Workspace",
      "createdByUserId": "w2lBkb",
      "createdAt": "2026-02-09T08:35:53.000Z",
      "updatedAt": "2026-02-09T08:35:53.000Z"
    }
  ],
  "page": 1,
  "limit": 50,
  "total": 1,
  "hasMore": false
}
```

#### 获取工作空间信息

```bash
GET /tally/workspaces/{workspaceId}
```

**响应：**
```json
{
  "id": "3jW9Q1",
  "name": "My Workspace",
  "createdByUserId": "w2lBkb",
  "createdAt": "2026-02-09T08:35:53.000Z",
  "members": [
    {
      "id": "w2lBkb",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com"
    }
  ]
}
```

#### 创建工作空间

**注意：** 创建工作空间需要 Pro 订阅。

#### 更新工作空间

```bash
PATCH /tally/workspaces/{workspaceId}
Content-Type: application/json

{
  "name": "Updated Workspace Name"
}
```

#### 删除工作空间

```bash
DELETE /tally/workspaces/{workspaceId}
```

工作空间及其所有表单将被移至“回收站”。

### 组织用户

#### 列出用户

```bash
GET /tally/organizations/{organizationId}/users
```

**响应：**
```json
[
  {
    "id": "w2lBkb",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "createdAt": "2026-02-07T20:58:54.000Z"
  }
]
```

#### 删除用户

```bash
DELETE /tally/organizations/{organizationId}/users/{userId}
```

### 组织邀请

#### 列出邀请信息

```bash
GET /tally/organizations/{organizationId}/invites
```

#### 创建邀请

```bash
POST /tally/organizations/{organizationId}/invites
Content-Type: application/json

{
  "email": "newuser@example.com",
  "workspaceIds": ["3jW9Q1"]
}
```

#### 取消邀请

```bash
DELETE /tally/organizations/{organizationId}/invites/{inviteId}
```

### Webhook

#### 列出 Webhook

**注意：** 列出 Webhook 可能需要特定的权限。

#### 创建 Webhook

```bash
POST /tally/webhooks
Content-Type: application/json

{
  "formId": "GxdRaQ",
  "url": "https://your-endpoint.com/webhook",
  "eventTypes": ["FORM_RESPONSE"]
}
```

**Webhook 事件类型：**
- `FORM_RESPONSE` - 当新的表单响应被提交时触发

#### 更新 Webhook

```bash
PATCH /tally/webhooks/{webhookId}
Content-Type: application/json

{
  "url": "https://new-endpoint.com/webhook"
}
```

#### 删除 Webhook

```bash
DELETE /tally/webhooks/{webhookId}
```

#### 列出 Webhook 事件

```bash
GET /tally/webhooks/{webhookId}/events
```

#### 重试 Webhook 事件

```bash
POST /tally/webhooks/{webhookId}/events/{eventId}
```

## 分页

Tally 使用基于页码的分页机制：

```bash
GET /tally/forms?page=1&limit=50
```

响应中包含分页信息：

```json
{
  "items": [...],
  "page": 1,
  "limit": 50,
  "total": 100,
  "hasMore": true
}
```

对于提交记录，也可以使用 `afterId` 进行基于游标的分页。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/tally/forms',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'User-Agent': 'Maton/1.0'
    }
  }
);
const data = await response.json();
console.log(data.items);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/tally/forms',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'Maton/1.0'
    }
)
data = response.json()
print(data['items'])
```

### 创建表单并获取提交记录

```python
import os
import requests
import uuid

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'User-Agent': 'Maton/1.0'
}

# Create a simple form
form_data = {
    'status': 'DRAFT',
    'blocks': [
        {
            'type': 'FORM_TITLE',
            'uuid': str(uuid.uuid4()),
            'groupUuid': str(uuid.uuid4()),
            'groupType': 'FORM_TITLE',
            'title': 'Contact Form',
            'payload': {}
        },
        {
            'type': 'INPUT_EMAIL',
            'uuid': str(uuid.uuid4()),
            'groupUuid': str(uuid.uuid4()),
            'groupType': 'INPUT_EMAIL',
            'title': 'Your email',
            'payload': {}
        }
    ]
}

response = requests.post(
    'https://gateway.maton.ai/tally/forms',
    headers=headers,
    json=form_data
)
form = response.json()
print(f"Created form: {form['id']}")

# Get submissions for a form
response = requests.get(
    f'https://gateway.maton.ai/tally/forms/{form["id"]}/submissions',
    headers=headers
)
submissions = response.json()
print(f"Total submissions: {submissions['totalNumberOfSubmissionsPerFilter']['all']}")
```

## 注意事项：

- 表单和工作空间的 ID 是简短的字母数字字符串（例如：`GxdRaQ`）。
- `uuid` 和 `groupUuid` 字段必须是有效的 UUID（GUID）。
- 创建工作空间需要 Pro 订阅。
- 该 API 处于公开测试阶段，可能会发生变化。
- 请求速率限制：每分钟 100 次请求。
- 使用 Webhook 而不是轮询来获取实时提交通知。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Tally 连接或验证错误 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求速率限制（每分钟 100 次请求） |
| 4xx/5xx | 来自 Tally API 的传递错误 |

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `tally` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/tally/forms`
- 错误的路径：`https://gateway.maton.ai/forms`

## 资源

- [Tally API 介绍](https://developers.tally.so/api-reference/introduction)
- [Tally API 参考文档](https://developers.tally.so/llms.txt)
- [Tally 帮助中心](https://help.tally.so/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)