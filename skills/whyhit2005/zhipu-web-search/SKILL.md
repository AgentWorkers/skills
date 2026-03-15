---
name: zhipu-web-search
description: >
  **Zhipu AI Web Search Tool** – 通过 `cURL` 直接提供灵活的搜索引擎功能。
  **适用场景：**  
  - 需要搜索网页信息以获取最新数据  
  - 需要使用特定的搜索引擎（默认为 Quark，同时支持 Sogou 和 Zhipu Search）  
  - 需要根据时间范围或域名过滤搜索结果  
  - 需要控制搜索结果的数量和详细程度  
  **支持的搜索引擎：**  
  - `search_std`（基础搜索）  
  - `search_pro`（高级搜索）  
  - `search_pro_sogou`（Sogou）  
  - `search_pro_quark`（Quark – 默认搜索引擎）
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ZHIPU_API_KEY"], "bins": ["curl"] },
      },
  }
---
# Zhipu 网页搜索

通过 Zhipu AI 的专用 API（`/paas/v4/web_search`）进行网页搜索，该 API 已重构为使用轻量级的 `cURL` 而不是 Python 或 `jq`。默认使用 `search_pro_quark` 搜索引擎，返回 20 条搜索结果。

## 快速入门

### 基本 `cURL` 使用方法

```bash
curl --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/web_search \
  --header "Authorization: Bearer $ZHIPU_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "search_query": "OpenClaw framework",
    "search_engine": "search_pro_quark",
    "search_intent": false,
    "count": 20
  }'
```

### 脚本使用方法

为方便使用，提供了一个封装好的 shell 脚本。

```bash
# Basic Search (defaults to search_pro_quark and 20 results)
bash scripts/zhipu_search.sh --query "AI development trends"

# Advanced Search
bash scripts/zhipu_search.sh \
  --query "latest open source LLMs" \
  --engine "search_pro_sogou" \
  --count 50 \
  --intent \
  --recency "oneWeek"
```

## API 参数参考

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|-------|---------|-----------|-------------------|
| `search_query` | 字符串 | 是 | - | 搜索内容，建议长度不超过 70 个字符 |
| `search_engine` | 枚举 | 是 | `search_pro_quark` | `search_std` / `search_pro` / `search_pro_sogou` / `search_pro_quark` |
| `search(intent` | 布尔值 | - | `false` | 是否启用搜索意图识别 |
| `count` | 整数 | - | `20` | 结果数量，范围 1-50 |
| `search_domain_filter` | 字符串 | - | - | 白名单域名过滤器 |
| `search_recency_filter` | 枚举 | - | `noLimit` | `oneDay` / `oneWeek` / `oneMonth` / `oneYear` / `noLimit` |
| `content_size` | 枚举 | - | `medium` | `medium`（摘要）/ `high`（详细） |

## 搜索引擎选择指南

| 引擎 | 适用场景 |
|--------|----------------------|
| `search_pro_quark` | 专为特定高级场景设计的 Quark 搜索引擎（**默认值**） |
| `search_std` | 基本搜索，适用于常规问答场景 |
| `search_pro` | 高级搜索，需要更精确的结果 |
| `search_pro_sogou` | 适用于搜索中国国内内容的 Sogou 搜索引擎 |

## 响应结构

API 直接返回 JSON 数据。

```json
{
  "id": "task-id",
  "created": 1704067200,
  "request_id": "request-id",
  "search_intent": [
    {
      "query": "original query",
      "intent": "SEARCH_ALL",
      "keywords": "rewritten keywords"
    }
  ],
  "search_result": [
    {
      "title": "title",
      "content": "content summary",
      "link": "result link",
      "media": "site name",
      "icon": "site icon",
      "refer": "reference number",
      "publish_date": "publish date"
    }
  ]
}
```

## 环境要求

- 必须配置环境变量 `ZHIPU_API_KEY`。
- 系统路径中必须包含 `curl` 命令。