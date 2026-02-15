---
name: intelligent-router
description: 智能模型路由系统用于子代理任务的分配。该系统会根据任务的复杂性、成本和能力要求来选择最合适的模型。通过将简单任务分配给成本更低的模型，从而降低整体成本，同时确保复杂任务的质量不受影响。
version: 2.2.0
---

# 智能路由器

## 快速设置

**这是你第一次使用这个技能吗？** 从这里开始：

1. **将 `config.json.example` 复制到 `config.json`（或自定义其中包含的 `config.json`）**
2. **编辑 `config.json`，添加你可用的模型及其成本和层级**
3. **测试 CLI**：`python scripts/router.py classify "你的任务描述"`
4. **在代理中使用**：在创建子代理时参考配置中的模型

**示例配置条目：**
```json
{
  "id": "anthropic/claude-sonnet-4",
  "alias": "Claude Sonnet",
  "tier": "COMPLEX",
  "input_cost_per_m": 3.00,
  "output_cost_per_m": 15.00,
  "capabilities": ["text", "code", "reasoning", "vision"]
}
```

---

## 🆕 v2.2 的新功能

**受 ClawRouter 启发的重大改进：**

1. **🧮 推理层级** - 新增的专用层级，用于形式证明、数学推导和逐步逻辑
   - 主要模型：DeepSeek R1 32B（0.20美元/百万输入）
   - 备用模型：QwQ 32B, DeepSeek Reasoner
   - 置信度阈值：0.97（需要强推理信号）

2. **🔁 自动回退链** - 模型现在有 2-3 个备用选项，并自动重试
   - **简单任务**：GLM-4.7 → GLM-4.5-Air → Ollama qwen2.5:32b
   - **中等任务**：DeepSeek V3.2 → Llama 3.3 70B → Ollama
   - **复杂任务**：Sonnet 4.5 → Gemini 3 Pro → Nemotron 253B
   - **推理任务**：R1 32B → QwQ 32B → DeepSeek Reasoner
   - 每个请求最多尝试 3 次

3. **🤖 代理任务检测** - 自动检测多步骤任务并相应地调整层级
   - 关键词："运行"、"测试"、"修复"、"部署"、"编辑"、"构建"、"创建"、"实现"
   - 多步骤模式："首先...然后"、编号列表
   - 工具存在检测

4. **⚖️ 加权评分（15 个维度）** - 用复杂的评分系统替代简单的关键词匹配
   - 15 个加权维度（推理标记、代码存在、多步骤模式等）
   - 置信度公式：`confidence = 1 / (1 + exp(-8 * (score - 0.5)))`
   - 通过置信度分数更准确地分类层级

**新的 CLI 命令：**
- `python scripts/router.py score "任务"` - 显示详细的评分明细
- 现在所有分类中都显示置信度分数

---

## 概述

此技能教授 AI 代理如何根据任务复杂性、成本和能力要求，智能地将子代理任务路由到不同的 LLM 模型。目标是**通过将简单任务路由到更便宜的模型来降低成本，同时保持复杂工作的质量**。

## 何时使用此技能

在以下情况下使用此技能：
- 创建子代理或将任务委托给其他模型
- 需要在不同的 LLM 选项之间进行选择
- 希望在不牺牲质量的情况下优化成本
- 处理不同复杂度的任务
- 需要在执行前估算成本

## 核心路由逻辑

### 1. 五层分类系统

任务根据复杂性和风险被分为五个层级：

| 层级 | 描述 | 示例任务 | 模型特性 |
|------|-------------|---------------|----------------------|
| **🟢 简单** | 常规、低风险操作 | 监控、状态检查、API 调用、总结 | 最便宜的可用模型，适合重复性任务 |
| **🟡 中等** | 中等复杂度的工作 | 代码修复、研究、小规模修补、数据分析 | 成本/质量平衡，通用性良好 |
| **🟠 复杂** | 多组件开发 | 功能构建、调试、架构设计、多文件更改 | 高质量的推理能力，优秀的代码生成 |
| **🧮 推理** | 形式逻辑和证明 | 数学证明、定理推导、逐步验证 | 专门用于推理的模型 |
| **🔴 关键** | 高风险操作 | 安全审计、生产部署、财务操作 | 最优秀的可用模型，可靠性最高 |

### 2. 模型选择策略

在 `config.json` 中配置你可用的模型，并将它们分配到相应的层级。路由器将根据任务分类自动推荐模型。

**配置示例：**
```json
{
  "models": [
    {
      "id": "{provider}/{model-name}",
      "alias": "Human-Friendly Name",
      "tier": "SIMPLE|MEDIUM|COMPLEX|CRITICAL",
      "provider": "anthropic|openai|google|local|etc",
      "input_cost_per_m": 0.50,
      "output_cost_per_m": 1.50,
      "context_window": 128000,
      "capabilities": ["text", "code", "reasoning", "vision"],
      "notes": "Optional notes about strengths/limitations"
    }
  ]
}
```

**层级推荐：**
- **简单层级**：每百万输入成本低于 0.50 美元的模型，注重速度/成本
- **中等层级**：每百万输入成本在 0.50-3.00 美元之间的模型，擅长编码/分析
- **复杂层级**：每百万输入成本在 3.00-5.00 美元之间的模型，推理能力出色 |
- **推理层级**：每百万输入成本在 0.20-2.00 美元之间的模型，专门用于数学/逻辑推理 |
- **关键层级**：最好的可用模型，成本次于质量 |

### 2a. 加权评分系统（15 个维度）

路由器使用复杂的 15 维度加权评分系统来准确分类任务：

**评分维度（权重如下）：**
1. **推理标记**（0.18） - 如 "prove"、"theorem"、"derive"、"verify"、"logic" 等关键词
2. **代码存在**（0.15） - 代码块、函数定义、文件扩展名
3. **多步骤模式**（0.12） - "首先...然后"、"步骤 1"、编号列表
4. **代理任务**（0.10） - 动作动词："运行"、"测试"、"修复"、"部署"、"构建"
5. **技术术语**（0.10） - "algorithm"、"architecture"、"optimization"、"security" 等
6. **词元数量**（0.08） - 基于长度估计的复杂性
7. **创造性标记**（0.05） - "creative"、"story"、"compose"、"brainstorm" 等
8. **问题复杂性**（0.05） - 多个问题、复杂查询
9. **约束条件数量**（0.04） - "must"、"require"、"only"、"exactly" 等
10. **命令动词**（0.03） - "analyze"、"evaluate"、"compare"、"assess" 等
11. **输出格式**（0.03） - 结构化输出请求（JSON、表格、markdown）
12. **简单指标**（0.02） - "check"、"get"、"show"、"status"（反向）
13. **领域特定性**（0.02） - 缩写词、技术符号
14. **引用复杂性**（0.02） - 引用、上下文依赖性
15. **否定复杂性**（0.01） - 否定句、例外情况、排除条件

**置信度计算：**
```
weighted_score = Σ(dimension_score × weight)
confidence = 1 / (1 + exp(-8 × (weighted_score - 0.5)))
```

这创建了一个平滑的 S 曲线：
- 分数 0.0 → 置信度约 2%
- 分数 0.5 → 置信度约 50%
- 分数 1.0 → 置信度约 98%

**查看详细评分：**
```bash
python scripts/router.py score "prove that sqrt(2) is irrational step by step"
# Shows breakdown of all 15 dimensions and top contributors
```

### 2b. 代理任务检测

如果任务涉及以下内容，会自动标记为“代理任务”：
- **动作关键词**：运行、测试、修复、部署、编辑、构建、创建、实现
- **多步骤模式**："首先...然后"、"步骤 1"、编号指令
- **工具的使用**（当以编程方式使用时）

**对路由的影响：**
- 代理任务会自动提升到至少中等层级
- 带有 `"agentic": true` 标志的模型会被优先用于这些任务
- 简单的监控任务不会被错误地分类为代理任务

**示例：**
```bash
router.py classify "Build a React component with tests, then deploy it"
# → COMPLEX tier (agentic task detected)

router.py classify "Check the server status"
# → SIMPLE tier (not agentic)
```

### 2c. 自动回退链**

每个层级现在都有 2-3 个备用模型，用于失败时的自动重试：

**配置的回退链：**
```json
{
  "SIMPLE": {
    "primary": "glm-4.7",
    "fallback_chain": ["glm-4.7-backup", "glm-4.5-air", "ollama-qwen"]
  },
  "MEDIUM": {
    "primary": "deepseek-v3.2",
    "fallback_chain": ["llama-3.3-70b", "ollama-llama"]
  },
  "COMPLEX": {
    "primary": "claude-sonnet-4.5",
    "fallback_chain": ["gemini-3-pro", "nemotron-253b"]
  },
  "REASONING": {
    "primary": "deepseek-r1-32b",
    "fallback_chain": ["qwq-32b", "deepseek-reasoner"]
  },
  "CRITICAL": {
    "primary": "claude-opus-4.6",
    "fallback_chain": ["claude-opus-oauth", "claude-sonnet-4.5"]
  }
}
```

**使用方法：**
- 每个请求最多尝试 3 次（1 个主要模型 + 2 个备用模型）
- 失败时自动尝试链中的下一个模型
- 通过首先尝试更便宜的选项来保持成本效率（在同一层级内）

### 3. 编码任务路由（重要！）

**针对编码任务：**

- **简单编码任务**（代码检查修复、小规模修补、单文件更改）
  - 使用中等层级的模型作为主要编码器
  - 考虑创建一个简单层级的模型作为质量保证（QA）审查者
  - **成本检查**：只有当组合成本低于直接使用复杂层级模型时才使用编码器+QA

- **复杂编码任务**（多文件构建、架构设计、调试）
  - 直接使用复杂或关键层级模型
  - 跳过委托——高级模型对于复杂工作更可靠且更具成本效益
  - 使用顶级模型时不需要质量保证审查

**编码任务的决策流程：**
```
IF task is simple code (lint, patch, single file):
  → {medium_model} as coder + optional {simple_model} QA
  → Only if (coder + QA cost) < {complex_model} solo

IF task is complex code (multi-file, architecture):
  → {complex_model} or {critical_model} directly
  → Skip delegation, skip QA — the model IS the quality
```

### 4. 使用模式

在创建子代理时，使用 `config.json` 中的模型 ID：

```python
# Use the router CLI to classify first (optional but recommended)
# $ python scripts/router.py classify "check GitHub notifications"
# → Recommends: SIMPLE tier, {simple_model}

# Simple task — monitoring
sessions_spawn(
    task="Check GitHub notifications and summarize recent activity",
    model="{simple_model}",  # Use your configured SIMPLE tier model ID
    label="github-monitor"
)

# Medium task — code fix
sessions_spawn(
    task="Fix lint errors in utils.js and write changes to disk",
    model="{medium_model}",  # Use your configured MEDIUM tier model ID
    label="lint-fix"
)

# Complex task — feature development
sessions_spawn(
    task="Build authentication system with JWT, middleware, tests",
    model="{complex_model}",  # Use your configured COMPLEX tier model ID
    label="auth-feature"
)

# Critical task — security audit
sessions_spawn(
    task="Security audit of authentication code for vulnerabilities",
    model="{critical_model}",  # Use your configured CRITICAL tier model ID
    label="security-audit"
)
```

### 5. 成本意识

了解成本结构有助于优化路由决策：

**典型的每百万词元（输入/输出）成本范围：**
- **简单层级**：0.10-0.50 美元 / 0.10-1.50 美元
- **中等层级**：0.40-3.00 美元 / 0.40-15.00 美元
- **复杂层级**：3.00-5.00 美元 / 1.30-25.00 美元
- **关键层级**：5.00 美元及以上 / 25.00 美元及以上

**成本估算：**
```bash
# Estimate cost before running
python scripts/router.py cost-estimate "build authentication system"
# Output: Tier: COMPLEX, Est. cost: $0.024 USD
```

**经验法则：**
- 高量重复性任务 → 更便宜的模型
- 一次性复杂关键任务 → 高级模型
- 不确定时 → 估算两种选项的成本并进行比较

### 6. 回退与升级策略

如果模型产生的结果不满意：

1. **确定问题**：是模型限制还是任务分类错误
2. **升级一个层级**：尝试同一任务的上一层模型
3. **记录失败情况**：记录模型特定的限制以供将来路由参考
4. **检查能力**：检查模型是否具备所需的能力（如视觉、函数调用等）
5. **审查分类**：任务是否被正确分类？

**升级路径：**
```
SIMPLE → MEDIUM → COMPLEX → CRITICAL
```

### 7. 决策启发式

常见模式的快速分类规则（现在通过加权评分自动化）：

**简单层级的指标：**
- 关键词：检查、监控、获取、获取、状态、列表、总结
- 高频操作（心跳、轮询）
- 逻辑简单的明确定义的 API 调用
- 无需分析的数据提取
- **示例**："2+2 等于多少？"

**中等层级的指标：**
- 关键词：修复、修补、更新、研究、分析、测试
- 代码更改少于 50 行
- 单文件修改
- 研究和文档任务
- **示例**："编写一个 Python 函数来排序列表"

**复杂层级的指标：**
- 关键词：构建、创建、架构设计、调试、设计
- 多文件更改或新功能
- 复杂的调试或故障排除
- 系统设计和架构工作
- 多步骤的代理任务
- **示例**："构建一个带有测试的 React 组件，然后部署它"

**推理层级的指标**（需要置信度 ≥ 0.97）：
- 关键词：证明、定理、推导、形式化、验证、逻辑、逐步
- 数学证明和推导
- 逐步逻辑推理
- 定理证明和引理
- **示例**："逐步证明 sqrt(2) 是无理数"

**关键层级的指标：**
- 关键词：安全、生产、部署、财务、审计
- 安全敏感的操作
- 生产部署
- 财务或法律分析
- 高风险决策
- **示例**："对认证代码进行安全审计以查找漏洞"

**分类是自动的：** 加权评分系统分析所有 15 个维度。这些启发式规则用于理解触发每个层级的因素。

**不确定时：** 升一级。配置过低会在重试中花费更多成本，而配置过高则会在模型质量上花费更多成本。

### 8. 扩展思维模式

某些模型支持扩展思维/推理，这可以提高质量但会增加成本：

**支持扩展思维的模型：**
- Anthropic Claude 模型：使用 `thinking="on"` 或 `thinking="budget_tokens:5000"`
- DeepSeek R1 变体：内置的思维链推理
- OpenAI o1/o3 模型：内置的推理能力

**何时使用扩展思维：**
- 需要深度推理的复杂任务
- 关键任务，准确性至关重要
- 多步骤逻辑问题
- 架构和设计决策

**何时避免使用扩展思维：**
- 简单层级的任务（浪费资源）
- 中等层级的常规操作
- 高频重复性任务
- 使用扩展思维令牌会导致成本不必要的增加（2-5 倍）

```python
# Enable thinking for complex architectural work
sessions_spawn(
    task="Design scalable microservices architecture for payment system",
    model="{complex_model}",
    thinking="on",  # or thinking="budget_tokens:5000"
    label="architecture-design"
)
```

## 高级模式

### 模式 1：两阶段处理

对于大型或不确定的任务，先使用较便宜的模型进行初步处理，然后使用更好的模型进行细化。

**注意：** 子代理是异步的——结果以通知形式返回，而不是同步返回。

```python
# Phase 1: Draft with cheaper model
sessions_spawn(
    task="Draft initial API design document outline",
    model="{simple_model}",
    label="draft-phase"
)

# Wait for draft-phase to complete and write output...

# Phase 2: Refine with capable model (after Phase 1 finishes)
sessions_spawn(
    task="Review and refine the draft at /tmp/api-draft.md, add detailed specs",
    model="{medium_model}",
    label="refine-phase"
)
```

**节省方法：** 使用便宜的模型处理大量内容，仅在需要细化时使用昂贵的模型。

### 模式 2：批量处理**

将多个类似的简单任务组合在一起以减少开销：

```python
# Instead of spawning 10 separate agents:
tasks = [
    "Check server1 status",
    "Check server2 status",
    # ... 10 tasks
]

# Batch them:
sessions_spawn(
    task=f"Run these checks: {', '.join(tasks)}. Report any issues.",
    model="{simple_model}",
    label="batch-monitoring"
)
```

### 模式 3：分层升级**

从中等层级开始，必要时升级到复杂层级：

```python
# Try MEDIUM first
sessions_spawn(
    task="Debug intermittent test failures in test_auth.py",
    model="{medium_model}",
    label="debug-attempt-1"
)

# If insufficient, escalate:
if debug_failed:
    sessions_spawn(
        task="Deep debug of test_auth.py failures (previous attempt incomplete)",
        model="{complex_model}",
        label="debug-attempt-2"
    )
```

### 模式 4：成本效益分析

在路由之前，请考虑：
1. **关键性**：失败的后果有多严重？→ 关键性越高，层级越高
2. **成本差异**：不同层级之间的价格差异有多大？→ 差异较小 → 倾向于选择更高级别的模型
3. **重试成本**：失败是否需要重试？→ 重试成本较高 → 从更高级别的模型开始
4. **时间敏感性**：完成的紧迫性如何？→ 紧急性越高 → 为了速度/可靠性选择更高级别的模型

## 使用路由器 CLI

附带的 `router.py` 脚本有助于分类和成本估算：

```bash
# Classify a task and get model recommendation
python scripts/router.py classify "fix authentication bug in login.py"
# Output: Classification: MEDIUM
#         Recommended Model: {medium_model}

# List all configured models
python scripts/router.py models
# Output: Models grouped by tier

# Check configuration health
python scripts/router.py health
# Output: Validates config.json structure

# Estimate task cost
python scripts/router.py cost-estimate "build payment processing system"
# Output: Tier: COMPLEX, Est. tokens: 5000/3000, Cost: $0.060 USD
```

**集成提示：** 在创建代理之前运行 `router.py classify` 以验证你的层级选择。

## 配置指南

### 设置你的模型

1. **列出你的模型**：列出你可以使用的所有 LLM 提供者和模型
2. **收集价格信息**：从提供商文档中获取每百万词元的输入/输出成本
3. **分配层级**：根据能力将模型映射到简单/中等/复杂/关键层级
4. **记录能力**：记录每个模型的功能（如视觉、函数调用等）
5. **添加备注**：包括限制或特殊特性

### 多提供者配置示例**

```json
{
  "models": [
    {
      "id": "local/ollama-qwen-1.5b",
      "alias": "Local Qwen",
      "tier": "SIMPLE",
      "provider": "ollama",
      "input_cost_per_m": 0.00,
      "output_cost_per_m": 0.00,
      "context_window": 32768,
      "capabilities": ["text"],
      "notes": "Free local model, good for testing and simple tasks"
    },
    {
      "id": "openai/gpt-4o-mini",
      "alias": "GPT-4o Mini",
      "tier": "MEDIUM",
      "provider": "openai",
      "input_cost_per_m": 0.15,
      "output_cost_per_m": 0.60,
      "context_window": 128000,
      "capabilities": ["text", "code", "vision"],
      "notes": "Great balance of cost and capability"
    },
    {
      "id": "anthropic/claude-sonnet-4",
      "alias": "Claude Sonnet",
      "tier": "COMPLEX",
      "provider": "anthropic",
      "input_cost_per_m": 3.00,
      "output_cost_per_m": 15.00,
      "context_window": 200000,
      "capabilities": ["text", "code", "reasoning", "vision"],
      "notes": "Excellent for complex coding and analysis"
    },
    {
      "id": "anthropic/claude-opus-4",
      "alias": "Claude Opus",
      "tier": "CRITICAL",
      "provider": "anthropic",
      "input_cost_per_m": 15.00,
      "output_cost_per_m": 75.00,
      "context_window": 200000,
      "capabilities": ["text", "code", "reasoning", "vision", "function-calling"],
      "notes": "Best available for critical operations"
    }
  ]
}
```

### 验证检查表

- [ ] 每个层级至少有一个模型（简单、中等、复杂、关键）
- [ ] 所有模型都包含所需字段（id、别名、层级、成本、能力）
- [ ] 模型 ID 与你的实际提供商/模型格式匹配
- [ ] 成本每百万词元准确无误
- [ ] 各层级之间的逻辑合理（简单层级比关键层级便宜）
- [ ] 运行 `python scripts/router.py health` 进行验证

## 资源

更多指导：
- **[references/model-catalog.md](references/model-catalog.md)** - 评估和选择每个层级模型的指南
- **[references/examples.md](references/examples.md)** - 实际的路由模式和示例
- **[config.json](config.json)** - 你的模型配置（可自定义！）

## 快速参考卡

**分类：**
- **"检查/监控/获取"** → 简单层级
- **"修复/修补/研究"** → 中等层级
- **"构建/调试/架构设计"** → 复杂层级
- **"安全/生产/财务"** → 关键层级

**编码任务：**
- 简单代码 → {medium_model} + 可选 {simple_model} QA
- 复杂代码 → {complex_model} 或 {critical_model} 直接使用

**成本优化：**
- 高量任务 → 更便宜的模型
- 一次性复杂任务 → 高级模型
- 不确定时 → 估算两种选项的成本

**通用规则：**
不确定时，选择更高级别的模型——重试的成本高于质量的成本。