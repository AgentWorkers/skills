---
name: ring-security
version: 1.0.0
description: 监控和管理Ring门铃及安全摄像头。查询设备状态、查看运动事件、调整设备模式，并导出事件记录。
---
# Ring 安全管理

您可以通过命令行访问 Ring 门铃和摄像头生态系统。

## 概述

该工具通过连接到 Ring 的云 API，让您能够实时监控家庭安全系统。您可以查看门铃和摄像头的状态、查看运动检测事件、管理安全模式，并下载历史事件数据进行分析。

> **注意：** Ring 并未提供官方的公共 API。此工具使用的端点与 Ring 移动应用相同。如果 Ring 更新其 API，功能可能会发生变化。

## 入门指南

### 凭据

Ring 使用电子邮件 + 密码进行身份验证，并支持双因素认证（2FA）：

```bash
export RING_EMAIL="you@example.com"
export RING_PASSWORD="your-password"
```

首次运行时，系统会要求您输入双因素认证代码。脚本会将刷新令牌缓存在 `~/.ring-security/token.json` 文件中。

### 首次连接

```bash
bash scripts/ring-security.sh auth login
# Enter 2FA code when prompted
# Token cached for future use

bash scripts/ring-security.sh auth check
# Verify token is valid
```

---

## 功能介绍

### 设备发现

首次连接后，脚本会自动识别您账户中的所有 Ring 设备：

```bash
$ bash scripts/ring-security.sh devices

Ring Devices Found:
┌──────────────────────┬─────────────────┬──────────┬─────────┐
│ Name                 │ Type            │ Battery  │ Status  │
├──────────────────────┼─────────────────┼──────────┼─────────┤
│ Front Door           │ Doorbell Pro 2  │ N/A      │ Online  │
│ Backyard             │ Spotlight Cam   │ 87%      │ Online  │
│ Garage               │ Stick Up Cam    │ 45%      │ Online  │
│ Side Gate            │ Floodlight Cam  │ N/A      │ Offline │
└──────────────────────┴─────────────────┴──────────┴─────────┘
```

### 实时状态

```bash
# All devices at a glance
bash scripts/ring-security.sh status

# Specific device details
bash scripts/ring-security.sh status "Front Door"

# Battery levels across all devices
bash scripts/ring-security.sh battery

# Wi-Fi signal strength
bash scripts/ring-security.sh signal
```

### 运动检测与事件记录

这是 Ring 监控系统的核心功能——您可以查看发生的事件及其时间。

```bash
# Recent events (last 20)
bash scripts/ring-security.sh events

# Events for a specific device
bash scripts/ring-security.sh events "Front Door" --limit 50

# Events in a time range
bash scripts/ring-security.sh events --from "2024-01-15 08:00" --to "2024-01-15 18:00"

# Motion events only
bash scripts/ring-security.sh events --type motion

# Ding (doorbell press) events only
bash scripts/ring-security.sh events --type ding

# Event details with snapshot URL
bash scripts/ring-security.sh event <event_id>
```

### 安全模式

您可以控制 Ring 报警系统的模式（需要安装 Ring Alarm 插件）：

```bash
# Current mode
bash scripts/ring-security.sh mode

# Set mode
bash scripts/ring-security.sh mode home
bash scripts/ring-security.sh mode away
bash scripts/ring-security.sh mode disarmed

# Mode history
bash scripts/ring-security.sh mode history
```

### 灯光控制

对于内置灯光功能的 Ring 设备（如 Floodlight Cam、Spotlight Cam）：

```bash
# Toggle lights
bash scripts/ring-security.sh light on "Backyard"
bash scripts/ring-security.sh light off "Backyard"

# Siren
bash scripts/ring-security.sh siren on "Backyard"
bash scripts/ring-security.sh siren off "Backyard"
```

### 事件导出与分析

```bash
# Export events as CSV
bash scripts/ring-security.sh export csv events_jan.csv --days 30

# Export as JSON
bash scripts/ring-security.sh export json events_jan.json --days 30

# Activity summary (events per device per day)
bash scripts/ring-security.sh analytics --days 7

# Peak activity hours
bash scripts/ring-security.sh analytics hourly --days 30
```

## 示例输出：数据分析结果

```
Activity Summary (Last 7 Days):
────────────────────────────────
Front Door:    ████████████████████ 47 events
Backyard:      █████████████ 31 events
Garage:        ██████ 14 events

Peak Hours:
  08:00-09:00  ████████ 18 events (morning deliveries)
  17:00-18:00  ██████████ 23 events (arrivals home)
  22:00-23:00  ████ 9 events (wildlife/wind)

Most Active Day: Tuesday (avg 15.2 events)
Quietest Day:   Sunday (avg 4.8 events)
```

## 自动化应用示例

- **每日安全摘要邮件：**
  ```bash
0 8 * * * bash /path/to/ring-security.sh analytics --days 1 | mail -s "Ring Daily Digest" you@email.com
```

- **电池电量低警报：**
  ```bash
bash scripts/ring-security.sh battery --below 20
# Outputs only devices below 20%, exit code 1 if any found
```

- **运动异常检测：**
  ```bash
# Alert if more than 20 events in the last hour
COUNT=$(bash scripts/ring-security.sh events --hours 1 --count)
if [ "$COUNT" -gt 20 ]; then
  echo "Unusual activity: $COUNT events in the last hour"
fi
```

## 注意事项

- Ring 的 API 并非官方提供的；Ring 应用的更新可能会导致功能暂时失效。
- 新登录需要启用双因素认证；缓存的令牌通常有效期为 2-4 周。
- 视频下载需要订阅 Ring Protect 服务。
- API 的使用频率限制未公开说明；脚本中设置了较为保守的延迟机制。
- 静态截图的链接会在几分钟后失效，请及时下载。