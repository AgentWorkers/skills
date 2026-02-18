---
name: feed-diet
version: 0.1.1
description: 审核您在 HackerNews (HN) 和 RSS 源中的信息摄入情况——提供包含分类统计、ASCII 图表以及个性化建议的精美报告。
author: CacheForge
tags: [productivity, reading, analysis, hacker-news, rss, information-diet, discord, discord-v2]
---
# 🍽️ 信息摄入与阅读习惯管理

审核您的信息摄入情况，并获得一份详细的报告，展示您实际阅读的内容。

## 触发条件

当用户提及以下内容时，该功能将被激活：
- “feed diet”（信息摄入管理）
- “information diet”（信息摄入）
- “audit my feeds”（审核我的阅读源）
- “what am I reading”（我在读什么）
- “analyze my HN”（分析我的 Hacker News 阅读习惯）
- “reading habits”（阅读习惯）
- “content diet”（内容摄入）
- “feed report”（阅读报告）

## 使用说明

### 审核模式（默认模式）

1. **确定数据来源。** 请用户提供以下信息之一：
   - 一个 **Hacker News 用户名**（例如：tosh）
   - 一个包含 RSS 订阅源的 **OPML 文件** 路径

2. **获取内容。** 运行相应的获取脚本：
   ```bash
   # For HN:
   bash "$SKILL_DIR/scripts/hn-fetch.sh" USERNAME 100
   
   # For OPML:
   bash "$SKILL_DIR/scripts/opml-parse.sh" /path/to/feeds.opml
   ```

3. **对内容进行分类。** 将获取到的内容传递给分类器进行处理：
   ```bash
   cat items.jsonl | bash "$SKILL_DIR/scripts/classify.sh" > classified.jsonl
   ```
   分类器会使用大型语言模型（LLM，前提是设置了 ANTHROPIC_API_KEY 或 OPENAI_API_KEY）；如果没有设置，则使用关键词匹配进行分类。

4. **生成报告。** 运行主处理脚本：
   ```bash
   bash "$SKILL_DIR/scripts/feed-diet.sh" audit --hn USERNAME --limit 100
   ```

5. **向用户展示报告。** 报告以 Markdown 格式呈现，可直接在浏览器中查看。

### 摘要模式（每周精选阅读）

当用户希望根据自身目标筛选阅读内容时，可以使用该模式：
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" digest --hn USERNAME --goal "systems programming, distributed systems" --days 7
```

### 快速参考

| 命令 | 描述 |
|---------|-------------|
| `feed-diet audit --hn USER` | 为 Hacker News 用户提供全面的阅读习惯审计报告 |
| `feed-diet audit --opml FILE` | 从 RSS 订阅源获取内容并生成审计报告 |
| `feed-diet digest --hn USER --goal "X"` | 根据用户目标筛选后的每周阅读摘要 |

### 对机器人的提示：

- **保持对话式交流。** 在展示报告后，可以提出一些建议，例如：“看起来您主要阅读新闻类内容，需要推荐一些更偏向技术的阅读资源吗？”
- 如果用户表现出对筛选阅读内容的兴趣，建议使用摘要模式。
- **报告本身非常重要。** 不要对其进行总结，而是完整地展示给用户；这份报告非常适合截图分享。
- 如果分类结果不准确，请提醒用户设置 LLM API 密钥以提高分类的准确性。

### Discord v2 交付模式（OpenClaw v2026.2.14+）

当对话在 Discord 频道中进行时：
- 首先发送一份简洁的摘要（主要阅读类别、内容多样性评分以及前 2 个推荐内容），然后询问用户是否需要查看完整报告。
- 确保第一条消息的字数控制在 1200 字以内，并避免在首条消息中展示过于复杂的类别列表。
- 如果支持 Discord 的交互功能，可以提供以下操作选项：
  - `Show Full Diet Report`（查看完整报告）
  - `Generate Weekly Digest`（生成每周摘要）
  - `Show Recommendations`（查看推荐内容）
- 如果不支持这些功能，可以用编号列表的形式提供相同的信息。
- 在分享长报告时，每条消息的长度应控制在 15 行以内。

## 参考文件

- `scripts/feed-diet.sh` — 主处理脚本
- `scripts/hn-fetch.sh` — 用于获取 Hacker News 内容的脚本
- `scripts/opml-parse.sh` — OPML/RSS 订阅源解析脚本
- `scripts/classify.sh` — 批量内容分类脚本（使用大型语言模型）
- `scripts/common.sh` — 公共工具和格式化脚本

## 示例

### 示例 1：Hacker News 阅读习惯审计

**用户：** “审核我的 Hacker News 阅读习惯——我的用户名是 tosh”

**机器人执行操作：**
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" audit --hn tosh --limit 50
```

**输出：** 一份包含类别统计、热门阅读内容、意外发现以及推荐内容的完整 Markdown 报告。

### 示例 2：每周阅读摘要

**用户：** “给我一份与我的编译器和编程语言相关的内容摘要”

**机器人执行操作：**
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" digest --hn tosh --goal "compilers, programming languages, parsers" --days 7
```

**输出：** 根据用户需求，筛选出的 10-20 篇相关阅读内容的列表。

### 示例 3：RSS 订阅源审计

**用户：** “这是我的 OPML 文件，请告诉我我的阅读内容构成是什么”

**机器人执行操作：**
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" audit --opml /path/to/feeds.opml
```