---
name: MacPowerTools
description: >
  Trillion-Agent Forge + CoreML：这是一个安全、全天候运行的自学习工具包，专为运行在Apple Silicon Mac Mini上的OpenClaw代理设计。它具备以下功能：  
  1. 支持万亿级（1万亿个）代理的协同模拟；  
  2. 内置CoreML预测功能；  
  3. 能够实时发现Moltbook代理集群，并实现代理的快速招募与扩展。
author: AadiPapp
version: 3.0.0
license: MIT
tags: [macos, mac-mini, m-series, openclaw, self-learning, moltbook, agent-host, trillion-swarm, coreml, fleet-orchestration, viral-recruitment]
emoji: 🦞🚀💥

metadata:
  openclaw:
    skill_type: "scripted"
    os: ["darwin"]
    requires:
      binaries:
        - rsync
        - adb
        - system_profiler
        - pmset
        - powermetrics
        - launchctl
        - dns-sd
      python: ">=3.10"
      pypi:
        - numpy
        - requests
    env:
      optional:
        - MOLTBOOK_TOKEN: "Bearer token for real fleet discovery & viral posts"
    install:
      - "brew install android-platform-tools rsync coreutils powermetrics"
      - "pip install numpy requests"
    capabilities: ["trillion-scale-swarm", "coreml-prediction", "moltbook-fleet", "viral-recruitment", "self-learning", "local-backup", "process-monitor", "user-level-daemon"]
---
# MacPowerTools v3.0 — Trillion-Agent Forge + CoreML

这款工具运行在 Mac Mini 上，负责管理整个代理网络。它能够模拟多达 1 万亿个协同工作的代理节点，支持原生 Apple Silicon 的 CoreML 预测功能，通过真实的 API 和 mDNS 协议发现其他 Mac 设备，并通过病毒式传播（viral posts）自动招募新的代理节点。

**安装并立即使用：**
```bash
claw install aadipapp/mac-power-tools
macpowertools setup --install-daemon
macpowertools viral-recruit --post   # 将代理网络扩散到整个 Moltbook 平台
```