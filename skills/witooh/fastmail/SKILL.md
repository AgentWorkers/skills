---
name: fastmail
description: 通过 JMAP 和 CalDAV API 管理 Fastmail 的电子邮件和日历功能。支持以下操作：  
- 电子邮件（读取、发送、回复、搜索、整理、批量操作、线程管理）  
- 日历（事件、提醒、回复邀请）  
系统会自动检测时区。
compatibility: opencode
metadata:
  author: witooh
  version: "2.1"
  api: JMAP, CalDAV
---

## 快速入门

通过命令行（CLI）调用工具：

```bash
# Install dependencies first
cd .opencode/skills/fastmail && bun install

# Email: List mailboxes
bunx fastmail list_mailboxes

# Email: Send
bunx fastmail send_email \
  '{"to": [{"email": "user@example.com"}], "subject": "Hi", "text_body": "Message"}'

# Calendar: List events
bunx fastmail list_events \
  '{"start_date": "2024-01-01", "end_date": "2024-01-31"}'

# Calendar: Create event with reminder
bunx fastmail create_event_with_reminder \
  '{"title": "Meeting", "start": "2024-01-15T10:00:00", "end": "2024-01-15T11:00:00", "reminder_minutes": [15, 60]}'

# List all available tools
bunx fastmail --list
```

## 何时使用这些技能

- 📧 查看收件箱或搜索邮件
- 📧 发送、回复或移动邮件
- 🏷️ 为邮件添加标签或整理邮件箱
- 📅 查看日历或事件
- 📅 创建、更新或删除事件
- 🔔 设置事件提醒或闹钟

## 邮件工具（共10个）

| 工具 | 功能 |
|------|---------|
| `list_mailboxes` | 列出所有文件夹 |
| `list_emails` | 列出邮件箱中的所有邮件 |
| `get_email` | 获取邮件的完整内容 |
| `get_thread` | 获取邮件对话中的所有邮件 |
| `search_emails` | 按文本查询搜索邮件 |
| `send_email` | 发送新邮件 |
| `reply_email` | 回复邮件 |
| `move_email` | 将邮件移动到其他文件夹 |
| `set_labels` | 为邮件添加标签（如 `$seen`, `$flagged`） |
| `delete_email` | 删除邮件（将其移至垃圾箱） |

## 批量邮件工具（共3个）

| 工具 | 功能 |
|------|---------|
| `bulk_move_emails` | 一次性移动多封邮件 |
| `bulk_set_labels` | 为多封邮件添加标签 |
| `bulk_delete_emails` | 一次性删除多封邮件 |

## 日历工具（共10个）

| 工具 | 功能 |
|------|---------|
| `list_calendars` | 列出所有日历 |
| `list_events` | 按日期范围列出事件 |
| `get_event` | 获取事件详情 |
| `create_event` | 创建新事件 |
| `update_event` | 更新现有事件 |
| `delete_event` | 删除事件 |
| `search_events` | 按标题/描述搜索事件 |
| `create_recurring_event` | 创建重复事件 |
| `list_invitations` | 列出日历邀请 |
| `respond_to_invitation` | 接受/拒绝/暂不接受邀请 |

## 提醒工具（共4个）

| 工具 | 功能 |
|------|---------|
| `add_event_reminder` | 为事件添加提醒 |
| `remove_event_reminder` | 删除事件提醒 |
| `list_event_reminders` | 列出事件的所有提醒 |
| `create_event_with_reminder` | 一次性创建事件和提醒 |

## 常见用法示例

```bash
# Check inbox (limit 10)
bunx fastmail list_emails '{"limit": 10}'

# Search for emails
bunx fastmail search_emails '{"query": "invoice"}'

# Get specific email content
bunx fastmail get_email '{"email_id": "xxx"}'

# Get email thread/conversation
bunx fastmail get_thread '{"email_id": "xxx"}'

# Bulk operations
bunx fastmail bulk_move_emails '{"email_ids": ["id1", "id2"], "target_mailbox_id": "archive"}'
bunx fastmail bulk_delete_emails '{"email_ids": ["id1", "id2", "id3"]}'

# Create recurring event (daily for 10 days)
bunx fastmail create_recurring_event \
  '{"title": "Standup", "start": "2024-01-01T09:00:00", "end": "2024-01-01T09:30:00", "recurrence": "daily", "recurrence_count": 10}'

# Calendar invitations
bunx fastmail list_invitations
bunx fastmail respond_to_invitation '{"event_id": "xxx", "response": "accept"}'
```

## 决策树

**需要管理邮件？**
- 列出/搜索邮件 → 使用 `list_emails` 或 `search_emails`
- 阅读邮件内容 → 使用 `get_email`
- 查看邮件对话 → 使用 `get_thread`
- 发送/回复邮件 → 使用 `send_email` 或 `reply_email`
- 整理邮件 → 使用 `move_email`, `set_labels`, `delete_email`
- 批量操作 → 使用 `bulk_move_emails`, `bulk_set_labels`, `bulk_delete_emails`

**需要管理日历？**
- 查看日历 → 使用 `list_calendars` 或 `list_events`
- 创建事件 → 使用 `create_event` 或 `create_recurring_event`
- 修改事件 → 使用 `update_event`
- 删除事件 → 使用 `delete_event`
- 管理邀请 → 使用 `list_invitations`, `respond_to_invitation`

## 输出格式

所有工具返回JSON格式的数据：

```json
{
  "success": true,
  "data": { /* tool-specific response */ },
  "timestamp": "2024-01-15T10:00:00+07:00"
}
```

## 环境变量

| 变量 | 用途 | 是否必填 |
|----------|---------|----------|
| `FASTMAIL_API_TOKEN` | 用于通过JMAP发送邮件 | 是（仅针对邮件功能） |
| `FASTMAIL_USERNAME` | 用于通过CalDAV访问日历 | 是（仅针对日历功能） |
| `FASTMAIL_PASSWORD` | 日历应用程序的密码 | 是（仅针对日历功能） |
| `FASTMAIL_TIMEZONE` | 日历时区（IANA格式） | 否（自动检测） |

**设置说明：**
```bash
export FASTMAIL_API_TOKEN="your-api-token"
export FASTMAIL_USERNAME="your-email@fastmail.com"
export FASTMAIL_PASSWORD="your-app-password"
# Optional: Override timezone (defaults to system local timezone)
export FASTMAIL_TIMEZONE="America/New_York"  # or "Asia/Bangkok", "Europe/London", etc.
```

## 时区支持

⏰ **可配置的日历时区**
- **默认设置：** 自动检测系统的本地时区
- **手动设置：** 通过 `FASTMAIL_TIMEZONE` 环境变量进行更改
- 使用IANA时区标识符（例如 `America/New_York`, `Asia/Bangkok`, `Europe/London`）
- 输入的时间将基于配置的时区显示
- 内部存储时间为UTC格式
- 自动处理夏令时（DST）

## 相关资源

- **详细参考文档：** `.opencode/skills/fastmail/references/TOOLS.md`
- **完整指南：** `.opencode/skills/fastmail/README.md`
- **设置帮助：** Fastmail设置 → 隐私与安全 → 集成