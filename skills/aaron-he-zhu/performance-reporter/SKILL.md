---
name: performance-reporter
version: "3.0.0"
description: '当用户请求生成“SEO报告”、“性能报告”、“流量报告”、“SEO仪表盘”、“向利益相关者汇报”、“展示相关数据”或“向老板展示SEO结果”时，应使用此技能。该技能能够生成包含排名、流量、反向链接以及AI可见性指标的全面SEO和GEO性能报告，并为利益相关者提供执行摘要和详细分析。如需进行详细的排名跟踪，请使用rank-tracker工具；如需针对特定链接进行分析，请使用backlink-analyzer工具。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: AMPLITUDE_API_KEY
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - performance report
    - seo report
    - traffic analysis
    - seo dashboard
    - executive summary
    - analytics report
    - kpi tracking
    - seo-reporting
    - kpi-dashboard
    - monthly-report
    - traffic-report
    - analytics-report
    - stakeholder-report
    - seo-metrics
    - organic-traffic
    - ctr-report
  triggers:
    - "generate SEO report"
    - "performance report"
    - "traffic report"
    - "SEO dashboard"
    - "report to stakeholders"
    - "monthly report"
    - "SEO analytics"
    - "show me the numbers"
    - "monthly SEO report"
    - "present SEO results to my boss"
---
# 性能报告工具

> **[SEO与GEO技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与GEO相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名跟踪器](../rank-tracker/) · [反向链接分析器](../backlink-analyzer/) · **性能报告工具** · [警报管理器](../alert-manager/)

**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该工具能够生成全面的SEO和GEO性能报告，将多种指标整合为可操作的洞察。报告包括执行摘要、详细分析以及用于利益相关者沟通的可视化数据展示。

## 适用场景

- 月度/季度SEO报告
- 向高层利益相关者汇报
- 为机构提供客户报告
- 跟踪营销活动效果
- 综合多种SEO指标
- 制作GEO可见性报告
- 记录SEO工作的投资回报率（ROI）

## 功能概述

1. **数据聚合**：整合多个SEO数据源
2. **趋势分析**：识别各项指标之间的模式
3. **执行摘要**：生成高层次的概览
4. **可视化报告**：以清晰的形式呈现数据
5. **基准对比**：根据目标和竞争对手进行跟踪
6. **内容质量监控**：整合审核页面的CORE-EEAT评分
7. **ROI计算**：衡量SEO投资的回报
8. **建议**：基于数据提出行动方案

## 使用方法

### 生成性能报告

```
Create an SEO performance report for [domain] for [time period]
```

### 执行摘要

```
Generate an executive summary of SEO performance for [month/quarter]
```

### 具体报告类型

```
Create a GEO visibility report for [domain]
```

```
Generate a content performance report
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以获取工具类别的占位符信息。

**当连接了以下工具时：**
- **分析工具**、**搜索控制台**、**SEO工具**和**AI监控工具**：自动汇总来自这些工具的流量指标、搜索性能数据、排名信息、反向链接数据以及GEO可见性数据，生成包含历史趋势的综合性多源报告。

**仅使用手动数据时：**
- 要求用户提供以下信息：
  - 分析工具的截图或流量数据导出（会话数、用户数、转化率）
  - 搜索控制台数据（展示次数、点击次数、平均排名）
  - 报告期间的关键词排名数据
  - 反向链接指标（引用域名、新增/丢失的链接）
  - 用于对比的关键绩效指标和目标
  - 如果需要跟踪GEO指标，请提供AI引用数据

**使用提供的数据进行完整分析。在报告中注明哪些数据来自自动化收集，哪些数据由用户提供。**

## 使用说明

当用户请求性能报告时，请按照以下步骤操作：

1. **定义报告参数**：域名、报告周期、对比周期、报告类型（月度/季度/年度）、目标受众（高层/技术团队/客户）以及关注的重点领域。
2. **生成执行摘要**：包括整体性能评分、主要成果/需要关注的领域、关键指标一览表（流量、排名、转化率、域名权威度、AI引用次数）以及SEO投资回报率计算结果。
3. **报告有机流量表现**：提供流量概览（会话数、用户数、页面浏览量、跳出率）、流量趋势可视化图表、按来源/设备划分的流量分布以及表现最佳的页面。
4. **报告关键词排名**：按排名范围展示排名情况、排名变化可视化图表、表现最佳的关键词以及排名下降的关键词。
5. **报告GEO/AI性能**：提供AI引用情况概览、按主题分类的引用次数、GEO方面的成果以及优化机会。
6. **报告域名权威度（CITE评分）**：如果已经进行了CITE审核，请包含CITE评分（C/I/T/E）及其随时间的变化趋势和审核状态；如果没有进行审核，请标注为“尚未评估”。
7. **内容质量（CORE-EEAT评分）**：如果已经进行了内容质量审核，请包含所有8个CORE-EEAT维度的平均评分及其变化趋势；如果没有进行审核，请标注为“尚未评估”。
8. **报告反向链接表现**：提供链接概况、每周新增链接情况、重要的新链接以及竞争地位。
9. **报告内容表现**：总结发布情况、表现最佳的内容、需要改进的内容以及内容的ROI。
10. **提出建议**：针对不同优先级、预期影响和责任方，提出即时/短期/长期的行动方案，并为下一阶段设定目标。
11. **编制完整报告**：将所有部分整合在一起，并附上目录和附录（数据来源、方法论、术语表）。

   > **参考资料**：请参阅[references/report-output-templates.md](./references/report-output-templates.md)，以获取所有11个报告部分的完整输出模板。

## 验证要点

### 输入验证
- **报告周期**明确且包含对比周期
- 所有所需数据来源均已获取或已注明替代方案
- 目标受众已确定（高层/技术团队/客户）
- 已设定用于基准对比的性能目标和KPI

### 输出验证
- 每个指标都标明了数据来源和收集日期
- 趋势数据包含跨时期的对比
- 建议具体、有优先级且具有可操作性
- 每个数据点的来源均明确标注（分析工具数据、搜索控制台数据、SEO工具数据或用户提供的数据）

## 示例

**用户请求**：“为cloudhosting.com生成2025年1月的月度SEO报告”

**输出示例**（省略了所有11个步骤的详细内容，仅展示部分结果）：

```markdown
# CloudHosting SEO & GEO Performance Report — January 2025

## Executive Summary — Overall Performance: Good

| Metric | Jan 2025 | Dec 2024 | Change | Target | Status |
|--------|----------|----------|--------|--------|--------|
| Organic Traffic | 52,100 | 45,200 | +15.3% | 50,000 | On track |
| Keywords Top 10 | 87 | 79 | +8 | 90 | Watch |
| Organic Conversions | 684 | 612 | +11.8% | 700 | Watch |
| Domain Rating | 54 | 53 | +1 | 55 | Watch |
| AI Citations | 18 | 12 | +50.0% | 20 | Watch |

**SEO ROI**: $8,200 invested / $41,040 organic revenue = 400%

**Immediate**: Fix 37 crawl errors on /pricing/ pages
**This Month**: Optimize mobile LCP; publish 3 AI Overview comparison pages
**This Quarter**: Build Wikidata entry for CloudHost Inc.
```

## 成功技巧

1. **以洞察力开头**：先从关键信息开始，而非原始数据。
2. **数据可视化**：使用图表和图形帮助理解数据。
3. **对比不同时间段**：提供上下文使数据更具意义。
4. **包含行动建议**：每份报告都应有助于决策制定。
5. **根据受众定制内容**：高层和管理团队需要的信息与技术团队不同。
6. **关注GEO指标**：AI驱动的可见性越来越重要。

## 参考资料

- [报告输出模板](./references/report-output-templates.md) — 所有11个报告部分的完整输出模板
- [KPI定义](./references/kpi-definitions.md) — SEO/GEO指标的定义，包括基准值、推荐范围、警告阈值、趋势分析方法及数据来源说明
- **按受众分类的报告模板](./references/report-templates.md) — 适用于高层、营销团队和技术团队的报告模板

## 相关技能

- [内容质量审核器](../../cross-cutting/content-quality-auditor/) — 在页面级别将CORE-EEAT评分作为内容质量KPI
- [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) — 在定期报告中将CITE评分作为域名级别的KPI
- [排名跟踪器](../rank-tracker/) — 提供详细的排名数据
- [反向链接分析器](../backlink-analyzer/) — 提供链接概况数据
- [警报管理器](../alert-manager/) — 设置报告触发条件
- [SERP分析](../../research/serp-analysis/) — 提供SERP组成数据
- [内存管理](../../cross-cutting/memory-management/) — 将报告存档到项目内存中
- [实体优化器](../../cross-cutting/entity-optimizer/) — 跟踪品牌搜索和知识面板指标
- [技术SEO检查器](../../optimize/technical-seo-checker/) — 将技术健康数据纳入报告