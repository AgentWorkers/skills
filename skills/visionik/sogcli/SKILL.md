---
name: sog
description: Standards Ops Gadget — 这是一款用于 IMAP/SMTP/CalDAV/CardDAV/WebDAV 的命令行工具（CLI）。它是 Google 的 gog 和 Microsoft 的 mog 的开源替代品，遵循开放标准（Open Standards）。
homepage: https://github.com/visionik/sogcli
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["sog"]},"install":[{"id":"go","kind":"go","package":"github.com/visionik/sogcli/cmd/sog@latest","bins":["sog"],"label":"Install sog (go install)"}]}}
---

# sog — 标准操作工具（Standards Operations Gadget）

这是一个用于处理 IMAP/SMTP/CalDAV/CardDAV/WebDAV 协议的命令行工具（CLI），是 Google 的 gog 和 Microsoft 的 mog 的开源替代品。

## 快速入门

```bash
sog auth add you@fastmail.com --discover
sog auth test
sog mail list
```

## 全局参数

```
--account, -a    Account email to use ($SOG_ACCOUNT)
--json           JSON output (for scripting)
--plain          TSV output (parseable)
--force          Skip confirmations
--no-input       Never prompt (CI mode)
--verbose, -v    Debug logging
--ai-help        Detailed help text
```

## 认证

```bash
sog auth add <email> [flags]
  --discover       Auto-discover servers from DNS
  --imap-host      IMAP server hostname
  --imap-port      IMAP port (default: 993)
  --smtp-host      SMTP server hostname
  --smtp-port      SMTP port (default: 587)
  --caldav-url     CalDAV server URL
  --carddav-url    CardDAV server URL
  --webdav-url     WebDAV server URL
  --password       Password (stored in keychain)

sog auth list                    # List accounts
sog auth test [email]            # Test connection
sog auth remove <email>          # Remove account
sog auth password <email>        # Set protocol-specific passwords
  --imap, --smtp, --caldav, --carddav, --webdav
```

## 邮件（IMAP/SMTP）

```bash
sog mail list [folder]
  --max N          Maximum messages (default: 20)
  --unseen         Only unread messages

sog mail get <uid>
  --headers        Headers only
  --raw            Raw RFC822 format

sog mail search <query>
  # IMAP SEARCH syntax: FROM, TO, SUBJECT, SINCE, BEFORE, etc.
  # Example: sog mail search "FROM john SINCE 1-Jan-2026"

sog mail send --to <email> --subject <text> [flags]
  --to             Recipient(s)
  --cc             CC recipient(s)
  --bcc            BCC recipient(s)
  --subject        Subject line
  --body           Message body
  --body-file      Read body from file (- for stdin)
  --body-html      HTML body content

sog mail reply <uid> --body <text>
sog mail forward <uid> --to <email>
sog mail move <uid> <folder>
sog mail copy <uid> <folder>
sog mail flag <uid> <flag>       # Flags: seen, flagged, answered, deleted
sog mail unflag <uid> <flag>
sog mail delete <uid>
```

## 文件夹

```bash
sog folders list
sog folders create <name>
sog folders delete <name>
sog folders rename <old> <new>
```

## 草稿

```bash
sog drafts list
sog drafts create [flags]        # Same flags as mail send
sog drafts send <uid>
sog drafts delete <uid>
```

## 日历（CalDAV）

```bash
sog cal list [calendar]
  --from           Start date (default: today)
  --to             End date (default: +30d)
  --max            Maximum events

sog cal get <uid>
sog cal search <query>           # Search in title/description/location
sog cal today [calendar]
sog cal week [calendar]

sog cal create <title> --start <datetime> [flags]
  --start          Start time (YYYY-MM-DDTHH:MM or YYYY-MM-DD for all-day)
  --end            End time
  --duration       Duration (1h, 30m)
  --location       Location
  --description    Description

sog cal update <uid> [flags]     # Same flags as create
sog cal delete <uid>
sog cal calendars                # List calendars
```

## 联系人（CardDAV）

```bash
sog contacts list [address-book]
  --max            Maximum contacts

sog contacts get <uid>
sog contacts search <query>      # Search name/email/phone

sog contacts create <name> [flags]
  -e, --email      Email address(es)
  -p, --phone      Phone number(s)
  --org            Organization
  --title          Job title
  --note           Note

sog contacts update <uid> [flags]  # Same flags as create
sog contacts delete <uid>
sog contacts books               # List address books
```

## 任务（CalDAV VTODO）

```bash
sog tasks list [list]
  --all            Include completed tasks

sog tasks add <title> [flags]
  --due            Due date (YYYY-MM-DD)
  -p, --priority   Priority (1-9, 1=highest)
  -d, --description Description

sog tasks get <uid>
sog tasks update <uid> [flags]   # Same flags as add
sog tasks done <uid>             # Mark complete
sog tasks undo <uid>             # Mark incomplete
sog tasks delete <uid>
sog tasks clear                  # Delete all completed tasks
sog tasks due <date>             # Tasks due by date
sog tasks overdue                # Overdue tasks
sog tasks lists                  # List task lists
```

## 文件（WebDAV）

```bash
sog drive ls [path]
  -l               Long format with details
  --all            Show hidden files

sog drive get <path>             # Get file metadata
sog drive download <remote> [local]
sog drive upload <local> [remote]
sog drive mkdir <path>
sog drive delete <path>
sog drive move <src> <dst>
sog drive copy <src> <dst>
sog drive cat <path>             # Output file to stdout
```

## 会议邀请（iTIP/iMIP）

```bash
sog invite send <summary> <attendees>... --start <datetime> [flags]
  --start          Start time
  --duration       Duration (default: 1h)
  --location       Location
  --description    Description

sog invite reply <file> --status <accept|decline|tentative>
  --comment        Optional comment

sog invite cancel <uid> <attendees>...
sog invite parse <file>          # Parse .ics file
sog invite preview <summary> <attendees>... --start <datetime>
```

## IMAP IDLE 模式

```bash
sog idle [folder]                # Watch for new mail (push notifications)
  --timeout        Timeout in seconds
```

## 输出格式

- **默认格式**：易于阅读的彩色输出
- `--json`：每行一个 JSON 对象（JSONL 格式）
- `--plain`：以制表符分隔的值（TSV 格式）

## 使用示例

```bash
# List recent emails
sog mail list --max 10

# Send an email
sog mail send --to user@example.com --subject "Hello" --body "Hi there"
sog mail send --to user@example.com --subject "Report" --body-file report.md
cat draft.txt | sog mail send --to user@example.com --subject "Hi" --body-file -

# Today's calendar
sog cal today

# Create a meeting with invite
sog invite send "Team Sync" alice@example.com bob@example.com \
  --start "2026-01-25T14:00" --duration 30m --location "Zoom"

# Add a task
sog tasks add "Review PR" --due 2026-01-26 -p 1

# Upload a file
sog drive upload report.pdf /documents/

# Search contacts
sog contacts search "John"
```

## 已测试的提供者

- **Fastmail** ✅（完全支持）

其他符合标准的提供者也应该可以正常使用，但尚未经过测试。

## 凭据存储

密码会安全地存储在系统的原生凭据存储库中：

| 平台 | 后端存储机制 |
|----------|---------|
| **macOS** | Keychain（钥匙链） |
| **Windows** | Windows 凭据管理器 |
| **Linux/BSD** | D-Bus Secret Service（GNOME Keyring、KWallet） |

该工具支持为每种协议（IMAP、SMTP、CalDAV、CardDAV、WebDAV）设置不同的密码。

## 注意事项

- 请设置 `SOG_ACCOUNT=you@example.com` 以避免重复输入 `--account` 参数
- 该工具属于 Ops Gadget 系列，包括 gog（Google）、mog（Microsoft）等工具。