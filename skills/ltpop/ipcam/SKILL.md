---
name: ipcam
title: "IP Camera - RTSP & ONVIF Control"
description: "ONVIF PTZ（云台）控制功能 + RTSP（实时传输协议）视频捕获 + 摄像头自动发现。支持所有符合 ONVIF Profile S/T 标准的摄像机。已通过 TP-Link、Hikvision、Dahua、Reolink、Amcrest、Axis 等品牌摄像机的测试验证。"
metadata:
  openclaw:
    emoji: "📹"
    version: "1.0.0"
    author: "tao"
    requires:
      bins: ["ffmpeg", "python3", "jq"]
      pip: ["onvif-zeep"]
    install:
      - id: "auto"
        kind: "script"
        label: "Run install.sh"
        instructions: "bash install.sh"
---

# IP摄像头技能

通过**RTSP**（抓取图片、录制视频）和**ONVIF**（云台控制、预设设置、设备发现）来控制IP摄像头。

已在使用TP-Link Tapo/Vigi摄像头的情况下进行测试，同时支持Hikvision、Dahua、Reolink、Amcrest、Axis等支持ONVIF协议的摄像头。

## 设置

```bash
bash skills/ipcam/install.sh
```

之后可以选择自动发现摄像头或手动配置摄像头：

```bash
# Auto-discover and add
ptz.py discover --add

# Or edit config
nano ~/.config/ipcam/config.json
```

### 配置格式

```json
{
  "default": "front-door",
  "cameras": {
    "front-door": {
      "ip": "192.168.1.100",
      "username": "admin",
      "password": "secret",
      "rtsp_port": 554,
      "onvif_port": 2020,
      "rtsp_main_path": "stream1",
      "rtsp_sub_path": "stream2"
    }
  }
}
```

- `onvif_port`: 2020（TP-Link），80（Hikvision/Dahua），8000，8080
- `rtsp_main_path` / `rtsp_sub_path`: 可通过`ptz.py stream-uri --save`命令自动检测
- 环境变量覆盖项：`CAM_IP`，`CAM_USER`，`CAM_PASS`，`CAM_RTSP_PORT`，`CAM_ONVIF_PORT`

## 使用方法

### RTSP控制（`camera.sh`）

```bash
camera.sh snapshot                         # capture frame
camera.sh --cam cam2 snapshot /tmp/cam.jpg # specific camera
camera.sh record 15                        # record 15s clip
camera.sh stream-url sub                   # print sub-stream URL
camera.sh info                             # test connectivity
camera.sh list-cameras                     # list configured cameras
```

### 云台控制（`ptz.py`）

```bash
ptz.py status                     # current position
ptz.py move left                  # pan left (speed 0.5, 0.5s)
ptz.py move zoomin 0.8 1.0        # zoom in, speed 0.8, 1s
ptz.py goto 0.5 -0.2 0.0          # absolute pan/tilt/zoom
ptz.py home                       # home position
ptz.py stop                       # stop movement
ptz.py preset list                # list presets
ptz.py preset goto 1              # go to preset 1
ptz.py preset set 2 "Door"        # save current pos as preset
```

### 设备发现与流媒体地址

```bash
ptz.py discover                   # scan network for ONVIF cameras
ptz.py discover --add             # scan and add to config
ptz.py stream-uri                 # query RTSP paths from ONVIF
ptz.py stream-uri --save          # save paths to config
```

多摄像头使用时：在任何命令后添加`--cam <摄像头名称>`参数。

### 控制指令

`left`（向左移动），`right`（向右移动），`up`（向上移动），`down`（向下移动），`zoomin`（放大），`zoomout`（缩小），`upleft`（左上角移动），`upright`（右上角移动），`downleft`（左下角移动），`downright`（右下角移动）

## 故障排除

- **RTSP连接失败**：检查IP地址、端口或防火墙设置。使用`ptz.py stream-uri`命令验证路径是否正确。部分摄像头可能限制同时进行的RTSP连接，请尝试关闭其他客户端。
- **ONVIF连接失败**：确认摄像头的ONVIF端口已启用，并在摄像头的网络管理界面中启用ONVIF功能。常见端口包括2020、80、8000、8080。
- **未找到摄像头**：确保所有摄像头位于同一子网内，且ONVIF功能已启用；同时检查UDP多播是否被阻止。
- **云台控制失败**：并非所有摄像头都支持云台控制功能，请确认摄像头是否支持ONVIF Profile S协议。
- **认证错误**：检查用户名和密码是否正确。特殊字符会自动进行URL编码处理。