---
name: deep-research
description: 使用本地的 SearXNG 进行全面的网页研究。通过迭代搜索的方式获取内容，并生成包含引用信息的报告。适用于需要多个信息来源的复杂研究问题。
homepage: https://github.com/romancircus/searxng-deep-research
metadata: {"clawdbot":{"emoji":"🔬","requires":{"bins":["python3"],"python":["aiohttp","beautifulsoup4"]},"install":[{"id":"python-deps","kind":"pip","packages":["aiohttp","beautifulsoup4"],"label":"Install Python dependencies"}]}}
---

# 深度研究（Deep Research）

通过本地的 SearXNG（非 Google 提供的服务，通过 VPN 路由）进行迭代式网络搜索。

## 快速使用方法

```bash
python3 ~/.clawdbot/skills/deep-research/deep_research.py "your research question"
```

或者使用 CLI 包装器：
```bash
deep-research "what are the best practices for kubernetes security in 2026"
```

## 工作原理

1. **迭代搜索**：最多进行 5 次迭代，并逐步细化查询内容。
2. **内容抓取**：从有效的 URL 中提取完整页面内容。
3. **去重**：记录已访问过的 URL 以避免重复结果。
4. **报告生成**：生成包含引用信息的 Markdown 报告。

## 算法原理

```
for iteration in 1..5:
    query = refine_query(original_query, iteration)
    results = search_searxng(query, offset=iteration * 10)

    for result in results:
        if url not in seen_urls and domain not in ignored:
            content = fetch_and_scrape(url)
            add_to_findings(title, url, content)

    if sufficient_results:
        break

generate_markdown_report(findings, citations)
```

## 查询细化规则

每次迭代都会添加相关的上下文关键词：
- 第一次迭代：原始查询
- 第二次迭代：+ “详细分析”
- 第三次迭代：+ “全面指南”
- 第四次迭代：+ “深入研究”
- 第五次迭代：+ “研究结果”

## 配置方法

编辑 `~/.clawdbot/skills/deep-research/deep_research.py` 文件：

```python
SEARXNG_URL = "http://localhost:8888"  # Your SearXNG instance
MAX_ITERATIONS = 5                      # Search iterations
RESULTS_PER_PAGE = 10                   # Results per iteration
PAGE_CONTENT_LIMIT = 2000               # Max words per source
REQUEST_TIMEOUT = 20                    # Fetch timeout (seconds)
```

## 被排除的域名

社交媒体和低价值域名会被自动排除：
- youtube.com, facebook.com, twitter.com
- instagram.com, tiktok.com, pinterest.com, linkedin.com

您可以通过修改 `IGNORED_DOMAINS` 列表来自定义排除的域名。

## 输出格式

```markdown
# Deep Research Report

**Query:** your research question
**Date:** 2026-01-27 15:30
**Sources:** 8

---

## Research Findings

### [1] Article Title
**Source:** https://example.com/article

Content preview from the article...

### [2] Another Source
...

---

## Sources

1. [Article Title](https://example.com/article)
2. [Another Source](https://example.com/other)
```

## 隐私保护特性

- **不使用 Google/Bing**：仅使用尊重用户隐私的搜索引擎。
- **通过 VPN 路由**：所有网络流量均通过 Tailscale/Mullvad 进行传输。
- **本地处理**：所有数据处理都在本地完成。
- **无需 API 密钥**：SearXNG 为自托管服务，无外部依赖。

## 系统要求

- Python 3.8 及以上版本。
- 需要在本地运行 SearXNG 服务（端口 8888）。
- 需要安装以下 Python 包：`aiohttp`、`beautifulsoup4`。

安装相关依赖包：
```bash
pip install aiohttp beautifulsoup4
```

## 使用示例

- 研究一个技术主题：
```bash
python3 ~/.clawdbot/skills/deep-research/deep_research.py "rust async runtime comparison tokio vs async-std 2026"
```

- 调查某个概念：
```bash
python3 ~/.clawdbot/skills/deep-research/deep_research.py "zero knowledge proofs practical applications"
```

- 比较不同技术：
```bash
python3 ~/.clawdbot/skills/deep-research/deep_research.py "comparing vector databases pinecone vs milvus vs qdrant"
```

## 常见问题解决方法

**未找到结果：**
- 检查 SearXNG 是否正在运行：`curl http://localhost:8888`
- 确保查询语句不是过于具体。
- 尝试使用更宽泛的搜索词。

**搜索速度慢：**
- 降低 `MAX_ITERATIONS` 的值。
- 减少 `RESULTS_PER_PAGE` 的数量。
- 部分网站可能设置了访问限制。

**内容无法提取：**
- 可能该网站需要 JavaScript 支持（但 SearXNG 不支持）。
- 尝试直接在浏览器中访问该 URL。
- 内容可能受到付费墙的保护。