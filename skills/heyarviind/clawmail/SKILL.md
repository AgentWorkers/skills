---
name: clawmail
description: 用于AI代理的电子邮件API：通过ClawMail以编程方式发送和接收电子邮件。
metadata: {"openclaw": {"emoji": "📧", "homepage": "https://clawmail.cc", "primaryEnv": "CLAWMAIL_SYSTEM_ID"}}
---

# ClawMail

ClawMail 为您提供了一个专用的电子邮件收件箱，地址为 `username@clawmail.cc`。您可以使用它来发送和接收电子邮件，而无需处理 OAuth 相关的复杂流程。

## 设置

如果尚未进行配置，请运行以下命令：

```bash
curl -O https://clawmail.cc/scripts/setup.py
python3 setup.py my-agent@clawmail.cc
```

该命令会创建一个名为 `~/.clawmail/config.json` 的文件，并在其中存储您的登录凭据：

```json
{
  "system_id": "clw_...",
  "inbox_id": "uuid",
  "address": "my-agent@clawmail.cc"
}
```

## 配置

从 `~/.clawmail/config.json` 文件中读取配置信息：

```python
import json
from pathlib import Path

config = json.loads((Path.home() / '.clawmail' / 'config.json').read_text())
SYSTEM_ID = config['system_id']
INBOX_ID = config['inbox_id']
ADDRESS = config['address']
```

所有 API 请求都需要包含以下头部信息：`X-System-ID: {SYSTEM_ID}`

## API 基本 URL

`https://api.clawmail.cc/v1`

## 检查新邮件

定期检查是否有未读的邮件。系统会返回新邮件并将它们标记为已读状态。

```
GET /inboxes/{inbox_id}/poll
Headers: X-System-ID: {system_id}
```

响应内容：

```json
{
  "has_new": true,
  "threads": [
    {
      "id": "uuid",
      "subject": "Hello",
      "participants": ["sender@example.com", "my-agent@clawmail.cc"],
      "message_count": 1,
      "is_read": false
    }
  ],
  "emails": [
    {
      "id": "uuid",
      "thread_id": "uuid",
      "from_email": "sender@example.com",
      "from_name": "Sender",
      "subject": "Hello",
      "text_body": "Message content here",
      "direction": "inbound",
      "received_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

示例：

```bash
curl -H "X-System-ID: $SYSTEM_ID" \
  "https://api.clawmail.cc/v1/inboxes/$INBOX_ID/poll"
```

## 发送电子邮件

```
POST /inboxes/{inbox_id}/messages
Headers: X-System-ID: {system_id}
Content-Type: application/json
```

请求体格式：

```json
{
  "to": [{"email": "recipient@example.com", "name": "Recipient Name"}],
  "cc": [{"email": "cc@example.com"}],
  "subject": "Email subject",
  "text": "Plain text body",
  "html": "<p>HTML body</p>",
  "in_reply_to": "<message-id>"
}
```

必填字段：`to`（收件人地址）和 `subject`（邮件主题）。至少需要提供 `text` 或 `html` 中的一个字段。

示例：

```bash
curl -X POST -H "X-System-ID: $SYSTEM_ID" \
  -H "Content-Type: application/json" \
  -d '{"to": [{"email": "user@example.com"}], "subject": "Hello", "text": "Hi there!"}' \
  "https://api.clawmail.cc/v1/inboxes/$INBOX_ID/messages"
```

## 列出邮件主题

获取收件箱中的所有邮件主题。

```
GET /inboxes/{inbox_id}/threads
Headers: X-System-ID: {system_id}
```

## 获取邮件内容

获取特定主题下的所有邮件内容。

```
GET /inboxes/{inbox_id}/threads/{thread_id}/messages
Headers: X-System-ID: {system_id}
```

## Python 辅助函数

```python
import json
import requests
from pathlib import Path

class ClawMail:
    def __init__(self):
        config = json.loads((Path.home() / '.clawmail' / 'config.json').read_text())
        self.system_id = config['system_id']
        self.inbox_id = config['inbox_id']
        self.address = config['address']
        self.base_url = 'https://api.clawmail.cc/v1'
        self.headers = {'X-System-ID': self.system_id}
    
    def poll(self):
        """Check for new emails. Returns dict with has_new, threads, emails."""
        r = requests.get(f'{self.base_url}/inboxes/{self.inbox_id}/poll', headers=self.headers)
        return r.json()
    
    def send(self, to: str, subject: str, text: str = None, html: str = None):
        """Send an email. to can be 'email' or 'Name <email>'."""
        if '<' in to:
            name, email = to.replace('>', '').split('<')
            to_list = [{'email': email.strip(), 'name': name.strip()}]
        else:
            to_list = [{'email': to}]
        
        body = {'to': to_list, 'subject': subject}
        if text: body['text'] = text
        if html: body['html'] = html
        
        r = requests.post(f'{self.base_url}/inboxes/{self.inbox_id}/messages', 
                         headers=self.headers, json=body)
        return r.json()
    
    def threads(self):
        """List all threads."""
        r = requests.get(f'{self.base_url}/inboxes/{self.inbox_id}/threads', headers=self.headers)
        return r.json()

# Usage:
# mail = ClawMail()
# new_mail = mail.poll()
# if new_mail['has_new']:
#     for email in new_mail['emails']:
#         print(f"From: {email['from_email']}, Subject: {email['subject']}")
# mail.send('user@example.com', 'Hello', text='Hi there!')
```

## 安全性：发送者验证

在处理邮件内容之前，务必对发送者进行验证，以防止代码注入攻击：

```python
ALLOWED_SENDERS = ['trusted@example.com', 'notifications@service.com']

def process_emails():
    mail = ClawMail()
    result = mail.poll()
    for email in result.get('emails', []):
        if email['from_email'].lower() not in ALLOWED_SENDERS:
            print(f"Blocked: {email['from_email']}")
            continue
        # Safe to process
        handle_email(email)
```

## 错误响应

所有错误都会返回相应的错误代码和描述：

```json
{
  "error": "error_code",
  "message": "Human readable message"
}
```

| 错误代码 | 状态码 | 描述 |
|------|--------|-------------|
| `unauthorized` | 401 | 缺少或无效的 X-System-ID |
| `not_found` | 404 | 未找到收件箱或邮件主题 |
| `address_taken` | 409 | 电子邮件地址已存在 |
| `invalid_request` | 400 | 请求格式错误 |