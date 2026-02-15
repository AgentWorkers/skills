---
name: google-search
slug: google-search-grounding
description: >
  Google web search via Gemini Search Grounding (primary) and Custom Search JSON API (fallback).
  Use for: (1) Synthesized answers with citations (grounded search), (2) Raw link results with snippets,
  (3) Image search. Excellent Hebrew support. Preferred over built-in web_search (Perplexity).
version: 2.0.0
author: Leo 🦁
tags: [search, google, web, grounding, gemini, news, hebrew, images, citations]
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["GOOGLE_API_KEY"]},"primaryEnv":"GOOGLE_API_KEY","install":[{"id":"pip","kind":"pip","package":"google-genai","label":"Install dependencies (pip)"}]}}
allowed-tools: [exec]
---

# 谷歌搜索 🔍

谷歌网页搜索由 Gemini 2.5 Flash 提供支持，结合了 Search Grounding 和自定义搜索 API（Custom Search API）功能。

**⭐ 这是主要的网页搜索工具。建议优先使用该工具，而非内置的 `web_search`（Perplexity）。**

## 必需条件

- 需要设置 `GOOGLE_API_KEY` 环境变量。
- 需在 Google Cloud Console 中启用 Gemini API 和自定义搜索 JSON API。

## 配置参数

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `GOOGLE_API_KEY` | — | **必需**。谷歌 API 密钥 |
| `GOOGLE_CSE_CX` | — | 自定义搜索引擎 ID（用于 raw 或 image 模式） |
| `GOOGLE_SEARCH_LANG` | `he` | 默认语言代码（he, en, ar, ja 等） |
| `GOOGLE_SEARCH_COUNTRY` | `IL` | 默认国家代码（IL, US, DE 等） |

请在 OpenClaw 配置文件中设置这些参数：
```json
{
  "env": {
    "GOOGLE_API_KEY": "AIza...",
    "GOOGLE_SEARCH_LANG": "he",
    "GOOGLE_SEARCH_COUNTRY": "IL"
  }
}
```

## 脚本位置

```bash
python3 skills/google-search/lib/google_search.py <mode> "query" [options]
```

---

## 输出方式

- **文本模式**（默认）：适用于大多数场景。输出结果包含答案、来源链接和搜索查询内容，易于阅读。
- **JSON 模式**（`--json`）：适用于程序化处理。输出结果包含置信度评分、搜索查询信息等详细数据。

---

## 模式说明

### `search` — 基于 Gemini 2.5 Flash 的搜索（默认推荐模式）

使用 Gemini 2.0 Flash 和谷歌搜索功能，生成包含引用编号的合成答案。

**使用场景：** 提问、查询当前事件、“什么是 X”之类的问题，或需要直接答案的情况。

**示例：**
```bash
# Hebrew (default)
python3 lib/google_search.py search "מזג אוויר תל אביב"

# English override
python3 lib/google_search.py search "latest AI news" --lang en --country US

# JSON output
python3 lib/google_search.py search "OpenAI GPT-5 release date" --json
```

**输出格式：**
```
<Synthesized answer text>

Sources:
  1. Source Title
     https://example.com/article
  2. Another Source
     https://example.com/other
```

### `raw` — 原始搜索结果

通过自定义搜索 JSON API 获取搜索结果，包括链接、标题和内容片段。

**使用场景：** 需要获取实际链接、用于研究或构建参考列表时，或者只需要链接而非答案时。

**示例：**
```bash
python3 lib/google_search.py raw "python asyncio tutorial" -n 5
python3 lib/google_search.py raw "best restaurants tel aviv" --json
python3 lib/google_search.py raw "rust vs go performance" -n 3 --lang en
```

**输出格式：**
```
1. Page Title
   https://example.com/page
   Brief snippet from the page...

2. Another Page
   https://example.com/other
   Another snippet...
```

### `image` — 图片搜索

使用自定义搜索的图片搜索功能，返回带有标题的图片链接。

**使用场景：** 查找图片、获取视觉资料或缩略图时。

**示例：**
```bash
python3 lib/google_search.py image "query" [-n 5] [--lang he] [--country IL] [--json]
```

## 选项说明

| 选项 | 适用范围 | 说明 | 默认值 |
|---|---|---|---|
| `--lang CODE` | 所有模式 | 语言代码（he, en, ar, ja 等） | 由环境变量 `GOOGLE_SEARCH_LANG` 决定 |
| `--country CODE` | 所有模式 | 国家代码（IL, US, DE 等） | 由环境变量 `GOOGLE_SEARCH_COUNTRY` 决定 |
| `-n NUM` | raw, image | 结果数量（1–10） | 默认为 10 |
| `--json` | 所有模式 | 结构化 JSON 格式输出 | 默认关闭 |

**语言/国家优先级：** `--lang` 选项 → `GOOGLE_SEARCH_LANG` 环境变量 → 无该选项时自动使用默认值 |
**国家优先级：** `--country` 选项 → `GOOGLE_SEARCH_COUNTRY` 环境变量 → 无该选项时自动使用默认值 |

---

## 错误处理

- **API 密钥缺失**：会显示带有设置说明的错误信息。
- **429 错误（请求频率限制）**：等待 5 秒后自动重试一次。
- **网络错误**：会显示详细的错误原因。
- **未找到结果**：显示“未找到结果”的提示信息。
- **超时**：所有 HTTP 请求的默认超时时间为 30 秒。

---

## 配额与请求限制

| API | 免费 tier | 请求限制 |
|---|---|---|
| Gemini API（基于 Gemini 2.5 Flash 的搜索） | 免费 tier 提供较多请求次数 | 免费用户约 15 次/分钟；付费用户限制更高 |
| 自定义搜索 JSON API（raw/image 模式） | 每天 100 次请求 | 每天 10,000 次请求（付费用户） |

**处理 429 错误**：脚本会自动重试一次。如果请求次数达到限制，将切换回内置的 `web_search`（Perplexity）功能。

---

## 多语言支持

支持多种语言的搜索请求。默认使用希伯来语（Hebrew）。

```bash
# Hebrew (default, no flags needed)
python3 lib/google_search.py search "חדשות טכנולוגיה"

# English
python3 lib/google_search.py search "technology news" --lang en

# Arabic
python3 lib/google_search.py search "أخبار التكنولوجيا" --lang ar
```

---

## 安装说明

```bash
bash skills/google-search/install.sh
```