---
name: podcast-discovery
description: "**Wherever.Audio 的播客发现功能：**  
该功能用于查找播客节目及其剧集，并生成指向这些内容的链接（URL）。"
user-invocable: true
metadata:
  openclaw:
    emoji: "🎧"
---
# podcast-discovery

这是一个用于Wherever(Audio)平台的播客发现功能。它可以根据自然语言查询找到相应的播客节目或剧集，并返回一个可以在wherever.audio平台上播放的链接。

**注意：** 请勿将此功能用于非播客相关的查询（如普通网页搜索、音乐搜索等）。

## 触发短语

当用户输入的文本包含以下关键词时，立即触发此功能：
- “find podcast”（查找播客）
- “find the podcast”（找到播客）
- “look up podcast”（查询播客）
- “search podcasts”（搜索播客）
- “find episode”（查找剧集）
- “podcast episode about”（关于……的播客剧集）
- “latest episodes”（最新剧集）
- “give me a wherever link”（提供一个wherever音频链接）
- “wherever link”（wherever链接）
- “listen link”（播放链接）
- “show link”（节目链接）
- 特定节目/主持人的名称，例如：“Radiolab”、“Lex Fridman”、“Hard Fork”或“Joe Rogan”

触发后，优先构建播放链接，而非提供元数据信息。

## 主要目标（最高优先级）

当有足够的信息时，立即生成一个可用的wherever音频链接（`/show`或`/listen`）。

**成功条件：**
1. 从Clawsica获取到有效的RSS URL。
2. 如果`contentScope`为`podcast-show`，立即返回节目链接。
3. 如果`contentScope`为`podcast-episode`且找到匹配的剧集，立即返回剧集链接。
即使获得了元数据、搜索摘要或候选列表，也不要停止处理，直到生成有效的链接。

## 链接模板

- **剧集链接（`contentScope = podcast-episode`）：**
  `https://wherever.audio/listen?rssUrl={rss_url}&itemGuid={guid}&fallbackLink={fallback}`

- **节目链接（`contentScope = podcast-show`）：**
  `https://wherever.audio/show?rssUrl={rss_url}`

所有`placeholder`值都必须进行URL编码。

## 行为策略：**先生成链接，再询问用户**

默认行为是直接生成并返回链接。只有在以下情况下才询问用户：
- 无法判断用户是需要节目还是剧集。
- 经过多次尝试后，Clawsica仍未返回合理的节目/RSS结果。
- 多个剧集候选项的匹配度相近，且没有明确的最佳选择。

如果以上情况都不适用，无需询问用户确认，直接返回链接。

## 令牌使用策略：
- 首先使用本地工具进行处理，然后仅将压缩后的结果字段发送给模型。
- 绝不要将原始RSS XML、完整的数据集或大量元数据发送给模型。
- 对于剧集匹配，仅传递用于决策和链接构建的顶级候选项。

## 工作流程

### 第1步——分类查询

在搜索之前，根据两个维度对用户的查询进行分类：

**intentType**——请求的类型是什么？
- `specific-podcaster`——用户指定了节目或主持人的名称（例如：“Lex Fridman”、“Radiolab”）
- `specific-topic`——用户描述了主题或嘉宾（例如：“关于AI的Geoffrey Hinton访谈”）
- `discovery`——广泛搜索（例如：“最佳科学播客”、“关于太空的播客”）

**contentScope**——用户需要查找什么？
- `podcast-show`——一个节目/数据集（例如：“查找Radiolab播客”）
- `podcast-episode`——一个特定的剧集（例如：“Radiolab关于颜色的剧集”）

### 第2步——查找节目

- **如果`intentType`为`specific-podcaster`**（已知节目名称）：
  直接使用Clawsica进行搜索（步骤3）。查询中通常包含节目名称。

- **如果`intentType`为`specific-topic`或`discovery`**（未知节目名称）：
  先在网络上搜索可能的节目名称，然后再使用这些名称在Clawsica中进行搜索。

### 第3步——使用Clawsica查找节目

使用公开的Clawsica接口查找播客节目。该接口会返回包括RSS feed URL在内的节目元数据。

```bash
curl -s "https://clawsica.wherever.audio/p?q=radiolab"
```

返回一个节目对象的JSON数组。每个对象包含一个`url`字段，其中存储了RSS feed的URL。

**重要提示：** 仅使用Clawsica结果中的`url`字段作为RSS URL。不要使用网页链接、Apple Podcasts链接、Spotify链接或其他类型的URL——Wherever(Audio仅支持RSS feed URL。如果Clawsica未返回结果且无法获取有效的RSS feed URL，请告知用户无法找到该播客，而不是使用非RSS URL进行猜测。

如果Clawsica未返回结果，可以尝试不同的拼写或更宽泛的搜索词。详细API参考请参见`references/CLAWSICA_API.md`。

### 第4步——根据`contentScope`进行分类

- **如果`contentScope`为`podcast-show`**：
  使用步骤3中的RSS URL生成节目链接，并立即展示给用户。无需再次确认。
  **示例：** `https://wherever.audio/show?rssUrl=https%3A%2F%2Ffeeds.feedburner.com%2Fradiolab`

- **如果`contentScope`为`podcast-episode`**：
  转到步骤5。

### 第5步——运行本地工具（用于查找剧集）

对于剧集的查找，使用本地工具而不是手动解析XML：

```bash
python scripts/search_feed_episodes.py --mode search --rss-url "https://feeds.feedburner.com/radiolab" --query "space stories" --limit 5
```

### 可选的语义重排序：

```bash
python scripts/search_feed_episodes.py --mode search --rss-url "https://feeds.feedburner.com/radiolab" --query "space stories" --limit 5 --semantic
```

**`search`输出的压缩格式：**
- **顶级键：** `mode`, `rssUrl`, `query`, `semanticUsed`, `candidateCount`, `candidates`
- **候选项键：** `guid`, `title`, `pubDate`, `fallbackLink`, `score`

使用这些候选项来选择最佳剧集。除非用户明确要求，否则不要返回数据集级别的元数据。

**选择规则：**
- 如果最高得分的候选项明显优于第二名，则自动选择。
- 如果顶级候选项得分相近，询问用户以消除歧义。

### 第6步——生成剧集链接

使用选中的`search`候选项的信息生成wherever.audio剧集链接：
- `rss_url`——步骤3中的feed URL
- `guid`——候选项的`guid`
- `fallback`——候选项的`fallbackLink`

**示例：**
```
https://wherever.audio/listen?rssUrl=https%3A%2F%2Ffeeds.feedburner.com%2Fradiolab&itemGuid=some-guid-value&fallbackLink=https%3A%2F%2Fradiolab.org%2Fepisode
```

将链接连同剧集标题和发布日期一起展示给用户。

### 可选功能——获取最新剧集和节目概览

如果用户请求获取某个已知节目的最新剧集：

```bash
python scripts/search_feed_episodes.py --mode newest --rss-url "https://feeds.feedburner.com/radiolab" --limit 10
```

**`newest`输出的压缩格式：**
- **顶级键：** `mode`, `rssUrl`, `count`, `items`
- **项目键：** `guid`, `title`, `pubDate`, `fallbackLink`

如果用户请求数据集级别的元数据：

```bash
python scripts/search_feed_episodes.py --mode overview --rss-url "https://feeds.feedburner.com/radiolab"
```

**`overview`输出的压缩格式：**
- **顶级键：** `mode`, `rssUrl`, `feedTitle`, `feedDescriptionShort`, `author`, `language`, `lastBuildDate`, `itemCount`

使用这些功能直接响应用户的需求，同时保持响应内容的简洁性。

**运行本地工具（适用于开发人员和测试）：**
路径：`scripts/search_feed_episodes.py`（相对于技能目录）
**依赖项：** `scripts/requirements.txt`（feedparser, rapidfuzz, pytest）
**快速启动（推荐，跨平台）：**
1. 在技能文件夹中创建并激活虚拟环境：
   `python3 -m venv .venv`
   `source .venv/bin/activate`   # macOS / Linux
   `venv\Scripts\activate`      # Windows (PowerShell)
2. 安装依赖项：
   `pip install -r scripts/requirements.txt`
3. 运行工具（示例）：
   `python scripts/search_feed_episodes.py --mode overview --rss-url "<RSS_URL>"
   `python scripts/search_feed_episodes.py --mode newest --rss-url "<RSS_URL>" --limit 10`
   `python scripts/search_feed_episodes.py --mode search --rss-url "<RSS_URL>" --query "attack on Iran" --limit 5 --semantic`
   注意：**该工具会输出符合技能要求的压缩JSON格式的结果。**
   **将脚本设置为可执行文件（`chmod +x scripts/search_feed_episodes.py`）以便直接运行。**
   如果系统限制了pip的使用，请使用虚拟环境。

## 响应格式

当链接可用时，按以下顺序响应：
1. Wherever音频的链接（第一行）。
2. 一行简短的说明，用于标识找到的节目/剧集。
3. 如果存在歧义，可添加一行说明。

**注意事项：**
- 如果可以生成wherever音频链接，请不要仅返回网页元数据。
- 如果所需的链接参数已经确定，无需询问用户“是否继续”。
- 除非确实需要消除歧义，否则不要提供候选选项。

**隐私政策：**
- 请勿泄露Clawsica的内部基础设施细节。
- Clawsica的搜索接口不需要身份验证。
- 详细API参考请参见`references/CLAWSICA_API.md`。
- 本地剧集搜索工具的命令和架构详情请参见`references/LOCAL_EPISODE_SEARCH.md`。

**示例提示：**
- “查找Geoffrey Hinton的访谈剧集，并提供一个wherever.audio链接。”
- “有哪些播客节目涵盖了Radiolab关于太空的节目？”
- “搜索BBC关于AI的科学播客。”
- “提供Lex Fridman的播客链接。”
- “查找Hard Fork播客。”