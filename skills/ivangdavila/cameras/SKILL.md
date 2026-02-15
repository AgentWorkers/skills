---
name: Cameras
description: 通过协议支持和智能家居集成功能，您可以连接安全摄像头、捕获快照、控制摄影设备，并处理视频流。
---

## 决策树

| 任务 | 参考文档 |
|------|-----------|
| 连接安全摄像头（Ring、Nest、IP摄像头） | 查看 `security-integration.md` |
| 从网络摄像头或USB摄像头捕获视频 | 查看 `capture.md` |
| 控制单反相机/无反相机（远程拍摄） | 查看 `photography-control.md` |
| 处理视频（检测、识别） | 查看 `processing.md` |
| 选择或比较摄像头（购买指南） | 查看 `buying-guide.md` |

---

## 核心功能

**具备此技能的代理可以执行以下操作：**

1. **根据需求从任何已连接的摄像头捕获快照**  
2. **录制短片（10-60秒）以供查看或发送**  
3. **列出系统或网络中可用的摄像头**  
4. **接收来自安全系统的运动警报**  
5. **控制摄影设备（拍摄、调整设置、下载视频）**  
6. **利用视觉模型描述摄像头所拍摄的内容**  

---

## 协议快速参考

| 协议 | 用例 | 访问方式 |
|----------|----------|---------------|
| **RTSP** | IP摄像头、NVR | `rtsp://user:pass@ip:554/stream` |
| **ONVIF** | 发现设备 + 控制 | `python-onvif-zeep`（自动发现） |
| **HTTP/MJPEG** | 简单的IP摄像头 | `/snapshot.jpg`, `/video.mjpg` |
| **Home Assistant** | 统一访问 | REST API `/api/camera_proxy/` |
| **Frigate** | 运动事件 + 视频片段 | MQTT + HTTP API |
| **USB/V4L2** | 网络摄像头、采集卡 | `ffmpeg`, `opencv`（通过设备索引访问） |
| **gPhoto2** | 单反相机/无反相机的控制 | 使用USB PTP协议 |

---

## 常用命令

```
# List cameras
ffmpeg -list_devices true -f avfoundation -i dummy  # macOS
v4l2-ctl --list-devices                              # Linux

# Snapshot from RTSP
ffmpeg -i "rtsp://user:pass@ip/stream" -frames:v 1 snapshot.jpg

# Snapshot from webcam
ffmpeg -f avfoundation -i "0" -frames:v 1 webcam.jpg  # macOS
ffmpeg -f v4l2 -i /dev/video0 -frames:v 1 webcam.jpg  # Linux

# Record 10s clip
ffmpeg -i "rtsp://ip/stream" -t 10 -c copy clip.mp4
```

---

## 集成模式

### 与Home Assistant集成
如果摄像头已经集成到Home Assistant中，可以使用REST API进行控制：
```
GET /api/camera_proxy/camera.front_door
→ Returns JPEG snapshot
```

### 与Frigate集成（推荐用于安全监控）
Frigate负责视频检测，代理只需监听相关事件：
- MQTT：`frigate/events`（接收运动警报）
- HTTP：`/api/events/{id}/snapshot.jpg`（获取快照）

### 与视觉模型集成
捕获快照后，将其发送给视觉模型进行处理：
```
1. ffmpeg → snapshot.jpg
2. Vision API → "A person standing at the front door"
3. Return description to user
```

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 摄像头无法连接 | 检查网络连接、电源状态以及IP地址是否更改 |
| RTSP连接超时 | 尝试添加 `?tcp` 参数或使用端口8554 |
| 权限问题 | 以sudo权限运行程序，或将用户添加到视频访问组 |
| 仅输出音频无视频 | 流媒体路径错误，尝试使用 `/stream1`, `/ch01/main` |
| gPhoto2相机占用中 | 关闭其他使用该相机的应用程序，重新插入USB线 |

---

（注：由于代码块内容未提供，实际翻译中保留了相应的占位符 `_CODE_BLOCK_0_`。在实际文档中，这些占位符将被具体的代码或说明替换。）