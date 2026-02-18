---
name: web_search
description: Web search and URL fetching via Perplexity (default: sonar, optional: sonar-pro). Use when searching the web, looking up information, fetching URL content, or configuring web search settings. Covers web_search tool (Perplexity direct API) and web_fetch tool (HTML to markdown extraction).
homepage: https://github.com/aligurelli/clawd/tree/main/skills/web_search
metadata: {"clawdbot":{"emoji":"🔎"}}
---

# 网络搜索技能

该技能通过 Perplexity（默认模型：sonar）进行网络搜索，并获取网页内容。如需更深入的分析，可选用 `sonar-pro` 模型。

## 凭据

该技能使用您在 OpenClaw 中配置的 Perplexity 密钥，不使用任何共享或第三方密钥。

如果您的环境尚未配置，请设置 `PERPLEXITY_API_KEY`，或在 OpenClaw 配置文件中配置该密钥。

**推荐默认设置（性价比高）：**
```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "<your-perplexity-api-key>",
          baseUrl: "https://api.perplexity.ai",
          model: "sonar"
        }
      }
    }
  }
}
```

**可选的深度搜索模式（质量更高，但成本也更高）：**
```json5
{
  tools: {
    web: {
      search: {
        perplexity: {
          model: "sonar-pro"
        }
      }
    }
  }
}
```

仅在确实需要更深入分析时使用 `sonar-pro` 模型。

您可以在以下链接获取 API 密钥：https://www.perplexity.ai/settings/api

## 数据处理

- 所有搜索请求都会发送到 Perplexity 的 API（`https://api.perplexity.ai`）
- `web-fetch` 用于获取网页内容，这些内容会在 OpenClaw 中被本地处理（不会发送到 Perplexity）
- 该技能本身不会持久化数据；查询的处理和保留遵循 OpenClaw 与 Perplexity 的相关规则
- 请勿在搜索请求中包含任何敏感信息或私人数据
- 您需要使用自己的 Perplexity API 密钥，并遵守其使用条款

## web_search

执行网络搜索，返回带有引用信息的 AI 合成答案。

参数：
- `query`（必填）— 搜索查询
- `count`（1-10）— 结果数量
- `country`— 两位字母的国家代码：TR、US、DE、ALL
- `search_lang`— 结果语言：tr、en、de、fr
- `freshness`— 时间筛选条件：pd（天）、pw（周）、pm（月）、py（年）

### 包含社交媒体平台的结果

对于市场研究或用户反馈查询，可以在查询中自然地添加社交媒体平台的名称。这样 Perplexity 会同时返回来自 Reddit、Twitter、Quora 等平台的结果——无需任何过滤或限制，覆盖范围更广。

```
web_search(query="cell tower finder app complaints features users want reddit twitter quora")
```

Perplexity 会在一次搜索中同时从普通网站和社交媒体平台获取结果。

如果您仅希望从特定平台获取结果，可以使用 `site:` 操作符：
```
web_search(query="site:reddit.com best stud finder app")
```

示例：
```
web_search(query="latest Flutter updates", freshness="pw")
web_search(query="İstanbul hava durumu", country="TR", search_lang="tr")
web_search(query="AI news", count=5, freshness="pd")
web_search(query="GLP-1 tracker app wish features complaints reddit twitter quora")
```

## web_fetch

以 Markdown 或文本格式获取网页内容。不会执行 JavaScript 代码。内容会在本地被提取。

参数：
- `url`（必填）— HTTP/HTTPS 网址
- `extractMode`— markdown（默认）或 text
- `maxChars`— 内容截取长度限制

## Perplexity 模型（用户可选）

- `sonar`（默认）— 快速问答 + 网络搜索，性价比高
- `sonar-pro`— 多步骤推理 + 网络搜索（适用于需要深入分析的情况）
- `sonar-reasoning-pro`— 深度思维链分析（成本较高，请谨慎使用）

根据您的预算和需求，在配置文件中选择合适的模型。