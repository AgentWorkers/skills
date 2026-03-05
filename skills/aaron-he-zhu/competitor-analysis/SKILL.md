---
name: competitor-analysis
version: "3.0.0"
description: '当用户提出以下请求时，应使用此技能：  
- “分析竞争对手”  
- “竞争对手的SEO策略”  
- “哪些竞争对手在搜索引擎中排名靠前”  
- “进行竞争分析”  
- “我的竞争对手在做什么？”  
- “他们的做法有何不同？”  
- “为什么他们的排名更高？”  
- “监视竞争对手的SEO策略”。  
该技能会分析竞争对手的SEO策略及地理位置策略，包括他们的排名关键词、内容创作方式、外部链接情况以及人工智能引用的模式。通过这些分析，可以发现超越竞争对手的机会。  
- 如需针对内容方面的差距进行分析，请参阅“content-gap-analysis”；  
- 如需了解外部链接的具体情况，请参阅“backlink-analyzer”。'
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
    - competitor analysis
    - competitive intelligence
    - benchmarking
    - market analysis
    - ranking analysis
    - competitive-seo
    - competitor-keywords
    - competitor-backlinks
    - market-analysis
    - battlecard
    - serp-competition
    - domain-comparison
    - content-benchmarking
    - gap-analysis
  triggers:
    - "analyze competitors"
    - "competitor SEO"
    - "who ranks for"
    - "competitive analysis"
    - "what are my competitors doing"
    - "competitor keywords"
    - "competitor backlinks"
    - "what are they doing differently"
    - "why do they rank higher"
    - "spy on competitor SEO"
---
# 竞争对手分析


> **[SEO与GEO技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与GEO相关技能 · 可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装


<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../keyword-research/) · **竞争对手分析** · [SERP分析](../serp-analysis/) · [内容差距分析](../content-gap-analysis/)

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [结构化标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪工具](../../monitor/rank-tracker/) · [反向链接分析工具](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威度审核工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)


</details>

该技能提供对竞争对手SEO和GEO策略的全面分析，帮助您了解市场中的有效策略，并发现超越竞争对手的机会。


## 适用场景

- 进入新市场或细分领域时
- 根据竞争对手的成功情况制定内容策略
- 了解竞争对手为何排名更高
- 寻找反向链接和合作机会
- 发现竞争对手遗漏的内容空白
- 分析竞争对手的人工智能引用策略
- 对比自己的SEO表现


## 功能概述

1. **关键词分析**：识别竞争对手排名的关键词
2. **内容审计**：分析竞争对手的内容策略和格式
3. **反向链接分析**：审查竞争对手的链接构建方式
4. **技术评估**：评估竞争对手网站的健康状况
5. **地理分析**：了解竞争对手在人工智能搜索结果中的表现
6. **差距识别**：发现竞争对手未注意到的机会
7. **策略提取**：从竞争对手的成功中提取可操作的洞察


## 使用方法

### 基本竞争对手分析


```
Analyze SEO strategy for [competitor URL]
```


```
Compare my site [URL] against [competitor 1], [competitor 2], [competitor 3]
```


### 详细分析


```
What content is driving the most traffic for [competitor]?
```


### 地理聚焦分析


```
How is [competitor] getting cited in AI responses? What can I learn?
```


## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。

**通过连接** [SEO工具 + 分析工具 + AI监控工具]：
- 自动获取竞争对手的关键词排名、反向链接信息、高表现内容以及域名权威度数据。
- 将这些数据与您的网站指标（来自分析工具或搜索控制台）进行对比。
- 使用AI监控工具检查您和竞争对手的人工智能引用模式。


**仅使用手动数据时**：
- 请用户提供以下信息：
  - 需要分析的竞争对手URL（建议2-5个）
  - 您自己的网站URL及当前指标（流量、排名等）
  - 行业或细分领域的背景信息
  - 需要关注的具体方面（关键词、内容、反向链接等）
  - 竞争对手的优缺点


根据提供的数据开展全面分析。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供的数据。


## 使用说明

当用户请求竞争对手分析时：

1. **确定竞争对手**：
   如果未指定，协助确定竞争对手：
   
   ```markdown
   ### Competitor Identification Framework
   
   **Direct Competitors** (same product/service)
   - Search "[your main keyword]" and note top 5 organic results
   - Check who's advertising for your keywords
   - Ask: Who do customers compare you to?
   
   **Indirect Competitors** (different solution, same problem)
   - Search problem-focused keywords
   - Look at alternative solutions
   
   **Content Competitors** (compete for same keywords)
   - May not sell same product
   - Rank for your target keywords
   - Include media sites, blogs, aggregators
   ```


2. **收集竞争对手数据**：
   收集每个竞争对手的以下信息：URL、域名年龄、预估流量、域名权威度、商业模式、目标受众及主要产品/服务。


3. **分析关键词排名**：
   记录所有关键词的排名情况、排名前10/3的关键词数量及表现最佳的关键词（包括排名位置、搜索量、页面URL），以及关键词的意图分布和差距。


4. **审计内容策略**：
   分析不同类型的内容数量、表现最佳的内容、内容模式（字数、频率、格式）、内容主题及成功因素。


5. **分析反向链接情况**：
   审查总反向链接数量、引用来源域名、链接质量分布、主要链接来源域名、链接获取方式及可链接的资源。


6. **技术SEO评估**：
   评估网站的核心网页指标（Core Web Vitals）、移动友好性、网站架构、内部链接质量、URL结构以及技术优势/劣势。


7. **地理/AI引用分析**：
   在人工智能系统中测试竞争对手的内容：记录哪些查询引用了他们的内容，分析他们的地理策略（定义、统计数据、问答信息及权威度信号），以及他们未充分利用的地理机会。


8. **整合竞争情报**：
   生成最终报告，内容包括：执行摘要、竞争格局对比表、域名权威度对比、可借鉴的优势、需要利用的劣势、关键词机会以及行动计划（立即执行/短期/长期）。
   > **参考**：详见 [references/analysis-templates.md](./references/analysis-templates.md) 中的详细报告模板。


## 验证要点

### 输入验证
- 确保竞争对手URL与您的细分领域相关
- 明确分析范围（全面分析或特定焦点）
- 提供可供对比的网站指标
- 确定至少2-3个竞争对手以发现有意义的趋势


### 输出验证
- 每条建议都基于具体数据
- 竞争对手的优势有可量化的证据支持（如指标、排名数据）
- 机会基于可识别的差距，而非假设
- 行动计划具体且可执行
- 明确每个数据点的来源（SEO工具数据、分析工具数据、AI监控数据或用户提供的数据）


## 示例

> **参考**：详见 [references/example-report.md](./references/example-report.md)，其中包含分析HubSpot营销关键词优势的完整示例。


## 高级分析类型

### 内容差距分析


```
Show me content [competitor] has that I don't, sorted by traffic potential
```


### 链接交叉分析


```
Find sites linking to [competitor 1] AND [competitor 2] but not me
```


### SERP特征分析


```
What SERP features do competitors win? (Featured snippets, PAA, etc.)
```


### 历史数据追踪


```
How has [competitor]'s SEO strategy evolved over the past year?
```


## 成功技巧

- **分析3-5个竞争对手** 以获得全面视图
- **包括间接竞争对手**——他们通常具有创新的方法
- **关注内容质量而非仅排名** 
- **研究他们的失败案例**以避免重蹈覆辙
- **定期监控**——竞争对手的策略会不断演变
- **关注可操作的洞察**——找出实际可行的改进点


## 参考资料

- [分析模板](./references/analysis-templates.md) — 每个分析步骤的详细模板
- [竞争态势分析卡](./references/battlecard-template.md) — 适用于销售和营销团队的快速参考工具
- [定位框架](./references/positioning-frameworks.md) — 定位图、信息矩阵和差异化分析工具
- [示例报告](./references/example-report.md) — 分析HubSpot营销关键词优势的完整示例


## 相关技能

- [域名权威度审核工具](../../cross-cutting/domain-authority-auditor/) — 比较竞争对手的域名权威度得分
- [关键词研究](../keyword-research/) — 研究竞争对手排名的关键词
- [内容差距分析](../content-gap-analysis/) — 发现内容改进机会
- [反向链接分析工具](../../monitor/backlink-analyzer/) — 深入分析反向链接
- [SERP分析](../serp-analysis/) — 了解搜索结果的构成
- [内存管理工具](../../cross-cutting/memory-management/) — 将竞争对手数据存储在项目中
- [实体优化工具](../../cross-cutting/entity-optimizer/) — 比较竞争对手的实体存在情况