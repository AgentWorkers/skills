---
name: beestat
description: 通过 Beestat API 查询 ecobee 温控器的数据，包括温度、湿度、空气质量（二氧化碳、挥发性有机化合物）、传感器信息以及 HVAC 系统的运行状态。当用户询问家庭温度、温控器状态、空气质量或供暖/制冷系统的使用情况时，可以使用此功能。
homepage: https://beestat.io
metadata:
  clawdbot:
    emoji: "🌡️"
    requires:
      bins: ["beestat"]
      env: ["BEESTAT_API_KEY"]
---

# Beestat CLI

Beestat CLI 是用于访问 Beestat API（ecobee 温控器分析服务）的命令行工具，可以查询温度、湿度、空气质量以及 HVAC 系统的运行状态。

## 安装

```bash
npm install -g beestat-cli
```

## 设置

1. 在 [beestat.io](https://beestat.io) 上创建账户，并将您的 ecobee 温控器与之关联。
2. 发送电子邮件至 contact@beestat.io，附上您的温控器序列号，以获取 API 密钥。
3. 设置环境变量：`export BEESTAT_API_KEY="your-key"`。

## 命令

### 查看系统状态

```bash
beestat status             # Current temps, humidity, setpoints, weather
beestat status --json
```

### 查看传感器数据

```bash
beestat sensors            # All sensors with temperature and occupancy
beestat sensors --json
```

### 查看空气质量

```bash
beestat air-quality        # CO2, VOC, and air quality score
beestat aq                 # Short alias
beestat aq --json
```

**注意：** 该功能需要使用 ecobee Smart Thermostat Premium 版本（该版本内置了空气质量传感器）。

**二氧化碳浓度：**
- < 800 ppm：优秀
- 800-1000 ppm：良好
- 1000-1500 ppm：一般（建议开窗通风）
- > 1500 ppm：较高（请立即通风！）

**挥发性有机化合物（VOC）浓度：**
- < 0.5 ppm：优秀
- 0.5-1.0 ppm：良好
- 1.0-3.0 ppm：一般
- > 3.0 ppm：较高

### 查看温控器信息

```bash
beestat thermostats        # Model info, HVAC details
beestat thermostats --json
```

### 查看系统运行统计信息

```bash
beestat summary            # Runtime history (default 7 days)
beestat summary --days 14  # Last 14 days
beestat summary --json
```

### 强制同步数据

```bash
beestat sync               # Force sync with ecobee
```

## 使用示例

**用户：** “家里的温度是多少？”
```bash
beestat status
```

**用户：** “空气质量怎么样？”
```bash
beestat aq
```

**用户：** **卧室里有人吗？**
```bash
beestat sensors
```

**用户：** **这周我们为房子供暖花了多少钱？**
```bash
beestat summary --days 7
```

**用户：** **我们有哪些类型的温控器？**
```bash
beestat thermostats
```

## 注意事项

- 空气质量数据来源于 ecobee 系统的运行数据，而非温控器的传感器数据。
- 所有命令都支持使用 `--json` 参数进行脚本编写或自动化操作。
- 如果数据更新不及时，可以使用 `beestat sync` 命令强制同步数据。