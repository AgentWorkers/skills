---
name: daily-ai-news
description: "该工具从多个来源（包括AI新闻网站和网络搜索）收集并汇总最新的AI新闻，提供简洁的新闻摘要，并附有指向原始文章的直接链接。当用户查询“今天的AI新闻”、“AI更新”、“最新的AI发展”或表示需要“每日AI简报”时，该工具便会自动启动并开始工作。"
---

# 每日AI新闻简报

> 从多个来源汇总最新的AI新闻，并提供带有直接链接的简洁摘要

## 何时使用此技能

当用户以下情况时，可激活此技能：
- 询问当天的AI新闻或最新的AI发展动态
- 请求每日AI简报或更新
- 表示想了解AI领域的最新动态
- 询问AI行业的新闻、趋势或突破性进展
- 希望获取最近的AI公告摘要
- 说：“给我今天的AI资讯”
- 说：“AI有什么新动态”

## 工作流程概述

此技能通过4个阶段来收集、筛选、分类和呈现AI新闻：

```
Phase 1: Information Gathering
  ├─ Direct website fetching (3-5 major AI news sites)
  └─ Web search with date filters
      ↓
Phase 2: Content Filtering
  ├─ Keep: Last 24-48 hours, major announcements
  └─ Remove: Duplicates, minor updates, old content
      ↓
Phase 3: Categorization
  └─ Organize into 5 categories
      ↓
Phase 4: Output Formatting
  └─ Present with links and structure
```

## 第1阶段：信息收集

### 步骤1.1：从主要AI新闻来源获取内容

使用`mcp__web_reader__webReader`从3-5个主要的AI新闻网站获取内容：

**推荐的主要来源**（每次会话选择3-5个）：
- VentureBeat AI: https://venturebeat.com/category/ai/
- TechCrunch AI: https://techcrunch.com/category/artificial-intelligence/
- The Verge AI: https://www.theverge.com/ai-artificial-intelligence
- MIT Technology Review AI: https://www.technologyreview.com/topic/artificial-intelligence/
- AI News: https://artificialintelligence-news.com/
- AI Hub Today: https://ai.hubtoday.app/

**参数**：
- `return_format`: markdown
- `with_images_summary`: false（仅关注文本内容）
- `timeout`: 每个来源20秒

### 步骤1.2：执行带有日期过滤的网页搜索查询

使用`WebSearch`执行带有日期过滤的查询，以发现更多新闻：

**查询模板**（动态调整日期）：
```
General: "AI news today" OR "artificial intelligence breakthrough" after:[2025-12-23]
Research: "AI research paper" OR "machine learning breakthrough" after:[2025-12-23]
Industry: "AI startup funding" OR "AI company news" after:[2025-12-23]
Products: "AI application launch" OR "new AI tool" after:[2025-12-23]
```

**最佳实践**：
- 始终使用当前日期或昨天的日期作为过滤条件
- 在不同类别中执行2-3次查询
- 每次查询限制结果数量为10-15条
- 优先选择过去24-48小时内的来源

### 步骤1.3：获取完整文章

对于搜索结果中排名前10-15条最相关的文章：
- 从搜索结果中提取URL
- 使用`mcp__web_reader__webReader`获取文章的完整内容
- 这样可以确保摘要的准确性，而不仅仅是片段

## 第2阶段：内容筛选

### 筛选标准

**保留**：
- 过去24-48小时内的新闻（最好是今天的）
- 重要公告（产品发布、模型发布、研究突破）
- 行业发展（融资、合作、法规、收购）
- 技术进展（新模型、新技术、基准测试）
- 重要公司的更新（如OpenAI、Google、Anthropic等）

**删除**：
- 重复的文章（多个来源中的相同新闻）
- 较小的更新或营销性内容
- 超过3天的内容（除非非常重要）
- 与AI无关的内容或间接相关的文章

### 去重策略

当同一篇文章出现在多个来源时：
- 保留最全面的版本
- 在摘要中注明其他来源
- 优先选择权威来源（公司博客 > 新闻聚合平台）

## 第3阶段：分类

将新闻分为5个类别：

### 🔥 重要公告
- 产品发布（新的AI工具、服务、功能）
- 模型发布（GPT更新、Claude功能、Gemini能力）
- 重要公司公告（OpenAI、Google、Anthropic、Microsoft、Meta）

### 🔬 研究与论文
- 学术突破
- 来自顶级会议的新研究论文
- 新技术或方法论
- 基准测试成果

### 💰 行业与商业
- 融资轮次和投资
- 合并和收购
- 合作与协作
- 市场趋势和分析

### 🛠️ 工具与应用
- 新的AI工具和框架
- 实用的AI应用
- 开源发布
- 开发者资源

### 🌍 政策与伦理
- AI法规和政策
- 安全与伦理讨论
- 社会影响研究
- 政府倡议

## 第4阶段：输出格式

使用以下模板进行一致的输出：

```markdown
# 📰 Daily AI News Briefing

**Date**: [Current Date, e.g., December 24, 2025]
**Sources**: [X] articles from [Y] sources
**Coverage**: Last 24 hours

---

## 🔥 Major Announcements

### [Headline 1]

**Summary**: [One-sentence overview of the news]

**Key Points**:
- [Important detail 1]
- [Important detail 2]
- [Important detail 3]

**Impact**: [Why this matters - 1 sentence]

📅 **Source**: [Publication Name] • [Publication Date]
🔗 **Link**: [URL to original article]

---

### [Headline 2]

[Same format as above]

---

## 🔬 Research & Papers

### [Headline 3]

[Same format as above]

---

## 💰 Industry & Business

### [Headline 4]

[Same format as above]

---

## 🛠️ Tools & Applications

### [Headline 5]

[Same format as above]

---

## 🌍 Policy & Ethics

### [Headline 6]

[Same format as above]

---

## 🎯 Key Takeaways

1. [The biggest news of the day - 1 sentence]
2. [Second most important development - 1 sentence]
3. [An emerging trend worth watching - 1 sentence]

---

**Generated on**: [Timestamp]
**Next update**: Check back tomorrow for the latest AI news
```

## 定制选项

在提供初始简报后，提供以下定制选项：

### 1. 关注领域
“您希望我关注特定主题吗？”
- 仅限研究论文
- 产品发布和工具
- 行业新闻和融资
- 特定公司（OpenAI/Google/Anthropic）
- 技术教程和指南

### 2. 详细程度
“我希望详细到什么程度？”
- **简略**：仅显示标题（每条新闻2-3个要点）
- **标准**：摘要 + 关键点（默认）
- **详细**：包括分析和影响

### 3. 时间范围
“您希望的时间范围是什么？”
- 过去24小时（默认）
- 过去3天
- 上周
- 自定义时间范围

### 4. 格式偏好
“您希望如何组织这些内容？”
- 按类别（默认）
- 按时间顺序
- 按公司
- 按重要性

## 后续交互

### 用户：“请告诉我更多关于[文章X]的信息”
**操作**：使用`mcp__web_reader__webReader`获取完整文章，并提供详细摘要和分析

### 用户：“专家对[主题Y]有什么看法？”
**操作**：搜索专家意见、Twitter上的反应和分析文章

### 用户：“找到与[文章Z]类似的故事”
**操作**：搜索相关主题，并提供对比摘要

### 用户：“仅显示研究论文”
**操作**：过滤并重新组织输出，排除行业新闻

## 质量标准

### 验证 checklist
- 所有链接都是有效且可访问的
- 各类别中没有重复的文章
- 所有内容都有时间戳（最好是今天的）
- 摘要准确无误
- 链接指向原始来源，而非新闻聚合平台
- 来源多样化（不全部来自同一出版物）
- 平衡新闻的热度和实质内容

### 错误处理
- 如果`webReader`无法访问某个URL → 跳过该来源并尝试下一个
- 如果搜索没有结果 → 扩大时间范围或尝试不同的查询
- 如果结果太多 → 提高重要性的判断标准
- 如果内容需要付费才能访问 → 使用可用的摘录并注明限制

## 示例

### 示例1：基本请求

**用户**：“给我今天的AI资讯”

**AI响应**：
[执行4个阶段的工作流程，并按类别呈现5-10篇新闻的格式化简报]

---

### 示例2：特定时间范围的请求

**用户**：“这周AI领域有什么新动态？”

**AI响应**：
[调整日期过滤器为过去7天，呈现每周的总结]

---

### 示例3：特定主题的请求

**用户**：“有关AI研究的最新更新吗？”

**AI响应**：
[专注于“研究与论文”类别，包括最近的研究论文和突破性进展]

---

### 示例4：深入探讨

**用户**：“请告诉我更多关于GPT-5的公告”

**AI响应**：
[获取完整文章，提供详细摘要，并提供专家意见]

## 额外资源

有关新闻来源的完整列表、搜索查询和输出模板，请参考：
- `references/news_sources.md` - 完整的AI新闻来源数据库
- `references/search_queries.md` - 按类别划分的搜索查询模板
- `references/output_templates.md` - 替代输出格式模板