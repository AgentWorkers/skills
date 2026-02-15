---
name: IELTS
slug: ielts
version: 1.0.0
description: 为准备雅思学术类或普通类考试提供支持，包括进度跟踪、薄弱环节分析、目标分数设定以及移民路径指导。
---

## 使用场景

用户正在准备雅思（International English Language Testing System）考试。该工具可作为全面的学习辅助工具，帮助用户进行诊断性评估、练习、分数评估以及目标规划。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 考试结构与评分标准 | `exam-config.md` |
| 进度跟踪系统 | `tracking.md` |
| 学习方法与练习 | `study-methods.md` |
| 根据目的设定分数目标 | `targets.md` |
| 不同用户类型的适配方案 | `user-types.md` |
| 自我提升跟踪 | `feedback.md` |

## 数据存储

用户数据存储在 `~/ielts/` 目录下：
```
~/ielts/
├── profile.md       # Goals, target band, exam date, test type
├── sections/        # Per-section progress (listening, reading, writing, speaking)
├── sessions/        # Study session logs
├── mocks/           # Practice test results and analysis
├── essays/          # Writing samples with feedback
└── speaking/        # Speaking recordings and transcripts
```

## 核心功能

1. **诊断性评估** — 确定当前的语言水平及薄弱环节
2. **分数差距分析** — 比较当前分数与目标分数，计算所需提高的分数
3. **练习生成** — 为各个考试部分生成新的练习任务（图表、作文题目等）
4. **写作评估** — 根据雅思评分标准（Task Achievement, Coherence, Language Range, Grammar and Rhythm）对作文进行评分
5. **口语模拟** — 进行计时模拟面试，并提供反馈
6. **进度跟踪** — 监控分数、学习时间以及进步情况
7. **目标设定指导** — 根据用户目标（大学申请、移民需求等）提供相应的建议

## 决策检查清单

在制定学习计划之前，请收集以下信息：
- [ ] 考试类型：学术类（Academic）还是普通类（General Training）
- [ ] 考试日期及剩余备考时间
- [ ] 目标总分及各部分最低分数要求
- [ ] 学习目的（大学申请、移民、职业注册等）
- [ ] 用户类型（首次考生、复考者、专业人士、学生）
- [ ] 通过诊断性评估或之前的考试所获得的当前预估分数

## 重要规则

- **学术类与普通类考试的区别** — 写作任务1的要求完全不同（学术类要求写图表，普通类要求写信）
- **任何部分不得低于最低分数要求** — 许多目标要求所有部分的分数都达到指定标准（例如，每部分至少6.5分）
- **分数有效期为2年** — 如果移民计划有延迟，需提前规划重考
- **单项技能重考** — 在初次考试后的60天内可申请重考。如果某项技能严重拖低总分，建议及时重考
- **分数描述** — 在提供写作/口语反馈时，请使用官方评分标准，而非个人主观印象