---
name: tg-channel-manager
description: >
  这是一个通用的、基于配置的内容处理引擎，适用于任何 Telegram 频道：
  - 通过 SearXNG 进行新闻搜索；
  - 支持草稿功能；
  - 允许定时发布内容；
  - 具备去重功能。
  所有频道相关的设置都通过配置文件来定义——一个配置文件即可适用于所有频道。
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: ["python3", "curl"]
      env: ["SEARXNG_URL"]
    primaryEnv: "SEARXNG_URL"
---
# TG Channel Manager

这是一个通用的内容管理系统，适用于任何 Telegram 频道。其工作流程为：**数据采集 → 草稿生成 → 人工审核 → 发布**。

所有具体配置（如主题、评分标准、样式、过滤规则等）都存储在 `config` 文件中，该脚本中没有任何硬编码的值。

## 配置

相关参数从 `openclaw.json` 文件中的 `skills.entries["tg-channel-manager"]` 部分读取：

### Telegram 配置

| 参数 | 类型 | 描述 |
|---------|------|-------------|
| `config.channelId` | 字符串 | 用于发布的 Telegram 频道 ID |
| `config.chatId` | 字符串 | 频道社区聊天室 ID（可选） |

### 限制与调度

| 参数 | 类型 | 描述 |
|---------|------|-------------|
| `config.maxPostsPerDay` | 数字 | 每天的最大发布数量 |
| `config.maxDraftsPerRun` | 数字 | 每次数据采集任务的最大草稿数量 |
| `config.timezone` | 字符串 | 时间区（IANA 格式） |
| `config.language` | 字符串 | 帖子的语言（如 ru、en 等） |
| `config.cronScoutTimes` | 字符串数组 | 数据采集任务的调度时间（cron 格式） |
| `config.cronPublisherTimes` | 字符串数组 | 发布任务的调度时间（cron 格式） |

### 内容配置

| 参数 | 类型 | 描述 |
|---------|------|-------------|
| `config.rubrics` | 数组 | 评分标准：`[{id, emoji, name}, ...]` |
| `config.searchQueries` | 字符串数组 | 用于 SearXNG 的搜索查询 |
| `config.searchInclude` | 字符串 | 需要包含的内容（过滤规则） |
| `config.searchExclude` | 字符串 | 需要排除的内容（过滤规则） |
| `config.evergreen` | 字符串数组 | 无新内容时使用的文章主题 |

### 帖子样式配置

| 参数 | 类型 | 描述 |
|---------|------|-------------|
| `config.postStyle.minChars` | 数字 | 每篇帖子的最小字符数 |
| `config.postStyle.maxChars` | 数字 | 每篇帖子的最大字符数 |
| `config.postStyle.emojiTitle` | 布尔值 | 标题前是否添加表情符号 |
| `config.postStyle.boldTitle` | 布尔值 | 标题是否加粗 |
| `config.postStyle.signature` | 字符串 | 帖子的签名 |
| `config.postStyle.newsFooter` | 字符串 | 新闻帖子的附加文本（为空表示不添加） |
| `config.postStyle.articleFooter` | 字符串 | 文章的附加文本（为空表示不添加） |

### 环境配置

| 参数 | 类型 | 描述 |
|---------|------|-------------|
| `env.SEARXNG_URL` | 字符串 | SearXNG 服务的 URL |

`{baseDir}` 表示该脚本所在的文件夹路径。

## 运行时文件

- **`content-queue.md`**：帖子队列（包含草稿和待发布的内容），位于代理的工作区，不在脚本文件夹内。
- **`content-index.json`：去重索引文件，也位于代理的工作区。

### `content-queue.md` 的条目格式

```markdown
### <number>
- **Status:** draft | pending
- **Rubric:** <emoji> <name> (from config.rubrics)
- **Topic:** <topic>
- **Source:** <url> (for news)
- **Text:**

<post text>
```

状态说明：
- **draft**：草稿状态，等待审核
- **pending**：审核通过，准备发布

发布后，该条目将从 `content-queue.md` 中删除。

## 工作流程

### 1. 数据采集（cron 任务）

执行命令：`{baseDir}/references/scout-prompt.md`

1. 通过 `$SEARXNG_URL` 执行 `config.searchQueries` 中指定的搜索查询。
2. 根据 `config.searchInclude` 和 `config.searchExclude` 进行过滤。
3. 使用 `dedup-check.py` 检查是否存在重复内容。
4. 将生成的草稿状态设置为 **draft**，并写入 `content-queue.md`。
5. 每次数据采集任务最多生成 `config.maxDraftsPerRun` 个草稿。
6. 如果未找到新内容，则从 `config.evergreen` 中选取一个主题生成新文章。

### 2. 人工审核

人工审核草稿，并将状态改为 **pending**。

### 3. 发布（cron 任务）

执行命令：`{baseDir}/references/publisher-prompt.md`

1. 读取 `content-queue.md` 中的待发布内容。
2. 选择第一条处于 **pending** 状态的帖子进行发布。
3. 根据需要选择不同的评分标准。
4. 添加 `config.postStyle.signature` 中定义的签名。
5. 通过 `message tool`（命令：`action=send, channel=telegram, target=<config.channelId>`）发布帖子。
6. 从 `content-queue.md` 中删除该条目。
7. 将发布后的帖子添加到去重索引中。
6. 每次任务最多发布 1 条帖子，每天最多发布 `config.maxPostsPerDay` 条。

## Telegram API

### 检查已发布的帖子
```
message tool (action=search, channel=telegram, target=<config.channelId>, query="keywords")
```

### 发布帖子
```
message tool (action=send, channel=telegram, target=<config.channelId>, text="post text")
```

## 去重处理

**在生成草稿之前**：必须执行去重检查。
```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --topic "topic" --links "url1" "url2"
```

**发布后**：将帖子添加到索引中。
```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --add <msgId> --topic "topic" --links "url"
```

**重建索引**（通过 Telegram 搜索功能）：
```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --rebuild --channel-id <config.channelId>
```

索引文件存储在 `<workspace>/content-index.json` 中。

## SearXNG — 新闻搜索

对于 `config.searchQueries` 中指定的每个搜索请求，执行以下操作：
```bash
curl '$SEARXNG_URL/search?q=<query>&format=json&time_range=day&language=en'
```

## 帖子格式

帖子格式由 `config.postStyle` 参数定义：

- 标题：包含表情符号（如果设置了 `emojiTitle`）；标题可能加粗（如果设置了 `boldTitle`）。
- 字数：介于 `minChars` 和 `maxChars` 之间。
- 语言：使用 `config.language` 中指定的语言。
- 签名：使用 `config.postStyle.signature`。
- 新闻帖子：包含原始来源链接及 `newsFooter`（如果有的话）。
- 文章帖子：包含 `articleFooter`（如果有的话）。
- 优先使用原始来源（如技术规范、GitHub 文档、官方博客）而非摘要。
- 所有链接均需以 `https://` 开头。
- 禁止使用任何个人数据。

## 评分标准

评分标准存储在 `config.rubrics` 中，每个评分标准的格式为 `{id, emoji, name}`。

数据采集任务会从该列表中选择合适的评分标准来生成草稿。

## 初始 Cron 任务设置

详细配置请参考 `{baseDir}/references/cron-setup.md`，其中包含 `openclaw cron add` 命令的模板。