---
name: auto-watchdog
description: "OpenClaw代理的自动健康监控与自我修复功能：监控cron作业、进程运行状态、磁盘使用情况以及API的运行状况。当服务崩溃时，系统会自动重启它们，并在出现问题时发出警报。设置完成后即可无需再进行额外操作。"
version: 1.0.0
---
# 自动监控工具 🐕

您的 OpenClaw 系统全天候运行，但谁来监控这些运行的进程呢？

Auto-Watchdog 会默默地监控所有系统组件，并在发现问题时自动进行修复。只有当真正出现严重问题时，您才会收到通知。

## 主要功能

### 1. Cron 任务监控器
- 每次系统心跳检查所有 Cron 任务：
  - 如果连续出错次数超过 0 次 → 立即发出警报
  - 如果任务未按预期运行 → 发出警报
  - 如果被禁用的任务越来越多 → 提出清理建议

### 2. 进程守护者
- 通过日志更新频率来监控关键进程（而不仅仅是进程 ID）：
  - 如果日志文件在 X 分钟内未更新 → 终止并重启进程
- 适用于所有 Node.js 进程
- 可为每个进程配置不同的阈值

### 3. 磁盘监控器
- 监控日志文件是否过大 → 自动旋转日志文件
- 提示工作区空间使用情况
- 清理临时文件

### 4. 网关监控器
- 每次系统心跳检查 OpenClaw 网关的状态
- 如果网关故障 → 通过任务调度器或 systemd 自动重启

### 5. 默认情况下保持静默
- 如果一切正常 → 不显示任何提示信息（状态码：HEARTBEAT_OK）
- 发现问题 → 向您的聊天工具发送针对性警报
- 避免发送不必要的垃圾信息

## 设置方法

### 在 HEARTBEAT.md 文件中添加以下代码：

```markdown
## 🔍 Health Check (silent = good)

### Crons
- `cron list` → check consecutiveErrors > 0 → alert
- Frequent crons not running >2 hours → alert

### Processes
- Check [your process] log freshness < [X] minutes
- If stale → restart and alert

### Gateway
- `openclaw gateway status` → alert if down

### Disk
- Check log sizes > 10MB → rotate
- Check workspace size > 1GB → alert
```

### 对于 Windows（使用任务调度器）：
创建一个 VBS 装饰器以实现无延迟的执行：

```vbs
' guardian-silent.vbs — zero flash process monitor
Set oShell = CreateObject("WScript.Shell")
oShell.Run "powershell.exe -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File ""C:\path\to\guardian.ps1""", 0, True
```

将该脚本注册为每 1-5 分钟执行一次的任务。

### 对于 Linux（使用 systemd）：
```bash
# /etc/systemd/system/openclaw-watchdog.service
[Service]
ExecStart=/usr/bin/node /path/to/guardian.js
Restart=always
RestartSec=60
```

## 设计理念

- 通过日志的更新频率来监控进程状态，而不仅仅是进程 ID。
- 一个进程可能看似“正在运行”，但实际上可能处于停滞状态（检查日志的时间戳即可判断）。
- 先修复问题，再发出警报。
- 如果可以自动重启进程，就立即执行重启操作；只有需要人工干预的问题才会被报告。
- 保持静默意味着系统运行正常；没有异常情况就无需通知。

## 经过生产环境测试
该工具专为全天候运行的自动化交易系统设计，适用于以下场景：
- 5 个竞争性的 AI 模块
- 20 多个 Cron 任务
- 战略研究工具每天运行 23 小时
- 在数周的运行期间从未出现过任何停机情况