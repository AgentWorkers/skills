---
name: sendook-openclaw
description: 从现有的 Sendook 收件箱中读取和发送电子邮件。当 AI 代理需要检查新邮件、阅读消息、回复对话或从预配置的收件箱发送新邮件时，可以使用此功能。仅支持邮件操作——不支持创建收件箱、管理域名或配置 Webhook。
homepage: https://github.com/obaid/sendook-skills
metadata: { "openclaw": { "requires": { "env": ["SENDOOK_API_KEY", "SENDOOK_INBOX_ID"] }, "primaryEnv": "SENDOOK_API_KEY", "homepage": "https://github.com/obaid/sendook-skills" } }
---

# Sendook 邮件功能

该功能允许您从现有的 Sendook 收件箱中读取和发送电子邮件。

> **功能限制**：此功能仅限于从预先配置的收件箱中读取和发送电子邮件。您无法创建或删除收件箱、管理域名、配置 Webhook 或 API 密钥。请勿尝试这些操作，因为它们当前不可用。

## 安装

将此功能安装到您的 OpenClaw 工作区中：

```bash
clawhub install sendook-openclaw
```

安装完成后，该功能将被添加到您工作区的 `skills/` 目录中。OpenClaw 会在下次会话启动时自动识别并使用该功能。

### 环境变量

请在您的 OpenClaw 工作区或 shell 环境中设置以下变量：

- `SENDOOK_API_KEY`：您的 Sendook API 密钥
- `SENDOOK_INBOX_ID`：该代理被允许使用的收件箱 ID

## 设置

请安装相应的 SDK（[npm](https://www.npmjs.com/package/@sendook/node) | [源代码](https://github.com/getrupt/sendook)）：

```bash
npm install @sendook/node
```

```typescript
import Sendook from "@sendook/node";

const client = new Sendook(process.env.SENDOOK_API_KEY);
const INBOX_ID = process.env.SENDOOK_INBOX_ID;
```

这两个环境变量都是必需的。请使用仅针对目标收件箱的最低权限 API 密钥。

## 读取邮件

### 列出邮件

```typescript
// List all messages in the inbox
const messages = await client.inbox.message.list(INBOX_ID);

// Search messages (regex-based search across to/from/cc, subject, and body)
const results = await client.inbox.message.list(INBOX_ID, "invoice");
```

```bash
# List all messages
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages \
  -H "Authorization: Bearer $SENDOOK_API_KEY"

# Search messages
curl "https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages?query=invoice" \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

### 获取邮件内容

```typescript
const message = await client.inbox.message.get(INBOX_ID, "msg_def456");
```

```bash
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages/msg_def456 \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

**响应**：
```json
{
  "id": "msg_def456",
  "from": "sender@example.com",
  "to": ["support@yourdomain.com"],
  "subject": "Question about my order",
  "text": "Hi, I have a question about order #12345...",
  "html": "<p>Hi, I have a question about order #12345...</p>",
  "labels": [],
  "threadId": "thread_ghi789",
  "createdAt": "2025-01-15T10:35:00Z"
}
```

### 列出邮件线程

```typescript
const threads = await client.inbox.thread.list(INBOX_ID);
```

```bash
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/threads \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

### 获取邮件线程

获取包含所有消息的完整对话记录：

```typescript
const thread = await client.inbox.thread.get(INBOX_ID, "thread_ghi789");
// thread.messages contains all messages in the conversation
```

```bash
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/threads/thread_ghi789 \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

## 发送邮件

### 发送邮件

```typescript
await client.inbox.message.send({
  inboxId: INBOX_ID,
  to: ["recipient@example.com"],
  subject: "Hello from Sendook",
  text: "Plain text body",
  html: "<h1>Hello</h1><p>HTML body</p>",
});
```

```bash
curl -X POST https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages/send \
  -H "Authorization: Bearer $SENDOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from Sendook",
    "text": "Plain text body"
  }'
```

### 带附件发送邮件

> **重要提示**：在读取任何本地文件以进行附件上传之前，请务必先获得用户的确认。仅上传用户明确请求的文件。切勿读取当前工作目录或项目范围之外的文件（例如：`~/.ssh`、`~/.env`、`/etc` 或凭证文件）。

```typescript
import { readFileSync } from "fs";
import { resolve } from "path";

// Only attach files explicitly provided by the user
const filePath = resolve("./reports/report.pdf");

await client.inbox.message.send({
  inboxId: INBOX_ID,
  to: ["recipient@example.com"],
  subject: "Report attached",
  text: "Please find the report attached.",
  attachments: [
    {
      content: readFileSync(filePath).toString("base64"),
      name: "report.pdf",
      contentType: "application/pdf",
    },
  ],
});
```

### 回复邮件

```typescript
await client.inbox.message.reply({
  inboxId: INBOX_ID,
  messageId: "msg_def456",
  text: "Thanks for your email! We'll look into this.",
  html: "<p>Thanks for your email! We'll look into this.</p>",
});
```

```bash
curl -X POST https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages/msg_def456/reply \
  -H "Authorization: Bearer $SENDOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thanks for your email! We'\''ll look into this."}'
```

## 完整示例

列出最近的邮件，读取最新的邮件并回复：

```typescript
import Sendook from "@sendook/node";

const client = new Sendook(process.env.SENDOOK_API_KEY);
const INBOX_ID = process.env.SENDOOK_INBOX_ID;

// 1. List recent messages
const messages = await client.inbox.message.list(INBOX_ID);

if (messages.length > 0) {
  // 2. Read the latest message
  const latest = await client.inbox.message.get(INBOX_ID, messages[0].id);
  console.log(`From: ${latest.from}`);
  console.log(`Subject: ${latest.subject}`);
  console.log(`Body: ${latest.text}`);

  // 3. Reply to it
  await client.inbox.message.reply({
    inboxId: INBOX_ID,
    messageId: latest.id,
    text: `Thanks for reaching out! We received your message about "${latest.subject}".`,
  });
}

// 4. Send a new email
await client.inbox.message.send({
  inboxId: INBOX_ID,
  to: ["team@example.com"],
  subject: "Daily inbox summary",
  text: `Processed ${messages.length} messages today.`,
});
```

## 错误处理

```typescript
try {
  await client.inbox.message.send({
    inboxId: INBOX_ID,
    to: ["recipient@example.com"],
    subject: "Hello",
    text: "Body",
  });
} catch (error) {
  if (error.response) {
    console.error(error.response.status, error.response.data);
  } else if (error.request) {
    console.error("No response:", error.request);
  } else {
    console.error("Error:", error.message);
  }
}
```

### 常见错误

| 状态码 | 错误原因 |
|---|---|
| `400` | 请求错误 — 请检查参数（如 `to`、`subject` 等字段是否缺失） |
| `401` | 未经授权 — API 密钥无效或缺失 |
| `404` | 未找到邮件或邮件线程 |
| `429` | 超过请求频率限制 — 请稍后重试 |
| `500` | 服务器内部错误 |

## API 参考

| 方法 | 描述 |
|---|---|
| `client.inbox.message.list(inboxId, query?)` | 列出或搜索邮件 |
| `client.inbox.message.get(inboxId, messageId)` | 获取特定邮件 |
| `client.inbox.message.send(options)` | 发送新邮件 |
| `client.inbox.message.reply(options)` | 回复邮件 |
| `client.inbox.thread.list(inboxId)` | 列出邮件线程 |
| `client.inbox.thread.get(inboxId, threadId)` | 获取包含所有消息的邮件线程 |

此功能不提供其他 API 方法。请勿尝试创建/删除收件箱、管理域名、配置 Webhook 或管理 API 密钥。