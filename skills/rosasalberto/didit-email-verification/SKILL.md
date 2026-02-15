---
name: didit-email-verification
description: >
  Integrate Didit Email Verification standalone API to verify email addresses via OTP.
  Use when the user wants to verify emails, send email OTP codes, check email verification codes,
  detect breached or disposable emails, check if an email is undeliverable, or implement
  email-based identity verification using Didit. Supports fraud signals (IP, device, user agent),
  configurable code length, alphanumeric codes, and policy-based auto-decline for risky emails.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "✉️"
    homepage: https://docs.didit.me
---

# Didit 邮箱验证 API

## 概述

通过一次性验证码实现两步邮箱验证流程：

1. **发送** 验证码到指定的电子邮件地址。
2. **检查** 用户输入的验证码。

**关键限制：**
- 验证码在 **5 分钟** 后失效。
- 每个验证码最多允许 **3 次尝试**（超过次数需重新发送）。
- 24 小时内最多允许 **2 次重新发送请求。
- 必须先调用 **Send** 方法，再调用 **Check** 方法；否则 `Check` 方法会返回 `"Expired or Not Found"`。

**功能：** 能够检测到被泄露的邮箱（通过已知的数据泄露事件）、临时/一次性邮箱服务提供商提供的邮箱以及无法接收邮件的邮箱。支持用于风险评分的欺诈检测信号。

**API 参考：** [发送验证码](https://docs.didit.me/reference/send-email-verification-code-api) | [检查验证码](https://docs.didit.me/reference/check-email-verification-code-api)

---

## 认证

所有请求都需要通过 `x-api-key` 头部字段传递 API 密钥。

**获取方法：** [Didit 商业控制台](https://business.didit.me) → API & Webhooks → 复制 API 密钥。

```
x-api-key: your_api_key_here
```

> `401` = API 密钥缺失或无效。`403` = 密钥权限不足或信用额度不足。

---

## 第一步：发送邮箱验证码

向指定的电子邮件地址发送一次性验证码。

### 请求

```
POST https://verification.didit.me/v3/email/send/
```

### 头部字段

| 字段 | 值 | 是否必填 |
|---|---|---|
| `x-api-key` | 你的 API 密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON）

| 参数 | 类型 | 是否必填 | 默认值 | 限制 | 说明 |
|---|---|---|---|---|---|
| `email` | string | 是 | — | 有效的电子邮件地址 | 需要发送验证码的邮箱地址 |
| `options.code_size` | integer | 否 | `6` | 验证码的长度，最小为 4 位，最大为 8 位 |
| `options.alphanumeric_code` | boolean | 否 | `false` | — | `true` 表示验证码只能由字母（A-Z）和数字（0-9）组成（不区分大小写） |
| `options.locale` | string | 否 | — | 邮件模板使用的区域设置，最多 5 个字符，例如 `en-US` |
| `signals.ip` | string | 否 | — | 用户的 IP 地址，用于欺诈检测 |
| `signals.device_id` | string | 否 | — | 最多 255 个字符的唯一设备标识符 |
| `signals.user_agent` | string | 否 | — | 最多 512 个字符的浏览器/客户端用户代理 |
| `vendor_data` | string | 否 | — | 用于会话跟踪的标识符 |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/email/send/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "email": "user@example.com",
        "options": {"code_size": 6},
        "signals": {"ip": "203.0.113.42"},
        "vendor_data": "session-abc-123",
    },
)
print(response.status_code, response.json())
```

```typescript
const response = await fetch("https://verification.didit.me/v3/email/send/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "user@example.com",
    options: { code_size: 6 },
    signals: { ip: "203.0.113.42" },
  }),
});
```

### 响应（200 OK）

```json
{
  "request_id": "e39cb057-92fc-4b59-b84e-02fec29a0f24",
  "status": "Success",
  "reason": null
}
```

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Success"` | 验证码已发送 | 继续流程——等待用户输入验证码，然后调用 `Check` 方法 |
| `"Retry"` | 邮件暂时无法送达 | 等待几秒钟后重新尝试发送（最多重试 2 次） |
| `"Undeliverable"` | 邮箱无法接收邮件 | 通知用户该邮箱无效或无法接收邮件 |

### 错误响应

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求体或电子邮件格式无效 | 检查电子邮件格式和参数是否正确 |
| `401` | API 密钥无效或缺失 | 确认 `x-api-key` 头部字段是否正确 |
| `403` | 信用额度不足或权限不足 | 在商业控制台检查信用额度 |
| `429` | 被限制使用 | 按提示等待一段时间后重试 |

---

## 第二步：检查邮箱验证码

检查用户收到的验证码。**必须在成功发送验证码后调用此方法**。可以选择自动拒绝高风险邮箱。

### 请求

```
POST https://verification.didit.me/v3/email/check/
```

### 头部字段

| 字段 | 值 | 是否必填 |---|
| `x-api-key` | 你的 API 密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON）

| 参数 | 类型 | 是否必填 | 默认值 | 可选值 | 说明 |
|---|---|---|---|---|
| `email` | string | 是 | — | 第一步中使用的有效电子邮件地址 |
| `code` | string | 是 | — | 用户收到的验证码，长度为 4-8 位 |
| `duplicated_email_action` | string | 否 | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | 如果该邮箱已被其他用户验证，则拒绝 |
| `breached_email_action` | string | 否 | `"NO_ACTION"` | `"NO_ACTION"` | 如果该邮箱在已知的数据泄露事件中被发现，则拒绝 |
| `disposable_email_action` | string | 否 | `"NO_ACTION"` | `"NO ACTION"` | 如果该邮箱是一次性/临时邮箱服务提供的，则拒绝 |
| `undeliverable_email_action` | string | 否 | `"NO_ACTION"` | `"NO ACTION"` | 如果该邮箱无法接收邮件，则拒绝 |

> **政策说明：** 当设置为 `"DECLINE"` 时，即使验证码正确也会拒绝验证请求。`email.*` 字段仍然会被填充，以便你查看拒绝原因。

### 示例

```python
response = requests.post(
    "https://verification.didit.me/v3/email/check/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "email": "user@example.com",
        "code": "123456",
        "breached_email_action": "DECLINE",
        "disposable_email_action": "DECLINE",
    },
)
```

```typescript
const response = await fetch("https://verification.didit.me/v3/email/check/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "user@example.com",
    code: "123456",
    breached_email_action: "DECLINE",
    disposable_email_action: "DECLINE",
  }),
});
```

### 响应（200 OK）

```json
{
  "request_id": "e39cb057-92fc-4b59-b84e-02fec29a0f24",
  "status": "Approved",
  "message": "The verification code is correct.",
  "email": {
    "status": "Approved",
    "email": "user@example.com",
    "is_breached": false,
    "breaches": [],
    "is_disposable": false,
    "is_undeliverable": false,
    "verification_attempts": 1,
    "verified_at": "2025-09-15T17:36:19.963451Z",
    "warnings": [],
    "lifecycle": [
      {"type": "EMAIL_VERIFICATION_MESSAGE_SENT", "timestamp": "...", "fee": 0.03},
      {"type": "VALID_CODE_ENTERED", "timestamp": "...", "fee": 0}
    ]
  },
  "created_at": "2025-09-15T17:36:19.703719+00:00"
}
```

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 验证码正确，且没有违反任何政策 | 邮箱验证成功——继续后续流程 |
| `"Failed"` | 验证码错误 | 要求用户重新输入验证码。如果连续失败 3 次，则重新发送一个新的验证码 |
| `"Declined"` | 验证码正确，但违反了某些政策 | 通知用户原因。可以查看 `email.warnings` 以获取详细信息 |
| `"Expired or Not Found"` | 没有有效的验证码 | 验证码已过期（超过 5 分钟）或未调用 `Send` 方法。需要重新发送验证码 |

### 错误响应

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求体或电子邮件格式无效 | 检查电子邮件和验证码的格式 |
| `401` | API 密钥无效或缺失 | 确认 `x-api-key` 头部字段是否正确 |
| `403` | 信用额度不足或权限不足 | 在商业控制台检查信用额度 |
| `404` | 验证码已过期或未找到 | 通过第一步重新发送一个新的验证码 |

---

## 响应字段说明

### `email` 对象

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | string | `"Approved"`, `"Failed"`, `"Declined"` |
| `email` | string | 已验证的电子邮件地址 |
| `is_breached` | boolean | 该邮箱是否在已知的数据泄露事件中被发现 |
| `breaches` | array | 数据泄露事件详情：`{name, domain, breach_date, data_classes, breach_emails_count}` |
| `is_disposable` | boolean | 该邮箱是否来自一次性/临时邮箱服务提供商 |
| `is_undeliverable` | boolean | 该邮箱是否无法接收邮件 |
| `verification_attempts` | integer | 验证尝试次数（最多 3 次） |
| `verified_at` | string | 验证时间的 ISO 8601 时间戳（未验证时为 `null`） |
| `warnings` | array | 风险警告：`{risk, log_type, short_description, long_description}` |
| `lifecycle` | array | 事件日志：`{type, timestamp, fee}` |

---

## 警告标签

| 标签 | 说明 | 自动拒绝条件 |
|---|---|---|
| `EMAIL_CODE_ATTEMPTS_EXCEEDED` | 验证码尝试次数超过限制 | 是 |
| `EMAIL_IN_BLOCKLIST` | 该邮箱在黑名单中 | 是 |
| `UNDELIVERABLE_EMAIL_DETECTED` | 该邮箱无法接收邮件 | 是 |
| `BREACHED_EMAIL_DETECTED` | 该邮箱在已知的数据泄露事件中被发现 | 可配置 |
| `DISPOSABLE_EMAIL_DETECTED` | 该邮箱是一次性/临时邮箱服务提供的 | 可配置 |
| `DUPLICATED_EMAIL` | 该邮箱已被其他用户验证 | 可配置 |

警告的严重程度：`error`（严重），`warning`（需要关注），`information`（信息提示）。

---

## 常见工作流程

### 基本邮箱验证

```
1. POST /v3/email/send/   → {"email": "user@example.com"}
2. Wait for user to provide the code
3. POST /v3/email/check/  → {"email": "user@example.com", "code": "123456"}
4. If "Approved"            → email is verified
   If "Failed"              → ask user to retry (up to 3 attempts)
   If "Expired or Not Found"→ go back to step 1
```

### 严格安全验证

```
1. POST /v3/email/send/   → include signals.ip, signals.device_id, signals.user_agent
2. Wait for user to provide the code
3. POST /v3/email/check/  → set all *_action fields to "DECLINE"
4. If "Approved"  → safe to proceed
   If "Declined" → check email.warnings for reason, block or warn user
```

---

## 实用脚本

**verify_email.py**：从命令行发送和检查邮箱验证码。

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"

python scripts/verify_email.py send user@example.com
python scripts/verify_email.py check user@example.com 123456 --decline-breached --decline-disposable
```

该脚本也可以作为库导入使用：

```python
from scripts.verify_email import send_code, check_code

send_result = send_code("user@example.com")
check_result = check_code("user@example.com", "123456", decline_breached=True)
```