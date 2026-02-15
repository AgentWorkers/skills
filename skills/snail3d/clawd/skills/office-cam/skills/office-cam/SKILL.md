---
name: office-cam
description: 多摄像头系统，适用于办公室或家庭监控。支持使用USB网络摄像头（如Logitech品牌）、WiFi Wyze摄像头（通过RTSP协议传输视频）以及ESP32开发板上的摄像头。该系统可用于查看房间内部情况、按需拍摄照片或监控多个区域。
metadata:
  clawdbot:
    emoji: 🎥
---

# 办公室摄像头系统 - 多摄像头集成方案

该系统支持多种类型的摄像头，可构建覆盖整个房屋的摄像头网络。

## 支持的摄像头类型

| 类型 | 可靠性 | 设置方式 | 适用场景 |
|------|-------------|-------|----------|
| 🖥️ **USB网络摄像头** | ⭐⭐⭐⭐⭐ | 即插即用 | 办公桌、办公室环境 |
| 📹 **Wyze PTZ/v3** | ⭐⭐⭐⭐⭐ | 支持RTSP流传输 | 房间、车库、仓库等 |
| 📡 **ESP32-CAM** | ⭐⭐⭐ | 仅支持ESP-NOW无线连接 | 适合DIY项目或电池供电设备 |

## 快速入门

```bash
# USB Webcam (instant)
~/clawd/skills/office-cam/scripts/capture.sh

# Wyze PTZ (one-time setup required)
~/clawd/skills/office-cam/scripts/wyze-dashboard add
~/clawd/skills/office-cam/scripts/wyze-dashboard capture shed

# ESP32-CAM (ESP-NOW wireless)
# Flash firmware, auto-discovers base station, sends photos wirelessly
```

---

## 🖥️ USB网络摄像头（Logitech）

**最可靠的解决方案——即刻可用。**

### 基本拍摄功能
```bash
cd ~/clawd/skills/office-cam
./scripts/capture.sh /tmp/office.jpg
```

### 动作检测功能 ⭐ 新功能
```bash
# Start motion detection (runs continuously)
./scripts/motion-detect.sh

# Captures saved to ~/.clawdbot/motion-captures/
# Automatically triggers when motion detected
# 5-second cooldown between captures
```

### 🔥 监控模式（AI监控） ⭐⭐⭐
```bash
# Start AI-powered continuous monitoring
./scripts/overwatch start

# Check status
./scripts/overwatch status

# Stop monitoring
./scripts/overwatch stop
```

**监控模式的功能：**
- 24/7后台监控摄像头画面
- 检测到动作时触发警报
- 可通过OpenClaw系统发送通知
- 将检测到的动作画面保存至 `~/.clawdbot/overwatch/` 目录

**操作指令：**
- *"启动监控模式"* 或 *"继续监控"* 

### 🤖 智能监控模式（AI自动触发） ⭐⭐⭐⭐⭐
```bash
# Start smart monitoring (zero cost until trigger)
./scripts/smart-overwatch start

# I will check for triggers and analyze when found
```

**工作原理：**
1. **本地动作检测**（通过文件大小变化判断动作）
- 检测到动作后，在 `~/.clawdbot/overwatch/triggers/` 目录生成触发文件
- 系统会使用视觉模型分析图像（仅当检测到动作时触发）
- **发现有人？** 发送警报并可选继续监控
- **无人？** 删除触发文件，恢复本地监控

**操作指令：**
- *"启动智能监控"*  
- *"发现有人时通知我"*  
- *"仅监控有人出现的情况"*  
- *"查看监控触发记录"*（手动查看分析结果）

**费用：** 在检测到动作前无需费用；分析图像时才产生费用

### 📸 即时通过Telegram发送照片 ⭐⭐⭐⭐⭐
**快速拍摄并发送照片——最简单的查看摄像头画面的方式**

**操作指令：**
- *"查看办公室画面"*  
- *"摄像头现在拍的是什么？"*  
- *"给我发张照片"*  

**工作流程：**
- 立即从摄像头拍摄照片  
- 分析照片中的清晰人脸或活动  
- 将最佳照片发送至您的Telegram账户  

**无需实时流传输——只需在需要时接收照片。**

### 🔥 监控模式高级版（全功能） ⭐⭐⭐⭐⭐⭐
**完整监控解决方案——包含Telegram警报和远程控制**

**功能：**
- 检测到动作时立即发送Telegram警报  
- 提供实时JPEG流（地址：http://localhost:8080）  
- 每2秒自动更新画面  
- 将所有拍摄的照片保存至 `~/.clawdbot/overwatch/`  
- 可通过Telegram机器人接收指令（如 `analyze`、`stream`、`capture`）  

**网络配置：**
```bash
# Local
http://localhost:8080

# From another device on same network
http://$(hostname -I | awk '{print $1}'):8080
```

**每日晨报（含照片）：**
- 每日上午8点（美国/丹佛时区）自动生成  
- 发送办公室的最新照片  
- 总结夜间发生的动作事件  
- 提供命令参考  

**动作检测要求：**
```bash
brew install imagemagick  # For image comparison
```

---

## 📹 Wyze摄像头

### 一次设置流程：

1. **在Wyze应用程序中启用RTSP功能：**
   - 打开Wyze应用 → 设置摄像头 → 高级设置  
   - 启用RTSP传输并设置密码  
   - 复制RTSP地址  

2. **将摄像头添加到系统：**
   ```bash
   ~/clawd/skills/office-cam/scripts/wyze-dashboard add
   # Enter camera name (e.g., "shed")
   # Enter RTSP URL
   ```

3. **开始拍摄：**
   ```bash
   # Single camera
   ~/clawd/skills/office-cam/scripts/wyze-dashboard capture shed
   
   # All cameras
   ~/clawd/skills/office-cam/scripts/wyze-dashboard capture-all
   
   # Quick one-liner (after setup)
   ~/clawd/skills/office-cam/scripts/wyze-capture shed
   ```

---

## 📡 ESP32-CAM（ESP-NOW无线摄像头）

**无需WiFi路由器！** 通过ESP32模块实现无线连接。

### 系统架构：**
```
┌─────────────────┐      ESP-NOW      ┌─────────────────┐
│  ESP32-CAM      │  ═══════════════► │  ESP32 Base     │◄── USB ──► Mac
│  (Camera Node)  │   (100m range)    │  (Receiver)     │
└─────────────────┘                   └─────────────────┘
        Battery powered                  Plugged into computer
```

### 组装步骤：

**基站**（普通ESP32模块，连接至Mac电脑）：
```bash
cd ~/clawd/skills/office-cam/firmware/espnow-base
pio run --target upload
```

**摄像头节点**（配备摄像头的ESP32模块）：
```bash
cd ~/clawd/skills/office-cam/firmware/espnow-cam-auto
pio run --target upload
```

**工作原理：**
- 基站每2秒发送一次信号  
- 摄像头自动检测并连接基站  
- 摄像头无线传输照片  
- 基站接收照片并保存至SD卡或串行端口  

**传输范围：** 超过100米（无需WiFi网络！）

---

## 相关文件

| 文件名 | 用途 |
|--------|---------|
| `capture.sh` | 用于USB网络摄像头控制 |
| `wyze-capture` | 快速拍摄Wyze摄像头画面 |
| `wyze-dashboard` | 多摄像头管理工具 |
| `firmware/espnow-base/` | ESP32接收端固件 |
| `firmware/espnow-cam-auto/` | ESP32-CAM发送端固件 |

---

## 故障排除

**Wyze摄像头连接失败：**
- 确认Wyze应用中已启用RTSP功能  
- 检查用户名和密码是否正确  
- 确保摄像头与基站处于同一WiFi网络  

**ESP32-CAM无法连接：**
- 保持设备在10英尺范围内  
- 检查LED指示灯状态：闪烁表示正在连接，常亮表示正在拍摄  
- 尝试重启设备  

**USB网络摄像头无法使用：**
- 安装 `imagesnap` 工具：`brew install imagesnap`  
- 进入系统设置 → 隐私设置 → 摄像头选项  

---