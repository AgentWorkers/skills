---
name: parallel
version: "1.1.0"
description: 通过 Parallel.ai API 进行高精度的网络搜索和研究。该服务专为 AI 代理优化，能够提供丰富的摘录和引用信息，并支持代理模式（agent mode），以实现高效的多步骤推理（token-efficient multi-step reasoning）。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-parallel
homepage: https://parallel.ai
triggers:
  - parallel
  - deep search
  - research
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      env:
        - PARALLEL_API_KEY
    primaryEnv: PARALLEL_API_KEY
    tags:
      - search
      - research
      - web
      - parallel
      - citations
---
# Parallel.ai 🔬

这是一个专为人工智能代理设计的高精度网络搜索API，在研究基准测试中的表现优于Perplexity/Exa。

## 设置

```bash
pip install parallel-web
```

API密钥已配置。支持使用Python SDK进行开发。

```python
from parallel import Parallel
client = Parallel(api_key="YOUR_KEY")
response = client.beta.search(
    mode="one-shot",  # or "fast" for lower latency/cost, "agentic" for multi-hop
    max_results=10,
    objective="your query"
)
```

## 模式

| 模式 | 使用场景 | 权衡点 |
|------|----------|----------|
| `one-shot` | 默认模式，平衡准确性和速度 | 适用于大多数查询 |
| `fast` ⚡ | 快速查找，注重成本效率 | 延迟和成本较低，但可能牺牲部分准确性 |
| `agentic` | 复杂的多步骤查询 | 更高的准确性，但使用成本更高 |

## 快速使用方法

```bash
# Default search (one-shot mode)
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5

# Fast mode - lower latency/cost ⚡
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --mode fast

# Agentic mode - complex research
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "compare transformer architectures" --mode agentic

# JSON output
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --json
```

## 响应格式

返回结构化结果，包括：
- `search_id` - 唯一的搜索标识符
- `results[]` - 结果数组，包含：
  - `url` - 网页链接
  - `title` - 页面标题
  - `excerpts[]` - 相关文本摘录
  - `publish_date` - 文章发布日期（如有的话）
- `usage` - API使用统计信息

## 适用场景

- **深度研究**：需要跨引用的事实验证
- **公司/人物研究**：包含引用信息
- **事实核查**：提供基于证据的输出
- **复杂查询**：需要多步骤推理的查询
- 对于研究任务而言，其准确性优于传统搜索引擎

## API参考文档

文档：https://docs.parallel.ai
平台：https://platform.parallel.ai