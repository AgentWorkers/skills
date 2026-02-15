---
name: nex
description: 访问您的 Nex CRM（客户关系管理系统）——您可以管理记录、列表、任务和笔记，查询您的业务数据图（context graph），并获取实时洞察。
emoji: "\U0001F4CA"
metadata: {"clawdbot": {"secrets": ["NEX_API_KEY"], "requires": {"bins": ["curl", "jq", "bash"]}, "emoji": "\U0001F4CA"}}
---
# Nex – 客户关系管理（CRM）与上下文图谱

Nex 为您的 AI 代理提供了全面的 CRM 功能：创建和管理记录、定义自定义数据结构、建立关联关系、跟踪任务和笔记、查询上下文图谱、处理对话内容，并实时获取洞察信息。

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

## 安全性与隐私

- 所有 API 调用都通过一个经过验证的封装脚本 (`scripts/nex-api.sh`) 进行路由。
- 该脚本确保所有请求仅发送到 `https://app.nex.ai/api/developers`。
- 不会将任何用户输入插入到 shell 命令字符串中。
- API 密钥从 `$NEX_API_KEY` 环境变量中读取（绝不会通过提示获取）。
- JSON 请求体通过标准输入（stdin）传递，以避免 shell 注入攻击。
- 封装脚本使用 `set -euo pipefail` 以确保 shell 命令的安全执行。

## 外部端点

| URL 模式 | 方法 | 发送的数据 |
|-------------|---------|-----------|
| `https://app.nex.ai/api/developers/v1/*` | GET, POST, PUT, PATCH, DELETE | CRM 记录、查询、文本内容 |

## 如何进行 API 调用

**重要提示**：Nex API 的响应时间可能为 10-60 秒。因此，在每次执行工具调用时，必须设置 `timeout: 120`。

所有 API 调用都通过位于 `{baseDir}/scripts/nex-api.sh` 的封装脚本进行：

**GET 请求**：
```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/objects",
  "timeout": 120
}
```

**带有 JSON 正文的 POST 请求**（通过 stdin 传递正文）：
```json
{
  "tool": "exec",
  "command": "echo '{\"query\":\"What do I know about John?\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/context/ask",
  "timeout": 120
}
```

**使用 jq 过滤器的 GET 请求**（第三个参数）：
```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET '/v1/insights?last=1h' '[.insights[] | {type, content}]'",
  "timeout": 120
}
```

**SSE 流**：
```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh sse /v1/insights/stream",
  "timeout": 120
}
```

### 处理大型响应

Nex API 的响应内容（尤其是洞察信息和记录列表）可能超过 10KB。执行工具可能会截断输出。**必须正确处理这种情况**。

**使用封装脚本中的 jq 过滤器（第三个参数）** 来提取所需的数据：
```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET '/v1/insights?last=1h' '[.insights[] | {type, content, confidence_level, who: .target.hint, evidence: [.evidence[].excerpt]}]'",
  "timeout": 120
}
```

**处理 API 输出的规则**：
1. **切勿在输出被截断或混乱时默认认为“没有数据”。** 如果输出看起来不完整，请使用 jq 过滤器重新获取完整的数据。
2. **在解析之前验证 JSON 数据。** 如果响应不以 `{` 或 `[` 开头，说明输出可能已被截断——请重新获取。
3. **每个洞察信息都可能具有实际价值。** 新联系人、提到的集成、会议、风险、机会等都应该被记录下来。不要将某些洞察信息视为“无用信息”或“旧信息”而忽略。
4. **如果执行工具显示“（尚未有输出）”，请等待并使用适当的限制次数重新获取结果。** 不要跳过任何结果。

## API 权限范围

每个 API 密钥都有一定的权限范围。在 [https://app.nex.ai/settings/developer](https://app.nex.ai/settings/developer) 创建密钥时，请申请所需的权限范围。

| 权限范围 | 授权访问的内容 |
|-------|-----------------|
| `object.read` | 列出对象、查看数据结构、获取对象定义 |
| `object.write` | 创建/更新/删除对象定义和属性 |
| `record.read` | 获取、列出、搜索记录、时间线 |
| `record.write` | 创建、更新、插入/删除记录 |
| `list.read` | 查看列表及其定义 |
| `list.member.read` | 查看列表成员 |
| `list.member.write` | 添加、更新、删除列表成员 |
| `relationship.read` | 读取关系定义 |
| `relationship.write` | 创建/删除关系定义和实例 |
| `task.read` | 读取任务 |
| `task.write` | 创建/更新/删除任务 |
| `note.read` | 读取笔记 |
| `note.write` | 创建/更新笔记 |
| `insight.stream` | 洞察信息的 REST 和 SSE 流 |

## 选择合适的 API

在调用端点之前，先确定哪种方法适合您的需求：

| 情况 | 使用的方法 | 原因 |
|-----------|-----|-----|
| 您有结构化的数据（包含已知字段，如名称、电子邮件、公司名称） | **Create/Update Record** | 可以精确映射字段 |
| 您有非结构化的文本（如会议记录、电子邮件、对话内容） | **ProcessText API** | AI 可以提取实体、创建/更新记录，并自动生成洞察信息 |
| 您不确定要传递哪些属性或数据格式混乱 | **ProcessText API** | 让 AI 自动识别实体和关系 |
| 您知道具体的对象标识符并需要筛选列表 | **AI List Job** | 使用自然语言查询特定的对象类型 |
| 您不确定要查询的对象类型或问题比较开放 | **Ask API** | 在整个上下文图谱中搜索 |
| 您需要根据 ID 或分页获取特定记录 | **Get/List Records** | 直接访问数据 |
| 您希望根据名称在所有类型中查找记录 | **Search API** | 在所有对象类型中进行快速文本搜索 |

**关键提示**：当处理对话或非结构化数据时，优先使用 ProcessText API。只有在数据结构清晰、字段名称已知的情况下，才使用确定性的 Record API。

## 功能

### 数据结构管理

#### 创建对象定义

创建一个新的自定义对象类型。

**端点**：`POST /v1/objects`
**权限范围**：`object.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `name` | string | 是 | 显示名称 |
| `name_plural` | string | 否 | 复数显示名称 |
| `slug` | string | 是 | URL 安全标识符 |
| `description` | string | 否 | 描述 |
| `type` | string | 否 | `"person"`, `"company"`, `"custom"`, `"deal"`（默认：`custom`） |

```json
{
  "tool": "exec",
  "command": "echo '{\"name\":\"Project\",\"name_plural\":\"Projects\",\"slug\":\"project\",\"description\":\"Project tracker\",\"type\":\"custom\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/objects",
  "timeout": 120
}
```

#### 获取对象定义

获取单个对象及其属性的定义。

**端点**：`GET /v1/objects/{slug}`
**权限范围**：`object.read`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/objects/project",
  "timeout": 120
}
```

#### 列出对象

查看可用的对象类型（如人员、公司等）及其属性结构。**在创建或查询记录之前，请先调用此端点**。

**端点**：`GET /v1/objects`
**权限范围**：`object.read`

**查询参数**：
- `include_attributes`（布尔值，可选）——设置为 `true` 以包含属性定义

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET '/v1/objects?include_attributes=true'",
  "timeout": 120
}
```

**响应**：
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
        }
      ]
    }
  ]
}
```

#### 更新对象定义

更新现有的对象定义。

**端点**：`PATCH /v1/objects/{slug}`
**权限范围**：`object.write`

**请求体**（所有字段均为可选）：
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `name` | string | 新显示名称 |
| `name_plural` | string | 新复数名称 |
| `description` | string | 新描述 |

```json
{
  "tool": "exec",
  "command": "echo '{\"name\":\"Updated Project\",\"description\":\"Updated description\"}' | bash {baseDir}/scripts/nex-api.sh PATCH /v1/objects/project",
  "timeout": 120
}
```

#### 删除对象定义

删除对象定义及其所有记录。

**端点**：`DELETE /v1/objects/{slug}`
**权限范围**：`object.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/objects/project",
  "timeout": 120
}
```

#### 创建属性定义

为对象类型添加新的属性。

**端点**：`POST /v1/objects/{slug}/attributes`
**权限范围**：`object.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `name` | string | 显示名称 |
| `slug` | string | URL 安全标识符 |
| `type` | string | `"text"`, `"number"`, `"email"`, `"phone"`, `"url"`, `"date"`, `"boolean"`, `"currency"`, `"location"`, `"select"`, `"social_profile"`, `"domain"`, `"full_name"` |
| `description` | string | 否 | 描述 |
| `options` | object | 否 | `is_required`, `is_unique`, `is_multi_value`, `use_raw_format`, `is_whole_number`, `select_options` |

```json
{
  "tool": "exec",
  "command": "echo '{\"name\":\"Status\",\"slug\":\"status\",\"type\":\"select\",\"description\":\"Current status\",\"options\":{\"is_required\":true,\"select_options\":[{\"name\":\"Open\"},{\"name\":\"In Progress\"},{\"name\":\"Done\"}]}}' | bash {baseDir}/scripts/nex-api.sh POST /v1/objects/project/attributes",
  "timeout": 120
}
```

#### 更新属性定义

更新现有的属性定义。

**端点**：`PATCH /v1/objects/{slug}/attributes/{attr_id}`
**权限范围**：`object.write`

**请求体**（所有字段均为可选）：
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `name` | 字符串 | 新显示名称 |
| `description` | 字符串 | 新描述 |
| `options` | object | `is_required`, `select_options`, `use_raw_format`, `is_whole_number` |

```json
{
  "tool": "exec",
  "command": "echo '{\"name\":\"Updated Status\",\"options\":{\"is_required\":false}}' | bash {baseDir}/scripts/nex-api.sh PATCH /v1/objects/project/attributes/456",
  "timeout": 120
}
```

#### 删除属性定义

从对象类型中删除属性。

**端点**：`DELETE /v1/objects/{slug}/attributes/{attr_id}`
**权限范围**：`object.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/objects/project/attributes/456",
  "timeout": 120
}
```

---

### 记录

> 当您的输入是非结构化文本（如对话记录、会议笔记、电子邮件）时，**优先使用 ProcessText API**。ProcessText 可以自动创建和更新记录、提取关系并生成洞察信息。只有在数据结构清晰、字段名称和值已知的情况下，才使用以下端点。

#### 创建记录

为特定对象类型创建新记录。

**端点**：`POST /v1/objects/{slug}`
**权限范围**：`record.write`

**请求体**：
- `attributes`（必填）——必须包含 `name`（字符串）。其他字段取决于对象的数据结构。

```json
{
  "tool": "exec",
  "command": "echo '{\"attributes\":{\"name\":{\"first_name\":\"Jane\",\"last_name\":\"Doe\"},\"email\":\"jane@example.com\",\"company\":\"Acme Corp\"}}' | bash {baseDir}/scripts/nex-api.sh POST /v1/objects/person",
  "timeout": 120
}
```

**响应**：
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

#### 插入记录

如果记录不存在，则创建新记录；如果找到匹配项，则更新记录。

**端点**：`PUT /v1/objects/{slug}`
**权限范围**：`record.write`

**请求体**：
- `attributes`（必填）——创建时必须包含 `name`。
- `matching_attribute`（必填）——要匹配的属性的标识符（例如，`email`）。

```json
{
  "tool": "exec",
  "command": "echo '{\"matching_attribute\":\"email\",\"attributes\":{\"name\":\"Jane Doe\",\"email\":\"jane@example.com\",\"job_title\":\"VP of Sales\"}}' | bash {baseDir}/scripts/nex-api.sh PUT /v1/objects/person",
  "timeout": 120
}
```

#### 获取记录

通过 ID 获取特定记录。

**端点**：`GET /v1/records/{record_id}`
**权限范围**：`record.read`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/records/789",
  "timeout": 120
}
```

#### 更新记录

更新现有记录的特定属性。仅更改提供的属性。

**端点**：`PATCH /v1/records/{record_id}`
**权限范围**：`record.write`

**请求体**：
- `attributes`——要更新的属性

```json
{
  "tool": "exec",
  "command": "echo '{\"attributes\":{\"job_title\":\"CTO\",\"phone\":\"+1-555-0123\"}}' | bash {baseDir}/scripts/nex-api.sh PATCH /v1/records/789",
  "timeout": 120
}
```

#### 删除记录

永久删除记录。

**端点**：`DELETE /v1/records/{record_id}`
**权限范围**：`record.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/records/789",
  "timeout": 120
}
```

#### 列出记录

列出特定对象类型的记录，并支持过滤、排序和分页。

**端点**：`POST /v1/objects/{slug}/records`
**权限范围**：`record.read`

**请求体**：
- `attributes`——要返回的属性：`all`、`primary`、`none` 或自定义对象。
- `limit`（整数）——返回的记录数量。
- `offset`（整数）——分页偏移量。
- `sort`——包含 `attribute`（标识符）和 `direction`（`"asc"` 或 `desc`）的字段。

**响应**：
```json
{
  "data": [
    {
      "id": "789",
      "type": "person",
      "attributes": {"name": "Jane Doe", "email": "jane@example.com"},
      "created_at": "2026-02-11T10:00:00Z",
      "updated_at": "2026-02-11T10:00:00Z"
    }
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

#### 获取记录时间线

获取记录的分页时间线事件（如任务、笔记、属性更改等）。

**端点**：`GET /v1/records/{record_id}/timeline`
**权限范围**：`record.read`

**查询参数**：
- `limit`（整数）——最大事件数量（1-100，默认：50）。
- `cursor`（字符串）——上一次响应的分页游标。

**响应**：
```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET '/v1/records/1001/timeline?limit=20'",
  "timeout": 120
}
```

**资源类型**：`entity`, `task`, `note`, `list_item`, `attribute`
**事件类型**：`created`, `updated`, `deleted`, `archived`

---

### 关系

#### 创建关系定义

定义两种对象类型之间的关系。

**端点**：`POST /v1/relationships`
**权限范围**：`relationship.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `type` | 字符串 | 是 | `"one_to_one"`, `"one_to_many"`, `"many_to_many"` |
| `entity_definition_1_id` | 字符串 | 是 | 第一个对象的定义 ID |
| `entity_definition_2_id` | 字符串 | 是 | 第二个对象的定义 ID |
| `entity_1_to_2predicate` | 字符串 | 1->2 方向的标签 |
| `entity_2_to_1predicate` | 字符串 | 2->1 方向的标签 |

```json
{
  "tool": "exec",
  "command": "echo '{\"type\":\"one_to_many\",\"entity_definition_1_id\":\"123\",\"entity_definition_2_id\":\"456\",\"entity_1_to_2_predicate\":\"has\",\"entity_2_to_1_predicate\":\"belongs to\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/relationships",
  "timeout": 120
}
```

**响应**：
```json
{
  "id": "789",
  "type": "one_to_many",
  "entity_definition_1_id": "123",
  "entity_definition_2_id": "456",
  "entity_1_to_2_predicate": "has",
  "entity_2_to_1_predicate": "belongs to",
  "created_at": "2026-02-13T10:00:00Z"
}
```

#### 列出关系定义

获取工作空间中的所有关系定义。

**端点**：`GET /v1/relationships`
**权限范围**：`relationship.read`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/relationships",
  "timeout": 120
}
```

#### 删除关系定义

删除关系定义。

**端点**：`DELETE /v1/relationships/{id}`
**权限范围**：`relationship.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/relationships/789",
  "timeout": 120
}
```

#### 创建关系实例

使用现有的关系定义连接两个记录。

**端点**：`POST /v1/records/{record_id}/relationships`
**权限范围**：`relationship.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `definition_id` | 字符串 | 是 | 关系定义 ID |
| `entity_1_id` | 字符串 | 是 | 第一个记录的 ID |
| `entity_2_id` | 字符串 | 是 | 第二个记录的 ID |

```json
{
  "tool": "exec",
  "command": "echo '{\"definition_id\":\"789\",\"entity_1_id\":\"1001\",\"entity_2_id\":\"2002\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/records/1001/relationships",
  "timeout": 120
}
```

#### 删除关系实例

删除两个记录之间的关系。

**端点**：`DELETE /v1/records/{record_id}/relationships/{relationship_id}`
**权限范围**：`relationship.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/records/1001/relationships/5001",
  "timeout": 120
}
```

---

### 列表

#### 列出对象列表

获取与特定对象类型关联的所有列表。

**端点**：`GET /v1/objects/{slug}/lists`
**权限范围**：`list.read`

**参数**：
- `slug`（路径）——对象类型的标识符（例如，`person`, `company`）。
- `include_attributes`（查询，可选）——是否包含属性定义。

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET '/v1/objects/person/lists?include_attributes=true'",
  "timeout": 120
}
```

**响应**：
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

#### 创建列表

为特定对象类型创建新列表。

**端点**：`POST /v1/objects/{slug}/lists`
**权限范围**：`object.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `name` | 字符串 | 是 | 列表显示名称 |
| `name_plural` | 字符串 | 否 | 复数名称 |
| `slug` | 字符串 | URL 安全标识符 |
| `description` | 字符串 | 否 | 描述 |

```json
{
  "tool": "exec",
  "command": "echo '{\"name\":\"VIP Contacts\",\"slug\":\"vip-contacts\",\"description\":\"High-value contacts\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/objects/contact/lists",
  "timeout": 120
}
```

#### 获取列表定义

通过 ID 获取列表定义。

**端点**：`GET /v1/lists/{id}`
**权限范围**：`list.read`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/lists/300",
  "timeout": 120
}
```

#### 删除列表

删除列表定义。

**端点**：`DELETE /v1/lists/{id}`
**权限范围**：`object.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/lists/300",
  "timeout": 120
}
```

#### 向列表中添加成员

将现有记录添加到列表中。

**端点**：`POST /v1/lists/{id}`
**权限范围**：`list.member.write`

**请求体**：
- `parent_id`（必填）——要添加的现有记录的 ID。
- `attributes`（可选）——列表特定的属性值。

```json
{
  "tool": "exec",
  "command": "echo '{\"parent_id\":\"789\",\"attributes\":{\"status\":\"active\"}}' | bash {baseDir}/scripts/nex-api.sh POST /v1/lists/456",
  "timeout": 120
}
```

#### 插入列表成员

将记录添加到列表中，或更新列表中的属性（如果记录已经是列表成员）。

**端点**：`PUT /v1/lists/{id}`
**权限范围**：`list.member.write`

**请求体**：
- `parent_id`（必填）——要添加的记录的 ID。
- `attributes`（可选）——列表特定的属性值。

```json
{
  "tool": "exec",
  "command": "echo '{\"parent_id\":\"789\",\"attributes\":{\"priority\":\"high\"}}' | bash {baseDir}/scripts/nex-api.sh PUT /v1/lists/456",
  "timeout": 120
}
```

#### 获取列表中的记录

从特定列表中获取分页记录。

**端点**：`POST /v1/lists/{id}/records`
**权限范围**：`list.member.read`

**请求体**：与 `List Records` 相同。

**请求体参数**：
- `attributes`——要返回的属性。
- `limit`——`attributes`。
- `offset`——分页偏移量。
- `sort`——包含 `attribute`（标识符）和 `direction`（`"asc"` 或 `desc`）的字段。

**响应**：
```json
{
  "data": [
    {
      "id": "789",
      "type": "person",
      "attributes": {"name": "Jane Doe", "email": "jane@example.com"},
      "created_at": "2026-02-11T10:00:00Z",
      "updated_at": "2026-02-11T10:00:00Z"
    }
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

#### 获取记录时间线

获取记录的分页时间线事件（如任务、笔记、属性更改等）。

**端点**：`GET /v1/records/{record_id}/timeline`
**权限范围**：`record.read`

**查询参数**：
- `limit`（整数）——最大事件数量（1-100，默认：50）。
- `cursor`（字符串）——上一次响应的分页游标。

**响应**：
```json
{
  "data": [
    {
      "id": "5000",
      "resource_type": "task",
      "resource_id": "800",
      "event_type": "created",
      "event_payload": {
        "task": {"id": "800", "title": "Follow up", "priority": "high"}
      },
      "event_timestamp": "2026-02-13T10:00:00Z",
      "created_by": "developer_api"
    }
  ],
  "has_next_page": true,
  "next_cursor": "4999"
}
```

**资源类型**：`entity`, `task`, `note`, `list_item`, `attribute`
**事件类型**：`created`, `updated`, `deleted`, `archived`

---

### 关系

#### 创建关系定义

定义两种对象类型之间的关系。

**端点**：`POST /v1/relationships`
**权限范围**：`relationship.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `type` | 字符串 | 是 | `"one_to_one"`, `"one_to_many"`, `"many_to_many"` |
| `entity_definition_1_id` | 字符串 | 是 | 第一个对象的定义 ID |
| `entity_definition_2_id` | 字符串 | 是 | 第二个对象的定义 ID |
| `entity_1_to_2predicate` | 字符串 | 1->2 方向的标签 |
| `entity_2_to_1predicate` | 字符串 | 2->1 方向的标签 |

```json
{
  "tool": "exec",
  "command": "echo '{\"type\":\"one_to_many\",\"entity_definition_1_id\":\"123\",\"entity_definition_2_id\":\"456\",\"entity_1_to_2_predicate\":\"has\",\"entity_2_to_1_predicate\":\"belongs to\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/relationships",
  "timeout": 120
}
```

**响应**：
```json
{
  "id": "789",
  "type": "one_to_many",
  "entity_definition_1_id": "123",
  "entity_definition_2_id": "456",
  "entity_1_to_2_predicate": "has",
  "entity_2_to_1_predicate": "belongs to",
  "created_at": "2026-02-13T10:00:00Z"
}
```

#### 列出关系定义

获取工作空间中的所有关系定义。

**端点**：`GET /v1/relationships`
**权限范围**：`relationship.read`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/relationships",
  "timeout": 120
}
```

#### 删除关系定义

删除关系定义。

**端点**：`DELETE /v1/relationships/{id}`
**权限范围**：`relationship.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/relationships/789",
  "timeout": 120
}
```

#### 创建关系实例

使用现有的关系定义连接两个记录。

**端点**：`POST /v1/records/{record_id}/relationships`
**权限范围**：`relationship.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `definition_id` | 字符串 | 是 | 关系定义 ID |
| `entity_1_id` | 字符串 | 是 | 第一个记录的 ID |
| `entity_2_id` | 字符串 | 是 | 第二个记录的 ID |

```json
{
  "tool": "exec",
  "command": "echo '{\"definition_id\":\"789\",\"entity_1_id\":\"1001\",\"entity_2_id\":\"2002\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/records/1001/relationships",
  "timeout": 120
}
```

#### 删除关系实例

删除两个记录之间的关系。

**端点**：`DELETE /v1/records/{record_id}/relationships/{relationship_id}`
**权限范围**：`relationship.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/records/1001/relationships/5001",
  "timeout": 120
}
```

---

### 列表

#### 列出对象列表

获取与特定对象类型关联的所有列表。

**端点**：`GET /v1/objects/{slug}/lists`
**权限范围**：`list.read`

**参数**：
- `slug`（路径）——对象类型的标识符（例如，`person`, `company`）。
- `include_attributes`（查询，可选）——是否包含属性定义。

**响应**：
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

#### 创建列表

为特定对象类型创建新列表。

**端点**：`POST /v1/objects/{slug}/lists`
**权限范围**：`object.write`

**请求体**：
| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `name` | 字符串 | 是 | 列表显示名称 |
| `name_plural` | 字符串 | 否 | 复数名称 |
| `slug` | 字符串 | URL 安全标识符 |
| `description` | 字符串 | 否 | 描述 |

```json
{
  "tool": "exec",
  "command": "echo '{\"name\":\"VIP Contacts\",\"slug\":\"vip-contacts\",\"description\":\"High-value contacts\"}' | bash {baseDir}/scripts/nex-api.sh POST /v1/objects/contact/lists",
  "timeout": 120
}
```

#### 获取列表定义

通过 ID 获取列表定义。

**端点**：`GET /v1/lists/{id}`
**权限范围**：`list.read`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET /v1/lists/300",
  "timeout": 120
}
```

#### 删除列表

删除列表定义。

**端点**：`DELETE /v1/lists/{id}`
**权限范围**：`object.write`

```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh DELETE /v1/lists/300",
  "timeout": 120
}
```

#### 向列表中添加成员

将现有记录添加到列表中。

**端点**：`POST /v1/lists/{id}`
**权限范围**：`list.member.write`

**请求体**：
- `parent_id`（必填）——要添加的记录的 ID。
- `attributes`（可选）——列表特定的属性值。

```json
{
  "tool": "exec",
  "command": "echo '{\"parent_id\":\"789\",\"attributes\":{\"status\":\"active\"}}' | bash {baseDir}/scripts/nex-api.sh POST /v1/lists/456",
  "timeout": 120
}
```

#### 插入列表成员

将记录添加到列表中，或更新列表中的属性（如果记录已经是列表成员）。

**端点**：`PUT /v1/lists/{id}`
**权限范围**：`list.member.write`

**请求体**：
- `parent_id`（必填）——要添加的记录的 ID。
- `attributes`（可选）——列表特定的属性值。

```json
{
  "tool": "exec",
  "command": "echo '{\"parent_id\":\"789\",\"attributes\":{\"priority\":\"high\"}}' | bash {baseDir}/scripts/nex-api.sh PUT /v1/lists/456",
  "timeout": 120
}
```

#### 获取列表中的记录

从特定列表中获取分页记录。

**端点**：`POST /v1/lists/{id}/records`
**权限范围**：`list.member.read`

**请求体**：与 `List Records` 相同。

**请求体参数**：
- `attributes`——要获取的属性。
- `limit`——`limit`。
- `offset`——分页偏移量。
- `sort`——包含 `attribute`（标识符）和 `direction`（`asc` 或 `desc`）的字段。

**响应**：
```json
{
  "data": [
    {
      "id": "789",
      "type": "person",
      "attributes": {"name": "Jane Doe", "email": "jane@example.com"},
      "created_at": "2026-02-11T10:00:00Z",
      "updated_at": "2026-02-11T10:00:00Z"
    }
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

#### 获取记录时间线

获取记录的分页时间线事件（如任务、笔记、属性更改等）。

**端点**：`GET /v1/records/{record_id}/timeline`
**权限范围**：`record.read`

**查询参数**：
- `limit`（整数）——最大事件数量（1-100，默认：50）。
- `cursor`（字符串）——上一次响应的分页游标。

**响应**：
```json
{
  "data": [
    {
      "id": "5000",
      "resource_type": "task",
      "resource_id": "800",
      "event_type": "created",
      "event_payload": {
        "task": {"id": "800", "title": "Follow up", "priority": "high"}
      },
      "event_timestamp": "2026-02-13T10:00:00Z",
      "created_by": "developer_api"
    }
  ],
  "has_next_page": true,
  "next_cursor": "4999"
}
```

**资源类型**：`entity`, `task`, `note`, `list_item`, `attribute`
**事件类型**：`created`, `updated`, `deleted`, `archived`

---

### 洞察信息

#### 获取洞察信息（REST）

按时间窗口查询洞察信息。支持两种模式。

**端点**：`GET /v1/insights`
**权限范围**：`insight.stream`

**查询参数**：
- `last`——时间窗口（例如，`30m`, `2h`, `1h30m`）。
- `from` + `to`——UTC 时间范围（RFC3339 格式）。
- `limit`（可选）——最大结果数量（默认：20，最大：100）。

如果未指定 `last` 或 `from`/`to`，则返回最新的 20 条洞察信息。

**推荐使用 jq 过滤器（第三个参数）**（响应内容可能超过 10KB）：
```json
{
  "tool": "exec",
  "command": "bash {baseDir}/scripts/nex-api.sh GET '/v1/insights?last=1h' '{insight_count: (.insights | length), insights: [.insights[] | {type, content, confidence_level, who: .target.hint, entity_type: .target.entity_type}]}'",
  "timeout": 120
}
```

**使用场景**：
- 在定期轮询时，而不是保持 SSE 连接时。
- 在启动时获取当前的洞察信息状态。
- 当 SSE 连接中断时作为备用方案。
- 查看特定时间段的洞察信息。

**哪些内容可被记录**（在定期轮询时）：
- 新出现的联系人或公司。
- 被提及的机会、风险或里程碑。
- 表达的集成或工具偏好。
- 发生或计划中的会议。
- 关系变化（新的联系、角色变更、公司变动）。
- 任何 `confidence_level` 为 `"high"` 或 `"very_high"` 的洞察信息。

**切勿** 将洞察信息视为“已见过”或“无用信息”而忽略。每个轮询窗口都是独立的——如果发现新的洞察信息，请务必记录下来。

#### 实时洞察流（SSE）

实时接收发现的洞察信息。

**端点**：`GET /v1/insights/stream`
**权限范围**：`insight.stream`

**连接行为**：
- 服务器在连接时发送 `: connected workspace_id=... token_id=...`。
- 最新的洞察信息会通过 `insight.replay` 事件立即重新播放（最多 20 条）。
- 每 30 秒发送一次 `: keepalive` 评论以保持连接。
- 实时事件以如下格式发送：`event: insight.batch.created\ndata: {...}\n\n`。

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

**洞察类型**：`opportunity`, `risk`, `relationship`, `preference`, `milestone`, `activity`, `characteristic`, `role_detail`

**使用建议**：
- 在进行活跃对话时，在后台保持 SSE 连接。对于一次性查询，可以使用 Ask API。

## 错误处理

| 状态码 | 含义 | 处理方式 |
|-------------|---------|--------|
| 400 | 请求无效 | 检查请求体和参数。 |
| 401 | API 密钥无效 | 确保 `NEX_API_KEY` 设置正确。 |
| 403 | 缺少权限范围 | 确保 API 密钥具有所需的权限范围。 |
| 404 | 未找到 | 检查记录/对象/列表 ID 是否存在。 |
| 429 | 请求频率限制 | 等待一段时间后重试。 |
| 500 | 服务器错误 | 稍后重试。 |

## 何时使用 Nex

**适用场景**：
- 在回复消息之前，查询有关人员的上下文信息。
- 对话结束后，处理对话记录以更新上下文图谱。
- 当被询问与联系人/公司的关系或历史记录时。
- 根据对话内容创建或更新 CRM 记录。
- 从联系人数据库中创建目标列表。
- 在会议前查看记录详情。
- 创建任务和笔记以跟踪后续行动。
- 在所有记录类型中搜索特定的人或公司。
- 为工作空间定义自定义对象结构和关系。

**不适用场景**：
- 一般性知识查询（使用网页搜索）。
- 实时日历/调度（使用日历工具）。
- 需要完整 Nex 用户界面的直接 CRM 数据输入。