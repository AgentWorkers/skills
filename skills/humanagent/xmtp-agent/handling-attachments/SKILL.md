---
name: handling-attachments
description: XMTP代理的文件附件处理功能：适用于发送或接收图片、文件或任何加密的远程附件时使用。该功能会在文件上传、图片发送或远程附件处理过程中被触发。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP附件

使用加密的远程附件来处理文件附件。文件会在本地被加密，然后上传到您的存储提供商，并作为远程附件消息发送。

## 适用场景

在以下情况下请参考这些指南：
- 从代理发送文件或图片
- 接收和下载附件
- 实现自定义的上传存储机制
- 处理加密文件传输

## 规则类别（按优先级排序）

| 优先级 | 类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 发送 | 关键性 | `send-` |
| 2 | 接收 | 关键性 | `receive-` |
| 3 | 上传 | 高优先级 | `upload-` |

## 快速参考

### 发送（关键性）
- `send-remote-attachment` - 发送加密的文件附件

### 接收（关键性）
- `receive-attachment` - 下载并解密附件

### 上传（高优先级）
- `upload-callback` - 实现自定义的上传存储机制（如Pinata、S3等）

## 快速入门

```typescript
import { type AttachmentUploadCallback } from "@xmtp/agent-sdk/util";

// Send an attachment
const file = new File(["Hello, World!"], "hello.txt", { type: "text/plain" });
await ctx.conversation.sendRemoteAttachment(file, uploadCallback);

// Receive an attachment
agent.on("attachment", async (ctx) => {
  const attachment = await downloadRemoteAttachment(ctx.message.content, agent);
  console.log(`Received: ${attachment.filename}`);
});
```

## 使用方法

请阅读各个规则文件以获取详细说明：

```
rules/send-remote-attachment.md
rules/receive-attachment.md
rules/upload-callback.md
```