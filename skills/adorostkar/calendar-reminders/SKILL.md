---
name: calendar-reminders
description: **日历提醒流程：**  
这是一个基于 `gcalcli`（Google 日历工具）的配置驱动型封装层，支持通过 `vdirsyncer+khal` 从 CalDAV 服务器同步日历数据（可选）。该流程还包括一个提醒规划器，能够生成用于 OpenClaw 的一次性提醒任务的 JSON 数据格式计划。
---

# gcalcli 日历封装工具 + 提醒计划器

此技能提供以下功能：
- `scripts/calendar`：`gcalcli` 的封装层
- `scripts/calendar/reminder_plan.py`：用于生成提醒计划的 JSON 文件
- `references/openclaw-calendar.example.json`：配置文件的示例格式

## 配置

将示例配置文件复制到私有目录并进行编辑：
- 默认路径：`~/.config/openclaw/calendar.json`
- 可通过环境变量覆盖：`OPENCLAW_CALENDAR_CONFIG=/path/to/calendar.json`

## 所需软件

- 必需软件：`python3`、`gcalcli`
- 可选软件（用于 CalDAV/iCloud）：`vdirsyncer`、`khal`

## 认证（Google）

`gcalcli` 需要 OAuth 认证。在无头服务器上，可能需要使用 SSH 端口转发功能。
该封装工具通过 `--noauth_local_server` 参数来显示相应的使用说明。

## 提醒计划功能

计划器会输出一个描述待安排提醒的 JSON 数据。您可以通过单独的 Cron 作业或代理程序来读取该 JSON 文件，并生成相应的 OpenClaw 提醒。

**默认设置**：
- 忽略生日提醒。
- 定时事件被视为重要事件。
- 全天事件仅在其标题包含配置关键词时才会触发提醒。

## 配置每日提醒计划器（使用 OpenClaw）

创建一个每日 Cron 作业（例如在本地时间 00:05 运行），该作业会执行以下操作：
1. 如果配置中启用了 CalDAV，运行 `vdirsyncer` 同步命令。
2. 运行 `scripts/calendar/reminder_plan.py` 以获取提醒计划。
3. 对于每个计划中的提醒，会在指定的时间（`reminderAtUtc`）生成一个一次性的 OpenClaw `systemEvent` 提醒。
4. 创建一个状态文件，以避免重复安排相同的提醒。

（本技能仅提供封装工具和计划生成功能；具体的提醒调度工作需由您通过 Cron 作业或代理程序来完成。）