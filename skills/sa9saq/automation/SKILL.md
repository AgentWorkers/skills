---
name: automation
description: 任务自动化专家：负责工作流程优化及定时任务的设置与管理。
---

# 任务自动化

使用 OpenClaw 的 cron、shell 脚本和系统工具来自动化重复性任务并优化工作流程。

## 指导步骤

1. **确定任务**：了解用户希望自动化的具体需求，包括执行频率、触发条件以及输入/输出内容。
2. **选择合适的工具**：

   | 任务类型 | 工具 | 示例 |
   |-----------|------|---------|
   | 定期检查 | OpenClaw cron | 每 30 分钟发送一次电子邮件检查 |
   | 文件处理 | Shell + cron | 每晚压缩日志文件 |
   | API 轮询 | curl + jq + cron | 价格警报 |
   | 网页抓取 | Puppeteer / fetch | 监控竞争对手网站 |
   | 数据处理流程 | Shell 流程 | 将 CSV 文件转换为 JSON 格式并发送到 API |
   | 基于事件的触发 | Webhooks / inotifywait | 文件更改时自动执行任务 |

3. **使用 OpenClaw cron 实现自动化**（适用于基于代理的任务）：
   ```bash
   # Example: System event every 30 minutes
   openclaw cron add --name "task-name" \
     --schedule "*/30 * * * *" \
     --payload '{"kind":"systemEvent","text":"Check X notifications"}'
   ```

4. **使用系统 cron 实现自动化**（适用于 shell 脚本）：
   ```bash
   # Edit crontab
   crontab -e
   # Add entry: every day at 2 AM
   0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1
   ```

5. **使用 systemd 定时器实现自动化**（适用于服务）：
   ```ini
   # /etc/systemd/system/task.timer
   [Timer]
   OnCalendar=*-*-* 02:00:00
   Persistent=true
   [Install]
   WantedBy=timers.target
   ```

## 自动化模式

### 带有重试机制的自动化
```bash
#!/bin/bash
MAX_RETRIES=3
DELAY=5
for i in $(seq 1 $MAX_RETRIES); do
  if your_command; then break; fi
  echo "Retry $i/$MAX_RETRIES in ${DELAY}s..."
  sleep $DELAY
  DELAY=$((DELAY * 2))
done
```

### 文件监控
```bash
inotifywait -m -e modify,create /path/to/watch | while read dir action file; do
  echo "File $file was $action"
  # trigger processing
done
```

### 针对幂等操作的脚本
```bash
# Use lock files to prevent concurrent runs
LOCKFILE="/tmp/mytask.lock"
if [ -f "$LOCKFILE" ]; then echo "Already running"; exit 0; fi
trap "rm -f $LOCKFILE" EXIT
touch "$LOCKFILE"
# ... your task here
```

### 带有错误处理的处理流程
```bash
set -euo pipefail
fetch_data | transform_json | upload_result \
  || { echo "Pipeline failed at stage $?"; notify_admin; exit 1; }
```

## Cron 表达式参考

| 表达式 | 含义 |
|-----------|---------|
| `*/5 * * * *` | 每 5 分钟执行一次 |
| `0 */2 * * *` | 每 2 小时执行一次 |
| `0 9 * * 1-5` | 工作日早上 9 点执行 |
| `0 2 * * *` | 每天凌晨 2 点执行 |
| `0 0 * * 0` | 每周日午夜执行 |
| `0 0 1 * *` | 每月 1 日执行 |

## 安全注意事项

- **切勿在 crontab 中存储敏感信息**——应使用环境变量或秘密文件来存储这些信息。
- **记录所有自动化操作**——将日志文件保存到 `~/.automation/logs/` 目录中。
- **限制 API 调用的频率**——遵守相关服务的使用条款。
- **使用锁文件**——防止任务被重复执行。
- **验证输入数据**——切勿将未经处理的数据传递给 shell 命令。

## 所需软件

- `cron` 或 `systemd`（Linux 系统已预装）。
- OpenClaw（用于基于代理的自动化任务）。
- 可选软件：`inotifywait`（来自 inotify-tools 包）、`jq`、`curl`。