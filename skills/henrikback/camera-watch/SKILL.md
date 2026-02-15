---
name: camera-watch
description: 基于YOLOv8的摄像头监控系统，具备物体检测功能。该系统兼容所有支持RTSP流或HTTP快照的IP摄像头（包括Hikvision、Dahua、Reolink、Amcrest、Unifi等品牌）。能够识别80多种物体类型（如人、汽车、狗等），并在检测到目标物体时发送包含快照的通知。适用于运动检测、夜间监控或安全监控场景。
---

# 监控摄像头

使用 YOLOv8 对 IP 摄像头进行实时物体检测。适用于支持 RTSP 或 HTTP 快照的任何摄像头。能够检测到人、车辆、动物以及 80 多种其他物体类型。检测到物体时，会发送包含快照的通知。

## 特点

- 支持 HTTP 快照模式（更可靠）或 RTSP 流媒体传输
- 使用 YOLOv8 进行物体检测（支持 80 个 COCO 类别）
- 通过 WhatsApp/iMessage 发送包含快照的通知
- 可配置检测置信度和检测间隔时间
- 支持多摄像头同时使用

## 设置

### 1. 创建项目目录

```bash
mkdir -p ~/camera-watch && cd ~/camera-watch
python -m venv venv
source venv/bin/activate
pip install opencv-python ultralytics pyyaml requests
```

### 2. 复制脚本

将 `scripts/camera_watch.py` 复制到项目目录中。

### 3. 创建 config.yaml 文件

```yaml
notifications:
  enabled: true
  whatsapp: "+1234567890"  # Your phone number
  cooldown_seconds: 60

recordings:
  snapshots_dir: "./snapshots"
  keep_days: 7

logging:
  file: "./logs/detections.log"
  level: "INFO"

cameras:
  front-door:
    name: "Front Door"
    ip: "192.168.1.100"      # Your camera IP
    channel: 1               # Hikvision channel number
    user: "admin"            # Camera username
    password: "yourpassword" # Camera password
    poll_interval: 2
    enabled: true
    track:
      - person
      - car
    confidence: 0.5

model:
  name: "yolov8s"  # Options: yolov8n (fast), yolov8s (balanced), yolov8m (accurate)
  device: "cpu"    # Use "mps" for Apple Silicon, "cuda" for NVIDIA
```

### 4. 运行脚本

```bash
# Test cameras
python camera_watch.py --test

# Run in foreground
python camera_watch.py

# Run in background
nohup python camera_watch.py > /tmp/camera-watch.log 2>&1 &
```

## 可检测的物体（YOLOv8 COCO 分类）

**人及动物：**
人、鸟、猫、狗、马、羊、牛、大象、熊、斑马、长颈鹿

**车辆：**
自行车、汽车、摩托车、飞机、公交车、火车、卡车、船只

**常见物体：**
背包、雨伞、手提包、行李箱、瓶子、杯子、椅子、沙发、床、笔记本电脑、手机、电视

**完整列表：** 包括运动器材、食品、家具等 80 个类别

## 与夜间监控功能集成

如需实现自动化的夜间监控流程，可以创建一个单独的脚本，用于：
1. 在夜间（例如 00:00）启动监控功能
2. 在早晨（例如 07:00）停止监控功能
3. 发送包含检测结果和快照的报告

示例 cron 表达式：
```bash
# Start at midnight
0 0 * * * cd ~/camera-watch && source venv/bin/activate && nohup python camera_watch.py > /tmp/camera-watch.log 2>&1 &

# Stop at 7am and send report
0 7 * * * pkill -f camera_watch.py
```

## 通知机制

该脚本通过 Clawdbot 网关 API 发送通知。请确保 Clawdbot 正在运行，并根据需要配置网关 URL。

## 故障排除

**摄像头无法连接：**
- 验证 IP 地址和登录凭据
- 检查摄像头是否支持 ISAPI（Hikvision 协议）或尝试使用 RTSP 协议
- 确保摄像头位于同一网络中

**误报情况：**
- 提高检测置信度（从 0.5 提高到 0.7）
- 清洁摄像头镜头（去除蜘蛛网或昆虫残骸）
- 如可能，调整检测区域

**CPU 使用率过高：**
- 增加检测间隔时间（从 2 秒改为 5 秒）
- 使用更轻量级的模型（例如 yolov8n 而不是 yolov8s）