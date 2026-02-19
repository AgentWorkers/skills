---
name: resend-inbound
description: >
  **使用场景：**  
  在接收包含“Resend”功能的电子邮件时，可用于配置入站域名、处理 `email.received` Webhook、检索邮件内容/附件，或转发收到的邮件。
inputs:
    - name: RESEND_API_KEY
      description: Resend API key for retrieving email content and attachments. Get yours at https://resend.com/api-keys
      required: true
    - name: RESEND_WEBHOOK_SECRET
      description: Webhook signing secret for verifying inbound email event payloads. Found in the Resend dashboard under Webhooks.
      required: true
---
# 接收电子邮件并重新发送

## 概述

该功能会为您的域名接收传入的电子邮件，并将相关Webhook事件发送到您的终端点。**Webhook仅包含元数据**——您需要通过单独的API来获取电子邮件的正文和附件内容。

## SDK版本要求

此功能需要Resend SDK的以下功能：Webhook验证（`webhooks.verify()`）和电子邮件接收（`emails.receiving.get()`）。请始终安装最新版本的SDK。如果项目中已安装了Resend SDK，请检查版本并在需要时进行升级。

| 语言 | 包名 | 最低版本 |
|----------|---------|-------------|
| Node.js | `resend` | >= 6.9.2 |
| Python | `resend` | >= 2.21.0 |
| Go | `send-go/v3` | >= 3.1.0 |
| Ruby | `resend` | >= 1.0.0 |
| PHP | `send/resend-php` | >= 1.1.0 |
| Rust | `send-rs` | >= 0.20.0 |
| Java | `send-java` | >= 4.11.0 |
| .NET | `Resend` | >= 0.2.1 |

有关完整的安装命令，请参阅`send-email`功能的[安装指南](../send-email/references/installation.md)。

## 快速入门

1. **配置接收域名**：使用Resend提供的`.resend.app`域名，或为自定义域名添加MX记录。
2. **设置Webhook**：订阅`email.received`事件。
3. **获取内容**：调用接收API获取邮件正文，调用附件API获取文件内容。

## 域名设置

### 选项1：Resend管理的域名（最快）

使用自动生成的地址：`<anything>@<your-id>.resend.app`

无需进行DNS配置。您可以在控制面板 → 电子邮件 → 接收 → “接收地址”中找到该地址。

### 选项2：自定义域名

为`<anything>@yourdomain.com`添加MX记录以接收邮件。

| 设置 | 值 |
|---------|-------|
| **类型** | MX |
| **主机** | 您的域名或子域名 |
| **值** | 在Resend控制面板中提供的值 |
| **优先级** | 优先级越低越好（数值越小优先级越高，但通常只使用10的倍数） |

**重要提示：**您的MX记录必须具有最低的优先级，否则邮件将不会被路由到Resend。

### 子域推荐

如果您已经设置了MX记录（例如，Google Workspace、Microsoft 365）：

| 方法 | 结果 |
|----------|--------|
| **使用子域名**（推荐） | `support.acme.com` → 路由到Resend，`acme.com` → 保留现有邮件服务 |
| **使用根域名** | 所有邮件都会被路由到Resend（可能导致现有邮件服务中断） |

**注意：**如果您在根域名上设置了Resend来接收邮件，那么所有邮件都会被路由到Resend，而不会被发送到其他邮箱。因此，建议使用子域名。

## Webhook设置

### 订阅`email.received`事件

在控制面板 → Webhooks → 添加Webhook → 选择`email.received`。

对于本地开发，可以使用隧道技术（如ngrok或VS Code的端口转发）：

```bash
ngrok http 3000
# Use https://abc123.ngrok.io/api/webhook as endpoint
```

### Webhook数据结构

**重要提示：**Webhook数据仅包含元数据，不包含邮件正文或附件内容。

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

### 验证Webhook签名

务必验证Webhook签名，以防止伪造事件：

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

## 获取电子邮件内容

Webhook不包含邮件正文和头部信息。您需要通过调用接收API来获取这些信息：

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

**为什么这样设计？** 无服务器环境通常有请求体大小的限制。将内容获取过程分离出来可以更好地处理大型邮件和附件。

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

**重要提示：**`download_url`在1小时后失效。如需获取新的下载链接，请再次调用API。

## 转发电子邮件

以下是接收并转发带附件的电子邮件的完整流程：

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

所有发送到您域名的电子邮件都会到达同一个Webhook。您可以根据`to`字段来路由邮件：

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

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| 期望从Webhook数据中获取邮件正文 | Webhook仅包含元数据——请调用`resend.emails.receiving.get()`来获取正文 |
| MX记录的优先级过高 | 确保Resend的MX记录具有最低的优先级 |
| 在现有邮件服务中使用根域名设置MX记录 | 使用子域名以避免干扰现有邮件服务 |
| 使用过期的下载链接 | 下载链接在1小时后失效——请再次调用附件API获取新的链接 |
| 未验证Webhook签名 | 必须进行签名验证——攻击者可能会发送伪造的事件 |
| 未返回200 OK状态码 | 如果响应状态码不是200，Resend会尝试重新发送 |

## 存储注意事项

即使以下情况发生，Resend仍会存储接收到的电子邮件：
- Webhook尚未配置
- Webhook端点暂时不可用

您可以在控制面板 → 电子邮件 → 接收选项卡中查看所有接收到的电子邮件。