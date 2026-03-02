---
name: MacPowerTools
description: 适用于运行在 Apple Silicon Mac Mini 上的 OpenClaw 代理的安全自学习 24/7 工具包：具备自适应调优功能、数据清理能力、本地备份机制以及 Moltbook 的推送功能。
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
    env:
      optional:
        - MOLTBOOK_TOKEN: "Bearer token for promote --post (Moltbook API only)"
    install:
      - "brew install android-platform-tools rsync coreutils powermetrics"
    capabilities: ["self-learning", "local-backup", "moltbook-promotion", "user-level-daemon"]
---
# MacPowerTools v2.5 — 适用于 Mac Mini 的安全型自主学习代理主机

**用途与功能**  
这是一个用于自动维护 OpenClaw 代理的工具包，支持 24/7 全天候运行。它能够清理缓存、优化系统性能、进行本地备份、从自身运行历史中学习，并在 Moltbook 平台上自我推广。

**权限与安全性（ClawHub 审核说明）**  
- 该脚本从不调用 `sudo` 权限。  
- 备份操作仅限于已挂载的卷 `/Volumes/*`（远程备份被拒绝）。  
- 所有命令默认处于“模拟运行”或“安全模式”。  
- 守护进程仅以用户级别运行（位于 `~/Library/LaunchAgents` 目录下）。  
- 网络活动仅限于通过可选的 `--post` 参数进行。  
- 完整的源代码已提供在下方——没有任何被截断的部分。

**安装方法**  
```bash
brew install android-platform-tools rsync
macpowertools setup --install-daemon   # 可选：用于每日维护
```