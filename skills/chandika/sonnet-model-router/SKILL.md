---
name: model-router
description: OpenClaw 的自感知多提供商模型路由系统：能够自动检测您可用的模型，推荐最佳的路由模式，并根据具体任务进行动态调整。Claude、Gemini、GPT、DeepSeek 等模型在系统中都作为路由选项存在，这些模型对应的路由信息被存储在路由表中，而非排行榜中。
version: 2.2.0
homepage: https://github.com/chandika/openclaw-model-router
metadata: {"clawdbot":{"emoji":"🧭"}}
---
# OpenClaw模型路由器

将合适的模型分配到相应的任务中。该技能会自动检测用户拥有的模型，告知用户应使用哪些模型，并在用户请求“提高性能”或“节省成本”时做出相应的调整。

## 安全性与隐私

- **本技能不会读取、存储或传输API密钥或凭证。** 它仅从您的网关配置中读取提供者名称和模型ID，以确定可用的模型。
- **不进行自动扫描。** 所有模型检测和网络搜索都由用户触发。除非用户明确要求，否则该技能不会在系统加载或心跳检测时运行。
- **网络搜索** 用于在添加新提供者时从模型卡片页面获取公开的性能测试数据和价格信息。这是正常的出站网络活动。
- **本地状态：** 该技能会将`model-registry.json`文件写入您的工作区（包含性能测试分数、价格和路由规则）。该文件中不存储任何敏感信息。

## 第0步：模型注册表（自学）

该技能在工作区的`model-registry.json`文件中维护一个实时更新的模型注册表。这就是路由器如何自动了解新模型的方式。

### 注册表文件格式

```json
{
  "lastScan": "2026-02-18T08:00:00Z",
  "models": {
    "anthropic/claude-opus-4-6": {
      "provider": "anthropic",
      "name": "Claude Opus 4.6",
      "addedAt": "2026-02-18",
      "pricing": { "input": 15.00, "output": 75.00, "unit": "1M tokens" },
      "context": 200000,
      "strengths": ["deep reasoning", "novel problems", "hard search", "complex coding"],
      "weaknesses": ["expensive", "slower"],
      "benchmarks": {
        "swe-bench": 80.8,
        "osworld": 72.7,
        "arc-agi-2": 75.2,
        "gpqa-diamond": 74.5,
        "gdpval-aa": 1559,
        "hle": 26.3
      },
      "routeTo": ["architecture", "deep-debugging", "novel-reasoning", "hard-search"],
      "tier": "premium"
    }
  },
  "routingRules": {
    "computer-use": "anthropic/claude-sonnet-4-6",
    "deep-reasoning": "anthropic/claude-opus-4-6",
    "office-finance": "anthropic/claude-sonnet-4-6",
    "standard-coding": "anthropic/claude-sonnet-4-6",
    "drafts-summaries": "cheapest-available",
    "hard-coding": "anthropic/claude-opus-4-6"
  }
}
```

### 新模型检测流程

**何时扫描：** 仅当用户明确请求时（例如：“检查新模型”、“扫描模型”、“我有哪些模型”）。系统加载或心跳检测时不会自动扫描。

**工作原理：**

1. **读取当前配置** — 通过`gateway config.get`获取所有配置的提供者和模型。
2. **与注册表对比** — 将配置中的模型与`model-registry.json`中的模型进行比较。
3. **对于每个新发现的模型：**

   a. **获取模型卡片** — 在网页上搜索`"[模型名称] benchmarks pricing model card [年份]"`
   
   b. **提取关键数据：**
      - 价格（每100万个输入所需的费用）
      - 上下文窗口大小
      - 性能测试分数（优先顺序：SWE-bench、OSWorld、GPQA、ARC-AGI-2、GDPval-AA、HLE、MATH-500）
      - 来自评论的优缺点
   
   c. **对模型进行分类：**
      - **高级** — 每100万个输入费用超过10美元（Opus级别）
      - **中等** — 每100万个输入费用在1到10美元之间（Sonnet、GPT-4o、Gemini Pro级别）
      - **经济型** — 每100万个输入费用在0.10到1美元之间（Flash、DeepSeek级别）
      - **免费** — 免费或费用极低
   
   d. **确定路由位置** — 根据性能测试结果，判断该模型相对于现有模型的优势：
      - 将每个模型的性能测试分数与当前最佳模型的分数进行比较
      - 如果新模型在某项性能测试中的得分超过当前模型的3分以上，则标记为更优的选项
      - 如果新模型价格更低且分数相差在2分以内，则标记为更具成本效益的替代方案
   
   e. **更新注册表** — 将模型信息写入`model-registry.json`
   
   f. **通知用户：**
      ```
      🧭 New model detected: [model name]
      
      Provider: [provider]
      Pricing: $X input / $Y output per 1M tokens
      Context: [N] tokens
      Tier: [tier]
      
      Key benchmarks:
      - SWE-bench: XX% (current best: YY% from [model])
      - [other relevant benchmarks]
      
      Routing recommendation:
      - [task type]: This model beats [current model] by X points. Switch?
      - [task type]: Close to [current model] but 3× cheaper. Consider for subagents?
      
      Want me to update routing? Or keep current setup?
      ```

4. **只有在用户允许的情况下才应用更改。** 必须先征求用户同意。

### 路由规则更新

当用户批准为新模型更改路由规则时：

1. 更新`model-registry.json`中的路由规则。
2. 如果是永久性更改，通过`gateway config.patch`应用配置。
3. 将更改记录到每日日志文件中。

当模型从配置中**移除**时：

1. 不要从注册表中删除该模型（保留性能测试数据以供参考）。
2. 将指向已移除模型的所有任务重新路由到下一个可用模型。
3. 通知用户：“模型X已被移除。已将[任务类型]重新路由到[模型Y]。”

### 保持数据更新

- **性能测试数据会过期。** 如果模型条目的创建时间超过90天，则在下次扫描时标记需要更新。
- **模型版本更新。** 如果模型ID发生变化（例如，`gemini-2.5-pro`变为`gemini-3-pro`），则视为新模型。不要假设之前的分数仍然有效。
- **通过网络搜索更新数据。** 在更新时，搜索`"[模型名称] latest benchmarks [当前年份]"并更新相应的分数。

---

## 第1步：检测可用模型

当用户请求查看模型或设置路由时，检查OpenClaw的配置以确定哪些提供者和模型可用：

1. 运行`gateway config.get`或读取`openclaw.json`。
2. 检查`agentsdefaults.model.primary` — 当前的主要模型是什么？
3. 检查`agentsdefaults.subagents.model` — 当前的子代理模型是什么？
4. 检查已配置的提供者（仅通过提供者名称和模型ID进行识别——不要读取或检查API密钥、令牌或认证凭证）。

5. 向用户报告：“您有[X、Y、Z]个可用模型。当前正在使用[模型]作为主要模型/子代理模型。推荐模式：[模式]。需要我为您应用吗？”

**不要盲目猜测。** 先检查，再推荐，只有在获得用户许可后才能应用。

## 第2步：选择模式

提供三种模式。用户可以选择一种，或者根据可用模型进行推荐。

### 🏆 **高性能模式** — “追求最佳效果”

*最佳结果。仅使用Claude模型。但会受速率限制的影响。*

| 角色 | 模型 | 每100万个输入的费用（输入/输出） |
|------|-------|-------------------|
| 主模型 | Opus 4.6 | 15美元 / 75美元 |
| 子代理模型 | Sonnet 4.6 | 3美元 / 15美元 |

**推荐情况：** 用户拥有Claude Max/API权限，并且希望获得“最佳质量”或“不要偷工减料”的结果。适用于关键任务，如架构设计、深度调试或复杂问题。

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-opus-4-6" },
      "subagents": { "model": "anthropic/claude-sonnet-4-6" }
    }
  }
}
```

### ⚖️ **平衡模式** — “常规模式”（推荐默认设置）

*智能路由。质量不错。速率限制能够满足日常需求。*

| 角色 | 模型 | 每100万个输入的费用（输入/输出） |
|------|-------|-------------------|
| 主模型 | Sonnet 4.6 | 3美元 / 15美元 |
| 子代理模型 | Gemini 2.5 Pro | 1.25美元 / 10美元 |

**推荐情况：** 用户同时拥有Claude模型和Google API权限。适用于大多数日常任务，如编码、研究和办公工作。Sonnet适合处理主要任务；Gemini则负责后台工作，效率是Sonnet的2.4倍。

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" },
      "subagents": { "model": "google/gemini-2.5-pro" }
    }
  }
}
```

**变体 — Claude + OpenAI：**
```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" },
      "subagents": { "model": "openai/gpt-4o" }
    }
  }
}
```

### 💰 **经济模式** — “节省成本”

*最低成本。适用于高吞吐量任务。质量仍然足够好。*

| 角色 | 模型 | 每100万个输入的费用（输入/输出） |
|------|-------|-------------------|
| 主模型 | Gemini 2.5 Pro | 1.25美元 / 10美元 |
| 子代理模型 | Gemini 2.5 Flash | 0.18美元 / 0.75美元 |

**推荐情况：** 用户仅使用API权限，且对成本有严格要求。或者希望“节省成本”或“高效运行”。**

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "google/gemini-2.5-pro" },
      "subagents": { "model": "google/gemini-2.5-flash" }
    }
  }
}
```

**超经济模式（使用DeepSeek子代理模型）：**
```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "google/gemini-2.5-pro" },
      "subagents": { "model": "openrouter/deepseek/deepseek-v3.2" }
    }
  }
}
```

---

## 第3步：自适应触发

根据用户的指令建议模式切换（不会自动应用）：

| 用户指令 | 操作建议 |
|-----------|--------|
| “提高性能” / “尝试更努力” / “追求最佳质量” | 建议切换到高性能模式或`/model anthropic/claude-opus-4-6` |
| “节省成本” / “降低费用” | 建议切换到经济模式 |
| “常规模式” / “平衡模式” | 建议切换到平衡模式 |
| “本次任务使用Opus” | 仅针对当前会话应用`/model anthropic/claude-opus-4-6` |
| “使用Gemini” | 仅针对当前会话应用`/model google/gemini-2.5-pro` |
| “使用DeepSeek” | 仅针对当前会话应用`/model openrouter/deepseek/deepseek-v3.2` |
| “重置” / “恢复到默认设置” | 应用`/model default`以恢复到配置默认设置 |

**会话级更改与永久性更改：** `/model X`仅影响当前会话。通过`gateway config.patch`进行的配置更改会在所有会话中持续生效。

---

## 第4步：特定任务的固定路由规则

某些任务有明确的最佳模型。当任务类型明确时，系统会自动进行路由调整：

| 任务类型 | 始终使用 | 原因 | 调整方式 |
|-----------|-----------|-----|-------------|
| 计算机使用 / 浏览器 | Claude（Sonnet或Opus） | 在经济模式下使用Gemini时，计算机使用任务的性能明显优于Claude（72.5% vs 38.2%） | 如用户处于经济模式，建议切换模型 |
| 深度推理 / 复杂问题 | Opus 4.6 | 在需要多步骤推理的问题上，Opus的表现优于Sonnet（75.2% vs 58.3%） | 建议使用Opus |
| 办公 / 财务 / 电子表格 | Sonnet 4.6 | Sonnet的Elo分数（1633）远高于Opus（1559）和GPT（1524） | Sonnet实际上是最佳选择 |
| 简单草稿 / 摘要 / 格式化 | 选择成本最低的模型 | 避免在简单任务上消耗高级模型 | 重新路由到子代理模型或建议使用DeepSeek |
| 编码（常规） | Sonnet 4.6或Opus 4.6 | 在SWE-bench测试中，Claude的表现优于GPT（79.6% vs 80.8%） | 对于复杂代码，建议使用Claude模型 |
| 编码（深度调试、架构设计） | Opus 4.6 | 在Terminal-Bench测试中，Claude的表现优于GPT（62.7% vs 59.1%） | 建议使用Opus |

**关键原则：** 不要所有任务都通过同一模型处理。即使在同一会话中，如果任务类型发生变化，也应建议更换模型。

---

## 性能测试表格

以下是2026年2月的跨提供者性能测试结果，可作为路由参考。

### 如何解读这些数据

每一行代表一个路由决策，而非排名。2分的差距属于正常范围；17分的差距具有指导意义；34分的差距则表明存在明显优势——在这种情况下应避免使用表现较差的模型。

### 编码任务

| 性能测试 | Sonnet 4.6 | Opus 4.6 | GPT-5.2 | Gemini 2.5 Pro |
|-----------|-----------|---------|---------|---------------|
| SWE-bench（验证） | 79.6% | 80.8% | 77.0% | 约75% |
| Terminal-Bench 2.0 | 59.1% | 62.7% | 46.7% | — |

→ Claude模型在常规编码任务中表现最佳；GPT和Gemini的表现较弱。

### 计算机使用任务

| 性能测试 | Sonnet 4.6 | Opus 4.6 | GPT-5.2 |
|-----------|-----------|---------|---------|
| OSWorld（验证） | 72.5% | 72.7% | 38.2% |
| Pace Insurance | 94% | — | — |

→ 在计算机使用任务中，始终推荐使用Claude模型。Claude与GPT之间的34分差距说明它们属于不同的性能级别。

### 推理任务

| 性能测试 | Sonnet 4.6 | Opus 4.6 | GPT-5.2 |
|-----------|-----------|---------|---------|
| GPQA Diamond | 74.1% | 74.5% | 73.8% |
| ARC-AGI-2 | 58.3% | 75.2% | — |
| Humanity’s Last Exam | 19.1% | 26.3% | 20.3% |
| MATH-500 | 97.8% | 97.6% | 97.4% |

→ 在GPQA和MATH任务中，三种模型的表现相近，可根据成本进行选择；ARC-AGI-2和HLE任务则建议使用Opus模型。

### 办公和领域相关任务

| 性能测试 | Sonnet 4.6 | Opus 4.6 | GPT-5.2 |
|-----------|-----------|---------|---------|
| GDPval-AA（办公领域） | 1633 | 1559 | 1524 | Sonnet在办公任务中的表现优于其他模型 |
| Finance Agent | 63.3% | 62.0% | 60.7% |
| MCP-Atlas工具 | 61.3% | 60.3% | — |

→ Sonnet在办公、财务和工具协调任务中表现最佳。

### 价格（每100万个输入）

| 模型 | 输入 | 输出 | OpenClaw提供者 | 相对成本 |
|-------|-------|--------|-------------------|----------|
| DeepSeek V3.2 | 0.14美元 | 0.28美元 | `openrouter/deepseek/deepseek-v3.2` | 比Opus便宜107倍 |
| Gemini 2.5 Flash | 0.18美元 | 0.75美元 | `google/gemini-2.5-flash` | 比Opus便宜100倍 |
| Grok 4.1 Fast | 0.20美元 | 0.50美元 | `xai/grok-4.1-fast` | 比Opus便宜75倍 |
| Gemini 2.5 Pro | 1.25美元 | 10.00美元 | `google/gemini-2.5-pro` | 比Opus便宜12倍 |
| Sonnet 4.6 | 3.00美元 | 15.00美元 | `anthropic/claude-sonnet-4-6` | 比Opus便宜5倍 |
| GPT-4o | 5.00美元 | 15.00美元 | `openai/gpt-4o` | 比Opus便宜3倍 |
| GPT-5.2 | — | — | `openai/gpt-5.2` | — |
| Opus 4.6 | 15.00美元 | 75.00美元 | `anthropic/claude-opus-4-6` | 最昂贵 |

---

## 提供者检测

在检查可用模型时，使用`gateway config.get`查看配置的提供者名称和模型ID。**不要读取或检查API密钥、令牌或认证凭证**。您只需要知道哪些提供者已被配置即可。

请检查配置文件中的`modelsproviders`以了解自定义设置。

**默认策略：**  
- 如果仅支持Anthropic模型，则推荐高性能模式。  
- 如果同时支持Anthropic和Google模型，则推荐平衡模式。  
- 如果仅支持Google模型，则推荐经济模式。  
- 如果所有模型都可用，则推荐平衡模式（默认设置）。

---

## 先决条件

- **需要OpenClaw v2026.2.17或更高版本**，以便在模型注册表中使用Sonnet 4.6模型。  
  - Docker：`docker pull openclaw/openclaw:latest`  
  - Git：`openclaw update`  
- **至少需要一个已配置认证信息的提供者**  
- 如果需要使用多个提供者，则需要在OpenClaw中配置额外的提供者API密钥。

---

## 模式切换

**会话级切换：** 使用`/model google/gemini-2.5-pro`切换回`/model default`。

**永久性切换：** 通过`gateway config.patch`命令进行配置更改，或编辑`openclaw.json`后重启应用。

**代理应理解的快速命令：**
- “切换到高性能模式” → 应用高性能配置  
- “切换到经济模式” → 应用经济模式配置  
- “切换到平衡模式” → 应用平衡模式配置  
- “本次任务使用Opus” → 仅针对当前会话应用该配置  
- “恢复到默认设置” → 应用`/model default`命令  

---

## 初始注册表生成

在首次运行时（如果`model-registry.json`文件不存在），该技能应：

1. 使用上述性能测试数据创建`model-registry.json`文件。
2. 扫描当前配置，标记实际可用的模型。
3. 向用户提供完整的状态报告：

```
🧭 Model Router initialized.

Available providers: Anthropic ✅, Google ✅, OpenAI ❌, xAI ❌
Available models: Opus 4.6, Sonnet 4.6, Gemini 2.5 Pro, Gemini 2.5 Flash

Current config: Opus main / Sonnet subagents (Performance mode)
Recommended: Balanced mode — Sonnet main / Gemini Pro subagents
  → Saves 2.4× on subagent costs, same quality for background tasks

Apply balanced mode? [yes/no]
```

**使用性能测试表格中的所有模型初始化注册表**，即使某些模型当前未配置也是如此。这样当新模型出现时，代理仍能进行比较。

---

## 设计理念

性能测试表格只是用于指导路由的参考，并非排名。2分的差距属于正常范围；34分的差距则表明存在明显优势，应避免使用表现较差的模型。

选择合适的模型取决于具体任务。该技能的作用是了解用户拥有的模型及其各自的优势，并据此进行路由分配。

它为用户提供模型选择和决策框架，帮助用户做出最佳决策。