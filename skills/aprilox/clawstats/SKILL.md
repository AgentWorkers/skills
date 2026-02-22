---
name: clawstats
description: Comprehensive system monitoring for OpenClaw: CPU, RAM, Disk, and Processes.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["free","df","top","ps"]},"install":[]}}
---
# 📊 ClawStat 技能

这是一个专为 OpenClaw 代理设计的全面系统监控技能，用于追踪服务器的健康状况和性能。

## 🚀 功能
- **CPU 和 RAM**：实时使用情况统计。
- **磁盘**：监控根分区的可用空间。
- **温度**：通过 `sensors` 或 `thermal_zone` 监控 CPU 温度。
- **顶级进程**：识别占用大量资源的应用程序。
- **负载平均值**：检查系统随时间的变化情况。

## 🛠️ 工具
该技能提供了一个多功能脚本：
- `monitor.sh [cpu|ram|disk|temp|top|all]`：获取特定或完整的系统统计数据。

## 📦 安装（手动）
1. 将此目录克隆或复制到 `~/.openclaw/workspace/skills/clawstats`。
2. 确保 `monitor.sh` 可执行：`chmod +x monitor.sh`。
3. （可选）安装 `lm-sensors` 以支持温度监控。

## 📖 使用示例
- `monitor.sh all`：获取完整的系统健康报告。
- `monitor.sh top`：查看哪些进程正在拖慢系统运行速度。

---
*由 Chela 🫐 和 Aprilox 创建*