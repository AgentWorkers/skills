---
name: lnemail
description: 如何使用 Bitcoin Lightning 支付在 LNemail.net 上设置并使用匿名电子邮件账户？当代理人需要电子邮件功能（用于两步验证、接收通知或进行无需身份验证（KYC）或个人信息的通信时，可以使用此方法。
---
# LNemail

通过 Lightning Network 提供匿名电子邮件账户。无需进行任何身份验证（KYC），也无需提供电子邮件地址——只需使用比特币支付即可注册。

## 概述

LNemail 提供每年 1000 萨特的完全功能的电子邮件地址。非常适合需要以下功能的代理：
- 接收双重身份验证（2FA）验证码
- 进行匿名通信
- 接收来自 Bitcoin/Lightning 服务的通知
- 无需提供身份信息即可通过 API 访问电子邮件服务

## 快速入门

### 1. 创建电子邮件账户

创建一个用于注册电子邮件账户的 Lightning 发票：

```bash
# Create the account (returns payment hash)
curl -X POST https://lnemail.net/api/v1/email

# Response:
# {
#   "payment_hash": "abc123...",
#   "amount": 1000,
#   "currency": "SATS"
# }
```

### 2. 使用 Lightning 进行支付

使用任何 Bitcoin Lightning Network 钱包（例如 Alby CLI）支付该发票：

```bash
# Get the invoice from payment status endpoint
curl -X GET https://lnemail.net/api/v1/payment/PAYMENT_HASH

# Response when pending:
# {
#   "payment_hash": "abc123...",
#   "status": "pending",
#   "lightning_invoice": "lnbc10u1pj..."
# }
```

### 3. 获取账户凭据

支付确认后（大约几秒钟），再次检查账户状态：

```bash
curl -X GET https://lnemail.net/api/v1/payment/PAYMENT_HASH

# Response when paid:
# {
#   "payment_hash": "abc123...",
#   "status": "paid",
#   "email": "abc123@lnemail.net",
#   "access_token": "eyJhbG..."
# }
```

**请保存这些凭据！** 将它们安全地存储在 `~/.lnemail/credentials.json` 文件中。

## 使用您的电子邮件账户

### 查看收件箱

```bash
curl -X GET https://lnemail.net/api/v1/emails \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response:
# [
#   {
#     "id": "msg_123",
#     "from": "sender@example.com",
#     "subject": "Your 2FA Code",
#     "received_at": "2024-01-15T10:30:00Z",
#     "has_attachments": false
#   }
# ]
```

### 阅读电子邮件内容

```bash
curl -X GET https://lnemail.net/api/v1/emails/EMAIL_ID \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response:
# {
#   "id": "msg_123",
#   "from": "sender@example.com",
#   "to": "abc123@lnemail.net",
#   "subject": "Your 2FA Code",
#   "body": "Your verification code is: 123456",
#   "received_at": "2024-01-15T10:30:00Z"
# }
```

**注意：** 为保障安全，电子邮件内容会被去除 HTML 格式，仅以纯文本形式显示。

### 发送电子邮件

发送电子邮件需要支付一定的费用（每封邮件约 100 萨特）：

```bash
# Create send request
curl -X POST https://lnemail.net/api/v1/email/send \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "recipient": "example@example.com",
    "subject": "Hello",
    "body": "Message content here"
  }'

# Response:
# {
#   "payment_hash": "def456...",
#   "amount": 100,
#   "currency": "SATS"
# }
```

支付发票费用后，再次检查账户状态：

```bash
curl -X GET https://lnemail.net/api/v1/email/send/status/PAYMENT_HASH

# Response when paid:
# {
#   "payment_hash": "def456...",
#   "status": "paid",
#   "message_id": "msg_sent_789"
# }
```

## API 参考

| API 端点 | 方法 | 认证方式 | 描述 |
|----------|--------|------|-------------|
| `/email` | POST | 无需认证 | 创建账户（返回支付哈希值） |
| `/payment/{hash}` | GET | 无需认证 | 检查账户支付状态 |
| `/emails` | GET | 无需认证 | 查看收件箱中的邮件 |
| `/emails/{id}` | GET | 无需认证 | 查看邮件内容 |
| `/email/send` | POST | 无需认证 | 创建发送请求（返回支付哈希值） |
| `/email/send/status/{hash}` | GET | 无需认证 | 检查邮件发送的支付状态 |

## 存储建议

将凭据保存在 `~/.lnemail/credentials.json` 文件中：

```json
{
  "email": "abc123@lnemail.net",
  "access_token": "eyJhbG..."
}
```

**注意：** `access_token` 是进行后续操作所需的唯一凭据。`payment_hash` 仅在初始设置时用于检查支付状态，获取到 `access_token` 后即可丢弃。

## 价格

| 服务 | 费用 |
|---------|------|
| 电子邮件账户（1 年） | 1000 萨特 |
| 发送电子邮件 | 约 100 萨特 |
| 接收电子邮件 | 免费 |

## 限制

- 仅支持纯文本邮件（HTML 格式的内容会被去除）
- 支持发送较小的附件
- 每封出站邮件费用为 100 萨特
- 账户自支付之日起有效期为 1 年

## 使用场景

- **接收 2FA 验证码：** 可靠的电子邮件发送方式
- **服务通知：** 收到来自 Bitcoin/Lightning 服务的提醒
- **匿名注册：** 需要电子邮件地址但无需提供身份信息的服务
- **代理间通信：** 代理之间通过电子邮件进行程序化通信

## 参考资料

- **LNemail：** https://lnemail.net
- **API 文档：** https://lnemail.net（请访问首页查看完整文档）
- **认证方式：** 在 `Authorization` 标头中使用 bearer token 进行认证