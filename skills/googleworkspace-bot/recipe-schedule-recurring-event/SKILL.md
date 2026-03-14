---
name: recipe-schedule-recurring-event
version: 1.0.0
description: "创建一个包含参与者的重复性 Google 日历事件。"
metadata:
  openclaw:
    category: "recipe"
    domain: "scheduling"
    requires:
      bins: ["gws"]
      skills: ["gws-calendar"]
---
# 安排定期会议

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-calendar`

创建一个带有参与者的定期 Google 日历事件。

## 步骤

1. 创建定期事件：`gws calendar events insert --params '{"calendarId": "primary"}' --json '{"summary": "每周例会", "start": {"dateTime": "2024-03-18T09:00:00", "timeZone": "America/New_York"}, "end": {"dateTime": "2024-03-18T09:30:00", "timeZone": "America/New_York"}, "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=MO"], "attendees": [{"email": "team@company.com"}]}'`
2. 验证事件是否已创建：`gws calendar +agenda --days 14 --format table`