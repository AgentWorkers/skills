---
name: google-workspace
description: Gmail、日历、云端硬盘（Drive）、文档（Docs）和表格（Sheets）——无需使用 Google Cloud Console，只需通过 OAuth 进行登录即可。与传统基于 Google API 的集成方式相比，设置过程完全无需复杂操作。
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["mcporter"]}}}
---

# Google Workspace 访问（无需使用 Cloud Console！）

**为什么选择这个技能？** 传统的 Google API 访问方式需要先在 Google Cloud Console 中创建项目、启用相关 API、生成 OAuth 凭据，并下载 `client_secret.json` 文件。而这个技能完全跳过了所有这些步骤。

该技能使用了 `@presto-ai/google-workspace-mcp` 库——只需使用您的 Google 账户登录即可开始使用。

## 主要优势

| 传统方法 | 本技能 |
|-------------------|------------|
| 创建 Google Cloud 项目 | ❌ 不需要 |
| 启用单个 API | ❌ 不需要 |
| 生成 OAuth 凭据 | ❌ 不需要 |
| 下载 `client_secret.json` | ❌ 不需要 |
| 配置重定向 URI | ❌ 不需要 |
| **只需使用 Google 账户登录** | ✅ 简单快捷 |

## 设置（已完成）

```bash
npm install -g @presto-ai/google-workspace-mcp
mcporter config add google-workspace --command "npx" --arg "-y" --arg "@presto-ai/google-workspace-mcp" --scope home
```

首次使用时，系统会打开浏览器进行 Google OAuth 认证。认证信息会存储在 `~/.config/google-workspace-mcp/` 文件中。

## 快速命令

### Gmail
```bash
# Search emails
mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=10

# Get email content
mcporter call --server google-workspace --tool "gmail.get" messageId="<id>"

# Send email
mcporter call --server google-workspace --tool "gmail.send" to="email@example.com" subject="Hi" body="Hello"

# Create draft
mcporter call --server google-workspace --tool "gmail.createDraft" to="email@example.com" subject="Hi" body="Hello"
```

### 日历
```bash
# List calendars
mcporter call --server google-workspace --tool "calendar.list"

# List events
mcporter call --server google-workspace --tool "calendar.listEvents" calendarId="your@email.com" timeMin="2026-01-27T00:00:00Z" timeMax="2026-01-27T23:59:59Z"

# Create event
mcporter call --server google-workspace --tool "calendar.createEvent" calendarId="your@email.com" summary="Meeting" start='{"dateTime":"2026-01-28T10:00:00Z"}' end='{"dateTime":"2026-01-28T11:00:00Z"}'

# Find free time
mcporter call --server google-workspace --tool "calendar.findFreeTime" attendees='["a@example.com","b@example.com"]' timeMin="2026-01-28T09:00:00Z" timeMax="2026-01-28T18:00:00Z" duration=30
```

### 驱动器（Drive）
```bash
# Search files
mcporter call --server google-workspace --tool "drive.search" query="Budget Q3"

# Download file
mcporter call --server google-workspace --tool "drive.downloadFile" fileId="<id>" localPath="/tmp/file.pdf"
```

### 文档（Docs）
```bash
# Find docs
mcporter call --server google-workspace --tool "docs.find" query="meeting notes"

# Read doc
mcporter call --server google-workspace --tool "docs.getText" documentId="<id>"

# Create doc
mcporter call --server google-workspace --tool "docs.create" title="New Doc" markdown="# Hello"
```

### 表格（Sheets）
```bash
# Read spreadsheet
mcporter call --server google-workspace --tool "sheets.getText" spreadsheetId="<id>"

# Get range
mcporter call --server google-workspace --tool "sheets.getRange" spreadsheetId="<id>" range="Sheet1!A1:B10"
```

## 可用的工具（共 49 个）

**认证相关：** `auth.clear`, `auth.refreshToken`
**文档相关：** `docs.create`, `docs.find`, `docs.getText`, `docs.insertText`, `docs.appendText`, `docs.replaceText`, `docs.move`, `docs.extractIdFromUrl`
**驱动器相关：** `drive.search`, `drive.downloadFile`, `drive.findFolder`
**表格相关：** `sheets.getText`, `sheets.getRange`, `sheets.find`, `sheets.getMetadata`
**幻灯片相关：** `slides.getText`, `slides.find`, `slides.getMetadata`
**日历相关：** `calendar.list`, `calendar.listEvents`, `calendar.getEvent`, `calendar.createEvent`, `calendar.updateEvent`, `calendar.deleteEvent`, `calendar.findFreeTime`, `calendar.respondToEvent`
**Gmail 相关：** `gmail.search`, `gmail.get`, `gmail.send`, `gmail.createDraft`, `gmail.sendDraft`, `gmail.modify`, `gmail.listLabels`, `gmail.downloadAttachment`
**聊天相关：** `chat.listSpaces`, `chat.findSpaceByName`, `chat.sendMessage`, `chat.getMessages`, `chat.sendDm`, `chat.findDmByEmail`, `chat.listThreads`, `chat.setUpSpace`
**人员信息相关：** `people.getUserProfile`, `people.getMe`
**时间相关：** `time.getCurrentDate`, `time.getCurrentTime`, `time.getTimeZone`

## 故障排除

### 重新认证
```bash
mcporter call --server google-workspace --tool "auth.clear"
```
执行此命令可重新进行认证。

### 刷新令牌
```bash
mcporter call --server google-workspace --tool "auth.refreshToken"
```

### 删除凭据
```bash
rm -rf ~/.config/google-workspace-mcp
```