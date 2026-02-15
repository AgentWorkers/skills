---
name: unione
description: >
  Send transactional and marketing emails via UniOne Email API.
  Manage email templates, validate email addresses, check delivery statistics,
  manage suppression lists, configure webhooks, and handle domain settings.
  UniOne delivers billions of emails annually with 99.88% deliverability.
metadata:
  openclaw:
    emoji: "📧"
    requires:
      env:
        - UNIONE_API_KEY
    primaryEnv: UNIONE_API_KEY
---

# UniOne 邮件 API

UniOne 是一个提供事务性邮件服务的平台，通过 Web API 可以大规模发送事务性邮件和营销邮件（每秒最多 3,000 封邮件）。该 API 允许您发送邮件、管理模板、验证地址、跟踪邮件送达情况等。

## 认证

所有请求都需要 `UNIONE_API_KEY` 环境变量。请将其作为 `X-API-KEY` 标头传递。

**基础 URL:** `https://api.unione.io/en/transactional/api/v1/{method}.json?platform=openclaw`

所有方法均使用 `POST` 请求，并且请求体为 JSON 格式。

---

## 重要提示：域名设置（发送邮件前必须完成）

**在发送邮件之前，必须先验证发送者的域名。** 在尝试发送任何邮件之前，请确保域名已经设置完成：

### 第一步：获取 DNS 记录信息 — `domain/get-dns-records.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/domain/get-dns-records.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"domain": "yourdomain.com"}'
```

**API 响应** 返回原始的 DNS 记录信息（不可直接使用）：

```json
{
  "status": "success",
  "domain": "yourdomain.com",
  "verification-record": "unione-validate-hash=483bb362ebdbeedd755cfb1d4d661",
  "dkim": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDo7"
}
```

**用户需要根据这些信息创建 3 个 DNS TXT 记录：**

| 记录主机 | 记录类型 | 值 |
|-------------|-------------|-------|
| `@` | TXT | `unione-validate-hash=<响应中的验证信息>` |
| `us._domainkey` | TXT | `k=rsa; p=<响应中的 DKIM 信息>` |
| `@` | TXT | `v=spf1 include:spf.unione.io ~all` |

请将这些记录清晰地展示给用户，并指导他们在他们的 DNS 提供商（如 Cloudflare、Route53、GoDaddy 等）处添加这些记录。SPF 记录的内容是固定的，不会通过 API 返回。

### 第二步：验证域名所有权 — `domain/validate-verification.json`

用户添加 DNS 记录后，请执行此步骤：

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/domain/validate-verification.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"domain": "yourdomain.com"}'
```

### 第三步：验证 DKIM — `domain/validate-dkim.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/domain/validate-dkim.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"domain": "yourdomain.com"}'
```

### 第四步：列出所有域名 — `domain/list.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/domain/list.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{}'
```

**如果域名验证失败：** DNS 记录的传播可能需要最多 48 小时。建议用户等待或检查 DNS 记录中是否有拼写错误。

---

## 错误处理与重试策略

### 重试逻辑

在发送 API 请求时，对于可重试的错误，请采用指数级退避策略进行重试：

**可重试的错误（需要采用指数级退避重试）：**

| HTTP 状态码 | 含义 | 重试策略 |
|-----------|---------|----------------|
| 429 | 超时限制 | 等待一段时间后重试。如果存在 `Retry-After` 标头，请遵循其指示 |
| 500 | 服务器内部错误 | 重试最多 3 次 |
| 502 | 网关错误 | 重试最多 3 次 |
| 503 | 服务不可用 | 重试最多 3 次 |
| 504 | 网关超时 | 重试最多 3 次 |

**推荐的重试时间表：**

| 重试次数 | 重试延迟 |
|---------|-------|
| 1       | 立即     |
| 2       | 1 秒     |
| 3       | 5 秒     |
| 4       | 30 秒     |

**不可重试的错误（不要重试）：**

| HTTP 状态码 | 含义 | 处理方式 |
|-----------|---------|--------|
| 400 | 请求错误 | 修复请求参数 |
| 401 | 未经授权 | 检查 API 密钥 |
| 403 | 禁止访问 | 检查权限/域名验证 |
| 404 | 未找到端点 | 检查请求路径 |
| 413 | 请求数据过大 | 减少请求大小 |

### 原子性

对于 `email/send.json` 请求，务必包含 `idempotency_key` 以防止重复发送。这对于生产环境至关重要。

`idempotency_key` 是一个唯一的字符串（建议使用 UUID），需要在请求体中传递。如果 UniOne 收到两个带有相同键的请求，它会返回第一次请求的结果，而不会再次发送邮件。

**对于每次发送操作，都必须生成一个唯一的 `idempotency_key`，并在重试时使用相同的键。**

---

## 1. 发送邮件 — `email/send.json`

向一个或多个收件人发送事务性或营销邮件。支持通过替换变量、模板、附件、跟踪信息和元数据进行个性化设置。

### 使用 curl 发送邮件

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{
    "idempotency_key": "unique-uuid-here",
    "message": {
      "recipients": [
        {
          "email": "recipient@example.com",
          "substitutions": {
            "to_name": "John Smith"
          }
        }
      ],
      "body": {
        "html": "<h1>Hello, {{to_name}}!</h1><p>Your order has been confirmed.</p>",
        "plaintext": "Hello, {{to_name}}! Your order has been confirmed."
      },
      "subject": "Order Confirmation",
      "from_email": "noreply@yourdomain.com",
      "from_name": "Your Store"
    }
  }'
```

### 使用 Node.js 发送邮件

```javascript
const response = await fetch("https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-KEY": process.env.UNIONE_API_KEY
  },
  body: JSON.stringify({
    idempotency_key: crypto.randomUUID(),
    message: {
      recipients: [{ email: "recipient@example.com", substitutions: { to_name: "John" } }],
      body: {
        html: "<h1>Hello, {{to_name}}!</h1><p>Your order has been confirmed.</p>",
        plaintext: "Hello, {{to_name}}! Your order has been confirmed."
      },
      subject: "Order Confirmation",
      from_email: "noreply@yourdomain.com",
      from_name: "Your Store"
    }
  })
});
const data = await response.json();
// data.status === "success" → data.job_id, data.emails
```

### 使用 Python 发送邮件

```python
import requests, uuid, os

response = requests.post(
    "https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw",
    headers={
        "Content-Type": "application/json",
        "X-API-KEY": os.environ["UNIONE_API_KEY"]
    },
    json={
        "idempotency_key": str(uuid.uuid4()),
        "message": {
            "recipients": [{"email": "recipient@example.com", "substitutions": {"to_name": "John"}}],
            "body": {
                "html": "<h1>Hello, {{to_name}}!</h1><p>Your order has been confirmed.</p>",
                "plaintext": "Hello, {{to_name}}! Your order has been confirmed."
            },
            "subject": "Order Confirmation",
            "from_email": "noreply@yourdomain.com",
            "from_name": "Your Store"
        }
    }
)
data = response.json()  # data["status"] == "success" → data["job_id"], data["emails"]
```

### 使用 Go 发送邮件

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "github.com/google/uuid"
)

func sendEmail() error {
    payload := map[string]interface{}{
        "idempotency_key": uuid.New().String(),
        "message": map[string]interface{}{
            "recipients": []map[string]interface{}{
                {"email": "recipient@example.com", "substitutions": map[string]string{"to_name": "John"}},
            },
            "body": map[string]string{
                "html":      "<h1>Hello, {{to_name}}!</h1><p>Your order has been confirmed.</p>",
                "plaintext": "Hello, {{to_name}}! Your order has been confirmed.",
            },
            "subject":    "Order Confirmation",
            "from_email": "noreply@yourdomain.com",
            "from_name":  "Your Store",
        },
    }
    body, _ := json.Marshal(payload)
    req, _ := http.NewRequest("POST",
        "https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw",
        bytes.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("X-API-KEY", os.Getenv("UNIONE_API_KEY"))
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    fmt.Println(result) // result["status"] == "success"
    return nil
}
```

### 使用 PHP 发送邮件

```php
$ch = curl_init("https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw");
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => [
        "Content-Type: application/json",
        "X-API-KEY: " . getenv("UNIONE_API_KEY")
    ],
    CURLOPT_POSTFIELDS => json_encode([
        "idempotency_key" => bin2hex(random_bytes(16)),
        "message" => [
            "recipients" => [["email" => "recipient@example.com", "substitutions" => ["to_name" => "John"]]],
            "body" => [
                "html" => "<h1>Hello, {{to_name}}!</h1><p>Your order has been confirmed.</p>",
                "plaintext" => "Hello, {{to_name}}! Your order has been confirmed."
            ],
            "subject" => "Order Confirmation",
            "from_email" => "noreply@yourdomain.com",
            "from_name" => "Your Store"
        ]
    ])
]);
$response = curl_exec($ch);
$data = json_decode($response, true); // $data["status"] === "success"
```

**成功响应：**
```json
{
  "status": "success",
  "job_id": "1ZymBc-00041N-9X",
  "emails": ["recipient@example.com"]
}
```

**`message` 对象的完整参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `recipients` | 数组 | 是 | 收件人对象数组。每个对象包含 `email`（必填）、`substitutions`（对象）、`metadata`（对象） |
| `body.html` | 字符串 | 是* | HTML 内容。可以使用 `{{variable}}` 进行替换 |
| `body.plaintext` | 字符串 | 否 | 纯文本版本 |
| `subject` | 字符串 | 是* | 邮件主题行。支持使用 `{{substitutions}}` 进行替换 |
| `from_email` | 字符串 | 是* | 发件人邮箱（必须来自已验证的域名） |
| `from_name` | 字符串 | 否 | 发件人显示名称 |
| `reply_to` | 字符串 | 否 | 回复邮箱地址 |
| `template_id` | 字符串 | 否 | 使用存储的模板代替 HTML 内容/主题 |
| `tags` | 数组 | 否 | 用于分类和过滤的标签 |
| `track_links` | 0/1 | 否 | 启用点击跟踪（默认值：0） |
| `track_read` | 0/1 | 启用打开链接跟踪（默认值：0） |
| `global_language` | 字符串 | 否 | 用于取消订阅页的语言（en, de, fr, es, it, pl, pt, ru, ua, be） |
| `template_engine` | 字符串 | 否 | 使用的模板引擎（默认值：`simple`、`velocity` 或 `liquid`） |
| `global_substitutions` | 对象 | 否 | 所有收件人都可以使用的变量 |
| `attachments` | 数组 | 否 | 包含 `{type, name, content}` 的数组，其中 `content` 为 Base64 编码的文件 |
| `skip_unsubscribe` | 0/1 | 否 | 是否跳过取消订阅页（仅适用于事务性邮件） |
| `headers` | 对象 | 否 | 自定义邮件头部 |

**顶级参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `idempotency_key` | 字符串 | 建议使用 | 唯一的键（UUID），用于防止重复发送。最多 36 个字符。 |

**使用模板发送邮件：**
```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{
    "idempotency_key": "unique-uuid-here",
    "message": {
      "recipients": [
        {
          "email": "customer@example.com",
          "substitutions": {
            "to_name": "Alice",
            "order_id": "ORD-12345",
            "total": "$59.99"
          }
        }
      ],
      "template_id": "your-template-id",
      "from_email": "shop@yourdomain.com",
      "from_name": "My Shop"
    }
  }'
```

**向多个收件人发送个性化邮件：**
```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/email/send.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{
    "idempotency_key": "unique-uuid-here",
    "message": {
      "recipients": [
        {"email": "alice@example.com", "substitutions": {"to_name": "Alice"}},
        {"email": "bob@example.com", "substitutions": {"to_name": "Bob"}}
      ],
      "body": {
        "html": "<p>Hi {{to_name}}, check out our new {{promo_name}}!</p>"
      },
      "subject": "Special offer for you, {{to_name}}!",
      "from_email": "marketing@yourdomain.com",
      "from_name": "Marketing Team",
      "global_substitutions": {"promo_name": "Summer Sale"},
      "track_links": 1,
      "track_read": 1,
      "tags": ["promo", "summer-2026"]
    }
  }'
```

---

## 2. 邮件地址验证 — `email-validation/single.json`

验证电子邮件地址是否有效且可送达。

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/email-validation/single.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"email": "user@example.com"}'
```

**响应：**
```json
{
  "status": "success",
  "email": "user@example.com",
  "result": "valid",
  "local_part": "user",
  "domain": "example.com",
  "mx_found": true,
  "mx_record": "mail.example.com"
}
```

可能的返回值：`"valid"`、`"invalid"`、`"unresolvable"`、`"unknown"`。

---

## 3. 模板管理

### 3.1 创建/更新模板 — `template/set.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/template/set.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{
    "template": {
      "name": "Order Confirmation",
      "subject": "Your order {{order_id}} is confirmed",
      "template_engine": "simple",
      "body": {
        "html": "<h1>Thank you, {{to_name}}!</h1><p>Order {{order_id}} total: {{total}}</p>",
        "plaintext": "Thank you, {{to_name}}! Order {{order_id}} total: {{total}}"
      },
      "from_email": "shop@yourdomain.com",
      "from_name": "My Shop"
    }
  }'
```

**响应：`{"status": "success", "template": {"id": "生成的模板 ID"}}`

**更新**现有模板时，请在模板对象中包含 `id` 字段。

### 3.2 获取模板 — `template/get.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/template/get.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"id": "template-id-here"}'
```

### 3.3 列出模板 — `template/list.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/template/list.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"limit": 50, "offset": 0}'
```

### 3.4 删除模板 — `template/delete.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/template/delete.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{"id": "template-id-here"}'
```

---

## 4. Webhook 管理

Webhook 可以将邮件事件的实时通知发送到您的 URL。

### 4.1 设置 Webhook — `webhook/set.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/webhook/set.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{
    "url": "https://yourapp.com/unione-webhook",
    "events": {
      "email_status": [
        "delivered", "opened", "clicked", "unsubscribed",
        "soft_bounced", "hard_bounced", "spam"
      ]
    }
  }'
```

### 4.2 列出 Webhook — `webhook/list.json`

```bash
curl -X POST "https://api.unione.io/en/transactional/api/v1/webhook/list.json?platform=openclaw" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $UNIONE_API_KEY" \
  -d '{}'
```

### 4.3 获取/删除 Webhook — `webhook/get.json` / `webhook/delete.json`

```bash
# Get
curl -X POST ".../webhook/get.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{"url": "https://yourapp.com/unione-webhook"}'

# Delete
curl -X POST ".../webhook/delete.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{"url": "https://yourapp.com/unione-webhook"}'
```

---

## 5. 邮件抑制列表管理

### 5.1 添加抑制规则 — `suppression/set.json`

**原因值：`"unsubscribed"`、`temporary_unavailable`、`permanent_unavailable`、`complained`**

### 5.2 检查抑制规则 — `suppression/get.json`

```bash
curl -X POST ".../suppression/get.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{"email": "user@example.com"}'
```

### 5.3 列出抑制规则 — `suppression/list.json`

```bash
curl -X POST ".../suppression/list.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{"cause": "hard_bounced", "limit": 50, "offset": 0}'
```

### 5.4 删除抑制规则 — `suppression/delete.json`

```bash
curl -X POST ".../suppression/delete.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{"email": "user@example.com"}'
```

---

## 6. 事件日志记录

### 6.1 创建事件日志 — `event-dump/create.json`

```bash
curl -X POST ".../event-dump/create.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"start_time": "2026-01-01 00:00:00", "end_time": "2026-01-31 23:59:59", "limit": 50000, "all_events": true}'
```

### 6.2 获取/列出/删除事件日志 — `event-dump/get.json` / `event-dump/delete.json`

---

## 7. 标签管理 — `tag/list.json` / `tag/delete.json`

```bash
# List tags
curl -X POST ".../tag/list.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{}'

# Delete tag
curl -X POST ".../tag/delete.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{"tag_id": 123}'
```

---

## 8. 项目管理 — `project/create.json` / `project/list.json`

```bash
# Create project
curl -X POST ".../project/create.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project": {"name": "My Project", "send_enabled": true}}'

# List projects
curl -X POST ".../project/list.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{}'
```

---

## 9. 系统信息 — `system/info.json`

```bash
curl -X POST ".../system/info.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" -d '{}'
```

---

## 10. 订阅（双确认） — `email/subscribe.json`

```bash
curl -X POST ".../email/subscribe.json?platform=openclaw" -H "X-API-KEY: $UNIONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"from_email": "newsletter@yourdomain.com", "from_name": "Newsletter", "to_email": "newsubscriber@example.com"}'
```

---

## 代理操作指南

1. **必须完成域名设置。** 在首次发送邮件之前，请务必检查用户的域名是否已验证。运行 `domain/list.json` 进行验证。如果未验证，请指导用户完成域名设置流程（参见“域名设置”部分）。
2. **所有请求的 API 主机必须使用 `api.unione.io`。**
3. **未经用户明确确认，切勿发送邮件。** 在执行 `email/send.json` 之前，务必向用户显示邮件内容、主题和邮件摘要。
4. **在 `email/send.json` 请求中务必包含 `idempotency_key`。** 为每次发送生成一个唯一的 UUID，并在重试时使用相同的键。
5. **对于 429 和 5xx 状态码的错误，采用指数级退避策略进行重试（参见错误处理部分）。不要重试 400、401、403、404、413 状态码的错误。**
6. **进行模板操作** 时，先列出可用的模板，然后再选择使用哪个模板。
7. **进行验证** 时，要清晰地显示结果并给出相应的处理建议。
8. **优雅地处理错误。** 如果请求返回错误，请说明问题所在并提供解决方法。
9. **提醒用户** 发件人邮箱必须在他们的 UniOne 账户中经过验证。
10. **替换变量的语法** 使用双大括号：`{{variable_name}}`。
11. **附件必须进行 Base64 编码。** 如有需要，可帮助用户进行文件编码。
12. **安全注意事项**：切勿记录或显示完整的 API 密钥。提醒用户保密 API 密钥。
13. **代码语言**：如果用户的项目使用特定的编程语言（如 Node.js、Python、Go、PHP 等），请提供相应的代码示例。本文档中的示例可以适配任何能够发送 JSON 格式请求的语言。

## 常见工作流程

### “发送测试邮件”
1. 检查域名是否已验证（`domain/list.json`）
2. 如果域名未验证，指导用户完成域名设置
3. 获取收件人的电子邮件地址
4. 撰写简单的测试邮件内容
5. 在发送前确认用户同意
6. 使用 `idempotency_key` 执行 `email/send.json`
7. 成功后报告作业 ID

### “检查我的邮件送达设置”
1. 运行 `system/info.json` 获取账户状态
2. 运行 `domain/list.json` 检查域名验证情况
3. 对于每个未验证的域名，运行 `domain/get-dns-records.json` 并显示所需的 DNS 记录
4. 运行 `domain/validate-dkim.json` 检查 DKIM 信息
5. 如果域名未完全验证，提供相应的修复建议

### “验证邮件列表”
1. 对每个邮件地址调用 `email-validation/single.json`
2. 对结果进行分类（有效、无效、未知）
3. 提供汇总报告

### “设置邮件送达跟踪”
1. 获取用于跟踪的 Webhook URL 和相关事件
2. 执行 `webhook/set.json`
3. 确认设置完成

## 资源

- 完整的 API 参考文档：https://docs.unione.io/en/web-api-ref
- 入门指南：https://docs.unione.io/en/
- 模板引擎：https://docs.unione.io/en/web-api#section-template-engines
- 注册：https://cp.unione.io/en/user/registration/