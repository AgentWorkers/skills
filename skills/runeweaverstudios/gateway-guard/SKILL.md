---
name: gateway-guard
displayName: Gateway Guard
description: Ensures OpenClaw gateway auth consistency and can auto-prompt "continue" when a run error (Unhandled stop reason: error) appears in gateway logs. Use when checking or fixing gateway token/password mismatch, device_token_mismatch errors, or before delegating to sub-agents.
---

# Gateway Guard

## 描述

本工具用于确保 OpenClaw 网关的身份验证一致性。当网关日志中出现运行错误（未处理的停止原因：“error”）时，它能够自动提示用户“继续”操作。适用于检查或修复网关令牌/密码不匹配的问题，或在将任务委托给子代理之前使用。

## 功能

- 确保 OpenClaw 网关的身份验证信息与 `openclaw.json` 文件保持一致。
- 当用户或代理遇到网关身份验证问题、设备令牌不匹配的情况时，或需要在委托任务给子代理之前验证网关是否使用正确的令牌/密码时，本工具非常有用。

## 元数据

- 本工具在 `_meta.json` 文件中配置为 `always: false`，这意味着它不会在每次代理运行时都被自动执行。只有当需要时（例如，在将任务委托给子代理之前），orchestrator 会触发该工具的执行。
- **可选的持久化功能（LaunchAgent）**：只有在运行安装脚本时才会被启用。具体安装方法请参见“安装前”部分的说明。

## 安装前注意事项

- **备份 `openclaw.json`**：安装脚本可能会添加或修改 `gateway.auth`（令牌/密码）字段。在运行 `ensure --apply` 命令之前，请先备份该文件。
- **先进行只读测试**：先运行 `python3 scripts/gateway_guard.py status --json` 和 `python3 scripts/gateway_guard.py ensure --json`（不带 `--apply` 参数），以了解该工具在允许重启或修改配置之前的行为。
- **确认自动发送“继续”消息的可行性**：如果网关日志中出现运行错误，watcher 可以通过 `openclaw agent --message continue --deliver` 来发送“继续”消息。请确保您的环境支持这种操作。
- **LaunchAgent 是可选的**：只有在使用 `install_watcher.sh` 脚本时，才会安装持久化功能（每隔 30 秒检查一次网关状态）。安装脚本会将所需的 plist 文件复制到 `~/Library/LaunchAgents` 目录，并通过 `launchctl load` 命令启动该服务。这些 plist 文件包含在 `scripts/com.openclaw.gateway-guard.watcher.plist` 和 `scripts/com.openclaw.gateway-guard.continue-on-error.plist` 中。请确保在安装前 `OPENCLAW_HOME` 和 `OPENCLAW_BIN` 的路径设置正确。
- 如果不确定是否需要该工具，请先在非生产环境中进行测试。

## 包含的文件

- `scripts/gateway_guard.py`：主要脚本，用于检查网关状态、执行身份验证验证以及处理错误。
- `scripts/install_watcher.sh`：用于安装用于同步令牌信息和在出现错误时发送“继续”消息的 LaunchAgent。
- `scripts/install_continue_on_error.sh`：用于引导安装 `install_watcher.sh` 脚本。
- `scripts/com.openclaw.gateway-guard.watcher.plist`：LaunchAgent 的 plist 配置文件。
- `scripts/com.openclaw.gateway-guard.continue-on-error.plist`：旧版本的 plist 文件（可选，安装时会替换为新的版本）。

## 使用方法

- 当用户或日志显示“网关身份验证问题”、“设备令牌不匹配”或“未经授权”等错误时，首先检查网关状态。
- 在运行路由器或 `sessions_spawn`（orchestrator 流程）之前，先验证网关状态。
- 安装或更新 OpenClaw 后，确认网关配置是否正确。
- 当 TUI 连接失败时，修复身份验证问题并重启网关。
- 当出现运行错误（未处理的停止原因：“error”）时，通过 `continue-on-error --loop` 命令（可以通过 LaunchAgent 或 cron 定时任务）自动向代理发送“继续”消息。

### 主要脚本功能

- **status**：检查当前运行的网关身份验证信息是否与 `openclaw.json` 中的配置一致。如果一致则返回 0，否则返回 1。
- **ensure**：执行相同的检查；如果发现不匹配，并且使用了 `--apply` 参数，则使用配置中的凭据重启网关。仅在 `gateway.auth` 信息缺失或错误时才更新 `openclaw.json` 文件。使用 `--wait` 参数可等待网关端口启动（最长 30 秒），以便客户端能够立即连接。
- **ensure_gateway_then.sh**：自动检测并连接网关（如果需要则启动网关，等待端口开放后执行用户指定的命令。例如：`ensure_gateway_then.sh openclaw tui` 或 `ensure_gateway_then.sh`（仅用于检查状态）。
- **continue-on-error**：当 `gateway.log` 中包含“未处理的停止原因：error”时，通过 `openclaw agent --message continue --deliver` 向代理发送“继续”消息。可以使用 `--once` 参数仅执行一次检查，或使用 `--loop` 参数每隔指定时间间隔执行检查。每次触发之间有 90 秒的冷却时间。相关状态信息保存在 `logs/gateway-guard.continue-state.json` 文件中。
- **watch**：这是一个组合型的守护进程（单个 LaunchAgent），每次运行时会执行以下操作：(1) 同步令牌信息（使用 `ensure --apply`），以防止设备令牌不匹配；(2) 提供最近发生的事件摘要；(3) 检查是否需要继续执行错误处理。可以通过 `bash <skill-dir>/scripts/install_watcher.sh`（或 `install_continue_on_error.sh`）来安装该守护进程。该脚本会替换旧的独立守护进程。

## 行为逻辑

- 读取 `openclaw.json` 文件中的 `gateway.auth`（令牌或密码）和 `gateway.port` 信息。
- 与监听该端口的进程进行比较（以及可选的守护进程状态文件）。
- 如果使用了 `--apply` 参数，会通过 `openclaw gateway stop` 命令停止网关，然后使用 `openclaw gateway --port N --auth token|password --token|--password SECRET` 命令重新启动网关。
- 如果配置中缺少令牌信息（仅限令牌模式），会生成一个新的令牌并写入配置文件；如果配置已经正确，则不会覆盖现有信息。
- **continue-on-error**：监控 `OPENCLAW_HOME/logs/gateway.log` 文件中是否包含“未处理的停止原因：error”这一错误信息。如果发现该错误且未处于冷却时间范围内，会通过 `openclaw agent --message continue --deliver` 向代理发送“继续”消息。可以通过 `install_continue_on_error.sh` 命令安装一个每隔 30 秒检查一次网关状态的守护进程。如果 TUI 中出现了错误但 watcher 未触发，可能是网关没有将错误信息记录到 `gateway.log` 中。

## JSON 输出格式（用于 orchestration）

- **status --json** / **ensure --json**：返回 `ok`, `secretMatchesConfig`, `running`, `pid`, `reason`, `recommendedAction`, `configPath`, `authMode`, `gatewayPort` 等信息。如果配置不正确，`recommendedAction` 为“run gateway_guard.py ensure --apply and restart client session”。

## 系统要求

- 需要安装 OpenClaw 并配置 `openclaw.json` 文件，其中包含 `gateway.auth`（模式为 `token` 或 `password`）和 `gateway.port`。
- 系统需要支持 `openclaw` CLI（用于执行 `ensure --apply` 和 `continue-on-error` 命令），以及 `lsof` 和 `ps`（macOS/Unix 系统）命令；在使用 LaunchAgent 时还需要 `launchctl`（macOS 系统）。
- 可选的环境变量：`OPENCLAW_HOME`（OpenClaw 的安装目录，默认为 `~/.openclaw`）和 `OPENCLAW_BIN`（OpenClaw 可执行文件的路径，默认为 `openclaw`）。

## 权限说明

本工具具有以下权限：可以读取和修改 `openclaw.json` 文件（包括在信息缺失或错误时更新 `gateway.auth`）；可以在 `OPENCLAW_HOME/logs/` 目录下写入状态和日志文件；可以通过 OpenClaw CLI 重启网关；如果安装了 watcher，还可以在检测到错误时自动发送“继续”消息。这些操作属于特权操作，只有在用户明确同意的情况下才会执行。