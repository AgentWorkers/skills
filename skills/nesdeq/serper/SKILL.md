---
name: serper
description: 通过 Serper API 进行 Google 搜索，并提取完整页面内容。该 API 支持快速查询以及并发页面抓取（超时时间为 3 秒）。一个精心设计的查询即可返回丰富的搜索结果，因此无需多次调用 API。提供两种搜索模式，并支持显式的地区设置。API 密钥通过 `.env` 文件进行配置。
metadata: {"version": "3.0.1", "tags": ["search", "web-search", "serper", "google", "content-extraction"]}
---

# Serper

通过 Serper API 进行 Google 搜索。该 API 不仅会获取搜索结果，还会读取实际网页内容，并使用 trafilatura 工具提取完整的文本信息（而不仅仅是网页片段）。因此，你能够获得整篇文章的文本内容。

### 工作原理

1. **调用 Serper API**：快速执行 Google 搜索，立即返回结果页面的 URL。
2. **并发抓取页面**：使用 trafilatura 并发抓取所有结果页面，每个页面的抓取超时时间为 3 秒。
3. **流式输出**：每当一个页面抓取完成，结果就会依次输出。

每次调用默认返回 5 个结果（`default` 模式），或在 `current` 模式下返回最多 6 个结果，每个结果都包含完整的页面内容。这些信息量已经非常丰富了。

---

## 查询技巧

**设计一个高质量的搜索查询**。这通常就足够了。

每次调用都会返回多个包含完整页面内容的结果——一个查询就能覆盖广泛的搜索范围。无需通过多次搜索来“探索”某个主题。一个设计合理的查询，配合正确的搜索模式，就能满足需求。

**最多进行两次调用**：如果用户的请求确实涉及两个不同的主题（例如“比较 X 和 Y”，此时需要分别进行两次搜索；或者一次 `default` 模式调用加上一次 `current` 模式调用来获取不同方面的信息）。绝对不要超过两次。

**请勿：**
- 用不同的表述方式重复执行相同的查询以“获取更多结果”。
- 通过多次连续搜索来“深入挖掘”信息——因为完整的页面内容本身已经包含了丰富的信息。
- 先进行一次搜索找到所需内容，然后再进行另一次搜索——请直接阅读你已获取到的内容。

---

## 适用场景

**在以下情况下使用 Serper：**
- 当你需要从网络上获取当前、真实的信息时。
- 当你需要研究需要整篇文章内容的主题时（而不仅仅是片段）。
- 当你需要获取新闻和时事信息时。
- 当你需要获取产品信息、价格、对比数据或评论时。
- 当你需要阅读技术文档或操作指南时。
- 在任何需要阅读完整网页内容的情况下。

**请勿在以下情况下使用此技能：**
- 对于可以通过训练数据回答的问题。
- 对于纯数学计算、代码执行或创意写作任务。
- 对于简单的问候或闲聊。

**重要提示：** 该技能已经完成了网页内容的获取和提取工作。请勿对 Serper 返回的 URL 使用 `web_fetch`、`WebFetch` 或其他任何 URL 获取工具——所需内容已经包含在输出结果中。

---

## 两种搜索模式

Serper 提供两种搜索模式，请根据查询内容选择合适的模式：

### `default` — 通用搜索（所有时间范围内的结果）
- 执行所有时间范围内的 Google 搜索，返回 **5 个结果**，每个结果都包含完整的页面内容。
- 适用于：一般性问题、研究、操作指南、长期有效的内容、产品信息、技术文档、对比分析、教程等不依赖时间敏感性的内容。

### `current` — 新闻和最新信息
- 搜索过去一周内的 Google 网页内容（3 个结果）以及 Google 新闻（3 个结果），每个结果都包含完整的页面内容。
- 适用于：新闻、时事、最新发展、突发新闻、公告等时效性强的内容。

#### 模式选择指南

| 查询关键词 | 使用模式 |
|---------------|------|
| “X 是如何工作的？”、“X 是什么？”、“解释 X” | `default` |
| 产品研究、对比分析、教程 | `default` |
| 技术文档、操作指南 | `default` |
| 历史性主题、长期有效的内容 | `default` |
| “新闻”、“最新的”、“本周的”、“最近的” | `current` |
| “发生了什么”、“突发新闻”、“已发布”、“新发布的” | `current` |
| 时事、政治、体育比分、股票价格 | `current` |

---

## 地区设置（非英语查询时必需）

**默认设置为全球范围**——不进行国家过滤，返回英文结果。此设置仅适用于英语查询。

**在以下任何情况下，你必须设置 `--gl` 和 `--hl` 参数：**
- 用户的消息使用非英语语言。
- 你构建的搜索查询使用非英语语言。
- 用户提到了特定的国家、城市或地区。
- 用户要求获取特定语言地区的结果（如价格、新闻、商店信息等）。

**如果用户使用德语输入，必须设置 `--gl de --hl de`。没有例外。**

| 情况 | 需要设置的参数 |
|----------|-------|
| 使用英语查询且不指定国家目标 | **省略 `--gl` 和 `--hl`** |
- 使用德语查询或用户使用德语输入，或搜索目标为德国/奥地利/瑞士 | `--gl de --hl de` |
- 使用法语查询或用户使用法语输入，或搜索目标为法国 | `--gl fr --hl fr` |
- 其他非英语语言或地区的查询 | `--gl XX --hl XX`（ISO 语言代码） |

**经验法则：** 如果查询字符串中包含非英语单词，请设置 `--gl` 和 `--hl` 以匹配相应的语言。

---

## 使用方法

```bash
python3 scripts/search.py -q "QUERY" [--mode MODE] [--gl COUNTRY] [--hl LANG]
```

### 示例

```bash
# English, general research
python3 scripts/search.py -q "how does HTTPS work"

# English, time-sensitive
python3 scripts/search.py -q "OpenAI latest announcements" --mode current

# German query — set locale + current mode for news/prices
python3 scripts/search.py -q "aktuelle Preise iPhone" --mode current --gl de --hl de

# German news
python3 scripts/search.py -q "Nachrichten aus Berlin" --mode current --gl de --hl de

# French product research
python3 scripts/search.py -q "meilleur smartphone 2026" --gl fr --hl fr

```

---

## 输出格式

输出结果是一个 **流式 JSON 数组**——每个页面抓取完成后，结果会依次以 JSON 格式输出：

```json
[{"query": "...", "mode": "default", "locale": {"gl": "world", "hl": "en"}, "results": [{"title": "...", "url": "...", "source": "web"}, ...]}
,{"title": "...", "url": "...", "source": "web", "content": "Full extracted page text..."}
,{"title": "...", "url": "...", "source": "news", "date": "2 hours ago", "content": "Full article text..."}
]
```

数组的第一个元素是搜索元数据，后续元素包含完整的页面内容。

结果字段包括：
- `title`：页面标题
- `url`：来源 URL
- `source`：`"web"`、`"news"` 或 `"knowledge_graph"`（表示数据来源）
- `content`：提取的完整页面文本（如果提取失败，则使用搜索片段）
- `date`：仅在新闻结果中提供（网页结果可能不包含此字段）

---

## 命令行接口（CLI）参考

| 参数 | 说明 |
|------|-------------|
| `-q, --query` | 搜索查询（必需） |
| `-m, --mode` | `default`（所有时间范围内的结果，5 个）或 `current`（过去一周内的结果及新闻，各 3 个） |
| `--gl` | 国家代码（例如 `de`、`us`、`fr`、`at`、`ch`） |
| `--hl` | 语言代码（例如 `en`、`de`、`fr`） |