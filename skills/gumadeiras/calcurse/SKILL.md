---
name: calcurse
description: 一个基于文本的日历和日程安排应用程序，仅用于通过命令行（CLI）进行日历管理。
metadata: {"clawdbot":{"emoji":"📅","requires":{"bins":["calcurse"]}}}
---

# calcurse

这是一个基于文本的日历和日程管理应用程序。

## 使用方法（命令行模式）

在非交互模式下使用 `calcurse` 可以快速查询和更新日程信息。

### 查询
- 列出接下来2天的日程安排：
  ```bash
calcurse -r2
```

- 查询特定日期范围内的日程：
  ```bash
calcurse -Q --from 2026-01-20 --to 2026-01-22
```

### 添加日程
- 添加一个日程安排：
  ```bash
calcurse -a "Meeting with Team" 2026-01-21 14:00 60
```
  格式：描述、日期、时间、持续时间（以分钟为单位）

- 添加一个待办事项：
  ```bash
calcurse -t "Buy milk" 1
```
  格式：描述、优先级

## 交互式模式（图形用户界面）
要体验完整的图形用户界面，请在终端会话中运行 `calcurse`（例如，在 `tmux` 中运行，或使用 `process` 命令并设置 `pty=true`）：
  ```bash
calcurse
```