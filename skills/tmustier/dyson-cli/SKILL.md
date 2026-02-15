---
name: dyson-cli
description: 通过本地 MQTT 协议控制 Dyson 空气净化器、风扇和加热器。当需要控制 Dyson 设备时，可以使用该功能来调节风扇转速、设置温度/加热模式、开启摆动功能，或查看房间内的温度/湿度。请确保您的设备与 Dyson 设备处于同一 WiFi 网络中。
---

# Dyson CLI

## 先决条件

1. CLI 已安装在 `~/dyson-cli` 目录下，并使用了 `venv` 环境。
2. **必须与 Dyson 在同一个 WiFi 网络中**——仅支持本地 MQTT 操作，远程操作不可行。

**快速检查：**
```bash
cd ~/dyson-cli && source .venv/bin/activate && dyson list --check
```

## 命令

### 开/关电源
```bash
dyson on                      # Turn on
dyson off                     # Turn off
```

### 风扇控制
```bash
dyson fan speed 5             # Speed 1-10
dyson fan speed auto          # Auto mode
dyson fan oscillate on        # Enable oscillation
dyson fan oscillate on -a 90  # 90° sweep (45/90/180/350)
dyson fan oscillate off       # Disable oscillation
```

### 加热/制冷模式控制（适用于 Hot+Cool 型号）
```bash
dyson heat on                 # Enable heating
dyson heat off                # Disable heating
dyson heat target 22          # Set target temp (°C)
```

### 其他功能
```bash
dyson night on                # Night mode on
dyson night off               # Night mode off
dyson status                  # Show current state
dyson status --json           # JSON output
```

### 多个设备

使用 `-d <设备名称>` 来指定特定设备：
```bash
dyson on -d "Bedroom"
dyson fan speed auto -d "Office"
```

## 常用操作模式

```bash
# "Turn on the Dyson and set to auto"
dyson on && dyson fan speed auto

# "Heat to 23 degrees"
dyson heat on && dyson heat target 23

# "Turn on with gentle oscillation"
dyson on && dyson fan speed 3 && dyson fan oscillate on -a 45

# "What's the current temperature?"
dyson status --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Temp: {d['temperature']-273:.1f}°C, Humidity: {d['humidity']}%\")"
```

## 故障排除

如果命令执行失败：
1. 检查设备是否已连接到网络：`dyson list --check`
2. 确保设备与 Dyson 在同一个 WiFi 网络中。
3. 如果认证信息已过期，请重新运行设置命令：`dyson setup`

有关安装、设备设置及完整文档，请参阅 [README.md](README.md)。