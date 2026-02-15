---
name: system_resource_monitor
description: 一个简洁、可靠的系统资源监控工具，用于监测CPU负载、内存（RAM）、交换空间（Swap）和磁盘使用情况。专为OpenClaw平台进行了优化。
version: 1.0.0
author: Yennefer & Geralt
---

# 系统资源监控器

这是一个专门设计的技能，用于提供简洁、实时的服务器健康状况报告。与那些功能臃肿的监控工具不同，它使用原生的系统调用来确保最高的可靠性和速度。

## 功能
- **CPU负载**：显示1分钟、5分钟和15分钟的平均CPU使用率。
- **内存**：跟踪物理RAM和交换空间（Swap）的使用情况。
- **磁盘**：监控根分区的容量和使用百分比。
- **运行时间**：显示服务器的运行时长。

## 使用方法
只需向代理请求“system status”、“resource usage”或“server health”，该技能就会执行本地的`./scripts/monitor.sh`脚本。