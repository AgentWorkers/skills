---
name: openclaw-architect
description: "**OpenClaw AI代理部署的设计、配置、调试与优化指南**
本指南全面介绍了OpenClaw AI代理的部署流程，涵盖了网关配置、`openclaw.json`文件设置、模型路由与回退机制、技能开发与发布、Cron作业调度、内存管理系统（Qdrant、Neo4j、SQLite）、Docker基础设施以及Tailscale VPN网络等方面的内容。同时，还提供了配置分析工具，可自动检查`openclaw.json`文件并提供建议以优化配置；此外还包含健康检查功能，用于验证OpenClaw的所有子系统是否正常运行。
**适用场景：**  
适用于AI代理的搭建、网关调试、技能开发与优化、成本控制以及基础设施故障排查。整个系统仅依赖Python标准库，无需额外安装任何第三方库。
**核心功能包括：**  
- **网关配置：** 完整指导如何配置OpenClaw网关，确保其与外部系统顺畅交互。  
- **`openclaw.json`设置：** 详细解释如何编辑该配置文件以定制代理行为。  
- **模型路由与回退机制：** 介绍如何设计高效的模型路由策略及备用方案。  
- **技能开发与发布：** 指导如何创建和发布新的AI技能供代理使用。  
- **Cron作业调度：** 教授如何使用Cron任务自动执行重复性任务。  
- **内存管理系统：** 介绍如何有效管理代理的内存资源（Qdrant、Neo4j、SQLite）。  
- **Docker基础设施：** 指导如何使用Docker容器化部署OpenClaw。  
- **Tailscale VPN网络：** 说明如何利用Tailscale构建安全的网络环境。  
**附加工具：**  
- **配置分析器：** 自动分析`openclaw.json`文件，提供优化建议。  
- **健康检查器：** 验证OpenClaw所有组件的运行状态。  
**适用人群：**  
软件开发人员、系统管理员、AI工程师以及希望高效部署和管理OpenClaw AI代理的从业者。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🏗️", "requires": {"env": ["OPENCLAW_WORKSPACE"]}, "primaryEnv": "OPENCLAW_WORKSPACE", "homepage": "https://www.agxntsix.ai"}}
---
# 🏗️ OpenClaw 架构师

这是一项全面掌握 OpenClaw 部署理解、配置、调试和优化技能的工具。该工具基于实际生产经验开发而成。

## 主要功能

- **配置分析** — 审查 `openclaw.json` 文件并提供建议
- **系统健康检查** — 通过一个命令验证所有 OpenClaw 子系统
- **模型路由配置** — 设置主模型、备用模型及成本层级
- **技能构建** — 支持 SKILL.md 格式，支持通过 CLI 进行操作，并可将构建的技能发布到 ClawHub
- **排查网关问题** — 故障排除、解决 cron 任务失败及会话崩溃等问题
- **性能优化** — 优化模型选择、降低成本、管理上下文信息
- **管理 cron 任务** — 调度任务、处理错误、实现重试机制
- **内存系统配置** — 支持与 Qdrant、Neo4j、SQLite 的集成
- **基础设施部署** — 支持使用 Docker、Tailscale VPN 及网络服务
- **升级后验证** — 提供安全升级的 checklist

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `OPENCLAW_WORKSPACE` | ✅ | OpenClaw 工作空间目录的路径 |

## 快速入门

```bash
PY=~/.openclaw/workspace/.venv/bin/python3

# Analyze your openclaw.json configuration
$PY skills/openclaw-architect/scripts/config_analyzer.py

# Health check all OpenClaw systems
$PY skills/openclaw-architect/scripts/health_check.py
```

## 命令

### 配置分析器
```bash
# Audit current configuration
$PY skills/openclaw-architect/scripts/config_analyzer.py

# Analyze a specific config file
$PY skills/openclaw-architect/scripts/config_analyzer.py --config /path/to/openclaw.json
```

### 系统健康检查
```bash
# Check all subsystems
$PY skills/openclaw-architect/scripts/health_check.py

# Check specific subsystem
$PY skills/openclaw-architect/scripts/health_check.py --check gateway
$PY skills/openclaw-architect/scripts/health_check.py --check cron
$PY skills/openclaw-architect/scripts/health_check.py --check memory
```

## 参考资料

| 文件 | 说明 |
|------|-------------|
| `references/architecture-overview.md` | OpenClaw 的端到端工作原理 |
| `references/config-reference.md` | 所有 `openclaw.json` 配置选项的详细说明 |
| `references/skills-guide.md` | 如何构建和发布技能 |
| `references/cron-guide.md` | cron 任务的调度与使用技巧 |
| `references/memory-guide.md` | 内存系统配置指南 |
| `references/troubleshooting.md` | 常见问题及调试方法 |
| `references/optimization-tips.md` | 性能优化指南 |

## 架构原则

1. **以策略为核心** — 数据存储依赖于 Mem0、Qdrant、Neo4j、SQLite；Markdown 文件仅用于存储操作日志。
2. **高容错性** — 必须配置至少两个备用模型，并确保每个模型都能正常运行。
3. **智能资源管理** — 监控资源使用情况，在资源耗尽前自动切换模型层级并发送警报。
4. **技能的可复用性** — 所有可重用的配置方案都会被发布到 ClawHub。
5. **系统自我监控** — 通过 cron 任务实时监控系统运行状态、可用时间和成本消耗。
6. **自动化处理重复性任务** — 对于重复性操作，使用 cron 任务或脚本自动执行。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/config_analyzer.py` | 审查 `openclaw.json` 配置文件 |
| `{baseDir}/scripts/health_check.py` | 验证所有 OpenClaw 子系统的运行状态 |

## 输出格式

所有命令的输出均为结构化文本，包含明确的成功/失败指示以及可执行的建议。

## 数据政策

该工具仅读取本地配置文件，不会向任何外部服务发送数据。

---

开发者：[M. Abidi](https://www.agxntsix.ai)

[LinkedIn](https://www.linkedin.com/in/mohammad-ali-abidi) · [YouTube](https://youtube.com/@aiwithabidi) · [GitHub](https://github.com/aiwithabidi) · [预约咨询](https://cal.com/agxntsix/abidi-openclaw)