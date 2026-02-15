---
name: devialet
description: "通过 HTTP API 控制 Devialet Phantom 扬声器。支持以下功能：播放/暂停、音量调节、静音/取消静音、源选择以及扬声器状态查询。需要使用 DOS 2.14 或更高版本的固件。该功能适用于 Phantom I、Phantom II、Phantom Reactor 和 Dialog 型号。"
---

# Devialet 扬声器控制

通过 Spotify 集成，在本地网络中控制 Devialet 扬声器（Phantom、Mania）。

## 自然语言指令

当用户说出以下指令时：
- **“在我的扬声器上播放 Nines - Lick Shots”** → 通过 Spotify 进行搜索并播放
- **“将扬声器音量设置为 40”** → 调整音量
- **“暂停音乐”** → 暂停播放
- **“正在播放什么？”** → 查看当前曲目和状态

## 设置

1. 查找扬声器的 IP 地址（可以在路由器或 Devialet 应用程序中查看）
2. 设置 `DEVIALET_IP` 环境变量，或将其添加到 `TOOLS.md` 文件中：
   ```
   ## Devialet Speaker
   - IP: 192.168.x.x
   ```

3. 为了实现 Spotify 集成，请安装 Spotify 桌面应用程序、`playerctl` 和 `xdotool`。

## 快速使用方法

```bash
# Set your speaker IP
export DEVIALET_IP="192.168.x.x"

# Play a song (search and play)
./scripts/play-on-devialet.sh "Drake - God's Plan"

# Play by Spotify URI
./scripts/play-on-devialet.sh spotify:track:4YZNJOA9d8wiO5ELNY5WxC

# Pause / Resume
./scripts/play-on-devialet.sh pause
./scripts/play-on-devialet.sh resume

# Volume
./scripts/play-on-devialet.sh volume 50

# Status
./scripts/play-on-devialet.sh status
```

## 硬件要求

- **配备 DOS 2.14+ 或 SDOS 1.3+ 固件版本的 Devialet 扬声器**
- **Spotify 集成（可选）**：
  - 运行并登录 Spotify 桌面应用程序
  - 安装 `playerctl` 和 `xdotool`（使用 `sudo apt install playerctl xdotool`）
  - 将扬声器设置为 Spotify Connect 设备（在 Spotify 应用程序中完成设置）

## 工作原理

1. 通过 Spotify 桌面应用程序（使用 D-Bus/MPRIS 协议）搜索曲目
2. 在 Spotify 中打开曲目的 URI
3. Spotify 通过 Spotify Connect 将音乐流传输到 Devialet 扬声器
4. Devialet 使用其 API 来控制播放和音量

## 直接使用 Devialet API

对于不依赖 Spotify 的控制方式（请将 `$DEVIALET_IP` 替换为实际的扬声器 IP 地址）：

```bash
# Volume (0-100)
curl -X POST -H "Content-Type: application/json" \
  -d '{"volume": 50}' \
  "http://$DEVIALET_IP/ipcontrol/v1/systems/current/sources/current/soundControl/volume"

# Play/Pause
curl -X POST "http://$DEVIALET_IP/ipcontrol/v1/groups/current/sources/current/playback/play"
curl -X POST "http://$DEVIALET_IP/ipcontrol/v1/groups/current/sources/current/playback/pause"

# Mute/Unmute
curl -X POST "http://$DEVIALET_IP/ipcontrol/v1/groups/current/sources/current/playback/mute"
curl -X POST "http://$DEVIALET_IP/ipcontrol/v1/groups/current/sources/current/playback/unmute"

# Get status
curl -s "http://$DEVIALET_IP/ipcontrol/v1/devices/current" | jq .
```

## 支持的型号

- Phantom I、Phantom II、Phantom Reactor（DOS 2.14+ 版本）
- Dialog
- Mania（SDOS 1.3+ 版本）

## API 参考

有关完整的 API 文档，请参阅 `references/api.md`。