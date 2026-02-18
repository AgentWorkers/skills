---
name: email-webhook
description: 这是一个通用的接收器，用于接收通过 JSON Webhook 发送的电子邮件。它将收到的邮件信息保存到本地的 JSONL 文件中，以便代理程序进行后续处理。该接收器对邮件来源（Cloudflare、Mailgun 或自定义代理）没有特定要求，可以灵活适应不同的邮件发送方式。
metadata: {
  "author": "Skippy & Lucas (AI Commander)",
  "homepage": "https://aicommander.dev",
  "env": {
    "PORT": { "description": "Port to listen on (default: 19192).", "default": "19192" },
    "WEBHOOK_SECRET": { "description": "Secret token for webhook authentication (Bearer token). REQUIRED for startup." },
    "INBOX_FILE": { "description": "Filename for the JSONL inbox (default: inbox.jsonl). Path traversal protected.", "default": "inbox.jsonl" }
  },
  "openclaw": {
    "requires": { "bins": ["node"] },
    "install": [
      {
        "id": "npm-deps",
        "kind": "exec",
        "command": "npm install express",
        "label": "Install Node.js dependencies"
      }
    ]
  }
}
---
# 通用电子邮件 Webhook 接收器

该技能允许代理以标准化的 JSON Webhook 形式接收电子邮件。它提供了一个端点，可以与其他电子邮件到 Webhook 的服务提供商（如 Cloudflare Email Routing、Mailgun Inbound 或 SendGrid Inbound Parse）集成。

## 预期的 Webhook 结构

接收器期望收到一个具有以下 JSON 结构的 `POST` 请求：

```json
{
  "from": "sender@example.com",
  "to": "agent@yourdomain.com",
  "subject": "Hello world",
  "text": "The plain text body",
  "html": "<div>Optional HTML content</div>",
  "timestamp": "ISO-8601 string",
  "attachments": [
    {
      "filename": "document.pdf",
      "mimeType": "application/pdf",
      "content": "base64-encoded-string"
    }
  ]
}
```

## 安全性与设置

1. **启动接收器**：运行 `scripts/webhook_server.js` 文件。
2. **身份验证**：所有请求必须包含 `Authorization: Bearer <WEBHOOK_SECRET>` 标头。
3. **本地收件箱**：收到的邮件会被添加到工作区目录下的 `inbox.jsonl` 文件中。

## 实现示例：Cloudflare Worker

您可以在连接到 **Email Routing** 的 Cloudflare Worker 中使用以下代码将电子邮件推送到该接收器：

```javascript
import PostalMime from 'postal-mime';

export default {
  async email(message, env, ctx) {
    const rawEmail = await new Response(message.raw).arrayBuffer();
    const parser = new PostalMime();
    const parsedEmail = await parser.parse(rawEmail);

    const payload = {
      from: message.from,
      to: message.to,
      subject: parsedEmail.subject,
      text: parsedEmail.text,
      html: parsedEmail.html,
      timestamp: new Date().toISOString()
    };

    await fetch(env.WEBHOOK_URL, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.WEBHOOK_SECRET}`
      },
      body: JSON.stringify(payload)
    });
  }
}
```

## 工具

### 启动 Webhook 服务器
```bash
WEBHOOK_SECRET=my-strong-token INBOX_FILE=inbox.jsonl node scripts/webhook_server.js
```

## 运行时要求
需要安装 `express` 和 `node` 模块。