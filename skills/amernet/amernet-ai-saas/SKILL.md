---
name: amernet-ai-saas
description: 通过 OpenClaw 将您的人工智能 SaaS 智能代理连接到任何消息传递渠道（包括 WhatsApp、Telegram、Slack、Discord、iMessage 等）。
homepage: https://saas.salesbay.ai
user-invocable: false
---
## AI SaaS 聊天机器人

该技能会将用户发送的消息转发给 AI SaaS 聊天机器人，并返回机器人的响应。它通过使用用户的频道名称和用户标识符作为会话键来维护对话上下文。

### 必需配置

以下环境变量必须设置在您的 `~/.openclaw/openclaw.json` 文件中的 `skills.entries.amernet-ai-saas.env` 部分：

| 变量 | 描述 |
|---|---|
| `AI_SAAS_API_KEY` | 从门户网站（Settings → API Keys）获取的 API 密钥。需要 `all` 权限。 |
| `AI_SAAS_CHATBOT_ID` | 要将所有消息路由到的聊天机器人 ID（从 Chatbots 页面复制）。 |
| `AI_SAAS_BASE_URL` | 您的 AI SaaS 实例的基 URL。默认值：`https://saas_salesbay.ai` |

### 消息路由

当用户通过任何连接的频道发送消息时：

1. 确定当前频道名称（例如 `whatsapp`、`telegram`、`slack`、`discord`）以及该频道上的用户标识符（电话号码、用户 ID 或用户名）。

2. 构建一个 `sender_id`，格式为 `<频道>:<用户标识符>`：
   - WhatsApp 示例：`whatsapp:+15551234567`
   - Telegram 示例：`telegram:123456789`
   - Slack 示例：`slack:U012AB3CD`
   - Discord 示例：`discord:123456789012345678`

3. 向聊天机器人 API 发送 POST 请求：

```
POST ${AI_SAAS_BASE_URL}/api/v1/chatbots/${AI_SAAS_CHATBOT_ID}/chat
Authorization: Bearer ${AI_SAAS_API_KEY}
Content-Type: application/json

{
  "sender_id": "<constructed sender_id>",
  "message": "<user message text>"
}
```

4. 解析 JSON 响应中的 `dataresponses` 数据。将每个响应的 `text` 字段作为单独的消息返回给用户。如果存在多个响应，请按顺序发送。

5. 如果 API 返回错误或无法访问，请回复：“抱歉，AI 助手暂时无法使用。请稍后再试。”

### 对话重置

如果用户明确输入 “reset”、“start over”、“clear chat” 或 “/reset”：

```
DELETE ${AI_SAAS_BASE_URL}/api/v1/chatbots/${AI_SAAS_CHATBOT_ID}/conversations/<sender_id>
Authorization: Bearer ${AI_SAAS_API_KEY}
```

然后回复：“对话已清除。有什么可以帮您的吗？”

### 状态检查

如果用户输入 “/status” 或 “/ping”：

```
GET ${AI_SAAS_BASE_URL}/api/v1/chatbots/${AI_SAAS_CHATBOT_ID}
Authorization: Bearer ${AI_SAAS_API_KEY}
```

报告聊天机器人的名称及其是否处于活动状态。