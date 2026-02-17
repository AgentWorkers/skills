---
name: web_search
description: Web search and URL fetching via Perplexity (default: sonar, optional: sonar-pro). Use when searching the web, looking up information, fetching URL content, or configuring web search settings. Covers web_search tool (Perplexity direct API) and web_fetch tool (HTML to markdown extraction).
---

# 网页搜索技能

该技能支持通过 Perplexity（默认模型：sonar）进行网页搜索，同时还可以获取网页内容。若需要更深入的分析，可选用 Sonar-Pro 模型。

## 认证信息

使用该技能需要您自己的 Perplexity API 密钥。系统不使用任何共享或第三方的 API 密钥。

请在您的环境变量中设置 `PERPLEXITY_API_KEY`，或在 OpenClaw 的配置文件中进行配置。

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

**高级模式（质量更高，但成本也更高）：**
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

您可以在以下链接获取 API 密钥：  
https://www.perplexity.ai/settings/api

## 数据处理

- 所有搜索请求都会发送到 Perplexity 的 API（地址：`https://api.perplexity.ai`）
- `web_fetch` 功能会本地处理获取到的网页内容（不会发送回 Perplexity）
- 该技能不会存储或保留任何数据
- 请遵守您自己的 Perplexity API 密钥使用规则及账户相关条款

## web_search

用于执行网页搜索，返回包含引用信息的 AI 合成答案。

**参数：**
- `query`（必填）——搜索查询内容
- `count`（1-10）——返回结果的数量
- `country`（2 个字母的代码）：TR、US、DE、ALL
- `search_lang`（结果语言）：tr、en、de、fr
- `freshness`（时间筛选选项）：pd（当天）、pw（本周）、pm（本月）、py（今年）

### 包含社交媒体平台的结果

对于市场调研或用户反馈查询，您可以在查询中自然地添加社交媒体平台的名称。这样 Perplexity 会同时返回来自 Reddit、Twitter、Quora 等平台的结果，无需任何过滤或限制，覆盖范围更广。

```
web_search(query="cell tower finder app complaints features users want reddit twitter quora")
```

Perplexity 会在一次搜索中同时从普通网站和社交媒体平台获取信息。

如果您仅希望从特定平台获取结果，可以使用 `site:` 操作符：
```
web_search(query="site:reddit.com best stud finder app")
```

**示例：**
```
web_search(query="latest Flutter updates", freshness="pw")
web_search(query="İstanbul hava durumu", country="TR", search_lang="tr")
web_search(query="AI news", count=5, freshness="pd")
web_search(query="GLP-1 tracker app wish features complaints reddit twitter quora")
```

## web_fetch

用于获取指定 URL 的内容，并以 Markdown 或文本格式返回。该功能不会执行 JavaScript 代码，内容会直接在本地提取。

**参数：**
- `url`（必填）——HTTP/HTTPS 网址
- `extractMode`（默认值）：markdown 或 text
- `maxChars`（可选）——内容截取长度限制

## Perplexity 模型选择（根据需求选择）

- `sonar`（默认模型）——快速问答功能 + 网页搜索，性价比高
- `sonar-pro`——多步骤推理功能 + 网页搜索（适用于需要深入分析的场景）
- `sonar-reasoning-pro`——深度思维链分析功能（成本较高，请谨慎使用）

请根据您的预算和需求，在配置文件中选择合适的模型。