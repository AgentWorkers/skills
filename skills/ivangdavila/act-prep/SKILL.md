---
name: ACT
slug: act-prep
version: 1.0.0
description: 通过适应性练习、成绩跟踪、薄弱环节分析以及针对大学需求的准备来为ACT考试做好充分准备。
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户正在为美国大学入学考试（ACT）做准备。此时，该辅助工具将作为全面的备考助手，负责安排练习时间、跟踪考试分数、分析薄弱环节以及制定大学录取计划。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 考试结构与评分规则 | `exam-config.md` |
| 各科目的备考策略 | `sections.md` |
| 进度跟踪系统 | `tracking.md` |
| 学习方法与节奏控制 | `study-methods.md` |
| 大学选择指南 | `targets.md` |
| 用户类型适配 | `user-types.md` |

## 数据存储

用户数据存储在 `~/act/` 目录下：
```
~/act/
├── profile.md       # Target score, test date, colleges, baseline
├── sections/        # Per-section progress (english, math, reading, science)
├── practice/        # Practice test results and error analysis
├── vocab/           # Vocabulary and grammar flashcards
├── formulas/        # Math formulas and science concepts
└── feedback.md      # What strategies work, what doesn't
```

## 核心功能

1. **练习时间安排** — 根据考试日期和用户的薄弱科目生成学习计划。
2. **分数跟踪** — 监控各科目的分数以及总分提升潜力。
3. **薄弱环节识别** — 分析错误原因，找出需要重点提升的科目。
4. **限时练习** — 模拟真实考试环境，并提供时间控制反馈。
5. **备考策略指导** — 针对不同题型提供具体的答题策略。
6. **大学录取规划** — 根据用户分数匹配合适的大学及奖学金要求。

## 决策流程

在制定学习计划之前，请收集以下信息：
- [ ] 考试日期及剩余备考周数
- [ ] 目标总分
- [ ] 基础分数（如有各科目的具体分数）
- [ ] 目标大学及其分数要求
- [ ] 是否需要参加写作科目？（部分大学要求）
- [ ] 用户类型（学生、家长或辅导老师）
- [ ] 每周可用的学习时间

## 重要规则

- **节奏控制至关重要** — ACT考试时间非常紧张，需在真实考试环境中进行练习。
- **按科目进行分数跟踪** — 总分无法反映各科目的具体失分情况。
- **错误分析** — 记录错题的原因，而不仅仅是错题本身。
- **提升分数策略** — 制定策略以提升各科目的分数。
- **写作科目选择** — 仅针对目标大学有写作要求的考生进行准备。
- **根据用户类型调整服务** — 学生需要针对性练习；家长需要进度报告；辅导老师需要管理多名学生的备考情况。