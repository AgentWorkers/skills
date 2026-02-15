---
name: apple-mail-search
description: 在 macOS 上，可以通过 SQLite 快速搜索 Apple Mail 中的邮件。支持按主题、发件人、日期或附件进行搜索；搜索速度约为 50 毫秒，而使用 AppleScript 时则需要 8 分钟以上。当需要查找、搜索或列出邮件时，可以使用此方法。
homepage: https://github.com/steipete/clawdbot
metadata: {"clawdbot":{"emoji":"📬","os":["darwin"],"requires":{"bins":["sqlite3"]}}}
---

# Apple Mail 搜索

通过 SQLite 可以即时搜索 Apple Mail.app 中的电子邮件。搜索速度约为 50 毫秒，而使用 AppleScript 则需要 8 分钟以上。

## 安装

```bash
# Copy mail-search to your PATH
cp mail-search /usr/local/bin/
chmod +x /usr/local/bin/mail-search
```

## 使用方法

```bash
mail-search subject "invoice"           # Search subjects
mail-search sender "@amazon.com"        # Search by sender email
mail-search from-name "John"            # Search by sender name
mail-search to "recipient@example.com"  # Search sent mail
mail-search unread                      # List unread emails
mail-search attachments                 # List emails with attachments
mail-search attachment-type pdf         # Find PDFs
mail-search recent 7                    # Last 7 days
mail-search date-range 2025-01-01 2025-01-31
mail-search open 12345                  # Open email by ID
mail-search stats                       # Database statistics
```

## 选项

```
-n, --limit N    Max results (default: 20)
-j, --json       Output as JSON
-c, --csv        Output as CSV
-q, --quiet      No headers
--db PATH        Override database path
```

## 示例

```bash
# Find bank statements from last month
mail-search subject "statement" -n 50

# Get unread emails as JSON for processing
mail-search unread --json | jq '.[] | .subject'

# Find all PDFs from a specific sender
mail-search sender "@bankofamerica.com" -n 100 | grep -i statement

# Export recent emails to CSV
mail-search recent 30 --csv > recent_emails.csv
```

## 该工具的必要性

| 方法 | 搜索 130,000 封电子邮件的时间 |
|--------|---------------------|
| AppleScript | 8 分钟以上 |
| Spotlight/mdfind | 自 macOS Big Sur 之后不再可用 |
| SQLite（本工具） | 约 50 毫秒 |

Apple 在 macOS Big Sur 中移除了用于导入 .emlx 文件的 Spotlight 功能。本工具直接查询 `Envelope Index` SQLite 数据库。

## 技术细节

**数据库位置：** `~/Library/Mail/V{9,10,11}/MailData/Envelope Index`

**主要表格：**
- `messages`：电子邮件元数据（日期、标记、外键）
- `subjects`：邮件主题行
- `addresses`：电子邮件地址和显示名称
- `recipients`：收件人/抄送人信息
- `attachments`：附件文件名

**限制：**
- 仅支持读取操作（无法创建或发送邮件）
- 仅包含元数据（.emlx 文件中的邮件正文不可访问）
- 仅适用于 Apple Mail.app（不支持 Outlook 等其他邮件客户端）

## 高级用法：原始 SQL 查询

如需自定义查询，可以直接使用 sqlite3：

```bash
sqlite3 -header -column ~/Library/Mail/V10/MailData/Envelope\ Index "
SELECT m.ROWID, s.subject, a.address
FROM messages m
JOIN subjects s ON m.subject = s.ROWID
LEFT JOIN addresses a ON m.sender = a.ROWID
WHERE s.subject LIKE '%your query%'
ORDER BY m.date_sent DESC
LIMIT 20;
"
```

## 许可证**

MIT 许可证