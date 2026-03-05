---
name: rank-tracker
version: "3.0.0"
description: '当用户请求“跟踪排名”、“查看关键词位置”、“监控排名变化”、“监测搜索引擎结果页（SERP）上的排名情况”、“我的排名如何”、“我在哪个关键词上排名靠前”、“我的排名有变化吗”或“关键词位置跟踪”时，应使用此功能。该功能能够跟踪并分析关键词在传统搜索结果和人工智能生成响应中的排名变化情况，监测排名趋势，并在出现显著变化时发出警报。如需自动化警报功能，请参阅“alert-manager”；如需综合报告，请参阅“performance-reporter”。'
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
    - rank tracking
    - keyword positions
    - serp monitoring
    - ranking trends
    - position tracking
    - ai ranking
    - keyword-rankings
    - position-tracking
    - ranking-changes
    - serp-positions
    - search-visibility
    - ranking-drops
    - ranking-improvements
    - rank-monitoring
  triggers:
    - "track rankings"
    - "check keyword positions"
    - "ranking changes"
    - "monitor SERP positions"
    - "how am I ranking"
    - "keyword tracking"
    - "position monitoring"
    - "where do I rank for this keyword"
    - "did my rankings change"
    - "keyword position tracking"
---
# 排名跟踪器

> **[SEO与GEO技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与GEO相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [结构化标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · **排名跟踪器** · [反向链接分析工具](../backlink-analyzer/) · [性能报告工具](../performance-reporter/) · [警报管理工具](../alert-manager/)

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威度审核工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具用于跟踪并分析关键词的排名变化，同时监控传统的SERP排名以及AI/GEO相关内容的可见性，提供全面的搜索性能洞察。

## 适用场景

- 为新营销活动设置排名跟踪
- 监控关键词排名的变化
- 分析排名趋势
- 与竞争对手进行排名对比
- 跟踪SERP中的特色内容
- 监控AI相关内容的展示情况
- 为利益相关者生成排名报告

## 功能介绍

1. **排名跟踪**：记录并监控关键词的排名情况。
2. **趋势分析**：识别排名随时间的变化模式。
3. **变化检测**：标记出显著的排名变动。
4. **竞争对手对比**：与竞争对手进行基准对比。
5. **SERP特色内容跟踪**：监控特色片段（Featured Snippets）和PAA（Positioned Answer Boxes）的展示情况。
6. **GEO可见性跟踪**：跟踪AI相关内容的引用情况。
7. **报告生成**：生成排名性能报告。

## 使用方法

### 设置跟踪

```
Set up rank tracking for [domain] targeting these keywords: [keyword list]
```

### 分析排名

```
Analyze ranking changes for [domain] over the past [time period]
```

### 与竞争对手对比

```
Compare my rankings to [competitor] for [keywords]
```

### 生成报告

```
Create a ranking report for [domain/campaign]
```

## 数据来源

> 有关工具类别的详细信息，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当连接了以下工具时：**
- **SEO工具**、**搜索控制台**、**分析工具**和**AI监控工具**：会自动从这些工具中获取排名数据、搜索量、流量数据以及AI相关内容的引用情况。系统每天自动检查排名，并提供历史趋势数据。

**仅使用手动数据时：**
- 需要用户提供以下信息：
  - 关键词的排名情况（当前和历史数据）
  - 目标关键词列表及其搜索量
  - 竞争对手的域名及其关键词排名
  - SERP中的特色内容状态（如特色片段、PAA的展示情况）
  - AI相关内容的引用数据（如果需要跟踪GEO指标）

**使用提供的数据进行完整分析**。在报告中明确区分哪些数据来自自动收集，哪些数据是用户提供的。

## 使用说明

当用户请求排名跟踪或分析时，请按照以下步骤操作：

1. **设置关键词跟踪**：配置域名、地理位置、设备类型和更新频率。添加关键词，包括关键词的搜索量、当前排名、类型和优先级。同时设置竞争对手的跟踪信息以及关键词的分类（品牌/产品/信息类/商业类）。
2. **记录当前排名**：生成按排名范围（如前1名、第2-3名等）的排名概览，展示排名分布图、详细排名信息（包含URL和SERP特色内容）以及排名变化情况。
3. **分析排名变化**：分析整体排名变化情况，找出排名提升或下降的原因，提出恢复建议，识别稳定的关键词和下降的关键词。
4. **跟踪SERP特色内容**：比较与竞争对手在特色片段、PAA等方面的表现。
5. **跟踪GEO/AI可见性**：监控每个关键词的AI相关内容展示情况、引用率和排名变化趋势，以及提升机会。
6. **与竞争对手对比**：生成对比报告，包括关键词的份额对比、逐个关键词的详细对比结果以及潜在的威胁等级。
7. **生成排名报告**：生成包含整体趋势、排名分布、关键亮点（优势/问题/机会）、详细分析结果、SERP特色内容报告、GEO可见性以及竞争情况的报告。

   > **参考资料**：请参阅[references/ranking-analysis-templates.md](./references/ranking-analysis-templates.md)，获取所有步骤的完整报告模板。

## 验证要点

### 输入验证
- 关键词列表是否完整，且包含相应的搜索量信息。
- 是否指定了目标域名和跟踪地理位置。
- 是否已确定用于对比的竞争对手域名。
- 是否有历史基线数据或已设置初始跟踪周期。

### 输出验证
- 每个指标都应明确标注数据来源和收集日期。
- 排名变化应附有背景说明。
- 重要的数据变化应有相应的解释或调查记录。
- 明确指出每个数据点的来源（来自SEO工具、搜索控制台、用户提供的数据或估算值）。

## 示例

**用户请求**：“分析我上个月的排名变化。”

**输出结果**：

```markdown
# Ranking Analysis: [current month, year]

## Summary

Your average position improved from 15.3 to 12.8 (-2.5 positions = better)
Keywords in top 10 increased from 12 to 17 (+5)

## Biggest Wins

| Keyword | Old | New | Change | Possible Cause |
|---------|-----|-----|--------|----------------|
| email marketing tips | 18 | 5 | +13 | Likely driven by content refresh |
| best crm software | 24 | 11 | +13 | Correlates with new backlinks acquired |
| sales automation | 15 | 7 | +8 | Correlates with schema markup addition |

## Needs Attention

| Keyword | Old | New | Change | Action |
|---------|-----|-----|--------|--------|
| marketing automation | 4 | 12 | -8 | Likely displaced by new HubSpot guide |

**Recommended**: Update your marketing automation guide with [current year] statistics and examples.
```

## 使用技巧

1. **保持一致性**：使用相同的时间、设备和地理位置进行跟踪。
2. **选择足够的关键词**：至少选择50-200个关键词以获得有意义的数据。
3. **按意图分类**：分别跟踪品牌类、商业类和信息类关键词。
4. **关注竞争对手**：了解竞争环境有助于更好地分析数据。
5. **关注SERP特色内容**：没有特色片段的排名可能低于有特色片段的排名。
6. **包含GEO指标**：AI相关内容的可见性越来越重要。

## 排名变化快速参考

### 应对策略

| 排名变化 | 时间范围 | 应对措施 |
|--------|-----------|--------|
| 排名下降1-3位 | 等待1-2周 | 监控情况，可能是正常波动 |
| 排名下降3-5位 | 在1周内进行调查 | 检查技术问题或竞争对手的变化 |
| 排名下降5-10位 | 立即调查 | 进行全面诊断（技术、内容、链接等方面） |
| 从第1名跌出排名 | 紧急处理 | 进行全面审计并制定恢复计划 |
| 排名上升 | 记录并分析原因 | 了解哪些因素起到了作用，能否复制这些做法？ |

> **参考资料**：请参阅[references/tracking-setup-guide.md](./references/tracking-setup-guide.md)，了解根本原因的分类、不同排名位置的点击率基准、SERP特色内容的点击率影响、算法更新的影响、跟踪配置的最佳实践、关键词选择和分组策略以及数据解读方法。

## 相关技能

- [关键词研究](../../research/keyword-research/)：用于寻找需要跟踪的关键词。
- [SERP分析](../../research/serp-analysis/)：帮助理解SERP的构成。
- [警报管理](../alert-manager/)：用于设置排名警报。
- [性能报告](../performance-reporter/)：用于生成全面的报告。
- [内存管理](../../cross-cutting/memory-management/)：用于在项目中存储排名历史数据。