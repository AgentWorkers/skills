---
name: granola-mcp
description: >
  **Granola与MCP的集成（支持管理式身份验证）**  
  当用户需要通过MCP搜索会议内容、获取会议摘要、查找待办事项或检索会议记录时，可使用此功能。对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# Granola MCP

通过MCP（模型上下文协议，Model Context Protocol）访问Granola服务，并支持身份验证。

## 快速入门

```bash
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
https://gateway.maton.ai/granola/{tool-name}
```

请将 `{tool-name}` 替换为相应的MCP工具名称（例如 `query_granola_meetings`）。该网关会将请求代理到 `mcp.granola.ai` 并自动插入您的凭据。

## 身份验证

所有请求都需要使用Maton API密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的Granola MCP连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=granola&method=MCP&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'granola', 'method': 'MCP'}).encode()
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
    "status": "PENDING",
    "creation_time": "2026-02-24T11:34:46.204677Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "granola",
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

如果您有多个Granola连接，必须使用 `Maton-Connection` 标头指定要使用的连接：

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

**注意：** 如果省略此参数，网关将使用默认的（最新的）活动连接。但如果该连接不是MCP连接，则可能会导致问题。

## MCP参考

所有MCP工具都使用 `POST` 方法：

| 工具 | 描述 | 数据格式 |
|------|-------------|--------|
| `query_granola_meetings` | 使用自然语言查询会议笔记 | [数据格式](schemas/query_granola_meetings.json) |
| `list_meetings` | 列出带有元数据和参与者的会议 | [数据格式](schemas/list_meetings.json) |
| `get_meetings` | 获取特定会议的详细内容 | [数据格式](schemas/get_meetings.json) |
| `get_meeting_transcript` | 获取原始会议记录（仅限付费版本） | [数据格式](schemas/get_meeting_transcript.json) |

### 查询会议

使用自然语言查询与会议笔记进行交互：
```bash
POST /granola/query_granola_meetings
Content-Type: application/json

{
  "query": "What action items came from my meetings this week?"
}
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
- “查找我会议中提到的所有与预算相关的内容”

### 列出会议

列出包含ID、标题、日期和参与者的会议：
```bash
POST /granola/list_meetings
Content-Type: application/json

{}
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
- `meetings_data`：包含 `from`、`to` 日期范围和会议数量的容器
- `meeting`：包含 `id`、`title` 和 `date` 属性的个别会议信息
- `known_participants`：包含参与者姓名、角色、公司和电子邮件的列表

### 获取会议详细信息

通过ID获取特定会议的详细内容：
```bash
POST /granola/get_meetings
Content-Type: application/json

{
  "meeting_ids": ["0dba4400-50f1-4262-9ac7-89cd27b79371"]
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "<meetings_data from=\"Feb 4, 2026\" to=\"Feb 4, 2026\" count=\"1\">\n<meeting id=\"0dba4400-50f1-4262-9ac7-89cd27b79371\" title=\"Team sync\" date=\"Feb 4, 2026 7:30 PM\">\n  <known_participants>\n  John Doe (note creator) from Acme <john@acme.com>\n  </known_participants>\n  \n  <summary>\n## Key Decisions\n- Approved Q1 roadmap\n- Budget increased by 15%\n\n## Action Items\n- @john: Review design specs by Friday\n- @jane: Schedule engineering sync\n</summary>\n</meeting>\n</meetings_data>"
    }
  ],
  "isError": false
}
```

**响应内容包括：**
- 会议元数据（ID、标题、日期、参与者）
- `summary`：由AI生成的会议摘要，包含关键决策和行动项
- 增强的会议笔记和私人笔记（如果可用）

### 获取会议记录

获取特定会议的原始记录（仅限付费版本）：
```bash
POST /granola/get_meeting_transcript
Content-Type: application/json

{
  "meeting_id": "0dba4400-50f1-4262-9ac7-89cd27b79371"
}
```

**付费版本的响应：**
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

**免费版本的响应：**
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
const response = await fetch('https://gateway.maton.ai/granola/query_granola_meetings', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
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

# Query meeting notes
response = requests.post(
    'https://gateway.maton.ai/granola/query_granola_meetings',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': 'What were the action items from my last meeting?'
    }
)
print(response.json())
```

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到Granola连接 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 日限请求次数达到上限（约100次/分钟） |

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

### 故障排除：应用程序名称错误

1. 确保您的URL路径以 `granola` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/granola/query_granola_meetings`
- 错误的路径：`https://gateway.maton.ai/query_granola_meetings`

### 故障排除：MCP参数错误

如果缺少必需的参数，MCP工具会返回验证错误：

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

## 注意事项

- 所有ID都是UUID（可能包含连字符或不包含连字符）
- MCP工具的响应数据采用 `{"content": [{"type": "text", "text": "..."}, "isError": false}` 的格式
- 用户只能查询自己的会议笔记；无法访问他人的共享笔记
- 基础（免费）计划用户只能查看过去30天的笔记
- `get_meeting_transcript` 工具仅适用于付费版本的Granola服务

## 资源

- [Granola MCP文档](https://docs.granola.ai/help-center/sharing/integrations/mcp)
- [Granola帮助中心](https://docs.granola.ai)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)