---
name: meyhem-search
description: Web search that learns from agent outcomes: every search, selection, and result improves rankings for all agents. Blends multiple engines. No API key.
version: 0.1.1
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Meyhem 搜索

您可以通过以下链接使用 Meyhem 在网络上进行搜索：https://api.rhdxm.com。Meyhem 联合了多个搜索引擎，对搜索结果进行去重处理，并根据以往代理的实际使用情况对结果进行排序。无需 API 密钥。

## 搜索

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "agent_id": "openclaw-agent", "max_results": 5}'
```

搜索结果将以 JSON 格式返回，其中包含 `search_id` 和 `results` 数组。每个结果包含 `url`、`title`、`snippet`、`score`、`provider` 以及其在数组中的 `position`（从 0 开始计数）。

## 选择结果

当您选择某个结果时，需要记录您的选择：

```bash
curl -s -X POST https://api.rhdxm.com/search/SEARCH_ID/select \
  -H "Content-Type: application/json" \
  -d '{"url": "SELECTED_URL", "position": POSITION, "provider": "PROVIDER"}'
```

使用您所选结果的 `position`（从 0 开始计数）和 `provider` 来获取该页面的完整内容。

## 报告搜索结果

使用某个结果后，请报告该结果是否帮助您完成了任务：

```bash
curl -s -X POST https://api.rhdxm.com/search/SEARCH_ID/outcome \
  -H "Content-Type: application/json" \
  -d '{"url": "SELECTED_URL", "success": true, "agent_id": "openclaw-agent"}'
```

如果结果帮助您完成了任务，请将 `success` 设置为 `true`；否则设置为 `false`。

## 工作流程

1. **搜索** 需要的信息。
2. **阅读** 搜索结果并挑选最佳答案。
3. **选择** 您想要使用的结果（系统会返回该页面的完整内容）。
4. **使用** 选中的内容来完成任务。
5. **报告** 该结果是否有效。

您报告的每个搜索结果都会提升所有代理的搜索排名。

## 隐私政策

该功能会将您的搜索查询和代理 ID 发送到 api.rhdxm.com。无需 API 密钥，也无需登录或提供任何个人身份信息。这些查询数据将用于提升所有代理的搜索排名。详情请参阅 [API 文档](https://api.rhdxm.com/docs)。