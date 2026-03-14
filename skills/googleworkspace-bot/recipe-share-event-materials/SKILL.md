---
name: recipe-share-event-materials
version: 1.0.0
description: "将 Google Drive 文件共享给 Google 日历事件中的所有参与者。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-calendar", "gws-drive"]
---
# 与会议参与者共享文件

> **前提条件：** 需要加载以下技能才能执行此操作：`gws-calendar`、`gws-drive`

将 Google Drive 文件共享给 Google 日历事件的所有参与者。

## 步骤

1. 获取事件参与者：`gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'`
2. 为每位参与者设置文件共享权限：`gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{"role": "reader", "type": "user", "emailAddress": "attendee@company.com"}'`
3. 验证文件共享设置：`gws drive permissions list --params '{"fileId": "FILE_ID"}' --format table`