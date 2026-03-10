---
name: smart-model-router
version: 1.2.0
description: "请停止向 Opus 发送“格式化这个 JSON 数据”的请求；也请停止向 Haiku 发送“重新设计认证系统”的请求。Smart Model Router 会根据每个任务的特点自动选择最合适的处理方式：对于明确的任务，它会使用决策树算法；对于成本敏感的任务，它会采用成本分层的策略；而对于那些情况较为模糊的任务，它还会提供一个可选的、成本较低的模型进行分类处理。"
metadata:
  openclaw:
    emoji: "🧭"
    notes:
      security: "No network calls. Decision tree logic only — reads task description, outputs model recommendation."
---
# 模型路由器

自动为任何任务选择合适的 large language model（LLM）。避免在简单任务上过度付费，也避免在复杂任务上使用性能不足的模型。

## 快速决策：无需分类器就能完成任务吗？

大多数任务都属于明显的类别。首先查看**快速路由表**。只有在情况不明确时才使用分类器。

### 快速路由表

| 任务中的信号 | 路由到 | 原因 |
|---|---|---|
| “什么时间” / “什么日期” / 简单查询 | **flash** | 无需任何推理 |
| 格式转换、CSV→JSON、提取字段 | **flash** | 机械性转换 |
| 摘要文本、列出项目点 | **fast** | 基于模式匹配，无需推理 |
| 翻译文本 | **fast** | 所有模型都具备良好的翻译能力 |
| 编写代码、实现功能、重构 | **mid** | 需要结构化思维 |
| 代码审查、查找错误、安全审计 | **mid** | 需要分析，但不需要深度创造力 |
| 草拟邮件、撰写内容 | **mid** | 需要考虑语气和上下文 |
| 从多个来源进行研究并综合信息 | **mid** | 需要广度，而非深度 |
| 调试复杂系统、多文件调查 | **strong** | 需要深度推理链 |
| 反思失败、自我改进 | **strong** | 需要真正的元认知 |
| 具有细微差别的创造性写作 | **strong** | 需要判断力、风格和原创性 |
| 数学证明、形式逻辑、复杂推理 | **reasoning** | 专门用于推理的模型 |
| 架构决策、权衡分析 | **strong** | 需要权衡多个因素 |

### 级别 → 模型映射

根据你可用的提供商来配置这些规则：

| 级别 | 默认模型 | 替代模型 | 每100个令牌的查询成本 |
|---|---|---|---|
| **flash** | `gemini-flash` | `haiku` | 约0.00007美元 |
| **fast** | `haiku` | `gemini-flash`, `gpt-4o-mini` | 约0.0003美元 |
| **mid** | `sonnet` | `gpt-5.2`, `gemini` | 约0.001美元 |
| **strong** | `opus` | `gpt-5.2-pro`, `gemini` | 约0.003美元 |
| **reasoning** | `openai/o3` | `opus`（带推理功能） | 约0.002美元 |

## “足够好”的原则

**并非每个任务都需要最智能的模型。大多数任务只需要一个快速、便宜且正确的模型。**

### 绝对不需要高端模型（flash/fast级别）

这些任务有唯一的正确答案或只需要机械性转换。没有哪个模型能“做得更好”——它们都能完成任务。使用最便宜的模型：

- 日期/时间查询、时区转换 |
- 正则表达式生成、字符串格式化 |
- JSON/CSV/XML转换 |
- 模板填充（邮件合并、表格信件） |
- 从结构化文本中提取数据 |
- 提供上下文的简单问答 |
- 拼写检查、语法修正 |
- 文件列表、目录扫描摘要 |
- 状态检查、健康报告格式化 |
- 翻译短文本 |

### 需要真正智能的模型（mid级别）

这些任务可以从好的模型中受益，但不需要最先进的模型。mid级别和strong级别之间的质量差异小于5%，但成本却是前者的5倍：

- 代码生成（函数、类、模块） |
- 代码审查和错误查找 |
- 内容写作（博客文章、文档） |
- 具有语气意识的邮件起草 |
- 带有叙述性的数据分析 |
- API集成代码 |
- 摘要长文档 |
- 早晨简报、每日报告 |

### 真正需要顶级模型（strong级别）

只有当任务确实需要深度推理或创造性，而较便宜的模型明显无法完成时，才使用顶级模型：

- 跨文件的多步骤调试 |
- 架构重构决策 |
- 自我反思和失败分析 |
- 具有细微差别的判断（我们应该做X还是Y？） |
- 具有特定风格/语气的创造性写作 |
- 复杂的谈判起草 |
- 综合矛盾的信息 |

## 分类器提示（用于情况不明确的情况）

当快速路由表无法明确匹配时，使用便宜的模型进行分类。将请求发送给 `gemini-flash` 或 `haiku`：

```
Classify this task into exactly one tier. Reply with ONLY the tier name.

Tiers:
- flash: mechanical lookup, formatting, simple extraction
- fast: summarization, translation, template work
- mid: code generation, content writing, analysis, drafting
- strong: complex debugging, self-reflection, creative writing, architectural decisions
- reasoning: math proofs, formal logic, multi-step deduction

Task: {TASK_DESCRIPTION}

Tier:
```

成本：约20个令牌（约0.000001美元）。可以忽略不计。

### “宁可多花一点，也不出错”的原则

如果分类器返回了一个模型级别，但你不确定：
- **非关键任务** → 信任分类器的判断 |
- **面向用户的输出** → 选择一个更高级别的模型 |
- **不可逆的操作** → 始终使用最强的模型 |
- **在两个级别之间难以抉择** → 选择更高级别的模型 |

这就是“宁可多花一点，也不出错”的原则：在更好的模型上多花费1美分，总比因为错误结果而重新做一遍要划算。

## 与 OpenClaw 的集成

### 子代理的生成

```javascript
// Before (manual):
sessions_spawn({ task: "Review this PR", model: "sonnet" })

// After (auto-routed):
// 1. Check Fast Route Table → "Review code" → mid → sonnet
sessions_spawn({ task: "Review this PR", model: "sonnet" })

// For ambiguous tasks:
// 1. Fast Route doesn't match clearly
// 2. Send classifier prompt to gemini-flash
// 3. Get tier → map to model
// 4. Spawn with that model
```

### 定时任务模型分配

在创建或审查定时任务时使用该表格：

```
heartbeat:        flash  → qwen3 (local, free)
cleaning-lady:    fast   → sonnet
morning-briefing: mid    → sonnet
code review:      mid    → sonnet
wind-down:        strong → opus
self-evolution:   strong → opus
```

### 代理级别规则（添加到 AGENTS.md 中）

```markdown
## Model Routing

When spawning sub-agents, auto-select model by task type:
- Mechanical/extraction/formatting → gemini-flash
- Summarization/translation → haiku
- Coding/drafting/analysis → sonnet
- Deep reasoning/self-reflection → opus
- Math/logic/chain-of-thought → o3
When in doubt, go one tier up. Overpaying 1¢ beats re-doing work.
```

## 提供商的强度（2026年基准测试）

有关详细模型比较，请参阅 `references/model-strengths.md`。

当多个模型属于同一级别时，快速选择模型的参考：

| 强度 | 最佳提供商 | 原因 |
|---|---|---|
| 编码（Terminal-Bench） | Claude（Opus/Sonnet） | 得分为65.4，在基准测试中领先 |
| 大规模上下文（>200K） | Gemini | 支持1M窗口，支持处理长文档 |
| 多模态（图像/视频） | Gemini | 支持完整的视频处理 |
| 结构化反馈 | GPT | 经过校准，格式一致 |
| 推理链 | o3 | 专为推理设计 |
| 速度 + 成本效率 | Gemini Flash | 最快且最便宜的级别 |
| 创造性/细致的写作 | Opus | 主观质量最佳 |

## 定时任务与子代理的路由

该路由器适用于所有模型选择，包括：
- 由定时任务生成的子代理（不仅仅是交互式代理） |
- 由其他子代理生成的子代理（递归路由） |
- 创建定时任务时指定的模型 |
- 分类器模型本身（始终使用 flash 模型）

### 定时任务模型分配
```
heartbeat:        flash/local  → qwen3 (free)
cleaning-lady:    fast         → haiku or sonnet
morning-briefing: mid          → sonnet
code review:      mid          → sonnet (or gpt for cross-model review)
wind-down:        strong       → opus (needs metacognition)
self-evolution:   strong       → opus
research reports: mid          → gemini (large context)
```

### 子代理生成规则
当定时任务生成子代理时，每个子代理都会被分配一个级别：
```
Cron: morning-briefing (sonnet)
  └── Sub-agent: check emails → fast (haiku)
  └── Sub-agent: calendar summary → flash (gemini-flash)
  └── Sub-agent: draft briefing text → mid (sonnet)
```

## 复杂任务的协调

有关复杂多步骤任务的详细信息，请参阅 `references/task-orchestration.md`：
- 分层监督者 → 工作器模式 |
- 管道模式（收集 → 分析 → 综合 |
- 并行处理并合并结果 |
- 隔离上下文以防止系统崩溃 |
- Claude 的代码架构示例（反向工程）

## 推理链优化

根据任务类型选择合适的推理链（CoT）技术，以实现最大投资回报。请参阅 `references/chain-of-thought.md`：
- flash/fast：不需要推理链（任务太简单） |
- mid：对于复杂的子任务，使用结构化的推理链 |
- strong：使用完整的推理链（Tree of Thought） |
- reasoning（o3）：内置推理链（无需额外提示）

## 应该保存在 Bootstrap 文件中还是辅助文件中

**在 AGENTS.md 中（每个提示中）：** 只保存路由规则（7行）：
```
When spawning sub-agents, auto-select model by task type:
- Mechanical/extraction/formatting → gemini-flash
- Summarization/translation → haiku
- Coding/drafting/analysis → sonnet
- Deep reasoning/self-reflection → opus
- Math/logic/chain-of-thought → o3
- Reviews/second opinions → gpt
When in doubt, go one tier up.
```

**在按需加载的技能文件中：** 完整的路由表、分类器提示、级别定义、提供商的强度信息。

**在需要时才加载的参考文件中：**
- `references/model-strengths.md` — 详细的基准测试和每个提供商的分析 |
- `references/task-orchestration.md` — 大型任务的分解方法、Claude 的代码架构 |
- `references/chain-of-thought.md` — 与级别匹配的推理链技术

遵循渐进式披露原则：始终加载7行基本信息，按需加载完整技能（约5KB），仅在任务需要时加载深度参考资料。

## 应避免的错误做法

- ❌ 对于“现在几点了”这样的简单任务使用 Opus 模型（会浪费资源） |
- ❌ 使用 Flash 模型进行调试（会错过关键问题） |
- ❌ 始终默认使用同一个模型（违背了使用目的） |
- ❌ 将面向用户的任务路由到最便宜的模型（质量很重要） |
- ❌ 对每个任务都进行分类（大多数任务显然适合快速路由表） |
- ❌ 将完整的路由表保存在 Bootstrap 文件中（每次请求都会浪费令牌） |
- ❌ 不为定时任务的子代理进行路由（它们也会消耗令牌） |
- ❌ 对输出进行自我审查（使用不同的模型进行审查）

## 适合搭配使用的工具

- [model-prompt-adapter](https://clawhub.com/globalcaos/model-prompt-adapter) — 一旦路由器选择了模型，该工具可以修复模型的特殊问题 |
- [subagent-overseer](https://clawhub.com/globalcaos/subagent-overseer) — 监控你正在路由的子代理 |
- [agent-superpowers](https://clawhub.com/globalcaos/agent-superpowers) — 这些被路由的代理应遵循的完整工程流程 |

👉 **https://github.com/globalcaos/tinkerclaw**

**克隆它。分支它。修改它。让它成为你的工具。**