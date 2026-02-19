---
name: Agency Command Center
slug: afrexai-agency-command-center
version: 1.0.0
description: 完整的代理运营系统——涵盖服务企业的客户生命周期管理、定价策略、项目交付流程、团队管理以及业务增长策略。
tags: agency, consulting, client management, project management, freelance, professional services
---
# 机构指挥中心  
为服务机构、咨询公司和自由职业者提供全面的操作系统，从首次客户咨询到实现持续收入。  

## 使用场景  
- 启动或扩展服务业务（开发、营销、设计、咨询、人工智能/自动化）  
- 同时管理多个客户和项目  
- 建立可复制的客户交付流程  
- 定价服务并撰写提案  
- 从个人创业发展到团队协作  

---

## 第一阶段：机构基础  
### 业务模式选择  
选择适合您的业务模式——它将决定后续的所有决策：  

| 模式 | 平均客户价值（ACV） | 团队规模 | 盈利目标 | 适用对象 |  
|-------|------------|-----------|---------------|----------|  
| 个人专家 | 5,000美元–25,000美元 | 1人 | 60–80% | 深度专业领域专家 |  
| 精英机构 | 25,000美元–100,000美元 | 3–8人 | 40–55% | 专注于高品质的细分市场 |  
| 成长型机构 | 100,000美元–500,000美元 | 10–30人 | 30–45% | 需要扩大规模的机构 |  
| 产品化服务 | 每月1,000美元–10,000美元 | 5–15人 | 50–70% | 需要可重复交付的服务 |  

### 服务打包框架  
**不要出售时间，而是出售结果。**  
将服务分为三个层级：  

```yaml
service_catalog:
  tier_1_starter:
    name: "[Quick Win Name]"
    price: "$X,XXX"
    duration: "1-2 weeks"
    deliverables:
      - "[Specific deliverable 1]"
      - "[Specific deliverable 2]"
    ideal_for: "Companies that need [specific outcome] fast"
    margin_target: "70%+"
    
  tier_2_standard:
    name: "[Core Service Name]"
    price: "$XX,XXX"
    duration: "4-8 weeks"
    deliverables:
      - "[Everything in Tier 1]"
      - "[Additional deliverable 3]"
      - "[Additional deliverable 4]"
    ideal_for: "Companies ready for [bigger transformation]"
    margin_target: "50%+"
    
  tier_3_premium:
    name: "[Flagship Engagement Name]"
    price: "$XXX,XXX+"
    duration: "3-6 months"
    deliverables:
      - "[Everything in Tier 2]"
      - "[Strategic deliverable 5]"
      - "[Ongoing support/retainer]"
    ideal_for: "Enterprises needing [complete solution]"
    margin_target: "40%+"
```  

### 细分市场选择评分表  
对每个潜在细分市场进行1-5分的评估：  

| 标准 | 权重 | 分数 | 总分 |  
|-----------|--------|-------|----------|  
| 市场规模（是否有足够的客户？） | 3倍 | /5 | /15 |  
| 支付意愿（是否愿意支付10,000美元以上的订单？） | 3倍 | /5 | /15 |  
| 你的专业能力（能否完成？） | 2倍 | /5 | /10 |  
| 竞争情况（是否有机会？） | 2倍 | /5 | /10 |  
| 热情（能否长期从事这项工作？） | 1倍 | /5 | /5 |  
| **总分** | | | **/55** |  
**总分35分以上 = 非常合适的细分市场。** 低于25分 = 继续寻找。 |  

---

## 第二阶段：客户获取机制  
### 入站线索评估（BANT-S）  
收到咨询时，提取关键信息：  

```yaml
lead_qualification:
  company: ""
  contact_name: ""
  contact_role: ""
  source: ""  # referral, website, social, cold
  
  budget:
    stated: ""
    estimated_range: ""
    budget_holder: ""  # Are they the decision maker?
    
  authority:
    decision_maker: true/false
    other_stakeholders: []
    approval_process: ""
    
  need:
    problem_statement: ""
    urgency: "low|medium|high|critical"
    current_solution: ""
    why_change_now: ""
    
  timeline:
    desired_start: ""
    desired_completion: ""
    hard_deadlines: []
    
  scope_fit:
    matches_services: true/false
    complexity: "simple|moderate|complex|enterprise"
    red_flags: []

  score: "/100"  # See scoring below
```  

### 线索评分（0-100分）  
| 因素 | 分数 | 标准 |  
|--------|--------|----------|  
| 预算匹配度 | 0-25分 | 预算在范围内：25分；可能：15分；不明确：5分；远低于预算：0分 |  
| 决策权 | 0-20分 | 拥有决策权：20分；有影响力：10分；仅是调研人员：0分 |  
| 需求紧迫性 | 0-20分 | 非常紧急/有截止日期：20分；较高：15分；中等：10分；正在探索：5分 |  
| 时间线匹配度 | 0-15分 | 与团队能力相符：15分；时间紧张但可行：10分；不可能：0分 |  
| 服务范围匹配度 | 0-10分 | 服务范围符合需求：10分；相关服务：5分；超出范围：0分 |  
| 来源质量 | 0-10分 | 来源可靠：10分；内部推荐：7分；外部获取：3分 |  
**80分以上 = 可快速推进**（2小时内回复）  
**60-79分 = 标准流程**（24小时内回复）  
**40-59分 = 需进一步跟进**（30天后再次联系）  
**低于40分 = 礼貌拒绝**  

### 发现阶段通话框架（45分钟）  
```
[0-5 min] Rapport + Agenda Setting
- "Thanks for taking the time. Here's what I'd like to cover..."
- Confirm their role and who else is involved in the decision

[5-20 min] Deep Problem Discovery
- "Walk me through what's happening today..."
- "What have you tried so far?"
- "What's the cost of NOT solving this?" ← KEY QUESTION
- "If we solve this perfectly, what does that look like in 6 months?"
- "What's your biggest concern about working with an agency?"

[20-30 min] Solution Exploration
- Mirror their language back: "So the core issue is [X], and ideally you'd have [Y]"
- Share relevant case study (1-2 min, not a pitch)
- Outline potential approach at high level
- "Based on what you've described, I'd suggest [Tier 2 service]"

[30-40 min] Logistics
- Timeline expectations
- Budget conversation: "Projects like this typically range $X-$Y. Does that align with what you had in mind?"
- Decision process and stakeholders
- Required access/resources from their side

[40-45 min] Next Steps
- "Here's exactly what happens next: I'll send a proposal by [date]..."
- Confirm follow-up date
- Ask: "Is there anything else I should know before putting this together?"
```  

### 外展模板  
**温暖推荐跟进：**  
```
Subject: [Referrer] suggested we connect

Hi [Name],

[Referrer] mentioned you're dealing with [specific problem]. We just helped [similar company] solve that — they went from [before state] to [after state] in [timeframe].

Worth a 20-minute call to see if we can do the same for you?

[Your name]
```  
**发现阶段后的提案邮件：**  
```
Subject: Your [problem] solution — proposal attached

Hi [Name],

Great talking on [day]. Attached is the proposal for [project name].

The quick version:
- We'll deliver [key outcome] by [date]
- Investment: $[amount]
- You'll see [specific metric improvement]

I've blocked [date] for a 15-min walkthrough if that works.

[Your name]
```  

---

## 第三阶段：提案与定价机制  
### 提案结构（提高中标率）  
所有提案均遵循此结构：  
```
1. EXECUTIVE SUMMARY (1 page)
   - Their problem in their words (mirror discovery call)
   - The cost of inaction (quantified)
   - Your recommended solution (1 paragraph)
   - Investment and timeline (bottom line up front)

2. SITUATION ANALYSIS (1-2 pages)
   - Current state (show you listened)
   - Desired future state
   - Gap analysis
   - Why now matters

3. RECOMMENDED APPROACH (2-3 pages)
   - Phase breakdown with deliverables
   - Timeline with milestones
   - What success looks like (measurable)
   - Your methodology/framework name

4. INVESTMENT (1 page)
   - 3-tier pricing (Good/Better/Best)
   - What's included in each tier
   - Payment terms
   - What's NOT included (scope boundaries)

5. WHY US (1 page)
   - 2-3 relevant case studies (results, not process)
   - Team bios (relevant experience only)
   - Unique approach/methodology

6. NEXT STEPS (half page)
   - Clear call to action
   - Timeline to start
   - What you need from them
```  

### 定价计算器  
```yaml
pricing_worksheet:
  # Cost basis
  estimated_hours: 0
  blended_hourly_rate: 0  # Your internal cost per hour
  direct_costs: 0  # Software, contractors, etc.
  total_cost: 0  # hours × rate + direct costs
  
  # Value basis
  client_problem_cost: 0  # Annual cost of their problem
  your_solution_value: 0  # Annual value you create
  value_price: 0  # 10-20% of value created
  
  # Market basis
  competitor_low: 0
  competitor_high: 0
  market_price: 0  # Your positioning in range
  
  # Final price
  floor_price: 0  # cost × 1.5 (minimum viable margin)
  target_price: 0  # MAX(value_price, market_price)
  anchor_price: 0  # target × 1.3 (your Tier 3)
  
  # Sanity checks
  margin_percent: 0  # Must be > 40%
  price_per_hour_effective: 0  # Must be > 2× your cost rate
  roi_for_client: "X:1"  # Must be > 3:1 or rethink
```  

### 定价规则  
1. **绝不要按小时收费**——始终基于项目或价值定价  
2. **提供三种定价选项**——将中间选项设定为“合理价格”  
3. **包含“快速启动”选项**——低风险入门方案（2,000美元–5,000美元）  
4. **项目金额低于25,000美元时，50%预付款，50%项目完成后支付**  
5. **月度维护费：至少3个月**——短期合作不值得承担入职成本  
6. **范围扩展条款**：“超出此范围的需求将另行报价”  
7. **价格调整**：每年涨价10–15%，现有客户可享受6个月的优惠  

### 维护费模型设计  
```yaml
retainer_tiers:
  growth:
    monthly_fee: "$X,XXX"
    hours_included: 20
    response_time: "24 hours"
    includes:
      - "[Core service deliverable]"
      - "Monthly strategy call"
      - "Slack/email support"
    overage_rate: "$XXX/hr"
    
  scale:
    monthly_fee: "$XX,XXX"
    hours_included: 40
    response_time: "4 hours"
    includes:
      - "[Everything in Growth]"
      - "[Additional strategic service]"
      - "Weekly check-in call"
      - "Quarterly business review"
    overage_rate: "$XXX/hr"
    
  enterprise:
    monthly_fee: "$XX,XXX+"
    hours_included: "Unlimited (fair use)"
    response_time: "2 hours"
    includes:
      - "[Everything in Scale]"
      - "Dedicated team member"
      - "24/7 emergency support"
      - "Executive sponsor access"
    overage_rate: "N/A"
```  

---

## 第四阶段：客户入职系统  
### 入职检查清单（前48小时）  
```yaml
onboarding:
  day_0_signed:
    - [ ] Contract signed and countersigned
    - [ ] First payment received
    - [ ] Welcome email sent (see template below)
    - [ ] Client folder created in project management
    - [ ] Internal kickoff scheduled
    - [ ] Client added to communication channel
    
  day_1:
    - [ ] Access credentials collected (see access request template)
    - [ ] Onboarding questionnaire sent
    - [ ] Project timeline shared
    - [ ] Team introductions made
    - [ ] First milestone confirmed
    
  day_2:
    - [ ] Kickoff call completed
    - [ ] Meeting notes distributed
    - [ ] First deliverable timeline confirmed
    - [ ] Weekly check-in cadence set
    - [ ] Client expectations document signed
```  

### 欢迎邮件模板  
```
Subject: Welcome to [Agency Name] — here's what happens next

Hi [Name],

We're excited to get started on [project name]. Here's your roadmap for the next 48 hours:

TODAY:
✅ Contract signed — check
✅ You'll receive an onboarding questionnaire (10 min to complete)
✅ We'll send access requests for [systems we need]

TOMORROW:
📋 We review your questionnaire answers
📞 Kickoff call at [time] — here's the agenda: [link]

THIS WEEK:
🚀 First milestone: [deliverable] by [date]
📊 Weekly update every [day] at [time]

YOUR TEAM:
- [Name] — Project Lead (your main point of contact)
- [Name] — [Role]
- For urgent issues: [emergency contact method]

Questions before kickoff? Reply to this email or message us on [Slack/channel].

Let's build something great.

[Your name]
```  

### 客户期望文档  
在入职时让客户签署此文件，以预防90%的问题：  
```
WORKING AGREEMENT

Communication:
- Primary channel: [Slack/email/tool]
- Response time: We respond within [X hours] on business days
- Urgent issues: [Phone/emergency process]
- Weekly updates: Every [day] by [time]

Feedback & Approvals:
- We'll send work for review with clear deadlines
- Feedback is due within [48 hours] of submission
- Delayed feedback = delayed timeline (no penalty to us)
- "Approved" means approved — revisions after approval are billed separately

Scope:
- This project covers: [specific deliverables from contract]
- Changes to scope require a written change order
- We'll flag scope creep early — no surprise invoices

Meetings:
- Weekly check-in: [30 min, day/time]
- We'll send agendas 24h before, notes within 24h after
- Cancel with 24h notice or it counts as held
```  

---

## 第五阶段：项目交付系统  
### 项目跟踪模板  
```yaml
project:
  name: ""
  client: ""
  status: "active|on-hold|at-risk|complete"
  
  health:
    schedule: "green|yellow|red"
    budget: "green|yellow|red"
    scope: "green|yellow|red"
    client_satisfaction: "green|yellow|red"
    overall: "green|yellow|red"
  
  financials:
    contract_value: 0
    collected: 0
    outstanding: 0
    hours_budgeted: 0
    hours_used: 0
    burn_rate_percent: 0  # hours_used / hours_budgeted × 100
    margin_actual: 0
    
  milestones:
    - name: ""
      due: "YYYY-MM-DD"
      status: "pending|in-progress|review|complete|late"
      deliverables: []
      
  risks:
    - description: ""
      probability: "low|medium|high"
      impact: "low|medium|high"
      mitigation: ""
      
  next_actions:
    - task: ""
      owner: ""
      due: "YYYY-MM-DD"
```  

### 每周客户更新模板  
每周同一时间发送：  
```
Subject: [Project Name] — Weekly Update #[N]

📊 STATUS: [GREEN/YELLOW/RED]

COMPLETED THIS WEEK:
✅ [Deliverable/milestone 1]
✅ [Deliverable/milestone 2]

IN PROGRESS:
🔄 [Task 1] — [% complete, expected done date]
🔄 [Task 2] — [% complete, expected done date]

NEXT WEEK:
📋 [Planned deliverable 1]
📋 [Planned deliverable 2]

⚠️ NEEDS YOUR INPUT:
- [Decision/approval/access needed] — please respond by [date]

TIMELINE: [On track / X days ahead / X days behind]
BUDGET: [X% used of total hours]
```  

### 范围扩展管理  
当客户提出超出范围的需求时：  
**步骤1：确认**——“这个想法很好，请让我看看具体内容。”  
**步骤2：分类**：  
- **小范围调整**（<2小时，能改进交付成果）→ 立即处理，并记录为善意调整  
- **中等范围调整**（2–8小时）→ “很高兴添加这个内容。预计需要额外[X]小时的工作，费用约为[金额]。需要我起草一份变更订单吗？”  
- **大规模调整**（超过8小时）→ “这实际上是一个独立的项目。我会重新评估范围并发送报价。”  
**步骤3：记录所有变更请求**：  
```yaml
change_request:
  date: ""
  requested_by: ""
  description: ""
  classification: "goodwill|change_order|new_project"
  estimated_hours: 0
  estimated_cost: 0
  status: "pending|approved|declined"
  impact_on_timeline: ""
```  

### 质量控制清单  
在任何交付成果发送给客户之前，必须满足以下条件：  
- [ ] 符合项目要求  
- [ ] 由非创建者审核  
- [ ] 经过测试/校对（无链接错误、拼写错误）  
- [ ] 格式专业（保持品牌一致性）  
- [ ] 包含背景信息（“这是[交付成果]，我们做出的关键决策：[X、Y、Z]”）  
- [ ] 明确下一步行动  
- [ ] 提前足够时间发送给客户审核  

---

## 第六阶段：团队与运营  
### 招聘决策框架  
**何时招聘全职员工与签订合同？**  
| 因素 | 招聘全职 | 签订合同/使用自由职业者 |  
|--------|---------------|-------------------|  
| 需求频率 | 持续性工作（每日） | 项目性工作（偶尔） |  
| 技能要求 | 核心业务所需 | 专业领域技能 |  
| 与客户互动 | 面向客户 | 背后支持工作 |  
| 当前工作量下的成本 | 比签订合同更便宜 | 比招聘更便宜 |  
| 培训周期 | 值得投资 | 需要员工立即投入工作 |  
### 团队利用率跟踪  
```yaml
team_member:
  name: ""
  role: ""
  cost_per_hour: 0  # Your cost (salary ÷ working hours)
  billable_target: "70%"  # % of time on client work
  
  this_week:
    total_hours: 40
    billable_hours: 0
    internal_hours: 0  # Sales, admin, training
    utilization: "0%"
    
  this_month:
    billable_hours: 0
    revenue_generated: 0
    effective_rate: 0  # revenue ÷ billable hours
```  
**利用率目标：**  
- **低于60%** = 未充分利用（需要增加客户或减少人员）  
- **60–75%** = 适中（有培训、销售和行政工作的空间）  
- **75–85%** = 最佳状态（高产出，可持续）  
- **超过85%** = 有人员流失风险（考虑招聘新员工或停止接新项目）  

### 授权机制  
随着机构规模扩大，按以下顺序进行授权：  
1. **执行任务**（首次招聘）——负责完成现有工作的人员  
2. **项目管理**——负责管理进度和客户沟通的人员  
3. **销售**——负责处理客户咨询和提案的人员  
4. **运营**——负责发票处理、入职培训和行政工作的人员  
5. **战略规划**——最后才进行授权（这是你的竞争优势）  

### 标准操作流程（SOP）模板  
为每个重复性流程创建一份SOP：  
```yaml
sop:
  name: ""
  owner: ""
  last_updated: ""
  frequency: ""  # How often this runs
  
  purpose: ""  # Why this exists
  
  trigger: ""  # What kicks this off
  
  steps:
    - step: 1
      action: ""
      tool: ""  # What software/tool
      time: ""  # Expected duration
      output: ""  # What this step produces
      notes: ""
      
  quality_check: ""  # How to verify it's done right
  
  common_mistakes:
    - mistake: ""
      prevention: ""
```  

---

## 第七阶段：财务管理  
### 月度损益表  
每月跟踪数据，每周进行审查：  
```yaml
monthly_financials:
  month: "YYYY-MM"
  
  revenue:
    project_revenue: 0
    retainer_revenue: 0
    other_revenue: 0
    total_revenue: 0
    
  cost_of_delivery:
    team_costs: 0  # Salaries/contractor payments for delivery
    software_tools: 0
    direct_expenses: 0  # Client-specific costs
    total_cod: 0
    
  gross_margin: 0  # revenue - cost_of_delivery
  gross_margin_percent: 0  # Should be > 50%
  
  operating_expenses:
    sales_marketing: 0
    admin_overhead: 0
    office_insurance: 0
    total_opex: 0
    
  net_profit: 0  # gross_margin - opex
  net_margin_percent: 0  # Target: 15-25%
  
  cash:
    opening_balance: 0
    cash_in: 0  # Actually received
    cash_out: 0  # Actually paid
    closing_balance: 0
    runway_months: 0  # closing ÷ monthly burn
    
  ar_aging:
    current: 0  # Not yet due
    days_30: 0
    days_60: 0
    days_90_plus: 0  # Chase these aggressively
```  

### 现金流管理规则  
1. **始终保留至少3个月的现金储备**  
2. **在里程碑达成后立即开具发票**  
3. **小型客户：净结算周期14天；大型企业：净结算周期30天**  
4. **逾期7天内催款（友好提醒）；14天（正式提醒）；21天（最终通知）**  
5. **逾期30天停止服务**——无例外  
6. **维护费客户需提前支付**——避免欠款  

### 拖欠付款处理流程  
```
Day 1 past due — Automated reminder:
"Hi [Name], friendly reminder that invoice #[X] for $[amount] was due on [date]. 
Payment link: [link]. Let me know if you have any questions."

Day 7 — Personal follow-up:
"Hi [Name], following up on invoice #[X]. Is everything okay? 
Happy to jump on a quick call if there's an issue with the invoice."

Day 14 — Firm notice:
"Hi [Name], invoice #[X] is now 14 days overdue. Per our agreement, 
work will pause on [date] if payment isn't received. 
Please process this at your earliest convenience."

Day 21 — Final notice:
"Hi [Name], this is a final notice for invoice #[X] ($[amount], 21 days overdue). 
Work on [project] will pause effective [date + 3 days] until payment is received. 
If there's a cash flow issue, let's discuss a payment plan."

Day 30 — Work stops. Send formal letter. Consider collections for large amounts.
```  

---

## 第八阶段：客户留存与增长  
### 客户健康状况评分（0-100分）  
每月对每位客户进行评估：  
| 维度 | 权重 | 评估指标 | 分数 |  
|-----------|--------|-----------|-------|  
| 参与度 | 25% | 回应时间、会议出席情况、反馈质量 | /25 |  
| 满意度 | 25% | 明确反馈、净推荐值（NPS）、投诉频率 | /25 |  
| 财务表现 | 20% | 按时付款、预算讨论、追加销售意愿 | /20 |  
| 成果表现 | 20% | 关键绩效指标上升、里程碑达成、投资回报率明显 | /20 |  
| 关系质量 | 10% | 客户忠诚度、利益相关者支持、推荐可能性 | /10 |  
**80分以上 = 客户状况良好**——保持并持续发展  
**60–79分 = 需要主动关注**  
**低于60分 = 需要干预**  

### 客户留存与增长策略  
**客户准备增加支出的信号：**  
- 询问未推荐的服务  
- 推荐你给同事  
- 说“您还能……吗？”  
- 当前合作项目实现投资回报率  
- 新的协作计划/预算周期开始  
- 关键利益相关者获得晋升（预算增加）  
**追加销售开场白：**  
“我们已经为[项目]提供了[成果]。根据目前情况，有进一步合作的潜力。需要我起草一份提案吗？”  

### 季度业务回顾（QBR）模板  
对于签订维护费合同的客户，每90天进行一次回顾：  
```
1. RESULTS RECAP (10 min)
   - KPIs: where we started vs. where we are
   - Key wins this quarter
   - ROI calculation

2. WHAT WORKED / WHAT DIDN'T (10 min)
   - Honest assessment of delivery
   - Process improvements made
   - Client feedback addressed

3. MARKET/INDUSTRY CONTEXT (5 min)
   - Relevant trends affecting their business
   - What competitors are doing
   - New opportunities you've spotted

4. NEXT QUARTER PLAN (10 min)
   - Recommended priorities
   - New ideas/initiatives to explore
   - Resource/budget implications

5. RELATIONSHIP CHECK (5 min)
   - "How's our communication working?"
   - "Anything we should do differently?"
   - "Anyone else on your team we should loop in?"
```  

### 客户离职处理  
处理客户离职时要得体——他们可能会再次合作或推荐新客户：  
```yaml
offboarding:
  - [ ] Exit interview (what went well, what didn't)
  - [ ] Final deliverables transferred
  - [ ] All access/credentials returned
  - [ ] Final invoice sent and collected
  - [ ] Knowledge transfer document provided
  - [ ] Testimonial requested (if relationship was positive)
  - [ ] Added to alumni newsletter/updates list
  - [ ] CRM status updated with reason for churn
  - [ ] Internal retrospective completed
  - [ ] Set 90-day re-engagement reminder
```  

---

## 第九阶段：机构增长策略  
### 收入集中风险  
**规则：任何单一客户的收入占比不得超过30%。**  
如果某个客户占据过高比例：  
- 积极开发新客户以分散风险  
- 不要专门为该客户招聘员工  
- 建立相当于其月收入的储备金  
**多元化接触渠道**（不要依赖单一客户）  

### 增长策略（优先级）  
1. **涨价**——涨价10%可带来约25%的利润增长（每年进行一次）  
2. **与现有客户扩展服务范围**——最经济的增长方式（追加销售、交叉销售）  
3. **获取推荐**——询问满意客户：“您还认识哪些有类似需求的人？”  
4. **提高成交率**——优化提案、加快跟进、提供案例研究  
5. **获取更多线索**——通过内容营销、合作伙伴关系、付费广告（成本最高，但效果最好）  

### 产品化服务发展路径  
从定制服务到可扩展收入的转型路径：  
```
Stage 1: Custom Projects (high margin, low scale)
↓ Identify repeated patterns
Stage 2: Templated Delivery (faster, more consistent)
↓ Package into fixed-scope offers
Stage 3: Productized Service (fixed price, predictable delivery)
↓ Build self-serve tools
Stage 4: Product + Service Hybrid (highest scale)
```  

### 机构指标仪表盘  
每周跟踪各项指标：  
```yaml
agency_dashboard:
  week_of: "YYYY-MM-DD"
  
  pipeline:
    new_leads: 0
    proposals_sent: 0
    proposals_won: 0
    win_rate: "0%"
    average_deal_size: 0
    pipeline_value: 0
    
  delivery:
    active_projects: 0
    projects_on_track: 0
    projects_at_risk: 0
    milestones_hit: 0
    milestones_missed: 0
    client_nps: 0
    
  financial:
    mrr: 0  # Monthly recurring revenue
    project_revenue: 0
    total_revenue: 0
    ar_outstanding: 0
    cash_position: 0
    
  team:
    avg_utilization: "0%"
    team_size: 0
    open_positions: 0
    attrition_ytd: 0
    
  growth:
    revenue_vs_last_month: "+0%"
    revenue_vs_last_year: "+0%"
    client_count: 0
    net_revenue_retention: "0%"  # Target: >110%
```  

---

## 第十阶段：特殊情况与高级管理  
### 处理复杂客户  
### 范围扩展问题  
- 在项目开始时明确设定界限  
- 对每个请求进行分类（参见第五阶段）  
- 每季度统计“免费”工作的累计量  
- 如果问题持续存在：**“我们已经花费了X美元用于额外工作。今后所有超出范围的调整都将通过变更订单处理。”**  

### 其他常见问题处理：  
- **沉默的客户**：  
  - 如果客户长时间不回复：**“只是想确认一下——我们需要您对[X]的反馈，以便按计划进行。”  
  - 如果超过48小时仍未回复：**“请在[日期]前给出反馈，否则进度将推迟。”  
  - 在合同中明确说明：“客户延迟会导致进度推迟[天数]。”  
- **过度干涉的客户**：  
  - 提前主动沟通，因为他们缺乏信心  
  - 每天更新进度；分享工作流程  
  - 提供“进度仪表盘”供客户随时查看  

### 多项目容量规划  
```yaml
capacity:
  total_team_hours_weekly: 0
  billable_target_hours: 0  # total × 0.75
  currently_committed: 0
  available_hours: 0
  
  projects:
    - name: ""
      hours_per_week: 0
      weeks_remaining: 0
      team_members: []
      
  can_take_new_work: true/false  # available > 20 hours
  next_availability: "YYYY-MM-DD"
```  

### 分包商管理  
**外包部分工作时：**  
- **禁止客户直接与分包商沟通**——你代表整个机构  
- **在分包商费用上加收30–50%的佣金**  
- **在分包商发票发出后7天内付款**——以建立信任  
- **签订保密协议并禁止分包商挖走客户**  
- **在交付成果前进行质量检查**  

### 远程/异步工作管理  
- **默认采用异步沟通**——会议成本较高  
- **所有工作都要记录下来**——未记录的内容视为未发生  
- **时区协调**：与客户的工作时间至少相差3小时  
- **每周召开一次协调会议**——这是必须同步进行的会议  
- **为所有工作制定标准操作流程**  

---

## 自然语言指令  
| 指令 | 机构工作人员的操作 |  
|-----|-----------|  
| “收到[公司]的新线索” | 使用BANT-S评分标准进行线索评估 |  
| “为[项目]生成提案” | 使用指定框架撰写提案 |  
| “为[客户名称]生成入职资料” | 生成入职检查清单和欢迎邮件 |  
| “向[客户]发送每周更新” | 根据项目数据生成进度更新 |  
| “检查客户健康状况” | 对所有活跃客户进行评估 |  
| **检查团队利用率” | 显示团队使用情况 |  
| **催收逾期发票** | 为逾期账款生成相应处理方案 |  
| **为[客户]生成季度回顾报告** | 生成季度评估报告 |  
| **整理机构仪表盘数据** | 汇总所有数据源的指标 |  
| **发出范围扩展警告** | 列出所有未定价的变更请求 |  
**制定增长计划** | 分析当前指标并推荐下一步增长策略 |