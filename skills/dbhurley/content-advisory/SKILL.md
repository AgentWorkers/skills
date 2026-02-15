---
name: content-advisory
description: 从 Kids-In-Mind 网站查询电影和电视节目的详细内容评级（包括性内容、裸露、暴力/血腥场面以及语言使用情况）。
homepage: https://kids-in-mind.com
metadata: { "clawdbot": { "emoji": "🎬", "requires": { "bins": ["uv"] } } }
---

# 内容建议（Content Advisory）

提供电影和电视节目的详细家长内容评级信息。这些评级不仅涵盖了MPAA的简单分类，还详细列出了可能引起不适的内容。

## 主要功能

- **详细评级**：性/裸露、暴力/血腥、语言等方面，采用0-10的评分标准
- **内容详情**：对可能引起不适的内容进行准确描述
- **物质使用**：涉及酒精、毒品、吸烟等场景的描述
- **讨论话题**：家长可以讨论的相关主题
- **主题/寓意**：电影的整体主题或寓意
- **缓存**：结果会本地缓存，以避免重复查询

## 命令

### 查找电影
```bash
uv run {baseDir}/scripts/content_advisory.py lookup "The Batman"
uv run {baseDir}/scripts/content_advisory.py lookup "Inside Out" --year 2015
uv run {baseDir}/scripts/content_advisory.py lookup "Oppenheimer" --json
```

### 搜索电影标题
```bash
uv run {baseDir}/scripts/content_advisory.py search "batman"
uv run {baseDir}/scripts/content_advisory.py search "pixar" --limit 10
```

### 清除缓存
```bash
uv run {baseDir}/scripts/content_advisory.py clear-cache
```

## 输出示例
```
🎬 The Batman (2022) | PG-13

📊 CONTENT RATINGS
   Sex/Nudity:    2 ▓▓░░░░░░░░
   Violence/Gore: 7 ▓▓▓▓▓▓▓░░░
   Language:      5 ▓▓▓▓▓░░░░░

📋 CATEGORY DETAILS
   Sex/Nudity: A man and woman kiss...
   Violence:   Multiple fight scenes with punching...
   Language:   15 uses of profanity including...

💊 SUBSTANCE USE
   Alcohol consumed at party scenes...

💬 DISCUSSION TOPICS
   Vigilantism, revenge, grief, corruption

📝 MESSAGE
   Justice requires restraint, not vengeance.
```

## 评分标准

| 评分 | 等级    | 描述                         |
| ----- | -------- | --------------------------- |
| 0-1   | 无      | 该类别中无不适内容                |
| 2-3   | 轻微     | 简短的非露骨内容                   |
| 4-5   | 中等     | 包含一些不适内容                   |
| 6-7   | 严重     | 包含大量不适内容                   |
| 8-10  | 高度不适 | 包含大量露骨内容                   |

## 数据来源

内容评级信息来自 [Kids-In-Mind.com](https://kids-in-mind.com)，这是一家自1992年以来一直从事电影评级的独立非营利组织。他们不提供年龄分级，但会提供客观的描述，帮助家长做出明智的决策。

## 使用示例

**“《蝙蝠侠》适合我12岁的孩子观看吗？”**
```bash
uv run {baseDir}/scripts/content_advisory.py lookup "The Batman"
```

**“《奥本海默》的暴力程度如何？”**
```bash
uv run {baseDir}/scripts/content_advisory.py lookup "Oppenheimer"
# Check the Violence/Gore rating and details
```

**“查找适合家庭观看的电影（评级较低的作品）”
```bash
uv run {baseDir}/scripts/content_advisory.py search "disney" --limit 20
# Review results for low-rated titles
```

## 数据存储

缓存数据存储在 `~/.clawdbot/content-advisory/cache.json` 文件中，以减少重复查询。

## 注意事项

- 结果数据来自Kids-In-Mind.com的抓取
- 并非所有电影都经过了评级——主要针对影院上映的电影
- 可以清除缓存以强制重新查询数据
- 如果您认为他们的服务很有价值，请支持Kids-In-Mind。