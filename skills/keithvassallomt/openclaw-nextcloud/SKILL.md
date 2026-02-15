---
name: openclaw-nextcloud
description: 您可以通过 CalDAV、WebDAV 和 Notes API 在 Nextcloud 实例中管理笔记、任务、日历、文件和联系人。这些功能可用于创建笔记、管理待办事项和日历事件、上传/下载文件以及管理联系人。
license: MIT
compatibility: Requires Node.js 20+. Needs network access to Nextcloud instance.
allowed-tools: Bash Read
---

# OpenClaw Nextcloud 技能

此技能提供了与 Nextcloud 实例的集成功能，支持访问笔记、任务（待办事项）、日历、文件和联系人信息。

## 配置

该技能需要以下环境变量：

- `NEXTCLOUD_URL`：您的 Nextcloud 实例的基 URL（例如：`https://cloud.example.com`）。
- `NEXTCLOUD_USER`：您的 Nextcloud 用户名。
- `NEXTCLOUD_TOKEN`：应用密码（推荐使用）或您的登录密码。

## 功能

### 1. 笔记（读/写）
- 列出、获取、创建、更新和删除笔记。
- API：`index.php/apps/notes/api/v1/notes`

### 2. 任务 / 待办事项（读/写）
- 列出、创建、更新、删除和完成任务。
- API：CalDAV（VTODO）

### 3. 日历（读/写）
- 列出、创建、更新和删除事件。
- API：CalDAV（VEVENT）

### 4. 文件（读/写）
- 列出、搜索、上传、下载和删除文件。
- API：WebDAV

### 5. 联系人（读/写）
- 列出、获取、创建、更新、删除和搜索联系人信息。
- API：CardDAV

## 使用方法

通过捆绑的脚本运行该技能。

```bash
node scripts/nextcloud.js <command> <subcommand> [options]
```

## 命令

### 笔记
- `notes list`
- `notes get --id <id>`
- `notes create --title <t> --content <c> [--category <cat>]`
- `notes edit --id <id> [--title <t>] [--content <c>] [--category <cat>]`
- `notes delete --id <id>`

### 任务
- `tasks list [--calendar <c>]`
- `tasks create --title <t> [--calendar <c>] [--due <d>] [--priority <p>] [--description <d>]`
- `tasks edit --uid <u> [--calendar <c>] [--title <t>] [--due <d>] [--priority <p>] [--description <d>]`
- `tasks delete --uid <u> [--calendar <c>]`
- `tasks complete --uid <u> [--calendar <c>]`

### 日历事件
- `calendar list [--from <iso>] [--to <iso>]`（默认为接下来的 7 天）
- `calendar create --summary <s> --start <iso> --end <iso> [--calendar <c>] [--description <d>]`
- `calendar edit --uid <u> [--calendar <c>] [--summary <s>] [--start <iso>] [--end <iso>] [--description <d>]`
- `calendar delete --uid <u> [--calendar <c>]`

### 日历（列出可用日历）
- `calendars list [--type <tasks|events>]`

### 文件
- `files list [--path <path>]`
- `files search --query <q>`
- `files get --path <path>`（下载文件内容）
- `files upload --path <path> --content <content>`
- `files delete --path <path>`

### 联系人
- `contacts list [--addressbook <ab>]`
- `contacts get --uid <u> [--addressbook <ab>]`
- `contacts search --query <q> [--addressbook <ab>]`
- `contacts create --name <n> [--addressbook <ab>] [--email <e>] [--phone <p>] [--organization <o>] [--title <t>] [--note <n>]`
- `contacts edit --uid <u> [--addressbook <ab>] [--name <n>] [--email <e>] [--phone <p>] [--organization <o>] [--title <t>] [--note <n>]`
- `contacts delete --uid <u> [--addressbook <ab>]`

### 地址簿（列出可用地址簿）
- `addressbooks list`

## 输出格式

所有输出均为 JSON 格式。

### 任务列表输出
```json
{
  "status": "success",
  "data": [
    {
      "uid": "unique-task-id",
      "calendar": "Calendar Name",
      "summary": "Task title",
      "status": "NEEDS-ACTION",
      "due": "20260201T153000Z",
      "priority": 0
    }
  ]
}
```
- `due`：CalDAV 格式的日期（YYYYMMDDTHHmmssZ）或空值
- `priority`：0-9（0 = 未定义，1 = 最高优先级，9 = 最低优先级）或空值

### 日历事件列表输出
```json
{
  "status": "success",
  "data": [
    {
      "uid": "unique-event-id",
      "calendar": "Calendar Name",
      "summary": "Event title",
      "start": "20260205T100000Z",
      "end": "20260205T110000Z"
    }
  ]
}
```

### 联系人列表输出
```json
{
  "status": "success",
  "data": [
    {
      "uid": "unique-contact-id",
      "addressBook": "Address Book Name",
      "fullName": "John Doe",
      "name": "Doe;John;;;",
      "phones": ["+1234567890"],
      "emails": ["john@example.com"],
      "organization": "ACME Inc",
      "title": "Developer",
      "note": "Met at conference"
    }
  ]
}
```
- `phones`：电话号码数组或空值
- `emails`：电子邮件地址数组或空值
- `name`：vCard 格式的结构化姓名（Last;First;Middle;Prefix;Suffix）

### 通用格式
```json
{
  "status": "success",
  "data": [ ... ]
}
```

或

```json
{
  "status": "error",
  "message": "Error description"
}
```

## 代理行为：默认日历选择

在创建任务或日历事件时，如果用户未指定日历：

1. **首次使用时（未设置默认日历）：**
   - 运行 `calendars list --type tasks`（针对任务）或 `calendars list --type events`（针对事件）
   - 从列表中询问用户选择使用哪个日历
   - 询问用户是否希望将其设置为未来操作的默认日历
   - 将用户的选择存储在内存中

2. **如果用户设置了默认日历：**
   - 记录 `default_task_calendar` 和/或 `default_event_calendar`
   - 在后续操作中自动使用该日历，无需再次询问

3. **如果用户拒绝设置默认日历：**
   - 在下次创建任务/事件时再次询问

4. **用户可以随时覆盖设置：**
   - 显式指定 `--calendar` 的优先级始终高于默认设置

## 内存键
- `default_task_calendar`：任务的默认日历名称（VTODO）
- `default_event_calendar`：事件的默认日历名称（VEVENT）

## 代理行为：默认地址簿选择

在创建联系人时，如果用户未指定地址簿：

1. **首次使用时（未设置默认地址簿）：**
   - 运行 `addressbooks list`
   - 从列表中询问用户选择使用哪个地址簿
   - 询问用户是否希望将其设置为未来操作的默认地址簿
   - 将用户的选择存储在内存中

2. **如果用户设置了默认地址簿：**
   - 记录 `default_addressbook`
   - 在后续操作中自动使用该地址簿，无需再次询问

3. **用户可以随时覆盖设置：**
   - 显式指定 `--addressbook` 的优先级始终高于默认设置

## 代理行为：信息展示

在向用户展示数据时，采用易于阅读的格式。输出可能发送到消息平台（如 Telegram、WhatsApp 等），这些平台可能不支持 Markdown 格式，因此请避免使用 Markdown 格式。

### 通用指南
- 使用表情符号使输出更易于阅读
- **禁止** 使用 Markdown 格式（如粗体、斜体、代码块、表格或带有 `-` 或 `*` 的列表）
- 使用纯文本并添加换行符来组织内容
- 将技术格式（如 CalDAV 日期）转换为人类可读的格式
- 逻辑地分组相关项目

### 表情符号参考
任务：✅（已完成），⬜（待处理），🔴（高优先级），🟡（中等优先级），🟢（低优先级）
日历：📅（事件），⏰（时间），📍（地点）
笔记：📝（笔记），📁（类别）
文件：📄（文件），📂（文件夹），💾（大小）
联系人：👤（联系人），📧（电子邮件），📱（电话），🏢（组织）
状态：✨（创建），✏️（更新），🗑️（删除），❌（错误）

### 示例展示

任务：
```
📋 Your Tasks

⬜ 🔴 Buy groceries — Due: Tomorrow 3:30 PM
⬜ 🟡 Review PR #42 — Due: Feb 5
✅ Send email to client
```

日历事件：
```
📅 Upcoming Events

🗓️ Team Standup
   ⏰ Mon, Feb 3 • 10:00 AM - 10:30 AM
   📍 Zoom

🗓️ Project Review
   ⏰ Wed, Feb 5 • 2:00 PM - 3:00 PM
```

联系人：
```
👤 John Doe
   📧 john@example.com
   📱 +1 234 567 890
   🏢 ACME Inc — Developer
```

文件：
```
📂 Documents/
   📄 report.pdf (2.3 MB)
   📄 notes.txt (4 KB)
   📂 Archive/
```

### 日期/时间格式

将 CalDAV 格式 `20260205T100000Z` 转换为可读格式，例如：Wed, Feb 5 • 10:00 AM
在适当的情况下显示相对日期，如 “Tomorrow”（明天）、”Next Monday”（下周一）、”In 3 days”（3 天后）
尽可能使用用户的本地时区