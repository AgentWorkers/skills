---
name: lametric-cli
description: 通过命令行控制 LaMetric 的 TIME/SKY 智能显示屏。适用于发送通知、调节设备亮度/音量、管理定时器，或在 LaMetric 设备上显示数据等场景。相关命令包括：“LaMetric”、“smart display”、“notification to device”、“set timer”以及“send alert to clock”。
license: MIT
homepage: https://github.com/dedene/lametric-cli
metadata:
  author: dedene
  version: "1.1.0"
  openclaw:
    primaryEnv: LAMETRIC_API_KEY
    requires:
      bins:
        - lametric
    install:
      - kind: brew
        tap: dedene/tap
        formula: lametric
        bins: [lametric]
      - kind: go
        package: github.com/dedene/lametric-cli/cmd/lametric
        bins: [lametric]
---
# LaMetric CLI

这是一个用于控制LaMetric TIME/SKY设备的命令行工具（CLI）。它支持发送通知、调整设备设置、管理定时器以及流式传输内容等功能。

## 先决条件

### 安装

```bash
# Homebrew (macOS/Linux)
brew install dedene/tap/lametric

# Or Go install
go install github.com/dedene/lametric-cli/cmd/lametric@latest
```

### 设置

1. 从LaMetric移动应用中获取API密钥：设备设置 > API密钥
2. 运行设置向导：

```bash
lametric setup
```

或者手动进行配置：

```bash
# Store API key securely
lametric auth set-key --device=living-room

# Or use environment variables
export LAMETRIC_API_KEY=your-api-key
export LAMETRIC_DEVICE=192.168.1.100
```

配置文件的位置：`~/.config/lametric-cli/config.yaml`

## 核心工作流程

### 发送通知

- **简单通知：**
```bash
lametric notify "Hello World"
```

- **带有图标和声音的通知：**
```bash
lametric notify "Build passed" --icon=checkmark --sound=positive1
```

- **紧急警报（唤醒设备、播放警报声）：**
```bash
lametric notify "ALERT: Server down" --priority=critical --sound=alarm1
```

- **进度指示器：**
```bash
lametric notify "Upload progress" --goal=75/100 --icon=upload
```

- **折线图：**
```bash
lametric notify "CPU Usage" --chart=10,25,50,30,45,80,60
```

- **从标准输入（用于数据管道）：**
```bash
echo "Build complete" | lametric notify
git log -1 --format="%s" | lametric notify --icon=github
```

- **等待用户确认关闭通知：**
```bash
lametric notify "Confirm deployment?" --wait
```

### 设备控制

- **获取设备信息：**
```bash
lametric device
```

- **显示屏幕亮度：**
```bash
lametric display get
lametric display brightness 50      # Set to 50%
lametric display mode auto          # Auto brightness
```

- **调整音量：**
```bash
lametric audio get
lametric audio volume 30            # Set to 30%
```

- **蓝牙连接：**
```bash
lametric bluetooth get
lametric bluetooth on
lametric bluetooth off
```

### 内置应用程序

- **定时器：**
```bash
lametric app timer set 5m           # Set 5 minute timer
lametric app timer set 1h30m        # Set 1 hour 30 minutes
lametric app timer start
lametric app timer pause
lametric app timer reset
```

- **秒表：**
```bash
lametric app stopwatch start
lametric app stopwatch pause
lametric app stopwatch reset
```

- **收音机：**
```bash
lametric app radio play
lametric app radio stop
lametric app radio next
lametric app radio prev
```

- **应用程序导航：**
```bash
lametric app list                   # List installed apps
lametric app next                   # Switch to next app
lametric app prev                   # Switch to previous app
```

### 流式传输

- 将图片或视频流式传输到设备显示屏：
```bash
lametric stream start               # Start streaming session
lametric stream image logo.png      # Send static image
lametric stream gif animation.gif   # Send animated GIF
lametric stream stop                # End streaming
```

- 从ffmpeg程序接收数据并传输：
```bash
ffmpeg -i video.mp4 -vf "scale=37:8" -f rawvideo -pix_fmt rgb24 - | lametric stream pipe
```

### 设备发现

- 在网络中查找LaMetric设备：
```bash
lametric discover
lametric discover --timeout=10s
```

## 常见使用场景

- **构建/持续集成（Build/CI）通知：**
```bash
# Success
lametric notify "Build #123 passed" --icon=checkmark --sound=positive1

# Failure
lametric notify "Build #123 failed" --icon=error --sound=negative1 --priority=warning

# Deployment
lametric notify "Deployed to prod" --icon=rocket --sound=positive2
```

- **系统监控：**
```bash
# CPU alert
lametric notify "High CPU: 95%" --priority=warning --icon=warning

# Disk space
lametric notify "Disk: 85% full" --goal=85/100 --icon=harddrive
```

- **Pomodoro计时器：**
```bash
lametric app timer set 25m && lametric app timer start
```

- **会议提醒：**
```bash
lametric notify "Meeting in 5 min" --icon=calendar --sound=alarm3 --priority=warning
```

## 快速参考

### 常用图标

| 图标 | 描述 |
|-------|-------------|
| `checkmark` | 成功/完成 |
| `error` | 错误/失败 |
| `warning` | 警告/注意 |
| `info` | 信息提示 |
| `rocket` | 部署/启动 |
| `github` | GitHub |
| `slack` | Slack通知 |
| `mail` | 电子邮件 |
| `calendar` | 日历/会议提醒 |
| `download` | 下载 |
| `upload` | 上传 |

运行 `lametric icons` 命令可查看所有可用图标。

### 常用声音效果

| 声音效果 | 类别 |
|-------|----------|
| `positive1-5` | 成功提示音 |
| `negative1-5` | 错误提示音 |
| `alarm1-13` | 警报音 |
| `notification1-4` | 轻柔的通知音 |

运行 `lametric sounds` 命令可查看所有可用声音效果。

### 全局参数

| 参数 | 描述 |
|------|-------------|
| `-d, --device` | 设备名称或IP地址 |
| `-j, --json` | 以JSON格式输出结果 |
| `--plain` | 以TSV格式输出结果（适用于脚本编写） |
| `-v, --verbose` | 详细日志输出 |

## 故障排除

- **连接失败**：
  1. 验证设备IP地址：`lametric discover`
  2. 确认设备处于同一网络中
  3. 检查API密钥是否正确：`lametric auth get-key --device=设备名称`

### 认证错误：
```bash
# Re-set API key
lametric auth set-key --device=living-room

# Or use environment variable
export LAMETRIC_API_KEY=your-api-key
```

### 设备未找到：
```bash
# Discover devices
lametric discover --timeout=10s

# Add to config
lametric setup
```

## 安装说明
```bash
brew install dedene/tap/lametric
```