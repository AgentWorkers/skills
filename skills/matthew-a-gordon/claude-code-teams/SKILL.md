---
name: claude-code-teams
description: Production skill for orchestrating Claude Code's native agent teams feature. Use when: (1) Multi-lens reviews, (2) Competing hypotheses debugging, (3) Full-stack features, (4) Architecture debates, (5) Cross-domain investigations.
metadata:
  openclaw:
    emoji: "🎭"
    requires:
      bins: ["claude"]
      env: ["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"]
    version: "1.0.0"
    author: "Matthew Gordon"
    tags: ["agents", "teams", "claude-code", "orchestration", "coordination"]
---

# Claude Code Agent Teams

Claude Code Agent Teams允许多个Claude Code代理协同处理复杂的任务。这些代理通过共享的任务列表进行协调，直接相互通信，并在独立的范围内并行工作。

## 使用场景

✅ **适用于需要并行独立完成的任务：**
- 多角度的代码审查（安全、性能、测试同时进行）
- 基于不同假设的调试（同时测试多种理论）
- 全栈功能的开发（前端/后端/测试由不同的专家负责）
- 架构决策的讨论（通过对抗性辩论来生成更好的解决方案）
- 跨领域的性能分析（分析不同系统之间的瓶颈）
- 数据并行处理（如库存分类、批量重构）

❌ **不适用的场景：**
- 需要严格依赖关系的顺序性工作
- 对同一文件的编辑（存在冲突风险）
- 简单的任务（协调开销大于收益）
- 学习或探索性任务（单个代理拥有完整上下文时效果更好）

**经验法则：** 使用代理团队会使令牌使用成本增加3-4倍。仅在并行化的收益超过协调开销时才使用该功能。

## 快速入门

### 1. 启用该功能

**环境变量：**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**或通过设置文件`~/.claude/settings.json`：**
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 2. 验证设置

```bash
./scripts/validate-setup.sh
```

检查环境变量是否已设置，`claude` CLI是否可用，以及`tmux`是否已安装（可选）。

### 3. 选择模板

| 模板 | 使用场景 |
|----------|----------|
| `parallel-review.md` | 多角度代码审查（安全 + 性能 + 测试） |
| `competing-hypotheses.md` | 基于不同假设的调试 |
| `fullstack-feature.md` | 前端/后端/测试的协同开发 |
| `architecture-decision.md` | 通过对抗性辩论进行架构决策 |
| `bottleneck-analysis.md` | 跨领域性能分析 |
| `inventory-classification.md` | 数据并行分类/重构 |

每个模板都包含了使用场景、团队结构、生成团队的提示语以及预期结果。

### 4. 创建团队

```bash
claude --pty
# Paste spawn prompt from template
```

可以使用`./scripts/team-monitor.sh`（在单独的终端中）或`Ctrl+T`（在Claude Code中）来监控团队的运行情况。

## 核心原则

1. **明确的文件边界** – 每位团队成员负责不同的文件或目录（避免冲突）
2. **使用代理模式** – 由负责人协调，团队成员负责具体实施（在生成团队的提示语中说明）
3. **合理分配任务** – 每位团队成员负责5-6个独立的任务
4. **等待任务完成** – 在团队成员尚未完成任务时，负责人不得合并结果
5. **先进行调研** – 先创建研究型团队成员，再创建执行型团队成员，以建立共同的理解基础

## 成本管理

使用代理团队会使令牌使用量增加3-4倍。每位团队成员都有自己的上下文窗口。

**优化方法：**
- **任务分配策略**：负责人使用`Opus`模板（战略决策），团队成员使用`Sonnet`模板（战术决策），可节省约40%的成本
- **减少广播通信** – 仅发送必要的消息（广播会发送给所有团队成员）
- **合理调整团队规模** – 通常3位团队成员是最优配置；超过6位团队成员仅适用于高度并行的任务

详细策略请参见`references/cost-management.md`。

## 故障排除

**团队成员无法生成？**
- 确认`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`是否设置为1
- 设置环境变量后重新启动Claude Code

**文件冲突？**
- 在生成团队的提示语中明确指定文件边界（按目录划分文件所有权）

**负责人负责实施而非协调？**
- 在生成团队的提示语中添加“使用代理模式：协调但不负责实施”
- 或按`Shift+Tab`切换到代理模式

完整故障排除指南请参见`references/troubleshooting.md`。

## 自动化

**监控进度：**
```bash
./scripts/team-monitor.sh
```

**优雅关闭（清理操作）：**
```bash
./scripts/team-cleanup.sh
```

## 显示模式

**默认模式**（单窗口显示）：所有团队成员在同一终端中
- `Shift+Up/Down` – 选择团队成员
- `Ctrl+T` – 切换任务列表
- `Escape` – 中断当前团队成员的操作

**分屏模式**（需要tmux或iTerm2）：每位团队成员拥有自己的独立窗口
- 在`~/.claude/settings.json`中设置`teammateMode: "tmux"`

## 参考资料

- **`templates/`** – 6个预设的团队生成提示语及使用指南
- **`scripts/`** – 自动化辅助工具（用于验证、监控和清理）
- **`references/best-practices.md` – 使用团队的最佳实践
- **`references/cost-management.md` – 令牌使用优化策略
- **`references/troubleshooting.md` – 常见问题及解决方法**
- **`examples/` – 实际应用案例（代码审查、漏洞排查、功能开发）

## 对比

| 方法 | 适用场景 |
|----------|----------|
| 单次会话 | 顺序性工作、探索性任务 |
| 代理团队 | 需要协调的并行独立任务 |
| OpenClaw子代理 | 后台任务、长时间运行的任务 |

## 贡献方式

如果您发现了有用的模式，请提交PR，包括：
- 模板或示例代码
- 使用场景及团队结构
- 生成团队的提示语及预期结果

## 致谢

本功能的开发基于Claude Code文档、ClaudeFast的最佳实践以及OpenClaw社区的贡献。

---

**仓库地址：** https://github.com/matthew-a-gordon/claude-code-teams  
**许可证：** MIT