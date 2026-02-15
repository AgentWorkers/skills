---
name: clawconnect
description: "**ClawConnect** – 适用于 AI 代理的通用账户连接器。通过一个统一的 API，您可以发送推文、收发 Gmail 邮件、管理日历、发送 Slack 消息等操作。"
---

# ClawConnect

这是一个通用的账户连接器，用于连接各种AI代理。通过一个API即可访问Gmail、Calendar、Twitter和Discord。

## 设置

1. 访问 https://clawconnect.dev 并注册账户。
2. 将您的账户（Twitter、Gmail、Calendar、Slack、Discord）连接到该服务。
3. 从控制面板中获取您的API密钥。
4. 所有请求都需要添加 `Authorization: Bearer <API_KEY>` 标头。

基础URL：`https://clawconnect.dev`

## API接口

### 连接管理

- 列出已连接的账户：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/connections
```

### Twitter

- 获取您的Twitter个人资料：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/twitter/me
```

- 获取您的Twitter时间线：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/twitter/timeline
```

- 发布推文：
  ```bash
curl -X POST -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from ClawConnect!"}' \
  https://clawconnect.dev/api/v1/twitter/tweet
```

### Gmail

- 列出电子邮件（支持可选搜索查询和结果数量限制）：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  "https://clawconnect.dev/api/v1/gmail/messages?q=is:unread&maxResults=10"
```

- 根据ID获取电子邮件：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/gmail/messages/MESSAGE_ID
```

- 发送电子邮件：
  ```bash
curl -X POST -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "recipient@example.com", "subject": "Hello", "body": "Email body here"}' \
  https://clawconnect.dev/api/v1/gmail/send
```

### Calendar

- 列出事件（支持可选时间范围和结果数量限制）：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  "https://clawconnect.dev/api/v1/calendar/events?timeMin=2025-01-01T00:00:00Z&timeMax=2025-01-31T23:59:59Z&maxResults=20"
```

### Slack

- 列出工作空间中的用户：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/slack/users
```

- 列出频道：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/slack/channels
```

- 获取您的Slack个人资料：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/slack/profile
```

- 发送消息（频道可以是频道ID或用户ID）：
  ```bash
curl -X POST -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C01234ABCDE", "text": "Hello!"}' \
  https://clawconnect.dev/api/v1/slack/send
```

### Discord

- 获取您的Discord个人资料：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/discord/me
```

- 列出您所属的服务器（Discord中的公会）：
  ```bash
curl -H "Authorization: Bearer $CLAWCONNECT_API_KEY" \
  https://clawconnect.dev/api/v1/discord/guilds
```

## 注意事项

- 在发送推文或电子邮件之前，请务必确认内容。
- 在Gmail中，可以使用 `q` 参数进行过滤（语法与Gmail的搜索功能相同）。
- Calendar的 `timeMin`/`timeMax` 参数支持ISO 8601时间戳格式。
- 目前Discord的发送功能被禁用（受用户OAuth权限限制），目前仅支持读取操作。
- 如果您使用多个Slack工作空间，请通过 `connection_id` 参数指定目标工作空间。