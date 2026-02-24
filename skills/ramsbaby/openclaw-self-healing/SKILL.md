---
name: openclaw-self-healing
version: 3.1.1
description: >
  OpenClaw Gateway 的四层自主自愈与自动恢复系统：  
  该系统能够实时监控网关的运行状态，在网关崩溃时自动重启；检测 OAuth 令牌是否过期；终止异常运行的进程（即“僵尸进程”）；并在自动恢复失败时向 Claude Code AI 寻求诊断支持。适用于 OpenClaw 网关出现崩溃、停止响应、进入重启循环，或需要自动监控与恢复的情况。系统具备以下功能：  
  - 监控机制（watchdog）  
  - 配置验证（config validation）  
  - 指数级重试策略（exponential backoff）  
  - 通过 Discord/Telegram 发送警报  
  支持操作系统：macOS 和 Linux。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["tmux", "claude", "jq"] },
        "install":
          [
            {
              "id": "tmux",
              "kind": "brew",
              "package": "tmux",
              "bins": ["tmux"],
              "label": "Install tmux (brew)",
            },
            {
              "id": "claude",
              "kind": "node",
              "package": "@anthropic-ai/claude-code",
              "bins": ["claude"],
              "label": "Install Claude Code CLI (npm)",
            },
            {
              "id": "jq",
              "kind": "brew",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew) - for metrics dashboard",
            },
          ],
      },
  }
---
# OpenClaw 自愈系统

> “一个能够自我修复的系统——或者在无法修复时请求帮助的系统。”

这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) Gateway 设计的 4 层级自主恢复系统，具备基于 Claude Code 的 **人工智能驱动的诊断** 功能。该系统已在 macOS 和 Linux 环境中通过实际生产环境进行了测试。

## 架构

```
Level 1: config-watch        → Config file change detection + instant reload
Level 2: Watchdog v4.4       → OAuth detection, zombie kill, exponential backoff
Level 3: Claude Code Doctor  → AI-powered diagnosis & repair (30 min window) 🧠
Level 4: Discord/Telegram    → Human escalation with full context
```

## v3.1.0 的新特性

- **完整的修复流程**：`config-watch` → `Watchdog` → `Emergency Recovery` 现在已完全连接在一起
- **安装程序重构**：一个 `install.sh` 脚本同时支持 macOS (LaunchAgent) 和 Linux (systemd) 的安装
- **Watchdog v4.4**：支持 OAuth 令牌过期检测、自动终止僵尸进程、指数级重试机制
- **Emergency Recovery v2**：引入持久化学习机制、记录推理过程、支持多种模型（Claude Code + Aider）
- **指标仪表盘**：通过 tmux 提供成功率、平均修复时间 (MTTR) 和趋势分析等功能

## 快速设置

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Ramsbaby/openclaw-self-healing/main/install.sh)
```

或者通过 ClawHub 进行安装：

```bash
npx clawhub@latest install openclaw-self-healing
```

## 4 层级的详细说明

| 层级 | 脚本 | 触发条件 | 执行操作 |
|-------|--------|---------|--------|
| L1 | `config-watch.sh` | 配置文件更改 | 验证配置并重新加载 Gateway |
| L2 | `gateway-watchdog.sh` | 进程异常或 HTTP 请求失败 | 终止异常进程 → 重启 → 采用指数级重试策略 |
| L3 | `emergency-recovery-v2.sh` | 连续故障 30 分钟 | 使用 Claude Code 进行实时诊断 |
| L4 | `emergency-recovery-monitor.sh` | L3 级别的触发条件 | 通过 Discord 和 Telegram 发送警报 |

## 配置

所有配置均通过 `~/.openclaw/.env` 文件中的环境变量进行设置：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `DISCORD_WEBHOOK_URL` | （无） | 用于 L4 级别警报的 Discord Webhook 地址 |
| `OPENCLAW_GATEWAY_URL` | `http://localhost:18789/` | Gateway 的健康检查 URL |
| `HEALTH_CHECK_MAX_RETRIES` | `3` | 在触发 L3 级别响应之前的重启尝试次数 |
| `EMERGENCY_RECOVERY_TIMEOUT` | `1800` | Claude 诊断的恢复超时时间（30 分钟） |

## 经验证的恢复案例

- **OAuth 令牌过期**：Watchdog v4.4 会在日志中检测到 401 错误，并在代理程序崩溃前自动重启
- **僵尸进程**：预检测到进程 ID 不匹配时，会立即终止该进程并通过 launchctl 重新启动
- **配置错误**：当检测到配置错误时，会自动执行 `openclaw doctor --fix` 命令进行修复
- **L3 级别触发**：Claude Code 会在 15 分钟内诊断并修复配置问题

## 链接

- **GitHub仓库**：https://github.com/Ramsbaby/openclaw-self-healing
- **更新日志**：https://github.com/Ramsbaby/openclaw-self-healing/blob/main/CHANGELOG.md
- **Linux 安装指南**：https://github.com/Ramsbaby/openclaw-self-healing/blob/main/docs/LINUX_SETUP.md

## 许可证

MIT 许可证 — 由 @ramsbaby 和 Jarvis 共同开发 🦞