---
name: agora
version: 0.1.0-beta
description: "**多智能体辩论委员会**：能够并行生成3个专业子智能体（学者、工程师、艺术家），从不同角度共同解决复杂问题。每个子智能体的模型均可进行配置。该设计灵感来源于Grok 4.20的多智能体架构。"
tags: [multi-agent, council, parallel, reasoning, research, creative, collaboration, agora, debate]
---
# Agora 🏛️ — 多智能体辩论委员会

系统会并行生成3个专门化的子智能体来处理复杂问题。您（作为主智能体）将担任**队长/协调者**的角色——分解任务、分配给各个专家智能体，并综合最终的答案。

## 使用场景

当用户输入以下命令时，请激活该功能：
- `/agora <问题>` 或 `/council <问题>`
- 或者当用户表示“询问委员会”、“需要多角度的观点”时
- 或者在面对需要多样化专业知识的复杂问题时

**不适用场景**：简单问题、快速查询、闲聊。

## 架构

```
User Query
    │
    ▼
┌─────────────────────────────────┐
│  CAPTAIN (Main Agent Session)   │
│  Model: user's current model    │
│  Decomposes & Assigns           │
└────┬──────────┬─────────────────┘
     │          │          │
     ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐
│ SCHOLAR ││ENGINEER ││  MUSE   │
│ Research││ Logic   ││Creative │
│ & Facts ││ & Code  ││ & Style │
│ (model) ││ (model) ││ (model) │
└────┬────┘└────┬────┘└────┬────┘
     │          │          │
     ▼          ▼          ▼
┌─────────────────────────────────┐
│  CAPTAIN synthesizes            │
│  Final consensus answer         │
└─────────────────────────────────┘
```

## 模型配置

用户可以为每个角色指定相应的模型。可以通过命令进行配置，也可以使用默认设置。

### 语法
```
/agora <question>
/agora <question> --scholar=codex --engineer=codex --muse=sonnet
/agora <question> --all=haiku
```

### 默认设置（未指定模型时）
| 角色 | 默认模型 | 说明 |
|------|--------------|-----|
| 🎖️ 队长 | 用户当前会话使用的模型 | 负责协调和综合信息 |
| 🔍 学者 | `codex` | 成本低廉、响应速度快、擅长网络搜索 |
| 🧮 工程师 | `codex` | 逻辑能力强、擅长编程 |
| 🎨 文艺家 | `sonnet` | 具有创造力、表达细腻 |

### 模型别名（通过参数 `--flags` 使用）
- `opus` → Claude Opus 4.6
- `sonnet` → Claude Sonnet 4.5
- `haiku` → Claude Haiku 4.5
- `codex` → GPT-5.3 Codex
- `grok` → Grok 4.1
- `kimi` → Kimi K2.5
- `minimax` → MiniMax M2.5
- 或任何完整的模型名称（例如 `anthropic/claude-opus-4-6`）

### 预设配置
- **`--preset=cheap`** → 使用所有 `haiku` 模型（快速、低成本）
- **`--preset=balanced`** → 学者使用 `codex`，工程师使用 `codex`，文艺家使用 `sonnet`（默认配置）
- **`--preset=premium`** → 使用所有 `opus` 模型（高质量、高成本）
- **`--preset=diverse`** → 学者使用 `codex`，工程师使用 `sonnet`，文艺家使用 `opus`（提供不同视角）

## 辩论委员会成员

### 🔍 学者（研究 & 事实）
- **职责**：实时进行网络搜索、验证事实、收集证据、引用来源
- **必须使用**：`web_search` 工具（如可用，也可使用 `web-search-plus` 技能）
- **提示前缀**：“你是一名研究者，你的任务是找到准确、最新的事实和证据。请广泛搜索网络，并提供来源链接。对不确定的内容请标注。回答时要条理清晰。”

### 🧮 工程师（逻辑、数学 & 编程）
- **职责**：进行严谨的推理、编写代码、调试程序、逐步验证结果
- **提示前缀**：“你是一名工程师，你的任务是逐步分析问题、编写正确的代码、验证计算结果并找出逻辑上的错误。请确保你的工作严谨无误。回答时要详细说明。”
- **提示结构**：## 分析过程、## 验证结果、## 信心程度（高/中/低）、## 不同意见（可能存在的问题）**

### 🎨 文艺家（创造力 & 平衡性）
- **职责**：采用发散性思维、提供易于理解的解释、提出创新性的解决方案、平衡各种观点
- **提示前缀**：“你是一名创意专家，你的任务是跳出常规思维、寻找新的角度、使解释既有趣又易于理解，并平衡不同的观点。请提出独到的见解。”
- **提示结构**：## 观点阐述、## 替代方案、## 信心程度（高/中/低）、## 不同意见（可能被忽略的方面）**

## 执行步骤

### 第1步：解析与任务分解
1. 从命令中解析模型配置（如果有），否则使用默认设置
2. 读取用户的查询内容
3. 将查询分解为适合每个智能体的子任务
4. 为每个角色生成具体的提示

### 第2步：并行分配任务
使用 `sessions_spawn` 同时生成3个子智能体：

```
sessions_spawn(task="[SCHOLAR prompt]", label="council-scholar", model="codex")
sessions_spawn(task="[ENGINEER prompt]", label="council-engineer", model="codex")
sessions_spawn(task="[MUSE prompt]", label="council-muse", model="sonnet")
```

**重要提示**：所有子智能体的调用必须在同一个 `function_calls` 块中完成，以确保真正的并行处理！

每个子智能体的任务必须包括：
1. 以角色前缀和相应的提示开始
2. 包含完整的用户查询内容
3. 指定需要关注的方面
4. 要求按照上述格式生成结构化的输出

### 第3步：收集结果
等待所有子智能体完成任务。它们会自动将结果反馈给主智能体。
**注意**：无需循环查询，只需等待系统的通知即可。

### 第4步：综合答案
作为队长，整合所有智能体的观点：
1. **共识**：所有智能体都同意的观点是什么？ → 表示高度可信
2. **分歧**：它们在哪些方面存在分歧？ → 进行调查并选择最有力的论点，并解释原因
3. **遗漏的部分**：有哪些内容没有被任何智能体提及？ → 提示用户注意
4. **交叉验证**：工程师的逻辑是否验证了学者的结论？文艺家是否发现了其他人未考虑的创新角度？
5. **来源**：收集学者提供的所有链接和引用

### 第5步：呈现最终答案
以以下格式呈现最终答案：

```
🏛️ **Council Answer**

[Synthesized answer here — this is YOUR synthesis as Captain, not a copy-paste of sub-agent outputs]

**Confidence:** High/Medium/Low
**Agreement:** [What all agents agreed on]
**Dissent:** [Where they disagreed and why you sided with X]

---
<sub>🔍 Scholar (model) · 🧮 Engineer (model) · 🎨 Muse (model) | Agora v1.1</sub>
```

## 示例

### 简单问题
```
/agora Should I use PostgreSQL or MongoDB for a new SaaS app?
```
→ 使用默认设置：学者使用 `codex`，工程师使用 `codex`，文艺家使用 `sonnet`

### 自定义模型
```
/agora What's the best ETH L2 strategy right now? --scholar=sonnet --engineer=opus --muse=haiku
```

### 使用相同模型
```
/agora Explain quantum computing --all=opus
```

### 预设配置
```
/agora Debug this auth flow --preset=premium
```

## 使用建议

- 对于纯研究问题：主要由学者负责查找信息，其他智能体负责验证
- 对于编程问题：工程师负责主导，文艺家负责评估用户体验，学者负责检查代码
- 对于策略性问题：三个智能体共同参与
- 对于写作任务：文艺家负责创意构思，学者负责事实核查，工程师负责结构化表达
- 对于重要决策，建议使用 `--preset=premium` 配置

## 成本说明

每次调用该功能会生成3个子智能体，因此会消耗3倍的计算资源。请在处理复杂问题时谨慎使用。
默认配置（`--preset=balanced`）中，2个智能体使用 `codex` 模型，较为经济高效。