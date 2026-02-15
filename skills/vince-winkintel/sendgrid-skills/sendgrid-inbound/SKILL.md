---
name: sendgrid-inbound
description: 通过 SendGrid 的 Inbound Parse Webhook 接收传入的电子邮件。内容包括 MX 记录的设置、Webhook 的配置、邮件内容的解析、附件的处理以及安全最佳实践。适用于需要以编程方式接收电子邮件、解析邮件内容、处理邮件回复或构建邮件到应用程序的工作流程的场景。该功能会在电子邮件被接收时触发，涉及的关键术语包括：MX 记录（MX record）、Webhook（Webhook）、邮件解析（email parsing）、邮件到应用程序的传输（email to app）等。
---

# 使用 SendGrid 接收电子邮件（Inbound Parse）

## 概述

SendGrid 的 **Inbound Parse Webhook** 会接收指定主机名/子域名的电子邮件，解析邮件内容后，以 `multipart/form-data` 的格式将其发送到您的 Webhook。

**与 Resend 的主要区别：**
- SendGrid 会直接将解析后的完整邮件内容（包括文本、HTML、头部信息及附件）发送到您的 Webhook。
- Inbound Parse 不提供官方的签名验证功能（与 SendGrid Event Webhook 不同），因此您需要自行保护您的 Webhook 端点。

## 快速入门

### 首先验证您的设置
```bash
# Check MX record and test webhook
../scripts/verify-inbound-setup.sh parse.example.com https://webhook.example.com/parse
```

**然后进行配置：**

1. 为指定的主机名（建议使用子域名）创建一个指向 `mx.sendgrid.net` 的 MX 记录。
2. 在 SendGrid 控制台中配置 Inbound Parse，设置接收域名和目标 URL。
3. 处理 Webhook 请求：解析 `multipart/form-data` 数据，提取文本、HTML、头部信息和附件内容。
4. 保护 Webhook 端点安全（使用基本认证、允许列表、限制请求大小等）。

### 解析 Webhook 的数据内容
```bash
# Debug or test payload parsing
node ../scripts/parse-webhook-payload.js < payload.txt
```

## DNS / MX 设置

为指定的主机名创建一个 MX 记录：

| 设置 | 值 |
|---------|-------|
| **类型** | MX |
| **主机** | `parse`（或其他子域名） |
| **优先级** | 10 |
| **值** | `mx.sendgrid.net` |

**建议：** 使用子域名以避免影响现有的邮件服务提供商（例如：`parse.example.com`）。

## Inbound Parse 配置

在 SendGrid 控制台中：
- 进入 **Settings → Inbound Parse**，
- 设置 **接收域名** 和 **目标 URL**，
- 示例接收地址：`anything@parse.example.com`。

## Webhook 数据内容（multipart/form-Data）

SendGrid 发送的数据包括：
- `from`、`to`、`cc`、`subject`
- `text`、`html`
- `headers`（原始邮件头部信息）
- `envelope`（包含 SMTP 信封数据的 JSON 对象）
- `attachments`（附件数量）
- `attachmentX`（附件内容；文件名包含在数据中）

**示例字段**（具体取决于配置）：
```
from: "Alice <alice@example.com>"
to: "support@parse.example.com"
subject: "Help"
text: "Plain text body"
html: "<p>HTML body</p>"
headers: "...raw headers..."
envelope: {"to":["support@parse.example.com"],"from":"alice@example.com"}
attachments: 2
attachment1: <file>
attachment2: <file>
```

## 如何保护 Inbound Parse Webhook 的安全？

```
Security requirements?
├─ Public endpoint (internet-facing)
│  └─ Basic auth + IP allowlist + size limits + content validation
├─ Internal only (VPN/private network)
│  └─ Network ACL + basic auth
└─ High security (PCI/HIPAA)
   └─ mTLS + custom signature verification + request logging
```

**最低限度的安全措施（针对公共 Webhook 端点）：**
- 在 Webhook URL 上启用基本认证。
- 设置 IP 允许列表（仅允许来自 SendGrid 指定的 IP 范围的请求）。
- 限制请求大小（通常为 10–25 MB）。
- 验证请求内容类型（确保为 `multipart/form-data`）。

**额外的安全措施：**
- 对每个发送者的请求进行速率限制。
- 过滤垃圾邮件并验证发送者身份。
- 在存储前对 HTML 内容进行清理和消毒。
- 对附件进行病毒扫描。

## 安全最佳实践

由于 Inbound Parse 不提供签名验证功能，因此请将接收到的数据视为不可信的：
- 在 Webhook URL 上强制使用基本认证。
- 根据需要设置发送者域名的允许列表。
- 限制请求大小，以防止滥用。
- 验证请求内容类型（确保为 `multipart/form-data`）。
- 在未进行清理处理之前，不要执行或渲染 HTML 内容。
- 如果将数据转发到 AI 系统，要防止代码注入攻击。

## 常见问题及解决方法

**MX 记录无法解析：**
- DNS 更新可能需要 24–48 小时。
- 使用 `dig parse.example.com MX` 或 `nslookup -type=MX parse.example.com` 命令验证 MX 记录是否正确配置。
- 检查主机名或值的拼写是否正确。

**Webhook 未接收到邮件：**
- 确保 Webhook URL 可以被外部访问（使用 curl 命令测试）。
- 检查防火墙规则和安全组设置。
- 确保 Webhook 端点返回 200 OK 响应。
- 查看 SendGrid 控制台中的 Inbound Parse 日志。

**数据解析错误：**
- 确保您正确处理了 `multipart/form-data` 数据。
- 使用适当的解析库（例如 Node.js 的 `multer`）来解析请求体。
- 记录原始请求内容以便调试。

**附件过大：**
- 配置 Web 服务器的文件大小限制（例如 Nginx 的 `client_max_body_size`）。
- 在应用程序中设置请求大小限制（例如 Express 的 `limit`）。
- SendGrid 的默认限制是每封邮件最多 30 MB。

**未经授权的 Webhook 访问：**
- 在 Webhook URL 上启用基本认证。
- 仅允许来自 SendGrid 指定的 IP 范围的请求。
- 仅使用 HTTPS 协议。
- 监控异常访问行为。

## 相关资源

- [参考文档：webhook-examples.md](references/webhook-examples.md)
- [参考文档：best-practices.md](references/best-practices.md)

## 相关技能

**发送自动回复：**
- 可参考 `send-email` 文档了解如何发送自动回复或确认邮件。
- 常见应用场景：自动回复支持工单、发送确认邮件等。