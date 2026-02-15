---
name: content-quality-auditor
description: '**使用场景：**  
当用户请求“审核内容质量”、“评估EEAT分数”、“进行内容质量检查”、“执行CORE-EEAT审计”、“了解我的内容质量如何”、“我的内容是否足够好以获得排名”、“进行EEAT评估”或“对我的内容质量进行评分”时，可使用该工具。该工具会执行全面的CORE-EEAT内容质量审计，涵盖8个维度，并根据内容类型进行加权评分。最终会生成一份详细报告，其中包含每项内容的得分、维度分析以及优先级的改进措施。  

**功能说明：**  
- 对内容进行全面的质量评估（共80项指标）。  
- 根据内容类型对各项指标进行加权评分。  
- 提供详细的报告，包括每项指标的得分、维度分析以及针对性的改进方案。  

**注意事项：**  
- 针对SEO方面的页面检查，请使用`on-page-seo-auditor`工具。  
- 针对域名级别的评估，请使用`domain-authority-auditor`工具。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - content audit
    - eeat
    - content quality
    - content scoring
    - quality assessment
    - expertise
    - authority
    - trust
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

# 内容质量审核器

> 本工具基于 [CORE-EEAT 内容基准](https://github.com/aaron-he-zhu/core-eeat-content-benchmark)。完整的基准参考请参见：[references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)

> **[SEO 与 GEO 技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含 20 项 SEO 和 GEO 相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部 20 项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP 分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO 内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面 SEO 审核器](../../optimize/on-page-seo-auditor/) · [技术 SEO 检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容复习工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · **内容质量审核器** · **域名权威性审核器** · **实体优化器** · **内存管理**

</details>

该工具根据 80 项标准化标准对内容质量进行评估，这些标准分为 8 个维度。它生成一份全面的审核报告，其中包含每个项目的评分、各维度的评分、按内容类型加权的总分，以及优先级的改进计划。

## 何时使用此技能

- 在发布内容前进行质量审核
- 评估现有内容以寻找改进机会
- 根据 CORE-EEAT 标准对内容进行基准测试
- 与其他竞争者的内容进行质量比较
- 评估内容的 GEO 准备情况（AI 引用潜力）和 SEO 强度（来源可信度）
- 作为内容维护计划的一部分定期进行内容质量检查
- 在使用 seo-content-writer 或 geo-content-optimizer 编写或优化内容后

## 该技能的功能

1. **全面 80 项审核**：对每个 CORE-EEAT 标准项目进行 Pass/Partial/Fail 的评分
2. **维度评分**：计算所有 8 个维度的得分（0-100 分）
3. **系统评分**：计算 GEO 分数（CORE）和 SEO 分数（EEAT）
4. **加权总分**：根据内容类型应用特定的权重
5. **关键违规项检测**：标记出严重的信任违规项（如 T04、C01、R10）
6. **优先级排序**：按影响程度排序出前 5 项需要改进的内容
7. **改进计划**：生成具体的、可操作的改进步骤

## 使用方法

### 审核内容

```
Audit this content against CORE-EEAT: [content text or URL]
```

```
Run a content quality audit on [URL] as a [content type]
```

### 按内容类型进行审核

```
CORE-EEAT audit for this product review: [content]
```

```
Score this how-to guide against the 80-item benchmark: [content]
```

### 对比审核

```
Audit my content vs competitor: [your content] vs [competitor content]
```

## 数据来源

> 有关工具类别的占位符，请参见 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接到 ~~网络爬虫 + ~~SEO 工具时：**
- 自动获取页面内容，提取 HTML 结构，检查架构标记，验证内部/外部链接，并获取竞争对手的内容以供比较。
**仅使用手动数据时：**
- 要求用户提供：
  - 内容文本、URL 或文件路径
  - 内容类型（如果无法自动检测）：产品评论、操作指南、对比文章、着陆页、博客文章、常见问题解答页面、最佳实践或用户评价
  - 可选：用于基准测试的竞争对手内容

使用提供的数据进行全面的 80 项审核。注意在输出中标记出因数据缺失（如反向链接数据、架构标记、站点级信号）而无法完全评估的项目。

## 使用说明

当用户请求内容质量审核时：

### 第 1 步：准备

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

如果任何关键违规项被触发，请在报告顶部显著标出，并建议在继续全面审核之前立即采取行动。

### 第 2 步：CORE 审核（40 项）

根据 [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md) 中的标准评估每个项目。

对每个项目进行评分：
- **Pass** = 10 分（完全符合标准）
- **Partial** = 5 分（部分符合标准）
- **Fail** = 0 分（不符合标准）

```markdown
### C — Contextual Clarity

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| C01 | Intent Alignment | Pass/Partial/Fail | [specific observation] |
| C02 | Direct Answer | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |
| C10 | Semantic Closure | Pass/Partial/Fail | [specific observation] |

**C Score**: [X]/100

### O — Organization

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| O01 | Heading Hierarchy | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**O Score**: [X]/100

### R — Referenceability

[Same format]

**R Score**: [X]/100

### E — Exclusivity

[Same format]

**E Score**: [X]/100
```

### 第 3 步：EEAT 审核（40 项）

Exp、Ept、A、T 维度的评分格式相同。

```markdown
### Exp — Experience

| ID | Check Item | Score | Notes |
|----|-----------|-------|-------|
| Exp01 | First-Person Narrative | Pass/Partial/Fail | [specific observation] |
| ... | ... | ... | ... |

**Exp Score**: [X]/100

### Ept — Expertise
[Same format]

### A — Authority
[Same format]

### T — Trust
[Same format]
```

#### 完整项目参考

| ID | 项目 | ID | 项目 |
|----|------|----|------|
| C01 | 意图一致性 | Exp01 | 第一人称叙述 |
| C02 | 直接答案 | Exp02 | 感官细节 |
| C03 | 查询覆盖范围 | Exp03 | 流程文档 |
| C04 | 定义优先 | Exp04 | 具体证据 |
| C05 | 主题范围 | Exp05 | 使用时长 |
| C06 | 目标受众 | Exp06 | 遇到的问题 |
| C07 | 语义连贯性 | Exp07 | 前后对比 |
| C08 | 用例映射 | Exp08 | 定量指标 |
| C09 | 常见问题解答覆盖 | Exp09 | 重复测试 |
| C10 | 语义完整性 | Exp10 | 承认局限性 |
| O01 | 标题层次结构 | Ept01 | 作者身份 |
| O02 | 摘要框 | Ept02 | 资质展示 |
| O03 | 数据表格 | Ept03 | 专业词汇 |
| O04 | 列表格式 | Ept04 | 技术深度 |
| O05 | 架构标记 | Ept05 | 方法论严谨性 |
| O06 | 部分划分 | Ept06 | 边缘情况意识 |
| O07 | 视觉层次结构 | Ept07 | 历史背景 |
| O08 | 锚点导航 | Ept08 | 推理透明度 |
| O09 | 信息密度 | Ept09 | 跨领域整合 |
| O10 | 多媒体结构 | Ept10 | 编辑流程 |
| R01 | 数据精确性 | A01 | 反向链接概况 |
| R02 | 引用密度 | A02 | 媒体提及 |
| R03 | 来源层次结构 | A03 | 行业奖项 |
| R04 | 证据与声明对应 | A04 | 发表记录 |
| R05 | 方法论透明度 | A05 | 品牌认知 |
| R06 | 时间戳与版本控制 | A06 | 社交证明 |
| R07 | 实体精确性 | A07 | 知识图谱存在 |
| R08 | 内部链接图 | A08 | 实体一致性 |
| R09 | HTML 语义 | A09 | 合作伙伴信号 |
| R10 | 内容一致性 | A10 | 社区地位 |
| E01 | 原始数据 | T01 | 合法合规性 |
| E02 | 新颖框架 | T02 | 联系方式透明度 |
| E03 | 主要研究 | T03 | 安全标准 |
| E04 | 反向观点 | T04 | 公开声明 |
| E05 | 专有视觉元素 | T05 | 编辑政策 |
| E06 | 缺陷填补 | T06 | 更正与更新政策 |
| E07 | 实用工具 | T07 | 广告体验 |
| E08 | 深度优势 | T08 | 风险免责声明 |
| E09 | 综合价值 | T09 | 评论真实性 |
| E10 | 前瞻性见解 | T10 | 客户支持 |

**关于站点级项目**：大多数权威性项目（A01-A10）和一些信任相关项目（T01-T03、T05、T07、T10）需要站点级或组织级数据，这些数据可能无法从单个页面获取。在审核没有站点上下文的独立页面时，将这些项目标记为 “N/A — 需要站点级数据”，并从维度平均值中排除。

### 第 4 步：评分与报告生成

计算得分并生成最终报告：

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

## 验证检查点

### 输入验证
- [ ] 已确定内容来源（文本、URL 或文件路径）
- [ ] 确认内容类型（自动检测或用户指定）
- [ ] 内容足够丰富，可以进行有意义的审核（≥300 字）
- [ ] 如果进行对比审核，也提供了竞争对手的内容

### 输出验证
- [ ] 所有 80 项都已评分（或标明 N/A 及原因）
- [ ] 所有 8 个维度的得分计算正确
- [ ] 加权总分与内容类型配置一致
- [ ] 关键违规项已检查并标记
- [ ] 按加权影响程度排序出前 5 项改进内容，而非随意排序
- [ ] 每条建议都是具体且可操作的（非泛泛而谈）
- [ ] 改进计划包含具体的步骤和所需努力

## 示例

**用户**：“根据 CORE-EEAT 标准审核这篇博客文章：[粘贴 '2025 年最佳远程团队管理工具']”

**输出**（部分示例——展示一个维度以演示格式）：

```markdown
## CORE-EEAT Audit Report

### Overview

- **Content**: "Best Project Management Tools for Remote Teams 2025"
- **Content Type**: Blog Post / Comparison
- **Audit Date**: 2025-06-15
- **Veto Status**: No triggers

### C -- Contextual Clarity (scored dimension example)

| ID  | Check Item         | Score   | Points | Notes                                                       |
|-----|--------------------|---------|--------|-------------------------------------------------------------|
| C01 | Intent Alignment   | Pass    | 10     | Matches "best X" comparison intent; title and body aligned  |
| C02 | Direct Answer      | Partial | 5      | Answer appears in first 300 words but no summary box        |
| C03 | Query Coverage     | Pass    | 10     | Covers "project management tools", "remote team software", "best PM tools" |
| C04 | Definition First   | Pass    | 10     | Key terms ("PM tool", "async collaboration") defined on first use |
| C05 | Topic Scope        | Partial | 5      | States what's covered but not what's excluded               |
| C06 | Audience Targeting | Pass    | 10     | Explicitly targets "remote team leads and managers"         |
| C07 | Semantic Coherence | Pass    | 10     | Logical flow: intro > criteria > tools > comparison > verdict |
| C08 | Use Case Mapping   | Pass    | 10     | Decision matrix for team size, budget, and features         |
| C09 | FAQ Coverage       | Fail    | 0      | No FAQ section despite long-tail potential ("free PM tools for small teams") |
| C10 | Semantic Closure   | Partial | 5      | Conclusion present but doesn't loop back to opening promise |

**C Dimension Score**: 75/100 (Good)
**Blog Post weight for C**: 25%
**Weighted contribution**: 18.75

#### Priority Improvements from C Dimension

1. **C09 FAQ Coverage** -- Add FAQ section with 3-5 long-tail questions
   - Current: Fail (0) | Potential gain: 2.5 weighted points
   - Action: Add FAQ with "Are there free PM tools for small remote teams?", "How to migrate between PM tools?", etc.

2. **C02 Direct Answer** -- Add a summary box above the fold
   - Current: Partial (5) | Potential gain: 1.25 weighted points
   - Action: Insert a "Top 3 Picks" callout box in the first 150 words

[... remaining 7 dimensions (O, R, E, Exp, Ept, A, T) follow the same per-item format ...]
[... then: Dimension Scores table, Top 5 Priority Improvements, Action Plan, Recommended Next Steps ...]
```

## 成功技巧

1. **优先处理关键违规项** — T04、C01、R10 是决定性因素，无论总分如何
   > 这些关键违规项符合 CORE-EEAT 基准（第 3 节），它们可以覆盖整体评分。
2. **关注高权重维度** — 不同类型的内容优先考虑不同的维度
3. **对于 AI 可见性而言，GEO 相关项目最为重要** — 如果目标是 AI 引用，请优先处理标记为 GEO 的项目 🎯
4. **某些 EEAT 项目需要站点级数据** — 不要因为仅在站点层面可观察到的内容（如反向链接、品牌认知）而对其进行扣分
5. **使用加权得分，而不仅仅是原始平均值** — 具有强大独占性的产品评论比具有高权威性的内容更重要
6. **改进后重新审核** — 重新运行审核以验证分数是否有所提升，并发现潜在的退步
7. **结合 CITE 工具获取域名级别的上下文** — 在权威性较低的域名上获得高分数意味着需要不同的优先级；使用 [domain-authority-auditor](../domain-authority-auditor/) 进行全面的 120 项评估

## 参考资料

- [CORE-EEAT 内容基准](../../references/core-eeat-benchmark.md) — 包含全部 80 项的基准测试标准、评分标准以及 GEO 相关项目的标记

## 相关技能

- [domain-authority-auditor](../domain-authority-auditor/) — 域名级别的 CITE 审核（40 项）——用于进行全面 120 项评估的辅助工具
- [seo-content-writer](../../build/seo-content-writer/) — 编写在 CORE 维度上得分较高的内容
- [geo-content-optimizer](../../build/geo-content-optimizer/) — 优化 GEO 相关项目
- [content-refresher](../../optimize/content-refresher/) — 更新内容以改进薄弱维度
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — 技术性的页面内容审核（补充此技能）
- [technical-seo-checker](../../optimize/technical-seo-checker/) — 有助于信任维度的技术信号
- [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) — 用于内容审核的链接质量信号
- [memory-management](../memory-management/) — 存储审核结果以便长期跟踪
- [entity-optimizer](../entity-optimizer/) — 在知识图谱和 AI 系统中检查实体的存在情况
- [performance-reporter](../../monitor/performance-reporter/) — 随时间跟踪内容质量趋势