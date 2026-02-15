---
name: cold-email
description: 使用人工智能生成高度个性化的冷邮件序列，将潜在客户数据转化为转化率高的营销活动。
metadata:
  clawdbot:
    requires:
      env:
        - MACHFIVE_API_KEY
---

# MachFive - 人工智能冷邮件生成工具

MachFive能够根据潜在客户的数据生成个性化的冷邮件序列。它利用人工智能来研究潜在客户，并定制独特且相关的邮件内容，而非使用模板。

## 设置

1. 在 [https://app.machfive.io/settings](https://app.machfive.io/settings) 获取您的 API 密钥（点击 “Integrations” → “API Keys”）。
2. 将 `MACHFIVE_API_KEY` 设置在您的环境变量中。

## 活动 ID

每个生成请求都需要在 URL 中包含一个 **活动 ID**：`/api/v1/campaigns/{campaign_id}/generate`（或 `/generate-batch`）。

- **如果用户未提供活动名称或 ID：** 先调用 `GET /api/v1/campaigns`（见下文）来查看他们工作空间中的所有活动，然后让他们通过名称或 ID 选择一个活动再执行生成操作。
- **如何手动获取活动 ID：** 访问 [https://app.machfive.io/campaigns](https://app.machfive.io/campaigns)，打开一个活动，然后从 URL 或设置中复制 ID。
- **无默认值：** 该工具不假设存在活动。用户（或代理）必须提供一个活动 ID。如果用户提供了活动 ID，代理可以为工作空间设置一个默认活动 ID（例如：“使用活动 X 进行我的请求”）。

## 端点

### 列出活动（在生成前查询）

列出工作空间中的所有活动，以便在用户未提供活动名称或 ID 时询问他们使用哪个活动。
```
GET https://app.machfive.io/api/v1/campaigns
Authorization: Bearer {MACHFIVE_API_KEY}
```
或者使用 `X-API-Key: {MACHFIVE_API_KEY}` 作为请求头。

可选查询参数：`?q=search` 或 `?name=search` 以按活动名称进行筛选。

**响应（200）：**
```json
{
  "campaigns": [
    { "id": "cb1bbb14-e576-4d8f-a8f3-6fa929076fd8", "name": "SaaS Q1 Outreach", "created_at": "2025-01-15T12:00:00Z" },
    { "id": "a1b2c3d4-...", "name": "Enterprise Leads", "created_at": "2025-01-10T08:00:00Z" }
  ]
}
```
如果未提供活动名称或 ID，请先调用此接口，然后询问用户：“我应该使用哪个活动？[列出所有活动名称/ID]。”

### 单个潜在客户（同步生成）

为单个潜在客户生成一封或多封邮件（每名潜在客户最多 3-5 封邮件）。系统会等待生成完成并直接返回邮件序列。**生成过程可能需要 3-5 分钟**（包括人工智能研究和邮件生成时间）；请设置客户端超时时间为至少 **300 秒（5 分钟）** 或 **600 秒（10 分钟）**。如果设置超时时间过短，响应可能会被中断。
```
POST https://app.machfive.io/api/v1/campaigns/{campaign_id}/generate
Authorization: Bearer {MACHFIVE_API_KEY}
Content-Type: application/json
```

或者使用 `X-API-Key: {MACHFIVE_API_KEY}` 作为请求头。
```json
{
  "lead": {
    "name": "John Smith",
    "title": "VP of Marketing",
    "company": "Acme Corp",
    "email": "john@acme.com",
    "company_website": "https://acme.com",
    "linkedin_url": "https://linkedin.com/in/johnsmith"
  },
  "options": {
    "list_name": "Q1 Outreach",
    "email_count": 3,
    "email_signature": "Best,\nYour Name",
    "approved_ctas": ["Direct Meeting CTA", "Lead Magnet CTA"]
  }
}
```

**响应（200）：**
```json
{
  "lead_id": "lead_xyz789",
  "list_id": "uuid",
  "sequence": [
    { "step": 1, "subject": "...", "body": "..." },
    { "step": 2, "subject": "...", "body": "..." },
    { "step": 3, "subject": "...", "body": "..." }
  ],
  "credits_remaining": 94
}
```

**恢复机制：** 响应中包含 `list_id`。如果请求超时或响应被截断，您仍可以通过调用 `GET /api/v1/lists/{list_id}` 来确认状态，然后通过 `GET /api/v1/lists/{list_id}/export?format=json` 来获取邮件序列。

### 批量处理（异步）

为多个潜在客户生成邮件序列（每个潜在客户对应一个序列）。系统会立即返回处理结果（状态码 202），同时返回 `list_id`；实际处理过程在后台进行。要获取结果，请轮询活动状态，然后调用 `export` 接口。
```
POST https://app.machfive.io/api/v1/campaigns/{campaign_id}/generate-batch
Authorization: Bearer {MACHFIVE_API_KEY}
Content-Type: application/json
```

或者使用 `X-API-Key: {MACHFIVE_API_KEY}` 作为请求头。
```json
{
  "leads": [
    { "name": "John Smith", "email": "john@acme.com", "company": "Acme Corp", "title": "VP Marketing" },
    { "name": "Jane Doe", "email": "jane@beta.com", "company": "Beta Inc", "title": "Director Sales" }
  ],
  "options": {
    "list_name": "Q1 Outreach Batch",
    "email_count": 3
  }
}
```

**响应（202）：**
```json
{
  "list_id": "uuid",
  "status": "processing",
  "leads_count": 2,
  "message": "Batch accepted. Poll list status or open in UI."
}
```

### 列出潜在客户列表

列出工作空间中的所有潜在客户列表。可选查询参数：`campaign_id`、`status`（`pending` | `processing` | `completed` | `failed`）、`limit`（默认 50，最大 100）、`offset`。
```
GET https://app.machfive.io/api/v1/lists
GET https://app.machfive.io/api/v1/lists?campaign_id={campaign_id}&status=completed&limit=20
Authorization: Bearer {MACHFIVE_API_KEY}
```

**响应（200）：** `{ "lists": [ { "id", "campaign_id", "custom_name", "processing_status", "created_at", "completed_at" }, ... ] }`。列表按 `created_at` 降序排列。

### 查询活动状态

持续轮询活动状态，直到所有邮件生成完成。请使用在 `generate` 或 `generate-batch` 接口中获得的 `list_id`。
```
GET https://app.machfive.io/api/v1/lists/{list_id}
Authorization: Bearer {MACHFIVE_API_KEY}
```

**响应（200）：** `id`、`campaign_id`、`custom_name`、`processing_status`（`pending` | `processing` | `completed` | `failed`）、`created_at`、`updated_at`。当 `processing_status` 为 `completed` 时，还会返回 `leads_count`、`emails_created`、`completed_at`；如果失败，则返回 `failed_at`。如果列表不存在或不在工作空间中，返回 **404**。

每 10-30 秒轮询一次，直到 `processing_status` 变为 `completed` 或 `failed`。如果失败，请重新提交请求以尝试生成新的邮件序列。

### 导出结果

在所有邮件生成完成后，可以获取处理后的结果。支持 **CSV**（默认格式）或 **JSON** 格式。
- **format=csv**（默认）：返回处理后的 CSV 文件（与 UI 下载内容相同），格式为 `Content-Disposition: attachment; filename="MachFive-{list_id}.csv"`。
- **format=json**：返回以下格式的数据：`{ "leads": [ { "email": "...", "sequence": [ { "step": 1, "subject": "...", "body": "..." }, ... ] }, ... ] }`。每个潜在客户的记录可能包含可选字段 `name`、`company`、`title`（例如：`{ "email": "john@acme.com", "name": "John Smith", "company": "Acme Corp", "title": "VP Marketing", "sequence": [ ... ] }`）。
- 如果列表尚未生成完成，会返回 **409**；如果列表不存在或不在工作空间中，会返回 **404**。

**批量处理流程：** 先发送 `POST /generate-batch` 请求（状态码 202），然后获取 `list_id`，接着轮询 `GET /lists/:id` 直到 `processing_status` 变为 `completed`，最后调用 `GET /lists/:id/export?format=csv` 或 `json` 来获取结果并返回给用户。

## 潜在客户字段

每个潜在客户记录必须包含一个有效的 **`email` 字段**；该字段用于在处理过程中识别潜在客户，并在生成的邮件中将其与原始记录关联起来（与应用程序 UI 中的显示方式一致）。其他字段均为可选，但有助于提高邮件的个性化程度。

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `email` | 是 | 潜在客户的电子邮件地址，用于处理过程和结果导出 |
| `name` | 否 | 完整姓名或名字，有助于提高个性化程度 |
| `company` | 否 | 公司名称，有助于提高个性化程度 |
| `title` | 否 | 职位名称，有助于提高个性化程度 |
| `company_website` | 否 | 公司网站地址，用于进一步研究潜在客户信息 |
| `linkedin_url` | 否 | 潜在客户的 LinkedIn 资料，用于更精确的个性化处理 |

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `list_name` | string | 自动生成 | 用于在 MachFive UI 中显示该列表的名称 |
| `email_count` | number | 3 | 每个潜在客户发送的邮件数量（1-5 封） |
| `email_signature` | string | 无 | 附加到邮件末尾的签名 |
| `campaign_angle` | string | 无 | 用于个性化处理的上下文信息 |
| `approved_ctas` | array | 来自活动的营销宣传材料（可选）；省略则使用活动的默认内容 |

## 限制

- **单个潜在客户（同步生成）：** 请求可能需要 5-10 分钟；请设置客户端超时时间为至少 300 秒（5 分钟）或 600 秒（10 分钟）。
- **批量处理（异步）：** 系统会立即返回处理结果（状态码 202），然后每 10-30 秒轮询一次 `GET /api/v1/lists/{list_id}`，直到 `processing_status` 变为 `completed` 或 `failed`。工作空间有并发处理批次的数量限制；如果收到 **429** 错误，请稍后重试。
- **列出潜在客户列表：** 查询参数 `limit` 的默认值为 50，最大值为 100；`offset` 用于分页。

## 错误代码及说明

| 代码 | 错误类型 | 说明 |
|------|-------|-------------|
| 400 | BAD_REQUEST | JSON 格式错误；缺少 `lead`/`leads` 字段，或潜在客户的 `email` 无效；或者活动没有相关数据存储 |
| 401 | UNAUTHORIZED | API 密钥无效或未提供 |
| 402 | INSUFFICIENT_CREDITS | 信用额度不足 |
| 403 | FORBIDDEN | 该活动不在您的工作空间内 |
| 404 | NOT_FOUND | 活动或列表不存在 |
| 409 | NOT_READY | 在列表生成完成前尝试导出（请先调用 `GET /lists/:id` 查询状态） |
| 429 | WORKSPACE_LIMIT | 并发处理批次数量超过限制；请稍后重试 |

## 使用示例

- “为 Stripe 公司的销售副总裁生成一封冷邮件”
- “为这 10 名潜在客户创建邮件序列”
- “为 SaaS 公司的市场总监生成 3 封邮件的邮件序列”

## 定价方案

- 免费版：每月 100 个信用额度 |
- 入门版：每月 2,000 个信用额度 |
- 成长版：每月 5,000 个信用额度 |
- 企业版：根据需求定制信用额度 |
- 每个信用额度对应处理 1 名潜在客户

立即开始使用：[https://machfive.io](https://machfive.io)