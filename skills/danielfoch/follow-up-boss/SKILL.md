---
name: follow-up-boss
description: 用于与“Follow Up Boss API”交互的命令行界面（CLI）。支持管理人员信息、笔记、任务、事件、交易记录、Webhook等。
---

# Follow Up Boss (CLI)

这是一个用于与 Follow Up Boss API 进行交互的命令行工具 (CLI)。

## 设置

1. **获取 API 密钥**：登录 Follow Up Boss → 管理员 → API → 创建 API 密钥

2. **设置环境变量**：
```bash
export FUB_API_KEY="fka_xxxxxxxxxxxx"
```

## CLI 使用方法

```bash
node fub.js <command> [options]
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `me` | 显示当前用户信息 |
| `people [query]` | 列出/搜索人员信息 |
| `person <id>` | 获取人员详细信息 |
| `people create <json>` | 通过 /events 功能创建人员（触发自动化流程） |
| `people update <id> <json>` | 更新人员信息 |
| `notes <personId>` | 获取人员的备注信息 |
| `notes create <json>` | 创建备注 |
| `tasks [query]` | 列出任务信息 |
| `tasks create <json>` | 创建任务 |
| `tasks complete <id>` | 完成任务 |
| `events [query]` | 列出事件信息 |
| `events create <json>` | 创建事件（用于客户跟进） |
| `pipelines` | 查看工作流程信息 |
| `deals [query]` | 列出交易信息 |
| `deals create <json>` | 创建交易 |
| `textmessages <personId>` | 获取人员的文本消息 |
| `textmessages create <json>` | 记录文本消息（仅用于存储，不实际发送） |
| `emails <personId>` | 获取人员的电子邮件信息 |
| `emails create <json>` | 记录电子邮件（仅用于存储，不实际发送） |
| `calls <personId>` | 获取人员的通话记录 |
| `calls create <json>` | 记录通话记录 |
| `webhooks` | 查看 Webhook 信息 |
| `webhooks create <json>` | 创建 Webhook |
| `webhooks delete <id>` | 删除 Webhook |
| `sources` | 查看客户来源信息 |
| `users` | 查看用户/代理信息 |
| `search <query>` | 进行全局搜索 |

## 示例

```bash
# List people
node fub.js people "limit=10"

# Get person
node fub.js person 123

# Create a lead (triggers automations!)
node fub.js events create '{"source":"Website","system":{"name":"John Doe","email":"john@test.com","phone":"5551234567"}}'

# Add a note
node fub.js notes create '{"personId":123,"body":"Called - left voicemail"}'

# Create task
node fub.js tasks create '{"personId":123,"body":"Follow up","dueDate":"2026-02-20"}'

# Complete task
node fub.js tasks complete 456

# Log a text (NOT sent - recorded!)
node fub.js textmessages create '{"personId":123,"body":"Hey!","direction":"outbound"}'

# Log a call
node fub.js calls create '{"personId":123,"direction":"outbound","outcome":"voicemail"}'

# Search
node fub.js search "john"
```

## 重要说明

- **文本/电子邮件记录**：该 API 可以记录文本消息和电子邮件，但无法实际发送它们。请使用 Follow Up Boss 内置的短信功能或像 SendHub 这样的第三方集成工具来发送。
- **请求速率限制**：
  - `GET /events`：每 10 秒 20 次请求
  - 其他所有请求：每 10 秒 250 次请求