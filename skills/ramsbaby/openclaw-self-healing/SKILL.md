---
name: openclaw-self-healing
version: 2.0.1
description: OpenClaw Gateway 的四层自主自愈系统，具备持续学习功能、推理日志记录以及多通道警报机制。该系统引入了 Claude Code 作为第三级“紧急医生”，负责基于人工智能的故障诊断与修复工作。
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

> **“一个能够自我修复的系统——或者在无法修复时寻求帮助的系统。”**

这是一个专为 OpenClaw Gateway 设计的、具有四层自主自愈功能的系统。

## 架构

```
Level 1: Watchdog (180s)     → Process monitoring (OpenClaw built-in)
Level 2: Health Check (300s) → HTTP 200 + 3 retries
Level 3: Claude Recovery     → 30min AI-powered diagnosis 🧠
Level 4: Discord Alert       → Human escalation
```

## 新功能（v2.0）

- **全球首创**：Claude Code 被用作三级紧急响应系统
- **持续学习**：自动记录故障恢复过程（症状 → 原因 → 解决方案 → 预防措施）
- **推理日志**：可解释的 AI 决策过程
- **多渠道警报**：支持 Discord 和 Telegram
- **指标仪表盘**：显示故障恢复率、恢复时间及趋势分析数据
- 已经过生产环境测试（2026年2月5日至6日验证）
- 支持与 macOS 的 LaunchAgent 集成

## 快速设置

### 1. 安装依赖项

```bash
brew install tmux
npm install -g @anthropic-ai/claude-code
```

### 2. 配置环境

```bash
# Copy template to OpenClaw config directory
cp .env.example ~/.openclaw/.env

# Edit and add your Discord webhook (optional)
nano ~/.openclaw/.env
```

### 3. 安装脚本

```bash
# Copy scripts
cp scripts/*.sh ~/openclaw/scripts/
chmod +x ~/openclaw/scripts/*.sh

# Install LaunchAgent
cp launchagent/com.openclaw.healthcheck.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.openclaw.healthcheck.plist
```

### 4. 验证系统功能

```bash
# Check Health Check is running
launchctl list | grep openclaw.healthcheck

# View logs
tail -f ~/openclaw/memory/healthcheck-$(date +%Y-%m-%d).log
```

## 脚本说明

| 脚本 | 所需权限级别 | 功能描述 |
|--------|-------|-------------|
| `gateway-healthcheck.sh` | 权限级别 2 | 执行 HTTP 200 健康检查，最多重试 3 次，必要时触发升级机制 |
| `emergency-recovery.sh` | 权限级别 3 | 使用 Claude Code 进行 AI 诊断（版本 1） |
| `emergency-recovery-v2.sh` | 权限级别 3 | 增强了学习功能及推理日志记录（版本 2） ⭐ |
| `emergency-recovery-monitor.sh` | 权限级别 4 | 在系统故障时通过 Discord/Telegram 发送通知 |
| `metrics-dashboard.sh` | 无特定权限要求 | 可视化故障恢复统计数据（新功能） |

## 配置

所有配置信息通过 `~/.openclaw/.env` 文件中的环境变量进行设置：

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `DISCORD_WEBHOOK_URL` | 无 | 用于发送警报的 Discord Webhook 地址 |
| `OPENCLAW_GATEWAY_URL` | `http://localhost:18789/` | Gateway 健康检查的 URL |
| `HEALTH_CHECK_MAX_RETRIES` | `3` | 重试次数上限 |
| `EMERGENCY_RECOVERY_TIMEOUT` | `1800` | Claude 诊断的超时时间（30 分钟） |

## 测试

### 测试二级功能（健康检查）

```bash
# Run manually
bash ~/openclaw/scripts/gateway-healthcheck.sh

# Expected output:
# ✅ Gateway healthy
```

### 测试三级功能（Claude 诊断与恢复）

```bash
# Inject a config error (backup first!)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# Wait for Health Check to detect and escalate (~8 min)
tail -f ~/openclaw/memory/emergency-recovery-*.log
```

## 链接

- **GitHub 仓库：** https://github.com/Ramsbaby/openclaw-self-healing |
- **文档：** https://github.com/Ramsbaby/openclaw-self-healing/tree/main/docs |

## 许可证

采用 MIT 许可证——您可以自由使用该系统。

由 @ramsbaby 和 Jarvis 共同开发 🦞