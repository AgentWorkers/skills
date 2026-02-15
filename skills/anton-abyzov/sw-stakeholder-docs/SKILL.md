---
name: stakeholder-docs
description: 来自技术文档的 executive 文档，包括业务概述、进度仪表板以及功能状态报告。用于与利益相关者进行沟通。
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
context: fork
model: sonnet
---

# 利益相关者文档撰写技能

擅长将技术性文档转化为易于利益相关者、高管和非技术团队成员理解的形式。

## 适用场景

- 制作高管摘要或董事会报告  
- 为管理层生成进度仪表盘  
- 编写业务影响分析报告  
- 创建功能状态概览  
- 准备季度/月度报告  
- 将技术文档翻译为适用于销售或客户端的版本  

## 生成内容  

### 1. 高管摘要  
项目/功能状态的一页概览：  
```markdown
# [Project Name] Executive Summary
*Generated: [Date] | Period: [Sprint/Quarter]*

## Quick Stats

| Metric | Value | Trend |
|--------|-------|-------|
| Features Delivered | 12 | +3 vs last quarter |
| Active Work Items | 8 | On track |
| Test Coverage | 87% | +5% |
| Documentation Currency | 94% | Stable |

## Key Achievements

1. **[Feature A]** - Reduced checkout time by 40%
2. **[Feature B]** - Enabled 3 new enterprise customers
3. **[Feature C]** - Improved system reliability to 99.9%

## Current Focus

- [Active Initiative 1] - ETA: 2 weeks
- [Active Initiative 2] - ETA: 4 weeks

## Risks & Blockers

| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk 1] | Medium | Mitigation plan in place |
| [Blocker 1] | High | Escalated, awaiting decision |

## Next Quarter Priorities

1. [Priority 1] - Business Value: [description]
2. [Priority 2] - Business Value: [description]
```  

### 2. 功能状态仪表盘  
所有功能的可视化进度跟踪：  
```markdown
# Feature Status Dashboard
*Last Updated: [Date]*

## Overall Progress

**Total Features**: 25 | **Completed**: 18 | **In Progress**: 5 | **Blocked**: 2

## Feature Breakdown

### Completed This Quarter

| Feature | Business Impact | Delivered |
|---------|-----------------|-----------|
| User Authentication | Security compliance | Q1 2025 |
| Payment Integration | Revenue enablement | Q1 2025 |

### In Progress

| Feature | Progress | ETA | Owner |
|---------|----------|-----|-------|
| Analytics Dashboard | 75% | Feb 2025 | Team A |
| API v2 | 40% | Mar 2025 | Team B |

### Blocked

| Feature | Blocker | Action Required |
|---------|---------|-----------------|
| Mobile App | Vendor delay | Escalate to CTO |
```  

### 3. 业务影响分析报告  
将每个功能的详细技术信息转化为业务价值：  
```markdown
# Business Impact: [Feature Name]

## Summary

**What**: [One sentence describing the feature]
**Why**: [Business problem solved]
**Who Benefits**: [Target users/customers]

## Business Value

| Metric | Before | After | Impact |
|--------|--------|-------|--------|
| Process Time | 5 min | 30 sec | 90% reduction |
| Error Rate | 5% | 0.1% | 98% reduction |
| Customer Satisfaction | 3.2 | 4.5 | +40% |

## ROI Calculation

- **Investment**: [Development cost]
- **Annual Savings**: [Cost reduction]
- **Revenue Impact**: [Revenue increase]
- **Payback Period**: [Months]

## Success Metrics

1. [Metric 1]: Target [X], Current [Y]
2. [Metric 2]: Target [X], Current [Y]
```  

### 4. 发布摘要  
为利益相关者准备的非技术性发布说明：  
```markdown
# Release [Version] Summary
*Release Date: [Date]*

## Highlights

This release delivers [X] improvements that [business benefit].

## What's New

### For Customers
- **[Feature 1]**: [Customer benefit in plain language]
- **[Feature 2]**: [Customer benefit in plain language]

### For Operations
- **[Improvement 1]**: [Operational benefit]
- **[Improvement 2]**: [Operational benefit]

## Known Limitations

- [Limitation 1] - Workaround: [description]

## Next Release Preview

Coming in [timeframe]: [brief preview of upcoming features]
```  

## 使用方法  

### 数据来源  
我从以下路径读取技术文档并进行转换：  
| 来源          | 输出          |  
|---------------|---------------|  
| `specs/`          | 功能状态仪表盘        |  
| `strategy/`       | 高管摘要        |  
| 增量元数据        | 进度报告        |  
| ADRs（变更请求）      | 风险/决策摘要      |  

### 生成命令  
```bash
# Generate executive summary
"Create an executive summary of our current project status"

# Generate feature dashboard
"Generate a feature status dashboard for Q1"

# Create business impact statement
"Write a business impact statement for the authentication feature"

# Prepare release summary
"Create a stakeholder-friendly release summary for v2.0"
```  

## 最佳实践  

### 应该做：  
1. **使用通俗的语言**——避免专业术语，解释缩写词。  
2. **关注结果**——例如：“等待时间减少了40%”，而非“优化了数据库查询”。  
3. **包含具体数据**——数字能让影响更直观。  
4. **尽早突出风险**——利益相关者需要了解潜在障碍。  
5. **以可视化方式展示进度**——使用表格、百分比和趋势图表。  

### 不应该做：  
1. **不要包含技术细节**——不要包含代码或架构图。  
2. **不要使用开发术语**——例如将“API”替换为“接口”，将“deploy”替换为“发布”。  
3. **不要隐瞒负面信息**——如果存在障碍，应首先说明。  
4. **不要信息过载**——精选关键内容，避免堆积过多数据。  

## 输出保存位置  
生成的文档会保存在：  
```
.specweave/docs/internal/strategy/
├── executive-summary.md      # Overall project summary
├── feature-dashboard.md      # Feature status tracking
├── quarterly-report-Q1.md    # Quarterly summaries
└── business-impact/
    └── [feature-name].md     # Per-feature impact statements
```  

## 与其他工具的集成  
该技能与以下工具配合使用效果最佳：  
- **living-docs-navigator**：用于导航技术文档。  
- **docs-writer**：用于生成详细文档。  
- **image-generation**：用于通过 `/sw:image-generation` 添加图表和可视化内容。  

## 激活关键词  
当您提到以下关键词时，该技能会自动启动：  
- “高管摘要”、“董事会报告”、“投资者更新”  
- “利益相关者”、“非技术性内容”、“业务视角”  
- “进度仪表盘”、“功能状态”  
- “季度报告”、“月度更新”  
- “业务影响”、“投资回报率”、“业务价值”  
- “发布摘要”、“面向客户的文档”