---
name: google-search
slug: google-search-grounding
description: >
  通过 Gemini Search Grounding（主要方式）和 Custom Search JSON API（备用方式）进行谷歌网络搜索。支持的功能包括：  
  (1) 带有引用信息的合成答案（基于实情搜索）；  
  (2) 带有摘要的原始链接结果；  
  (3) 图片搜索。  
  该工具对希伯来语的支持非常出色。相比内置的 web_search（Perplexity）功能，更受推荐。
version: 2.1.0
author: Leo 🦁
tags: [search, google, web, grounding, gemini, news, hebrew, images, citations]
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["GOOGLE_API_KEY"]},"primaryEnv":"GOOGLE_API_KEY","secondaryEnv":["GOOGLE_CSE_CX","GOOGLE_SEARCH_LANG","GOOGLE_SEARCH_COUNTRY"],"install":[{"id":"pip","kind":"pip","package":"google-genai","label":"Install google-genai library"}],"notes":"GOOGLE_CSE_CX is required only for raw/image modes (Custom Search API). The default search mode (Gemini grounding) needs only GOOGLE_API_KEY. No hardcoded CSE IDs — users must supply their own."}}
allowed-tools: [exec]
---
# 谷歌搜索 🔍

谷歌网页搜索功能由 Gemini 2.5 Flash 提供支持，结合了 Search Grounding 和自定义搜索 API（Custom Search API）。

**⭐ 这是主要的网页搜索工具。建议优先使用该工具，而非内置的 `web_search`（Perplexity）。**

## 需求

- 需要设置 `GOOGLE_API_KEY` 环境变量。
- 需要在 Google Cloud Console 中启用 Gemini API 和自定义搜索 JSON API。

## 配置

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `GOOGLE_API_KEY` | — | **必需**。Google API 密钥 |
| `GOOGLE_CSE_CX` | — | 自定义搜索引擎 ID（用于 raw 或 image 模式） |
| `GOOGLE_SEARCH_LANG` | `he` | 默认语言代码（he, en, ar, ja 等） |
| `GOOGLE_SEARCH_COUNTRY` | `IL` | 默认国家代码（IL, US, DE 等） |

请在 OpenClaw 配置文件中设置这些变量：
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

## 输出模式

- **文本模式**（默认）：适用于大多数场景。输出结果包含答案、来源链接和搜索查询内容，易于阅读。
- **JSON 模式**（`--json`）：适用于程序化处理。输出结果包含置信度评分、搜索支持信息以及搜索查询内容。

---

## 模式

### `search` — 基于 Gemini 2.0 Flash 的搜索（默认推荐模式）

使用 Gemini 2.0 Flash 和谷歌搜索功能，生成带有编号引用信息的综合答案。

```bash
python3 lib/google_search.py search "query" [--lang he] [--country IL] [--json]
```

**使用场景：** 提问、查询当前事件、询问“X 是什么”、使用希伯来语进行搜索等，任何需要直接答案的情况。

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

---

### `raw` — 原始搜索结果

通过自定义搜索 JSON API 获取搜索结果，输出包含链接、标题和内容片段。

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

---

### `image` — 图片搜索

使用自定义搜索的图片搜索功能，获取带有标题的图片链接。

**使用场景：** 查找图片、获取视觉参考资料或缩略图时。

**示例：**
```bash
python3 lib/google_search.py image "query" [-n 5] [--lang he] [--country IL] [--json]
```

---

## 选项参考

| 选项 | 适用范围 | 说明 | 默认值 |
|---|---|---|---|
| `--lang CODE` | 所有模式 | 语言代码（he, en, ar, ja 等） | 由环境变量 `GOOGLE_SEARCH_LANG` 决定 |
| `--country CODE` | 所有模式 | 国家代码（IL, US, DE 等） | 由环境变量 `GOOGLE_SEARCH_COUNTRY` 决定 |
| `-n NUM` | raw, image | 结果数量（1–10） | 10 |
| `--json` | 所有模式 | 结构化 JSON 输出 | 否 |

**语言优先级：** `--lang` 选项 → 环境变量 `GOOGLE_SEARCH_LANG` → 无（自动选择）  
**国家优先级：** `--country` 选项 → 环境变量 `GOOGLE_SEARCH_COUNTRY` → 无（自动选择）  

---

## 错误处理

- **API 密钥缺失**：会显示清晰的错误信息并附带设置指南。
- **429 错误（请求频率限制）**：等待 5 秒后自动重试一次。
- **网络错误**：会显示包含原因的详细错误信息。
- **未找到结果**：会显示“未找到结果”的提示信息。
- **超时**：所有 HTTP 请求的默认超时时间为 30 秒。

---

## 配额与请求限制

| API | 免费 tier | 请求限制 |
|---|---|---|
| Gemini API（基于 Gemini 2.0 Flash 的搜索） | 免费 tier 提供大量请求量 | 免费用户约 15 次/分钟；付费用户限制更高 |
| 自定义搜索 JSON API（raw/image 模式） | 每天 100 次请求 | 每天 10,000 次请求（付费用户） |

**遇到 429 错误时**：脚本会自动重试一次。如果配额用尽，将切换到内置的 `web_search`（Perplexity）功能。

---

## 多语言支持**

支持使用任何语言进行搜索。默认使用希伯来语。

```bash
# Hebrew (default, no flags needed)
python3 lib/google_search.py search "חדשות טכנולוגיה"

# English
python3 lib/google_search.py search "technology news" --lang en

# Arabic
python3 lib/google_search.py search "أخبار التكنولوجيا" --lang ar
```

---

## 安装方法

```bash
bash skills/google-search/install.sh
```