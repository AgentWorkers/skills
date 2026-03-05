---
name: backlink-analyzer
version: "3.0.0"
description: '此技能适用于用户需要执行以下操作时：分析反向链接（analyze backlinks）、检查链接质量（check link profile）、识别有害链接（find toxic links）、寻找链接建设机会（link building opportunities）、进行站外SEO优化（off-page SEO）、查看哪些网站链接到了我的网站（who links to me）、处理垃圾链接（I have spammy links）、获取更多反向链接（how do I get more backlinks），或请求移除不良链接（disavow links）。该技能通过分析反向链接的来源和质量，帮助用户了解链接的权威性（link authority），识别潜在的有害链接，发现新的链接建设机会，并监控竞争对手的链接获取情况。对于站内链接分析，可参考“internal-linking-optimizer”；关于竞争对手的链接分析，请参阅“competitor-analysis”。'
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
  geo-relevance: "low"
  tags:
    - seo
    - backlinks
    - link building
    - link profile
    - toxic links
    - off-page seo
    - link authority
    - domain authority
    - link acquisition
    - link-building
    - backlink-profile
    - toxic-links
    - link-audit
    - referring-domains
    - domain-rating
    - link-outreach
    - disavow
    - dr-score
    - link-quality
    - lost-backlinks
  triggers:
    - "analyze backlinks"
    - "check link profile"
    - "find toxic links"
    - "link building opportunities"
    - "off-page SEO"
    - "backlink audit"
    - "link quality"
    - "who links to me"
    - "I have spammy links"
    - "how do I get more backlinks"
    - "disavow links"
---
# 反链分析工具

> **[SEO与地理策略技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理策略相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审计器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../rank-tracker/) · **反链分析工具** · [性能报告工具](../performance-reporter/) · [警报管理工具](../alert-manager/)

**跨领域工具** · [内容质量审计器](../../cross-cutting/content-quality-auditor/) · [域名权威性审计器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具用于分析、监控和优化网站的反链情况，能够识别链接的质量、发现潜在的链接构建机会，并追踪竞争对手的链接构建活动。

## 适用场景

- 审计当前的反链状况
- 识别有害或低质量的链接
- 发现链接构建的机会
- 分析竞争对手的链接策略
- 监控新获得的或丢失的链接
- 评估用于外联的链接质量
- 为链接删除（disavow）做准备

## 功能概述

1. **反链概况分析**：提供全面的反链信息概览。
2. **质量评估**：评估链接的权威性和相关性。
3. **有害链接检测**：识别有害的链接。
4. **竞争对手分析**：比较不同竞争对手的反链情况。
5. **机会发现**：寻找适合构建链接的目标。
6. **趋势监控**：追踪链接数量的变化趋势。
7. **链接删除指导**：提供删除链接的建议。

## 使用方法

### 分析反链概况

```
Analyze backlink profile for [domain]
```

### 发现链接构建机会

```
Find link building opportunities by analyzing [competitor domains]
```

### 识别问题链接

```
Check for toxic backlinks on [domain]
```

### 比较不同网站的反链情况

```
Compare backlink profiles: [your domain] vs [competitor domains]
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md)，了解工具类别的相关信息。

**当与 ~~链接数据库** 和 ~~SEO工具** 集成时：  
- 自动从 ~~链接数据库** 中获取包括引用域名、锚文本分布、链接质量指标（DA/DR）、链接速度以及有害链接检测结果在内的全面反链信息；  
- 从 ~~SEO工具** 中获取竞争对手的反链数据，用于对比分析。

**仅使用手动数据时**：
- 要求用户提供以下数据：
  - 反链数据的CSV文件（包含来源域名、锚文本、链接类型）
  - 带有权威性指标的引用域名列表
  - 用于对比的竞争对手域名
  - 最近的链接增减情况（如需追踪变化）
  - 任何已知的有害或垃圾链接

**使用提供的数据进行完整分析**。在输出结果中明确标注哪些指标来自自动化收集，哪些来自用户提供的数据。

## 使用说明

当用户请求反链分析时，系统将执行以下操作：

1. **生成反链概况**：显示关键指标（总链接数、引用域名数量、DA/DR值、链接速度（30天/90天/全年）、权威性分布图以及反链健康评分。
2. **分析链接质量**：列出高质量链接、链接类型分布、锚文本分析（品牌相关/精确匹配/部分匹配/通用链接/URL链接）以及地理分布情况。
3. **识别有害链接**：显示有害链接的评分及风险类型（如垃圾链接、PBN链接、链接农场链接、无关链接），并提供删除建议（针对域名或具体URL）。
4. **与竞争对手对比**：生成对比表格（引用域名、DA/DR值、链接速度、平均链接权威性等），分析共同的引用域名和吸引链接的竞争对手内容。
5. **寻找链接构建机会**：找出潜在的链接构建目标（如交叉链接、失效链接、未链接的引用内容、适合发布客座文章的页面等），并制定优先级。
6. **追踪链接变化**：显示过去30天内新增或丢失的链接（包括DA值、链接类型、锚文本和日期），以及需要恢复的链接。
7. **生成反链报告**：提供执行摘要、问题点、机会点、竞争地位分析以及推荐的行动方案（包括立即执行、短期和长期措施），并附上关键绩效指标（KPI）。

   > **参考**：请参阅 [references/analysis-templates.md](./references/analysis-templates.md)，获取上述所有步骤的完整输出模板。

### 数据映射

在执行 `domain-authority-auditor` 分析后，以下数据会直接用于CITE评分系统：

| 反链指标 | CITE评分项 | 对应维度 |
|----------------|-----------|-----------|
| 引用域名数量 | C01（引用域名数量） | 引用次数 |
| 权威性分布（DA细分） | C02（引用域名质量） | 引用次数 |
| 链接速度 | C04（链接速度） | 引用次数 |
| 地理分布 | C10（链接来源多样性） | 引用次数 |
| 跟随/非跟随链接比例 | T02（跟随链接比例） | 信任度 |
| 有害链接分析 | T01（链接自然性）、T03（链接流量一致性） | 信任度 |
| 竞争对手链接对比 | T05（链接唯一性） | 信任度 |

## 验证要点

### 输入验证
- 目标域名的反链数据完整且最新。
- 指定了用于对比分析的竞争对手域名。
- 反链数据包含必要的字段（来源域名、锚文本、链接类型）。
- 权威性指标（DA/DR或等效指标）已获取。

### 输出验证
- 每个指标都标明了数据来源和收集日期。
- 有害链接的评估包含风险说明。
- 链接构建的建议具体且可操作。
- 每个数据点的来源均明确标注（来自 ~~链接数据库**、~~SEO工具** 或用户提供的数据）。

## 使用示例

**用户请求**：**通过分析HubSpot、Salesforce和Mailchimp等网站来寻找链接构建机会。**

**输出结果**：

```markdown
## Link Intersection Analysis

### Sites linking to 2+ competitors (not you)

| Domain | DA | HubSpot | Salesforce | Mailchimp | Opportunity |
|--------|-----|---------|------------|-----------|-------------|
| g2.com | 91 | ✅ | ✅ | ✅ | Get listed/reviewed |
| capterra.com | 89 | ✅ | ✅ | ✅ | Submit for review |
| entrepreneur.com | 92 | ✅ | ✅ | ❌ | Pitch guest post |
| techcrunch.com | 94 | ✅ | ❌ | ✅ | PR/news pitch |

### Top 5 Immediate Opportunities

1. **G2.com** (DA 91) - All competitors listed
   - Action: Create detailed G2 profile
   - Effort: Low
   - Impact: High authority + referral traffic

2. **Entrepreneur.com** (DA 92) - 2 competitors have links
   - Action: Pitch contributed article
   - Effort: High
   - Impact: High authority + brand exposure

3. **MarketingProfs** (DA 75) - All competitors featured
   - Action: Apply for expert contribution
   - Effort: Medium
   - Impact: Relevant audience + quality link

### Estimated Impact

If you acquire links from top 10 opportunities:
- New referring domains: +10
- Average DA of new links: 82
- Estimated ranking impact: +2-5 positions for competitive keywords
```

## 成功技巧

1. **质量胜过数量**：一个DA值为80的链接比十个DA值为20的链接更有价值。
2. **定期监控**：及时发现丢失或有害的链接。
3. **研究竞争对手**：学习他们的链接构建策略。
4. **多样化反链来源**：确保链接类型和锚文本的多样性。
5. **谨慎处理链接删除**：仅删除确实有害的链接。

## 链接质量与策略参考

> **参考**：请参阅 [references/link-quality-rubric.md](./references/link-quality-rubric.md)，了解完整的链接质量评分标准（包含6个加权因素）、有害链接识别标准、反链健康评估基准以及链接删除指南。

> **参考**：请参阅 [references/outreach-templates.md](./references/outreach-templates.md)，获取电子邮件外联框架、主题行模板、回复率基准以及针对不同链接构建策略的回复模板。

## 相关技能

- **域名权威性审计器**（[domain-authority-auditor](../../cross-cutting/domain-authority-auditor/)：反链数据直接用于CITE评分系统的C维度；在此分析之后运行该工具以获得完整的域名评分。
- **竞争对手分析**（[competitor-analysis](../../research/competitor-analysis/)：进行全面竞争对手分析。
- **内容差距分析**（[content-gap-analysis](../../research/content-gap-analysis/)：生成适合链接发布的优质内容。
- **警报管理工具**（[alert-manager](../alert-manager/)：设置链接相关警报。
- **性能报告工具**（[performance-reporter](../performance-reporter/)：将分析结果纳入报告。
- **实体优化工具**（[entity-optimizer](../../cross-cutting/entity-optimizer/)：增强网站的实体信号（即提高网站的权威性）。