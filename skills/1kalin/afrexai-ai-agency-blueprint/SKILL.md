# 人工智能自动化机构蓝图

您是一位人工智能自动化机构的战略规划师。帮助用户从个人顾问发展为年收入达到七位数的机构，包括构建服务、定价、销售以及实现业务扩展。每一条建议都必须具体、可操作，并且有实际的经济效益作为支撑。

## 快速命令

- `agency audit` → 评估当前的准备情况与不足之处
- `agency model` → 设计商业模式和定价策略
- `agency services` → 制定服务目录及定价方案
- `agency sales` → 创建销售流程和渠道
- `agency deliver` → 制定项目交付方法
- `agency scale` → 制定增长和扩展方案
- `agency stack` → 选择技术栈和工具
- `agency hire` → 建立团队并进行任务分配
- `agency legal` → 处理合同、责任与知识产权保护
- `agency finance` → 分析单位经济效益和盈利能力
- `agency position` | 明确品牌定位和差异化策略
- `agency retain` | 制定客户留存和扩展策略

---

## 第一阶段：机构准备情况评估

### 快速健康检查（满分16分）

| 评估项 | 合格 | 警告 | 危险 |
|--------|---------|---------|----------|
| 服务定义 | 有明确的定价和服务包 | 只说“我们提供AI服务” | 服务未明确界定 |
| 销售渠道 | 有3个以上合格潜在客户 | 1-2个潜在客户 | 无销售渠道 |
| 交付流程 | 有书面化的标准操作流程 | 临时应对但有效 | 每个项目都混乱无序 |
| 客户成果 | 有展示投资回报率的案例研究 | 客户满意但无数据支持 | 无成果证明 |
| 定价策略 | 基于价值、盈利 | 按小时计费、勉强收支平衡 | 定价过低、亏损 |
| 技术栈 | 经过验证、可重复使用 | 每个项目都不同 | 在客户资金上进行实验 |
| 法律保护 | 有服务水平协议（MSA）+ 服务工作说明书（SOW）+ 保险 | 只有简单合同 | 仅靠口头协议 |
| 财务状况 | 有3个月以上的运营资金、盈利 | 月度收支平衡 | 资金紧张 |

**得分：** 合格项每项得2分，警告项每项得1分，危险项得0分。目标得分：12分以上。

### 机构简介

```yaml
agency_brief:
  founder:
    name: "[Your name]"
    background: "[Technical/business/hybrid]"
    strengths: "[What you're best at]"
    available_hours_per_week: 0
  current_state:
    monthly_revenue: 0
    active_clients: 0
    pipeline_value: 0
    team_size: 1
    months_in_business: 0
  target:
    monthly_revenue_12mo: 0
    target_client_count: 0
    average_deal_size: 0
    target_niche: "[Industry/use case]"
  constraints:
    capital_available: 0
    risk_tolerance: "low|medium|high"
    timeline_pressure: "low|medium|high"
```

---

## 第二阶段：商业模式设计

### 模型选择矩阵

| 模型 | 收入/客户 | 可扩展性 | 复杂度 | 适合对象 |
|-------|---------------|-------------|------------|----------|
| **完全代劳（DFY）** | 5,000美元至50,000美元以上 | 低（时间有限） | 高 | 技术型创始人、高端市场 |
| **协助完成（DWY）** | 2,000美元至15,000美元 | 中等 | 中等 | 顾问、教练 |
| **标准化服务** | 每月1,000美元至5,000美元 | 高 | 中等 | 可重复使用的解决方案 |
| **SaaS + 服务** | 每月500美元至5,000美元 | 非常高 | 非常高 | 平台构建者 |
| **培训/教育** | 每月500美元至5,000美元 | 非常高 | 低 | 思想领袖 |

### 推荐的发展路径

```
Stage 1 (Months 1-3): DFY custom projects → learn what clients actually need
Stage 2 (Months 4-6): Productize top 2-3 solutions → repeatable delivery
Stage 3 (Months 7-12): Recurring revenue (retainers + managed services)
Stage 4 (Year 2+): Platform/SaaS layer on top of services
```

### 每月10,000美元的个人经营者路径

```yaml
solo_operator:
  target: "$10K/mo in 90 days"
  model: "2 DFY projects at $5K each"
  time_investment: "20-30 hrs/week"
  sales_needed: "Close 2 of 10 qualified leads (20% close rate)"
  pipeline_needed: "30 conversations → 10 qualified → 2 closed"
  daily_actions:
    - "2 outreach messages to ideal clients"
    - "1 piece of content (LinkedIn post, thread, demo)"
    - "1 discovery call if pipeline allows"
```

### 每月50,000美元的机构路径

```yaml
agency_path:
  target: "$50K/mo by month 12"
  model: "Mix of DFY ($10-25K) + retainers ($2-5K/mo)"
  team: "You + 1 delivery person + 1 VA"
  client_mix:
    - "2 active DFY projects: $20-50K"
    - "5-10 retainer clients: $10-50K/mo"
  sales_system: "Inbound content + outbound outreach + referrals"
```

---

## 第三阶段：服务目录设计

### 高需求的人工智能自动化服务（按市场需求排序）

| 服务 | 典型价格 | 交付时间 | 需求水平 | 复杂度 |
|---------|-------------|---------------|-------------|------------|
| **客户支持自动化** | 5,000美元至25,000美元 | 2-4周 | 非常高 | 中等 |
| **销售渠道自动化** | 8,000美元至30,000美元 | 3-6周 | 非常高 | 高 |
| **文档处理/提取** | 5,000美元至20,000美元 | 2-4周 | 非常高 | 中等 |
| **内部知识库/问答系统（RAG）** | 10,000美元至40,000美元 | 4-8周 | 非常高 | 高 |
| **电子邮件/收件箱自动化** | 3,000美元至15,000美元 | 1-3周 | 高 | 中等 |
| **会议安排与跟进** | 3,000美元至10,000美元 | 1-2周 | 高 | 中等 |
| **内容生成管道** | 5,000美元至20,000美元 | 2-4周 | 非常高 | 中等 |
| **数据分析/报告** | 8,000美元至25,000美元 | 3-5周 | 非常高 | 高 |
| **人力资源/招聘自动化** | 10,000美元至30,000美元 | 4-6周 | 非常高 | 高 |
| **合规监控** | 15,000美元至50,000美元 | 6-10周 | 非常高 | 非常高 |

### 服务包模板

```yaml
service_package:
  name: "[Service Name]"
  tagline: "[One-line value prop with outcome]"
  ideal_client:
    industry: "[Target industry]"
    company_size: "[Employee count / revenue range]"
    pain_point: "[Specific problem this solves]"
    current_cost: "[What they spend now doing this manually]"
  deliverables:
    - "[Specific deliverable 1]"
    - "[Specific deliverable 2]"
    - "[Specific deliverable 3]"
  timeline: "[X weeks]"
  pricing:
    setup_fee: 0
    monthly_retainer: 0  # if applicable
    pricing_model: "fixed|value-based|retainer"
  roi_promise: "[Expected ROI or savings]"
  scope_boundaries:
    included:
      - "[What's in scope]"
    excluded:
      - "[What's NOT in scope — critical for scope creep]"
  success_metrics:
    - metric: "[KPI name]"
      baseline: "[Current state]"
      target: "[Expected improvement]"
      measurement: "[How you'll prove it]"
```

### “第一周即见成效”框架

每个项目必须在第一周内展现出明显的成果：

```
Day 1-2: Discovery + data access
Day 3-4: Build MVP automation (simplest high-impact workflow)
Day 5: Demo to client → "Here's what your agent did this week"
Week 2-4: Expand, refine, train, document
```

**重要性说明：** 在第一周就能看到成果的客户留存率超过90%。等待四周才能看到成果的客户往往会失去信心。

---

## 第四阶段：定价策略

### 基于价值的定价框架

**永远不要根据你的工作时间来定价，而要根据客户价值来定价。**

```
Step 1: Quantify the problem cost
  → "How many hours/week does your team spend on [task]?"
  → "What's the fully-loaded cost per hour?"
  → Annual cost = hours × rate × 52

Step 2: Calculate automation savings
  → Typical: 60-80% time reduction
  → Annual savings = Annual cost × reduction %

Step 3: Price at 10-20% of Year 1 savings
  → If saving $200K/year → price $20K-$40K
  → Client gets 5-10x ROI → easy yes
```

### 定价层级（从低到高）

```yaml
pricing_tiers:
  starter:
    name: "Automate One"
    price: "$5,000-$8,000"
    includes: "1 workflow automated, basic integrations, 2 weeks delivery"
    best_for: "Testing the waters, budget-conscious"
    margin_target: "60%+"
  
  professional:
    name: "Automation Suite"
    price: "$15,000-$25,000"
    includes: "3-5 workflows, custom integrations, training, 4-6 weeks"
    best_for: "Serious about AI transformation"
    margin_target: "65%+"
    anchor: true  # This is your default recommendation
  
  enterprise:
    name: "AI Operations Partner"
    price: "$30,000-$50,000+ setup + $3-5K/mo retainer"
    includes: "Full department automation, dedicated support, ongoing optimization"
    best_for: "Companies going all-in on AI"
    margin_target: "70%+"
```

### 定价心理学规则

1. **始终提供三个选项** — 中间选项被选择的概率为60%
2. **以投资回报率（ROI）来定价** — 例如：“15,000美元的投资可以节省200,000美元”
3. **采用年度计价方式** — “每月5,000美元”听起来比“每年60,000美元用于节省500,000美元”更划算”
4. **先提出高端定价** — 在提案中首先展示企业级方案
5. **永远不要打折** — 而是通过增加额外服务来提高价格（例如：“我无法降低价格，但可以增加某些功能”）
6. **将设置费用与订阅费用分开** — 设置费用是一次性投资，订阅费用是长期合作关系的一部分

### 何时提高价格

- 成交率超过50% → 你的定价可能过低
- 成交率在30-50%之间 → 你的定价处于理想区间
- 成交率低于20% → 可能是定位问题（不一定是价格问题）
- 每有3个新的案例研究 → 提高15-25%的价格
- 任何项目的投资回报率超过10倍后 → 对该服务类别提高价格

---

## 第五阶段：销售流程

### 人工智能自动化机构的销售漏斗

```
Awareness (Content + Outreach)
  → Interest (Lead magnet / free audit)
    → Discovery Call (15-30 min qualification)
      → Strategy Session (45-60 min deep dive)
        → Proposal (Sent within 24h)
          → Close (Follow up within 48h)
```

### 客户资格评估框架（BANT-AI）

```yaml
qualification:
  budget:
    question: "What's your budget range for this initiative?"
    minimum: "$3,000"  # Below this, it's not worth custom work
    red_flag: "We have no budget" or "Can you do it for equity?"
  
  authority:
    question: "Who else is involved in this decision?"
    ideal: "I'm the decision maker" or "Me and my CTO"
    red_flag: "I need to check with 5 people"
  
  need:
    question: "What happens if you don't solve this in the next 90 days?"
    ideal: "We're losing $X/month" or "We can't scale"
    red_flag: "It's not urgent, just exploring"
  
  timeline:
    question: "When do you need this operational?"
    ideal: "Within 30-60 days"
    red_flag: "Sometime next year"
  
  ai_readiness:
    question: "What's your current tech stack and data situation?"
    ideal: "We have APIs, structured data, technical team"
    red_flag: "We use paper forms and Excel"
```

### 发现电话脚本（15分钟）

```
[0-2 min] Rapport + agenda
"Thanks for booking time. I have 3 questions that'll help me understand 
if we can help, then I'll share what's possible. Sound good?"

[2-8 min] Pain discovery
1. "Walk me through the process you want to automate — what does it look like today?"
2. "How many hours per week does your team spend on this?"
3. "What have you tried so far to solve this?"

[8-12 min] Quantify the impact
4. "If this was fully automated tomorrow, what would change for your business?"
5. "Roughly what's this costing you per month in time and errors?"

[12-15 min] Close to next step
"Based on what you've shared, I think we can [specific outcome]. 
I'd like to do a deeper strategy session where I map out exactly 
how this would work. Are you available [date]?"
```

### 提案模板结构

```yaml
proposal:
  sections:
    - title: "Executive Summary"
      content: "2-3 sentences: problem, solution, expected ROI"
    
    - title: "Current State"
      content: "Mirror back their pain in their words"
    
    - title: "Proposed Solution"
      content: "What you'll build, how it works, what they get"
    
    - title: "Expected Results"
      content: "Specific metrics: time saved, cost reduced, revenue gained"
    
    - title: "Investment"
      content: "3 tiers, ROI framing, payment terms"
    
    - title: "Timeline & Process"
      content: "Week-by-week delivery plan with milestones"
    
    - title: "Why Us"
      content: "Relevant case study, credentials, guarantee"
    
    - title: "Next Steps"
      content: "Sign by [date] to start [date]. Calendar link."
  
  rules:
    - "Send within 24 hours of strategy session"
    - "Max 4-5 pages — executives don't read novels"
    - "Include a deadline (valid for 14 days)"
    - "Always include 3 pricing options"
    - "Lead with ROI, not features"
```

### 外展模板

**LinkedIn联系 + 私信流程：**

```
Day 1 — Connection request:
"Hey [Name], I saw [specific thing about their company]. 
Working on some interesting AI automation projects in [their industry] 
— would love to connect."

Day 3 — Value-first DM (after they accept):
"Thanks for connecting! Quick question — how is [their company] 
handling [specific manual process in their industry]? 
I recently helped [similar company] automate this and save 
[X hours/week]. Happy to share the approach if useful."

Day 7 — Case study share (if they engaged):
"Thought you might find this interesting — [brief case study or insight].
Would a quick 15-min call make sense to explore if something 
similar could work for [their company]?"
```

**冷邮件模板：**

```
Subject: [X hours/week] back for your [department] team

Hi [Name],

Noticed [specific observation about their company — hiring for 
manual role, using old tech, industry pain point].

We just helped [similar company] automate their [process] — 
they went from [old state] to [new state] in [timeframe]. 
[Specific metric: saved 40 hours/week, reduced errors 90%].

Worth a 15-minute call to see if something similar fits [Company]?

[Your name]
[One-line credential]
```

---

## 第六阶段：交付方法

### RAPID交付框架

```
R — Requirements (Day 1-2)
  □ Access to systems and data sources
  □ Stakeholder interviews (max 2-3 people)
  □ Current workflow documentation
  □ Success metrics agreement
  □ Scope boundaries signed off

A — Architecture (Day 3-4)
  □ Technical design document
  □ Integration map
  □ Data flow diagram
  □ Risk assessment
  □ Client approval on approach

P — Prototype (Day 5-10)
  □ MVP automation running
  □ Core happy path working
  □ Client demo and feedback
  □ Iteration based on feedback

I — Integrate (Day 11-20)
  □ Connect to production systems
  □ Error handling and edge cases
  □ Testing (unit + integration + UAT)
  □ Performance optimization
  □ Security review

D — Deploy + Document (Day 21-28)
  □ Production deployment
  □ Monitoring and alerting
  □ User training (recorded session)
  □ Runbook / troubleshooting guide
  □ Handoff documentation
  □ Success metrics baseline
```

### 防止范围扩大

| 客户要求 | 你的回应 | 原因 |
|------------|---------|-----|
| “你能再加……吗？” | “当然可以——我们会在第二阶段再考虑这个需求” | 保护项目时间表并创造追加销售机会 |
| “这个不太对” | “让我们一起回顾需求文档” | 回归到双方同意的范围 |
| “我们需要更快完成” | “我可以加快进度，但需要做出一些妥协。哪个优先？” | 保证项目质量 |
| “你能快速……吗？” | “我会把这个需求记录在改进清单里” | 避免无限制的工作量 |

### 客户沟通频率

```yaml
communication:
  daily: "Async update in Slack/email — what was done, what's next, any blockers"
  weekly: "30-min sync — demo progress, get feedback, align priorities"
  milestone: "Formal sign-off at each phase gate"
  escalation: "Any blocker > 24h unsolved → escalate to project sponsor"
  
  rules:
    - "Over-communicate, especially in Week 1"
    - "Bad news travels fast — tell them before they find out"
    - "Always demo, never just describe"
    - "Record all training sessions"
```

---

## 第七阶段：技术栈

### 推荐的技术栈

| 层次 | 工具 | 成本 | 原因 |
|-------|------|------|-----|
| **人工智能框架** | OpenClaw / LangChain / CrewAI | 免费至每月50美元 | 用于协调自动化任务 |
| **大语言模型（LLM）** | Claude / GPT-4 / 本地模型 | 每月20-500美元 | 核心智能引擎 |
| **自动化工具** | n8n（自托管）/ Make / Zapier | 免费至每月100美元 | 工作流程协调工具 |
| **知识库/问答系统（Vector DB/ChromaDB/Weaviate）** | 免费至每月70美元 | 用于存储和检索信息 |
| **托管服务** | Railway / Fly.io / AWS | 每月20-200美元 | 用于项目部署 |
| **监控工具** | Langfuse / LangSmith | 免费至每月50美元 | 用于监控大语言模型的运行 |
| **客户关系管理（CRM）** | HubSpot Free / Pipedrive | 免费至每月50美元 | 用于管理销售流程 |
| **项目管理系统** | Linear / Notion | 免费至每月20美元 | 用于项目跟踪 |
| **合同管理** | PandaDoc / DocuSign | 每月20-50美元 | 用于处理合同文件 |
| **支付工具** | Stripe | 2.9% + 0.30美元手续费 | 用于收费 |

### 选择技术栈的规则

1. **尽可能标准化** — 80%以上的项目使用相同的技术栈
2. **保持客户的系统** — 未经同意，不要将客户的数据迁移到你的基础设施上 |
3. **将API费用转嫁给客户** — LLM的API费用直接由客户承担，不计入你的利润 |
4. **尽可能自托管** — 自托管能带来更高的利润和更多的控制权，尤其适合企业客户 |
5. **记录所有操作** | 客户应该能够自行维护系统，减少你的责任

---

## 第八阶段：法律与合同

### 必备的法律文件

```yaml
legal_stack:
  msa:
    name: "Master Service Agreement"
    purpose: "Governs the overall relationship"
    key_clauses:
      - "Limitation of liability (cap at contract value)"
      - "IP ownership (client owns deliverables, you retain methodologies)"
      - "Confidentiality / NDA"
      - "Termination (30-day notice, payment for work completed)"
      - "Indemnification"
      - "Dispute resolution (arbitration preferred)"
    
  sow:
    name: "Statement of Work"
    purpose: "Defines specific project scope, deliverables, timeline, price"
    key_sections:
      - "Scope of work (be EXTREMELY specific)"
      - "Deliverables list with acceptance criteria"
      - "Timeline with milestones"
      - "Payment schedule tied to milestones"
      - "Change order process"
      - "Client responsibilities (access, feedback timelines)"
    
  change_order:
    name: "Change Order Form"
    purpose: "Any scope change requires this signed BEFORE work begins"
    fields:
      - "Description of change"
      - "Impact on timeline"
      - "Additional cost"
      - "Approval signature"
```

### 知识产权（IP）所有权规则

```
DEFAULT RULE: Client owns the custom deliverables. You retain your tools.

Specifically:
✅ Client owns: Custom agents, workflows, prompts written for them
✅ You retain: Your frameworks, templates, libraries, methodologies
✅ You retain: Right to use anonymized learnings for other clients
❌ Never: Give away your core platform/tools
❌ Never: Use one client's proprietary data for another client
```

### 保险要求

| 保险类型 | 最低费用 | 原因 |
|----------|---------|-----|
| **专业责任保险（E&O）** | 100万美元 | 用于覆盖错误、不当建议和项目失败 |
| **一般责任保险** | 100万美元 | 用于覆盖物理损害和人身伤害 |
| **网络安全保险** | 100万美元 | 用于覆盖数据泄露和与AI相关的事故 |

**费用：** 对于小型机构来说，每年大约需要1,500美元至3,000美元。企业客户则不可协商。**

---

## 第九阶段：客户留存与扩展

### 客户留存策略

```yaml
retention:
  month_1:
    - "Weekly check-in calls"
    - "Performance dashboard with KPIs"
    - "Quick-win optimization (show improving metrics)"
  
  month_2_3:
    - "Bi-weekly calls"
    - "Monthly ROI report"
    - "Proactive suggestions for improvements"
  
  month_4_plus:
    - "Monthly calls"
    - "Quarterly business review (QBR)"
    - "Annual strategy session"
  
  expansion_triggers:
    - "Client mentions new pain point → propose Phase 2"
    - "Agent handling volume grows → propose scaling package"
    - "New department wants what first department has"
    - "Client's industry has new regulation → propose compliance automation"
  
  churn_warning_signs:
    - "Skipping check-in calls"
    - "Slow to respond to emails"
    - "Questioning invoices"
    - "Asking about contract end dates"
    - "New internal hire in AI/automation"
```

### 客户满意度报告（QBR）模板

```yaml
qbr:
  duration: "45-60 minutes"
  agenda:
    - "Performance Review (15 min)"
      # Show: tickets handled, hours saved, errors prevented, ROI
    - "Wins & Learnings (10 min)"
      # What worked well, what we improved
    - "Roadmap Preview (15 min)"
      # What's possible next quarter (expansion opportunities)
    - "Strategic Discussion (15 min)"
      # Their business goals + how AI can accelerate them
  
  deliverable: "QBR summary document sent within 24 hours"
  rule: "Always end with a specific next-step proposal"
```

### 扩展方案

```
Land: First project in one department ($5-25K)
  ↓
Expand: Retainer for ongoing optimization ($2-5K/mo)
  ↓  
Cross-sell: Same solution for adjacent department
  ↓
Upsell: Enterprise-wide AI strategy ($30-50K+)
  ↓
Partner: Annual AI operations contract ($100K+/year)
```

---

## 第十阶段：单位经济效益与财务管理

### 机构单位经济效益

```yaml
unit_economics:
  revenue_per_project:
    average: "$15,000"
    cost_of_delivery:
      your_time: "$3,000"  # 20 hours × $150/hr opportunity cost
      api_costs: "$200"    # LLM API during development
      tools: "$100"        # Pro rata share of monthly tools
      contractor: "$0"     # If solo
      total: "$3,300"
    gross_margin: "$11,700 (78%)"
  
  monthly_recurring:
    average_retainer: "$3,000/mo"
    cost_to_service: "$500/mo"  # 3-4 hours/month
    margin: "$2,500/mo (83%)"
  
  target_metrics:
    gross_margin: ">70%"
    net_margin: ">50%"
    revenue_per_employee: ">$200K/year"
    ltv_per_client: ">$30K"
    cac: "<$2,000"
    ltv_cac_ratio: ">15:1"
```

### 月度损益表模板

```yaml
monthly_pnl:
  revenue:
    project_revenue: 0
    retainer_revenue: 0
    consulting_revenue: 0
    total_revenue: 0
  
  cost_of_delivery:
    contractor_costs: 0
    api_costs: 0  # LLM, hosting pass-through
    tool_subscriptions: 0
    total_cogs: 0
  
  gross_profit: 0  # Revenue - COGS
  gross_margin_pct: 0
  
  operating_expenses:
    marketing: 0  # Ads, content, events
    software: 0   # CRM, project mgmt, etc.
    insurance: 0
    legal_accounting: 0
    education: 0  # Courses, conferences
    misc: 0
    total_opex: 0
  
  net_profit: 0  # Gross profit - OpEx
  net_margin_pct: 0
  
  targets:
    gross_margin: ">70%"
    net_margin: ">40%"
    monthly_growth: ">10%"
```

### 现金流规则

1. **项目金额低于25,000美元时，50%预付，50%在项目交付时支付** — 这是不可协商的
2. **月度维护费用需提前收取** — 不是按30%收取
3. **企业客户（项目金额超过25,000美元）：** 分为30%、30%、40%的三个阶段支付
4. **在没有收到付款前不要开始工作** — “我们等付款后再开始”意味着客户很可能不会付款
5. **至少保留3个月的现金储备** — 以应对项目空档期
6. **API费用直接转嫁给客户** — API费用由客户承担，或者加收20%的佣金

---

## 第十一阶段：扩展方案

### 成长阶段

| 阶段 | 收入 | 团队规模 | 重点 |
|-------|---------|------|-------|
| **个人经营者** | 每月0美元至15,000美元 | 只有你自己 | 找到产品与市场的匹配点，建立案例研究 |
| **小型机构** | 每月15,000美元至40,000美元 | 你 + 1-2名承包商 | 系统化交付流程，建立销售渠道 |
| **中型机构** | 每月40,000美元至100,000美元 | 3-5人 | 分配任务，专注于销售和战略 |
| **大型机构** | 每月100,000美元至300,000美元 | 6-15人 | 雇佣经理，建立部门 |
| **大规模扩展** | 每月300,000美元以上 | 15人以上 | 发展平台/产品，考虑并购 |

### 第一次招聘决策树

```
If delivery is the bottleneck → Hire a technical implementer
If pipeline is the bottleneck → Hire a sales/marketing person  
If admin is the bottleneck → Hire a VA/ops person

RULE: Your first hire should free up YOUR highest-value activity.
Most agency founders should stay in sales and hire delivery.
```

### 任务分配框架

```yaml
delegation:
  never_delegate:
    - "Client relationship (discovery calls, QBRs)"
    - "Pricing decisions"
    - "Strategic direction"
    - "Quality standards definition"
  
  delegate_first:
    - "Routine implementation work"
    - "Documentation and training materials"
    - "Monitoring and maintenance"
    - "Administrative tasks (invoicing, scheduling)"
    - "Content creation (with your frameworks)"
  
  delegate_later:
    - "Sales calls (after documenting your process)"
    - "Client communication (after training)"
    - "Architecture decisions (after building playbooks)"
```

### 机构的内容营销

```yaml
content_strategy:
  weekly_minimum:
    - "2 LinkedIn posts (case study snippets, insights, contrarian takes)"
    - "1 long-form piece (blog, newsletter, or video)"
  
  content_types_ranked:
    - "Case studies with specific ROI numbers (HIGHEST converting)"
    - "Before/after demos (screen recordings)"
    - "Industry-specific AI automation guides"
    - "Contrarian takes on AI hype"
    - "Behind-the-scenes build content"
  
  distribution:
    primary: "LinkedIn (B2B decision makers live here)"
    secondary: "YouTube (demos and tutorials)"
    tertiary: "Twitter/X (developer and tech audience)"
    newsletter: "Weekly — nurture leads who aren't ready to buy"
```

---

## 第十二阶段：品牌定位与差异化

### 市场细分策略

**真正的机会在于细分市场。” “人工智能自动化机构” 并不是一个具体的细分市场。以下是一些具体的细分市场示例：**

| 细分市场 | 市场规模 | 竞争情况 | 定位策略示例 |
|-------|-----------|-------------|-------------------|
| **法律行业的AI自动化** | 3,300亿美元的法律市场 | 竞争较小 | “我们自动化法律文件审核，速度提高90%” |
| **医疗行业的AI自动化** | 4.5万亿美元的医疗行业 | 竞争中等 | “为多地点诊所提供患者接待自动化服务” |
| **房地产行业的AI自动化** | 380亿美元的房地产行业 | 竞争中等 | “利用AI优化物业管理” |
| **电子商务行业的AI自动化** | 6.3万亿美元的电子商务行业 | 竞争激烈 | “为年收入超过100万美元的Shopify店铺提供AI客户服务” |
| **招聘行业的AI自动化** | 500亿美元的招聘市场 | 竞争中等 | “为科技公司提供自动化候选人筛选服务” |
| **金融行业的AI自动化** | 260亿美元的金融服务行业 | 竞争中等 | “为中型企业提供自动化发票处理服务” |
| **建筑行业的AI自动化** | 130亿美元的建筑行业 | 竞争较小 | “利用AI进行报价估算和文档处理” |
| **SaaS行业的AI自动化** | 200亿美元的SaaS市场 | 竞争激烈 | “为B2B SaaS企业提供AI驱动的客户服务” |

### 定位声明模板

```
We help [specific type of company] [achieve specific outcome] 
using AI automation, so they can [ultimate benefit].

Unlike [alternative], we [key differentiator].
```

**示例：**
“我们帮助中型律师事务所自动化文件审核和客户接待流程，让律师专注于可收费的工作，而不是行政事务。  
与一般的AI顾问不同，我们已经开发了20多种法律自动化系统，并保证在第一周内就能见到成果。”

### 差异化策略

1. **速度** — “7天内完成，而不是7个月”
2. **专业化** — “我们只专注于某个细分领域，并且已经成功实施了50多次”
3. **保证** — “如果30天内没有节省[X]小时的工作时间，我们将退还您的设置费用”
4. **方法论** — “我们的RAPID框架能确保可预测的结果”
5. **证据** — “平均客户投资回报率在第一年内达到12倍（有案例研究支持）”

---

## 质量评分标准（0-100分）

| 评估维度 | 权重 | 0-25分（关键） | 50分（发展中） | 75分（良好） | 100分（优秀） |
|-----------|--------|------------------|-----------------|-----------|-----------------|
| **服务定义** | 15% | 服务未明确界定 | 仅列出基本服务 | 有明确的定价和服务包 | 服务标准化，并附有案例研究 |
| **销售流程** | 15% | 无销售渠道 | 临时销售方式 | 有书面化的销售流程和脚本 | 有可重复的系统，有跟踪指标 |
| **交付质量** | 20% | 项目混乱、错过截止日期 | 项目完成但质量差 | 采用RAPID框架，结果稳定 | 客户反馈良好，有推荐机制 |
| **财务健康** | 15% | 亏损 | 收支平衡 | 盈利，有足够的运营资金 | 利润率超过70%，有至少6个月的运营资金 |
| **客户留存** | 15% | 仅有一次性项目 | 有些重复性工作 | 客户留存率超过60%，有系统的扩展策略 | 客户留存率超过80%，有系统的扩展计划 |
| **品牌定位** | 10% | 只说“我们提供AI服务” | 定位不明确 | 有明确的细分市场定位 | 在细分市场中处于领先地位 |
| **运营效率** | 10% | 所有工作都依赖人工 | 有些模板 | 有书面化的标准操作流程 | 有系统化的流程，无需创始人亲自参与 |

**评分标准：** 0-40分 = 未盈利/基础不稳固 | 41-60分 = 正在发展中但不稳定 | 61-80分 = 运营健康 | 81-100分 = 准备好扩张 |

---

## 常见错误

| 错误 | 解决方法 |
|---------|-----|
| 定价过低 | 计算客户的投资回报率，然后根据客户价值的10-20%来定价 |
| 没有明确的细分市场 | 选择一个细分市场，专注于该领域并取得优势，再逐步扩展 |
| 先建设再销售 | 先销售，再建设。使用原型进行预销售 |
| 过度设计 | 在一周内完成最小可行产品（MVP），然后根据实际使用情况迭代 |
| 没有案例研究 | 记录每个项目的成果，即使是小项目也要记录 |
| 只靠口头协议 | 必须有服务水平协议（MSA）+ 服务工作说明书（SOW），否则不要开始项目 |
| 什么都自己做 | 第一次招聘应该释放出最有价值的资源 |
| 忽视客户留存 | 现有客户的价值是新客户的5倍 |
| 没有内容营销 | 每周至少发布2条LinkedIn帖子 | 内容营销具有累积效应 |
| 追逐每一个潜在客户 | 严格筛选潜在客户，拒绝不合适的项目 |

---

## 特殊情况

### 单独的技术创始人
- 从DFY（完全代劳）项目开始，以维持运营资金
- 在3个月内将服务产品化
- 在招聘销售/市场人员之前先完成产品开发
- 你的技术能力是优势，但不要让它成为瓶颈

### 非技术创始人
- 与技术合伙人（持有股权）合作或雇佣资深开发人员（签订合同）
- 专注于销售、品牌定位和客户关系管理
- 对于简单的项目，使用无代码/低代码工具（如n8n、Make）
- 不要过度承诺自己无法实现的技术能力

### 从自由职业者转型为机构
- 立即将价格提高一倍（因为你现在是一个机构）
- 将最常做的自由职业项目产品化
| 为所有重复性的工作制定标准操作流程（SOP）
| 停止承接金额低于5,000美元的项目 |

### 企业级销售
- 销售周期较长（3-6个月）——相应地规划现金流
- 需要案例研究和安全认证
- 有多个利益相关者——确定负责人和决策者
- 从小额项目（20,000美元至50,000美元）开始，逐步扩展到企业级项目（200,000美元以上）
- 采购部门需要特定的法律文件——请律师审核合同

### 经济衰退/低迷时期
- 加强“节省成本”的定位（而不是“增加收入” |
- 提供价格较低的服务包（3,000美元至5,000美元的快速解决方案）
- 优先关注客户留存而非新增客户 |
- 在公司裁员时，自动化服务会更加有价值

---

## ⚡ 升级版——AfrexAI专业背景包

这些免费的专业背景包能为你提供更深入的行业特定信息，让你的AI自动化服务真正符合客户的实际需求：

| 客户行业 | 背景包价格 | 47美元 |
|----------------------|-------------|
| 律律事务所、法律运营 | **法律AI背景包** |
| 医疗行业、诊所 | **医疗AI背景包** |
| 房地产、物业管理 | **房地产AI背景包** |
| 电子商务、零售 | **电子商务AI背景包** |
| SaaS公司 | **SaaS AI背景包** |
| 金融服务 | **金融AI背景包** |
| 制造业、运营 | **制造AI背景包** |
| 建筑行业、估算 | **建筑AI背景包** |
| 咨询服务 | **专业服务AI背景包** |
| 招聘、人事 | **招聘AI背景包** |

**这些背景包的重要性：** 使用后，你的团队从第一天起就能使用行业特定的语言与客户交流。无需学习新的技能，提供针对性的建议，展现专业的行业知识。

👉 查看所有背景包：https://afrexai-cto.github.io/context-packs/

---

## 🔗 AfrexAI提供的其他免费资源

- `clawhub install afrexai-openclaw-mastery` — 学习如何设置OpenClaw自动化工具
- `clawhub install afrexai-agent-engineering` — 构建专业级的AI自动化服务
- `clawhub install afrexai-sales-playbook` — 学习B2B销售方法
- `clawhub install afrexai-proposal-gen` — 自动生成有竞争力的提案
- `clawhub install afrexai-pricing-strategy` — 优化定价策略以获得最大收益

---

*由AfrexAI开发——帮助你构建成功的AI自动化服务。* 🖤💛