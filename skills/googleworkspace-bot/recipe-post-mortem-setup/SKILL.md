---
name: recipe-post-mortem-setup
version: 1.0.0
description: "创建一份 Google Docs 的事后分析报告，安排一次 Google Calendar 的审查会议，并通过 Chat 发送通知。"
metadata:
  openclaw:
    category: "recipe"
    domain: "engineering"
    requires:
      bins: ["gws"]
      skills: ["gws-docs", "gws-calendar", "gws-chat"]
---
# 设置事故后的分析流程

> **前提条件：** 需要加载以下技能才能执行此操作：`gws-docs`、`gws-calendar`、`gws-chat`

创建一个 Google Docs 文档用于事故分析，安排一次 Google Calendar 的审查会议，并通过 Chat 发送通知。

## 步骤

1. 创建事故分析文档：`gws docs +write --title '事故分析：[事件名称]' --body '## 总结\n\n## 事件时间线\n\n## 根本原因\n\n## 需要采取的行动'`
2. 安排审查会议：`gws calendar +insert --summary '事故分析会议：[事件名称]' --attendee team@company.com --start '2026-03-16T14:00:00' --end '2026-03-16T15:00:00'`
3. 通过 Chat 发送通知：`gws chat +send --space spaces/ENG_SPACE --text '🔍 [事件名称] 的事故分析会议已安排。'`