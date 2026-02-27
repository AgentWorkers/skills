# Cron调度器

使用Cron来管理系统中的定时任务和自动化操作。

**类别：** 自动化、生产力  
**是否需要API密钥：** 不需要  

## 功能介绍  

在您的机器上创建、管理和监控定时任务（即Cron作业）。您可以自动化执行备份、健康检查、清理脚本、API调用、通知等需要按计划运行的操作。该工具会处理Cron语法，因此您无需亲自编写相关代码。  

## 工具命令  

### 列出所有Cron作业  
```bash
echo "=== User crontab ==="
crontab -l 2>/dev/null || echo "(empty)"
echo ""
echo "=== System cron ==="
ls /etc/cron.d/ 2>/dev/null
echo ""
echo "=== Cron directories ==="
echo "Hourly:  $(ls /etc/cron.hourly/ 2>/dev/null | wc -l) jobs"
echo "Daily:   $(ls /etc/cron.daily/ 2>/dev/null | wc -l) jobs"
echo "Weekly:  $(ls /etc/cron.weekly/ 2>/dev/null | wc -l) jobs"
echo "Monthly: $(ls /etc/cron.monthly/ 2>/dev/null | wc -l) jobs"
```  

### 添加一个新的Cron作业  
```bash
# Add to user crontab
(crontab -l 2>/dev/null; echo "SCHEDULE COMMAND") | crontab -

# Common schedules:
# Every minute:        * * * * *
# Every 5 minutes:     */5 * * * *
# Every hour:          0 * * * *
# Every day at 2am:    0 2 * * *
# Every Monday 9am:    0 9 * * 1
# Every 1st of month:  0 0 1 * *
# Weekdays at 8am:     0 8 * * 1-5
```  

### 删除一个Cron作业  
```bash
# Edit crontab interactively
crontab -e

# Or remove a specific line
crontab -l | grep -v "PATTERN_TO_REMOVE" | crontab -
```  

### 查看Cron日志  
```bash
# Recent cron activity
grep CRON /var/log/syslog | tail -20

# Or on systems using journald
journalctl -u cron --since "1 hour ago" --no-pager | tail -20
```  

### 测试Cron命令  
```bash
# Run the command manually first to make sure it works
COMMAND_HERE

# Check it produces expected output
echo "Exit code: $?"
```  

### Cron语法参考  
```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * * command
```  

### 常见使用模式  
```bash
# Disk space alert daily at 8am
0 8 * * * df -h / | awk 'NR==2 && $5+0 > 80 {print "Disk alert: " $5 " used"}' | mail -s "Disk Warning" you@email.com

# Clean /tmp weekly
0 3 * * 0 find /tmp -type f -mtime +7 -delete

# Backup database nightly
0 2 * * * pg_dump mydb > /backups/db_$(date +\%Y\%m\%d).sql

# Restart a service if it crashes (every 5 min check)
*/5 * * * * systemctl is-active myservice || systemctl restart myservice

# Log system stats every 15 minutes
*/15 * * * * echo "$(date): $(uptime)" >> /var/log/system-stats.log
```  

### Cron中的环境变量  
```bash
# Cron runs with minimal environment. Set what you need:
(crontab -l 2>/dev/null; echo "PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash
0 2 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1") | crontab -
```  

### 重定向输出（非常重要！）  
```bash
# Log output
* * * * * command >> /var/log/myjob.log 2>&1

# Discard output
* * * * * command > /dev/null 2>&1

# Email output (if mail is configured)
MAILTO=you@email.com
0 8 * * * command
```  

## 使用示例  

**用户示例：** “每晚2点运行我的备份脚本”  
→ `crontab -l 2>/dev/null; echo "0 2 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1" | crontab -`  

**用户示例：** “每小时检查一次磁盘空间，如果空间使用率超过80%则发送警报”  
→ 创建检查脚本并设置相应的Cron作业。  

**用户示例：** “当前有哪些定时任务正在运行？”  
→ 列出所有的Cron作业和系统中的Cron目录。  

**用户示例：** “停止每日执行的清理任务”  
→ 找到并删除相应的Cron条目。  

## 限制事项：  

- Cron的路径环境变量非常有限，因此请使用绝对路径来执行命令。  
- 必须重定向命令的输出（例如 `>> logfile 2>&1`），否则Cron可能会占用邮件系统空间。  
- Cron使用系统的时区设置（请使用 `timedatectl` 命令查询）。  
- 最小的时间间隔为1分钟；如果需要更精确的时间控制，需要在脚本中使用循环结构。  
- 用户创建的Cron作业会在用户删除账户后自动删除。  
- 在安排任务之前，请先手动测试相关命令是否能够正常执行。