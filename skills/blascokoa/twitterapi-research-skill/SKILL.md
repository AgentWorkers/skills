---
name: x-research
description: >
  通用型X/Twitter研究工具。该工具用于在X平台上搜索实时观点、开发者讨论、产品反馈、文化评论、突发新闻以及专家意见。其工作原理类似于传统的网络研究工具，但以X平台作为数据来源。适用场景包括：  
  (1) 用户请求“进行X平台研究”、“在X平台上搜索某内容”、“查看人们对某事的看法”、“了解Twitter上的讨论”等；  
  (2) 用户正在处理需要X平台最新信息的项目（如新库发布、API变更、产品发布、文化事件或行业动态）；  
  (3) 用户希望了解开发者、专家或社区对某个主题的看法。  
  **注意：** 该工具不适用于发布推文或管理账户。  
  该工具通过第三方API（twitterapi.io）实现全文检索功能，可查询超过7天内的所有数据。
---
# X 研究

这是一套用于在 X（Twitter）平台上进行通用信息收集与分析的工具集。它能够将任何研究问题分解为多个针对性的搜索任务，通过迭代优化搜索策略、跟踪相关讨论线索、深入分析链接内容，并最终整理成一份有依据的研究报告。

有关 twitterapi.io API 的详细信息（端点、操作符及响应格式），请参阅 `references/x-api.md`。

## 命令行工具（CLI）

所有命令均在该工具目录下执行：

```bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env  # needs TWITTERAPI_IO_KEY
```

### 搜索

```bash
bun run x-search.ts search "<query>" [options]
```

**选项：**
- `--sort likes|impressions|retweets|recent` — 排序方式（默认：按点赞数排序）
- `--since 1h|3h|12h|1d|7d` — 时间筛选条件（默认：过去 7 天）。也支持以分钟（`30m`）或 ISO 时间戳形式指定。
- `--min-likes N` — 筛选条件：至少获得 `N` 个点赞的推文
- `--min-impressions N` — 筛选条件：至少获得 `N` 次展示的推文
- `--pages N` — 获取的页面数（1-25 页，默认：每页约 20 条推文）
- `--limit N` — 显示的结果数量上限（默认：15 条）
- `--quick` — 快速模式：仅显示第 1 页内容，最多 10 条推文，自动过滤无关内容（`-is:retweet -is:reply`），并显示费用统计信息
- `--from <username>` — 简写形式，等同于 `from:username` 的查询条件
- `--quality` — 筛选互动度较高的推文（至少获得 10 个点赞）
- `--no-replies` — 不包括回复内容
- `--save` — 将搜索结果保存到 `~/clawd/drafts/x-research-{slug}-{date}.md`
- `--json` — 以原始 JSON 格式输出结果
- `--markdown` — 以 Markdown 格式输出结果，便于编写研究报告

系统会自动添加 `-is:retweet` 这一筛选条件（除非用户已在查询中明确指定）。所有搜索结果都会显示预估的 API 使用费用。

**注意：** twitterapi.io 的搜索功能可覆盖全部数据（不受 7 天时间限制）。时间筛选通过 `since:` 操作符实现。

**示例：**
```bash
bun run x-search.ts search "BNKR" --sort likes --limit 10
bun run x-search.ts search "from:frankdegods" --sort recent
bun run x-search.ts search "(opus 4.6 OR claude) trading" --pages 2 --save
bun run x-search.ts search "$BNKR (revenue OR fees)" --min-likes 5
bun run x-search.ts search "BNKR" --quick
bun run x-search.ts search "BNKR" --from voidcider --quick
bun run x-search.ts search "AI agents" --quality --quick
```

### 查看用户资料

```bash
bun run x-search.ts profile <username> [--count N] [--replies] [--json]
```

用于获取指定用户的最新推文（默认不包含回复内容）。

### 跟踪讨论线索

```bash
bun run x-search.ts thread <tweet_id> [--pages N]
```

根据根推文的 ID 获取完整的讨论线索。

### 查看单条推文

```bash
bun run x-search.ts tweet <tweet_id> [--json]
```

### 添加到关注列表

```bash
bun run x-search.ts watchlist                       # Show all
bun run x-search.ts watchlist add <user> [note]     # Add account
bun run x-search.ts watchlist remove <user>          # Remove account
bun run x-search.ts watchlist check                  # Check recent from all
```

关注列表信息存储在 `data/watchlist.json` 文件中。可用于定期检查关键账户是否发布了重要内容。

### 缓存机制

系统采用 15 分钟的缓存机制，避免重复请求相同的数据。

## 研究流程（详细步骤）

在进行深入研究时，请遵循以下步骤：

### 1. 将问题分解为多个搜索任务

将研究问题转化为 3-5 个关键词查询：
- **核心查询**：直接与研究主题相关的关键词
- **专家观点**：使用 `from:` 指定特定专家的推文
- **问题点**：如 `(broken OR bug OR issue OR migration)` 等关键词
- **积极信号**：如 `(shipped OR love OR fast OR benchmark)` 等关键词
- **链接资源**：如 `url:github.com` 或指向特定网站的链接
- **过滤无关内容**：自动添加 `-is:retweet`；如需要可添加 `-is:reply`
- **过滤加密货币相关垃圾信息**：在涉及加密货币的搜索中添加 `-airdrop -giveaway -whitelist`

### 2. 执行搜索并提取信息

通过 CLI 执行每个查询。每次搜索后，评估以下内容：
- 找到的信息是否有价值？是否属于关键信息？
- 是否需要通过 `from:` 指定特定专家的推文进行进一步分析？
- 是否有值得深入研究的讨论线索（使用 `thread` 命令）？
- 是否有值得分析的链接资源（使用 `web_fetch` 命令）？

### 3. 跟踪讨论线索

当某条推文的互动度较高或是一个讨论的起点时，继续深入分析相关推文：

```bash
bun run x-search.ts thread <tweet_id>
```

### 4. 深入分析链接内容

当推文指向 GitHub 仓库、博客文章或文档时，使用 `web_fetch` 命令获取这些资源。优先选择以下类型的链接：
- 被多条推文引用的链接
- 来自互动度较高的推文的链接
- 与研究主题直接相关的资源

### 5. 整理分析结果

按主题对收集到的信息进行分类，而非按原始查询条件进行分组：

```
### [Theme/Finding Title]

[1-2 sentence summary]

- @username: "[key quote]" (NL, NI) [Tweet](url)
- @username2: "[another perspective]" (NL, NI) [Tweet](url)

Resources shared:
- [Resource title](url) — [what it is]
```

### 6. 保存结果

使用 `--save` 选项将结果保存到 `~/clawd/drafts/x-research/{topic-slug}-{YYYY-MM-DD}.md` 文件中。

## 优化建议：

- **信息过多？** 添加 `-is:reply` 以过滤无关回复；使用 `--sort likes` 根据点赞数排序；缩小搜索范围。
- **结果太少？** 使用 `OR` 运算符扩大搜索范围；移除过于具体的筛选条件。
- **遇到加密货币相关垃圾信息？** 添加 `-airdrop -giveaway -whitelist` 以过滤无关内容。
- **只关注专家观点？** 使用 `from:` 指定专家的推文；或设置 `--min-likes 50` 来筛选至少获得 50 个点赞的推文。
- **注重实质内容而非表面观点？** 使用 `has:links` 进行更精确的搜索。

## 定期检查机制

在定期检查系统中，可以运行 `watchlist check` 命令，查看关键账户是否发布了重要内容。只有真正有价值或具有行动意义的推文才会被报告给相关人员。

## 文件结构

```
skills/x-research/
├── SKILL.md           (this file)
├── x-search.ts        (CLI entry point)
├── lib/
│   ├── api.ts         (twitterapi.io wrapper: search, thread, profile, tweet)
│   ├── cache.ts       (file-based cache, 15min TTL)
│   └── format.ts      (Telegram + markdown formatters)
├── data/
│   ├── watchlist.json  (accounts to monitor)
│   └── cache/          (auto-managed)
└── references/
    └── x-api.md        (twitterapi.io endpoint reference)
```