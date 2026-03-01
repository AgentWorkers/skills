---
name: bambu
description: 通过 CLI（命令行界面）控制 Bambu Lab 的 3D 打印机（H2D、X1C、P1S、A1）。支持打印管理、AMS 线材控制、温度调节、风扇控制、灯光控制、校准功能以及文件管理，并提供实时监控功能。适用于操作 3D 打印机、启动打印任务、监控打印进度、管理线材使用情况或排查打印机故障的场景。
---
# Bambu Lab 3D打印机控制

通过MQTT和FTP实现对Bambu Lab打印机的完全控制。该控制方式不依赖于任何特定的代理（agent），仅支持本地连接，不涉及云服务。

## 前提条件

- 打印机必须处于**开发者模式**（Settings → LAN Only → Enable Developer Mode）。
- 需要获取打印机的IP地址、序列号以及LAN访问密码（这些信息可以从打印机的触摸屏上获取）。
- 确保全局安装了`@versatly/bambu` CLI工具（通过`npm i -g @versatly/bambu`命令安装）。

## 设置

```bash
bambu setup <ip> <serial> <access_code>
bambu ping  # verify connection
```

配置信息存储在`~/.bambu/config.json`文件中。

## 分步操作指南

仅加载当前任务所需的功能：

### 第1级：状态检查（最常用）
```bash
bambu status          # full status overview
bambu status --json   # programmatic access
bambu temp            # just temperatures  
bambu ams             # just AMS/filament info
bambu errors          # any active errors
```

### 第2级：打印操作
```bash
# Start a print from SD card
bambu print "filename.3mf"

# Upload and print in one step
bambu job upload-and-print ./my-part.3mf

# Control running print
bambu pause
bambu resume  
bambu stop

# Live monitoring (streams progress)
bambu watch
```

### 第3级：硬件控制
```bash
# Temperature
bambu heat nozzle:220 bed:60
bambu cooldown

# Fans (0-100%)
bambu fan part 80
bambu fan aux 50
bambu fan chamber 30

# Lights
bambu light on
bambu light off

# Movement
bambu home
bambu move x:10 y:20 z:5
bambu gcode "G28"
```

### 第4级：AMS耗材管理
```bash
# Check what's loaded
bambu ams

# Load specific tray (0-3)
bambu load 0
bambu load 2

# Unload current filament
bambu unload
```

### 第5级：文件管理与校准
```bash
# SD card files
bambu files
bambu upload ./part.3mf
bambu delete old-print.3mf

# Calibration
bambu calibrate bed
bambu calibrate vibration
bambu calibrate flow
bambu calibrate all
```

## 常用操作流程

### “打印此文件”
```bash
bambu job upload-and-print ./part.3mf
bambu watch  # monitor until done
```

### “检查打印机是否准备就绪”
```bash
bambu status --json | jq '.gcode_state'
# IDLE = ready, RUNNING = busy, FAILED = needs attention
```

### “当前加载了哪种耗材？”
```bash
bambu ams --json
```

### “为PLA材料预热”
```bash
bambu heat nozzle:210 bed:60
```

### “为ABS材料预热”
```bash
bambu heat nozzle:260 bed:100
```

### “出现故障”
```bash
bambu errors --json   # check HMS error codes
bambu status          # full state overview
```

### “完成操作并关闭打印机”
```bash
bambu cooldown
bambu light off
```

## 输出格式

- **默认格式**：易于人类阅读的文本格式，消息前缀包含表情符号，内容简洁紧凑，适用于聊天机器人（LLM）的显示窗口。
- **--json格式**：原始的JSON格式，适用于程序化处理。可以使用`jq`工具提取所需数据。

## 安全注意事项

- `bambu status`、`bambu temp`、`bambu ams`、`bambu errors`、`bambu version`、`bambu files`等命令仅用于读取数据，不会对打印机造成任何影响，因此始终是安全的。
- `bambu print`、`bambu stop`、`bambu heat`、`bambu move`、`bambu gcode`等命令会直接控制打印机的物理操作（喷嘴温度可达到200°C以上，请谨慎使用）。
- `bambu calibrate`命令用于移动打印机喷头，请确保打印平台（bed）上没有障碍物。
- `bambu gcode`命令用于发送原始的G代码文件，在使用前请确保了解其含义。

## 故障排除

| 故障类型 | 解决方法 |
|-------|-----|
| 连接超时 | 确保已启用开发者模式，IP地址正确，打印机已开机。 |
| 认证失败 | 请检查LAN访问密码（重新启用开发者模式后密码可能会发生变化）。 |
| FTP连接错误 | 确保使用端口990，并且打印机处于LAN模式下。 |
| 无法获取AMS耗材信息 | 检查AMS耗材是否已连接并被识别；同时查看打印机触摸屏上的信息。 |
| MQTT通信中断 | 可能是由于WiFi信号较弱导致的。请查看`bambu status`中的`wifi_signal`字段。 |