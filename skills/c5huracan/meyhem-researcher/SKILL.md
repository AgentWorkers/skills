---
name: meyhem-researcher
description: Deep research agent with outcome-driven ranking: results get smarter the more agents use it. Multi-angle search, cited reports. No API key.
version: 0.1.1
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Meyhem 深度研究助手

这是一个由 Meyhem 搜索引擎驱动的多步骤研究辅助工具，可通过以下地址访问：https://api.rhdxm.com。用户只需提出一个研究问题，该工具便会将其分解为多个针对性的搜索查询，分别执行这些查询，挑选出最相关的结果，阅读其内容，并生成一份包含引用来源的完整研究报告。使用该工具无需任何 API 密钥。

## 第一步：问题分解

将用户的研究问题拆分为 3-5 个聚焦于不同方面的搜索查询。

## 第二步：执行搜索

针对每个查询，在 Meyhem 中进行搜索：

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "agent_id": "openclaw-researcher", "num_results": 10}'
```

搜索结果将以 JSON 格式返回，其中包含 `search_id` 和 `results` 数组。每个搜索结果包含 `url`、`title`、`snippet`、`score`、`provider` 和 `position` 等字段。

## 第三步：结果筛选

从所有查询中挑选出 6-10 个最相关的结果，并获取每个结果的具体内容：

```bash
curl -s -X POST https://api.rhdxm.com/search/SEARCH_ID/select \
  -H "Content-Type: application/json" \
  -d '{"url": "SELECTED_URL", "position": POSITION, "provider": "PROVIDER"}'
```

系统会返回所选结果的全页面内容。

## 第四步：撰写报告

利用筛选出的结果内容，撰写一份全面的研究报告：
- 彻底回答原始研究问题；
- 以 [1]、[2] 等格式标注引用来源；
- 包含一个“来源”部分，列出所有引用内容的标题和网址；
- 突出关键发现以及存在共识或分歧的领域。

## 第五步：评估结果

对于每个筛选出的结果，判断其是否对报告的撰写有帮助：

```bash
curl -s -X POST https://api.rhdxm.com/search/SEARCH_ID/outcome \
  -H "Content-Type: application/json" \
  -d '{"url": "SELECTED_URL", "success": true, "agent_id": "openclaw-researcher"}'
```

如果某个结果对报告的撰写有实际帮助，则将 `success` 参数设置为 `true`；否则设置为 `false`。

## 工作流程总结

1. 将研究问题分解为 3-5 个搜索查询；
2. 对每个查询在 Meyhem 中进行搜索（每个查询返回 10 个结果）；
3. 从所有查询中挑选出 6-10 个最相关的结果，并获取它们的具体内容；
4. 根据这些内容撰写一份包含引用来源的研究报告；
5. 评估每个筛选出的结果是否对报告的完成起到了积极作用。

每次搜索、结果筛选和报告生成的过程都会提升 Meyhem 搜索引擎在所有辅助工具中的排名。

## 隐私政策

使用该工具时，系统会向 api.rhdxm.com 发送用户的搜索查询信息及辅助工具的 ID。无需提供 API 密钥或登录信息，也不会收集任何个人身份信息。所有查询数据仅用于提升所有辅助工具的搜索排名。详情请参阅 [API 文档](https://api.rhdxm.com/docs)。