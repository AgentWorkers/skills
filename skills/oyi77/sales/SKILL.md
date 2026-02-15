---
name: sales
version: 1.0.0
description: "CRM集成、潜在客户跟踪、外联自动化以及销售流程管理——将这些功能结合起来，就能将您的人工智能助手转变为一个不会让任何潜在客户错失的完美销售助手。"
author: openclaw
---

# 销售技能 💼

**将您的人工智能代理打造成精英级的销售运营伙伴。**

跟踪潜在客户、管理销售流程、自动化外联工作，再也不会因为跟进不及时而错失任何交易机会。

---

## 该技能的功能

✅ **潜在客户跟踪** — 通过销售流程捕捉、评估并跟踪潜在客户
✅ **CRM集成** — 与现有的CRM系统配合使用，或利用内置的跟踪功能
✅ **外联自动化** — 生成个性化的沟通方案
✅ **销售流程管理** — 跟踪交易进展、预测收入、识别瓶颈
✅ **跟进自动化** — 确保不会错过任何一次跟进机会
✅ **销售分析** — 监控转化率、销售速度以及成交/失败的原因

---

## 快速入门

1. 设置您的销售工作空间：
```bash
./scripts/sales-init.sh
```

2. 在 `TOOLS.md` 中配置您的偏好设置：
```markdown
### Sales
- CRM: [HubSpot/Salesforce/Notion/Built-in]
- Default pipeline stages: [Stages]
- Follow-up cadence: [Days between touchpoints]
- Meeting booking link: [URL]
```

3. 开始跟踪潜在客户吧！

---

## 潜在客户管理

### 潜在客户评估框架（BANT）

| 评估标准 | 问题 | 权重 |
|----------|----------|--------|
| **预算** | 他们是否有足够的预算？ | 25% |
| **决策权** | 他们是否拥有决策权？ | 25% |
| **需求** | 他们是否真的有您能解决的需求？ | 30% |
| **时间表** | 他们何时需要解决方案？ | 20% |

**潜在客户评分阈值：**
- 80-100：高热度 🔥 — 立即联系
- 60-79：中等热度 — 积极跟进
- 40-59：低热度 — 继续培养关系
- 0-39：低优先级

### 潜在客户捕获模板
```markdown
# Lead: [Company Name]

## Contact Info
- **Name:** [Full Name]
- **Title:** [Job Title]
- **Email:** [Email]
- **Phone:** [Phone]
- **LinkedIn:** [URL]
- **Company:** [Company]
- **Website:** [URL]

## Qualification (BANT)
- **Budget:** [Yes/No/Unknown] — [Notes]
- **Authority:** [Decision-maker/Influencer/User] — [Notes]
- **Need:** [Strong/Moderate/Weak] — [Notes]
- **Timeline:** [Immediate/1-3mo/3-6mo/6mo+] — [Notes]
- **Lead Score:** [X/100]

## Source
- **How they found us:** [Source]
- **First touchpoint:** [Date]
- **Initial interest:** [What they asked about]

## Notes
[Relevant context, pain points, opportunities]

## Next Action
- [ ] [Action] — Due: [Date]
```

---

## 销售流程管理

### 标准销售流程阶段

| 阶段 | 定义 | 常见操作 |
|-------|------------|-----------------|
| **潜在客户** | 初次接触，尚未评估 | 评估需求、进行初步沟通 |
| **评估通过** | 符合BANT标准 | 进行需求分析 |
| **需求发现** | 了解客户需求 | 准备演示材料、识别相关利益相关者 |
| **演示/提案** | 展示解决方案 | 提交演示文稿、制定提案 |
| **谈判** | 协商条款 | 处理异议、进行谈判 |
| **成交** | 交易达成 | 完成交接流程 |
| **失败** | 交易失败 | 分析失败原因、继续跟进 |

### 销售流程跟踪模板
```markdown
# Sales Pipeline — [Month]

## Summary
- Total pipeline value: $[X]
- Weighted pipeline: $[X]
- Deals in pipeline: [X]
- Expected closes this month: [X]

## By Stage

### Lead ([X] deals, $[X])
| Company | Value | Owner | Last Activity | Next Step |
|---------|-------|-------|---------------|-----------|
| [Name] | $[X] | [You] | [Date] | [Action] |

### Qualified ([X] deals, $[X])
...

### Demo/Proposal ([X] deals, $[X])
...

### Negotiation ([X] deals, $[X])
...

## Stale Deals (>14 days no activity)
| Company | Stage | Last Activity | Recommended Action |
|---------|-------|---------------|-------------------|
```

### 销售流程效率指标

| 指标 | 计算方法 | 目标值 |
|--------|------------------|--------|
| **成交率** | 成交数 ÷ (成交数 + 失败数) | >25% |
| **平均交易额** | 总成交额 ÷ 成交数 | 跟踪趋势 |
| **销售周期** | 从潜在客户到成交的平均天数 | <30天 |
| **销售流程覆盖率** | 销售流程数量 ÷ 销售配额 | ≥3倍 |

---

## 外联自动化

### 冷启动（初次联系）流程

**第1天：初次邮件**
```
Subject: [Personalized hook based on research]

Hi [Name],

[Observation about their company/role — show you did research].

[One sentence about what you do and why it's relevant to them].

[Specific question or soft CTA].

Best,
[Your name]
```

**第3天：第一次跟进**
```
Subject: Re: [Original subject]

Hi [Name],

Wanted to make sure this didn't get buried — [brief restate of value].

[New angle or additional value point].

Worth a quick chat?

[Your name]
```

**第7天：第二次跟进（提供额外价值）**
```
Subject: [Related resource or insight]

Hi [Name],

Found this [article/resource/insight] and thought of you: [link]

[Brief explanation of why it's relevant].

If this resonates, happy to share how we helped [similar company] with [similar challenge].

[Your name]
```

**第14天：结束邮件**
```
Subject: Should I close your file?

Hi [Name],

I haven't heard back, so I'm assuming the timing isn't right.

No worries — I'll close out my notes for now.

If things change, feel free to reply anytime.

[Your name]
```

### 个性化信息收集清单

在开始外联之前，请收集以下信息：
- [ ] 公司的最新动态（融资、新产品发布、人员变动）
- [ ] 该公司在LinkedIn上的活动（帖子、评论、点赞）
- [ ] 公司的博客/新闻通讯
- [ ] 与您的潜在客户之间的共同联系人
- [ ] 如果相关的话，他们的技术栈信息
- [ ] 他们可能使用的竞争对手产品

---

## 进销系统

### 确保不错过任何一次跟进

**规则：** 每笔交易都有明确的下一步行动和截止日期。没有例外。

**不同阶段的跟进频率：**
| 阶段 | 进度检查频率 |
|-------|--------------------|
| 潜在客户 | 每3-5天 |
| 评估通过的客户 | 每2-3天 |
| 进行演示/提案的客户 | 每1-2天 |
| 谈判中的客户 | 每天 |

### 进销提醒模板
```markdown
# Daily Follow-up Queue

## Due Today
| Lead | Stage | Last Contact | Reason | Next Action |
|------|-------|--------------|--------|-------------|
| [Co] | [Stage] | [Date] | [Context] | [Action] |

## Overdue
| Lead | Stage | Days Overdue | Priority |
|------|-------|--------------|----------|
| [Co] | [Stage] | [X] days | 🔥/⚠️ |
```

## 会议管理

### 会议前准备模板
```markdown
# Meeting Prep: [Company]
**Date:** [Date/Time]
**Attendees:** [Names, titles]

## Company Research
- Founded: [Year]
- Size: [Employees]
- Funding: [Stage/Amount]
- Recent news: [Key items]

## Attendee Research
- [Name 1]: [Background, relevant info]
- [Name 2]: [Background, relevant info]

## Their Likely Pain Points
1. [Pain point based on research]
2. [Pain point based on research]

## Questions to Ask
1. [Discovery question]
2. [Discovery question]
3. [Qualification question]

## Our Value Proposition for Them
[Customized pitch based on research]

## Objections to Expect
1. [Likely objection] → [Response]
2. [Likely objection] → [Response]

## Meeting Goals
1. [Specific goal]
2. [Specific goal]
```

### 会议后记录模板
```markdown
# Meeting Notes: [Company] — [Date]

## Attendees
- [Name, Title]

## Key Takeaways
1. [Insight]
2. [Insight]

## Pain Points Confirmed
- [Pain point]

## Decision Process
- Decision maker: [Name]
- Influencers: [Names]
- Timeline: [When]
- Budget: [Range if discussed]

## Objections Raised
- [Objection]: [How we handled it]

## Next Steps
- [ ] [Action] — Owner: [Name] — Due: [Date]
- [ ] [Action] — Owner: [Name] — Due: [Date]

## Follow-up Email
[Draft the follow-up email here]
```

---

## 异议处理

### 常见异议及应对策略

| 异议 | 应对方法 |
|-----------|-------------------|
| **“价格太贵”** | 强调价值与成本：“如果不解决这个问题，会带来多大的损失？” |
| **“我们使用竞争对手的产品”** | “您为什么选择他们？他们的产品有哪些优点/缺点？” |
| **“现在不是合适的时机”** | “什么时间会合适？我们可以再联系吗？” |
| **“需要考虑一下”** | “当然可以。您具体想了解哪些方面？” |
| **“请发送相关信息给我”** | “很乐意提供。您希望看到哪些具体信息？” |
| **“我们的公司规模太小”** | “实际上，这正是我们的优势。[举例说明类似客户的成功案例]”

### 异议记录

记录客户提出的异议，以便优化销售策略：
```markdown
# Objection Log

| Date | Company | Objection | Our Response | Result |
|------|---------|-----------|--------------|--------|
| [Date] | [Co] | [Objection] | [Response] | Won/Lost |
```

## 销售分析

### 周销售报告模板
```markdown
# Sales Report — Week of [Date]

## Summary
- New leads: [X]
- Deals advanced: [X]
- Deals closed won: [X] ($[X])
- Deals closed lost: [X]

## Pipeline Health
- Total pipeline: $[X]
- Change from last week: +/-[X]%
- Weighted pipeline: $[X]
- Forecast this month: $[X]

## Activity Metrics
- Outreach sent: [X]
- Meetings held: [X]
- Proposals sent: [X]
- Follow-ups completed: [X]

## Wins
| Company | Value | Time to Close | Key Factor |
|---------|-------|---------------|------------|
| [Name] | $[X] | [X] days | [What won it] |

## Losses
| Company | Value | Stage Lost | Reason |
|---------|-------|------------|--------|
| [Name] | $[X] | [Stage] | [Why] |

## Focus for Next Week
1. [Priority]
2. [Priority]
```

### 成交/失败分析
```markdown
# Win/Loss Analysis — [Quarter]

## Win Patterns
- Common traits of won deals: [Patterns]
- Average deal size: $[X]
- Average sales cycle: [X] days
- Top win reasons:
  1. [Reason]
  2. [Reason]

## Loss Patterns
- Where deals die: [Stage]
- Common objections: [List]
- Top loss reasons:
  1. [Reason]
  2. [Reason]

## Insights & Actions
- [Insight] → [Action to take]
```

---

## 脚本

### sales-init.sh
使用模板和跟踪工具初始化您的销售工作空间。

### lead-tracker.sh
用于快速管理潜在客户的CLI工具。

```bash
# Add new lead
./scripts/lead-tracker.sh add "Company Name" "Contact Name" "email@company.com"

# List all leads
./scripts/lead-tracker.sh list

# Update lead stage
./scripts/lead-tracker.sh update "Company Name" --stage "demo"

# Get daily follow-ups
./scripts/lead-tracker.sh followups
```

### pipeline-report.sh
生成销售流程报告。

```bash
# Weekly pipeline summary
./scripts/pipeline-report.sh weekly

# Monthly forecast
./scripts/pipeline-report.sh forecast
```

## CRM集成

### 内置跟踪功能

如果您不使用外部CRM系统，可以使用Markdown文件进行跟踪：

```
sales/
├── leads/
│   ├── company-name.md
│   └── ...
├── pipeline.md
├── analytics/
│   ├── weekly-YYYY-MM-DD.md
│   └── ...
└── templates/
```

### 外部CRM集成

**HubSpot：** 使用HubSpot API进行数据同步
**Salesforce：** 使用Salesforce API进行数据同步
**Notion：** 通过CSV或API导入/导出数据

---

## 最佳实践

1. **持续跟进** — 80%的交易需要5次或更多的沟通机会
2. **一切都要个性化** — 通用化的沟通方式往往会被忽略
3. **每次沟通后都要明确下一步行动** | 每次交流都应明确下一步计划
4. **分析失败原因** — 这比分析成功原因更重要
5. **快速响应** — 尽可能在5分钟内回复潜在客户
6. **多倾听，少推销** | 先了解客户需求，再提出解决方案
7. **详细记录一切** — 未来的自己会感谢您所做的这些记录
8. **每周检查销售流程** | 不及时跟进的潜在客户会影响销售预测

---

## 常见错误

❌ **在未充分了解客户需求前就进行推销** — 先了解客户需求再行动
❌ **忘记跟进** — 定期使用提醒工具
❌ **关注表面的数据指标** | 实际上，通话次数不如会议的质量重要
❌ **忽视已失败的交易** — 这些潜在客户未来仍有可能成为成交机会
❌ **不维护CRM系统的数据** — 不准确的数据会导致错误的决策

---

## 许可证

**许可证：** MIT许可 — 可自由使用、修改和分发。

---

*“销售不再仅仅是推销产品，而是建立信任和提供教育。” — Siva Devaki*