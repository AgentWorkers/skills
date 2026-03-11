---
name: crontab-wizard
description: >
  **解释、生成、验证和预览 Cron 表达式**  
  当用户需要了解 Cron 表达式的含义、创建新的 Cron 计划、检查 Cron 表达式的有效性，或查看 Cron 作业的下一次运行时间时，可以使用该功能。支持标准的 5 字段 Cron 语法以及诸如 `@daily`、`@hourly`、`@weekly` 等快捷方式。无需任何外部依赖。
---
# CronTab Wizard

一个用于从命令行解码、生成、验证和预览Cron任务的工具。完全无需依赖任何第三方库。

## 快速入门

```bash
# Explain what a cron expression does
python3 scripts/cronwiz.py explain "*/5 * * * *"

# Generate an expression from options
python3 scripts/cronwiz.py generate --every 5m

# Check if an expression is valid
python3 scripts/cronwiz.py validate "0 9 * * 1-5"

# See when it runs next
python3 scripts/cronwiz.py next "0 9 * * 1-5" --count 10
```

## 命令

### explain — 将Cron表达式解析为人类可读的文本

```bash
python3 scripts/cronwiz.py explain "30 2 * * 0"
# → At 02:30, on Sunday

python3 scripts/cronwiz.py explain "@daily"
# → At 00:00

python3 scripts/cronwiz.py explain "0 */6 * * *"
# → At minute 0, every 6 hours
```

### validate — 检查Cron表达式是否存在语法错误

```bash
python3 scripts/cronwiz.py validate "0 9 * * 1-5"
# → VALID: 0 9 * * 1-5

python3 scripts/cronwiz.py validate "0 25 * * *"
# → INVALID: hour: 25 out of range (0-23)
```

### next — 预览即将执行的Cron任务

```bash
python3 scripts/cronwiz.py next "0 9 * * 1-5" --count 5
# Shows next 5 weekday 9 AM runs with dates
```

### generate — 根据用户输入的参数生成Cron表达式

```bash
python3 scripts/cronwiz.py generate --every 5m
# → */5 * * * *

python3 scripts/cronwiz.py generate --every daily --at 09:00
# → 0 9 * * *

python3 scripts/cronwiz.py generate --every week --at 14:30 --on friday
# → 30 14 * * 5
```

#### 可用的参数

| 参数 | 可能的值 | 说明 |
|------|--------|-------------|
| `--every` | `5m`, `2h`, `daily`, `weekly`, `monthly` | 任务执行的间隔时间（单位：分钟/小时/天/月） |
| `--at` | `HH:MM` | 任务执行的具体时间（格式：小时:分钟） |
| `--on` | `mon`–`sun`, `weekdays`, `weekends` | 任务执行的具体星期几 |

## 支持的快捷方式

`@yearly`, `@annually`, `@monthly`, `@weekly`, `@daily`, `@midnight`, `@hourly`

## 依赖关系

本工具完全基于Python编写，无需安装任何额外的依赖库（如pip）。