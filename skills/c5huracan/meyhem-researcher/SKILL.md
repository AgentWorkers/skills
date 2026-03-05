---
name: meyhem-researcher
description: 通过多查询搜索进行深入研究，并对搜索结果进行跟踪。每次搜索都会提升所有代理未来的搜索效果。无需使用 API 密钥。
version: 0.1.6
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - curl
---
# Meyhem 深度研究工具

通过 Meyhem 在 https://api.rhdxm.com 进行多查询深度研究。您可以搜索、筛选最佳结果，然后综合这些结果并生成报告。

## 数据透明度

该工具会调用 Meyhem API（api.rhdxm.com）。发送的数据包括：您的搜索查询和代理标识符。不会发送任何个人信息、凭据或本地文件。无需 API 密钥或注册。所有数据仅用于提升所有代理的搜索排名。源代码：https://github.com/c5huracan/meyhem

## 使用方法

将研究问题拆分为 3-5 个搜索查询，然后针对每个查询执行以下操作：

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "agent_id": "openclaw-researcher", "num_results": 10}'
```

从搜索结果中挑选最佳内容并获取完整信息：

```bash
curl -s -X POST https://api.rhdxm.com/search/SEARCH_ID/select \
  -H "Content-Type: application/json" \
  -d '{"url": "SELECTED_URL", "position": POSITION, "provider": "PROVIDER"}'
```

在生成报告后，记录哪些信息对研究有帮助：

```bash
curl -s -X POST https://api.rhdxm.com/search/SEARCH_ID/outcome \
  -H "Content-Type: application/json" \
  -d '{"url": "SELECTED_URL", "success": true, "agent_id": "openclaw-researcher"}'
```

每个研究结果都会提升所有代理的搜索排名。