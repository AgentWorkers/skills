---
name: openclaw-optimizer
slug: openclaw-optimizer
version: 2026.3.8
description: >
  **使用场景：**  
  当您希望优化 OpenClaw 的配置（版本：v2026.2.23 及以上）时，这些工具非常有用。具体应用场景包括：降低成本、优化模型路由、配置服务提供商、管理运行环境、实现定时任务自动化、调整子代理架构、优化代理的个性/身份设置（相关文档：SOUL.md、IDENTITY.md、AGENTS.md、USER.md）。此外，这些工具也适用于排查各种 OpenClaw 相关的错误、启动失败问题、通道故障或服务提供商相关的问题。  
  **工作原理：**  
  优先采用命令行界面（CLI）进行操作。系统默认提供审计功能，会先分析当前配置并提出具体的修改建议，只有在获得批准后才会实际执行修改。最终输出内容包括：优化的具体方案、所需的 CLI 命令、配置更新内容以及相应的回滚方案。
triggers:
  - optimize agent
  - optimizing agent
  - improve OpenClaw setup
  - agent best practices
  - OpenClaw optimization
  - model routing
  - add provider
  - configure provider
  - custom provider
  - cron job
  - context bloat
  - reduce costs
  - sub-agent
  - skills openclaw
  - troubleshoot
  - not working
  - error
  - gateway
  - no response
  - channel not working
  - personality audit
  - identity audit
  - bootstrap audit
  - agent personality
  - agent identity
  - optimize personality
  - SOUL.md
  - IDENTITY.md
  - USER.md
metadata:
  openclaw:
    emoji: "🧰"
---
# OpenClaw优化器

**兼容版本：** OpenClaw v2026.3.8 | Skill v1.19.0 | 更新时间：2026-03-09 | 首先通过CLI进行提示

优化和排查OpenClaw工作区的问题：成本敏感的路由、提供者配置、上下文规范、精简自动化、多代理架构以及错误解决。

**参考文件（需要时加载）：**
- `referencesproviders.md` — 所有40多个提供者、自定义提供者模式、故障转移配置
- `references/troubleshooting.md` — 完整的错误参考、7种故障类型、GitHub问题解决方法
- `references/cli-reference.md` — 完整的CLI命令参考
- `references/identity-optimizer.md` — 代理身份/个性审计检查列表、文件角色、操作流程