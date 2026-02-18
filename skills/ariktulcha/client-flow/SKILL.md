---
name: client-flow
description: 自动化客户入职流程和项目生命周期管理。通过一条消息，即可创建 Google Drive/Dropbox 项目文件夹结构、生成项目简介、发送模板化的欢迎邮件、在 Google Calendar 上安排启动会议、在 Todoist/ClickUp/Linear/Asana/Notion 中设置任务板、配置跟进提醒，并维护一个包含项目状态跟踪的客户端注册表。该功能适用于以下场景：新客户入职、项目设置、客户信息收集、发送欢迎邮件、安排启动会议、项目启动、客户管理、项目状态监控、查看客户项目概览、项目生命周期跟踪、客户沟通模板、进度更新邮件、项目关闭流程、自由职业者项目管理、代理机构客户管理，或任何涉及设置和跟踪客户项目的工作。一条消息即可替代在电子邮件、日历、文件存储和任务管理工具中花费的 30 分钟手动设置时间。
metadata:
  openclaw:
    emoji: "🤝"
---
# 客户流程

新客户？只需发送一条消息，即可完成全部设置流程。从创建文件夹结构、发送欢迎邮件到安排启动会议——整个过程仅需30秒，而非30分钟。

## 该功能的必要性

客户入职流程是OpenClaw社区中用户反馈最多的功能之一，但ClawHub中却完全没有相关的自动化工具。自由职业者、机构和小企业每次面对新客户时都不得不重复相同的8个步骤：创建文件夹、发送邮件、安排电话会议、设置任务。这个自动化工具可以彻底简化这一流程。

## 入职流程的详细步骤

当收到如下信息时，该功能会自动启动：  
“新客户：Acme Corp，联系人：sarah@acme.com，项目：网站重新设计，预算：1.5万美元，截止日期：3月30日”

该功能会提取提供的所有信息，询问任何缺失的关键信息，然后执行完整的入职流程：

### 第1步：创建项目结构  
为该项目创建一个有组织的文件夹结构：  
```
[Client Name]/
├── 01-Brief/
│   └── project-brief.md (auto-generated from intake info)
├── 02-Contracts/
├── 03-Design/
├── 04-Development/
├── 05-Content/
├── 06-Deliverables/
└── 07-Communications/
    └── meeting-notes/
```  

**存储位置：**  
- **Google Drive**：如果使用`gog`工具，可存储在“Clients”文件夹中  
- **Dropbox**：如果使用Dropbox功能  
- **本地文件系统**：如果在本地运行，可存储在可配置的路径下（默认为`~/Clients/`）  
- **Notion**：如果使用Notion功能，可创建项目页面而非文件夹  

### 第2步：生成项目概述文档  
根据收集到的信息自动生成项目概述文档：  
```markdown
# Project Brief: [Project Name]
**Client**: [Company Name]
**Contact**: [Name] ([Email])
**Start Date**: [Today or specified]
**Deadline**: [Date]
**Budget**: [Amount]

## Project Description
[Generated from user's input — expand into 2-3 sentences]

## Objectives
- [Extracted or inferred from project type]
- [...]

## Deliverables
- [Inferred from project type — e.g., "website redesign" → wireframes, mockups, final site]
- [...]

## Timeline
- Week 1-2: Discovery & Planning
- Week 3-4: [Phase based on project type]
- [...]

## Notes
[Any additional context from the user's message]
```  
将此文档保存到项目文件夹中。  

### 第3步：发送欢迎邮件  
撰写并发送（或草拟）欢迎邮件给客户：  
```
Subject: Welcome to [Your Name/Company] — [Project Name] Kickoff

Hi [Client First Name],

Thank you for choosing to work with us on [Project Name]. I'm excited to get started!

Here's what happens next:
1. I'll send a kickoff meeting invite for [suggested date/time]
2. Please review and sign the project agreement [if applicable]
3. We'll begin the discovery phase right away

If you have any questions before we kick off, don't hesitate to reach out.

Looking forward to working together!

[User's name/signature from memory]
```  
**发送方式：**  
- 如果配置了邮件发送功能，直接发送（需用户确认）  
- 否则，将邮件内容输出供用户手动复制并发送  

### 第4步：安排启动会议  
为启动会议创建日历事件：  
- **时间**：建议在2-3个工作日后举行（或根据用户指定）  
- **时长**：30分钟（默认值，可自定义）  
- **参会人员**：客户联系人 + 用户  
- **标题**："[客户名称] — 项目启动会议"  
- **描述**：包含项目概述和会议议程：  
  ```
  Agenda:
  1. Introductions & project overview (5 min)
  2. Requirements review (10 min)
  3. Timeline & milestones (10 min)
  4. Next steps & action items (5 min)
  ```  
通过`gog`工具使用Google Calendar，或根据配置使用Outlook。  

### 第5步：创建任务管理列表  
在用户偏好的任务管理工具中设置项目任务：  
**对于Todoist / ClickUp / Linear / Asana：**  
创建包含以下默认任务的项目：  
- [ ] 发送合同/协议  
- [ ] 启动会议  
- [ ] 需求收集  
- [ ] 第一次交付物审核  
- [ ] 中期检查  
- [ ] 最终交付  
- [ ] 客户反馈  
- [ ] 项目关闭  

**对于GitHub Issues：**（如果项目涉及技术内容）  
为每个阶段创建里程碑和问题。  

**对于Notion：**（如果使用Notion作为任务管理工具）  
在项目页面中创建任务数据库。  
每个任务的截止日期会根据项目时间线进行估算。  

### 第6步：设置提醒  
配置后续提醒：  
- **启动会议前一天**：提醒用户做好准备  
- **每周检查**：定期提醒用户更新项目进度  
- **里程碑日期**：为每个交付物截止日期设置提醒  
- **截止日期前一周**：发送“最终冲刺”提醒  

使用OpenClaw的定时任务功能或任务管理工具的提醒系统。  

### 第7步：更新客户信息  
维护所有客户和项目的清单：  
```markdown
# Client Registry

| Client | Project | Status | Contact | Start | Deadline | Value |
|--------|---------|--------|---------|-------|----------|-------|
| Acme Corp | Website Redesign | 🟢 Active | sarah@acme.com | Feb 15 | Mar 30 | $15k |
| Beta LLC | Brand Identity | 🟡 In Review | john@beta.io | Jan 20 | Feb 28 | $8k |
| Gamma Inc | Mobile App | ✅ Completed | lisa@gamma.co | Nov 1 | Jan 15 | $25k |
```  
将信息存储在工作区内存中，或作为Markdown文件保存在“Business”文件夹中。  

## 入职后的项目管理  

### 状态检查  
**用户**：“我的项目进展如何？”或“客户状态如何？”  
→ 从客户信息库和任务管理工具中获取数据并生成相应报告：  
```
🤝 Active Projects

1. Acme Corp — Website Redesign
   Status: On track ✅
   Next milestone: First mockup review (Feb 22)
   Outstanding tasks: 3 of 8 completed
   Budget used: ~40%
   
2. Beta LLC — Brand Identity
   Status: Needs attention ⚠️
   Next milestone: Final delivery (Feb 28) — 5 days away
   Outstanding tasks: 2 remaining
   Blocker: Waiting for client feedback since Feb 10
```  

### 客户沟通  
**用户**：“为Acme Corp起草更新邮件”  
→ 根据项目数据生成进度更新邮件：  
- 自上次更新以来已完成的工作  
- 当前状态及下一步计划  
- 客户的任何问题或需求  
- 项目时间线更新  

### 项目关闭  
**用户**：“关闭Beta LLC项目”  
→ 执行项目关闭流程：  
1. 在信息库中标记项目为已完成  
2. 向客户发送感谢邮件  
3. 归档项目文件夹  
4. 创建项目总结笔记  
5. 设置30天的跟进提醒以获取客户评价  
6. 设置90天的跟进提醒以探讨是否有可能再次合作  

## 模板  
将可自定义的模板存储在工作区内存中。虽然提供了默认模板，但用户可以自行修改：  
- **欢迎邮件模板**：调整语气、签名和包含的链接  
- **文件夹结构**：根据项目类型添加或删除文件夹  
- **任务列表**：根据项目类型自定义默认任务  
- **项目类型**：为“网站”、“品牌设计”、“咨询”、“开发”等设置不同的模板  

**用户**：“在为新开发客户入职时，还需添加GitHub仓库设置和Slack频道创建”  
→ 将这些设置保存为“开发”项目类型的模板。  

## 配置  
首次使用时，请设置以下内容：  
1. **业务信息**：公司名称、用户名、邮件签名、时区  
2. **默认工具**：使用的任务管理工具、文件存储服务、日历软件、邮件发送方式  
3. **项目类型**：通常处理的项目类型  
4. **模板**：查看并自定义默认模板  
5. **客户文件夹位置**：项目文件夹的存储位置  

所有设置完成后，只需执行一个命令即可完成新客户的入职流程。  

## 特殊情况处理：  
- **信息不足**：如果用户仅提供“新客户：Acme”这样的信息，要求提供联系邮箱（必填）和项目名称；其他信息可使用默认值。  
- **重复客户**：如果客户名称与现有记录匹配，询问是否是同一客户的新项目；如果是，则将任务添加到现有客户文件夹中，而非创建新文件夹。  
- **未使用任务管理工具**：如果未配置外部任务管理工具，可将任务以清单形式添加到项目概述文档中。  
- **未配置邮件发送功能**：将欢迎邮件内容输出供用户手动发送，但不要跳过此步骤。  
- **国际客户**：在安排会议时需考虑时区差异。  
- **团队项目**：如果涉及多个团队成员，允许将任务分配给不同人员。  
- **预算跟踪**：该功能不负责开票（这是单独的处理事项），但会跟踪预算的预估值与实际支出情况。