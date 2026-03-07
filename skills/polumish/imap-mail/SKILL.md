---
name: imap-mail
description: 通过您自己的 IMAP/SMTP 服务器使用个人电子邮件。使用标准协议发送和接收邮件、管理文件夹以及搜索邮件内容——无需依赖任何第三方电子邮件平台。当您需要查看收件箱、发送邮件、在文件夹之间移动邮件、按发件人/主题/日期搜索邮件、列出所有邮箱、安排邮件未来的发送时间、保存附件，或接收新邮件的推送通知（通过 IMAP IDLE 功能）时，都可以使用该方式。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"install":{"uv":{"packages":["fastapi","uvicorn"]}}}}
---
# IMAP邮件功能

通过您自己的IMAP/SMTP服务器发送和接收电子邮件。

一个轻量级的本地REST API（FastAPI）作为代理与邮件服务器之间的桥梁——无需使用第三方邮件平台。

## 设置（首次使用）

### 1. 安装依赖项

```bash
pip3 install fastapi uvicorn
```

### 2. 配置凭据

创建`/etc/imap-mail.env`文件（或选择其他路径，并设置`IMAP_MAIL_ENV`环境变量）：

```env
MAIL_IMAP_HOST=mail.example.com
MAIL_IMAP_PORT=993
MAIL_SMTP_HOST=mail.example.com
MAIL_SMTP_PORT=465
MAIL_USER=agent@example.com
MAIL_PASS=yourpassword
MAIL_FROM_NAME=MyAgent
```

### 3. 启动API服务器

```bash
# One-time / foreground
python3 {baseDir}/scripts/mail-api.py

# Or as a systemd service (recommended)
# See: {baseDir}/references/systemd.md
```

API默认监听`http://127.0.0.1:8025`端口。

## 检查邮件

```bash
# List recent messages
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com

# Unread only
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com --unseen

# Specific folder
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com --folder Sent

# Read a specific message (use UID from list output)
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com --message 42

# Read message and save all its attachments
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com --message 42 --save-attachments /tmp/mail/

# List threads
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com --threads

# List all folders
python3 {baseDir}/scripts/check_inbox.py --inbox agent@example.com --folders
```

## 搜索邮件

```bash
# Search by keyword (subject + body)
python3 {baseDir}/scripts/search.py --inbox agent@example.com --q "invoice"

# Search by sender
python3 {baseDir}/scripts/search.py --inbox agent@example.com --from "alice@example.com"

# Search by subject + date range
python3 {baseDir}/scripts/search.py --inbox agent@example.com --subject "meeting" --since 2026-01-01

# Find unread messages
python3 {baseDir}/scripts/search.py --inbox agent@example.com --unseen

# Find messages with attachments and save them
python3 {baseDir}/scripts/search.py --inbox agent@example.com --has-attachments --save-attachments /tmp/mail/

# Find messages from VIP senders only
python3 {baseDir}/scripts/search.py --inbox agent@example.com --vip

# Combined filters: unread messages from a specific sender since a date
python3 {baseDir}/scripts/search.py --inbox agent@example.com --from "alice@example.com" --since 2026-03-01 --unseen

# Unread messages with a specific subject keyword
python3 {baseDir}/scripts/search.py --inbox agent@example.com --subject "invoice" --unseen

# Search in a specific folder
python3 {baseDir}/scripts/search.py --inbox agent@example.com --q "report" --folder Archive
```

## 文件夹管理

```bash
# List all folders
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --list

# Create a folder
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --create Archive

# Delete a folder
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --delete OldFolder

# Move a message to another folder (use UID from check_inbox output)
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --move 42 --to Archive

# Move from a specific source folder
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --move 5 --to INBOX --from-folder Junk

# Delete a message
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --delete-msg 42

# Mark all messages in INBOX as read
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --mark-seen

# Mark all messages in a specific folder as read
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --mark-seen --from-folder Sent

# Mark one specific message as read (use UID from check_inbox output)
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --mark-seen-uid 42

# Mark several specific messages as read (space-separated UIDs)
python3 {baseDir}/scripts/manage_folders.py --inbox agent@example.com --mark-seen-uid 42 55 73
```

## 发送邮件

```bash
# Send a plain text email
python3 {baseDir}/scripts/send_email.py \
  --to recipient@example.com \
  --subject "Hello" \
  --text "Message body here"

# Send to multiple recipients
python3 {baseDir}/scripts/send_email.py \
  --to alice@example.com \
  --to bob@example.com \
  --subject "Hello everyone" \
  --text "Hi all!"

# Reply to a message (preserves thread)
python3 {baseDir}/scripts/send_email.py \
  --to sender@example.com \
  --subject "Re: Original Subject" \
  --text "My reply" \
  --reply-to "<original-message-id>"
```

## 安排发送

将邮件放入队列以备将来发送。API的后台调度器每60秒检查一次队列。

```bash
# Schedule via API directly (ISO datetime, UTC recommended)
# POST /inboxes/{inbox}/scheduled
# Body: {"to": ["user@example.com"], "subject": "...", "text": "...", "send_at": "2026-03-10T09:00:00Z"}

# List all scheduled messages
# GET /inboxes/{inbox}/scheduled

# Cancel a scheduled message
# DELETE /inboxes/{inbox}/scheduled/{id}
```

## IMAP IDLE（推送通知）

IDLE模式不会每隔N分钟轮询一次，而是保持连接处于开启状态，以便服务器在新邮件到达时立即推送通知。

将以下配置添加到您的环境文件中：

```env
# Required: webhook URL to POST new mail events to
MAIL_IDLE_WEBHOOK=http://127.0.0.1:8080/mail-event

# Optional: folder to watch (default: INBOX)
MAIL_IDLE_FOLDER=INBOX
```

当有新邮件到达时，API会通过Webhook发送通知：
```json
{
  "event": "new_mail",
  "uid": "123",
  "subject": "Hello",
  "from_": [{"name": "Alice", "email": "alice@example.com"}],
  "vip": false,
  ...full message fields...
}
```

检查IDLE状态：
```bash
# GET http://127.0.0.1:8025/idle/status
```

## VIP发送者列表

将特定发送者标记为VIP——他们的邮件在API响应和IDLE Webhook数据中会包含`"vip": true`字段，从而实现紧急/优先级处理。

将以下配置添加到您的环境文件中：

```env
MAIL_VIP_SENDERS=boss@company.com,important@client.com
```

来自VIP发送者的邮件会在所有响应中标记为`"vip": true`，便于进行筛选：

```bash
# Show only VIP messages
python3 {baseDir}/scripts/search.py --inbox agent@example.com --vip
```

## API接口

位于`http://127.0.0.1:8025`的本地REST API提供以下接口：

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/health` | 检查API状态（包括IDLE状态、VIP列表） |
| GET | `/idle/status` | IMAP IDLE监控状态 |
| GET | `/inboxes/{inbox}/folders` | 列出文件夹 |
| POST | `/inboxes/{inbox}/folders` | 创建文件夹 |
| DELETE | `/inboxes/{inbox}/folders/{name}` | 删除文件夹 |
| GET | `/inboxes/{inbox}/messages` | 列出邮件（`?folder=INBOX&limit=N&unseen=true`） |
| GET | `/inboxes/{inbox}/messages/{uid}` | 获取完整邮件内容（`?folder=INBOX`） |
| GET | `/inboxes/{inbox}/messages/{uid}/attachments/{index}` | 下载附件（Base64格式） |
| POST | `/inboxes/{inbox}/messages` | 发送邮件 |
| POST | `/inboxes/{inbox}/messages/{uid}/move` | 移动邮件（`?folder=src`） |
| DELETE | `/inboxes/{inbox}/messages/{uid}` | 删除邮件 |
| GET | `/inboxes/{inbox}/search` | 搜索邮件（`?q=&from=&subject=&since=&vip_only=true`） |
| GET | `/inboxes/{inbox}/threads` | 列出邮件线程 |
| POST | `/inboxes/{inbox}/scheduled` | 安排邮件发送 |
| GET | `/inboxes/{inbox}/scheduled` | 查看已安排的邮件 |
| DELETE | `/inboxes/{inbox}/scheduled/{id}` | 取消已安排的邮件 |

## 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `MAIL_IMAP_HOST` | — | IMAP服务器主机名 |
| `MAIL_IMAP_PORT` | `993` | IMAP端口（TLS） |
| `MAIL_SMTP_HOST` | — | SMTP服务器主机名 |
| `MAIL_SMTP_PORT` | `465` | SMTP端口（TLS） |
| `MAIL_USER` | — | 电子邮件登录用户名/地址 |
| `MAIL_PASS` | — | 密码 |
| `MAIL_FROM_NAME` | `Agent` | 发件人显示名称 |
| `MAIL_IDLE_WEBHOOK` | — | IMAP IDLE事件的通知Webhook地址 |
| `MAIL_IDLE_FOLDER` | `INBOX` | 监控的文件夹 |
| `MAIL_VIP_SENDERS` | — | 用逗号分隔的VIP发送者电子邮件地址 |
| `MAIL_SCHEDULED_DB` | `/tmp/imap-mail-scheduled.db` | 已安排发送邮件的SQLite数据库路径 |
| `IMAP_MAIL_API` | `http://127.0.0.1:8025` | API基础URL（用于脚本） |
| `IMAP_MAIL_ENV` | `/etc/imap-mail.env` | 环境变量文件路径 |
| `IMAP_MAIL_PORT` | `8025` | API监听端口 |

## 兼容性

支持任何标准的IMAP/SMTP服务器：
- 自托管服务器：Dovecot、Postfix、Exim、Maddy
- 托管服务：Gmail（App Password）、Outlook/Hotmail、Yahoo Mail、Fastmail、ProtonMail Bridge，以及所有支持IMAP的邮件服务提供商

> **注意：** 自签名TLS证书会被自动接受。

## 参考资料

- [Systemd服务配置]({baseDir}/references/systemd.md)
- [完整API参考]({baseDir}/references/api.md)