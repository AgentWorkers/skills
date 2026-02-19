---
name: sentinel
description: 如何将配备IP网络摄像头的安卓手机通过OpenClaw转换为智能的边缘AI安全系统？
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["compare","curl","awk"]},"install":[{"id":"apt","kind":"apt","packages":["imagemagick"],"bins":["compare"],"label":"Install ImageMagick (apt)"}]}}
---
# 通过IP摄像头实现的Android应用安全监控

利用**Clawd Sentinel**模式，可以将任何普通的Android智能手机转变为一个高效、低成本的智能运动检测系统。

## 设置步骤

1. **Android端**：安装"Pavel Khlebovich"开发的"IP Webcam"应用，并启动服务器。
2. **连接设置**：记下设备的本地IP地址（例如：`192.168.1.100:8080`）。
3. **OpenClaw工作区**：
   - `bin/sentinel_ultra_frugal.sh`：负责像素差异检测的核心逻辑。
   - `bin/sentinel_runner.sh`：负责后台循环运行的脚本。

## 详细的API交互方式

IP Webcam服务器提供了类似REST的API，支持远程控制所有功能。基础URL为：`http://<IP>:8080/`

### 视频捕获功能
- **标准快照**：`/shot.jpg`（最快获取方式，显示当前帧）
- **自动对焦快照**：`/photoaf.jpg`（拍摄前会自动对焦，画质最高）
- **视频录制**：
  - 开始录制：`/startvideo?name=alert_123`
  - 停止录制：`/stopvideo`
  - 列出所有录制文件：`/list_videos`（返回JSON或HTML格式）
  - 下载视频：`/v/<filename>.mp4`

### 相机控制与设置
- **对焦距离**：`/settings/focus_distance?set=<0.0-10.0>`（0.0表示无限远）
- **闪光灯**：`/enabletorch` | `/disabletorch`
- **对焦模式**：`/settings/focusmode?set=<on|off|macro|infinity|fixed>`
- **场景模式**：`/settings/scenemode?set=<auto|night|action|party...>`
- **白平衡**：`/settings/whitebalance?set=<auto|daylight|cloudy...>`

### 设备状态监控
- **传感器数据**：`/sensors.json`（电池电量、光线强度、距离传感器、加速度计数据）
- **系统状态**：`/status.json`（摄像头状态、录制状态、运行时长）

### 音频功能
- **音频流**：`/audio.wav` 或 `/audio.opus`（实时音频流）

### 集成示例（使用curl命令）

```bash
# Get battery level via jq
curl -s http://<IP>:8080/sensors.json | jq '.battery_level[0][1][0]'

# Toggle flash remotely
curl http://<IP>:8080/enabletorch
```

## 推荐的阈值设置

- **白天（有雾或云层覆盖时）**：2500
- **夜间（光线较弱时）**：1500

## 注意事项
- **资源消耗**：只有当像素差异超过预设阈值时，系统才会消耗额外的计算资源。
- **隐私保护**：原始视频帧会保存在本地设备上，仅触发警报的视频帧才会被发送到AI服务器。
- **维护建议**：定期检查手机电池电量和Wi-Fi连接稳定性。
- **镜头眩光处理**：夜间模式下出现的长时间彩虹色眩光通常表示是固定光源（如路灯），而非车辆移动。