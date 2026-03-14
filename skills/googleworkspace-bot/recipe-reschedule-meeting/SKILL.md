---
name: recipe-reschedule-meeting
version: 1.0.0
description: "将 Google 日历事件的时间更改为新的时间，并自动通知所有参与者。"
metadata:
  openclaw:
    category: "recipe"
    domain: "scheduling"
    requires:
      bins: ["gws"]
      skills: ["gws-calendar"]
---
# 重新安排 Google 日历会议

> **前提条件：** 需要具备以下技能才能执行此操作：`gws-calendar`

将 Google 日历事件的时间重新安排，并自动通知所有参与者。

## 步骤

1. 查找事件：`gws calendar +agenda`
2. 获取事件详情：`gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'`
3. 更新事件时间：`gws calendar events patch --params '{"calendarId": "primary", "eventId": "EVENT_ID", "sendUpdates": "all"}' --json '{"start": {"dateTime": "2025-01-22T14:00:00", "timeZone": "America/New_York"}, "end": {"dateTime": "2025-01-22T15:00:00", "timeZone": "America/New_York"}}'`