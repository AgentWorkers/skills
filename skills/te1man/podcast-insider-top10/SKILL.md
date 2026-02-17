---
name: podcast_insider_top10
description: 专业分析汇总了来自全球顶级媒体的播客行业十大新闻、趋势及商业洞察。
tags: podcasting, audio, media, industry, analytics
---
# Podcast Insider：十大必备技能

该技能通过汇总、分析并整合来自全球领先播客机构的新闻，为播客行业提供全面的情报。

## 目标
根据用户需求（例如：“播客行业新闻”），系统需从指定的RSS源中收集信息，分析市场动态、技术变革及平台更新，并整理出一份精选的十大新闻简报。

## 精选信息来源：
1. **Podnews Daily** (https://podnews.net/feed) - 行业权威的每日新闻来源。
2. **The Podcast Sessions** (https://thepodsessions.com/feed/) - 行业洞察与访谈。
3. **Discover Pods** (https://discoverpods.com/feed/) - 播客评论与行业趋势分析。
4. **Pacific Content** (https://pacific-content.com/feed/) - 品牌内容与策略研究。
5. **Podcaster News** (https://podcasternews.com/feed/) - 全球播客新闻。
6. **Business of Podcasting** (https://www.thepodcasthost.com/business-of-podcasting/feed) - 播客盈利模式与行业发展。
7. **Buzzsprout Blog** (https://www.buzzsprout.com/blog.rss) - 以创作者为中心的新闻与趋势报道。
8. **Spreaker Blog** (https://blog.spreaker.com/feed/) - 平台更新与技术解析。
9. **Bingeworthy** (https://bingeworthy.substack.com/feed) - 高质量内容评论与行业背景分析。
10. **The Audio Insurgent** (https://audioinsurgent.substack.com/feed) - 行业资深人士的战略分析。
11. **The Squeeze** (https://www.thisisthesqueeze.com/feed) - 深度行业报道与调查性文章。

## 操作步骤与逻辑：
- **验证与整合**：对比多个来源中的重要新闻，形成统一、详细的报道内容。
- **趋势识别**：关注盈利模式、音频技术整合以及平台政策变化等重复出现的主题。
- **分类**：将新闻分为“市场动态”、“平台更新”、“内容策略”或“技术创新”等类别。
- **深入研究**：对于重大行业变革（如Spotify的收购事件或重要的广告技术更新），使用`web_search`工具查找更多背景信息和历史数据。
- **重要性排序**：根据新闻对创作者和媒体所有者可能产生的影响进行排名。

## 格式规范：
- **标题**：简洁明了且专业。
- **战略分析**：简要说明该新闻对全球播客生态系统的影响。
- **来源链接**：提供原始新闻的直接链接。
- **输出语言**：根据用户设置，以用户偏好的语言呈现内容。

## 使用工具：
- `web_fetch`：用于解析RSS源和文章内容。
- `web_search`：用于跨来源对比和深入分析。
- `LLM Reasoning`：用于信息总结、分类及战略分析。