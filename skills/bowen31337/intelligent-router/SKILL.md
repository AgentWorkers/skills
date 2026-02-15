---
name: intelligent-router
description: 智能模型路由机制用于子代理任务的分派。根据任务的复杂性、成本和能力要求选择最合适的模型。通过将简单任务分配给成本更低的模型来降低成本，同时确保复杂任务的质量得到保障。
version: 2.0.0
---

# 智能路由器

## 快速设置

**这是您第一次使用此技能吗？** 从这里开始：

1. **将 `config.json.example` 复制到 `config.json`（或自定义其中包含的 `config.json`）**
2. **编辑 `config.json`**，添加可用的模型及其成本和层级
3. **测试 CLI**：`python scripts/router.py classify "您的任务描述"`
4. **在您的代理中使用**：在创建子代理时参考配置中的模型

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

## 概述

此技能教会 AI 代理如何根据任务复杂性、成本和能力要求，智能地将子代理任务路由到不同的 LLM（大型语言模型）上。其目标是**通过将简单任务路由到更便宜的模型来降低成本，同时保持复杂工作的质量**。

## 何时使用此技能

在以下情况下使用此技能：
- 创建子代理或将任务委托给其他模型
- 需要在不同的 LLM 选项之间进行选择
- 希望在不过度牺牲质量的情况下优化成本
- 处理具有不同复杂性的任务
- 需要在执行前估算成本

## 核心路由逻辑

### 1. 四层分类系统

任务根据复杂性和风险被分为四个层级：

| 层级 | 描述 | 示例任务 | 模型特性 |
|------|-------------|---------------|----------------------|
| **🟢 简单** | 常规的、低风险的操作 | 监控、状态检查、API 调用、总结 | 最便宜的可用模型，适合重复性任务 |
| **🟡 中等** | 中等复杂性的工作 | 代码修复、研究、小规模修补、数据分析 | 成本/质量平衡，通用性良好 |
| **🟠 复杂** | 多组件开发 | 功能构建、调试、架构设计、多文件修改 | 高质量的推理能力，优秀的代码生成 |
| **🔴 关键** | 高风险的操作 | 安全审计、生产部署、财务操作 | 最优秀的可用模型，可靠性最高 |

### 2. 模型选择策略

在 `config.json` 中配置可用的模型，并将它们分配到相应的层级。路由器将根据任务分类自动推荐模型。

**配置模式：**
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
- **简单层级**：每百万输入成本低于 $0.50 的模型，注重速度/成本优化 |
- **中等层级**：每百万输入成本在 $0.50-$3.00 之间的模型，擅长编码/分析 |
- **复杂层级**：每百万输入成本在 $3.00-$5.00 之间的模型，具有出色的推理能力 |
- **关键层级**：最优秀的可用模型，成本其次于质量 |

### 3. 编码任务路由（重要！）

**针对编码任务：**

- **简单代码任务**（代码检查、小规模修补、单文件修改）：
  - 使用中等层级的模型作为主要编码器
  - 考虑创建一个简单层级的模型作为质量保证（QA）审核者
  - **成本检查**：只有当组合成本低于直接使用复杂层级模型时才使用编码器+QA

- **复杂代码任务**（多文件构建、架构设计、调试）：
  - 直接使用复杂或关键层级的模型
  - 跳过委托——高级模型在处理复杂任务时更可靠且更具成本效益
  - 使用顶级模型时无需进行 QA 审核

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

**每百万令牌（输入/输出）的典型成本范围：**
- **简单层级**：$0.10-$0.50 / $0.10-$1.50
- **中等层级**：$0.40-$3.00 / $0.40-$15.00
- **复杂层级**：$3.00-$5.00 / $1.30-$25.00
- **关键层级**：$5.00+ / $25.00+

**成本估算：**
```bash
# Estimate cost before running
python scripts/router.py cost-estimate "build authentication system"
# Output: Tier: COMPLEX, Est. cost: $0.024 USD
```

**经验法则：**
- 高量重复性任务 → 使用更便宜的模型
- 一次性复杂关键任务 → 使用高级模型
- 有疑问时 → 估算两种选项的成本并进行比较

### 6. 回退与升级策略

如果模型产生的结果不满意：

1. **确定问题**：是模型本身的限制还是任务分类错误
2. **升级一个层级**：尝试使用更高层级的模型处理相同任务
3. **记录失败情况**：记录模型的具体限制以便将来参考
4. **检查能力**：确认模型是否具备所需的功能（如视觉处理、函数调用等）
5. **重新评估分类**：任务最初的分类是否正确？

**升级路径：**
```
SIMPLE → MEDIUM → COMPLEX → CRITICAL
```

### 7. 决策启发式规则

常见模式的快速分类规则：

**简单层级的指标：**
- 关键词：检查、监控、获取、状态、列表、总结
- 高频率的操作（心跳请求、轮询）
- 逻辑简单的 API 调用
- 仅进行数据提取而无需分析

**中等层级的指标：**
- 关键词：修复、修补、更新、研究、分析、测试
- 代码修改量少于 50 行
- 单文件修改
- 研究和文档编写任务

**复杂层级的指标：**
- 关键词：构建、创建、架构设计、调试、设计
- 多文件修改或新功能添加
- 复杂的调试或故障排除
- 系统设计和架构工作

**关键层级的指标：**
- 关键词：安全、生产、部署、财务、审计
- 高风险的操作
- 生产环境部署
- 财务或法律分析
- 需要高决策力的任务

**有疑问时**：选择更高级别的模型。选择低于实际需求的模型会在重试中带来更高的成本。

### 8. 扩展思维模式

某些模型支持扩展思维/推理，这可以提高质量但会增加成本：

**支持扩展思维的模型：**
- Anthropic Claude 模型：使用 `thinking="on"` 或 `thinking="budget_tokens:5000"`
- DeepSeek R1 变体：内置的思维链推理功能
- OpenAI o1/o3 模型：具备原生推理能力

**何时使用扩展思维：**
- 需要深度推理的复杂任务
- 关键任务，尤其是对准确性要求极高的任务
- 多步骤逻辑问题
- 架构和设计决策

**何时避免使用扩展思维：**
- 简单层级任务（浪费资源）
- 中等层级的常规操作
- 高频率的重复性任务
- 使用扩展思维会不必要地增加 2-5 倍的成本

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

对于大型或不确定的任务，先使用较便宜的模型进行处理，然后再使用更高级的模型进行优化。

**注意：** 子代理是异步的——结果以通知的形式返回，而不是同步返回。

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

**节省成本的方法：** 使用便宜的模型处理大量内容，仅在需要优化时使用高级模型。

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

### 模式 3：分层升级

从中等层级开始，根据需要升级到复杂层级：

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

在路由任务之前，请考虑以下因素：

1. **任务的重要性**：失败造成的影响有多大？ → 重要性越高，层级应越高
2. **成本差异**：不同层级之间的价格差异有多大？ → 差异较小时倾向于选择更高级别的模型
3. **重试成本**：任务失败是否需要重试？ → 重试成本较高时，应选择更高级别的模型
4. **时间紧迫性**：任务完成的紧迫性如何？ → 时间紧迫时，应选择更高级别的模型以提高速度和可靠性

## 使用路由器 CLI

随附的 `router.py` 脚本可以帮助进行分类和成本估算：

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

**集成提示：** 在创建代理之前运行 `router.py classify` 以验证您的层级选择。

## 配置指南

### 设置您的模型

1. **列出您的模型**：列出所有可用的 LLM 提供商及其模型
2. **收集价格信息**：从提供商文档中获取每百万令牌的输入/输出成本
3. **分配层级**：根据模型的能力将其分配到简单/中等/复杂/关键层级
4. **记录模型功能**：记录每个模型的功能（如视觉处理、函数调用等）
5. **添加备注**：记录模型的限制或特殊特性

### 多提供者配置示例

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

### 验证清单

- **每个层级至少有一个模型（简单、中等、复杂、关键）**
- **所有模型都包含必需的字段（ID、别名、层级、成本、功能）**
- **模型 ID 与实际提供商/模型的格式相匹配**
- **成本数据准确无误（每百万令牌的成本）**
- **各层级之间的逻辑关系合理（简单层级比关键层级更便宜）**
- **运行 `python scripts/router.py health` 进行验证**

## 资源

更多指导信息请参考：
- **[references/model-catalog.md](references/model-catalog.md)** - 用于评估和选择各层级模型的指南
- **[references/examples.md](references/examples.md)** - 实际的路由模式和示例
- **[config.json](config.json)** - 您的模型配置文件（可自定义！）

## 快速参考卡

**分类：**
- **"检查/监控/获取" → 简单层级**
- **"修复/修补/研究" → 中等层级**
- **"构建/调试/设计" → 复杂层级**
- **"安全/生产/财务" → 关键层级**

**编码任务：**
- 简单代码 → 使用 {medium_model} + 可选 {simple_model} 进行质量保证
- 复杂代码 → 直接使用 {complex_model} 或 {critical_model}

**成本优化：**
- 高量任务 → 使用更便宜的模型
- 一次性复杂任务 → 使用高级模型
- 有疑问时 → 估算两种选项的成本

**通用规则：**
有疑问时，选择更高级别的模型——重试的成本通常高于提高模型质量所带来的收益。