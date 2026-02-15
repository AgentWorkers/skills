---
name: log-tail
description: "从 systemd 日志中流式读取最近的日志记录"
metadata:
  {
    "openclaw":
      {
        "emoji": "📜",
        "requires": { "bins": ["journalctl"] },
        "install": [],
      },
  }
---

# Log Tail

从 systemd 日志中流式显示最近的日志记录。可以按服务单元、日志行数进行筛选，并可选择实时查看日志。

## 命令

```bash
# Show recent journal logs (default: 50 lines)
log-tail [--unit <service>] [--lines 50]

# Follow logs for a specific service in real time
log-tail --follow <service>
```

## 安装

无需安装。`journalctl` 已经存在于基于 systemd 的系统中（如 Bazzite/Fedora）。