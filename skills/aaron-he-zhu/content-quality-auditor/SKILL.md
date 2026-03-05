---
name: content-quality-auditor
version: "3.0.0"
description: '当用户请求“审核内容质量”、“EEAT评分”、“E-E-A-T审核”、“内容质量检查”、“CORE-EEAT审核”、“有用的内容评估”、“内容的权威性及可信度评估”、“我的内容有多好”、“我的内容是否值得被AI引用”、“内容改进计划”、“有用的内容更新对SEO的影响”或“GEO质量评分”时，应使用此技能。该技能会执行全面的80项CORE-EEAT审核，涵盖8个维度：上下文清晰度（Contextual Clarity）、组织结构（Organization）、可参考性（Referenceability）、独创性（Exclusivity，侧重于GEO领域），以及经验（Experience）、专业知识（Expertise）、权威性（Authoritativeness）和可信度（Trust，侧重于SEO）。审核结果会包括GEO评分、SEO评分、按内容类型加权后的总分、每项内容的通过/部分通过/未通过状态，以及带有优先级排序的修复计划（包含需要特别关注的错误）。有关页面元素SEO审核的详细信息，请参阅on-page-seo-auditor；有关域名权威性的评估，请参阅domain-authority-auditor。'
license: Apache-2.0
allowed-tools: WebFetch
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - e-e-a-t
    - helpful-content
    - content-quality
    - content-scoring
    - ai-quality
    - core-eeat
    - experience-expertise-authoritativeness-trust
    - helpful-content-update
  triggers:
    - "audit content quality"
    - "EEAT score"
    - "content quality check"
    - "CORE-EEAT audit"
    - "how good is my content"
    - "content assessment"
    - "quality score"
    - "is my content good enough to rank"
    - "EEAT check"
    - "rate my content quality"
---
# 内容质量审计器

> 本工具基于 [CORE-EEAT 内容基准](https://github.com/aaron-he-zhu/core-eeat-content-benchmark) 进行内容质量评估。完整基准参考文档请参见：[references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)

> **[SEO 与 GEO 技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含 20 项 SEO 与 GEO 相关技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部 20 项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP 分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO 内容编写器](../../build/seo-content-writer/) · [GEO 内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面 SEO 审计器](../../optimize/on-page-seo-auditor/) · [技术 SEO 检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容刷新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · **内容质量审计器** · **域名权威性审计器** ([domain-authority-auditor]) · [实体优化器](../entity-optimizer/) · [内存管理](../memory-management/)

</details>

该工具根据 8 个维度对内容质量进行综合评估，涵盖 80 项标准化评估标准。它生成详细的审计报告，包括每项内容的评分、各维度的得分、按内容类型加权后的总分，以及优先级的改进措施。

## 适用场景

- 在发布前审计内容质量  
- 评估现有内容以寻找改进机会  
- 根据 CORE-EEAT 标准对内容进行基准测试  
- 与其他竞争对手的内容质量进行比较  
- 评估内容的 GEO 准备情况（AI 引用潜力）和 SEO 实力（来源可信度）  
- 作为内容维护计划的一部分定期进行内容质量检查  
- 在使用 `seo-content-writer` 或 `geo-content-optimizer` 编写或优化内容后  

## 功能概述  

1. **全面审计（80 项）**：对每个 CORE-EEAT 评估项进行“通过/部分通过/未通过”评分  
2. **维度评分**：计算所有 8 个维度的得分（0-100 分）  
3. **系统评分**：计算 GEO 评分（CORE）和 SEO 评分（EEAT）  
4. **加权总分**：根据内容类型应用相应的权重  
5. **关键违规项检测**：标记出严重的信任违规项（如 T04、C01、R10）  
6. **优先级排序**：按影响程度排序出最重要的 5 项改进措施  
7. **制定行动计划**：生成具体且可执行的改进步骤  

## 使用方法  

### 审计内容  
```
Audit this content against CORE-EEAT: [content text or URL]
```  

### 按内容类型进行审计  
```
CORE-EEAT audit for this product review: [content]
```  

### 对比性审计  
```
Score this how-to guide against the 80-item benchmark: [content]
```  

## 数据来源  

> 有关工具类别的详细信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。  

**当连接了 **网络爬虫** 和 **SEO 工具** 时：**  
自动获取页面内容，提取 HTML 结构，验证内部/外部链接，并获取竞争对手的内容以供对比。  

**仅使用手动数据时：**  
要求用户提供：  
1. 内容文本、URL 或文件路径  
2. 内容类型（如无法自动识别）：产品评论、操作指南、对比文章、登录页面、博客文章、常见问题解答页面、精选内容或用户评价  
3. 可选：用于基准测试的竞争对手内容  

使用提供的数据进行全面的 80 项审计。请在输出中注明因数据缺失（如反向链接数据、架构标记、站点级信号）而无法完全评估的项。  

## 使用说明  

当用户请求内容质量审计时：  

### 第一步：准备  
```markdown
### Audit Setup

**Content**: [title or URL]
**Content Type**: [auto-detected or user-specified]
**Dimension Weights**: [loaded from content-type weight table]

#### Veto Check (Emergency Brake)

| Veto Item | Status | Action |
|-----------|--------|--------|
| T04: Disclosure Statements | ✅ Pass / ⚠️ VETO | [If VETO: "Add disclosure banner at page top immediately"] |
| C01: Intent Alignment | ✅ Pass / ⚠️ VETO | [If VETO: "Rewrite title and first paragraph"] |
| R10: Content Consistency | ✅ Pass / ⚠️ VETO | [If VETO: "Verify all data before publishing"] |
```  

如果发现任何关键违规项，请在报告顶部醒目标注，并建议用户立即采取措施后再继续进行完整审计。  

### 第二步：CORE 评估（40 项）  
根据 [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md) 中的标准对每个项目进行评估。  
评分标准如下：  
- **通过** = 10 分（完全符合标准）  
- **部分通过** = 5 分（部分符合标准）  
- **未通过** = 0 分（不符合标准）  
```markdown
### C — Contextual Clarity

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Intent Alignment | Pass/Partial/Fail | [specific observation] |
| C02 | Direct Answer | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |
| C10 | Semantic Closure | Pass/Partial/Fail | [specific observation] |

**C Score**: [X]/100
```  

重复上述表格格式，对 **组织性（O）**、**可引用性（R）** 和 **独创性（E）** 进行评分（每个维度 10 个项目）。  

### 第三步：EEAT 评估（40 项）  
```markdown
### Exp — Experience

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| Exp01 | First-Person Narrative | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**Exp Score**: [X]/100
```  

重复上述表格格式，对 **专业性（Ept）**、**权威性（A）** 和 **信任度（T）** 进行评分（每个维度 10 个项目）。  
详细信息请参阅 [references/item-reference.md](./references/item-reference.md)。  

### 第四步：评分与生成报告  
```markdown
## CORE-EEAT Audit Report

### Overview

- **Content**: [title]
- **Content Type**: [type]
- **Audit Date**: [date]
- **Total Score**: [score]/100 ([rating])
- **GEO Score**: [score]/100 | **SEO Score**: [score]/100
- **Veto Status**: ✅ No triggers / ⚠️ [item] triggered

### Dimension Scores

| Dimension | Score | Rating | Weight | Weighted |
|-----------|-------|--------|--------|----------|
| C — Contextual Clarity | [X]/100 | [rating] | [X]% | [X] |
| O — Organization | [X]/100 | [rating] | [X]% | [X] |
| R — Referenceability | [X]/100 | [rating] | [X]% | [X] |
| E — Exclusivity | [X]/100 | [rating] | [X]% | [X] |
| Exp — Experience | [X]/100 | [rating] | [X]% | [X] |
| Ept — Expertise | [X]/100 | [rating] | [X]% | [X] |
| A — Authority | [X]/100 | [rating] | [X]% | [X] |
| T — Trust | [X]/100 | [rating] | [X]% | [X] |
| **Weighted Total** | | | | **[X]/100** |

**Score Calculation**:
- GEO Score = (C + O + R + E) / 4
- SEO Score = (Exp + Ept + A + T) / 4
- Weighted Score = Σ (dimension_score × content_type_weight)

**Rating Scale**: 90-100 Excellent | 75-89 Good | 60-74 Medium | 40-59 Low | 0-39 Poor

### N/A Item Handling

When an item cannot be evaluated (e.g., A01 Backlink Profile requires site-level data not available):

1. Mark the item as "N/A" with reason
2. Exclude N/A items from the dimension score calculation
3. Dimension Score = (sum of scored items) / (number of scored items x 10) x 100
4. If more than 50% of a dimension's items are N/A, flag the dimension as "Insufficient Data" and exclude it from the weighted total
5. Recalculate weighted total using only dimensions with sufficient data, re-normalizing weights to sum to 100%

**Example**: Authority dimension with 8 N/A items and 2 scored items (A05=8, A07=5):
- Dimension score = (8+5) / (2 x 10) x 100 = 65
- But 8/10 items are N/A (>50%), so flag as "Insufficient Data -- Authority"
- Exclude A dimension from weighted total; redistribute its weight proportionally to remaining dimensions

### Per-Item Scores

#### CORE — Content Body (40 Items)

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Intent Alignment | [Pass/Partial/Fail] | [observation] |
| C02 | Direct Answer | [Pass/Partial/Fail] | [observation] |
| ... | ... | ... | ... |

#### EEAT — Source Credibility (40 Items)

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| Exp01 | First-Person Narrative | [Pass/Partial/Fail] | [observation] |
| ... | ... | ... | ... |

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

#### Quick Wins (< 30 minutes each)
- [ ] [Action 1]
- [ ] [Action 2]

#### Medium Effort (1-2 hours)
- [ ] [Action 3]
- [ ] [Action 4]

#### Strategic (Requires planning)
- [ ] [Action 5]
- [ ] [Action 6]

### Recommended Next Steps

- For full content rewrite: use [seo-content-writer](../../build/seo-content-writer/) with CORE-EEAT constraints
- For GEO optimization: use [geo-content-optimizer](../../build/geo-content-optimizer/) targeting failed GEO-First items
- For content refresh: use [content-refresher](../../optimize/content-refresher/) with weak dimensions as focus
- For technical fixes: run `/seo:check-technical` for site-level issues
```  

## 验证要点  

### 输入验证  
- [ ] 确定了内容来源（文本、URL 或文件路径）  
- [ ] 确认了内容类型（自动检测或用户指定）  
- [ ] 内容长度足够（≥300 字）  
- [ ] 如果进行对比性审计，还需提供竞争对手的内容  

### 输出验证  
- [ ] 所有 80 项均已完成评分（或标明“N/A”并说明原因）  
- [ ] 所有 8 个维度的得分计算正确  
- [ ] 加权总分与内容类型的权重配置一致  
- [ ] 关键违规项已被检测并标记  
- [ ] 按影响程度排序出最重要的 5 项改进措施  
- [ ] 每条建议都具体且可执行  
- [ ] 行动计划包含具体的步骤和所需时间  

## 示例  
请参阅 [references/item-reference.md](./references/item-reference.md)，查看包含所有 10 个维度评分、优先改进措施和加权得分的完整示例报告。  

## 成功技巧  

1. **优先处理关键违规项** — T04、C01、R10 是决定性因素，无论总分如何  
   > 这些违规项符合 CORE-EEAT 基准（第 3 节）的定义，它们会直接影响最终评分。  
2. **关注高权重维度** — 不同类型的内容需要关注不同的维度  
3. **对于 AI 可见性而言，GEO 相关项最为重要** — 如果目标是提高 AI 引用率，请优先处理标记为 GEO 的项目  
4. **某些 EEAT 评估项需要站点级数据** — 不要因仅在站点层面可观察到的因素（如反向链接、品牌知名度）而降低内容评分  
5. **使用加权评分，而不仅仅是原始平均值** — 具有高独创性的产品评论比高权威性的内容更重要  
6. **改进后重新审计** — 重新运行审计以验证评分是否提升并发现潜在问题  
7. **结合 CITE 工具获取域名层面的信息** — 在低权威性域名上获得高内容评分意味着不同的优先级；此时可运行 [domain-authority-auditor](../domain-authority-auditor/) 进行全面的 120 项评估  

## 参考资料  

- [CORE-EEAT 内容基准](../../references/core-eeat-benchmark.md) — 包含 80 项评估标准、维度定义和 GEO 相关项的完整基准  
- [references/item-reference.md](./references/item-reference.md) — 包含所有 80 项的详细信息表、站点级处理说明及评分示例报告  

## 相关技能  

- [domain-authority-auditor](../domain-authority-auditor/) — 域名层面的 CITE 评估（40 项）  
- [seo-content-writer](../../build/seo-content-writer/) — 编写在 CORE 维度上得分较高的内容  
- [geo-content-optimizer](../../build/geo-content-optimizer/) — 优化内容以提高 GEO 相关项的得分  
- [content-refresher](../../optimize/content-refresher/) — 更新内容以提升薄弱维度  
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — 用于技术层面的页面审计（补充本工具的功能）