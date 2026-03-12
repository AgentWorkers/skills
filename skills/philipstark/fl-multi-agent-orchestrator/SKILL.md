---
name: multi-agent-orchestrator
description: 生产级多代理编排模式：将复杂任务分解为并行子任务，协调代理集群的工作流程，构建顺序执行的数据处理管道，并执行代码审查流程。这些模式已在实际代码库中经过严格测试，能够支持同时运行20到50个代理的复杂系统。
version: 1.0.0
license: MIT
author: felipe-lobo
tags: [agents, orchestration, parallel, swarm, pipeline, multi-agent, coordination, task-decomposition, fan-out, fan-in]
category: Agent-to-Agent Protocols
---
# 多智能体编排系统

我们是一个专业的多智能体编排系统，致力于帮助用户分解复杂任务、协调多个AI智能体，并通过适当的错误处理、资源管理和结果聚合来管理并行工作流程。

## 核心原则

1. **执行前先分解** — 在启动智能体之前，将复杂任务分解为依赖关系图。
2. **最小化共享状态** — 每个智能体应拥有自己的文件/资源；在不可避免的冲突情况下使用锁机制。
3. **优雅地处理失败** — 任何智能体都可能失败；编排系统必须处理重试、回退和部分结果。
4. **预算控制** — 跟踪每个智能体的成本，并实施严格的预算限制以防止成本失控。
5. **质量把关** — 使用高级模型（Opus）进行规划和审查；使用成本较低的模型（Haiku/Sonnet）执行具体任务。

## 编排模式

### 模式1：扇形展开/扇形聚合（并行研究）

**适用场景：** 多个独立的子任务可以同时运行，并在最后汇总结果。

**架构：**
```
                    ┌─── Agent A (research topic 1) ───┐
User Task ──► Planner ├─── Agent B (research topic 2) ───┤──► Aggregator ──► Result
                    └─── Agent C (research topic 3) ───┘
```

**实施步骤：**
1. 将任务分解为N个独立的子任务。
2. 为每个子任务分配一个具有特定提示和工具集的智能体。
3. 并行执行所有智能体（遵守最大并发限制）。
4. 汇总结果 — 合并输出、解决冲突，生成最终交付物。

**智能体提示模板：**
```
You are Agent [N] in a parallel research team.
Your ONLY task: [specific subtask description]
Scope: [specific files/topics to cover]
Output format: [structured format for aggregation]
DO NOT touch: [files/topics assigned to other agents]
Time budget: [max turns or time limit]
```

**错误处理：**
- 如果某个智能体失败，记录错误并继续执行其他智能体。
- 聚合器应记录哪些子任务的结果缺失。
- 失败的智能体最多重试2次，之后标记为失败。

**实际应用示例：** 使用5个智能体研究市场数据：一个负责竞争对手分析，一个负责SEO关键词分析，一个负责社区情绪分析，一个负责价格数据收集，一个负责技术趋势分析。聚合器将这些结果整合成一份策略文档。

---

### 模式2：顺序流水线

**适用场景：** 每个步骤都依赖于前一步的输出，需要按顺序处理任务。

**架构：**
```
Task ──► Agent A (generate) ──► Agent B (review) ──► Agent C (refine) ──► Agent D (test) ──► Result
```

**实施步骤：**
1. 定义具有明确输入/输出规范的阶段。
2. 顺序执行每个智能体 — 每个智能体都以前一个智能体的输出作为上下文。
3. 在阶段之间进行验证 — 在传递给下一个智能体之前检查输出是否有效。
4. 在关键失败情况下中断流程（如果代码无法编译，则不执行后续测试）。

**阶段规范模板：**
```
Stage: [name]
Input: [what this stage receives — file paths, text, structured data]
Agent model: [opus/sonnet/haiku based on complexity]
Tools allowed: [minimal set needed]
Output: [exact format the next stage expects]
Success criteria: [how to validate this stage passed]
Failure action: [retry / abort / skip]
```

**流水线定义示例：**
```yaml
pipeline:
  - stage: generate
    agent: coder
    model: sonnet
    input: "User requirements document"
    output: "Generated code files"
    tools: [Read, Write, Edit, Bash]

  - stage: review
    agent: reviewer
    model: opus
    input: "Generated code files from stage 1"
    output: "Review report with issues list"
    tools: [Read, Grep, Glob]

  - stage: fix
    agent: coder
    model: sonnet
    input: "Code files + review report"
    output: "Fixed code files"
    tools: [Read, Write, Edit]
    condition: "review.issues.length > 0"

  - stage: test
    agent: tester
    model: haiku
    input: "Final code files"
    output: "Test results"
    tools: [Read, Write, Bash]
```

**错误处理：**
- 每个阶段都有最大重试次数。
- 失败的阶段可以触发回滚（撤销文件更改）。
- 即使部分失败，流水线也会生成报告。

---

### 模式3：群体协作（自主智能体，共享目标）

**适用场景：** 大规模任务，多个智能体同时处理相同的代码库。

**架构：**
```
┌──────────────────────────────────────────┐
│            Swarm Orchestrator            │
│                                          │
│  Wave 1: ┌────────┐ ┌────────┐          │
│           │ Agent 1 │ │ Agent 2 │ (parallel)
│           │ coder   │ │ coder   │          │
│           └────┬────┘ └────┬────┘          │
│  Wave 2:       └─────┬─────┘              │
│                ┌─────▼─────┐              │
│                │  Agent 3  │ (depends)    │
│                │  tester   │              │
│                └─────┬─────┘              │
│  Wave 3:       ┌─────▼─────┐              │
│                │  Agent 4  │ (depends)    │
│                │  reviewer │              │
│                └───────────┘              │
│                                          │
│  File Locks: {auth.ts -> Agent 1}        │
│  Budget: $0.23 / $5.00                   │
└──────────────────────────────────────────┘
```

**关键协调机制：**
1. **文件锁定** — 在智能体修改文件之前，它必须先获取文件锁。其他智能体需要等待或处理其他文件。
   ```
   Lock table:
     src/auth.ts       -> Agent 1 (locked)
     src/middleware.ts  -> Agent 2 (locked)
     src/routes.ts     -> available
   ```

2. **依赖关系图** — 使用拓扑排序确定执行顺序。
   ```
   Wave 1: [task-1, task-2, task-3]  (no dependencies — run in parallel)
   Wave 2: [task-4]                   (depends on task-1 and task-2)
   Wave 3: [task-5]                   (depends on task-4)
   ```

3. **预算控制** — 跟踪所有智能体的累计成本。达到预算阈值时取消待定任务。
4. **冲突解决** — 如果两个智能体需要同一个文件，让其中一个智能体的执行依赖于另一个智能体的结果。禁止两个智能体同时编辑同一个文件。

**群体协作配置模板：**
```yaml
swarm:
  name: full-stack-refactor
  max_concurrent: 4
  budget_usd: 5.0
  retry_per_task: 2

agents:
  coder:
    model: sonnet
    tools: [Read, Write, Edit, Bash, Grep, Glob]
  reviewer:
    model: opus
    tools: [Read, Grep, Glob]
  tester:
    model: haiku
    tools: [Read, Write, Bash]

tasks:
  - id: task-1
    type: coder
    description: "Refactor auth module"
    files: [src/auth.ts, src/auth.test.ts]
    dependencies: []

  - id: task-2
    type: coder
    description: "Refactor middleware"
    files: [src/middleware.ts]
    dependencies: []

  - id: task-3
    type: tester
    description: "Write integration tests"
    files: [tests/integration.test.ts]
    dependencies: [task-1, task-2]

  - id: task-4
    type: reviewer
    description: "Review all changes"
    files: []
    dependencies: [task-1, task-2, task-3]
```

---

### 模式4：审查循环（构建-审查-修复循环）

**适用场景：** 需要迭代改进的任务，通过多次审查和优化来达到质量标准。

**架构：**
```
         ┌──────────────────────────────────┐
         │                                  │
         ▼                                  │
Task ──► Builder Agent ──► Reviewer Agent ──┤──► (pass) ──► Result
                                            │
                                   (fail + feedback)
```

**实施步骤：**
1. **构建者** 创建初始输出（代码、内容、分析结果）。
2. **审查者** 根据标准进行评估并给出评分和反馈。
3. **如果评分低于阈值**，构建者根据反馈进行迭代。
4. 设置最大迭代次数（通常为3轮）以防止无限循环。
5. **最终输出** 包含审查历史记录，以确保透明度。

**审查标准模板：**
```
Review this output against these criteria (score 1-10 each):

1. Correctness: Does it work? Are there bugs?
2. Completeness: Does it cover all requirements?
3. Code quality: Is it clean, maintainable, well-structured?
4. Security: Any vulnerabilities or unsafe patterns?
5. Performance: Any obvious bottlenecks?

Overall score (1-10):
Verdict: PASS (>= 7) or FAIL (< 7)

If FAIL, provide specific feedback:
- Issue 1: [description] → [suggested fix]
- Issue 2: [description] → [suggested fix]
```

**循环控制：**
```
max_iterations: 3
pass_threshold: 7
escalation: "If still failing after max iterations, flag for human review"
```

## 任务分解协议

当用户提交一个复杂任务时，请遵循以下分解步骤：

### 第1步：分析任务范围
- 用户的具体需求是什么？
- 包含多少个独立的子任务？
- 子任务之间有哪些依赖关系？
- 每个子任务会修改哪些文件/资源？

### 第2步：选择合适的模式
- **子任务独立？** → 选择扇形展开/扇形聚合模式。
- **步骤之间存在依赖关系？** → 选择顺序流水线模式。
- **共享代码库，需要多次修改？** → 选择群体协作模式。
- **结果对质量要求较高？** → 选择审查循环模式。
- **项目复杂？** → 结合使用多种模式（例如：群体协作 + 审查循环）。

### 第3步：制定执行计划
生成一个结构化的执行计划：
```json
{
  "pattern": "swarm|pipeline|fan-out|review-cycle|hybrid",
  "total_agents": 4,
  "estimated_cost_usd": 0.50,
  "max_concurrent": 3,
  "tasks": [
    {
      "id": "task-1",
      "description": "What this agent does",
      "agent_type": "coder|reviewer|tester|researcher|documenter",
      "model": "opus|sonnet|haiku",
      "dependencies": [],
      "files_to_modify": ["src/auth.ts"],
      "tools": ["Read", "Write", "Edit"],
      "prompt": "Detailed agent instructions...",
      "retry_count": 2,
      "timeout_minutes": 5
    }
  ],
  "aggregation_strategy": "How to combine results",
  "quality_gate": {
    "enabled": true,
    "model": "opus",
    "pass_threshold": 7
  }
}
```

### 第4步：执行任务
- 根据依赖关系图启动智能体。
- 监控进度和成本。
- 使用重试和回退机制处理失败情况。
- 汇总结果。

### 第5步：生成报告
生成一份总结报告：
```
Orchestration Report
====================
Pattern: Swarm
Tasks: 4/4 completed
Agents used: 4
Total cost: $0.45
Duration: 32s
Quality gate: PASS (8/10)

Results:
- task-1 (coder): Refactored auth module [COMPLETED - $0.12]
- task-2 (coder): Refactored middleware [COMPLETED - $0.08]
- task-3 (tester): Integration tests [COMPLETED - $0.15]
- task-4 (reviewer): Code review [COMPLETED - $0.10]
```

## 模型选择策略

| 角色 | 推荐模型 | 原因 |
|------|-------------------|-----|
| 任务分解/规划 | Opus | 需要对依赖关系和架构进行深入分析 |
| 代码生成/修改 | Sonnet | 在代码生成任务中，性能与成本平衡良好 |
| 测试/简单任务 | Haiku | 对于范围明确的任务，速度快且成本低 |
| 代码审查/质量把关 | Opus | 需要全面了解情况并发现细微问题 |
| 文档编写 | Sonnet | 需要良好的写作能力，但不需要深入分析 |
| 研究/分析 | Sonnet | 需要广泛的知识覆盖 |

**成本优化规则：** 仅在规划和审查阶段使用Opus模型（最多使用2次）。其他任务使用Haiku/Sonnet模型。这样通常可以将成本降低60-70%。

## 安全性与隔离

### 智能体隔离规则
1. **最小化工具集** — 每个智能体只获取所需的工具。审查者不应具有写入/编辑权限。
2. **文件访问限制** — 明确指定每个智能体可以访问的文件范围。智能体不应修改超出其权限范围的文件。
3. **禁止访问敏感信息** — 智能体不得读取.env文件、凭证或API密钥。在工具使用前进行相应的限制。
4. **实施预算限制** — 为每个智能体设置预算上限，并设定总预算限制。超出预算的智能体会被终止。
5. **超时机制** — 为每个智能体设置最大执行次数（通常为10-20次），以防止无限循环。

### 资源限制模板
```yaml
limits:
  per_agent:
    max_turns: 20
    max_budget_usd: 0.50
    timeout_minutes: 5
    allowed_tools: [Read, Write, Edit, Bash, Grep, Glob]
    blocked_files: ["*.env", "*.key", "*.pem", "credentials.*"]
  total:
    max_agents: 8
    max_budget_usd: 5.00
    max_duration_minutes: 30
```

## 错误处理与恢复

### 失败类型及应对措施

| 失败类型 | 检测方式 | 应对措施 |
|---------|-----------|----------|
| 智能体超时 | 执行次数超过上限 | 终止该智能体，用新的智能体重新尝试任务 |
| 智能体错误 | 执行过程中出现异常 | 重试最多N次，然后标记为失败 |
| 预算超出 | 累计成本超过限制 | 取消所有待定任务，仅报告部分结果 |
| 文件冲突 | 两个智能体同时尝试修改同一个文件 | 阻止后续的智能体执行，等待第一个智能体完成 |
| 审查失败 | 审查评分未达到标准 | 将审查结果反馈给构建者，重新开始审查循环 |
| 重试次数用尽 | 重试次数达到上限 | 将任务标记为失败，继续执行其他不相关的任务 |

### 部分成功策略
并非所有任务都必须成功才能使整个编排过程有价值。当任务失败时：
1. 完成所有仍可执行的独立任务。
2. 报告失败的任务及其原因。
3. 提供已成功完成的部分结果。
4. 提供针对失败部分的手动修复建议。

## 高级模式

### 混合模式：群体协作 + 审查循环
对于需要质量保证的大规模重构项目：
1. 将任务分解为多个群体协作任务。
2. 分阶段执行这些任务。
3. 所有任务完成后，对合并后的结果进行审查。
4. 如果审查失败，创建针对性的修复任务并再次执行群体协作流程。

### 动态扩展
根据任务复杂度逐步增加智能体数量：
```
if task_count <= 3: max_concurrent = 2
elif task_count <= 6: max_concurrent = 4
elif task_count <= 12: max_concurrent = 6
else: max_concurrent = 8
```

### 智能体之间的上下文传递
当智能体B需要智能体A提供的上下文时：
1. 智能体A将其输出写入特定文件（例如：`.orchestrator/task-1-output.md`）。
2. 智能体B的提示中包含：“读取`.orchestrator/task-1-output.md`以获取前一个阶段的上下文”。
3. 这种方式可以避免在提示之间复制大量输出数据时造成的资源浪费。

## 快速参考

### 选择合适的模式
```
Is the task decomposable into independent parts?
  YES → Are there more than 5 parts?
    YES → Swarm (with file locking)
    NO  → Fan-Out/Fan-In
  NO → Is the output quality-critical?
    YES → Review Cycle (build-review-fix)
    NO  → Pipeline (sequential stages)
```

### 最小化部署的编排方案
对于简单的2-3个智能体的场景，不需要完整的群体协作基础设施：
1. 智能体1：执行任务（使用Sonnet模型）。
2. 智能体2：审查任务（使用Opus模型）。
3. 如果审查失败，智能体1根据反馈进行修复。
就这么简单。不要过度设计。