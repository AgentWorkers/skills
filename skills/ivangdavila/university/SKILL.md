---
name: University
slug: university
version: 1.0.0
description: 用基于人工智能的学位课程、自适应学习系统、考试准备工具以及学习进度跟踪功能来取代或补充传统的大学教育模式。
metadata: {"clawdbot":{"emoji":"🎓","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户可能希望：  
- 通过自学完成整个学位课程或提升职业技能；  
- 辅助现有的大学学习；  
- 为认证考试或职业资格考试做准备；  
- 通过系统化的技能提升来转换职业；  
- 帮助他人学习。  

**系统管理员（Agent）** 的职责是管理整个学习过程，确保学习计划的顺利执行。  

## 快速参考  

| 功能领域 | 对应文件 |  
|------|------|  
| 学位/职业规划 | `degrees.md` |  
| 内容生成 | `content.md` |  
| 评估与考试 | `assessment.md` |  
| 计划与日程管理 | `planning.md` |  
| 进度跟踪 | `tracking.md` |  
| 学习方式 | `formats.md` |  
| 学习偏好设置 | `feedback.md` |  

## 工作区结构  

所有学习数据都存储在 `~/university/` 目录下：  

```
~/university/
├── degrees/              # One folder per degree/career/certification
│   ├── index.md          # Active degrees list with status
│   └── [degree-name]/    # Per-degree folder
│       ├── curriculum.md # Full curriculum with modules
│       ├── progress.md   # Module completion, mastery levels
│       ├── calendar.md   # Exam dates, deadlines, milestones
│       └── modules/      # Study materials by module
├── resources/            # Uploaded PDFs, slides, recordings
├── exams/               # Test history, practice exams
├── flashcards/          # Spaced repetition card sets
└── config.md            # Study preferences, schedule, goals
```