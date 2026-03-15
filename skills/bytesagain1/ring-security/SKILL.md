---
name: ring-security
description: "监控和管理Ring门铃及安全摄像头。可以查询设备状态、查看运动事件、调整设备模式以及导出事件记录。适用于需要Ring安全功能的场景。触发条件：Ring安全系统被触发时。"
---
# Ring 安全管理

您可以通过命令行来管理 Ring 门铃和摄像头系统。

## 概述

该工具通过连接 Ring 的云 API，让您能够实时监控家庭安全系统。您可以查看门铃和摄像头的状态、查看运动检测事件、管理安全模式，并下载历史事件数据进行分析。

> **注意：** Ring 并未提供官方的公共 API。此工具使用与 Ring 移动应用相同的接口端点。如果 Ring 更新了其 API，功能可能会发生变化。

## 开始使用

### 认证信息

Ring 使用电子邮件 + 密码进行认证，并支持双重身份验证（2FA）：

```bash
export RING_EMAIL="you@example.com"
export RING_PASSWORD="your-password"
```

首次运行时，系统会要求您输入双重身份验证的验证码。脚本会将刷新令牌缓存到本地文件 `~/.ring-security/token.json` 中。

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

首次连接后，脚本会自动检测您账户中的所有 Ring 设备：

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

对于配备了内置灯光的 Ring 设备（如 Floodlight Cam、Spotlight Cam）：

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

## 自动化建议

- **每日安全摘要邮件：**
  自动发送每日安全事件摘要邮件。

- **电池电量低警报：**
  在电池电量低于预设阈值时发送警报。

- **运动异常检测：**
  在检测到异常运动时发送警报。

## 注意事项

- Ring 的 API 是非官方的，因此 Ring 应用程序的更新可能会暂时影响该工具的功能。
- 新登录需要启用双重身份验证；缓存的令牌通常有效期为 2-4 周。
- 视频下载需要订阅 Ring Protect 服务。
- API 的使用频率限制未公开说明；脚本中已设置了适当的延迟机制。
- 快照链接会在几分钟后失效，请及时下载。

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com

## 命令

运行 `ring-security help` 可查看所有可用命令。