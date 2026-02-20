---
name: calendar-reminders
description: Calendar reminders pipeline: config-driven wrapper around gcalcli (Google Calendar) plus optional CalDAV source via vdirsyncer+khal, and a reminder planner that outputs a JSON plan for one-shot OpenClaw reminders.
---

# gcalcli 日历封装工具 + 提醒计划器

本技能提供以下功能：
- `scripts/calendar`：`gcalcli` 的封装层
- `scripts/calendar_reminder_plan.py`：用于生成提醒计划的 JSON 数据
- `references/openclaw-calendar.example.json`：示例配置文件格式

## 配置

将示例配置文件复制到私有目录并进行编辑：
- 默认路径：`~/.config/openclaw/calendar.json`
- 可通过环境变量覆盖：`OPENCLAW_CALENDAR_CONFIG=/path/to/calendar.json`

## 所需软件

- 必需软件：`python3`, `gcalcli`
- 可选软件（用于 CalDAV/iCloud）：`vdirsyncer`, `khal`

## 安全注意事项（为什么 ClawHub 会标记此技能为“高风险”）

本技能会调用外部二进制文件，并且依赖配置文件进行操作：
- 计划器通过 `subprocess.check_output([...], shell=False)` 来执行 `gcalcli` 或 `khal`（以参数列表的形式，可防止来自事件标题的 Shell 注入攻击）。
- 如果您通过 Cron 作业来运行 `vdirsyncerSyncCommand`，请确保以参数列表的形式执行（`subprocess.run(cmd_list, shell=False)`），而不是作为 Shell 命令字符串。
- 请确保将 `gcalcliPath` 和 `khalBin` 指向 **受信任的二进制文件**（建议使用绝对路径），切勿使用不受信任的路径。

## 身份验证（Google）

`gcalcli` 需要 OAuth 认证。在无头服务器上，您可能需要使用 SSH 端口转发。
该封装工具会使用 `--noauth_local_server` 选项来显示相应的使用说明。

## 提醒计划功能

计划器会输出一个 JSON 数据，其中包含需要安排的提醒信息。您可以通过单独的 Cron 作业或代理程序读取该数据，并在 OpenClaw 中创建相应的提醒。

**默认设置：**
- 忽略生日提醒。
- 定时事件被视为重要事件。
- 全天事件仅在其标题与配置的关键字匹配时才会触发提醒。

## 配置每日提醒计划器（OpenClaw）

创建一个每日 Cron 作业（例如在本地时间 00:05 执行）：
1. 如果配置中启用了 CalDAV，该作业会运行配置好的 `vdirsyncer` 同步命令。
2. 该作业会调用 `scripts/calendar_reminder_plan.py` 以获取提醒计划数据。
3. 对于每个计划中的提醒，它会在指定的时间（`reminderAtUtc`）在 OpenClaw 中创建一次性提醒。
4. 作业会生成一个状态文件，以避免重复安排相同的提醒。

**说明：**
本技能仅提供封装工具和计划生成功能，具体的提醒调度工作需由您通过 Cron 作业或代理程序来完成。