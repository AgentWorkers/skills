---
name: Agency
slug: agency
version: 1.0.1
description: 构建并运营一家服务 agency，具备客户管理、项目跟踪、定价以及团队协调等功能。
metadata: {"clawdbot":{"emoji":"🏢","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## 使用场景

当用户希望成立或扩展服务公司（如市场营销、开发、设计、咨询、内容制作、自动化服务等）时，该文档提供了相应的指导。服务公司负责日常运营，从而让团队能够专注于客户关系和业务策略的制定。

## 快速参考

| 领域 | 对应文件 |
|------|------|
| 客户入职 | `onboarding.md` |
| 定价与提案 | `pricing.md` |
| 项目管理 | `projects.md` |
| 客户沟通 | `communication.md` |
| 交付物工作流程 | `deliverables.md` |
| 团队协作 | `team.md` |
| 服务类型特定说明 | `by-type.md` |
| 学习与反馈系统 | `feedback.md` |

## 工作区结构

所有服务公司的相关数据都存储在 `~/agency/` 目录下：

```
~/agency/
├── clients/           # One file per client
│   ├── index.md       # Client list with status
│   └── [name].md      # Client profile, history, preferences
├── projects/          # Active project tracking
├── templates/         # Reusable proposals, briefs, reports
├── knowledge/         # SOPs, learnings, case studies
└── config.md          # Rates, margins, team structure
```

## 核心运营流程

**客户接洽：**  
- 收到客户简报（音频、邮件、文档形式）  
- 挖掘项目范围、预算和时间表  
- 生成结构化的项目文档  
- 标记潜在问题（如项目范围超出预期、截止日期不现实）  
- 创建客户专属文件夹。

**定价：**  
- 根据项目范围，参考配置文件中的费率表  
- 使用复杂度系数计算估算费用  
- 生成提案PDF文件  
- 与历史类似项目进行对比。

**项目跟踪：**  
- 维护所有活跃项目的统一管理视图  
- 在截止日期前发出提醒  
- 发现项目进展停滞时及时处理  
- 按客户分类生成每周项目进度报告。

**交付物制作：**  
- 将初步笔记或输入内容整理成结构化的交付物  
- 根据项目文档进行审核  
- 根据需要调整交付物的格式。

## 重要规则：  
- 未经上级批准，严禁直接发送提案或与客户沟通  
- 实时跟踪项目实际花费与预算的差异，发现亏损时立即报警  
- 从客户反馈中学习，不断更新模板和知识库  
- 在不同会议中保持对客户情况的了解，参考历史记录。

## 配置文件  

请在 `~/agency/config.md` 文件中配置服务公司的费率、团队结构和利润 margin。具体格式请参考 `pricing.md` 文件。