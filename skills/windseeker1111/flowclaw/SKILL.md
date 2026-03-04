---
name: FlowClaw
description: "专为 OpenClaw 设计的“不死”大型语言模型（LLM）负载均衡器。该系统实时监控 Anthropic、Google、OpenAI、GitHub Copilot 和 Ollama 等平台上的模型使用情况，根据任务的紧急程度对模型进行排序，并自动切换到备用模型。这样一来，您的使用体验永远不会受到任何影响（即您的代理程序永远不会因模型故障而停滞）。"
metadata:
  openclaw:
    emoji: "🦞"
    os:
      - darwin
      - linux
    requires:
      bins:
        - curl
        - python3
---
# FlowClaw — LLM（大型语言模型）使用情况监控与负载均衡器

> *监控使用情况，合理分配路由请求，确保信用不被浪费。*

FlowClaw 提供统一的仪表盘和自动路由功能，适用于您所有的 LLM（大型语言模型）订阅服务。它采用“最早到期优先”的调度策略——优先处理那些信用即将耗尽的账户，从而避免信用的浪费。

## 支持的提供商

| 提供商 | 认证方式 | 数据来源 |
|----------|------|------------|
| **Anthropic Claude Max** | OAuth（无限账户） | `api.anthropic.com/api/oauth/usage` |
| **Google Gemini CLI** | 通过 OpenClaw 进行 OAuth 认证 | `cloudcode-pa.googleapis.com` |
| **Google Antigravity** | 使用 codexbar 提供的数据 | codexbar 使用情况 API |
| **OpenAI Codex** | 通过 OpenClaw 进行 OAuth 认证 | `chatgpt.com/backend-api/wham/usage` |
| **GitHub Copilot** | 通过 OpenClaw 进行 OAuth 认证 | `api.github.com/copilot_internal/user` |
| **Ollama** | 本地检测（自动识别） | `localhost:11434/api/tags` |

## 命令

```bash
# 📊 Usage Monitoring
flowclaw status [--fresh] [--json]     # Full provider dashboard
flowclaw monitor [--json] [--cached]   # Clean usage report (no scoring)

# 🧠 Load Balancing
flowclaw score [--json]                # Scored ranking of all accounts
flowclaw optimize [--dry-run]          # Reorder OpenClaw model priority
flowclaw auto                          # Optimize silently (for cron jobs)

# 🛠 Utilities
flowclaw test                          # Run scoring engine unit tests
flowclaw history [N]                   # Routing decision history
```

## 设置

### Anthropic（Claude Max）——无限账户
```bash
claude login
bash {baseDir}/scripts/save-account.sh
# Repeat for each account
```

### Google Gemini CLI
```bash
openclaw models auth login --provider google-gemini-cli
```

### Google Antigravity
```bash
openclaw models auth login --provider google-antigravity
brew install --cask steipete/tap/codexbar   # Required for usage metrics
```

### OpenAI Codex
```bash
openclaw models auth login --provider openai-codex
```

### GitHub Copilot
```bash
openclaw models auth login-github-copilot
```

### Ollama
```bash
brew install ollama && ollama pull qwen3:235b
# Auto-detected — no config needed
```

### 定时任务自动化
```bash
# Optimize routing every 30 minutes
*/30 * * * * bash ~/clawd/skills/flowclaw/scripts/flowclaw.sh auto
```

## 评分算法

```
score = urgency(0.30) + availability(0.25) + proximity(0.15) + weekly_headroom(0.20) + tier(0.10)
```

| 评分因素 | 计算公式 | 衡量指标 |
|--------|---------|----------|
| 紧急性 | `剩余信用 / 重置所需时间` | 每小时浪费的信用数量 |
| 可用性 | `√(剩余信用)` | 当前可用资源 |
| 接近性 | `1 - (剩余时间 / 时间窗口)` | 到期的紧迫程度 |
| 周期性余量 | `(100 - 当前使用率) / 100` | 7 天内的资源储备 |
| 等级加成 | 免费用户=+0.8，订阅用户=0，本地用户=-0.3 | 用户的使用成本偏好 |

**有效期说明：** 5 小时的会话时间和 7 天的周期都会过期。当距离重置时间小于等于 6 小时时，系统会取消惩罚机制，允许用户继续使用剩余信用。**注意：** 只允许在同一能力等级内的模型之间进行切换（例如：Opus ↔ Opus，不允许 Opus ↔ Gemini）。