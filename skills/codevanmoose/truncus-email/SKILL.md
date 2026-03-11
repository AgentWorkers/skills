---
name: truncus-email
description: "通过 Truncus API 发送事务性电子邮件（警报、报告、收据、通知）。当工作流程需要向收件人发送电子邮件时，请使用此功能。"
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TRUNCUS_API_KEY
    primaryEnv: TRUNCUS_API_KEY
    homepage: https://github.com/codevanmoose/truncus-openclaw-skill
    emoji: "📧"
---
# Truncus Email

Truncus 是一个用于发送警报、报告、收据和通知的交易型电子邮件 API。它基于欧盟本土的基础设施（AWS SES eu-west-1）运行，确保邮件能够被可靠地送达，并提供幂等性保障以及完整的事件追踪功能。

## 使用场景

当工作流程需要发送电子邮件时，可以使用 Truncus，例如：系统警报、生成的报告、订单收据、密码重置通知、入职流程通知，或任何需要程序化发送电子邮件的场景。

## 认证

Truncus 使用承载令牌（Bearer token）进行认证。API 密钥从 `TRUNCUS_API_KEY` 环境变量中获取。

**请求头格式：**

```
Authorization: Bearer <TRUNCUS_API_KEY>
```

API 密钥以 `tr_live_` 为前缀，后跟 64 个十六进制字符。如果密钥缺失、格式错误或已被吊销，API 会返回 HTTP 401 错误（错误代码包括 `MISSING_API_KEY`、`INVALID_API_KEY` 或 `API_KEY_REVOKED`）。

## 发送端点

```
POST https://truncus.co/api/v1/emails/send
```

### 必需的请求头

| 请求头            | 值                          | 是否必需 |
|-------------------|--------------------------------|----------|
| `Authorization`   | `Bearer <TRUNCUS_API_KEY>`     | 是      |
| `Idempotency-Key` | 每次发送尝试的唯一字符串             | 是      |
| `Content-Type`    | `application/json`             | 是      |

`Idempotency-Key` 请求头是 **必需的**。如果没有提供该头，API 会返回 HTTP 400 错误（错误代码为 `MISSING_IDEMPOTENCY_KEY`）。如果提交重复的密钥，API 会返回原始邮件而不会重新发送（状态码为 `duplicate`）。

### 必需的请求体字段

| 字段     | 类型   | 描述                                       |
|-----------|--------|---------------------------------------------------|
| `to`      | 字符串 | 收件人电子邮件地址（单个地址）           |
| `from`    | 字符串 | 发件人地址（必须是经过验证的域名）         |
| `subject` | 字符串 | 电子邮件主题行（不能为空）                     |

邮件正文必须包含 `html`、`react` 或 `template_id` 中至少其中一个字段。

| 字段         | 类型   | 描述                            |
|---------------|--------|----------------------------------------|
| `html`        | 字符串 | HTML 正文（最大 256KB）                  |
| `react`       | 字符串 | React 电子邮件 JSX 模板（最大 64KB）    |
| `template_id` | 字符串 | 服务器端模板 ID                |

### 可选的请求体字段

| 字段          | 类型              | 描述                                         |
|----------------|-------------------|-----------------------------------------------------|
| `text`         | 字符串            | 纯文本备用内容（最大 128KB）                      |
| `cc`           | 字符串[]          | 抄送收件人                                        |
| `bcc`          | 字符串[]          | 密送收件人                                       |
| `variables`    | 对象            | 模板变量替换（使用 Handlebars 格式）                    |
| `metadata`     | 对象            | 与电子邮件一起存储的任意键值对元数据           |
| `tenant_id`    | 字符串            | 多租户隔离标识符                    |
| `attachments`  | Attachment[]      | 最多 10 个附件，总大小不超过 10MB                 |
| `send_at`      | 字符串 (ISO 8601) | 安排在未来某个时间发送                         |
| `track_opens`  | 布尔值           | 启用打开跟踪像素（默认：`true`）         |
| `track_clicks` | 布尔值           | 启用点击跟踪（默认：`true`）                     |

**附件对象：**

```json
{
  "filename": "report.pdf",
  "content": "<base64-encoded-content>",
  "content_type": "application/pdf"
}
```

### 请求示例

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "from": "notifications@yourapp.com",
    "subject": "Your weekly report is ready",
    "html": "<h1>Weekly Report</h1><p>All systems operational.</p>",
    "text": "Weekly Report\n\nAll systems operational.",
    "metadata": { "report_type": "weekly", "user_id": "usr_123" }
  }'
```

## 响应处理

### 成功（HTTP 200）

```json
{
  "status": "sent",
  "message_id": "cuid-string",
  "provider_message_id": "ses-message-id",
  "warnings": []
}
```

### 预定发送（HTTP 200）

当提供了 `send_at` 时：

```json
{
  "status": "scheduled",
  "message_id": "cuid-string",
  "send_at": "2026-03-15T10:00:00.000Z"
}
```

### 重复请求（HTTP 200）

当使用相同的 `Idempotency-Key` 时：

```json
{
  "status": "duplicate",
  "message_id": "cuid-string",
  "email_status": "sent",
  "created_at": "2026-03-11T14:30:00.000Z"
}
```

### 队列中等待重试（HTTP 200）

在遇到临时性的服务提供商错误时：

```json
{
  "status": "queued",
  "message_id": "cuid-string",
  "retry_scheduled": true,
  "retry_at": "2026-03-11T14:30:30.000Z"
}
```

### 验证错误（HTTP 400）

```json
{
  "error": "to: Invalid email",
  "code": "INVALID_REQUEST"
}
```

### 域名错误（HTTP 400）

```json
{
  "status": "blocked",
  "reason": "Sending domain not found or not configured for this project",
  "code": "DOMAIN_NOT_FOUND"
}
```

### 邮件被屏蔽（HTTP 200）

如果收件人被添加到屏蔽列表中：

```json
{
  "status": "blocked",
  "reason": "All recipients are suppressed",
  "code": "ALL_RECIPIENTS_SUPPRESSED",
  "message_id": "cuid-string",
  "suppressed_addresses": ["bounced@example.com"]
}
```

### 服务提供商故障（HTTP 502）

```json
{
  "status": "failed",
  "message_id": "cuid-string",
  "error": "SES error message",
  "code": "PROVIDER_ERROR"
}
```

### 认证错误（HTTP 401）

```json
{
  "error": "Missing Authorization header",
  "code": "MISSING_API_KEY"
}
```

### 权限错误（HTTP 403）

```json
{
  "error": "Missing required scope: send",
  "code": "SCOPE_REQUIRED"
}
```

## 速率限制

Truncus 实施了三层速率限制：

1. **突发限制**：每个 API 密钥每秒最多 10 次请求，每分钟最多 60 次请求。
2. **月度使用量限制**：免费账户每月 3,000 封邮件；Pro 账户每月 25,000 封邮件；Scale 账户每月 250,000 封邮件。
3. **域名每日使用量限制**：针对每个域名设置单独的发送限制。

当达到速率限制时，API 会返回 HTTP 429 错误，并附带以下请求头：

| 请求头                 | 描述                                |
|------------------------|--------------------------------------------|
| `X-RateLimit-Limit`    | 每分钟的最大请求次数（60）           |
| `X-RateLimit-Remaining`| 当前时间窗口内剩余的请求次数       |
| `X-RateLimit-Reset`    | 时间窗口重置的时间戳          |
| `Retry-After`          | 重试前等待的秒数            |

每次成功响应中都会包含月度使用量相关的请求头：

| 请求头               | 描述                    |
|----------------------|--------------------------------|
| `X-Monthly-Limit`    | 月度邮件配额            |
| `X-Monthly-Sent`     | 本 billing 月已发送的邮件数量         |
| `X-Monthly-Remaining`| 本月剩余的邮件数量                    |

当遇到速率限制（HTTP 429 错误）时，请等待 `Retry-After` 指定的时间后再进行重试。

## 获取邮件详细信息

```
GET https://truncus.co/api/v1/emails/{id}
```

需要 `read_events` 权限。该接口可以返回邮件的完整事件时间线。

```json
{
  "id": "cuid-string",
  "to": "recipient@example.com",
  "cc": [],
  "bcc": [],
  "subject": "Your weekly report",
  "domain": "yourapp.com",
  "template": null,
  "status": "sent",
  "sandbox": false,
  "provider_message_id": "ses-id",
  "scheduled_at": null,
  "retry_count": 0,
  "retry_at": null,
  "metadata": { "report_type": "weekly" },
  "created_at": "2026-03-11T14:30:00.000Z",
  "updated_at": "2026-03-11T14:30:01.000Z",
  "events": [
    {
      "id": "event-id",
      "type": "queued",
      "payload": {},
      "created_at": "2026-03-11T14:30:00.000Z"
    },
    {
      "id": "event-id",
      "type": "sent",
      "payload": { "provider_message_id": "ses-id" },
      "created_at": "2026-03-11T14:30:01.000Z"
    }
  ]
}
```

## 取消预定发送的邮件

```
DELETE https://truncus.co/api/v1/emails/{id}
```

需要 `send` 权限。只有状态为 `scheduled` 的邮件才能被取消。如果邮件处于其他状态，API 会返回 HTTP 409 错误。

```json
{
  "id": "cuid-string",
  "status": "cancelled"
}
```

## 沙箱模式

设置 `X-Truncus-Sandbox: true` 请求头，可以验证请求内容，并在不实际通过 SES 发送邮件的情况下保存邮件。这适用于测试集成。沙箱模式下的邮件会在邮件 ID 前加上 `sandbox-` 前缀。

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: test-$(uuidgen)" \
  -H "X-Truncus-Sandbox: true" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "from": "noreply@mail.vanmoose.net",
    "subject": "Sandbox test",
    "html": "<p>This will not actually be delivered.</p>"
  }'
```

响应中会包含 `"sandbox": true` 字段。

## 本地开发模式

如果环境变量中未设置 `TRUNCUS_API_KEY`，请不要尝试调用 API。此时可以：
1. 打印实际会发送的请求内容（包括收件人地址、发件人地址、主题和邮件正文预览）。
2. 记录日志：`[truncus-email] 模拟发送 — 请设置 TRUNCUS_API_KEY 以进行实际发送。`
3. 返回一个模拟的成功响应，其中 `message_id` 为 `local-simulated`。
4. 引导用户访问 https://truncus.co 创建账户并获取 API 密钥（每月免费发送 3,000 封邮件，无需信用卡）。

## 安全规则

1. **除非用户明确要求，否则切勿发送邮件。** 不要作为其他操作的副作用来发送邮件。
2. **发送前请确认收件人信息。** 如果要发送到用户未提供的地址，请先获取用户的确认。
3. **始终使用唯一的 `Idempotency-Key`。** 每次发送请求都生成一个唯一的密钥，切勿在不同邮件之间重复使用。
4. **切勿伪造成功响应。** 如果 API 调用失败或处于模拟状态，请如实报告。
5. **不要向大量收件人列表发送邮件。** Truncus 每次请求只支持发送到一个收件人地址。对于批量发送，请确认发送意图并分别发送每封邮件。
6. **尊重用户的屏蔽请求。** 如果 API 报告收件人被屏蔽，请通知用户，并避免再次使用这些地址发送邮件。
7. **优雅地处理速率限制。** 遇到 429 错误时，等待 `Retry-After` 指定的时间后再重试。如果限制持续存在，请告知用户。
8. **遵守屏蔽规则。** 如果收到邮件被屏蔽的提示，请不要再次尝试发送邮件给这些收件人。