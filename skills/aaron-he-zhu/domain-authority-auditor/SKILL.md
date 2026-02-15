---
name: domain-authority-auditor
description: 执行一次全面的 CITE 40 项域名权威性审计，根据域名类型对各个维度进行加权评分。生成一份详细的报告，其中包含每项的得分、维度分析、否决检查结果以及优先级行动计划。
geo-relevance: "medium"
---

# 域名权威性审计工具

> 该工具基于 [CITE 域名评级](https://github.com/aaron-he-zhu/cite-domain-rating) 算法进行评估。完整的基准测试参考文档请参见：[references/cite-domain-rating.md](../../references/cite-domain-rating.md)

该工具通过 40 个标准化指标对域名权威性进行综合评估，这些指标分为 4 个维度。评估结果会生成一份详细的审计报告，包括每个指标的得分、各维度的得分、按域名类型划分的加权总分、存在问题的指标以及优先改进措施。

**相关工具**：[content-quality-auditor](../content-quality-auditor/) 用于页面级别的内容质量评估（共 80 个指标）。这两个工具结合使用，可以完成对域名及其内容的全面评估（共 120 个指标）。

**命名规则说明**：  
- CITE 使用 C01-C10 来表示引用相关指标；CORE-EEAT 使用 C01-C10 来表示上下文清晰度相关指标。在综合评估中，需要在前缀中加上相应的框架名称（例如：CITE-C01 vs CORE-C01），以避免混淆。

## 适用场景  
- 在开展地理定位（GEO）营销活动之前评估域名权威性  
- 将自己的域名与竞争对手进行对比  
- 判断某个域名作为引用来源的可靠性  
- 定期检查域名的健康状况  
- 在进行链接建设活动后评估效果  
- 识别潜在的域名操纵行为（如虚假网站、链接农场、被处罚的历史记录）  
- 制定提升域名权威性的策略  
- 与 [content-quality-auditor] 结合使用，进行全面的 120 项评估  

## 工具功能  
1. **全面评估（40 个指标）**：对每个 CITE 指标进行“通过/部分通过/未通过”的评分  
2. **维度评分**：计算 4 个维度的得分（每个维度 0-100 分）  
3. **加权计算**：根据域名类型为 CITE 得分应用相应的权重  
4. **问题检测**：标记出关键的操纵行为（如 T03、T05、T09）  
5. **优先级排序**：按影响程度排序出需要优先改进的 5 个方面  
6. **制定改进计划**：生成具体可行的改进步骤  
7. **交叉验证**：可选择与 [CORE-EEAT] 结合使用，进行综合诊断  

## 使用方法  
### 审计单个域名  
```
Audit domain authority for [domain]
```  

### 按域名类型进行审计  
```
CITE audit for example.com as an e-commerce site
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

**当连接到以下工具时**：  
- **链接数据库**：自动获取反向链接信息及链接质量数据  
- **SEO 工具**：获取域名权威性评分和关键词排名  
- **AI 监测工具**：获取 AI 引用数据  
- **知识图谱**：获取实体存在信息  
- **品牌监控工具**：获取品牌提及数据  

**仅使用手动数据时**：  
- 用户需提供以下信息：  
  - 需要评估的域名  
  - 域名类型（系统自动检测或用户手动指定：内容发布者、产品与服务、电子商务、社区与用户生成内容、工具与实用工具、权威机构）  
  - 反向链接数据：引用域名的数量、域名权威性、主要链接来源  
  - 流量数据（可来自任何 SEO 工具或 SimilarWeb）  
  - 对比用的竞争对手域名（可选）  

使用提供的数据完成 40 项的全面审计。注意报告中会标注因数据缺失而无法完全评估的指标（如 AI 引用数据、知识图谱查询结果、WHOIS 历史记录等）。  

## 使用说明  
当用户请求域名权威性审计时：  
### 第一步：准备工作  
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
如果发现任何问题指标，请在报告顶部显著标出。无论其他指标得分如何，CITE 的最高得分仅为 39 分（表示域名权威性较低）。  

### 第二步：评估引用相关指标（20 项）  
根据 [references/cite-domain-rating.md](../../references/cite-domain-rating.md) 中的标准对每个指标进行评分：  
- **通过** = 10 分（完全符合标准）  
- **部分通过** = 5 分（部分符合标准）  
- **未通过** = 0 分  

### 第三步：评估信任度和影响力相关指标（20 项）  
评分方式相同。  

**注意**：部分指标需要专门的数据（如 C05-C08 的 AI 引用数据、I01 的知识图谱查询结果、T04-T05 的 IP 分析数据）。对于无法验证的指标，标记为“N/A — 需要 [数据来源]”并排除在维度总分之外。  

### 第四步：计算得分并生成报告  
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

**Score Calculation**:
- CITE Score = C × [w_C] + I × [w_I] + T × [w_T] + E × [w_E]

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
- **输入验证**：  
  - 域名已识别且可访问  
  - 域名类型已确认（系统自动检测或用户手动指定）  
  - 反向链接数据齐全（至少包括引用域名的数量、域名权威性）  
  - 如果进行对比审计，需提供竞争对手的域名信息  

**输出验证**：  
- 所有 40 个指标均已完成评分（或标明“N/A”并说明原因）  
- 所有 4 个维度的得分计算正确  
- 加权后的 CITE 得分与设定的域名类型权重配置一致  
- 三个问题指标均已检查并标记（如有问题）  
- 按影响程度排序出的优先改进事项是合理的  
- 每条建议都是具体且可操作的  
- 行动计划包含具体的步骤及所需时间  

**示例**：  
**用户请求**：**作为内容发布者，审计 cloudhosting.com 的域名权威性**  

**输出结果**：  
```markdown
## CITE Domain Authority Report

### Overview

- **Domain**: cloudhosting.com
- **Domain Type**: Content Publisher
- **Audit Date**: 2025-02-03
- **CITE Score**: 69.9/100 (Medium)
- **Veto Status**: ✅ No triggers

#### Veto Check (Emergency Brake)

| Veto Item | Status | Action |
|-----------|--------|--------|
| T03: Link-Traffic Coherence | ✅ Pass | Link growth correlates with traffic growth |
| T05: Backlink Profile Uniqueness | ✅ Pass | No PBN patterns detected; diverse link sources |
| T09: Penalty & Deindex History | ✅ Pass | No manual actions; clean penalty history |

### Dimension Scores

| Dimension | Score | Rating | Weight | Weighted |
|-----------|-------|--------|--------|----------|
| C — Citation | 72/100 | Medium | 40% | 28.8 |
| I — Identity | 58/100 | Low | 15% | 8.7 |
| T — Trust | 81/100 | Good | 20% | 16.2 |
| E — Eminence | 65/100 | Medium | 25% | 16.25 |
| **CITE Score** | | | | **69.9/100** |

**Score Calculation**:
- CITE Score = 72 × 0.40 + 58 × 0.15 + 81 × 0.20 + 65 × 0.25 = 69.9

**Rating Scale**: 90-100 Excellent | 75-89 Good | 60-74 Medium | 40-59 Low | 0-39 Poor

### Top 5 Priority Improvements

Sorted by: weight × points lost (highest impact first)

1. **I01 Knowledge Graph Presence** — Create entity entry in Google Knowledge Graph
   - Current: Fail | Potential gain: 1.5 weighted points
   - Action: Create Wikidata entry for CloudHost Inc. with P856 (website), P452 (industry), P571 (inception)

2. **C05 AI Citation Volume** — Increase citations in AI-generated answers
   - Current: Partial | Potential gain: 2.0 weighted points
   - Action: Optimize top 10 pages for GEO; add definitive statements AI can quote directly

3. **I03 Brand SERP Control** — Branded SERP shows only 4 of 10 results from owned properties
   - Current: Partial | Potential gain: 0.75 weighted points
   - Action: Claim Google Business Profile; build out social profiles; create CrunchBase entry

4. **E04 Content Freshness Cadence** — 40% of content is >12 months without update
   - Current: Partial | Potential gain: 1.25 weighted points
   - Action: Establish monthly content refresh schedule; prioritize top 20 traffic pages

5. **I05 Schema.org Completeness** — Organization schema missing sameAs, founder, foundingDate
   - Current: Partial | Potential gain: 0.75 weighted points
   - Action: Add complete Organization schema with sameAs links to Wikidata, LinkedIn, CrunchBase

### Action Plan

#### Quick Wins (< 1 week)
- [ ] Add sameAs, founder, and foundingDate to Organization schema
- [ ] Claim Google Business Profile for branded SERP control

#### Medium Effort (1-4 weeks)
- [ ] Create Wikidata entry with complete properties and references
- [ ] Optimize top 10 pages with GEO-friendly definitive statements
- [ ] Create or complete CrunchBase, LinkedIn company page profiles

#### Strategic (1-3 months)
- [ ] Launch monthly content refresh program targeting stale pages
- [ ] Build topical authority through 3-4 pillar content clusters
- [ ] Pursue digital PR to earn mentions on industry publications (TechCrunch, G2)

### Cross-Reference with CORE-EEAT

| Assessment | Score | Rating |
|-----------|-------|--------|
| CITE (Domain) | 69.9/100 | Medium |
| CORE-EEAT (Content) | Run content-quality-auditor on sample pages | — |

**Diagnosis**: Low CITE + unknown CORE-EEAT → Run `/seo:audit-page` on top 5 landing pages to determine whether to prioritize content quality or domain authority first.

### Recommended Next Steps

- For entity building: run [entity-optimizer](../entity-optimizer/) to strengthen I-dimension signals
- For content audit: use [content-quality-auditor](../content-quality-auditor/) on key pages
- For tracking progress: run `/seo:report` with CITE score trends quarterly
```  

**使用建议**：  
1. **优先检查问题指标**（T03、T05、T09）——这些指标可能会影响整体评分结果  
2. **先确定域名类型**——不同类型的域名在评估中的权重不同  
3. **AI 引用指标（C05-C08）对地理定位策略至关重要**——通过相关问题查询 AI 工具进行测试  
4. **部分指标需要专用工具**——如果相关工具未连接，可能需要手动查询知识图谱或分析 IP 数据  
5. **结合使用 CORE-EEAT 进行全面评估**——仅评估域名权威性而忽略内容质量会片面了解实际情况  
6. **每季度重新审计一次**——域名权威性变化较慢，大多数域名类型每季度审计一次即可  
7. **与竞争对手进行对比**——绝对得分不如在行业内的相对排名重要  

**参考资料**：  
- [CITE 域名评级](../../references/cite-domain-rating.md)：包含 40 个评估指标的详细说明、评分标准、权重表及问题指标  

**相关工具**：  
- [content-quality-auditor](../content-quality-auditor/)：用于页面级别的内容质量评估（80 个指标）  
- [backlink-analyzer](../../monitor/backlink-analyzer/)：深入分析反向链接情况  
- [competitor-analysis](../../research/competitor-analysis/)：比较多个域名的 CITE 得分  
- [performance-reporter](../../monitor/performance-reporter/)：跟踪 CITE 得分的趋势变化  
- [geo-content-optimizer](../../build/geo-content-optimizer/)：进行页面级别的地理定位优化  
- [memory-management](../memory-management/)：存储域名审计结果以供后续参考  
- [entity-optimizer](../entity-optimizer/)：评估实体的在线存在情况，补充 CITE 的评估内容