---
name: confluence
description: |
  Confluence API integration with managed OAuth. Manage pages, spaces, blogposts, comments, and attachments.
  Use this skill when users want to create, read, update, or delete Confluence content, manage spaces, or work with comments and attachments.
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

# Confluence

您可以使用受管理的OAuth身份验证来访问Confluence Cloud API，从而管理页面、空间、博客文章、评论、附件和属性。

## 快速入门

```bash
# List pages in your Confluence site
python3 <<'EOF'
import urllib.request, os, json

# First get your Cloud ID
req = urllib.request.Request('https://gateway.maton.ai/confluence/oauth/token/accessible-resources')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
resources = json.load(urllib.request.urlopen(req))
cloud_id = resources[0]['id']

# Then list pages
req = urllib.request.Request(f'https://gateway.maton.ai/confluence/ex/confluence/{cloud_id}/wiki/api/v2/pages')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/confluence/{atlassian-api-path}
```

Confluence Cloud使用两种URL模式：

**V2 API（推荐使用）：**
```
https://gateway.maton.ai/confluence/ex/confluence/{cloudId}/wiki/api/v2/{resource}
```

**V1 REST API（功能有限）：**
```
https://gateway.maton.ai/confluence/ex/confluence/{cloudId}/wiki/rest/api/{resource}
```

所有API调用都需要`{cloudId}`。您可以通过`accessible-resources`端点获取它（详见下文）。

## 身份验证

所有请求都必须在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Confluence OAuth连接。

### 列出连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=confluence&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'confluence'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python3 <<'EOF'
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
    "connection_id": "6cb7787f-7c32-4658-a3c3-4ddf1367a4ce",
    "status": "ACTIVE",
    "creation_time": "2026-02-13T00:00:00.000000Z",
    "last_updated_time": "2026-02-13T00:00:00.000000Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "confluence",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成OAuth身份验证。

### 删除连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个Confluence连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python3 <<'EOF'
import urllib.request, os, json
cloud_id = "YOUR_CLOUD_ID"
req = urllib.request.Request(f'https://gateway.maton.ai/confluence/ex/confluence/{cloud_id}/wiki/api/v2/pages')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '6cb7787f-7c32-4658-a3c3-4ddf1367a4ce')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## 获取您的Cloud ID

在调用API之前，您必须获取Confluence Cloud ID：

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/confluence/oauth/token/accessible-resources')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
resources = json.load(urllib.request.urlopen(req))
print(json.dumps(resources, indent=2))
# Use resources[0]['id'] as your cloudId
EOF
```

**响应：**
```json
[
  {
    "id": "62909843-b784-4c35-b770-e4e2a26f024b",
    "name": "your-site-name",
    "url": "https://your-site.atlassian.net",
    "scopes": ["read:confluence-content.all", "write:confluence-content", ...],
    "avatarUrl": "https://..."
  }
]
```

## API参考

所有V2 API端点都使用相同的基路径：
```
/confluence/ex/confluence/{cloudId}/wiki/api/v2
```

### 页面

#### 列出页面

```bash
GET /pages
GET /pages?space-id={spaceId}
GET /pages?limit=25
GET /pages?status=current
GET /pages?body-format=storage
```

**响应：**
```json
{
  "results": [
    {
      "id": "98391",
      "status": "current",
      "title": "My Page",
      "spaceId": "98306",
      "parentId": "98305",
      "parentType": "page",
      "authorId": "557058:...",
      "createdAt": "2026-02-12T23:00:00.000Z",
      "version": {
        "number": 1,
        "authorId": "557058:...",
        "createdAt": "2026-02-12T23:00:00.000Z"
      },
      "_links": {
        "webui": "/spaces/SPACEKEY/pages/98391/My+Page"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/pages?cursor=..."
  }
}
```

#### 获取页面信息

```bash
GET /pages/{pageId}
GET /pages/{pageId}?body-format=storage
GET /pages/{pageId}?body-format=atlas_doc_format
GET /pages/{pageId}?body-format=view
```

**响应体格式：**
- `storage` - Confluence存储格式（类似XML）
- `atlas_doc_format` - Atlassian文档格式（JSON）
- `view` - 渲染后的HTML

#### 创建页面

```bash
POST /pages
Content-Type: application/json

{
  "spaceId": "98306",
  "status": "current",
  "title": "New Page Title",
  "body": {
    "representation": "storage",
    "value": "<p>Page content in storage format</p>"
  }
}
```

要创建子页面，请包含`parentId`参数：

```json
{
  "spaceId": "98306",
  "parentId": "98391",
  "status": "current",
  "title": "Child Page",
  "body": {
    "representation": "storage",
    "value": "<p>Child page content</p>"
  }
}
```

**响应：**
```json
{
  "id": "98642",
  "status": "current",
  "title": "New Page Title",
  "spaceId": "98306",
  "version": {
    "number": 1
  }
}
```

#### 更新页面

```bash
PUT /pages/{pageId}
Content-Type: application/json

{
  "id": "98391",
  "status": "current",
  "title": "Updated Page Title",
  "body": {
    "representation": "storage",
    "value": "<p>Updated content</p>"
  },
  "version": {
    "number": 2,
    "message": "Updated via API"
  }
}
```

**注意：**每次更新时都必须递增版本号。

#### 删除页面

```bash
DELETE /pages/{pageId}
```

成功时返回`204 No Content`。

#### 获取页面子内容

```bash
GET /pages/{pageId}/children
```

#### 获取页面版本信息

```bash
GET /pages/{pageId}/versions
```

#### 获取页面标签

```bash
GET /pages/{pageId}/labels
```

#### 获取页面附件

```bash
GET /pages/{pageId}/attachments
```

#### 获取页面评论

```bash
GET /pages/{pageId}/footer-comments
```

#### 获取页面属性

```bash
GET /pages/{pageId}/properties
GET /pages/{pageId}/properties/{propertyId}
```

#### 创建页面属性

```bash
POST /pages/{pageId}/properties
Content-Type: application/json

{
  "key": "my-property-key",
  "value": {"customKey": "customValue"}
}
```

#### 更新页面属性

```bash
PUT /pages/{pageId}/properties/{propertyId}
Content-Type: application/json

{
  "key": "my-property-key",
  "value": {"customKey": "updatedValue"},
  "version": {"number": 2}
}
```

#### 删除页面属性

```bash
DELETE /pages/{pageId}/properties/{propertyId}
```

### 空间

#### 列出空间

```bash
GET /spaces
GET /spaces?limit=25
GET /spaces?type=global
```

**响应：**
```json
{
  "results": [
    {
      "id": "98306",
      "key": "SPACEKEY",
      "name": "Space Name",
      "type": "global",
      "status": "current",
      "authorId": "557058:...",
      "createdAt": "2026-02-12T23:00:00.000Z",
      "homepageId": "98305",
      "_links": {
        "webui": "/spaces/SPACEKEY"
      }
    }
  ]
}
```

#### 获取空间信息

```bash
GET /spaces/{spaceId}
```

#### 获取空间中的页面

```bash
GET /spaces/{spaceId}/pages
```

#### 获取空间中的博客文章

```bash
GET /spaces/{spaceId}/blogposts
```

#### 获取空间属性

```bash
GET /spaces/{spaceId}/properties
```

#### 创建空间属性

```bash
POST /spaces/{spaceId}/properties
Content-Type: application/json

{
  "key": "space-property-key",
  "value": {"key": "value"}
}
```

#### 获取空间权限

```bash
GET /spaces/{spaceId}/permissions
```

#### 获取空间标签

```bash
GET /spaces/{spaceId}/labels
```

### 博客文章

#### 列出博客文章

```bash
GET /blogposts
GET /blogposts?space-id={spaceId}
GET /blogposts?limit=25
```

#### 获取博客文章信息

```bash
GET /blogposts/{blogpostId}
GET /blogposts/{blogpostId}?body-format=storage
```

#### 创建博客文章

```bash
POST /blogposts
Content-Type: application/json

{
  "spaceId": "98306",
  "title": "My Blog Post",
  "body": {
    "representation": "storage",
    "value": "<p>Blog post content</p>"
  }
}
```

#### 更新博客文章

```bash
PUT /blogposts/{blogpostId}
Content-Type: application/json

{
  "id": "458753",
  "status": "current",
  "title": "Updated Blog Post",
  "body": {
    "representation": "storage",
    "value": "<p>Updated content</p>"
  },
  "version": {
    "number": 2
  }
}
```

#### 删除博客文章

```bash
DELETE /blogposts/{blogpostId}
```

#### 获取博客文章标签

```bash
GET /blogposts/{blogpostId}/labels
```

#### 获取博客文章版本信息

```bash
GET /blogposts/{blogpostId}/versions
```

#### 获取博客文章评论

```bash
GET /blogposts/{blogpostId}/footer-comments
```

### 评论

#### 列出底部评论

```bash
GET /footer-comments
GET /footer-comments?body-format=storage
```

#### 获取评论信息

```bash
GET /footer-comments/{commentId}
```

#### 创建底部评论

```bash
POST /footer-comments
Content-Type: application/json

{
  "pageId": "98391",
  "body": {
    "representation": "storage",
    "value": "<p>Comment text</p>"
  }
}
```

对于博客文章的评论：
```json
{
  "blogpostId": "458753",
  "body": {
    "representation": "storage",
    "value": "<p>Comment on blogpost</p>"
  }
}
```

#### 更新评论

```bash
PUT /footer-comments/{commentId}
Content-Type: application/json

{
  "version": {"number": 2},
  "body": {
    "representation": "storage",
    "value": "<p>Updated comment</p>"
  }
}
```

#### 删除评论

```bash
DELETE /footer-comments/{commentId}
```

#### 获取评论回复

```bash
GET /footer-comments/{commentId}/children
```

#### 列出内联评论

```bash
GET /inline-comments
```

### 附件

#### 列出附件

```bash
GET /attachments
GET /attachments?limit=25
```

#### 获取附件信息

```bash
GET /attachments/{attachmentId}
```

#### 获取页面上的附件

```bash
GET /pages/{pageId}/attachments
```

### 任务

#### 列出任务

```bash
GET /tasks
```

#### 获取任务信息

```bash
GET /tasks/{taskId}
```

### 标签

#### 列出标签

```bash
GET /labels
GET /labels?prefix=global
```

### 自定义内容

#### 列出自定义内容

```bash
GET /custom-content
GET /custom-content?type={customContentType}
```

### 用户（V1 API）

当前用户端点使用V1 REST API：

```bash
GET /confluence/ex/confluence/{cloudId}/wiki/rest/api/user/current
```

**响应：**
```json
{
  "type": "known",
  "accountId": "557058:...",
  "accountType": "atlassian",
  "email": "user@example.com",
  "publicName": "User Name",
  "displayName": "User Name"
}
```

## 分页

V2 API使用基于游标的分页方式。当还有更多结果时，响应中会包含 `_links.next` URL。

```bash
GET /pages?limit=25
```

**响应：**
```json
{
  "results": [...],
  "_links": {
    "next": "/wiki/api/v2/pages?cursor=eyJpZCI6Ijk4MzkyIn0"
  }
}
```

要获取下一页，请提取游标并传递它：

```bash
GET /pages?limit=25&cursor=eyJpZCI6Ijk4MzkyIn0
```

## 代码示例

### JavaScript

```javascript
// Get Cloud ID first
const resourcesRes = await fetch(
  'https://gateway.maton.ai/confluence/oauth/token/accessible-resources',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const resources = await resourcesRes.json();
const cloudId = resources[0].id;

// List pages
const response = await fetch(
  `https://gateway.maton.ai/confluence/ex/confluence/${cloudId}/wiki/api/v2/pages`,
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

# Get Cloud ID first
resources = requests.get(
    'https://gateway.maton.ai/confluence/oauth/token/accessible-resources',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
).json()
cloud_id = resources[0]['id']

# List pages
response = requests.get(
    f'https://gateway.maton.ai/confluence/ex/confluence/{cloud_id}/wiki/api/v2/pages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- **必须获取Cloud ID**：在调用API之前，您需要通过`/oauth/token/accessible-resources`获取Cloud ID。
- **推荐使用V2 API**：对于大多数操作，请使用V2 API（`/wiki/api/v2/`）。V1 API（`/wiki/rest/api/`）的功能有限。
- **响应体格式**：使用`storage`格式来创建/更新内容；使用`view`格式来获取渲染后的HTML。
- **版本号**：更新页面或博客文章时，必须递增版本号。
- **存储格式**：内容采用Confluence存储格式（类似XML）。例如：`<p>段落</p>`、`<h1>标题</h1>`。
- **删除操作返回204**：DELETE操作返回`204 No Content`，且不返回响应体。
- **ID为字符串**：页面、空间等ID应以字符串形式传递。
- **重要提示**：当将curl输出传递给`jq`或其他命令时，在某些Shell环境中，环境变量（如`$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或数据格式错误 |
| 401 | API密钥无效或OAuth权限不足 |
| 403 | 没有权限 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，标题重复） |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自Confluence API的传递错误 |

### 故障排除：API密钥问题

1. 确保`MATON_API_KEY`环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

确保您的URL路径以`confluence`开头。例如：

- 正确：`https://gateway.maton.ai/confluence/ex/confluence/{cloudId}/wiki/api/v2/pages`
- 错误：`https://gateway.maton.ai/ex/confluence/{cloudId}/wiki/api/v2/pages`

### 故障排除：权限问题

如果收到“scope does not match”的错误，您可能需要使用所需的权限范围重新授权。请删除现有连接并创建一个新的连接：

```bash
# Delete existing connection
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF

# Create new connection
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'confluence'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 资源

- [Confluence REST API V2文档](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
- [Confluence REST API V2参考](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/)
- [Confluence存储格式](https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)