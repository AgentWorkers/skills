---
name: keyword-research
description: '**使用场景：**  
当用户提出“查找关键词”、“进行关键词研究”、“我应该写些什么内容”、“识别内容排名机会”、“获取主题灵感”、“人们正在搜索什么”、“我应该针对哪些关键词”或“提供关键词建议”等需求时，本工具可发挥作用。它通过搜索意图分析、难度评估以及内容机会映射，帮助用户发现高价值的关键词。这是制定任何SEO或地理位置（GEO）内容策略的基础工具。如需专门分析竞争对手使用的关键词，请参阅“竞争对手分析”（competitor-analysis）；如需了解内容主题上的空白点，请参阅“内容差距分析”（content-gap-analysis）。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - keywords
    - search intent
    - content strategy
    - topic research
    - content planning
    - search volume
    - long-tail keywords
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

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能的安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · **关键词研究** · [竞争对手分析](../competitor-analysis/) · [SERP分析](../serp-analysis/) · [内容差距分析](../content-gap-analysis/)

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [Schema标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审计工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪工具](../../monitor/rank-tracker/) · [反向链接分析工具](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审计工具](../../cross-cutting/content-quality-auditor/) · [域名权威度审计工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该技能可帮助您发现、分析并优先选择用于SEO和地理定位（GEO）内容策略的关键词。它根据搜索量、竞争情况、用户意图和业务相关性来识别高价值的机会。

## 何时使用此技能

- 在开始新的内容策略或活动时
- 扩展到新的主题或市场时
- 为特定产品或服务寻找关键词时
- 识别长尾关键词机会时
- 了解您所在行业的搜索意图时
- 规划内容日程时
- 为地理定位优化研究关键词时

## 该技能的功能

1. **关键词发现**：从初始关键词生成全面的关键词列表
2. **意图分类**：根据用户意图（信息性、导航性、商业性、交易性）对关键词进行分类
3. **难度评估**：评估竞争程度和排名难度
4. **机会评分**：根据潜在的投资回报率（ROI）对关键词进行优先排序
5. **聚类**：将相关关键词分组到主题簇中
6. **地理相关性**：识别可能触发人工智能（AI）响应的关键词

## 使用方法

### 基本关键词研究

```
Research keywords for [topic/product/service]
```

```
Find keyword opportunities for a [industry] business targeting [audience]
```

### 带有特定目标的研究

```
Find low-competition keywords for [topic] with commercial intent
```

### 竞争对手分析

```
What keywords is [competitor URL] ranking for that I should target?
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以获取工具类别的相关信息。

**当与 ~~SEO工具 + ~~搜索控制台连接时：**
自动获取历史搜索量数据、关键词难度评分、SERP分析结果、当前排名以及竞争对手的关键词重叠情况。该技能会提取初始关键词指标、相关关键词建议和搜索趋势数据。

**仅使用手动数据时：**
要求用户提供：
1. 初始关键词或主题描述
2. 目标受众和地理位置
3. 商业目标（流量、潜在客户、销售额）
4. 当前域名权威度（如果已知）或网站年龄
5. 任何已知的关键词表现数据或搜索量估计值

使用提供的数据进行完整分析。在输出中注明哪些指标来自自动化收集，哪些来自用户提供的数据。

## 指导说明

当用户请求关键词研究时：

1. **了解背景**
   如果用户未提供相关信息，请询问以下问题：
   - 您的产品/服务/主题是什么？
   - 目标受众是谁？
   - 您的商业目标是什么？（流量、潜在客户、销售额）
   - 您当前的域名权威度如何？（新网站还是成熟网站）
   有特定的地理定位要求吗？
   偏好的语言是什么？

2. **生成初始关键词**
   从以下方面开始：
   - 核心产品/服务术语
   - 与问题相关的关键词
   - 解决方案相关的关键词
   与受众相关的术语
   行业术语

3. **扩展关键词列表**
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

4. **分类搜索意图**
   对每个关键词进行分类：

   | 意图 | 信号词 | 示例 | 内容类型 |
   |--------|---------|---------|--------------|
   | 信息性 | what, how, why, guide, learn | “什么是SEO” | 博文、指南 |
   | 导航性 | 品牌名称、特定网站 | “google analytics login” | 主页、产品页面 |
   | 商业性 | best, review, vs, compare | “最佳SEO工具[当前年份]” | 对比文章、评论 |
   | 交易性 | buy, price, discount, order | “购买SEO软件” | 产品页面、价格信息 |

5. **评估关键词难度**
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

6. **计算机会评分**
   公式：`机会评分 = (搜索量 × 意图价值) / 难度`

   **意图价值**根据搜索意图分配数值权重：
   - 信息性 = 1
   - 导航性 = 1
   - 商业性 = 2
   - 交易性 = 3

   ```markdown
   ### Opportunity Matrix
   
   | Scenario | Volume | Difficulty | Intent | Priority |
   |----------|--------|------------|--------|----------|
   | Quick Win | Low-Med | Low | High | ⭐⭐⭐⭐⭐ |
   | Growth | High | Medium | High | ⭐⭐⭐⭐ |
   | Long-term | High | High | High | ⭐⭐⭐ |
   | Research | Low | Low | Low | ⭐⭐ |
   ```

7. **识别地理定位机会**
   可能触发AI响应的关键词：
   
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

8. **创建主题簇**
   将关键词分组到内容簇中：

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

9. **生成输出报告**
   ```markdown
   # Keyword Research Report: [Topic]
   
   **Generated**: [Date]
   **Target Audience**: [Audience]
   **Business Goal**: [Goal]
   
   ## Executive Summary
   
   - Total keywords analyzed: [X]
   - High-priority opportunities: [X]
   - Estimated traffic potential: [X]/month
   - Recommended focus areas: [List]
   
   ## Top Keyword Opportunities
   
   ### Quick Wins (Low difficulty, High value)
   
   | Keyword | Volume | Difficulty | Intent | Score |
   |---------|--------|------------|--------|-------|
   | [keyword 1] | [X] | [X] | [type] | [X] |
   | [keyword 2] | [X] | [X] | [type] | [X] |
   
   ### Growth Keywords (Medium difficulty, High volume)
   
   | Keyword | Volume | Difficulty | Intent | Score |
   |---------|--------|------------|--------|-------|
   | [keyword 1] | [X] | [X] | [type] | [X] |
   
   ### GEO Opportunities (AI-citation potential)
   
   | Keyword | Type | AI Potential | Recommended Format |
   |---------|------|--------------|-------------------|
   | [keyword 1] | Question | High | Q&A section |
   | [keyword 2] | Definition | High | Clear definition |
   
   ## Topic Clusters
   
   [Include cluster maps]
   
   ## Content Calendar Recommendations
   
   | Month | Content | Target Keyword | Type |
   |-------|---------|----------------|------|
   | [Month] | [Title] | [Keyword] | [Type] |
   
   ## Next Steps

   1. [Action item 1]
   2. [Action item 2]
   3. [Action item 3]
   ```

## 验证要点

### 输入验证
- [ ] 是否提供了清晰的初始关键词或主题描述
- [ ] 是否指定了目标受众和商业目标
- [ ] 是否确认了地理定位和语言目标
- [ ] 是否确定了域名权威度或网站成熟度

### 输出验证
- [ ] 每个建议都引用了具体的数据点（而非泛化建议）
- [ ] 每个关键词都包含了搜索量和难度评分
- [ ] 关键词按意图分类并对应到内容类型
- [ ] 主题簇之间显示了明确的关联关系
- [ ] 明确说明了每个数据点的来源（来自SEO工具、用户提供或估算）

## 示例

**用户**：“为一家针对小型企业的项目管理软件公司研究关键词”

**输出**：

```markdown
# Keyword Research Report: Project Management Software

**Generated**: [current month and year]
**Target Audience**: Small business owners and teams
**Business Goal**: Software signups and trials

## Executive Summary

- Total keywords analyzed: 150+
- High-priority opportunities: 23
- Estimated traffic potential: 45,000/month
- Recommended focus areas: 
  - Task management workflows
  - Team collaboration
  - Small business productivity

## Top Keyword Opportunities

### Quick Wins (Priority: Immediate)

| Keyword | Volume | Difficulty | Intent | Score |
|---------|--------|------------|--------|-------|
| project management for small teams | 1,200 | 28 | Commercial | 92 |
| simple task management software | 890 | 25 | Commercial | 89 |
| best free project management tool | 2,400 | 35 | Commercial | 85 |
| how to manage remote team projects | 720 | 22 | Informational | 82 |
| project tracking spreadsheet alternative | 480 | 18 | Commercial | 80 |

### Growth Keywords (Priority: 3-6 months)

| Keyword | Volume | Difficulty | Intent | Score |
|---------|--------|------------|--------|-------|
| project management software | 18,000 | 72 | Commercial | 65 |
| best project management tools [current year] | 8,500 | 65 | Commercial | 62 |
| project management app | 12,000 | 68 | Commercial | 58 |

### GEO Opportunities (AI-citation potential)

| Keyword | Type | AI Potential | Recommended Format |
|---------|------|--------------|-------------------|
| what is project management | Definition | ⭐⭐⭐⭐⭐ | Clear definition + methodology |
| agile vs waterfall | Comparison | ⭐⭐⭐⭐⭐ | Side-by-side comparison table |
| project management methodologies | List | ⭐⭐⭐⭐ | Comprehensive list with pros/cons |
| how to create a project plan | How-to | ⭐⭐⭐⭐ | Step-by-step guide |
| project management best practices | List | ⭐⭐⭐⭐ | Numbered best practices |

## Topic Clusters

### Cluster 1: Project Management Fundamentals

**Pillar**: "Complete Guide to Project Management" (8,500 volume)

Cluster articles:
1. What is project management? (2,200 volume)
2. Project management methodologies explained (1,800 volume)
3. How to create a project plan (1,400 volume)
4. Project management best practices (1,200 volume)
5. Project management roles and responsibilities (890 volume)

### Cluster 2: Team Collaboration

**Pillar**: "Team Collaboration Tools Guide" (4,200 volume)

Cluster articles:
1. How to improve team communication (1,600 volume)
2. Remote team management tips (1,400 volume)
3. Best practices for distributed teams (920 volume)
4. Team productivity tools comparison (780 volume)

## Content Calendar Recommendations

| Month | Content | Target Keyword | Type |
|-------|---------|----------------|------|
| Week 1 | Simple Task Management Guide | simple task management software | Blog + Demo |
| Week 2 | Project Management for Small Teams | project management for small teams | Pillar Page |
| Week 3 | Agile vs Waterfall: Complete Comparison | agile vs waterfall | Comparison |
| Week 4 | Free PM Tools Roundup | best free project management tool | Listicle |

## Next Steps

1. **Immediate**: Create landing pages for top 5 quick-win keywords
2. **Week 1-2**: Write pillar content for "Project Management Fundamentals"
3. **Week 3-4**: Build out cluster content with internal linking
4. **Ongoing**: Track rankings and adjust strategy based on performance
```

## 高级功能

### 意图映射

```
Map all keywords for [topic] by search intent and funnel stage
```

### 季节性分析

```
Identify seasonal keyword trends for [industry]
```

### 竞争对手差距分析

```
What keywords do [competitor 1], [competitor 2], [competitor 3] rank for 
that I'm missing?
```

### 地方关键词

```
Research local keywords for [business type] in [city/region]
```

## 成功技巧

1. **从描述您核心产品的初始关键词开始**
2. **不要忽视长尾关键词**——它们通常转化率最高
3. **确保内容与用户意图相匹配**——信息性查询需要的是指南，而不是销售页面
4. **将关键词分组到簇中**以建立主题权威性
5. **优先处理能够快速见效的内容**以建立势头和可信度
6. **在策略中包含地理定位关键词**以提高AI的识别度
7. **每季度进行一次审查**——关键词的趋势会随时间变化

## 关键词意图分类

理解搜索意图对于关键词选择和内容规划至关重要。

### 意图分类矩阵

| 意图类型 | 用户目标 | SERP信号词 | 内容策略 | 转化潜力 |
|------------|-----------|--------------|-----------------|---------------------|
| 信息性 | 学习知识 | 特色片段、PAA（搜索建议）、知识面板 | 指南、教程 | 低（培养用户兴趣） |
| 导航性 | 寻找特定网站/页面 | 品牌结果、站点链接 | 品牌页面、登录页面 | 中等（提升品牌知名度） |
| 商业性 | 购买前调查 | 对比结果、评论、“最佳”列表 | 对比文章、评论 | 高（转化率较高） |
| 交易性 | 完成交易 | 购物结果、广告、产品页面 | 产品页面、价格信息 | 最高（转化率最高） |

### 意图信号词

| 意图 | 信号词 | 示例关键词 |
|--------|-------------|-----------------|
| 信息性 | how, what, why, guide, tutorial, learn | “如何提高SEO”，“什么是Schema标记” |
| 导航性 | [品牌名称]，login，sign in，official，website | “Ahrefs login”，“Google Search Console” |
| 商业性 | best，top，review，comparison，vs，alternative，pricing | “2026年最佳SEO工具”，“Ahrefs vs SEMrush” |
| 交易性 | buy，purchase，discount，coupon，free trial，download，hire | “购买Ahrefs订阅”，“免费SEO审计工具” |

## 主题簇架构

### 中心辐射模型

**核心页面**：针对广泛关键词的综合性概述（3,000-5,000字）
**簇页面**：针对特定长尾关键词的专题文章（1,500-2,500字）
**内部链接**：每个簇页面链接到核心页面；核心页面链接到所有簇页面

### 主题簇规划模板

| 核心主题 | 核心关键词 | 簇主题 | 簇关键词 | 搜索量 | 难度 | 状态 |
|-------------|---------------|--------------|----------------|--------|-----------|--------|
| [广泛主题] | [主要关键词] | [子主题1] | [长尾关键词1] | [X] | [X] | [草稿/已发布] |

## 关键词优先级框架

**使用哪个评分标准**：使用“优先级评分”（如下）进行初步的关键词筛选。使用“机会评分”（步骤6）进行最终的内容日程安排，其中地理定位和竞争因素会提供更细致的排名参考。

### 优先级评分矩阵

根据以下因素为每个关键词打分（1-5分），然后计算加权总分：

| 因素 | 权重 | 评分1（低） | 评分5（高） |
|--------|--------|---------------|----------------|
| 搜索量 | 20% | <100次/月 | >10,000次/月 |
| 关键词难度 | 25% | 难度大于80（高难度） | 难度小于20（低难度） |
| 商业相关性 | 30% | 与业务关联度低 | 与业务高度相关 |
| 搜索意图匹配 | 15% | 仅信息性查询 | 交易性/商业性查询 |
| 趋势方向 | 10% | 趋势下降 | 趋势上升 |

**优先级评分** = Σ（因素权重 × 评分） / 5

### 优先级类别

| 优先级 | 评分范围 | 行动建议 |
|----------|------------|--------|
| P0 — 必须优先处理 | 4.0-5.0 | 立即创建内容 |
| P1 — 高价值 | 3.0-3.9 | 排入下一次内容计划 |
| P2 — 有机会 | 2.0-2.9 | 规划未来的内容 |
| P3 — 监控 | 1.0-1.9 | 追踪但不优先处理 |

## 季节性关键词模式

### 季节性分析框架

| 季节性触发因素 | 示例关键词 | 规划提前时间 | 内容策略 |
|---------------|-----------------|-------------------|-----------------|
| 日历事件 | “黑色星期五SEO”，“新年营销计划” | 提前3-4个月 | 在高峰期前6-8周发布 |
| 行业事件 | “[会议]要点”，“Google算法更新” | 1-2个月/反应式 | 提前规划模板，快速响应 |
| 预算周期 | “第一季度营销预算模板”，“SEO投资回报率报告” | 提前2-3个月 | 针对规划季节（10月-12月） |
| 季节性需求 | “夏季营销创意”，“假日邮件活动” | 提前2-3个月 | 每年根据新数据更新 |

## 参考资料

- [关键词意图分类](./references/keyword-intent-taxonomy.md) — 完整的意图分类及信号词和内容策略 |
- [主题簇模板](./references/topic-cluster-templates.md) — 中心辐射架构的模板

## 相关技能

- [竞争对手分析](../competitor-analysis/) — 查看竞争对手排名的关键词
- [内容差距分析](../content-gap-analysis/) — 发现缺失的关键词机会
- [SEO内容撰写工具](../../build/seo-content-writer/) — 为目标关键词创建内容 |
- [地理内容优化工具](../../build/geo-content-optimizer/) — 优化内容以获得AI的引用 |
- [排名追踪工具](../../monitor/rank-tracker/) — 监控关键词的排名变化 |
- [内存管理](../../cross-cutting/memory-management/) — 将关键词数据存储在项目内存中 |
- [SERP分析](../serp-analysis/) — SERP模式有助于关键词策略的制定