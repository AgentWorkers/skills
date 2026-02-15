---
name: systeme
description: |
  Systeme.io API integration with managed OAuth. Manage contacts, tags, courses, communities, and subscriptions.
  Use this skill when users want to manage Systeme.io contacts, enroll students in courses, manage community memberships, or handle subscriptions.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
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

# Systeme.io

您可以使用受管理的 OAuth 认证来访问 Systeme.io API。该 API 允许您管理联系人、标签、课程、社区和订阅信息。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/systeme/api/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/systeme/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Systeme.io API 端点路径。该网关会将请求代理到 `api.systeme.io`，并自动插入您的 API 密钥。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Systeme.io 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=systeme&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'systeme'}).encode()
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
    "app": "systeme",
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

如果您有多个 Systeme.io 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/systeme/api/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 联系人操作

#### 列出联系人

```bash
GET /systeme/api/contacts
```

**查询参数：**
- `limit` - 每页显示的项目数量（10-100，可选）
- `startingAfter` - 用于分页的上一页面最后一条记录的 ID（可选）
- `order` - 排序方式：`asc` 或 `desc`（默认：`desc`，可选）

#### 获取联系人信息

```bash
GET /systeme/api/contacts/{id}
```

#### 创建联系人

```bash
POST /systeme/api/contacts
Content-Type: application/json

{
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "phoneNumber": "+1234567890",
  "locale": "en",
  "fields": [
    {
      "slug": "custom_field_slug",
      "value": "custom value"
    }
  ]
}
```

#### 更新联系人信息

```bash
PATCH /systeme/api/contacts/{id}
Content-Type: application/merge-patch+json

{
  "firstName": "Jane",
  "lastName": "Smith"
}
```

#### 删除联系人

```bash
DELETE /systeme/api/contacts/{id}
```

### 标签操作

#### 列出标签

```bash
GET /systeme/api/tags
```

#### 获取标签信息

```bash
GET /systeme/api/tags/{id}
```

#### 创建标签

```bash
POST /systeme/api/tags
Content-Type: application/json

{
  "name": "VIP Customer"
}
```

#### 更新标签信息

```bash
PUT /systeme/api/tags/{id}
Content-Type: application/json

{
  "name": "Premium Customer"
}
```

#### 删除标签

```bash
DELETE /systeme/api/tags/{id}
```

### 联系人与标签关联操作

#### 为联系人分配标签

```bash
POST /systeme/api/contacts/{id}/tags
Content-Type: application/json

{
  "tagId": 12345
}
```

#### 从联系人中移除标签

```bash
DELETE /systeme/api/contacts/{id}/tags/{tagId}
```

### 联系人字段操作

#### 列出联系人字段

```bash
GET /systeme/api/contact_fields
```

#### 创建联系人字段

```bash
POST /systeme/api/contact_fields
Content-Type: application/json

{
  "name": "Company Name",
  "slug": "company_name"
}
```

#### 更新联系人字段

```bash
PATCH /systeme/api/contact_fields/{slug}
Content-Type: application/merge-patch+json

{
  "name": "Organization Name"
}
```

#### 删除联系人字段

```bash
DELETE /systeme/api/contact_fields/{slug}
```

### 课程操作

#### 列出课程

```bash
GET /systeme/api/school/courses
```

#### 列出报名信息

```bash
GET /systeme/api/school/enrollments
```

#### 创建报名记录

```bash
POST /systeme/api/school/courses/{courseId}/enrollments
Content-Type: application/json

{
  "contactId": 12345,
  "accessType": "full_access"
}
```

**必填字段：**
- `contactId` - 要报名的联系人的 ID
- `accessType` - 访问类型：`full_access`、`partial_access` 或 `dripping_content`

**注意：** 如果 `accessType` 为 `partial_access`，您还需要提供包含模块 ID 的 `modules` 数组。

#### 删除报名记录

```bash
DELETE /systeme/api/school/enrollments/{id}
```

### 社区操作

#### 列出社区

```bash
GET /systeme/api/community/communities
```

#### 列出成员信息

```bash
GET /systeme/api/community/memberships
```

#### 创建成员资格

```bash
POST /systeme/api/community/communities/{communityId}/memberships
Content-Type: application/json

{
  "contactId": 12345
}
```

#### 删除成员资格

```bash
DELETE /systeme/api/community/memberships/{id}
```

### 订阅操作

#### 列出订阅信息

```bash
GET /systeme/api/payment/subscriptions
```

#### 取消订阅

```bash
POST /systeme/api/payment/subscriptions/{id}/cancel
```

## 分页

Systeme.io 使用基于游标的分页机制，相关参数如下：

```bash
GET /systeme/api/contacts?limit=50&startingAfter=12345&order=asc
```

**参数：**
- `limit` - 每页显示的项目数量（10-100）
- `startingAfter` - 上一页最后一条记录的 ID
- `order` - 排序方式：`asc` 或 `desc`（默认：`desc`）

**响应：**
```json
{
  "items": [...],
  "hasMore": true
}
```

当 `hasMore` 为 `true` 时，使用 `items` 中最后一条记录的 ID 作为 `startingAfter` 以获取下一页的内容。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/systeme/api/contacts',
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
    'https://gateway.maton.ai/systeme/api/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### 创建带有标签的联系人

```python
import os
import requests

# Create contact
contact = requests.post(
    'https://gateway.maton.ai/systeme/api/contacts',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'email': 'new@example.com',
        'firstName': 'New',
        'lastName': 'Contact'
    }
).json()

# Assign tag
requests.post(
    f'https://gateway.maton.ai/systeme/api/contacts/{contact["id"]}/tags',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'tagId': 12345}
)
```

## 注意事项

- Systeme.io 使用 API 密钥进行认证（以 `X-API-Key` 头的形式传递）。
- 网关会自动处理认证头的转换。
- 对于 `PATCH` 请求，请使用 `application/merge-patch+json` 的内容类型。
- 联系人、标签、课程和报名记录的 ID 都是数字整数。
- 通过 `X-RateLimit-*` 头实施速率限制。
- Systeme.io 会验证电子邮件域名——仅接受具有有效 MX 记录的真实电子邮件地址。
- 如果未配置支付功能，订阅端点（`/api/payment/subscriptions`）可能会返回 404 错误。
- **重要提示：** 当 URL 中包含括号时，使用 `curl -g` 命令可以禁用全局解析。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Systeme.io 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 达到速率限制（请查看 `Retry-After` 头） |
| 4xx/5xx | 来自 Systeme.io API 的传递错误 |

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

1. 确保您的 URL 路径以 `systeme` 开头。例如：
- 正确：`https://gateway.maton.ai/systeme/api/contacts`
- 错误：`https://gateway.maton.ai/api/contacts`

## 资源

- [Systeme.io API 参考文档](https://developer.systeme.io/reference)
- [Systeme.io API 概述](https://developer.systeme.io/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)