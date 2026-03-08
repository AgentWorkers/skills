---
name: perplexity-research
version: 2.0.0
description: 使用 Perplexity Agent API 进行深入研究，该 API 支持网络搜索、推理以及多模型分析功能。当用户需要获取当前信息、市场研究数据、趋势分析结果、投资建议，或对任何需要网络搜索和推理能力的主题进行综合研究时，可以使用该工具。
---
# 混乱度研究（Perplexity Research）

该研究助手由 Perplexity Agent API 提供支持，具备网页搜索和推理功能。

## 快速入门

Perplexity 客户端位于该技能文件夹中的 `scripts/perplexity_client.py` 文件中。

**默认模型**：`openai/gpt-5.2`（GPT 的最新版本）

**核心功能**：
- 进行网页搜索以获取当前信息
- 进行深度分析，需要较高的推理能力
- 支持多模型比较
- 提供流式响应
- 支持成本跟踪

## 常见研究模式

### 1. 深度研究查询（Deep Research Query）

适用于需要结合网页搜索和推理的综合性分析：

```python
# Import from skill scripts folder
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from perplexity_client import PerplexityClient

client = PerplexityClient()
result = client.research_query(
    query="Your research question here",
    model="openai/gpt-5.2",
    reasoning_effort="high",
    max_tokens=2000
)

if "error" not in result:
    print(result["answer"])
    print(f"Tokens: {result['tokens']}, Cost: ${result['cost']}")
```

### 2. 快速网页搜索（Quick Web Search）

适用于获取时效性强或最新的信息：

```python
result = client.search_query(
    query="Your question about current events",
    model="openai/gpt-5.2",
    max_tokens=1000
)
```

### 3. 模型比较（Model Comparison）

在输出质量至关重要的情况下使用：

```python
results = client.compare_models(
    query="Your question",
    models=["openai/gpt-5.2", "anthropic/claude-3-5-sonnet", "google/gemini-2.0-flash"],
    max_tokens=300
)

for result in results:
    if "error" not in result:
        print(f"\n{result['model']}: {result['answer']}")
```

### 4. 流式响应（Streaming Response）

适用于需要长时间分析的场景，以提升用户体验：

```python
client.stream_query(
    query="Your question",
    model="openai/gpt-5.2",
    use_search=True,
    max_tokens=2000
)
```

## 研究工作流程

进行研究时，请按照以下步骤操作：
1. **初步探索**：使用 `research_query()` 并启用网页搜索功能。
2. **验证结果**：使用 `compare_models()` 将不同模型的分析结果进行比较。
3. **深入分析**：使用流式响应对特定方面进行详细分析。
4. **关注成本**：监控结果中的令牌使用量和费用。

## 模型选择

**默认模型**：`openai/gpt-5.2`（最新的 GPT 模型）

其他可选模型：
- `anthropic/claude-3-5-sonnet` - 推理能力强，性能均衡。
- `google/gemini-2.0-flash` - 响应速度快，成本效益高。
- `meta/llama-3.3-70b` - 开源替代方案。

根据以下需求选择模型：
- 如果需要最佳结果，选择 `gpt-5.2`。
- 如果需要快速响应，选择 `gemini-2.0-flash`。
- 如果有成本限制，可以比较不同模型的费用。

## 推理难度级别（Reasoning Effort Levels）

通过 `reasoning_effort` 参数控制分析的深度：
- `"low"`：快速响应，推理最少。
- `"medium"`：推理能力适中（大多数查询的默认设置）。
- `"high"`：深度分析，适用于需要全面研究的场景。

## 环境配置

确保 `PERPLEXITY_API_KEY` 已正确设置：

```bash
export PERPLEXITY_API_KEY='your_api_key_here'
```

或者在该技能的 `scripts/` 目录下创建一个 `.env` 文件来配置 API 密钥：

```
PERPLEXITY_API_KEY=your_api_key_here
```

## 错误处理

所有方法都会返回错误信息：

```python
result = client.research_query("Your question")

if "error" in result:
    print(f"Error: {result['error']}")
    # Handle error appropriately
else:
    # Process successful result
    print(result["answer"])
```

## 成本优化策略：
- 使用 `max_tokens` 参数限制响应长度。
- 对于简单问题，优先使用 `search_query()` 而非 `research_query()`。
- 通过 `result["cost"]` 字段监控研究成本。

## 集成示例：

### 投资研究（Investment Research）

```python
client = PerplexityClient()

# Market analysis
result = client.research_query(
    query="Analyze recent developments in AI chip market and key competitors",
    reasoning_effort="high"
)

# Company deep dive
result = client.search_query(
    query="Latest earnings report for NVIDIA Q4 2025"
)

# Multi-model validation
results = client.compare_models(
    query="What are the biggest risks in the semiconductor industry?",
    models=["openai/gpt-5.2", "anthropic/claude-3-5-sonnet"]
)
```

### 趋势分析（Trend Analysis）

```python
# Current trends with web search
result = client.research_query(
    query="Emerging trends in sustainable investing and ESG adoption rates",
    reasoning_effort="high",
    max_tokens=2000
)

# Stream for real-time updates
client.stream_query(
    query="Latest developments in quantum computing commercialization",
    use_search=True
)
```

### 多轮研究（Multi-Turn Research）

```python
# Build context across multiple queries
messages = [
    {"role": "user", "content": "What is the current state of fusion energy?"},
    {"role": "assistant", "content": "...previous response..."},
    {"role": "user", "content": "Which companies are leading in this space?"}
]

result = client.conversation(
    messages=messages,
    use_search=True
)
```

## 最佳实践：
1. 对于大多数研究任务，优先使用 `research_query()`——它结合了网页搜索和高级推理功能。
2. 在面向用户的应用程序中，使用流式响应来展示研究进度。
3. 在关键决策或对质量要求较高的场景下，比较不同模型的分析结果。
4. 为摘要设置合理的 `max_tokens` 值（例如 1000 个令牌），为深度分析设置更多令牌（例如 2000 个以上）。
5. 通过 `result["cost"]` 和 `result["tokens"]` 监控研究成本。
6. 优雅地处理错误——始终检查结果中的 “error” 键以获取错误信息。

## API 参考文档

请参阅 [reference.md](reference.md) 以获取完整的 API 文档。此外，`scripts/perplexity_client.py` 文件中包含：
- 完整的方法签名。
- 额外参数。
- CLI 使用示例。
- 实现细节。

## 命令行用法

从技能目录中运行相关命令：

```bash
# Research mode
python scripts/perplexity_client.py research "Your question"

# Web search
python scripts/perplexity_client.py search "Your question"

# Streaming
python scripts/perplexity_client.py stream "Your question"

# Compare models
python scripts/perplexity_client.py compare "Your question"
```