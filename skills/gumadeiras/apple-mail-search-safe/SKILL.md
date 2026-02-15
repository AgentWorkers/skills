---
name: apple-mail-search
description: 快速且安全的 Apple Mail 搜索功能，支持查看邮件正文内容。
homepage: https://clawdhub.com/gumadeiras/apple-mail-search-safe
repository: https://github.com/gumadeiras/apple-mail-search-cli
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["fruitmail"]},"install":[{"id":"node","kind":"node","package":"apple-mail-search-cli","bins":["fruitmail"],"label":"Install fruitmail CLI (npm)"}]}}
---

# Fruitmail（快速且安全）

这是一个基于SQLite的苹果邮件应用程序（Apple Mail.app）搜索工具，支持查看邮件的完整内容。

## 安装

```bash
npm install -g apple-mail-search-cli
```

## 使用方法

```bash
# Complex search
fruitmail search --subject "invoice" --days 30 --unread

# Search by sender
fruitmail sender "@amazon.com"

# List unread emails
fruitmail unread

# Read full email body (supports --json)
fruitmail body 94695

# Open in Mail.app
fruitmail open 94695

# Database stats
fruitmail stats
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `search` | 使用过滤器进行复杂搜索 |
| `sender <查询>` | 按发送者邮箱地址搜索 |
| `unread` | 列出未读邮件 |
| `body <id>` | 阅读邮件的完整内容（通过AppleScript） |
| `open <id>` | 在Mail.app中打开邮件 |
| `stats` | 查看数据库统计信息 |

## 搜索选项

```
--subject <text>   Search subject lines
--days <n>         Last N days
--unread           Only unread emails
--limit <n>        Max results (default: 20)
--json             Output as JSON
--copy             Copy DB before query (safest mode)
```

## 示例

```bash
# Find bank statements from last month
fruitmail search --subject "statement" --days 30

# Get unread emails as JSON
fruitmail unread --json | jq '.[] | .subject'

# Find emails from Amazon
fruitmail sender "@amazon.com" --limit 50
```

## 性能

| 方法 | 搜索13万封邮件所需时间 |
|--------|---------------------|
| AppleScript（全遍历） | 8分钟以上 |
| SQLite（本工具） | **约50毫秒** |

## 技术细节

- **数据库位置：** `~/Library/Mail/V{9,10,11}/MailData/Envelope Index` |
- **查询方式：** 使用SQLite（只读）结合AppleScript来获取邮件内容 |
- **安全性：** 仅支持只读操作，防止数据被修改；支持可选的`--copy`模式用于复制数据 |

## 注意事项

- **仅适用于macOS** — 该工具会查询Apple Mail.app的本地数据库 |
- **仅支持读取操作** — 无法发送或新建邮件 |
- **如需发送邮件，请使用`himalaya`工具（支持IMAP/SMTP协议） |

## 来源

https://github.com/gumadeiras/apple-mail-search-cli