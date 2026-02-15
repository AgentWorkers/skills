---
name: email-to-calendar
version: 1.13.1
description: 从电子邮件中提取日历事件并创建日历条目。支持两种模式：  
(1) 直接监控收件箱：扫描所有电子邮件中的日历事件；  
(2) 转发的电子邮件：处理您转发到指定地址的电子邮件。  
具备以下功能：  
- 智能入职引导（帮助新用户快速熟悉系统）；  
- 事件跟踪；  
- 待处理的邀请提醒；  
- 撤销操作支持；  
- 静默活动日志记录；  
- 截止日期检测（并生成相应的提醒事件）；  
- 对需要采取行动的邮件发送通知；  
- 提供可扩展的接口，便于未来功能的扩展。
---

> **重要规则 - 在处理任何电子邮件之前请阅读本文件**

> 1. **切勿直接使用 `gog` 命令** - 必须始终使用包装脚本（如 `create_event.sh`、`email_read.sh` 等）。直接使用 `gog` 会绕过跟踪机制，导致事件重复。这一点没有商量的余地。
> 2. **忽略日历通知** - 不要处理来自 `calendar-notification@google.com` 的电子邮件（如 “已接受”、“已拒绝”、“待定” 等）。这些只是对现有邀请的回复，并非新的事件。请运行 `process_calendar_replies.sh` 来归档这些邮件。
> 3. **创建事件前务必询问用户** - 在当前对话中未获得明确用户确认之前，切勿创建日历事件。
> 4. **检查是否已处理** - 在处理任何电子邮件之前，请检查 `index.json` 文件中的 `processed_emails` 列表。
> 5. **先阅读配置文件** - 在展示事件信息之前，请加载并应用 `ignore_patterns` 和 `auto_create_patterns` 规则。
> 6. **查看 `memory.MD` 文件** - 检查用户从上一次会话中保存的偏好设置。
> 7. **包含所有配置的参与者** - 在创建/更新/删除事件时，务必使用 `--attendees` 标志包含配置中的参与者（如果支持的话，还可以使用 `--send-updates all`）。
> 8. **先查找已跟踪的事件** - 在使用日历搜索功能之前，请使用 `lookup_event.sh --email-id` 命令查找已存在的事件（这样更快、更可靠）。
> 9. **跟踪所有创建的事件** - `create_event.sh` 脚本会自动跟踪事件；更新或删除事件时请使用相应的跟踪 ID。
> 10. **显示星期几** - 在展示事件信息时，务必包含星期几，以便用户核对。

> ⛔ **禁止：严禁直接使用 `gog` 命令** ⛔

> **错误用法：** `gog calendar create ...` 或 `gog gmail ...`
> **正确用法：** `"$SCRIPTS_DIR/create_event.sh" ...` 或 `"$SCRIPTS_DIR/email_read.sh" ...`

> 直接使用 CLI 命令会绕过事件跟踪机制，导致事件重复。所有操作都必须通过 `scripts/` 目录下的包装脚本来完成。

# **将电子邮件内容导入日历的功能**

该功能负责从电子邮件中提取日历事件和待办事项，展示给用户审核，并创建/更新日历事件，同时支持重复检测和撤销操作。

**首次设置：** 请参阅 [SETUP.md](SETUP.md) 以了解配置选项和智能引导流程。

## 阅读电子邮件内容

**重要提示：** 在提取事件信息之前，必须先阅读电子邮件正文。请使用相应的包装脚本。

```bash
SCRIPTS_DIR="$HOME/.openclaw/workspace/skills/email-to-calendar/scripts"

# Get a single email by ID (PREFERRED)
"$SCRIPTS_DIR/email_read.sh" --email-id "<messageId>"

# Search with body content included
"$SCRIPTS_DIR/email_search.sh" --query "in:inbox is:unread" --max 20 --include-body
```

**关于过期的转发邮件：** 不要使用 `newer_than:1d` 这个条件，因为它检查的是电子邮件的原始日期头信息，而不是邮件接收的时间。请处理所有未读的电子邮件，并依赖 `processed_emails` 列表来判断邮件是否已被处理。

## 工作流程

### 0. 预处理检查（必选）

```bash
SCRIPTS_DIR="$HOME/.openclaw/workspace/skills/email-to-calendar/scripts"
CONFIG_FILE="$HOME/.config/email-to-calendar/config.json"
INDEX_FILE="$HOME/.openclaw/workspace/memory/email-extractions/index.json"

# Start activity logging
"$SCRIPTS_DIR/activity_log.sh" start-session

# Check email mode
EMAIL_MODE=$(jq -r '.email_mode // "forwarded"' "$CONFIG_FILE")

# Check if email was already processed
EMAIL_ID="<the email message ID>"
if jq -e ".extractions[] | select(.email_id == \"$EMAIL_ID\")" "$INDEX_FILE" > /dev/null 2>&1; then
    "$SCRIPTS_DIR/activity_log.sh" log-skip --email-id "$EMAIL_ID" --subject "Subject" --reason "Already processed"
    exit 0
fi

# Load ignore/auto-create patterns
IGNORE_PATTERNS=$(jq -r '.event_rules.ignore_patterns[]' "$CONFIG_FILE")
AUTO_CREATE_PATTERNS=$(jq -r '.event_rules.auto_create_patterns[]' "$CONFIG_FILE")
```

### 1. 找出需要处理的电子邮件

**直接模式：** 扫描所有未读的电子邮件，查找事件相关的信息（日期、时间、会议关键词）。

**转发模式：** 仅处理带有转发标记（如 “Fwd:”）的电子邮件。

### 2. 提取事件信息（由代理程序直接完成）

读取电子邮件并提取事件信息，将其结构化。每个事件应包含以下内容：
- **标题**：描述性名称（最多 80 个字符）
- **日期**：事件发生的日期
- **星期几**：用于验证
- **时间**：开始/结束时间（默认为上午 9:00 至下午 5:00）
- **是否跨多天**：事件是否持续多天
- **是否重复**：事件是否定期重复
- **可信度**：高/中/低
- **URL**：电子邮件中包含的所有 URL（必填项 - 请务必查找注册链接、信息页面、购票网站等）
- **截止日期**：回复/注册/购票的截止日期（如果有的话）
- **截止日期操作**：用户需要执行的操作（例如 “回复”、“购票”、“注册”）
- **截止日期链接**：用于执行操作的直接链接（通常与事件链接相同）

**URL 提取规则：** 请务必在事件描述的开头处包含最相关的 URL。

### 2.1 判断截止日期

扫描电子邮件中的截止日期提示，以确定用户需要执行的操作：

**常见的截止日期提示：**
- “请在 [日期] 之前回复”
- “请在 [日期] 之前注册”
- “注册截止日期为 [日期]”
- “购票截止日期为 [日期]”
- “早鸟优惠截止日期为 [日期]”
- “必须在 [日期] 之前回复”
- “请在 [日期] 之前报名”
- “截止日期：[日期]”
- “[操作] 的最后期限为 [日期]”

发现截止日期后：
1. 提取截止日期
2. 确定需要执行的操作（回复、注册、购票等）
3. 查找执行操作的链接
4. 标记该事件为需要特殊处理（详见下文）

### 3. 向用户展示信息并等待用户回复

应用事件规则后，以编号列表的形式向用户展示信息：

```
I found the following potential events:

1. ~~ELAC Meeting (Feb 2, Monday at 8:15 AM)~~ - SKIP (matches ignore pattern)
2. **Team Offsite (Feb 2-6, Sun-Thu)** - PENDING
3. **Staff Development Day (Feb 12, Wednesday)** - AUTO-CREATE

Reply with numbers to create (e.g., '2, 3'), 'all', or 'none'.
```

**等待用户的回复。**

展示信息后，记录待处理的邀请信息，以便后续提醒：

```bash
# Record pending invites using add_pending.sh
"$SCRIPTS_DIR/add_pending.sh" \
    --email-id "$EMAIL_ID" \
    --email-subject "$EMAIL_SUBJECT" \
    --events-json '[{"title":"Event Name","date":"2026-02-15","time":"14:00","status":"pending"}]'
```

### 4. 检查重复事件（必选）

**在创建任何事件之前，请务必检查：**

```bash
# Step 1: Check local tracking first (fast)
TRACKED=$("$SCRIPTS_DIR/lookup_event.sh" --email-id "$EMAIL_ID")
if [ "$(echo "$TRACKED" | jq 'length')" -gt 0 ]; then
    EXISTING_EVENT_ID=$(echo "$TRACKED" | jq -r '.[0].event_id')
fi

# Step 2: If not found, try summary match
if [ -z "$EXISTING_EVENT_ID" ]; then
    TRACKED=$("$SCRIPTS_DIR/lookup_event.sh" --summary "$EVENT_TITLE")
fi

# Step 3: Fall back to calendar search using wrapper script
if [ -z "$EXISTING_EVENT_ID" ]; then
    "$SCRIPTS_DIR/calendar_search.sh" --calendar-id "$CALENDAR_ID" --from "${EVENT_DATE}T00:00:00" --to "${EVENT_DATE}T23:59:59"
fi
```

使用大型语言模型（LLM）进行语义匹配，以检测重复事件（例如：“Team Offsite” 与 “Team Offsite 5-6pm”）。

### 5. 创建或更新日历事件

**推荐使用 `create_event.sh` 脚本** - 该脚本负责日期解析、事件跟踪和日志记录：

```bash
# Create new event
"$SCRIPTS_DIR/create_event.sh" \
    "$CALENDAR_ID" \
    "Event Title" \
    "February 11, 2026" \
    "9:00 AM" \
    "5:00 PM" \
    "Description" \
    "$ATTENDEE_EMAILS" \
    "" \
    "$EMAIL_ID"

# Update existing event (pass event_id as 8th parameter)
"$SCRIPTS_DIR/create_event.sh" \
    "$CALENDAR_ID" \
    "Updated Title" \
    "February 11, 2026" \
    "10:00 AM" \
    "6:00 PM" \
    "Updated description" \
    "$ATTENDEE_EMAILS" \
    "$EXISTING_EVENT_ID" \
    "$EMAIL_ID"
```

有关直接使用 `gog` 命令和高级选项的详细信息，请参阅 [references/gog-commands.md](references/gog-commands.md)。

### 6. 电子邮件处理（自动完成）

电子邮件的处理方式（标记为已读和/或归档）由 `create_event.sh` 根据配置设置自动完成。无需手动操作——事件创建完成后，系统会自动处理邮件。

**如需手动处理电子邮件：**
```bash
"$SCRIPTS_DIR/disposition_email.sh" --email-id "$EMAIL_ID"
```

**处理日历回复邮件（接受、拒绝、待定）：**
```bash
"$SCRIPTS_DIR/process_calendar_replies.sh"           # Process all
"$SCRIPTS_DIR/process_calendar_replies.sh" --dry-run # Preview only
```

```bash
# End activity session
"$SCRIPTS_DIR/activity_log.sh" end-session
```

## 事件创建规则

### 日期/时间处理
- **单日事件**：默认时间为上午 9:00 至下午 5:00
- **多日事件**（例如：2 月 2 日至 6 日）：使用 `--rrule "RRULE:FREQ=DAILY;COUNT=N"` 进行设置
- **具有具体时间的事件**：使用电子邮件中的确切时间

### 事件描述

事件描述的格式如下：
1. **操作提示**（如果存在截止日期）：
   ```
   *** ACTION REQUIRED: [ACTION] BY [DATE] ***
   ```

2. **事件链接**（如果找到相关链接）：
   ```
   Event Link: [URL]
   ```

3. **事件详情**：从电子邮件中提取的信息

**包含截止日期的示例：**
```
*** ACTION REQUIRED: GET TICKETS BY FEB 15 ***

Event Link: https://example.com/tickets

Spring Concert at Downtown Theater
Doors open at 7 PM
VIP meet & greet available
```

**不包含截止日期的示例：**
```
Event Link: https://example.com/event

Spring Concert at Downtown Theater
Doors open at 7 PM
```

### 重复事件检测

如果满足以下条件，则视为重复事件：
- 日期相同且标题相似（通过语义匹配判断）
- 时间重叠

请始终更新现有事件，而不是创建重复事件。

### 创建截止日期事件

当事件有截止日期（如需要回复、注册或购票）时，需要创建两个日历事件：
- **主事件**：按常规方式创建事件，并在描述中添加提示信息：
```bash
"$SCRIPTS_DIR/create_event.sh" \
    "$CALENDAR_ID" \
    "Spring Concert" \
    "March 1, 2026" \
    "7:00 PM" \
    "10:00 PM" \
    "*** ACTION REQUIRED: GET TICKETS BY FEB 15 ***

Event Link: https://example.com/tickets

Spring Concert at Downtown Theater
Doors open at 7 PM" \
    "$ATTENDEE_EMAILS" \
    "" \
    "$EMAIL_ID"
```

- **截止日期提醒事件**：在截止日期当天创建一个单独的事件：
```bash
# Use create_event.sh for deadline reminders too (ensures tracking)
"$SCRIPTS_DIR/create_event.sh" \
    "$CALENDAR_ID" \
    "DEADLINE: Get tickets for Spring Concert" \
    "2026-02-15" \
    "09:00" \
    "09:30" \
    "Action required: Get tickets

Event Link: https://example.com/tickets

Main event: Spring Concert on March 1, 2026" \
    "" \
    "" \
    "$EMAIL_ID"
```

**截止日期事件的属性：**
- **标题格式**：`DEADLINE: [操作] for [事件名称]`
- **日期**：截止日期
- **时间**：上午 9:00（持续 30 分钟）
- **提醒方式**：在截止日期前一天发送电子邮件提醒 + 提前 1 小时弹出提醒
- **描述**：需要执行的操作、相关链接以及主事件的链接

### 发送截止日期通知

在创建包含截止日期的事件时，发送通知邮件以提醒用户：

```bash
# Load config
CONFIG_FILE="$HOME/.config/email-to-calendar/config.json"
USER_EMAIL=$(jq -r '.deadline_notifications.email_recipient // .gmail_account' "$CONFIG_FILE")
NOTIFICATIONS_ENABLED=$(jq -r '.deadline_notifications.enabled // false' "$CONFIG_FILE")

# Send notification if enabled (using wrapper script)
if [ "$NOTIFICATIONS_ENABLED" = "true" ]; then
    "$SCRIPTS_DIR/email_send.sh" \
        --to "$USER_EMAIL" \
        --subject "ACTION REQUIRED: Get tickets for Spring Concert by Feb 15" \
        --body "A calendar event has been created that requires your action.

Event: Spring Concert
Date: March 1, 2026
Deadline: February 15, 2026
Action Required: Get tickets

Link: https://example.com/tickets

Calendar events created:
- Main event: Spring Concert (March 1)
- Deadline reminder: DEADLINE: Get tickets for Spring Concert (Feb 15)

---
This notification was sent by the email-to-calendar skill."
fi
```

**发送通知的条件：**
- 配置文件中的 `deadline_notifications.enabled` 必须设置为 `true`
- 仅针对需要用户操作的截止日期事件
- 包含截止日期、操作内容、链接和事件详情

## 活动日志

```bash
# Start session
"$SCRIPTS_DIR/activity_log.sh" start-session

# Log skipped emails
"$SCRIPTS_DIR/activity_log.sh" log-skip --email-id "abc" --subject "Newsletter" --reason "No events"

# Log events
"$SCRIPTS_DIR/activity_log.sh" log-event --email-id "def" --title "Meeting" --action created

# End session
"$SCRIPTS_DIR/activity_log.sh" end-session

# Show recent activity
"$SCRIPTS_DIR/activity_log.sh" show --last 3
```

## 日志记录和撤销操作

更改可以在 24 小时内撤销：

```bash
# List recent changes
"$SCRIPTS_DIR/changelog.sh" list --last 10

# List undoable changes
"$SCRIPTS_DIR/undo.sh" list

# Undo most recent change
"$SCRIPTS_DIR/undo.sh" last

# Undo specific change
"$SCRIPTS_DIR/undo.sh" --change-id "chg_20260202_143000_001"
```

## 待处理的邀请

未立即处理的邀请会被记录下来，以便后续提醒：

```bash
# Add pending invites (after presenting events to user)
"$SCRIPTS_DIR/add_pending.sh" \
    --email-id "$EMAIL_ID" \
    --email-subject "Party Invite" \
    --events-json '[{"title":"Birthday Party","date":"2026-02-15","time":"14:00","status":"pending"}]'

# List pending invites (JSON)
"$SCRIPTS_DIR/list_pending.sh"

# Human-readable summary
"$SCRIPTS_DIR/list_pending.sh" --summary

# Update reminder tracking
"$SCRIPTS_DIR/list_pending.sh" --summary --update-reminded

# Auto-dismiss after 3 ignored reminders
"$SCRIPTS_DIR/list_pending.sh" --summary --auto-dismiss
```

## 事件跟踪

```bash
# Look up by email ID
"$SCRIPTS_DIR/lookup_event.sh" --email-id "19c1c86dcc389443"

# Look up by summary
"$SCRIPTS_DIR/lookup_event.sh" --summary "Staff Development"

# List all tracked events
"$SCRIPTS_DIR/lookup_event.sh" --list

# Validate events exist (removes orphans)
"$SCRIPTS_DIR/lookup_event.sh" --email-id "abc" --validate
```

## 文件位置

| 文件 | 用途 |
|------|---------|
| `~/.config/email-to-calendar/config.json` | 用户配置文件 |
| `~/.openclaw/workspace/memory/email-extractions/` | 提取的数据 |
| `~/.openclaw/workspace/memory/email-extractions/index.json` | 处理索引文件 |
| `~/.openclaw/workspace/memory/email-to-calendar/events.json` | 事件跟踪记录 |
| `~/.openclaw/workspace/memory/email-to-calendar/pending_invites.json` | 待处理的邀请信息 |
| `~/.openclaw/workspace/memory/email-to-calendar/activity.json` | 活动日志 |
| `~/.openclaw/workspace/memory/email-to-calendar/changelog.json` | 变更记录 |
| `~/.openclaw/workspace/skills/email-to-calendar/scripts/` | 功能脚本 |
| `~/.openclaw/workspace/skills/email-to-calendar/MEMORY.md` | 用户偏好设置 |

## 参考资料

- **设置指南**：[SETUP.md] - 配置和入门指南
- **CLI 参考**：[references/gog-commands.md] - 详细的 `gog` CLI 使用说明
- **提取模式**：[references/extraction-patterns.md] - 日期/时间解析规则
- **工作流程示例**：[references/workflow-example.md] - 完整的工作流程示例

## 注意事项

### 日期解析
支持以下常见格式：
- 2026 年 1 月 15 日，星期三
- 01/15/2026
- 日期范围示例：2 月 2 日至 6 日

### 时区
所有时间均以本地时区为准。描述中会保留时区信息。