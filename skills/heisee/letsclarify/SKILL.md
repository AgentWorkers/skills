---
name: letsclarify
description: 通过网页表单收集结构化的人类输入（如审批意见、决策结果、评审内容、数据等）。创建一个基于 JSON 模式的表单，向用户发送唯一的 URL，然后等待用户的反馈。当你的工作流程需要在继续进行之前获得人类的确认或反馈时，可以使用这种方法。
homepage: https://letsclarify.ai
license: MIT
metadata: {"clawdbot":{"emoji":"📋","primaryEnv":"LETSCLARIFY_API_KEY"}}
---
# 让我们明确一下功能：**Let's Clarify**

**Let's Clarify** 是一种基于“人在循环中”（Human-in-the-Loop）原理的基础设施服务。当您的工作流程需要结构化的人类输入（如审批、决策、数据收集、文档审核）时，可以使用该服务来确保流程的顺利进行。

**基础URL：** `https://letsclarify.ai`

**集成方式：** 该服务提供了MCP服务器（推荐用于兼容MCP的代理）和REST API。详情请参见下方的[MCP服务器](#mcp-server-remote)。

## 快速入门

### 0. 注册（或删除）API密钥

```bash
curl -X POST https://letsclarify.ai/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "email": "agent@example.com"}'
```

**响应（201）：**
```json
{
  "api_key": "lc_...",
  "key_prefix": "lc_xxxxx",
  "warning": "Store securely. Shown only once."
}
```

请安全地存储`api_key`值。该密钥仅显示一次，在后续的所有API调用中需使用`Authorization: Bearer lc_...`进行身份验证。

**错误（422）：** 验证失败（例如，缺少姓名/电子邮件）时返回：
```json
{ "error": "validation_failed", "message": "..." }
```

**删除API密钥：**
```bash
curl -X DELETE https://letsclarify.ai/api/v1/register \
  -H "Authorization: Bearer lc_..."
```

**响应（200）：**
```json
{ "deleted": true }
```

### 1. 创建表单

```bash
curl -X POST https://letsclarify.ai/api/v1/forms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{
    "title": "Approve Budget Increase",
    "context_markdown": "## Q3 Budget\nPlease review the proposed 15% increase.",
    "recipient_count": 3,
    "retention_days": 7,
    "webhook_url": "https://your-agent.example.com/webhook",
    "schema": [
      {
        "id": "decision",
        "type": "radio",
        "label": "Your decision",
        "required": true,
        "options": [
          { "value": "approve", "label": "Approve" },
          { "value": "reject", "label": "Reject" }
        ]
      },
      {
        "id": "notes",
        "type": "textarea",
        "label": "Additional notes",
        "required": false,
        "validation": { "max_length": 1000 }
      }
    ]
  }'
```

**响应（201）：**
```json
{
  "form_token": "xK9m2...",
  "delete_token": "dT3r...",
  "base_url_template": "https://letsclarify.ai/f/xK9m2.../{recipient_uuid}",
  "poll_url": "https://letsclarify.ai/api/v1/forms/xK9m2.../results",
  "summary_url": "https://letsclarify.ai/api/v1/forms/xK9m2.../summary",
  "delete_url": "https://letsclarify.ai/api/v1/forms/xK9m2...",
  "recipients": ["uuid-1", "uuid-2", "uuid-3"]
}
```

`recipient_count` 的取值范围为1到1,000。您可以使用`recipients`端点添加更多接收者（最多可添加10,000个接收者）。

#### 高级功能：客户端提供的UUID和预填充值

您可以传递一个`recipients`数组，其中包含每个接收者的`uuid`和`prefill`值（可选）：

```bash
curl -X POST https://letsclarify.ai/api/v1/forms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{
    "schema": [{"id":"name","type":"text","label":"Name","required":true}],
    "recipients": [
      {"uuid": "550e8400-e29b-41d4-a716-446655440001", "prefill": {"name": "Alice"}},
      {"uuid": "550e8400-e29b-41d4-a716-446655440002", "prefill": {"name": "Bob"}},
      {}
    ],
    "recipient_count": 5
  }'
```

**规则：**
- `uuid`必须为有效的UUID v4格式，并且在全球范围内是唯一的（请求或数据库中存在重复值时会返回400错误）。
- `prefill`必须是一个JSON对象，大小不超过10KB。如果`prefill`中的键与表单的任何字段`id`不匹配，将被忽略。
- `recipient_count`与`recipients`数组结合使用时，数量必须大于或等于数组的长度。多余的接收者将由服务器生成UUID，且不会被预填充。
- 如果`recipient_count`为空且`recipients`数组也为空，会返回400错误。
- 预填充的值会作为表单的默认值显示，用户可以在提交前进行修改。
- 优先级顺序为：会话存储（sessionStorage）> 上次提交的内容 > 预填充的值 > 无默认值。

### 2. 为接收者生成URL

针对每个接收者的`uuid`，生成相应的URL：
```
https://letsclarify.ai/f/{form_token}/{recipient_uuid}
```

您可以通过电子邮件、Slack、WhatsApp或其他渠道将URL发送给接收者。每个接收者的URL都是唯一的。

### 3. 增加接收者

```bash
curl -X POST https://letsclarify.ai/api/v1/forms/{form_token}/recipients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{ "count": 5 }'
```

**响应（201）：**
```json
{ "recipients": ["uuid-4", "uuid-5", "uuid-6", "uuid-7", "uuid-8"] }
```

每次请求最多可添加1,000个接收者，每个表单最多可添加10,000个接收者。

#### 高级功能：客户端提供的UUID和预填充值

与创建表单时使用的`recipients`数组相同：

```bash
curl -X POST https://letsclarify.ai/api/v1/forms/{form_token}/recipients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{
    "recipients": [
      {"uuid": "550e8400-e29b-41d4-a716-446655440003", "prefill": {"name": "Charlie"}},
      {}
    ],
    "count": 5
  }'
```

规则相同：UUID必须唯一，预填充的值需要符合表单的字段格式，且数量必须大于或等于数组的长度。

### 4. 查询汇总信息

```bash
curl https://letsclarify.ai/api/v1/forms/{form_token}/summary \
  -H "Authorization: Bearer lc_..."
```

```json
{
  "expired": false,
  "known_total": 8,
  "submitted_total": 3,
  "pending_total": 5,
  "updated_at_max": "2026-02-13T12:00:00Z"
}
```

### 5. 获取查询结果

```bash
# Basic polling
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?limit=25"

# With status filter
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?status=submitted"

# With cursor pagination
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?cursor=djE6OTA0Mg"

# With file contents (base64)
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?include_files=1"

# Efficient polling (only changes since last check)
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?updated_since=2026-02-13T11:00:00Z"
```

**响应：**
```json
{
  "expired": false,
  "next_cursor": "djE6MTAw" | null,
  "server_time": "2026-02-13T12:00:00Z",
  "results": [
    {
      "recipient_uuid": "uuid-1",
      "status": "submitted",
      "submitted_at": "2026-02-13T11:30:00Z",
      "updated_at": "2026-02-13T11:30:00Z",
      "response_json": { "decision": "approve", "notes": "Looks good" },
      "files": { "expected_file_count": 0 }
    },
    {
      "recipient_uuid": "uuid-2",
      "status": "pending",
      "submitted_at": null,
      "updated_at": "2026-02-13T10:00:00Z",
      "response_json": null
    }
  ]
}
```

**高效的数据查询流程：**
1. **初始同步**：使用游标分页查询数据，直到`next_cursor`为`null`。同时记录`server_time`。
2. **查询更新内容**：使用`updated_since={stored_server_time}`来获取最新的变化。
3. 在获取所有数据后，更新`server_time`。

### 6. 删除表单

```bash
curl -X DELETE https://letsclarify.ai/api/v1/forms/{form_token} \
  -H "Authorization: Bearer lc_..." \
  -H "X-Delete-Token: {delete_token}"
```

```json
{ "deleted": true }
```

表单、所有提交记录以及上传的文件将被永久删除。

### 7. 使用Webhook

如果在创建表单时提供了`webhook_url`，每次提交时都会发送POST请求：

```json
{
  "form_token": "xK9m2...",
  "recipient_uuid": "uuid-1",
  "submitted_at": "2026-02-13T11:30:00Z",
  "response_json": { "decision": "approve", "notes": "Looks good" }
}
```

- Webhook URL必须使用HTTPS协议。
- 超时时间：10秒。
- 重试次数：最多3次，采用指数级退避策略（仅针对5xx错误和网络故障；4xx错误不会被重试）。
- 提交操作是非阻塞的，无论Webhook的状态如何都会成功完成。

### 8. 可嵌入的表单插件

您可以直接将表单嵌入到任何网站中，而无需将用户引导到托管的表单页面（`/f/{form_token}/{recipient_uuid}`）：

```html
<script src="https://letsclarify.ai/embed.js"></script>
<div data-letsclarify-form="{form_token}"
     data-letsclarify-recipient="{recipient_uuid}">
</div>
```

该插件会在页面加载时自动初始化，执行以下操作：
- 从嵌入API获取表单的配置信息。
- 显示所有字段类型（文本、文本区域、单选按钮、下拉菜单、复选框、复选框组、文件上传）。
- 处理客户端的验证、提交和成功提示。
- 支持重新提交（会提醒用户并覆盖之前的响应结果）。
- 自动插入自身的CSS样式表（`/embed.css`），无需额外的样式表。
- 会自动应用在创建表单时设置的`theme_color`。

**可选属性：**
- `data-letsclarify-host="https://your-instance.com"` — 用于自定义托管实例（默认值：根据脚本来源自动检测）

**两种展示表单的方式：**

| 方法 | 使用场景 |
|---|---|
| 托管URL：`https://letsclarify.ai/f/{token}/{uuid}` | 通过电子邮件、Slack等方式发送链接 |
| 嵌入插件：`<div data-letsclarify-form="..." ...>` | 直接嵌入到您的网站、仪表板或应用程序中 |

两种方法都使用相同的后端API，查询结果会显示在相同的查询或Webhook响应中。

## 等待结果（非常重要！）

创建表单并发送URL给接收者后，**必须**设置异步查询来收集结果。不要假设接收者会立即做出响应。请使用以下策略之一：

### 策略A：使用MCP工具的Cron任务（推荐给兼容MCP的代理）

创建一个定期执行的Cron任务，并使用该服务提供的`get_summary`和`get_results`接口来检查状态和获取结果。

```bash
openclaw cron add \
  --name "poll-letsclarify-{form_token}" \
  --every 10m \
  --message "Check Let's Clarify form {form_token}: Use get_summary to \
see if submitted_total == known_total. If all responded, use get_results \
to fetch submissions and summarize the responses, then remove this cron \
job. If expired, fetch what exists and clean up."
```

**一次性检查（延迟后执行一次）：**

```bash
openclaw cron add \
  --name "check-letsclarify-{form_token}" \
  --at +1h \
  --delete-after-run \
  --message "Check Let's Clarify form {form_token} results. If responses \
exist, fetch and summarize them. Report status either way."
```

### 策略B：基于意图的Cron任务（适用于不使用MCP的代理）

如果无法使用MCP工具，可以使用基于意图的消息机制。代理可以通过上述API参考信息来访问相应的端点。

```bash
openclaw cron add \
  --name "poll-letsclarify-{form_token}" \
  --every 10m \
  --message "Check if all recipients of Let's Clarify form {form_token} \
have responded. If yes, fetch and summarize all submitted results, then \
remove this cron job. If the form has expired, fetch whatever results \
exist and clean up."
```

### 策略C：使用Webhook（如果您有HTTPS端点）

在创建表单时提供`webhook_url`。每次提交时，**Let's Clarify**都会向该URL发送POST请求。请确保您控制的端点支持Webhook请求。

### 数据查询流程：

1. **创建表单** → 保存`form_token`和`api_key`。
2. **通过Telegram、电子邮件等方式将URL发送给接收者**。
3. **设置查询任务**：创建一个Cron任务，每隔5-15分钟检查一次汇总信息。
4. **查询时**：比较`submitted_total`和`known_total`：
   - 如果所有接收者都已响应 → 获取全部结果并采取相应操作，然后删除Cron任务。
   - 如果不是所有接收者都响应 → 什么都不做，等待下一次查询。
   - 如果表单已过期 → 获取现有结果，然后删除Cron任务。
5. **清理**：完成后删除表单（可选，表单会在`retention_days`后自动过期）。

## 表单字段类型及配置

**支持的字段类型：**

| 类型 | 描述 | 是否需要配置选项 |
|---|---|---|
| `text` | 单行文本输入 | 否 |
| `textarea` | 多行文本输入 | 否 |
| `checkbox` | 单个复选框 | 否 |
| `checkbox_group` | 多个复选框 | 是 |
| `radio` | 单选按钮组 | 是 |
| `select` | 下拉菜单 | 是 |
| `file` | 文件上传 | 否 |

**可选的验证规则：**
- `min_length` / `max_length` — 用于文本/文本区域字段 |
- `pattern` — 用于文本/文本区域字段的正则表达式验证 |
- `min_items` / `max_items` — 用于复选框组字段

**文件上传配置（仅适用于`file`类型）：**
- `accept` — 可接受的MIME类型或文件扩展名（例如`["image/*", ".pdf"]`） |
- `max_size_mb` — 文件最大大小（1-10MB） |
- `max_files` — 最大文件数量（1-10个）

## MCP服务器（远程）

**Let's Clarify**提供了远程的MCP（Model Context Protocol）端点，方便AI代理直接集成。兼容MCP的客户端（如Claude Code、Cursor等）可以直接将**Let's Clarify**作为原生工具使用。

**端点：** `https://letsclarify.ai/mcp`

**配置方法：**

将以下配置添加到您的MCP客户端配置中：

```json
{
  "mcpServers": {
    "letsclarify": {
      "url": "https://letsclarify.ai/mcp",
      "headers": {
        "Authorization": "Bearer lc_..."
      }
    }
  }
}
```

对于未授权的访问（仅用于注册工具），请省略`headers`字段。

### 可用的工具

| 工具 | 是否需要认证 | 功能描述 |
|---|---|---|
| `register` | 否 | 注册新的API密钥 |
| `create_form` | 是 | 创建表单并获取URL和token |
| `add_recipients` | 是 | 为现有表单添加接收者信息 |
| `get_summary` | 是 | 快速检查表单状态（总数、已提交数量、待处理数量） |
| `get_results` | 是 | 获取带有分页和过滤功能的提交记录 |
| `delete_form` | 是 | 永久删除表单及其所有数据 |

## MCP速率限制

| 端点 | 限制次数 | 时间窗口 |
|---|---|---|
| POST /mcp（每个IP） | 60次 | 1分钟 |
| POST /mcp（每个API密钥） | 60次 | 1分钟 |

## 速率限制与重试策略

| 端点 | 限制次数 | 时间窗口 |
|---|---|---|
| POST /api/v1/register | 3次 | 1小时 |
| POST /api/v1/forms | 10次 | 1分钟 |
| 所有API端点 | 60次 | 1分钟 |
| GET /api/v1/embed/:token/:uuid | 30次 | 1分钟 |
| POST /api/v1/embed/:token/:uuid | 20次 | 1分钟 |

**当遇到速率限制（HTTP 429错误）时：**
1. 读取`Retry-After`头部字段中的延迟时间（以秒为单位）。
2. 等待指定时间后再进行重试。
3. 采用指数级退避策略进行重试：`wait = Retry-After * 2^attempt`。
4. 最多尝试5次后失败。

## 数据保留策略

- 默认保留时间为30天。
- 最长保留时间为365天。
- 过期的表单在API响应中会标记为`expired: true`。
- 所有数据在过期后会被永久删除。
- 可通过删除端点立即清理数据。