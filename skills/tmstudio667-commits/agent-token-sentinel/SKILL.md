---
name: agent-token-sentinel
description: "实时成本与配额监控工具，专为AI代理设计。该工具能够监控API的使用情况，并自动终止递归循环或过度的推理操作，从而保护您的资金安全。专为2026年的“代理经济”（Agentic Economy）环境进行了优化。"
metadata:
  {
    "openclaw": { "emoji": "💰" },
    "author": "System Architect Zero",
    "category": "Utility"
  }
---
# 代理令牌哨兵（Agent Token Sentinel）

保护您的资金不受失控的AI逻辑的影响。该功能充当财务“断路器”，确保您的代理工作流程始终在预算范围内运行。

## 主要特性
- **循环检测（Loop Detection）**：终止那些重复执行相同任务但毫无进展的进程。
- **配额管理（Quota Management）**：为每次会话设置令牌使用的上限。
- **成本分析（Cost Analytics）**：提供您AI基础设施的实时盈亏情况。

## 使用方法
```bash
npx openclaw skill run agent-token-sentinel --cap 5.00
```

## 架构师备注
自主性意味着财务上的稳健性。确保您的代理系统能够持续盈利。