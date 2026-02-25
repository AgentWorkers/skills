---
name: living-room-smoke-detector
description: 这是一个用于客厅的简易烟雾/火灾检测器。它每5分钟查询一次空气质量传感器的数据，当检测到PM2.5浓度超过250或二氧化碳浓度超过2000时，会通过Mac的扬声器持续播放紧急警报，直到空气质量恢复正常。该设备可作为常规烟雾报警器的备用方案。
---
# 客厅烟雾探测器

这是一个简单且专注的烟雾与火灾检测系统，通过 Dirigera 中心监控客厅的 ALPSTUGA 空气传感器。

## 功能概述

- **每 5 分钟直接查询 Dirigera**（而非从数据库查询）
- **仅保留最新数据**：仅保存最新的检测结果，不记录历史数据
- **检测危险情况**：PM2.5 浓度 > 250 微克/立方米 或 CO2 浓度 > 2000 百万分之一
- **持续警报**：通过 Mac 的扬声器播放 “注意！检测到异常烟雾浓度”
- **循环警报**：在空气质量恢复正常之前，每 5 秒重复播放警报
- **作为备用烟雾报警器**：与您的常规烟雾报警器同时使用

## 设置步骤

### 1. 复制警报声音文件（可选）

如果您已经有了来自空气监测器的警报声音文件：

```bash
cp ~/.openclaw/workspace/skills/living-room-air-monitor/data/smoke_alert_message.mp3 \
   ~/.openclaw/workspace/skills/living-room-smoke-detector/data/alert.mp3
```

否则系统会在首次运行时自动生成警报声音文件。

### 2. 设置 Cron 任务

将以下命令添加到 crontab 中，以实现每 5 分钟检查一次：

```bash
*/5 * * * * /opt/homebrew/bin/python3 /Users/macmini/.openclaw/workspace/skills/living-room-smoke-detector/scripts/smoke_detector.py >> /tmp/smoke_detector.log 2>&1
```

## 使用方法

### 手动检查

```bash
python3 ~/.openclaw/workspace/skills/living-room-smoke-detector/scripts/smoke_detector.py
```

### 查看状态

```bash
# Latest reading
cat ~/.openclaw/workspace/skills/living-room-smoke-detector/data/detector_state.json

# Log
tail -f /tmp/smoke_detector.log
```

## 工作原理

1. **Cron 任务每 5 分钟触发一次检测**
2. **直接从 Dirigera 中心获取数据**
3. **检查阈值**：
   - PM2.5 浓度 > 250 微克/立方米（烟雾颗粒）
   - CO2 浓度 > 2000 百万分之一（燃烧产生的副产品）
4. **检测到危险情况时**：
   - 将状态设置为 “alert_active = true”
   - 进入警报循环
   - 每 5 秒播放一次警报声音
   - 在播放警报期间持续重新检测传感器数据
   - **空气质量恢复正常后退出警报循环**
5. **恢复正常后**：更新状态并退出警报循环

## 状态文件

`data/detector_state.json`：

```json
{
  "latest_reading": {
    "pm25": 3,
    "co2": 525,
    "time": "2026-02-25T20:30:00"
  },
  "alert_active": false,
  "last_check": "2026-02-25T20:30:00"
}
```

## 警报行为

检测到危险情况时：
- Mac 的扬声器会播放：“注意！检测到异常烟雾浓度”
- 等待 5 秒后再次检测传感器数据
- 重复上述过程，直到 PM2.5 浓度和 CO2 浓度均恢复正常
- 如需手动停止警报，可按下 Ctrl+C

## 相关文件

| 文件 | 用途 |
|------|---------|
| `scripts/smoke_detector.py` | 主检测脚本 |
| `data/alert.mp3` | 警报声音文件 |
| `data/detector_state.json` | 最新检测结果和状态信息 |

## 所需依赖项

- Python 3.x
- 可访问 Dirigera 中心（地址：192.168.1.100）
- 访问 Dirigera 中心所需的认证令牌（位于 `~/.openclaw/workspace/.dirigera_token`）
- macOS 系统自带的 `afplay` 命令
- `say` 和 `ffmpeg` 工具（用于生成警报声音）

## 与空气监测器的区别

| 功能 | 空气监测器 | 烟雾探测器 |
|---------|-------------|----------------|
| 数据存储 | 完整的 SQLite 数据库 | 仅保存最新检测结果 |
| 数据查询来源 | 数据库 | 直接从 Dirigera 中心查询 |
| 检测频率 | 每 2 分钟一次 | 每 5 分钟一次 |
| 使用目的 | 记录历史数据并生成图表 | 即时发出警报 |
| 警报方式 | 单次播放警报 | 持续循环警报 |
| 复杂程度 | 多功能 | 单一用途 |

建议同时使用这两种系统：空气监测器用于数据记录，烟雾探测器用于实时警报提醒，以实现全面的监测效果。