# Home Assistant Skill

通过 Home Assistant API 控制智能家居设备。

## 技能元数据

- **名称**: homeassistant
- **类型**: OpenClaw 技能
- **用途**: 通过 HA API 控制灯光、开关、百叶窗、气候系统、场景以及脚本

## 设置命令

### 先决条件

1. Home Assistant 已在本地网络中运行
2. 从 Home Assistant 的个人资料页面获取长期有效的访问令牌

### 配置（单命令）

```bash
# Run this to configure
ha-cli setup <HA_URL> <TOKEN>

# Example:
ha-cli setup 192.168.1.100 your_long_lived_token_here
```

或者设置环境变量：

```bash
export HA_URL="http://homeassistant.local:8123"
export HA_TOKEN="your_token_here"
```

## 使用命令

### 基本控制

```bash
# Turn on device (any type)
ha-cli on <device_name>
ha-cli <device_name> on

# Turn off device
ha-cli off <device_name>
ha-cli <device_name> off
```

### 亮度与颜色

```bash
# Set brightness (0-100)
ha-cli brightness <0-100> <device_name>
ha-cli <device_name> brightness 75

# Set RGB color
ha-cli rgb #RRGGBB <device_name>
ha-cli rgb #FF5500 "Living Room"
```

### 温度

```bash
# Set temperature
ha-cli <temperature> <thermostat_name>
ha-cli 22 thermostat
```

### 场景与脚本

```bash
# Activate scene
ha-cli scene <scene_name>
ha-cli scene movie

# Run script
ha-cli script <script_name>
ha-cli script morning
```

### 状态与设备发现

```bash
# Check HA status
ha-cli status
ha-cli info

# List all entities
ha-cli list
ha-cli list entities

# List by domain
ha-cli list light
ha-cli list switch
ha-cli list climate
```

## 支持的设备类型

| 设备类型 | 命令 | 例子 |
|--------|----------|----------|
| 灯光 | 开启/关闭、调节亮度、更改颜色 | `ha-cli on living room` |
| 开关 | 开启/关闭 | `ha-cli off tv` |
| 百叶窗 | 打开/关闭 | `ha-cli open blinds` |
| 气候系统 | 设置温度/模式 | `ha-cli 22 thermostat` |
| 锁具 | 锁定/解锁 | `ha-cli lock front door` |
| 场景 | 激活场景 | `ha-cli scene movie` |
| 脚本 | 运行脚本 | `ha-cli script morning` |

## 实体匹配

- 不区分大小写
- 支持部分名称匹配（例如：bed → Bedroom Light）
- 支持模糊匹配

## 错误处理

- 连接错误：显示 Home Assistant 的 URL 和令牌设置指南
- 未找到设备：显示相似设备的建议
- 命令无效：显示使用帮助信息

## 相关技能

- openhue（Philips Hue 控制器）
- sonoscli（Sonos 音响控制）
- eightctl（Eight Sleep 控制系统）

## 文件

```
homeassistant/
├── SKILL.md      # This file
├── README.md     # User documentation
├── ha-cli        # Main CLI executable
├── ha            # Bash wrapper
└── config.json   # Saved configuration
```