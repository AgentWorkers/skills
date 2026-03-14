---
name: one-note
description: >
  **OneNote API集成：通过Microsoft Graph实现受管理的OAuth认证**  
  该功能允许用户访问OneNote中的笔记本、章节、章节组以及页面内容。当用户需要创建或管理OneNote笔记本、整理笔记或处理页面内容时，可利用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# OneNote

您可以通过 Microsoft Graph 和管理的 OAuth 认证来访问 OneNote API。该 API 允许您创建和管理笔记本、章节、章节组以及页面，以实现笔记的记录和整理。

## 快速入门

```bash
# List notebooks
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/one-note/v1.0/me/onenote/{resource}
```

该网关会将请求代理到 Microsoft Graph（`graph.microsoft.com`），并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 标头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建一个账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 OneNote OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=one-note&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'one-note'}).encode()
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
    "connection_id": "1447c2f4-3e5f-4ece-93df-67bc7e7a2857",
    "status": "ACTIVE",
    "creation_time": "2026-03-12T10:24:32.321168Z",
    "last_updated_time": "2026-03-12T10:24:49.890969Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "one-note",
    "metadata": {},
    "method": "OAUTH2"
  }
}
```

在浏览器中打开返回的 `url`，以完成与 Microsoft 的 OAuth 认证。

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

如果您有多个 OneNote 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '1447c2f4-3e5f-4ece-93df-67bc7e7a2857')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该参数，网关将使用默认的（最新的）活动连接。

## API 参考

### 笔记本

管理 OneNote 笔记本。

#### 列出笔记本

```bash
GET /one-note/v1.0/me/onenote/notebooks
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "value": [
    {
      "id": "1-30487038-8c2e-440a-860d-e82c6dc74f10",
      "displayName": "My Notebook",
      "createdDateTime": "2026-03-12T10:25:00Z",
      "lastModifiedDateTime": "2026-03-12T10:30:00Z",
      "isDefault": true,
      "isShared": false,
      "sectionsUrl": "https://graph.microsoft.com/v1.0/me/onenote/notebooks/.../sections",
      "sectionGroupsUrl": "https://graph.microsoft.com/v1.0/me/onenote/notebooks/.../sectionGroups"
    }
  ]
}
```

#### 列出包含章节的笔记本

使用 `$expand` 可以同时列出章节和章节组：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks?$expand=sections,sectionGroups')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取笔记本信息

```bash
GET /one-note/v1.0/me/onenote/notebooks/{notebook_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks/{notebook_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建笔记本

```bash
POST /one-note/v1.0/me/onenote/notebooks
Content-Type: application/json

{
  "displayName": "New Notebook"
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'displayName': 'My New Notebook'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 复制笔记本

```bash
POST /one-note/v1.0/me/onenote/notebooks/{notebook_id}/copyNotebook
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'renameAs': 'Copied Notebook'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks/{notebook_id}/copyNotebook', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

> **注意：** 复制操作是异步的。响应中会包含一个状态 URL，用于查看操作进度。

#### 获取最近的笔记本

```bash
GET /one-note/v1.0/me/onenote/notebooks/getRecentNotebooks(includePersonalNotebooks=true)
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks/getRecentNotebooks(includePersonalNotebooks=true)')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 章节

管理笔记本内的章节。

#### 列出所有章节

```bash
GET /one-note/v1.0/me/onenote/sections
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/sections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "value": [
    {
      "id": "1-c9d63289-4f64-4579-9043-155543978c78",
      "displayName": "My Section",
      "createdDateTime": "2026-03-12T10:26:00Z",
      "lastModifiedDateTime": "2026-03-12T10:28:00Z",
      "isDefault": false,
      "pagesUrl": "https://graph.microsoft.com/v1.0/me/onenote/sections/.../pages"
    }
  ]
}
```

#### 列出笔记本中的章节

```bash
GET /one-note/v1.0/me/onenote/notebooks/{notebook_id}/sections
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks/{notebook_id}/sections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取章节信息

```bash
GET /one-note/v1.0/me/onenote/sections/{section_id}
```

#### 创建章节

```bash
POST /one-note/v1.0/me/onenote/notebooks/{notebook_id}/sections
Content-Type: application/json

{
  "displayName": "New Section"
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'displayName': 'Meeting Notes'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks/{notebook_id}/sections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 章节组

将章节组织成组。

#### 列出所有章节组

```bash
GET /one-note/v1.0/me/onenote/sectionGroups
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/sectionGroups')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 列出笔记本中的章节组

```bash
GET /one-note/v1.0/me/onenote/notebooks/{notebook_id}/sectionGroups
```

#### 获取章节组信息

```bash
GET /one-note/v1.0/me/onenote/sectionGroups/{section_group_id}
```

#### 创建章节组

```bash
POST /one-note/v1.0/me/onenote/notebooks/{notebook_id}/sectionGroups
Content-Type: application/json

{
  "displayName": "New Section Group"
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'displayName': 'Project Notes'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks/{notebook_id}/sectionGroups', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 页面

创建和管理包含丰富内容的页面。

#### 列出所有页面

```bash
GET /one-note/v1.0/me/onenote/pages
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/pages')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "value": [
    {
      "id": "1-42a904024c734393b561d0a85428965d!251-c9d63289-4f64-4579-9043-155543978c78",
      "title": "My Page",
      "createdDateTime": "2026-03-12T10:29:42Z",
      "lastModifiedDateTime": "2026-03-12T10:30:00Z",
      "contentUrl": "https://graph.microsoft.com/v1.0/me/onenote/pages/.../content"
    }
  ]
}
```

#### 列出章节中的页面

```bash
GET /one-note/v1.0/me/onenote/sections/{section_id}/pages
```

#### 获取页面信息

**返回页面的 HTML 内容：**

```bash
GET /one-note/v1.0/me/onenote/pages/{page_id}/content
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/pages/{page_id}/content')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
resp = urllib.request.urlopen(req)
print(resp.read().decode())
EOF
```

#### 创建页面

页面使用 HTML 内容创建：

```bash
POST /one-note/v1.0/me/onenote/sections/{section_id}/pages
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <p>Page content here</p>
  </body>
</html>
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
html = """<!DOCTYPE html>
<html>
  <head>
    <title>Meeting Notes - March 12</title>
  </head>
  <body>
    <h1>Meeting Notes</h1>
    <p>Attendees: Alice, Bob, Charlie</p>
    <ul>
      <li>Discussed Q1 goals</li>
      <li>Reviewed project timeline</li>
    </ul>
  </body>
</html>""".encode()
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/sections/{section_id}/pages', data=html, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'text/html')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新页面内容

可以使用 `PATCH` 方法来添加、插入或替换页面内容：

**操作：**
- `append` - 在目标内容的末尾添加内容
- `prepend` - 在目标内容的开头添加内容
- `replace` - 替换目标内容
- `insert` - 在目标内容之后插入新内容

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps([
    {
        "target": "body",
        "action": "append",
        "content": "<p>Updated at 2026-03-12</p>"
    }
]).encode()
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/pages/{page_id}/content', data=data, method='PATCH')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
resp = urllib.request.urlopen(req)
print(f"Updated: {resp.status}")
EOF
```

## OData 查询参数

OneNote API 支持 OData 查询参数：

| 参数 | 描述 | 示例 |
|-----------|-------------|---------|
| `$select` | 选择特定属性 | `$select=id,displayName` |
| `$expand` | 包含相关资源 | `$expand=sections,sectionGroups` |
| `$filter` | 筛选结果 | `$filter=isDefault eq true` |
| `$orderby` | 对结果进行排序 | `$orderby=displayName` |
| `$top` | 限制结果数量 | `$top=10` |
| `$skip` | 跳过部分结果 | `$skip=20` |

**使用 `$select` 的示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks?$select=id,displayName')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 页面 HTML 格式

OneNote 页面使用特定的 HTML 格式：

### 基本结构

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Page Title</title>
    <meta name="created" content="2026-03-12T10:00:00Z" />
  </head>
  <body>
    <p>Content here</p>
  </body>
</html>
```

### 支持的元素

- 标题：`<h1>` 到 `<h6>`
- 段落：`<p>`
- 列表：`<ul>`, `<ol>`, `<li>`
- 表格：`<table>`, `<tr>`, `<td>`
- 图片：`<img src="..." />`
- 链接：`<a href="...">`
- 格式化：`<b>`, `<i>`, `<u>`, `<strike>`

### 添加图片

```html
<img src="https://example.com/image.jpg" alt="Description" />
```

或者嵌入 Base64 编码的图片：

```html
<img src="data:image/png;base64,..." alt="Embedded image" />
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.value);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
notebooks = response.json()
print(notebooks['value'])
```

### 使用 Python 创建页面

```python
import os
import requests

html_content = """<!DOCTYPE html>
<html>
  <head><title>New Page</title></head>
  <body><p>Hello from Python!</p></body>
</html>"""

response = requests.post(
    f'https://gateway.maton.ai/one-note/v1.0/me/onenote/sections/{section_id}/pages',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'text/html'
    },
    data=html_content
)
page = response.json()
print(f"Created page: {page['title']}")
```

## 注意事项

- OneNote 使用的是 Microsoft Graph API v1.0。
- 页面使用 HTML 内容创建（Content-Type: text/html）。
- 页面更新通过包含 JSON 操作数组的 `PATCH` 请求实现。
- 复制操作是异步的——请检查返回的状态 URL 以获取操作进度。
- 使用 `$expand=sections,sectionGroups` 可以一次性获取笔记本的所有内容。
- 笔记本和章节的名称在其容器内必须是唯一的。
- **重要提示：** 当将 curl 的输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或缺少 OneNote 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 禁止访问——权限不足 |
| 404 | 资源未找到 |
| 409 | 冲突——名称重复 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Microsoft Graph 的错误 |

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

1. 确保您的 URL 路径以 `one-note` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/one-note/v1.0/me/onenote/notebooks`
- 错误的路径：`https://gateway.maton.ai/v1.0/me/onenote/notebooks`

## 资源

- [OneNote API 概述](https://learn.microsoft.com/en-us/graph/integrate-with-onenote)
- [OneNote REST API 参考](https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview)
- [页面 HTML 参考](https://learn.microsoft.com/en-us/graph/onenote-input-output-html)
- [Microsoft Graph Explorer](https://developer.microsoft.com/graph/graph-explorer)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)