---
name: clippy
description: Microsoft 365 / Outlook CLI：用于管理 Outlook 日历（查看、创建、更新、删除事件、查找会议时间、回复邀请）、发送/阅读电子邮件，以及在组织内搜索人员或会议室。
metadata: {"clawdbot":{"requires":{"bins":["clippy"]}}}
---

# Clippy - Microsoft 365 命令行工具 (Microsoft 365 CLI)

来源：https://github.com/foeken/clippy

该工具通过浏览器自动化（使用 Playwright）来操作 Microsoft 365 的 Web 界面，而非通过 Graph API。无需注册 Azure AD 账户，只需使用浏览器登录即可。

## 安装

```bash
git clone https://github.com/foeken/clippy.git
cd clippy && bun install
bun run src/cli.ts --help
```

或者全局链接：`bun link`

## 认证

```bash
# Interactive login (opens browser, establishes session)
clippy login --interactive

# Check auth status
clippy whoami
```

### 保持会话活跃（推荐）

为防止令牌过期，请保持浏览器会话处于活跃状态：

```bash
# Start keepalive (keeps browser open, refreshes every 10min)
clippy keepalive --interval 10
```

若需持续运行该工具，可在 macOS 上将其设置为 launchd 服务，在 Linux 上设置为 systemd 服务。

**健康检查：**每次成功刷新时，Clippy 会向 `~/.config/clippy/keepalive-health.txt` 文件中写入信息。若该文件超过 15 分钟未更新，则表示工具出现故障。

## 日历功能

```bash
# Today's events
clippy calendar

# Specific day
clippy calendar --day tomorrow
clippy calendar --day monday
clippy calendar --day 2024-02-15

# Week view
clippy calendar --week

# With details (description, attendees)
clippy calendar --details
```

### 创建事件

```bash
clippy create-event "Title" 09:00 10:00

# Full options
clippy create-event "Meeting" 14:00 15:00 \
  --day tomorrow \
  --description "Meeting notes" \
  --attendees "alice@company.com,bob@company.com" \
  --teams \
  --find-room

# Recurring
clippy create-event "Standup" 09:00 09:15 --repeat daily
clippy create-event "Sync" 14:00 15:00 --repeat weekly --days mon,wed,fri
```

### 更新/删除事件

```bash
clippy update-event 1 --title "New Title"
clippy update-event 1 --start 10:00 --end 11:00
clippy delete-event 1
clippy delete-event 1 --message "Need to reschedule"
```

### 回应邀请

```bash
clippy respond                           # List pending
clippy respond accept --id <eventId>
clippy respond decline --id <eventId> --message "Conflict"
clippy respond tentative --id <eventId>
```

### 查找会议时间

```bash
clippy findtime
clippy findtime --attendees "alice@company.com,bob@company.com"
clippy findtime --duration 60 --days 5
```

## 邮件功能

```bash
# Inbox
clippy mail
clippy mail --unread
clippy mail -n 20
clippy mail --search "invoice"

# Other folders
clippy mail sent
clippy mail drafts
clippy mail archive

# Read email
clippy mail -r <number>

# Download attachments
clippy mail -d <number> -o ~/Downloads
```

### 发送邮件

```bash
clippy send \
  --to "recipient@example.com" \
  --subject "Subject" \
  --body "Message body"

# With CC, attachments, markdown
clippy send \
  --to "alice@example.com" \
  --cc "manager@example.com" \
  --subject "Report" \
  --body "**See attached**" \
  --markdown \
  --attach "report.pdf"
```

### 回复/转发邮件

```bash
clippy mail --reply <number> --message "Thanks!"
clippy mail --reply-all <number> --message "Got it"
clippy mail --forward <number> --to-addr "colleague@example.com"
```

### 邮件相关操作

```bash
clippy mail --mark-read <number>
clippy mail --flag <number>
clippy mail --move <number> --to archive
```

## 人员/会议室搜索

```bash
clippy find "john"                       # People
clippy find "conference" --rooms         # Rooms
```

## JSON 输出

```bash
clippy calendar --json
clippy mail --json
```

## 配置

配置文件目录可以自定义：
```bash
export CLIPPY_PROFILE_DIR=~/.config/clippy/my-profile
```