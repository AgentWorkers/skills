---
name: model-router
description: >
  **自动选择LLM模型以执行子代理任务**  
  该系统会根据任务的复杂性和类型对任务进行分类，随后选择最合适的模型（综合考虑成本与模型能力）。适用于创建子代理、为定时任务（cron jobs）选择模型，或决定执行特定任务时应使用哪个模型。通过提供决策树以及可选的“低成本模型分类器”来处理模糊情况，从而彻底避免了手动指定模型的需要。
---
# 模型路由器

自动为任何任务选择合适的 large language model (LLM)。避免在简单任务上过度付费，也避免在复杂任务上使用性能不足的模型。

## 快速决策：无需分类器就能完成路由吗？

大多数任务都属于明显的类别。首先查看 **快速路由表**。只有在情况不明确时才使用分类器。

### 快速路由表

| 任务中的信号 | 路由到 | 原因 |
|---|---|---|
| “什么时间” / “什么日期” / 简单查询 | **flash** | 无需任何推理 |
| 格式转换、CSV→JSON、提取字段 | **flash** | 机械性操作 |
| 摘要文本、列出项目符号 | **fast** | 基于模式匹配，无需推理 |
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

### 等级 → 模型映射

根据你可用的提供者来配置这些模型：

| 等级 | 默认模型 | 替代模型 | 每 100 个令牌的查询成本 |
|---|---|---|---|
| **flash** | `gemini-flash` | `haiku` | 约 0.00007 美元 |
| **fast** | `haiku` | `gemini-flash`, `gpt-4o-mini` | 约 0.0003 美元 |
| **mid** | `sonnet` | `gpt-5.2`, `gemini` | 约 0.001 美元 |
| **strong** | `opus` | `gpt-5.2-pro`, `gemini` | 约 0.003 美元 |
| **reasoning** | `openai/o3` | `opus`（带推理功能） | 约 0.002 美元 |

## “足够好”的原则

**并非每个任务都需要最智能的模型。大多数任务只需要一个快速、便宜且正确的模型。**

### 绝对不需要高端模型（flash/fast 等级）

这些任务有唯一的正确答案或只需要机械性操作。没有哪个模型能“做得更好”——它们都能完成这些任务。使用最便宜的模型即可：

- 日期/时间查询、时区转换 |
- 正则表达式生成、字符串格式化 |
- JSON/CSV/XML 转换 |
- 模板填充（邮件合并、表单信件） |
- 从结构化文本中提取数据 |
- 提供上下文的简单问答 |
- 拼写检查、语法修正 |
- 文件列表、目录扫描摘要 |
- 状态检查、健康报告格式化 |
- 翻译短文本 |

### 需要真正智能的模型（mid 等级）

这些任务可以从好的模型中受益，但不需要最先进的模型。mid 等级和 strong 等级之间的质量差异小于 5%，但成本却是前者的 5 倍：

- 代码生成（函数、类、模块） |
- 代码审查和错误查找 |
- 内容写作（博客文章、文档） |
- 考虑语气的邮件起草 |
- 带有叙述性的数据分析 |
- API 集成代码 |
- 摘要长文档 |
- 早晨简报、每日报告 |

### 真正需要顶级模型（strong 等级）

只有当任务确实需要深度推理或创造性，而较便宜的模型明显无法完成时，才使用顶级模型：

- 跨文件的多步骤调试 |
- 架构重构决策 |
- 自我反思和失败分析 |
- 需要细致判断的决策（我们应该做 X 还是 Y？） |
- 具有特定风格/语气的创造性写作 |
- 综合矛盾信息 |
- 出错代价高昂的任务 |

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

成本：约 20 个令牌（约 0.000001 美元）。可以忽略不计。

## “有疑问时，选择更高级的模型”原则

如果分类器返回了一个模型等级，但你不确定：
- **非关键任务** → 信任分类器的选择 |
- **面向用户的输出** → 选择更高级的模型 |
- **不可逆的操作** → 始终使用 strong 等级的模型 |
- **两个等级之间难以抉择** → 选择更高级的模型 |

这就是“有疑问时选择更高级模型”的原则：在更好的模型上多花费一点钱，总比因为错误而重新做一遍要划算。

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

### Cron 作业中的模型分配

在创建或审查 Cron 作业时使用以下表格：

```
heartbeat:        flash  → qwen3 (local, free)
cleaning-lady:    fast   → sonnet
morning-briefing: mid    → sonnet
code review:      mid    → sonnet
wind-down:        strong → opus
self-evolution:   strong → opus
```

### 代理级别规则（添加到 AGENTS.md）

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

## 提供者的优势（2026 年基准测试）

有关模型详细比较，请参阅 `references/model-strengths.md`。

当多个模型属于同一等级时，快速选择模型的参考：

| 优势 | 最佳提供者 | 原因 |
|---|---|---|
| 编码（Terminal-Bench） | Claude（Opus/Sonnet） | 得分为 65.4，在基准测试中领先 |
| 大规模上下文（>200K 字符） | Gemini | 支持 100 万字符的文档处理 |
| 多模态（图像/视频） | Gemini | 支持完整的视频处理 |
| 结构化反馈 | GPT | 经过校准，格式一致 |
| 推理链 | o3 | 专为推理设计 |
| 速度 + 成本效率 | Gemini Flash | 最快且最便宜的等级 |
| 创造性/细致的写作 | Opus | 主观质量最佳 |

## Cron 作业与子代理的路由

该路由器适用于所有模型选择，包括：
- 由 Cron 作业生成的子代理（不仅仅是交互式代理） |
- 由其他子代理生成的子代理（递归路由） |
- 创建 Cron 作业时指定的模型 |
- 分类器模型本身（始终使用 flash 等级）

### Cron 作业中的模型分配
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
当 Cron 作业生成子代理时，每个子代理都会被分配一个等级：
```
Cron: morning-briefing (sonnet)
  └── Sub-agent: check emails → fast (haiku)
  └── Sub-agent: calendar summary → flash (gemini-flash)
  └── Sub-agent: draft briefing text → mid (sonnet)
```

## 复杂任务的协调

有关复杂多步骤任务的详细信息，请参阅 `references/task-orchestration.md`：
- 层级监督者 → 工作器模式 |
- 管道模式（收集 → 分析 → 综合 |
- 并行处理并合并结果 |
- 隔离上下文以防止系统崩溃 |
- Claude 的代码架构设计（逆向工程）

## 推理链优化

根据任务的复杂程度选择合适的推理链技术（CoT）以获得最大投资回报。详情请参阅 `references/chain-of-thought.md`：
- flash/fast 等级：无需使用推理链（任务太简单） |
- mid 等级：对于复杂的子任务使用结构化的推理链 |
- strong 等级：使用完整的推理链（Tree of Thought） |
- reasoning 等级（o3）：内置推理链（无需额外提示）

## 应将哪些内容保存在 Bootstrap 文件中，哪些内容保存在辅助文件中

**在 AGENTS.md 中（每个提示中）：** 仅保存路由规则（7 行）：
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

**在按需加载的技能文件中：** 完整的路由表、分类器提示、等级定义、提供者优势。

**在需要时才加载的参考文件中：**
- `references/model-strengths.md` — 详细的基准测试和每个提供者的分析 |
- `references/task-orchestration.md` — 复杂任务的分解方法、Claude 的代码架构 |
- `references/chain-of-thought.md` — 与等级相匹配的推理链技术

遵循渐进式披露原则：始终加载 7 行基本信息，按需加载完整技能（约 5KB），仅在任务需要时加载深度参考资料。

## 应避免的错误做法：

- ❌ 对于“现在几点了”这样的简单任务使用 Opus 模型（会浪费大量资源） |
- ❌ 使用 Flash 模型进行竞态条件调试（会忽略关键问题） |
- ❌ 始终默认使用同一模型（违背了使用目的） |
- ❌ 将面向用户的任务路由到最便宜的模型（质量很重要） |
- ❌ 对每个任务都进行分类（大多数任务显然适合快速路由表） |
- ❌ 将完整的路由表保存在 Bootstrap 文件中（每次请求都会浪费令牌） |
- ❌ 不为 Cron 作业生成的子代理分配模型（它们也会消耗令牌） |
- ❌ 使用相同的模型来审查输出（应该使用不同的模型进行审查）