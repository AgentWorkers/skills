---
name: ravi-inbox
description: 读取传入的短信或电子邮件消息——包括一次性密码（OTPs）、验证码、验证链接以及收到的邮件。请勿使用该功能来发送电子邮件（请使用 `ravi-email-send`），也不要用它来管理凭据（请使用 `ravi-passwords` 或 `ravi-secrets`）。
---
# Ravi 收件箱

用于查看通过您的 Ravi 账户接收到的短信和电子邮件。在触发身份验证、二次验证（2FA）或预期有新消息到达时可以使用此功能。

## 短信（一次性密码，验证码）

```bash
# List SMS conversations (grouped by sender)
ravi inbox sms --json

# Only conversations with unread messages
ravi inbox sms --unread --json

# View a specific conversation (all messages)
ravi inbox sms <conversation_id> --json
# conversation_id format: {phone_id}_{from_number}, e.g. "1_+15559876543"
```

**JSON 格式 — 对话列表：**
```json
[{
  "conversation_id": "1_+15559876543",
  "from_number": "+15559876543",
  "phone_number": "+15551234567",
  "preview": "Your code is 847291",
  "message_count": 3,
  "unread_count": 1,
  "latest_message_dt": "2026-02-25T10:30:00Z"
}]
```

**JSON 格式 — 对话详情：**
```json
{
  "conversation_id": "1_+15559876543",
  "from_number": "+15559876543",
  "messages": [
    {"id": 42, "body": "Your code is 847291", "direction": "incoming", "is_read": false, "created_dt": "..."}
  ]
}
```

## 电子邮件（验证链接，确认信息）

```bash
# List email threads
ravi inbox email --json

# Only threads with unread messages
ravi inbox email --unread --json

# View a specific thread (all messages with full content)
ravi inbox email <thread_id> --json
```

**JSON 格式 — 邮件线程详情：**
```json
{
  "thread_id": "abc123",
  "subject": "Verify your email",
  "messages": [
    {
      "id": 10,
      "from_email": "noreply@example.com",
      "to_email": "janedoe@example.com",
      "subject": "Verify your email",
      "text_content": "Click here to verify: https://example.com/verify?token=xyz",
      "direction": "incoming",
      "is_read": false,
      "created_dt": "..."
    }
  ]
}
```

## 单个消息（平铺显示，不按对话分组）

当您需要按消息 ID 而不是按对话来查看消息时，可以使用这些功能：

```bash
ravi message sms --json              # All SMS messages
ravi message sms --unread --json     # Unread only
ravi message sms <message_id> --json # Specific message

ravi message email --json              # All email messages
ravi message email --unread --json     # Unread only
ravi message email <message_id> --json # Specific message
```

## 快速操作指南

### 从短信中提取一次性密码（OTP）

```bash
ravi inbox sms --unread --json | jq -r '.[].preview' | grep -oE '[0-9]{4,8}'
```

### 从电子邮件中提取验证链接

```bash
THREAD_ID=$(ravi inbox email --unread --json | jq -r '.[0].thread_id')
ravi inbox email "$THREAD_ID" --json | jq -r '.messages[].text_content' | grep -oE 'https?://[^ ]+'
```

## 重要提示

- **耐心等待** — 短信/电子邮件的发送通常需要 2-10 秒，请在检查前使用 `sleep 5` 命令等待。
- **自动联系人管理** — 当您发送或接收电子邮件/短信时，Ravi 会自动创建或更新联系人信息。可以使用 `ravi contacts search` 来查找与您互动过的人。
- **始终使用 `--json` 格式** — 为便于人类阅读而生成的输出格式并不适合程序解析。

## 相关技能

- **ravi-email-send** — 回复、全部回复或转发已阅读的电子邮件
- **ravi-email-writing** — 撰写格式正确、语气得体的专业回复
- **ravi-contacts** — 从电子邮件或电话号码中查询发件人的姓名或详细信息
- **ravi-login** — 使用收件箱进行端到端的注册/登录流程，并从中提取一次性密码（OTP）
- **ravi-feedback** — 报告收件箱相关问题或提出改进建议