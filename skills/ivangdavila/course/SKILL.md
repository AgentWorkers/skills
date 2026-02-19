---
name: Course
slug: course
version: 1.0.1
changelog: Minor refinements for consistency
description: 创建、发布并管理在线或面授课程，包括课程设计、内容制作、营销自动化以及学生互动功能。
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户希望实现以下目标：  
- 利用自身专业知识创建课程以实现盈利；  
- 将现有资料转换为在线格式；  
- 发布并销售课程；  
- 管理学生并跟踪他们的学习进度；  
- 对现有课程进行改进。  
该方案适用于在线、面授或混合教学模式。  

**不适用场景**：  
- 以学生身份参加课程（请使用 `university` 或 `school` 相关方案）；  
- 无明确课程结构的常规教学活动；  
- 仅用于企业合规性培训的培训项目。  

## 快速参考  

| 功能领域 | 对应文件 |  
|------|------|  
| 针对特定受众的工作流程 | `by-audience.md` |  
| 课程设计与内容制作 | `content.md` |  
| 视频、幻灯片、资料制作 | `production.md` |  
| 课程发布与销售推广 | `marketing.md` |  
| 学生支持与社区管理 | `students.md` |  
| 数据分析与课程优化 | `analytics.md` |  

## 工作区结构  

所有课程数据存储在 `~/courses/` 目录下：  

```
~/courses/
├── [course-name]/           # One folder per course
│   ├── curriculum.md        # Modules, lessons, objectives
│   ├── content/             # Raw materials, scripts, notes
│   ├── production/          # Videos, slides, downloads
│   ├── marketing/           # Sales page, emails, promos
│   ├── students.md          # Enrollment, progress tracking
│   └── analytics.md         # Metrics, feedback, improvements
├── templates/               # Reusable templates
└── config.md                # Platforms, integrations, defaults
```