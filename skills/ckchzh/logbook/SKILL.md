---
name: LogBook
description: "这是一个用于日常记录和知识管理的个人数字日志本。您可以在此记录带有时间戳的条目，通过关键词搜索所有过去的日志，查看当天的条目或每周的总结，通过统计数据来跟踪自己的记录习惯，并将所有内容导出为 Markdown 格式。所有数据都存储在本地，确保您的想法保持私密性。"
version: "1.0.0"
author: "BytesAgain"
tags: ["journal","diary","log","daily","writing","personal","productivity","notes"]
categories: ["Personal Management", "Productivity", "Writing"]
---
# LogBook

LogBook 是一个运行在终端中的个人数字日记工具。你可以在这里记录自己的想法、灵感以及日常观察。你可以随时查看自己的记录历史，也可以追踪自己的日记写作习惯。

## 为什么使用 LogBook？

- **即时记录**：只需 2 秒即可记录下你的想法。
- **可搜索**：可以通过关键词快速查找过去的记录。
- **隐私保护**：所有数据都存储在你的本地机器上。
- **轻量级**：无需数据库或账户，仅使用文件进行存储。
- **可导出**：可以将日记内容导出为 Markdown 格式，以便备份或分享。

## 命令

- `write <text>` — 创建新的日志条目（会自动添加时间戳）。
- `today` — 查看今天的所有条目。
- `week` — 按日期分组查看过去 7 天的条目。
- `search <keyword>` — 在所有条目中全文搜索。
- `stats` — 查看日记写作统计信息（总条目数、最活跃的日子、每日平均条目数）。
- `export` — 将所有条目导出为格式化的 Markdown 文件。
- `info` — 显示软件的版本信息。
- `help` — 显示可用的命令列表。

## 使用示例

```bash
logbook write Had a great meeting about the new project
logbook write Reminder: call dentist tomorrow
logbook today
logbook search project
logbook week
logbook stats
```

## 数据存储

所有日志条目都存储在 `~/.logbook/entries.json` 文件中。请定期备份该文件，以保护你的日记内容。

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com