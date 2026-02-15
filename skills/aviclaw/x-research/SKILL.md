---
name: x-research
version: 1.0.0
description: >
  通用型X/Twitter研究工具。该工具可在X平台上搜索实时观点、开发者讨论、产品反馈、文化评论、突发新闻以及专家意见。其工作原理类似于传统的网络研究工具，但以X平台作为数据来源。适用场景包括：  
  (1) 用户请求“进行X平台相关研究”、“在X平台上搜索某内容”、“查看人们对某事的看法”等；  
  (2) 当用户正在处理需要X平台最新讨论内容作为背景信息的项目时（例如新库发布、API变更、产品发布、文化事件或行业动态）；  
  (3) 用户希望了解开发者、专家或社区对某个话题的看法。  
  **不适用场景**：发布推文、账户管理，或搜索超过7天前的历史数据。
---
# X 研究

这是一套用于在 X/Twitter 上进行通用信息收集和分析的工具集。它可以将任何研究问题分解为多个针对性的搜索任务，通过迭代的方式优化搜索结果，跟踪相关讨论线程，深入分析链接内容，并最终整理成一份详细的报告。

有关 X API 的详细信息（端点、操作符、响应格式），请参阅 `references/x-api.md`。

## 命令行工具（CLI）

所有命令均在该工具目录下执行：

```bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
```

### 搜索

```bash
bun run x-search.ts search "<query>" [options]
```

**选项：**
- `--sort likes|impressions|retweets|recent` — 排序方式（默认：按点赞数）
- `--since 1h|3h|12h|1d|7d` — 时间筛选条件（默认：过去 7 天）。也支持以分钟（`30m`）或 ISO 时间戳为单位进行筛选。
- `--min-likes N` — 根据最低点赞数进行筛选
- `--min-impressions N` — 根据最低浏览量进行筛选
- `--pages N` — 要获取的页面数（1-5 页，默认：每页 100 条推文）
- `--limit N` — 显示的最大结果数量（默认：15 条）
- `--quick` — 快速模式：仅显示第 1 页的内容，最多 10 条结果，自动过滤无关内容（`-is:retweet -is:reply`），并保留 1 小时的缓存记录，同时提供费用统计信息
- `--from <username>` — 用于简化查询中的 `from:username` 参数
- `--quality` — 筛选互动量较高的推文（至少获得 10 个点赞）
- `--no-replies` — 不包括回复内容
- `--save` — 将搜索结果保存到 `~/clawd/drafts/x-research-{slug}-{date}.md`
- `--json` — 以原始 JSON 格式输出结果
- `--markdown` — 以 Markdown 格式输出结果，便于编写研究文档

系统会自动添加 `-is:retweet` 参数（除非用户在查询中已经明确指定了该条件）。所有搜索结果都会显示预估的 API 使用费用。

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

### 个人资料查询

```bash
bun run x-search.ts profile <username> [--count N] [--replies] [--json]
```

用于获取指定用户的最新推文（默认不包含回复内容）。

### 线程查询

```bash
bun run x-search.ts thread <tweet_id> [--pages N]
```

根据根推文的 ID 获取完整的讨论线程。

### 单条推文查询

```bash
bun run x-search.ts tweet <tweet_id> [--json]
```

### 关注列表

```bash
bun run x-search.ts watchlist                       # Show all
bun run x-search.ts watchlist add <user> [note]     # Add account
bun run x-search.ts watchlist remove <user>          # Remove account
bun run x-search.ts watchlist check                  # Check recent from all
```

关注列表信息存储在 `data/watchlist.json` 文件中。可用于实时监控：检查关键账户是否发布了重要内容。

### 缓存

```bash
bun run x-search.ts cache clear    # Clear all cached results
```

缓存有效期为 15 分钟，以避免重复请求相同的数据。

## 研究流程（详细步骤）

在进行深入研究时（而不仅仅是简单搜索），请按照以下步骤操作：

### 1. 将问题分解为多个查询

将研究问题转化为 3-5 个关键词查询：
- **核心查询**：与主题直接相关的关键词
- **专家观点**：使用 `from:` 指定特定的专家
- **问题点**：如 `(broken OR bug OR issue OR migration)` 等关键词
- **积极信号**：如 `(shipped OR love OR fast OR benchmark)` 等关键词
- **链接**：如 `url:github.com` 或指向特定域名的链接
- **减少无关内容**：自动添加 `-is:retweet`，如有需要可添加 `-is:reply`
- **处理加密货币相关垃圾信息**：在处理加密货币相关内容时，添加 `-airdrop -giveaway -whitelist` 参数

### 2. 执行搜索并提取结果

通过 CLI 执行每个查询。每次搜索后，需要评估：
- 所获取的信息是有用的还是无用的？根据需要调整查询条件。
- 是否有值得关注的专家观点（使用 `from:` 指定专家）？
- 是否有值得跟踪的讨论线程（使用 `thread` 命令）？
- 是否有值得深入分析的链接资源（使用 `web_fetch` 命令）？

### 3. 跟踪讨论线程

当某条推文的互动量较高或是一个讨论的起点时，需要继续跟踪该线程：

```bash
bun run x-search.ts thread <tweet_id>
```

### 4. 深入分析链接内容

当推文链接到 GitHub 仓库、博客文章或文档时，使用 `web_fetch` 命令获取这些资源。优先选择以下类型的链接：
- 被多条推文引用的链接
- 来自互动量较高的推文的链接
- 与研究主题直接相关的资源

### 5. 整理分析结果

按主题对收集到的信息进行分类，而不是按原始查询条件进行分类：

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

- **信息过多？** 添加 `-is:reply` 参数，使用 `--sort likes` 选项缩小搜索范围，或进一步细化关键词。
- **结果太少？** 使用 `OR` 运算符扩大搜索范围，或移除过于严格的查询条件。
- **遇到加密货币相关垃圾信息？** 添加 `-airdrop -giveaway -whitelist` 参数来过滤这些内容。
- **只关注专家的观点？** 使用 `from:` 指定专家，或设置 `--min-likes 50` 来筛选。
- **注重实质内容而非表面观点？** 使用 `has:links` 来筛选有实际价值的链接。

## 实时监控集成

在系统运行时，可以通过 `watchlist check` 命令检查关键账户是否发布了重要内容。只有真正有趣或具有行动价值的推文才需要报告给 Frank。

## 文件结构

```
skills/x-research/
├── SKILL.md           (this file)
├── x-search.ts        (CLI entry point)
├── lib/
│   ├── api.ts         (X API wrapper: search, thread, profile, tweet)
│   ├── cache.ts       (file-based cache, 15min TTL)
│   └── format.ts      (Telegram + markdown formatters)
├── data/
│   ├── watchlist.json  (accounts to monitor)
│   └── cache/          (auto-managed)
└── references/
    └── x-api.md        (X API endpoint reference)
```