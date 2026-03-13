---
name: clawaimail
version: 0.2.2
description: 为你的AI代理提供一个真实的电子邮件地址。通过API发送、接收和管理电子邮件。
author: ClawAIMail
author_url: https://clawaimail.com
repository: https://github.com/joansongjr/clawaimail
license: MIT
tags:
  - email
  - inbox
  - send-email
  - receive-email
  - ai-agent
  - mcp-server
  - api
  - automation
---
# ClawAIMail - 专为AI代理设计的电子邮件服务

为您的AI代理分配一个专属的电子邮件地址。通过简单的API，您可以创建收件箱、发送和接收真实的电子邮件、搜索邮件以及管理邮件线程。

## 功能介绍

- **创建收件箱**：立即生成如 `mybot@clawaimail.com` 这样的电子邮件地址。
- **发送电子邮件**：使用代理的地址发送真实的电子邮件。
- **接收电子邮件**：通过Webhook或WebSocket接收邮件到达的通知。
- **阅读与搜索**：阅读邮件内容、按关键词搜索邮件、跟踪邮件线程。
- **管理功能**：为收件箱设置标签、使用自定义域名等。

## 设置步骤

1. 在 [https://clawaimail.com](https://clawaimail.com) 获取您的API密钥（免费 tier：3个收件箱，每月3000封邮件）。
2. 设置环境变量：

```
CLAWAIMAIL_API_KEY=pb_your_api_key
```

## OpenClaw配置说明

⚠️ **重要提示**：请勿在 `openclaw.json` 文件中添加 `mcpServers` 字段——该字段不受支持，可能会导致Gateway崩溃。

请使用 **mcporter**（OpenClaw的MCP管理工具）进行配置：

```bash
# Add ClawAIMail as an MCP server
mcporter config add clawaimail "npx -y clawaimail-mcp" --env CLAWAIMAIL_API_KEY="pb_your_api_key"

# Test it works
mcporter call clawaimail.list_inboxes

# Check status
mcporter status
```

`mcporter` 会将其配置文件保存在 `~/.openclaw/config/mcporter.json` 中，与OpenClaw Gateway的配置文件分开存储。

### 常见问题与解决方法

| 问题 | 原因 | 解决方案 |
|---------|-------|-----|
| Gateway启动时崩溃 | 在 `openclaw.json` 中添加了 `mcpServers` | 从 `openclaw.json` 中删除该字段，改用 `mcporter` 进行配置。 |
| 出现 “CLAWAIMAIL_API_KEY未设置” 的警告 | 环境变量缺失 | 在 `mcporter` 的配置文件中添加 `--env CLAWAIMAIL_API_KEY="..."`。 |
| API调用返回错误 | API密钥无效或服务不可用 | 在 [https://clawaimail.com/dashboard](https://clawaimail.com/dashboard) 检查API密钥是否正确。 |

## MCP服务器配置（适用于Claude Desktop/Cursor等非OpenClaw客户端）

```json
{
  "mcpServers": {
    "clawaimail": {
      "command": "npx",
      "args": ["-y", "clawaimail-mcp"],
      "env": {
        "CLAWAIMAIL_API_KEY": "pb_your_api_key"
      }
    }
  }
}
```

## 可用工具

| 工具 | 功能说明 |
|------|-------------|
| `list_inboxes` | 列出所有电子邮件收件箱。 |
| `create_inbox` | 创建新的电子邮件收件箱（例如：mybot@clawaimail.com）。 |
| `send_email` | 从收件箱发送电子邮件。 |
| `list_messages` | 查看收件箱中的所有邮件。 |
| `read_email` | 阅读指定的电子邮件。 |
| `search_emails` | 按关键词搜索邮件。 |
| `delete_inbox` | 删除收件箱及其所有邮件。 |
| `account_info` | 获取账户信息、使用限制等详情。 |

## 使用示例

### 创建收件箱并发送电子邮件
```
User: Create an email inbox called "assistant"
Agent: [calls create_inbox with username "assistant"]
       Created inbox: assistant@clawaimail.com

User: Send an email to john@example.com saying hello
Agent: [calls send_email with to "john@example.com", subject "Hello", text "Hello from your AI assistant!"]
       Email sent successfully.
```

### 检查新邮件
```
User: Check my inbox for new messages
Agent: [calls list_messages with inbox_id 1, unread true]
       You have 3 unread messages:
       1. From: jane@company.com - Subject: "Meeting tomorrow"
       2. From: support@service.com - Subject: "Your ticket #1234"
       3. From: newsletter@tech.io - Subject: "Weekly digest"
```

### 搜索邮件
```
User: Find any emails about invoices
Agent: [calls search_emails with query "invoice"]
       Found 2 emails mentioning "invoice":
       1. From: billing@vendor.com - "Invoice #5678 - Due March 15"
       2. From: accounting@partner.org - "Updated invoice attached"
```

## 定价方案

- **免费版**：3个收件箱，每月3000封邮件。
- **入门版**（5美元/月）：10个收件箱，每月5000封邮件。
- **专业版**（29美元/月）：50个收件箱，每月50000封邮件，支持自定义域名。
- **企业版**（99美元/月）：200个收件箱，每月200000封邮件。

## 更新日志

### 0.1.2版本
- 修复了所有API调用中的错误处理问题（不再因API密钥缺失或网络问题导致崩溃）。
- 支持使用数字或字符串格式的 `inbox_id`/`message_id`。
- 当 `CLAWAIMAIL_API_KEY` 未设置时，会显示启动警告信息。
- 添加了全局异常处理机制，防止程序崩溃。

### 0.1.0版本
- 初始版本。

## 相关链接

- 官网：[https://clawaimail.com](https://clawaimail.com)
- API文档：[https://clawaimail.com/docs/](https://clawaimail.com/docs/)
- GitHub仓库：[https://github.com/joansongjr/clawaimail](https://github.com/joansongjr/clawaimail)
- npm包：[https://www.npmjs.com/package/clawaimail-mcp](https://www.npmjs.com/package/clawaimail-mcp)
- ClawHub集成：[https://clawhub.com/skills/clawaimail](https://clawhub.com/skills/clawaimail)
- Node.js SDK：`npm install clawaimail`
- Python SDK：`pip install clawaimail`