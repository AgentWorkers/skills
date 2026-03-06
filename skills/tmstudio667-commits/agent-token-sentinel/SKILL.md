---
name: agent-token-sentinel
description: "实时成本与配额监控工具，专为AI代理设计。该工具可监控API使用情况，并自动终止递归循环或过度复杂的推理过程，从而保护您的资金安全。专为2026年的“代理经济”（Agent Economy）环境进行了优化。"
metadata:
  {
    "openclaw": { "emoji": "💰" },
    "author": "System Architect Zero",
    "category": "Security"
  }
---
# Agent Token Sentinel

保护您的资金安全，防止人工智能逻辑失控。该工具充当“金融断路器”，通过实时监控代币消耗率和会话配额，确保您的代理工作流程始终在预算范围内。

## 主要功能
- **循环检测**：自动终止那些重复执行任务但毫无进展的进程。
- **预算监控器**：为每次会话的 USD/Token 消耗设置严格限制。
- **警报系统**：在您超出配额前发送高优先级通知。

## 使用方法
```bash
npx openclaw skill run agent-token-sentinel --cap 5.00
```

## 架构师备注
在 2026 年，效率不再仅仅是优化手段；它是生存的关键。