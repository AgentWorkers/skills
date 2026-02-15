---
name: host-ping
description: 通过发送 ping 请求来检测主机（IP：39.106.7.8）是否在线。如果主机处于离线状态，将返回相应的状态信息（如“可达”、“延迟”或“错误”）。
metadata:
  openclaw:
    requires:
      bins: ["ping"]  # Requires the 'ping' command-line tool
    emoji: "🔔"  # Optional: UI icon for the skill
    homepage: "https://example.com/host-ping"  # Optional: Link to more info
    os: ["darwin", "linux", "win32"]  # Supported OS (macOS, Linux, Windows)
    install: []  # No additional installation needed if ping is available
---

## 代理的使用说明

要使用此功能，请对主机 IP 地址 39.106.7.8 执行 `ping` 命令。请通过 shell 来运行该命令：

```bash
ping -c 4 39.106.7.8  # 发送 4 个 ping 数据包（跨平台兼容）
```