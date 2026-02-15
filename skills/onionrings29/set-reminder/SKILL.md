---
name: set-reminder
description: **使用场景：**  
当用户希望在特定时间或按照重复的日程安排收到提醒时，可以使用该功能。系统会通过 iMessage、Discord 或其他配置好的渠道发送基于 Cron 表达式的提醒信息。
---

# 设置提醒

使用 OpenClaw 的 cron 系统创建经过验证的提醒。该功能负责时间解析、通道验证，并通过配置的通道发送提醒信息。

## 使用方法

从任意工作区执行：
```bash
python3 skills/set-reminder/scripts/set_reminder.py --at <when> --message "<text>" [--channel <name>]
python3 skills/set-reminder/scripts/set_reminder.py --every <duration> --message "<text>" [--channel <name>]
python3 skills/set-reminder/scripts/set_reminder.py --cron "<expr>" --message "<text>" [--channel <name>]
```

或者使用 `{baseDir}`（技能目录）：
```bash
python3 {baseDir}/scripts/set_reminder.py --at <when> --message "<text>" [--channel <name>]
python3 {baseDir}/scripts/set_reminder.py --every <duration> --message "<text>" [--channel <name>]
python3 {baseDir}/scripts/set_reminder.py --cron "<expr>" --message "<text>" [--channel <name>]
```

## 参数

| 参数 | 描述 |
|-----------|-------------|
| `--at` | 单次执行：ISO 日期时间格式（例如 `2025-02-01T14:00:00`）或相对时间表达式（例如 `+20m`、`+1h`、`+2d`） |
| `--every` | 定时执行间隔：`30m`、`2h`、`1d` |
| `--cron` | 五字段 cron 表达式（例如 `"0 9 * * *"`） |
| `--message` | 提醒内容（必填） |
| `--channel` | 配置中的通道名称（可选，使用默认值） |

## 示例

```bash
# Remind in 20 minutes
python3 skills/set-reminder/scripts/set_reminder.py --at "+20m" --message "Take medicine"

# Daily at 9 AM via discord
python3 skills/set-reminder/scripts/set_reminder.py --cron "0 9 * * *" --message "Standup" --channel discord

# Every 2 hours
python3 skills/set-reminder/scripts/set_reminder.py --every "2h" --message "Drink water"
```

## 配置

**工作区/本地技能（推荐配置）：**
在技能目录下创建 `config.json` 文件：

```json
{
  "default": "imessage",
  "timezone": "America/Edmonton",
  "channels": {
    "imessage": "user@example.com",
    "discord": "1234567890123456789"
  }
}
```

**托管技能（旧版本配置）：**
在 `~/.openclaw/openclaw.json` 文件中的 `skills.entries.set-reminder.config.<agentId>` 部分进行配置：

```json
"set-reminder": {
  "enabled": true,
  "config": {
    "main": {
      "default": "imessage",
      "timezone": "America/Edmonton",
      "channels": { "imessage": "user@example.com" }
    }
  }
}
```

**必填字段：** `default`、`timezone`、`channels`

## 工作原理

1. 从技能目录（工作区/本地）或托管技能的位置加载配置文件。
2. 验证输入内容（时间格式、通道是否存在）。
3. 通过 `openclaw cron add` 命令创建 cron 任务。
4. 提醒信息会在指定时间通过配置的通道发送。

**配置优先级：**
1. `<skill_dir>/config.json`（工作区/本地技能配置，优先级最高）
2. `~/.openclaw/skills/set-reminder/config.json`（托管技能配置）
3. `~/.openclaw/openclaw.json` 中的 `skills.entries.set-reminder.config`（旧版本配置，作为备用选项）