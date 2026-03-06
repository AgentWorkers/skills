---
name: sharepoint
description: >
  通过 Microsoft Graph 和托管的 OAuth 实现 SharePoint API 集成。可以访问 SharePoint 网站、列表、文档库和文件。  
  当用户需要使用 SharePoint 进行文档管理、列表操作或网站内容管理时，可以使用此技能。  
  对于其他第三方应用程序，请使用 `api-gateway` 技能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# SharePoint

您可以通过 Microsoft Graph API 使用托管的 OAuth 认证来访问 SharePoint。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/sharepoint/v1.0/sites/root')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/sharepoint/{native-api-path}
```

该网关代理会将请求转发到 `graph.microsoft.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 SharePoint OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=sharepoint&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'sharepoint'}).encode()
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
    "status": "PENDING",
    "creation_time": "2026-03-05T08:00:00.000000Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "sharepoint",
    "method": "OAUTH2",
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

---

## API 参考

### 站点

#### 获取根站点

```bash
GET /sharepoint/v1.0/sites/root
```

**响应：**
```json
{
  "id": "contoso.sharepoint.com,guid1,guid2",
  "displayName": "Communication site",
  "name": "root",
  "webUrl": "https://contoso.sharepoint.com"
}
```

#### 通过 ID 获取站点

```bash
GET /sharepoint/v1.0/sites/{site_id}
```

站点 ID 的格式为：`{hostname},{site-guid},{web-guid}`

#### 通过主机名和路径获取站点

```bash
GET /sharepoint/v1.0/sites/{hostname}:/{site-path}
```

示例：`GET /sharepoint/v1.0/sites/contoso.sharepoint.com:/sites/marketing`

#### 搜索站点

```bash
GET /sharepoint/v1.0/sites?search={query}
```

#### 列出子站点

```bash
GET /sharepoint/v1.0/sites/{site_id}/sites
```

#### 获取站点列

```bash
GET /sharepoint/v1.0/sites/{site_id}/columns
```

#### 获取被关注的站点

```bash
GET /sharepoint/v1.0/me/followedSites
```

---

### 列表

#### 列出站点列表

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists
```

**响应：**
```json
{
  "value": [
    {
      "id": "b23974d6-a0aa-4e9b-9535-25393598b973",
      "name": "Events",
      "displayName": "Events",
      "webUrl": "https://contoso.sharepoint.com/Lists/Events"
    }
  ]
}
```

#### 获取列表

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}
```

#### 列出列表列

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/columns
```

#### 列出内容类型

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/contentTypes
```

#### 列出项目

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items
```

（包含字段值时使用 `$expand=fields`）：

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items?$expand=fields
```

**响应：**
```json
{
  "value": [
    {
      "id": "1",
      "createdDateTime": "2026-03-05T08:00:00Z",
      "fields": {
        "Title": "Team Meeting",
        "EventDate": "2026-03-10T14:00:00Z",
        "Location": "Conference Room A"
      }
    }
  ]
}
```

#### 获取列表项目

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}?$expand=fields
```

#### 创建列表项目

```bash
POST /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items
Content-Type: application/json

{
  "fields": {
    "Title": "New Event",
    "EventDate": "2026-04-01T10:00:00Z",
    "Location": "Main Hall"
  }
}
```

#### 更新列表项目

```bash
PATCH /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}/fields
Content-Type: application/json

{
  "Title": "Updated Event Title"
}
```

#### 删除列表项目

```bash
DELETE /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}
```

成功时返回 `204 No Content`。

---

### 驱动器（文档库）

#### 列出站点驱动器

```bash
GET /sharepoint/v1.0/sites/{site_id}/drives
```

#### 获取默认驱动器

```bash
GET /sharepoint/v1.0/sites/{site_id}/drive
```

#### 通过 ID 获取驱动器

```bash
GET /sharepoint/v1.0/drives/{drive_id}
```

**注意：** 包含 `!` 的驱动器 ID（例如 `b!abc123`）必须进行 URL 编码：`b%21abc123`

---

### 文件和文件夹

#### 列出根目录内容

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root/children
```

**响应：**
```json
{
  "value": [
    {
      "id": "01WBMXT7NQEEYJ3BAXL5...",
      "name": "Documents",
      "folder": { "childCount": 5 },
      "webUrl": "https://contoso.sharepoint.com/Shared%20Documents/Documents"
    },
    {
      "id": "01WBMXT7LISS5OMIG4CZ...",
      "name": "report.docx",
      "file": { "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document" },
      "size": 25600
    }
  ]
}
```

#### 通过 ID 获取项目

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
```

#### 通过路径获取项目

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root:/{path}
```

示例：`GET /sharepoint/v1.0/drives/{drive_id}/root:/Reports/Q1.xlsx`

#### 列出文件夹内容

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{folder_id}/children
```

**或者通过路径：**

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root:/{folder_path}:/children
```

#### 下载文件

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/content
```

**或者通过路径：**

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root:/{path}:/content
```

返回下载 URL（跟随重定向以获取文件内容）。

#### 上传文件（简单 - 最大 4MB）

```bash
PUT /sharepoint/v1.0/drives/{drive_id}/root:/{filename}:/content
Content-Type: application/octet-stream

<file content>
```

示例：
```bash
curl -X PUT "https://gateway.maton.ai/sharepoint/v1.0/drives/{drive_id}/root:/documents/report.txt:/content" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: text/plain" \
  -d "File content here"
```

#### 创建文件夹

```bash
POST /sharepoint/v1.0/drives/{drive_id}/root/children
Content-Type: application/json

{
  "name": "New Folder",
  "folder": {},
  "@microsoft.graph.conflictBehavior": "rename"
}
```

**或者在特定文件夹中创建：**

```bash
POST /sharepoint/v1.0/drives/{drive_id}/items/{parent_id}/children
```

#### 重命名/移动项目

```bash
PATCH /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
Content-Type: application/json

{
  "name": "new-filename.txt"
}
```

**移动到另一个文件夹：**

```bash
PATCH /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
Content-Type: application/json

{
  "parentReference": {
    "id": "{target_folder_id}"
  }
}
```

#### 复制项目

```bash
POST /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/copy
Content-Type: application/json

{
  "name": "copied-file.txt"
}
```

这是一个异步操作 - 返回 `202 Accepted` 并带有 `Location` 标头以跟踪进度。

#### 删除项目

```bash
DELETE /sharepoint/v1.0/drives/{drive_id}/items/{item_id}
```

成功时返回 `204 No Content`。删除的项目会被移至回收站。

#### 搜索文件

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root/search(q='{query}')
```

**响应：**
```json
{
  "value": [
    {
      "id": "01WBMXT7...",
      "name": "quarterly-report.xlsx",
      "webUrl": "https://contoso.sharepoint.com/..."
    }
  ]
}
```

#### 跟踪更改（Delta）

```bash
GET /sharepoint/v1.0/drives/{drive_id}/root/delta
```

返回更改的项目以及用于后续请求的 `@odata.deltaLink`。

---

### 共享和权限

#### 获取项目权限

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/permissions
```

#### 创建共享链接

```bash
POST /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/createLink
Content-Type: application/json

{
  "type": "view",
  "scope": "organization"
}
```

**参数：**
- `type`：`view`、`edit` 或 `embed`
- `scope`：`anonymous`、`organization` 或 `users`

**响应：**
```json
{
  "id": "f0cfb2bd-ef5f-4451-9932-8e9a3e219aaa",
  "roles": ["read"],
  "link": {
    "type": "view",
    "scope": "organization",
    "webUrl": "https://contoso.sharepoint.com/:t:/g/..."
  }
}
```

---

### 版本

#### 列出文件版本

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/versions
```

**响应：**
```json
{
  "value": [
    {
      "id": "2.0",
      "lastModifiedDateTime": "2026-03-05T08:07:12Z",
      "size": 25600,
      "lastModifiedBy": {
        "user": { "displayName": "John Doe" }
      }
    },
    {
      "id": "1.0",
      "lastModifiedDateTime": "2026-03-04T10:00:00Z",
      "size": 24000
    }
  ]
}
```

#### 获取特定版本

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/versions/{version_id}
```

#### 下载版本内容

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/versions/{version_id}/content
```

---

### 缩略图

#### 获取项目缩略图

```bash
GET /sharepoint/v1.0/drives/{drive_id}/items/{item_id}/thumbnails
```

**响应：**
```json
{
  "value": [
    {
      "id": "0",
      "small": { "height": 96, "width": 96, "url": "..." },
      "medium": { "height": 176, "width": 176, "url": "..." },
      "large": { "height": 800, "width": 800, "url": "..." }
    }
  ]
}
```

---

## OData 查询参数

SharePoint/Graph API 支持 OData 查询参数：

| 参数 | 描述 | 示例 |
|-----------|-------------|---------|
| `$select` | 选择特定属性 | `?$select=id,name,size` |
| `$expand` | 展开相关实体 | `?$expand=fields` |
| `$filter` | 过滤结果 | `?$filter=name eq 'Report'` |
| `$orderby` | 对结果进行排序 | `?$orderby=lastModifiedDateTime desc` |
| `$top` | 限制结果数量 | `?$top=10` |
| `$skip` | 跳过结果（分页） | `?$skip=10` |

带有多个参数的示例：

```bash
GET /sharepoint/v1.0/sites/{site_id}/lists/{list_id}/items?$expand=fields&$top=50&$orderby=createdDateTime desc
```

---

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/sharepoint/v1.0/sites/root', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  }
});
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/sharepoint/v1.0/sites/root',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
    }
)
print(response.json())
```

---

## 注意事项

- 站点 ID 的格式为：`{hostname},{site-guid},{web-guid}`。
- 包含 `!` 的驱动器 ID（例如 `b!abc123`）必须进行 URL 编码（`b%21abc123`）。
- 项目 ID 是不透明的字符串（例如 `01WBMXT7NQEEYJ3BAXL5...`）。
- 通过 PUT 上传文件的大小限制为 4MB；对于较大的文件，请使用上传会话。
- 复制操作是异步的 - 请检查 `Location` 标头以获取进度。
- 删除的项目会被移至 SharePoint 回收站。
- 某些管理操作需要提升的权限（如 `Sites.FullControl.All`）。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 200 | 成功 |
| 201 | 创建成功 |
| 202 | 操作已开始（异步操作） |
| 204 | 无内容（删除成功） |
| 400 | 请求无效 / JSON 格式错误 |
| 401 | 验证失败或认证信息缺失 |
| 403 | 访问被拒绝 / 权限不足 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，项目已存在） |
| 429 | 请求次数受限 |

## 资源

- [SharePoint 站点 API](https://learn.microsoft.com/en-us/graph/api/resources/sharepoint)
- [DriveItem API](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [List API](https://learn.microsoft.com/en-us/graph/api/resources/list)
- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)