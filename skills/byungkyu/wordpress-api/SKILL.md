---
name: wordpress
description: |
  WordPress.com API integration with managed OAuth. Manage posts, pages, sites, and content.
  Use this skill when users want to create, read, update, or delete WordPress.com posts, pages, or manage site content.
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

# WordPress.com

您可以使用管理的 OAuth 认证来访问 WordPress.com 的 REST API，从而在托管在 WordPress.com 上的网站上创建和管理帖子、页面以及站点内容。

## 快速入门

```bash
# List posts from a site
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site_id}/posts?number=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/wordpress/rest/v1.1/{endpoint}
```

该网关会将请求代理到 `public-api.wordpress.com`，并自动插入您的 OAuth 令牌。

**注意：** WordPress.com 使用的是 REST v1.1 API。特定站点的端点遵循 `/sites/{site_id_or_domain}/{resource}` 的模式。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 WordPress.com OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=wordpress&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'wordpress'}).encode()
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
    "connection_id": "fb327990-1a43-4325-9c15-bad771b6a288",
    "status": "ACTIVE",
    "creation_time": "2026-02-10T07:46:26.908898Z",
    "last_updated_time": "2026-02-10T07:49:33.440422Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "wordpress",
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

如果您有多个 WordPress.com 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site_id}/posts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'fb327990-1a43-4325-9c15-bad771b6a288')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 站点

#### 获取站点信息

```bash
GET /wordpress/rest/v1.1/sites/{site_id_or_domain}
```

**响应：**
```json
{
  "ID": 252505333,
  "name": "My Blog",
  "description": "Just another WordPress.com site",
  "URL": "https://myblog.wordpress.com",
  "capabilities": {
    "edit_pages": true,
    "edit_posts": true,
    "edit_others_posts": true,
    "delete_posts": true
  }
}
```

站点标识符可以是：
- 数字站点 ID（例如：`252505333`）
- 域名（例如：`myblog.wordpress.com` 或 `en.blog.wordpress.com`）

### 帖子

#### 列出帖子

```bash
GET /wordpress/rest/v1.1/sites/{site}/posts
```

**查询参数：**
- `number` - 要返回的帖子数量（默认：20，最大：100）
- `offset` - 分页偏移量
- `page` - 页码
- `page_handle` - 分页游标（来自响应中的 `meta.next_page`）
- `order` - 排序方式：`DESC` 或 `ASC`
- `order_by` - 排序字段：`date`、`modified`、`title`、`comment_count`、`ID`
- `status` - 帖子状态：`publish`、`draft`、`pending`、`private`、`future`、`trash`、`any`
- `type` - 帖子类型：`post`、`page`、`any`
- `search` - 搜索词
- `category` - 分类别别名
- `tag` - 标签别名
- `author` - 作者 ID
- `fields` - 要返回的字段列表（用逗号分隔）

**响应：**
```json
{
  "found": 150,
  "posts": [
    {
      "ID": 83587,
      "site_ID": 3584907,
      "author": {
        "ID": 257479511,
        "login": "username",
        "name": "John Doe"
      },
      "date": "2026-02-09T15:00:00+00:00",
      "modified": "2026-02-09T16:30:00+00:00",
      "title": "My Post Title",
      "excerpt": "<p>Post excerpt...</p>",
      "content": "<p>Full post content...</p>",
      "slug": "my-post-title",
      "status": "publish",
      "type": "post",
      "categories": {...},
      "tags": {...}
    }
  ],
  "meta": {
    "next_page": "value=2026-02-09T15%3A00%3A00%2B00%3A00&id=83587"
  }
}
```

#### 获取帖子详细信息

```bash
GET /wordpress/rest/v1.1/sites/{site}/posts/{post_id}
```

**响应：**
```json
{
  "ID": 83587,
  "site_ID": 3584907,
  "author": {...},
  "date": "2026-02-09T15:00:00+00:00",
  "title": "My Post Title",
  "content": "<p>Full post content...</p>",
  "slug": "my-post-title",
  "status": "publish",
  "type": "post",
  "categories": {
    "news": {
      "ID": 123,
      "name": "News",
      "slug": "news"
    }
  },
  "tags": {
    "featured": {
      "ID": 456,
      "name": "Featured",
      "slug": "featured"
    }
  }
}
```

#### 创建帖子

```bash
POST /wordpress/rest/v1.1/sites/{site}/posts/new
Content-Type: application/json

{
  "title": "New Post Title",
  "content": "<p>Post content here...</p>",
  "status": "draft",
  "categories": "news, updates",
  "tags": "featured, important"
}
```

**参数：**
- `title` - 帖子标题（必填）
- `content` - 帖子内容（HTML 格式）
- `excerpt` - 帖子摘要
- `status` - 帖子状态：`publish`、`draft`、`pending`、`private`、`future`
- `date` - 帖子发布日期（ISO 8601 格式）
- `categories` - 用逗号分隔的分类别名
- `tags` - 用逗号分隔的标签别名
- `format` - 帖子格式：`standard`、`aside`、`chat`、`gallery`、`link`、`image`、`quote`、`status`、`video`、`audio`
- `slug` - 帖子 URL 别名
- `featured_image` - 特色图片附件 ID
- `sticky` - 帖子是否固定显示（布尔值）
- `password` - 保护帖子的密码

**响应：**
```json
{
  "ID": 123,
  "site_ID": 252505333,
  "title": "New Post Title",
  "status": "draft",
  "date": "2026-02-10T09:50:35+00:00"
}
```

#### 更新帖子

```bash
POST /wordpress/rest/v1.1/sites/{site}/posts/{post_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "<p>Updated content...</p>"
}
```

使用与创建帖子相同的参数。

#### 删除帖子

```bash
POST /wordpress/rest/v1.1/sites/{site}/posts/{post_id}/delete
```

将帖子移至“回收站”，并返回状态为 `status: "trash"` 的帖子。

### 页面

页面使用与帖子相同的端点，只需在 `type` 参数中指定 `page`：

#### 列出页面

```bash
GET /wordpress/rest/v1.1/sites/{site}/posts?type=page
```

#### 创建页面

```bash
POST /wordpress/rest/v1.1/sites/{site}/posts/new?type=page
Content-Type: application/json

{
  "title": "About Us",
  "content": "<p>About page content...</p>",
  "status": "publish"
}
```

#### 获取页面下拉列表

```bash
GET /wordpress/rest/v1.1/sites/{site}/dropdown-pages/
```

返回用于下拉菜单/导航的简化页面列表。

#### 获取页面模板

```bash
GET /wordpress/rest/v1.1/sites/{site}/page-templates
```

返回站点主题中可用的页面模板。

### 帖子点赞

#### 获取帖子点赞数

```bash
GET /wordpress/rest/v1.1/sites/{site}/posts/{post_id}/likes
```

**响应：**
```json
{
  "found": 99,
  "i_like": false,
  "can_like": true,
  "site_ID": 3584907,
  "post_ID": 83587,
  "likes": [...]
}
```

#### 点赞帖子

```bash
POST /wordpress/rest/v1.1/sites/{site}/posts/{post_id}/likes/new
```

#### 取消点赞帖子

```bash
POST /wordpress/rest/v1.1/sites/{site}/posts/{post_id}/likes/mine/delete
```

### 重新发布帖子

#### 检查重新发布的状态

```bash
GET /wordpress/rest/v1.1/sites/{site}/posts/{post_id}/reblogs/mine
```

**响应：**
```json
{
  "can_reblog": true,
  "can_user_reblog": true,
  "is_reblogged": false
}
```

### 帖子类型

#### 列出帖子类型

```bash
GET /wordpress/rest/v1.1/sites/{site}/post-types
```

**响应：**
```json
{
  "found": 3,
  "post_types": {
    "post": {
      "name": "post",
      "label": "Posts",
      "labels": {...}
    },
    "page": {
      "name": "page",
      "label": "Pages",
      "labels": {...}
    }
  }
}
```

### 获取帖子数量

```bash
GET /wordpress/rest/v1.1/sites/{site}/post-counts/{post_type}
```

**示例：** `/sites/{site}/post-counts/post` 或 `/sites/{site}/post-counts/page`

**响应：**
```json
{
  "counts": {
    "all": {"count": 150},
    "publish": {"count": 120},
    "draft": {"count": 25},
    "trash": {"count": 5}
  }
}
```

### 用户

#### 列出站点用户

```bash
GET /wordpress/rest/v1.1/sites/{site}/users
```

**响应：**
```json
{
  "found": 3,
  "users": [
    {
      "ID": 277004271,
      "login": "username",
      "name": "John Doe",
      "email": "john@example.com",
      "roles": ["administrator"]
    }
  ]
}
```

### 用户设置

#### 获取用户设置

```bash
GET /wordpress/rest/v1.1/me/settings
```

**响应：**
```json
{
  "enable_translator": true,
  "surprise_me": false,
  "holidaysnow": false,
  "user_login": "username"
}
```

#### 更新用户设置

```bash
POST /wordpress/rest/v1.1/me/settings/
Content-Type: application/json

{
  "enable_translator": false
}
```

### 用户点赞

#### 获取用户点赞的帖子

```bash
GET /wordpress/rest/v1.1/me/likes
```

**响应：**
```json
{
  "found": 10,
  "likes": [
    {
      "ID": 83587,
      "site_ID": 3584907,
      "title": "Liked Post Title"
    }
  ]
}
```

### 嵌入内容

#### 获取站点可用的嵌入功能

```bash
GET /wordpress/rest/v1.1/sites/{site}/embeds
```

返回站点上可用的嵌入处理程序。

### 短代码

#### 获取可用的短代码

```bash
GET /wordpress/rest/v1.1/sites/{site}/shortcodes
```

返回站点上可用的短代码。

## 分页

WordPress.com 使用基于游标的分页方式，通过 `page_handle` 进行分页：

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
}

# Initial request
response = requests.get(
    'https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site}/posts',
    headers=headers,
    params={'number': 20}
)
result = response.json()
all_posts = result['posts']

# Continue with page_handle
while result.get('meta', {}).get('next_page'):
    response = requests.get(
        'https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site}/posts',
        headers=headers,
        params={'number': 20, 'page_handle': result['meta']['next_page']}
    )
    result = response.json()
    all_posts.extend(result['posts'])

print(f"Total posts: {len(all_posts)}")
```

或者，您也可以使用 `offset` 进行简单分页：

```bash
GET /wordpress/rest/v1.1/sites/{site}/posts?number=20&offset=20
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site}/posts?number=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(`Found ${data.found} posts`);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site}/posts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'number': 10, 'status': 'publish'}
)
data = response.json()
print(f"Found {data['found']} posts")
```

### Python（创建帖子）

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site}/posts/new',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'title': 'My New Post',
        'content': '<p>Hello World!</p>',
        'status': 'draft',
        'categories': 'news',
        'tags': 'hello, first-post'
    }
)
post = response.json()
print(f"Created post ID: {post['ID']}")
```

## 注意事项

- WordPress.com API 使用的是 REST v1.1（而非 v2）
- 站点标识符可以是数字 ID 或域名
- 对 `/posts/{id}` 的 POST 请求用于更新帖子（而非 PUT/PATCH 请求）
- 删除帖子使用 `/posts/{id}/delete` 的 POST 请求（而非 HTTP DELETE 请求）
- 当在帖子中引用分类别或标签时，它们会自动创建
- 日期/时间值采用 ISO 8601 格式
- 所有内容均为 HTML 格式
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 WordPress 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足或 OAuth 范围不正确 |
| 404 | 站点或资源未找到 |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自 WordPress.com API 的传递错误 |

错误响应会包含详细信息：
```json
{
  "error": "unauthorized",
  "message": "User cannot view users for specified site"
}
```

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

1. 确保您的 URL 路径以 `wordpress` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/wordpress/rest/v1.1/sites/{site_id}/posts`
- 错误的路径：`https://gateway.maton.ai/rest/v1.1/sites/{site_id}/posts`

## 资源

- [WordPress.com REST API 概述](https://developer.wordpress.com/docs/api/)
- [入门指南](https://developer.wordpress.com/docs/api/getting-started/)
- [API 参考](https://developer.wordpress.com/docs/api/rest-api-reference/)
- [OAuth 认证](https://developer.wordpress.com/docs/oauth2/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)