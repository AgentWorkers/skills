---
name: token-optimizer
description: 将 OpenClaw AI 的成本降低 97%：采用 Haiku 模型路由技术、免费使用 Ollama 的心跳数据、实现提示缓存功能，并进行预算控制。只需 5 分钟，每月费用即可从 1,500 美元降至 50 美元。
homepage: https://github.com/smartpeopleconnected/openclaw-token-optimizer
triggers:
  - too expensive
  - costs too much
  - burning tokens
  - high token usage
  - reduce costs
  - save money
  - optimize tokens
  - budget exceeded
  - token optimization
  - cut api costs
  - lower ai spend
  - cheaper model
  - cost savings
  - api bill
  - spending too much
  - waste tokens
  - token budget
  - reduce token usage
---
# OpenClaw令牌优化器

将您的人工智能成本从每月1500美元以上降至50美元以下。

## 问题所在

OpenClaw默认更注重功能的实现而非成本控制。您在Haiku能够完美处理的任务上仍在消耗昂贵的Sonnet/Opus令牌；为API请求支付费用（而这些请求本可以在本地免费完成）；并且在只需要8KB上下文数据的情况下却加载了50KB的数据。

## 解决方案

通过四项核心优化措施以及强大的工具集来降低成本：

### 模型路由（节省92%的成本）
- 默认使用Haiku模型；仅在必要时使用Sonnet/Opus模型。

### 多供应商API请求（节省100%的成本）
- 将API请求路由到Ollama、LM Studio或Groq等平台，或完全禁用这些请求。无需绑定到单一供应商。

### 会话管理（节省80%的成本）
- 仅加载8KB的上下文数据，而非50KB。

### 缓存（节省90%的成本）
- 以10%的成本重复使用提示信息。

### v1.0.8的新功能：
- **回滚**：即时列出并恢复配置备份。
- **健康检查**：通过一个命令快速查看系统状态。
- **差异预览**：在应用更改前查看具体修改内容。
- **--no-color**：适用于持续集成（CI）/管道（pipeline）环境的输出格式。

## 成本对比

| 时期 | 使用OpenClaw前的成本 | 使用优化器后的成本 |
|--------|----------------|----------------------|
| 每日 | 2-3美元 | 0.10美元 |
| 每月 | 70-90美元 | 3-5美元 |
| 每年 | 800美元以上 | 40-60美元 |

## 包含内容：
- 一个带有差异预览功能的命令行优化器。
- 支持多供应商API请求（Ollama、LM Studio、Groq）。
- 配置回滚和健康检查命令。
- 可直接使用的配置模板（SOUL.md、USER.md）。
- 用于优化代理提示信息的规则。
- 验证和成本节省报告。

## 该工具的修改范围

所有修改均保存在`~/.openclaw/`目录下。在进行任何修改之前，系统会自动创建备份。

| 目录路径 | 功能 |
|------------|-------------------------|
| `~/.openclaw/openclaw.json` | 主要OpenClaw配置文件（模型路由、API请求设置等） |
| `~/.openclaw/backups/` | 带时间戳的配置备份文件（自动生成） |
| `~/.openclaw/workspace/` | 模板文件（SOUL.md、USER.md、IDENTITY.md） |
| `~/.openclaw/prompts/` | 代理提示信息优化规则 |
| `~/.openclaw/token-optimizer-stats.json` | 用于生成成本节省报告的使用统计信息 |

**默认为安全模式**：所有命令均以预览模式运行。需使用`--apply`参数才能应用更改。

## 快速入门

```bash
# Install
clawhub install token-optimizer

# Analyze current setup
python cli.py analyze

# Preview changes (dry-run by default)
python cli.py optimize

# Apply all optimizations
python cli.py optimize --apply

# Verify setup
python cli.py verify

# Quick health check
python cli.py health

# Configure heartbeat provider (preview)
python cli.py setup-heartbeat --provider ollama

# Configure heartbeat provider (apply)
python cli.py setup-heartbeat --provider ollama --apply

# List and restore backups
python cli.py rollback --list
python cli.py rollback --to <backup-file>
```

## 生成的配置文件

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-haiku-4-5" },
      "cache": { "enabled": true, "ttl": "5m" }
    }
  },
  "heartbeat": {
    "provider": "ollama",
    "model": "ollama/llama3.2:3b"
  },
  "budgets": {
    "daily": 5.00,
    "monthly": 200.00
  }
}
```

## 链接：
- **GitHub仓库**：https://github.com/smartpeopleconnected/openclaw-token-optimizer
- **问题反馈**：https://github.com/smartpeopleconnected/openclaw-token-optimizer/issues

## 开发者：
**Smart People Connected**
- GitHub账号：[@smartpeopleconnected](https://github.com/smartpeopleconnected)
- 电子邮件：smartpeopleconnected@gmail.com

## 许可证：
MIT许可证——免费使用、修改和分发。

---

**设置仅需5分钟。成本可降低97%。立即停止浪费令牌，开始节省开支吧！**

---

*注：文件中的````bash
# Install
clawhub install token-optimizer

# Analyze current setup
python cli.py analyze

# Preview changes (dry-run by default)
python cli.py optimize

# Apply all optimizations
python cli.py optimize --apply

# Verify setup
python cli.py verify

# Quick health check
python cli.py health

# Configure heartbeat provider (preview)
python cli.py setup-heartbeat --provider ollama

# Configure heartbeat provider (apply)
python cli.py setup-heartbeat --provider ollama --apply

# List and restore backups
python cli.py rollback --list
python cli.py rollback --to <backup-file>
````和````json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-haiku-4-5" },
      "cache": { "enabled": true, "ttl": "5m" }
    }
  },
  "heartbeat": {
    "provider": "ollama",
    "model": "ollama/llama3.2:3b"
  },
  "budgets": {
    "daily": 5.00,
    "monthly": 200.00
  }
}
````为占位符，实际代码内容需根据实际情况填写。*