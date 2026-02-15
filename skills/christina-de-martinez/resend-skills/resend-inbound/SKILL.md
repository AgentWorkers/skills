---
name: resend-inbound
description: **使用场景：**  
在接收包含“Resend”功能的电子邮件时，该功能可用于配置入站域名、处理 `email.received` Webhook、检索电子邮件内容/附件，或转发收到的电子邮件。
---

# 接收邮件并重新发送

## 概述

Resend 会为您的域名处理传入的邮件，并将 Webhook 事件发送到您的端点。**Webhook 仅包含元数据**——您需要调用单独的 API 来获取邮件正文和附件。

## 快速入门

1. **配置接收域名**：使用 Resend 的 `.resend.app` 域名，或为自定义域名添加 MX 记录。
2. **设置 Webhook**：订阅 `email.received` 事件。
3. **获取邮件内容**：调用 Receiving API 获取邮件正文，调用 Attachments API 获取附件文件。

## 域名设置

### 选项 1：Resend 管理的域名（最快）

使用自动生成的地址：`<anything>@<your-id>.resend.app`

无需进行 DNS 配置。您可以在仪表板 → 邮件 → 接收 → “接收地址” 中找到该地址。

### 选项 2：自定义域名

为 `<anything>@yourdomain.com` 添加 MX 记录以接收邮件。

| 设置 | 值 |
|---------|-------|
| **类型** | MX |
| **主机** | 您的域名或子域名 |
| **值** | 在 Resend 仪表板中提供 |
| **优先级** | 优先级越低（数字越小）越好（在冲突情况下优先级越低），但通常只使用 10 的倍数 |

**重要提示：** 您的 MX 记录必须具有最低的优先级，否则邮件将不会被路由到 Resend。

### 子域名推荐

如果您已经有了 MX 记录（例如 Google Workspace、Microsoft 365）：

| 方法 | 结果 |
|----------|--------|
| **使用子域名**（推荐） | `support.acme.com` → 转发到 Resend，`acme.com` → 继续发送到现有服务 |
| **使用根域名** | 所有邮件都会被转发到 Resend（可能会中断现有的邮件服务） |

**注意：** 如果您在根域名上设置 Resend 来接收邮件，*所有* 邮件流量都将被路由到 Resend，而不会发送到其他邮箱。因此，建议使用子域名。

## Webhook 设置

### 订阅 `email.received` 事件

在仪表板 → Webhooks → 添加 Webhook → 选择 `email.received`。

对于本地开发，可以使用隧道技术（如 ngrok 或 VS Code 的端口转发）：

```bash
ngrok http 3000
# Use https://abc123.ngrok.io/api/webhook as endpoint
```

### Webhook 载荷结构

**重要提示：** 载荷仅包含元数据，不包含邮件正文或附件内容。

```json
{
  "type": "email.received",
  "created_at": "2024-02-22T23:41:12.126Z",
  "data": {
    "email_id": "a1b2c3d4-...",
    "from": "sender@example.com",
    "to": ["support@acme.com"],
    "cc": [],
    "bcc": [],
    "subject": "Question about my order",
    "attachments": [
      {
        "id": "att_abc123",
        "filename": "receipt.pdf",
        "content_type": "application/pdf"
      }
    ]
  }
}
```

### 验证 Webhook 签名

始终验证 Webhook 签名，以防止伪造事件：

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: Request) {
  const payload = await req.text();

  const event = resend.webhooks.verify({
    payload,
    headers: {
      'svix-id': req.headers.get('svix-id'),
      'svix-timestamp': req.headers.get('svix-timestamp'),
      'svix-signature': req.headers.get('svix-signature'),
    },
    secret: process.env.RESEND_WEBHOOK_SECRET,
  });

  if (event.type === 'email.received') {
    // Process the email
  }

  return new Response('OK', { status: 200 });
}
```

## 获取邮件内容

Webhook 不包含邮件正文和头部信息。您需要调用 Receiving API 来获取这些信息：

```typescript
if (event.type === 'email.received') {
  const { data: email } = await resend.emails.receiving.get(
    event.data.email_id
  );

  console.log(email.html);    // HTML body
  console.log(email.text);    // Plain text body
  console.log(email.headers); // Email headers
}
```

**为什么这样设计？** 无服务器环境通常对请求正文的大小有限制。将内容获取过程分离出来可以更好地处理大型邮件和附件。

## 处理附件

### 获取附件元数据和下载链接

```typescript
const { data: attachments } = await resend.emails.receiving.attachments.list({
  emailId: event.data.email_id,
});

for (const attachment of attachments) {
  console.log(attachment.filename);
  console.log(attachment.download_url);  // Valid for 1 hour
  console.log(attachment.expires_at);
}
```

### 下载附件内容

```typescript
const response = await fetch(attachment.download_url);
const buffer = await response.arrayBuffer();

// Save to storage, process, etc.
await saveToStorage(attachment.filename, buffer);
```

**重要提示：** `download_url` 在 1 小时后失效。如果需要，请再次调用 API 以获取新的下载链接。

## 转发邮件

以下是接收并转发带有附件的邮件的完整流程：

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: Request) {
  const payload = await req.text();
  const event = resend.webhooks.verify({ /* ... */ });

  if (event.type === 'email.received') {
    // 1. Get email content
    const { data: email } = await resend.emails.receiving.get(
      event.data.email_id
    );

    // 2. Get attachments (if any)
    const { data: attachmentList } = await resend.emails.receiving.attachments.list({
      emailId: event.data.email_id,
    });

    // 3. Download and encode attachments
    const attachments = await Promise.all(
      attachmentList.map(async (att) => {
        const res = await fetch(att.download_url);
        const buffer = Buffer.from(await res.arrayBuffer());
        return {
          filename: att.filename,
          content: buffer.toString('base64'),
        };
      })
    );

    // 4. Forward the email
    await resend.emails.send({
      from: 'Support System <system@acme.com>',
      to: ['team@acme.com'],
      subject: `Fwd: ${email.subject}`,
      html: email.html,
      text: email.text,
      attachments,
    });
  }

  return new Response('OK', { status: 200 });
}
```

## 根据收件人路由邮件

所有发送到您域名的邮件都会到达同一个 Webhook。您可以根据 `to` 字段来路由邮件：

```typescript
if (event.type === 'email.received') {
  const recipient = event.data.to[0];

  if (recipient.includes('support@')) {
    await handleSupportEmail(event.data);
  } else if (recipient.includes('billing@')) {
    await handleBillingEmail(event.data);
  } else {
    await handleUnknownEmail(event.data);
  }
}
```

## 常见错误

| 错误 | 修复方法 |
|---------|-----|
| 期望在 Webhook 载荷中获取邮件正文 | Webhook 仅包含元数据——请调用 `resend.emails.receiving.get()` 来获取正文 |
| MX 记录的优先级过高 | 确保 Resend 的 MX 记录具有最低的优先级 |
| 在现有邮件服务使用的根域名上添加 MX 记录 | 使用子域名以避免干扰现有邮件服务 |
| 使用过期的下载链接 | 下载链接在 1 小时后失效——请再次调用附件 API 以获取新的链接 |
| 未验证 Webhook 签名 | 必须始终验证签名，以防止攻击者发送伪造事件 |
| 忘记返回 200 OK 状态码 | 如果响应状态码不是 200，Resend 会尝试重新发送 |

## 存储注意事项

即使以下情况发生，Resend 也会保留接收到的邮件：
- Webhook 尚未配置
- Webhook 端点不可用

您可以在仪表板 → 邮件 → 接收 页面查看所有接收到的邮件。