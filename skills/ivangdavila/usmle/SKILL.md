---
name: USMLE
slug: usmle
version: 1.0.1
description: 通过进度跟踪、薄弱环节分析、题库管理以及住院医师匹配计划来准备美国医学执照考试。
---

## 使用场景

用户正在准备美国医学执照考试（USMLE）。该工具作为全面的学习辅助工具，负责为美国医学博士（US MDs）、骨科医学博士（US DOs）和国际医学毕业生（IMGs）安排学习计划、跟踪学习进度以及规划后续的住院医师培训（residency）事宜。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 考试结构与评分规则 | `exam-config.md` |
| 进度跟踪系统 | `tracking.md` |
| 学习方法与资源 | `study-methods.md` |
| 压力管理与身心健康 | `wellbeing.md` |
| 住院医师培训目标规划 | `targets.md` |
| 用户类型适配 | `user-types.md` |

## 数据存储

用户数据存储在 `~/usmle/` 目录下：
```
~/usmle/
├── profile.md       # Goals, target score, exam dates, user type
├── steps/           # Per-step progress (step1, step2ck, step3)
├── sessions/        # Study session logs
├── assessments/     # NBME, UWorld self-assessments, practice tests
├── qbank/           # Question bank tracking (UWorld, Amboss, etc.)
└── feedback.md      # What works, what doesn't
```

## 核心功能

1. **每日学习计划制定** — 根据考试倒计时及用户的薄弱环节生成个性化的学习计划。
2. **进度跟踪** — 监控用户的总分、学习时间以及各科目的掌握程度。
3. **薄弱环节识别** — 分析错误答案，找出需要重点加强的学习内容。
4. **题库管理** — 记录用户在使用 UWorld、Amboss 等学习平台时的答题情况（完成度、正确率等）。
5. **评估分析** — 解释用户的 NBME/UWSA 考试成绩，并预测其最终分数。
6. **住院医师培训目标规划** — 根据用户成绩预测其适合的专科方向。

## 决策流程

在制定学习计划之前，请收集以下信息：
- [ ] 目标考试阶段（Step 1、Step 2、CK 或 Step 3）
- [ ] 考试日期及剩余备考天数
- [ ] 用户类型（美国医学博士、骨科医学博士、国际医学毕业生或重考生）
- [ ] 目标分数范围或期望报考的专科
- [ ] 当前基础成绩（如有 NBME/UWSA 成绩）
- [ ] 正在使用的学习资源（UWorld、First Aid、Anki 等）

## 重要规则

- **以学习效率为核心** — 优先选择能够帮助用户快速提升成绩的科目。
- **全面记录学习数据** — 将学习过程、成绩及错误答案全部记录到 `~/usmle/` 目录中。
- **根据用户类型调整学习策略**：
  - 美国医学博士需关注 Step 3 的时间安排；
  - 国际医学毕业生需追求最高分数以增强竞争力；
  - 重考生需针对薄弱环节进行针对性复习。
- **注意考试阶段的变化**：
  - 自 2022 年起，Step 1 为及格/不及格考试；Step 2 的成绩对后续住院医师培训至关重要。
- **以实践为主** — 通过实际做题来巩固知识，比被动阅读更有效。
- **关注身心健康** — 避免过度学习导致的压力，确保学习期间有适当的休息和放松时间。