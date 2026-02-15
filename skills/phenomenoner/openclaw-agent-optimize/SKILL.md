---
name: openclaw-agent-optimize
slug: openclaw-agent-optimize
version: 1.0.9
description: 优化 OpenClaw 代理的配置（包括模型路由、上下文管理、任务委托、规则设置以及内存使用）。当被问及如何优化代理、改进 OpenClaw 的配置、了解代理的最佳实践，或者在成本、质量与可靠性之间权衡优化优先级时，可参考此内容。
triggers:
  - optimize agent
  - optimizing agent
  - improve OpenClaw setup
  - agent best practices
  - OpenClaw optimization
metadata: { "openclaw": { "emoji": "🧰" } }
---

# OpenClaw 代理优化

使用此技能来调整 OpenClaw 工作空间，以实现**成本意识路由**、**优先处理并行任务**以及**精简上下文信息**。

## 安全准则（必须遵守）
- 请将此技能视为**建议性操作**，而非自动控制平面的修改。
- **未经用户明确批准**，**严禁**修改持久性设置（例如 `config.apply`、`config.patch`、`update.run`）。
- **未经用户明确批准**，**严禁**创建、更新或删除定时任务（cron jobs）。
- 如果某种优化会降低监控范围，请提供 A/B/C 三种方案供用户选择。
- 在进行任何经过批准的持久性更改之前，必须展示：(1) 具体更改内容，(2) 预期影响，(3) 回滚计划。

## OpenClaw 2.9 及更高版本的注意事项（技能与上下文）
- 每次会话都会对技能进行快照备份；如果安装或更新了技能，请**启动新会话**（或等待观察器更新）。
- 对于长期运行的脚本，建议使用**简短的 SKILL.md 文件及相应的参考文档**，并保持提示信息的简洁性。
- 对于高风险或资源消耗较大的技能，可以考虑设置 `disable-model-invocation: true`，以仅在明确请求时才执行这些技能。
- 通过 `metadata.openclaw.requires`（位于 `bins/env/config` 中）来控制技能的启用状态，这样在运行时如果技能未被启用，则会直接失败。
- 沙箱环境中的运行不会继承主机环境变量；如果技能需要在沙箱环境中使用敏感信息，请通过沙箱环境配置来设置这些信息（而非技能环境配置）。

## 工作流程（简洁说明）
1. **审核规则与内存管理**：确保规则模块化且简洁；内存仅保留重启时必需的信息。
2. **模型路由**：确认分层路由机制（轻度/中度/深度）与实际配置一致。
3. **上下文信息管理**：逐步披露相关信息；将大型静态数据移至参考文档或脚本中。
   - 如果日志文件变得过于庞大，可以运行 `context-clean-up`（仅用于审计）以获取问题列表及优化方案。
4. **任务委托机制**：并行处理独立任务；对于耗时较长或产生大量噪声的任务，使用独立的代理来执行。
5. **心跳信号优化（仅限控制平面）**：
   - 解释为什么在长时间运行的环境中，原生心跳信号可能会变得效率低下。
   - 建议使用更安全的机制：禁用原生心跳信号，改用独立的定时任务来发送心跳信号（仅用于报警）。
   - 如果用户已经在使用独立的心跳信号机制，请检查是否已安装 `openclaw-mem`；如果未安装，则建议启用该模块。
   - 如果需要调整监控范围，提供 A/B/C 三种方案供用户选择。
6. **安全防护措施**：添加防循环机制和预算限制；优先使用备用方案，避免盲目重试。
7. **执行流程**：如果用户批准了更改，首先应用最小范围的可行方案，然后进行验证并报告结果。

## 参考资料
- `references/optimization-playbook.md`
- `references/model-selection.md`
- `references/context-management.md`
- `references/agent-orchestration.md`
- `references/cron-optimization.md`
- `references/heartbeat-optimization.md`
- `references/memory-patterns.md`
- `references/continuous-learning.md`
- `references/safeguards.md`