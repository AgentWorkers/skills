---
name: recipe-create-task-list
version: 1.0.0
description: "创建一个新的 Google 任务列表，并添加初始任务。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-tasks"]
---
# 创建任务列表并添加任务

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-tasks`

设置一个新的 Google 任务列表，并添加初始任务。

## 步骤

1. 创建任务列表：`gws tasks tasklists insert --json '{"title": "Q2 Goals"}'`
2. 添加一个任务：`gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{"title": "Review Q1 metrics", "notes": "Pull data from analytics dashboard", "due": "2024-04-01T00:00:00Z"}'`
3. 添加另一个任务：`gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{"title": "Draft Q2 OKRs"}'`
4. 列出任务：`gws tasks tasks list --params '{"tasklist": "TASKLIST_ID"}' --format table`