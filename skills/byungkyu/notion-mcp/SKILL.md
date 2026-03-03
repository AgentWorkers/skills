---
name: notion-mcp
description: >
  **Notion MCP集成与受管理的身份验证**  
  该技能支持通过MCP（Management Console Platform）与Notion进行交互，包括查询数据库、创建和更新页面以及管理页面中的内容块。当用户希望使用MCP来操作Notion工作空间时，可以运用此技能。  
  - 对于REST API相关的操作，请使用`notion`技能（https://clawhub.ai/byungkyu/notion-api-skill）；  
  - 对于其他第三方应用程序的集成，建议使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）。
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
# Notion MCP

通过MCP（Model Context Protocol）访问Notion，并支持身份验证。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'meeting notes', 'query_type': 'internal'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/notion/notion-search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/notion/{tool-name}
```

请将 `{tool-name}` 替换为相应的MCP工具名称（例如 `notion-search`）。该网关会将请求代理到 `mcp.notion.com` 并自动插入您的凭据。

## 请求头

MCP请求使用 `Mcp-Session-Id` 头部来进行会话管理。如果未指定，网关会初始化一个新的会话，并在 `Mcp-Session-Id` 响应头部返回会话ID。您可以在后续请求中包含此会话ID以重用相同的会话。

## 身份验证

所有请求都需要Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Notion MCP连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=notion&method=MCP&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'notion', 'method': 'MCP'}).encode()
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
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "notion",
    "method": "MCP",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth授权。

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

如果您有多个Notion连接（例如OAuth2、MCP），必须使用 `Maton-Connection` 头部指定要使用的MCP连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'meeting notes', 'query_type': 'internal'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/notion/notion-search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**注意：** 如果省略此字段，网关将使用默认的（最旧的）活动连接。如果该连接不是MCP连接，可能会导致失败。

## MCP参考

所有MCP工具都使用 `POST` 方法：

| 工具 | 描述 | 方式 |
|------|-------------|--------|
| `notion-search` | 搜索工作区和已连接的服务 | [schema](schemas/notion-search.json) |
| `notion-fetch` | 从页面/数据库中检索内容 | [schema](schemas/notion-fetch.json) |
| `notion-create-pages` | 创建带有属性和内容的页面 | [schema](schemas/notion-create-pages.json) |
| `notion-update-page` | 更新页面属性和内容 | [schema](schemas/notion-update-page.json) |
| `notion-move-pages` | 将页面移动到新的父页面 | [schema](schemas/notion-move-pages.json) |
| `notion-duplicate-page` | 复制工作区内的页面 | [schema](schemas/notion-duplicate-page.json) |
| `notion-create-database` | 使用模式创建数据库 | [schema](schemas/notion-create-database.json) |
| `notion-update-data-source` | 修改数据源属性 | [schema](schemas/notion-update-data-source.json) |
| `notion-create-comment` | 为页面/块添加评论 | [schema](schemas/notion-create-comment.json) |
| `notion-get-comments` | 检索页面评论 | [schema](schemas/notion-get-comments.json) |
| `notion-get-teams` | 列出工作区团队 | [schema](schemas/notion-get-teams.json) |
| `notion-get-users` | 列出工作区用户 | [schema](schemas/notion-get-users.json) |

### 搜索

搜索页面和数据库：
```bash
POST /notion/notion-search
Content-Type: application/json

{
  "query": "meeting notes",
  "query_type": "internal"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"results\":[{\"id\":\"30702dc5-9a3b-8106-b51b-ed6d1bfeeed4\",\"title\":\"Meeting Summary Report\",\"url\":\"https://www.notion.so/30702dc59a3b8106b51bed6d1bfeeed4\",\"type\":\"page\",\"highlight\":\"Meeting materials\",\"timestamp\":\"2026-02-15T00:07:00.000Z\"}],\"type\":\"workspace_search\"}"
    }
  ],
  "isError": false
}
```

搜索用户：
```bash
POST /notion/notion-search
Content-Type: application/json

{
  "query": "john@example.com",
  "query_type": "user"
}
```

**带日期过滤：**
```bash
POST /notion/notion-search
Content-Type: application/json

{
  "query": "quarterly report",
  "query_type": "internal",
  "filters": {
    "created_date_range": {
      "start_date": "2024-01-01",
      "end_date": "2025-01-01"
    }
  }
}
```

### 获取内容

通过URL获取页面内容：
```bash
POST /notion/notion-fetch
Content-Type: application/json

{
  "id": "https://notion.so/workspace/Page-a1b2c3d4e5f67890"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"metadata\":{\"type\":\"page\"},\"title\":\"Project Overview\",\"url\":\"https://www.notion.so/30702dc59a3b8106b51bed6d1bfeeed4\",\"text\":\"Here is the result of \\\"view\\\" for the Page with URL https://www.notion.so/30702dc59a3b8106b51bed6d1bfeeed4 as of 2026-02-14T22:56:21.276Z:\\n<page url=\\\"https://www.notion.so/30702dc59a3b8106b51bed6d1bfeeed4\\\">\\n<properties>\\n{\\\"title\\\":\\\"Project Overview\\\"}\\n</properties>\\n<content>\\n# Project Overview\\n\\nThis document outlines the project goals and milestones.\\n</content>\\n</page>\"}"
    }
  ],
  "isError": false
}
```

通过UUID获取内容：
```bash
POST /notion/notion-fetch
Content-Type: application/json

{
  "id": "12345678-90ab-cdef-1234-567890abcdef"
}
```

获取数据源（集合）：
```bash
POST /notion/notion-fetch
Content-Type: application/json

{
  "id": "collection://12345678-90ab-cdef-1234-567890abcdef"
}
```

**包含讨论：**
```bash
POST /notion/notion-fetch
Content-Type: application/json

{
  "id": "page-uuid",
  "include_discussions": true
}
```

### 创建页面

创建一个简单的页面：
```bash
POST /notion/notion-create-pages
Content-Type: application/json

{
  "pages": [
    {
      "properties": {"title": "My New Page"},
      "content": "# Introduction\n\nThis is my new page content."
    }
  ]
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"pages\":[{\"id\":\"31502dc5-9a3b-816d-a2ac-e9b7ec9aece7\",\"url\":\"https://www.notion.so/31502dc59a3b816da2ace9b7ec9aece7\",\"properties\":{\"title\":\"My New Page\"}}]}"
    }
  ],
  "isError": false
}
```

在父页面下创建页面：
```bash
POST /notion/notion-create-pages
Content-Type: application/json

{
  "parent": {"page_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
  "pages": [
    {
      "properties": {"title": "Child Page"},
      "content": "# Child Page Content"
    }
  ]
}
```

在数据源（数据库）中创建页面：
```bash
POST /notion/notion-create-pages
Content-Type: application/json

{
  "parent": {"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd"},
  "pages": [
    {
      "properties": {
        "Task Name": "New Task",
        "Status": "In Progress",
        "Priority": 5,
        "Is Complete": "__NO__",
        "date:Due Date:start": "2024-12-25"
      }
    }
  ]
}
```

### 更新页面

更新属性：
```bash
POST /notion/notion-update-page
Content-Type: application/json

{
  "page_id": "f336d0bc-b841-465b-8045-024475c079dd",
  "command": "update_properties",
  "properties": {
    "title": "Updated Page Title",
    "Status": "Done"
  }
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"page_id\":\"f336d0bc-b841-465b-8045-024475c079dd\"}"
    }
  ],
  "isError": false
}
```

替换全部内容：
```bash
POST /notion/notion-update-page
Content-Type: application/json

{
  "page_id": "f336d0bc-b841-465b-8045-024475c079dd",
  "command": "replace_content",
  "new_str": "# New Heading\n\nCompletely replaced content."
}
```

替换内容范围：
```bash
POST /notion/notion-update-page
Content-Type: application/json

{
  "page_id": "f336d0bc-b841-465b-8045-024475c079dd",
  "command": "replace_content_range",
  "selection_with_ellipsis": "# Old Section...end of section",
  "new_str": "# New Section\n\nUpdated section content."
}
```

在指定位置后插入内容：
```bash
POST /notion/notion-update-page
Content-Type: application/json

{
  "page_id": "f336d0bc-b841-465b-8045-024475c079dd",
  "command": "insert_content_after",
  "selection_with_ellipsis": "## Previous section...",
  "new_str": "\n## New Section\n\nInserted content here."
}
```

### 移动页面

将页面移动到：
```bash
POST /notion/notion-move-pages
Content-Type: application/json

{
  "page_or_database_ids": ["31502dc5-9a3b-816d-a2ac-e9b7ec9aece7"],
  "new_parent": {
    "page_id": "31502dc5-9a3b-81e4-b090-c6f705459e38"
  }
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"result\":\"Successfully moved 1 item: 31502dc5-9a3b-816d-a2ac-e9b7ec9aece7\"}"
    }
  ],
  "isError": false
}
```

将页面移动到工作区：
```bash
POST /notion/notion-move-pages
Content-Type: application/json

{
  "page_or_database_ids": ["page-id-1", "page-id-2"],
  "new_parent": {
    "type": "workspace"
  }
}
```

将页面移动到数据库：
```bash
POST /notion/notion-move-pages
Content-Type: application/json

{
  "page_or_database_ids": ["page-id"],
  "new_parent": {
    "data_source_id": "f336d0bc-b841-465b-8045-024475c079dd"
  }
}
```

### 复制页面

```bash
POST /notion/notion-duplicate-page
Content-Type: application/json

{
  "page_id": "31502dc5-9a3b-816d-a2ac-e9b7ec9aece7"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"page_id\":\"31502dc5-9a3b-812d-a865-ccac00a21f72\",\"page_url\":\"https://www.notion.so/31502dc59a3b812da865ccac00a21f72\"}"
    }
  ],
  "isError": false
}
```

### 创建数据库

使用SQL DDL模式创建数据库：
```bash
POST /notion/notion-create-database
Content-Type: application/json

{
  "title": "Task Database",
  "schema": "CREATE TABLE (\"Task Name\" TITLE, \"Status\" SELECT('To Do':red, 'In Progress':yellow, 'Done':green), \"Priority\" NUMBER)"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"result\":\"Created database: <database url=\\\"{{https://www.notion.so/2a3cdbb18c1c475b909a84e5615c7b74}}\\\" inline=\\\"false\\\">\\nThe title of this Database is: Task Database\\n<data-sources>\\n<data-source url=\\\"{{collection://c0f0ce51-c470-4e96-8c3f-cafca780f1a0}}\\\">\\n...\"}"
    }
  ],
  "isError": false
}
```

### 更新数据源

```bash
POST /notion/notion-update-data-source
Content-Type: application/json

{
  "data_source_id": "c0f0ce51-c470-4e96-8c3f-cafca780f1a0",
  "name": "Updated Database Name"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"result\":\"Updated data source: <database url=\\\"{{https://www.notion.so/2a3cdbb18c1c475b909a84e5615c7b74}}\\\">\\n...\"}"
    }
  ],
  "isError": false
}
```

### 获取评论

```bash
POST /notion/notion-get-comments
Content-Type: application/json

{
  "page_id": "30702dc5-9a3b-8106-b51b-ed6d1bfeeed4"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"results\":[{\"object\":\"comment\",\"id\":\"31502dc5-9a3b-8164-aa9c-001dfb9cb942\",\"discussion_id\":\"discussion://pageId/blockId/discussionId\",\"created_time\":\"2026-02-28T20:00:00.000Z\",\"last_edited_time\":\"2026-02-28T20:00:00.000Z\",\"created_by\":{\"object\":\"user\",\"id\":\"237d872b-594c-81d6-b88e-000200ac4d04\"},\"rich_text\":[{\"type\":\"text\",\"text\":{\"content\":\"This looks great! Ready for review.\"},\"annotations\":{\"bold\":false,\"italic\":false,\"strikethrough\":false,\"underline\":false,\"code\":false,\"color\":\"default\"}}]}],\"has_more\":false}"
    }
  ],
  "isError": false
}
```

### 创建评论

```bash
POST /notion/notion-create-comment
Content-Type: application/json

{
  "page_id": "f336d0bc-b841-465b-8045-024475c079dd",
  "rich_text": [
    {
      "type": "text",
      "text": {
        "content": "This looks great! Ready for review."
      }
    }
  ]
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"result\":{\"status\":\"success\",\"id\":\"31502dc5-9a3b-8164-aa9c-001dfb9cb942\"}}"
    }
  ],
  "isError": false
}
```

### 列出团队

```bash
POST /notion/notion-get-teams
Content-Type: application/json

{}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"joinedTeams\":[],\"otherTeams\":[],\"hasMore\":false}"
    }
  ],
  "isError": false
}
```

### 列出用户

```bash
POST /notion/notion-get-users
Content-Type: application/json

{}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"results\":[{\"type\":\"person\",\"id\":\"237d872b-594c-81d6-b88e-000200ac4d04\",\"name\":\"John Doe\",\"email\":\"john@example.com\"},{\"type\":\"bot\",\"id\":\"b638ec59-55e9-4889-8dc1-a523ff2c8677\",\"name\":\"Notion MCP\"}],\"has_more\":false}"
    }
  ],
  "isError": false
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/notion/notion-search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({
    query: 'meeting notes',
    query_type: 'internal'
  })
});
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/notion/notion-search',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': 'meeting notes',
        'query_type': 'internal'
    }
)
print(response.json())
```

## 属性类型参考

在数据库中创建或更新页面时，请使用以下属性类型：

| 属性类型 | 格式 |
|---------------|--------|
| Title | `"Title Property": "页面标题"` |
| Text | `"Text Property": "一些文本"` |
| Number | `"Number Property": 42` |
|Checkbox | `"Checkbox Property": "__YES__"` 或 `"__NO__"` |
| Select | `"Select Property": "选项名称"` |
| Multi-select | `"Multi Property": "选项1, 选项2"` |
| Date (start) | `"date:Date Property:start": "2024-12-25"` |
| Date (end) | `"date:Date Property:end": "2024-12-31"` |
| Date (is datetime) | `"date:Date Property:is_datetime": 1` |
| Place (name) | `"place:Location:name": "办公室总部"` |
| Place (coordinates) | `"place:Location:latitude": 37.7749"` |

**特殊命名规则：** 名称为 "id" 或 "url" 的属性必须以 `userDefined:` 为前缀（例如，`"userDefined:URL"`）。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少MCP连接或工具名称无效 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 每个账户的请求速率限制为10次/秒 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的URL路径以 `notion` 开头。例如：

- 正确：`https://gateway.maton.ai/notion/v1/search`
- 错误：`https://gateway.maton.ai/v1/search`

## 注意事项

- 所有ID都是UUID（可能包含或不包含连字符）。
- MCP工具的响应内容采用 `{"content": [{"type": "text", "text": "..."}, "isError": false}` 的格式。
- `text` 字段包含需要解析的JSON字符串数据。
- 在创建或更新页面之前，请使用 `notion-fetch` 获取页面/数据库的结构。
- 对于数据库，首先获取数据源ID（`collection://...` URL）。

## 资源

- [Notion MCP概述](https://developers.notion.com/guides/mcp)
- [MCP支持的工具](https://developers.notion.com/guides/mcp/mcp-supported-tools)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)