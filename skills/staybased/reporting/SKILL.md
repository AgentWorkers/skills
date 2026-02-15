---
name: reporting
description: |
  Standardized templates for periodic reports, system audits, revenue tracking, and progress logs.
  All output goes to workspace/artifacts/ directory.

  Use when: generating periodic reports, system audits, performance reviews, revenue tracking,
  weekly retrospectives, daily progress logs, full workspace audits.

  Don't use when: ad-hoc status updates in chat, quick summaries in Discord,
  one-off answers to "how's it going?", real-time dashboards.

  Negative examples:
  - "Give me a quick update" → No. Just answer in chat.
  - "What's the weather?" → No. This is for structured reports.
  - "Post a status to Discord" → No. Just send a message.

  Edge cases:
  - Mid-week report requested → Use weekly template but note partial week.
  - Audit requested for single subsystem → Use full audit template, mark other sections N/A.
  - Revenue snapshot with $0 revenue → Still generate it. Zeros are data.
version: "1.0"
---

# 报告——标准化报告模板

所有报告均输出到 `workspace/artifacts/` 目录，文件命名规则为：`{type}-{YYYY-MM-DD}.md`

---

## 报告类型

### 1. 周度回顾报告

**文件路径：** `artifacts/weekly-retro-YYYY-MM-DD.md`
**提交时间：** 每周日晚上
**模板文件：** `templates/weekly-retro.md`

报告内容涵盖：收入情况、代理运行状况、已完成的工作、停滞的项目、服务可用时间以及下周的优先事项。

### 2. 全系统审计报告

**文件路径：** `artifacts/full-audit-YYYY-MM-DD.md`
**提交频率：** 每月一次或按需提交
**模板文件：** `templates/full-audit.md`

报告内容涵盖：执行摘要、收入流程、工作流程中的问题、代理使用效率、基础设施性能、工具库存、定时任务执行情况、战略评估、内容更新状态以及改进建议。

### 3. 日志报告

**文件路径：** `artifacts/daily-log-YYYY-MM-DD.md`
**提交时间：** 每天结束时
**模板文件：** `templates/daily-log.md`

报告内容涵盖：当天完成的任务、做出的决策、遇到的阻碍以及第二天的工作重点。

### 4. 收入快照报告

**文件路径：** `artifacts/revenue-YYYY-MM-DD.md`
**提交频率：** 每周一次或按需提交
**模板文件：** `templates/revenue-snapshot.md`

报告内容涵盖：各收入来源的收入情况、支出明细、净利润（P&L）、目标完成进度以及交易表现。

---

## 模板说明

请查看 `templates/` 目录中的各个模板文件。所有模板均使用 `{{PLACEHOLDER}}` 语法来实现变量替换。

---

## 输出标准

- 所有报告文件需保存在 `workspace/artifacts/` 目录中。
- 文件名应使用 ISO 格式的日期格式。
- 每份报告的末尾需包含生成时间和作者信息。
- 对于超过一页的报告，需在顶部添加“执行摘要”部分。
- 在可能的情况下，需提供原始数据的链接。