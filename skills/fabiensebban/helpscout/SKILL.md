---
name: helpscout
description: 从特定的 Helpscout 收件箱中获取消息
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

该技能用于与 Helpscout 交互，从指定的收件箱中获取对话内容，并提供强大的过滤选项。它旨在简化将客户支持对话直接导入 OpenClaw 的过程，从而实现便捷的集成和后续处理。

## 特点
- 从多个 Helpscout 收件箱中获取对话内容
- 可根据状态、文件夹、分配者、客户、标签等条件进行过滤
- 按多种字段对对话内容进行排序
- 可将对话的详细信息直接嵌入到响应结果中
- 通过 API 密钥和 App Secret 进行安全认证
- 能够优雅地处理无效凭据或网络问题等潜在错误

## 设置说明

要使用此技能，您需要配置 Helpscout 的凭据，并指定要从中获取对话内容的收件箱 ID。

### 1. 获取 Helpscout API 密钥和 App Secret
1. 登录您的 Helpscout 账户。
2. 转到 **管理 > 应用程序**。
3. 创建或打开您的应用程序以获取以下信息：
   - **API 密钥**
   - **App Secret**

### 2. 收集收件箱 ID
1. 根据 Helpscout 的 [API 文档](https://developer.helpscout.com/) 获取您想要获取对话内容的收件箱 ID。

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
确保凭据配置正确：

```bash
openclaw gateway config.get
```
请检查 `helpscout` 对象的配置是否正确（切勿泄露 `API_KEY` 或 `APP_SECRET`）。

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

### 可用参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `status` | 字符串 | 按状态过滤：`active`（活跃）、`pending`（待处理）、`closed`（已关闭）、`spam`（垃圾邮件）或 `all`（全部）（默认：`active`） |
| `folderId` | 数字 | 按文件夹 ID 过滤 |
| `assignedTo` | 数字 | 按用户 ID 过滤 |
| `customerId` | 数字 | 按客户 ID 过滤 |
| `number` | 数字 | 按对话编号过滤 |
| `modifiedSince` | 字符串 | ISO8601 格式的日期，用于过滤在该日期之后修改的对话 |
| `sortField` | 字符串 | 排序字段：`createdAt`（创建时间）、`mailboxId`（收件箱 ID）、`modifiedAt`（修改时间）、`number`（对话编号）、`score`（评分）、`status`（状态）、`subject`（主题）（默认：`createdAt`） |
| `sortOrder` | 字符串 | 排序方式：`asc`（升序）或 `desc`（降序）（默认：`desc`） |
| `tag` | 字符串 | 按标签名称过滤 |
| `query` | 字符串 | 以 `fieldId:value` 格式进行高级搜索 |
| `embed` | 字符串 | 用逗号分隔的嵌入资源列表：`threads`（对话线程） |
| `page` | 数字 | 分页页码（默认：1） |

### 安全最佳实践
- 切勿将凭据硬编码到代码库中。
- 使用 OpenClaw 的 `config.apply` 系统来安全地管理敏感信息。
- 避免与他人共享配置输出中的敏感部分（`API_KEY` 和 `APP_SECRET`）。

## 贡献指南
- 确保遵守 Helpscout 的 API 使用政策。
- 为新添加的功能添加相应的文档说明。