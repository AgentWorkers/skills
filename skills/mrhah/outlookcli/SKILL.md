---
name: outlook
description: >
  通过 `m365-cli` 命令行工具管理个人 Microsoft 365 (Outlook.com/Hotmail/Live) 的电子邮件、日历和 OneDrive。**所需环境**：Node.js 18 及更高版本，以及全局安装的 `m365-cli`（使用 `npm install -g m365-cli` 进行安装），同时需要 OAuth 认证（执行 `m365 login --account-type personal`）。该工具可以访问敏感数据，包括电子邮件、日历事件、OneDrive 文件和联系人。**使用场景**：  
  - 阅读、发送或搜索电子邮件  
  - 管理日历事件（列出、创建、更新、删除）  
  - 上传/下载 OneDrive 文件  
  - 搜索用户/联系人  
  - 删除或移动电子邮件  
  - 管理邮件文件夹  
  - 通过终端执行任何与个人 Outlook/Hotmail/Live 账户相关的操作  
  **可执行的命令示例**：  
  - `check my email`：检查我的电子邮件  
  - `send an email`：发送电子邮件  
  - `schedule a meeting`：安排会议  
  - `list my calendar`：列出我的日历  
  - `upload to OneDrive`：上传文件到 OneDrive  
  - `download from OneDrive`：从 OneDrive 下载文件  
  - `search mail`：搜索邮件  
  - `what's on my calendar`：查看我的日历安排  
  - `manage Outlook`：管理 Outlook 账户  
  - `delete email`：删除电子邮件  
  - `move email`：移动电子邮件  
  - `mail folders`：操作邮件文件夹  
  - `create folder`：创建文件夹  
  - `organize email`：整理邮件
  Manage personal Microsoft 365 (Outlook.com/Hotmail/Live) email, calendar, and OneDrive
  via the m365-cli command-line tool. Requires: Node.js 18+ and `m365-cli` installed globally
  (`npm install -g m365-cli`), plus OAuth authentication (`m365 login --account-type personal`).
  Accesses sensitive data: emails, calendar events, OneDrive files, and contacts.
  Use when: (1) reading, sending, or searching emails,
  (2) managing calendar events (list, create, update, delete), (3) uploading/downloading OneDrive files,
  (4) searching users/people, (5) deleting or moving emails, (6) managing mail folders,
  (7) any task involving personal Outlook/Hotmail/Live account management
  from the terminal. Triggers: "check my email", "send an email", "schedule a meeting",
  "list my calendar", "upload to OneDrive", "download from OneDrive", "search mail",
  "what's on my calendar", "manage Outlook", "m365", "outlook", "delete email",
  "move email", "mail folders", "create folder", "organize email".
---
# Outlook Skill (m365-cli)

通过 `m365` CLI 管理个人 Microsoft 账户（Outlook.com / Hotmail / Live）。
使用 `--json` 选项可获取结构化输出，以便 AI 代理使用（大多数命令都支持该选项）。

## 先决条件

- Node.js 18 及以上版本
- 全局安装了 `m365-cli`：`npm install -g m365-cli`
- 已登录：`m365 login --account-type personal`

如果尚未登录，请先执行登录操作。该 CLI 使用设备代码流（Device Code Flow）进行身份验证——请按照屏幕上的提示操作。

## 关键约定

- **使用 `--json` 选项** 以获取程序化输出（大多数命令支持该选项；`trust`/`untrust` 选项不支持）。
- **个人账户** 支持以下功能：邮件（包括删除、移动和文件夹管理）、日历、OneDrive、用户搜索。**不** 支持 SharePoint。
- 日历日期格式：`YYYY-MM-DDTHH:MM:SS`（本地时间）或 `YYYY-MM-DD`（全天事件）。
- **ID**：邮件/事件的 ID 是长字符串。请从 `--json` 的列表/搜索输出中解析 `id` 字段。
- 时区：自动检测；如需自定义，请设置 `export M365_TIMEZONE="Asia/Shanghai"`。

## 快速工作流程参考

### 登录

```bash
m365 login --account-type personal    # First-time login
m365 logout                           # Clear credentials
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

有关共享、邀请和高级 OneDrive 功能，请参阅 [references/commands.md](references/commands.md)。

### 用户搜索

```bash
m365 user search "John" --top 5 --json    # Searches contacts and people
```

## 常用操作模式

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

## 可信发送者（安全设置）

`m365 mail read` 会过滤不可信发送者的邮件内容（仅显示元数据）。如需忽略此过滤，请使用 `--force` 选项。
有关白名单管理的命令，请参阅 [references/commands.md](references/commands.md#m365-mail-trust)。

## 完整命令参考

请参阅 [references/commands.md](references/commands.md)，了解所有命令、子命令、标志及默认值的详细信息。

## 故障排除

- **“未登录”**：`m365 login --account-type personal`
- **令牌过期**：系统会自动刷新令牌；如果失败，请重新登录。
- **SharePoint 相关错误**：个人账户不支持 SharePoint 功能。
- **时区错误**：设置 `export M365_TIMEZONE="Your/Timezone"` 以调整时区。

## 安全与隐私

此技能会访问用户的个人邮件、日历、文件和联系人信息——这些都属于敏感的个人信息（PII）。

- **切勿** 阅读、输出或记录 `~/.m365-cli/credentials.json` 文件，因为其中包含 OAuth 令牌。
- **除非用户明确要求，否则** **切勿** 在代理输出中包含完整的邮件正文或附件内容。
- **在向用户展示结果时**，请**总结** 邮件内容而非逐字复制。
- **令牌更新** 是自动进行的；切勿尝试手动编辑或解析该文件。
- 在列出邮件时，建议优先显示元数据（主题、发送者、日期）而非邮件正文。