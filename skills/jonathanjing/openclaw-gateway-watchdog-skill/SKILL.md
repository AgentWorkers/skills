---
name: gateway-watchdog
description: 使用 watchdog 状态机监控 OpenClaw 网关的健康状况，通过 Discord 发送警报，并在 macOS 上实现冷却机制以避免重复通知；同时提供隔离的备用部署方案。适用于需要检测网关故障、自动恢复机制以及低干扰度 Discord 事件通知的场景。
version: "1.0.2"
metadata:
  {
    "openclaw":
      {
        "emoji": "🚨",
        "requires": { "bins": ["bash", "python3", "openclaw"], "config": ["channels.discord.enabled"] },
      },
  }
---
# Gateway Watchdog（Discord）

这是一个专为 OpenClaw 网关事件设计的 Discord 监控工具。

## 🛠️ 安装

### 1. 建议使用 OpenClaw 的内置功能
直接告诉 OpenClaw：“安装 gateway-watchdog 功能。”该工具会自动完成安装和配置。

### 2. 手动安装（通过 CLI）
如果您更喜欢在终端中操作，请运行以下命令：
```bash
clawhub install gateway-watchdog
```

## 数据隔离机制
- 监控数据存储在 `~/.openclaw/watchdogs/gateway-discord/` 目录下。
- 无需修改 `openclaw.json` 配置文件。
- 默认模式下，该工具仅提供只读监控功能（`GW_watchDOG_ENABLE_RESTART=0`）。
- 自动重启功能是可选的，并且会限制重启次数。

## 该工具包含的文件：
- `scripts/gateway-watchdog.sh`：负责执行健康检查、状态管理以及向 Discord 发送通知。
- `scripts/install-launchd.sh`：用于根据模板安装用户自定义的 LaunchAgent。
- `references/com.openclaw.gateway-watchdog.plist.template`：LaunchAgent 的启动配置模板。
- `references/cron-agent-turn.md`：用于配置 cron 任务的模板文件。

## 健康检查
该监控工具会检查以下各项：
```bash
openclaw gateway status --json
openclaw health --json --timeout <ms>
```

**通过标准**：
- 网关服务正在运行。
- RPC 探针正常工作（如果存在的话）。
- 健康检查请求能够成功返回结果。

**失败原因**：
- `runtime_stopped`：网关服务已停止。
- `rpc_probe_failed`：RPC 探针无法正常工作。
- `health_unreachable`：无法连接到网关服务。
- `auth_mismatch`：认证信息不匹配。
- `config_invalid`：配置文件无效。

## 快速启动（手动运行）
```bash
bash "{baseDir}/scripts/gateway-watchdog.sh"
```

**可选环境变量**：
```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export DISCORD_BOT_TOKEN="discord_bot_token"
export DISCORD_CHANNEL_ID="<your_discord_channel_id>"
export GW_WATCHDOG_SOURCE="manual"
export GW_WATCHDOG_FAIL_THRESHOLD=2
export GW_WATCHDOG_COOLDOWN_SECONDS=300
```

**数据传输优先级**：
1. `DISCORD_WEBHOOK_URL`：用于接收来自 Discord 的 Webhook 请求的 URL。
2. `DISCORD_BOT_TOKEN + DISCORD_CHANNEL_ID`：用于生成 Discord 机器人的访问令牌和频道 ID。

## macOS 背景模式（使用 LaunchAgent）
请按照以下步骤安装 LaunchAgent（该工具不会修改 OpenClaw 的核心配置文件）：
```bash
bash "{baseDir}/scripts/install-launchd.sh" --interval 30 --load
```

**检查状态**：
```bash
launchctl list | rg "com.openclaw.gateway-watchdog"
```

## OpenClaw 的 cron 模式（内部执行）
该监控工具会通过独立的 cron 任务进行监控，并将所有消息发送到指定的 Discord 频道中：
```bash
openclaw cron add \
  --name "gateway-watchdog-internal" \
  --cron "*/1 * * * *" \
  --session isolated \
  --message "Run bash {baseDir}/scripts/gateway-watchdog.sh and report state changes only." \
  --announce \
  --channel discord \
  --to "channel:<your_channel_id>" \
  --best-effort-deliver
```

## 自动恢复策略（可选）
**启用自动重启功能**：
```bash
export GW_WATCHDOG_ENABLE_RESTART=1
export GW_WATCHDOG_MAX_RESTART_ATTEMPTS=2
```

**安全限制**：
- 仅在达到预设的故障阈值后才会触发重启。
- 每次事件窗口内最多允许尝试重启指定次数。
- 禁止重新安装或对系统进行破坏性修改。

## 备份与审计记录：
- 状态文件：`~/.openclaw/watchdogs/gateway-discord/state.json`
- 状态备份文件：`~/.openclaw/watchdogs/gateway-discord/backups/state-*.json`
- 事件日志：`~/.openclaw/watchdogs/gateway-discord/events.jsonl`

该工具会定期删除旧备份文件，并保留最近的日志以备回滚或调试使用。