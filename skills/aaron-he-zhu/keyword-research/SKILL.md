---
name: keyword-research
description: 通过搜索意图分析、难度评估以及内容机会映射，发现具有高价值的关键词。这是启动任何SEO或地理内容策略（GEO content strategy）的基础。
geo-relevance: "medium"
---

# 关键词研究

该技能可帮助您发现、分析并优先选择用于 SEO 和地理定位（GEO）内容策略的关键词。它根据搜索量、竞争情况、用户意图以及与业务的相关性来识别高价值的机会。

## 何时使用该技能

- 在开始新的内容策略或活动时
- 扩展到新的主题或市场时
- 为特定产品或服务寻找关键词时
- 识别长尾关键词机会时
- 了解您所在行业的搜索意图时
- 规划内容日程时
- 研究用于 GEO 优化的关键词时

## 该技能的功能

1. **关键词发现**：从初始关键词生成全面的关键词列表
2. **意图分类**：根据用户意图（信息性、导航性、商业性、交易性）对关键词进行分类
3. **难度评估**：评估竞争程度和排名难度
4. **机会评分**：根据潜在的投资回报率（ROI）对关键词进行优先级排序
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

### 基于特定目标的研究

```
Find low-competition keywords for [topic] with commercial intent
```

```
Identify question-based keywords for [topic] that AI systems might answer
```

### 竞争对手分析

```
What keywords is [competitor URL] ranking for that I should target?
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的占位符信息。

**当连接到 ~~SEO 工具 + ~~搜索控制台时**：
- 自动获取历史搜索量数据、关键词难度评分、SERP 分析结果、当前排名以及竞争对手的关键词重叠情况。该技能将获取初始关键词指标、相关关键词建议和搜索趋势数据。

**仅使用手动数据时**：
- 请用户提供以下信息：
  - 初始关键词或主题描述
  - 目标受众和地理位置
  - 商业目标（流量、潜在客户、销售额）
  - 当前域名权威度（如果已知）或网站年龄
  - 任何已知的关键词表现数据或搜索量估计值

- 使用提供的数据继续进行完整分析。在输出中注明哪些指标来自自动化收集，哪些来自用户提供的数据。

## 指导说明

当用户请求关键词研究时：

1. **了解背景**：
   - 如果用户未提供相关信息，请提出澄清性问题：
     - 您的产品/服务/主题是什么？
     - 目标受众是谁？
     - 您的商业目标是什么？（流量、潜在客户、销售额）
     - 您当前的域名权威度如何？（新网站还是已建立的网站？）
     - 有特定的地理定位要求吗？
     - 偏好的语言是什么？

2. **生成初始关键词**：
   - 从以下方面开始：
     - 核心产品/服务术语
     - 与问题相关的关键词
     - 解决方案相关的关键词
     - 针对特定受众的术语
     - 行业术语

3. **扩展关键词列表**：
   - 对每个初始关键词生成变体：
   
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
   - 按用户意图对每个关键词进行分类：

   | 意图 | 信号词 | 示例 | 内容类型 |
   |--------|---------|---------|--------------|
   | 信息性 | 什么、如何、为什么、指南、学习 | “什么是 SEO” | 博文、指南 |
   | 导航性 | 品牌名称、特定网站 | “Google Analytics 登录” | 主页、产品页面 |
   | 商业性 | 最佳、评论、对比 | “2026 年最佳 SEO 工具” | 对比文章、评论 |
   | 交易性 | 购买、价格、折扣、订单 | “购买 SEO 软件” | 产品页面、价格信息 |

5. **评估关键词难度**：
   - 为每个关键词打分（1-100 分）：
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
   公式：`机会评分 = (搜索量 × 意图价值) / 难度`

   **意图价值** 根据搜索意图分配数值权重：
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

7. **识别地理相关机会**：
   - 识别可能触发 AI 响应的关键词：
   
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
   - 将关键词分组到内容簇中：
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

## 验证检查点

### 输入验证
- [ ] 是否提供了明确的初始关键词或主题描述
- [ ] 是否指定了目标受众和商业目标
- [ ] 是否确认了地理和语言定位
- [ ] 是否确定了域名权威度或网站成熟度

### 输出验证
- [ ] 每个建议都引用了具体的数据点（而非泛泛而谈的建议）
- [ ] 每个关键词都包含了搜索量和难度评分
- [ ] 关键词按意图分类并对应到相应的内容类型
- [ ] 主题簇之间显示了清晰的关系
- [ ] 明确说明了每个数据点的来源（来自 ~~SEO 工具数据、用户提供的数据或估算值）

## 示例

**用户**：“为一家针对中小企业的项目管理软件公司研究关键词”

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
5. **优先处理能够快速产生效果的关键词**以建立势头和可信度
6. **在策略中包含地理关键词**以提高 AI 的识别度
7. **每季度进行一次审查**——关键词的趋势会随时间变化

## 关键词意图分类

理解搜索意图对于关键词选择和内容规划至关重要。

### 意图分类矩阵

| 意图类型 | 用户目标 | SERP 信号词 | 内容策略 | 转化潜力 |
|------------|-----------|--------------|-----------------|---------------------|
| 信息性 | 学习新知识 | 推荐片段、PAA（个性化广告）、知识面板 | 指南、教程、解释性文章 | 低（培养用户兴趣） |
| 导航性 | 查找特定网站/页面 | 品牌相关结果、站点链接 | 品牌页面、登录页面 | 中等（提升品牌知名度） |
| 商业性 | 购买前调查 | 对比结果、评论、“最佳”列表 | 对比文章、评论、购买指南 | 高（转化率较高） |
| 交易性 | 完成购买动作 | 购物结果、广告、产品页面 | 产品页面、价格信息 | 最高（转化率最高） |

### 意图信号词

| 意图 | 信号词 | 示例关键词 |
|--------|-------------|-----------------|
| 信息性 | 如何、什么、为什么、指南、教程、学习、示例 | “如何提高 SEO”，“什么是 Schema 标记” |
| 导航性 | [品牌名称]、登录、注册、官方网站 | “Ahrefs 登录”，“Google Search Console” |
| 商业性 | 最佳、顶级、评论、对比、替代方案、价格 | “2026 年最佳 SEO 工具”，“Ahrefs 与 SEMrush 的对比” |
| 交易性 | 购买、付款、折扣、优惠券、免费试用、下载 | “购买 Ahrefs 订阅”，“免费 SEO 审计工具” |

## 主题簇架构

### 中心辐射模型

```
                    ┌──────────────┐
              ┌─────│  Sub-topic A  │
              │     └──────────────┘
              │     ┌──────────────┐
┌─────────┐   ├─────│  Sub-topic B  │
│  PILLAR  │───┤     └──────────────┘
│  PAGE    │   ├─────┌──────────────┐
└─────────┘   │     │  Sub-topic C  │
              │     └──────────────┘
              └─────┌──────────────┐
                    │  Sub-topic D  │
                    └──────────────┘
```

**核心页面**：针对广泛关键词的综合性概述（3,000-5,000 字）
**簇页面**：针对特定长尾关键词的专题文章（1,500-2,500 字）
**内部链接**：每个簇页面链接到核心页面；核心页面链接到所有簇页面

### 主题簇规划模板

| 核心主题 | 核心关键词 | 子主题 | 长尾关键词 | 搜索量 | 难度 | 状态 |
|-------------|---------------|--------------|----------------|--------|-----------|--------|
| [广泛主题] | [主要关键词] | [子主题 1] | [长尾关键词 1] | [X] | [X] | [草稿/已发布] |

## 关键词优先级框架

**使用哪种评分标准**：使用优先级评分（如下）进行初步的关键词筛选。使用机会评分（步骤 6）进行最终的内容日程安排，其中额外的地理和竞争因素会提供更细致的排名依据。

### 优先级评分矩阵

根据以下因素为每个关键词打分（1-5 分），然后计算加权总分：

| 因素 | 权重 | 评分 1（低） | 评分 5（高） |
|--------|--------|---------------|----------------|
| 搜索量 | 20% | <100 次/月 | >10,000 次/月 |
| 关键词难度 | 25% | 难度 >80（高） | 难度 <20（低） |
| 业务相关性 | 30% | 与业务关联度低 | 与业务高度相关 |
| 意图匹配度 | 15% | 仅针对信息性查询 | 针对交易性或商业性查询 |
| 趋势方向 | 10% | 趋势下降 | 趋势上升 |

**优先级评分** = Σ（因素权重 × 评分）/ 5

### 优先级分类

| 优先级 | 评分范围 | 行动建议 |
|----------|------------|--------|
| P0 — 必须优先处理 | 4.0-5.0 | 立即创建内容 |
| P1 — 高价值 | 3.0-3.9 | 列入下一次内容计划 |
| P2 — 有潜力 | 2.0-2.9 | 规划未来的内容 |
| P3 — 监控 | 1.0-1.9 | 追踪但不优先处理 |

## 季节性关键词模式

### 季节性分析框架

| 季节性触发因素 | 示例关键词 | 规划提前时间 | 内容策略 |
|---------------|-----------------|-------------------|-----------------|
| 日历事件 | “黑色星期五 SEO”，“新年营销计划” | 提前 3-4 个月 | 在高峰期前 6-8 周发布 |
| 行业事件 | “[会议] 备忘录”，“Google 算法更新” | 1-2 个月 / 反应式规划 | 提前准备模板，快速响应 |
| 预算周期 | “第一季度营销预算模板”，“SEO ROI 报告” | 提前 2-3 个月 | 针对特定季节进行规划 |
| 季节性需求 | “夏季营销创意”，“节日邮件活动” | 提前 2-3 个月 | 根据新数据每年更新 |

## 参考资料

- [关键词意图分类](./references/keyword-intent-taxonomy.md) — 完整的意图分类及相关信号词和内容策略
- [主题簇模板](./references/topic-cluster-templates.md) — 用于构建核心页面和簇页面的内容模板

## 相关技能

- [竞争对手分析](../competitor-analysis/) — 查看竞争对手排名的关键词
- [内容差距分析](../content-gap-analysis/) — 发现缺失的关键词机会
- [SEO 内容编写](../../build/seo-content-writer/) — 为目标关键词创建内容
- [地理内容优化](../../build/geo-content-optimizer/) — 优化以提升 AI 的引用率
- [排名跟踪](../../monitor/rank-tracker/) — 监测关键词排名的变化
- [内存管理](../../cross-cutting/memory-management/) — 将关键词数据存储在项目内存中
- [SERP 分析](../serp-analysis/) — SERP 数据有助于制定关键词策略