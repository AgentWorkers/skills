---
name: agent-orchestrator
version: 1.0.5
author: molter-white
description: 多智能体编排的五种成熟模式：工作小组（Work Crew）、监督者（Supervisor）、流水线（Pipeline）、决策委员会（Council）以及自动路由（Auto-Routing）
license: MIT
tags: multi-agent,orchestration,automation,productivity,ai-workflow
compatibility: OpenClaw 0.8+
---
# agent-orchestrator

OpenClaw的多智能体协调系统。实现了5种经过验证的智能体协作模式：工作小组（Work Crew）、监督者（Supervisor）、流水线（Pipeline）、专家委员会（Expert Council）和自动路由（Auto-Routing）。

**适用场景：**
- 需要并行处理任务以提高效率或实现冗余（工作小组模式）
- 复杂任务需要动态规划和任务分配（监督者模式）
- 任务遵循可预测的流程阶段（流水线模式）
- 需要跨领域专家的输入（专家委员会模式）
- 混合类型的任务需要自动路由到相应的专家（自动路由模式）
- 研究任务需要从多个角度进行广度优先的探索
- 高风险决策需要通过多方面的观点来提高决策的准确性

**不适用场景：**
- 适合单个智能体处理的简单任务（请使用主会话模式）
- 无法并行化的顺序任务（请使用常规工具调用）
- 一次性、确定性的任务（请使用单个智能体）
- 需要实时智能体间交流的任务（本系统采用异步启动机制）
- 任务所需的代币成本过高，无法承受
- 协调开销超过收益的快速/简单任务

**输出结果：**
- 来自多个并行智能体的汇总结果
- 综合后的共识建议
- 任务到相应专家的路由决策
- 分阶段处理的结构化输出

## 决策矩阵

| 模式 | 适用场景 | 避免场景 |
|---------|----------|------------|
| **工作小组** | 从多个角度处理相同任务、验证结果、广泛的研究 | 结果难以比较或合并 |
| **监督者** | 需要动态任务分解和复杂规划 | 工作流程固定、任务分配简单 |
| **流水线** | 有明确顺序的阶段、内容创建 | 路径需要实时调整 |
| **专家委员会** | 需要跨领域专业知识、风险评估、政策审查 | 单一领域任务、需要快速达成共识 |
| **自动路由** | 混合类型的工作负载、自动任务分类 | 任务类型已知 |

## 自动路由模式

`route`命令会分析任务并根据类型自动对其进行分类，然后将其路由到相应的专家：

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

- **高信心（>0.85）**：立即自动路由
- **良好信心（0.7-0.85）**：提供选择后确认的选项
- **中等信心（0.5-0.7）**：显示最佳替代方案
- **低信心（<0.5）**：请求进一步澄清

可用专家：编码员、研究员、写手、分析师、规划师、审稿人、创意人员、数据分析师、DevOps工程师、支持人员

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

## 不当使用示例

**不要：对简单的问题使用工作小组模式**
```bash
# WRONG: Wasteful for simple facts
claw agent-orchestrator crew --task "What is 2+2?" --agents 3

# RIGHT: Use main session directly
What is 2+2?
```

**不要：在流水线模式足够的情况下使用监督者模式**
```bash
# WRONG: Over-engineering fixed workflows
claw agent-orchestrator supervise --task "Draft, edit, publish"

# RIGHT: Use pipeline for fixed sequences
claw agent-orchestrator pipeline --stages draft,edit,publish
```

**不要：在任务类型明确的情况下使用自动路由模式**
```bash
# WRONG: Unnecessary classification overhead
claw agent-orchestrator route --task "Write Python code"

# RIGHT: Direct to appropriate specialist
claw agent-orchestrator crew --pattern code --task "Write Python code"
```

**不要：对非常简单/小规模的任务使用多智能体模式**
```bash
# WRONG: Coordination overhead exceeds value
claw agent-orchestrator crew --task "Fix typo" --agents 2

# RIGHT: Single agent or direct edit
edit file.py "typo" "correct"
```

## 代币成本警告

多智能体模式使用的代币数量大约是单智能体模式的15倍。仅适用于那些通过提高质量能够带来显著收益的高价值任务。参考Anthropic的研究：代币使用情况可以解释复杂任务中80%的性能差异。

## 所需依赖项：
- Python 3.8及以上版本
- OpenClaw的`spawn`功能
- OpenClaw的`sessions_list`功能
- OpenClaw的`sessions_history`功能

## 相关文件：
- `__main__.py` - 命令行接口入口
- `crew.py` - 工作小组模式实现
- `supervise.py` - 监督者模式（第二阶段）
- `council.py` - 专家委员会模式（第二阶段）
- `pipeline.py` - 流水线模式（第二阶段）
- `route.py` - 自动路由模式（第二阶段）
- `utils.py` - 用于会话管理的共享工具库

## 状态：
- MVP：工作小组模式已实现
- **第二阶段：100%完成**
  - [x] 监督者模式实现 - 动态任务分解和任务分配
  - [x] 流水线模式实现 - 有序的分阶段处理及验证机制
  - [x] 专家委员会模式实现 - 多专家讨论及共识形成机制
  - [x] 自动路由模式实现 - 智能任务分类和专家路由

## 参考文献：
- Anthropic多智能体研究系统
- LangGraph监督者模式
- CrewAI框架
- AutoGen对话式智能体