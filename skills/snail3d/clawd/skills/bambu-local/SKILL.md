---
name: bambu-local
description: **通过 MQTT 在本地控制 Bambu Lab 3D 打印机（无需使用云服务）**  
支持型号：A1、A1 Mini、P1P、P1S、X1C。
homepage: https://github.com/Doridian/OpenBambuAPI
metadata: {"clawdbot":{"emoji":"🖨️","requires":{"bins":["python3"]}}}
---
# Bambu Local - 3D打印机本地控制

无需依赖云服务，即可通过MQTT协议本地控制Bambu Lab打印机。

## 设置

1. 创建虚拟环境：
```bash
python3 -m venv ~/bambu-env
source ~/bambu-env/bin/activate
pip install paho-mqtt
```

2. 在`skill`文件夹中创建`config.json`文件：
```json
{
  "printer_ip": "192.168.x.x",
  "access_code": "xxxxxxxx",
  "serial": "xxxxxxxxxxxx",
  "printer_name": "MyPrinter"
}
```

从打印机上获取以下信息：设置 → 仅限局域网模式（访问代码）以及设置 → 设备（串行端口）。

## 命令

### 状态查询
```bash
run ~/clawd/skills/bambu-local/bambu status
```

### 灯光控制
```bash
run ~/clawd/skills/bambu-local/bambu light on
run ~/clawd/skills/bambu-local/bambu light off
```

### 打印控制
```bash
run ~/clawd/skills/bambu-local/bambu print pause
run ~/clawd/skills/bambu-local/bambu print resume
run ~/clawd/skills/bambu-local/bambu print stop
```

### 打印速度（1=静音模式，2=标准模式，3=高速模式，4=极限模式）
```bash
run ~/clawd/skills/bambu-local/bambu speed 2
```

### 温度设置
```bash
run ~/clawd/skills/bambu-local/bambu temp --bed 60
run ~/clawd/skills/bambu-local/bambu temp --nozzle 200
```

### G-code文件传输
```bash
run ~/clawd/skills/bambu-local/bambu gcode "G28"
```

## 支持的打印机型号
- Bambu Lab A1 / A1 Mini
- Bambu Lab P1P / P1S  
- Bambu Lab X1 / X1C