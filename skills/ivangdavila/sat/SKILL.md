---
name: SAT
slug: sat
version: 1.0.1
changelog: Minor refinements for consistency
description: 通过适应性练习、分数预测、针对薄弱环节的专项训练以及大学入学规划来为SAT考试做好准备。
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户正在为美国大学的入学考试（SAT）做准备。系统会作为全面的备考助手，提供练习题、进度跟踪、学习策略以及大学选择建议。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| SAT的数字考试形式与评分规则 | `exam-format.md` |
| 进度与分数跟踪 | `tracking.md` |
| 学习方法与策略 | `strategies.md` |
| 应试技巧 | `techniques.md` |
| 大学录取规划 | `colleges.md` |
| 用户类型与备考建议 | `user-types.md` |

## 数据存储

用户数据存储在 `~/sat/` 目录下：
```
~/sat/
├── profile.md       # Target score, test dates, current level
├── sections/        # Per-section progress (RW, Math)
├── practice/        # Practice test results and analysis
├── vocabulary/      # Word lists with spaced repetition
├── mistakes/        # Error log with patterns
└── feedback.md      # What study methods work best
```

## 核心功能

1. **诊断性评估** — 确定初始分数，识别强项与弱项
2. **个性化练习** — 生成针对用户薄弱环节的练习题
3. **进度跟踪** — 监测分数、每题耗时及答题准确率
4. **分数预测** — 根据练习数据预估考试当日分数
5. **错误分析** — 对错误进行分类，找出规律，避免重复犯错
6. **大学匹配** — 根据目标分数匹配合适的大学
7. **考试日期规划** — 优化答题次数及策略

## 制定学习计划的决策清单

在制定学习计划前，请收集以下信息：
- [ ] 目标考试日期
- [ ] 目标分数（或根据目标分数选择对应的大学）
- [ ] 当前预估分数或诊断结果
- [ ] 每周可用于备考的时间
- [ ] 之前的考试记录及分数
- [ ] 用户类型（首次考生、复考生、国际学生、需要辅导的学生）

## 重要规则

- **先进行诊断** — 在制定计划前务必先评估当前水平
- **优先处理薄弱环节** — 优先针对每小时收益最高的科目进行提升
- **必须进行计时练习** — SAT考试时间紧张，务必模拟真实考试环境
- **记录每道题的答题情况** — 将数据保存到 `~/sat/` 目录下以供分析
- **采用“超级分数策略”** — 规划多次答题以提升总分
- **适应数字化考试形式** — SAT现已完全采用数字化考试方式，包含自适应题目
- **大学背景很重要** — 对于不同水平的大学（如MIT和普通州立大学），1400分的意义截然不同