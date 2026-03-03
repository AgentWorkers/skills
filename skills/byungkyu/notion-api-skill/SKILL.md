---
name: notion
description: Notion API与托管的OAuth集成：支持查询数据库、创建和更新页面以及管理页面内容。当用户需要与Notion的工作空间、数据库或页面进行交互时，可以使用此功能。对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# Notion

您可以使用受管理的 OAuth 认证来访问 Notion API。该 API 允许您查询数据库、创建页面、管理块内容以及搜索您的工作区。

## 快速入门

```bash
# Search for pages
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'meeting notes'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/notion/v1/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Notion-Version', '2025-09-03')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基础 URL

```
https://gateway.maton.ai/notion/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Notion API 端点路径。该网关会将请求代理到 `api.notion.com`，并自动插入您的 OAuth 令牌。

## 必需的请求头

所有 Notion API 请求都需要包含以下版本头：

```
Notion-Version: 2025-09-03
```

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

您可以在 `https://ctrl.maton.ai` 管理您的 Notion OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=notion&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'notion'}).encode()
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
    "app": "notion",
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

### 指定连接

如果您有多个 Notion 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'meeting notes'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/notion/v1/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Notion-Version', '2025-09-03')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## 关键概念：数据库与数据源

在 API 版本 2025-09-03 中，数据库和数据源是分开的：

| 概念 | 用途 |
|---------|---------|
| **数据库** | 创建数据库、获取数据源 ID |
| **数据源** | 查询数据、更新数据源结构、更新数据源属性 |

使用 `GET /databases/{id}` 来获取 `data_sources` 数组，然后使用 `/data_sources/` 端点来操作数据源：

```json
{
  "object": "database",
  "id": "abc123",
  "data_sources": [
    {"id": "def456", "name": "My Database"}
  ]
}
```

## API 参考

### 搜索

搜索页面：

```bash
POST /notion/v1/search
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "query": "meeting notes",
  "filter": {"property": "object", "value": "page"}
}
```

搜索数据源：

```bash
POST /notion/v1/search
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "filter": {"property": "object", "value": "data_source"}
}
```

### 数据源

#### 获取数据源信息

```bash
GET /notion/v1/data_sources/{dataSourceId}
Notion-Version: 2025-09-03
```

#### 查询数据源

```bash
POST /notion/v1/data_sources/{dataSourceId}/query
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "filter": {
    "property": "Status",
    "select": {"equals": "Active"}
  },
  "sorts": [
    {"property": "Created", "direction": "descending"}
  ],
  "page_size": 100
}
```

#### 更新数据源

```bash
PATCH /notion/v1/data_sources/{dataSourceId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "title": [{"type": "text", "text": {"content": "Updated Title"}}],
  "properties": {
    "NewColumn": {"rich_text": {}}
  }
}
```

### 数据库

#### 获取数据库信息

```bash
GET /notion/v1/databases/{databaseId}
Notion-Version: 2025-09-03
```

#### 创建数据库

```bash
POST /notion/v1/databases
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "parent": {"type": "page_id", "page_id": "PARENT_PAGE_ID"},
  "title": [{"type": "text", "text": {"content": "New Database"}}],
  "properties": {
    "Name": {"title": {}},
    "Status": {"select": {"options": [{"name": "Active"}, {"name": "Done"}]}}
  }
}
```

### 页面

#### 获取页面信息

```bash
GET /notion/v1/pages/{pageId}
Notion-Version: 2025-09-03
```

#### 创建页面

```bash
POST /notion/v1/pages
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "parent": {"page_id": "PARENT_PAGE_ID"},
  "properties": {
    "title": {"title": [{"text": {"content": "New Page"}}]}
  }
}
```

#### 在数据源中创建页面

```bash
POST /notion/v1/pages
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "parent": {"data_source_id": "DATA_SOURCE_ID"},
  "properties": {
    "Name": {"title": [{"text": {"content": "New Page"}}]},
    "Status": {"select": {"name": "Active"}}
  }
}
```

#### 更新页面属性

```bash
PATCH /notion/v1/pages/{pageId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "properties": {
    "Status": {"select": {"name": "Done"}}
  }
}
```

#### 更改页面图标

```bash
PATCH /notion/v1/pages/{pageId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "icon": {"type": "emoji", "emoji": "🚀"}
}
```

#### 将页面归档

```bash
PATCH /notion/v1/pages/{pageId}
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "archived": true
}
```

### 块

#### 获取块的子元素

```bash
GET /notion/v1/blocks/{blockId}/children
Notion-Version: 2025-09-03
```

#### 向块中添加子元素

```bash
PATCH /notion/v1/blocks/{blockId}/children
Content-Type: application/json
Notion-Version: 2025-09-03

{
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "New paragraph"}}]
      }
    }
  ]
}
```

#### 删除块

```bash
DELETE /notion/v1/blocks/{blockId}
Notion-Version: 2025-09-03
```

### 用户

#### 列出用户

```bash
GET /notion/v1/users
Notion-Version: 2025-09-03
```

#### 获取当前用户信息

```bash
GET /notion/v1/users/me
Notion-Version: 2025-09-03
```

## 过滤操作符

- `equals`（等于）
- `does_not_equal`（不等于）
- `contains`（包含）
- `does_not_contain`（不包含）
- `starts_with`（以……开头）
- `ends_with`（以……结尾）
- `is_empty`（为空）
- `is_not_empty`（不为空）
- `greater_than`（大于）
- `less_than`（小于）

## 块类型

- `paragraph`（段落）
- `heading_1`（标题 1）
- `heading_2`（标题 2）
- `heading_3`（标题 3）
- `bulleted_list_item`（项目符号列表项）
- `numbered_list_item`（编号列表项）
- `to_do`（待办事项）
- `code`（代码块）
- `quote`（引用）
- `divider`（分隔符）

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/notion/v1/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Notion-Version': '2025-09-03'
  },
  body: JSON.stringify({ query: 'meeting' })
});
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/notion/v1/search',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Notion-Version': '2025-09-03'
    },
    json={'query': 'meeting'}
)
```

## 注意事项：

- 所有 ID 都是 UUID（可能包含或不包含连字符）。
- 使用 `GET /databases/{id}` 来获取包含数据源 ID 的 `data_sources` 数组。
- 创建数据库需要使用 `POST /databases` 端点。
- 删除块时，返回的响应中会包含 `archived: true` 字段，表示块已被归档。
- **重要提示：** 当使用 `curl` 命令时，如果 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 选项以禁用全局解析功能。
- **重要提示：** 当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Notion 连接 |
| 401 | API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Notion API 的传递错误 |

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

1. 确保您的 URL 路径以 `notion` 开头。例如：
   - 正确的路径：`https://gateway.maton.ai/notion/v1/search`
   - 错误的路径：`https://gateway.maton.ai/v1/search`

## 资源

- [Notion API 介绍](https://developers.notion.com/reference/intro)
- [搜索](https://developers.notion.com/reference/post-search.md)
- [查询数据库](https://developers.notion.com/reference/post-database-query.md)
- [获取页面信息](https://developers.notion.com/reference/retrieve-a-page.md)
- [创建页面](https://developers.notion.com/reference/post-page.md)
- [更新页面信息](https://developers.notion.com/reference/patch-page.md)
- [向块中添加子元素](https://developers.notion.com/reference/patch-block-children.md)
- [过滤参考](https://developers.notion.com/reference/post-database-query-filter.md)
- [大语言模型参考](https://developers.notion.com/llms.txt)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)