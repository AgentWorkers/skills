---
name: apple-media
description: 在 macOS 上发现并控制 Apple 媒体设备/AirPlay 设备（如 HomePod、Apple TV、AirPlay 扬声器）。当您需要扫描 AirPlay 设备、将设备名称映射到对应的 IP 地址/ID、进行配对连接，以及使用 pyatv (atvremote) 和 Airfoil 来控制播放或音量时，可参考本文档。
---

# Apple Media（AirPlay + Apple TV 控制）

**作者：** Parth Maniar — [@officialpm](https://github.com/officialpm)

此技能是一个基于两个工具的工作流程封装：

- **pyatv**（`atvremote`）：用于发现 Apple TV 和 HomePod，并支持发送遥控器风格的命令（如果设备支持配对的话）。
- **Airfoil**：通过现有的 `airfoil` 技能，实现对 AirPlay 扬声器（包括 HomePod）的可靠连接/断开以及音量控制。

## 设置

此技能依赖于通过 **pipx** 安装的 **pyatv**。

安装/修复（已固定为 Python 3.12 版本，以避免 Python 3.14 的 asyncio 相关问题）：

```bash
pipx install pyatv || pipx upgrade pyatv
pipx reinstall pyatv --python python3.12
```

验证安装是否成功：

```bash
atvremote --help | head
```

## 快速入门

### 1) 扫描网络中的设备

```bash
# Fast scan (5s)
./scripts/scan.sh 5

# Faster scan when you know IP(s)
./scripts/scan-hosts.sh "10.0.0.28,10.0.0.111" 3

# Or JSON output
node ./scripts/scan-json.js 5
```

你将看到以下设备：
- HomePod（例如：“Living Room”（客厅）、“Bedroom”（卧室）等）
- Apple TV
- 支持 AirPlay 的电视

### 2) 控制 HomePod 或扬声器的音量（推荐方法）

使用 Airfoil 来控制扬声器的音量（对 HomePod 来说更为可靠）：

```bash
# List speakers Airfoil can see
../airfoil/airfoil.sh list

# Connect and set volume
./scripts/connect.sh "Living Room"
./scripts/volume.sh "Living Room" 35

# Disconnect (direct)
../airfoil/airfoil.sh disconnect "Living Room"
```

### 3) Apple TV 的遥控器命令（使用 pyatv）

首先扫描以获取 Apple TV 的名称或 ID，然后执行相应的命令：

```bash
# Examples (device name can be Apple TV or other targets)
atvremote -n "TV" playing
atvremote -n "TV" play_pause
atvremote -n "TV" turn_on
atvremote -n "TV" turn_off
```

如果出现认证或协议错误，可能需要输入设备配对信息（具体取决于设备类型）。

## 注意事项

- **使用 pyatv 控制 HomePod 时通常需要身份验证**，并且可能不支持所有的遥控器命令。
  - 如果使用 pyatv 时在播放或调节音量方面遇到问题，建议使用 Airfoil 来进行音量控制和扬声器路由。
- `atvremote scan` 是获取设备 IP 地址和 ID 的主要来源。

## 配置脚本

### `scripts/scan.sh`

该脚本会运行 `atvremote scan` 并允许用户配置超时时间。

```bash
./scripts/scan.sh 5
```

### `scripts/scan-json.js`

该脚本会将 `atvremote scan` 的输出解析为结构化的 JSON 格式（包含设备名称、地址、型号和服务信息）。

```bash
node ./scripts/scan-json.js
```