---
name: google-workspace-admin
description: |
  Google Workspace Admin SDK integration with managed OAuth. Manage users, groups, organizational units, and domain settings. Use this skill when users want to administer Google Workspace. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Workspace 管理

通过管理的 OAuth 认证来访问 Google Workspace 管理 SDK。您可以管理 Google Workspace 的用户、组、组织单元、角色和域名设置。

## 快速入门

```bash
# List users in the domain
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer&maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-workspace-admin/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Admin SDK API 端点路径。该网关会将请求代理到 `admin.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-workspace-admin&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-workspace-admin'}).encode()
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
    "app": "google-workspace-admin",
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

如果您有多个 Google Workspace 管理连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户

#### 列出用户

```bash
GET /google-workspace-admin/admin/directory/v1/users?customer=my_customer&maxResults=100
```

查询参数：
- `customer` - 客户 ID 或 `my_customer`（用于您的域名）（必填）
- `domain` - 按特定域名过滤
- `maxResults` - 每页的最大结果数（1-500，默认为 100）
- `orderBy` - 按 `email`、`familyName` 或 `givenName` 排序
- `query` - 搜索查询（例如：`email:john*`、`name:John*`）
- `pageToken` - 分页令牌

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer&query=email:john*')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "kind": "admin#directory#users",
  "users": [
    {
      "id": "123456789",
      "primaryEmail": "john@example.com",
      "name": {
        "givenName": "John",
        "familyName": "Doe",
        "fullName": "John Doe"
      },
      "isAdmin": false,
      "isDelegatedAdmin": false,
      "suspended": false,
      "creationTime": "2024-01-15T10:30:00.000Z",
      "lastLoginTime": "2025-02-01T08:00:00.000Z",
      "orgUnitPath": "/Sales"
    }
  ],
  "nextPageToken": "..."
}
```

#### 获取用户信息

```bash
GET /google-workspace-admin/admin/directory/v1/users/{userKey}
```

`userKey` 可以是用户的主要电子邮件地址或唯一用户 ID。

#### 创建用户

```bash
POST /google-workspace-admin/admin/directory/v1/users
Content-Type: application/json

{
  "primaryEmail": "newuser@example.com",
  "name": {
    "givenName": "Jane",
    "familyName": "Smith"
  },
  "password": "temporaryPassword123!",
  "changePasswordAtNextLogin": true,
  "orgUnitPath": "/Engineering"
}
```

#### 更新用户信息

```bash
PUT /google-workspace-admin/admin/directory/v1/users/{userKey}
Content-Type: application/json

{
  "name": {
    "givenName": "Jane",
    "familyName": "Smith-Johnson"
  },
  "suspended": false,
  "orgUnitPath": "/Sales"
}
```

#### 部分更新用户信息

```bash
PATCH /google-workspace-admin/admin/directory/v1/users/{userKey}
Content-Type: application/json

{
  "suspended": true
}
```

#### 删除用户

```bash
DELETE /google-workspace-admin/admin/directory/v1/users/{userKey}
```

#### 将用户设置为管理员

```bash
POST /google-workspace-admin/admin/directory/v1/users/{userKey}/makeAdmin
Content-Type: application/json

{
  "status": true
}
```

### 组

#### 列出组

```bash
GET /google-workspace-admin/admin/directory/v1/groups?customer=my_customer
```

查询参数：
- `customer` - 客户 ID 或 `my_customer`（必填）
- `domain` - 按域名过滤
- `maxResults` - 最大结果数（1-200）
- `userKey` - 为特定用户列出所属的组

#### 获取组信息

```bash
GET /google-workspace-admin/admin/directory/v1/groups/{groupKey}
```

`groupKey` 可以是组的电子邮件地址或唯一 ID。

#### 创建组

```bash
POST /google-workspace-admin/admin/directory/v1/groups
Content-Type: application/json

{
  "email": "engineering@example.com",
  "name": "Engineering Team",
  "description": "All engineering staff"
}
```

#### 更新组信息

```bash
PUT /google-workspace-admin/admin/directory/v1/groups/{groupKey}
Content-Type: application/json

{
  "name": "Engineering Department",
  "description": "Updated description"
}
```

#### 删除组

```bash
DELETE /google-workspace-admin/admin/directory/v1/groups/{groupKey}
```

### 组成员

#### 列出组成员

```bash
GET /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members
```

#### 添加成员

```bash
POST /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members
Content-Type: application/json

{
  "email": "user@example.com",
  "role": "MEMBER"
}
```

角色：`OWNER`、`MANAGER`、`MEMBER`

#### 更新成员的角色

```bash
PATCH /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members/{memberKey}
Content-Type: application/json

{
  "role": "MANAGER"
}
```

#### 删除成员

```bash
DELETE /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members/{memberKey}
```

### 组织单元

#### 列出组织单元

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits
```

查询参数：
- `type` - `all`（默认）或 `children`
- `orgUnitPath` - 父组织单元路径

#### 获取组织单元信息

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits/{orgUnitPath}
```

#### 创建组织单元

```bash
POST /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits
Content-Type: application/json

{
  "name": "Engineering",
  "parentOrgUnitPath": "/",
  "description": "Engineering department"
}
```

#### 更新组织单元信息

```bash
PUT /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits/{orgUnitPath}
Content-Type: application/json

{
  "description": "Updated description"
}
```

#### 删除组织单元

```bash
DELETE /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits/{orgUnitPath}
```

### 域名

#### 列出域名

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/domains
```

#### 获取域名信息

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/domains/{domainName}
```

### 角色

#### 列出角色

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/roles
```

#### 列出角色分配

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/roleassignments
```

查询参数：
- `userKey` - 按用户过滤
- `roleId` - 按角色过滤

#### 创建角色分配

```bash
POST /google-workspace-admin/admin/directory/v1/customer/my_customer/roleassignments
Content-Type: application/json

{
  "roleId": "123456789",
  "assignedTo": "user_id",
  "scopeType": "CUSTOMER"
}
```

## 代码示例

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`
};

// List users
const users = await fetch(
  'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer',
  { headers }
).then(r => r.json());

// Create user
await fetch(
  'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users',
  {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      primaryEmail: 'newuser@example.com',
      name: { givenName: 'New', familyName: 'User' },
      password: 'TempPass123!',
      changePasswordAtNextLogin: true
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# List users
users = requests.get(
    'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users',
    headers=headers,
    params={'customer': 'my_customer'}
).json()

# Create user
response = requests.post(
    'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users',
    headers=headers,
    json={
        'primaryEmail': 'newuser@example.com',
        'name': {'givenName': 'New', 'familyName': 'User'},
        'password': 'TempPass123!',
        'changePasswordAtNextLogin': True
    }
)
```

## 注意事项

- 对于您自己的域名，请使用 `my_customer` 作为客户 ID。
- 用户键可以是主要电子邮件地址或唯一用户 ID。
- 组键可以是组的电子邮件地址或唯一组 ID。
- 组织单元路径以 `/` 开头（例如：`/Engineering/Frontend`）。
- 大多数操作需要管理员权限。
- 密码必须符合 Google 的复杂性要求。
- 重要提示：当 URL 包含方括号（`fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 Google Workspace 管理连接 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 缺乏管理员权限 |
| 404 | 用户、组或资源未找到 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Admin SDK API 的传递错误 |

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

1. 确保您的 URL 路径以 `google-workspace-admin` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer`
- 错误的格式：`https://gateway.maton.ai/admin/directory/v1/users?customer=my_customer`

## 资源

- [Admin SDK 概述](https://developers.google.com/admin-sdk)
- [Directory API 用户](https://developers.google.com/admin-sdk/directory/reference/rest/v1/users)
- [Directory API 组](https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups)
- [Directory API 成员](https://developers.google.com/admin-sdk/directory/reference/rest/v1/members)
- [Directory API 组织单元](https://developers.google.com/admin-sdk/directory/reference/rest/v1/orgunits)
- [Directory API 域名](https://developers.google.com/admin-sdk/directory/reference/rest/v1/domains)
- [Directory API 角色](https://developers.google.com/admin-sdk/directory/reference/rest/v1/roles)
- [Admin SDK 文档](https://developers.google.com/admin-sdk/directory/v1/guides)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)