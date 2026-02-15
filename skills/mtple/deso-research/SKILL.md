---
name: deso-research
description: 使用 deso-ag CLI 工具在去中心化社交网络（Farcaster、Lens、Nostr、Bluesky）中研究并分析内容。当用户希望在去中心化社交平台上研究某个主题、分析热门内容、提取讨论关键词、浏览 Farcaster 的频道或比较不同网络之间的用户参与度时，可以使用此技能。触发指令包括：“在 Farcaster 上研究 X”、“Lens 上的热门内容是什么”、“分析 [主题] 在各个去中心化网络中的情况”、“在 deso 网络中搜索 [主题]”、“提取热门关键词”、“浏览 Farcaster 的频道”、“人们在 Farcaster/Lens/Nostr/Bluesky 上对 X 有什么评价”等。无论用户只是简单地说“查看 Farcaster”或“在 Lens 上查找 [主题]”，都应使用此技能来完成相关的去中心化社交研究任务。
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - deso-ag
    install:
      - id: npm
        kind: npm
        package: deso-ag
        global: true
        bins:
          - deso-ag
        label: "Install deso-ag CLI (npm)"
---

# deso-research

使用 [deso-ag](https://www.npmjs.com/package/deso-ag) 在去中心化社交网络中研究和分析内容。

**deso-ag** 是一个命令行工具（CLI），它可以汇总来自 Farcaster、Lens、Nostr 和 Bluesky 的帖子。该工具提供搜索、趋势分析、术语提取和频道浏览功能，并支持专为 AI 代理设计的 `compact` 输出格式。

## 先决条件

### 检查安装

如果系统中没有 `deso-ag`，请先安装它：

**安装命令：**  
`npm install -g deso-ag`

### API 密钥（可选）

**deso-ag** 在没有 API 密钥的情况下也能正常运行**，因为 Lens、Nostr 和 Bluesky 的趋势分析功能都不需要密钥。不过，使用以下环境变量可以访问更多网络：

| 变量                | 可访问的网络            | 获取方式                          |
|------------------|------------------|-------------------------------------------|
| `NEYNAR_API_KEY`       | Farcaster 的搜索和趋势分析功能 | 在 neynar.com 上免费获取                   |
| `BLUESKY_IDENTIFIER` | Bluesky 的搜索功能       | 使用您的用户名（例如：user.bsky.social）             |
| `BLUESKY_APP_PASSWORD` | Bluesky 的应用密码       | 在 bsky.app/settings/app-passwords 中设置             |

如果没有相应的 API 密钥，相关网络将被自动跳过，其他功能仍可正常使用。

在运行命令之前，请先确认可访问的网络有哪些。

## 核心工作流程

### 1. 搜索内容

使用 `search` 命令查找关于特定主题的帖子。为确保数据能被 AI 代理顺利处理，请务必使用 `--format compact` 选项。

### 2. 查看热门内容

使用 `trending` 命令查看当前最受欢迎的内容。

### 3. 提取讨论主题

使用 `terms` 命令提取讨论最多的主题（结果会按照互动次数进行排序）。

### 4. 浏览 Farcaster 频道

### 输出处理

对于搜索和趋势分析命令，**务必使用 `--format compact`** 选项。这种格式返回的 JSON 数据结构简洁，便于 AI 代理进行分析：

`score` 字段的计算方式为：`点赞数 + 转发数 × 2 + 评论数`，可用于排序。

对于 `terms` 命令，使用 `--format json` 选项可获取结构化的术语频率数据。

## 分析指南

收集数据后，需对结果进行归纳和分析，切勿直接将原始 JSON 数据提供给用户：

1. **总结整体情况**：共找到了多少帖子，分布在哪些网络中，时间范围是什么？
2. **突出热门内容**：展示互动次数最高的帖子，包括作者、来源和简要概述。
3. **识别主题**：将相关帖子归类并提取共同的主题线索。
4. **提供互动背景**：分析哪些内容最受用户欢迎及其原因。
5. **提供原始链接**：提供帖子的链接，方便用户直接访问。

只有在用户明确要求跨网络比较时，才进行跨网络的数据分析。

### 分析示例输出

## 命令参考

| 命令            | 功能                        | 默认排序方式       | 默认输出格式       |
|------------------|------------------|------------------|-------------------|
| `search [查询内容]`     | 查找关于特定主题的帖子            | 相关性         | markdown          |
| `trending`       | 查看当前热门内容                | 互动次数         | summary         |
| `terms`         | 提取热门讨论术语                |              |                |
| `channels`       | 浏览 Farcaster 频道                |              |                |

### 常用选项

| 选项            | 缩写            | 可选值          | 默认值           |
|------------------|------------------|------------------|-------------------|
| `--sources`       | `-s`            | farcaster,lens,nostr,bluesky   | all            |
| `--timeframe`      | `-t`            | 24h, 48h, week       | 24h            |
| `--format`       | `-f`            | json, markdown, summary, compact | json           |
| `--limit`        | `-l`            | 任意正整数        | 25              |
| `--sort`        | `-o`            | 互动次数, 最新, 相关性     | engagement, recent, relevance |
| `--channel`      | `-c`            | 频道 ID（仅限 Farcaster）    | none            |
| `--top`         | `-n`            | 任意正整数（仅限术语）     | 3              |

有关完整的命令参考、输出格式和库使用说明，请参阅 `references/command-reference.md`。

## 错误处理

- 如果系统找不到 `deso-ag`，请安装它：`npm install -g deso-ag`
- 如果某个网络没有返回结果，可能是缺少 API 密钥——请告知用户。
- Nostr 的响应可能较慢或不稳定——如果超时，请尝试重新请求。
- 如果遇到请求速率限制错误，请告知用户，并建议他们在高负载情况下自行搭建相应的基础设施。