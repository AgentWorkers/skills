# Speckit Swarm - 代理编排系统

## 概述

这是一个基于 OpenClaw 工具实现的、遵循 oh-my-opencode 标准的编排系统。

## 架构

### 核心组件

1. **Ultrawork Detector** - 检测 “ulw”/“ultrawork” 关键字，并触发任务的并行执行。
2. **Agent Personas** - 为不同任务提供专门的系统提示。
3. **Task Planner** - 将复杂任务分解为多个并行子任务。
4. **Continuation Enforcer** - 确保任务能够完全执行完毕。

## 文件结构

```
skills/speckit-swarm/
├── SKILL.md                      # This file
├── src/
│   ├── ultrawork.ts              # Ultrawork detection & trigger
│   ├── personas/
│   │   ├── mod.ts               # Persona exports
│   │   ├── sisyphus.ts          # Main orchestrator
│   │   ├── hephaestus.ts        # Deep worker
│   │   ├── oracle.ts            # Design/debug
│   │   ├── librarian.ts         # Research/docs
│   │   └── explore.ts            # Fast scout
│   ├── planner.ts               # Task decomposition
│   └── index.ts                 # Main entry
```

## 使用方法

### 手动模式
```bash
# Use personas directly
sessions_spawn task:"..." model:"minimax-m2.5" thinking:"high"
```

### Ultrawork 模式
当用户输入 “ulw” 或 “ultrawork” 时：
1. 检测到该关键字。
2. 将任务分解为多个并行子任务。
3. 使用 parallel_spawn 功能执行这些子任务。
4. 合并所有子任务的结果。

## 代理角色（Agent Personas）

### Sisyphus（主要编排器）
- 模型：minimax-m2.5
- 思维能力：高
- 行为特征：持续执行任务、进行并行协调、管理待办事项。

### Hephaestus（深度工作者）
- 模型：minimax-m2.5
- 思维能力：高
- 行为特征：自主执行任务、无需人工干预、完成全部工作范围。

### Oracle（设计/调试）
- 模型：minimax-m2.5
- 思维能力：高
- 行为特征：负责系统架构设计、漏洞排查、代码审查。

### Librarian（研究型代理）
- 模型：minimax-m2.1
- 思维能力：中等
- 行为特征：查找文档、探索代码、发现开发模式。

### Explore（侦察型代理）
- 模型：minimax-m2.5-highspeed
- 思维能力：较低
- 行为特征：快速搜索文件、快速分析数据。

## 使用方法

### 1. 直接使用代理角色
```typescript
import { PERSONAS, buildTaskPrompt } from './speckit-swarm';

const persona = PERSONAS.hephaestus;
const task = "Fix the login bug in auth.ts";

sessions_spawn({
  task: buildTaskPrompt({ task, persona: 'hephaestus' }),
  model: persona.config.model,
  thinking: persona.config.thinking
});
```

### 2. 自动检测 Ultrawork 模式
当用户输入 “ulw” 或 “ultrawork” 时：
```typescript
import { planTask, shouldUseUltrawork } from './speckit-swarm';

const task = "ulw refactor the auth module";
if (shouldUseUltrawork(task)) {
  const plan = planTask(task);
  // Execute plan.chunks with parallel_spawn
}
```

### 任务分解
```typescript
import { planTask } from './speckit-swarm';

const plan = planTask("Create a new API endpoint");
// plan.chunks = [{ label: 'spec', ... }, { label: 'setup', ... }, ...]
```

## Ultrawork 处理器
该处理器会自动检测 “ulw” 关键字，并准备任务以供并行执行。

### 导出的功能
```typescript
// Verifica se contém keyword ulw
containsUltrawork(task: string): boolean

// Limpa o prefixo ulw da tarefa
cleanUltraworkTask(task: string): string

// Prepara execução ultrawork
prepareUltrawork(task: string): {
  shouldExecute: boolean;
  chunks: Array<{
    label: string;
    task: string;
    model?: string;
    thinking?: string;
  }>;
  cleanedTask: string;
}
```

### 使用示例
```typescript
// Na minha resposta, quando receber mensagem com "ulw":

const ultrawork = prepareUltrawork("ulw create a new API");

if (ultrawork.shouldExecute) {
  // Executar com parallel_spawn
  parallel_spawn({
    tasks: ultrawork.chunks,
    wait: "all"
  });
}
```

### 我是如何检测和执行任务的？

### 竞争安全性分析
在任务并行执行之前，我会检查是否存在冲突：

| 任务类型 | 执行策略 |
|----------------|------------|
| 创建新项目/CLI/API | **并行执行** ✓ |
| 处理多个新文件 | **并行执行** ✓ |
| 重构模块 | **谨慎处理（检查依赖关系）** |
| 修复漏洞 | **顺序执行** ✗ |
| 修改同一文件 | **顺序执行** ✗ |
| 简单任务 | **单独执行** |

### 决策流程
1. **分析任务复杂性**：任务是否复杂？
2. **检查是否存在冲突**：是否会修改同一文件？
3. **选择执行策略**：并行执行、顺序执行或单独执行。

这样可以避免多个代理同时修改同一文件时产生的竞争问题。

### 使用示例
```typescript
// Detecção automática
const result = prepareParallelExecution("criar um novo CLI");
// result.shouldExecute = true (detectou complexidade)

if (result.shouldExecute) {
  parallel_spawn({
    tasks: result.chunks,
    wait: "all"
  });
}
```