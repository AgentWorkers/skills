---
name: content-gap-analysis
version: "3.0.0"
description: '当用户提出以下问题时，应使用此技能：  
“我有哪些知识盲点？”、“我遗漏了哪些内容？”、“需要涵盖哪些主题？”、“有哪些内容创作的机会？”、“竞争对手在哪些方面有我尚未涉及的内容？”、“我的竞争对手覆盖了哪些我尚未涉及的主题？”或“我的内容存在哪些不足之处？”  
该技能通过识别竞争对手所涵盖但您尚未涉及的主题和关键词，来发现内容创作的机会，并揭示您内容策略中的潜在空白和战略缺口。  
如需更全面的竞争情报分析，请参阅“竞争对手分析”（Competitor-Analysis）；如需进行一般的关键词挖掘，请参阅“关键词研究”（Keyword-Research）。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: AHREFS_API_KEY
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - content gaps
    - content opportunities
    - topic analysis
    - content strategy
    - competitive content
    - content-gaps
    - topic-gaps
    - missing-content
    - content-opportunities
    - competitive-gap
    - topic-coverage
    - editorial-calendar
    - content-strategy
  triggers:
    - "find content gaps"
    - "what am I missing"
    - "topics to cover"
    - "content opportunities"
    - "what do competitors write about"
    - "untapped topics"
    - "content strategy gaps"
    - "what topics am I missing"
    - "they cover this but I don't"
    - "where are my content blind spots"
---
# 内容差距分析

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能的安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../keyword-research/) · [竞争对手分析](../competitor-analysis/) · [SERP分析](../serp-analysis/) · **内容差距分析**

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [架构标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪工具](../../monitor/rank-tracker/) · [反向链接分析工具](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威度审核工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该技能通过分析网站内容与竞争对手内容之间的差距，帮助识别内容创作的机会，发现缺失的主题、未被利用的关键词以及值得创作的内容类型。

## 适用场景

- 规划内容策略和编辑计划
- 寻找能够快速见效的内容创作机会
- 了解竞争对手在哪些方面表现优于你
- 发现你所在领域中尚未被充分覆盖的主题
- 扩展到相关主题领域
- 确定内容创作的优先级
- 发现竞争对手忽略的地理定位相关机会

## 功能介绍

1. **关键词差距分析**：找出竞争对手排名靠前但你的网站尚未覆盖的关键词。
2. **主题覆盖范围分析**：识别需要补充内容的主题领域。
3. **内容格式差距**：揭示缺失的内容类型（如视频、教程、指南等）。
4. **受众需求分析**：将差距与受众的阅读路径相匹配。
5. **地理定位机会识别**：发现可以通过人工智能回答的相关主题。
6. **优先级排序**：根据影响力和所需工作量对差距进行排序。
7. **内容计划制定**：制定填补这些差距的内容创作计划。

## 使用方法

### 基本差距分析

```
Find content gaps between my site [URL] and [competitor URLs]
```

```
What content am I missing compared to my top 3 competitors?
```

### 针对特定主题的分析

```
Find content gaps in [topic area] compared to industry leaders
```

```
What [content type] do competitors have that I don't?
```

### 以受众为中心的分析

```
What content gaps exist for [audience segment] in my niche?
```

## 数据来源

> 有关工具类别的更多信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接了以下工具时：**
- **SEO工具** + **搜索分析工具** + **数据分析工具** + **AI监控工具**：
  可自动获取你网站的内容清单（包括索引页面、每页流量、关键词排名）、竞争对手的内容数据（关键词排名、热门页面、反向链接数量），以及AI提供的引用数据。关键词重叠分析和差距识别可以自动化完成。

**仅使用手动数据时：**
  请用户提供以下信息：
  - 你的网站URL和内容清单（包含已发布的内容及其主题）
  - 3-5个竞争对手的网站URL
  - 你当前的网站流量和关键词表现数据（如有）
  - 你网站内容的优势与劣势
  - 行业背景和业务目标

  使用提供的数据开始全面分析。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供。

## 使用说明

当用户请求进行内容差距分析时，请按照以下步骤操作：

1. **定义分析范围**
   明确分析的具体参数：
   ```markdown
   ### Analysis Parameters
   
   **Your Site**: [URL]
   **Competitors to Analyze**: [URLs or "identify for me"]
   **Topic Focus**: [specific area or "all"]
   **Content Types**: [blogs, guides, tools, videos, or "all"]
   **Audience**: [target audience]
   **Business Goals**: [traffic, leads, authority, etc.]
   ```

2. **审核现有内容**
   记录网站的总索引页面数、内容类型及主题分类、表现最佳的内容，以及内容的优势与劣势。

3. **分析竞争对手内容**
   对每个竞争对手，记录其内容量、每月流量、内容类型分布、与你的内容相比的覆盖范围，以及他们独有的内容。

4. **识别关键词差距**
   找出竞争对手排名靠前但你的网站尚未覆盖的关键词。将这些关键词分为三类：高优先级（高流量、易于实现）、快速见效（低流量、低难度）和长期目标（高流量、高难度）。同时进行关键词重叠分析。

5. **绘制主题覆盖范围对比图**
   制作一个涵盖所有竞争对手的主题覆盖范围对比表。对于每个缺失的主题领域，记录其业务相关性、竞争对手的覆盖情况、机会大小、子主题，以及推荐的创作方向。

6. **识别内容格式差距**
   比较竞争对手和行业平均水平在内容格式上的差异（如指南、教程、对比分析、案例研究、工具、模板、视频、信息图、研究报告等）。评估每种格式的创作难度和预期效果。

7. **分析地理定位/人工智能相关差距**
   识别竞争对手获得了AI引用但你的网站尚未覆盖的主题。记录缺失的问答内容、定义/解释性内容以及相关对比内容。根据传统SEO价值和地理定位价值对每个差距进行评分。

8. **与受众阅读路径对齐**
   比较你们网站在受众阅读路径的各个阶段（认知、考虑、决策、留存）的覆盖情况与竞争对手的平均水平。详细说明每个阶段的差距。

9. **确定优先级并制定行动计划**
   制定最终报告，包括：执行摘要、优先级差距列表（一级快速见效项、二级战略性内容、三级长期目标）、内容创作计划以及成功指标。
   > **参考资料**：详细报告模板请参见 [references/analysis-templates.md](./references/analysis-templates.md)。

## 验证要点

### 输入验证
- 你的内容清单完整或提供了具有代表性的样本。
- 已识别出至少2-3个竞争对手的网站URL。
- 分析范围已明确（具体主题或全面分析）。
- 业务目标和优先级已明确。

### 输出验证
- 每条建议都基于具体的数据点（而非泛泛而谈）。
- 差距分析是对比类似的内容（同类主题之间的对比）。
- 优先级排序基于可衡量的标准（如内容量、难度、业务契合度）。
- 内容计划将差距与实际的时间框架对应起来。
- 每个数据来源都明确标注（来自SEO工具、数据分析工具、AI监控工具或用户提供的数据）。

## 示例

> **参考示例**：请参阅 [references/example-report.md](./references/example-report.md)，了解如何分析SaaS营销博客与HubSpot和Drift之间的内容差距。

## 高级分析方法

### 竞争对手群体对比分析

```
Compare our topic cluster coverage for [topic] vs top 5 competitors
```

### 时间序列差距分析

```
What content have competitors published in the last 6 months that we haven't covered?
```

### 基于用户意图的差距分析

```
Find gaps in our [commercial/informational] intent content
```

## 成功技巧

1. **专注于可操作的差距**：并非所有差距都值得填补。
2. **考虑自身资源**：根据执行能力来安排优先级。
3. **质量优先于数量**：填补5个高质量的内容比填补20个低质量的内容更有价值。
4. **跟踪效果**：衡量填补差距的实际效果。
5. **定期更新**：随着竞争对手发布新内容，差距也会发生变化。
6. **关注地理定位相关机会**：不要只针对传统搜索进行优化。

## 参考资料

- [分析模板](./references/analysis-templates.md) — 每个分析步骤的详细模板（内容清单、竞争对手内容、关键词差距、主题差距、格式差距、地理定位差距、受众旅程分析、优先级报告）
- [差距分析框架](./references/gap-analysis-frameworks.md) — 内容审核矩阵、受众路径映射和差距优先级评分方法
- [示例报告](./references/example-report.md) — 分析SaaS营销博客与HubSpot和Drift之间差距的完整示例

## 相关技能

- [关键词研究](../keyword-research/) — 深入挖掘关键词差距
- [竞争对手分析](../competitor-analysis/) — 了解竞争对手的策略
- [SEO内容撰写工具](../../build/seo-content-writer/) — 创建用于填补差距的内容
- [内容更新工具](../../optimize/content-refresher/) — 更新现有内容以填补发现的差距
- [内部链接优化工具](../../optimize/internal-linking-optimizer/) — 识别并修复内部链接问题
- [反向链接分析工具](../../monitor/backlink-analyzer/) — 分析反向链接的潜在机会
- [内存管理工具](../../cross-cutting/memory-management/) — 随时间跟踪内容差距的变化