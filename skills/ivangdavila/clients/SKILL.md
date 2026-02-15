---
name: Clients
description: 构建一个个人客户端系统，用于跟踪人际关系、项目、文档以及相关历史记录。
metadata: {"clawdbot":{"emoji":"💼","os":["linux","darwin","win32"]}}
---

## 核心行为
- 当用户提到某个客户时，主动提供创建或更新客户档案的服务。
- 当用户需要相关背景信息时，展示与该客户相关的历史记录。
- 当用户分享文档时，协助将其与相应的客户关联起来。
- 创建 `~/clients/` 作为工作文件夹。

## 文件结构
```
~/clients/
├── active/
│   └── acme-corp/
│       ├── profile.md
│       ├── projects/
│       ├── documents/
│       ├── communications/
│       └── notes.md
├── past/
├── leads/
└── templates/
```

## 客户文件夹结构
```
acme-corp/
├── profile.md          # Main info, contacts
├── projects/
│   ├── 2024-rebrand/
│   └── 2023-website/
├── documents/
│   ├── contracts/
│   ├── invoices/
│   ├── proposals/
│   └── assets/
├── communications/
│   └── meeting-notes/
└── notes.md            # Quick notes, observations
```

## 客户档案
```markdown
# profile.md
## Company
Acme Corp
Industry: E-commerce
Website: acme.com
Since: 2022

## Contacts
### Primary
Sarah Chen — VP Product
sarah@acme.com | +1 555-0123
Best channel: Slack

### Others
- Mike Torres — Engineering
- Lisa Park — Finance/Invoicing

## Preferences
- Communication: Slack, quick responses
- Meetings: Tuesdays, mornings
- Decisions: Needs CEO approval over $5k

## Key Info
- Payment terms: Net 30
- Timezone: PST
- Fiscal year ends: December
```

## 项目
```markdown
# projects/2024-rebrand/project.md
## Overview
Scope: Full brand refresh
Budget: $25,000
Timeline: Feb - April 2024
Status: In progress

## Milestones
- [x] Discovery
- [x] Brand strategy
- [ ] Visual identity — due Feb 20
- [ ] Guidelines

## Team
- Lead: Sarah
- Stakeholders: CEO, Marketing

## Deliverables
/documents/deliverables/

## Notes
Scope expanded to include motion graphics (+$5k approved)
```

## 文档管理
```
documents/
├── contracts/
│   └── 2024-service-agreement.pdf
├── invoices/
│   ├── INV-2024-001.pdf
│   └── INV-2024-002.pdf
├── proposals/
│   └── rebrand-proposal-v2.pdf
├── assets/
│   └── brand-files/
└── received/
    └── their-materials/
```

## 沟通记录
```markdown
# communications/log.md
## 2024-02-10 — Call with Sarah
- Reviewed wireframes, approved with minor changes
- Budget discussion: approved motion graphics add-on
- Next: send revised timeline by Friday

## 2024-02-03 — Email thread
- Sent proposal v2
- Questions about timeline, addressed
```

## 快速笔记
```markdown
# notes.md
## Observations
- Prefers visual presentations over documents
- CEO is hands-off until final review
- Always pays on time
- Referred two other clients

## To Remember
- Sarah's assistant handles scheduling
- Use project code "ACM24" on invoices
- They close office last week of December
```

## 客户跟进事项
```markdown
# leads/pipeline.md
## Hot
- TechStartup — proposal sent, decision Friday

## Warm
- AgencyXYZ — interested, following up next week

## Cold
- BigCorp — revisit Q3
```

## 需要展示的信息：
- “与 Acme 的最后一次联系是在两周前。”
- “Sarah 更喜欢使用 Slack 进行沟通。”
- “合同将于下个月到期，需要续签。”
- “未结发票金额为 $5,000，已于 15 天前发送。”

## 会议前的准备工作：
- 获取客户的相关背景信息：
  - 当前项目进度
  - 最后一次沟通内容
  - 未完成的事项
  - 客户的沟通偏好

## 需要跟踪的信息：
- 与客户的所有联系记录
- 客户的沟通偏好
- 项目历史记录及结果
- 支付方式
- 重要日期（如合同续签日期、审核日期）

## 逐步改进的步骤：
- 首先：为活跃的客户创建文件夹。
- 添加关键联系人和他们的沟通偏好信息。
- 将相关文档整理到相应的文件夹中。
- 会议结束后记录所有的沟通内容。

## 不应该做的事情：
- 不要将文档随意放置在客户文件夹之外。
- 忘记记录重要的电话沟通。
- 丢失未结发票的信息。
- 错过合同续签的日期。