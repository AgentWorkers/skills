---
name: meyhem-researcher
description: Deep research agent: multi-query web search with outcome tracking across multiple engines. Synthesize reports from full page content. No API key.
version: 0.1.9
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Meyhem 深度研究者（Meyhem Deep Researcher）

Meyhem 深度研究者是一款基于多引擎搜索技术的多查询深度研究工具。它能够将复杂的问题分解为多个具体的查询，检索完整网页内容，整合搜索结果，并生成详细的报告。所有这些操作都有助于提升后续搜索的效率。

**无需 API 密钥**、**无需注册**，也**没有使用限制**。

## 为什么选择 Meyhem 深度研究者？

- **高效的研究流程**：将问题拆分为多个查询，进行搜索、筛选和结果整合。
- **获取完整网页内容**：不仅提供片段，还能获取每个来源的完整文本。
- **并行搜索多个引擎**：结合语义分析技术和 AI 优化后的搜索结果。
- **结果排名机制**：每次生成的报告都会为所有用户带来更好的搜索体验。

## 快速入门

```bash
python3 researcher.py "transformer attention mechanism"
python3 researcher.py "kubernetes networking" -n 3 -q 5
```

## 快速入门（REST API）

完整的 API 文档：https://api.rhdxm.com/docs

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "agent_id": "my-researcher", "max_results": 10}'
```

## MCP（Multi-Channel Platform）

通过 `https://api.rhdxm.com/mcp/` 使用 Streamable HTTP 协议进行连接，支持以下操作：`search`（搜索）、`select`（筛选）、`report_outcome`（生成报告）。

## 数据透明度

**发送的数据**：搜索查询、用户标识符以及用户选择的 URL。
**不发送的数据**：个人信息、凭证、本地文件或系统数据。
**数据存储方式**：查询记录、筛选结果和最终报告会被存储在统一的数据库中，且不会与个人身份关联。
**数据用途**：仅用于提升所有用户的搜索体验，无其他用途。
**无需 API 密钥或账户**。源代码：https://github.com/c5huracan/meyhem