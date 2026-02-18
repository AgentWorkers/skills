---
name: agent-orchestrator
version: 1.0.2
author: molter-white
description: 多智能体编排的五种成熟模式：工作小组（Work Crew）、监督者（Supervisor）、流水线（Pipeline）、决策委员会（Council）和自动路由（Auto-Routing）
license: MIT
tags: multi-agent,orchestration,automation,productivity,ai-workflow
compatibility: OpenClaw 0.8+
---
# agent-orchestrator

这是一个用于 OpenClaw 的多智能体协调系统，实现了五种经过验证的智能体协作模式：工作小组（Work Crew）、监督者（Supervisor）、流水线（Pipeline）、专家委员会（Expert Council）和自动路由（Auto-Routing）。

**适用场景：**
- 需要对任务进行并行处理以提高效率或实现冗余（工作小组模式）。
- 复杂任务需要动态规划和任务分配（监督者模式）。
- 任务执行遵循可预测的阶段顺序（流水线模式）。
- 需要从多个专家那里获取跨领域的输入（专家委员会模式）。
- 混合类型的任务需要自动路由到相应的专家（自动路由模式）。
- 研究任务需要从多个角度进行广度优先的探索。
- 高风险决策需要通过多方面的观点来确保决策的准确性。

**不适用场景：**
- 任务简单，可以在单个智能体的处理范围内完成（请使用主会话模式）。
- 任务是顺序执行的，且没有并行处理的必要（请使用常规的工具调用方式）。
- 一次性、确定性的任务（请使用单个智能体处理）。
- 需要实时智能体间通信的任务（本系统采用异步任务调度机制）。
- 任务处理所需的代币成本过高，不值得投入（请避免使用多智能体模式）。
- 任务简单快速，协调开销大于收益的情况（请避免使用多智能体模式）。

**输出结果：**
- 来自多个并行智能体的汇总结果。
- 综合后的共识建议。
- 将任务路由到相应的专家。
- 经过分阶段处理后的结构化输出结果。

## 决策矩阵

| 模式        | 适用场景                | 避免场景                |
|-------------|-------------------|---------------------|
| **工作小组（Crew）** | 从多个角度处理相同任务、验证结果、需要广泛的研究 | 结果难以比较或合并             |
| **监督者（Supervisor）** | 需要动态任务分解、复杂任务规划        | 固定的工作流程、简单的任务分配        |
| **流水线（Pipeline）** | 有明确顺序的阶段、内容创建        | 路径需要在运行时进行调整         |
| **专家委员会（Council）** | 需要跨领域专业知识、风险评估、政策审查    | 单一领域的任务、需要快速达成共识       |
| **自动路由（Route）** | 混合类型的任务、需要自动分类        | 任务类型已经明确             |

## 自动路由模式

`route` 命令会分析任务类型，并自动将任务分配给相应的专家：

```bash
# Basic routing
claw agent-orchestrator route --task "Write Python parser"

# With custom specialist pool
claw agent-orchestrator route \
  --task "Analyze data and create report" \
  --specialists "analyst,data,writer"

# Force specific specialist
claw agent-orchestrator route \
  --task "Something complex" \
  --force coder
```

### 信心阈值

- **高信心（>0.85）**：立即自动路由任务。
- **良好信心（0.7-0.85）**：提供选择后需要确认的选项。
- **中等信心（0.5-0.7）**：显示多个可选方案供参考。
- **低信心（<0.5）**：请求进一步澄清。

可用的专家类型：编码员（coder）、研究员（researcher）、写手（writer）、分析师（analyst）、规划师（planner）、审稿人（reviewer）、创意人员（creative）、数据专家（data）、DevOps 专家（devops）、支持人员（support）。

## 常见工作流程

```bash
# Parallel research with consensus
claw agent-orchestrator crew \
  --task "Research Bitcoin Lightning 2026 adoption" \
  --agents 4 \
  --perspectives technical,business,security,competitors \
  --converge consensus

# Best-of redundancy for critical analysis
claw agent-orchestrator crew \
  --task "Audit this smart contract for vulnerabilities" \
  --agents 3 \
  --converge best-of

# Supervisor-managed code review
claw agent-orchestrator supervise \
  --task "Refactor authentication module" \
  --workers coder,reviewer,tester \
  --strategy adaptive

# Staged content pipeline
claw agent-orchestrator pipeline \
  --stages research,draft,review,finalize \
  --input "topic: AI agent adoption trends"

# Expert council for decision
claw agent-orchestrator council \
  --question "Should we publish this blog post about unreleased features?" \
  --experts skeptic,ethicist,strategist \
  --converge consensus \
  --rounds 2

# Auto-route mixed tasks
claw agent-orchestrator route \
  --task "Write Python function to analyze CSV data" \
  --specialists coder,researcher,writer,analyst

# Force route to specific specialist
claw agent-orchestrator route \
  --task "Debug authentication error" \
  --force coder \
  --confidence-threshold 0.9

# Route and output as JSON for scripting
claw agent-orchestrator route \
  --task $TASK \
  --format json \
  --specialists "coder,data,analyst"
```

## 错误示例：

**不要**：对于简单的问题使用“工作小组”模式（因为只需要单一答案）。
**不要**：在“流水线”模式足够适用的情况下使用“监督者”模式。
**不要**：当任务类型已经明确时使用自动路由功能。
**不要**：对于非常简单的任务使用多智能体协作模式。

## 注意事项：**
- 多智能体模式使用的代币数量大约是单智能体模式的 15 倍。仅适用于那些通过提高质量能够带来显著收益的高价值任务。参考 Anthropic 的研究：代币使用情况可以解释复杂任务中 80% 的性能差异。

## 所需依赖库/工具：
- Python 3.8 及以上版本。
- OpenClaw 的 `spawn` 功能。
- OpenClaw 的 `sessions_list` 功能。
- OpenClaw 的 `sessions_history` 功能。

**相关文件：**
- `__main__.py`：命令行接口的入口文件。
- `crew.py`：实现“工作小组”模式的核心代码。
- `supervise.py`：实现“监督者”模式的代码（第二阶段）。
- `council.py`：实现“专家委员会”模式的代码（第二阶段）。
- `pipeline.py`：实现“流水线”模式的代码（第二阶段）。
- `route.py`：实现“自动路由”模式的代码（第二阶段）。
- `utils.py`：用于会话管理的通用工具模块。

## 系统现状：
- 最小可行产品（MVP）：已实现“工作小组”模式。
- **第二阶段：100% 完成**
  - [√] 已实现“监督者”模式：支持动态任务分解和任务分配。
  - [√] 已实现“流水线”模式：包含顺序处理和验证机制。
  - [√] 已实现“专家委员会”模式：支持多专家讨论和共识形成。
  - [√] 已实现“自动路由”模式：支持智能任务分类和专家路由。

## 参考文献：
- Anthropic 多智能体研究系统。
- LangGraph 监督者模式。
- CrewAI 框架。
- AutoGen 对话式智能体系统。