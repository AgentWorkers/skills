---
name: domain-authority-auditor
version: "3.0.0"
description: '当用户询问“域名权威性审计”、“域名信任评分”、“CITE审计”、“我的网站的权威性如何”、“域名可信度检查”、“我的域名是否可信”或“域名可信度评分”时，应使用此技能。该技能会执行全面的CITE 40项域名权威性审计，根据域名类型对域名进行多维度评分（采用加权评分方式）。最终生成一份详细报告，其中包含每项评分的结果、维度分析、需要重点关注的问题以及优先级的行动计划。如需进行内容层面的评估，请参考“content-quality-auditor”；如需了解链接概况的详细信息，请参考“backlink-analyzer”。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - domain audit
    - credibility
    - domain scoring
    - domain-authority
    - domain-rating
    - domain-trust
    - trust-signals
    - site-authority
    - da-checker
    - ahrefs-dr
    - moz-da
    - cite-framework
    - domain-strength
  triggers:
    - "audit domain authority"
    - "domain trust score"
    - "CITE audit"
    - "how authoritative is my site"
    - "domain credibility check"
    - "domain rating"
    - "site authority"
    - "is my domain trustworthy"
    - "domain credibility score"
---
# 域名权威度审计工具

> 该工具基于 [CITE 域名评级](https://github.com/aaron-he-zhu/cite-domain-rating) 算法进行评估。完整的基准测试参考文档请参见：[references/cite-domain-rating.md](../../references/cite-domain-rating.md)

> **[SEO 与 GEO 技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含 20 项 SEO 和 GEO 相关技能 · 通过命令 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 可轻松安装

<details>
<summary>浏览全部 20 项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP 分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO 内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面 SEO 审计工具](../../optimize/on-page-seo-auditor/) · [技术 SEO 检查工具](../../optimize/technical-seo-checker/) · [内部链接优化工具](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审计工具](../content-quality-auditor/) · **域名权威度审计工具** · [实体优化工具](../entity-optimizer/) · [内存管理工具](../memory-management/)

</details>

该工具通过 40 个标准化指标对域名权威度进行评估，这些指标分为 4 个维度。它生成一份详细的审计报告，包括每个指标的得分、各维度的得分、按域名类型划分的加权得分、需要禁止的操作项以及优先级排序的改进措施。

**关联技能**：[内容质量审计工具](../content-quality-auditor/) 用于评估页面级别的内容（80 项指标）。该工具用于评估内容背后的域名（40 项指标）。两者结合可提供完整的 120 项评估。

> **命名空间说明**：CITE 使用 C01-C10 来标识引用相关指标；CORE-EEAT 使用 C01-C10 来标识上下文清晰度相关指标。在综合评估中，需要在前缀中加上框架名称（例如 CITE-C01 vs CORE-C01）以避免混淆。

## 适用场景

- 在开展 GEO 活动前评估域名权威度
- 将自己的域名与竞争对手进行对比
- 评估某个域名作为引用来源的可靠性
- 定期检查域名健康状况或在链接建设活动后进行评估
- 识别潜在的域名操纵行为（如 PBN、链接农场、处罚记录）
- 与内容质量审计工具结合使用，进行全面的 120 项评估

## 工具功能

1. **全面 40 项审计**：对每个 CITE 指标进行“通过/部分通过/未通过”的评分
2. **维度评分**：计算 4 个维度的得分（每个维度 0-100 分）
3. **加权计算**：根据域名类型为 CITE 得分应用相应的权重
4. **异常检测**：标记关键的操纵行为（如 T03、T05、T09）
5. **优先级排序**：按影响程度排序出最需要改进的 5 项
6. **制定行动计划**：生成具体可行的改进步骤
7. **交叉验证**：可选择与 CORE-EEAT 结合使用，进行综合诊断

## 使用方法

### 审计域名

```
Audit domain authority for [domain]
Run a CITE domain audit on [domain] as a [domain type]
```

### 按域名类型进行审计

```
CITE audit for example.com as an e-commerce site
Score this SaaS domain against the 40-item benchmark: [domain]
```

### 对比审计

```
Compare domain authority: [your domain] vs [competitor 1] vs [competitor 2]
```

### 综合评估

```
Run full 120-item assessment on [domain]: CITE domain audit + CORE-EEAT content audit on [sample pages]
```

## 数据来源

> 有关工具类别的详细信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接了以下工具时：**
- **链接数据库**：自动获取反向链接信息和链接质量数据
- **SEO 工具**：获取域名权威度评分和关键词排名
- **AI 监控工具**：获取 AI 引用数据
- **知识图谱**：获取实体存在信息
- **品牌监控工具**：获取品牌提及数据

**仅使用手动数据时**：
- 请用户提供以下信息：
  - 需要审计的域名
  - 域名类型（如无法自动识别：内容发布者、产品与服务、电子商务、社区与用户生成内容、工具与实用工具、权威机构）
  - 反向链接数据：引用域名的数量、域名权威度、主要链接来源域名
  - 流量数据（可来自任何 SEO 工具或 SimilarWeb）
  - 对比用的竞争对手域名（可选）

使用提供的数据执行全面的 40 项审计。注意报告中哪些指标因数据缺失而无法完全评估（例如 AI 引用数据、知识图谱查询、WHOIS 历史记录）。

## 使用说明

当用户请求域名权威度审计时：

### 第一步：准备

```markdown
### Audit Setup

**Domain**: [domain]
**Domain Type**: [auto-detected or user-specified]
**Dimension Weights**: [from domain-type weight table below]

#### Domain-Type Weight Table

> Canonical source: `references/cite-domain-rating.md`. This inline copy is for convenience.

| Dim | Default | Content Publisher | Product & Service | E-commerce | Community & UGC | Tool & Utility | Authority & Institutional |
|-----|:-------:|:-:|:-:|:-:|:-:|:-:|:-:|
| C | 35% | **40%** | 25% | 20% | 35% | 25% | **45%** |
| I | 20% | 15% | **30%** | 20% | 10% | **30%** | 20% |
| T | 25% | 20% | 25% | **35%** | 25% | 25% | 20% |
| E | 20% | 25% | 20% | 25% | **30%** | 20% | 15% |

#### Veto Check (Emergency Brake)

| Veto Item | Status | Action |
|-----------|--------|--------|
| T03: Link-Traffic Coherence | ✅ Pass / ⚠️ VETO | [If VETO: "Audit backlink profile; disavow toxic links"] |
| T05: Backlink Profile Uniqueness | ✅ Pass / ⚠️ VETO | [If VETO: "Flag as manipulation network; investigate link sources"] |
| T09: Penalty & Deindex History | ✅ Pass / ⚠️ VETO | [If VETO: "Address penalty first; all other optimization is futile"] |
```

如果发现任何需要禁止的操作项，请在报告顶部醒目地标出。无论其他指标得分如何，CITE 得分最高为 39 分（表示权威度较低）。

### 第二步：C + I 部分（20 项指标）

根据 [references/cite-domain-rating.md](../../references/cite-domain-rating.md) 中的标准评估每个指标。

- **通过** = 10 分（完全符合标准）
- **部分通过** = 5 分（部分符合标准）
- **未通过** = 0 分（不符合标准）

```markdown
### C — Citation

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Referring Domains Volume | Pass/Partial/Fail | [specific observation] |
| C02 | Referring Domains Quality | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |
| C10 | Link Source Diversity | Pass/Partial/Fail | [specific observation] |

**C Score**: [X]/100

### I — Identity

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| I01 | Knowledge Graph Presence | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**I Score**: [X]/100
```

### 第三步：T + E 部分（20 项指标）

信任度和声望维度的评估方法相同。

```markdown
### T — Trust

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| T01 | Link Profile Naturalness | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**T Score**: [X]/100

### E — Eminence

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| E01 | Organic Search Visibility | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**E Score**: [X]/100
```

**注意**：部分指标需要专门的数据（如 C05-C08 的 AI 引用数据、I01 的知识图谱查询、T04-T05 的 IP/个人资料分析）。对于无法验证的指标，标记为“N/A — 需要 [数据来源]”并排除在维度平均值计算之外。

### 第四步：评分与生成报告

计算得分并生成最终报告：

```markdown
## CITE Domain Authority Report

### Overview

- **Domain**: [domain]
- **Domain Type**: [type]
- **Audit Date**: [date]
- **CITE Score**: [score]/100 ([rating])
- **Veto Status**: ✅ No triggers / ⚠️ [item] triggered — Score capped at 39

### Dimension Scores

| Dimension | Score | Rating | Weight | Weighted |
|-----------|-------|--------|--------|----------|
| C — Citation | [X]/100 | [rating] | [X]% | [X] |
| I — Identity | [X]/100 | [rating] | [X]% | [X] |
| T — Trust | [X]/100 | [rating] | [X]% | [X] |
| E — Eminence | [X]/100 | [rating] | [X]% | [X] |
| **CITE Score** | | | | **[X]/100** |

**Score Calculation**: CITE Score = C × [w_C] + I × [w_I] + T × [w_T] + E × [w_E]

**Rating Scale**: 90-100 Excellent | 75-89 Good | 60-74 Medium | 40-59 Low | 0-39 Poor

### Per-Item Scores

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Referring Domains Volume | [Pass/Partial/Fail] | [observation] |
| C02 | Referring Domains Quality | [Pass/Partial/Fail] | [observation] |
| ... | ... | ... | ... |
| E10 | Industry Share of Voice | [Pass/Partial/Fail] | [observation] |

### Top 5 Priority Improvements

Sorted by: weight × points lost (highest impact first)

1. **[ID] [Name]** — [specific modification suggestion]
   - Current: [Fail/Partial] | Potential gain: [X] weighted points
   - Action: [concrete step]
2. **[ID] [Name]** — [specific modification suggestion]
   - Current: [Fail/Partial] | Potential gain: [X] weighted points
   - Action: [concrete step]
3–5. [Same format]

### Action Plan

#### Quick Wins (< 1 week)
- [ ] [Action 1]
- [ ] [Action 2]
#### Medium Effort (1-4 weeks)
- [ ] [Action 3]
- [ ] [Action 4]
#### Strategic (1-3 months)
- [ ] [Action 5]
- [ ] [Action 6]

### Cross-Reference with CORE-EEAT

For a complete assessment, pair this CITE audit with a CORE-EEAT content audit:

| Assessment | Score | Rating |
|-----------|-------|--------|
| CITE (Domain) | [X]/100 | [rating] |
| CORE-EEAT (Content) | [Run content-quality-auditor on sample pages] | — |

**Diagnosis Matrix**:
- High CITE + High CORE-EEAT → Maintain and expand
- High CITE + Low CORE-EEAT → Prioritize content quality
- Low CITE + High CORE-EEAT → Build domain authority
- Low CITE + Low CORE-EEAT → Start with content, then domain

### Recommended Next Steps

- For domain authority building: focus on top 5 priorities above
- For content improvement: use [content-quality-auditor](../content-quality-auditor/) on key pages
- For backlink strategy: use [backlink-analyzer](../../monitor/backlink-analyzer/) for detailed link analysis
- For competitor benchmarking: use [competitor-analysis](../../research/competitor-analysis/) with CITE scores
- For tracking progress: run `/seo:report` with CITE score trends
```

## 验证要点

### 输入验证
- 域名已识别且可访问
- 域名类型已确认（自动检测或用户指定）
- 反向链接数据可用（至少包括引用域名的数量、域名权威度）
- 如果进行对比审计，还需提供竞争对手域名

### 输出验证
- 所有 40 项指标均已评分（或标记为 N/A 并说明原因）
- 所有 4 个维度的得分计算正确
- CITE 得分的加权计算符合域名类型的权重设置
- 所有 3 个需要禁止的操作项均已检查并标记
- 最需要改进的 5 项按影响程度排序
- 每条建议都是具体且可操作的
- 行动计划包含具体的步骤和所需的工作量估算

## 示例

请参阅 [references/example-report.md](./references/example-report.md)，其中包含 cloudhosting.com 的完整审计报告，包括禁止操作项的检测结果、各维度得分、需要改进的 5 项、行动计划以及与 CORE-EEAT 的对比结果。

## 使用技巧

1. **优先检查需要禁止的操作项** — T03、T05、T09 可能导致整个评估结果无效
2. **先确定域名类型** — 不同类型的域名在评分中的权重差异很大
3. **AI 引用指标（C05-C08）对 GEO 评估至关重要** — 通过向 AI 工具提出相关问题进行测试
4. **部分指标需要专用工具** — 如果相关工具未连接，知识图谱查询、AI 引用监控和 IP 多样性分析可能需要手动处理
5. **结合 CORE-EEAT 进行全面评估** — 仅评估域名权威度而不考虑内容质量（或反之）只能了解部分情况

## 参考资料

- [CITE 域名评级](../../references/cite-domain-rating.md)：包含完整的 40 项评估标准、维度定义、权重表和禁止操作项
- [references/example-report.md](./references/example-report.md)：包含完整的审计示例报告，包括各维度得分、需要改进的 5 项、行动计划以及与 CORE-EEAT 的对比结果

## 相关技能

- [内容质量审计工具](../content-quality-auditor/)：用于页面级别的内容评估（80 项指标）
- [反向链接分析工具](../../monitor/backlink-analyzer/)：深入分析反向链接信息
- [竞争对手分析工具](../../research/competitor-analysis/)：比较不同竞争对手的 CITE 得分
- [性能报告工具](../../monitor/performance-reporter/)：跟踪 CITE 得分的趋势变化
- [实体优化工具](../entity-optimizer/)：用于评估实体的存在情况，补充 CITE 的 I 维度评估