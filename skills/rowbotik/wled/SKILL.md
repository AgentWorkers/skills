---
name: wled
description: 通过 HTTP API 控制 WLED LED 控制器。当用户需要控制 WLED 灯具、LED 线条或基于 ESP 的 LED 控制器时，可以使用该功能。支持开关电源、调节亮度、设置颜色（RGB）、应用各种效果、选择颜色调色板、使用预设设置以及查询设备状态。
---

# WLED 控制

通过 HTTP JSON API 来控制 WLED LED 线条和矩阵。

## 前提条件

- WLED 设备必须位于同一网络内。
- 需知道设备的 IP 地址或主机名。
- 需要 Python 3 环境（无需额外依赖库）。

## 使用方法

所有命令都需要使用 `--host`（或 `-H`）参数来指定 WLED 设备的 IP 地址或主机名。

### 电源控制

```bash
python3 scripts/wled.py -H <ip> power          # Get power state
python3 scripts/wled.py -H <ip> power on       # Turn on
python3 scripts/wled.py -H <ip> power off      # Turn off
```

### 亮度调节

```bash
python3 scripts/wled.py -H <ip> brightness          # Get current brightness
python3 scripts/wled.py -H <ip> brightness 255      # Max brightness
python3 scripts/wled.py -H <ip> brightness 128      # 50% brightness
```

### 颜色设置

```bash
python3 scripts/wled.py -H <ip> color 255 0 0       # Red
python3 scripts/wled.py -H <ip> color 0 255 0       # Green
python3 scripts/wled.py -H <ip> color 0 0 255       # Blue
python3 scripts/wled.py -H <ip> color 255 255 255   # White
```

### 动画效果

```bash
python3 scripts/wled.py -H <ip> effects             # List all effects with IDs
python3 scripts/wled.py -H <ip> effect 0            # Solid color
python3 scripts/wled.py -H <ip> effect 9            # Rainbow
python3 scripts/wled.py -H <ip> effect 9 -s 200     # Rainbow, fast speed
python3 scripts/wled.py -H <ip> effect 9 -i 128     # Rainbow, medium intensity
```

### 色彩调色板

```bash
python3 scripts/wled.py -H <ip> palettes            # List all palettes with IDs
python3 scripts/wled.py -H <ip> palette 6           # Set Party palette
```

### 预设模式

```bash
python3 scripts/wled.py -H <ip> presets             # List saved presets
python3 scripts/wled.py -H <ip> preset 1            # Load preset #1
```

### 设备状态查询

```bash
python3 scripts/wled.py -H <ip> status              # Full device status
```

## 参考文档

完整的 API 文档请参见 [references/api.md](references/api.md)。

## 配置优化

为了避免每次使用命令时都输入 `--host` 参数，可以创建一个配置文件（位于 `~/.wled/config.json`）：

```json
{
  "bedroom": "192.168.1.100",
  "kitchen": "192.168.1.101",
  "living_room": "wled-abc123.local"
}
```

之后，可以使用别名来简化命令：
```bash
python3 scripts/wled.py -H bedroom brightness 255
python3 scripts/wled.py -H kitchen color 255 0 0
```

或者设置 `WLED_HOST` 环境变量：
```bash
export WLED_HOST=192.168.1.100
python3 scripts/wled.py brightness 255
```

## 查找 WLED 设备

通常可以通过以下方式找到 WLED 设备：
- 路由器管理面板（查找 ESP 设备相关选项）
- mDNS/Bonjour：`wled-<mac>.local`
- 使用 WLED 应用程序进行设备发现

## 推荐使用静态 IP 地址

IP 地址可能会随时间发生变化。为了避免频繁更新配置文件，建议为 WLED 设备设置一个静态 IP 地址：

**方法 1：通过路由器设置（最简单）**
1. 打开路由器管理面板。
2. 根据 MAC 地址找到 WLED 设备。
3. 为该设备分配一个静态 IP 地址。

**方法 2：通过设备本身设置**
1. 访问 WLED 的 Web 界面（地址：`http://<当前 IP 地址>`）。
2. 进入“设置” → “WiFi 设置”。
3. 手动设置静态 IP 地址。
4. 保存设置并重启设备。

使用 mDNS 主机名（例如 `wled-abc123.local`）也可以避免 IP 地址的变动，因为路由器会自动解析这些主机名。