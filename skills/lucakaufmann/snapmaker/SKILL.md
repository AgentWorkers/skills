---
name: snapmaker
version: 1.0.0
description: 监控并控制 Snapmaker 3D 打印机（使用 Moonraker/Klipper 系统）。适用于查看打印状态、温度、进度，以及执行打印控制操作（暂停/恢复/取消）。相关事件触发词包括：`printer`、`3D print`、`Snapmaker`、`print status`、`nozzle temp`、`bed temp`。
license: MIT
---

# Snapmaker 打印机控制

通过 Moonraker API 控制 Snapmaker U1 打印机。

## 配置

在 `~/clawd/config/snapmaker.json` 文件中创建配置文件：
```json
{
  "ip": "192.168.x.x",
  "port": 80
}
```

或者使用环境变量：
```bash
export SNAPMAKER_IP=192.168.x.x
export SNAPMAKER_PORT=80  # optional, defaults to 80
```

**配置搜索顺序：**
1. `SNAPMAKER_IP` 环境变量（最高优先级）
2. `~/clawd/config/snapmaker.json`
3. `~/.config/clawdbot/snapmaker.json`

## 快速命令

### 检查状态
```bash
scripts/snapmaker.py status
```

### 线材信息
```bash
scripts/snapmaker.py filament
```
显示每个线材槽的 RFID 标签数据：材料类型、颜色（十六进制）、温度范围和传感器状态。

### 监控打印过程（实时）
```bash
scripts/snapmaker.py monitor
```

### 打印控制
```bash
scripts/snapmaker.py pause
scripts/snapmaker.py resume  
scripts/snapmaker.py cancel
```

### 温度
```bash
scripts/snapmaker.py temps
```

## API 参考

U1 打印机使用 Moonraker REST API，端口为 80：

| 端点 | 描述 |
|----------|-------------|
| `/server/info` | 服务器状态 |
| `/printer/info` | 打印机信息 |
| `/printer/objects/query?heater_bed&extruder&print_stats` | 打印机状态 |
| `/printer/print/pause` | 暂停打印 |
| `/printer/print/resume` | 恢复打印 |
| `/printer/print/cancel` | 取消打印 |

## 状态响应字段

- `print_stats.state`：`standby`（待机）、`printing`（打印中）、`paused`（暂停）、`complete`（完成）、`error`（错误）
- `print_stats.filename`：当前打印文件名
- `print_stats.print_duration`：已花费的秒数
- `virtual_sdcard.progress`：0.0 到 1.0（进度百分比）
- `heater_bed_temperature` / `heater_bed.target`：加热床温度
- `extruder_temperature` / `extruder.target`：喷头温度

## 线材与传感器数据

查询线材的 RFID 标签和传感器数据：
```
/printer/objects/query?filament_detect&filament_motion_sensor%20e0_filament&filament_motion_sensor%20e1_filament&filament_motion_sensor%20e2_filament&filament_motion_sensor%20e3_filament
```

### filament_detect.info[]

包含 4 个线材槽的 RFID 标签数据数组（如果没有标签，则使用默认值）：

| 字段 | 描述 |
|-------|-------------|
| `VENDOR` | “Snapmaker” 或 “NONE”（如果没有 RFID 标签） |
| `MANUFACTURER` | 例如：“Polymaker” |
| `MAIN_TYPE` | 材料类型：如 “PLA”、“PETG”、“ABS” 等 |
| `SUB_TYPE` | 变体类型：如 “SnapSpeed”、“generic” 等 |
| `RGB_1` | 颜色（十进制整数，转换方式：`#${(rgb>>16&0xFF).toString(16)}...`) |
| `ARGB_COLOR` | 带阿尔法通道的颜色（十进制） |
| `WEIGHT` | 线材卷的重量（克） |
| `HOTEND_MIN_TEMP` / `HOTEND_MAX_TEMP` | 喷头温度范围 |
| `BED_TEMP` | 推荐的加热床温度 |
| `OFFICIAL` | 如果是官方 Snapmaker 线材，则为 `true` |

### filament_motion_sensor e{0-3}_filament

| 字段 | 描述 |
|-------|-------------|
| `filament_detected` | 布尔值——表示线材是否存在于该槽中 |
| `enabled` | 布尔值——表示传感器是否处于活动状态 |

**注意：** 某个线材槽可能显示 `filament Detected: true` 但 `VENDOR: NONE`，这意味着该线材是第三方生产的、没有 RFID 标签的线材。