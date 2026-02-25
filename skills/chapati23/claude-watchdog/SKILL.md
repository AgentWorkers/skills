---
name: claude-watchdog
description: 使用 Telegram 提供的丰富警报功能，监控 Claude API 的故障和延迟峰值。支持状态监控、延迟检测以及自动恢复通知。
homepage: https://github.com/gisk0/claude-watchdog
metadata:
  openclaw:
    emoji: "🐕"
    requires:
      bins: [python3, crontab, curl]
      env: [TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OPENCLAW_GATEWAY_TOKEN]
    primaryEnv: TELEGRAM_BOT_TOKEN
---
# Claude Watchdog 🐕

本工具用于监控Anthropic/Claude API的故障和延迟峰值情况，并通过Telegram发送详细的警报。在状态检查过程中不会消耗任何代理令牌。

## 功能介绍

### 状态监控 (`status-check.py`)
- 每15分钟通过cron任务自动查询 `status.claude.com`
- 显示事件名称、最新更新信息以及各组件的状态
- 如果某些组件（如Haiku）受到影响，但您使用的是Sonnet模型，会将该事件标记为“（非我们的模型）”
- 在系统恢复正常后发送“一切正常”的警报
- **完全免费**

### 延迟检测 (`latency-probe.py`)
- 每15分钟通过OpenClaw的本地网关发送一个简单的请求
- 测量与Anthropic API之间的实际端到端延迟
- 维护一个滚动基线（过去20个样本的中位数）
- 根据延迟峰值的大小使用不同的严重等级（🟡/🟠/🔴）发送警报
- 延迟恢复正常后发送“一切正常”的警报
- **每次检测费用约为0.000001美元**

## 设置方法

运行交互式设置脚本：

```bash
bash /path/to/skills/claude-watchdog/scripts/setup.sh
```

您需要准备以下内容：
1. **Telegram机器人令牌** — 请从[@BotFather](https://t.me/BotFather)获取
2. **Telegram聊天ID** — 向您的机器人发送消息，然后查看 `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. **OpenClaw网关令牌** — 运行以下命令获取：
   ```bash
   python3 -c "from pathlib import Path; import json; print(json.load(open(Path.home() / '.openclaw/openclaw.json'))['gateway']['auth']['token'])"
   ```
4. **网关端口** — 默认值为`18789`

设置脚本会生成配置文件、创建cron任务，并执行首次检查。

如需卸载该工具（可删除cron任务及配置文件/状态数据）：
```bash
bash /path/to/skills/claude-watchdog/scripts/setup.sh --uninstall
```

## 配置文件

配置文件存储在 `~/.openclaw/skills/claude-watchdog/claude-watchdog.env` 中。您可以通过重新运行 `setup.sh` 或直接编辑该文件来修改配置。更改将在下一次cron任务执行时生效（最多15分钟内）。

```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
OPENCLAW_GATEWAY_TOKEN=...
OPENCLAW_GATEWAY_PORT=18789
MONITOR_MODEL=sonnet
PROBE_MODEL=openclaw
PROBE_AGENT_ID=main
```

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | *(必填)* | 来自[@BotFather]的Telegram机器人令牌 |
| `TELEGRAMCHAT_ID` | *(必填)* | 用于接收警报的目标聊天ID |
| `OPENCLAW_GATEWAY_TOKEN` | *(必填)* | 用于访问OpenClaw网关的认证令牌 |
| `OPENCLAW_GATEWAY_PORT` | `18789` | OpenClaw网关监听的端口 |
| `MONITOR_MODEL` | `sonnet` | 用于状态检测的模型名称（例如“sonnet”或“haiku”） |
| `PROBE_MODEL` | `openclaw` | 用于延迟检测的模型别名；`openclaw`会使用网关的默认模型路由 |
| `PROBE_AGENT_ID` | `main` | 与检测请求一起发送的 `x-openclaw-agent-id` 头部的值 |
| `FILTER_KEYWORDS` | *(可选)* | 用于过滤状态警报的关键词（以逗号分隔，例如“skills,Artifacts,Memory”）。空值表示接收所有警报 |

这些配置也可以通过环境变量进行设置（环境变量优先级更高）。

### 安全提示

配置文件中包含敏感信息（Telegram机器人令牌和网关令牌）。设置脚本会将文件权限设置为`600`（仅允许文件所有者读写）。如果您手动创建或修改该文件，请确保权限设置正确：

```bash
chmod 600 ~/.openclaw/skills/claude-watchdog/claude-watchdog.env
```

## 警报示例

**状态异常：**
```
🟠 Anthropic Status: Partially Degraded Service

📌 Elevated error rates on Claude 3.5 Haiku (not our model)
Status: Investigating
Update: "We are investigating increased error rates..."

Components:
  🟠 API: partial outage

🔗 https://status.claude.com
```

**延迟峰值：**
```
🟡 Anthropic API — High Latency Detected

Current: 12.3s
Baseline: 3.1s (median of last 19 samples)
Ratio: 4.0×

Slow responses are expected right now.
```

**系统恢复正常：**
```
✅ Anthropic API — Latency Back to Normal

Current: 2.8s
Baseline: 3.1s
Was: 12.3s when alert fired
```

## 状态记录与日志

所有状态记录和日志文件都存储在 `~/.openclaw/skills/claude-watchdog/` 目录下：

| 文件名 | 用途 |
|------|---------|
| `claude-watchdog-status.json` | 状态检测结果 |
| `claude-watchdog-latency.json` | 延迟检测结果及数据样本 |
| `claude-watchdog-status.log` | 状态检测日志 |
| `claude-watchdog-latency.log` | 延迟检测日志 |

## 调优阈值

您可以在 `latency-probe.py` 文件的顶部修改以下配置常量：

| 常量 | 默认值 | 含义 |
|----------|---------|---------|
| `ALERT_MULTIPLIER` | 2.5 | 当延迟超过基线中位数的N倍时触发警报 |
| `ALERT_HARD_FLOOR` | 10.0秒 | 超过此绝对阈值时立即触发警报 |
| `RECOVER_MULTIPLIER` | 1.5 | 当延迟低于基线中位数的N倍时清除警报 |
| `BASELINE_WINDOW` | 20 | 滚动样本窗口的大小 |
| `BASELINE_MIN_samples` | 5 | 触发警报前的最小样本数量 |
| `PROBE_TIMEOUT` | 45秒 | 超过此时间后停止检测 |

## 系统要求

- Python 3.10及以上版本（仅需要标准库，无需安装pip依赖）
- 本地运行的OpenClaw网关
- 拥有访问目标聊天频道的Telegram机器人