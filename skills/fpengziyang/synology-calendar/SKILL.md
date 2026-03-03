---
name: synology-calendar
description: 通过 API 管理 Synology 日历中的事件和待办事项。支持日历、事件、待办事项以及联系人功能。遵循官方的 Calendar API 文档（版本 5）。
---
# Synology 日历 API 技能

## 概述

使用官方的日历 API 来管理 Synology 日历。

**文档：** [Calendar_API_Guide_enu.pdf](references/Calendar_API_Guide_enu.pdf)

## 连接

### 环境变量

```bash
export SYNOLOGY_URL="http://{nas_ip}:5000"  # 内网地址
export SYNOLOGY_USER="{username}"
export SYNOLOGY_PASSWORD="your-password"
```

### 快速入门

```python
from client import SynologyCalendar

cal = SynologyCalendar()
cal.login()

# List calendars
calendars = cal.get_calendars()
for c in calendars:
    print(f"{c['cal_id']}: {c['cal_displayname']}")

cal.logout()
```

---

## API 参考

### 日历操作 (SYNO.Cal.Cal)

| 方法 | 描述 | 状态 |
|--------|-------------|--------|
| `get_calendars()` | 列出所有日历 | ✅ 可用 |
| `get_calendar(cal_id)` | 获取日历详情 | ✅ 可用 |
| `create_calendar(...)` | 创建日历 | ✅ 可用 |
| `delete_calendar(cal_id)` | 删除日历 | ✅ 可用 |

### 事件操作 (SYNO.Cal.Event)

| 方法 | 描述 | 状态 |
|--------|-------------|--------|
| `list_events(cal_id_list)` | 列出事件 | ✅ 可用 |
| `get_event(evt_id)` | 获取事件详情 | ✅ 可用 |
| `create_event(...)` | 创建事件 | ✅ 可用 |
| `delete_event(evt_id)` | 删除事件 | ✅ 可用 |

**事件创建注意事项：**

✅ 现在所有事件类型都可以通过 v1 API 正确创建。

**⚠️ 重要提示：** `_sid` 参数必须放在 URL 中，而不是 JSON 正文中。

Synology 日历 v1 API 要求在 URL 查询字符串中提供 `_sid` 参数，而不是在 JSON 正文中。

**create_event 方法的参数：**

| 参数 | 类型 | 是否必填 | 示例 |
|-----------|------|----------|---------|
| cal_id | 字符串 | ✅ | `/admin/home/` |
| summary | 字符串 | ✅ | 事件标题 |
| dtstart | 整数 | ✅ | 事件开始时间（Unix 时间戳） |
| dtend | 整数 | ✅ | 事件结束时间（Unix 时间戳） |
| is_all_day | 布尔值 | ✅ | `false` 表示非全天事件 |
| is_repeatevt | 布尔值 | ✅ | `false` 表示非重复事件 |
| color | 字符串 | ✅ | 事件颜色 |
| description | 字符串 | ✅ | 事件描述 |
| notify_setting | 数组 | ✅ | 通知设置 |
| participant | 数组 | ✅ | 参与者列表 |
| timezone | 字符串 | （非全天事件时需要） | `Asia/Shanghai` |

**示例：**
```python
# Non-all-day event (working)
cal.create_event(
    cal_id='/{username}/home/',
    summary='Meeting',
    dtstart=now,
    dtend=now + 3600,
    is_all_day=False,
    is_repeat_evt=False,
    description='Team meeting',
    color='#D9AE00',
    timezone='Asia/Shanghai'
)
```

### 待办事项操作 (SYNO.Cal.Todo)

| 方法 | 描述 | 状态 |
|--------|-------------|--------|
| `create_todo(...)` | 创建待办事项 | ✅ 可用 |
| `list_todos(...)` | 列出待办事项 | ✅ 可用 |
| `get_todo(evt_id)` | 获取待办事项详情 | ✅ 可用 |
| `delete_todo(evt_id)` | 删除待办事项 | ✅ 可用 |
| `complete_todo(evt_id)` | 标记待办事项为已完成 | ✅ 可用 |

### 联系人操作 (SYNO.Cal.Contact)

| 方法 | 描述 | 状态 |