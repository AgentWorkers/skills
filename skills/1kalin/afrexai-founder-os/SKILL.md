---
name: Founder OS
description: >
  **从概念验证到A轮融资：完整的创业操作系统**  
  本书涵盖了客户发现、产品市场 fit（PMF）评估、融资、团队建设、财务规划以及创始人心理等方面的内容，适用于创业公司的建立、启动、业务调整或扩张阶段。
metadata: {"clawdbot":{"emoji":"🚀","os":["linux","darwin","win32"]}}
---
# Founder OS — 完整的创业操作系统

作为一名创业顾问和运营者，请遵循这套系统来指导创业者从想法走向规模化发展。每一条建议都必须具体、可操作，并基于真实的创业方法论。

---

## 第1阶段：想法验证（第1-2周）

### 问题验证简述

在编写任何代码之前，请完成以下步骤：
```yaml
problem_validation:
  problem_statement: "[WHO] struggles with [WHAT] because [WHY]"
  existing_alternatives:
    - name: ""
      weakness: ""
      price: ""
  frequency: "daily | weekly | monthly | yearly"
  severity: "annoying | painful | hair-on-fire"
  willingness_to_pay: "free-only | would-pay | actively-searching"
  target_customer:
    demographics: ""
    psychographics: ""
    watering_holes: "where they congregate online/offline"
  validation_status: "assumption | talked-to-5 | talked-to-20 | pre-orders"
```

### 停止的判断标准：
- 问题发生的频率低于每月一次，且严重程度较低
- 经过20次沟通后，对方仍表示不愿意付费
- 市场规模小于1亿美元（无法吸引投资者或维持增长）
- 你无法用一句话解释这个问题
- 现有的解决方案已经“足够好”，且切换成本较高

### 客户发现访谈脚本

**开场（2分钟）：**
“请告诉我你上次遇到[问题]的情况。请详细讲讲当时的经历。”

**深入探讨（15分钟）：**
1. “这个问题多久出现一次？”
2. “你目前是如何处理的？”（现有的解决方法反映了真实的需求）
3. “你当前的方法中最令人困扰的地方是什么？”
4. “你尝试过其他方法吗？结果如何？”
5. “如果可以变魔术，你会改变什么？”
6. “这个问题每周/每月给你带来多少时间和金钱上的成本？”

**承诺测试（3分钟）：**
- “我可以把你加入我们的测试名单吗？”（电子邮件回复 = 信号较弱）
- “你愿意每月支付X美元使用这个服务吗？”（口头回答 = 信号中等）
- “我现在可以收取X美元的费用让你提前使用吗？”（支付行为 = 信号较强）
- “你能推荐3个也有同样问题的人给我吗？”（推荐 = 信号最强）

**规则：**
- 在发现问题的过程中，绝对不要推销你的解决方案
- 绝不要问“你会使用X服务吗？”——这种假设性问题毫无意义
- 一定要询问对方过去的行为——“请告诉我你上次遇到这个问题的情况……”
- 详细记录对方的回答——措辞很重要
- 在开始任何开发之前，至少进行20次访谈

### 访谈总结模板

每进行5次访谈后，更新以下内容：
```yaml
discovery_synthesis:
  interviews_completed: 0
  top_3_problems:
    - problem: ""
      frequency: ""
      quotes: ["", ""]
      mentioned_by: "X of Y"
  patterns:
    consistent: [""]  # same across all interviews
    surprising: [""]  # didn't expect this
    contradictory: [""]  # different people say opposite things
  existing_solutions_used: [""]
  price_sensitivity: "anchored at $X-Y/mo"
  decision: "proceed | pivot-problem | pivot-customer | kill"
  confidence: "low | medium | high"
```

---

## 第2阶段：最小可行产品（MVP）与产品发布（第3-8周）

### MVP范围决策矩阵

| 方法 | 适用场景 | 时间表 | 成本 |
|----------|-------------|----------|------|
| 简单的 landing page 加等待名单 | 验证需求 | 1天 | 0-50美元 |
| “ Concierge MVP”（一站式服务） | 复杂的工作流程 | 1周 | 0美元 |
| “Wizard of Oz”模式（人工辅助的自动化产品） | 1-2周 | 0美元 |
| 无代码原型 | 简单的CRUD应用程序、市场平台 | 2-3周 | 50-200美元/月 |
| 有代码的MVP | 技术产品、API、开发者工具 | 4-6周 | 0-500美元 |

**规则：**
- 如果可以通过非代码方式验证假设，就先这么做
- MVP必须验证一个具体的假设——不是“人们是否会使用这个产品”，而是“[特定用户群体]是否会为[具体价值]支付X美元？”
- 最长开发周期为6周——如果超过这个时间，说明项目范围过大
- 首先向10位用户发布产品，而不是10,000位用户——用户的直接反馈比虚荣的指标更重要

### 产品发布检查清单
```yaml
pre_launch:
  - [ ] 20+ discovery interviews completed
  - [ ] Problem validated (frequency + severity + WTP)
  - [ ] MVP tests primary hypothesis
  - [ ] 10+ beta users committed (by name)
  - [ ] Pricing set (see pricing section)
  - [ ] Analytics installed (activation event defined)
  - [ ] Feedback channel open (Slack, email, Intercom)

launch_day:
  - [ ] Personal message to every beta user
  - [ ] Monitor activation within first 24h
  - [ ] Respond to every piece of feedback < 1h
  - [ ] Track: signups, activations, WTP confirmations

post_launch_week_1:
  - [ ] Call every activated user — what worked?
  - [ ] Call every churned user — what failed?
  - [ ] Identify top 3 friction points
  - [ ] Fix #1 friction point immediately
  - [ ] Update problem/solution hypothesis
```

---

## 第3阶段：产品与市场的匹配度（第2-12个月）

### PMF（产品市场契合度）测量框架

**Sean Ellis测试（主要指标）：**
问：“如果你不能再使用[产品]，你会感觉如何？”
- 非常失望 → 记录这些用户
- 有点失望
- 没有失望
- 不再使用（已停止使用）

**测试标准：** “非常失望”的用户占比超过40% = 产品市场契合度（PMF）达到

在用户体验到产品的核心价值后（不是第一天），进行这项调查。

**辅助指标：**

| 指标 | PMF之前 | PMF期间 | PMF之后 |
|--------|---------|-----|------------|
| Sean Ellis测试中的“非常失望”用户比例 | <25% | 40%+ | 60%+ |
| 第1周的用户留存率 | <20% | 40%+ | 60%+ |
| 第3个月的用户留存率 | <5% | 20%+ | 40%+ |
| 客户净推荐值（NPS） | <0 | 30%+ | 50%+ |
| 自然增长/推荐带来的新用户占比 | <10% | 25%+ | 50%+ |
| 月收入流失率 | >5% | <3% | <1% |

**PMF之前的运营规则：**
1. 每天与用户沟通
2. 每周至少发布一次更新
3. 不要招聘非必要的职位
4. 不要投入付费营销
5. 先修复产品问题，再优化用户体验
6. 关注用户的学习速度，而不是收入增长

### PMF决策流程
```
Week 1-2: Ship feature/change
Week 2-3: Measure impact (retention, NPS, Ellis test)
Week 3-4: Interview users about change
Week 4: Decide → double down or try something else

Repeat until 40%+ "very disappointed"
```

### 转型决策框架
```yaml
pivot_assessment:
  current_retention_trend: "improving | flat | declining"
  months_of_runway: 0
  customer_segments_tested: 0
  pivots_remaining: "runway_months / 3"  # each pivot needs ~3 months
  
  pivot_types:
    zoom_in: "One feature IS the product — kill the rest"
    zoom_out: "Product is one feature of something bigger"
    customer_segment: "Same product, different buyer"
    customer_need: "Same customer, different problem"
    channel: "Same product, different distribution"
    pricing: "Same product, different business model"
    technology: "Same problem, different solution"
  
  decision_rules:
    - "If retention is improving (even slowly) → stay the course"
    - "If flat for 3+ months after real iteration → pivot"
    - "If < 6 months runway → pivot NOW or raise bridge"
    - "If you've tested 3+ segments with same product → pivot product"
    - "If users love it but won't pay → pricing/segment pivot"
```

---

## 第4阶段：单位经济模型与定价策略

### 创业公司定价框架

**步骤1：基于价值定价**
```
Annual value delivered to customer: $________
Price = 10-20% of value delivered
Example: Save customer $50K/year → price at $5K-10K/year
```

**步骤2：选择定价模型**

| 定价模型 | 适用场景 | 是否适合扩展？ |
|-------|----------|---------------------|
| 固定月费 | 简单产品、小型企业 | 不适合——需要分级定价 |
| 按用户数量收费 | 协作工具 | 适合——用户数量越多，费用越高 |
| 按使用量收费 | API、基础设施 | 适合——使用量越多，费用越高 |
| 分层定价 | 多个用户群体 | 适合——不同用户群体有不同的定价 |
| 收益分成 | 市场平台、金融科技 | 适合——收入增长时调整价格 |

**步骤3：三层定价架构**
```yaml
pricing_tiers:
  starter:
    price: "$X/mo"  # anchor low, capture market
    features: "core value only"
    target: "individual / small team"
    purpose: "land"
    
  professional:
    price: "$3-4X/mo"  # this is where margin lives
    features: "core + collaboration + integrations"
    target: "growing team"
    purpose: "expand (should be 60-70% of revenue)"
    highlight: true  # "Most Popular" badge
    
  enterprise:
    price: "Custom ($10X+)"
    features: "everything + SSO + SLA + dedicated support"
    target: "large org"
    purpose: "signal legitimacy + capture whales"
```

**定价规则：**
- 定价要高于你的预期——你可以随时打折，但很难提高价格
- 年度折扣=两个月免费（折扣20%）——不要超过这个比例
- 绝不要只靠价格竞争——要靠价值、速度或用户体验来竞争
- 给早期用户提供优惠——忠诚度很重要
- 每季度重新评估定价——大多数创业公司定价过低

### 单位经济模型的健康状况检查
```yaml
unit_economics:
  CAC: "$___"  # total sales+marketing spend / new customers
  LTV: "$___"  # avg revenue per customer × avg lifespan in months
  LTV_CAC_ratio: "___"  # target: 3:1+
  CAC_payback_months: "___"  # target: <12
  gross_margin: "___%"  # target: >70% for SaaS
  burn_multiple: "___"  # net burn / net new ARR — target: <2
  magic_number: "___"  # net new ARR / S&M spend last quarter — target: >0.75
  
  health_assessment:
    - "LTV:CAC > 3:1 → healthy, can invest in growth"
    - "LTV:CAC 1-3:1 → cautious, optimize before scaling"  
    - "LTV:CAC < 1:1 → STOP — losing money on every customer"
    - "Payback > 18mo → cash flow problem, even if profitable long-term"
    - "Burn multiple > 3 → spending too much for growth achieved"
```

---

## 第5阶段：融资准备

### 融资准备检查清单
```yaml
raise_when:
  - [ ] You have momentum (growing MoM, not flatlined)
  - [ ] You know what the money is for (specific milestones, not "general")
  - [ ] You have 6+ months runway (raising from strength, not desperation)
  - [ ] Your story is crisp (problem → solution → traction → vision in 60 seconds)

do_not_raise_when:
  - "Pre-PMF with no traction (unless deep tech / biotech)"
  - "To avoid hard decisions about business model"
  - "Because competitors raised"
  - "When you have < 3 months runway (terms will be terrible)"
```

### 融资计算
```yaml
round_benchmarks:
  pre_seed:
    raise: "$250K-$1M"
    valuation: "$3-6M"
    dilution: "10-20%"
    what_you_need: "idea + team + early signal"
    timeline: "2-4 weeks"
    
  seed:
    raise: "$1-4M"
    valuation: "$8-15M"
    dilution: "15-25%"
    what_you_need: "$10-50K MRR or strong engagement metrics"
    timeline: "4-8 weeks"
    
  series_a:
    raise: "$5-15M"
    valuation: "$30-80M"
    dilution: "15-25%"
    what_you_need: "$1-3M ARR, 3x+ YoY growth, clear PMF"
    timeline: "8-16 weeks"

instruments:
  SAFE:
    pros: "fast, simple, no board seat, no maturity date"
    cons: "uncapped = bad for founder, stacking SAFEs = dilution surprise"
    use_when: "pre-seed, angel rounds, speed matters"
    
  convertible_note:
    pros: "familiar to angels, interest accrues"
    cons: "maturity date pressure, more legal work"
    use_when: "bridge rounds, angel-heavy rounds"
    
  priced_round:
    pros: "clean cap table, board governance, signals maturity"
    cons: "expensive legal ($15-30K), takes longer"
    use_when: "seed+ with institutional VCs"
```

### 演讲稿结构（最多10-12页）
```yaml
deck_structure:
  1_title: "Company name, one-line description, your name"
  2_problem: "Specific pain point with data — make them FEEL it"
  3_solution: "How you solve it — demo screenshot or 3-step process"
  4_demo: "Show, don't tell — screenshot or video link"
  5_market: "TAM/SAM/SOM with bottom-up logic, not top-down fantasy"
  6_business_model: "How you make money, current pricing, unit economics"
  7_traction: "The slide that matters most — chart goes up and to the right"
  8_team: "Why THIS team wins — relevant experience, not impressive titles"
  9_competition: "Honest positioning — category creation or clear differentiator"
  10_financials: "18-month projection, assumptions stated, use of funds"
  11_ask: "Amount raising, milestones it unlocks, timeline"

rules:
  - "Traction slide = most important. If chart doesn't impress, you're not ready."
  - "One point per slide. No text walls."
  - "TAM/SAM/SOM = bottom-up (# customers × price), not 'it's a $50B market'"
  - "Team slide: show domain expertise, not pedigree"
  - "Competition: never say 'no competitors' — it means no market"
  - "Financial projections: realistic Year 1, ambitious Year 3"
```

### 面对风险投资家的会议流程

**会议前：**
- 研究潜在投资家的投资组合、博客文章和Twitter动态
- 找到你们投资组合中的共同点——提及相关公司
- 准备好回答这些问题：“你的竞争优势是什么？”以及“为什么现在是合适的时机？”

**30分钟演讲内容：**
```
0-2 min: Hook — start with the problem story (specific customer, not abstract)
2-5 min: Solution — show, don't tell
5-8 min: Traction — numbers, growth, quotes
8-12 min: Market + business model
12-15 min: Team + why you
15-30 min: Q&A (this is where deals are won or lost)
```

**会议后：**
- 在会议后2小时内发送跟进信息——内容简洁，最多包含3点
- 如果对方说“让我考虑一下”，在5个工作日内再次联系
- 如果对方表示“我们愿意进一步讨论”，当天提供数据室访问权限
- 记录所有接触过的风险投资家的进展：冷启动 → 介绍 → 第一次会议 → 合作会议 → 投资条款书 → 完成交易

**常见风险投资家问题（提前准备答案）：**
1. “什么让你夜不能寐？”
2. “为什么你认为这个项目能成长为价值10亿美元的公司？”
3. “如果竞争对手复制了你的产品，你会怎么办？”
4. “随着业务扩张，你的客户获取成本（CAC）会如何变化？”
5. “是什么让你考虑放弃这个项目？”
6. “为什么你的公司增长速度不够快？”
7. “请给我讲讲一个差点流失的客户的情况——发生了什么？”

---

## 第6阶段：团队建设（前20次招聘）

### 招聘决策框架
```yaml
hire_when:
  - "Role has been painfully vacant for 4+ weeks"
  - "You (founder) are doing the job AND it's blocking growth"
  - "Revenue supports the hire within 6 months"
  - "You can describe success in 90 days clearly"

do_not_hire_when:
  - "You're lonely and want company"
  - "Investor told you to 'build the team'"
  - "Someone impressive is available (hire for need, not availability)"
  - "You haven't done the job yourself (you can't evaluate candidates)"
```

### 前10次招聘的优先级

| 招聘顺序 | 职位 | 招聘理由 |
|--------|------|---------|
| 1-2 | 共同创始人/技术负责人 | 无法独自完成项目 |
| 3 | 第一名工程师 | 加快产品发布速度 |
| 4 | 面向客户的团队成员（客服/销售） | 创始人无法与所有客户直接沟通 |
| 5 | 第二名工程师 | 解决技术瓶颈 |
| 6 | 营销/增长团队 | 需要更多渠道来获取客户 |
| 7-8 | 工程师 | 扩大产品规模 |
| 9 | 运营/财务团队 | 管理工作占用了创始人的太多时间 |
| 10 | 第一名经理 | 扩大管理范围 |

### 早期阶段的薪酬体系
```yaml
compensation_bands:
  pre_seed:
    founder_salary: "$0-60K (below market)"
    early_employee: "60-80% of market + 0.5-2% equity"
    equity_pool: "10-15% of company"
    vesting: "4 years, 1-year cliff"
    
  seed:
    founder_salary: "$80-120K"
    early_employee: "80-90% of market + 0.1-0.5% equity"
    equity_pool: "10-15%"
    
  series_a:
    founder_salary: "$120-180K"
    employee: "market rate + 0.01-0.1% equity"
    equity_pool: "10-12% (refresh grants)"

equity_rules:
  - "First 5 employees: 0.5-2% each"
  - "Employees 6-15: 0.1-0.5% each"
  - "Employees 16-30: 0.05-0.25% each"
  - "Always use 4-year vesting with 1-year cliff"
  - "Double-trigger acceleration on M&A (not single)"
  - "83(b) election within 30 days — ALWAYS remind employees"
```

### 文化与沟通

**每周的团队例会（不可协商）：**
```yaml
weekly_cadence:
  monday:
    - "All-hands (15 min): this week's goals, blockers, wins"
    - "Founder shares 1 customer story"
  daily:
    - "Async standup: done yesterday, doing today, blocked by"
  friday:
    - "Week review: what worked, what didn't, 1 lesson learned"
    - "Ship log: what went live this week"
  monthly:
    - "Town hall: metrics, roadmap, Q&A (radical transparency)"
    - "1:1s with every direct report (30 min)"
```

---

## 第7阶段：财务规划与运营计划

### 创业公司的财务模型（简化版）
```yaml
monthly_tracking:
  revenue:
    mrr: 0
    mrr_growth_rate: "0%"
    arr: "MRR × 12"
  costs:
    team: 0  # salaries + benefits + contractors
    infrastructure: 0  # hosting, tools, SaaS
    marketing: 0  # paid + content + events
    other: 0  # legal, office, travel
    total_burn: 0
  metrics:
    net_burn: "total_costs - revenue"
    runway_months: "cash_balance / net_burn"
    runway_weeks: "runway_months × 4.3"  # think in weeks, not months
    default_alive: "if growth_rate continues, will revenue > costs before cash = 0?"
```

**现金管理规则：**
- 必须明确公司的运营周期——说“6个月”听起来安全，但“26周”会带来紧迫感
- 如果运营周期少于6个月，立即削减成本或寻求融资
- 如果运营周期少于3个月，进入紧急状态：立即削减所有非必要的开支
- 保留至少2个月的运营费用作为备用资金
- 收入是公司的生命线——免费试用和“以后再付钱”的策略会毁掉公司

### 情景规划
```yaml
scenarios:
  best_case:
    mrr_growth: "20% MoM"
    new_hires: "as planned"
    fundraise: "on schedule"
    runway: "___"
    
  base_case:
    mrr_growth: "10% MoM"
    new_hires: "only critical"
    fundraise: "3 months delayed"
    runway: "___"
    
  worst_case:
    mrr_growth: "0%"
    new_hires: "freeze"
    fundraise: "fails"
    runway: "___"
    action_plan: "what do you cut to survive 12+ months?"
```

---

## 第8阶段：创始人心理与韧性

### 能量管理框架
```yaml
founder_energy:
  high_energy_tasks: "customer calls, hiring, fundraising, product decisions"
  low_energy_tasks: "admin, email, reporting, routine meetings"
  
  rules:
    - "Schedule high-energy work in your peak hours (morning for most)"
    - "Batch low-energy tasks to afternoon blocks"
    - "Never fundraise AND do product work in the same day"
    - "One CEO day per week: stepping back to think strategically"
    - "Sleep 7+ hours — non-negotiable. Exhaustion kills judgment."
    
  burnout_signals:
    - "Dreading Monday morning → step back, not push through"
    - "Snapping at team → you need rest, not discipline"
    - "Can't make decisions → information overload, reduce inputs"
    - "Working weekends regularly → broken system, not work ethic"
    
  recovery_actions:
    - "24h fully offline — phone off, no Slack"
    - "Talk to a founder peer (not advisor, not investor)"
    - "Exercise — any kind, just move"
    - "Revisit WHY you started — reconnect with mission"
```

### 在压力下的决策制定
```yaml
decision_framework:
  type_1: "irreversible (fundraising terms, firing, pivoting)"
    process: "sleep on it, get 2 outside opinions, decide in 48h"
  type_2: "reversible (features, pricing experiments, marketing channels)"
    process: "decide in < 1 day, run experiment, adjust"
    
  when_stuck:
    - "Ask: 'What would I do if I had to decide in 5 minutes?'"
    - "Ask: 'What would I regret NOT doing in 6 months?'"
    - "Ask: 'If I do nothing, what happens?'"
    - "Ask: 'Am I avoiding this because it's hard or because it's wrong?'"
```

### 创始人支持系统

**组建非正式的顾问团队：**
```yaml
support_network:
  founder_peer_group:
    what: "3-5 founders at same stage"
    frequency: "bi-weekly dinner or call"
    purpose: "no one else understands"
    
  mentor:
    what: "1-2 people who've done this before"
    frequency: "monthly call"
    purpose: "pattern recognition you don't have"
    
  executive_coach:
    what: "professional who holds mirror up"
    frequency: "bi-weekly session"
    purpose: "you don't know your blind spots"
    
  partner_family:
    what: "keep them informed, not surprised"
    frequency: "weekly honest update"
    purpose: "they're on this ride too"
```

---

## 第9阶段：产品扩张策略（产品市场契合度之后）

### 扩张准备检查清单
```yaml
scale_when:
  - [ ] PMF confirmed (40%+ Ellis test, strong retention)
  - [ ] Unit economics positive (LTV:CAC > 3:1)
  - [ ] At least 2 acquisition channels working
  - [ ] Onboarding is systematized (doesn't need founder)
  - [ ] Core team can operate without founder for 1 week
  - [ ] Gross margin > 60%

do_not_scale_when:
  - "PMF is 'sort of' there — 30% Ellis test"
  - "Only one channel works (founder selling)"
  - "Customers love it but CAC payback > 18 months"
  - "Product requires heavy customization per customer"
```

### 成长推动因素

| 推动因素 | 阶段 | 需要的投资 | 时间表 |
|-------|-------|-----------|----------|
| 创始人销售 | 种子轮 → 预种子轮 | 需要创始人投入时间 | 立即 |
| 内容与搜索引擎优化（SEO） | 种子轮 | 需要1名内容编辑 | 6-12个月 |
| 推荐计划 | 获得10位满意客户后 | 需要工程师时间 | 1-3个月 |
| 付费获取客户 | 在单位经济模型稳定后 | 需要预算 | 立即，但成本较高 |
| 合作伙伴关系 | 品牌知名度提升后 | 需要招聘商务拓展人员 | 3-6个月 |
| 产品驱动的增长 | 在发现具有传播力的功能后 | 需要工程师 | 3-6个月 |
| 外部销售 | 在验证了扩张策略后 | 需要销售团队 | 2-4个月 |

---

## 常用命令

1. “验证我的创业想法” → 运行第1阶段的想法验证流程
2. “我准备好融资了吗？” → 运行融资准备检查清单
3. “审核我的演讲稿” → 根据演讲稿结构和常见风险投资家问题进行评估
4. “我应该转型吗？” → 运行转型决策流程
5. “检查我的单位经济模型” → 计算客户生命周期价值（LTV）与客户获取成本（CAC），以及资金消耗情况
6. “规划我的下一次招聘” → 使用招聘决策框架和优先级顺序
7. “我的运营周期如何？” → 分析财务模型和情景规划
8. “帮我制定产品定价” → 完整的定价策略
9. “为与[投资人姓名]的会议做准备” → 阅读会议流程和可能被问到的问题
10. “我感到精疲力竭了” → 学习能量管理方法并采取恢复措施
11. “评估我的产品市场契合度” → 运用Sean Ellis测试和辅助指标
12. “建立我的融资渠道” → 建立风险投资家跟踪系统并安排沟通计划

---

## 特殊情况

### 单人创始人
- 优点：决策更快，拥有全部股权
- 缺点：想法未经验证，投资者可能对单人创始人持偏见
- 应对措施：组建强大的顾问团队，同时寻找联合创始人，并展示项目的快速进展

### 技术型创始人与非技术型创始人
- 技术型创始人：可以快速开发产品，但如何销售？
- 非技术型创始人但有创意：在开始开发之前先找到技术合伙人
- 绝不要将核心产品外包给第三方机构——需要内部团队来负责

### 自筹资金与风险投资支持
```yaml
bootstrap_when:
  - "Market is niche (<$1B TAM) but profitable"
  - "Business model works from day 1 (services, SaaS with clear buyer)"
  - "You want control and lifestyle design"
  - "Growth rate of 50-100% YoY is acceptable"

raise_vc_when:
  - "Winner-take-most market dynamics"
  - "Need to spend before earning (marketplace, hardware, deep tech)"
  - "Speed is everything (AI, crypto — windows close fast)"
  - "TAM > $10B and you want to go big"
```

### 国际创始人
- 如果目标是美国的风险投资家，可以在特拉华州注册公司（C-Corp）
- 使用Stripe Atlas、Firstbase或Clerky等工具
- 对于非美国投资者，可以考虑在开曼群岛设立公司
- 签证问题：O-1（特殊才能）或L-1（转移签证）——不适用H-1B签证

### 第二次创业的创始人
- 融资速度更快，但期望也更高
- 避免与第一次创业时重复相同的模式——新公司需要新的策略
- 最大的风险是招聘过快（虽然有资金，但产品市场契合度（PMF）尚未建立）

---

---

（注：由于文档内容较长，部分内容在翻译时进行了简化处理。如果需要更详细的翻译，请提供完整的SKILL.md文件。）