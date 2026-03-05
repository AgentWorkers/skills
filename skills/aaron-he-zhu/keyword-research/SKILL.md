---
name: keyword-research
version: "3.0.0"
description: '此技能适用于用户提出以下需求时：查找关键词、进行关键词研究、确定写作主题、评估关键词的难度等级、获取搜索量数据、识别提升排名机会的关键词、获取主题灵感、了解人们的搜索需求、选择目标关键词，或为特定主题提供内容创意。该技能能够识别高价值的关键词，并提供关键词的分类（信息型/商业型/交易型/导航型）、难度评分、每月搜索量、每次点击费用（CPC）估算以及人工智能推荐的引用潜力等信息。同时，该技能还能生成排名靠前的关键词列表、主题集群（包含核心页面和辅助页面的分配方案），并制定优先级排序的内容发布计划。支持使用Ahrefs、SEMRush、Google Keyword Planner、Google Search Console等工具，也可手动输入数据进行分析。关于竞争对手的关键词差距，可参考“竞争对手分析”部分；关于主题覆盖范围的不足，可参考“内容缺口分析”部分。'
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
    - keywords
    - ahrefs
    - semrush
    - google-keyword-planner
    - kd-score
    - search-volume
    - cpc
    - topic-clusters
    - pillar-pages
    - long-tail-keywords
    - content-calendar
    - keyword-gap
    - search-intent-classification
  triggers:
    - "find keywords"
    - "keyword research"
    - "what should I write about"
    - "identify ranking opportunities"
    - "topic ideas"
    - "search volume"
    - "content opportunities"
    - "what are people searching for"
    - "which keywords should I target"
    - "give me keyword ideas"
---
# 关键词研究

> **[SEO与地理定位（GEO）技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与GEO相关技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究** · **关键词研究** · [竞争对手分析](../competitor-analysis/) · [SERP分析](../serp-analysis/) · [内容差距分析](../content-gap-analysis/)

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [结构化标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名跟踪工具](../../monitor/rank-tracker/) · [反向链接分析工具](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威性审核工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

该技能用于发现、分析并优先处理SEO和GEO内容策略所需的关键词。根据搜索量、竞争情况、用户意图和业务相关性来识别高价值的机会。

## 适用场景

- 开始新的内容策略或营销活动时
- 扩展到新的主题或市场时
- 为特定产品或服务寻找关键词时
- 识别长尾关键词机会时
- 了解所在行业的搜索意图时
- 规划内容发布计划时
- 进行GEO优化时

## 功能介绍

1. **关键词发现**：从初始关键词生成全面的关键词列表。
2. **意图分类**：根据用户意图（信息型、导航型、商业型、交易型）对关键词进行分类。
3. **难度评估**：评估关键词的竞争程度和排名难度。
4. **机会评分**：根据潜在的投资回报率（ROI）对关键词进行优先级排序。
5. **聚类**：将相关关键词分组到不同的主题簇中。
6. **地理相关性**：识别可能触发人工智能响应的关键词。

## 使用方法

### 基本关键词研究

```
Research keywords for [topic/product/service]
```

```
Find keyword opportunities for a [industry] business targeting [audience]
```

### 针对特定目标的研究

```
Find low-competition keywords for [topic] with commercial intent
```

### 竞争对手分析

```
What keywords is [competitor URL] ranking for that I should target?
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。

**当连接到 ~~SEO工具 + ~~搜索控制台时**：
可以自动获取历史搜索量数据、关键词难度评分、SERP分析结果、当前排名以及竞争对手的关键词信息。该技能会提取初始关键词指标、相关关键词建议和搜索趋势数据。

**仅使用手动数据时**：
用户需要提供以下信息：
1. 初始关键词或主题描述
2. 目标受众和地理位置
3. 商业目标（流量、潜在客户、销售额）
4. 当前域名权威性（如果已知）或网站年龄
5. 任何已知的关键词表现数据或搜索量估算

使用提供的数据进行分析。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供。

## 使用说明

当用户请求关键词研究时，请按照以下步骤操作：

1. **了解背景**：
   - 如果用户未提供相关信息，请询问：
     - 你的产品/服务/主题是什么？
     - 目标受众是谁？
     - 你的业务目标是什么（流量、潜在客户、销售额）？
     - 你的域名权威性如何（新网站还是成熟网站）？
     - 有特定的地理定位要求吗？
     - 偏好的语言是什么？

2. **生成初始关键词**：
   - 从以下关键词开始：
     - 核心产品/服务相关词汇
     - 与问题相关的关键词
     - 与解决方案相关的关键词
     - 针对特定受众的词汇
     - 行业术语

3. **扩展关键词列表**：
   为每个初始关键词生成变体：

   ```markdown
   ## Keyword Expansion Patterns
   
   ### Modifiers
   - Best [keyword]
   - Top [keyword]
   - [keyword] for [audience]
   - [keyword] near me
   - [keyword] [year]
   - How to [keyword]
   - What is [keyword]
   - [keyword] vs [alternative]
   - [keyword] examples
   - [keyword] tools
   
   ### Long-tail Variations
   - [keyword] for beginners
   - [keyword] for small business
   - Free [keyword]
   - [keyword] software/tool/service
   - [keyword] template
   - [keyword] checklist
   - [keyword] guide
   ```

4. **分类搜索意图**：
   根据用户意图对关键词进行分类：

| 意图 | 信号词 | 示例 | 内容类型 |
|--------|---------|---------|--------------|
| 信息型 | 什么是、如何、为什么、指南、学习 | “什么是SEO” | 博文、指南 |
| 导航型 | 品牌名称、特定网站 | “谷歌分析登录” | 主页、产品页面 |
| 商业型 | 最佳、评价、对比 | “最佳SEO工具[年份]” | 对比文章、评价 |
| 交易型 | 购买、价格、折扣、订单 | “购买SEO软件” | 产品页面、价格页面 |

5. **评估关键词难度**：
   为每个关键词打分（1-100分）：

   ```markdown
   ### Difficulty Factors
   
   **High Difficulty (70-100)**
   - Major brands ranking
   - High domain authority competitors
   - Established content (1000+ backlinks)
   - Paid ads dominating SERP
   
   **Medium Difficulty (40-69)**
   - Mix of authority and niche sites
   - Some opportunities for quality content
   - Moderate backlink requirements
   
   **Low Difficulty (1-39)**
   - Few authoritative competitors
   - Thin or outdated content ranking
   - Long-tail variations
   - New or emerging topics
   ```

6. **计算机会评分**：
   计算公式：`机会值 = (搜索量 × 意图价值) / 困难度`

   **意图价值** 根据搜索意图分配不同的权重：
   - 信息型 = 1
   - 导航型 = 1
   - 商业型 = 2
   - 交易型 = 3

   ```markdown
   ### Opportunity Matrix
   
   | Scenario | Volume | Difficulty | Intent | Priority |
   |----------|--------|------------|--------|----------|
   | Quick Win | Low-Med | Low | High | ⭐⭐⭐⭐⭐ |
   | Growth | High | Medium | High | ⭐⭐⭐⭐ |
   | Long-term | High | High | High | ⭐⭐⭐ |
   | Research | Low | Low | Low | ⭐⭐ |
   ```

7. **识别地理相关机会**：
   识别可能触发人工智能响应的关键词：

   ```markdown
   ### GEO-Relevant Keywords
   
   **High GEO Potential**
   - Question formats: "What is...", "How does...", "Why is..."
   - Definition queries: "[term] meaning", "[term] definition"
   - Comparison queries: "[A] vs [B]", "difference between..."
   - List queries: "best [category]", "top [number] [items]"
   - How-to queries: "how to [action]", "steps to [goal]"
   
   **AI Answer Indicators**
   - Query is factual/definitional
   - Answer can be summarized concisely
   - Topic is well-documented online
   - Low commercial intent
   ```

8. **创建主题簇**：
   将关键词分组到相应的主题簇中：

   ```markdown
   ## Topic Cluster: [Main Topic]
   
   **Pillar Content**: [Primary keyword]
   - Search volume: [X]
   - Difficulty: [X]
   - Content type: Comprehensive guide
   
   **Cluster Content**:
   
   ### Sub-topic 1: [Secondary keyword]
   - Volume: [X]
   - Difficulty: [X]
   - Links to: Pillar
   - Content type: [Blog post/Tutorial/etc.]
   
   ### Sub-topic 2: [Secondary keyword]
   - Volume: [X]
   - Difficulty: [X]
   - Links to: Pillar + Sub-topic 1
   - Content type: [Blog post/Tutorial/etc.]
   
   [Continue for all cluster keywords...]
   ```

9. **生成输出报告**：
   生成包含以下内容的报告：执行摘要、主要关键词机会（快速见效的关键词、增长潜力关键词、地理相关关键词）、主题簇、内容发布计划以及下一步行动。

   > **参考**：请参阅 [references/example-report.md](./references/example-report.md) 以获取完整的报告模板和示例。

## 验证要点

### 输入验证：
- 是否提供了明确的初始关键词或主题描述
- 是否指定了目标受众和业务目标
- 是否确认了地理定位和语言要求
- 是否明确了域名权威性或网站成熟度

### 输出验证：
- 每条建议都应引用具体的数据来源
- 每个关键词都应包含搜索量和难度评分
- 关键词应按意图分类并对应到相应的内容类型
- 主题簇之间应显示清晰的关联关系
- 明确标注每个数据点的来源（来自SEO工具、用户提供的数据或估算值）

## 示例

> **参考**：请参阅 [references/example-report.md](./references/example-report.md)，了解关于“小型企业项目管理软件”的完整报告示例。

### 高级用法：
- **意图映射**：根据搜索意图和用户需求阶段，将所有关键词进行分类。
- **季节性分析**：识别特定行业的季节性关键词趋势。
- **竞争对手差距分析**：竞争对手1和竞争对手2在哪些关键词上排名领先，而你的网站尚未覆盖？
- **本地关键词**：研究特定[业务类型]在[城市/地区]的本地关键词。

## 成功技巧：
1. 从描述你核心产品的初始关键词开始。
- 不要忽视长尾关键词——它们通常转化率最高。
- 确保内容与用户意图相匹配（信息型查询需要指南，而非销售页面）。
- 将关键词分组到相应的主题簇中，以提高内容的权威性。
- 优先处理能够快速带来效果的关键词，以建立项目进展和信誉。
- 在策略中加入地理相关关键词，以提高在人工智能搜索结果中的可见性。
- 每季度进行一次关键词更新，因为关键词的动态会随时间变化。

## 参考资料：
- [关键词意图分类](./references/keyword-intent-taxonomy.md) — 完整的意图分类体系及相关信号词和内容策略
- [主题簇模板](./references/topic-cluster-templates.md) — 用于构建主题内容和簇结构的模板
- [关键词优先级框架](./references/keyword-prioritization-framework.md) — 优先级评分矩阵、分类标准和季节性关键词模式
- [示例报告](./references/example-report.md) — 关于项目管理软件的完整关键词研究报告示例

## 相关技能：
- [竞争对手分析](../competitor-analysis/) — 查看竞争对手在哪些关键词上排名
- [内容差距分析](../content-gap-analysis/) — 发现缺失的关键词机会
- [SEO内容撰写工具](../../build/seo-content-writer/) — 为目标关键词创建内容
- [地理内容优化工具](../../build/geo-content-optimizer/) — 优化内容以获得人工智能的推荐
- [排名跟踪工具](../../monitor/rank-tracker/) — 监控关键词排名随时间的变化