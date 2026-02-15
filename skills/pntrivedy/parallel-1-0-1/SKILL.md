---
name: parallel
description: 通过 Parallel.ai API 进行高精度的网络搜索和研究。该服务专为 AI 代理优化，提供丰富的摘录和引用信息。
triggers:
  - parallel
  - deep search
  - research
metadata:
  clawdbot:
    emoji: "🔬"
---

# Parallel.ai 🔬

专为AI代理设计的高精度网络搜索API。在研究基准测试中，其性能优于Perplexity/Exa。

## 设置

```bash
pip install parallel-web
```

API密钥已配置。支持使用Python SDK进行开发。

```python
from parallel import Parallel
client = Parallel(api_key="YOUR_KEY")
response = client.beta.search(
    mode="one-shot",
    max_results=10,
    objective="your query"
)
```

## 快速使用方法

```bash
# Search with Python SDK
python3 {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5

# JSON output
python3 {baseDir}/scripts/search.py "latest AI news" --json
```

## 响应格式

返回结构化的搜索结果，包含以下内容：
- `search_id`：唯一的搜索标识符
- `results[]`：结果数组，包含：
  - `url`：源网址
  - `title`：页面标题
  - `excerpts[]`：相关文本摘录
  - `publish_date`：（如有的话）发布日期
  - `usage`：API使用统计信息

## 适用场景

- **深度研究**：需要跨引用事实的场景
- **公司/人物研究**：包含引用的研究
- **事实核查**：提供基于证据的核查结果
- **复杂查询**：需要多步骤推理的查询
- 对于研究任务而言，其搜索精度高于传统搜索引擎

## API参考文档

文档链接：https://docs.parallel.ai
平台官网：https://platform.parallel.ai