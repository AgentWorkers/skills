---
name: Cameras
slug: cameras
version: 1.0.1
description: 通过协议支持，连接到安全摄像头，捕获快照，并处理视频流。
changelog: User-driven credential model, declared tool requirements
metadata: {"clawdbot":{"emoji":"📷","requires":{"bins":["ffmpeg"]},"os":["linux","darwin"]}}
---
## 范围

本技能包括：
- ✅ 生成用于摄像头捕获的命令
- ✅ 指导如何将摄像头集成到安全系统中
- ✅ 提供针对摄像头问题的故障排除支持

**用户驱动的模型：**
- 用户提供摄像头访问凭据（RTSP地址、密码）
- 用户运行捕获命令
- 用户安装所需的工具

**本技能不执行以下操作：**
- ❌ 保存摄像头凭据
- ❌ 未经用户请求自动运行捕获操作
- ❌ 未经用户提供访问信息的情况下访问摄像头

## 要求

**必备软件：**
- `ffmpeg` — 用于捕获和录制视频

**可选软件（用户可根据需要安装）：**
- `gphoto2` — 用于控制DSLR或无反光镜相机
- `v4l2-ctl` — 用于Linux系统上的USB摄像头

## 快速参考

| 主题 | 对应文档文件 |
|-------|------|
| 安全摄像头集成 | `security-integration.md` |
| USB/网络摄像头捕获 | `capture.md` |
| DSLR控制 | `photography-control.md` |
| 视频处理 | `processing.md` |

## 核心规则

### 1. 用户提供摄像头访问权限
当用户请求进行视频捕获时：
```
User: "Snapshot from my front door camera"
Agent: "I need the RTSP URL. Format: rtsp://user:pass@ip/stream
        Provide it or set CAMERA_FRONT_URL in env."
User: "rtsp://admin:pass@192.168.1.50/stream1"
→ Agent generates: ffmpeg -i "URL" -frames:v 1 snapshot.jpg
```

### 2. 常用命令
```bash
# Snapshot from RTSP (user provides URL)
ffmpeg -i "$RTSP_URL" -frames:v 1 snapshot.jpg

# Record 10s clip
ffmpeg -i "$RTSP_URL" -t 10 -c copy clip.mp4

# Webcam snapshot (macOS)
ffmpeg -f avfoundation -i "0" -frames:v 1 webcam.jpg

# Webcam snapshot (Linux)
ffmpeg -f v4l2 -i /dev/video0 -frames:v 1 webcam.jpg
```

### 3. 协议参考
| 协议 | 使用场景 | URL格式 |
|----------|----------|------------|
| RTSP | IP摄像头 | `rtsp://user:pass@ip:554/stream` |
| HTTP | 简单摄像头 | `http://ip/snapshot.jpg` |
| V4L2 | USB摄像头 | `/dev/video0` |

### 4. 集成方式
**与Home Assistant集成：**
```
GET /api/camera_proxy/camera.front_door
```
用户需要提供Home Assistant的URL和访问令牌。

**与Frigate集成：**
- 使用MQTT协议发送事件：`frigate/events`（用于接收警报）
- 使用HTTP协议获取截图：`/api/events/{id}/snapshot.jpg`

### 5. 安全性注意事项**
- **严禁记录包含凭据的摄像头URL**  
- **建议用户将相关URL存储在环境变量中**  
- **RTSP流可能未加密——请注意局域网安全风险**