---
name: outlook
description: 通过 Microsoft Graph API 读取、搜索和管理 Outlook 邮件及日历。当用户询问有关邮件、收件箱、Outlook、Microsoft 邮件、日历事件或日程安排的信息时，可以使用此功能。
version: 1.3.0
author: jotamed
---

# Outlook Skill

通过使用 OAuth2 和 Microsoft Graph API，您可以访问 Outlook/Hotmail 的电子邮件和日历功能。

## 快速设置（自动化）

```bash
# Requires: Azure CLI, jq
./scripts/outlook-setup.sh
```

设置脚本将完成以下操作：
1. 使用设备代码流登录 Azure
2. 自动创建应用程序注册
3. 配置 API 权限（Mail.ReadWrite、Mail.Send、Calendars.ReadWrite）
4. 指导您完成授权过程
5. 将凭据保存到 `~/.outlook-mcp/` 文件夹中

## 手动设置

请参阅 `references/setup.md`，了解如何通过 Azure 门户进行手动配置的详细步骤。

## 使用方法

### 令牌管理
```bash
./scripts/outlook-token.sh refresh  # Refresh expired token
./scripts/outlook-token.sh test     # Test connection
./scripts/outlook-token.sh get      # Print access token
```

### 阅读电子邮件
```bash
./scripts/outlook-mail.sh inbox [count]           # List latest emails (default: 10)
./scripts/outlook-mail.sh unread [count]          # List unread emails
./scripts/outlook-mail.sh search "query" [count]  # Search emails
./scripts/outlook-mail.sh from <email> [count]    # List emails from sender
./scripts/outlook-mail.sh read <id>               # Read email content
./scripts/outlook-mail.sh attachments <id>        # List email attachments
```

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

访问令牌大约 1 后会过期。请使用以下命令刷新令牌：

```bash
./scripts/outlook-token.sh refresh
```

## 文件夹与配置文件

- `~/.outlook-mcp/config.json` – 客户端 ID 和密钥
- `~/.outlook-mcp/credentials.json` – OAuth 令牌（包括访问令牌和刷新令牌）

## 权限说明

- `Mail.ReadWrite`：读取和修改电子邮件
- `Mail.Send`：发送电子邮件
- `Calendars.ReadWrite`：读取和修改日历事件
- `offline_access`：允许在离线状态下保持登录状态
- `User.Read`：读取基本用户信息

## 注意事项

- **电子邮件 ID**：`id` 字段显示了完整邮件 ID 的最后 20 个字符。请使用此 ID 来执行 `read`、`mark-read`、`delete` 等操作。
- **结果编号**：电子邮件会按顺序编号（例如：1、2、3……），以便于查找。
- **文本提取**：HTML 格式的邮件正文会自动转换为纯文本。
- **令牌过期**：访问令牌大约 1 后会过期。如果出现授权错误，请运行 `outlook-token.sh refresh` 命令刷新令牌。
- **最近收到的邮件**：`read`、`mark-read` 等命令会从最近收到的 100 封邮件中查找目标邮件。

## 故障排除

- **“令牌过期”**：运行 `outlook-token.sh refresh` 命令刷新令牌。
- **“授权失败”**：令牌无效，请重新运行 `outlook-setup.sh` 进行设置。
- **“权限不足”**：请在 Azure 门户中检查应用程序权限（API 权限设置）。
- **“邮件未找到”**：该邮件可能不在最近收到的 100 封邮件范围内，请使用搜索功能查找。
- **“文件夹未找到”**：请使用准确的文件夹名称。运行 `folders` 命令查看可用的文件夹。

## 支持的账户类型

- 个人 Microsoft 账户（outlook.com、hotmail.com、live.com）
- 工作/学校账户（Microsoft 365）：可能需要管理员授权

## 更新日志

### v1.3.0
- 新增：日历功能（`outlook-calendar.sh`）
  - 查看事件（今日、本周、即将发生的事件）
  - 创建/快速创建事件
  - 更新事件详情（主题、地点、时间）
  - 删除事件
  - 查看事件可用性（空闲/忙碌）
  - 列出日历
- 新增：`Calendars.ReadWrite` 权限

### v1.2.0
- 新增：`mark-unread`：将邮件标记为未读
- 新增：`flag/unflag`：将邮件标记为重要或取消标记
- 新增：`delete`：将邮件移至垃圾箱
- 新增：`archive`：将邮件归档
- 新增：`move`：将邮件移动到任意文件夹
- 新增：`from`：按发件人过滤邮件
- 新增：`attachments`：列出邮件附件
- 新增：`reply`：回复邮件
- 优化：`send` 命令的错误处理和状态输出
- 优化：`move` 命令：支持不区分大小写的文件夹名称，并在出错时显示可用文件夹

### v1.1.0
- 修复：电子邮件 ID 现在会使用唯一的后缀（最后 20 个字符）
- 新增：结果按顺序编号（例如：1、2、3……）
- 优化：HTML 格式的邮件正文会自动转换为纯文本
- 新增：在阅读结果中显示 `to` 字段

### v1.0.0
- 首次发布