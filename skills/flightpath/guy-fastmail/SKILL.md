---
name: guy-fastmail
description: 您可以通过 JMAP API 和 WebDAV 访问 Access Guy 的 Fastmail 电子邮件、联系人和文件存储服务。当用户需要阅读、发送、搜索、回复或管理电子邮件时，可以使用这些接口。同时，这些接口也支持联系人的查找、文件存储中的文件搜索及文件管理等功能。此外，还提供了邮箱管理、归档、标记等实用功能。
---
# Fastmail（JMAP API）

通过 Fastmail 的 JMAP API 可以完全访问电子邮件和联系人信息。

## 脚本

`scripts/jmap.sh <action> [args...]`

### 邮件相关操作

- `mailboxes` — 列出所有邮箱及其未读邮件数量/总邮件数量
- `inbox [count]` — 列出收件箱中的最近邮件（默认数量：20 封）
- `smart-inbox [timeframe] [count]` — 智能文件夹：来自所有邮箱的最近邮件（时间范围：今天-昨天/本周/上周；默认范围：今天-昨天，默认数量：50 封）
- `mailbox-emails <mailbox-id> [count]` — 列出特定邮箱中的邮件（默认数量：100 封）
- `unread [count]` — 列出未读邮件（默认数量：20 封）
- `read <email-id>` — 通过邮件 ID 读取完整邮件内容
- `search <query> [count]` — 按文本搜索邮件（默认返回 20 条结果）
- `send <to> <subject> <body> [cc]` — 发送新邮件
- `reply <email-id> <body> [reply-all]` — 回复邮件（`reply-all` 参数表示是否回复所有收件人）
- `move <email-id> <mailbox-id>` — 将邮件移动到其他邮箱（使用 `mailboxes` 命令获取邮箱 ID）
- `archive <email-id>` — 将邮件归档
- `delete <email-id>` — 将邮件移至垃圾箱
- `batch-delete` — 将多封邮件移至垃圾箱（从标准输入读取邮件 ID，每行一个）
- `batch-destroy` — 永久删除多封邮件（从标准输入读取邮件 ID，每行一个）
- `create-mailbox <name> [parent-id]` — 创建新邮箱/文件夹
- `flag <email-id> <flag> <true|false>` — 设置邮件标记（已读/已标记/已回复）

### 隐藏邮箱相关操作

- `masked-list [count]` — 列出所有隐藏的电子邮件地址（默认数量：50 封）
- `masked-search <query>` — 按地址、域名或描述搜索隐藏的电子邮件
- `masked-create [domain] [description]` — 创建新的隐藏电子邮件地址
- `masked-enable <id>` — 恢复被禁用的隐藏电子邮件地址的转发功能
- `masked-disable <id>` — 禁用隐藏电子邮件地址的转发功能
- `masked-delete <id>` — 删除隐藏的电子邮件地址（操作前需用户确认！）

### 文件相关操作（WebDAV）

- `files-list [path]` — 列出文件和文件夹（默认路径：/）
- `files-upload <local-path> <remote-path>` — 上传文件
- `files-download <remote-path> <local-path>` — 下载文件
- `files-mkdir <path>` — 创建文件夹
- `files-delete <path>` — 删除文件或文件夹（操作前需用户确认！）

### 联系人相关操作

- `contacts [count]` — 列出联系人信息（默认数量：50 个）
- `contact-search <query>` — 按姓名、电子邮件或电话号码搜索联系人

### 日历相关操作（CalDAV）

- `calendars` — 列出所有日历
- `calendar-create <name> [color]` — 创建新日历（颜色格式为十六进制，例如 #FF0000）
- `calendar-delete <calendar-id>` — 删除日历及其所有事件（操作前需用户确认！）
- `events [days] [calendar-id]` — 列出即将发生的事件（默认范围：14 天，涵盖所有日历）
- `event-search <query> [days]` — 按文本搜索事件（默认搜索范围：±90 天）
- `event-add <calendar-id> <title> <start> <end> [location> [description>` — 创建事件（开始/结束时间格式为 `YYYY-MM-DDTHH:MM`，`YYYY-MM-DD` 表示全天事件；时间采用 CT 时区）
- `event-get <calendar-id> <uid>` — 获取事件详细信息
- `event-edit <calendar-id> <uid> <field> <value>` — 编辑事件信息（标题/开始时间/结束时间/地点/描述）
- `event-delete <calendar-id> <uid>` — 删除事件（操作前需用户确认！）

### 示例

```bash
# Check unread emails
bash scripts/jmap.sh unread

# Smart inbox: see what arrived today/yesterday across all folders
bash scripts/jmap.sh smart-inbox

# Smart inbox: see what arrived this week
bash scripts/jmap.sh smart-inbox this-week

# Read a specific email
bash scripts/jmap.sh read "M1234abc"

# Search for emails about invoices
bash scripts/jmap.sh search "invoice"

# Send an email
bash scripts/jmap.sh send "someone@example.com" "Hello" "Hey, how are you?"

# Reply to an email
bash scripts/jmap.sh reply "M1234abc" "Thanks, got it!"

# List emails from a specific mailbox
bash scripts/jmap.sh mailbox-emails "POV" 50

# Batch delete emails (from a file with email IDs)
cat email_ids.txt | bash scripts/jmap.sh batch-delete

# Permanently delete emails from trash
cat trash_ids.txt | bash scripts/jmap.sh batch-destroy

# Find a contact
bash scripts/jmap.sh contact-search "Vivien"
```

## 注意事项

- 邮件 ID 以方括号的形式显示，例如 `[M1234abc]`；在读取、回复或移动邮件时请使用这些 ID。
- 发送邮件前务必先与 Guy 确认。
- 回复邮件时，如果适用，请在邮件正文中引用相关内容。
- `search` 操作会搜索邮件主题、正文、发件人和收件人字段。
- 日历操作使用 CalDAV 协议，需要单独设置密码。
- 如果需要通过 IMAP 访问邮件，可以安装 Himalaya CLI 作为备用方案。