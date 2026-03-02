---
name: icloud-toolkit
description: >
  统一的 iCloud 集成功能，支持日历、电子邮件和联系人管理。适用场景包括：  
  (1) 创建、查看、搜索或删除日历事件；  
  (2) 阅读、发送或搜索电子邮件；  
  (3) 查找、创建、编辑或删除联系人；  
  (4) 任何涉及 iCloud 日历、电子邮件或联系人的操作。  
  该功能支持时区转换、符合 iCloud 格式的显示，并能自动与 vdirsyncer 进行数据同步。
metadata:
  openclaw:
    emoji: "☁️"
    install: ["brew install vdirsyncer", "brew install khal", "brew install himalaya", "brew install khard"]
    requires:
      bins: ["python3", "himalaya", "khal", "vdirsyncer", "khard"]
---
# iCloud 工具包

这是一个集日历、邮件和联系人管理功能的命令行工具（CLI）。通过一个脚本，可以完成所有与 iCloud 相关的操作。

**脚本文件：** `scripts/icloud.py` | **配置文件：** `config/config.json`

## 使用规则

- **请始终使用以下 CLI 命令**，而不是直接读取源文件、解析 .ics 或 .vcf 文件或手动查找代码。CLI 负责处理 CalDAV 发现、IMAP 操作、数据获取、同步、时区转换和格式化等工作。
- **先执行一次查询，只有在需要时才进一步扩展操作。** 首先执行 `calendar list --days N` 或 `calendar search "<关键词>"` 等命令，查看查询结果后再执行其他操作。不要同时执行多个包含不同关键词的查询。每个命令都会触发一次同步过程，因此减少调用次数可以提高响应速度。
- **对于涉及多个日历的查询**（例如：“我们俩什么时候有空？”），需要分别对每个日历执行 `calendar list` 命令，然后根据合并后的结果进行分析。
- **已订阅的日历仅支持读取操作。** 可以列出和搜索这些日历，但 `calendar create` 和 `calendar delete` 命令仅适用于用户自己拥有的日历。
- 如果用户表示要订阅新的日历，请执行 `calendar refresh` 命令。
- 如果某个日历没有返回任何事件，请告知用户，无需进行调试。空结果也是正常的，可能是因为用户没有事件，或者该日历需要更新数据（执行 `calendar refresh`）。切勿通过编写脚本来解析数据或调用 API 来绕过这一限制。
- 在代表用户发送或删除邮件之前，务必先获取用户的授权。
- **无需每次使用脚本时都重新读取本文件**。一旦在当前会话中阅读了 `SKILL.md`，就可以直接使用其中的命令了。

## 快速参考

```bash
ICLOUD=~/.openclaw/workspace/skills/icloud-toolkit/scripts/icloud.py

# Calendar
python3 $ICLOUD calendar list                                    # Today
python3 $ICLOUD calendar list --days 7                           # Next 7 days
python3 $ICLOUD calendar list --days 7 --calendar Appointments   # Specific calendar
python3 $ICLOUD calendar search "meeting"                        # Search events
python3 $ICLOUD calendar create <cal> <date> <start> <end> <title> [--location X] [--description X]
python3 $ICLOUD calendar create-allday <cal> <date> <title> [--description X]
python3 $ICLOUD calendar delete <uid>
python3 $ICLOUD calendar sync                                    # Manual sync
python3 $ICLOUD calendar disable <name>                          # Hide from listings
python3 $ICLOUD calendar enable <name>                           # Show in listings
python3 $ICLOUD calendar refresh                                 # Re-discover calendars

# Email
python3 $ICLOUD email list                                       # Latest 10
python3 $ICLOUD email list --count 20 --folder "Sent Messages"   # Sent folder
python3 $ICLOUD email list --unread                              # Unread only
python3 $ICLOUD email read <id> [--folder X]
python3 $ICLOUD email send <to> <subject> <body>
python3 $ICLOUD email reply <id> <body> [--all] [--folder X]
python3 $ICLOUD email search "from Apple" [--folder X]
python3 $ICLOUD email move <folder> <id> [--source X]            # Move (folder first, then id)
python3 $ICLOUD email delete <id> [--folder X]

# Folder
python3 $ICLOUD folder purge <folder>                            # Purge all emails from folder

# Contacts
python3 $ICLOUD contact list [--addressbook X] [--count N]
python3 $ICLOUD contact show <uid>
python3 $ICLOUD contact search "John"
python3 $ICLOUD contact create John Doe --email j@x.com --phone +15551234567
python3 $ICLOUD contact create --fn "Acme Corp" --org "Acme Corp"
python3 $ICLOUD contact edit <uid> --add-email new@x.com
python3 $ICLOUD contact edit <uid> --first Jane --last Smith
python3 $ICLOUD contact delete <uid>
python3 $ICLOUD contact sync

# Heartbeat
python3 $ICLOUD heartbeat enable                              # Add cron job
python3 $ICLOUD heartbeat disable                             # Remove cron job
python3 $ICLOUD heartbeat status                              # Show status + last run
```

## 日历

时间显示为本地时间，CLI 会自动根据配置的时区将其转换为 UTC 格式。

```bash
python3 $ICLOUD calendar create Appointments 2026-03-15 14:00 15:30 "Team Meeting" \
  --location "Board Room" --description "Weekly sync"
python3 $ICLOUD calendar create-allday General 2026-03-15 "Company Holiday"
```

日历名称在设置过程中进行配置。要查看可用的日历，可以运行 `calendar list` 命令。

### 多日历查询

对于涉及多个日历的查询（例如：“我们俩什么时候有空？”、“我有冲突吗？”）：

1. 对每个相关的日历分别执行 `calendar list --days N --calendar <日历名称>` 命令。
2. 解析输出结果以确定用户的忙碌/空闲时间。
3. 根据合并后的结果给出答案。

### 禁用/启用日历

可以随时将任何日历（无论是用户自己拥有的还是已订阅的）从显示列表中排除：

```bash
python3 $ICLOUD calendar disable "Garbage Collection"   # Exclude from list/search
python3 $ICLOUD calendar enable "Garbage Collection"    # Include again
```

### 刷新日历

执行 `calendar refresh` 命令，以便在初次设置后能够获取新订阅的日历信息。

## 邮件

iCloud 的文件夹包括：收件箱（INBOX）、已发送邮件（Sent Messages）、草稿（Drafts）、已删除邮件（Deleted Messages）、垃圾邮件（Junk）和存档（Archive）。

搜索功能支持 Himalaya 查询语法（基于位置的信息检索）：

```bash
python3 $ICLOUD email search "from Apple"
python3 $ICLOUD email search "subject invoice"
python3 $ICLOUD email search "after 2026-02-01"
python3 $ICLOUD email search "from Apple and after 2026-01-01"
```

邮件发送地址使用配置文件中的 `account_email`，该地址可能与用于身份验证的 Apple ID 不同（例如，使用自定义域的用户）。

回复邮件时，系统会自动将发件地址设置为接收原始邮件的地址。

## 联系人

```bash
# Full contact creation
python3 $ICLOUD contact create John Doe \
  --email john@work.com --email john@home.com \
  --phone +15551234567 --phone +15559876543 \
  --org "Acme Corp" --title "Engineer" \
  --nickname "Johnny" --birthday 1990-01-15 \
  --note "Met at conference" --category friend \
  --addressbook Work

# Editing preserves all existing data — only specified fields change
python3 $ICLOUD contact edit <uid> --add-email new@x.com     # Add (keeps existing)
python3 $ICLOUD contact edit <uid> --remove-email old@x.com  # Remove specific
python3 $ICLOUD contact edit <uid> --email only@x.com        # Replace all
python3 $ICLOUD contact edit <uid> --add-phone +15559999999
python3 $ICLOUD contact edit <uid> --remove-phone +15551111111
python3 $ICLOUD contact edit <uid> --org "New Corp" --title "Manager"
```

## 邮件通知（心跳机制）

`scripts/heartbeat-cron.py` 每 5 分钟检查一次是否有新的未读 iCloud 邮件，并向相关代理发送处理提示。

```bash
python3 $ICLOUD heartbeat enable              # Add cron job
python3 $ICLOUD heartbeat disable             # Remove cron job
python3 $ICLOUD heartbeat status              # Show cron + last run info
```

**手动运行方式（非定时任务）：**

```bash
python3 scripts/heartbeat-cron.py             # Normal run
python3 scripts/heartbeat-cron.py --dry-run   # Preview without agent call
```

状态信息存储在 `state/heartbeat-state.json` 文件中（仅在本技能内部使用）。日志记录保存在 `~/.openclaw/logs/heartbeat-icloud.log` 文件中。

## 其他说明

- **数据同步** 是在读取数据之前以及写入数据之前自动完成的。手动同步操作可以通过 `calendar sync` 或 `contact sync` 命令实现。
- **自我测试命令：** `python3 $ICLOUD --test`

## 首次设置

如果配置文件 `config/config.json` 不存在，该技能会提示用户“需要先进行设置”。请按照以下两步进行操作：

### 第一步：配置

请求用户提供他们的 **Apple ID**、**发送邮件地址**（除非使用自定义域，否则与 Apple ID 相同）、**显示名称** 以及 **时区**（格式为 IANA 标准，如果用户未提供时区信息，系统会自动检测）。

密码通过 `$ICLOUD_APP_PASSWORD` 变量进行管理。如果密码尚未设置：
> 访问 https://appleid.apple.com → 登录 → 安全设置 → 应用专用密码 → 为 “iCloud 工具包” 生成一个新的密码。然后使用以下命令设置密码：`/secret set ICLOUD_APP_PASSWORD`

```bash
# Most users (sending address = Apple ID):
python3 $ICLOUD setup configure --email APPLE_ID --name "USER_NAME" --timezone TIMEZONE

# Custom domain users:
python3 $ICLOUD setup configure --email SENDING_ADDRESS --apple-id APPLE_ID --name "USER_NAME" --timezone TIMEZONE
```

此步骤会保存用户的认证信息，生成 vdirsyncer 的配置文件，执行日历和通讯录的发现及同步操作，并将结果以 JSON 格式输出。

### 第二步：完成设置

系统会自动检测用户的日历列表，用户只需选择一个默认日历即可。

```bash
python3 $ICLOUD setup finalize --email SENDING_ADDRESS --apple-id APPLE_ID --name "USER_NAME" --timezone TIMEZONE \
  --default Personal \
  --addressbooks '{"Contacts":"uuid-from-discovery"}' --default-addressbook Contacts
```

如果省略了 `--calendars` 参数，该技能会自动从 iCloud 中检测所有日历，并将其分为用户自己拥有的日历和已订阅的日历。`--addressbooks` 和 `--default-addressbook` 参数是可选的。

```bash
python3 $ICLOUD setup verify    # Run smoke tests
```