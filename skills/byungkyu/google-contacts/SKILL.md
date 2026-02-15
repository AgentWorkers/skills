---
name: google-contacts
description: |
  Google Contacts API integration with managed OAuth. Manage contacts, contact groups, and search your address book.
  Use this skill when users want to create, read, update, or delete contacts, manage contact groups, or search for people in their Google account.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Contacts

您可以使用托管的 OAuth 认证来访问 Google People API，从而管理联系人、联系人组，并搜索您的通讯录。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-contacts/v1/people/me/connections?personFields=names,emailAddresses,phoneNumbers&pageSize=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-contacts/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google People API 端点路径。该网关会将请求代理到 `people.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google Contacts OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-contacts&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-contacts'}).encode()
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
    "app": "google-contacts",
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

如果您有多个 Google Contacts 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-contacts/v1/people/me/connections?personFields=names&pageSize=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 联系人操作

#### 列出联系人

```bash
GET /google-contacts/v1/people/me/connections?personFields=names,emailAddresses,phoneNumbers&pageSize=100
```

**查询参数：**
- `personFields`（必填）：需要返回的字段列表（详见“联系人字段”部分）
- `pageSize`：返回的联系人数（最多 1000 人，默认为 100 人）
- `pageToken`：分页令牌
- `sortOrder`：`LAST_MODIFIED_ASCENDING`、`LAST_MODIFIED_DESCENDING`、`FIRST_NAME_ASCENDING` 或 `LAST_NAME_ASCENDING`

**响应：**
```json
{
  "connections": [
    {
      "resourceName": "people/c1234567890",
      "names": [{"displayName": "John Doe", "givenName": "John", "familyName": "Doe"}],
      "emailAddresses": [{"value": "john@example.com"}],
      "phoneNumbers": [{"value": "+1-555-0123"}]
    }
  ],
  "totalPeople": 1,
  "totalItems": 1,
  "nextPageToken": "..."
}
```

#### 获取联系人信息

```bash
GET /google-contacts/v1/people/{resourceName}?personFields=names,emailAddresses,phoneNumbers
```

使用列表或创建操作返回的资源名称（例如：`people/c1234567890`）。

#### 创建联系人

```bash
POST /google-contacts/v1/people:createContact
Content-Type: application/json

{
  "names": [{"givenName": "John", "familyName": "Doe"}],
  "emailAddresses": [{"value": "john@example.com"}],
  "phoneNumbers": [{"value": "+1-555-0123"}],
  "organizations": [{"name": "Acme Corp", "title": "Engineer"}]
}
```

#### 更新联系人信息

```bash
PATCH /google-contacts/v1/people/{resourceName}:updateContact?updatePersonFields=names,emailAddresses
Content-Type: application/json

{
  "etag": "%EgcBAgkLLjc9...",
  "names": [{"givenName": "John", "familyName": "Smith"}],
  "emailAddresses": [{"value": "john.smith@example.com"}]
}
```

**注意：** 请包含从获取/列出响应中得到的 `etag`，以确保更新的是最新版本的信息。

#### 删除联系人

```bash
DELETE /google-contacts/v1/people/{resourceName}:deleteContact
```

#### 批量获取联系人信息

```bash
GET /google-contacts/v1/people:batchGet?resourceNames=people/c123&resourceNames=people/c456&personFields=names,emailAddresses
```

#### 批量创建联系人信息

```bash
POST /google-contacts/v1/people:batchCreateContacts
Content-Type: application/json

{
  "contacts": [
    {
      "contactPerson": {
        "names": [{"givenName": "Alice", "familyName": "Smith"}],
        "emailAddresses": [{"value": "alice@example.com"}]
      }
    },
    {
      "contactPerson": {
        "names": [{"givenName": "Bob", "familyName": "Jones"}],
        "emailAddresses": [{"value": "bob@example.com"}]
      }
    }
  ],
  "readMask": "names,emailAddresses"
}
```

#### 批量删除联系人信息

```bash
POST /google-contacts/v1/people:batchDeleteContacts
Content-Type: application/json

{
  "resourceNames": ["people/c123", "people/c456"]
}
```

#### 搜索联系人

```bash
GET /google-contacts/v1/people:searchContacts?query=John&readMask=names,emailAddresses
```

**注意：** 对于新创建的联系人，搜索结果可能会有延迟，因为系统需要对其进行索引。

### 联系人组操作

#### 列出联系人组

```bash
GET /google-contacts/v1/contactGroups?pageSize=100
```

**响应：**
```json
{
  "contactGroups": [
    {
      "resourceName": "contactGroups/starred",
      "groupType": "SYSTEM_CONTACT_GROUP",
      "name": "starred",
      "formattedName": "Starred"
    },
    {
      "resourceName": "contactGroups/abc123",
      "groupType": "USER_CONTACT_GROUP",
      "name": "Work",
      "formattedName": "Work",
      "memberCount": 5
    }
  ],
  "totalItems": 2
}
```

#### 获取联系人组信息

```bash
GET /google-contacts/v1/contactGroups/{resourceName}?maxMembers=100
```

可以使用 `contactGroups/starred`、`contactGroups/family` 等来表示系统联系人组，或使用资源名称来表示用户联系人组。

#### 创建联系人组

```bash
POST /google-contacts/v1/contactGroups
Content-Type: application/json

{
  "contactGroup": {
    "name": "Work Contacts"
  }
}
```

#### 删除联系人组

```bash
DELETE /google-contacts/v1/contactGroups/{resourceName}?deleteContacts=false
```

设置 `deleteContacts=true` 以同时删除该联系人组中的所有联系人。

#### 批量获取联系人组信息

```bash
GET /google-contacts/v1/contactGroups:batchGet?resourceNames=contactGroups/starred&resourceNames=contactGroups/family
```

#### 修改联系人组成员

向联系人组中添加或删除联系人：

```bash
POST /google-contacts/v1/contactGroups/{resourceName}/members:modify
Content-Type: application/json

{
  "resourceNamesToAdd": ["people/c123", "people/c456"],
  "resourceNamesToRemove": ["people/c789"]
}
```

### 其他联系人

其他联系人是指您通过电子邮件等方式有过互动但尚未明确添加到您的联系人列表中的人。

#### 列出其他联系人

```bash
GET /google-contacts/v1/otherContacts?readMask=names,emailAddresses&pageSize=100
```

#### 将其他联系人复制到我的联系人列表中

```bash
POST /google-contacts/v1/{resourceName}:copyOtherContactToMyContactsGroup
Content-Type: application/json

{
  "copyMask": "names,emailAddresses,phoneNumbers"
}
```

## 联系人字段

您可以使用以下字段与 `personFields` 或 `readMask` 参数一起使用：

| 字段 | 描述 |
|-------|-------------|
| `names` | 显示名称（包括名和姓） |
| `emailAddresses` | 带类型的电子邮件地址 |
| `phoneNumbers` | 带类型的电话号码 |
| `addresses` | 邮政地址 |
| `organizations` | 公司、职位、部门 |
| `biographies` | 有关此人的简介/备注 |
| `birthdays` | 生日信息 |
| `urls` | 个人网站链接 |
| `photos` | 个人资料照片 |
| `memberships` | 所在的联系人组 |
| `metadata` | 来源和更新信息 |

多个字段的示例：`personFields=names,emailAddresses,phoneNumbers,organizations`

## 分页

使用 `pageSize` 和 `pageToken` 进行分页：

```bash
GET /google-contacts/v1/people/me/connections?personFields=names&pageSize=100&pageToken=NEXT_PAGE_TOKEN
```

响应中包含分页信息：

```json
{
  "connections": [...],
  "totalPeople": 500,
  "nextPageToken": "...",
  "nextSyncToken": "..."
}
```

继续使用 `pageToken` 进行请求，直到不再返回 `nextPageToken`。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-contacts/v1/people/me/connections?personFields=names,emailAddresses&pageSize=50',
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
    'https://gateway.maton.ai/google-contacts/v1/people/me/connections',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={
        'personFields': 'names,emailAddresses,phoneNumbers',
        'pageSize': 50
    }
)
data = response.json()
```

## 注意事项

- 联系人的资源名称遵循 `people/c{id}` 的模式（例如：`people/c1234567890`）
- 联系人组的资源名称遵循 `contactGroups/{id}` 的模式（例如：`contactGroups/abc123`）
- 系统联系人组包括：`starred`、`friends`、`family`、`coworkers`、`myContacts`、`all`、`blocked`
- 对于大多数读取操作，`personFields` 参数是必需的
- 在更新联系人信息时，请包含 `etag` 以避免覆盖其他用户的更改
- 对同一用户进行多次修改时，应依次发送请求，以避免延迟增加和失败
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 选项来禁用全局解析
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google Contacts 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限被拒绝（请检查 OAuth 权限范围） |
| 404 | 未找到联系人或联系人组 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Google People API 的传递错误 |

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

1. 确保您的 URL 路径以 `google-contacts` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/google-contacts/v1/people/me/connections`
  - 错误的路径：`https://gateway.maton.ai/v1/people/me/connections`

## 资源

- [Google People API 概述](https://developers.google.com/people/api/rest)
- [联系人资源](https://developers.google.com/people/api/rest/v1/people)
- [联系人组资源](https://developers.google.com/people/api/rest/v1/contactGroups)
- [联系人字段参考](https://developers.google.com/people/api/rest/v1/people#Person)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)