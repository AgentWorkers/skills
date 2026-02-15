---
name: mactop
description: |
  Retrieve real-time hardware metrics from Apple Silicon Macs using mactop's TOON format.
  Provides CPU, RAM, GPU, power, thermal, network, disk I/O, and Thunderbolt bus information.
  Use when the user wants system stats, hardware monitoring, or performance metrics on Apple Silicon Macs.
---

# Mactop 技能

以无头（headless）TOON 模式运行 mactop，并解析输出以获取硬件指标。

## 先决条件

- **已安装 mactop**：`brew install mactop`
- **PATH 包含 /usr/sbin**：这是访问 sysctl 所必需的

## 使用方法

### 获取完整指标

```bash
mactop --format toon --headless --count 1
```

### 解析关键指标

**CPU 使用率：**
```bash
mactop --format toon --headless --count 1 | grep "^cpu_usage:" | awk '{print $2}'
```

**内存（已使用/总容量，GB）：**
```bash
mactop --format toon --headless --count 1 | grep -E "^  (Used|Total):" | awk '{printf "%.1f", $2/1073741824}'
```

**GPU 使用率：**
```bash
mactop --format toon --headless --count 1 | grep "^gpu_usage:" | awk '{print $2}'
```

**功耗（总功耗/CPU 功耗/GPU 功耗）：**
```bash
mactop --format toon --headless --count 1 | grep -E "^  (TotalPower|CPUPower|GPUPower):" | awk '{print $2}'
```

**温度状态：**
```bash
mactop --format toon --headless --count 1 | grep "^thermal_state:" | awk '{print $2}'
```

**温度：**
```bash
mactop --format toon --headless --count 1 | grep "^  SocTemp:" | awk '{print $2}'
```

**芯片信息：**
```bash
mactop --format toon --headless --count 1 | grep "^  Name:" | awk '{print $2}'
```

**网络 I/O（字节/秒）：**
```bash
mactop --format toon --headless --count 1 | grep -E "^(  InBytesPerSec|  OutBytesPerSec):" | awk '{print $2}'
```

**Thunderbolt 总线：**
```bash
mactop --format toon --headless --count 1 | grep "^    Name:" | awk '{print $2}'
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `--count N` | 样本数量（默认值：1） |
| `--interval MS` | 样本间隔（以毫秒为单位）（默认值：1000） |

## TOON 格式

```
timestamp: "2026-01-25T20:00:00-07:00"
soc_metrics:
  CPUPower: 0.15
  GPUPower: 0.02
  TotalPower: 8.5
  SocTemp: 42.3
memory:
  Total: 25769803776
  Used: 14852408320
  Available: 10917395456
cpu_usage: 5.2
gpu_usage: 1.8
thermal_state: Normal
system_info:
  Name: Apple M4 Pro
  CoreCount: 12
```

## 响应示例

以易于阅读的格式显示指标：

```
┌─ Apple M4 Pro ──────────────────────┐
│ CPU:   5.2%  |  RAM: 13.8/24.0 GB  │
│ GPU:   1.8%  |  Power: 8.5W total  │
│ Thermal: Normal  |  SoC: 42.3°C    │
└─────────────────────────────────────┘
```

## 故障排除

- 如果出现 “sysctl not found” 的错误，请将 `/usr/sbin` 添加到 PATH 环境变量中。
- 如果没有输出，请确认 mactop 已正确安装：`which mactop`