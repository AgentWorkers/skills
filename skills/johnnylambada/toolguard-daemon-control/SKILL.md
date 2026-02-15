---
name: toolguard-daemon-control
description: 将长时间运行的进程作为 macOS 的 launchd 服务来管理。当需要启动、停止、重启、检查状态或管理后台服务/守护进程时，可以使用该功能。它负责处理 launchd 的 plist 文件创建、服务生命周期的管理以及日志访问相关事宜。对于任何需要在当前会话结束后仍持续运行的进程，建议使用此方法而非传统的后台执行方式。
---

# toolguard-daemon-control

该工具用于将任何可执行文件作为持久的 macOS launchd 用户代理来管理。

## 概述

这些服务以 `~/Library/LaunchAgents/ai.toolguard.<name>.plist` 的格式安装，并作为用户级别的启动代理运行。当服务出现故障时，它们会自动重启，并将日志记录到 `~/Library/Logs/toolguard/` 目录中。

## 脚本

所有脚本都位于该工具的 `scripts/` 目录中。可以使用 `bash` 来执行这些脚本。

### install.sh — 创建并启动服务

```bash
bash scripts/install.sh <service-name> <command> [args...] [--workdir <dir>] [--env KEY=VALUE ...]
```

- `service-name`：服务的简短标识符（例如 `toolguard-proxy`），用于 plist 文件名和日志路径中。
- `command`：可执行文件的绝对路径。
- `args`：传递给命令的参数。
- `--workdir <dir>`：进程的工作目录（默认为 `$HOME`）。
- `--env KEY=VALUE`：环境变量（可重复设置）。

示例：
```bash
bash scripts/install.sh toolguard-proxy /usr/local/go/bin/go run ./cmd/server --config toolguard.dev.yaml --workdir ~/Documents/toolguard
```

### uninstall.sh — 停止并删除服务

```bash
bash scripts/uninstall.sh <service-name>
```

该脚本会停止服务并删除对应的 plist 文件，同时保留日志记录。

### status.sh — 检查服务状态

```bash
bash scripts/status.sh [service-name]
```

如果不提供参数，该脚本会列出所有 `ai.toolguard.*` 服务；如果提供了服务名称，则会显示该服务的详细状态。

### logs.sh — 查看服务日志

```bash
bash scripts/logs.sh <service-name> [--follow] [--lines <n>]
```

该脚本会显示标准输出（stdout）和标准错误（stderr）日志，默认显示最后 50 行。

### list.sh — 列出所有受管理的服务

```bash
bash scripts/list.sh
```

该脚本会列出所有已安装的 `ai.toolguard.*` 服务及其运行状态。

## 注意事项

- 服务以当前用户身份运行（无需使用 sudo）。
- 服务在崩溃时会自动重启（`KeepAlive = true`）。
- 要运行 Go 项目，请使用编译后的二进制文件路径，或者将其封装在 shell 脚本中执行——launchd 不支持直接使用 `go run` 命令。请先使用 `go build` 编译项目，然后再运行二进制文件。
- 日志目录：`~/Library/Logs/toolguard/<service-name>/`
- plist 文件位置：`~/Library/LaunchAgents/ai.toolguard.<service-name>.plist`