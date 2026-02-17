---
name: switchboard
description: 通过根据任务的复杂性将任务路由到合适的模型来优化AI代理的运行成本。在以下情况下使用此技能：(1) 选择用于任务的模型；(2) 创建子代理；(3) 考虑成本效率；(4) 当当前模型对于任务来说过于复杂/昂贵时。相关触发词：`model routing`（模型路由）、`cost optimization`（成本优化）、`which model`（使用哪个模型）、`too expensive`（太贵）、`spawn agent`（创建代理）、`cheap model`（廉价模型）、`expensive`（昂贵模型）、`tier 1`（一级模型）、`tier 2`（二级模型）、`tier 3`（三级模型）。
---
# SwitchBoard

将任务分配给能够处理这些任务的最便宜的模型。大多数代理的工作都是常规性的。

## 先决条件

此技能需要一个 [OpenRouter](https://openrouter.ai/) API 密钥来进行模型路由。请将其添加到您的 OpenClaw 用户配置中：

```jsonc
// ~/.openclaw/openclaw.json
{
  "openrouter_api_key": "sk-or-v1-..."
}
```

如果没有这个密钥，`/model` 路由和使用非默认模型的 `sessions_spawn` 操作将会失败。您可以在 [openrouter.ai/keys](https://openrouter.ai/keys) 获取密钥。

> **隐私声明：** 本技能中列出的一些模型（例如 Aurora Alpha、Free Router）可能会记录提示和完成内容，用于提供商的培训。**请勿通过免费或未经审核的模型传输敏感数据**（如 API 密钥、密码、私人 PII）。在使用前，请查阅 [openrouter.ai/docs](https://openrouter.ai/docs) 中的模型隐私政策。

## 核心原则

80% 的代理任务都是常规性的任务，例如文件读取、状态检查、格式化、简单的问答等。这些任务不需要昂贵的模型。将高级模型保留给真正需要深度推理的问题。

## 模型等级

有关 OpenRouter 的具体定价和模型信息，请参阅 [references/openrouter-models.md](references/openrouter-models.md)。

### 第 0 级：免费

| 模型 | 上下文 | 工具 | 适合的场景 |
|-------|---------|-------|----------|
| Aurora Alpha | 128K | ✅ | 免费模型，适合零成本的推理 |
| Free Router | 200K | ✅ | 自动路由到最合适的免费模型 |
| Step 3.5 Flash (免费) | 256K | ✅ | 免费模型，支持长上下文的推理 |

*免费模型有使用频率限制，可用性也不稳定。适用于非关键性的后台任务。*

### 第 1 级：低成本（0.02-0.50 美元/百万令牌）

| 模型 | 输入 | 输出 | 上下文 | 工具 | 适合的场景 |
|-------|-------|--------|---------|-------|----------|
| Qwen3 Coder Next | 0.07 美元 | 0.30 美元 | 262K | ✅ | 适合代理编程任务 |
| Gemini 2.0 Flash Lite | 0.07 美元 | 0.30 美元 | 100 万词汇量 | ✅ | 适合处理大量数据和复杂上下文的任务 |
| Gemini 2.0 Flash | 0.10 美元 | 0.40 美元 | 100 万词汇量 | ✅ | 适合常规任务 |
| GPT-4o-mini | 0.15 美元 | 0.60 美元 | 128K | ✅ | 响应迅速，工具使用稳定 |
| DeepSeek Chat | 0.30 美元 | 1.20 美元 | 164K | ✅ | 适合常规任务 |
| Claude 3 Haiku | 0.25 美元 | 1.25 美元 | 200K | ✅ | 工具使用快速，输出结构化 |
| Kimi K2.5 | 0.45 美元 | 2.20 美元 | 262K | ✅ | 支持多模态处理和视觉编码 |

### 第 2 级：中等成本（1-5 美元/百万令牌）

| 模型 | 输入 | 输出 | 上下文 | 工具 | 适合的场景 |
|-------|-------|--------|---------|-------|----------|
| o3-mini | 1.10 美元 | 4.40 美元 | 200K | ✅ | 适合预算有限的推理任务 |
| Gemini 2.5 Pro | 1.25 美元 | 10.00 美元 | 100 万词汇量 | ✅ | 适合处理长上下文的复杂任务 |
| GPT-4o | 2.50 美元 | 10.00 美元 | 128K | ✅ | 适合多模态任务 |
| Claude Sonnet | 3.00 美元 | 15.00 美元 | 100 万词汇量 | ✅ | 性能均衡，适合代理任务 |

### 第 3 级：高级（5 美元/百万令牌）

| 模型 | 输入 | 输出 | 上下文 | 工具 | 适合的场景 |
|-------|-------|--------|---------|-------|----------|
| Claude Opus 4.6 | 5.00 美元 | 25.00 美元 | 100 万词汇量 | ✅ | 适合复杂推理任务 |
| o1 | 15.00 美元 | 60.00 美元 | 200K | ✅ | 适合多步骤推理 |
| GPT-4.5 | 75.00 美元 | 150.00 美元 | 128K | ✅ | 适合前沿任务 |

*价格截至 2026 年 2 月。请查看提供商的文档以获取最新价格。上下文 = 最大上下文窗口。工具 = 支持函数调用。*

## 任务分类

在执行任何任务之前，先对其进行分类：

### 常规任务 → 使用第 1 级模型

**特征：**
- 单步操作
- 指令清晰明确
- 不需要判断
- 预期输出是确定的

**示例：**
- 文件读写操作
- 状态检查和健康监控
- 简单的查询（时间、天气、定义）
- 文本格式化和重构
- 列表操作（过滤、排序、转换）
- 使用已知参数的 API 调用
- 心跳任务和定时任务
- URL 获取和基本解析

### 中等难度任务 → 使用第 2 级模型

**特征：**
- 多步骤但规则明确
- 需要一定的合成能力
- 需要遵循标准模式
- 质量重要但不是决定性因素

**示例：**
- 代码生成（遵循标准模式）
- 摘要和合成
- 草稿编写（电子邮件、文档、消息）
- 数据分析和转换
- 多文件操作
- 工具协调
- 代码审查（非安全相关）
- 搜索和研究任务

### 复杂任务 → 使用第 3 级模型

**特征：**
- 需要解决新颖的问题
- 有多种可行的方法
- 需要细致的判断
- 风险高或不可逆
- 之前的尝试失败了

**示例：**
- 多步骤调试
- 架构和设计决策
- 与安全相关的代码审查
- 更便宜的模型已经无法完成任务
- 需要解释的模糊要求
- 长上下文的推理（超过 50 万令牌）
- 需要创造性的工作
- 处理对抗性或边缘情况

## 决策算法

```
function selectModel(task):
  # Rule 1: Escalation override
  if task.previousAttemptFailed:
    return nextTierUp(task.previousModel)

  # Rule 2: Hard constraints (filter before cost)
  candidates = ALL_MODELS
  if task.requiresToolUse:
    candidates = candidates.filter(m => m.supportsTools)
  if task.estimatedTokens > 128_000:
    candidates = candidates.filter(m => m.contextWindow >= task.estimatedTokens)
  if task.requiresMultimodal:
    candidates = candidates.filter(m => m.supportsImages)

  # Rule 3: Latency constraint
  if task.isRealTime or task.inAgentLoop:
    candidates = candidates.filter(m => m.latencyTier <= "fast")

  # Rule 4: Complexity classification
  if task.hasSignal("debug", "architect", "design", "security"):
    return cheapestIn(candidates, TIER_3)
  if task.hasSignal("summarize", "analyze", "refactor"):
    return cheapestIn(candidates, TIER_2)

  complexity = classifyTask(task)
  if complexity == ROUTINE:
    return cheapestIn(candidates, TIER_1)
  elif complexity == MODERATE:
    return cheapestIn(candidates, TIER_2)
  else:
    return cheapestIn(candidates, TIER_3)
```

> **注意：** 单独使用 “write”（写入）、“read”（读取）或 “code”（编码）作为路由依据是不够准确的——“write a file”（写入文件）属于第 1 级任务，而不是第 2 级。应根据 *任务结构* 进行分类，而不是基于个别关键词。

## 延迟考虑

成本不是唯一的考虑因素。对于实时代理循环来说，延迟也很重要：

| 级别 | 典型首次响应时间（TTFT） | 吞吐量 | 适用场景 |
|------|-------------|------------|----------|
| 免费 | 1-5 秒 | 变动 | 背景任务，对时间不敏感 |
| 第 1 级 | 200-800 毫秒 | 50-100 令牌/秒 | 代理循环，实时处理流程 |
| 第 2 级 | 500 毫秒-2 秒 | 30-80 令牌/秒 | 交互式会话，异步任务 |
| 第 3 级 | 1-10 秒 | 10-40 令牌/秒 | 一次性复杂任务，仅限异步 |

*TTFT = 首次响应所需时间。推理模型（如 o1、o3-mini）由于思考时间较长，但适用于复杂问题。*

**经验法则：** 如果代理在等待响应时陷入循环，使用第 1 级模型。如果任务是一次性完成的任务，那么成本比速度更重要。

## 行为规则

### 对于主会话

1. 对于交互式任务，默认使用第 2 级模型
2. 在执行常规任务时建议降级：“这是常规任务——我可以用更便宜的模型来完成，或者创建一个子代理。”
3. 如果遇到困难，请求升级：“这需要更强的推理能力。切换到 [高级模型]。”

### 对于子代理

1. 除非任务明显属于中等难度以上，否则默认使用第 1 级模型
2. 将类似的任务批量处理以分摊开销
3. 将失败情况报告给上级以便进一步处理
4. 在发送任务之前检查上下文窗口的限制——不要将 200 万令牌的任务发送给只能处理 32 万词汇量的模型

### 对于自动化任务

1. 心跳/监控任务 → 始终使用第 1 级模型（如果有免费模型则使用免费模型）
2. 定时报告 → 根据任务复杂性选择第 1 级或第 2 级模型
3. 警报响应 → 开始使用第 2 级模型，必要时升级
4. 背景数据获取 → 如果任务不重要，使用免费模型

## 沟通方式

在建议模型变更时，使用清晰的语言：

**降级建议：**
> “这看起来像是常规的文件处理任务。需要我在 DeepSeek 上创建一个子代理来完成吗？效果相同，但成本更低。”

**升级请求：**
> “我目前的处理能力已经达到极限了。这需要高级模型的推理能力。需要升级模型。”

**解释层级结构：**
> “我正在使用 Sonnet 进行复杂的分析，同时让子代理在 DeepSeek 上获取数据。这样可以在不牺牲质量的情况下降低成本。”

## 成本影响

假设平均每天使用 100 万令牌：

| 策略 | 月成本 | 备注 |
|----------|--------------|-------|
| 仅使用 Opus 4.6 | 约 75 美元 | 最高级别的模型，但成本低于旧版 Opus |
| 仅使用 Sonnet | 约 45 美元 | 对于大多数任务来说是很好的选择 |
| 仅使用 DeepSeek | 约 9 美元 | 成本较低，但在复杂任务上有限 |
| 仅使用 Qwen3 Coder | 约 2 美元 | 对于编程任务来说是最便宜的选择 |
| 混合使用（80/15/5） | 约 12 美元 | 最佳的平衡方案 |
| 使用免费模型（85/10/4/1） | 约 8 美元 | 高效的优化方案 |

80/15/5 的分配比例：
- 80% 的任务使用第 1 级模型（约 4 美元）
- 15% 的任务使用第 2 级模型（约 5 美元）
- 5% 的任务使用第 3 级模型（约 3 美元）

结果：与仅使用高级模型相比，成本可降低 6-10 倍，同时保持相同的质量。

## OpenClaw 集成

### 会话模型切换

```yaml
# config.yml - set your default session model
model: anthropic/claude-sonnet-4

# Mid-session, switch down for routine work
/model deepseek/deepseek-chat

# Switch up when you hit a wall
/model anthropic/claude-opus-4
```

### 创建子代理

```yaml
# Batch routine tasks on cheap models
sessions_spawn:
  task: "Fetch and parse these 50 URLs"
  model: deepseek/deepseek-chat

# Use Qwen3 Coder for file-heavy agent work
sessions_spawn:
  task: "Refactor these test files to use the new helper"
  model: qwen/qwen3-coder-next

# Free tier for non-critical background jobs
sessions_spawn:
  task: "Check health of all endpoints and log status"
  model: openrouter/free
```

### OpenClaw 的推荐默认设置

| 任务类型 | 模型 | 原因 |
|-----------|-------|-----|
| 主交互会话 | `claude-sonnet-4` | 性能与成本的最佳平衡 |
| 文件操作、数据获取、格式化 | `deepseek/deepseek-chat` | 成本低，可靠性高 |
| 代理编程子任务 | `qwen/qwen3-coder-next` | 每百万令牌 0.07 美元，支持 262 万词汇量的处理，适合工具使用 |
| 背景监控 | `openrouter/free` | 免费模型 |
| 遇到困难/复杂调试 | `anthropic/claude-opus-4` | 仅在必要时升级 |

## 避免的错误做法

**不要：**
- 当任务明显是常规任务时，仍然使用 Opus 模型——`/model deepseek` 的存在是有原因的 |
- 创建子代理时不指定模型——子代理会继承当前会话的模型（通常是第 2 级模型） |
- 对于文件解析、URL 获取或状态检查等任务使用第 3 级模型 |
- 忘记上下文窗口的限制——将 200 万令牌的任务发送给只能处理 32 万词汇量的模型会导致任务失败 |
- 对于重复或定期的任务，使用高于第 1 级的模型

**应该这样做：**
- 将 `model: anthropic/claude-sonnet-4` 设置为 `config.yml` 的默认值——这是一个良好的基准设置 |
- 在 `sessions_spawn` 中始终指定 `model` 字段——默认使用 `deepseek/deepseek-chat` 或 `qwen/qwen3-coder-next` |
- 一旦发现任务是常规任务，立即将 `model` 更改为更便宜的模型 |
- 一旦遇到困难，立即升级模型——不要在性能较差的模型上浪费令牌 |
- 对于无需复杂处理的背景任务，始终使用免费模型

## 优化此技能

随着时间的推移，您可以不断优化您的任务分配策略：

1. **跟踪实际成本**——每周查看 OpenRouter 仪表板，了解哪些模型消耗了最多的令牌 |
2. **添加自定义的路由规则**——如果您的工作流程中有特定术语（例如 “settlement”（结算）、“pricing”（定价）、“vault”（保险库），请将其映射到相应的模型等级 |
3. **调整 80/15/5 的分配比例**——如果发现升级的任务占比超过 5%，说明您的分类可能过于激进 |
4. **固定使用某些模型版本**——当某个廉价模型表现良好时，固定使用该版本（例如 `deepseek/deepseek-chat-v3.1`），以防止提供商的更新影响您的流程 |
5. **设置 OpenRouter 预算警报**——在高级模型使用量失控之前及时发现并采取措施