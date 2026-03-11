---
name: roomba-control
version: 1.0.0
description: 通过云API管理iRobot Roomba扫地机器人。可以启动/停止/安排清洁任务，监控耗材的使用情况，并查看清洁地图和历史记录。
---
# Roomba 控制

您可以通过终端来控制您的 iRobot Roomba。

---

## 目录

- [系统要求](#requirements)
- [配置](#configuration)
- [核心命令](#core-commands)
- [清洁任务](#cleaning-jobs)
- [调度](#scheduling)
- [消耗品追踪](#consumable-tracking)
- [清洁历史记录与地图](#cleaning-history--maps)
- [多机器人支持](#multi-robot-support)
- [脚本编写与自动化](#scripting--automation)

---

## 系统要求

- 支持 Wi-Fi 连接的 iRobot Roomba（600/700/800/900/i/j/s 系列）
- iRobot 账户凭据
- Python 3.6 或更高版本
- 可访问 iRobot 云服务的网络连接

## 配置

```bash
export IROBOT_EMAIL="you@example.com"
export IROBOT_PASSWORD="your-password"
```

首次设置时会自动检测您的机器人：

```bash
$ bash scripts/roomba-ctl.sh setup

Discovering robots on your account...
Found 2 robots:
  [1] Rosie       — Roomba j7+    (Online, Docked)
  [2] Dusty       — Roomba i3     (Online, Docked)

Configuration saved to ~/.roomba-control/config.json
Default robot set to: Rosie
```

---

## 核心命令

```bash
# Robot status
bash scripts/roomba-ctl.sh status
# Output: Rosie (j7+) | Docked | Battery: 94% | Last clean: 2h ago | Bin: OK

# Detailed info
bash scripts/roomba-ctl.sh info

# Network/connectivity check
bash scripts/roomba-ctl.sh ping

# Identify robot (plays a sound)
bash scripts/roomba-ctl.sh find
```

---

## 清洁任务

### 启动与停止

```bash
# Start cleaning (full house)
bash scripts/roomba-ctl.sh clean

# Clean specific rooms (requires room-mapping capable models)
bash scripts/roomba-ctl.sh clean --rooms "Kitchen,Living Room"

# Pause current job
bash scripts/roomba-ctl.sh pause

# Resume paused job
bash scripts/roomba-ctl.sh resume

# Send back to dock
bash scripts/roomba-ctl.sh dock

# Emergency stop
bash scripts/roomba-ctl.sh stop
```

### 任务监控

```bash
# Current job progress
bash scripts/roomba-ctl.sh progress
# Output: Cleaning... 65% complete | 23 min elapsed | Kitchen ✓ | Living Room (in progress)

# Follow job in real-time (updates every 30s)
bash scripts/roomba-ctl.sh progress --follow
```

---

## 调度

```bash
# View current schedule
bash scripts/roomba-ctl.sh schedule

# Set daily schedule
bash scripts/roomba-ctl.sh schedule set --daily 09:00

# Set weekday-only schedule
bash scripts/roomba-ctl.sh schedule set --weekdays 10:00

# Custom schedule
bash scripts/roomba-ctl.sh schedule set --days mon,wed,fri --time 14:00

# Specific rooms on schedule
bash scripts/roomba-ctl.sh schedule set --daily 09:00 --rooms "Kitchen,Hallway"

# Disable schedule
bash scripts/roomba-ctl.sh schedule off

# Enable schedule
bash scripts/roomba-ctl.sh schedule on
```

---

## 消耗品追踪

实时监控需要更换的部件：

```bash
$ bash scripts/roomba-ctl.sh consumables

Consumable Status — Rosie (j7+)
────────────────────────────────────
Main Brush:     ████████░░ 78%   (~44 hours remaining)
Side Brush:     █████░░░░░ 52%   (~26 hours remaining)
Filter:         ███░░░░░░░ 31%   (~15 hours remaining)  ⚠️ Replace soon
Bin:            Full — Empty before next clean
Dust Bag:       ███████░░░ 68%   (auto-empty base)

Estimated based on 6.2 hrs/week average usage.
```

```bash
# Alert if any consumable below threshold
bash scripts/roomba-ctl.sh consumables --alert 20
# Exit code 1 if any below 20%

# Reset consumable counter after replacement
bash scripts/roomba-ctl.sh consumables reset filter
bash scripts/roomba-ctl.sh consumables reset main_brush
```

---

## 清洁历史记录与地图

查看清洁历史记录和地图信息：

```bash
# Recent cleaning sessions
bash scripts/roomba-ctl.sh history
bash scripts/roomba-ctl.sh history --limit 20

# Detailed session report
bash scripts/roomba-ctl.sh history <session_id>

# Cleaning statistics
bash scripts/roomba-ctl.sh stats
# Output: This week: 4 cleans, 3.2 hrs, 1,240 sq ft avg
#         This month: 14 cleans, 11.8 hrs, 1,180 sq ft avg
#         Lifetime: 342 cleans, 298.5 hrs

# Export history as CSV
bash scripts/roomba-ctl.sh history export cleaning_log.csv --days 90

# Coverage map (ASCII visualization)
bash scripts/roomba-ctl.sh map
```

---

## 多机器人支持

支持多台 Roomba 的同时使用：

```bash
# List all robots
bash scripts/roomba-ctl.sh robots

# Switch default robot
bash scripts/roomba-ctl.sh use "Dusty"

# Command a specific robot
bash scripts/roomba-ctl.sh --robot "Dusty" clean

# Start all robots
bash scripts/roomba-ctl.sh clean --all

# Status of all robots
bash scripts/roomba-ctl.sh status --all
```

---

## 脚本编写与自动化

**在客人到来前自动清洁（使用 cron 任务）：**
```bash
# Friday at 4 PM — clean living areas
0 16 * * 5 bash /path/to/roomba-ctl.sh clean --rooms "Living Room,Dining Room,Kitchen"
```

**清洁完成后发送通知：**
```bash
bash scripts/roomba-ctl.sh clean
while bash scripts/roomba-ctl.sh status --raw | grep -q "running"; do sleep 60; done
echo "Cleaning complete!" | mail -s "Roomba Done" you@email.com
```

**提醒购买消耗品：**
```bash
LOW=$(bash scripts/roomba-ctl.sh consumables --alert 25 --names)
if [ -n "$LOW" ]; then
  echo "Time to order: $LOW" | mail -s "Roomba Parts Needed" you@email.com
fi
```

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “机器人离线” | 检查 Wi-Fi 连接。重启机器人（按 CLEAN 键 10 秒）。确认 iRobot 应用程序正常工作。 |
| “认证失败” | 重新运行 `setup` 命令。检查凭据。如果启用了 2FA（双重身份验证），请重新输入。 |
| “找不到房间” | 房间名称必须完全匹配。使用 `bash scripts/roomba-ctl.sh rooms` 命令列出所有房间。 |
| “无法清洁——垃圾箱已满” | 清空垃圾箱或灰尘袋，然后重试。 |
| 响应缓慢 | iRobot 云服务的响应可能较慢。脚本会尝试 3 次，并在每次尝试之间增加延迟时间。 |