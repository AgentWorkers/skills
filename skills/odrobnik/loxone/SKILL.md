---
name: loxone
version: 1.3.3
homepage: https://github.com/odrobnik/loxone-skill
metadata:
  openclaw:
    emoji: "🏠"
    requires:
      bins: ["python3"]
      python: ["requests", "websockets"]
description: 通过 HTTP API 和实时 WebSocket 来控制和监控 Loxone Miniserver（智能家居设备）。该功能可用于查询房间/设备的状态（如温度、灯光状态），查看实时事件，以及发送安全的控制指令。
---

# Loxone（智能家居）

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 命令
- `python3 scripts/loxone.py rooms`  
- `python3 scripts/loxone.py map`  
- `python3 scripts/loxone.py status "<Room>"`  
- `python3 scripts/loxone.py control "<Room>" "<Control>" on|off`  
- `python3 scripts/loxone_watch.py --room "<Room>" [--changes-only] [--duration <sec>]`  

## 注意事项  
- 默认情况下，这些命令仅具有 **只读** 功能；仅在明确请求时使用控制命令。  
- WebSocket 认证过程可能比较复杂；如果 WebSocket 连接失败，系统会回退到使用 HTTP 请求来获取设备状态。