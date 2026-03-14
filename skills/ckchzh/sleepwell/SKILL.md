---
name: SleepWell
description: "**睡眠质量追踪器，助您获得更好的休息体验：**  
您可以记录自己的就寝时间和起床时间，并为睡眠质量打分（1-5分）。该工具能够追踪您的睡眠时长模式，通过可视化图表展示每周的睡眠状况，提供长期睡眠统计数据（包括平均睡眠时长和质量），并给出基于科学依据的睡眠改善建议。它还能帮助您判断自己是否达到了推荐的7-9小时睡眠时间。"
version: "1.0.0"
author: "BytesAgain"
tags: ["sleep","health","wellness","tracker","rest","habits","quality","bedtime"]
categories: ["Health & Wellness", "Personal Management", "Productivity"]
---
# SleepWell

SleepWell 帮助您了解并改善自己的睡眠习惯。它可以记录您上床睡觉的时间、起床时间以及睡眠质量，从而让您能够观察到这些数据随时间的变化趋势。

## 为什么选择 SleepWell？

- **简单的记录方式**：只需一条命令即可记录睡眠信息。
- **睡眠质量评估**：您可以给睡眠质量评分（1-5分），同时记录睡眠时长。
- **可视化图表**：提供每周的睡眠时长条形图。
- **智能提醒**：当睡眠时间低于建议的 7-9 小时时，系统会发出提醒。
- **睡眠建议**：提供基于科学证据的改善睡眠质量的建议。
- **数据隐私**：所有数据都存储在本地，不会被上传到云端。

## 命令列表

- `log <bedtime> <wakeup> [quality 1-5]` — 记录一晚的睡眠情况（时间格式为 HH:MM）。
- `today` — 查看今天的睡眠记录。
- `week` — 查看每周的睡眠时长图表。
- `stats` — 查看长期的睡眠统计数据（平均睡眠时长、睡眠质量以及最佳/最差的睡眠夜晚）。
- `tips` — 随机获取一条基于科学证据的睡眠改善建议。
- `info` — 显示程序的版本信息。
- `help` — 显示可用的命令列表。

## 使用示例

```bash
sleepwell log 23:00 07:00 4
sleepwell log 00:30 08:15 3
sleepwell week
sleepwell stats
sleepwell tips
```

## 周睡眠时长图表示例

```
03-08 ████████  8.0h (q:4)
03-09 ███████   7.0h (q:3)
03-10 █████     5.5h (q:2)
03-11 ████████  8.5h (q:5)
  Avg: 7.3h/night, quality 3.5/5
```

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 开发 | bytesagain.com