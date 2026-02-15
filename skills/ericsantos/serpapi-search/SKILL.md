---
name: serpapi
description: 通过 SerpAPI 搜索 Google（包括 Google 搜索、Google 新闻和 Google 本地服务）。当您需要在网上搜索、查找新闻文章或查询本地企业信息时，可以使用该工具。它支持根据国家/语言设置来获取特定地区的搜索结果。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["curl","python3"],"env":["SERPAPI_API_KEY"]},"primaryEnv":"SERPAPI_API_KEY"}}
---

# SerpAPI 搜索

通过 SerpAPI 进行谷歌搜索，并可指定目标国家/语言。

## 快速入门

```bash
# Google Search
{baseDir}/scripts/search.sh "artificial intelligence B2B" --country br --lang pt

# Google News
{baseDir}/scripts/search.sh "inteligência artificial" --engine google_news --country br --lang pt

# Google Local
{baseDir}/scripts/search.sh "AI companies" --engine google_local --country us --location "San Francisco, California"
```

## 可用的搜索引擎

| 搜索引擎 | 适用场景 | 关键结果字段 |
|--------|----------|-------------------|
| `google` | 网页搜索（默认） | `organic_results` |
| `google_news` | 新闻文章 | `news_results` |
| `google_local` | 当地企业/地点 | `local_results` |

## 参数选项

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--engine` | `google`, `google_news`, `google_local` | `google` |
| `--country` | 两位字母的国家代码（如 `br`, `us`, `de` 等） | `us` |
| `--lang` | 语言代码（如 `pt`, `en`, `es` 等） | `en` |
| `--location` | 地点字符串（例如：“São Paulo, Brazil”） | — |
| `--num` | 结果数量 | `10` |
| `--json` | 原始 JSON 格式输出 | `off` |

## API 密钥

请设置 `SERPAPI_API_KEY` 环境变量，或将其存储在合适的位置：

```bash
mkdir -p ~/.config/serpapi
echo "your_key_here" > ~/.config/serpapi/api_key
chmod 600 ~/.config/serpapi/api_key
```

## 常见的国家代码

`br`（巴西），`us`（美国），`pt`（葡萄牙），`de`（德国），`fr`（法国），`es`（西班牙），`gb`（英国），`jp`（日本），`in`（印度）。