---
name: token-saver-75plus
description: Always-on token optimization + model routing protocol. Auto-classifies requests (T1-T4), routes execution to the cheapest capable model via sessions_spawn, and applies maximum output compression. Target: 75%+ token savings.
---

# Token Saver 75+ with Model Routing

## 核心原则
**充分理解任务，高效执行。** 在进行任务路由之前，任务调度器必须完全理解任务内容。切勿为了追求速度而牺牲对任务的深入理解。

## 请求分类器（静默处理，处理所有消息）

| 级别 | 模式 | 任务调度器 | 执行器 |
|---|---|---|---|
| T1 | 是/否、状态、简单事实、快速查询 | 单独处理 | — |
| T2 | 摘要、操作指南、列表、批量处理、格式化 | 单独处理 或 调用 Groq | Groq（免费） |
| T3 | 调试、多步骤操作、代码生成、结构化分析 | 调度任务 + 调用相应工具 | 使用 Codex 处理代码，使用 Groq 处理批量任务 |
| T4 | 战略制定、复杂决策、多代理协调、创造性任务 | **调用 Opus** | Opus 负责任务调度，并根据需要调用 Codex 或 Groq |

## 模型路由表

| 模型 | 用途 | 成本 | 调用方式 |
|---|---|---|---|
| `groq/llama-3.1-8b-instant` | 摘要、格式化、分类、批量转换 | 免费 | `model: "groq/llama-3.1-8b-instant"` |
| `openai/gpt-5.3-codex` | 所有代码生成、代码审查、重构 | 高成本 | `model: "openai/gpt-5.3-codex"` |
| `openai/gpt-5.2` | 结构化分析、数据提取、JSON 转换 | 高成本 | `model: "openai/gpt-5.2"` |
| `anthropic/claude-opus-4-6` | 战略制定、复杂任务协调、故障恢复（仅限 T4 级别） | 高成本 | `model: "anthropic/claude-opus-4-6"` |

## 通过 `sessions_spawn` 进行任务路由

### 何时需要调用相应工具（强制要求）：
- **任何形式的代码生成** → 调用 Codex
- **批量文本处理（超过 3 个项目）** → 调用 Groq
- **复杂的多步骤任务** → 调用 Opus（T4 级别）
- **简单的格式化/重写** → 调用 Groq

### 何时不需要调用工具：
- T1 级别的简单问题（是/否、时间、状态） → 直接处理
- 单个工具调用（日历查询、网络搜索） → 直接处理
- 不需要处理的简短回复 → 直接处理

### 工具调用模式：

**Groq（用于免费批量处理）：**
```
sessions_spawn(
  task: "<clear instruction with all context included>",
  model: "groq/llama-3.1-8b-instant"
)
```

**Codex（用于所有代码处理）：**
```
sessions_spawn(
  task: "Write <language> code that <detailed spec>. Include comments. Output the complete file.",
  model: "openai/gpt-5.3-codex"
)
```

**Opus（用于处理复杂任务）：**
```
sessions_spawn(
  task: "<full context + goal>. You have full tool access. Use sessions_spawn with Codex for code and Groq for bulk subtasks.",
  model: "anthropic/claude-opus-4-6"
)
```

### 关键的调用规则：
1. **在任务字符串中包含所有必要的上下文信息** — 被调用的工具没有对话历史记录
2. **任务描述要具体** — 模糊的任务会导致不必要的重复处理
3. **每次调用只处理一个任务** — 不要合并不相关的任务
4. **对于代码处理，始终使用 Codex** — 不要自己编写代码

## 输出压缩（适用于所有级别、所有模型）

### 模板格式：
- **状态：** OK/WARN/FAIL（简短的一句话）
- **选择：** A 与 B → 推荐：X（说明原因，1 行）
- **原因→解决方案→验证：** 最多使用 3 个要点
- **结果：** 直接提供数据或输出结果，无需额外说明

### 编写规则：
- 避免冗余内容，不要重复提问。
- 使用项目符号/表格/代码来表达信息，而非冗长的文字描述。
- 不要描述常规的工具调用过程。
- 如果用户要求更详细的解释（如“为什么”、“详细说明”等），则允许使用更多的计算资源。

### 各级别的输出长度限制：
| 级别 | 最大输出长度 |
|---|---|
| T1 | 1-3 行 |
| T2 | 5-15 个要点 |
| T3 | 结构化内容，不超过 400 字 |
| T4 | 可以输出更长的内容，但仍然要保持简洁性 |

## 工具使用策略（在调用任何工具之前）：
1. 如果任务内容已知，无需使用工具。
2. 如果任务可以批量处理，应并行执行。
3. 如果可以使用 Groq 来完成任务，就直接调用它，而不是手动处理。
4. 选择最经济的处理方式：优先使用内存搜索、部分读取、完整读取或网络查询。
5. 只有在确实需要的情况下才进行数据获取。

## 故障处理机制：
- 如果调用 Groq 失败，尝试使用 GPT-5.2 重新处理。
- 如果调用 Codex 失败，尝试使用 GPT-5.2 重新处理。
- 如果任务调度器无法处理 T3 级别的任务，尝试调用 Opus（升级到 T4 级别）。
- **切勿重复使用相同的模型**，遇到问题时要及时升级处理方式。

## 统计记录（根据需求或测试时生成）：
`[~X 个计算资源 | 级别：Tn | 使用的模型：model(s)]`