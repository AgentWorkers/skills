---
name: agent-os
description: OpenClaw的持久化代理操作系统：代理能够在不同会话之间保持状态，从经验中学习，并在复杂项目中协同工作，避免重复劳动。
---
# Agent OS — 持久化代理操作系统

这些代理能够记住任务、学习新知识并协同工作。

## 功能概述

Agent OS 支持多代理项目执行，并具备持久化内存功能：

- **代理内存**：每个代理都会记录过去的任务、学习到的经验以及任务的成功率。
- **任务分解**：将高层次的目标分解为可执行的任务序列。
- **智能路由**：根据代理的能力将任务分配给合适的代理。
- **执行跟踪**：提供实时进度显示，展示每个代理的当前工作状态。
- **状态持久化**：项目状态在重启后仍可保留（允许在项目中途恢复执行）。

## 快速入门

### 安装

```bash
clawhub install nova/agent-os
```

### 基本使用

```javascript
const { AgentOS } = require('agent-os');

const os = new AgentOS('my-project');

// Register agents with capabilities
os.registerAgent('research', '🔍 Research', ['research', 'planning']);
os.registerAgent('design', '🎨 Design', ['design', 'planning']);
os.registerAgent('dev', '💻 Development', ['development']);

os.initialize();

// Run a project
const result = await os.runProject('Build a feature', [
  'planning',
  'design',
  'development',
]);

console.log(result.progress); // 100
```

## 核心概念

### 代理（Agent）
- **持久化内存**：存储过去的任务、学习经验及任务成功率。
- **状态**：当前正在执行的任务、进度以及遇到的障碍。
- **能力**：代理所擅长的工作类型（如研究、设计、开发等）。

### TaskRouter
- 将项目目标分解为可执行的任务。
- 根据代理的能力将任务分配给相应的代理。
- 确保任务之间的依赖关系得到满足（例如：任务 A 必须先完成才能开始任务 B）。

### Executor
- 顺序执行任务。
- 实时跟踪任务进度。
- 保持状态信息，确保项目在重启后仍能继续执行。
- 处理执行过程中遇到的障碍和错误。

### AgentOS
- 负责协调所有代理的活动：
- 注册代理。
- 初始化系统。
- 运行项目。
- 提供项目状态信息。

## 架构

```
AgentOS (top-level orchestration)
├── Agent (persistent worker)
│   ├── Memory (lessons, capabilities, history)
│   └── State (current task, progress)
├── TaskRouter (goal decomposition)
│   ├── Templates (planning, design, development, etc.)
│   └── Matcher (task → agent assignment)
└── Executor (task execution)
    ├── Sequential runner
    ├── Progress tracking
    └── State persistence
```

## 状态持久化

所有项目状态数据都保存在 `data/` 目录中：
- `[agent-id]-memory.json`：代理的知识库。
- `[agent-id]-state.json`：代理的当前状态。
- `[project-id]-project.json`：项目的任务列表及状态信息。

**这意味着：**
- 项目在重启后仍可继续执行。
- 代理能够记住之前的工作内容。
- 可以在项目中途无缝恢复执行。

## 文件结构

```
agent-os/
├── core/
│   ├── agent.js          # Agent class
│   ├── task-router.js    # Task decomposition
│   ├── executor.js       # Execution scheduler
│   └── index.js          # AgentOS class
├── ui/
│   ├── dashboard.html    # Live progress UI
│   ├── dashboard.js      # Dashboard logic
│   └── style.css         # Styling
├── examples/
│   └── research-project.js  # Full working example
├── data/                 # Auto-created (persistent state)
└── package.json
```

## API 参考

### AgentOS

```javascript
new AgentOS(projectId?)
registerAgent(id, name, capabilities)
initialize()
runProject(goal, taskTypes)
getStatus()
getAgentStatus(agentId)
toJSON()
```

### Agent

```javascript
startTask(task)
updateProgress(percentage, message)
completeTask(output)
setBlocker(message)
recordError(error)
learnLesson(category, lesson)
reset()
getStatus()
```

### TaskRouter

```javascript
decompose(goal, taskTypes)
matchAgent(taskType)
getTasksForAgent(agentId, tasks)
canExecuteTask(task, allTasks)
getNextTask(tasks)
completeTask(taskId, tasks, output)
getProjectStatus(tasks)
```

### Executor

```javascript
initializeProject(goal, taskTypes)
execute()
executeTask(task)
getStatus()
```

## 示例：研究 + 设计 + 开发

请参考 `examples/research-project.js` 以了解具体示例：
- 3 个具有不同能力的代理。
- 12 个分布在三个阶段（规划、设计、开发）的任务。
- 任务的顺序执行及进度跟踪。
- 状态数据保存到磁盘。
- 最终的状态报告。

**预期输出：**
```
✅ Registered 3 agents
📋 Task Plan: 12 tasks
🚀 Starting execution...
✅ [Task 1] Complete
✅ [Task 2] Complete
...
📊 PROJECT COMPLETE - 100% progress
```

## 即将推出的功能（v0.2+）
- HTTP 服务器 + 实时仪表盘。
- 并行任务执行（基于有向无环图 DAG 的解决方案）。
- 能力学习系统（自动评估代理的能力）。
- 智能任务分配机制（将任务分配给最合适的代理）。
- 故障恢复及重试机制。
- 成本跟踪（记录每个代理的 API 调用次数）。
- 人工审核机制（用于审查高风险输出结果）。

## 设计理念

**代理应该记住它们所学到的知识。**

大多数代理框架都是无状态的。Agent OS 通过提供持久化内存，使得代理能够：
1. **记住**：避免不必要的上下文重置。
2. **学习**：随着时间的推移不断提升自身的能力。
3. **协同工作**：共享状态信息，避免重复劳动。
4. **降低成本**：减少不必要的上下文切换，从而降低 API 调用的成本。

## 许可证

MIT 许可证。

---

**由 Nova 为 OpenClaw 开发。**

更多详细信息请参阅 README.md 和 ARCHITECTURE.md 文件。