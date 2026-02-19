---
name: letsclarify
description: 通过网页表单收集结构化的人类输入（如审批意见、决策结果、评审内容、数据等）。创建一个基于 JSON 模式的表单，向用户发送唯一的 URL，然后收集他们的反馈结果。当你的工作流程需要在继续进行之前获得人类的确认或审批时，可以使用这种方法。
homepage: https://letsclarify.ai
license: MIT
metadata: {"openclaw":{"emoji":"📋","primaryEnv":"LETSCLARIFY_API_KEY"}}
---
# 让我们明确一下“Let’s Clarify”的功能

“Let’s Clarify”是一款基于“人在回路”（Human-in-the-Loop）原理的基础设施服务。当您的工作流程需要结构化的人类输入（如审批、决策、数据收集、文档审核）时，可以使用该服务来确保流程的顺利进行。

**基础URL：** `https://letsclarify.ai`

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

请妥善保管`api_key`，因为它只会显示一次。在后续的所有API调用中，需要将`api_key`作为`Authorization: Bearer lc_...`包含在请求头中。

**错误（422）：** 验证失败（例如，缺少姓名/电子邮件信息）时返回：
```json
{ "error": "validation_failed", "message": "..." }
```

**删除您的API密钥：**
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

`recipient_count`的取值范围是1到1,000。您可以使用`recipient`端点来添加更多接收者（最多可添加10,000个接收者）。

### 2. 为接收者生成URL

对于每个接收者的UUID，生成相应的URL：
```
https://letsclarify.ai/f/{form_token}/{recipient_uuid}
```

您可以通过电子邮件、Slack、WhatsApp或其他渠道将这些URL发送给接收者。每个接收者的URL都是唯一的。

### 3. 增加接收者数量

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

每次请求最多允许添加1,000个接收者，每个表单最多支持10,000个接收者。

### 4. 获取汇总数据

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

### 5. 查看投票结果

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

**高效的投票流程：**
1. **初始同步：** 使用分页机制获取数据，直到`next_cursor`为`null`。同时记录`server_time`。
2. **轮询：** 使用`updated_since={stored_server_time}`来仅获取更新过的信息。
3. 在获取完所有数据后，更新`server_time`。

### 6. 删除表单

```bash
curl -X DELETE https://letsclarify.ai/api/v1/forms/{form_token} \
  -H "Authorization: Bearer lc_..." \
  -H "X-Delete-Token: {delete_token}"
```

```json
{ "deleted": true }
```

表单、所有提交内容以及上传的文件将被永久删除。

### 7. 使用Webhook

如果在创建表单时提供了`webhook_url`，每次提交时都会向该URL发送POST请求：

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
- 重试策略：对于5xx错误和网络故障，最多尝试3次（4xx错误不会被重试）。
- 非阻塞式处理：无论Webhook的状态如何，提交操作都会成功完成。

### 8. 可嵌入的表单组件

您可以直接将表单嵌入到任何网站中，而无需将用户引导至托管的表单页面（`/f/{form_token}/{recipient_uuid}`）：

```html
<script src="https://letsclarify.ai/embed.js"></script>
<div data-letsclarify-form="{form_token}"
     data-letsclarify-recipient="{recipient_uuid}">
</div>
```

该组件会在页面加载时自动初始化，执行以下操作：
- 从嵌入API获取表单结构。
- 显示所有字段类型（文本、文本区域、单选按钮、下拉菜单、复选框、复选框组、文件上传）。
- 处理客户端端的验证、提交以及成功提示。
- 支持重新提交（会向用户发出警告，并覆盖之前的响应结果）。
- 自动插入自定义CSS样式（`/embed.css`），无需额外添加样式表。
- 会使用表单创建时设置的`theme_color`。

**可选属性：**
- `data-letsclarify-host="https://your-instance.com"` — 用于自定义托管环境（默认值：由脚本自动检测）。

**向用户展示表单的两种方式：**

| 方法 | 适用场景 |
|---|---|
| 托管URL：`https://letsclarify.ai/f/{token}/{uuid}` | 通过电子邮件、Slack等方式发送链接 |
| 嵌入组件：`<div data-letsclarify-form="..." ...>` | 直接嵌入到您的网站、仪表板或应用程序中 |

这两种方式都使用相同的后端API，因此结果会显示在相同的投票或Webhook接口中。

## 等待结果（非常重要！）

创建表单并发送URL给接收者后，**必须**设置异步轮询机制来收集结果。请不要假设接收者会立即做出响应。可以使用以下策略之一：

### 策略A：Cron轮询（推荐）

创建一个定时任务（Cron Job），定期轮询汇总数据端点。当所有接收者的响应都收集完毕或表单过期后，处理结果并停止定时任务。

```bash
# Create a cron job that polls every 10 minutes
openclaw cron add \
  --name "poll-letsclarify-{form_token}" \
  --every 10m \
  --message "Poll Let's Clarify form {form_token}: run curl -H 'Authorization: Bearer {api_key}' 'https://letsclarify.ai/api/v1/forms/{form_token}/summary'. If submitted_total equals known_total (all responded), fetch full results with curl -H 'Authorization: Bearer {api_key}' 'https://letsclarify.ai/api/v1/forms/{form_token}/results?status=submitted', process them, then delete this cron job with openclaw cron rm {job_id}. If not all responded yet, do nothing and wait for the next poll."

# Or: one-shot check after a delay
openclaw cron add \
  --name "check-letsclarify-{form_token}" \
  --at +1h \
  --delete-after-run \
  --message "Check Let's Clarify form {form_token} results: ..."
```

### 策略B：使用Webhook（如果您有HTTPS端点）

在创建表单时提供`webhook_url`。每当有新的提交时，“Let’s Clarify”会向该URL发送POST请求。仅当您能够控制一个可以接收Webhook请求的HTTPS端点时，才使用此方法。

### 轮询流程：
1. **创建表单** → 保存`form_token`和`api_key`。
2. **通过Telegram、电子邮件等方式将表单URL发送给接收者**。
3. **创建定时任务**，每隔5-15分钟轮询一次汇总数据。
4. **在轮询时**：比较`submitted_total`和`known_total`：
   - 如果所有接收者都已响应 → 获取完整结果并处理后停止定时任务。
   - 如果还有未响应的接收者 → 继续等待下一次轮询。
   - 如果表单已过期 → 获取现有结果并停止定时任务。
5. **清理**：完成后删除表单（可选，表单会在`retention_days`后自动过期）。

## 表单字段类型

**支持的字段类型：**

| 类型 | 描述 | 是否需要选项 |
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
- `pattern` — 用于文本/文本区域字段的正则表达式 |
- `min_items` / `max_items` — 用于复选框组字段

**文件配置（仅适用于`file`类型）：**
- `accept` — 文件格式或扩展名数组（例如：`["image/*", ".pdf"]`）
- `max_size_mb` — 文件最大大小（以MB为单位） |
- `max_files` — 最大文件数量 |

## MCP服务器（远程接口）

“Let’s Clarify”提供了一个远程的MCP（Model Context Protocol）接口，支持与AI代理的直接集成。使用MCP兼容的客户端（如Claude Code、Cursor等）可以直接将“Let’s Clarify”作为原生工具使用。

**接口地址：** `https://letsclarify.ai/mcp`

### 配置方法

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

如果不需要身份验证（仅用于注册工具），可以省略`headers`字段。

### 可用的工具

| 工具 | 是否需要认证 | 功能描述 |
|---|---|---|
| `register` | 否 | 注册新的API密钥 |
| `create_form` | 是 | 创建表单并获取相应的URL和token |
| `add_recipients` | 是 | 为现有表单添加接收者 |
| `get_summary` | 是 | 快速查看状态（总数、已提交数量、待处理数量） |
| `get_results` | 是 | 获取提交的数据（支持分页和过滤） |
| `delete_form` | 是 | 永久删除表单及其所有数据 |

## MCP速率限制

| 接口 | 限制次数 | 时间窗口 |
|---|---|---|
| POST /mcp（每个IP） | 60次/分钟 | 1分钟 |
| POST /mcp（每个API密钥） | 60次/分钟 | 1分钟 |

## 速率限制与重试策略

| 接口 | 限制次数 | 时间窗口 |
|---|---|---|
| POST /api/v1/register | 3次/分钟 | 1小时 |
| POST /api/v1/forms | 10次/分钟 | 1分钟 |
| 所有API接口 | 60次/分钟 | 1分钟 |
| GET /api/v1/embed/:token/:uuid | 30次/分钟 | 1分钟 |
| POST /api/v1/embed/:token/:uuid | 20次/分钟 | 1分钟 |

**当遇到速率限制（HTTP 429错误）时：**
1. 读取`Retry-After`头部字段中的延迟时间（以秒为单位）。
2. 等待指定时间后重新尝试。
3. 采用指数级重试策略：`wait = Retry-After * 2^attempt`。
4. 最多尝试5次后失败。

## 数据保留策略

- 默认保留时间为30天。
- 最长保留时间为365天。
- 过期的表单在API响应中会标记为`expired: true`。
- 所有数据在过期后会被永久删除。
- 可通过删除接口立即清理数据。