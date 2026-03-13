---
name: recipe-compare-sheet-tabs
version: 1.0.0
description: "从 Google Sheets 的两个标签页中读取数据，以便进行比较并找出差异。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-sheets"]
---
# 比较两个 Google Sheets 的工作表

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-sheets`

从两个 Google Sheets 的工作表中读取数据，以进行比较并找出差异。

## 步骤

1. 读取第一个工作表的数据：`gws sheets +read --spreadsheet-id SHEET_ID --range "January!A1:D"`
2. 读取第二个工作表的数据：`gws sheets +read --spreadsheet-id SHEET_ID --range "February!A1:D"`
3. 比较数据并识别变化