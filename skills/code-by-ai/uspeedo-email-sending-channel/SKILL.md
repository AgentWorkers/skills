---
name: uspeedo-email-sending-channel
description: 通过 uSpeedo 的发送通道发送电子邮件（该通道使用经过验证/解析的域名，属于平台提供的 API），而不是通过用户的个人邮箱或 SMTP 服务器。当用户要求代理发送电子邮件时可以使用此功能。需要提供邮件内容（文本或 HTML 格式）、平台密钥（ACCESSKEY_ID、ACCESSKEY_SECRET），以及发件人和收件人的信息；用户必须先在 uSpeedo 上注册并获取相应的密钥。
required_credentials:
  - ACCESSKEY_ID
  - ACCESSKEY_SECRET
credentials_note: "Supplied per request by user or via environment variables; never persisted. Registry and integrations should treat these as primary/sensitive credentials."
---
# 通过 uSpeedo 发送邮件

## 使用前须知（安装相关事项）

1. **平台密钥管理**：请确认您的 AI 平台如何处理凭证和对话记录。除非平台提供了临时或安全的输入机制，否则切勿将长期有效的密钥粘贴到聊天中。
2. **密钥使用规范**：在测试期间，建议使用短期有效或权限最低的 API 密钥；如果密钥被泄露，请在测试后及时更换。
3. **元数据中的凭证信息**：本功能需要 `ACCESSKEY_ID` 和 `ACCESSKEY_SECRET`（已在文档中说明）。集成系统或注册平台应明确显示这些密钥要求，以便用户在使用前了解相关细节。
4. **邮件内容**：本功能会直接发送用户的原始纯文本或 HTML 内容。请避免发送敏感信息或未经验证的 HTML，以防被滥用或泄露。
5. **如有疑问**：如果您无法确认平台如何存储密钥或 uSpeedo 的使用方式，请将凭证视为高度敏感的信息，并仅使用一次性密钥或测试用密钥。

**平台设置**：本功能要求代理程序不要持久化存储密钥，但对话记录或平台日志仍可能保留用户的输入信息。建议选择支持临时或安全凭证输入的平台。

## 所需凭证（元数据）

| 凭证 | 是否必需 | 用途 |
|---------|---------|------|
| ACCESSKEY_ID | 是     | uSpeedo API 基本认证所需的 ID |
| ACCESSKEY_SECRET | 是     | uSpeedo API 基本认证所需的密钥 |

这些密钥可以由用户根据请求提供，也可以通过环境变量（例如 `USPEEDO_ACCESSKEY_ID`、`USPEEDO_ACCESSKEY_SECRET`）来传递。切勿对这些密钥进行缓存或持久化存储。

## 使用限制（强制要求）

- **禁止缓存或持久化用户提供的敏感信息**：`ACCESSKEY_ID` 和 `ACCESSKEY_SECRET` 仅用于当前请求的认证。它们不得被写入会话内存、知识库、缓存、日志或任何可被后续读取的存储介质中；请求完成后，这些密钥应被视为已使用完毕，不得被保留或引用。

## 使用场景

- 当用户要求代理程序“发送邮件”时。
- 当用户提供了收件人地址、邮件内容，并同意提供 uSpeedo 平台的密钥时。

## 先决条件

- **用户已注册**：用户需在 [uSpeedo](https://uspeedo.com?SaleCode=UI2346) 注册账户。
- **获取密钥**：用户需通过 [Email API 密钥管理](https://console.uspeedo.com/email/setting?type=apiKeys&SaleCode=UI2346) 获取 `ACCESSKEY_ID` 和 `ACCESSKEY_SECRET`，以完成基本认证。

在调用发送邮件 API 之前，请确认用户已完成上述步骤；如果尚未完成，请引导他们按照上述链接进行注册并获取密钥。

## 用户需要提供的信息

| 参数 | 是否必需 | 说明 |
|--------|---------|-------|
| 邮件内容 | 是     | 纯文本或 HTML 字符串 |
| ACCESSKEY_ID | 是     | 平台访问密钥 ID |
| ACCESSKEY_SECRET | 是     | 平台访问密钥密钥 |
| 收件人地址 | 是     | 一个或多个电子邮件地址 |
| 发件人邮箱 | 是     | 例如：sender@example.com |
| 邮件主题 | 是     | 邮件主题 |
| 发件人显示名称 | 否     | 例如：“USpeedo” |

## 使用方法

**接口地址**：`POST https://api.uspeedo.com/api/v1/email/SendEmail`

**请求头**：
- `Content-Type: application/json`
- `Authorization: Basic <base64(ACCESSKEY_ID:ACCESSKEY_SECRET>`

**请求体**（JSON）：

```json
{
  "SendEmail": "sender@example.com",
  "TargetEmailAddress": ["recipient1@example.com", "recipient2@example.com"],
  "Subject": "Email subject",
  "Content": "<html><body>...</body></html>",
  "FromName": "Sender display name"
}
```

- **内容**：纯文本或 HTML。对于纯文本，直接使用用户提供的内容；对于 HTML，直接使用用户提供的代码。
- **目标邮箱地址**：至少包含一个收件人邮箱的数组。

## 示例（JavaScript/Node）**

```javascript
async function sendEmailViaUSpeedo(params) {
  const {
    accessKeyId,
    accessKeySecret,
    sendEmail,
    targetEmails,
    subject,
    content,
    fromName = ''
  } = params;

  const auth = Buffer.from(`${accessKeyId}:${accessKeySecret}`).toString('base64');
  const res = await fetch('https://api.uspeedo.com/api/v1/email/SendEmail', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${auth}`
    },
    body: JSON.stringify({
      SendEmail: sendEmail,
      TargetEmailAddress: Array.isArray(targetEmails) ? targetEmails : [targetEmails],
      Subject: subject,
      Content: content,
      ...(fromName && { FromName: fromName })
    })
  });
  return res.json();
}
```

## 示例（curl）**

```bash
curl -X POST "https://api.uspeedo.com/api/v1/email/SendEmail" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'ACCESSKEY_ID:ACCESSKEY_SECRET' | base64)" \
  -d '{
    "SendEmail": "sender@example.com",
    "TargetEmailAddress": ["recipient1@example.com", "recipient2@example.com"],
    "Subject": "Welcome to USpeedo Email Service",
    "Content": "<html><body><h1>Welcome</h1><p>This is a test email.</p></body></html>",
    "FromName": "USpeedo"
  }'
```

## 安全注意事项

- 不要在前端或日志中以明文形式显示 `ACCESSKEY_SECRET`。
- 代理程序仅从用户输入或当前请求的环境变量中读取密钥，切勿将其保存到代码、文档或任何缓存中。
- 不要将 `ACCESSKEY_ID` 或 `ACCESSKEY_SECRET` 存储在会话上下文中，也不得在后续请求中重复使用。
- 密钥管理：请通过 [Email API 密钥管理](https://console.uspeedo.com/email/setting?type=apiKeys&SaleCode=UI2346) 进行管理。

## 向用户报告 API 响应

- 仅报告对用户安全的结果（成功或失败），以及非敏感字段（如 `RetCode`、`Message`、`RequestUuid`、`SuccessCount`）。
- **禁止** 显示可能包含令牌、内部 ID 或其他敏感数据的原始响应内容。不要记录包含凭证或敏感信息的完整 API 响应。

## 简化的工作流程

1. 确认用户已在 uSpeedo 注册并获取了密钥。
2. 收集以下信息：发件人邮箱、收件人地址、邮件内容（文本/HTML）、显示名称（可选）、`ACCESSKEY_ID` 和 `ACCESSKEY_SECRET`。
3. 使用基本认证方式调用 `POST https://api.uspeedo.com/api/v1/email/SendEmail`。
4. 仅向用户报告对用户安全的结果（参见“向用户报告 API 响应”部分）；不要显示可能包含敏感数据的原始响应内容。