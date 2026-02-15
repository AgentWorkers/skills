---
name: appletv
version: 1.0.0
description: 通过 pyatv 控制 Apple TV。可以用于播放/暂停、导航、调节音量、启动应用程序、控制电源状态以及查看当前正在播放的内容。该命令会在以下关键词被触发时执行相应操作：Apple TV、TV、正在播放的内容、暂停电视、播放电视、关闭电视。
license: MIT
---

# Apple TV 控制

通过 `pyatv` 库来控制 Apple TV。

## 前提条件

```bash
pipx install pyatv --python python3.11
```

> **注意：** `pyatv` 需要 Python 3.13 或更低版本。Python 3.14 及更高版本引入了可能导致程序异常的 `asyncio` 更改。请使用 `--python python3.11` 或 `python3.13` 与 `pipx` 进行安装。

## 配置

配置文件位于 `~/clawd/config/appletv.json`：

```json
{
  "name": "Living Room",
  "id": "DEVICE_ID",
  "ip": "192.168.x.x",
  "credentials": {
    "companion": "...",
    "airplay": "..."
  }
}
```

### 首次配对

```bash
# Find your Apple TV
atvremote scan

# Pair Companion protocol (required)
atvremote --id <DEVICE_ID> --protocol companion pair

# Pair AirPlay protocol (for media)
atvremote --id <DEVICE_ID> --protocol airplay pair
```

将凭据保存到配置文件中。

## 快速命令

### 查看状态与播放内容
```bash
scripts/appletv.py status     # Full status with now playing
scripts/appletv.py playing    # What's currently playing
```

### 播放控制
```bash
scripts/appletv.py play       # Play/resume
scripts/appletv.py pause      # Pause
scripts/appletv.py stop       # Stop
scripts/appletv.py next       # Next track/chapter
scripts/appletv.py prev       # Previous
```

### 导航
```bash
scripts/appletv.py up         # Navigate up
scripts/appletv.py down       # Navigate down
scripts/appletv.py left       # Navigate left
scripts/appletv.py right      # Navigate right
scripts/appletv.py select     # Press select/OK
scripts/appletv.py menu       # Menu button
scripts/appletv.py home       # Home screen
```

### 音量调节
```bash
scripts/appletv.py volume_up
scripts/appletv.py volume_down
```

### 电源控制
```bash
scripts/appletv.py turn_on    # Wake from sleep
scripts/appletv.py turn_off   # Put to sleep
scripts/appletv.py power      # Toggle
```

### 应用程序管理
```bash
scripts/appletv.py apps       # List installed apps
scripts/appletv.py app Netflix
scripts/appletv.py app YouTube
scripts/appletv.py app "Disney+"
```

### 应用程序发现
```bash
scripts/appletv.py scan       # Find Apple TVs on network
```

## 示例交互

- “电视上正在播放什么？” → `scripts/appletv.py status`
- “暂停电视” → `scripts/appletv.py pause`
- “关闭 Apple TV” → `scripts/appletv.py turn_off`
- “在电视上打开 Netflix” → `scripts/appletv.py app Netflix`