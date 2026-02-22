---
name: clawzembic
description: OpenClaw的Lighthouse风格效率审计工具：该工具会根据6个方面对您的实例进行评分（从A+到F）——包括上下文注入（context injection）、Cron任务的健康状况、会话数据膨胀（session bloat）、配置问题（config）、技能使用情况（skills）、以及系统日志记录（transcripts）。该工具能够识别出被浪费的令牌（tokens）、膨胀的会话数据（bloated sessions）、配置错误的Cron任务（misconfigured crons），以及模型优化（model right-sizing）的机会。该工具完全不依赖任何第三方库，仅使用Python的标准库（Python stdlib）。
metadata:
  openclaw:
    emoji: "💊"
    requires:
      anyBins: ["python3"]
    tags:
      - audit
      - optimization
      - efficiency
      - diagnostics
      - performance
---
# Clawzembic — 为您的 OpenClaw 实例提供减肥方案（优化建议）

**OpenClaw 效率的审计工具（采用 Lighthouse 风格）**：运行该工具后，您将获得一个评分（从 A+ 到 F），从而识别并优化系统中的冗余部分。

该工具会扫描您的 OpenClaw 安装环境，并从六个关键方面进行评估：上下文注入（Context Injection）、Cron 任务管理（Cron Health）、会话管理（Session Bloat）、配置管理（Config Health）、技能管理（Skill Bloat）以及日志文件大小（Transcript Size）。您将获得一个总体评分，同时还会看到每个方面的详细分析及相应的优化建议。

**完全无依赖性**：仅依赖 Python 3.8 及更高版本的标准库。

## 快速入门

```bash
# Audit this machine
bash skills/clawzembic/lean-audit.sh

# Audit a remote instance (VM, etc.)
bash skills/clawzembic/lean-audit.sh --remote user@host

# JSON output for dashboards/integrations
bash skills/clawzembic/lean-audit.sh --json

# Show automated fix suggestions
bash skills/clawzembic/lean-audit.sh --fix

# Custom .openclaw directory
bash skills/clawzembic/lean-audit.sh --dir /path/to/.openclaw
```

## 审计内容

| 评估类别 | 权重 | 被标记的问题 |
|----------|--------|-------------------|
| 上下文注入 | 25% | 大型的 MEMORY.md 文件、臃肿的工作区文件占用过多系统资源 |
| Cron 任务管理 | 25% | 使用错误的模型处理常规任务、主会话受到污染 |
| 会话管理 | 20% | 过时的会话占用过多系统资源、资源浪费率超过 35% |
| 配置管理 | 15% | 心跳检测频率过高、子代理默认设置不当、缺少数据压缩机制 |
| 技能管理 | 10% | 注入的技能过多、未使用的技能导致系统响应变慢 |
| 日志文件大小 | 5% | 日志文件过大（超过 10MB），占用大量磁盘空间 |

## 评分标准

- **A+/A**（90-100 分）：系统运行非常高效 💪
- **B+/B**（75-89 分）：整体表现良好，需要少量优化 |
- **C+/C**（60-74 分）：存在一些问题，需要改进 🍕
- **D+/D**（45-59 分）：系统存在明显冗余，需要重点优化 🫠
- **F**（低于 45 分）：系统运行状况极差，急需使用 Clawzembic 进行紧急修复 💊

## 代理使用说明

当 Jeffrey 要求您对 OpenClaw 实例进行审计或优化时，请执行以下操作：

1. 运行 `bash skills/clawzembic/lean-audit.sh`（或对于虚拟机，使用 `--remote user@claudette`）；
2. 查看审计报告并理解其中的关键发现；
3. 如果评分低于 75 分，可以使用 `--fix` 模式进行自动修复。

对于远程实例，请确保已配置基于 SSH 的身份验证机制。该工具通过 SSH 在远程执行审计任务，无需在目标系统上安装任何代理程序。