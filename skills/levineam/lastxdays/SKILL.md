---
name: lastxdays
description: 研究并总结在过去N天内（或指定日期范围内）关于某个主题发生的所有事件。可以选择使用Reddit API以及x-cli/API/archive工具来获取数据；如果这些工具无法使用，则可退而求其次，通过网页方式获取信息。
---
# lastXdays 技能

该技能用于总结用户指定主题在**过去 N 天**（或特定日期范围 **YYYY-MM-DD → YYYY-MM-DD**）内发生的事情。

默认行为是优先使用网络资源（`web_search` + 选择性 `web_fetch`）。如果提供了可选的凭据或数据，可以尝试通过 API 从 Reddit 或 X 平台获取信息（优先使用 `x-cli`），如果这些方式不可用，则会回退到网络搜索。

## 触发模式

当用户消息中包含以下关键词时，该技能会被激活：
- `lastXdays` / `lastxdays`
- `过去 x 天`
- 类似这样的问题：“过去 N 天发生了什么”（后面可以跟一个主题）

## 默认模型

作为子代理启动时，默认使用 `sonnet` 模型（`anthropic/claude-sonnet-4-6`）。

仅对于简单的单源查询（一个主题、一个平台，无需读取文件），可以使用 `flash` 模型（`openrouter/google/gemini-2.0-flash-001`）。不过，`flash` 模型不适用于需要多步骤处理的复杂任务（如搜索 → 获取数据 → 读取文件 → 合成报告）。如果有疑问，请使用 `sonnet` 模型。

## 输入解析

从用户消息中解析以下信息：

### 1) 日期范围（如果明确提供更好）
如果用户提供了日期范围，例如：
- `from 2026-01-10 to 2026-02-08`
- `2026-01-10 → 2026-02-08`
那么：
- `start = YYYY-MM-DD`
- `end = YYYY-MM-DD`
如果这两个参数都提供了，则忽略 `N` 参数。

### 2) 天数（N）
否则，自动推断 `N` 的值：
- 在请求中查找整数 `N`，例如：
  - `lastxdays 7 <topic>`
  - `7 lastxdays <topic>`
  - `过去 14 天发生了什么（关于|re:) <topic>`
- 默认值：`N = 30`
- 限制范围：`N = min(max(N, 365)`

### 3) 数据来源（可选）
支持的数据来源包括：`web`、`reddit`、`x` 或 `all`。
- 可以输入的命令示例：
  - `for web` / `sources web`
  - `for reddit` / `sources reddit`
  - `for x` / `sources x`
  - `for all` / `sources all`
- 如果未指定来源，则默认使用 `all`。

### 4) 主题
- 去除触发词、日期范围和数据来源信息后剩余的文本即为查询主题。
- 如果主题为空或不明确，系统会询问一个明确的问题以获取更多信息。

## 日期范围的计算方式

使用**包含性**的日期范围（以本地时间为基准）：
- `freshness = start + "to" + end`（例如：`2026-01-10to2026-02-08`）

用于计算“过去 N 天”范围的辅助脚本：`node scripts/lastxdays_range.js <N>`

## 可选的非网络数据来源（Reddit/X）

可以使用以下脚本从 Reddit 或 X 平台获取数据：
- `node scripts/lastxdays_ingest.js --source=reddit|x --topic "..." --start YYYY-MM-DD --end YYYY-MM-DD --limit 40`
- 该脚本会尝试：
  - **Reddit**：使用 OAuth 访问官方 API（如果有凭据）；否则返回 `fallback:true`
  - **X**：首先使用 `x-cli` 进行搜索（如果已安装/配置），然后使用 Twitter API v2 的最近搜索功能（如果使用了 bearer token 且搜索范围在 7 天内有效）；如果这些方法不可用，则使用本地档案 `~/clawd/data/x-archive/`。如果这些方法都不可用，也会返回 `fallback:true`。

**使用 API 模式时需要设置的环境变量**：
- Reddit：
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - 推荐使用 `REDDIT_REFRESH_TOKEN`，或者 `REDDIT_USERNAME` + `REDDIT_PASSWORD`
  - 可选：`REDDIT_USER_AGENT`
- X API（仅适用于最近的数据）：
  - `X_BEARER_TOKEN`（也可以使用 `TWITTER_BEARER_TOKEN`
- x-cli（推荐用于代理任务）：
  - 安装：`uv tool install x-cli`（或从源代码安装）
  - 在 `~/.config/x-cli/.env` 中配置凭据（支持与 x-mcp 共享配置）
  - 如果使用了 x-cli，`lastxdays_ingest.js` 会优先使用这些凭据进行搜索

**凭据加载机制**：
- 如果存在 `~/.config/last30days/.env` 文件，会从中读取凭据；如果文件缺失，系统会尝试使用环境变量。

## 研究流程：
1) 计算开始日期、结束日期和数据的新鲜度。
2) 对于每个指定的数据来源：
    - **Web**：
      - 查询：`<topic>`
      - 使用 `web_search` 并设置 `freshness` 参数（返回 5–8 条结果）
      - 可选地使用 `web_fetch` 获取 2–6 条最佳链接。
    - **Reddit**：
      - 使用 `node scripts/lastxdays_ingest.js --source=reddit ...` 进行搜索
      - 如果返回的结果数组 `items[]` 为空或数量过少（例如少于 3 条），可以回退到网络搜索以获取更多信息。
    - **X**：
      - 使用 `node scripts/lastxdays_ingest.js --source=x ...` 进行搜索
      - 如果 `mode` 设置为 `x-cli`、`api` 或 `archive`，返回的结果被视为“重要链接”（每个链接都有对应的 URL）
        - 如果 `mode` 为 `x-cli`，说明结果来自本地 `x-cli` 的执行
        - 如果 `mode` 为 `archive`，说明链接来自本地 X 档案
      - 如果结果数组为空或数量过少，可以回退到网络搜索以获取更多信息。

## 输出格式（Markdown）

输出格式如下：
```
## lastXdays — <N> 天 — <topic>
```
- 如果指定了日期范围，可以将 `<N> 天` 替换为 `YYYY-MM-DD → YYYY-MM-DD`。

输出内容包括以下部分：
1) **使用的日期范围**：`YYYY-MM-DD → YYYY-MM-DD`（可选包括新鲜度信息）
2) **主要主题**：3–7 条要点，总结主要的故事线或趋势
3) **重要链接**：按平台分组显示（仅包括实际被搜索的平台）：
  - **Web**
  - **Reddit**
  - **X**
对于每个链接或内容：
  - 以 Markdown 格式显示链接
  - 说明该链接的重要性（如果无法获取完整内容，会标注说明）
4) **后续建议**：提供 3 个可供复制的搜索建议

## 本地测试示例：
- `node scripts/lastxdays_range.js 7`：测试日期范围的计算
- `node scripts/lastxdays_ingest.js --source=reddit ...`：从 Reddit 获取数据（需要凭据）
- `node scripts/lastxdays_ingest.js --source=x ...`：从 X 平台获取数据（如果安装了 x-cli；否则使用 API）
- `x-cli -v -j tweet search ...`：直接使用 x-cli 进行搜索

**示例用法**：
- `lastxdays AI agents for web`：查询关于 AI 的网络内容
- `last x days 10 bitcoin ETF flows`：查询过去 x 天内的比特币 ETF 流动情况
- `what happened in the last 7 days about OpenAI for reddit`：查询过去 7 天内关于 OpenAI 的 Reddit 内容
- `14 lastXdays Apple Vision Pro for web`：查询过去 14 天内关于 Apple Vision Pro 的网络内容
- `lastxdays 30 OpenAI sources all`：查询过去 30 天内的 OpenAI 相关信息（涵盖所有来源）
- `lastxdays from 2026-01-01 to 2026-01-15 about Anthropic sources reddit`：查询过去 15 天内关于 Anthropic 的 Reddit 内容
```