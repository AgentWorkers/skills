---
name: arena-research
description: >
  通用型 Are.na 研究工具。它可以在 Are.na 平台上搜索精心策划的资料集、参考资料、视觉灵感以及与任何主题相关的链接资源。该工具还能分析各个频道之间的关联关系，帮助用户发现相关的想法和核心策划者。适用场景包括：  
  (1) 用户输入“arena research”、“search arena for”、“search are.na for”等指令时；  
  (2) 用户正在进行需要精心策划的参考资料支持的工作（如设计研究、文化分析、艺术指导、概念探索或阅读列表制定等）；  
  (3) 用户希望了解人们如何围绕某个主题组织信息（即通过频道结构来获取洞察）。  
  **不适用场景**：  
  - 发布内容  
  - 账户管理  
  - 实时新闻或突发新闻（请使用 x-research 工具）。
---
# Arena Research

这是一种通用的研究方法，用于在Are.na平台上进行探索性研究。你可以将任何研究问题分解为多个具体的搜索任务，探索不同的信息渠道，通过连接图发现相关的想法，识别关键的策划者（curators），深入研究相关的内容，并将这些信息整合成一份有来源的简报。

有关API的详细信息（端点、认证方式、响应格式），请参阅`references/arena-api.md`。

## 何时使用Arena与其他资源

- **Are.na**：提供精选的参考资料、视觉化的研究内容、设计思维分析、文化研究资料、阅读清单，以及人们组织信息的方式。这些资源具有较高的信息价值，由人工策划，属于长尾内容。
- **X/Twitter**（x-research）：实时反馈、开发者讨论、产品发布、突发新闻以及专家的观点。信息更新迅速，但数量庞大。
- **网络搜索**：提供事实性答案、文档资料、时事信息以及具体的URL链接。

Are.na不仅仅是一个信息库，它的价值还在于人们如何组织这些内容，以及他们将这些内容与其他什么内容进行了关联。

## 命令行工具（CLI）

所有命令都在这个技能目录下执行：

```bash
cd ~/clawd/skills/arena-research
source ~/.config/env/global.env
```

### 搜索

```bash
bun run arena-search.ts search "<query>" [options]
```

**选项：**
- `--type Channel|Block|Text|Image|Link|User|Group` — 过滤结果类型（默认：全部）
- `--sort score|created|updated|connections|random` — 排序方式（默认：按评分排序）
- `--scope all|my|following` — 搜索范围（默认：全部；`my`/`following`需要认证）
- `--per N` — 每页显示的结果数量（默认：24条，最多100条）
- `--page N` — 页码
- `--quick` — 快速模式：显示10条结果，缓存1小时，仅显示频道内容，按连接关系排序
- `--save` — 将结果保存到`~/clawd/drafts/arena-research-{slug}-{date}.md`
- `--json` — 以原始JSON格式输出结果
- `--markdown` — 以Markdown格式输出结果

**示例：**
```bash
bun run arena-search.ts search "tools for thought" --type Channel --sort connections
bun run arena-search.ts search "brutalist web design" --quick
bun run arena-search.ts search "cybernetics" --type Link --per 50
bun run arena-search.ts search "spatial computing" --scope my
```

### 频道（Channel）

```bash
bun run arena-search.ts channel <slug-or-id> [options]
```

**选项：**
- `--sort position|created|updated` — 内容排序方式（默认：按显示顺序）
- `--type Text|Image|Link|Attachment|Embed|Channel` — 过滤内容类型
- `--per N` / `--page N` — 分页显示结果
- `--connections` — 显示与该频道共享内容的频道（通过连接图显示）
- `--save` / `--json` / `--markdown` — 保存相关内容

**示例：**
```bash
bun run arena-search.ts channel arena-influences
bun run arena-search.ts channel arena-influences --type Link --per 50
bun run arena-search.ts channel arena-influences --connections
```

### 块（Block）

```bash
bun run arena-search.ts block <id> [options]
```

**选项：**
- `--connections` — 显示该块出现在哪些频道中（通过连接图显示）
- `--json` — 以JSON格式输出相关频道信息

**示例：**
```bash
bun run arena-search.ts block 3235876
bun run arena-search.ts block 3235876 --connections
```

### 用户（User）

```bash
bun run arena-search.ts user <slug-or-id> [options]
```

**选项：**
- `--per N` / `--page N` — 显示指定数量的用户信息
- `--json` — 以JSON格式输出用户信息

### 我（Me）

```bash
bun run arena-search.ts me
```

显示已认证用户的个人资料和其关注的频道。需要`ARENA_ACCESS_TOKEN`才能使用此功能。

### 缓存（Cache）

```bash
bun run arena-search.ts cache clear
```

## 研究流程（探索性研究）

在进行深入研究时，请遵循以下步骤：

### 1. 将问题分解为多个搜索策略

将研究问题转化为3-5个搜索查询，从不同角度来探讨这个主题。

从多个抽象层次考虑这个主题：
- **直接关键词**：显而易见的搜索词（如“空间计算”、“极简主义网页设计”）
- **相关概念**：相关领域（如“触觉界面”、“具体建筑”）
- **用户用语**：Are.na用户实际使用的术语（如“思考工具”、“数字花园”、“网络用语”）
- **更广泛的类别**：该领域的总体主题（如“交互设计”、“网页美学”）
- **具体参考资料**：该领域内的知名作品、人物或项目

首先，按照频道之间的连接关系对结果进行排序，找到关联度最高的频道：

```bash
bun run arena-search.ts search "tools for thought" --type Channel --sort connections --per 20
```

### 2. 搜索并评估频道

执行每个搜索查询。每次搜索后，评估以下内容：
- **哪些频道包含深入的信息？** 查看结果中的条目数量。条目数量在2-3条的频道可能是简略的信息集合；条目数量超过50条的频道则可能是较为专业的资源集合。
- **这些频道由谁维护？** 如果同一个用户或团队在多个相关频道中都有内容，那么他们可能是值得直接探索的关键策划者。
- **还有哪些频道值得我深入了解吗？** 根据内容数量和相关性，选择排名前3-5的频道。

同时，也可以直接搜索特定的块（block）以找到相关的内容：

```bash
bun run arena-search.ts search "cybernetics" --type Link --sort connections --per 20
```

### 3. 深入探索热门频道

对于每个有潜力的频道，获取其所有内容：

```bash
bun run arena-search.ts channel tools-for-thought --per 50
```

**仅查看外部链接（这些链接对深入研究最有价值）：**

```bash
bun run arena-search.ts channel tools-for-thought --type Link --per 50
```

寻找以下类型的内容：
- **链接块（Link Block）**：带有来源URL的链接，这些是值得深入研究的参考资料
- **文本块（Text Block）**：包含文字内容的块，可用于做笔记或注释
- **图片块（Image Block）**：查看图片的标题和描述，但这类内容通常不适用于基于文本的研究
- **嵌套频道（Nested Channel）**：类型为“Channel”的子集合，也值得探索

### 4. 跟踪连接图

这是Are.na研究功能的核心。有两种策略：
- **块之间的连接关系**：对于那些内容有趣的块（链接或描述详细的块），查看它们出现在哪些其他频道中。
  这可以帮助你了解不同用户是如何理解同一主题的。
- **频道之间的关联关系**：对于你认为质量较高的频道，找出与其共享内容的其他频道。
  这可以帮助你发现与该频道相关的其他概念或领域。

**图谱深度**：通常一次连接就足够了。除非有特殊原因，否则不需要进一步深入探索。

### 5. 识别关键策划者

在探索过程中，记录那些频繁出现的用户：
- 同一用户可能维护多个相关频道
- 同一用户可能与你探索过的多个频道都有关联
- 在该领域内拥有大量关注者的用户

获取这些用户的个人资料和他们关注的频道：

```bash
bun run arena-search.ts user charles-broskoski
```

### 6. 深入研究链接内容

如果某个块是链接类型（Link Type）并且带有来源URL，可以使用`web_fetch`命令来读取实际内容。优先选择以下类型的链接：
- 在多个频道中出现的链接（在步骤4a中关联度较高的链接）
- 来自内容丰富或关注者众多的频道的链接
- 指向论文、博客文章、GitHub仓库、研究论文或文档的链接
- 与研究问题直接相关的链接

**无需深入研究的链接类型包括：**
- 社交媒体帖子
- 图片库或作品集
- 需付费才能访问的内容
- 已失效的链接（请检查`state`字段，`available`表示链接仍然有效）

### 7. 搜索你自己的收藏内容

如果你在寻找自己之前保存的内容，可以使用相应的命令：

```bash
bun run arena-search.ts search "query" --scope my
```

或者搜索你关注的用户发布的内容：

```bash
bun run arena-search.ts search "query" --scope following
```

### 8. 整合研究结果

按照**主题**对搜索结果进行分类，而不是按照搜索查询来分组。每个主题应该能够涵盖一组相关的频道、块和策划者。

```markdown
### [Theme/Finding Title]

[1-2 sentence summary of what curators are collecting and how they frame it]

**Key channels:**
- [Channel Title](https://www.are.na/owner/slug) by @username — N items
  [Brief description of scope and quality]
- [Channel Title](https://www.are.na/owner/slug) by @username — N items
  [Brief description]

**Notable content:**
- [Block title](source_url) — found in N channels
  [Why it's significant]

**Key curators:**
- [@username](https://www.are.na/slug) — N channels, N followers
  [What they focus on]

**Connected territory:**
- [Adjacent channel](https://www.are.na/owner/slug) — overlaps via shared blocks
  [What this connection reveals about the topic]
```

### 9. 保存结果

使用`--save`选项将结果保存到`~/clawd/drafts/arena-research/{topic-slug}-{YYYY-MM-DD}.md`文件中。

保存时请添加元数据脚注：

```markdown
---
## Research Metadata
- **Query**: [original question]
- **Date**: YYYY-MM-DD
- **Source**: Are.na v3 API
- **API calls**: N search queries + N channel fetches + N block connection lookups + N deep-dives
- **Channels explored**: N
- **Blocks scanned**: ~N
- **Search terms used**: [list the actual search strings]
- **Limitations**: [any gaps]
```

## 优化建议：
- **结果中包含太多浅层信息？** 可以过滤掉结果数量少于10条的频道
- **结果太少？** 扩大搜索关键词范围，尝试使用同义词，或者取消`--type`过滤选项
- **想要查看被保存最多的内容？** 可以使用`--sort connections`选项按连接关系排序结果
- **需要查找特定类型的链接？** 使用`--type Link`搜索外部链接，使用`--type Text`搜索文本内容
- **某个频道的内容太多，难以浏览？** 可以使用`--type`和`--sort`选项来筛选频道
- **想进一步扩展搜索范围？** 选择连接数量最多的3个块，然后继续探索它们的关联内容
- **遇到困难？** 可以搜索已知的参考资料或相关专家，再从他们的频道开始探索
- **需要进行视觉化研究？** 使用`--type Image`选项，因为Are.na常用于制作情绪板或艺术方向的素材

## 内容类型快速参考

| 内容类型 | 关键字段 | 研究价值 |
|-----------|-----------|---------------|
| `Link` | `source.url`, `source.title`, `description` | 外部参考资料，可使用`web_fetch`深入研究 |
| `Text` | `content`（Markdown格式） | 笔记、注释或原创内容 |
| `Image` | `image.src`, `title`, `description` | 视觉参考资料 |
| `Attachment` | `attachment.url`, `title` | PDF文件或文档 |
| `Embed` | `embed.url`, `title` | 视频或音频文件 |
| `Channel` | 嵌套在内容中的频道 | 可能包含子集合，值得进一步探索 |

## 文件结构

```
skills/arena-research/
├── SKILL.md              (this file)
├── arena-search.ts       (CLI entry point)
├── lib/
│   ├── api.ts            (Are.na v3 API wrapper: search, channels, blocks, users)
│   ├── cache.ts          (file-based cache, 15min TTL)
│   └── format.ts         (terminal + markdown formatters)
├── data/
│   └── cache/            (auto-managed)
└── references/
    └── arena-api.md      (Are.na v3 API endpoint reference)
```