---
name: lastxdays
description: 研究并总结在过去N天内（或指定的日期范围内）关于某个主题发生的事情。可以选择使用Reddit API以及x-cli/API/archive工具来获取数据；如果这些工具无法使用，则可以退而求其次，通过网页方式获取信息。
---

# lastXdays 技能

该技能用于汇总用户指定主题在**过去 N 天**（或特定日期范围 **YYYY-MM-DD → YYYY-MM-DD**）内发生的相关事件。

默认行为是优先使用网络资源（`web_search`）并进行选择性数据获取（`web_fetch`）。如果用户提供了可选的凭证或数据，可以尝试通过 API 从 Reddit 或 X 平台获取信息（优先使用 `x-cli`），如果这些资源不可用，则会回退到网络搜索。

## 触发模式

当用户消息中包含以下关键词时，该技能会被激活：
- `lastXdays` / `lastxdays`
- `last x days`
- 类似于 “过去 N 天发生了什么” 的问题（后面可以跟主题）

## 输入解析

从用户消息中解析以下信息：

### 1) 日期范围（如果明确提供则更好）
如果用户指定了一个日期范围，例如：
- `from 2026-01-10 to 2026-02-08`
- `2026-01-10 → 2026-02-08`

那么：
- `start = YYYY-MM-DD`
- `end = YYYY-MM-DD`
- 如果同时提供了 `start` 和 `end`，则忽略 `N` 参数。

### 2) 天数（N）
否则，系统会自动推断 `N` 的值：
- 从请求中查找整数 `N`，例如：
  - `lastxdays 7 <topic>`
  - `7 lastdays <topic>`
  - `what happened in the last 14 days (about|re:) <topic>`
- 默认值：`N = 30`
- 限制范围：`N = min(max(N, 365)`

### 3) 数据来源（可选）
支持的数据来源包括：`web`、`reddit`、`x` 或 `all`。
- 可以输入的参数有：
  - `for web` / `sources web`
  - `for reddit` / `sources reddit`
  - `for x` / `sources x`
  - `for all` / `sources all`
- 如果未指定，则默认使用 `all` 作为数据来源。

### 4) 主题
- 用户消息中剩余的部分（去除触发词、日期范围和数据来源信息后得到的内容即为主题。
- 如果主题为空或不明确，系统会询问一个明确的补充问题，然后停止处理。

## 日期范围的计算方式
使用**包含性**的日期范围（以本地时间为基准）：
- `freshness = start + "to" + end`（例如：`2026-01-10to2026-02-08`）

用于计算过去 N 天的辅助脚本：`node scripts/lastxdays_range.js <N>`

## 可选的非网络数据获取方式（Reddit/X）

可以使用以下辅助脚本从 Reddit 或 X 平台获取数据：
- `node scripts/lastxdays_ingest.js --source=reddit|x --topic "..." --start YYYY-MM-DD --end YYYY-MM-DD --limit 40`

脚本的获取方式如下：
- **Reddit**：如果用户有 OAuth 凭证，会使用官方 API；否则返回 `fallback:true`。
- **X**：首先尝试使用 `x-cli` 进行搜索（如果已安装/配置）；如果使用 bearer token 且搜索范围在 7 天以内，会使用 Twitter API v2 的近期搜索功能；如果这些方法都不可用，则会从本地档案 `~/clawd/data/x-archive/` 中获取数据，此时也会返回 `fallback:true`。

### 所需的环境变量（启用 API 模式时）

- Reddit：
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - 推荐使用 `REDDIT_REFRESH_TOKEN`，或者 `REDDIT_USERNAME` + `REDDIT_PASSWORD`
  - 可选：`REDDIT_USER_AGENT`

- X API（仅适用于近期数据）：
  - `X_BEARER_TOKEN`（也可以使用 `TWITTER_BEARER_TOKEN`）

- `x-cli`（推荐使用）：
  - 需要安装：`uv tool install x-cli`（或从源代码安装）
  - 在 `~/.config/x-cli/.env` 中配置凭证（支持与 x-mcp 共享配置）
  - 如果使用了 `x-cli`，`lastxdays_ingest.js` 会优先使用它来获取数据，而不是直接调用 API 或本地档案。

### 凭证加载机制
- 如果存在 `~/.config/last30days/.env` 文件，脚本会从中读取凭证信息；如果文件缺失，系统会使用环境变量来填充空白值。

## 数据获取流程
1) 计算 `start`、`end` 和 `freshness` 的值。
2) 对于每个指定的数据来源：
    - **Web**：查询 `<topic>`，并使用 `freshness` 参数进行搜索（返回 5–8 条结果）；可选地，使用 `web_fetch` 获取前 2–6 条最相关的链接。
    - **Reddit**：推荐使用 `node scripts/lastxdays_ingest.js --source=reddit ...`；如果返回的结果为空或数量过少（例如少于 3 条），可以回退到网络搜索。
    - **X**：推荐使用 `node scripts/lastxdays_ingest.js --source=x ...`；如果返回的结果为空或数量过少，也可以回退到网络搜索。

### 回退策略（当 `fallback=true` 时）
- 如果设置了 `fallback=true`，则会使用以下方式获取数据：
    - **Web**：查询 `site:reddit.com/r <topic>`，并使用相同的 `freshness` 参数。
    - **X**：查询 `site:x.com <topic>`，并使用相同的 `freshness` 参数。

### 链接/内容的筛选与去重
- 网络来源的数据优先选择权威性强的内容；Reddit 和 X 平台的数据优先选择互动度高或信息量大的内容。
- 最终显示的链接/条目数量限制在 10–20 条左右。

## 输出格式（Markdown）

输出格式如下：
```
## lastXdays — <N> 天 — <topic>
  - 如果指定了日期范围，可以将 `<N> 天` 替换为 `YYYY-MM-DD → YYYY-MM-DD`。

输出内容包括以下部分：
1) **使用的日期范围**：`YYYY-MM-DD → YYYY-MM-DD`（以及可选的新鲜度信息）
2) **主要趋势**：3–7 条总结主要事件或趋势的列表
3) **重要链接**：按平台分类显示链接（仅包括实际被搜索过的平台）：
  - **Web**
  - **Reddit**
  - **X**
    - 对于每个链接/条目：
      - 使用 Markdown 格式显示链接
      - 说明该链接的重要性
      - 如果无法获取内容或仅显示摘要，会进行相应说明
4) **后续可进行的操作**：提供 3 条可供复制的搜索建议
```

## 示例用法：
- `lastxdays AI agents for web`
- `last x days 10 bitcoin ETF flows`
- `what happened in the last 7 days about OpenAI for reddit`
- `14 lastXdays Apple Vision Pro for web`
- `lastxdays 30 OpenAI sources all`
- `lastxdays from 2026-01-01 to 2026-01-15 about Anthropic sources reddit`
```