---
name: weekly-report
description: 为团队和利益相关者生成一致、专业的每周状态报告。
version: 1.0.0
author: Claude Office Skills Contributors
license: MIT
tags: [productivity, reporting, communication]
---

# 周报

## 概述

本技能可帮助您创建结构清晰、内容一致的周度状态报告，有效向团队、经理或利益相关者传达项目进展、遇到的阻碍以及后续计划。

**使用场景：**
- 个人贡献者的状态更新
- 团队领导的汇总报告
- 项目进度更新
- 高管摘要
- 客户进度报告

## 使用方法

1. 说明您本周完成了哪些工作
2. 分享遇到的阻碍或挑战
3. 描述下周的计划
4. 指定报告的受众（经理、团队、高管或客户）

**示例提示：**
- “为我的经理生成每周状态报告”
- “根据这些个人更新内容生成团队汇总报告”
- “撰写项目进度的 executive summary”
- “起草面向客户的周度更新报告”

## 报告模板

### 个人周报

```markdown
# Weekly Status Report

**Name:** [Your Name]
**Week of:** [Date Range]
**Department/Team:** [Team Name]

## 🎯 Summary
[1-2 sentence highlight of the week]

## ✅ Accomplishments
- [Completed task 1]
- [Completed task 2]
- [Completed task 3]

## 🚧 In Progress
| Task | Status | Expected Completion |
|------|--------|---------------------|
| [Task] | [%] | [Date] |

## 🚫 Blockers
- [Blocker 1] - [Impact] - [Help needed]

## 📅 Next Week's Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## 📊 Key Metrics (if applicable)
| Metric | This Week | Last Week | Target |
|--------|-----------|-----------|--------|
| [KPI] | [Value] | [Value] | [Target] |

## 💬 Notes/FYI
- [Any additional information]
```

### 团队汇总报告

```markdown
# Team Weekly Report

**Team:** [Team Name]
**Week of:** [Date Range]
**Report by:** [Your Name]

## 📊 Team Summary
- **Velocity:** [Points/tasks completed]
- **On Track:** [X] items
- **At Risk:** [X] items
- **Blocked:** [X] items

## 🏆 Key Wins
1. [Major accomplishment 1]
2. [Major accomplishment 2]

## 👥 Individual Updates

### [Team Member 1]
- ✅ [Completed]
- 🔄 [In progress]

### [Team Member 2]
- ✅ [Completed]
- 🔄 [In progress]

## 🚨 Team Blockers
| Blocker | Impact | Owner | Escalation Needed |
|---------|--------|-------|-------------------|
| [Issue] | High/Med/Low | [Name] | Yes/No |

## 📈 Progress Against Goals
| Goal | Target | Current | Status |
|------|--------|---------|--------|
| [Goal] | [Target] | [Current] | 🟢/🟡/🔴 |

## 📅 Next Week Focus
- [Team priority 1]
- [Team priority 2]

## 🆘 Support Needed
- [Request for other teams/management]
```

### 高管摘要报告

```markdown
# Executive Weekly Update

**Project/Initiative:** [Name]
**Week of:** [Date]
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## TL;DR
[2-3 sentences capturing the most important information]

## Key Highlights
- ✅ [Major win or milestone]
- ⚠️ [Key risk or concern]
- 📊 [Important metric or trend]

## Progress vs Plan
| Milestone | Planned | Actual | Variance |
|-----------|---------|--------|----------|
| [Milestone] | [Date] | [Date] | [+/- days] |

## Financial Summary (if applicable)
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| [Category] | $X | $Y | +/-$Z |

## Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Plan] |

## Decisions Needed
- [Decision requiring executive input]

## Next Week Preview
- [Key activities/milestones]
```

### 客户进度报告

```markdown
# Weekly Progress Update

**Project:** [Project Name]
**Client:** [Client Name]
**Week of:** [Date]
**Prepared by:** [Your Name]

---

Dear [Client Name],

Please find below our weekly progress update for [Project Name].

## Summary
[Brief overview of week's progress]

## Completed This Week
- ✅ [Deliverable 1]
- ✅ [Deliverable 2]

## In Progress
| Item | Progress | Expected Delivery |
|------|----------|-------------------|
| [Work item] | [%] | [Date] |

## Upcoming Milestones
| Milestone | Date | Status |
|-----------|------|--------|
| [Milestone] | [Date] | On Track/At Risk |

## Items Requiring Your Input
- [ ] [Decision or feedback needed]
- [ ] [Approval required]

## Next Week's Focus
- [Planned activities]

---

Please let us know if you have any questions or concerns.

Best regards,
[Your Name]
```

## 编写指南

### 成就
- 使用动词开头（已完成、交付、启动、解决）
- 具体说明成果，而不仅仅是活动
- 在可能的情况下量化影响
- 链接到业务价值

**示例：**“将 API 响应时间缩短了 40%，提升了每天 5 万用户的体验”
**示例：**“一直在优化系统性能”

### 障碍
- 明确问题的具体内容
- 说明影响（延误、依赖关系）
- 说明需要哪些帮助
- 包括尝试过的解决方案

**示例：**“正在等待 IT 部门的 API 访问权限（工单编号 #1234）。这阻碍了本周的集成工作。需要向 IT 经理请示。”
**示例：**“无法继续进行集成工作”

### 下周计划
- 根据实际情况制定合理计划
- 确定优先级（前 3-5 项任务）
- 说明依赖关系
- 提及任何风险或假设

## 输出格式

我将根据您的需求生成报告：

```markdown
# [Report Title]

**Period:** [Date range]
**Author:** [Name]
**Audience:** [Manager/Team/Executives/Client]

[Structured content based on template]
```

## 自定义选项

请告知您的偏好：
- **长度**：简短（项目符号形式）、标准格式或详细格式
- **受众**：团队、经理、高管或客户
- **重点**：成就、阻碍或指标
- **频率**：可以每日/每两周/每月生成
- **语气**：非正式的团队更新或正式的利益相关者报告

## 限制

- 无法访问您的实际工作系统或日历
- 报告内容基于您提供的信息
- 可能需要根据您组织的具体格式进行调整
- 在发送前请核对报告的准确性

## 示例

### 示例：快速状态更新

**输入：**“我完成了仪表盘的重设计，修复了 3 个漏洞，目前仍在处理用户身份验证功能，但由于等待安全审查而进度延迟。下周我将专注于完成身份验证功能并开始移动端优化。”

**输出：**

# 周报

**姓名：** [您的姓名]
**周次：** [当前周]

## 🎯 摘要
- 完成了仪表盘重设计的里程碑
- 用户身份验证功能正在进行中，等待安全审查结果

## ✅ 成就
- 完成了仪表盘重设计（UI/UX 里程碑）
- 修复了 3 个生产环境中的漏洞
- 用户身份验证功能开发进展中

## 🚧 进行中
| 任务 | 状态 | 预计完成时间 |
|------|--------|---------------------|
| 用户身份验证功能 | 70% | 等待安全审查结果 |

## 🚫 障碍
- **安全审查待定** – 在安全团队完成审查之前，用户身份验证功能无法部署。影响：延误 2-3 天。*需要采取的行动：与安全团队确认审查时间表。*

## 📅 下周计划
1. 完成用户身份验证功能（安全审查后）
2. 开始移动端优化工作
3. 处理仪表盘重设计中收到的反馈

## 💬 备注
- 仪表盘重设计已完成，可根据需要向利益相关者进行演示