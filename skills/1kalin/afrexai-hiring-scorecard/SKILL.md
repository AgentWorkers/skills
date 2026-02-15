# 招聘评分卡功能

使用加权标准客观地评估和比较求职者，避免基于直觉的招聘决策。

## 使用方法

告诉您的招聘助手：“为[职位]对这位候选人进行评分”或“比较这3位后端工程师职位的候选人”。

## 工作原理

1. **定义职位**—— 提供职位名称和关键要求
2. **设置评分标准**—— 招聘助手会使用6个默认维度（您也可以自定义）：
   - 技术能力（权重：25%）
   - 相关经验（权重：20%）
   - 企业文化匹配度（权重：15%）
   - 沟通能力（权重：15%）
   - 解决问题的能力（权重：15%）
   - 发展潜力（权重：10%）
3. **对候选人进行评分**—— 每个维度根据面试/评估结果给出1-5分的评分
4. **计算加权总分**—— 根据评分结果给出“录用”或“不录用”的建议

## 命令

- `score candidate [姓名] for [职位]` — 开始一个新的评分卡
- `add criterion [名称] weight [%]` — 自定义评分维度
- `compare candidates` — 进行并排排名比较
- `hiring summary` — 获取包含建议的执行摘要

## 评分卡模板

```markdown
# Candidate Scorecard: [Name]
**Role:** [Title]
**Date:** [Date]
**Interviewer:** [Name]

| Criterion | Weight | Score (1-5) | Weighted |
|-----------|--------|-------------|----------|
| Technical Skills | 25% | _ | _ |
| Relevant Experience | 20% | _ | _ |
| Culture Fit | 15% | _ | _ |
| Communication | 15% | _ | _ |
| Problem Solving | 15% | _ | _ |
| Growth Potential | 10% | _ | _ |
| **TOTAL** | **100%** | | **_/5.0** |

### Notes
- Strengths:
- Concerns:
- Recommendation: HIRE / NO HIRE / MAYBE

### Scoring Guide
5 = Exceptional — top 5% of candidates seen
4 = Strong — clearly above average
3 = Meets bar — would do the job well
2 = Below bar — notable gaps
1 = Not a fit — significant concerns
```

## 提示

- 在每次面试后尽快评分，以便印象更清晰
- 让多名面试官独立评分后再进行比较
- 根据职位调整各维度的权重（例如，将技术能力的权重提高到40%（针对高级工程师）
- 随时间跟踪评分结果，以调整招聘标准

## 更多业务工具

在[AfrexAI](https://afrexai-cto.github.io/context-packs/)获取行业特定的AI助手配置包—— 为招聘、销售、运营等场景提供预先构建的配置方案。直接使用即可。