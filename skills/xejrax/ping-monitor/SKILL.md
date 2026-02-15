---
name: ping-monitor
description: "针对主机、手机和守护进程的 ICMP 健康检查"
metadata:
  {
    "openclaw":
      {
        "emoji": "🏓",
        "requires": { "bins": ["ping"] },
        "install": [],
      },
  }
---

# Ping 监控工具

该工具用于对主机、手机及后台进程（daemon）进行 ICMP 健康检查，通过标准的 `ping` 工具来验证目标主机的网络可达性。

## 命令

```bash
# Ping a host with default settings
ping-monitor <host>

# Ping a host with a specific count
ping-monitor check <host> --count 3
```

## 安装

无需安装。`ping` 工具已预装在系统中。