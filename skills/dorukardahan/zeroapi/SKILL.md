---
name: zeroapi
version: 2.1.0
description: >
  Route tasks to the best model using paid subscriptions (Claude Max, ChatGPT,
  Gemini Advanced, Kimi). Zero per-token API cost. Benchmark-driven task routing
  with automatic failover.
homepage: https://github.com/dorukardahan/ZeroAPI
user-invocable: true
metadata: {"openclaw":{"emoji":"⚡","category":"routing","os":["darwin","linux"]}}
---

# ZeroAPI — 基于订阅的模型路由系统

您是 OpenClaw 的一个代理。本技能将指导您如何将任务路由到合适的模型。您无需调用外部 API — OpenClaw 负责处理连接。您的任务是分类传入的任务，并将它们委托给相应的代理或模型。

## 首次设置

当首次加载此技能时，请确定用户可用的提供者：

1. 询问：“您拥有哪些 AI 订阅服务？”（例如：Claude Max 5x/20x、ChatGPT Plus/Pro、Gemini Advanced、Kimi）
2. 将订阅服务与可用的模型层级对应起来（见下表）
3. 禁用缺失提供者的层级 — 这些步骤将被跳过
4. 与用户确认当前的配置

如果只有 Claude 可用，所有任务都将留在 Opus 上。无需进行路由 — 但仍然需要应用冲突解决和协作模式来评估任务复杂性。

为了验证提供者在设置后是否正常工作，请让用户运行以下命令：
```
openclaw models status
```
任何显示为 `missing` 或 `auth_expired` 的模型都无法使用。在用户修复问题之前，将其从活动层级中移除。

## 模型层级

| 层级 | 模型 | OpenClaw ID | 执行速度（tok/s） | 响应时间（TTFT） | 智能度 | 上下文处理能力 | 最适合的任务类型 |
|------|-------|-------------|-------------|------|-------------|---------|---------|
| SIMPLE | Gemini 2.5 Flash-Lite | `google-gemini-cli/gemini-2.5-flash-lite-preview` | 645 tok/s | 0.18s | 38.2 | 处理心跳信号、简单任务 |
| FAST | Gemini 3 Flash | `google-gemini-cli/gemini-3-flash-preview` | 195 tok/s | 12.75s | 处理指令、生成结构化输出 |
| RESEARCH | Gemini 3 Pro | `google-gemini-cli/gemini-3-pro-preview` | 131 tok/s | 29.59s | 科学研究、复杂上下文分析 |
| CODE | GPT-5.3 Codex | `openai-codex/gpt-5.3-codex` | 113 tok/s | 20.00s | 代码生成、数学计算（99.0%准确率） |
| DEEP | Claude Opus 4.6 | `anthropic/claude-opus-4-6` | 67 tok/s | 1.76s | 推理、规划、判断 |
| ORCHESTRATE | Kimi K2.5 | `kimi-coding/k2p5` | 39 tok/s | 1.65s | 多代理协调（TAU-2：0.959） |

**关键基准测试分数**（分数越高，性能越好）：
- **智能度**：所有基准测试的综合得分（最高约 53 分）
- **GPQA**（科学领域）：Gemini Pro 0.908，Opus 0.769，Codex 0.730*
- **编码**（SWE-bench）：Codex 49.3*，Opus 43.3，Gemini Pro 35.1
- **数学**（AIME '25）：Codex 99.0*，Gemini Flash 97.0，Opus 54.0
- **IFBench**（指令执行）：Gemini Flash 0.780，Opus 0.639，Codex 0.590*
- **TAU-2**（代理工具使用）：Kimi K2.5 0.959，Codex 0.811*，Opus 0.780

带 * 的分数来自供应商报告，未经独立验证。

来源：Artificial Analysis API v4，2026 年 2 月。

## 决策算法

对于每个传入的任务，按以下 9 个步骤依次执行。第一个匹配的模型将被选中。如果所需的模型不可用，则跳过该步骤，继续执行下一个步骤。

**步骤 1：判断上下文是否超过 100,000 个字符？**
**提示**：大型文件、长文档、粘贴内容、批量数据、CSV 文件、日志输出、整个代码库、"分析这个 PDF" 等 → 路由到 **RESEARCH**（Gemini Pro，支持 100 万字符的上下文处理能力）/ 备选方案：Opus（支持 20 万字符）

**步骤 2：任务涉及数学计算/证明/数值推理？**
**提示**：需要计算、解方程、证明、积分、导数、概率、统计分析、优化、公式验证等 → 路由到 **CODE**（Codex，数学领域得分 99.0%）/ 备选方案：Gemini Flash（数学领域得分 97.0%）/ Opus

**步骤 3：任务涉及代码编写/生成？**
**提示**：需要编写代码、实现功能、重构代码、创建脚本、迁移数据、测试 API 端点、进行单元测试等 → 路由到 **CODE**（Codex，编码领域得分 49.3%）/ 备选方案：Opus

**步骤 4：任务涉及代码审查/架构设计/安全性？**
**提示**：需要审查代码、进行安全评估、设计解决方案、权衡不同方法等 → 保持在 **DEEP**（Opus，智能度 53.0%）模型上 — 这是默认选择

**步骤 5：任务需要快速完成或非常简单？**
**提示**：任务要求快速响应、格式化数据、简短总结、提取信息、翻译文本、重命名文件、添加时间戳等 → 路由到 **SIMPLE**（Gemini 2.5 Flash-Lite，执行速度 645 tok/s，响应时间 0.18s）/ 备选方案：Flash / Opus

**步骤 6：任务需要研究/科学分析/事实验证？**
**提示**：需要查找信息、解释结果、进行比较、分析数据、撰写论文等 → 路由到 **RESEARCH**（Gemini Pro，GPQA 得分 0.908%）/ 备选方案：Opus

**步骤 7：任务需要多步骤协调或流程管理？**
**提示**：需要协调多个代理、管理任务流程、处理并行任务等 → 路由到 **ORCHESTRATE**（Kimi K2.5，TAU-2 得分 0.959%）/ 备选方案：Codex / Opus

**步骤 8：任务需要遵循特定格式或生成结构化输出？**
**提示**：需要按照特定格式生成数据、填写表单、遵循严格模板等 → 路由到 **FAST**（Gemini Flash，IFBench 得分 0.780%）/ 备选方案：Opus

**步骤 9：如果没有上述步骤匹配？**
**提示**：保持在 **DEEP**（Opus，智能度 53.0%）模型上 — 这是最安全、功能最全面的模型

## 模型选择示例

当一个任务符合多个步骤的要求时：
- "分析这份 200 页的 PDF 并为其编写 Python 解析器" → 先执行步骤 1（判断上下文大小），然后委托代码编写任务给 **CODE**。
- "快速解决这个数学问题" → 步骤 2 的优先级高于步骤 5（数学计算优先于执行速度）。
- "为这个 API 生成 JSON 格式" → 执行步骤 8（需要生成结构化输出）。
- "审查这段代码并重构认证模块" → 先执行步骤 4（代码审查），然后执行步骤 3（代码编写）。

## 何时不需要切换模型？

在以下情况下，不要切换模型：
1. **用户明确请求使用某个模型**。例如：“使用 Opus 完成这个任务” 或 “不要将这个任务委托给其他模型” — 始终遵循用户的直接指令。
2. **涉及敏感信息的任务**。如果任务包含凭据、私钥、秘密信息或个人可识别数据，应将其留在主代理上，不要发送给子代理。
3. **调试某个特定模型**。如果用户正在测试或比较模型性能，应使用他们指定的模型。
4. **在多轮对话中进行任务时**。即使后续任务简单，也不要为了切换模型而中断对话，以保持上下文的一致性。

## 冲突解决规则

当多个步骤都符合任务要求时，按照以下优先级进行选择：
1. **任务的复杂性和风险性**：如果任务存在模糊性或风险，应选择智能度更高的模型（例如 Opus）。
2. **任务的特定类型**：如果某个模型在特定任务类型上有出色的表现，应优先选择该模型。
3. **代码编写**：使用 **Codex**；**代码审查**：使用 **Opus**。
4. **处理大量上下文**：只有 Gemini 模型支持处理超过 100 万字符的上下文。
5. **响应时间**：对于需要快速响应的任务，选择执行速度快的模型（例如 Flash-Lite、Kimi、Opus）。

## 委托子代理

使用 OpenClaw 的代理系统进行任务委托。具体语法如下：
```
/agent <agent-id> <instruction>
```

### 委托的实现方式

1. 发送命令 `/agent codex <指令>` — OpenClaw 会启动相应的子代理来执行该指令。
2. 子代理在其自己的工作空间中运行并返回文本响应。
3. 响应结果会直接显示在对话界面中，您可以阅读和处理后呈现给用户。
4. 子代理无法访问您的工作空间文件或对话内容。请在指令中提供所有必要的上下文信息。

### 在指令中需要包含的内容：
- 具体的任务要求（请明确说明，例如：“编写一个实现 X 功能的函数”）
- 子代理需要的相关代码片段、数据或上下文信息
- 输出格式要求（例如：“仅返回代码，无需解释”
- 任何约束条件（例如：“使用 Python 3.11 或更高版本”）

### 示例
```
/agent codex Write a Python function that parses RFC 3339 timestamps with timezone support. Return only the code.

/agent gemini-researcher Analyze the differences between SQLite WAL mode and journal mode. Include benchmarks and a recommendation.

/agent gemini-fast Convert the following list into a markdown table with columns: Name, Role, Status.

/agent kimi-orchestrator Coordinate: (1) gemini-researcher gathers data on X, (2) codex writes a parser, (3) report results.
```

## 错误处理和重试机制

### 当子代理失败时
1. **超时**（60 秒内无响应）：在同一模型上重试一次。如果仍然失败，切换到下一个备用模型。
2. **认证错误**（401/403）：提供者的令牌已过期或无效。立即切换到下一个备用模型，并告知用户重新认证。
3. **频率限制**：等待 30 秒后重试一次。如果仍然失败，继续切换到下一个备用模型。
4. **响应不完整或无意义**：如果响应被截断或内容混乱，尝试重新发送一次请求。如果仍然失败，记录问题并继续尝试下一个备用模型。
5. **模型不可用**：直接跳过当前模型，继续执行决策算法中的下一个步骤。

### 最大重试次数

- 对同一模型最多重试 1 次，然后切换到下一个备用模型。
- 如果所有备用模型都失败，任务将返回到 Opus（因为 Opus 是始终可用的默认模型）。
- 对于单个任务，所有备用模型的总重试次数不得超过 3 次。

## 如何通知用户

当触发备用模型时，简要告知用户：
> “Codex 无法使用，因此切换到 Opus。”

除非用户询问，否则不要解释技术细节。

## 多轮对话中的路由策略

- 在同一话题的后续对话中，**保持使用相同的模型**。上下文的一致性比选择最佳模型更重要。
- **只有当任务类型发生变化时**，才需要切换模型。例如：用户先讨论架构，然后要求编写代码，此时将任务委托给 **CODE**。

## 在对话过程中切换模型时
1. 总结当前对话中的相关内容。
2. 将总结内容作为委托指令的一部分发送给子代理。
3. 将子代理的响应结果呈现给用户。
4. 在原始模型（Opus）上继续对话，同时参考子代理的处理结果。

## 工作空间隔离

每个代理都有自己的工作空间目录（在 `openclaw.json` 中定义）。这意味着：
- **子代理无法访问您的工作空间文件**。如果子代理需要文件内容，请将其内容粘贴到指令中。
- **子代理无法修改您的工作空间**。它们的输出会以文本形式返回给用户。
- **子代理之间互不共享信息**。两个子代理在完全隔离的环境中运行。
- **主代理可以读取子代理的响应结果**，但无法直接访问它们的工作空间文件。

这种隔离设计是为了防止子代理意外修改主工作空间。

## OpenClaw 代理配置

要使用路由功能，用户需要在 `openclaw.json` 中配置代理。以下是配置 4 个提供者的推荐设置：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": [
          "google-gemini-cli/gemini-3-pro-preview",
          "openai-codex/gpt-5.3-codex",
          "kimi-coding/k2p5"
        ]
      }
    },
    "list": [
      {
        "id": "main",
        "model": { "primary": "anthropic/claude-opus-4-6" },
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "codex",
        "model": { "primary": "openai-codex/gpt-5.3-codex" },
        "workspace": "~/.openclaw/workspace-codex"
      },
      {
        "id": "gemini-researcher",
        "model": { "primary": "google-gemini-cli/gemini-3-pro-preview" },
        "workspace": "~/.openclaw/workspace-gemini-research"
      },
      {
        "id": "gemini-fast",
        "model": {
          "primary": "google-gemini-cli/gemini-2.5-flash-lite-preview",
          "fallbacks": ["google-gemini-cli/gemini-3-flash-preview"]
        },
        "workspace": "~/.openclaw/workspace-gemini"
      },
      {
        "id": "kimi-orchestrator",
        "model": { "primary": "kimi-coding/k2p5" },
        "workspace": "~/.openclaw/workspace-kimi"
      }
    ]
  }
}
```

如果使用的提供者较少，只需删除不需要的代理。例如：仅使用 Claude 和 Gemini 时，只需从配置列表中删除 `codex` 和 `kimi-orchestrator`，并相应地修改 `fallbacks` 配置。

### 提供者配置

每个非内置提供者都需要进行额外配置。大多数配置信息位于 `openclaw.json` 的 `modelsproviders` 部分，但 **使用订阅服务的 Google Gemini` 需要特殊处理**（详见下文）。

**在 `openclaw.json` 中配置 Codex 和 Kimi 提供者：**
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "openai-codex": {
        "baseUrl": "https://chatgpt.com/backend-api",
        "api": "openai-responses",
        "models": [{ "id": "gpt-5.3-codex" }]
      },
      "kimi-coding": {
        "baseUrl": "https://api.kimi.com/coding/v1",
        "api": "openai-completions",
        "models": [{ "id": "k2p5" }]
      }
    }
  }
}
```

**对于使用订阅服务的 Google Gemini**，请注意以下配置：
**注意**：OpenClaw 的配置文件不接受 `"api": "google-gemini-cli"` 作为有效类型。实际上，运行时系统会自动将其视为可用的服务。正确的配置方法是将 `google-gemini-cli` 添加到每个代理的 `models.json` 文件中（文件路径为 `~/.openclaw/agents/<agent-id>/agent/models.json`）。请注意，这个配置文件不经过官方的验证：

```json
{
  "google-gemini-cli": {
    "api": "google-gemini-cli",
    "models": [
      { "id": "gemini-3-pro-preview" },
      { "id": "gemini-3-flash-preview" },
      { "id": "gemini-2.5-flash-lite-preview" }
    ]
  }
}
```

**对于 Google Gemini（使用订阅服务）的特殊配置：**
- **不要设置 `baseUrl` — 因为 `google-gemini-cli` 服务使用固定的默认端点 (`cloudcode-pa.googleapis.com`)**。设置 `baseUrl` 会导致 404 错误。
- **不要设置 `apiKey` — OAuth 令牌会通过 `Authorization: Bearer` 头部自动获取**。
- **不要将此提供者添加到 `openclaw.json` 中**，否则会导致配置错误。

**重要提示**：对于使用订阅服务的 Google Gemini，`api` 字段是必需的（OpenClaw 2026.2.6 及更高版本）。如果省略此字段，系统会显示错误信息 “No API provider registered for api: undefined”。

Anthropic（`claude-opus-4-6`）已包含在 OpenClaw 的内置模型列表中，因此无需额外配置。

## 协作模式

### 顺序执行（Pipeline）
**适用于需要先收集数据再执行任务的场景**。

### 并行处理 + 合并结果（Parallel + Merge）
**适用于需要探索多种解决方案或时间紧迫的情况**。

### 安全性敏感的任务（Adversarial Review）
**适用于处理涉及敏感信息的代码或关键生产任务的场景**。

### 多代理协调（Orchestrated）
**适用于需要多个代理协同完成复杂任务的场景**。注意：Kimi 的执行速度较慢（39 tok/s），但在任务协调方面表现最佳（TAU-2 得分 0.959）。

## 备用模型链（Fallback Chains）

当某个模型不可用或受到频率限制时，按照以下顺序选择备用模型：Gemini（稳定的 OAuth 访问方式）> Codex（不太稳定的 OAuth 访问方式）> Kimi（使用 API 密钥）。

### 完整的模型组合（Full Stack）
| 任务类型 | 主要使用的模型 | 备用模型 1 | 备用模型 2 | 备用模型 3 |
|-----------|---------|------------|------------|------------|
| 推理任务 | Opus | Gemini Pro | Codex | Kimi K2.5 |
| 代码编写任务 | Codex | Opus | Gemini Pro | — |
| 研究任务 | Gemini Pro | Opus | Codex | — |
| 快速任务 | Flash-Lite | Flash | Opus | — |
| 代理协调任务 | Kimi K2.5 | Codex | Opus | — |

### 使用 Claude 和 Gemini（2 个模型）
| 任务类型 | 主要使用的模型 | 备用模型 1 | 备用模型 2 |
|-----------|---------|------------|------------|
| 推理任务 | Opus | Gemini Pro | — |
| 代码编写任务 | Opus | Gemini Pro | — |
| 研究任务 | Gemini Pro | Opus | — |
| 快速任务 | Flash-Lite | Flash | Opus | — |

### 使用 Claude 和 Codex（2 个模型）
| 任务类型 | 主要使用的模型 | 备用模型 1 |
|-----------|---------|------------|
| 推理任务 | Opus | Codex |
| 代码编写任务 | Codex | Opus |
| 其他所有任务 | Opus | Codex |

### 仅使用 Claude（1 个模型）
所有任务都会路由到 Opus，无需使用备用模型。

## 提供者配置方法

| 提供者 | 认证方式 | 配置命令 |
|----------|-----------|---------------|
| Anthropic | API 令牌 | `openclaw onboard --auth-choice setup-token` |
| Google Gemini | OAuth（通过 CLI 插件） | `openclaw plugins enable google-gemini-cli-auth && openclaw models auth login --provider google-gemini-cli` |
| OpenAI Codex | OAuth（通过 ChatGPT 插件） | `openclaw onboard --auth-choice openai-codex` |
| Kimi | API 密钥（订阅服务） | `openclaw onboard --auth-choice kimi-code-api-key` |

**认证方式的可靠性排序**：Anthropic 令牌（永不过期）> Gemini OAuth（自动刷新）> Kimi API 密钥（静态密钥）> Codex OAuth（较不稳定，因为在其他设备上登录 ChatGPT 可能会导致令牌失效；需要重新运行配置命令）。

## 故障排除

### 如果出现以下问题，请进行相应的处理：
- **“No API provider registered for api: undefined”**：检查自定义提供者的 `api` 字段是否缺失。例如，在 `openclaw.json` 中为 OpenAI Codex 设置 `"api": "openai-responses"`。
- **Google Gemini 报错 “API key not valid”**：检查是否使用了错误的 API 类型。对于使用订阅服务的 Google Gemini，应使用 `"api": "google-gemini-cli"`。
- **Codex 停止工作**：可能是 ChatGPT 的 OAuth 令牌失效。请重新登录或更新配置。

### 其他常见问题及解决方法：
- **Gateway崩溃**：检查 `openclaw.json` 中是否正确配置了提供者的 `api` 字段。
- **Kimi 显示 “missing”**：检查模型的 ID 是否与提供者的目录匹配。
- **子代理返回 “Unknown model”**：确认模型的提供者配置是否正确。

## 订阅计划（截至 2026 年 2 月）

| 提供者 | 订阅计划 | 月费 |
|----------|------|---------|
| Anthropic | Claude Max 5x | $100 |
| Anthropic | Claude Max 20x | $200 |
| OpenAI | ChatGPT Plus | $20 |
| OpenAI | ChatGPT Pro | $200 |
| Google | Gemini Advanced | $20 |
| Moonshot | Kimi Andante | 约 $10 |

## 常见配置方案

| 配置方式 | 月费 | 备注 |
|-------|---------|-------|
| **仅使用 Claude（Max 5x）** | $100 | 不支持任务路由，所有任务由 Opus 处理 |
| **仅使用 Claude（Max 20x）** | $200 | 不支持任务路由，但限制使用频率为 20x |
| **平衡配置（Max 20x + Gemini）** | $220 | 包含 Flash-Lite 的快速处理能力和 Gemini 的高级研究功能 |
| **专注于代码（Max 20x + Gemini + ChatGPT Plus）** | $240 | 包含 Codex 的代码生成和数学计算功能 |
| **全套配置（所有 4 个模型 + ChatGPT Pro）** | $250 | 提供全面的功能和最优的频率限制 |

来源：Artificial Analysis API v4，2026 年 2 月。Codex 的评分数据来源于 OpenAI 的官方博客。