---
name: pi-health
description: **Raspberry Pi 健康监测工具**  
该工具可用于检查 Raspberry Pi 的各项运行状态：  
- CPU 温度  
- 动态调频（throttling）状态  
- 电压水平  
- 内存/磁盘使用情况  
- 风扇转速（RPM）  
- 过频检测  
- 电源问题  

适用于监控 Raspberry Pi 的整体运行状况、诊断因高温导致的性能下降、检测电压是否过低，以及验证系统的稳定性。  
支持以下型号的 Raspberry Pi：Pi 3/4/5，以及基于 arm64/armhf 架构的系统。
---

# Raspberry Pi 系统健康检查

运行健康检查脚本：

```bash
bash scripts/health.sh
```

## 检查项目

| 检查项 | 来源           | 警告等级 | 严重等级 |
|-------|---------------|---------|----------|
| CPU 温度 | thermal_zone0     | >70°C   | >80°C   |
| 节能策略 | vcgencmd get_throttled | 任何节能策略被启用 | 电压过低 |
| 电压     | vcgencmd measure_volts | —      | —      |
| 内存使用率 | free -m        | >75%    | >90%    |
| 磁盘空间 | df /           | >75%    | >90%    |
| CPU 频率   | cpufreq sysfs     | —      | —      |
| 平均负载   | /proc/loadavg     | >nCPU   | >2×nCPU   |
| 风扇状态 | hwmon sysfs     | —      | —      |
| 超频设置 | config.txt       | 检测到超频   | —      |
| 电源状态 | dmesg          | —      | 电压过低 |

## 返回代码

- `0` — 系统健康（所有检查项均通过）
- `1` — 存在警告（非严重问题）
- `2` — 存在严重问题（需要立即处理）

## 所需软件

- Raspberry Pi 操作系统（Bookworm 或更高版本）
- `vcgencmd`（可选，但推荐使用——包含在 `libraspberrypi-bin` 中）
- `bc`（Raspberry Pi 操作系统的标准工具）

**注：** 本脚本不依赖于任何外部依赖项或 API 密钥。