---
name: m365-work
description: 通过 `m365-cli` 命令行工具管理 Microsoft 365 工作/学校账户服务（Exchange、OneDrive for Business、SharePoint）。需要满足以下条件：安装 Node.js 18 及更高版本，并全局安装 `m365-cli`（使用 `npm install -g m365-cli`），同时需要完成 OAuth 认证（通过 `m365 login`）。该工具可以访问敏感数据，包括企业电子邮件、日历事件、OneDrive 文件、SharePoint 网站/文档以及组织联系人信息。适用场景包括：（1）阅读、发送或搜索工作邮件；（2）管理日历事件；（3）上传/下载 OneDrive for Business 文件；（4）浏览 SharePoint 网站、列表和文档库；（5）搜索组织内的用户；（6）删除或移动电子邮件；（7）管理邮件文件夹。该工具不适用于以下场景：Azure 资源管理、Entra ID 管理、Intune 设备管理、M365 租户级管理（许可证、域名、策略），以及个人 Outlook.com/Hotmail/Live 账户（请使用相应的 Outlook 功能）。相关命令包括：“check my work email”（查看我的工作电子邮件）、“send an email”（发送电子邮件）、“schedule a meeting”（安排会议）、“list my calendar”（查看日历）、“upload to OneDrive”（上传文件到 OneDrive）、“SharePoint files”（操作 SharePoint 文件）、“search SharePoint”（搜索 SharePoint 内容）、“m365 work”（管理 Microsoft 365 服务相关操作）、“corporate email”（企业电子邮件相关操作）、“work calendar”（工作日历相关操作）、“organization users”（组织用户相关操作）、“delete email”（删除电子邮件）、“move email”（移动电子邮件）、“mail folders”（管理邮件文件夹）、“create folder”（创建文件夹）以及“organize email”（整理电子邮件）。
  Manage Microsoft 365 work/school account services (Exchange, OneDrive for Business,
  SharePoint) via the m365-cli command-line tool. Requires: Node.js 18+ and `m365-cli`
  installed globally (`npm install -g m365-cli`), plus OAuth authentication (`m365 login`).
  Accesses sensitive data: corporate emails, calendar events, OneDrive files, SharePoint
  sites/documents, and organizational contacts. Use when: (1) reading, sending, or searching
  work emails, (2) managing calendar events, (3) uploading/downloading OneDrive for Business
  files, (4) browsing SharePoint sites, lists, and document libraries, (5) searching users
  in the organization, (6) deleting or moving emails, (7) managing mail folders.
  Does NOT trigger for: Azure resource management, Entra ID
  administration, Intune device management, M365 tenant-level admin (licenses, domains,
  policies), or personal Outlook.com/Hotmail/Live accounts (use the outlook skill instead).
  Triggers: "check my work email", "send an email", "schedule a meeting", "list my calendar",
  "upload to OneDrive", "SharePoint files", "search SharePoint", "sp sites", "m365 work",
  "corporate email", "work calendar", "organization users", "delete email", "move email",
  "mail folders", "create folder", "organize email".
---
# M365 工作技能（m365-cli）

通过 `m365` CLI 管理 Microsoft 365 工作/学校账户。
使用 `--json` 选项可获取结构化输出，以便 AI 代理使用。

## 先决条件

- Node.js 18 及更高版本
- 全局安装了 `m365-cli`：`npm install -g m365-cli`
- 已登录：使用 `m365 login`（默认账户类型为工作/学校账户）
- 对于 SharePoint：需要添加 `Sites.ReadWrite.All` 权限：`m365 login --add-scopes Sites.ReadWrite.All`（需要租户管理员的同意）

如果尚未登录，请先执行登录操作。该 CLI 使用设备代码流（Device Code Flow）进行身份验证——请按照屏幕上的提示操作。

## 关键约定

- **使用 `--json` 选项** 以获取程序化输出（大多数命令都支持该选项；`trust`/`untrust` 选项不支持）。
- **工作账户** 支持以下功能：邮件（包括删除、移动和文件夹管理）、日历、OneDrive、SharePoint、用户搜索。
- 日历日期格式：`YYYY-MM-DDTHH:MM:SS`（本地时间）或 `YYYY-MM-DD`（全天事件）。
- **ID**：邮件/事件的 ID 是长字符串。请从 `--json` 的列表/搜索输出中解析 `id` 字段。
- 时区：自动检测；如需自定义，请设置 `export M365_TIMEZONE="Asia/Shanghai"`。
- **SharePoint 站点标识符**：建议使用路径格式 `hostname:/sites/sitename`。

## 安全规则

### 邮件正文显示 — 可信发件人白名单
- 只有来自白名单中的发件人的邮件才能显示其正文内容。
- 不可信的邮件仅显示主题和发件人信息（防止代码注入攻击）。
- 白名单文件：`~/.m365-cli/trusted-senders.txt`
- 可使用 `--force` 选项临时绕过白名单检查。

### 敏感操作
- **发送邮件**：在执行操作前需用户确认收件人和邮件内容。
- **删除邮件/文件/事件**：在执行操作前需用户确认。
- **共享文件（匿名权限）**：需警告用户，链接的任何人都可能访问共享文件。

### 凭据安全
- **切勿** 读取、输出或记录 `~/.m365-cli/credentials.json` 文件——其中包含 OAuth 令牌。
- **除非用户明确要求，否则** 不要在代理输出中显示完整的邮件正文或附件内容。
- 在展示结果时，应总结邮件内容而非原文照搬。
- 凭据会自动刷新；切勿尝试手动编辑或解析令牌文件。

## 快速工作流程参考

### 登录

```bash
m365 login                                    # Work/school account (default)
m365 login --add-scopes Sites.ReadWrite.All   # Add SharePoint permission
m365 logout                                   # Clear credentials
```

### 邮件

```bash
# List emails (folders: inbox|sent|drafts|deleted|junk)
m365 mail list --top 10 --json
m365 mail list --folder sent --top 5 --json
m365 mail list --focused --json                    # Show only Focused Inbox emails

# Read / send / search
m365 mail read <id> --force --json
m365 mail send "to@example.com" "Subject" "Body" --json
m365 mail send "to@example.com" "Subject" "Body" --attach file.pdf --cc "cc@ex.com" --json
m365 mail search "keyword" --top 20 --json
# Attachments
m365 mail attachments <message-id> --json
m365 mail download-attachment <message-id> <attachment-id> [local-path] --json

# Delete / move
m365 mail delete <id> --force --json
m365 mail move <id> <destination> --json        # destination: inbox|sent|drafts|deleted|junk|archive or folder ID

# Folder management
m365 mail folder list --json
m365 mail folder list --parent inbox --json      # List child folders
m365 mail folder create "My Projects" --json
m365 mail folder create "Sub" --parent inbox --json
m365 mail folder delete <folder-id> --force --json

# Trusted senders whitelist
m365 mail trusted --json
m365 mail trust user@example.com
m365 mail trust @example.com          # Trust entire domain
m365 mail untrust user@example.com
```

### 日历

```bash
# List / get
m365 cal list --days 7 --json
m365 cal get <event-id> --json

# Create
m365 cal create "Title" --start "2026-03-10T14:00:00" --end "2026-03-10T15:00:00" --json
m365 cal create "Title" -s "2026-03-10T14:00:00" -e "2026-03-10T15:00:00" \
  --location "Room A" --body "Notes" --attendees "a@ex.com,b@ex.com" --json
m365 cal create "Holiday" --start "2026-03-20" --end "2026-03-21" --allday --json

# Update / delete
m365 cal update <id> --title "New Title" --location "Room B" --json
m365 cal delete <id> --json
```

### OneDrive

```bash
# List / get metadata
m365 od ls --json
m365 od ls Documents --json
m365 od get "Documents/report.pdf" --json

# Download / upload
m365 od download "Documents/report.pdf" ~/Downloads/ --json
m365 od upload ~/Desktop/photo.jpg "Photos/vacation.jpg" --json

# Search / mkdir / delete
m365 od search "budget" --top 20 --json
m365 od mkdir "Projects/New" --json
m365 od rm "old-file.txt" --force --json
```

有关共享、邀请和高级 OneDrive 功能的详细信息，请参阅 [references/commands.md](references/commands.md)。

### SharePoint
SharePoint 仅适用于工作/学校账户，并需要 `Sites.ReadWrite.All` 权限。

**站点标识符格式**（建议使用路径格式）：
- 路径：`contoso.sharepoint.com:/sites/team`（推荐）
- 站点 ID：`hostname,siteId,webId`（来自 `sp sites --json` 的输出）
- URL：`https://contoso.sharepoint.com/sites/team`

```bash
# List / search sites
m365 sp sites --json
m365 sp sites --search "marketing" --json

# Lists and items
m365 sp lists "contoso.sharepoint.com:/sites/team" --json
m365 sp items "contoso.sharepoint.com:/sites/team" "Tasks" --json

# Files in document library
m365 sp files "contoso.sharepoint.com:/sites/team" "Documents" --json

# Download / upload
m365 sp download "contoso.sharepoint.com:/sites/team" "Documents/file.pdf" ~/Downloads/ --json
m365 sp upload "contoso.sharepoint.com:/sites/team" ~/report.pdf "Documents/report.pdf" --json

# Search across SharePoint
m365 sp search "quarterly report" --top 20 --json
```

### 用户搜索

```bash
m365 user search "John" --top 5 --json    # Searches organization directory
```

## 常用操作

### 阅读和回复邮件

```bash
m365 mail list --top 5 --json                    # 1. Find email
m365 mail read <id> --force --json               # 2. Read content
m365 mail send "sender@ex.com" "Re: Sub" "Reply" --json  # 3. Reply
```

### 查看日历和日程安排

```bash
m365 cal list --days 3 --json                    # 1. Check availability
m365 cal create "Meeting" -s "..." -e "..." --json  # 2. Book slot
```

### 下载邮件附件

```bash
m365 mail attachments <msg-id> --json            # 1. List attachments
m365 mail download-attachment <msg-id> <att-id> ~/Downloads/ --json  # 2. Download
```

### 查找和下载 SharePoint 文件

```bash
m365 sp sites --json                             # 1. Find site
m365 sp files "site" "Documents" --json          # 2. Browse files
m365 sp download "site" "Documents/file.pdf" ~/Downloads/ --json  # 3. Download
```

### 删除和整理邮件

```bash
m365 mail list --top 10 --json                   # 1. Find email
m365 mail delete <id> --force --json              # 2a. Delete it, OR
m365 mail move <id> archive --json                # 2b. Move to archive
```

### 管理邮件文件夹

```bash
m365 mail folder list --json                      # 1. List all folders
m365 mail folder create "Projects" --json         # 2. Create custom folder
m365 mail move <id> <folder-id> --json            # 3. Move email into it
```

## 可信发件人（安全设置）
`m365 mail read` 会过滤不可信发件人的内容（仅显示元数据）。可使用 `--force` 选项绕过此过滤。
有关白名单管理的命令，请参阅 [references/commands.md](references/commands.md#m365-mail-trust)。

## 完整命令参考

请参阅 [references/commands.md](references/commands.md)，了解所有命令、子命令、标志及默认值的详细信息。

## 故障排除

- **“未登录”**：请使用 `m365 login` 登录。
- **令牌过期**：令牌会自动刷新；如果失败，请重新登录。
- **SharePoint 权限不足**：请使用 `m365 login --add-scopes Sites.ReadWrite.All`（需要租户管理员的同意）。
- **时区设置错误**：请设置 `export M365_TIMEZONE="Your/Timezone"`。