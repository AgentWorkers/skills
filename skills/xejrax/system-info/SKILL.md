---
name: system-info
description: "快速系统诊断：CPU、内存、磁盘以及系统运行时间"
metadata:
  {
    "openclaw":
      {
        "emoji": "💻",
        "requires": { "bins": ["free"] },
        "install": [],
      },
  }
---

# 系统信息

提供关于CPU、内存、磁盘和运行时间的快速系统诊断。使用的是标准Linux工具，这些工具在系统中始终可用。

## 命令

```bash
# Show all system info (CPU, memory, disk, uptime)
system-info

# Show CPU information
system-info cpu

# Show memory usage
system-info mem

# Show disk usage
system-info disk

# Show system uptime
system-info uptime
```

## 安装

无需安装。`free`及相关工具在系统中已经存在。