---
name: gateway-monitor-macos
description: 在 macOS 上使用 LaunchAgent 和 watchdog 安装并运行本地 OpenClaw Gateway Monitor 堆栈。该工具适用于设置、修复或验证 gateway-monitor 服务，支持一键安装/卸载/查看状态，以及自动通过 launchctl 进行服务注册。
---
# Gateway Monitor (macOS)

当您需要在 macOS 上重现 gateway monitor 和 watchdog 的安装过程时，请运行此技能。

## 安装

运行：

```bash
bash scripts/install.sh
```

安装过程包括：
- 将 monitor 相关文件复制到 `~/.openclaw/tools/gateway-monitor` 目录中。
- 安装或更新以下 LaunchAgents：
  - `ai.openclaw.gateway-monitor`
  - `ai.openclaw.gateway-watchdog`
- 使用 `launchctl` 重新加载这两个服务。
- 验证 monitor 的 API 运行状态（通过访问 `/api/summary`）。

## 查看状态

运行：

```bash
bash scripts/status.sh
```

## 卸载

运行：

```bash
bash scripts/uninstall.sh
```

## 注意事项：
- 本技能仅适用于 macOS 的 `launchd` 服务管理机制。
- 安装过程是幂等的（即多次运行不会导致问题），因此可以放心重复执行。
- 在覆盖现有配置文件之前，系统会将备份文件保存到 `~/.openclaw/config-backups` 目录中。