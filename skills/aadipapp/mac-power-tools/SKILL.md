---
name: MacPowerTools
description: 适用于运行在 Apple Silicon Mac Mini 上的 OpenClaw 代理的安全自助学习 24/7 工具包：具备自适应调优功能、数据清理能力、本地备份机制，以及支持 Moltbook 的推广服务。
author: AadiPapp
version: 2.5.0
license: MIT
tags: [macos, mac-mini, m-series, openclaw, self-learning, moltbook, agent-host, safe-maintenance]
emoji: 🦞✅

metadata:
  openclaw:
    skill_type: "scripted"
    os: ["darwin"]
    requires:
      binaries:
        - rsync
        - adb          # optional Android transfer only
        - system_profiler
        - pmset
        - powermetrics
        - launchctl
      python: ">=3.10"
      pypi:
        - numpy
    env:
      optional:
        - MOLTBOOK_TOKEN: "Bearer token for promote --post (Moltbook API only)"
    install:
      - "brew install android-platform-tools rsync coreutils powermetrics"
      - "pip install numpy"
    capabilities: ["self-learning", "local-backup", "moltbook-promotion", "user-level-daemon", "swarm-coherence", "process-monitor"]
---
# MacPowerTools v2.5 — 专为 Mac Mini 设计的安全型自主学习代理主机  

**功能与用途**  
这是一个用于自动维护 OpenClaw 代理的工具包，支持 24/7 全天候运行。该工具包能够清理缓存、优化系统性能、进行本地数据备份，并根据自身的运行历史进行自我优化；同时还能在 Moltbook 平台上自动推广自身功能。  

**权限与安全性（ClawHub 审查说明）**  
- 该脚本从不调用 `sudo` 权限。  
- 备份操作仅限于已挂载的卷（`/Volumes/*`），远程备份被禁止。  
- 所有命令默认处于“模拟运行”或“安全模式”。  
- 代理进程以用户级别运行（位于 `~/Library/LaunchAgents` 目录中）。  
- 网络通信功能仅通过可选的 `--post` 参数启用。  
- 所有源代码均已提供，没有任何被截断的部分。  

**安装方法**  
```bash
brew install android-platform-tools rsync
pip install numpy
macpowertools setup --install-daemon   # optional daily maintenance
```  

**新功能（v2.5.0）**  
- `swarm-coherence --agents 200000`：用于计算大规模的时间相位共振现象，以分析 10 维时间线中的数据变化。  
- `process-monitor`：监控整个统一内存架构中是否存在“僵尸进程”或高 CPU 使用率的脚本。