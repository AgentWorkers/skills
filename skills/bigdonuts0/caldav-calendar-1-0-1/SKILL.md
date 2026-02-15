---
name: caldav-calendar
description: 使用 `vdirsyncer` 和 `khal` 同步并查询 CalDAV 日历（如 iCloud、Google、Fastmail、Nextcloud 等）。该方案适用于 Linux 系统。
metadata: {"clawdbot":{"emoji":"📅","os":["linux"],"requires":{"bins":["vdirsyncer","khal"]},"install":[{"id":"apt","kind":"apt","packages":["vdirsyncer","khal"],"bins":["vdirsyncer","khal"],"label":"Install vdirsyncer + khal via apt"}]}}
---

# CalDAV 日历管理工具（vdirsyncer + khal）

**vdirsyncer** 将 CalDAV 日历同步到本地的 `.ics` 文件中，**khal** 则负责读取和写入这些文件。

## 先进行同步

在查询日历数据或对日历内容进行修改之前，务必先完成同步操作：
```bash
vdirsyncer sync
```

## 查看事件

```bash
khal list                        # Today
khal list today 7d               # Next 7 days
khal list tomorrow               # Tomorrow
khal list 2026-01-15 2026-01-20  # Date range
khal list -a Work today          # Specific calendar
```

## 搜索事件

```bash
khal search "meeting"
khal search "dentist" --format "{start-date} {title}"
```

## 创建事件

```bash
khal new 2026-01-15 10:00 11:00 "Meeting title"
khal new 2026-01-15 "All day event"
khal new tomorrow 14:00 15:30 "Call" -a Work
khal new 2026-01-15 10:00 11:00 "With notes" :: Description goes here
```

创建事件后，需要再次同步以将更改内容上传到服务器：
```bash
vdirsyncer sync
```

## 编辑事件（交互式）

`khal edit` 命令支持交互式编辑，需要使用终端（TTY）进行操作。如果需要自动化执行编辑操作，可以使用 `tmux`：
```bash
khal edit "search term"
khal edit -a CalendarName "search term"
khal edit --show-past "old event"
```

菜单选项：
- `s` → 编辑事件摘要
- `d` → 编辑事件描述
- `t` → 修改事件的时间范围
- `l` → 修改事件地点
- `D` → 删除事件
- `n` → 跳过当前事件，继续查找下一个匹配项
- `q` → 退出编辑界面

编辑完成后，需要再次同步日历数据：
```bash
vdirsyncer sync
```

## 删除事件

使用 `khal edit` 命令进行编辑，然后按下 `D` 键即可删除事件。

## 输出格式

适用于脚本编程：
```bash
khal list --format "{start-date} {start-time}-{end-time} {title}" today 7d
khal list --format "{uid} | {title} | {calendar}" today
```

占位符说明：
- `{title}`：事件标题
- `{description}`：事件描述
- `{start}`：事件开始时间
- `{end}`：事件结束时间
- `{start-date}`：事件开始日期
- `{start-time}`：事件开始时间（格式为 YYYY-MM-DD HH:MM:SS）
- `{end-date}`：事件结束日期
- `{end-time}`：事件结束时间（格式为 YYYY-MM-DD HH:MM:SS）
- `{location}`：事件地点
- `{calendar}`：事件所属的日历服务器
- `{uid}`：事件的唯一标识符

## 缓存机制

`khal` 会将事件数据缓存到 `~/.local/share/khal/khal.db` 文件中。如果同步后数据仍然显示为“过期”状态（即数据可能已过时），可以采取相应措施：
```bash
rm ~/.local/share/khal/khal.db
```

## 初始设置

### 1. 配置 vdirsyncer（`~/.config/vdirsyncer/config`）

以 iCloud 为例：
```ini
[general]
status_path = "~/.local/share/vdirsyncer/status/"

[pair icloud_calendar]
a = "icloud_remote"
b = "icloud_local"
collections = ["from a", "from b"]
conflict_resolution = "a wins"

[storage icloud_remote]
type = "caldav"
url = "https://caldav.icloud.com/"
username = "your@icloud.com"
password.fetch = ["command", "cat", "~/.config/vdirsyncer/icloud_password"]

[storage icloud_local]
type = "filesystem"
path = "~/.local/share/vdirsyncer/calendars/"
fileext = ".ics"
```

配置参数示例：
- iCloud：`https://caldav.icloud.com/`
- Google：使用 `google_calendar` 作为日历存储类型
- Fastmail：`https://caldav.fastmail.com/dav/calendars/user/EMAIL/`
- Nextcloud：`https://YOUR.CLOUD/remote.php/dav/calendars/USERNAME/`

### 2. 配置 khal（`~/.config/khal/config`）

```ini
[calendars]
[[my_calendars]]
path = ~/.local/share/vdirsyncer/calendars/*
type = discover

[default]
default_calendar = Home
highlight_event_days = True

[locale]
timeformat = %H:%M
dateformat = %Y-%m-%d
```

### 3. 发现并同步日历数据

```bash
vdirsyncer discover   # First time only
vdirsyncer sync
```