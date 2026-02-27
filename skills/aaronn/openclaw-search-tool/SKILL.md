---
name: research-tool
description: 通过 OpenRouter 使用大型语言模型（LLMs）来搜索网页。可以用于获取当前网页数据、API 文档、市场研究、新闻、事实核查，或任何需要实时互联网访问和推理的问题。
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": ["research-tool"], "env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://github.com/aaronn/openclaw-search-tool"}}
---
# OpenClaw研究工具

通过OpenRouter支持的网络搜索功能，您可以查询OpenClaw代理。使用自然语言提出问题，即可获得带有引用来源的准确答案。默认使用GPT-5.2模型，该模型在文档查询和需要大量引用的研究任务中表现出色。

> **注意：** 即使是简单的查询也可能需要**1分钟或更长时间**来完成。复杂的查询可能需要**10分钟以上**。这是正常的——模型需要在网上搜索信息、阅读网页并合成答案。

> **建议：** 在**子代理**中运行研究工具，以确保您的主会话保持响应状态：
> ```
> sessions_spawn task:"research-tool 'your query here'"
> ```

> **⚠️ 在运行研究工具时** **切勿设置超时**。查询通常需要1到10分钟以上的时间。您可以使用`yieldMs`将其置于后台执行，然后定期检查进度——但**切勿设置超时**，否则查询过程可能会在搜索过程中被中断。

`:online`模型后缀表示该模型具有**实时网络访问能力**——它可以在线搜索、读取网页、引用URL并合成答案。

## 安装

```bash
cargo install openclaw-search-tool
```

需要`OPENROUTER_API_KEY`环境变量。请在https://openrouter.ai/keys获取API密钥。

## 快速入门

```bash
research-tool "What are the x.com API rate limits?"
research-tool "How do I set reasoning effort parameters on OpenRouter?"
```

### 从OpenClaw代理开始使用

```python
# Best: run in a sub-agent (main session stays responsive)
sessions_spawn task:"research-tool 'your query here'"

# Or via exec — NEVER set timeout, use yieldMs to background:
exec command:"research-tool 'your query'" yieldMs:5000
# then poll the session until complete
```

## 参数说明

### `--effort`, `-e`（默认值：`low`）

控制模型在回答问题前进行推理的深度。设置得越高，分析越详细，但响应速度越慢，消耗的模型令牌数也越多。

```bash
research-tool --effort low "What year was Rust 1.0 released?"
research-tool --effort medium "Explain how OpenRouter routes requests to different model providers"
research-tool --effort high "Compare tradeoffs between Opus 4.6 and gpt-5.3-codex for programming"
research-tool --effort xhigh "Deep analysis of React Server Components vs traditional SSR approaches"
```

| 级别 | 响应速度 | 适用场景 |
|-------|-------|-------------|
| `low` | 约1-3分钟 | 快速查找事实、简单问题 |
| `medium` | 约2-5分钟 | 标准研究、中等复杂度分析 |
| `high` | 约3-10分钟 | 深度分析、需要仔细推理的问题 |
| `xhigh` | 约5-20分钟以上 | 最高级别的推理、涉及多个信息源的综合分析 |

也可以通过环境变量`RESEARCH_EFFORT`来设置该参数。

### `--model`, `-m`（默认值：`openai/gpt-5.2:online`）

指定使用的模型。默认使用带有`:online`后缀的GPT-5.2模型，因为该模型在需要引用和准确文档查询的场景中表现优异。`:online`后缀使模型能够进行实时网络搜索，并适用于OpenRouter上的**任何模型**。

```bash
# Default: GPT-5.2 with web search (great for docs and cited answers)
research-tool "current weather in San Francisco"

# Claude with web search
research-tool -m "anthropic/claude-sonnet-4-20250514:online" "Summarize recent changes to the OpenAI API"

# GPT-5.2 without web search (training data only)
research-tool -m "openai/gpt-5.2" "Explain the React Server Components architecture"

# Any OpenRouter model
research-tool -m "google/gemini-2.5-pro:online" "Compare React vs Svelte in 2026"
```

也可以通过环境变量`RESEARCH_MODEL`来设置该参数。

### `--system`, `-s`

覆盖系统的提示语，为模型指定特定的角色或指令。

```bash
research-tool -s "You are a senior infrastructure engineer" "Best practices for zero-downtime Kubernetes deployments"
research-tool -s "You are a Rust systems programmer" "Best async patterns for WebSocket servers"
```

### `--stdin`

从标准输入（stdin）读取查询内容。适用于长查询或多行查询。

```bash
echo "Explain the OpenRouter model routing architecture" | research-tool --stdin
cat detailed-prompt.txt | research-tool --stdin
```

### `--max-tokens`（默认值：`12800`）

响应中的最大令牌数。

### `--timeout`（可选，无默认值）

默认情况下没有超时限制——查询会一直运行直到模型完成。只有在需要设定时间上限时才需要设置此参数（例如：`--timeout 300`）。

## 输出格式

- **stdout**：仅包含响应文本（带有引用的Markdown格式）——适合通过管道传输
- **stderr**：显示进度状态、推理过程和令牌使用情况

```
🔍 Researching with openai/gpt-5.2:online (effort: high)...
✅ Connected — waiting for response...

[response text on stdout]

📊 Tokens: 4470 prompt + 184 completion = 4654 total | ⏱ 5s
```

## 状态指示器

- `🔍 正在搜索中...` — 请求已发送至OpenRouter
- `✅ 已连接 — 正在等待响应...` — 服务器已接收请求，模型正在搜索/处理
- `⏳ 15秒... ⏳ 30秒...` — 进度时间（仅显示在交互式终端中，代理执行时不显示）
- `❌ 无法连接到OpenRouter` — 网络问题导致连接失败
- `❌ 连接中断` — 在等待响应时连接丢失。是否需要重试？

## 提高查询效果的小贴士

- **使用自然语言提问。** 例如：“Rust错误处理的最佳实践是什么？在什么情况下应该使用`anyhow`而不是`thiserror`？”这样的提问方式效果更好。
- **提供尽可能多的背景信息。** 模型从零开始理解问题，因此请提供相关背景信息、您已掌握的知识以及所有相关的子问题。详细的提示会显著提高查询效果。
- **合理选择难度级别。** 对于快速查询使用`low`级别，对于深入研究使用`high`级别，对于复杂的多源分析使用`xhigh`级别。
- **使用`-s`参数指定领域专业知识。** 为模型指定特定的领域角色，可以获得更专业的回答。

## 成本

每次查询的费用约为0.01–0.05美元。每次查询后，模型消耗的令牌数会显示在`stderr`中。