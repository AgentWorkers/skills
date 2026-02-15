---
name: vimeo
description: |
  Vimeo API integration with managed OAuth. Video hosting and sharing platform.
  Use this skill when users want to upload, manage, or organize videos, create showcases/albums, manage folders, or interact with the Vimeo community.
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

# Vimeo

您可以使用托管的 OAuth 认证来访问 Vimeo API。该 API 允许您上传和管理视频、创建展示集和文件夹、管理视频的点赞次数以及安排视频的观看时间，同时还能与 Vimeo 社区进行互动。

## 快速入门

```bash
# Get current user info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/vimeo/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/vimeo/{resource}
```

该网关会将请求代理到 `api.vimeo.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Vimeo OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=vimeo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'vimeo'}).encode()
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
    "connection_id": "a6ecb894-3148-4f4c-a54c-e9d917e3f2a9",
    "status": "ACTIVE",
    "creation_time": "2026-02-09T08:56:53.522100Z",
    "last_updated_time": "2026-02-09T08:58:39.407864Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "vimeo",
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

如果您有多个 Vimeo 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/vimeo/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'a6ecb894-3148-4f4c-a54c-e9d917e3f2a9')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户操作

#### 获取当前用户信息

```bash
GET /vimeo/me
```

**响应：**
```json
{
  "uri": "/users/254399456",
  "name": "Chris",
  "link": "https://vimeo.com/user254399456",
  "account": "free",
  "created_time": "2026-02-09T07:00:20+00:00",
  "pictures": {...},
  "metadata": {
    "connections": {
      "videos": {"uri": "/users/254399456/videos", "total": 2},
      "albums": {"uri": "/users/254399456/albums", "total": 0},
      "folders": {"uri": "/users/254399456/folders", "total": 0},
      "likes": {"uri": "/users/254399456/likes", "total": 0},
      "followers": {"uri": "/users/254399456/followers", "total": 0},
      "following": {"uri": "/users/254399456/following", "total": 0}
    }
  }
}
```

#### 根据 ID 获取用户信息

```bash
GET /vimeo/users/{user_id}
```

#### 获取用户动态

```bash
GET /vimeo/me/feed
```

### 视频操作

#### 列出用户发布的视频

```bash
GET /vimeo/me/videos
```

**响应：**
```json
{
  "total": 2,
  "page": 1,
  "per_page": 25,
  "paging": {
    "next": null,
    "previous": null,
    "first": "/me/videos?page=1",
    "last": "/me/videos?page=1"
  },
  "data": [
    {
      "uri": "/videos/1163160198",
      "name": "My Video",
      "description": "Video description",
      "link": "https://vimeo.com/1163160198",
      "duration": 20,
      "width": 1920,
      "height": 1080,
      "created_time": "2026-02-09T07:05:00+00:00"
    }
  ]
}
```

#### 获取单个视频信息

```bash
GET /vimeo/videos/{video_id}
```

#### 搜索视频

```bash
GET /vimeo/videos?query=nature&per_page=10
```

查询参数：
- `query` - 搜索关键字
- `per_page` - 每页显示的结果数量（最多 100 个）
- `page` - 页码
- `sort` - 排序方式：`relevant`（相关）、`date`（日期）、`alphabetical`（字母顺序）、`plays`（播放次数）、`likes`（点赞次数）、`comments`（评论数量）、`duration`（时长）
- `direction` - 排序方向：`asc`（升序）、`desc`（降序）

#### 更新视频信息

```bash
PATCH /vimeo/videos/{video_id}
Content-Type: application/json

{
  "name": "New Video Title",
  "description": "Updated description"
}
```

#### 删除视频

```bash
DELETE /vimeo/videos/{video_id}
```

成功时返回 204（表示“无内容”）。

### 文件夹操作（项目）

#### 列出文件夹

```bash
GET /vimeo/me/folders
```

**响应：**
```json
{
  "total": 1,
  "page": 1,
  "per_page": 25,
  "data": [
    {
      "uri": "/users/254399456/projects/28177219",
      "name": "My Folder",
      "created_time": "2026-02-09T08:59:20+00:00",
      "privacy": {"view": "nobody"},
      "manage_link": "https://vimeo.com/user/254399456/folder/28177219"
    }
  ]
}
```

#### 创建文件夹

```bash
POST /vimeo/me/folders
Content-Type: application/json

{
  "name": "New Folder"
}
```

#### 更新文件夹信息

```bash
PATCH /vimeo/me/projects/{project_id}
Content-Type: application/json

{
  "name": "Renamed Folder"
}
```

#### 删除文件夹

```bash
DELETE /vimeo/me/projects/{project_id}
```

成功时返回 204（表示“无内容”）。

#### 获取文件夹中的视频列表

```bash
GET /vimeo/me/projects/{project_id}/videos
```

#### 将视频添加到文件夹中

```bash
PUT /vimeo/me/projects/{project_id}/videos/{video_id}
```

成功时返回 204（表示“无内容”）。

#### 从文件夹中删除视频

```bash
DELETE /vimeo/me/projects/{project_id}/videos/{video_id}
```

### 相册操作（展示集）

#### 列出相册

```bash
GET /vimeo/me/albums
```

#### 创建相册

```bash
POST /vimeo/me/albums
Content-Type: application/json

{
  "name": "My Showcase",
  "description": "A collection of videos"
}
```

**响应：**
```json
{
  "uri": "/users/254399456/albums/12099981",
  "name": "My Showcase",
  "description": "A collection of videos",
  "created_time": "2026-02-09T09:00:00+00:00"
}
```

#### 更新相册信息

```bash
PATCH /vimeo/me/albums/{album_id}
Content-Type: application/json

{
  "name": "Updated Showcase Name"
}
```

#### 删除相册

```bash
DELETE /vimeo/me/albums/{album_id}
```

成功时返回 204（表示“无内容”）。

#### 获取相册中的视频列表

```bash
GET /vimeo/me/albums/{album_id}/videos
```

#### 将视频添加到相册中

```bash
PUT /vimeo/me/albums/{album_id}/videos/{video_id}
```

成功时返回 204（表示“无内容”）。

#### 从相册中删除视频

```bash
DELETE /vimeo/me/albums/{album_id}/videos/{video_id}
```

### 评论操作

#### 获取视频评论

```bash
GET /vimeo/videos/{video_id}/comments
```

#### 添加评论

```bash
POST /vimeo/videos/{video_id}/comments
Content-Type: application/json

{
  "text": "Great video!"
}
```

**响应：**
```json
{
  "uri": "/videos/1163160198/comments/21372988",
  "text": "Great video!",
  "created_on": "2026-02-09T09:05:00+00:00"
}
```

#### 删除评论

```bash
DELETE /vimeo/videos/{video_id}/comments/{comment_id}
```

成功时返回 204（表示“无内容”）。

### 点赞操作

#### 获取用户点赞的视频列表

```bash
GET /vimeo/me/likes
```

#### 给视频点赞

```bash
PUT /vimeo/me/likes/{video_id}
```

成功时返回 204（表示“无内容”）。

#### 取消对视频的点赞

```bash
DELETE /vimeo/me/likes/{video_id}
```

成功时返回 204（表示“无内容”）。

### 安排视频观看

#### 获取待观看视频列表

```bash
GET /vimeo/me/watchlater
```

#### 将视频添加到待观看列表

```bash
PUT /vimeo/me/watchlater/{video_id}
```

成功时返回 204（表示“无内容”）。

#### 从待观看列表中删除视频

```bash
DELETE /vimeo/me/watchlater/{video_id}
```

成功时返回 204（表示“无内容”）。

### 关注者与被关注者

#### 获取用户关注者列表

```bash
GET /vimeo/me/followers
```

#### 获取用户关注列表

```bash
GET /vimeo/me/following
```

#### 关注用户

```bash
PUT /vimeo/me/following/{user_id}
```

#### 取消关注用户

```bash
DELETE /vimeo/me/following/{user_id}
```

### 频道与分类

#### 列出所有频道

```bash
GET /vimeo/channels
```

#### 获取单个频道信息

```bash
GET /vimeo/channels/{channel_id}
```

#### 列出所有分类

```bash
GET /vimeo/categories
```

**响应：**
```json
{
  "total": 10,
  "data": [
    {"uri": "/categories/animation", "name": "Animation"},
    {"uri": "/categories/comedy", "name": "Comedy"},
    {"uri": "/categories/documentary", "name": "Documentary"}
  ]
}
```

#### 获取某个分类下的视频列表

```bash
GET /vimeo/categories/{category}/videos
```

## 分页

Vimeo 使用基于页码的分页机制：

```bash
GET /vimeo/me/videos?page=1&per_page=25
```

**响应：**
```json
{
  "total": 50,
  "page": 1,
  "per_page": 25,
  "paging": {
    "next": "/me/videos?page=2",
    "previous": null,
    "first": "/me/videos?page=1",
    "last": "/me/videos?page=2"
  },
  "data": [...]
}
```

参数：
- `page` - 页码（默认为 1）
- `per_page` - 每页显示的结果数量（默认为 25 个，最多 100 个）

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/vimeo/me/videos',
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
    'https://gateway.maton.ai/vimeo/me/videos',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python（创建文件夹）

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/vimeo/me/folders',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'name': 'New Folder'}
)
folder = response.json()
print(f"Created folder: {folder['uri']}")
```

### Python（更新视频信息）

```python
import os
import requests

video_id = "1163160198"
response = requests.patch(
    f'https://gateway.maton.ai/vimeo/videos/{video_id}',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'Updated Title',
        'description': 'New description'
    }
)
video = response.json()
print(f"Updated video: {video['name']}")
```

## 注意事项

- 视频 ID 为数字格式（例如：`1163160198`）
- 用户 ID 为数字格式（例如：`254399456`）
- 在 API 路径中，文件夹被称为 “projects”
- 在 Vimeo 用户界面中，相册也被称为 “Showcases”
- `DELETE` 和 `PUT` 操作成功时返回 204（表示“无内容”）
- 视频上传需要使用 TUS 协议（此处未详细说明）
- 各账户类型的速率限制有所不同
- 重要提示：当将 curl 命令的输出传递给 `jq` 或其他工具时，环境变量 `$MATON_API_KEY` 在某些 shell 环境中可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Vimeo 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足或权限范围不正确 |
| 404 | 资源未找到 |
| 429 | 超过速率限制 |
| 4xx/5xx | 来自 Vimeo API 的传递错误 |

Vimeo 的错误代码会附带详细的错误信息：
```json
{
  "error": "Your access token does not have the \"create\" scope"
}
```

### 故障排除：API 密钥问题

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

### 故障排除：应用名称错误

1. 确保您的 URL 路径以 `vimeo` 开头。例如：
- 正确格式：`https://gateway.maton.ai/vimeo/me/videos`
- 错误格式：`https://gateway.maton.ai/me/videos`

## 资源

- [Vimeo API 参考文档](https://developer.vimeo.com/api/reference)
- [Vimeo 开发者门户](https://developer.vimeo.com)
- [Vimeo API 认证指南](https://developer.vimeo.com/api/authentication)
- [Vimeo 上传 API](https://developer.vimeo.com/api/upload/videos)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 技术支持](mailto:support@maton.ai)