---
name: ping-beads
description: "验证 bead 守护进程是否正在运行且能够正常响应请求。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🫘",
        "requires": { "bins": ["bd"] },
        "install": [],
      },
  }
---

# Ping Beads

用于验证 bead 守护进程是否正常运行且能够响应请求。通过检查 `bd.sock` 套接字来确认 bead 守护进程（`bd`）正在运行并接受连接。

## 命令

```bash
# Check if the bead daemon is alive (checks bd.sock)
ping-beads

# Show detailed bead daemon status
ping-beads status
```

## 安装

无需安装。`bd` 应该已经包含在 beads 系统的 PATH 环境变量中。