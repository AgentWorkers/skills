---
name: recipe-review-overdue-tasks
version: 1.0.0
description: "查找已过期且需要处理的 Google 任务。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-tasks"]
---
# 查看逾期任务

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-tasks`

查找已过期且需要处理的 Google 任务。

## 步骤

1. 列出任务列表：`gws tasks tasklists list --format table`
2. 列出任务状态：`gws tasks tasks list --params '{"tasklist": "TASKLIST_ID", "showCompleted": false}' --format table`
3. 查看截止日期并对逾期任务进行优先级排序