---
name: engagelab-otp
description: 调用 EngageLab 的 OTP REST API 可以发送一次性密码（OTP）、验证验证码、发送自定义消息，并通过 SMS、WhatsApp、电子邮件和语音渠道管理 OTP 模板。当用户需要通过 EngageLab 发送 OTP 或验证码、通过 OTP 平台发送自定义消息、管理 OTP 模板、配置回调 Webhook 或通过 SMPP 进行集成时，都可以使用此功能。此外，当用户提及 “engagelab otp”、“otp api”、“send otp”、“verify otp”、“one-time password”、“verification code”、“engagelab verification”、“otp template”、“multi-channel otp”、“whatsapp otp”、“sms otp”、“voice otp”、“email otp” 或请求与 EngageLab OTP 平台集成时，也会触发此功能。该功能涵盖 OTP 的生成、发送、验证、自定义消息发送、模板管理以及 SMPP 集成等操作——即使用户只需要其中的一项功能，也可以使用它。
---
# EngageLab OTP API 技能

该技能支持与 EngageLab OTP REST API 的交互。OTP 服务负责生成一次性密码（OTP），并通过多种渠道（短信、WhatsApp、电子邮件、语音）发送密码，同时提供验证功能以及欺诈监控服务。

该技能涵盖以下六个方面：

1. **发送 OTP** — 由平台生成的 OTP 代码的发送
2. **自定义 OTP 发送** — 由用户生成的 OTP 代码的发送
3. **验证 OTP** — 验证 OTP 代码的有效性
4. **发送自定义消息** — 发送基于自定义模板的消息（通知、营销信息）
5. **模板管理** — 创建、列出、获取和删除 OTP 模板
6. **回调与 SMPP** — 配置 Webhook 以及集成 SMPP 协议

## 资源

### 脚本

- **`otp_client.py`** — Python 客户端类（`EngageLabOTP`），封装了所有 API 端点：`send_otp()`、`send_custom_otp()`、`verify()`、`send_custom_message()` 和模板 CRUD 操作。该脚本处理身份验证、请求构建以及错误处理。可以直接使用，或将其导入用户的项目中。
- **`verify_callback.py`** — 用于验证来自 OTP 回调 Webhook 的 HMAC-SHA256 签名。解析 `X-CALLBACK-ID` 标头以确认请求的真实性。可将其集成到任何 Web 框架（如 Flask、FastAPI、Django）中，以保护回调端点。

### 参考文档

- **`error-codes.md`** — 所有 OTP API 的完整错误代码表
- **`template-api.md` — 包含所有渠道配置的模板 CRUD 规范
- **`callback-config.md` — Webhook 设置、安全机制及所有事件类型的说明
- **`smpp-guide.md** — SMPP 协议的连接、消息发送及报告功能

## 身份验证

所有 EngageLab OTP API 调用均使用 **HTTP Basic Authentication** 进行身份验证。

- **基础 URL**：`https://otp.api.engagelab.cc`
- **请求头**：`Authorization: Basic <base64(dev_key:dev_secret>`
- **Content-Type**：`application/json`

用户必须提供他们的 `dev_key` 和 `dev_secret`，并将其编码为 `base64("dev_key:dev_secret)`，然后设置在请求头中。

**示例**（使用 curl）：

```bash
curl -X POST https://otp.api.engagelab.cc/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'YOUR_DEV_KEY:YOUR_DEV_SECRET' | base64)" \
  -d '{ ... }'
```

如果用户尚未提供凭据，请在生成 API 调用之前要求他们提供 `dev_key` 和 `dev_secret`。

## 快速参考 — 所有端点

| 操作 | 方法 | 路径 |
|-----------|--------|------|
| 发送 OTP（平台生成） | `POST` | `/v1/messages` |
| 发送自定义 OTP 代码 | `POST` | `/v1/codes` |
| 验证 OTP | `POST` | `/v1/verifications` |
| 发送自定义消息 | `POST` | `/v1/custom-messages` |
| 列出模板 | `GET` | `/v1/template-configs` |
| 获取模板详情 | `GET` | `/v1/template-configs/:templateId` |
| 创建模板 | `POST` | `/v1/template-configs` |
| 删除模板 | `DELETE` | `/v1/template-configs/:templateId` |

## 发送 OTP（平台生成的代码）

当您希望 **由 EngageLab 生成** 验证代码并通过指定渠道（短信、WhatsApp、电子邮件、语音）发送时，使用此功能。

**端点**：`POST /v1/messages`

### 请求体

```json
{
  "to": "+8618701235678",
  "template": {
    "id": "test-template-1",
    "language": "default",
    "params": {
      "key1": "value1"
    }
  }
}
```

### 参数

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `to` | `string` | 是 | 手机号码（包含国家代码，例如 `+8613800138000`）或电子邮件地址 |
| `template.id` | `string` | 是 | 模板 ID |
| `template.language` | `string` | 否 | 语言：`default`、`zh_CN`、`zh_HK`、`en`、`ja`、`th`、`es`。默认为 `default` |
| `template.params` | `object` | 否 | 以键值对形式提供的自定义模板变量 |

### 关于 `params` 的说明

- 预设变量（如 `{{brand_name}}`、`{{ttl}}`、`{{pwa_url}}`）会从模板设置中自动填充，无需手动传递。
- 对于模板中的自定义变量（例如 `Hi {{name}}, your code is {{code}}`），请通过 `params` 传递值：`{"name": "Bob"}`。
- 如果模板中的 `from_id` 字段已预设，且您传递了 `{"from_id": "12345"`，则预设值会被覆盖。

### 响应

**成功**：

```json
{
  "message_id": "1725407449772531712",
  "send_channel": "sms"
}
```

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `message_id` | `string` | 唯一的消息 ID，用于验证和追踪 |
| `send_channel` | `string` | 当前的发送渠道：`whatsapp`、`sms`、`email` 或 `voice` |

`send_channel` 表示初始发送渠道；如果配置了回退机制（例如，WhatsApp → SMS），实际发送渠道可能会有所不同。

有关错误代码的详细信息，请参阅 `references/error-codes.md`。

## 自定义 OTP 发送（用户生成的代码）

当您希望 **自己生成** 验证代码并让 EngageLab 发送时，使用此功能。此 API 不负责生成代码，也不需要后续调用验证 API。

**端点**：`POST /v1/codes`

### 请求体

```json
{
  "to": "+8618701235678",
  "code": "398210",
  "template": {
    "id": "test-template-1",
    "language": "default",
    "params": {
      "key1": "value1"
    }
  }
}
```

### 参数

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `to` | `string` | 是 | 手机号码或电子邮件地址 |
| `code` | `string` | 是 | 用户自定义的验证代码 |
| `template.id` | `string` | 是 | 模板 ID |
| `template.language` | `string` | 否 | 语言（与发送 OTP 时相同）。默认为 `default` |
| `template.params` | `object` | 否 | 自定义模板变量 |

### 响应

响应格式与发送 OTP 时相同，返回 `message_id` 和 `send_channel`。

## 验证 OTP

用于验证通过 `/v1/messages` API 发送的验证代码。仅适用于平台生成的 OTP 代码，自定义 OTP 发送不需要此功能。

**端点**：`POST /v1/verifications`

### 请求体

```json
{
  "message_id": "1725407449772531712",
  "verify_code": "667090"
}
```

### 参数

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `message_id` | `string` | 由 `/v1messages` 返回的消息 ID |
| `verify_code` | `string` | 用户输入的验证码 |

### 响应

**成功**：

```json
{
  "message_id": "1725407449772531712",
  "verify_code": "667090",
  "verified": true
}
```

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `message_id` | `string` | 消息 ID |
| `verify_code` | `string` | 用户输入的验证码 |
| `verified` | `boolean` | `true` 表示验证成功，`false` 表示验证失败 |

**重要提示**：成功验证的代码无法再次验证——后续尝试将失败。过期的代码会返回错误代码 `3003`。

## 发送自定义消息

使用在 OTP 平台上创建的模板发送自定义内容（验证代码、通知或营销信息）。

**端点**：`POST /v1/custom-messages`

### 请求体

```json
{
  "to": "+8618701235678",
  "template": {
    "id": "test-template-1",
    "params": {
      "code": "123456",
      "var1": "value1"
    }
  }
}
```

### 参数

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `to` | `string` 或 `string[]` | 是 | 单个接收者（字符串）或多个接收者（数组）。手机号码或电子邮件地址 |
| `template.id` | `string` | 是 | 模板 ID |
| `template.params` | `object` | 否 | 模板变量 |
| `template.params.code` | `string` | 条件性 | 如果模板类型为验证代码，则必填 |

### 关于 `params` 的说明

- 预设变量（`{{brand_name}}`、`{{ttl}}`、`{{pwa_url}}`）会从模板设置中自动替换。
- 对于验证代码模板，**必须** 提供 `{{code}}`，否则会导致错误。
- 自定义变量需要通过 `params` 传递值，例如：`{"name": "Bob"}` 用于生成消息 `Hi {{name}}`。

### 响应

响应格式与发送 OTP 时相同，返回 `message_id` 和 `send_channel`。

## 使用案例示例

**验证代码**：
```json
{
  "to": "+8618701235678",
  "template": { "id": "code-template", "params": { "code": "123456" } }
}
```

**通知**：
```json
{
  "to": ["+8618701235678"],
  "template": { "id": "notification-template", "params": { "order": "123456" } }
}
```

**营销信息**：
```json
{
  "to": ["+8618701235678"],
  "template": { "id": "marketing-template", "params": { "name": "EngageLab", "promotion": "30%" } }
}
```

## 模板管理

OTP 模板定义了消息内容、发送渠道以及验证代码的设置。模板支持多渠道发送，并支持回退机制（例如，WhatsApp → SMS）。

有关所有请求/响应的详细信息（包括所有渠道配置，如 WhatsApp、SMS、语音、电子邮件），请参阅 `references/template-api.md`。

### 快速总结

- **创建模板**：`POST /v1/template-configs`
- **列出所有模板**：`GET /v1/template-configs`（返回模板列表，不包含具体内容）
- **获取模板详情**：`GET /v1/template-configs/:templateId`（返回包含渠道配置的模板详细信息）
- **删除模板**：`DELETE /v1/template-configs/:templateId`

### 模板状态

| 状态码 | 描述 |
|-------|--------|
| 1 | 待审核 |
| 2 | 已批准 |
| 3 | 被拒绝 |

### 渠道策略

使用 `|` 来定义发送渠道的回退顺序。例如：
- `"sms"` — 仅通过短信发送
- `"whatsapp|sms"` — 先尝试 WhatsApp，若失败则发送短信
- `"whatsapp|sms|email"` — 先尝试 WhatsApp，若失败则发送短信，再发送电子邮件

支持的渠道：`whatsapp`、`sms`、`voice`、`email`

### 验证代码配置

| 参数 | 范围 | 描述 |
|-------|-------|-------------|
| `verify_code_type` | 1–7 | 1=数字；2=小写字母；4=大写字母；组合形式：3=数字+小写字母 |
| `verify_code_len` | 4–10 | 密码长度 |
| `verify_code_ttl` | 1–10 | 代码的有效时间（以分钟为单位）。对于 WhatsApp，仅支持 1、5 或 10 分钟 |

## 回调配置

配置 Webhook URL 以接收实时发送状态、通知事件、消息响应和系统事件。

有关完整的回调数据结构、安全机制及事件类型的详细信息，请参阅 `references/callback-config.md`。

## SMPP 集成

有关基于 TCP 的 SMPP 协议集成（用于运营商级别的短信发送），请参阅 `references/smpp-guide.md`。

## 生成代码

当用户请求发送 OTP 或管理模板时，系统会生成相应的代码。默认使用 `curl`；用户也可以指定其他编程语言。支持的编程语言及工具包括：

- **curl** — 带有正确身份验证头的 Shell 命令
- **Python** — 使用 `requests` 库
- **Node.js** — 使用 `fetch` 或 `axios`
- **Java** — 使用 `HttpClient`
- **Go** — 使用 `net/http`

请务必包含身份验证头部并处理错误。如果用户尚未提供凭据，可以使用占位符 `YOUR_DEV_KEY` 和 `YOUR_DEV_SECRET`。

### Python 示例 — 发送 OTP 和验证 OTP

```python
import requests
import base64

DEV_KEY = "YOUR_DEV_KEY"
DEV_SECRET = "YOUR_DEV_SECRET"
BASE_URL = "https://otp.api.engagelab.cc"

auth_string = base64.b64encode(f"{DEV_KEY}:{DEV_SECRET}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_string}"
}

# Step 1: Send OTP
send_resp = requests.post(f"{BASE_URL}/v1/messages", headers=headers, json={
    "to": "+8618701235678",
    "template": {"id": "my-template", "language": "default"}
})
result = send_resp.json()
message_id = result["message_id"]

# Step 2: Verify OTP (after user enters the code)
verify_resp = requests.post(f"{BASE_URL}/v1/verifications", headers=headers, json={
    "message_id": message_id,
    "verify_code": "123456"
})
verification = verify_resp.json()
print(f"Verified: {verification['verified']}")
```