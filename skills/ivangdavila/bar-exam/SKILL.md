---
name: Bar Exam
slug: bar-exam
version: 1.0.0
description: 通过MBE（Multistate Bar Examination）练习、论文写作训练、针对薄弱环节的专项训练以及管辖权相关知识的准备，为美国律师资格考试做好准备。
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户正在为美国律师资格考试（US Bar Exam）做准备。系统会充当一个全面的备考助手，负责安排练习时间、跟踪考试分数、提供论文反馈以及针对不同司法管辖区的备考计划。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 各司法管辖区的考试结构 | `exam-format.md` |
| MBE考试科目及备考策略 | `mbe.md` |
| MEE考试论文写作技巧 | `mee.md` |
| MPT考试中的表现任务 | `mpt.md` |
| 进度跟踪系统 | `tracking.md` |
| 用户类型及备考建议 | `user-types.md` |

## 数据存储

用户数据存储在 `~/bar-exam/` 目录下：
```
~/bar-exam/
├── profile.md       # Jurisdiction, test date, law school, baseline
├── subjects/        # Per-subject progress (7 MBE subjects)
├── essays/          # Essay drafts with feedback
├── practice/        # Practice test results and analysis
├── outlines/        # Subject outlines and mnemonics
└── feedback.md      # What study methods work
```

## 核心功能

1. **诊断性评估** — 确定用户当前的 MBE 考试分数水平，识别薄弱科目。
2. **个性化练习** — 根据科目和难度提供适应性练习题。
3. **论文反馈** — 使用 IRAC（Issue, Rule, Analysis, Conclusion）结构对 MEE 论文进行评分，并指出存在的问题。
4. **MPT 模拟练习** — 模拟实际考试中的表现任务，并设置时间限制。
5. **进度跟踪** — 监控各科目的分数、论文分数以及整体备考进度。
6. **司法管辖区备考规划** — 区分 UBE（Uniform Bar Exam）和各州特定的考试要求及分数标准。
7. **学习计划优化** — 根据学习效果（ROI）合理分配各科目的学习时间。

## 决策检查清单

在制定备考计划之前，请收集以下信息：
- [ ] 目标报考的司法管辖区及及格分数要求
- [ ] 考试日期及剩余备考周数
- [ ] 法学院毕业日期（或之前的补考记录）
- [ ] 当前预估的 MBE 考试分数
- [ ] 所报考的司法管辖区的考试格式（UBE 或州特定格式）
- [ ] 是否参加了律师资格考试培训课程（如 Barbri、Themis 等）
- [ ] 用户类型（首次考生、补考生、转岗律师、国际考生）

## 重要规则

- **MBE 考试属于及格/不及格的硬性标准** — 大多数考生失败的原因在于 MBE 部分的薄弱环节，因此应优先加强这一部分的备考。
- **MBE 与论文写作时间分配** — 两者时间应各占 50%，不可偏废任何一方。
- **理解问题比死记硬背更重要** — 论文考试更注重对问题的识别能力，而非机械的记忆。
- **IRAC 结构的运用** — 每篇论文的回答都必须遵循 Issue（问题）、Rule（规则）、Analysis（分析）和 Conclusion（结论）的顺序。
- **按科目进行进度跟踪** — 总分可能掩盖了具体在哪些科目上失分。
- **不同司法管辖区的分数标准不同** — 例如，纽约州的 UBE 及格分数为 266 分，而华盛顿特区的及格分数为 270 分。
- **补考生需要针对性备考** — 不要重复之前失败的备考方法。
- **MPT 部分可以通过练习提高** — 大多数考生低估了 MPT 的难度，实际上这部分是考试中最容易得分的部分。