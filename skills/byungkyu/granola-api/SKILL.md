---
name: granola
description: >
  Granola MCP服务器与受管理的OAuth集成：用户可以查询会议记录、查看会议列表以及访问会议记录的文字版本。  
  当用户需要搜索会议内容、获取会议摘要、查找待办事项或从Granola中检索会议记录时，可以使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  该功能需要网络连接以及有效的Maton API密钥。
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
# Granola

您可以使用受管理的OAuth认证来访问Granola的MCP服务器。该服务器支持查询会议记录、列出会议信息、搜索会议内容以及检索会议记录的文字稿。

## 快速入门

```bash
# Query your meeting notes
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'What action items came from my last meeting?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/query_granola_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/granola/{tool_name}
```

请将 `{tool_name}` 替换为实际的MCP工具名称。该网关会将请求代理到 `mcp.granola.ai`，并自动处理OAuth认证过程。

## 认证

所有请求都必须在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

___CODEBLOCK_3___

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Granola OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=granola&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'granola'}).encode()
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
    "connection_id": "8a413c45-6427-45d9-b69d-8118ce62ffce",
    "status": "ACTIVE",
    "creation_time": "2026-02-24T11:34:46.204677Z",
    "last_updated_time": "2026-02-24T11:37:01.221812Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "granola",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证流程。

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

如果您有多个Granola连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'What were my action items?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/query_granola_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '8a413c45-6427-45d9-b69d-8118ce62ffce')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最新的）活动连接。

## MCP工具参考

Granola提供了四种MCP工具。所有工具都通过带有JSON参数的POST请求进行调用。

### query_granola_meetings

使用自然语言查询与您的会议记录进行交互。这是与会议数据进行对话式交互的主要工具。

**端点：**
```
POST /granola/query_granola_meetings
```

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `query` | 字符串 | 是 | 用于查询会议的自然语言语句 |

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'What action items came from my meetings this week?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/query_granola_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "You had 2 recent meetings:\n**Feb 4, 2026 at 7:30 PM** - \"Team sync\" [[0]](https://notes.granola.ai/d/abc123)\n- Action item: Review Q1 roadmap\n- Action item: Schedule follow-up with engineering\n**Jan 27, 2026 at 1:04 AM** - \"Finance integration\" [[1]](https://notes.granola.ai/d/def456)\n- Discussed workflow automation platforms\n- Action item: Evaluate n8n vs Zapier"
    }
  ],
  "isError": false
}
```

**使用场景：**
- “哪些行动项被分配给了我？”
- “总结我上周的会议内容”
- “我们讨论了产品发布的哪些内容？”
- “查找我会议中所有关于预算的提及”

---

### list_meetings

列出包含ID、标题、日期和参与者的会议信息。您可以使用这些信息来获取其他工具所需的会议ID。

**端点：**
```
POST /granola/list_meetings
```

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| （无） | - | - | 默认返回最近的会议列表 |

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/list_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "<meetings_data from=\"Jan 27, 2026\" to=\"Feb 4, 2026\" count=\"2\">\n<meeting id=\"0dba4400-50f1-4262-9ac7-89cd27b79371\" title=\"Team sync\" date=\"Feb 4, 2026 7:30 PM\">\n    <known_participants>\n    John Doe (note creator) from Acme <john@acme.com>\n    Jane Smith from Acme <jane@acme.com>\n    </known_participants>\n  </meeting>\n\n<meeting id=\"4ebc086f-ba8d-49e8-8cd1-ed81ac8f2e3b\" title=\"Finance integration\" date=\"Jan 27, 2026 1:04 AM\">\n    <known_participants>\n    John Doe (note creator) from Acme <john@acme.com>\n    </known_participants>\n  </meeting>\n</meetings_data>"
    }
  ],
  "isError": false
}
```

**响应数据格式（XML）：**
- `meetings_data`：包含 `from`、`to` 日期范围和 `count` 的容器。
- `meeting`：包含 `id`、`title` 和 `date` 属性的单独会议信息。
- `known_participants`：包含参与者姓名、角色、公司和电子邮件的列表。

---

### get_meetings

根据会议ID检索特定会议的详细内容，包括会议摘要、增强型笔记和私人笔记。

**端点：**
```
POST /granola/get_meetings
```

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `meeting_ids` | 字符串数组 | 是 | 需要检索的会议ID列表 |

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'meeting_ids': ['0dba4400-50f1-4262-9ac7-89cd27b79371']}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/get_meetings', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应内容：**
- 会议元数据（ID、标题、日期、参与者）
- `summary`：由AI生成的会议摘要，包含关键决策和行动项。
- 增强型笔记和私人笔记（如有的话）。

---

### get_meeting_transcript

检索特定会议的原始文字稿。**仅限付费Granola用户使用。**

**端点：**
```
POST /granola/get_meeting_transcript
```

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| `meeting_id` | 字符串 | 是 | 需要获取文字稿的会议ID |

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'meeting_id': '0dba4400-50f1-4262-9ac7-89cd27b79371'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/granola/get_meeting_transcript', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**付费版本响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "<transcript meeting_id=\"0dba4400-50f1-4262-9ac7-89cd27b79371\">\n[00:00:15] John: Let's get started with the Q1 planning...\n[00:01:23] Jane: I've prepared the budget breakdown...\n[00:03:45] John: That looks good. What about the timeline?\n</transcript>"
    }
  ],
  "isError": false
}
```

**免费版本响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Transcripts are only available to paid Granola tiers"
    }
  ],
  "isError": true
}
```

## 代码示例

### JavaScript

```javascript
// Query meeting notes
const response = await fetch('https://gateway.maton.ai/granola/query_granola_meetings', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'What were the action items from my last meeting?'
  })
});
const data = await response.json();
console.log(data.content[0].text);
```

### Python

```python
import os
import requests

# List all meetings
response = requests.post(
    'https://gateway.maton.ai/granola/list_meetings',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={}
)
data = response.json()

# Get specific meeting content
meeting_ids = ['0dba4400-50f1-4262-9ac7-89cd27b79371']
response = requests.post(
    'https://gateway.maton.ai/granola/get_meetings',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'meeting_ids': meeting_ids}
)
```

## 注意事项

- **MCP协议**：Granola使用Model Context Protocol (MCP)。所有工具调用都是带有JSON参数的POST请求。
- **响应格式**：所有响应都遵循MCP格式，其中 `content` 数组包含 `type: "text"` 的对象以及一个 `isError` 布尔值。
- **访问控制**：用户只能查询自己的会议记录。无法访问他人的共享笔记。
- **免费版本限制**：基础（免费）计划用户仅能查看过去30天的笔记。
- **文字稿访问**：`get_meeting_transcript` 工具仅限于付费Granola用户使用。
- **速率限制**：每分钟大约100个请求（具体取决于计划等级）。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到Granola连接 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 超过速率限制 |
| MCP -32602 | 工具参数无效（请检查必填字段） |

**MCP错误响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "MCP error -32602: Input validation error: Invalid arguments for tool get_meetings: [\n  {\n    \"code\": \"invalid_type\",\n    \"expected\": \"array\",\n    \"received\": \"undefined\",\n    \"path\": [\"meeting_ids\"],\n    \"message\": \"Required\"\n  }\n]"
    }
  ],
  "isError": true
}
```

## 资源

- [Granola MCP文档](https://docs.granola.ai/help-center/sharing/integrations/mcp)
- [Granola帮助中心](https://docs.granola.ai)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)