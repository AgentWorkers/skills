# SEO 分析器技能

该工具用于分析网站和页面的 SEO 相关因素，是 Ahrefs、SEMRush 等付费工具的免费替代品。

## 功能概述

- **页面 SEO 分析**：可分析任何 URL 的元标签、标题和内容结构。
- **关键词建议**：根据主题提供关键词建议。
- **竞争对手分析**：比较不同页面的 SEO 指标。
- **站点审计**：检查常见的 SEO 问题。
- **排名检测**：查询页面在搜索结果中的排名情况。

## 使用方法

```
/seo-analyze <url> - Full page analysis
/seo-keywords <topic> - Get keyword ideas
/seo-compare <url1> vs <url2> - Compare two pages
/seo-audit <url> - Check for technical issues
```

## 所使用的工具

- `web_fetch`：用于获取页面内容以供分析。
- `web_search`：用于查询页面的排名和关键词信息。
- `browser`：用于需要 JavaScript 渲染的动态页面。

## 系统要求

- 需要 Brave Search API 来获取关键词和排名数据。
- 可直接分析大多数静态页面。
- 对于单页应用（SPA）或动态网站，需要使用浏览器进行解析。

## 输出格式

输出内容包括：
- 元标题和描述（附带优化建议）
- 标题层级（H1-H6）
- 单词数量和可读性
- 内部/外部链接
- 图片（检查图片的替代文本）
- 发现的技术问题
- 有潜力的关键词

## 可替代的付费工具

- Ahrefs（每月费用 99-999 美元）
- SEMrush（每月费用 119-449 美元）
- Moz Pro（每月费用 99 美元）
- Ubersuggest（每月费用 29-199 美元）

该工具能够免费提供 80% 的基本 SEO 分析功能。