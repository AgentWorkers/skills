---
name: cron-scheduling
description: 使用 cron 和 systemd 定时器来安排和管理重复性任务。这些工具适用于设置 cron 作业、编写 systemd 定时器单元文件、处理时区相关的调度问题、监控失败的任务、实现重试机制，以及调试为什么某个定时任务没有执行的原因。
metadata: {"clawdbot":{"emoji":"⏰","requires":{"anyBins":["crontab","systemctl","at"]},"os":["linux","darwin"]}}
---

# Cron与任务调度

用于安排和管理重复性任务。内容包括Cron语法、crontab管理、systemd定时器、一次性任务调度、时区处理、任务监控以及常见的故障模式。

## 使用场景

- 定时运行脚本（如备份、生成报告、清理文件）
- 设置systemd定时器（现代版的Cron）
- 调试定时任务未执行的原因
- 处理定时任务中的时区问题
- 监控任务执行情况并发送警报
- 运行一次性延迟执行的命令

## Cron语法

### Cron的五个字段

```
┌───────── minute (0-59)
│ ┌─────── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌─── month (1-12 or JAN-DEC)
│ │ │ │ ┌─ day of week (0-7, 0 and 7 = Sunday, or SUN-SAT)
│ │ │ │ │
* * * * * command
```

### 常见的时间调度表达式

```bash
# Every minute
* * * * * /path/to/script.sh

# Every 5 minutes
*/5 * * * * /path/to/script.sh

# Every hour at :00
0 * * * * /path/to/script.sh

# Every day at 2:30 AM
30 2 * * * /path/to/script.sh

# Every Monday at 9:00 AM
0 9 * * 1 /path/to/script.sh

# Every weekday at 8:00 AM
0 8 * * 1-5 /path/to/script.sh

# First day of every month at midnight
0 0 1 * * /path/to/script.sh

# Every 15 minutes during business hours (Mon-Fri 9-17)
*/15 9-17 * * 1-5 /path/to/script.sh

# Twice a day (9 AM and 5 PM)
0 9,17 * * * /path/to/script.sh

# Every quarter (Jan, Apr, Jul, Oct) on the 1st at midnight
0 0 1 1,4,7,10 * /path/to/script.sh

# Every Sunday at 3 AM
0 3 * * 0 /path/to/script.sh
```

### 特殊字符串（简写形式）

```bash
@reboot    /path/to/script.sh   # Run once at startup
@yearly    /path/to/script.sh   # 0 0 1 1 *
@monthly   /path/to/script.sh   # 0 0 1 * *
@weekly    /path/to/script.sh   # 0 0 * * 0
@daily     /path/to/script.sh   # 0 0 * * *
@hourly    /path/to/script.sh   # 0 * * * *
```

## crontab管理

```bash
# Edit current user's crontab
crontab -e

# List current crontab
crontab -l

# Edit another user's crontab (root)
sudo crontab -u www-data -e

# Remove all cron jobs (be careful!)
crontab -r

# Install crontab from file
crontab mycrontab.txt

# Backup crontab
crontab -l > crontab-backup-$(date +%Y%m%d).txt
```

### crontab的最佳实践

```bash
# Set PATH explicitly (cron has minimal PATH)
PATH=/usr/local/bin:/usr/bin:/bin

# Set MAILTO for error notifications
MAILTO=admin@example.com

# Set shell explicitly
SHELL=/bin/bash

# Full crontab example
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=admin@example.com
SHELL=/bin/bash

# Backups
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

# Cleanup old logs
0 3 * * 0 find /var/log/myapp -name "*.log" -mtime +30 -delete

# Health check
*/5 * * * * /opt/scripts/healthcheck.sh || /opt/scripts/alert.sh "Health check failed"
```

## systemd定时器

### 创建定时器（现代版的Cron）

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
User=backup
StandardOutput=journal
StandardError=journal
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily at 2 AM

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### OnCalendar语法

```ini
# Systemd calendar expressions

# Daily at midnight
OnCalendar=daily
# or: OnCalendar=*-*-* 00:00:00

# Every Monday at 9 AM
OnCalendar=Mon *-*-* 09:00:00

# Every 15 minutes
OnCalendar=*:0/15

# Weekdays at 8 AM
OnCalendar=Mon..Fri *-*-* 08:00:00

# First of every month
OnCalendar=*-*-01 00:00:00

# Every 6 hours
OnCalendar=0/6:00:00

# Specific dates
OnCalendar=2026-02-03 12:00:00

# Test calendar expressions
systemd-analyze calendar "Mon *-*-* 09:00:00"
systemd-analyze calendar "*:0/15"
systemd-analyze calendar --iterations=5 "Mon..Fri *-*-* 08:00:00"
```

### systemd定时器相比Cron的优势

```
Systemd timers vs cron:
+ Logs in journald (journalctl -u service-name)
+ Persistent: catches up on missed runs after reboot
+ RandomizedDelaySec: prevents thundering herd
+ Dependencies: can depend on network, mounts, etc.
+ Resource limits: CPUQuota, MemoryMax, etc.
+ No lost-email problem (MAILTO often misconfigured)
- More files to create (service + timer)
- More verbose configuration
```

## 一次性任务调度

- `at`：在指定时间点运行一次任务
- `sleep`：基于延迟时间运行的简单方式

## 时区处理

```bash
# Cron runs in the system timezone by default
# Check system timezone
timedatectl
date +%Z

# Set timezone for a specific cron job
# Method 1: TZ variable in crontab
TZ=America/New_York
0 9 * * * /opt/scripts/report.sh

# Method 2: In the script itself
#!/bin/bash
export TZ=UTC
# All date operations now use UTC

# Method 3: Wrapper
TZ=Europe/London date '+%Y-%m-%d %H:%M:%S'

# List available timezones
timedatectl list-timezones
timedatectl list-timezones | grep America
```

### 处理夏令时（DST）相关问题

```
Problem: A job scheduled for 2:30 AM may run twice or not at all
during DST transitions.

"Spring forward": 2:30 AM doesn't exist (clock jumps 2:00 → 3:00)
"Fall back": 2:30 AM happens twice

Mitigation:
1. Schedule critical jobs outside 1:00-3:00 AM
2. Use UTC for the schedule: TZ=UTC in crontab
3. Make jobs idempotent (safe to run twice)
4. Systemd timers handle DST correctly
```

## 任务监控与调试

- 为什么我的Cron任务没有执行？
- 使用带有日志记录和警报功能的任务封装机制
- 采用锁定机制防止任务重复执行

## 任务的可重复性（Idempotent Jobs）

- 确保任务的可重复性：即使任务因夏令时、手动触发或系统崩溃等原因重复执行，也应产生相同的结果

## 提示

- 在Cron任务中务必重定向输出：`>> /var/log/job.log 2>&1`。否则，输出会发送到邮件（如果配置了邮件发送功能）或被忽略。
- 使用`env -i`模拟Cron的最低配置环境来测试任务，多数故障是由于缺少`PATH`或环境变量引起的。
- 使用`flock`命令防止任务在超时后仍继续执行。
- 确保所有定时任务都是可重复执行的。
- 使用`systemd-analyze calendar`工具在部署前验证定时器的正确性。
- 如果地区使用夏令时，切勿在凌晨1:00至3:00之间安排关键任务，建议使用UTC时间格式。
- 记录每个Cron任务的开始时间、结束时间和退出代码，以便事后排查故障。
- 对于生产环境的服务，优先选择systemd定时器：它提供了journald日志记录、错过任务的自动补发功能（`Persistent=true`）以及资源限制功能。