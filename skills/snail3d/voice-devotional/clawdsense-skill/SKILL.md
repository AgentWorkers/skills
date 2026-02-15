---
name: clawdsense
description: 实时图像分析功能由ClawdSense ESP32扩展板实现：该扩展板可监控媒体接收器，从设备中捕获照片，并通过Groq Vision技术进行即时图像分析。当ClawdSense通过`/photo`命令或按钮控制发送照片时，该功能可立即对房间环境进行分析，包括检测房间内的人员数量及环境状况。
---

# ClawdSense 技能

该技能支持通过 ClawdSense ESP32 适配器进行实时图像捕获与分析。

## 快速入门

### 启动服务

```bash
# Terminal 1: Media receiver (accepts photo uploads from ESP32)
node ~/clawd/clawdsense-skill/scripts/media-receiver.js

# Terminal 2: Analyzer (monitors inbound folder, analyzes with Groq)
node ~/clawd/clawdsense-skill/scripts/analyzer.js

# Terminal 3: Health monitor (keeps both services alive)
node ~/clawd/clawdsense-skill/scripts/health-monitor.js
```

### 使用方法

1. 通过 Telegram 向 ClawdSense 发送 `/photo` 命令。
2. 设备会捕获图像并将其发送到媒体接收器（端口 5555）。
3. 分析器会检测到新图像，并使用 Groq Vision 进行分析。
4. 分析结果会显示在控制台。

## 架构

### 三个主要组件

**媒体接收器**（端口 5555）
- 接收来自 ESP32 的 multipart/form-data 格式的数据上传。
- 将捕获的图像存储在 `~/.clawdbot/media/inbound/` 目录中。
- 提供以下接口：
  - POST `/inbound/photo` - 用于上传 JPEG 格式的图像
  - POST `/inbound/audio` - 用于上传 WAV 格式的音频
  - POST `/inbound/video` - 用于上传 AVI 格式的视频

**分析器**（实时轮询）
- 每 500 毫秒轮询一次 `inbound` 目录。
- 自动检测新上传的图像。
- 将图像数据发送到 Groq Vision API 进行分析。
- 使用 pixtral-12b 模型快速生成分析结果。

**健康监控**
- 每 30 秒检查两次两个服务的运行状态。
- 如果任一服务出现故障，会自动重启。
- 将服务状态记录到控制台。

## 性能

- **检测延迟**：约 500 毫秒（轮询间隔）
- **分析时间**：1-3 秒（Groq API 处理时间）
- **从图像捕获到结果输出的总时间**：约 2-5 秒

## 配置

### ESP32 固件配置

设备需要按照以下要求进行配置：
```
MEDIA_RECEIVER_URL = "http://localhost:5555"
or for public: "https://your-ngrok-url"
```

### Groq API 密钥

API 密钥需存储在环境变量中：
```bash
export GROQ_API_KEY="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"
```

## 故障排除

**“媒体接收器无法正常工作”**
- 检查端口 5555 是否被占用。
- 重启媒体接收器服务：`node ~/clawd/clawdsense-skill/scripts/media-receiver.js`

**“未检测到新图像”**
- 确认设备是否已向媒体接收器发送数据？查看设备日志。
- 媒体接收器是否正在运行？通过curl命令检查 `http://localhost:5555/health`。
- 检查 `inbound` 目录的访问权限。

**“Groq API 出现错误”**
- 确认 API 密钥已正确设置。
- 检查账户的配额或计费情况。

## 参考资料

- 有关 Groq Vision 的配置信息，请参阅 `references/groq-vision-api.md`。
- 有关设备配置的详细信息，请参阅 `references/esp32-setup.md`。