---
name: vector-robot
description: 通过 Wire-Pod 控制 Anki Vector 机器人：  
- 可以通过 Vector 机器人发声；  
- 可以查看其摄像头拍摄的画面；  
- 可以移动机器人的头部、升降其高度或驱动其轮子；  
- 可以改变机器人眼睛的颜色；  
- 可以触发机器人预设的动画效果。  

适用于以下场景：  
- 当用户提到 Vector 机器人时；  
- 当用户希望通过机器人发声时；  
- 当用户需要控制这个实体机器人时；  
- 当用户需要与 Wire-Pod 进行交互时。
---

# 向量机器人控制

用于控制运行 wire-pod 的 Anki Vector 机器人。

## 先决条件

- 安装了 escape pod 固件版本的 Anki Vector 机器人
- wire-pod 已经安装并运行（https://github.com/kercre123/wire-pod）
- 需要 OpenClaw 代理服务器来处理语音输入（可选）

## 快速参考

所有 API 调用都需要 `&serial=SERIAL` 参数。默认值：`00501a68`。

```bash
SERIAL="00501a68"
WIREPOD="http://127.0.0.1:8080"
```

### 语音输出

```bash
# Make Vector speak (URL encode the text)
curl -s -X POST "$WIREPOD/api-sdk/assume_behavior_control?priority=high&serial=$SERIAL"
curl -s -X POST "$WIREPOD/api-sdk/say_text?text=Hello%20world&serial=$SERIAL"
curl -s -X POST "$WIREPOD/api-sdk/release_behavior_control?serial=$SERIAL"
```

或者使用辅助脚本：`scripts/vector-say.sh "Hello world"`

### 相机

```bash
# Capture frame from MJPEG stream
timeout 2 curl -s "$WIREPOD/cam-stream?serial=$SERIAL" > /tmp/stream.mjpeg
# Extract JPEG with Python (see scripts/vector-see.sh)
```

### 移动

**⚠️ 注意：在行为控制过程中，悬崖传感器将被禁用。请小心机器人的轮子运动！**

```bash
# Head: speed -2 to 2
curl -s -X POST "$WIREPOD/api-sdk/move_head?speed=2&serial=$SERIAL"  # up
curl -s -X POST "$WIREPOD/api-sdk/move_head?speed=-2&serial=$SERIAL" # down
curl -s -X POST "$WIREPOD/api-sdk/move_head?speed=0&serial=$SERIAL"  # stop

# Lift: speed -2 to 2  
curl -s -X POST "$WIREPOD/api-sdk/move_lift?speed=2&serial=$SERIAL"  # up
curl -s -X POST "$WIREPOD/api-sdk/move_lift?speed=-2&serial=$SERIAL" # down

# Wheels: lw/rw -200 to 200 (USE WITH CAUTION)
curl -s -X POST "$WIREPOD/api-sdk/move_wheels?lw=100&rw=100&serial=$SERIAL"  # forward
curl -s -X POST "$WIREPOD/api-sdk/move_wheels?lw=-50&rw=50&serial=$SERIAL"   # turn left
curl -s -X POST "$WIREPOD/api-sdk/move_wheels?lw=0&rw=0&serial=$SERIAL"      # stop
```

### 设置

```bash
# Volume: 0-5
curl -s -X POST "$WIREPOD/api-sdk/volume?volume=5&serial=$SERIAL"

# Eye color: 0-6
curl -s -X POST "$WIREPOD/api-sdk/eye_color?color=4&serial=$SERIAL"

# Battery status
curl -s "$WIREPOD/api-sdk/get_battery?serial=$SERIAL"
```

### 动作/意图

**可用意图：** `intent_imperative_dance`（强制跳舞）、`intent_system_sleep`（系统睡眠）、`intent_system_charger`（系统充电）、`intent_imperative-fetchcube`（获取立方体）、`explore_start`（开始探索）

## 语音输入（OpenClaw 集成）

要接收来自 Vector 的语音命令，请运行代理服务器：

```bash
node scripts/proxy-server.js
```

配置 wire-pod 的知识图谱（http://127.0.0.1:8080 → 服务器设置）：
- 提供者：自定义
- API 密钥：`openclaw`
- 端点：`http://localhost:11435/v1`
- 模型：`openclaw`

代理服务器会将接收到的问题写入 `request.json` 文件。您需要通过写入 `response.json` 文件来响应这些问题：

```json
{"timestamp": 1234567890000, "answer": "Your response here"}
```

## LaunchAgent（在 macOS 上自动启动）

将代理程序安装到 `~/Library/LaunchAgents/com.openclaw.vector-proxy.plist` 文件中以实现自动启动。详情请参阅 `scripts/install-launchagent.sh`。

## API 参考

有关完整的端点文档，请参阅 `references/api.md`。