---
name: ragora
description: 使用 Ragora MCP 工具和 REST API 来发现、搜索并从知识库中合成答案。当用户请求从 Ragora 收集中获取有根据的答案、进行跨集合比较、基于来源的摘要生成、尽职调查研究，或使用市场数据进行验证时，触发相应操作。
metadata: {"openclaw": {"emoji": "🔎", "homepage": "https://github.com/velarynai/ragora-openclaw", "requires": {"env": ["RAGORA_API_KEY"]}, "primaryEnv": "RAGORA_API_KEY"}}
---

# OpenClaw的Ragora技能

使用此技能可以通过Ragora数据来回答问题。您有两种集成方式：

1. **MCP（模型上下文协议）** — 当您的客户端支持MCP工具绑定时推荐使用。
2. **REST API** — 当MCP不可用或需要细粒度控制时，可以通过HTTP直接使用。

这两种方式共享相同的认证、数据模型和搜索功能。

## 参考文档

当在不同环境中的行为不同时，请首先查阅以下文档：

- MCP指南：`https://ragora.app/docs?section=mcp-guide`
- 入门指南：`https://ragora.app/docs?section=getting-started`
- API概述：`https://ragora.app/docs?section=api-overview`
- API检索：`https://ragora.app/docs?section=api-retrieve`
- 错误和限制：`https://ragora.app/docs?section=api-errors`
- 账费API：`https://ragora.app/docs?section=api-billing`

---

## 核心概念

在使用任何工具之前，请先了解Ragora的数据模型。

### 收集（Collections）

**收集**是一个知识库——一组为语义搜索而编目的文档。每个收集包含：

- **名称** — 人类可读的标签（例如：“员工手册”）。
- **slug** — 用于动态工具和API路径的URL安全标识符（例如：`employee_handbook`）。
- **描述** — 收集的内容及其使用场景。
- **统计信息** — 文档数量、块数量、最后更新时间戳。

### 文档与块（Documents & Chunks）

每个收集包含**文档**（文件、页面、文章）。文档被分割成**块**——这些小段落优化了语义检索。搜索时，结果会以块的形式返回，并附带指向源文档的元数据。

### 版本（Versions）

某些收集支持**版本化的文档**（例如，API文档v1.0、v2.0）。使用`list_versions_{slug}()`或API来发现可用版本，然后通过`version`参数来限定搜索范围。

### 标签与过滤器（Tags & Filters）

收集可能支持：

- **自定义标签** — 附加到文档的字符串标签（例如：`["legal", "msa", "2024"]`）。作为`custom_tags`传递以缩小搜索范围。
- **过滤器** — 键值元数据过滤器（例如：`{"region": "US", "department": "engineering"}`）。作为`filters`传递以限制搜索结果。

### 信用与计费（Credits & Billing）

- **自己的收集和订阅** — 免费MCP/API访问，无需支付信用费用。
- **市场产品（按使用计费）** — 每次检索都会根据卖家的定价扣除信用费用。
- 信用以美元计。可以通过`check_balance()`或`GET /v1/billing/balance`来查看余额。
- 在`https://app.ragora.app/settings/billing`处充值。

---

## 连接设置

### 认证（Authentication）

所有请求（MCP和REST）都需要Ragora API密钥。

- **格式**：`sk_live_<uuid>`（例如：`sk_live_a1b2c3d4-e5f6-7890-abcd-ef1234567890`）
- **创建一个**：`https://app.ragora.app/settings/api-keys`
- **创建时显示一次** — 复制并安全存储它。
- **在服务器上哈希** — 使用SHA-256 + bcrypt。Ragora无法恢复丢失的密钥；请生成一个新的。

### 安全规则

- 切勿在URL查询参数中传递API密钥。
- 切勿在日志、输出或最终答案中打印完整的API密钥。
- 如果密钥丢失或无效，请停止操作并请求用户提供有效的密钥。
- 在任何调试输出中屏蔽密钥：`sk_live_****...`。

### MCP端点（MCP endpoint）

- **URL**：`https://mcp.ragora.app/mcp`
- **认证头**：`Authorization: Bearer <RAGORA_API_KEY>`

OpenClaw配置（YAML）：

```yaml
name: ragora
type: http
url: https://mcp.ragora.app/mcp
headers:
  Authorization: Bearer ${RAGORA_API_KEY}
```

Claude Desktop / Cursor / VS Code配置（JSON）：

```json
{
  "mcpServers": {
    "ragora": {
      "type": "http",
      "url": "https://mcp.ragora.app/mcp",
      "headers": {
        "Authorization": "Bearer ${RAGORA_API_KEY}"
      }
    }
  }
}
```

> **安全提示**：将`RAGORA_API_KEY`设置为操作系统或秘密管理器中的环境变量。切勿将原始的`sk_live_`值硬编码在可能提交到版本控制的配置文件中。

### REST API基础URL

- **基础**：`https://api.ragora.app/v1`
- **认证头**：`Authorization: Bearer <RAGORA_API_KEY>`
- **Content-Type**：对于所有POST/PUT请求，使用`application/json`。

---

## 连接性检查（首先运行）

### 通过MCP

1. 确认服务器是否正常运行：

```bash
curl -s https://mcp.ragora.app/health
```

2. 调用`discover_collections()`。如果返回了收集信息，说明已连接成功。

3. 如果没有结果——用户可能需要访问知识库：`https://ragora.app/marketplace`

4. 如果信用不足——调用`check_balance()`并提示用户前往`https://app.ragora.app/settings/billing`充值。

### 通过REST API

1. 确认服务器是否正常运行：

```bash
curl -s https://api.ragora.app/v1/health
```

2. 列出收集信息：

```bash
curl https://api.ragora.app/v1/collections \
  -H "Authorization: Bearer <RAGORA_API_KEY>"
```

3. 如果响应为`401`或`403`，则表示API密钥无效或已过期。请用户生成一个新的密钥。

---

## 操作规则

- 在进行针对性检索之前，先使用`discover_collections()`（MCP）或`GET /v1/collections`（API），除非用户明确指定了一个已知的收集。
- 一旦知道了可能的收集范围，优先使用针对性搜索而不是全局搜索。
- 仅在需要广泛探索时使用全局搜索——例如存在歧义、来源未知或初次发现时。
- 保持检索的迭代性：多次进行针对性查询，而不是使用一次性的长查询。
- 在最终答案中包含来源引用。
- 当证据不完整、相互矛盾或缺失时，要说明情况。
- 如果信用不足或出现错误，请提示用户检查余额并报告限制。
- 在MCP工具可用时优先使用MCP；当MCP绑定失败或需要MCP未提供的功能（例如分页、收集元数据）时，使用REST API。

---

## MCP工具参考

### 静态工具（始终可用）

| 工具 | 参数 | 描述 |
|------|-----------|-------------|
| `discover_collections()` | 无 | 列出所有可访问的知识库，包括描述、统计信息、可用操作和使用示例。 |
| `search(query, top_k?)` | `query`（必填），`top_k`（1-20，默认5） | 同时搜索所有可访问的收集。 |
| `search_collection(collection_name, query, top_k?, custom_tags?, filters?)` | `collection_name`（必填），`query`（必填），`top_k`（1-20，默认5），`custom_tags`（字符串列表），`filters`（对象） | 按名称或slug搜索特定收集。 |
| `check_balance()` | 无 | 剩余信用和估计的USD价值。 |

### 动态工具（每个收集都会在清单中生成）

网关会为您可访问的每个收集生成这些工具。`{slug}`是收集的URL安全名称（例如：`employee_handbook`，`k8s_troubleshooting`）。

| 工具 | 参数 | 描述 |
|------|-----------|-------------|
| `search_{slug}(query, top_k?, version?, custom_tags?, filters?)` | `query`（必填），`top_k`（1-20，可选字符串），`version`（可选字符串），`custom_tags`（字符串列表），`filters`（对象） | 在收集内进行语义搜索。 |
| `get_topic_{slug}(topic)` | `topic`（必填字符串） | 从收集中检索特定主题的信息。 |
| `list_versions_{slug}()` | 无 | 列出该收集的所有可用文档版本。 |

### MCP资源

| URI | 描述 |
|-----|-------------|
| `ragora://collections` | 列出所有可访问的收集，包括元数据和可用操作。 |

### MCP提示

| 提示 | 参数 | 描述 |
|--------|-----------|-------------|
| `search_collection_prompt` | `collection_name`, `query` | 用于搜索特定收集的预构建提示。 |
| `summarize_collection` | `collection_name` | 用于总结整个收集的预构建提示。 |
| `compare_sources` | `collection_names`, `question` | 用于比较多个收集信息的预构建提示。 |

---

## REST API参考

当MCP工具绑定不可用，或者您需要直接通过HTTP进行控制时，请使用这些端点。

**所有端点都需要**：`Authorization: Bearer <RAGORA_API_KEY>`

### 健康检查

```
GET https://api.ragora.app/v1/health
```

如果服务正常运行，响应将为`200 OK`，并包含`{"status": "ok"`。

### 列出收集信息

```
GET https://api.ragora.app/v1/collections
```

返回认证用户可访问的所有收集信息。

响应：

```json
{
  "collections": [
    {
      "name": "Employee Handbook",
      "slug": "employee_handbook",
      "description": "Company policies, benefits, and procedures",
      "stats": {
        "document_count": 45,
        "chunk_count": 1230,
        "last_updated": "2025-11-15T08:30:00Z"
      },
      "supported_features": ["search", "get_topic", "versions", "filters"]
    }
  ]
}
```

### 在所有收集中搜索

```
POST https://api.ragora.app/v1/search
```

请求：

```json
{
  "query": "vacation policy for remote employees",
  "top_k": 5
}
```

响应：

```json
{
  "results": [
    {
      "content": "Remote employees are entitled to 20 days of paid vacation per year...",
      "score": 0.94,
      "source": {
        "collection": "employee_handbook",
        "document": "benefits-guide.md",
        "chunk_id": "ch_abc123"
      },
      "metadata": {}
    }
  ],
  "usage": {
    "cost_usd": 0.0,
    "balance_remaining_usd": 99.95
  }
}
```

### 搜索特定收集

```
POST https://api.ragora.app/v1/collections/{slug}/search
```

请求：

```json
{
  "query": "log retention duration and deletion policy",
  "top_k": 5,
  "version": "2.0",
  "custom_tags": ["compliance", "soc2"],
  "filters": {
    "region": "US"
  }
}
```

响应：与全局搜索的结构相同，但仅限于指定的收集。

### 从收集中获取主题

```
POST https://api.ragora.app/v1/collections/{slug}/topic
```

请求：

```json
{
  "topic": "remote work policy"
}
```

响应：

```json
{
  "content": "Detailed information about the remote work policy...",
  "source": {
    "collection": "employee_handbook",
    "document": "remote-work.md"
  },
  "usage": {
    "cost_usd": 0.0,
    "balance_remaining_usd": 99.95
  }
}
```

### 列出收集的版本

```
GET https://api.ragora.app/v1/collections/{slug}/versions
```

响应：

```json
{
  "versions": [
    {"version": "2.0", "label": "v2.0 (latest)", "is_default": true},
    {"version": "1.5", "label": "v1.5", "is_default": false},
    {"version": "1.0", "label": "v1.0 (legacy)", "is_default": false}
  ]
}
```

### 检查余额

```
GET https://api.ragora.app/v1/billing/balance
```

响应：

```json
{
  "credits_remaining": 9950,
  "estimated_usd": 99.50,
  "currency": "USD"
}
```

### MCP网关端点（工具代理）

如果您需要通过REST调用MCP工具（例如，动态工具`search_employee_handbook`）：

**获取清单** — 列出您账户可用的所有MCP工具：

```
GET https://api.ragora.app/v1/mcp/manifest
```

**执行工具** — 通过名称调用任何MCP工具：

```
POST https://api.ragora.app/v1/mcp/execute
```

请求：

```json
{
  "tool": "search_employee_handbook",
  "arguments": {
    "query": "vacation policy",
    "top_k": 5
  }
}
```

响应：

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 5 results:\n\n1. **Vacation Policy** (score: 0.95)\n   Remote employees are entitled to...\n   Source: benefits-guide.md"
    }
  ],
  "usage": {
    "cost_usd": 0.0,
    "balance_remaining_usd": 99.95
  }
}
```

---

## 错误代码与状态处理

### HTTP状态码

| 状态 | 含义 | 代理操作 |
|--------|---------|--------------|
| `200` | 成功 | 正常处理结果。 |
| `400` | 请求错误 — 请求格式错误，缺少必需参数 | 检查请求格式，修复请求后重试。 |
| `401` | 未经授权 — 缺少或无效的API密钥 | 停止操作，请求用户提供有效的`sk_live_`密钥。 |
| `403` | 禁止访问 — 密钥有效但无权限访问该收集 | 告知用户需要在市场购买/订阅该收集。 |
| `404` | 未找到 — 收集slug或端点不存在 | 使用`discover_collections()`或`GET /v1/collections`检查slug。 |
| `422` | 验证错误 — 参数存在但无效（例如，`top_k=50`） | 阅读错误信息，修复参数后重试。 |
| `429` | 超过速率限制 | 等待一段时间后重试（使用指数退避策略）。 |
| `402` | 需要支付费用 — 信用不足 | 调用`check_balance()`，提示用户前往计费页面充值。 |
| `500` | 服务器错误 | 2秒后重试一次。如果问题持续，请告知用户服务暂时不可用。 |
| `503` | 服务不可用 | 5秒后重试一次。如果问题持续，请告知用户。 |

### 错误响应格式

```json
{
  "error": {
    "code": "insufficient_credits",
    "message": "Your balance is too low to complete this search. Current balance: $0.05.",
    "details": {}
  }
}
```

### 常见错误代码及其含义

| 代码 | 描述 | 代理操作 |
|------|-------------|--------------|
| `invalid_api_key` | 密钥格式错误或密钥已被吊销 | 请求用户提供新的密钥。 |
| `expired_api_key` | 密钥已过期 | 请用户在控制台生成新的密钥。 |
| `insufficient_credits` | 信用不足 | 报告余额并链接到计费页面。 |
| `collection_not_found` | slug与任何收集都不匹配 | 重新运行发现操作，检查拼写。 |
| `collection_access_denied` | 用户未购买访问权限 | 链接用户到市场页面。 |
| `rate_limit_exceeded` | 在指定时间内请求过多 | 等待一段时间后重试。 |

### 超限与重试策略

### 限制

- **MCP工具**：每个API密钥每分钟60次请求。
- **REST API**：每个API密钥每分钟120次请求。
- 每个响应都会返回速率限制头部信息：
  - `X-RateLimit-Limit` — 指定时间窗口内的最大请求次数。
  - `X-RateLimit-Remaining` — 当前时间窗口内剩余的请求次数。
  - `X-RateLimit-Reset` — 时间窗口重置的Unix时间戳。

### 重试策略

收到`429`响应时：

1. 如果存在`Retry-After`头部，请按照其指示的延迟时间等待。
2. 如果没有`Retry-After`，使用指数退避策略：等待1秒，然后2秒，然后4秒。
3. 最多尝试3次后放弃并告知用户。
4. 不要重试`401`或`403`错误——这些错误需要用户操作，无需等待。

### 避免速率限制的最佳实践

- 逻辑上批量处理请求：每次任务3-5次针对性查询，而不是连续发送20次快速请求。
- 使用`top_k=10-15`而不是对同一问题发送多次`top_k=3`的请求。
- 在会话期间缓存`discover_collections()`的结果——收集列表在对话过程中很少变化。

---

## 认证故障排除

| 症状 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| 每次请求都出现`401 Unauthorized` | `Authorization`头部缺失或格式错误 | 确保头部格式为`Authorization: Bearer sk_live_xxxxx`。不要在参数周围添加额外的空格或引号。 |
| `401`但密钥看起来正确 | 密钥已被吊销或重新生成 | 请用户在`https://app.ragora.app/settings/api-keys`检查有效的密钥。 |
| `401`且显示`invalid_api_key`代码 | 密钥格式错误（例如，缺少`sk_live_`前缀） | 验证格式：必须以`sk_live_`开头，后跟UUID。 |
| `401`且显示`expired_api_key`代码 | 密钥已过期 | 请在控制台生成新的密钥。 |
| `403 Forbidden` | 密钥有效但无权限访问该收集 | 用户需要购买或订阅该收集。 |
| MCP工具未显示 | MCP服务器未配置或URL错误 | 确认MCP URL是否为`https://mcp.ragora.app/mcp`，并设置正确的头部。 |
| MCP工具显示但返回错误 | MCP配置中的密钥是占位符 | 将`sk_live_xxx`替换为实际的密钥。 |
| `ECONNREFUSED`或超时 | 网络问题或服务中断 | 检查`https://mcp.ragora.app/health`。如果服务中断，切换到REST API或等待。 |

## 核心工作流程

### 1. 理解意图

- 分类请求类型：事实查找、总结、比较、提取或验证。
- 从用户的话语中识别可能的领域/收集。

### 2. 发现范围

- 运行`discover_collections()`（MCP）或`GET /v1/collections`（API）。
- 选择与问题最相关的1-3个收集。
- 如果没有相关的收集，请明确说明并停止操作。

### 3. 检索证据

- **第一轮**：对每个选定的收集进行一次针对性查询。
- **第二轮**：使用具体的子查询（日期、实体、声明、阈值）进行细化。
- 根据任务调整`top_k`：
  - 对于直接的事实性问题，使用`top_k=3-5`。
  - 对于比较或全面总结，使用`top_k=8-12`。
  - 对于彻底的研究或尽职调查，使用`top_k=15-20`。

### 4. 综合证据

- 按声明合并证据，而不是按来源顺序。
- 通过直接引用和内容的最新性来解决冲突。
- 区分事实和推断。

### 5. 回答

- 首先给出简洁的答案。
- 然后提供带有收集/来源引用的证据。
- 在信心不足时，说明存在的空白或需要进一步查询的地方。

## 多步骤工作流程示例

### 在多个收集中研究一个主题

**场景**：用户询问“我们的数据保留政策是什么，它与SOC 2要求有何不同？”

1. `discover_collections()` → 找到`security_handbook`、`compliance_docs`、`soc2_guide`
2. `search_collection("security_handbook", "data retention policy duration", top_k=5)`
3. `search_collection("compliance_docs", "SOC 2 data retention requirements", top_k=5)`
4. `search_collection("soc2_guide", "retention controls audit evidence", top_k=5)`
5. 综合：比较内部政策与SOC 2要求，指出差异。
6. 用每个收集的结果来回答问题。

### 比较两个供应商的合同

**场景**：用户询问“比较供应商A和供应商B的SLA条款。”

1. `discover_collections()` → 找到`vendor_a_contract`、`vendor_b_contract`
2. `search_collection("vendor_a_contract", "SLA uptime guarantees penalties", top_k=8)`
3. `search_collection("vendor_b_contract", "SLA uptime guarantees penalties", top_k=8)`
4. 进一步细化：
   - `search_collection("vendor_a_contract", "termination notice period remedies", top_k=5)`
   - `search_collection("vendor_b_contract", "termination notice period remedies", top_k=5)`
5. 构建比较表：正常运行时间百分比、处罚结构、通知期、排除项。
6. 强调关键差异和风险。

### 深入进行尽职调查

**场景**：用户询问“关于公司X的安全态势，我们了解多少？”

1. `search("Company X security audit penetration test vulnerability", top_k=15)` — 进行广泛的发现。
2. 确定返回的结果收集（例如，`due_diligence_reports`、`vendor_assessments`）。
3. 进行针对性查询：
   - `search_collection("due_diligence_reports", "Company X SOC 2 ISO 27001 certifications", top_k=10)`
   - `search_collection("vendor_assessments", "Company X data encryption access controls", top_k=10)`
   - `search_collection("due_diligence_reports", "Company X incident history breach", top_k=5)`
4. 按类别组织发现结果：认证、技术控制、事件历史。
5. 以信心水平呈现结果，并指出数据缺失的部分。

### 查找版本化的文档

**场景**：用户询问“API v1和v2之间的认证流程发生了哪些变化？”

1. `list_versions_api_docs()` → 返回`["1.0", "2.0"]`
2. `search_api_docs(query="authentication flow token exchange", version="1.0", top_k=5)`
3. `search_api_docs(query="authentication flow token exchange", version="2.0", top_k=5)`
4. 比较结果：哪些内容被添加、更改或删除。
5. 以变更日志的形式呈现清晰的总结。

### REST API工作流程（无MCP）

**场景**：MCP绑定不可用。用户询问“查找我们的休假政策。”

1. 健康检查：
```bash
curl -s https://api.ragora.app/v1/health
```

2. 列出收集信息：
```bash
curl https://api.ragora.app/v1/collections \
  -H "Authorization: Bearer $RAGORA_API_KEY"
```

3. 在相关收集中搜索：
```bash
curl -X POST https://api.ragora.app/v1/collections/employee_handbook/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "vacation policy paid time off", "top_k": 5}'
```

4. 解析`results`数组，提取`content`和`source`字段，然后组成答案。

---

## 查询模式

使用简短、具体的查询。优先使用多次查询，而不是一次性进行复杂的查询。

### 根据任务类型

| 任务 | 查询模式 | 示例 |
|------|--------------|---------|
| 事实查找 | `"<实体> <指标/属性> <时间范围>"` | `"ACME Corp revenue 2024 Q3"` |
| 政策/要求 | `"<政策类型> 资格标准例外"` | `"parental leave eligibility criteria exceptions"` |
| 比较 | 在每个收集中运行相同的查询 | `"pricing limits SLA exclusions"` × 2个收集 |
| 验证 | 先使用`"<声明>"`，然后使用`"<声明>的反例"` | `"all employees get 20 vacation days"`然后`"exceptions to vacation day policy"` |
| 提取 | `"<实体> <具体数据点>"` | `"ACME Corp CEO contact information"` |
| 时间线 | `"<实体> <事件类型> 时间顺序"` | `"product launches timeline 2023 2024"` |

### 查询细化策略

1. **首先广泛搜索**：`"data retention policy"` — 查看有哪些可用信息。
2. **按实体细化**：`"customer data retention policy"` — 将范围缩小到特定领域。
3. **按属性细化**：`"customer data retention duration deletion schedule"` — 获取具体细节。
4. **添加约束**：如果结果混乱，使用`filters`和`custom_tags`。

### 工具使用手册

### 发现收集

MCP：
```text
discover_collections()
```

API：
```bash
curl https://api.ragora.app/v1/collections \
  -H "Authorization: Bearer $RAGORA_API_KEY"
```

### 不确定时进行广泛搜索

MCP：
```text
search(query="SOC 2 retention policy for customer logs", top_k=8)
```

API：
```bash
curl -X POST https://api.ragora.app/v1/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SOC 2 retention policy for customer logs", "top_k": 8}'
```

### 针对性收集搜索

MCP：
```text
search_collection(
  collection_name="security-handbook",
  query="log retention duration and deletion policy",
  top_k=5
)
```

API：
```bash
curl -X POST https://api.ragora.app/v1/collections/security_handbook/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "log retention duration and deletion policy", "top_k": 5}'
```

### 带版本搜索

MCP：
```text
search_api_docs(
  query="authentication flow changes",
  version="2.0",
  top_k=5
)
```

API：
```bash
curl -X POST https://api.ragora.app/v1/collections/api_docs/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication flow changes", "version": "2.0", "top_k": 5}'
```

### 从收集中获取主题

MCP：
```text
get_topic_employee_handbook(topic="remote work policy")
```

API：
```bash
curl -X POST https://api.ragora.app/v1/collections/employee_handbook/topic \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"topic": "remote work policy"}'
```

### 过滤搜索

MCP：
```text
search_collection(
  collection_name="contracts",
  query="termination for convenience notice period",
  top_k=10,
  custom_tags=["msa", "legal"],
  filters={"region": "US"}
)
```

API：
```bash
curl -X POST https://api.ragora.app/v1/collections/contracts/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "termination for convenience notice period", "top_k": 10, "custom_tags": ["msa", "legal"], "filters": {"region": "US"}}'
```

### 检查信用

MCP：
```text
check_balance()
```

API：
```bash
curl https://api.ragora.app/v1/billing/balance \
  -H "Authorization: Bearer $RAGORA_API_KEY"
```

### 在多个收集之间进行比较

MCP提示：
```text
compare_sources(
  collection_names=["vendor-a-docs", "vendor-b-docs"],
  question="What are the SLA differences?"
)
```

API（手动——执行两次搜索并比较）：
```bash
# Search vendor A
curl -X POST https://api.ragora.app/v1/collections/vendor_a_docs/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SLA uptime guarantees penalties", "top_k": 8}'

# Search vendor B
curl -X POST https://api.ragora.app/v1/collections/vendor_b_docs/search \
  -H "Authorization: Bearer $RAGORA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "SLA uptime guarantees penalties", "top_k": 8}'
```

## 上下文管理

### 选择`top_k`

| 场景 | 推荐的`top_k` | 原因 |
|----------|---------------------|-----------|
| 简单的事实性问题 | 3-5 | 少量精确的结果有助于保持上下文简洁。 |
| 多方面问题 | 5-8 | 需要在子主题之间进行覆盖。 |
| 在多个收集之间进行比较 | 每个收集8-12 | 需要从每个方面获取足够的证据。 |
| 彻底的研究/尽职调查 | 15-20 | 全面的覆盖会带来更多的上下文。 |
| 快速验证声明 | 2-3 | 只需要确认或否定。 |

### 管理上下文范围

- **优先使用针对性搜索**。`search_collection()`返回的结果较少，但更相关。
- **边搜索边总结**。在获取结果后，提取关键事实，然后再进行下一次查询。
- **丢弃相关性低的结果**。如果结果的相关性得分低或与问题无关，请忽略它。
- **不要重复获取已知的信息**。如果之前的查询已经回答了部分问题，请不要再次查询。

### 当结果过多时

如果单个查询返回的文本过多：

1. 将`top_k`减少到3。
2. 添加`custom_tags`或`filters`来缩小范围。
3. 使用更具体的查询，而不是广泛的查询。
4. 专注于得分最高的结果，忽略其余的结果。

### 当结果不足时

如果查询没有返回结果或返回的结果无关：

1. 扩展查询范围：删除特定术语，使用同义词。
2. 尝试使用全局`search()`而不是特定于收集的查询。
3. 使用`discover_collections()`检查收集是否存在。
4. 如果有多个收集，请尝试其他收集。
5. 如果仍然没有结果，告诉用户没有找到相关数据。

## 输出格式指南

### 标准响应结构

```
**Answer**: <2-6 sentence direct answer>

**Evidence**:
- <claim> — *<collection_name> / <source_document>*
- <claim> — *<collection_name> / <source_document>*
- <claim> — *<collection_name> / <source_document>*

**Caveats**:
- <what is missing, uncertain, or conflicting>

**Suggested follow-ups** (if applicable):
- <exact query the user could ask next>
```

### 来源引用规则

- 对每个声明，始终引用**收集名称**和**来源文档**。
- 格式：`— *Collection Name / document-name.md*`
- 如果多个结果支持相同的声明，请引用得分最高的那个。
- 如果结果相互矛盾，请引用两个结果并说明矛盾之处。

### 信心指标

- **高信心**：多个结果一致，相关性得分高（>0.85），来自权威收集。
- **中等信心**：单个结果或中等得分（0.6-0.85）。注意：“基于单一来源。”
- **低信心**：得分低（<0.6），结果间接或推断得出。注意：“这是推断出来的，可能需要验证。”

### 比较格式

在比较多个收集时，使用表格：

```
| Aspect | Vendor A | Vendor B |
|--------|----------|----------|
| Uptime SLA | 99.9% | 99.95% |
| Penalty | 5% credit per hour | 10% credit per hour |
| Notice period | 30 days | 60 days |

*Sources: vendor_a_contract/sla.md, vendor_b_contract/sla.md*
```

---

## 失败处理

| 失败情况 | 代理操作 |
|---------|-------------|
| **没有结果** | 扩展查询范围，去除过于具体的约束，使用`search()`重试。如果仍然没有结果，告知用户。 |
| **结果太多且混乱** | 通过收集进行限制，添加`custom_tags`/`filters`，使用更具体的实体/日期术语。 |
| **证据冲突** | 展示双方的观点，说明冲突，引用两个来源，并提出进一步的查询来解决问题。 |
| **访问被拒绝（403）** | 解释可能需要购买访问权限。链接到市场页面。 |
| **信用错误（402）** | 运行`check_balance()`，报告余额，并链接到计费页面。 |
| **速率限制（429）** | 按`Retry-After`头部等待一段时间后重试。最多尝试3次。 |
| **服务器错误（500/503）** | 2-5秒后重试一次。如果问题持续，告知用户服务暂时不可用。 |
| **MCP连接失败** | 切换到REST API端点。告知用户切换原因。 |
| **超时** | 减少`top_k`，简化查询，然后重试。 |
| **无效的收集slug** | 重新运行`discover_collections()`并检查可用的slug。 |

## 质量标准

- 永远不要编造未见过的信息——所有声明都必须基于检索到的证据。
- 始终用检索到的证据和来源引用来支持声明。
- 优先使用精确的表述，避免泛泛而谈。
- 保持最终答案的简洁性，以决策为导向，并提供来源支持。
- 区分直接陈述的事实和推断出的结论。
- 当证据不完整时，明确说明缺失的部分。
- 如果无法从现有收集中回答问题，请直接说明。