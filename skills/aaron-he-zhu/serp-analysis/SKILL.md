---
name: serp-analysis
version: "3.0.0"
description: '此技能适用于用户提出以下请求时：分析搜索结果（analyze search results）、进行搜索引擎结果页面（SERP）分析（SERP analysis）、了解哪些页面获得了较高的排名（what ranks for）、研究SERP的展示特点（SERP features）、探究某个页面为何能获得高排名（why does this page rank）、查找针对特定查询显示在首页的内容（what is on page one for this query）、识别针对某个关键词排名较高的网站（who ranks for this keyword），或询问Google针对该关键词展示了哪些内容（what does Google show for）。该技能用于分析搜索引擎的结果页面（SERPs），以理解排名背后的因素、SERP的展示特点、用户搜索意图的模式，以及与人工智能相关的触发机制（AI overview triggers）。对于跟踪页面的长期排名变化，可参考rank-tracker工具；如需进行关键词挖掘（keyword discovery），请参阅keyword-research相关内容。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
allowed-tools: WebFetch
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: AHREFS_API_KEY
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - serp
    - search results
    - ranking factors
    - serp features
    - ai overviews
    - featured snippets
    - search intent
    - serp-features
    - featured-snippet
    - google-ai-overview
    - ai-overview
    - people-also-ask
    - knowledge-panel
    - serp-composition
    - position-zero
    - serp-intent
  triggers:
    - "analyze search results"
    - "SERP analysis"
    - "what ranks for"
    - "SERP features"
    - "why does this page rank"
    - "featured snippets"
    - "AI overviews"
    - "what's on page one for this query"
    - "who ranks for this keyword"
    - "what does Google show for"
---
# SERP分析


> **[SEO与地理技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理相关技能 · 全部技能的安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`


<details>
<summary>浏览全部20项技能</summary>


**研究** · [关键词研究](../keyword-research/) · [竞争对手分析](../competitor-analysis/) · **SERP分析** · [内容差距分析](../content-gap-analysis/)


**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构标记生成器](../../build/schema-markup-generator/)


**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容复习工具](../../optimize/content-refresher/)


**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)


**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)


</details>

该技能用于分析搜索引擎结果页面（SERP），以了解哪些内容有助于提高排名、哪些SERP元素会被展示出来，以及哪些因素会触发AI生成的答案。在创建内容之前，先了解这些信息是非常重要的。


## 何时使用该技能

- 在为目标关键词创建内容之前
- 了解为什么某些页面能排在第1位
- 识别SERP元素中的优化机会（如特色片段、PAA等）
- 分析AI生成的答案的模式
- 更准确地评估关键词的难度
- 根据排名情况规划内容格式
- 确定特定查询的排名因素


## 该技能的功能

1. **SERP组成分析**：展示结果页面上的所有元素
2. **排名因素识别**：揭示顶级结果排名的原因
3. **SERP元素映射**：识别特色片段、PAA、知识面板等元素
4. **AI生成答案分析**：分析AI生成答案的时间和方式
5. **意图信号检测**：从SERP内容中判断用户意图
6. **内容格式建议**：根据SERP情况提供最佳内容格式建议
7. **难度评估**：评估内容的实际排名潜力


## 使用方法

### 基础SERP分析


```
Analyze the SERP for [keyword]
```


```
What does it take to rank for [keyword]?
```


### 特定元素分析


```
Analyze featured snippet opportunities for [keyword list]
```


```
Which of these keywords trigger AI Overviews? [keyword list]
```


### 竞争对手SERP分析


```
Why does [URL] rank #1 for [keyword]?
```


## 数据来源

> 有关工具类别的更多信息，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当连接了~~SEO工具 + ~~搜索控制台 + ~~AI监控工具时：**
可以自动获取目标关键词的SERP快照，提取排名页面的指标（域名权威度、反向链接、内容长度），提取SERP元素数据，并使用~~AI监控工具检查AI生成答案的情况。还可以自动获取历史SERP变化数据以及移动设备与桌面设备的差异。



**仅使用手动数据时：**
请用户提供以下信息：
1. 需要分析的目标关键词
2. SERP截图或搜索结果的详细描述
3. 前10名排名页面的URL
4. 搜索位置和设备类型（移动设备/桌面设备）
5. 关于SERP元素的任何观察结果（如特色片段、PAA等）

使用提供的数据进行完整分析。在输出结果中注明哪些指标来自自动化收集，哪些来自用户提供的数据。


## 使用说明

当用户请求SERP分析时：

1. **理解查询意图**
   如有需要，明确以下信息：
   - 需要分析的目标关键词
   - 搜索位置/语言
   - 设备类型（移动设备/桌面设备）
   - 关于SERP的具体问题


2. **绘制SERP组成图**
   记录结果页面上出现的所有元素：AI生成的内容、广告、特色片段、自然搜索结果、PAA、知识面板、图片结果、购物结果、新闻结果、站点链接及相关搜索结果。


3. **分析排名靠前的页面**
   对于前10名结果中的每个页面，记录以下信息：URL、域名、域名权威度、内容类型、字数、发布/更新日期、页面元素（标题、元描述、H1标签、URL结构）、内容结构（标题、图片、表格、常见问题解答）、预估的排名指标（反向链接、引用域名），以及该页面排名的原因。


4. **识别排名规律**
   分析前5名结果中的共同特征：字数、域名权威度、反向链接数量、内容新鲜度、HTTPS支持情况、移动设备优化情况。记录内容格式的分布、域名类型的分布以及关键的成功因素。


5. **分析SERP元素**
   对于每个出现的SERP元素，分析当前占据该位置的页面的特点、内容格式以及其获胜策略。包括特色片段（类型、内容、获胜策略）、PAA（相关问题、当前提供的答案、优化方法）以及AI生成的内容（引用来源、内容模式、引用策略）。



6. **确定搜索意图**
   从SERP内容中判断用户的搜索意图。记录证据、意图占比以及内容格式的影响（如格式、语气、呼叫行动按钮CTA）。



7. **计算实际难度**
   根据以下因素评估整体难度（1-100分）：排名前10的网站权威度、页面权威度、所需反向链接数量、内容质量，以及SERP的稳定性。为新网站、成长中的网站和已建立的网站提供实际的排名评估，并提供更简单的优化方案。



8. **生成建议**
   提供分析总结，包括：主要发现、内容排名要求（最低要求及差异化因素）、SERP元素优化策略、推荐的内容大纲以及下一步行动建议。
   > **参考**：详细分析模板请参见[references/analysis-templates.md](./references/analysis-templates.md)。



## 验证要点

### 输入验证
- [ ] 目标关键词已明确指定
- [ ] 搜索位置和设备类型已确认
- [ ] SERP数据为最新数据（日期已确认）
- [ ] 已识别或提供了前10名排名页面的URL


### 输出验证
- [ ] 每条建议都基于具体的数据点（而非泛化建议）
- [ ] SERP组成图已完整记录所有元素
- [ ] 排名因素是根据对前10名页面的实际分析得出的（而非猜测）
- [ ] 内容要求基于当前SERP中的观察结果
- [ ] 每个数据点的来源已明确说明（SEO工具数据、AI监控数据或用户提供的数据）


## 示例

> **参考**：请参阅[references/example-report.md](./references/example-report.md)，其中包含一个关于“如何开始播客”这一关键词的SERP分析示例。



## 高级分析

### 多关键词SERP比较


```
Compare SERPs for [keyword 1], [keyword 2], [keyword 3]
```


### 历史SERP变化


```
How has the SERP for [keyword] changed over time?
```


### 移动设备与桌面设备的SERP差异


```
Analyze mobile vs desktop SERP differences for [keyword]
```


## 成功技巧

1. **撰写内容前务必检查SERP** —— 不要盲目猜测，务必核实
2. **使内容格式与SERP相匹配** —— 如果列表形式在SERP中占优，就采用列表格式
3. **识别SERP中的优化机会** —— 这类位置的竞争通常较小
4. **注意SERP的稳定性** —— 稳定的SERP更难被突破
5. **研究异常情况** —— 为什么某些排名较低的网站也能排在高位？这可能是优化机会！
6. **考虑优化AI生成的内容** —— 这个方面的重要性日益增加


## 参考资料

- [分析模板](./references/analysis-templates.md) —— 每个分析步骤的详细模板（SERP组成、排名结果、排名规律、元素分析、意图判断、难度评估、优化建议）
- [SERP元素分类](./references/serp-feature-taxonomy.md) —— 完整的SERP元素分类体系，包括触发条件、AI生成答案的框架、意图判断方法以及稳定性评估
- [示例报告](./references/example-report.md) —— 一个关于“如何开始播客”这一关键词的SERP分析示例


## 相关技能

- [关键词研究](../keyword-research/) —— 寻找需要分析的关键词
- [竞争对手分析](../competitor-analysis/) —— 深入研究竞争对手的排名情况
- [页面SEO审核器](../../optimize/on-page-seo-auditor/) —— 根据分析结果进行优化
- [地理内容优化器](../../build/geo-content-optimizer/) —— 优化内容以获得AI的引用
- [元标签优化器](../../build/meta-tags-optimizer/) —— 通过元标签优化SERP的展示效果
- [排名追踪器](../../monitor/rank-tracker/) —— 跟踪关键词在SERP中的排名变化
- [性能报告工具](../../monitor/performance-reporter/) —— 随时间跟踪SERP的可见性指标