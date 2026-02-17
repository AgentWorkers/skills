---
name: cinema_insider_top10
description: 利用先进的AI聚合和交叉引用技术，对电影及电视行业的十大新闻进行了专业的分析总结。
tags: cinema, movies, tv, production, Hollywood, analytics
---
# Cinema Insider Top-10 技能

该技能通过汇总、去重和分析来自国际顶级新闻来源的信息，为电影和电视行业提供高级别的情报。

## 目标
根据用户请求（例如：“电影新闻”），系统需要从精选的 RSS 源中收集新闻，进行跨来源验证，并提供一份按重要性排名的前 10 项行业事件简报。

## 精选的新闻来源
1. **Variety** (http://variety.com/feed/) - 专注于商业和制作方面的新闻。
2. **Deadline Hollywood** (https://deadline.com/feed/) - 实时突发新闻。
3. **The Hollywood Reporter** (https://www.hollywoodreporter.com/c/movies/feed/) - 深度报道行业动态。
4. **ComingSoon.net**, **Collider**, **Screen Rant**, **ScreenCrush**, **LRMonline**, **Entertainment Weekly**, **TV Insider**, **IMP Awards**.

## 指令与逻辑
- **验证与去重**：如果同一条新闻出现在多个来源中，将其所有细节整合成一条高质量的新闻条目，避免重复报道同一事件。
- **深入分析**：对于重要的“突发新闻”（如重大选角、制片厂合作或导演任命），使用 `web_search` 工具收集额外的背景信息、制作时间线或历史意义。
- **分类**：将每条新闻归类为“制作”、“商业”、“选角”或“营销”。
- **视觉呈现**：对于具有高度视觉冲击力的新闻（如新预告片发布或海报曝光），使用 `browser` 工具捕捉并展示预览内容（如适用）。
- **排名**：根据新闻对行业的影响程度进行排序，将制作和商业策略相关的新闻置于预告片及一般娱乐新闻之前。

## 格式规范
- **标题**：简洁明了且专业。
- **分析说明**：简要解释这条新闻对行业专业人士的重要性。
- **来源信息**：提供直接链接，并说明该新闻是否得到了多个顶级媒体的验证。
- **输出语言**：根据用户偏好的语言进行翻译，确保翻译内容与原文保持一致。

## 使用的工具
- `web_fetch`：用于解析主要的 RSS 源。
- `web_search`：用于跨来源验证、查询突发新闻并补充详细信息。
- `browser`：用于查看新闻来源的视觉内容并捕捉媒体预览。
- `LLM Reasoning`：用于总结新闻内容、进行重要性排序和去重处理。