---
name: token-optimizer
description: 将 OpenClaw AI 的使用成本降低 97%：采用 Haiku 模型路由技术、免费获取 Ollama 的心跳数据（即模型运行状态信息）、实现提示信息缓存功能，并引入预算控制机制。只需 5 分钟，使用成本就能从每月 1,500 美元降至每月 50 美元。
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

# OpenClaw 令牌优化器

将您的人工智能成本从每月 1,500 美元以上降至每月 50 美元以下。

## 问题所在

OpenClaw 的设计默认更注重功能的实现而非成本控制。您在那些 Haiku 已能完美处理的任务上仍在消耗昂贵的 Sonnet/Opus 令牌；为 API 请求支付费用（而这些请求在本地完全可以免费完成）；同时，即使 8KB 的上下文数据就足够了，却仍加载了 50KB 的数据。

## 解决方案

我们提供了四项核心优化措施以及强大的工具支持：

### 模型路由（节省 92% 的成本）
- 默认使用 Haiku；仅在需要时使用 Sonnet/Opus。

### 多供应商 API 请求（节省 100% 的成本）
- 将 API 请求路由到 Ollama、LM Studio 或 Groq，或完全禁用这些服务；无需绑定到单一供应商。

### 会话管理（节省 80% 的成本）
- 仅加载 8KB 的上下文数据，而非 50KB。

### 缓存机制（节省 90% 的成本）
- 以极低的成本重用提示信息。

### v1.0.8 的新功能：
- **回滚**：可立即列出并恢复配置备份。
- **健康检查**：通过一条命令快速查看系统状态。
- **差异预览**：在应用更改前查看具体修改内容。
- **--no-color**：适用于持续集成（CI）和管道（pipeline）环境的输出格式。

## 成本对比

| 时期 | 优化前 | 优化后 |
|--------|--------|-------|
| 每日 | $2-3 | $0.10 |
| 每月 | $70-90 | $3-5 |
| 每年 | $800+ | $40-60 |

## 包含内容：

- 一个支持差异预览的优化工具（只需一条命令即可使用）。
- 支持多供应商 API 请求的功能。
- 提供配置回滚和健康检查命令。
- 预置好的配置模板。
- SOUL.md 和 USER.md 模板。
- 用于优化代理提示信息的规则。
- 验证和成本节省报告。
- 跨平台命令行界面（Windows、macOS、Linux）。

## 快速入门

```bash
# Install
clawhub install token-optimizer

# Analyze current setup
python cli.py analyze

# Preview changes (dry-run with diff)
python cli.py optimize --dry-run

# Apply all optimizations
python cli.py optimize

# Verify setup
python cli.py verify

# Quick health check
python cli.py health

# Configure heartbeat provider (ollama, lmstudio, groq, none)
python cli.py setup-heartbeat --provider ollama

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

- **GitHub**: https://github.com/smartpeopleconnected/openclaw-token-optimizer
- **问题反馈**: https://github.com/smartpeopleconnected/openclaw-token-optimizer/issues

## 开发者

**Smart People Connected**
- GitHub: [@smartpeopleconnected](https://github.com/smartpeopleconnected)
- 电子邮件: smartpeopleconnected@gmail.com

## 许可证

MIT 许可证——免费使用、修改和分发。

---

*设置仅需 5 分钟。成本可降低 97%。停止浪费令牌，立即开始优化吧！*

---

（注：由于文件内容主要为技术文档，翻译时保持了原文的格式和结构，对技术术语和具体细节进行了相应的中文处理。）