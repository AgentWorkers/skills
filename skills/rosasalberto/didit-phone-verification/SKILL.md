---
name: didit-phone-verification
description: >
  Integrate Didit Phone Verification standalone API to verify phone numbers via OTP.
  Use when the user wants to verify phones, send SMS or WhatsApp or Telegram codes,
  check phone verification codes, detect disposable or VoIP numbers, or implement
  phone-based identity verification using Didit. Supports multiple delivery channels
  (SMS, WhatsApp, Telegram, voice), fraud signals, and policy-based auto-decline.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "📱"
    homepage: https://docs.didit.me
---

# Didit 手机验证码 API

## 概述

通过一次性验证码实现两步手机验证流程：

1. **发送** 验证码到指定手机号码。
2. **检查** 用户输入的验证码。

**关键限制：**
- 验证码在 **5分钟后** 失效。
- 每个验证码最多允许 **3次尝试**（失败后需要重新发送）。
- 24小时内最多允许 **2次重新发送请求**。
- 每个手机号码每小时最多发送 **4次** 验证码。
- 手机号码必须采用 **E.164** 格式（例如：`+14155552671`）。
- 必须先调用 `Send` 方法，然后再调用 `Check` 方法。

**发送方式：** SMS（默认方式）、WhatsApp、Telegram、语音通话。如果首选方式不可用，系统会自动切换为 SMS。

**功能：** 能够检测到一次性/临时号码、VoIP号码、运营商信息以及重复号码，并支持用于风险评估的欺诈检测机制。

**API 参考：** [发送验证码](https://docs.didit.me/reference/send-phone-verification-code-api) | [检查验证码](https://docs.didit.me/reference/check-phone-verification-code-api-1)

---

## 认证

所有请求都需要通过 `x-api-key` 头部字段传递 API 密钥。

**获取方式：** [Didit 商业控制台](https://business.didit.me) → API & Webhooks → 复制 API 密钥。

```
x-api-key: your_api_key_here
```

---

## 第一步：发送手机验证码

### 请求

```
POST https://verification.didit.me/v3/phone/send/
```

### 头部字段

| 头部字段 | 值 | 是否必填 |
| --- | --- |
| `x-api-key` | 你的 API 密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON）

| 参数 | 类型 | 是否必填 | 默认值 | 限制 | 说明 |
| --- | --- | --- | --- | --- |
| `phone_number` | 字符串 | 是 | — | 必须采用 E.164 格式 | 手机号码（例如：`+14155552671`） |
| `options.code_size` | 整数 | 否 | `6` | 最小长度：4，最大长度：8 | 验证码长度 |
| `options.locale` | 字符串 | 否 | — | 最多 5 个字符 | 消息显示的语言（例如：`en-US`） |
| `options.preferred_channel` | 字符串 | 否 | `"whatsapp"` | 可选发送方式 | `"sms"`、`"whatsapp"`、`"telegram"`、`"voice"` |
| `signals.ip` | 字符串 | 否 | — | 用户的 IP 地址（用于欺诈检测） |
| `signals.device_id` | 字符串 | 否 | — | 最大长度：255 个字符 | 设备唯一标识符 |
| `signals.device_platform` | 字符串 | 否 | — | 枚举值：`"android"`、`"ios"`、`"ipados"`、`"tvos"`、`"web"` |
| `signals.device_model` | 字符串 | 否 | — | 最大长度：255 个字符 | 设备型号（例如：`iPhone17,2`） |
| `signals.os_version` | 字符串 | 否 | — | 最大长度：64 个字符 | 操作系统版本 |
| `signals.app_version` | 字符串 | 否 | 最大长度：64 个字符 | 应用程序版本 |
| `signals.user_agent` | 字符串 | 否 | 最大长度：512 个字符 | 浏览器用户代理 |
| `vendor_data` | 字符串 | 否 | — | 用于会话跟踪的标识符 |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/phone/send/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "phone_number": "+14155552671",
        "options": {"preferred_channel": "sms", "code_size": 6},
        "vendor_data": "session-abc-123",
    },
)
```

```typescript
const response = await fetch("https://verification.didit.me/v3/phone/send/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    phone_number: "+14155552671",
    options: { preferred_channel: "sms", code_size: 6 },
  }),
});
```

### 状态码及处理方式

| 状态码 | 含义 | 处理方式 |
| --- | --- | --- |
| `"Success"` | 验证码已发送 | 等待用户输入验证码，然后调用 `Check` 方法 |
| `"Retry"` | 发生临时问题 | 等待几秒钟后重试（最多重试 2 次） |
| `"Undeliverable"` | 手机号码无法接收消息 | 通知用户并尝试其他号码 |
| `"Blocked"` | 手机号码被屏蔽（可能是垃圾信息） | 使用其他号码 |

### 错误响应

| 状态码 | 含义 | 处理方式 |
| --- | --- | --- |
| `400` | 请求体无效 | 检查电话号码格式（E.164）和参数是否正确 |
| `401` | API 密钥无效或缺失 | 确认 `x-api-key` 头部字段是否正确 |
| `403` | 信用额度不足/权限不足 | 在商业控制台检查信用额度 |
| `429` | 每小时每个号码的发送次数达到限制 | 等待冷却时间后再尝试 |

---

## 第二步：检查手机验证码

**必须在成功发送验证码后调用此方法。** 可选择自动拒绝高风险号码。

### 请求

```
POST https://verification.didit.me/v3/phone/check/
```

### 请求体（JSON）

| 参数 | 类型 | 是否必填 | 默认值 | 可选值 | 说明 |
| --- | --- | --- | --- | --- |
| `phone_number` | 字符串 | 是 | — | 第一步中使用的手机号码（E.164 格式） |
| `code` | 字符串 | 是 | — | 用户收到的验证码（4-8 位） |
| `duplicated_phone_number_action` | 字符串 | 否 | `"NO_ACTION"` | `"DECLINE"` | 如果该号码已被其他用户验证，则拒绝 |
| `disposable_number_action` | 字符串 | 否 | `"NO_ACTION"` | `"DECLINE"` | 如果是临时号码，则拒绝 |
| `voip_number_action` | 字符串 | 否 | `"NO_ACTION"` | `"DECLINE"` | 如果是 VoIP 号码，则拒绝 |

### 示例

```python
response = requests.post(
    "https://verification.didit.me/v3/phone/check/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "phone_number": "+14155552671",
        "code": "123456",
        "disposable_number_action": "DECLINE",
        "voip_number_action": "DECLINE",
    },
)
```

### 响应（200 OK）

```json
{
  "request_id": "e39cb057-...",
  "status": "Approved",
  "message": "The verification code is correct.",
  "phone": {
    "status": "Approved",
    "phone_number_prefix": "+1",
    "phone_number": "4155552671",
    "full_number": "+14155552671",
    "country_code": "US",
    "country_name": "United States",
    "carrier": {"name": "ATT", "type": "mobile"},
    "is_disposable": false,
    "is_virtual": false,
    "verification_method": "sms",
    "verification_attempts": 1,
    "verified_at": "2025-08-24T09:12:39.662232Z",
    "warnings": [],
    "lifecycle": [...]
  }
}
```

### 状态码及处理方式

| 状态码 | 含义 | 处理方式 |
| --- | --- | --- |
| `"Approved"` | 验证码正确，未违反任何规则 | 验证成功，可继续下一步 |
| `"Failed"` | 验证码错误 | 请用户重新尝试（最多尝试 3 次） |
| `"Declined"` | 验证码正确，但违反规则 | 查看 `phone.warnings` 以获取拒绝原因 |
| `"Expired or Not Found"` | 未找到有效的验证码 | 通过第一步重新发送验证码 |

---

## 响应字段说明

### `phone` 对象

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `status` | 字符串 | `"Approved"`、`"Failed"`、`"Declined"` |
| `phone_number_prefix` | 字符串 | 国家代码前缀（例如：`+1`） |
| `full_number` | 字符串 | 完整的 E.164 格式电话号码 |
| `country_code` | 字符串 | ISO 3166-1 国家代码 |
| `carrier.name` | 字符串 | 运营商名称 |
| `carrier.type` | 字符串 | `"mobile"`、`"landline"`、`"voip"`、`"unknown"` |
| `is_disposable` | 布尔值 | 是否为一次性/临时号码 |
| `is_virtual` | 布尔值 | 是否为 VoIP 号码 |
| `verification_method` | 字符串 | `"sms"`、`"whatsapp"`、`"telegram"`、`"voice"` |
| `verification_attempts` | 整数 | 验证尝试次数（最多 3 次） |
| `warnings` | 数组 | `{risk, log_type, short_description, long_description}` | 验证相关警告信息 |

---

## 警告标签

| 标签 | 说明 | 是否自动拒绝 |
| --- | --- | --- |
| `VERIFICATION_CODE_ATTEMPTS_EXCEEDED` | 超过最大尝试次数 | 是 |
| `PHONE_NUMBER_IN_BLOCKLIST` | 手机号码在黑名单中 | 是 |
| `HIGH_RISK_PHONE_NUMBER` | 被识别为高风险号码 | 是 |
| `DISPOSABLE_NUMBER_DETECTED` | 检测到临时号码 | 可配置 |
| `VOIP_NUMBER_DETECTED` | 检测到 VoIP 号码 | 可配置 |
| `DUPLICATED_PHONE_NUMBER` | 该号码已被其他用户验证 | 可配置 |

---

## 常见使用场景

### 基本手机验证流程

```
1. POST /v3/phone/send/   → {"phone_number": "+14155552671"}
2. Wait for user to provide the code
3. POST /v3/phone/check/  → {"phone_number": "+14155552671", "code": "123456"}
4. If "Approved"            → phone is verified
   If "Failed"              → retry (up to 3 attempts)
   If "Expired or Not Found"→ resend (step 1)
```

### 严格安全验证流程

```
1. POST /v3/phone/send/   → include signals.ip, signals.device_platform, channel: "sms"
2. POST /v3/phone/check/  → set disposable_number_action + voip_number_action to "DECLINE"
3. If "Declined" → check phone.warnings, block or warn user
```

---

## 实用脚本

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/verify_phone.py send +14155552671 --channel sms
python scripts/verify_phone.py check +14155552671 123456 --decline-voip
```