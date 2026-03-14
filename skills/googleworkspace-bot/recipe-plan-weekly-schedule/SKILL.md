---
name: recipe-plan-weekly-schedule
version: 1.0.0
description: "查看你的 Google 日历本周的安排，找出空缺的时间段，然后添加相应的事件来填补这些时间。"
metadata:
  openclaw:
    category: "recipe"
    domain: "scheduling"
    requires:
      bins: ["gws"]
      skills: ["gws-calendar"]
---
# 规划你的每周 Google 日程表

> **先决条件：** 需要安装以下技能才能执行此操作：`gws-calendar`

查看你的 Google 日程表，找出空闲时间，并添加相应的事件来填补这些空缺。

## 步骤

1. 查看本周的日程安排：`gws calendar +agenda`
2. 查询本周的空闲/忙碌时间：`gws calendar freebusy query --json '{"timeMin": "2025-01-20T00:00:00Z", "timeMax": "2025-01-25T00:00:00Z", "items": [{"id": "primary"}]}'`
3. 添加一个新事件：`gws calendar +insert --summary '深度工作时间' --start '2026-01-21T14:00:00' --end '2026-01-21T16:00:00'`
4. 查看更新后的日程安排：`gws calendar +agenda`