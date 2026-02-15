---
name: autonomous-skill-orchestrator
description: >
  Deterministically coordinates autonomous planning and execution across available skills under
  strict guardrails. Use only when the user explicitly activates this skill by name to run
  autonomously until a stop command is issued. Trigger keywords include: "use autonomous-skill-orchestrator",
  "activate autonomous-skill-orchestrator", "start autonomous orchestration".
metadata:
  version: "2.0.0"
  owner: "user"
  inspired_by: "oh-my-opencode (Sisyphus, Atlas, Prometheus)"
---

# 自主技能编排器 v2.0

> 受 oh-my-opencode 三层架构的启发，专为 OpenClaw 生态系统进行了适配。

## 核心理念

传统的 AI 模式是：用户提出请求 → AI 进行响应。但在处理复杂任务时，这种模式会遇到以下问题：
1. **上下文过载**：大型任务超出了 AI 的处理范围；
2. **认知偏差**：AI 在执行过程中容易偏离目标；
3. **验证缺失**：缺乏系统的完整性检查；
4. **人为瓶颈**：需要持续的人工干预。

我们的技能通过 **专业化与任务分解** 来解决这些问题。

---

## 架构

```
┌─────────────────────────────────────────────────────────┐
│  PLANNING LAYER (Interview + Plan Generation)          │
│  • Clarify intent through interview                     │
│  • Generate structured work plan                        │
│  • Review plan for gaps                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER (Atlas - The Conductor)           │
│  • Read plan, delegate tasks                            │
│  • Accumulate wisdom across tasks                       │
│  • Verify results independently                         │
│  • NEVER write code directly — only delegate            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  EXECUTION LAYER (Sub-agents via sessions_spawn)       │
│  • Focused task execution                               │
│  • Return results + learnings                           │
│  • Isolated context per task                            │
└─────────────────────────────────────────────────────────┘
```

---

## 激活方式

### 显式触发命令
- `use autonomous-skill-orchestrator`
- `activate autonomous-skill-orchestrator`
- `start autonomous orchestration`
- `ulw` 或 `ultrawork`（魔法关键词模式）

### 魔法关键词：`ultrawork` / `ulw`
在命令中包含 `ultrawork` 或 `ulw` 即可自动进入全自动化编排模式。其余工作将由系统自动完成——包括并行任务的分配、后台任务的执行以及持续的执行，直至任务完成。

---

## 第一阶段：规划（Prometheus 模式）

### 第 1.1 步：访谈
在开始规划之前，通过简短的访谈来明确需求：

**仅询问必要的信息：**
- 核心目标是什么？
- 任务的边界是什么（哪些不在计划范围内）？
- 有哪些约束条件或偏好？
- 如何判断任务是否完成？

**根据不同目的进行访谈：**
| 目的 | 重点 | 例题 |
|--------|-------|-------------------|
| **重构** | 安全性 | “有哪些测试可以验证当前的行为？” |
| **新建** | 设计模式 | “是遵循现有规范还是进行创新？” |
| **调试/修复** | 问题重现 | “问题重现的步骤是什么？错误信息是什么？” |
| **研究** | 任务范围 | “是追求深度还是广度？时间上有何限制？” |

### 第 1.2 步：制定计划
访谈结束后，生成结构化的计划：

```markdown
## Work Plan: [Title]

### Objective
[One sentence, frozen intent]

### Tasks
- [ ] Task 1: [Description]
  - Acceptance: [How to verify completion]
  - References: [Files, docs, skills needed]
  - Category: [quick|general|deep|creative]
  
- [ ] Task 2: ...

### Guardrails
- MUST: [Required constraints]
- MUST NOT: [Forbidden actions]

### Verification
[How to verify overall completion]
```

### 第 1.3 步：计划审核（自我检查）
在执行前，需要验证以下内容：
- 每个任务都有明确的验收标准；
- 参考资料具体明确（不模糊不清）；
- 任务范围没有超出最初设定的目标；
- 任务之间的依赖关系清晰明确；
- 防范措施切实可行。

如果任何一项检查未通过，请在继续执行前完善计划。

---

## 第二阶段：编排（Atlas 模式）

### 编排规则
- 编排器能够读取文件以理解任务背景；
- 编排器可以运行命令来验证执行结果；
- 编排器可以使用 grep/glob 等工具搜索相关信息；
- 编排器可以创建子代理来执行具体任务。

**注意：**
- 编排器 **严禁** 直接编写或修改代码；
- 编排器 **严禁** 盲目信任子代理的报告结果；
- 编排器 **严禁** 跳过任何验证步骤。

### 第 2.1 步：任务分配
使用 `sessions_spawn` 命令，并根据任务类别配置相应的参数：

| 任务类别 | 适用场景 | 所需模型 | 最大执行时间 |
|----------|---------|------------|---------|
| `quick` | 简单任务、单文件修改 | 快速模型 | 2-5 分钟 |
| `general` | 标准实现 | 默认模型 | 5-10 分钟 |
| `deep` | 复杂逻辑、架构设计 | 高级模型 | 10-20 分钟 |
| `creative` | 用户界面/用户体验设计、内容生成 | 创意模型 | 5-10 分钟 |
| `research` | 文档编写、代码库探索 | 需要广泛搜索的信息 | 5 分钟 |

**任务分配模板：**
```
sessions_spawn(
  label: "task-{n}-{short-desc}",
  task: """
  ## Task
  {exact task from plan}
  
  ## Expected Outcome
  {acceptance criteria}
  
  ## Context
  {accumulated wisdom from previous tasks}
  
  ## Constraints
  - MUST: {guardrails}
  - MUST NOT: {forbidden actions}
  
  ## References
  {relevant files, docs}
  """,
  runTimeoutSeconds: {based on category}
)
```

### 第 2.2 步：并行执行
识别出没有文件冲突、也没有依赖关系的独立任务，并同时启动它们：

```
# Tasks 2, 3, 4 have no dependencies
sessions_spawn(label="task-2", task="...")
sessions_spawn(label="task-3", task="...")
sessions_spawn(label="task-4", task="...")
# All run in parallel
```

### 第 2.3 步：知识积累
每个任务完成后，提取并记录相关的经验与知识：

```markdown
## Wisdom Log

### Conventions Discovered
- [Pattern found in codebase]

### Successful Approaches
- [What worked]

### Gotchas
- [Pitfalls to avoid]

### Commands Used
- [Useful commands for similar tasks]
```

将这些知识保存到 `memory/orchestrator-wisdom.md` 文件中（会话期间仅允许追加内容）。

并将这些知识传递给所有后续的子代理。

### 第 2.4 步：独立验证
**切勿盲目信任子代理的报告结果**。每个任务完成后，需要执行以下操作：
1. 查看实际被修改的文件；
2. 如有必要，运行测试或代码检查工具；
3. 独立验证任务是否达到验收标准；
4. 将结果与计划要求进行对比。

如果验证失败：
- 将失败情况记录在 `memory/orchestrator-wisdom.md` 中；
- 重新分配任务，并提供失败的具体原因；
- 每个任务最多允许重试两次，之后需要用户介入处理。

---

## 第三阶段：任务完成

### 第 3.1 步：最终验证
- 确保所有任务都已完成；
- 所有验收标准都得到满足；
- `memory/orchestrator-wisdom.md` 中没有未解决的问题。

### 第 3.2 步：生成总结报告
```markdown
## Orchestration Complete

### Completed Tasks
- [x] Task 1: {summary}
- [x] Task 2: {summary}

### Learnings
{key wisdom accumulated}

### Files Changed
{list of modified files}

### Next Steps (if any)
{recommendations}
```

---

## 安全防护机制

### 停止条件（立即停止）
- 用户发出明确的停止命令；
- 检测到不可逆的破坏性操作；
- 任务范围超出最初设定的范围；
- 连续三次任务失败；
- 子代理尝试创建更多的子代理（禁止递归调用）。

### 风险分类
| 风险等级 | 描述 | 应对措施 |
|-------|-------------|--------|
| A | 不可逆、具有破坏性或无限制的行为 | 立即停止 |
| B | 有明确界限、可以通过澄清解决 | 暂停操作，询问用户 |
| C | 仅影响外观、不影响功能 | 继续执行，但需记录异常情况 |

### 禁止的操作
- 创建新的自主技能编排器；
- 修改本技能相关的配置文件；
- 无必要时访问系统权限；
- 调用不在原始计划范围内的外部 API；
- 递归地创建子代理（禁止子代理再创建其他子代理）。

---

## 停止命令
用户可以使用以下命令随时停止任务：
- `stop`
- `halt`
- `cancel orchestration`
- `abort`

停止命令执行后，系统会立即终止所有正在运行的任务，输出已完成工作的总结，并等待新的指令。

---

## 数据存储与整合

### 在编排过程中
- 将学习到的内容追加到 `memory/orchestrator-wisdom.md` 文件中；
- 在执行过程中参考之前的记录以获取上下文信息。

### 编排结束后
- 每天更新 `memory/orchestrator-wisdom.md` 文件，记录编排过程中的重要信息；
- 如果有价值的内容，会将其保存到 `MEMORY.md` 文件中。

---

## 使用示例

**简单使用（使用魔法关键词）：**
```
ulw refactor the authentication module to use JWT
```

**显式激活命令：**
```
activate autonomous-skill-orchestrator

Build a REST API with user registration, login, and profile endpoints
```

**在有约束条件的情况下使用：**
```
use autonomous-skill-orchestrator
- Build payment integration with Stripe
- MUST: Use existing database patterns
- MUST NOT: Store card numbers locally
- Deadline: Complete core flow only
```