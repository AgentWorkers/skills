---
name: helpscout
description: 获取并回复 Helpscout 对话内容
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["API_KEY", "APP_SECRET", "INBOX_IDS"] },
      },
  }
---

# Helpscout 技能

## 描述

此技能用于与 Helpscout 交互，以从指定的收件箱中获取对话内容并发送回复。它旨在简化直接通过 OpenClaw 进行的客户服务操作。

## 功能
- 从多个 Helpscout 收件箱中获取对话内容
- 向对话内容发送回复（客户可见或内部备注）
- 根据状态、文件夹、负责人、客户、标签等条件进行过滤
- 按多种字段对对话内容进行排序
- 直接在回复中嵌入对话线程数据
- 使用 API 密钥和 App Secret 进行安全认证
- 良好地处理潜在错误（如无效凭据或网络问题）

## 设置说明

要使用此技能，您需要配置 Helpscout 凭据，并指定要从中获取对话内容的收件箱 ID。

### 1. 获取 Helpscout API 密钥和 App Secret
1. 登录您的 Helpscout 账户。
2. 转到 **管理 > 应用程序**。
3. 创建或打开您的应用程序以获取以下详细信息：
   - **API 密钥**
   - **App Secret**

### 2. 收集收件箱 ID
1. 根据 Helpscout 的 [API 文档](https://developer.helpscout.com/) 获取您想要从中获取对话内容的收件箱 ID。

### 3. 在 OpenClaw 中保存凭据
使用以下命令保存您的 Helpscout 凭据：

```bash
cat ~/.openclaw/openclaw.json | jq '.skills.entries.helpscout = {
  enabled: true,
  env: {
    API_KEY: "your-api-key",
    APP_SECRET: "your-app-secret",
    INBOX_IDS: ["inbox-id-1", "inbox-id-2"]
  }
}' | openclaw gateway config.apply
```

### 4. 验证配置
确保凭据设置正确，请检查您的配置：

```bash
openclaw gateway config.get
```
请确保 `helpscout` 对象的配置正确（避免泄露 `API_KEY` 或 `APP_SECRET`）。

## 使用方法

### 基本用法
从已配置的收件箱中获取所有活跃的对话内容：

```javascript
const { fetchAllInboxes } = require('./index.js');

// Fetch all active conversations (default)
const results = await fetchAllInboxes();
```

### 高级过滤

```javascript
const { fetchConversations } = require('./index.js');

// Fetch closed conversations from a specific inbox
const conversations = await fetchConversations(321755, {
  status: 'closed',
  sortField: 'modifiedAt',
  sortOrder: 'desc',
  page: 1
});

// Fetch conversations assigned to a specific user
const assigned = await fetchConversations(321755, {
  assignedTo: 782728,
  status: 'active'
});

// Fetch conversations with a specific tag
const tagged = await fetchConversations(321755, {
  tag: 'urgent',
  status: 'active'
});

// Fetch conversations with embedded threads
const withThreads = await fetchConversations(321755, {
  embed: 'threads',
  status: 'active'
});

// Advanced search query
const searched = await fetchConversations(321755, {
  query: '(customerEmail:user@example.com)',
  status: 'all'
});
```

### 发送回复

```javascript
const { sendReply } = require('./index.js');

// Send a customer-visible reply (will send email)
await sendReply(3227506031, {
  text: 'Hi there,\n\nThanks for your message!\n\nBest regards,',
  inboxId: 321755  // Required to auto-fetch customer ID
});

// Send a reply without emailing the customer (imported)
await sendReply(3227506031, {
  text: 'Draft reply - not sent to customer yet',
  customerId: 856475517,  // Or provide inboxId to auto-fetch
  imported: true
});

// Send a reply and close the conversation
await sendReply(3227506031, {
  text: 'All done! Let me know if you need anything else.',
  inboxId: 321755,
  status: 'closed'
});

// Create an internal note
const { createNote } = require('./index.js');
await createNote(3227506031, 'Internal note: Customer called, issue resolved.');
```

### sendReply 参数说明

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `text` | 字符串 | **必填。** 回复文本（支持 HTML 格式） |
| `inboxId` | 数字 | 收件箱 ID - 如果未提供 `customerId`，则自动使用此参数（会自动获取客户信息） |
| `customerId` | 数字 | 客户 ID - 如果未提供，将使用 `inboxId` 自动获取 |
| `imported` | 布尔值 | 标记为已导入（不会通过电子邮件通知客户）。默认值：`false` |
| `status` | 字符串 | 回复后的对话状态：`active`（活跃）、`pending`（待处理）、`closed`（已关闭）。可选。 |
| `userId` | 数字 | 发送回复的用户 ID。可选（默认为当前登录用户）。 |

### createNote 参数说明

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `text` | 字符串 | **必填。** 备注文本（支持 HTML 格式） |

### fetchConversations 可用参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `status` | 字符串 | 根据状态过滤：`active`（活跃）、`pending`（待处理）、`closed`（已关闭）或 `all`（全部）（默认：`active`） |
| `folderId` | 数字 | 根据文件夹 ID 进行过滤 |
| `assignedTo` | 数字 | 根据用户 ID 进行过滤 |
| `customerId` | 数字 | 根据客户 ID 进行过滤 |
| `number` | 数字 | 根据对话编号进行过滤 |
| `modifiedSince` | 字符串 | ISO8601 格式的日期，用于过滤在此日期之后修改的对话 |
| `sortField` | 字符串 | 排序字段：`createdAt`（创建时间）、`mailboxId`（收件箱 ID）、`modifiedAt`（修改时间）、`number`（对话编号）、`score`（评分）、`status`（状态）、`subject`（主题）（默认：`createdAt`） |
| `sortOrder` | 字符串 | 排序顺序：`asc`（升序）或 `desc`（降序）（默认：`desc`） |
| `tag` | 字符串 | 根据标签名称进行过滤 |
| `query` | 字符串 | 使用 `fieldId:value` 格式的高级搜索查询 |
| `embed` | 字符串 | 用逗号分隔的嵌入资源列表：`threads`（对话线程） |
| `page` | 数字 | 分页页码（默认：1） |

### 安全最佳实践
- 切勿将凭据硬编码到代码库中。
- 使用 OpenClaw 的 `config.apply` 系统来安全地管理敏感信息。
- 避免与他人共享配置输出中的敏感部分（`API_KEY` 和 `APP_SECRET`）。

## 贡献指南
- 确保遵守 Helpscout 的 API 使用政策。
- 为新增的功能添加相应的文档说明。