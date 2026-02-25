---
name: system-watchdog
description: 系统资源监控功能能够检测到浪费资源或行为可疑的进程，并为任何用户提供结构化的 JSON 数据输出。
---
# 系统看门狗（System Watchdog）

该工具用于监控系统资源，并标记出浪费资源或行为可疑的进程。它可以作为独立的 Bash 脚本运行——有关通过 Cron 表达式进行定时监控的设置，请参阅 `openclaw.md`。

## 独立使用（Standalone Usage）

直接运行检查脚本，无需依赖 OpenClaw：

```bash
bash check.sh
```

脚本会将检查结果以 JSON 格式输出到标准输出（stdout）。您可以根据需要自行解析这些数据：可以将输出结果传递给 `jq` 工具进行处理，或者将其集成到您自己的监控系统中。

### 输出格式（Output Format）

```json
{
  "suspicious": true,
  "summary": {
    "ram": "12.3/31.2 GB (39%)",
    "swap": "0.5/8.0 GB (6%)",
    "load": "1.2/0.8/0.6",
    "cores": 8,
    "disk": "120/256 GB (45%)"
  },
  "issues": [
    {
      "type": "high_ram",
      "description": "claude (PID 1234) 4650MB RAM",
      "details": { "pid": 1234, "name": "claude", "cpu_pct": 2.1, "mem_mb": 4650, "elapsed": "3d" }
    }
  ],
  "top_processes": [
    { "pid": 1234, "name": "claude", "cpu_pct": 2.1, "mem_mb": 4650, "elapsed": "3d" }
  ]
}
```

- `suspicious: true` → 至少有一个指标超过了预设的阈值
- `suspicious: false` → 系统运行正常

### 阈值设置（Thresholds）

| 检查项 | 阈值 | 问题类型 |
|-------|-----------|------------|
| 进程内存占用 | > 4096 MB | `high_ram` |
| 进程 CPU 使用率 | > 50% | `high_cpu` |
| 长期未关闭的进程 | 运行时间超过 2 天，且内存占用超过 100 MB 或 CPU 使用率超过 1% | `stale` |
| 磁盘使用率 | root 目录下的磁盘使用率超过 80% | `disk` |

### 常见问题来源（Common Issues）

- `claude` / `codex`：长时间运行的 AI 编程代理程序
- `whisper` / `whisper-server`：消耗大量 GPU 资源或内存的语音转文本服务器
- `python` / `python3`：失控运行的脚本或泄漏的进程
- `node`：持续运行的开发服务器或构建脚本

## 代理流程（针对 AI 代理）（Agent Workflow for AI Agents）

1. 运行 `check.sh` 脚本
2. 解析 JSON 输出结果
3. 如果 `suspicious` 的值为 `false`，则无需采取任何行动（无需生成报告）
4. 如果 `suspicious` 的值为 `true`，则生成简洁的报告并通知用户

### 建议的报告格式（Suggested Report Format）

```
⚠️ System Watchdog Report

📊 System: RAM 12.3/31.2 GB (39%) | Swap 0.5/8.0 GB (6%) | Load 1.2/0.8/0.6
💾 Disk: / 45% (120/256 GB)

🔴 Issues Found:

HIGH RAM — claude (PID 1234)
  CPU: 2.1% | RAM: 4650 MB | Running: 3 days
  → Likely stale, safe to kill

💡 Suggested: kill 1234
```

## 平台说明（Platform Notes）

- **仅适用于 macOS**：`check.sh` 脚本依赖于 `sysctl`、`vm_stat` 以及 macOS 的 `ps` 命令。在 Linux 系统上需要相应地调整这些命令（例如，使用 `free`、`/proc/meminfo` 等工具）。
- **偶尔出现的解析错误**：由于进程扫描过程中的竞争条件（race condition），脚本可能在首次运行时出现解析错误。在报告错误之前，请尝试重新运行脚本一次。