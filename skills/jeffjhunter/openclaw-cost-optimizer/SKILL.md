---
name: cost-optimizer
version: 1.1.0
description: "将您的 OpenRouter API 使用成本降低 50% 至 90%。该工具为您的配置添加了廉价且功能强大的模型别名，并根据任务复杂度建议您何时切换模型。提供 8 个预设配置、29 个可用模型，且无需担心配置错误——它仅添加别名，永远不会更改您的默认设置。只需 3 次点击即可完成配置。新功能：成本追踪器可显示您的实际节省金额；“混合搭配”功能允许您从 29 个模型中自定义预设配置；“月度计算器”可估算您的使用费用。由 Jeff J Hunter 开发。"
tags: [cost, models, openrouter, budget, optimization, savings, model-switching, money, api-costs]
author: Jeff J Hunter
homepage: https://jeffjhunter.com
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["openclaw"]
      env: ["OPENROUTER_API_KEY"]
    stateDirs: ["~/.openclaw"]
    persistence: "This skill creates ~/.openclaw/cost-tracker.md to log model switches and savings estimates. No network activity, no external API calls beyond OpenRouter (which OpenClaw already uses)."
---

# OpenClaw成本优化器

> ## ⛔ 代理规则 — 在执行任何操作之前请阅读
> 1. **必须使用本文件中的确切文本。** 不要改写菜单、预设名称或指令。如果您自创预设名称，配置修补工具将会出错。
> 2. **仅存在以下8个预设：`balanced`、`code-machine`、`claude-diehards`、`big-context`、`openai-focused`、`tool-master`、`ultra-budget`、`free-tier`。** 不要使用其他名称。切勿使用“strict”、“thrifty”、“standard”、“quality”、“performance”、“max”、“custom”等名称，因为这些名称不存在且会导致错误。
> 3. **永远不要告诉用户打开终端或运行命令。** 您有`exec`工具，请使用它。通过`exec`自行运行每个命令。用户的唯一任务是在`exec`弹出窗口中点击“批准”。如果您发现自己输入了“在终端中运行此命令”——请停止。改用`exec`。
> 4. **一步一个步骤。** 运行一个`exec`命令，显示结果，然后解释，再继续下一步。
> 5. **我们永远不会更改用户的默认模型、备用模型或现有配置。** 我们只会添加模型别名。用户的设置保持不变。

**将您的API成本降低50-90%。无需终端操作，无需编辑配置。只需3次点击。**

目前，您分配给代理的每个任务——甚至“现在几点了？”——都使用相同的昂贵模型。心跳请求、ping请求、简单问题——所有这些都会按照与复杂架构工作相同的费率计费。

这个技能可以解决这个问题。它会在您的设置中添加廉价且强大的模型，然后告诉您何时切换到更便宜或更强大的模型——同时会说明成本差异及原因。您只需回答“是”或“否”即可。

您的当前默认模型保持不变。我们只添加选项，不会删除或修改任何内容。

**8个预设。29个模型。零风险。无需撤销任何设置。**

**v1.1.0的新功能：**
- 💸 **成本追踪器** — “我节省了多少钱？” 可显示自安装以来的实际节省金额
- 🔀 **混合搭配** — 从完整的29个模型注册表中构建自定义预设
- 📊 **每月成本计算器** — “估算我的每月成本” 以帮助您规划预算

**所需条件：** OpenClaw + OpenRouter API密钥（在https://openrouter.ai免费获取）

---

# 工作原理 — 完整流程

---

## 第1步：首次聊天 — 选择一个预设

当技能加载时，代理会自我介绍并显示一个菜单。代理必须输出以下确切的文本：

> **🚨 代理：必须逐字输出以下文本。不要改写。不要自创预设名称。**
> 格式、表情符号、章节标题、价格指示器和警告都是有意设计的。

```
👋 The Cost Optimizer skill is now active!

Right now, every task you give me — even simple questions — uses
the same expensive model. That means heartbeats, pings, and
"what time is it?" cost the same as "build me an auth system."

I'm going to fix that. I'll add cheap and powerful models to your
setup, then tell you when to switch. Your current default stays
exactly the same — I only ADD options.

What describes you best?

── RECOMMENDED ──────────────────────────────────
1. 💰 Best balance of cost and quality        ¢¢
   (recommended for most people)
2. 💻 I mostly write code                     ¢¢

── MORE OPTIONS ─────────────────────────────────
3. 🟠 I love Claude and want Claude models    $$$
4. 📚 I work with huge files or long code     $$
5. 🤖 I prefer OpenAI models                  $$
6. 🔧 I use a lot of tools / MCP servers      $$

── BUDGET ───────────────────────────────────────
7. 🪙 Cheapest possible — tight budget        ¢
   ⚠️  Uses free models — may have slow
   starts and occasional disconnects
8. 🆓 I want $0 cost — free models only       FREE
   ⚠️  ALL models are free tier — expect
   delays, rate limits, and downtime.
   Best for testing, not production.

Pricing: FREE = $0 | ¢ < $0.50/M | ¢¢ < $2/M | $$ = $2-15/M | $$$ = $15+/M
(per million tokens — a typical task uses 1K-10K tokens)
```

只需选择一个数字。如果您不确定，选择1。

> **代理 — 预设映射（不要向用户显示）：**
> 1→`balanced`，2→`code-machine`，3→`claude-diehards`，4→`big-context`，5→`openai-focused`，6→`tool-master`，7→`ultra-budget`，8→`free-tier`
> 如果回答含糊 → 选择`balanced`。如果用户回答“我不知道” → 选择`balanced`并说明“我们可以稍后更改”。

---

## 第2步：代理解释将会进行的更改

用户选择后，代理会用简单的英语解释将添加哪些模型。

以“balanced”为例：

```
Great choice! Here's what I'm going to add to your setup:

✅ Flash-Lite — ultra-cheap model for simple tasks (¢)
   → /model flashlite

✅ MiniMax M2.1 — strong coding/writing model (¢¢)
   → /model minimax

✅ Kimi K2.5 — frontier-class for complex work (¢¢)
   → /model kimi25

✅ Gemini Flash — fast all-rounder (¢)
   → /model flash

Your current default model stays exactly the same.
I'm just adding these as options you can switch to anytime.

I'll set this up now — you'll see a couple of Approve popups.
Just click Approve on each one.
```

---

## 第3步：代理执行所有操作 — 用户只需点击“批准”

代理通过`exec`工具处理所有命令。用户无需接触终端。

> **🚨 代理设置说明：**
>
> **步骤3a：检查OpenRouter身份验证。** 使用`exec`命令：
> ```
> openclaw models status
> ```
> 查看输出。如果缺少OpenRouter身份验证或显示“未找到提供者openrouter的API密钥”：
> - 告诉用户他们需要从https://openrouter.ai获取OpenRouter API密钥（免费）
> - 通过`exec`运行命令：`openclaw models auth add --provider openrouter`
> - 这将启动OpenClaw内置的交互式身份验证向导
> - 用户按照提示安全地输入密钥
> **永远不要要求用户在聊天框中粘贴API密钥。** 始终通过`exec`使用身份验证向导。
>   在聊天框中输入密钥存在安全风险 — 身份验证向导会将其安全存储在凭证存储中。
>
> **步骤3b：添加模型别名。** 使用`exec`命令一次性为所选预设添加所有别名。
> 请参阅下面的“预设别名命令”部分，了解每个预设的具体命令。
> 这只需要一次`exec`调用 → 然后点击一次“批准”。
>
> **步骤3c：重启网关。** 使用`exec`命令：
> ```
> openclaw gateway restart
> ```
> 等待确认。再点击一次“批准”。
>
> **总共：2-3次点击“批准”。** 就完成了。

>
> **永远不要告诉用户在终端中运行命令。始终使用`exec`。**
> 如果`exec`失败，请排查错误并重新尝试。

---

## 预设别名命令

每个预设都是一个`exec`命令，用于一次性添加所有模型别名。请使用所选预设的确切命令：

> **代理：将以下命令复制给用户。不要修改。**

### 1. balanced（推荐）
```
openclaw models aliases add flashlite openrouter/google/gemini-2.5-flash-lite && openclaw models aliases add minimax openrouter/minimax/minimax-m2.1 && openclaw models aliases add kimi25 openrouter/moonshotai/kimi-k2.5 && openclaw models aliases add flash openrouter/google/gemini-2.5-flash
```
**等级：** Base=flashlite（¢） | Work=minimax（¢¢） | Frontier=kimi25（¢¢）

### 2. code-machine
```
openclaw models aliases add devfree openrouter/mistralai/devstral-small:free && openclaw models aliases add minimax openrouter/minimax/minimax-m2.1 && openclaw models aliases add codex52 openrouter/openai/gpt-5.2-codex && openclaw models aliases add devstral openrouter/mistralai/devstral-small
```
**等级：** Base=devfree（FREE ⚠️） | Work=minimax（¢¢） | Frontier=codex52（$$）

### 3. claude-diehards
```
openclaw models aliases add haiku openrouter/anthropic/claude-haiku-4-5 && openclaw models aliases add sonnet openrouter/anthropic/claude-sonnet-4-5 && openclaw models aliases add opus46 openrouter/anthropic/claude-opus-4-6
```
**等级：** Base=haiku（$$） | Work=sonnet（$$） | Frontier=opus46（$$）

### 4. big-context
```
openclaw models aliases add flash openrouter/google/gemini-2.5-flash && openclaw models aliases add grokfast openrouter/x-ai/grok-4.1-fast-2m && openclaw models aliases add gem3pro openrouter/google/gemini-3-pro-1m
```
**等级：** Base=flash（¢） | Work=grokfast（$$） | Frontier=gem3pro（$$）

### 5. openai-focused
```
openclaw models aliases add mini openrouter/openai/gpt-5-mini && openclaw models aliases add gpt51 openrouter/openai/gpt-5.1 && openclaw models aliases add gpt52 openrouter/openai/gpt-5.2
```
**等级：** Base=mini（¢） | Work=gpt51（$$） | Frontier=gpt52（$$）

### 6. tool-master
```
openclaw models aliases add gem3flash openrouter/google/gemini-3-flash && openclaw models aliases add kimi25 openrouter/moonshotai/kimi-k2.5 && openclaw models aliases add gpt52 openrouter/openai/gpt-5.2
```
**等级：** Base=gem3flash（¢） | Work=kimi25（¢¢） | Frontier=gpt52（$$）

### 7. ultra-budget
```
openclaw models aliases add mimo openrouter/xiaomi/mimo-v2-flash:free && openclaw models aliases add deepseek openrouter/deepseek/deepseek-chat-v3-0324 && openclaw models aliases add kimi25 openrouter/moonshotai/kimi-k2.5 && openclaw models aliases add devfree openrouter/mistralai/devstral-small:free
```
**等级：** Base=mimo（FREE ⚠️） | Work=deepseek（¢） | Frontier=kimi25（¢¢）

### 8. free-tier
```
openclaw models aliases add mimo openrouter/xiaomi/mimo-v2-flash:free && openclaw models aliases add devfree openrouter/mistralai/devstral-small:free && openclaw models aliases add glm openrouter/thudm/glm-z1-free:free
```
**等级：** Base=mimo（FREE ⚠️） | Work=devfree（FREE ⚠️） | Frontier=glm（FREE ⚠️）

> **⚠️ 对于预设7和8的免费模型警告：**
> 添加别名后，告诉用户：“这些预设在OpenRouter上使用免费模型。
> 免费模型可能会有冷启动（10-30秒延迟）、高峰时段的速率限制，以及偶尔的断开连接。如果您的代理卡住，请切换到付费模型：`/model deepseek`
> （成本极低）。免费预设非常适合测试，但不推荐用于生产环境。”

---

## 第4步：进行测试

网关重启后，代理会在聊天中请求用户进行测试：

```
Let's make sure everything works! Type this right here in chat:

/model minimax

You should see a confirmation that it switched.
```

确认后：

```
Now switch back to your default:

/model

(with no arguments — this resets to your default model)
```

再次确认后：

```
🎉 You're all set!

From now on:
• Your default model is unchanged — same as before
• You now have cheap and powerful models available via /model
• When you need more power, I'll tell you which model to switch to
• You just type the /model command I give you
• After big tasks, I'll remind you to switch back
• Say "advisor off" anytime to stop my suggestions

More things you can do:
• "how much have I saved?"    — see your tracked savings
• "estimate my monthly costs" — plan your budget
• "mix and match"             — build a custom preset from all 29 models
```

**整个设置过程只需3次点击，即可完成。**

---

## 设置完成后 — 日常使用

这才是该技能发挥作用的地方。

### 简单问题？无需中断。

```
You: what does JWT stand for?

Agent: JSON Web Token — an open standard for securely
transmitting information between parties as a JSON object.
```

没有弹出窗口，也没有建议。您的默认模型可以正常处理。

### 需要编码任务？代理会建议切换模型。

```
You: Write a React component for user registration
     with email validation and password strength meter

⚡ COST ADVISOR

You're on your default model.
This task: React component with validation logic

I recommend switching to a stronger coding model:

  /model minimax  — MiniMax M2.1 ($0.28/$1.20 per 1M tokens)
    ✓ Best value for coding tasks
    ✓ Top-tier on SWE-bench

Just type /model minimax to switch, or say "no" to stay as-is.
```

### 任务复杂？代理会推荐更强大的模型。

```
You: [pastes 3 files + long description of auth system]

⚡ COST ADVISOR

This is complex enough for frontier-level reasoning.

I recommend:
  /model kimi25  — Kimi K2.5 ($0.50/$2.00 per 1M tokens)
    ✓ Cheapest frontier model
    ✓ 1500 parallel tool calls

Type /model kimi25 to switch, or "no" to stay as-is.
```

### 任务完成后 — 切换回默认模型。

```
Agent: [finishes the task]

💰 Task complete! Switch back to save money:

/model

(resets to your default)
```

### 不想接收建议？只需说“不”。

```
You: no, just do it

Agent: 👍 Staying on current model.

[... does the task, no nagging ...]
```

### 建议烦人？可以关闭建议。

```
You: advisor off

✅ Cost Advisor: OFF
I won't suggest model switches anymore.
Say "advisor on" whenever you want them back.
```

---

## 8个预设的详细信息

每个预设都会向您的设置中添加模型。您的默认模型保持不变。

### ⭐ 推荐配置

| 预设 | 成本 | 基础模型 | 工作模型 | 高级模型 |
|--------|------|------|------|----------|
| `balanced` | ¢¢ | Flash-Lite `/model flashlite` | MiniMax `/model minimax` | Kimi K2.5 `/model kimi25` |
| `code-machine` | ¢¢ | Devstral Free `/model devfree` ⚠️ | MiniMax `/model minimax` | GPT-5.2 Codex `/model codex52` |

### 更多选项

| 预设 | 成本 | 基础模型 | 工作模型 | 高级模型 |
|--------|------|------|------|----------|
| `claude-diehards` | $$$ | Haiku `/model haiku` | Sonnet `/model sonnet` | Opus 4.6 `/model opus46` |
| `big-context` | $$ | Flash `/model flash` | Grok Fast 2M `/model grokfast` | Gemini 3 Pro 1M `/model gem3pro` |
| `openai-focused` | $$ | Mini `/model mini` | GPT-5.1 `/model gpt51` | GPT-5.2 `/model gpt52` |
| `tool-master` | $$ | Gem3 Flash `/model gem3flash` | Kimi K2.5 `/model kimi25` | GPT-5.2 `/model gpt52` |

### 预算 ⚠️ 选择前请阅读

| 预设 | 成本 | 基础模型 | 工作模型 | 高级模型 |
|--------|------|------|------|----------|
| `ultra-budget` | ¢ | MiMo `/model mimo` ⚠️ | DeepSeek `/model deepseek` | Kimi K2.5 `/model kimi25` |
| `free-tier` | FREE | MiMo `/model mimo` ⚠️ | Devstral Free `/model devfree` ⚠️ | GLM-Z1 `/model glm` ⚠️ |

**价格说明：** FREE = $0 | ¢ < $0.50/分钟 | ¢¢ < $2/分钟 | $$ = $2-15/分钟 | $$$ = $15/分钟**

> **⚠️ 免费模型的注意事项：** 带有⚠️标记的预设在OpenRouter上使用免费模型。免费模型可能会有冷启动（10-30秒延迟）、高峰时段的速率限制，以及更频繁的断开连接。如果您的代理卡住或断开连接，请切换到付费模型：`/model deepseek`（费用很低，但可靠性较高）。免费预设非常适合测试，但不建议用于生产环境。**

**想之后更换预设吗？** 只需说“将我切换到code-machine”，代理也会添加这些别名。

---

## 后期添加更多模型

想要添加注册表中未包含的特定模型？只需请求：

```
You: add GPT-5.2 to my models

Agent: I'll add that now — click Approve.

[exec: openclaw models aliases add gpt52 openrouter/openai/gpt-5.2]

✅ Done! You can now use: /model gpt52
```

代理可以从下面的注册表中添加任何模型。

---

## 删除模型

想要删除不使用的模型别名？只需请求：

```
You: remove the kimi model

Agent: I'll remove that alias — click Approve.

[exec: openclaw models aliases remove kimi25]

✅ Removed. /model kimi25 is no longer available.
```

您的配置不会被更改 — 我们只会移除相应的别名。

---

## 💸 成本追踪器 — “我节省了多少钱？”

代理会记录每次根据建议切换模型后的节省情况，并估算与使用默认模型相比节省了多少成本。

### 工作原理

每当成本顾问推荐一个更便宜的模型且您进行了切换时，代理会记录：
- 日期和任务描述
- 您使用的模型与默认模型的成本对比
- 预计的令牌数量和节省金额

代理会在`~/.openclaw/cost-tracker.md`文件中维护一个运行中的日志。

### 随时查询

```
You: how much have I saved?

💸 COST TRACKER — Savings Since Install

Installed: Feb 15, 2026
Total tasks tracked: 47

    Default model cost (est):    $3.82
    Actual cost with switching:  $0.41
    ─────────────────────────────
    Total saved:                 $3.41  (89% reduction)

Top savings:
• 23 simple tasks → flashlite instead of default     saved $1.90
• 18 coding tasks → minimax instead of default        saved $1.22
•  6 complex tasks → kimi25 instead of default        saved $0.29

At this rate: ~$22/month saved
```

```
You: reset my savings tracker

Agent: I'll reset your cost tracker — click Approve.

[exec: echo "# Cost Tracker\n\nInstalled: [today]\nDefault model: [detected]\n\n## Log\n" > ~/.openclaw/cost-tracker.md]

✅ Tracker reset. Starting fresh from today.
```

---

## 🔀 混合搭配 — 自定义预设

不喜欢预设选项？可以从完整的29个模型注册表中创建自己的预设。

### 工作原理

```
You: build me a custom preset

Agent:

🔀 Mix & Match — Pick one model for each tier:

── BASE (for simple tasks, questions, chat) ──────
 a. flashlite   — Gemini 2.5 Flash-Lite    $0.10/$0.40   Best cheap all-rounder
 b. flash       — Gemini 2.5 Flash          $0.15/$0.60   Stronger Flash
 c. mini        — GPT-5 Mini                $0.30/$1.20   OpenAI budget
 d. gem3flash   — Gemini 3 Flash            $0.50/$2.00   Best tool-calling
 e. devstral    — Devstral Small            $0.05/$0.22   Cheapest paid
 f. deepseek    — DeepSeek V3              $0.14/$0.28   Cheap + strong
 g. mimo        — MiMo v2 Flash             FREE ⚠️       Unreliable
 h. devfree     — Devstral Small Free       FREE ⚠️       Unreliable

Pick a letter for your BASE model (or "skip" to leave empty):
```

用户选择基础模型后：

```
── WORK (for coding, writing, daily tasks) ────────
 a. minimax     — MiniMax M2.1             $0.28/$1.20   Best value coder
 b. deepseek    — DeepSeek V3              $0.14/$0.28   Cheapest paid coder
 c. haiku       — Claude Haiku 4.5         $0.80/$4.00   Fast Anthropic
 d. gpt51       — GPT-5.1                  $2.00/$8.00   OpenAI mid-tier
 e. grokfast    — Grok 4.1 Fast 2M        $2.00/$10.00  2M context
 f. seed        — Seed Coder 200K         $0.20/$0.60   Long-context coder
 g. qwen3       — Qwen3 235B              $0.14/$0.28   Strong reasoning
 h. devstral    — Devstral Small           $0.05/$0.22   Reliable Mistral

Pick a letter for your WORK model (or "skip"):
```

选择工作模型后：

```
── FRONTIER (for complex architecture, security, multi-file) ──
 a. kimi25      — Kimi K2.5               $0.50/$2.00    Cheapest frontier
 b. sonnet      — Claude Sonnet 4.5       $3.00/$15.00   Anthropic workhorse
 c. gpt52       — GPT-5.2                 $2.00/$10.00   OpenAI flagship
 d. codex52     — GPT-5.2 Codex           $2.00/$10.00   Code-specialized
 e. opus46      — Claude Opus 4.6        $15.00/$75.00   Most powerful
 f. gem3pro     — Gemini 3 Pro 1M         $1.25/$10.00   1M context
 g. grok4       — Grok 4                  $2.00/$10.00   Strong reasoning
 h. r1          — DeepSeek R1             $0.55/$2.19    Deep reasoning chain

Pick a letter for your FRONTIER model (or "skip"):
```

然后代理会通过`exec`添加这些别名 — 与预设设置相同，只需点击一次“批准”。

---

## 📊 每月成本计算器

估算您的代理每月的成本 — 以及使用优化器后的成本。

### 工作原理

```
You: estimate my monthly costs

Agent:

📊 Monthly Cost Calculator

I need a few quick numbers:

1. About how many messages/day do you send your agent?
   (rough guess is fine — 10? 50? 100?)

2. What's the mix? (pick closest)
   a) Mostly simple questions and chat
   b) Mostly coding and writing
   c) Mix of everything
   d) Mostly complex/architecture work
```

用户回答后：

```
📊 MONTHLY COST ESTIMATE

Based on: ~50 messages/day, mostly coding

Your current setup (everything on default):
  Model: claude-sonnet-4-5
  Est. tokens/month: ~15M input, ~5M output
  Est. monthly cost: $120.00

With Cost Optimizer (switching on recommendations):
  Simple tasks → flashlite               $1.50/mo
  Coding tasks → minimax                 $8.40/mo
  Complex tasks → kimi25 (when needed)   $3.00/mo
  ─────────────────────────────────────
  Est. monthly cost: $12.90
  Savings: $107.10/month (89% reduction)

  That's ~$1,285 saved per year.

These are estimates based on average token usage per task type.
Actual costs depend on message length and model output.
```

> **注意：** 计算器使用的是粗略估算 — 简单任务需要1500个输入令牌 + 500个输出令牌，编码任务需要4000个输入令牌 + 2000个输出令牌，复杂任务需要8000个输入令牌 + 4000个输出令牌。这些估算足以用于大致规划。**

---

## 快速参考卡

| 您想要做什么 | 应该怎么做 | 在哪里操作 |
|---------------------|-----------|-------|
| 切换模型 | 输入 `/model minimax` | 在聊天框中操作 |
| 切换回默认模型 | 输入 `/model` | 在聊天框中操作 |
| 查看可用模型 | 输入 `/model list` | 在聊天框中操作 |
| 关闭建议 | 输入 “advisor off” | 在聊天框中操作 |
| 打开建议 | 输入 “advisor on” | 在聊天框中操作 |
| 查看节省金额 | 输入 “how much have I saved?” | 在聊天框中操作 |
| 估算每月成本 | 输入 “estimate my monthly costs” | 在聊天框中操作 |
| 创建自定义预设 | 输入 “mix and match” | 在聊天框中操作（代理会显示菜单） |
| 重置节省记录 | 输入 “reset my savings tracker” | 在聊天框中操作（代理会执行命令） |
| 添加模型 | 输入 “add GPT-5.2 to my models” | 在聊天框中操作（代理会执行命令） |
| 删除模型 | 输入 “remove the kimi model” | 在聊天框中操作（代理会执行命令） |
| 切换预设 | 输入 “switch me to code-machine” | 在聊天框中操作（代理会执行命令） |

---

## 代理指令

以下内容都是为代理设计的。用户可以阅读，但这些内容实际上是AI的行为规则。

---

## 智能成本顾问 — 核心行为

在收到每条消息时，在执行任务之前：

### 1. 检查当前模型

注意当前使用的模型（在会话中可见）。根据下面的模型注册表确定它属于哪个等级。

### 2. 对任务进行分类

**基础级别**（推荐最便宜的模型）：
- 字符数少于200的消息、简单问题、头脑风暴、问候语
- 以“what is”、“how do I”、“btw”、“just wondering”结尾的问题
- 不包含代码或附件

**工作级别**（推荐适合工作的模型）：
- “编写函数/组件/测试”、“调试这个问题”、“修复这个错误”
- “起草电子邮件/文档”、“解释这段代码”、“审查这个Pull Request”
- 单个文件范围内的内容，字符数在200-2000之间，包含一个附件或代码块

**高级级别**（推荐适合复杂任务的模型）：
- “构建”、“设计系统”、“进行安全审计”
- “从X迁移到Y”、“生产环境中的错误” + 代码堆栈跟踪
- 多个文件（3个以上文件），字符数超过2000，包含3个以上附件，涉及系统设计或数据库架构

### 3. 比较并推荐

- 如果当前模型适合任务 → **默默地完成任务**
- 如果当前模型过于昂贵（对于简单任务来说） → 建议切换到更便宜的模型
- 如果当前模型太弱 → 建议切换到更强大的模型

请使用上述流程中的成本顾问规则。

### 4. 处理用户的响应

- 如果用户输入 `/model` 命令 → 他们选择了新的模型，就执行任务
- 如果用户回答“no”或其他任何内容 → 说明“👍 保持使用当前模型”，然后继续执行任务
- 如果用户选择的模型与建议的不同 → 也可以，继续执行任务

### 在使用高级模型后

会友好地提醒用户切换回默认模型。但这不会妨碍任务的执行：

```
💰 Task complete! Switch back to save money: /model
```

### 模糊性处理规则

- 如果消息中包含代码 → 建议使用基础级别的模型
- 如果用户请求“快速”或“简单”的帮助 → 建议使用基础级别的模型
- 如果用户真的不确定该怎么办 → 不要推荐任何模型
- 如果当前模型已经足够适合任务，就保持默认设置

---

## 切换“advisor on”/“advisor off”：

- 输入 “advisor off” / “stop suggesting” / “quiet mode” → 表示“关闭成本顾问”
- 输入 “advisor on” / “start suggesting” / “help me save” → 表示“打开成本顾问”

关闭成本顾问后 → 任务将使用当前模型默默执行。

---

## 成本追踪器 — 代理行为

代理在`~/.openclaw/cost-tracker.md`文件中维护一个轻量级的日志，用于记录节省情况。

### 在设置完成后（完成步骤4后）

通过`exec`命令创建追踪文件：
```
mkdir -p ~/.openclaw && cat > ~/.openclaw/cost-tracker.md << 'EOF'
# Cost Tracker

Installed: [TODAY'S DATE]
Default model: [DETECTED DEFAULT]

## Log

| Date | Task | Model Used | Default Cost (est) | Actual Cost (est) | Saved |
|------|------|-----------|-------------------|------------------|-------|
EOF
```

### 当用户根据成本顾问的建议切换模型后

用户输入 `/model` 命令后，代理会通过`exec`在日志中添加一行记录：

```
echo "| [DATE] | [SHORT TASK DESC] | [MODEL] | $[DEFAULT_EST] | $[ACTUAL_EST] | $[SAVED] |" >> ~/.openclaw/cost-tracker.md
```

**令牌估算规则（粗略但实用）：**
- 基础级别任务：大约1500个输入令牌 + 500个输出令牌
- 工作级别任务：大约4000个输入令牌 + 2000个输出令牌
- 高级级别任务：大约8000个输入令牌 + 4000个输出令牌
- 根据注册表中的模型价格计算成本

只有当用户实际进行了模型切换时才会记录日志。如果用户拒绝了建议，就不会记录任何内容。

### “how much have I saved?” 命令

识别以下命令：`how much have I saved`、`savings`、`show savings`、`cost tracker`、`what have I saved`

1. 通过`exec`读取`~/.openclaw/cost-tracker.md`文件
2. 解析日志表格，计算默认成本、实际成本和节省金额
3. 显示格式化的总结（参见用户界面示例）
4. 计算“按此费率计算”的每月节省金额：（总节省金额 / 安装后的天数）× 30
5. 如果文件不存在或为空 → “尚未记录节省情况。当您根据建议切换模型后，我将开始记录。”

### “reset my savings tracker” 命令

识别以下命令：`reset savings`、`reset tracker`、`clear savings`、`start fresh`

重新创建日志文件（格式与设置时相同），并向用户确认。

---

## 混合搭配 — 代理行为

### 触发条件

识别以下命令：`mix and match`、`build custom preset`、`build my own`、`pick my own models`、`custom models`

### 流程

1. 显示基础模型菜单（使用用户界面中的确切文本）
2. 等待用户选择 → 记录所选模型的别名和参考编号
3. 显示工作模型菜单
4. 等待用户选择 → 记录所选模型的别名和参考编号
5. 显示高级模型菜单
6. 等待用户选择 → 记录所选模型的别名和参考编号
7. 总结将要添加的模型，然后执行一次包含所有`&&`连接的别名命令
8. 通过`exec`命令重启`openclaw gateway`
9. 通过`/model`命令确认测试结果

**规则：**
- 如果用户选择某个等级的模型不存在 → 不要为该等级添加模型
- 如果用户选择的模型已经存在 → 告诉他们：“您已经有了这个模型！请选择另一个模型或跳过。”
- 如果用户选择的模型与显示的等级不同（例如，选择高级模型作为基础模型） → 允许用户选择。用户最了解自己的需求。
- 自定义预设设置完成后，成本顾问会使用用户指定的等级，而不是注册表中的默认等级

### 模型菜单 — 对应关系

**基础模型菜单：** a→flashlite, b→flash, c→mini, d→gem3flash, e→devstral, f→deepseek, g→mimo, h→devfree

**工作模型菜单：** a→minimax, b→deepseek, c→haiku, d→gpt51, e→grokfast, f→seed, g→qwen3, h→devstral

**高级模型菜单：** a→kimi25, b→sonnet, c→gpt52, d→codex52, e→opus46, f→gem3pro, g→grok4, h→r1

---

## 每月成本计算器 — 代理行为

### 触发条件

识别以下命令：`estimate my costs`、`monthly cost`、`how much am I spending`、`cost calculator`、`what does this cost`、`estimate monthly`

### 流程

1. 提出两个问题（每天收到的消息数量 + 任务类型）
2. 等待用户回答
3. 根据用户的回答和模型价格进行计算

**计算方法：**

**步骤1：估算每月的消息数量**
`messages_per_day × 30 = monthly_messages`

**步骤2：根据用户的选择划分任务类型**

| 任务类型 | 占比 |
|-----------|---------|
| 主要简单任务 | 70% |
| 主要编码任务 | 20% |
| 混合类型任务 | 40% |
| 主要复杂任务 | 15% |

**步骤3：估算每种任务类型的令牌数量**

| 任务类型 | 输入令牌 | 输出令牌 |
|-----------|-------------|--------------|
| 简单任务 | 1,500 | 500 |
| 编码任务 | 4,000 | 2,000 |
| 复杂任务 | 8,000 | 4,000 |

**步骤4：计算成本**

- **默认成本**：使用用户检测到的默认模型价格
- **优化后的成本**：根据用户选择的模型进行计算：
  - 简单任务：使用用户的默认模型价格
  - 编码任务：使用用户的工作模型价格
  - 复杂任务：使用用户的高级模型价格

**步骤5：显示比较结果**

显示默认成本和优化后的成本对比。

如果代理无法检测到用户的默认模型，会询问：“您当前使用的默认模型是什么？”

---

## 首次使用时的设置流程

### 触发条件：

- 技能首次加载后
- 用户提到成本、节省费用或设置相关内容
- 用户询问“你能做什么”或“这是什么”

无需等待特定的触发语句。如果技能已加载但用户尚未完成设置，先进行自我介绍。

### 流程：

1. 显示介绍和预设选择器（使用步骤1中的确切文本）
2. 用户选择后 → 解释将添加哪些模型（参见步骤2）
3. 使用`exec`检查身份验证：`openclaw models status` — 告诉用户点击“批准”
4. 如果缺少OpenRouter身份验证 → 指导用户完成身份验证（参见步骤3a）
5. 使用`exec`添加所选预设的所有别名（参见“预设别名命令”） — 告诉用户点击“批准”
6. 使用`exec`重启网关：`openclaw gateway restart` — 告诉用户点击“批准”
7. 指导用户进行 `/model` 测试（参见步骤4）
8. 解释成本顾问的功能以及是否开启建议

**始终一步一个步骤。** 运行一个`exec`命令，显示结果，然后继续下一步。如果`exec`失败，请先排查错误再继续。

**始终使用`exec`。** 切勿告诉用户在终端中运行命令。如果`exec`失败，请排查错误并重新尝试。

### 预设对应关系：

1 → `balanced`，2 → `code-machine`，3 → `claude-diehards`，4 → `big-context`，5 → `openai-focused`，6 → `tool-master`，7 → `ultra-budget`，8 → `free-tier`

如果用户回答含糊 → 选择`balanced`。如果用户回答“我不知道” → 选择`balanced`并说明“我们可以稍后更改”。

---

## 完整的模型注册表

OpenRouter上提供了所有29个经过验证的模型。代理需要知道这些模型，以便提供成本建议。

### 第1级 — 基础模型（适合简单任务，价格最低）

| 别名 | 模型 | OpenRouter参考链接 | 每百万输入/输出令牌价格 | 备注 |
|-------|-------|---------------|---------------------|-------|
| `flashlite` | Gemini 2.5 Flash-Lite | `openrouter/google/gemini-2.5-flash-lite` | $0.10/$0.40 | 最便宜的通用模型 |
| `flash` | Gemini 2.5 Flash | `openrouter/google/gemini-2.5-flash` | $0.15/$0.60 | 比Flash-Lite性能更强 |
| `mini` | GPT-5 Mini | `openrouter/openai/gpt-5-mini` | $0.30/$1.20 | OpenAI推荐的预算模型 |
| `gem3flash` | Gemini 3 Flash | `openrouter/google/gemini-3-flash` | $0.50/$2.00 | 最适合调用API的模型 |
| `mimo` | MiMo v2 Flash | `openrouter/xiaomi/mimo-v2-flash:free` | FREE | ⚠️ 免费等级 — 可能不稳定 |
| `devfree` | Devstral Small Free | `openrouter/mistralai/devstral-small:free` | FREE | ⚠️ 免费等级 — 可能不稳定 |
| `glm` | GLM-Z1 Free | `openrouter/thudm/glm-z1-free:free` | FREE | ⚠️ 免费等级 — 可能不稳定 |

### 第2级 — 适合编码、写作等任务的模型

| 别名 | 模型 | OpenRouter参考链接 | 每百万输入/输出令牌价格 | 备注 |
|-------|-------|---------------|---------------------|-------|
| `minimax` | MiniMax M2.1 | `openrouter/minimax/minimax-m2.1` | $0.28/$1.20 | 性价比最高的编码模型 |
| `deepseek` | DeepSeek V3 | `openrouter/deepseek/deepseek-chat-v3-0324` | $0.14/$0.28 | 最便宜的付费编码模型 |
| `devstral` | Devstral Small | `openrouter/mistralai/devstral-small` | $0.05/$0.22 | 支付费用的Devstral模型，可靠性较高 |
| `haiku` | Claude Haiku 4.5 | `openrouter/anthropic/claude-haiku-4-5` | $0.80/$4.00 | Anthropic推荐的模型 |
| `gpt51` | GPT-5.1 | `openrouter/openai/gpt-5.1` | $2.00/$8.00 | OpenAI的中端模型 |
| `grokfast` | Grok 4.1 Fast 2M | `openrouter/x-ai/grok-4.1-fast-2m` | $2.00/$10.00 | 支持2百万上下文的模型 |
| `seed` | ByteDance Seed 200K | `openrouter/bytedance/seed-coder-200k` | $0.20/$0.60 | 长上下文的编码模型 |
| `qwen3` | Qwen3 235B | `openrouter/qwen/qwen3-235b` | $0.14/$0.28 | 强大的推理模型 |

### 第3级 — 适合复杂任务、安全需求或多文件处理的模型

| 别名 | 模型 | OpenRouter参考链接 | 每百万输入/输出令牌价格 | 备注 |
|-------|-------|---------------|---------------------|-------|
| `kimi25` | Kimi K2.5 | `openrouter/moonshotai/kimi-k2.5` | $0.50/$2.00 | 最便宜的高级模型，支持1500个并行任务 |
| `sonnet` | Claude Sonnet 4.5 | `openrouter/anthropic/claude-sonnet-4-5` | $3.00/$15.00 | Anthropic推荐的模型 |
| `gpt52` | GPT-5.2 | `openrouter/openai/gpt-5.2` | $2.00/$10.00 | OpenAI的高端模型 |
| `codex52` | GPT-5.2 Codex | `openrouter/openai/gpt-5.2-codex` | $2.00/$10.00 | 专门用于代码处理的GPT-5.2模型 |
| `opus46` | Claude Opus 4.6 | `openrouter/anthropic/claude-opus-4-6` | $15.00/$75.00 | 最强大的模型 |
| `gem3pro` | Gemini 3 Pro 1M | `openrouter/google/gemini-3-pro-1m` | $1.25/$10.00 | 支持1百万上下文的模型 |
| `grok4` | Grok 4 | `openrouter/x-ai/grok-4` | $2.00/$10.00 | 强大的推理模型 |
| `r1` | DeepSeek R1 | `openrouter/deepseek/deepseek-r1` | $0.55/$2.19 | 强大的推理模型 |

### 可根据需求添加的额外模型

| 模型 | OpenRouter参考链接 | 每百万输入/输出令牌价格 | 备注 |
|-------|---------------|---------------------|-------|
| Gemma 3 27B | `openrouter/google/gemma-3-27b` | $0.10/$0.20 | 小型模型，运行速度快 |
| Llama 4 Scout | `openrouter/meta-llama/llama-4-scout` | $0.15/$0.40 | Meta推荐的模型 |
| Llama 4 Maverick | `openrouter/meta-llama/llama-4-maverick` | $0.20/$0.60 | Meta的中端模型 |
| GPT-5 | `openrouter/openai/gpt-5` | $2.00/$8.00 | OpenAI之前的旗舰模型 |
| Claude Sonnet 4 | `openrouter/anthropic/claude-sonnet-4` | $3.00/$15.00 | OpenAI之前的旗舰模型 |
| Claude Opus 4 | `openrouter/anthropic/claude-opus-4` | $15.00/$75.00 | OpenAI之前的高端模型 |
| Grok 3 Mini | `openrouter/x-ai/grok-3-mini` | $0.30/$0.50 | 经济实惠的模型 |

---

## 该技能使用的配置文件

| 文件 | 用途 |
|------|---------|
| `SKILL.md` | 本文件包含整个技能的配置 |
| `MODEL-REFERENCE.md` | 为用户提供的快速参考指南 |

**就是这样。** 没有脚本，没有自动生成的配置文件，也没有备份系统。只有代理所需的指令。**

---

## 为什么会有这个工具

我通过AI Persona方法培训了数千人来构建AI角色。用户在使用后的主要反馈是：

> “我的代理表现很好，但成本太高。即使只是问‘现在几点了？’这样的简单问题，也会使用相同的昂贵模型。”

问题并不在于模型本身，而在于某些任务本可以使用成本更低的模型来完成。`Cost Optimizer`正是我用来降低生产环境代理成本的工具，现在它也可以供您使用。

---

## 开发者简介

**Jeff J Hunter** 是AI Persona方法的创建者，也是全球首个AI认证顾问项目的创始人。

他运营着最大的AI社区（拥有360多万成员），并曾出现在《Entrepreneur》、《Forbes》、《ABC》和CBS等媒体上。作为VA Staffer（150多个虚拟助手）的创始人，Jeff花费了十年时间开发让人类和AI有效合作的系统。

`Cost Optimizer`正是这一目标的一部分 — 使AI代理变得实用且价格合理。

---

## 想通过AI赚钱吗？

大多数人使用API信用却没有任何实际收益。

`Cost Optimizer`可以帮助您节省成本。但如果您想将AI转化为实际收入，还需要掌握完整的技能。

**→ 加入AI Money Group：** https://aimoneygroup.com

学习如何构建能够自我盈利的AI系统。

---

## 联系方式

- **网站：** https://jeffjhunter.com
- **AI Persona Method：** https://aipersonamethod.com
- **AI Money Group：** https://aimoneygroup.com
- **LinkedIn：** /in/jeffjhunter

---

## 许可证

MIT许可 — 可自由使用、修改和分发。欢迎注明出处。

---

*Cost Optimizer — 停止过度支付您的代理费用。开始从中获利吧。*