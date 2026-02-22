---
name: outlook
description: 通过 Microsoft Graph API 读取、搜索和管理 Outlook 邮件及日历。当用户询问有关邮件、收件箱、Outlook、Microsoft 邮件、日历事件或日程安排的信息时，可使用此功能。
version: 1.9.0
author: cristiandan
homepage: https://github.com/cristiandan/outlook-skill
metadata: {"clawdbot":{"requires":{"bins":["az","jq"]},"credentials":{"note":"Setup creates Azure App Registration and stores client_id/client_secret/OAuth tokens in ~/.outlook-mcp. The token script can print access tokens. Treat these as sensitive."}}}
---
# Outlook Skill

通过 Microsoft Graph API 使用 OAuth2 访问 Outlook/Hotmail 的电子邮件和日历功能。

## 快速设置（自动化）

```bash
# Requires: Azure CLI, jq
./scripts/outlook-setup.sh
```

设置脚本将：
1. 使用设备代码流登录 Azure
2. 自动创建应用程序注册
3. 配置 API 权限（Mail.ReadWrite, Mail.Send, Calendars.ReadWrite）
4. 指导您完成授权过程
5. 将凭据保存到 `~/.outlook-mcp/` 文件夹中

## 手动设置

请参阅 `references/setup.md` 以获取通过 Azure 门户进行手动配置的详细步骤。

## 多个账户

您可以连接多个 Outlook 账户（个人账户、工作账户等）：

### 设置额外账户
```bash
./scripts/outlook-setup.sh --account work
./scripts/outlook-setup.sh --account personal
```

### 使用特定账户
```bash
./scripts/outlook-mail.sh --account work inbox
./scripts/outlook-calendar.sh --account personal today
./scripts/outlook-token.sh --account work refresh
```

### 或使用环境变量
```bash
export OUTLOOK_ACCOUNT=work
./scripts/outlook-mail.sh inbox
```

### 列出已配置的账户
```bash
./scripts/outlook-token.sh list
```

凭据分别存储在以下位置：
```
~/.outlook-mcp/
  default/
    config.json
    credentials.json
  work/
    config.json  
    credentials.json
```

现有的单账户设置会自动迁移到 `default` 账户。

## 使用方法

### 令牌管理
```bash
./scripts/outlook-token.sh refresh       # Refresh expired token
./scripts/outlook-token.sh test          # Test connection
./scripts/outlook-token.sh get --confirm # Print access token (requires confirmation)
```

### 阅读电子邮件
```bash
./scripts/outlook-mail.sh inbox [count]           # List latest emails (default: 10)
./scripts/outlook-mail.sh unread [count]          # List unread emails
./scripts/outlook-mail.sh search "query" [count]  # Search emails (KQL syntax)
./scripts/outlook-mail.sh from <email> [count]    # List emails from sender
./scripts/outlook-mail.sh read <id>               # Read email content
./scripts/outlook-mail.sh attachments <id>        # List email attachments
```

### 高级查询
```bash
# Date range filters
./scripts/outlook-mail.sh query --after 2024-01-01 --before 2024-01-31

# Folder + unread filter
./scripts/outlook-mail.sh query --folder Inbox --unread --count 50

# Sender + attachments filter
./scripts/outlook-mail.sh query --from boss@work.com --has-attachments

# Combined filters
./scripts/outlook-mail.sh query --after 2024-06-01 --folder "Sent Items" --count 100
```

查询选项：
- `--after DATE` — 在指定日期之后收到的电子邮件（格式：YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS）
- `--before DATE` — 在指定日期之前收到的电子邮件
- `--folder NAME` — 在指定文件夹中搜索
- `--from EMAIL` — 按发件人电子邮件过滤
- `--unread` — 仅显示未读邮件
- `--has-attachments` — 仅显示包含附件的邮件
- `--count N` — 最大显示结果数量（默认：20）

### 管理电子邮件
```bash
./scripts/outlook-mail.sh mark-read <id>          # Mark as read
./scripts/outlook-mail.sh mark-unread <id>        # Mark as unread
./scripts/outlook-mail.sh flag <id>               # Flag as important
./scripts/outlook-mail.sh unflag <id>             # Remove flag
./scripts/outlook-mail.sh delete <id>             # Move to trash
./scripts/outlook-mail.sh archive <id>            # Move to archive
./scripts/outlook-mail.sh move <id> <folder>      # Move to folder
```

### 发送电子邮件
```bash
./scripts/outlook-mail.sh send <to> <subj> <body> # Send new email
./scripts/outlook-mail.sh reply <id> "body"       # Reply to email
```

### 文件夹与统计信息
```bash
./scripts/outlook-mail.sh folders                 # List mail folders
./scripts/outlook-mail.sh stats                   # Inbox statistics
```

## 日历

### 查看事件
```bash
./scripts/outlook-calendar.sh events [count]      # List upcoming events
./scripts/outlook-calendar.sh today               # Today's events
./scripts/outlook-calendar.sh week                # This week's events
./scripts/outlook-calendar.sh read <id>           # Event details
./scripts/outlook-calendar.sh calendars           # List all calendars
./scripts/outlook-calendar.sh free <start> <end>  # Check availability
```

### 创建事件
```bash
./scripts/outlook-calendar.sh create <subj> <start> <end> [location]  # Create event
./scripts/outlook-calendar.sh quick <subject> [time]                  # Quick 1-hour event
```

### 管理事件
```bash
./scripts/outlook-calendar.sh update <id> <field> <value>  # Update (subject/location/start/end)
./scripts/outlook-calendar.sh delete <id>                  # Delete event
```

日期格式：`YYYY-MM-DDTHH:MM`（例如：`2026-01-26T10:00`

### 示例输出

```bash
$ ./scripts/outlook-mail.sh inbox 3

{
  "n": 1,
  "subject": "Your weekly digest",
  "from": "digest@example.com",
  "date": "2026-01-25T15:44",
  "read": false,
  "id": "icYY6QAIUE26PgAAAA=="
}
{
  "n": 2,
  "subject": "Meeting reminder",
  "from": "calendar@outlook.com",
  "date": "2026-01-25T14:06",
  "read": true,
  "id": "icYY6QAIUE26PQAAAA=="
}

$ ./scripts/outlook-mail.sh read "icYY6QAIUE26PgAAAA=="

{
  "subject": "Your weekly digest",
  "from": { "name": "Digest", "address": "digest@example.com" },
  "to": ["you@hotmail.com"],
  "date": "2026-01-25T15:44:00Z",
  "body": "Here's what happened this week..."
}

$ ./scripts/outlook-mail.sh stats

{
  "folder": "Inbox",
  "total": 14098,
  "unread": 2955
}

$ ./scripts/outlook-calendar.sh today

{
  "n": 1,
  "subject": "Team standup",
  "start": "2026-01-25T10:00",
  "end": "2026-01-25T10:30",
  "location": "Teams",
  "id": "AAMkAGQ5NzE4YjQ3..."
}

$ ./scripts/outlook-calendar.sh create "Lunch with client" "2026-01-26T13:00" "2026-01-26T14:00" "Restaurant"

{
  "status": "event created",
  "subject": "Lunch with client",
  "start": "2026-01-26T13:00",
  "end": "2026-01-26T14:00",
  "id": "AAMkAGQ5NzE4YjQ3..."
}
```

## 令牌刷新

访问令牌在大约 1 小时后失效。请使用以下命令刷新令牌：
```bash
./scripts/outlook-token.sh refresh
```

## 文件

- `~/.outlook-mcp/config.json` - 客户端 ID 和密钥
- `~/.outlook-mcp/credentials.json` - OAuth 令牌（包括访问令牌和刷新令牌）

## 权限

- `Mail.ReadWrite` — 读取和修改电子邮件
- `Mail.Send` — 发送电子邮件
- `Calendars.ReadWrite` — 读取和修改日历事件
- `offline_access` — 刷新令牌（保持登录状态）
- `User.Read` — 基本用户信息

## 注意事项

- **电子邮件 ID**：`id` 字段显示了完整邮件 ID 的最后 20 个字符。请使用此 ID 来执行 `read`、`mark-read`、`delete` 等命令。
- **邮件编号**：电子邮件会按顺序编号（例如：1、2、3……），以便于引用。
- **文本提取**：HTML 格式的邮件正文会自动转换为纯文本。
- **令牌过期**：访问令牌在大约 1 小时后失效。如果出现授权错误，请运行 `outlook-token.sh refresh` 命令刷新令牌。
- **最近收到的邮件**：`read`、`mark-read` 等命令会从最近的 100 封邮件中查找相应的邮件。

## 故障排除

- **“令牌过期”**：运行 `outlook-token.sh refresh` 命令刷新令牌。
- **“授权无效”**：令牌无效，请重新运行 `outlook-setup.sh` 进行设置。
- **“权限不足”**：请在 Azure 门户中检查应用程序权限（API 权限设置）。
- **“找不到邮件”**：该邮件可能已超出存储限制（最多存储 100 封邮件），请先使用搜索功能查找。
- **“找不到文件夹”**：请使用准确的文件夹名称。运行 `folders` 命令查看可用的文件夹。

## 支持的账户类型

- 个人 Microsoft 账户（outlook.com、hotmail.com、live.com）
- 工作/学校账户（Microsoft 365）——可能需要管理员授权

## 安全注意事项

- **Azure 应用程序注册**：自动化设置会在您的 Azure 租户中创建一个具有以下权限的应用程序注册：`Mail.ReadWrite`、`Mail.Send`、`Calendars.ReadWrite`、`offline_access`、`User.Read`。
- **本地凭据存储**：客户端 ID、客户端密钥和 OAuth 令牌存储在 `~/.outlook-mcp/` 文件夹中，文件权限设置为 `chmod 600`。
- **令牌显示**：运行 `outlook-token.sh get --confirm` 命令可以查看访问令牌（需要明确指定此选项）。
- **先决条件**：需要安装 [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) 和 `jq` 工具。

如果您不希望使用自动化设置，请按照 `references/setup.md` 中的说明进行手动配置。