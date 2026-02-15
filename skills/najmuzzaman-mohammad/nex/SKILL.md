---
name: nex
description: 访问您的 Nex CRM——管理记录、列表，查询您的上下文图谱，并获取实时洞察。
emoji: "\U0001F4CA"
metadata: {"openclaw": {"requires": {"env": ["NEX_API_KEY"]}, "primaryEnv": "NEX_API_KEY"}}
---

# Nex – OpenClaw 的客户关系管理（CRM）与上下文图谱工具

Nex 为您的 AI 代理提供了全面的 CRM 功能：可以创建和管理记录、查询上下文图谱、处理对话内容，并实时获取洞察信息。

## 设置

1. 从 [https://app.nex.ai/settings/developer](https://app.nex.ai/settings/developer) 获取您的 API 密钥。
2. 将 API 密钥添加到 `~/.openclaw/openclaw.json` 文件中：
   ```json
   {
     "skills": {
       "entries": {
         "nex": {
           "enabled": true,
           "env": {
             "NEX_API_KEY": "sk-your_key_here"
           }
         }
       }
     }
   }
   ```

## 如何进行 API 调用

**重要提示**：Nex API 的响应时间可能为 10 至 60 秒。您必须在执行 API 调用时设置 `timeout: 120` 参数。

使用 `exec` 工具时，务必包含以下内容：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST ...",
  "timeout": 120
}
```

## API 权限范围

每个 API 密钥都有一定的权限范围。在 [https://app.nex.ai/settings/developer](https://app.nex.ai/settings/developer) 创建密钥时，请申请所需的权限范围。

| 权限范围 | 授权访问的内容 |
|---------|-----------------|
| `object.read` | 列出对象、查看对象结构 |
| `record.read` | 获取和列出记录 |
| `record.write` | 创建、更新或插入记录 |
| `list.read` | 查看列表 |
| `list.member.read` | 查看列表成员 |
| `list.member.write` | 添加或更新列表成员 |
| `insight.stream` | 获取洞察信息（REST + SSE 流式传输） |

## 功能介绍

### 对象与结构查询

#### 列出对象

查询可用的对象类型（如人员、公司等）及其属性结构。在创建或查询记录之前，请先调用此接口以了解可用的字段。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/objects`
**权限范围**：`object.read`

**查询参数**：
- `include_attributes`（布尔值，可选）——设置为 `true` 以包含属性定义

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/objects?include_attributes=true' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "data": [
    {
      "id": "123",
      "slug": "person",
      "name": "Person",
      "name_plural": "People",
      "type": "object",
      "description": "A contact or person",
      "attributes": [
        {
          "id": "1",
          "slug": "name",
          "name": "Name",
          "type": "name",
          "options": {
            "is_required": true,
            "is_unique": false,
            "is_multi_value": false
          }
        },
        {
          "id": "2",
          "slug": "email",
          "name": "Email",
          "type": "email",
          "options": {
            "is_required": false,
            "is_unique": true
          }
        }
      ]
    }
  ]
}
```

#### 列出对象所属的列表

获取与特定对象类型关联的所有列表。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/objects/{slug}/lists`
**权限范围**：`list.read`

**参数**：
- `slug`（路径）——对象类型的标识符（例如 `person`、`company`）
- `include_attributes`（查询参数，可选）——是否包含属性定义

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/objects/person/lists?include_attributes=true' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "data": [
    {
      "id": "456",
      "slug": "vip-contacts",
      "name": "VIP Contacts",
      "type": "list",
      "attributes": []
    }
  ]
}
```

---

### 记录操作

#### 创建记录

为特定对象类型创建新记录。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/objects/{slug}`
**权限范围**：`record.write`

**请求参数**：
- `slug`（路径）——对象类型的标识符（例如 `person`、`company`）

**请求体**：
- `attributes`（必填）——必须包含 `name`（字符串或对象）。其他字段取决于对象的结构。

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/objects/person' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"attributes\":{\"name\":{\"first_name\":\"Jane\",\"last_name\":\"Doe\"},\"email\":\"jane@example.com\",\"company\":\"Acme Corp\"}}'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "id": "789",
  "object_id": "123",
  "type": "person",
  "workspace_id": "111",
  "attributes": {
    "name": {"first_name": "Jane", "last_name": "Doe"},
    "email": "jane@example.com",
    "company": "Acme Corp"
  },
  "created_at": "2026-02-11T10:00:00Z",
  "updated_at": "2026-02-11T10:00:00Z"
}
```

#### 插入/更新记录

如果记录不存在，则创建新记录；如果找到匹配项，则更新现有记录。

**接口地址**：`PUT https://app.nex.ai/api/developers/v1/objects/{slug}`
**权限范围**：`record.write`

**请求体**：
- `attributes`（必填）——创建记录时必须提供 `name`
- `matching_attribute`（必填）——用于匹配的属性的标识符或 ID（例如 `email`）

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X PUT 'https://app.nex.ai/api/developers/v1/objects/person' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"matching_attribute\":\"email\",\"attributes\":{\"name\":\"Jane Doe\",\"email\":\"jane@example.com\",\"job_title\":\"VP of Sales\"}}'",
  "timeout": 120
}
```

#### 获取记录

通过记录 ID 获取特定记录。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/records/{record_id}`
**权限范围**：`record.read`

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/records/789' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

#### 更新记录

更新现有记录的特定属性。仅修改提供的属性。

**接口地址**：`PATCH https://app.nex.ai/api/developers/v1/records/{record_id}`
**权限范围**：`record.write`

**请求体**：
- `attributes`——需要更新的属性

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X PATCH 'https://app.nex.ai/api/developers/v1/records/789' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"attributes\":{\"job_title\":\"CTO\",\"phone\":\"+1-555-0123\"}}'",
  "timeout": 120
}
```

#### 列出记录

列出特定对象类型的记录，支持过滤、排序和分页。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/objects/{slug}/records`
**权限范围**：`record.read`

**请求参数**：
- `attributes`——返回哪些属性：`"all"`、`"primary"`、`"none"` 或自定义对象
- `limit`（整数）——返回的记录数量
- `offset`（整数）——分页偏移量
- `sort`——包含 `attribute`（属性名称）和 `direction`（`"asc"` 或 `desc`）的对象

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/objects/person/records' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"attributes\":\"all\",\"limit\":10,\"offset\":0,\"sort\":{\"attribute\":\"updated_at\",\"direction\":\"desc\"}}'",
  "timeout": 120
}
```

#### 向列表中添加成员

向列表中添加现有记录。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/lists/{id}`
**权限范围**：`list.member.write`

**请求参数**：
- `id`（路径）——列表的 ID
- `attributes`（可选）——要添加的记录的属性值

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/lists/456' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"parent_id\":\"789\",\"attributes\":{\"status\":\"active\"}}'",
  "timeout": 120
}
```

#### 更新列表成员

向列表中添加记录，或更新已存在的成员的列表特定属性。

**接口地址**：`PUT https://app.nex.ai/api/developers/v1/lists/{id}`
**权限范围**：`list.member.write`

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X PUT 'https://app.nex.ai/api/developers/v1/lists/456' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"parent_id\":\"789\",\"attributes\":{\"priority\":\"high\"}}'",
  "timeout": 120
}
```

#### 获取列表中的记录

从特定列表中获取分页记录。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/lists/{id}/records`
**权限范围**：`list.member.read`

**请求参数**：
- `attributes`——与 `List Records` 相同
- `limit`、`offset`、`sort` 参数也相同

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/lists/456/records' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"attributes\":\"all\",\"limit\":20}'",
  "timeout": 120
}
```

#### 更新列表记录

更新列表中记录的列表特定属性。

**接口地址**：`PATCH https://app.nex.ai/api/developers/v1/lists/{id}/records/{record_id}`
**权限范围**：`list.member.write`

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X PATCH 'https://app.nex.ai/api/developers/v1/lists/456/records/789' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"attributes\":{\"status\":\"closed-won\"}}'",
  "timeout": 120
}
```

### 上下文与 AI 功能

#### 查询上下文（使用 Ask API）

当需要检索关于联系人、公司或关系的信息时，使用此接口。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/context/ask`
**权限范围**：`record.read`

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/context/ask' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"query\":\"What do I know about John Smith?\"}'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "answer": "John Smith is a VP of Sales at Acme Corp...",
  "entities_considered": [
    {"id": 123, "name": "John Smith", "type": "contact"}
  ],
  "signals_used": [
    {"id": 456, "content": "Met at conference last month"}
  ],
  "metadata": {
    "query_type": "entity_specific"
  }
}
```

**示例查询**：
- “这周与我联系最频繁的联系人是谁？”
- “我们在医疗行业与哪些公司合作？”
- “我上次与 Sarah 的会议中讨论了什么？”

#### 添加上下文（使用 ProcessText API）

使用此接口将新信息（来自对话、会议记录或其他文本）导入系统。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/context/text`
**权限范围**：`record.write`

**请求参数**：
- `content`（必填）——需要处理的文本
- `context`（可选）——关于文本的额外上下文信息（例如：“销售电话记录”）

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/context/text' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"content\":\"Had a great call with John Smith from Acme Corp.\",\"context\":\"Sales call notes\"}'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "artifact_id": "abc123"
}
```

调用 ProcessText 后，使用 `GetArtifactStatus` 接口检查处理结果。

#### 获取处理结果状态

调用 ProcessText 后，使用此接口检查处理状态和结果。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/context/artifacts/{artifact_id}`
**权限范围**：`record.read`

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/context/artifacts/abc123' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "operation_id": 48066188026052610,
  "status": "completed",
  "result": {
    "entities_extracted": [
      {"name": "John Smith", "type": "PERSON", "action": "created"},
      {"name": "Acme Corp", "type": "COMPANY", "action": "updated"}
    ],
    "entities_created": 1,
    "entities_updated": 1,
    "relationships": 1,
    "insights": [
      {"content": "Acme Corp expanding to APAC", "confidence": 0.85}
    ],
    "tasks": []
  },
  "created_at": "2026-02-05T10:30:00Z",
  "completed_at": "2026-02-05T10:30:15Z"
}
```

**状态值**：`pending`、`processing`、`completed`、`failed`

**典型工作流程**：
1. 调用 ProcessText -> 获取 `artifact_id`
2. 每 2-5 秒轮询一次 `GetArtifactStatus`
3. 当状态变为 `completed` 或 `failed` 时停止轮询
4. 将提取的实体和洞察信息报告给用户

#### 创建 AI 列表任务

使用自然语言查询上下文图谱，生成联系人或公司的列表。

**接口地址**：`POST https://app.nex.ai/api/developers/v1/context/list/jobs`
**权限范围**：`record.read`

**请求参数**：
- `query`（必填）——自然语言查询（例如：“所有要求签订合同的公司”）
- `object_type`（可选）——`"contact"` 或 `"company"`（默认值：`"contact"`）
- `limit`（可选）——结果数量（默认值：50，最大值：100）
- `include_attributes`（可选）——是否包含所有实体属性（默认值：false）

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s -X POST 'https://app.nex.ai/api/developers/v1/context/list/jobs' -H 'Authorization: Bearer $NEX_API_KEY' -H 'Content-Type: application/json' -d '{\"query\":\"high priority contacts in enterprise deals\",\"object_type\":\"contact\",\"limit\":20,\"include_attributes\":true}'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "message": {
    "job_id": "12345678901234567",
    "status": "pending"
  }
}
```

#### 检查 AI 列表任务状态

检查 AI 列表生成任务的进度和结果。持续轮询直到状态变为 `completed` 或 `failed`。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/context/list/jobs/{job_id}`
**权限范围**：`record.read`

**查询参数**：
- `include_attributes`（布尔值，可选）——是否包含每个实体的完整属性

**调用方式**：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/context/list/jobs/12345678901234567?include_attributes=true' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

**响应内容**：
```json
{
  "message": {
    "job_id": "12345678901234567",
    "status": "completed",
    "created_at": "2026-02-11T10:00:00Z",
    "count": 5,
    "query_interpretation": "Finding contacts involved in enterprise-level deals marked as high priority",
    "entities": [
      {
        "id": "789",
        "name": "Jane Doe",
        "type": "contact",
        "reason": "Lead on $500K enterprise deal with Acme Corp, marked high priority",
        "highlights": [
          "Contract negotiation in progress",
          "Budget approved Q1 2026",
          "Executive sponsor confirmed"
        ],
        "attributes": {}
      }
    ]
  }
}
```

**状态值**：`pending`、`processing`、`completed`、`failed`

**典型工作流程**：
1. 使用自然语言查询创建任务 -> 获取 `job_id`
2. 每 2-5 秒轮询一次 `GetAIListJobStatus`
3. 当状态变为 `completed` 或 `failed` 时停止轮询
4. 向用户展示匹配的实体及其相关信息

### 获取洞察信息

#### 获取洞察信息（REST 方式）

按时间窗口查询洞察信息。支持两种模式。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/insights`
**权限范围**：`insight.stream`

**查询参数**：
- `last`——时间窗口（例如 `30m`、`2h`、`1h30m`
- `from` + `to`——UTC 时间范围（RFC3339 格式）
- `limit`（可选）——最大结果数量（默认值：20，最大值：100）

如果未指定 `last` 或 `from`/`to`，则返回最近的 20 条洞察信息。

**调用方式**：
- 获取过去 30 分钟的洞察信息：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/insights?last=30m' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

- 在两个日期之间查询：
```json
{
  "tool": "exec",
  "command": "curl -s 'https://app.nex.ai/api/developers/v1/insights?from=2026-02-07T00:00:00Z&to=2026-02-08T00:00:00Z' -H 'Authorization: Bearer $NEX_API_KEY'",
  "timeout": 120
}
```

**使用场景**：
- 在需要定期轮询时（无需维持 SSE 连接）
- 启动时获取当前的洞察状态
- 当 SSE 连接中断时作为备用方案
- 查看特定时间段的洞察信息

#### 实时洞察流（SSE）

实时接收新生成的洞察信息。

**接口地址**：`GET https://app.nex.ai/api/developers/v1/insights/stream`
**权限范围**：`insight.stream`

**连接方式**：
- 服务器在连接时发送 `: connected workspace_id=... token_id=...` 的信息
- 最新的洞察信息会通过 `insight.replay` 事件立即重播（最多 20 条）
- 每 30 秒发送一次保持连接的请求（`: keepalive`）
- 实时事件格式为：`event: insight.batch.created\ndata: {...}\n\n`

**事件数据结构**：
```json
{
  "workspace": {
    "name": "Acme Corp",
    "slug": "acme",
    "business_info": {"name": "Acme Corp", "domain": "acme.com"}
  },
  "insights": [{
    "type": "opportunity",
    "type_description": "A potential business opportunity",
    "content": "Budget approval expected next quarter",
    "confidence": 0.85,
    "confidence_level": "high",
    "target": {
      "type": "entity",
      "entity_type": "person",
      "hint": "John Smith",
      "signals": [{"type": "email", "value": "john@acme.com"}]
    },
    "evidence": [{
      "excerpt": "We should have budget approval by Q2",
      "artifact": {"type": "email", "subject": "RE: Proposal"}
    }]
  }],
  "insight_count": 1,
  "emitted_at": "2026-02-05T10:30:00Z"
}
```

**洞察类型**：`opportunity`、`risk`、`relationship`、`preference`、`milestone`、`activity`、`characteristic`、`role_detail`

**使用建议**：在活跃的对话过程中保持 SSE 连接处于开启状态。对于一次性查询，建议使用 Ask API。

## 错误处理

| 状态码 | 含义 | 应对措施 |
|-------------|---------|--------|
| 400 | 请求无效 | 检查请求体和参数 |
| 401 | API 密钥无效 | 确保 NEX_API_KEY 设置正确 |
| 403 | 缺少必要的权限范围 | 确保 API 密钥具有所需的权限范围 |
| 404 | 未找到记录/对象/列表 | 检查记录/对象/列表 ID 是否存在 |
| 429 | 请求频率限制 | 等待一段时间后重试（采用指数级退避策略） |
| 500 | 服务器错误 | 稍后重试 |

## Nex 的适用场景

**适用场景**：
- 在回复消息前，查询有关联系人的上下文信息
- 对话结束后，处理对话记录以更新上下文图谱
- 当被询问联系人或公司的关系或历史记录时
- 根据对话内容创建或更新 CRM 记录
- 从联系人数据库中构建目标列表
- 在会议前查询记录详情

**不适用场景**：
- 一般性知识查询（使用网页搜索）
- 实时日历/调度（使用日历工具）
- 需要完整 Nex 用户界面的直接 CRM 数据录入