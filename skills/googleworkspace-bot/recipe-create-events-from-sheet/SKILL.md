---
name: recipe-create-events-from-sheet
version: 1.0.0
description: "从 Google Sheets 电子表格中读取事件数据，并为每一行创建相应的 Google 日历条目。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-sheets", "gws-calendar"]
---
# 从 Google Sheets 创建 Google 日历事件

> **前提条件：** 需要安装以下技能才能执行此操作：`gws-sheets`、`gws-calendar`

从 Google Sheets 电子表格中读取事件数据，并为每一行创建相应的 Google 日历条目。

## 步骤

1. 读取事件数据：`gws sheets +read --spreadsheet-id SHEET_ID --range "Events!A2:D"`
2. 对于每一行数据，创建一个日历事件：`gws calendar +insert --summary '团队站会' --start '2025-01-20T09:00' --duration 30 --attendees alice@company.com,bob@company.com`