---
description: 从日本的新闻来源中获取并汇总最热门的新闻，将其整理成每日分类、易于阅读的新闻摘要。
---

# 日本新闻摘要

该功能用于获取、分类并总结日本的热门新闻。

**适用场景**：当用户请求日本新闻、每日新闻摘要或了解日本当前发生的事情时。

**触发词**："Japan news", "日本のニュース", "news digest", "today's news Japan"

## 功能要求

- 需要使用 `web_search` 和 `web_fetch` 工具
- 无需 API 密钥

## 使用步骤

1. **获取新闻**：执行 2-3 次搜索：
   ```
   web_search("Japan news today", country="JP", count=10)
   web_search("日本 ニュース 今日", search_lang="ja", count=10)
   ```
   - 对于特定主题：
     - 科技/人工智能：`"日本 AI テクノロジー 最新"`
     - 商业：`"日本 経済 ビジネス"`
     - 政治：`"日本 政治 国会"`
   
2. **使用 `web_fetch` 阅读值得关注的文章**：挑选出 5-8 篇最有趣或最重要的文章。

3. **分类新闻**：
   - 🏛️ 政治与社会
   - 💰 商业与经济
   - 🤖 科技与人工智能
   - 🌏 国际事务
   - 🎌 文化与娱乐

4. **输出格式**：
   ```
   ## 📰 Japan News Digest
   **Date:** YYYY-MM-DD

   ### 🔥 Top Story
   **[Headline](URL)**
   2-3 sentence summary. Key takeaway.

   ### 🤖 Technology
   **[Headline](URL)**
   Summary. (Source: NHK)

   ### 💰 Economy
   **[Headline](URL)**
   Summary. (Source: 日経)

   ---
   📌 = Important | 🔥 = Breaking | 💡 = Interesting
   *Sources: NHK, 日経, 朝日, Reuters Japan*
   ```

5. **可选**：如用户要求，可将新闻摘要保存到 `~/news-digests/YYYY-MM-DD.md` 文件中。

## 使用指南

- 默认输出语言为日语摘要；如需英文摘要，请另行指定。
- 根据相关性对文章进行排序：🔥 紧急新闻 > 📌 重要新闻 > 💡 有趣新闻
- 必须注明文章来源
- 不得提取需要付费才能阅读的内容，仅从可预览的文本中进行总结
- 每份新闻摘要包含 5-8 篇文章（篇幅适中）

## 特殊情况处理

- **没有重要新闻**：可包含热门话题或有趣的专题内容。
- **存在重复文章**：合并多个来源的报道，并注明所有出处。
- **用户请求英文摘要**：使用英文查询并生成英文摘要。
- **用户指定特定主题**：仅搜索和展示该主题的相关内容。