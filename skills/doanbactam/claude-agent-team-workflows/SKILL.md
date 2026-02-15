---
name: agent-team-workflows
description: "使用 Claude Code Agent Teams 实现通用型多代理工作流编排。适用于用户需要运行团队工作流、创建代理团队，或协调多个团队成员之间的并行工作时——无论涉及哪个领域（软件、内容、数据、策略、研究等）。"
---

# 代理团队工作流程

这是一个适用于5人团队（1名负责人+4名团队成员）的通用协调框架，适用于任何领域。

## 先决条件

必须启用代理团队功能。请在`~/.claude/settings.json`中添加以下配置：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 通用角色

团队成员的ID是固定的，他们的**职能**会根据不同的领域通过**角色卡片**进行重新分配。

| 角色 | ID | 通用职能 | 核心职责 |
|------|----|------------------|---------------------|
| **负责人** | (session) | 调度者 | 分配任务、传递上下文、进行质量审核、整合最终成果 |
| **A位成员** | `architect` | **规划者** | 明确问题、分解任务、制定计划/蓝图 |
| **B位成员** | `developer` | **构建者** | 制作主要成果（代码、草稿、数据集、模型、提案） |
| **C位成员** | `tester` | **验证者** | 根据验收标准进行检查、进行测试、评估正确性 |
| **D位成员** | `reviewer` | **评审者** | 评估质量、风险、一致性、合规性，并提出改进建议 |

### 角色卡片（领域映射）

每个领域都预设了专门的**角色卡片**，以细化通用职能：

| 领域 | 规划者 | 构建者 | 验证者 | 评审者 |
|--------|---------|---------|-----------|--------|
| 软件开发 | 架构师 | 开发者 | 测试者 | 代码评审者 |
| 内容创作 | 制作者 | 编辑者 | 事实核查者 | 校对者 |
| 数据分析 | 分析负责人 | 数据工程师 | 统计学家 | 同行评审者 |
| 商业策略 | 战略师 | 商业分析师 | 财务建模师 | 风险顾问 |
| 研究 | 研究负责人 | 研究员 | 方法论审核者 | 同行评审者 |

> 完整的角色卡片及成果要求请参见 `reference/domain-presets.md`

## 流程模式

共有4种标准的控制流程模式。模式的含义取决于所使用的角色卡片，而非流程本身。

### 1. 顺序流程 — 逐步执行

**适用场景：**工作是线性的，且每个步骤都依赖于前一步的输出。
**示例：**功能开发、内容创作、报告撰写。

### 2. 并行合并 — 同时探索后合并

**适用场景：**多个视角可以独立工作，之后再进行合并。
**示例：**研究、战略分析、多角度评估。

### 3. 迭代评审 — 构建-评审循环

**适用场景：**质量需要创建者和评审者之间的多次迭代。
**示例：**内容编辑、设计优化、提案起草。
**注意：**默认最多进行2轮迭代。超过2轮需要用户批准。

### 4. 分发-聚合 — 分而治之

**适用场景：**大型工作可以分解为多个独立的部分进行并行处理。
**示例：**多模块功能开发、大数据集处理、代码库审计。

> 有关这些模式的详细说明及示例，请参见 `reference/patterns.md`

## 协调协议

这是一个严格的6步协议，适用于所有领域。

### 第1步：确认范围

在组建团队之前，需与用户确认以下内容：
1. **目标** — 具体的交付成果
2. **领域** — 选择预设的角色卡片或自定义角色卡片
3. **流程模式** — 适合哪种流程模式
4. **约束条件** — 使用的工具、技术栈、风格要求、合规性、预算
5. **输入资料** — 原始材料、现有资产、上下文文件
6. **完成标准** — 用户同意的验收标准

### 第2步：填写工作流程模板

请填写通用模板：

```
WORKFLOW INSTANCE SPEC
─────────────────────
Objective:      [deliverable]
Pattern:        [sequential | parallel-merge | iterative-review | fan-out-fan-in]
Domain:         [preset name or "custom"]

ROLE CARDS
  Planner (architect):  [domain title] — [specific responsibility]
  Builder (developer):  [domain title] — [specific responsibility]
  Validator (tester):   [domain title] — [specific responsibility]
  Critic (reviewer):    [domain title] — [specific responsibility]

ARTIFACTS (per step)
  Step 1 → [artifact name]: [format/content description]
  Step 2 → [artifact name]: [format/content description]
  Step 3 → [artifact name]: [format/content description]
  Step 4 → [artifact name]: [format/content description]

CONSTRAINTS:    [tools, rules, limits]
INPUTS:         [files, data, references]
DEFINITION OF DONE:
  □ [criterion 1]
  □ [criterion 2]
  □ [criterion 3]
```

### 第3步：组建团队

```
Create a team of 4 teammates:
- architect: [Planner role card — context and responsibility]
- developer: [Builder role card — context and responsibility]
- tester:    [Validator role card — context and responsibility]
- reviewer:  [Critic role card — context and responsibility]
```

### 第4步：创建带有依赖关系的任务

根据所选流程模式创建任务。每个任务必须包含：
- 明确的描述，引用对应的角色卡片
- 所需的输入成果（来自上一步或原始输入）
- 所需的输出成果（格式和内容）
- 验收标准
- 对前一个任务的依赖关系

### 第5步：为团队成员提供详细信息

每位团队成员在创建任务时必须收到以下信息：
1. **角色卡片** — 他们的领域职责
2. **分配的任务** — 需要完成的工作内容
3. **输入成果** — 上一步的输出结果（由负责人传递）
4. **输出成果要求** — 预期的格式和内容
5. **约束条件** — 领域规则、风格指南、合规性要求
6. **交接指示** — “完成任务后通过消息通知负责人”

**通用创建任务模板：**
```
Spawn a [ID] teammate with the prompt:
"You are the [Domain Title] ([Generic Function]).

YOUR TASK: [task description]

INPUT: [paste or reference previous step's output]

PRODUCE: [artifact name]
Format: [expected format]
Must include: [required sections/elements]

CONSTRAINTS:
- [rule 1]
- [rule 2]

When done, message the lead with your complete [artifact name].
If you encounter blockers, message the lead immediately."
```

### 第6步：协调任务交接

当团队成员完成他们的任务后：
1. 负责人通过消息接收成果
2. 负责人根据验收标准验证成果
3. 负责人将成果及相关上下文通过消息传递给下一位团队成员
4. 如果成果不符合要求 → 提供具体反馈，并要求重新修改

### 第7步：整合并交付

所有步骤完成后：
1. 收集所有成果
2. 确认所有完成标准都已满足
3. 总结已完成的工作（可追溯性：每个标准对应了哪个步骤）
4. 列出剩余的待办事项或已知问题
5. 向用户交付最终成果

## 负责人的行为准则

1. **仅进行任务分配** — 负责人不直接制作主要成果。使用“委托”模式（按`Shift+Tab`键）。
2. **传递所有上下文** — 团队成员之间没有共享的历史记录。负责人必须在步骤之间传递相关成果。
3. **使用私信** — 使用私信进行沟通，避免广播（节省4倍的消息成本）。仅在需要同步时使用广播。
4. **合理分配任务** — 每位团队成员最多负责5-6个任务。将大型工作分解为小部分。
5. **对高风险操作进行审核** — 需要用户批准的操作包括：不可逆的更改、外部发布、法律/合规性要求、高成本的操作、生产环境的部署。
6. **等待团队成员完成** — 在进行下一步之前，务必等待所有团队成员完成任务。

## 处理失败情况

| 情况 | 应对措施 |
|-----------|--------|
| 团队成员遇到困难 | 发送额外信息、提示或简化后的子任务 |
| 成果不合格 | 提供具体反馈，并要求重新修改 |
| 团队成员停止工作 | 重新分配任务，提供相同的上下文及已完成工作的总结 |
| 团队成员之间发生冲突 | 负责人进行调解，做出最终决定，并向双方发送消息说明解决方案 |
| 任务过于复杂 | 负责人将任务拆分为子任务，并重新分配给团队成员 |
| 迭代循环超过最大轮次 | 询问用户是否同意继续进行更多轮次迭代或直接确定最终结果 |

## 成本估算指南

| 流程模式 | 预计成本 | 适用场景 |
|---------|-----------|---------------|
| 顺序流程 | 约是单个工作量的4-5倍 | 需要处理3个以上成果或文件，且流程清晰 |
| 并行合并 | 约是单个工作量的4倍 | 需要3个以上的独立视角 |
| 迭代评审 | 约是单个工作量的3-4倍 | 需要创建者和评审者之间的多次沟通 |
| 分发-聚合 | 约是单个工作量的5倍 | 大型工作可以分解为独立的部分 |

**经验法则：**如果一个代理可以在一次会话中完成任务，就不要使用团队。当工作可以并行处理或需要多个专业视角时，团队才能发挥最大作用。

## 领域预设（快速参考）

| 预设 | 推荐的流程模式 | 关键成果 |
|--------|-------------------|---------------|
| `软件开发` | 顺序流程 / 分发-聚合 | 设计文档、源代码、测试套件、评审报告 |
| `内容创作` | 迭代评审 | 内容概要、草稿、事实核查报告、最终编辑 |
| `数据分析` | 分发-聚合 | 分析计划、数据集/转换结果、统计评估报告 |
| `商业策略` | 并行合并 | 战略框架、市场分析、财务模型、风险评估 |
| `研究` | 并行合并 | 研究计划、文献综述、方法论审核、综合报告 |

> 完整的预设信息（包括角色卡片、成果示例和详细说明）请参见 `reference/domain-presets.md`
> 可直接使用的提示模板请参见 `reference/prompt-templates.md`
> 有关各流程模式的详细说明请参见 `reference/patterns.md`