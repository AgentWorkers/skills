---
name: companycam
description: |
  CompanyCam API integration with managed OAuth. Photo documentation platform for contractors.
  Use this skill when users want to manage projects, photos, users, tags, groups, or documents in CompanyCam.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# CompanyCam

您可以使用受管理的 OAuth 认证来访问 CompanyCam API。该 API 允许您管理项目、照片、用户、标签、组、文档以及用于承包商照片记录的 Webhook。

## 快速入门

```bash
# List projects
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/companycam/v2/projects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/companycam/v2/{resource}
```

请将 `{resource}` 替换为实际的 CompanyCam API 端点路径。该网关会将请求代理到 `api.companycam.com/v2` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 CompanyCam OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=companycam&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'companycam'}).encode()
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
    "connection_id": "d274cf68-9e76-464c-92e3-ff274c44526e",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T01:56:32.259046Z",
    "last_updated_time": "2026-02-12T01:57:38.944271Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "companycam",
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

如果您有多个 CompanyCam 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/companycam/v2/projects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'd274cf68-9e76-464c-92e3-ff274c44526e')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最新的）活动连接。

## API 参考

### 公司信息

#### 获取公司信息

```bash
GET /companycam/v2/company
```

返回当前公司的信息。

### 用户信息

#### 获取当前用户

```bash
GET /companycam/v2/users/current
```

#### 列出用户

```bash
GET /companycam/v2/users
```

查询参数：
- `page` - 页码
- `per_page` - 每页显示的结果数量（默认：25）
- `status` - 按状态过滤（活动/非活动）

#### 创建用户

```bash
POST /companycam/v2/users
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email_address": "john@example.com",
  "user_role": "standard"
}
```

用户角色：`admin`、`standard`、`limited`

#### 获取用户信息

```bash
GET /companycam/v2/users/{id}
```

#### 更新用户信息

```bash
PUT /companycam/v2/users/{id}
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith"
}
```

#### 删除用户

```bash
DELETE /companycam/v2/users/{id}
```

### 项目信息

#### 列出项目

```bash
GET /companycam/v2/projects
```

查询参数：
- `page` - 页码
- `per_page` - 每页显示的结果数量（默认：25）
- `query` - 搜索查询
- `status` - 按状态过滤
- `modified_since` - 用于过滤的 Unix 时间戳

#### 创建项目

```bash
POST /companycam/v2/projects
Content-Type: application/json

{
  "name": "New Construction Project",
  "address": {
    "street_address_1": "123 Main St",
    "city": "Los Angeles",
    "state": "CA",
    "postal_code": "90210",
    "country": "US"
  }
}
```

#### 获取项目信息

```bash
GET /companycam/v2/projects/{id}
```

#### 更新项目信息

```bash
PUT /companycam/v2/projects/{id}
Content-Type: application/json

{
  "name": "Updated Project Name"
}
```

#### 删除项目

```bash
DELETE /companycam/v2/projects/{id}
```

#### 归档项目

```bash
PATCH /companycam/v2/projects/{id}/archive
```

#### 恢复项目

```bash
PUT /companycam/v2/projects/{id}/restore
```

### 项目照片

#### 列出项目照片

```bash
GET /companycam/v2/projects/{project_id}/photos
```

查询参数：
- `page` - 页码
- `per_page` - 每页显示的结果数量
- `start_date` - 按开始日期过滤（Unix 时间戳）
- `end_date` - 按结束日期过滤（Unix 时间戳）
- `user_ids` - 按用户 ID 过滤
- `group_ids` - 按组 ID 过滤
- `tag_ids` - 按标签 ID 过滤

#### 向项目添加照片

```bash
POST /companycam/v2/projects/{project_id}/photos
Content-Type: application/json

{
  "uri": "https://example.com/photo.jpg",
  "captured_at": 1609459200,
  "coordinates": {
    "lat": 34.0522,
    "lon": -118.2437
  },
  "tags": ["exterior", "front"]
}
```

### 项目评论

#### 列出项目评论

```bash
GET /companycam/v2/projects/{project_id}/comments
```

#### 添加项目评论

```bash
POST /companycam/v2/projects/{project_id}/comments
Content-Type: application/json

{
  "comment": {
    "content": "Work completed successfully"
  }
}
```

### 项目标签

#### 列出项目标签

```bash
GET /companycam/v2/projects/{project_id}/labels
```

#### 向项目添加标签

```bash
POST /companycam/v2/projects/{project_id}/labels
Content-Type: application/json

{
  "labels": ["priority", "urgent"]
}
```

#### 删除项目标签

```bash
DELETE /companycam/v2/projects/{project_id}/labels/{label_id}
```

### 项目文档

#### 列出项目文档

```bash
GET /companycam/v2/projects/{project_id}/documents
```

#### 上传文档

```bash
POST /companycam/v2/projects/{project_id}/documents
Content-Type: application/json

{
  "uri": "https://example.com/document.pdf",
  "name": "Contract.pdf"
}
```

### 项目检查表

#### 列出项目检查表

```bash
GET /companycam/v2/projects/{project_id}/checklists
```

#### 根据模板创建检查表

```bash
POST /companycam/v2/projects/{project_id}/checklists
Content-Type: application/json

{
  "checklist_template_id": "template_id"
}
```

#### 获取项目检查表信息

```bash
GET /companycam/v2/projects/{project_id}/checklists/{checklist_id}
```

### 项目用户

#### 列出分配给项目的用户

```bash
GET /companycam/v2/projects/{project_id}/assigned_users
```

#### 将用户分配给项目

```bash
PUT /companycam/v2/projects/{project_id}/assigned_users/{user_id}
```

### 项目协作者

#### 列出项目协作者

```bash
GET /companycam/v2/projects/{project_id}/collaborators
```

### 照片

#### 列出所有照片

```bash
GET /companycam/v2/photos
```

查询参数：
- `page` - 页码
- `per_page` - 每页显示的结果数量

#### 获取照片信息

```bash
GET /companycam/v2/photos/{id}
```

#### 更新照片信息

```bash
PUT /companycam/v2/photos/{id}
Content-Type: application/json

{
  "photo": {
    "captured_at": 1609459200
  }
}
```

#### 删除照片

```bash
DELETE /companycam/v2/photos/{id}
```

#### 列出照片标签

```bash
GET /companycam/v2/photos/{id}/tags
```

#### 向照片添加标签

```bash
POST /companycam/v2/photos/{id}/tags
Content-Type: application/json

{
  "tags": ["exterior", "completed"]
}
```

#### 列出照片评论

```bash
GET /companycam/v2/photos/{id}/comments
```

#### 添加照片评论

```bash
POST /companycam/v2/photos/{id}/comments
Content-Type: application/json

{
  "comment": {
    "content": "Great progress!"
  }
}
```

### 标签

#### 列出所有标签

```bash
GET /companycam/v2/tags
```

#### 创建标签

```bash
POST /companycam/v2/tags
Content-Type: application/json

{
  "display_value": "Exterior",
  "color": "#FF5733"
}
```

#### 获取标签信息

```bash
GET /companycam/v2/tags/{id}
```

#### 更新标签信息

```bash
PUT /companycam/v2/tags/{id}
Content-Type: application/json

{
  "display_value": "Interior",
  "color": "#3498DB"
}
```

#### 删除标签

```bash
DELETE /companycam/v2/tags/{id}
```

### 组信息

#### 列出所有组

```bash
GET /companycam/v2/groups
```

#### 创建组

```bash
POST /companycam/v2/groups
Content-Type: application/json

{
  "name": "Roofing Team"
}
```

#### 获取组信息

```bash
GET /companycam/v2/groups/{id}
```

#### 更新组信息

```bash
PUT /companycam/v2/groups/{id}
Content-Type: application/json

{
  "name": "Updated Team Name"
}
```

#### 删除组

```bash
DELETE /companycam/v2/groups/{id}
```

### 检查表

#### 列出所有检查表

```bash
GET /companycam/v2/checklists
```

查询参数：
- `page` - 页码
- `per_page` - 每页显示的结果数量
- `completed` - 按完成状态过滤（true/false）

### Webhook

#### 列出所有 Webhook

```bash
GET /companycam/v2/webhooks
```

#### 创建 Webhook

```bash
POST /companycam/v2/webhooks
Content-Type: application/json

{
  "url": "https://example.com/webhook",
  "scopes": ["project.created", "photo.created"]
}
```

可用的作用域：
- `project-created`
- `project.updated`
- `project_deleted`
- `photo-created`
- `photo.updated`
- `photo_deleted`
- `document-created`
- `label-created`
- `label_deleted`

#### 获取 Webhook 信息

```bash
GET /companycam/v2/webhooks/{id}
```

#### 更新 Webhook

```bash
PUT /companycam/v2/webhooks/{id}
Content-Type: application/json

{
  "url": "https://example.com/new-webhook",
  "enabled": true
}
```

#### 删除 Webhook

```bash
DELETE /companycam/v2/webhooks/{id}
```

## 分页

CompanyCam 使用基于页码的分页机制：

```bash
GET /companycam/v2/projects?page=2&per_page=25
```

查询参数：
- `page` - 页码（默认：1）
- `per_page` - 每页显示的结果数量（默认：25）

## 代码示例

### JavaScript - 列出项目

```javascript
const response = await fetch(
  'https://gateway.maton.ai/companycam/v2/projects?per_page=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const projects = await response.json();
console.log(projects);
```

### Python - 列出项目

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/companycam/v2/projects',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'per_page': 10}
)
projects = response.json()
for project in projects:
    print(f"{project['name']}: {project['id']}")
```

### Python - 创建包含照片的项目

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
base_url = 'https://gateway.maton.ai/companycam/v2'

# Create project
project_response = requests.post(
    f'{base_url}/projects',
    headers=headers,
    json={
        'name': 'Kitchen Renovation',
        'address': {
            'street_address_1': '456 Oak Ave',
            'city': 'Denver',
            'state': 'CO',
            'postal_code': '80202',
            'country': 'US'
        }
    }
)
project = project_response.json()
print(f"Created project: {project['id']}")

# Add photo to project
photo_response = requests.post(
    f'{base_url}/projects/{project["id"]}/photos',
    headers=headers,
    json={
        'uri': 'https://example.com/kitchen-before.jpg',
        'tags': ['before', 'kitchen']
    }
)
photo = photo_response.json()
print(f"Added photo: {photo['id']}")
```

## 注意事项

- 项目 ID 和其他 ID 以字符串形式返回。
- 时间戳为 Unix 时间戳（自纪元以来的秒数）。
- 可以通过 URL（uri 参数）添加照片。
- 评论必须封装在 `comment` 对象中。
- Webhook 使用 `scopes` 参数（而不是 `events`）。
- 用户角色：`admin`、`standard`、`limited`。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 以避免全局解析。
- 重要提示：将 curl 输出传递给 `jq` 时，环境变量可能无法正确解析。建议使用 Python 示例。

## 速率限制

| 操作 | 限制 |
|-----------|-------|
| GET 请求 | 每分钟 240 次 |
| POST/PUT/DELETE | 每分钟 100 次 |

当达到速率限制时，API 会返回 429 状态码。请实施指数退避策略进行重试。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或缺少 CompanyCam 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 422 | 验证错误（请检查错误消息） |
| 429 | 达到速率限制 |
| 4xx/5xx | 来自 CompanyCam API 的传递错误 |

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

1. 确保您的 URL 路径以 `companycam` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/companycam/v2/projects`
- 错误的路径：`https://gateway.maton.ai/v2/projects`

## 资源

- [CompanyCam API 文档](https://docs.companycam.com)
- [CompanyCam API 参考](https://docs.companycam.com/reference)
- [CompanyCam 快速入门](https://docs.companycam.com/docs/getting-started)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)