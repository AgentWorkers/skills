---
name: caldav
description: 管理 CalDAV 日历和事件，特别支持 Radicale 服务器。适用于用户需要创建、更新、删除或查询日历事件、管理日历，或配置/管理 Radicale CalDAV 服务器的场景。
homepage: https://github.com/python-caldav/caldav
metadata:
  clawdbot:
    emoji: "📅"
    requires:
      bins: ["python3"]
      env: []
---
# CalDAV 与 Radicale 管理

与 CalDAV 服务器（日历、事件、待办事项）进行交互，并管理 Radicale 服务器的配置。

## 概述

CalDAV 是一种用于访问和管理日历信息的协议（RFC 4791）。Radicale 是一个轻量级的 CalDAV/CardDAV 服务器。该功能支持以下操作：

- 日历的创建、列出、更新、删除等 CRUD 操作
- 事件的管理（创建、更新、删除、查询）
- 待办事项/任务的管理
- Radicale 服务器的配置与管理

## 先决条件

### Python 库

安装 `caldav` 库：

```bash
pip install caldav
```

如需异步支持，请安装以下库：

```bash
pip install caldav[async]
```

### 环境变量（推荐）

将凭据安全地存储在环境变量或配置文件中：

```bash
export CALDAV_URL="http://localhost:5232"
export CALDAV_USER="your_username"
export CALDAV_PASSWORD="your_password"
```

或者使用位于 `~/.config/caldav/config.json` 的配置文件：

```json
{
  "url": "http://localhost:5232",
  "username": "your_username",
  "password": "your_password"
}
```

## 脚本

### 日历操作

```bash
# List all calendars
python3 {baseDir}/scripts/calendars.py list

# Create a new calendar
python3 {baseDir}/scripts/calendars.py create --name "Work Calendar" --id work

# Delete a calendar
python3 {baseDir}/scripts/calendars.py delete --id work

# Get calendar info
python3 {baseDir}/scripts/calendars.py info --id work
```

### 事件操作

```bash
# List events (all calendars, next 30 days)
python3 {baseDir}/scripts/events.py list

# List events from specific calendar
python3 {baseDir}/scripts/events.py list --calendar work

# List events in date range
python3 {baseDir}/scripts/events.py list --start 2024-01-01 --end 2024-01-31

# Create an event
python3 {baseDir}/scripts/events.py create \
  --calendar work \
  --summary "Team Meeting" \
  --start "2024-01-15 14:00" \
  --end "2024-01-15 15:00" \
  --description "Weekly sync"

# Create all-day event
python3 {baseDir}/scripts/events.py create \
  --calendar personal \
  --summary "Birthday" \
  --start 2024-02-14 \
  --allday

# Update an event
python3 {baseDir}/scripts/events.py update \
  --uid "event-uid-here" \
  --summary "Updated Title"

# Delete an event
python3 {baseDir}/scripts/events.py delete --uid "event-uid-here"

# Search events by text
python3 {baseDir}/scripts/events.py search --query "meeting"
```

### 待办事项操作

```bash
# List todos
python3 {baseDir}/scripts/todos.py list [--calendar name]

# Create a todo
python3 {baseDir}/scripts/todos.py create \
  --calendar work \
  --summary "Complete report" \
  --due "2024-01-20"

# Complete a todo
python3 {baseDir}/scripts/todos.py complete --uid "todo-uid-here"

# Delete a todo
python3 {baseDir}/scripts/todos.py delete --uid "todo-uid-here"
```

### Radicale 服务器管理

```bash
# Check Radicale status
python3 {baseDir}/scripts/radicale.py status

# List users (from htpasswd file)
python3 {baseDir}/scripts/radicale.py users list

# Add user
python3 {baseDir}/scripts/radicale.py users add --username newuser

# View Radicale config
python3 {baseDir}/scripts/radicale.py config show

# Validate Radicale config
python3 {baseDir}/scripts/radicale.py config validate

# Check storage integrity
python3 {baseDir}/scripts/radicale.py storage verify
```

## 直接的 HTTP/DAV 操作

对于低级操作，可以使用 `curl` 命令通过 CalDAV 协议进行操作：

```bash
# Discover principal URL
curl -u user:pass -X PROPFIND \
  -H "Depth: 0" \
  -H "Content-Type: application/xml" \
  -d '<d:propfind xmlns:d="DAV:"><d:prop><d:current-user-principal/></d:prop></d:propfind>' \
  http://localhost:5232/

# List calendars
curl -u user:pass -X PROPFIND \
  -H "Depth: 1" \
  -H "Content-Type: application/xml" \
  -d '<d:propfind xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav"><d:prop><d:displayname/><c:calendar-timezone/><d:resourcetype/></d:prop></d:propfind>' \
  http://localhost:5232/user/

# Query events by time range
curl -u user:pass -X REPORT \
  -H "Depth: 1" \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="utf-8"?>
<c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:prop><d:getetag/><c:calendar-data/></d:prop>
  <c:filter>
    <c:comp-filter name="VCALENDAR">
      <c:comp-filter name="VEVENT">
        <c:time-range start="20240101T000000Z" end="20240131T235959Z"/>
      </c:comp-filter>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>' \
  http://localhost:5232/user/calendar/

# Create calendar (MKCALENDAR)
curl -u user:pass -X MKCALENDAR \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="utf-8"?>
<d:mkcalendar xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:set><d:prop>
    <d:displayname>New Calendar</d:displayname>
  </d:prop></d:set>
</d:mkcalendar>' \
  http://localhost:5232/user/new-calendar/
```

## Radicale 配置

### 配置文件位置

Radicale 会在以下位置查找配置文件：
- `/etc/radicale/config`（系统全局配置）
- `~/.config/radicale/config`（用户配置）
- 通过 `--config` 或 `RADICALE_CONFIG` 环境变量指定自定义配置路径

### 主要配置部分

```ini
[server]
hosts = localhost:5232
max_connections = 20
max_content_length = 100000000
timeout = 30
ssl = False

[auth]
type = htpasswd
htpasswd_filename = /etc/radicale/users
htpasswd_encryption = autodetect

[storage]
filesystem_folder = /var/lib/radicale/collections

[rights]
type = owner_only
```

### 认证类型

| 认证类型 | 描述 |
|------|-------------|
| `none` | 不进行认证（仅限开发使用！） |
| `denyall` | 拒绝所有请求（自 3.5.0 版本起为默认设置） |
| `htpasswd` | 使用 Apache 的 htpasswd 文件进行认证 |
| `remote_user` | 由 WSGI 提供的用户名 |
| `http_x_remote_user` | 通过反向代理头传递的用户名 |
| `ldap` | 使用 LDAP/AD 进行认证 |
| `dovecot` | 使用 Dovecot 进行认证 |
| `imap` | 使用 IMAP 服务器进行认证 |
| `oauth2` | 使用 OAuth2 进行认证 |
| `pam` | 使用 PAM 进行认证 |

### 创建 htpasswd 用户

```bash
# Create new file with SHA-512
htpasswd -5 -c /etc/radicale/users user1

# Add another user
htpasswd -5 /etc/radicale/users user2
```

### 以服务形式运行（systemd）

```bash
# Enable and start
sudo systemctl enable radicale
sudo systemctl start radicale

# Check status
sudo systemctl status radicale

# View logs
journalctl -u radicale -f
```

## iCalendar 格式简介

事件数据使用 iCalendar（RFC 5545）格式：

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp//CalDAV Client//EN
BEGIN:VEVENT
UID:unique-id@example.com
DTSTAMP:20240115T120000Z
DTSTART:20240115T140000Z
DTEND:20240115T150000Z
SUMMARY:Team Meeting
DESCRIPTION:Weekly sync
LOCATION:Conference Room
END:VEVENT
END:VCALENDAR
```

### 常见属性

| 属性 | 描述 |
|----------|-------------|
| `UID` | 唯一标识符 |
| `DTSTART` | 开始时间 |
| `DTEND` | 结束时间 |
| `DTSTAMP` | 创建/修改时间 |
| `SUMMARY` | 事件标题 |
| `DESCRIPTION` | 事件描述 |
| `LOCATION` | 事件地点 |
| `RRULE` | 事件重复规则 |
| `EXDATE` | 排除日期 |
| `ATTENDEE` | 参与者 |
| `ORGANIZER` | 事件组织者 |
| `STATUS` | 确认/暂定/取消 |

### 日期格式

```
# DateTime with timezone
DTSTART:20240115T140000Z  ; UTC (Z suffix)
DTSTART;TZID=America/New_York:20240115T090000

# All-day event
DTSTART;VALUE=DATE:20240214

# DateTime local (floating)
DTSTART:20240115T140000
```

## 故障排除

### 连接问题

```bash
# Test basic connectivity
curl -v http://localhost:5232/

# Check with authentication
curl -v -u user:pass http://localhost:5232/

# Verify CalDAV support
curl -X OPTIONS http://localhost:5232/ -I | grep -i dav
```

### 常见错误

| 错误代码 | 原因 | 解决方案 |
|-------|-------|----------|
| 401 Unauthorized | 凭据错误 | 检查 htpasswd 文件 |
| 403 Forbidden | 权限限制 | 检查 `[rights]` 配置 |
| 404 Not Found | URL 路径错误 | 检查日历文件的路径 |
| 409 Conflict | 资源已存在 | 使用不同的 UID |
| 415 Unsupported Media Type | 内容类型错误 | 使用 `text/calendar` 作为内容类型 |

### 调试模式

以调试模式运行 Radicale 服务器：

```bash
python3 -m radicale --debug
```

## Python API 简介

```python
from caldav import DAVClient

# Connect
client = DAVClient(
    url="http://localhost:5232",
    username="user",
    password="pass"
)

# Get principal
principal = client.principal()

# List calendars
for cal in principal.calendars():
    print(f"Calendar: {cal.name} ({cal.url})")

# Create calendar
cal = principal.make_calendar(name="My Calendar", cal_id="my-cal")

# Create event
cal.save_event(
    dtstart="2024-01-15 14:00",
    dtend="2024-01-15 15:00",
    summary="Meeting"
)

# Query events by date range
events = cal.date_search(
    start="2024-01-01",
    end="2024-01-31"
)
for event in events:
    print(event.vobject_instance.vevent.summary.value)

# Get event by UID
event = cal.event_by_uid("event-uid")

# Delete event
event.delete()

# Create todo
todo = cal.save_todo(
    summary="Task",
    due="2024-01-20"
)
```

## 工作流程示例

### 创建重复事件

```bash
python3 {baseDir}/scripts/events.py create \
  --calendar work \
  --summary "Weekly Standup" \
  --start "2024-01-15 09:00" \
  --end "2024-01-15 09:30" \
  --rrule "FREQ=WEEKLY;BYDAY=MO,WE,FR"
```

### 将日历导出为 iCalendar 格式

```bash
# Via curl
curl -u user:pass http://localhost:5232/user/calendar/ > calendar.ics

# Via script
python3 {baseDir}/scripts/calendars.py export --id work --output work.ics
```

### 与 Git 同步（使用 Radicale）

配置 Radicale 以跟踪版本变更：

```ini
[storage]
hook = git add -A && (git diff --cached --quiet || git commit -m "Changes by \"%(user)s\"")
```

在存储文件夹中初始化 Git：

```bash
cd /var/lib/radicale/collections
git init
git config user.email "radicale@localhost"
```