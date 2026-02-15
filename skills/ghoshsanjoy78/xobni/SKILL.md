---
name: xobni
description: 通过 Xobni.ai 为 AI 代理提供电子邮件基础设施。该平台提供真实的电子邮件地址（@xobni.ai）以及 REST API 和 MCP 服务器访问权限。当 AI 代理需要发送/接收电子邮件、搜索收件箱、管理附件或设置电子邮件通知的 Webhook 时，可以使用该服务。
---

# Xobni.ai 邮件功能

为 AI 代理提供真实的电子邮件地址以及完整的收件箱功能。

## 快速入门

1. 在 [xobni.ai/agents/new](https://xobni.ai/agents/new) 创建代理 → 代理的电子邮件地址格式为 `your-agent@xobni.ai`。
2. 在 [xobni.ai/settings/api-keys](https://xobni.ai/settings/api-keys) 为该代理创建 API 密钥。
3. 通过 REST API 或 MCP 连接该代理。

## API 密钥的权限范围

每个 API 密钥仅针对 **一个代理** 授权。该密钥仅能访问该代理的电子邮件、邮件线程、附件和 Webhook。无需传递 `account_id` 或 `agent_id`，因为这些信息会从密钥中自动获取。

**密钥的权限：**
- 读取、发送、搜索和管理电子邮件
- 创建和管理 Webhook
- 查看代理信息及存储使用情况

**密钥的权限限制：**
- 无法访问其他代理的数据（会返回 403 错误）
- 无法创建或删除代理
- 无法管理 API 密钥或账单信息

## MCP 连接

**URL**: `https://api.xobni.ai/mcp/`  
**传输方式**: Streamable HTTP  
**认证方式**: `Authorization: Bearer YOUR_API_KEY`

### Claude 桌面应用配置
```json
{
  "mcpServers": {
    "xobni": {
      "url": "https://api.xobni.ai/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

## 核心操作

### 读取收件箱
```bash
curl -H "Authorization: Bearer $XOBNI_KEY" \
  "https://api.xobni.ai/api/v1/emails?status=received&limit=20"
```

### 发送电子邮件
```bash
curl -X POST -H "Authorization: Bearer $XOBNI_KEY" \
  -H "Content-Type: application/json" \
  "https://api.xobni.ai/api/v1/emails/send" \
  -d '{"to":["recipient@example.com"],"subject":"Hello","body_text":"Message here"}'
```

### 带附件发送电子邮件
```bash
curl -X POST -H "Authorization: Bearer $XOBNI_KEY" \
  -H "Content-Type: application/json" \
  "https://api.xobni.ai/api/v1/emails/send" \
  -d '{
    "to":["recipient@example.com"],
    "subject":"Report",
    "body_text":"See attached.",
    "attachments":[{"filename":"report.pdf","data":"<base64>","content_type":"application/pdf"}]
  }'
```

### 搜索（语义搜索）
```bash
curl -X POST -H "Authorization: Bearer $XOBNI_KEY" \
  -H "Content-Type: application/json" \
  "https://api.xobni.ai/api/v1/search" \
  -d '{"query":"invoices from last month","limit":10}'
```

### 获取代理信息
```bash
curl -H "Authorization: Bearer $XOBNI_KEY" \
  "https://api.xobni.ai/api/v1/agents"
```

### 查看存储使用情况
```bash
curl -H "Authorization: Bearer $XOBNI_KEY" \
  "https://api.xobni.ai/api/v1/emails/storage-usage"
```

## MCP 工具（共 14 个）

| 工具 | 功能 |
|------|---------|
| `get_agent_info` | 获取代理的名称、电子邮件地址、唯一标识符（slug）和状态 |
| `read_inbox` | 根据条件（状态、数量限制、偏移量）列出电子邮件 |
| `read_email` | 通过 ID 获取电子邮件的完整内容 |
| `send_email` | 发送电子邮件，支持附加附件并支持回复功能 |
| `get_thread` | 获取邮件对话中的所有邮件 |
| `listattachments` | 列出电子邮件的所有附件 |
| `download_attachment` | 获取预签名的附件下载链接（有效期 15 分钟） |
| `get_attachment_text` | 从 PDF/DOCX/XLSX/PPTX 文件中提取文本 |
| `mark_email` | 更新邮件状态（已读/未读/加星/取消加星/归档） |
| `search_emails` | 对电子邮件及其附件进行语义搜索 |
| `list_webhooks` | 列出已配置的 Webhook |
| `create_webhook` | 为电子邮件接收或发送事件创建 Webhook |
| `delete_webhook` | 删除 Webhook |
| `list_webhook_deliveries` | 查看 Webhook 的发送记录 |

## Webhook

当电子邮件到达或发送时，可以设置实时通知：

```bash
curl -X POST -H "Authorization: Bearer $XOBNI_KEY" \
  -H "Content-Type: application/json" \
  "https://api.xobni.ai/api/v1/event-hooks" \
  -d '{
    "url": "https://your-endpoint.com/webhook",
    "events": ["email.received"],
    "description": "Email notifications"
  }'
```

支持的事件：`email.received`、`email.sent`。事件数据中包含电子邮件元信息和 200 个字符的摘要内容。可以使用 `read_email` 获取邮件的完整内容。

## API 参考文档

请参阅 [references/api.md](references/api.md) 以获取完整的端点文档。

## 关键概念

- **代理级密钥**：每个密钥仅适用于一个代理。代理 ID 会自动从密钥中解析。
- **语义搜索**：支持在电子邮件正文及附件（PDF、DOCX 等格式）中进行自然语言搜索。
- **附件**：支持通过 Base64 编码发送文件（最多 10 个文件，总大小不超过 10MB）。
- **Webhook**：支持通过 n8n、Zapier、Make 或任何 HTTP 端点接收电子邮件事件的实时通知。