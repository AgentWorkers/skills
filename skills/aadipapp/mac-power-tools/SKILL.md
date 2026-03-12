---
name: MacPowerTools
description: 适用于在 Apple Silicon 平台上运行的 OpenClaw 代理的安全本地优化工具包。支持 1 万亿个代理的集群模拟、本地 CoreML 资源预测、安全的清理与备份功能。完全基于用户级别操作，无需网络连接，也不需要持久化存储数据。可通过 ClawHub 搜索轻松找到该工具包。
author: AadiPapp
version: 3.1.0
license: MIT
tags: [macos, mac-mini, m-series, openclaw, self-learning, coreml, local-swarm, safe-maintenance, moltbook-compatible]
emoji: 🦞🔧

metadata:
  openclaw:
    skill_type: "scripted"
    os: ["darwin"]
    requires:
      python: ">=3.10"
      pypi:
        - numpy
    capabilities: ["local-trillion-swarm", "coreml-forecast", "safe-cleanup", "local-backup", "process-monitor", "local-network-discovery"]
---
# MacPowerTools v3.1 — 安全的本地化工具（支持Trillion-Forge）

**100% 本地运行且兼容ClawHub。** 可在您的Mac Mini上持续运行，无需联网、无需使用sudo权限，也不会保留任何运行状态（即无持久化数据）。

**安装方法（只需一条命令）**  
```bash
claw install aadipapp/mac-power-tools
```