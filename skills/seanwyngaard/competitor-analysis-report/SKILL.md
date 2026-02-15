---
name: competitor-analysis-report
description: 生成结构化的竞争分析报告，内容包括功能对比、价格分析、SWOT分析以及战略建议。这些报告可用于分析竞争对手、撰写市场研究报告或为客户提供竞争情报。
argument-hint: "[business-or-product] [competitor1] [competitor2] [competitor3]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch
---

# 竞争对手分析报告

本工具可生成专业的、适合客户使用的竞争对手分析报告。报告内容包括对竞争对手的研究、功能与定价的对比、SWOT分析以及具有实际操作意义的建议。

## 使用方法

```
/competitor-analysis-report "Notion" "Obsidian" "Coda" "Roam Research"
/competitor-analysis-report "My SaaS product" --competitors "Competitor A, Competitor B, Competitor C"
/competitor-analysis-report brief.txt
```

- `$ARGUMENTS[0]`：需要分析的主要业务/产品（可以是客户的产品或目标公司）
- 其余参数：2-5个需要分析的竞争对手

## 报告生成流程

### 第一步：研究每个竞争对手

对于每个公司/产品，收集以下信息：
- **产品概述**：该公司的业务范围及目标客户群体
- **功能**：核心功能与能力
- **定价**：定价方案、价格层级及免费试用选项
- **目标受众**：市场定位
- **市场定位**：公司的自我描述（标语、价值主张）
- **优势**：公司的核心竞争力
- **劣势**：常见的反馈、存在的不足或负面评价
- **近期变化**：新功能、价格调整或业务方向调整

请仅使用网络搜索和公开可获取的信息进行调研。

### 第二步：生成报告

报告的结构如下：

```markdown
# Competitive Analysis Report
**Prepared for**: [Client/Product Name]
**Date**: [Today's date]
**Competitors Analyzed**: [List]

---

## Executive Summary
[3-5 sentence overview of the competitive landscape.
Key finding. Biggest opportunity. Primary threat.]

---

## Competitor Profiles

### [Competitor 1]
- **Founded**: [Year]
- **Headquarters**: [Location]
- **Positioning**: "[Their tagline or value prop]"
- **Target Market**: [Who they serve]
- **Key Differentiator**: [What makes them unique]

[Repeat for each competitor]

---

## Feature Comparison Matrix

| Feature | [Your Product] | [Comp 1] | [Comp 2] | [Comp 3] |
|---------|---------------|----------|----------|----------|
| [Feature 1] | ✅ | ✅ | ❌ | ✅ |
| [Feature 2] | ✅ | ✅ | ✅ | ❌ |
| [Feature 3] | ❌ | ✅ | ✅ | ✅ |
| ... | | | | |

**Key Takeaway**: [1-2 sentences on where you lead and lag]

---

## Pricing Analysis

| Plan | [Your Product] | [Comp 1] | [Comp 2] | [Comp 3] |
|------|---------------|----------|----------|----------|
| Free Tier | [Details] | [Details] | [Details] | [Details] |
| Basic/Starter | $X/mo | $X/mo | $X/mo | $X/mo |
| Professional | $X/mo | $X/mo | $X/mo | $X/mo |
| Enterprise | Custom | Custom | $X/mo | Custom |

**Price Positioning**: [Where client sits relative to market — premium, mid-market, value]
**Key Takeaway**: [Pricing opportunity or risk]

---

## SWOT Analysis

For each competitor:

### [Competitor 1] SWOT

| Strengths | Weaknesses |
|-----------|------------|
| • [Point] | • [Point] |
| • [Point] | • [Point] |

| Opportunities | Threats |
|--------------|---------|
| • [Point] | • [Point] |
| • [Point] | • [Point] |

---

## Market Positioning Map

```
                    高价          │
          企业级        │    高端版
          [竞争对手3]     │    [您]
                        │
   低价          ─────────────────┼───────────────── 高价
   功能          │              功能
                        │
          经济型        │    最高性价比
          [竞争对手2]     │    [您]
                        │
                    低价          │
```

---

## Opportunities & Threats

### Opportunities (Where You Can Win)
1. **[Gap in competitor offerings]**: [How to exploit it]
2. **[Underserved segment]**: [How to capture it]
3. **[Competitor weakness]**: [How to position against it]

### Threats (What to Watch)
1. **[Competitor advantage]**: [How to defend against it]
2. **[Market trend]**: [How it could impact you]
3. **[New entrant risk]**: [Who might enter the space]

---

## Strategic Recommendations

### Immediate Actions (Next 30 Days)
1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]

### Medium-Term (Next Quarter)
1. [Strategic initiative]
2. [Feature/positioning change]

### Long-Term (Next 6-12 Months)
1. [Market positioning play]
2. [Competitive moat building]

---

## Appendix
- Data sources and methodology
- Detailed feature descriptions
- Competitor screenshots/examples (described, not included)
```

### 第三步：输出报告

将生成的报告保存到 `output/competitor-analysis/` 目录下：

```
output/competitor-analysis/
  report.md                    # Full report in Markdown
  report.html                  # Professional HTML version
  executive-summary.md         # Standalone exec summary (1 page)
  feature-matrix.csv           # Spreadsheet-ready comparison
```

HTML版本的报告应具备以下特点：
- 专业的排版（清晰的字体、带边框的表格）
- 适合打印的布局
- 带有锚链接的目录
- 主要章节之间有分页

## 质量标准
- 所有数据均来自公开来源
- 功能对比至少涵盖10个关键方面
- 定价信息最新且准确
- SWOT分析每个方面至少包含3个要点
- 建议具体且具有可操作性（避免泛泛而谈）
- 执行摘要可独立使用（客户可将其直接发送给上级）
- 不将猜测内容当作事实呈现——明确标注假设内容
- 报告格式专业，适合向利益相关者展示