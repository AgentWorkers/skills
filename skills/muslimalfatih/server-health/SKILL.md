---
name: server-health
description: 全面的服务器健康监控功能，可显示系统统计信息、主要进程运行状态、OpenClaw网关的状态以及正在运行的服务。非常适合通过Telegram或命令行界面（CLI）快速进行服务器健康检查。
---

# 服务器健康检查功能

提供快速的服务器监控服务，包括系统统计信息、进程状态、OpenClaw网关信息以及正在运行的服务。

## 使用方法

**标准视图：**
```bash
./server-health.sh
```

**详细视图（包含临时文件使用情况、网络流量、交换空间使用情况、I/O操作信息）：**
```bash
./server-health.sh --verbose
```

**JSON格式输出（适用于自动化脚本）：**
```bash
./server-health.sh --json
```

**仅显示警告/错误信息：**
```bash
./server-health.sh --alerts
```

## 功能展示

### 🔴 始终显示的内容
- 系统统计信息（CPU使用率、内存使用率、磁盘使用情况、服务器运行时间）
- 占用CPU或内存资源最多的前3-5个进程
- OpenClaw网关的状态及配置信息
- 正在运行的服务（如Docker容器、PostgreSQL数据库等）

### 🟡 条件性显示的内容
- 当磁盘使用率超过90%、内存使用率超过80%或CPU使用率超过90%时触发警报
- 交换空间的使用情况（如果系统启用了交换空间）

### 🟢 仅显示详细信息的内容
- 系统温度（如果安装了温度传感器）
- 网络流量数据
- 磁盘I/O操作详细信息
- 各服务的详细运行状态

## 示例输出**
```
🖥️ SERVER HEALTH
━━━━━━━━━━━━━━━━━━━━

💻 SYSTEM
CPU: ████░░░░░░ 42% (Load: 1.2, 0.8, 0.5)
RAM: ██████░░░░ 1.4GB/8GB (18%)
DISK: ████░░░░░░ 45GB/100GB (45%)
UP: ⏱️ 5d 3h

🔄 TOP PROCESSES
node         35%    450MB
postgres     12%    280MB
openclaw      8%    180MB

⚡ OPENCLAW GATEWAY
Status: ✅ Running (PID: 1639125)
Uptime: 2d 5h | Port: 18789 | v2026.2.6-3

🤖 MODEL CONFIG
Primary: claude-sonnet-4-5
Context: 43k/128k (33%) | 574↓ 182↑ tokens
Fallbacks: glm-4.7 → copilot-sonnet → opus-4-5

📊 SESSIONS
Active: 3 | Heartbeat: 30m | Last: 1m ago

🐳 SERVICES
Docker: ✅ 3 containers
PostgreSQL: ✅ Running
```