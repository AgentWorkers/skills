---
name: reachy-mini
description: 通过 Pollen Robotics/Hugging Face 提供的 REST API 和 SSH 协议来控制 Reachy Mini 机器人。您可以使用这些接口执行以下操作：  
- 移动机器人的头部、身体或天线  
- 播放预设的情绪表达或舞蹈动作  
- 拍摄摄像头截图  
- 调整音量  
- 管理机器人运行的应用程序  
- 查查机器人的当前状态  
- 以及进行其他与机器人相关的物理交互操作。  

该机器人具备以下功能：  
- 6 自由度的头部运动  
- 360° 的身体旋转能力  
- 两个可动画显示的信息天线  
- 一个广角摄像头（支持 WebRTC 协议进行实时视频传输）  
- 由 4 个麦克风组成的阵列  
- 一个内置扬声器
---

# Reachy Mini 机器人控制

## 快速入门

您可以使用 CLI 脚本或 `curl` 来控制机器人。脚本的路径为：
```
~/clawd/skills/reachy-mini/scripts/reachy.sh
```

您可以通过设置环境变量 `REACHY_HOST` 或使用 `--host` 标志来指定机器人的 IP 地址。默认值为 `192.168.8.17`。

### 常用命令
```bash
reachy.sh status                    # Daemon status, version, IP
reachy.sh state                     # Full robot state
reachy.sh wake-up                   # Wake the robot
reachy.sh sleep                     # Put to sleep
reachy.sh snap                      # Camera snapshot → /tmp/reachy_snap.jpg
reachy.sh snap /path/to/photo.jpg   # Snapshot to custom path
reachy.sh play-emotion cheerful1    # Play an emotion
reachy.sh play-dance groovy_sway_and_roll  # Play a dance
reachy.sh goto --head 0.2,0,0 --duration 1.5  # Nod down
reachy.sh volume-set 70             # Set speaker volume
reachy.sh emotions                  # List all emotions
reachy.sh dances                    # List all dances
```

## 环境配置

| 变量          | 默认值       | 说明                          |
|-----------------|------------|-------------------------------------------|
| `REACHY_HOST`     | `192.168.8.17`    | 机器人 IP 地址                      |
| `REACHY_PORT`     | `8000`      | REST API 端口                      |
| `REACHY_SSH_USER`   | `pollen`     | SSH 用户名（用于 `snap` 命令）                |
| `REACHY_SSH_PASS`   | `root`     | SSH 密码（用于 `snap` 命令，使用 `sshpass`）            |

## 运动控制

### 头部控制（6 自由度）
头部可以执行俯仰（pitch）、偏航（yaw）和滚动（roll）动作，单位为弧度：
- **俯仰**（上下看）：-0.5（向上）到 0.5（向下）  
- **偏航**（左右看）：-0.8（向右）到 0.8（向左）  
- **滚动**（侧倾）：-0.5 到 0.5  

```bash
# Look up
reachy.sh goto --head -0.3,0,0 --duration 1.0

# Look left
reachy.sh goto --head 0,0.4,0 --duration 1.0

# Tilt head right, look slightly up
reachy.sh goto --head -0.1,0,-0.3 --duration 1.5

# Return to neutral
reachy.sh goto --head 0,0,0 --duration 1.0
```

### 身体旋转（360°）
身体偏航的角度，单位为弧度。0 表示向前，正值表示向左，负值表示向右。

```bash
reachy.sh goto --body 1.57 --duration 2.0   # Turn 90° left
reachy.sh goto --body -1.57 --duration 2.0  # Turn 90° right
reachy.sh goto --body 0 --duration 2.0      # Face forward
```

### 天线
机器人有两个天线（左侧和右侧），角度范围为约 -0.5 到 0.5 弧度。

```bash
reachy.sh goto --antennas 0.4,0.4 --duration 0.5    # Both up
reachy.sh goto --antennas -0.3,-0.3 --duration 0.5   # Both down
reachy.sh goto --antennas 0.4,-0.4 --duration 0.5    # Asymmetric
```

### 综合运动
```bash
# Look left and turn body left with antennas up
reachy.sh goto --head 0,0.3,0 --body 0.5 --antennas 0.4,0.4 --duration 2.0
```

### 插值模式
使用 `--interp` 参数与 `goto` 命令结合使用：
- `minjerk` — 平滑、自然的运动方式（默认值）  
- `linear` — 匀速运动  
- `ease` — 运动过程平滑过渡  
- `cartoon` — 动作夸张、富有动感  

## 情感表达与舞蹈动作

### 情感表达
机器人支持 80 多种预录制的表情动画，您可以根据场景选择合适的动画。

```bash
reachy.sh play-emotion curious1       # Curious look
reachy.sh play-emotion cheerful1      # Happy expression
reachy.sh play-emotion surprised1     # Surprise reaction
reachy.sh play-emotion thoughtful1    # Thinking pose
reachy.sh play-emotion welcoming1     # Greeting gesture
reachy.sh play-emotion yes1           # Nodding yes
reachy.sh play-emotion no1            # Shaking no
```

### 舞蹈动作
机器人共有 19 种舞蹈动作，非常适合娱乐或庆祝场合。

```bash
reachy.sh play-dance groovy_sway_and_roll
reachy.sh play-dance chicken_peck
reachy.sh play-dance dizzy_spin
```

### 完整列表
运行 `reachy.sh emotions` 或 `reachy.sh dances` 可查看所有可用的动作。

## 电机控制
在开始运动之前，必须先启用电机。请使用 `reachy.sh motors` 命令进行配置。

```bash
reachy.sh motors-enable     # Enable (needed for movement commands)
reachy.sh motors-disable    # Disable (robot goes limp)
reachy.sh motors-gravity    # Gravity compensation (manually pose the robot)
```

## 音量控制
```bash
reachy.sh volume            # Current speaker volume
reachy.sh volume-set 50     # Set speaker to 50%
reachy.sh volume-test       # Play test sound
reachy.sh mic-volume        # Microphone level
reachy.sh mic-volume-set 80 # Set microphone to 80%
```

## 应用管理
Reachy Mini 支持运行 HuggingFace Space 应用程序。您可以通过以下方式管理这些应用程序：
```bash
reachy.sh apps              # List all available apps
reachy.sh apps-installed    # Installed apps only
reachy.sh app-status        # What's running now
reachy.sh app-start NAME    # Start an app
reachy.sh app-stop          # Stop current app
```

**重要提示**：同一时间只能运行一个应用程序。启动新应用程序会停止当前正在运行的应用程序。某些应用程序可能会独占控制权，因此在发送手动运动指令前，请确保当前应用程序已停止运行。

## 相机快照
您可以使用 WebRTC 从机器人的 IMX708 宽角相机捕获 JPEG 格式的照片，这一过程不会干扰机器人的正常运行。

```bash
reachy.sh snap                        # Save to /tmp/reachy_snap.jpg
reachy.sh snap /path/to/output.jpg    # Custom output path
```

**使用要求**：需要通过 SSH 访问机器人（使用 `sshpass` 和环境变量 `REACHY_SSH_PASS`，默认值为 `root`）。

**工作原理**：机器人通过 GStreamer 的 `webrtcsrc` 插件连接到守护进程的 WebRTC 信号服务器（端口 8443），捕获一个 H264 解码后的帧并保存为 JPEG 图像。此过程不会导致守护进程重启或电机中断。

**注意**：为了获得清晰的图像，机器人必须处于“唤醒”状态（头部朝上）。如果机器人处于睡眠状态，相机会朝向身体方向。请先运行 `reachy.sh wake-up` 命令唤醒机器人。

## 音频感应
```bash
reachy.sh doa               # Direction of Arrival from mic array
```
该功能可以返回角度（单位为弧度，0 表示左侧，π/2 表示前方，π 表示右侧），以及语音检测结果（布尔值）。

## 基于上下文的反应（与 Clawdbot 的集成）
您可以使用 `reachy-react.sh` 脚本根据心率、定时任务或会话响应来触发机器人的特定行为。

```
~/clawd/skills/reachy-mini/scripts/reachy-react.sh
```

### 反应动作
```bash
reachy-react.sh ack           # Nod acknowledgment (received a request)
reachy-react.sh success       # Cheerful emotion (task done)
reachy-react.sh alert         # Surprised + antennas up (urgent email, alert)
reachy-react.sh remind        # Welcoming/curious (meeting reminder, to-do)
reachy-react.sh idle          # Subtle animation (heartbeat presence)
reachy-react.sh morning       # Wake up + greeting (morning briefing)
reachy-react.sh goodnight     # Sleepy emotion + sleep (night mode)
reachy-react.sh patrol        # Camera snapshot, prints image path
reachy-react.sh doa-track     # Turn head toward detected sound source
reachy-react.sh celebrate     # Random dance (fun moments)
```

使用 `--bg` 参数可以使脚本在后台运行（非阻塞模式）。

### 内置行为
- **安静时段**（美国东部时间 22:00–06:29）：除了 `morning`、`goodnight` 和 `patrol` 之外的所有反应动作都会被忽略。
- **自动唤醒**：在执行任何动作前，系统会确保机器人处于唤醒状态（如果需要，会重新启动守护进程）。
- **容错机制**：如果无法与机器人通信，相关反应会正常退出，而不会出现错误。

### 集成方式
| 触发条件 | 对应反应 | 备注                        |
|---------|------------|-----------------------------------------|
| 早晨提醒（6:30 AM） | `morning`   | 机器人醒来并打招呼                |
| 晚安提醒（10:00 PM） | `goodnight`   | 机器人播放安静的表情动画并进入睡眠状态       |
| 心跳检测 | `idle`     | 头部轻微倾斜、天线摆动或环顾四周                |
| 心跳检测（每 4 秒一次） | `doa-track` | 检测附近的语音并转向语音来源           |
| 心跳检测（每 6 秒一次） | `patrol`    | 通过相机快照监测房间环境                |
| 重要未读邮件 | `alert`     | 天线抬起并显示惊讶的表情              |
| 2 小时内的会议 | `remind`    | 表示欢迎或好奇的表情动作             |
| 亚历山大发送请求 | `ack`     | 简单点头回应                    |
| 任务完成   | `success`    | 随机播放欢快的表情动画                |
| 好消息或庆祝事件 | `celebrate`   | 随机执行舞蹈动作                    |

### 方向检测（DOA）
`doa-track` 功能利用机器人的四麦克风阵列检测语音方向，并使头部转向语音来源。方向角度（0=左侧，π/2=前方，π=右侧）会被映射到机器人的偏航动作。

### 监控房间
`patrol` 功能会定期拍摄房间照片并打印路径。您可以在心跳检测时使用该功能来监测房间内的活动或变化。

## 直接 API 访问
对于 CLI 未涵盖的功能，您可以使用 `curl` 或 `raw` 命令进行操作。

```bash
# Via raw command
reachy.sh raw GET /api/state/full
reachy.sh raw POST /api/move/goto '{"duration":1.0,"head_pose":{"pitch":0.2,"yaw":0,"roll":0}}'

# Via curl directly
curl -s http://192.168.8.17:8000/api/state/full | jq
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"duration":1.5,"head_pose":{"pitch":0,"yaw":0.3,"roll":0}}' \
  http://192.168.8.17:8000/api/move/goto
```

## 参考资料
有关完整的 API 端点列表、数据结构（如 GotoModelRequest、FullBodyTarget、XYZRPYPose）以及所有表情和舞蹈动作的详细信息，请参阅 [references/api-reference.md](references/api-reference.md)。

## 故障排除
- **机器人无法移动**：检查 `reachy.sh motors` 命令，确保电机已启用。运行 `reachy.sh motors-enable`。
- **无响应**：检查 `reachy.sh status` 命令，确认机器人处于运行状态。如果不是，请运行 `reachy.sh reboot-daemon`。
- **动作未被执行**：可能是某个应用程序正在独占控制权。请先使用 `reachy.sh app-stop` 停止该应用程序。
- **网络连接问题**：使用 `ping $REACHY_HOST` 命令验证机器人 IP 地址。同时检查 `reachy.sh wifi-status` 命令的状态。
- **快照显示黑屏**：机器人可能处于睡眠状态（头部向下）。请先运行 `reachy.sh wake-up` 命令唤醒机器人。
- **使用 SSH 时出现错误**：确保已安装 `sshpass` 并正确设置了 `REACHY_SSH_PASS`。