---
name: roku-control
description: "通过局域网（使用ECP协议）控制Roku设备。当用户需要操作他们的Roku电视或流媒体设备时，可以使用此方法：切换频道、启动应用程序（如Netflix、YouTube、Hulu等）、浏览菜单、调节音量、播放/暂停内容、搜索节目或关闭设备。该功能支持局域网连接，无需任何身份验证。"
---

# 控制 Roku 设备

您可以使用外部控制协议（ECP）通过本地网络来控制 Roku 设备。无需身份验证、云服务或复杂的设置——只需使用本地 HTTP 命令即可。

## 先决条件

- Roku 设备与 OpenClaw 在同一网络中。
- 确保已获取 Roku 的 IP 地址（可以自动检测）。

## 设置（首次使用）

**1. 检测 Roku 设备：**

```bash
python3 scripts/roku_control.py discover
```

这将显示网络中的所有 Roku 设备及其 IP 地址。

**2. 保存 Roku 的 IP 地址：**

记下 Roku 的 IP 地址（例如 `192.168.1.100`），以便在后续命令中使用。

**3. 测试连接：**

```bash
python3 scripts/roku_control.py --ip 192.168.1.100 info
```

## 常见操作

### 设备信息

```bash
# Get device details
python3 scripts/roku_control.py --ip 192.168.1.100 info

# List all installed apps
python3 scripts/roku_control.py --ip 192.168.1.100 apps

# See what's currently playing
python3 scripts/roku_control.py --ip 192.168.1.100 active
```

### 导航与控制

```bash
# Navigate menus
python3 scripts/roku_control.py --ip 192.168.1.100 key Up
python3 scripts/roku_control.py --ip 192.168.1.100 key Down
python3 scripts/roku_control.py --ip 192.168.1.100 key Left
python3 scripts/roku_control.py --ip 192.168.1.100 key Right
python3 scripts/roku_control.py --ip 192.168.1.100 key Select

# Go home
python3 scripts/roku_control.py --ip 192.168.1.100 key Home

# Go back
python3 scripts/roku_control.py --ip 192.168.1.100 key Back
```

### 播放

```bash
# Play/pause
python3 scripts/roku_control.py --ip 192.168.1.100 key Play
python3 scripts/roku_control.py --ip 192.168.1.100 key Pause

# Rewind/fast forward
python3 scripts/roku_control.py --ip 192.168.1.100 key Rev
python3 scripts/roku_control.py --ip 192.168.1.100 key Fwd

# Instant replay (back 10 seconds)
python3 scripts/roku_control.py --ip 192.168.1.100 key InstantReplay
```

### 音量与电源

```bash
# Volume control (Roku TV or HDMI-CEC enabled)
python3 scripts/roku_control.py --ip 192.168.1.100 key VolumeUp
python3 scripts/roku_control.py --ip 192.168.1.100 key VolumeDown
python3 scripts/roku_control.py --ip 192.168.1.100 key VolumeMute

# Power off
python3 scripts/roku_control.py --ip 192.168.1.100 key PowerOff
```

### 启动应用程序

```bash
# Launch by app ID (faster)
python3 scripts/roku_control.py --ip 192.168.1.100 launch 12  # Netflix

# Launch by app name (case-insensitive)
python3 scripts/roku_control.py --ip 192.168.1.100 launch Netflix
python3 scripts/roku_control.py --ip 192.168.1.100 launch YouTube
python3 scripts/roku_control.py --ip 192.168.1.100 launch "Disney+"
```

### 搜索与文本输入

```bash
# Send search text
python3 scripts/roku_control.py --ip 192.168.1.100 text "Breaking Bad"

# This is much faster than individual key presses for searches
```

## 自然语言转换

将用户指令转换为相应的命令：

**导航：**
- “返回主屏幕” → `按 Home 键`
- “返回上一级” → `按 Back 键`
- “向下滚动” → `按 Down 键`
- “选择此选项” → `按 Select 键`

**播放：**
- “播放” → `按 Play 键`
- “暂停” → `按 Pause 键`
- “倒带” → `按 Rev 键`
- “快进” → `按 Fwd 键`
- “回放 10 秒” → `按 InstantReplay 键`

**音量：**
- “调高音量” → `按 VolumeUp 键`
- “调低音量” → `按 VolumeDown 键`
- “静音” → `按 VolumeMute 键`

**应用程序：**
- “打开 Netflix” → `launch Netflix`
- “打开 YouTube” → `launch YouTube`
- “打开 Hulu” → `launch Hulu`

**搜索：**
- “搜索《绝命毒师》” → `输入 “Breaking Bad”`
- “查找《怪奇物语》” → 打开搜索框并输入相关内容

**电源：**
- “关闭电视” → `按 PowerOff 键`

## 常见应用程序 ID

请参阅 [references/common-apps.md](references/common-apps.md) 以获取完整的应用程序 ID 列表。

**快速参考：**
- Netflix: 12
- YouTube: 837
- Hulu: 2285
- Disney+: 291097
- Amazon Prime Video: 13
- HBO Max: 61322
- The Roku Channel: 151908

要获取您的特定 Roku 设备的应用程序 ID，请参阅 [references/remote-keys.md](references/remote-keys.md)。

## 完整的按键参考

请参阅 [references/remote-keys.md](references/remote-keys.md) 以了解所有支持的操作按键。

**常用按键：** Home, Back, Up, Down, Left, Right, Select, Play, Pause, Rev, Fwd, VolumeUp, VolumeDown, VolumeMute, PowerOff, Search, Info

## 高级用法

### 观看 Netflix

```bash
# Go home, launch Netflix
python3 scripts/roku_control.py --ip 192.168.1.100 key Home
sleep 1
python3 scripts/roku_control.py --ip 192.168.1.100 launch 12
```

### 搜索与播放

```bash
# Open search, send text, select first result
python3 scripts/roku_control.py --ip 192.168.1.100 key Search
sleep 1
python3 scripts/roku_control.py --ip 192.168.1.100 text "The Office"
sleep 1
python3 scripts/roku_control.py --ip 192.168.1.100 key Select
```

### 快速回放

```bash
# Go back 10 seconds and resume
python3 scripts/roku_control.py --ip 192.168.1.100 key InstantReplay
sleep 1
python3 scripts/roku_control.py --ip 192.168.1.100 key Play
```

### 电影之夜设置

```bash
# Launch streaming app, adjust volume
python3 scripts/roku_control.py --ip 192.168.1.100 launch "Disney+"
sleep 2
python3 scripts/roku_control.py --ip 192.168.1.100 key VolumeDown
python3 scripts/roku_control.py --ip 192.168.1.100 key VolumeDown
```

## 设备映射

将 Roku 的 IP 地址保存到 `references/roku.json` 文件中：

```json
{
  "living_room": {
    "ip": "192.168.1.100",
    "name": "Living Room TV",
    "model": "Roku Ultra"
  },
  "bedroom": {
    "ip": "192.168.1.101",
    "name": "Bedroom Roku",
    "model": "Roku Streaming Stick+"
  }
}
```

之后可以在对话中通过友好名称来引用该设备。

## 故障排除

**“未找到 Roku 设备”**
- 确保 Roku 已开机并连接到网络。
- 检查 OpenClaw 和 Roku 是否在同一网络/子网中。
- 有些路由器会阻止 SSDP 协议的检测——如果知道 Roku 的 IP 地址，可以尝试手动输入 IP 地址。
- 在 Roku 的设置 → 网络选项中验证网络设置。

**“连接超时”**
- 确认 IP 地址正确。
- 使用 `ping <roku-ip>` 命令测试连接。
- 检查防火墙是否阻止了端口 8060 的通信。
- Roku 的 IP 地址可能发生了变化（请使用 DHCP 预留地址）。

**“按键无效”**
- 有些按键仅适用于特定的 Roku 电视（如音量、电源按键）。
- 音量按键可能需要 HDMI-CEC 功能或支持该功能的 Roku 电视。
- 旧版本的设备可能不支持某些电源控制命令。
- 请参阅 [references/remote-keys.md](references/remote-keys.md) 以确认兼容性。

**应用程序无法启动**
- 确认应用程序已安装：运行 `apps` 命令。
- 使用正确的应用程序 ID（名称匹配时区分大小写）。
- 有些应用程序需要在应用程序界面中进行额外的身份验证。

**设备无法被检测到**
- 如果知道 Roku 的 IP 地址，可以尝试手动输入：检查路由器的 DHCP 配置。
- Roku 的 IP 地址可以在设置 → 网络 → 关于中查看。
- 为提高稳定性，可以设置静态 IP 地址或使用 DHCP 预留地址。

## 与其他技能的集成

### 电影之夜流程

可以将此功能与 Govee 灯光控制技能结合使用：

```bash
# Dim lights
for light in "living room" "tv lights"; do
  python3 govee-lights/scripts/govee_control.py brightness "$light" 15
  python3 govee-lights/scripts/govee_control.py temp "$light" 2700
done

# Launch streaming app
python3 roku-control/scripts/roku_control.py --ip 192.168.1.100 launch Netflix

# Set comfortable volume
python3 roku-control/scripts/roku_control.py --ip 192.168.1.100 key VolumeDown
```

## 注意事项

- ECP 协议完全通过局域网工作（无需互联网连接）。
- 无需身份验证或 API 密钥。
- 命令响应迅速（基于本地网络速度）。
- 可以独立控制多个 Roku 设备。
- 支持 Roku 电视、流媒体控制器和播放设备。
- 无法通过按键直接开机（ECP 协议的限制——Roku 必须处于开机状态）。
- 如果支持 HDMI-CEC 功能，可以使用该功能来开机。

## 限制

- 无法关闭完全关闭的 Roku 设备（ECP 协议仅在设备开机时有效）。
- 音量/电源控制命令仅适用于 Roku 电视或支持 HDMI-CEC 功能的设备。
- 有些命令没有操作成功的反馈。
- 文本输入是逐个字符输入的（长搜索时速度较慢）。
- 设备检测需要依赖 SSDP 协议（某些网络可能会阻止多播通信）。