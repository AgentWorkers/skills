---
name: gateway-monitor-installer
description: 在 macOS 上，通过 LaunchAgent 安装、更新、运行以及卸载 OpenClaw Gateway Monitor 和 Gateway Watchdog。这些工具可用于实现一键监控功能、自动恢复故障的网关守护进程、检查 launchctl 的运行状态，或卸载相应的监控/守护服务。
---
# Gateway Monitor Installer

请使用捆绑的脚本来执行确定性操作（即每次运行都会产生相同的结果）。

## 运行脚本（Runbook）

1. 安装或更新软件：

```bash
bash scripts/install.sh
```

2. 验证软件状态：

```bash
bash scripts/status.sh
```

3. 清洁卸载软件：

```bash
bash scripts/uninstall.sh
```

## `install.sh` 的功能

- 将监控程序（monitor）和监视器守护进程（watchdog）的二进制文件复制到 `~/.openclaw/tools/gateway-monitor/bin/` 目录中。
- 将 `LaunchAgent` 模板文件生成到 `~/Library/LaunchAgents/` 目录中。
- 备份现有的 `.plist` 配置文件到 `~/.openclaw/config-backups/` 目录中。
- 启动并启用这两个守护进程，并执行启动后的状态检查。

## 相关服务

- `ai.openclaw.gateway-monitor`：监控用户界面服务器（地址：`http://127.0.0.1:18990`）
- `ai.openclaw.gateway-watchdog`：定期执行网关自修复检查。

## 注意事项

- 重新运行 `install.sh` 是安全的（具有幂等性，即多次运行不会产生不同的结果）。
- `watchdog` 脚本依赖于 `/opt/homebrew/bin/openclaw` 路径下的 OpenClaw CLI 工具。
- 如果节点路径不同，请在安装前修改 `assets/bin/gateway-watchdog.sh` 文件中的相关设置。