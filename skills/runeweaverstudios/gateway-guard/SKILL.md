---
name: gateway-guard
description: Ensures OpenClaw gateway auth consistency and can auto-prompt "continue" when a run error (Unhandled stop reason: error) appears in gateway logs. Use when checking or fixing gateway token/password mismatch, device_token_mismatch errors, or before delegating to sub-agents.
---

# Gateway Guard

## 描述

该工具用于确保 OpenClaw 网关的认证信息保持一致。当网关日志中出现运行错误（未处理的停止原因：“error”）时，它可以自动提示用户“继续”执行后续操作。适用于检查或修复网关令牌/密码不匹配的问题，以及在将任务委托给子代理之前使用。

## 使用方法

- 当用户或系统日志显示“网关认证问题”、“设备令牌不匹配”或“未经授权”等错误时，首先检查网关状态。
- 在运行路由器或 `sessions_spawn`（编排流程）之前，务必先检查网关状态。
- 安装或更新 OpenClaw 后，验证网关配置是否正确。
- 当 TUI（图形用户界面）断开连接或无法正常连接时，修复认证问题并重启网关。
- 如果网关日志中包含“未处理的停止原因：error”这样的错误信息，可以使用 `continue-on-error` 命令（例如通过 LaunchAgent 或 cron 脚本）自动向代理发送继续执行的提示。

### 命令参数说明：

- **status**：检查当前运行的网关认证信息是否与 `openclaw.json` 中的配置一致。如果匹配则输出 0，不匹配则输出 1。
- **ensure**：执行相同的检查；如果发现不匹配且使用了 `--apply` 参数，则使用配置文件中的凭据重启网关。仅当配置中的认证信息缺失或错误时，才会更新 `openclaw.json` 文件中的认证信息（不会覆盖正确的配置）。
- **continue-on-error**：当 `gateway.log` 中出现“未处理的停止原因：error”时，通过 `openclaw agent --message continue --deliver` 命令向代理发送继续执行的提示。可以使用 `--once` 选项仅检查一次并退出，或使用 `--loop` 选项每隔指定时间间隔（`--interval`）检查一次。触发间隔为 90 秒。相关状态信息保存在 `logs/gateway-guard.continue-state.json` 文件中。
- **watch**：这是一个组合型的守护进程（由一个 LaunchAgent 实现）。每次运行时，它会执行以下操作：(1) 使用 `ensure --apply` 命令同步令牌信息，以防止设备令牌不匹配的问题；(2) 显示刚刚发生的错误信息；(3) 再次检查是否需要继续执行任务。**安装方法**：执行 `bash <skill-dir>/scripts/install_watcher.sh`（或 `install_continue_on_error.sh`）命令。该命令会卸载旧的单独的监控脚本，并加载 `com.openclaw.gateway-guard.watcher`，从而让用户只需使用一个守护进程即可完成监控任务。对于需要定期检查网关状态并自动重启的情况（例如每 10 秒检查一次），可以使用单独的 `gateway-watchdog` 工具。

## 行为逻辑

- 该工具会读取 `openclaw.json` 文件中的 `gateway.auth`（令牌或密码）和 `gateway.port` 配置。
- 将这些信息与监听在指定端口的进程进行比较。
- 如果使用了 `ensure --apply` 参数，会通过 `openclaw gateway stop` 命令停止当前网关，然后使用 `openclaw gateway --port N --auth token|password --token|--password SECRET` 命令重启网关。
- 如果配置文件中缺少令牌信息（仅适用于令牌认证模式），则会生成一个新的令牌并写入配置文件；如果配置信息已经正确，则不会进行覆盖。
- 当 `gateway.log` 中包含“未处理的停止原因：error”时，会通过 `openclaw agent --message continue --deliver` 命令向代理发送继续执行的提示。

## JSON 输出格式（用于编排场景）

- **status --json** / **ensure --json**：返回以下信息：`ok`、`secretMatchesConfig`、`running`、`pid`、`reason`、`recommendedAction`、`configPath`、`authMode`、`gatewayPort`。如果配置有问题，`recommendedAction` 会提示“运行 `gateway_guard.py ensure --apply and restart client session”以重启客户端会话。

## 所需环境

- 确保系统中已安装 OpenClaw，并且 `openclaw.json` 文件中包含 `gateway.auth`（认证模式为 `token` 或 `password`）以及 `gateway.port` 配置。
- 需要 `openclaw` CLI 工具，并将其添加到系统的 PATH 环境变量中（用于执行 `ensure --apply` 和 `continue-on-error` 命令）；同时需要 `lsof` 和 `ps`（macOS/Unix 系统）或 `launchctl`（macOS 上使用 LaunchAgent 时）。
- 可选环境变量：`OPENCLAW_HOME`（OpenClaw 的安装目录，默认为 `~/.openclaw`）；`OPENCLAW_BIN`（OpenClaw 可执行文件的路径或名称，默认为 `openclaw`）。