---
name: Applicant Screening
description: 根据职位要求筛选求职申请，并对候选人进行评分。
author: claude-office-skills
version: "1.0"
tags: [hr, recruitment, hiring, screening, resume]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# 申请人筛选

通过对比职位要求来筛选求职申请，从而高效地确定最佳候选人。

## 概述

此技能可帮助您：
- 根据职位要求评估简历
- 一致地对候选人进行评分
- 区分必备资格和可选资格
- 标记潜在问题
- 对候选人进行面试排序

## 使用方法

### 单个候选人筛选
```
"Screen this resume against our [Job Title] requirements"
"Evaluate this application for the [Position] role"
```

### 批量筛选
```
"Screen these 10 applications for the Senior Developer position"
"Rank these candidates based on our requirements"
```

### 基于特定标准的筛选
```
"Screen for: 5+ years Python, AWS experience required, ML nice-to-have"
```

## 筛选框架

### 要求矩阵
```markdown
## Job Requirements: [Position]

### Must-Have (Required)
| Requirement | Weight | Criteria |
|-------------|--------|----------|
| [Skill 1] | 20% | [X] years experience |
| [Skill 2] | 15% | [Certification/level] |
| [Education] | 10% | [Degree type] |
| [Experience] | 25% | [Industry/role type] |

### Nice-to-Have (Preferred)
| Requirement | Bonus | Criteria |
|-------------|-------|----------|
| [Skill 3] | +5pts | [Description] |
| [Skill 4] | +5pts | [Description] |
| [Trait] | +3pts | [Indicator] |

### Disqualifiers
- [ ] No work authorization
- [ ] Below minimum experience
- [ ] Missing required certification
- [ ] Salary expectation mismatch
```

## 输出格式

### 个人筛选报告
```markdown
# Candidate Screening: [Name]

## Quick Summary
| Attribute | Value |
|-----------|-------|
| **Position** | [Job Title] |
| **Score** | [X]/100 |
| **Recommendation** | 🟢 Interview / 🟡 Maybe / 🔴 Pass |

## Candidate Profile
- **Name**: [Full Name]
- **Location**: [City, State]
- **Current Role**: [Title] at [Company]
- **Total Experience**: [X] years
- **Education**: [Degree, School]

## Requirements Match

### Must-Have Requirements
| Requirement | Met? | Evidence | Score |
|-------------|------|----------|-------|
| [5+ years Python] | ✅ | 7 years at 2 companies | 20/20 |
| [AWS experience] | ✅ | AWS Certified, 3 years | 15/15 |
| [Bachelor's CS] | ✅ | BS Computer Science, MIT | 10/10 |
| [Team lead exp] | ⚠️ | Led 2-person team | 5/10 |

**Must-Have Score**: [X]/[Total]

### Nice-to-Have
| Requirement | Met? | Evidence | Bonus |
|-------------|------|----------|-------|
| [ML experience] | ✅ | Built recommendation system | +5 |
| [Startup exp] | ✅ | 2 early-stage startups | +5 |
| [Open source] | ❌ | Not mentioned | 0 |

**Nice-to-Have Bonus**: +[X] points

## Strengths 💪
1. [Strength 1 with evidence]
2. [Strength 2 with evidence]
3. [Strength 3 with evidence]

## Concerns ⚠️
1. [Concern 1 - question to ask in interview]
2. [Concern 2 - what to verify]

## Red Flags 🚩
- [If any - employment gaps, inconsistencies, etc.]

## Interview Questions
Based on this candidate's profile, consider asking:
1. [Question about specific experience]
2. [Question about concern area]
3. [Question about growth potential]

## Overall Assessment
[2-3 sentence summary of fit]

**Final Score**: [X]/100
**Recommendation**: [Interview / Phone Screen / Pass]
**Priority**: [High / Medium / Low]
```

### 批量排名报告
```markdown
# Applicant Ranking: [Position]

**Date**: [Date]
**Total Applications**: [X]
**Reviewed**: [X]

## Summary
| Category | Count | % |
|----------|-------|---|
| 🟢 Strong Interview | [X] | [%] |
| 🟡 Phone Screen | [X] | [%] |
| 🔵 Maybe/Hold | [X] | [%] |
| 🔴 Not a Fit | [X] | [%] |

## Top Candidates

### 🥇 Tier 1: Strong Interview (Score 80+)

| Rank | Name | Score | Key Strengths | Concerns |
|------|------|-------|---------------|----------|
| 1 | [Name] | 92 | [Strengths] | [Concerns] |
| 2 | [Name] | 88 | [Strengths] | [Concerns] |
| 3 | [Name] | 85 | [Strengths] | [Concerns] |

### 🥈 Tier 2: Phone Screen (Score 65-79)

| Rank | Name | Score | Key Strengths | Gap to Address |
|------|------|-------|---------------|----------------|
| 4 | [Name] | 75 | [Strengths] | [Gap] |
| 5 | [Name] | 72 | [Strengths] | [Gap] |

### 🥉 Tier 3: Maybe/Hold (Score 50-64)

| Name | Score | Reason for Hold |
|------|-------|-----------------|
| [Name] | 58 | [Reason] |

### ❌ Not Proceeding (Score <50)

| Name | Score | Primary Reason |
|------|-------|----------------|
| [Name] | 45 | Missing required [X] |
| [Name] | 38 | Below minimum experience |

## Insights

### Applicant Pool Quality
[Assessment of overall pool quality]

### Common Strengths
- [Frequently seen strength]
- [Frequently seen strength]

### Common Gaps
- [What most candidates lack]
- [Skill shortage in pool]

### Recommendations
1. [Action for top candidates]
2. [Suggestion for sourcing if pool weak]
```

## 评分标准

### 工作经验评分
| 年数 | 初级 | 中级 | 高级 | 领导级 |
|-------|-------|-----|--------|------|
| 0-1年 | 10/10 | 3/10 | 0/10 | 0/10 |
| 2-3年 | 8/10 | 7/10 | 3/10 | 0/10 |
| 4-5年 | 5/10 | 10/10 | 7/10 | 3/10 |
| 6-8年 | 3/10 | 8/10 | 10/10 | 7/10 |
| 9年以上 | 0/10 | 5/10 | 10/10 | 10/10 |

### 教育背景评分
| 学历层次 | 技术岗位 | 非技术岗位 |
|-------|----------------|---------------|
| 博士 | 10/10 | 8/10 |
| 硕士 | 9/10 | 9/10 |
| 学士 | 8/10 | 10/10 |
| 副学士 | 5/10 | 7/10 |
| 培训营 | 6/10 | 不适用 |
| 自学 | 4/10 | 不适用 |

## 最佳实践

### 公平筛选
- 仅关注与职位相关的标准
- 忽略受保护的特征（如种族、性别等）
- 采用一致的评分标准
- 记录所有评分决策
- 考虑候选人的多样化背景

### 偏见意识
- 名称/性别偏见：侧重于候选人的实际能力
- 亲和偏见：组建多元化的面试小组
- 证实偏见：在凭直觉做出评分前先进行客观评估
- 光环效应：单独评估每个评分标准

### 法律考量
- 仅使用与职位相关的标准
- 一致地应用评分标准
- 保留筛选记录
- 由人力资源部门进行审核
- 考虑筛选过程可能带来的负面影响

## 局限性
- 无法核实候选人的工作经历
- 可能无法全面了解非传统背景下的候选人的实际情况
- 评分结果仅供参考，非绝对标准
- 无法完全评估候选人的文化适应能力和软技能
- 最终决策仍需依赖人工判断