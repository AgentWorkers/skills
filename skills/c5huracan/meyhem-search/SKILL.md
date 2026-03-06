---
name: meyhem-search
description: **多引擎网络搜索**：通过代理任务完成情况对搜索结果进行排名。无需 API 密钥，也无需注册。
version: 0.1.9
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# Meyhem 搜索

这是一个专为 AI 代理设计的多引擎网络搜索工具。它能够同时查询多个搜索引擎，消除重复结果，并根据实际帮助代理完成任务的效果对结果进行排序。使用该工具的代理越多，所有代理的搜索结果就会越好。

无需 API 密钥，无需注册，也没有使用频率限制。

## 为什么选择 Meyhem？

- **多引擎，一次查询**：支持语义搜索和 AI 优化的并行查询；
- **基于结果排名的结果**：所有代理提供的成功/失败反馈会被用于结果排序；
- **完整页面内容**：选择某个结果后，可以获取整个页面的文本，而不仅仅是片段；
- 随着更多代理提交反馈，该工具会持续更新和优化。

## 快速入门

```bash
python3 search.py "transformer attention mechanism"
python3 search.py "async python best practices" -n 3
python3 search.py "react server components" --content
python3 search.py "kubernetes debugging" --agent my-agent
```

## 快速入门（REST API）

完整的 API 文档：https://api.rhdxm.com/docs

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "agent_id": "my-agent", "max_results": 5}'
```

## MCP

通过流式 HTTP 连接到 `https://api.rhdxm.com/mcp/`，可以使用以下 API 功能：`search`、`select`、`report_outcome`。

## 数据透明度

**发送的数据**：搜索查询、您选择的代理标识符以及选定的 URL；
**不发送的数据**：个人信息、凭证、本地文件或系统数据；
**存储的数据**：查询记录、选择结果以及任务完成情况，但这些数据不会与个人关联；
**用途**：仅用于优化所有代理的搜索排名，无其他用途；
**无需 API 密钥或账户**。源代码：https://github.com/c5huracan/meyhem