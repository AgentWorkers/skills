---
name: tasmota
description: 在本地网络中发现、监控和控制 Tasmota 智能家居设备。适用于需要通过网络扫描来查找 Tasmota 设备、检查设备状态和电源状态、控制设备（开关、亮度、颜色）、管理设备清单，或对运行 Tasmota 固件的 ESP8266 或 ESP32 设备进行其他 Tasmota 管理操作的场景。
---

# Tasmota设备管理

## 概述

本工具用于自动化发现和控制本地网络中的Tasmota智能设备（基于ESP8266/ESP32芯片）。支持网络扫描、设备状态监控、电源控制、亮度调节、颜色设置以及设备库存管理等功能。

## 快速入门

**扫描网络中的Tasmota设备：**
```bash
python3 scripts/tasmota-discovery.py
```

**检查设备状态：**
```bash
python3 scripts/tasmota-control.py <IP> status 0
```

**控制设备：**
```bash
python3 scripts/tasmota-control.py <IP> power on|off|toggle
python3 scripts/tasmota-control.py <IP> brightness 0-100
python3 scripts/tasmota-control.py <IP> color <hex-rgb>
```

## 设备发现

### 网络扫描

执行全面的网络扫描以找到所有Tasmota设备：

```bash
python3 scripts/tasmota-discovery.py
```

脚本功能：
1. 发送ping请求以识别活跃的设备；
2. 扫描活跃设备上的HTTP端口（80）；
3. 通过服务器头部信息（例如“Tasmota/13.1.0”）识别Tasmota设备；
4. 通过JSON API (`/cm?cmnd>Status%200`) 确认设备身份；
5. 获取设备的名称、版本和硬件信息。

输出内容包括：
- IP地址；
- 设备的友好名称；
- Tasmota版本；
- 硬件平台（ESP8266/ESP32）；
- 响应时间。

### 设备识别信号

Tasmota设备的识别依据包括：
- **服务器头部信息**：`Tasmota/<version> (<hardware>)`；
- **JSON API响应**：`/cm?cmnd>Status%200` 返回设备状态信息；
- **HTML内容中的关键词**：`Tasmota`。

## 设备控制

### 电源控制

切换或设置设备的电源状态：

```bash
# Toggle
python3 scripts/tasmota-control.py <IP> power toggle

# On/Off
python3 scripts/tasmota-control.py <IP> power on
python3 scripts/tasmota-control.py <IP> power off
```

### 亮度调节（支持调光功能的设备）

设置设备的亮度级别（0-100）：

```bash
python3 scripts/tasmota-control.py <IP> brightness 50
```

**注意：** 仅适用于支持调光功能的设备（需先通过 `StatusSTS` 检查设备是否支持调光功能）。

### 颜色设置（RGB灯）

设置RGB颜色（以十六进制或逗号分隔的形式）：

```bash
# Hex format
python3 scripts/tasmota-control.py <IP> color FF0000  # Red
python3 scripts/tasmota-control.py <IP> color 00FF00  # Green

# RGB comma format
python3 scripts/tasmota-control.py <IP> color 255,0,0
```

**注意：** 仅适用于支持RGB显示的设备（如AiYaTo-RGBCW等）。

## 状态查询

### 设备状态

获取设备的状态信息：

```bash
# Basic status
python3 scripts/tasmota-control.py <IP> status 0

# All statuses
python3 scripts/tasmota-control.py <IP> status all
```

**状态代码说明：**
- `0 = 设备状态` - 包括设备信息、友好名称和电源状态；
- `1 = 参数信息` - 包括设备运行时间、MAC地址等；
- `2 = 固件版本`；
- `3 = 日志设置`；
- `4 = 网络配置`（IP地址、网关信息、WiFi连接状态）；
- `5 = MQTT配置`；
- `9 = 时间信息`（时间、时区、日出/日落时间）。

### 关键状态字段

**StatusSTS（状态代码0）：**
- `POWER` - 当前电源状态（开/关）；
- `Dimmer` - 亮度级别（0-100）；
- `Wifi.RSSI` - WiFi信号强度；
- `Wifi.SSId` - 连接的WiFi网络ID。

**StatusNET：**
- `IPAddress` - 设备的IP地址；
- `Hostname` - mDNS主机名；
- `Mac` - 设备的MAC地址。

## 批量操作

### 获取所有设备状态

```bash
python3 scripts/tasmota-status.py
```

遍历设备清单文件，显示所有设备的电源状态。

### 设备库存管理

设备信息存储在CSV格式的清单文件中。文件格式如下：

```
IP Address,Device Name,Version,Hardware,Response Time (ms)
192.168.1.116,Office Hall Light,13.1.0,ESP8266EX,53
```

发现设备后，将扫描结果保存到清单文件中以便进行批量操作。

## 常见操作

### 查找带有标签的设备

```bash
# Scan and grep for specific device names
python3 scripts/tasmota-discovery.py | grep "Kitchen"
python3 scripts/tasmota-discovery.py | grep "Bulb"
```

### 检查所有灯光设备

```bash
# Get status of all devices
python3 scripts/tasmota-status.py
```

### 重启设备

```bash
# Off, wait 2s, on
python3 scripts/tasmota-control.py 192.168.1.116 power off
sleep 2
python3 scripts/tasmota-control.py 192.168.1.116 power on
```

## Tasmota API参考

### 命令格式

```
http://<IP>/cm?cmnd=<COMMAND>
```

### 常用命令

| 命令 | 功能 |
|---------|-------------|
| `Power` | 切换设备电源状态 |
| `Power ON` | 开启设备 |
| `Power OFF` | 关闭设备 |
| `Power TOGGLE` | 切换设备电源状态 |
| `Status 0` | 获取设备状态信息 |
| `Status 4` | 获取网络配置信息 |
| `Dimmer <0-100>` | 设置设备亮度 |
| `Color <hex>` | 设置设备RGB颜色 |
| `Fade <ON|OFF>` | 启用/关闭设备渐变效果 |

## 故障排除

### 设备未找到

- 确认设备位于同一子网内；
- 检查设备是否启用了HTTP服务器（配置文件中的Webserver 2选项）；
- 确保设备已通电并连接到WiFi网络；
- 尝试直接发送HTTP请求：`curl http://<IP>/cm?cmnd=Status%200`。

### 超时错误

- 设备可能处于节能模式（WiFi睡眠状态）；
- 网络延迟或数据包丢失；
- 检查设备是否最近重启过。

### 未知的电源状态

某些设备（如BLE网关、传感器）可能不支持电源控制功能。请通过 `StatusSTS` 检查设备的实际功能。

## 网络配置

Tasmota设备通常：
- 连接到WiFi的1-11频道；
- 使用DHCP自动获取IP地址（通过 `StatusNET` 查看当前IP）；
- 可能响应mDNS请求（主机名格式：tasmota-XXXXXX）；
- 使用HTTP协议（端口80）进行通信。

## 最佳实践

- 在网络维护期间进行扫描（避免高峰使用时段）；
- 缓存设备清单文件以避免重复扫描；
- 为设备设置易于识别的友好名称；
- 为关键设备设置静态IP地址（通过Tasmota网页界面或DHCP预留功能）；
- 在设备清单中按位置或功能对设备进行分组。

## 资源

### scripts/tasmota-discovery.py  
用于扫描网络并识别Tasmota设备的脚本，通过HTTP和JSON API进行设备识别。

### scripts/tasmota-control.py  
用于控制设备电源状态、亮度、颜色以及查询设备状态的脚本，通过Tasmota的JSON API实现。

### scripts/tasmota-status.py  
用于批量查询设备状态并显示设备电源状态的脚本。