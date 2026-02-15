---
name: afrexai-startup-metrics-engine
model: default
version: 1.0.0
description: 完整的启动指标指挥中心——从原始数据到面向投资者的仪表板。涵盖所有阶段（种子轮到B+轮融资），所有业务模式（SaaS、市场平台、消费产品、硬件），提供诊断工具、基准测试数据库以及适合董事会使用的报告功能。
tags: [startup, metrics, saas, kpis, unit-economics, growth, fundraising, investor, dashboard, arr, mrr, churn, ltv, cac]
---
# 启动指标指挥中心  
（Startup Metrics Command Center）  

这是一个全面的系统，用于追踪、诊断并传达公司的运营健康状况——不仅仅是具体的数据指标，更重要的是思考这些指标的选取依据、监测时机，以及当数据异常时应采取的措施。  

---

## 第一阶段：指标体系构建（Phase 1: Metrics Architecture）  

### 第一步：确定业务模型与所处的阶段  
在开始追踪任何指标之前，首先明确自己的业务模型和所处的发展阶段：  

**业务模型（Business Model）：**  
```yaml
model_type:
  saas:
    sub_type: # self-serve | sales-led | PLG | hybrid
    pricing: # per-seat | usage-based | flat | tiered
    contract: # monthly | annual | multi-year
  marketplace:
    type: # managed | unmanaged | SaaS-enabled
    unit: # GMV | take-rate | transaction
  consumer:
    type: # subscription | ad-supported | freemium | transactional
    engagement_model: # DAU/MAU | session-based | content
  hardware_plus_software:
    type: # device + subscription | IoT | embedded
```  

**发展阶段（Determines what to track）：**  
| 阶段 | 收入范围（ARR） | 关键关注点 | 董事会关心的指标 |  
|-------|-----------|-------------------|-------------------|  
| 预种子期（Pre-seed） | 0–5万美元 | 用户活跃度与留存率 | 产品与问题的匹配度 |  
| 种子期（Seed） | 5万–50万美元 | 用户群体留存率与早期收入 | 产品与市场的契合度 |  
| A轮融资期（Series A） | 500万–300万美元 | 增长效率与单位经济指标 | 生命周期价值（LTV）与客户获取成本（CAC）、新客户转化率（NDR）、增长率 |  
| B轮融资期（Series B） | 300万–1500万美元 | 可扩展性及运营效率 | 40法则、关键运营指标（如“burn multiple”） |  
| 成长期（Growth） | 1500万美元以上 | 资本利用效率与市场份额 | 净利润率（Net Margin）、新客户留存率（NRR）、竞争优势（Competitive Moat） |  

### 第二步：构建指标体系  
**第一层：日常监控的健康指标（Health Vitals, tracked daily）**  
```
- Revenue: MRR, ARR, net new MRR
- Growth: MoM growth rate, WoW for early stage
- Retention: Logo churn rate, revenue churn rate
- Cash: Monthly burn, runway in months
```  
**第二层：每周监控的效率指标（Efficiency, tracked weekly）**  
```
- Unit economics: CAC, LTV, LTV:CAC ratio, payback months
- Sales: Pipeline coverage, win rate, sales cycle length
- Product: Activation rate, feature adoption, NPS/CSAT
- Team: Revenue per employee, quota attainment
```  
**第三层：每月监控的战略指标（Strategic indicators, tracked monthly）**  
```
- NDR (Net Dollar Retention)
- Burn multiple
- Rule of 40 score
- Magic number
- Cohort analysis curves
```  

---

## 第二阶段：完整的指标参考体系（Phase 2: Complete Metric Reference）  

### 收入相关指标（Revenue Metrics）  
```
MRR = Σ(active_subscriptions × monthly_price)
ARR = MRR × 12

Net New MRR = New MRR + Expansion MRR - Churned MRR - Contraction MRR

MRR Components:
  new_mrr:         First-time customer revenue this month
  expansion_mrr:   Upsell + cross-sell from existing customers
  churned_mrr:     Revenue lost from customers who left
  contraction_mrr: Revenue lost from downgrades (customer stayed)
  reactivation_mrr: Revenue from returning churned customers

MoM Growth = (MRR_current - MRR_previous) / MRR_previous
CMGR (Compound Monthly Growth Rate) = (MRR_end / MRR_start)^(1/months) - 1
```  
**为什么使用月度增长率（CMGR）而非环比增长率（MoM）？**  
月度增长率波动较大，而月度增长率（CMGR）能够平滑6–12个月的数据，从而更准确地反映真实趋势。  

### 单位经济指标（Unit Economics）  
```
CAC = Total_Sales_Marketing_Spend / New_Customers_Acquired
  - Include: salaries, commissions, tools, ads, events, content costs
  - Exclude: product/engineering, CS (post-sale)
  - Time-lag adjustment: match spend to cohort it generated (typically 1-3 month lag)

Blended CAC vs Channel CAC:
  blended_cac = total_spend / total_new_customers
  channel_cac = channel_spend / channel_new_customers
  # Always track both — blended hides channel problems

LTV = ARPU × Gross_Margin% × Average_Customer_Lifetime
  # Or: LTV = ARPU × Gross_Margin% × (1 / Monthly_Churn_Rate)
  # Cap at 5 years for conservative estimates

LTV:CAC Ratio — THE ratio:
  > 5.0  → Under-investing in growth (spend more!)
  3.0-5.0 → Excellent efficiency
  1.5-3.0 → Healthy but watch payback period
  1.0-1.5 → Marginal — fix churn or reduce CAC
  < 1.0  → Burning cash per customer — STOP and fix

CAC Payback = CAC / (Monthly_ARPU × Gross_Margin%)
  < 6 months  → Elite (PLG companies)
  6-12 months → Great
  12-18 months → Acceptable for enterprise
  > 18 months → Danger zone (unless >130% NDR)
```  
### 用户留存与流失（Retention & Churn）  
```
Logo Churn Rate = Customers_Lost / Customers_Start_of_Period
Revenue Churn Rate = MRR_Lost / MRR_Start_of_Period
  # Revenue churn > logo churn = losing big customers (very bad)
  # Revenue churn < logo churn = losing small customers (less bad)

Net Dollar Retention (NDR) = (Starting_MRR + Expansion - Contraction - Churn) / Starting_MRR
  > 130% → World-class (Snowflake, Twilio territory)
  110-130% → Excellent
  100-110% → Good
  90-100% → Acceptable but concerning
  < 90% → Leaky bucket — growth can't outrun churn

Gross Dollar Retention (GDR) = (Starting_MRR - Contraction - Churn) / Starting_MRR
  # NDR without expansion — shows your floor
  > 90% → Sticky product
  80-90% → Normal for SMB
  < 80% → Product or market problem
```  
### 增长效率（Growth Efficiency）  
```
Burn Multiple = Net_Burn / Net_New_ARR
  < 1.0 → Amazing (rare at early stage)
  1.0-1.5 → Great
  1.5-2.0 → Good
  2.0-3.0 → Mediocre
  > 3.0 → Bad — inefficient growth

Rule of 40 = Revenue_Growth_Rate% + Profit_Margin%
  > 40 → Healthy SaaS (IPO-ready)
  # Example: 60% growth + -20% margin = 40 ✓
  # Example: 20% growth + 20% margin = 40 ✓

Magic Number = Net_New_ARR_This_Quarter / Sales_Marketing_Spend_Last_Quarter
  > 1.0 → Efficient, invest more in S&M
  0.5-1.0 → OK, optimize before scaling
  < 0.5 → Inefficient — fix before spending more

Hype Ratio = Valuation / ARR
  # Reality check on fundraising expectations
  # Median SaaS multiples: 6-12x ARR (varies by growth + retention)
```  
### 现金流与运营周期（Cash & Runway）  
```
Monthly Burn = Total_Monthly_Expenses - Total_Monthly_Revenue
Gross Burn = Total_Monthly_Expenses (ignoring revenue)
Net Burn = Gross_Burn - Revenue

Runway = Cash_Balance / Monthly_Net_Burn
  > 18 months → Comfortable
  12-18 months → Start planning next raise
  6-12 months → Urgently fundraising
  < 6 months → Default alive or dead calculation needed

Default Alive? = Can_Current_Growth_Rate_Make_Revenue > Expenses_Before_Cash_Runs_Out
  # Paul Graham's test — if growing, project the intersection
```  
### 销售效率（Sales Efficiency）  
```
Sales Cycle Length = Avg_Days(First_Touch → Closed_Won)
Pipeline Coverage = Total_Pipeline_Value / Revenue_Target
  # Need 3-4x for predictable revenue
  
Win Rate = Deals_Won / Total_Deals_in_Stage
  By stage: SQL→Opp (30-40%), Opp→Proposal (50-60%), Proposal→Close (60-70%)

ACV (Annual Contract Value) = Total_Contract_Value / Contract_Years
ASP (Average Selling Price) = Total_Revenue / Deals_Closed

Quota Attainment = Actual_Bookings / Quota_Target
  # Healthy org: 60-70% of reps hitting quota

Sales Efficiency = Net_New_ARR / Fully_Loaded_Sales_Cost
  > 1.0 → Scalable
```  

---

## 第三阶段：诊断框架——PULSE方法（Phase 3: Diagnostic Framework – PULSE Method）  
当某个指标出现异常时，不要仅仅报告结果，而是要深入分析其原因：  

### P – 模式识别（Pattern Recognition）  
```
Questions:
- Is this a trend (3+ months) or a blip (1 month)?
- Is it seasonal or structural?
- Did it change gradually or suddenly?
- Which cohorts/segments are affected?
```  
### U – 上游原因追踪（Upstream Tracing）  
```
Every metric has upstream drivers. Trace back:

Revenue declining? →
  ├── New MRR down? → Lead volume? → Conversion rate? → Channel performance?
  ├── Expansion down? → Upsell attempts? → Product adoption? → CSM activity?
  └── Churn up? → Which segment? → Voluntary vs involuntary? → Reasons?

CAC increasing? →
  ├── Spend up? → Which channels? → CPM/CPC changes?
  ├── Volume same but cost up? → Market saturation? → Competition?
  └── Conversion down? → Funnel stage? → Lead quality? → Sales process?
```  
### L – 关键影响点（Leverage Point）  
```
Find the highest-impact intervention:
- Which single metric, if improved 10%, would cascade the most?
- What's the cheapest/fastest fix vs highest-impact fix?
- Score: Impact (1-5) × Feasibility (1-5) × Speed (1-5)
```  
### S – 后续行动方案（So-What Translation）  
```
Convert metric into business language:
- "Churn increased 2%" → "We'll lose $X00K ARR this year at this rate"
- "CAC payback is 18 months" → "Each new customer is cash-negative for 1.5 years"
- "NDR is 95%" → "Even with zero new sales, we shrink 5% annually"
```  
### E – 实验设计（Experiment Design）  
```yaml
diagnostic_experiment:
  hypothesis: "[Metric] is declining because [upstream cause]"
  test: "[Specific action] for [time period]"
  success_metric: "[Metric] improves by [X%] within [timeframe]"
  sample: "[Segment/cohort to test on]"
  kill_criteria: "Stop if [negative signal] within [days]"
```  

---

## 第四阶段：群体分析（Phase 4: Cohort Analysis）  
汇总后的数据可能具有误导性，而群体分析才能揭示真相：  
**收入群体分析表（Revenue Cohort Table）**  
```
Track each monthly cohort's MRR over time:

         Month 0   Month 1   Month 3   Month 6   Month 12
Jan '25  $50K      $48K      $45K      $42K      $38K
Feb '25  $55K      $53K      $50K      $48K      —
Mar '25  $60K      $58K      $57K      $56K      —
Apr '25  $45K      $44K      $43K      —         —

Reading this:
- Jan cohort retained 76% at month 12 → mediocre
- Mar cohort retained 93% at month 3 → improving! What changed?
- Apr cohort started smaller but retention looks good
```  
**用户活跃度群体分析（Non-revenue signals）**  
```yaml
cohort_engagement:
  week_1_activation: # % completing key action within 7 days
  week_4_habit: # % using product 3+ days in week 4
  month_3_retention: # % still active at 90 days
  
  # Leading indicators of revenue retention
  # If engagement drops, revenue follows 1-3 months later
```  
**异常群体警示（Cohort Red Flags）**  
```
🚩 Each new cohort retains worse → product-market fit eroding
🚩 Large cohorts churn more → scaling quality issues
🚩 Specific channel cohorts churn fast → bad-fit leads
🚩 Expansion only in old cohorts → pricing/packaging problem
```  

---

## 第五阶段：董事会与投资者报告（Phase 5: Board & Investor Reporting）  
### 月度投资者更新模板（Monthly Investor Update Template）  
```yaml
investor_update:
  subject: "[Company] — [Month] Update: [One-line headline]"
  
  # 1. TL;DR (3 bullets max)
  highlights:
    - "ARR: $X (+Y% MoM) — [context]"
    - "Key win: [biggest achievement]"
    - "Challenge: [biggest problem + what you're doing]"
  
  # 2. Key Metrics Table
  metrics:
    arr: {current: "", prior_month: "", delta: ""}
    mrr: {current: "", growth_mom: ""}
    customers: {total: "", new: "", churned: ""}
    ndr: ""
    burn_rate: ""
    runway_months: ""
    cash_balance: ""
    
  # 3. What Happened (5-7 bullets)
  wins: []
  challenges: []
  
  # 4. What's Next (3-5 bullets)
  next_month_priorities: []
  
  # 5. Asks (be specific!)
  asks:
    - intro: "Looking for intro to [person/company] for [reason]"
    - advice: "Would love 15 min on [specific topic]"
    - hiring: "Seeking [role] — know anyone?"
```  
### 董事会汇报用的指标幻灯片（Board Deck Metric Slides）  
**幻灯片1：业务健康状况仪表盘（Business Health Dashboard）**  
```
ARR: $___     MoM: ___%     NDR: ___%
Customers: ___  New: ___    Churned: ___
Runway: ___ months          Burn Multiple: ___

Traffic light: 🟢 On track | 🟡 Watch | 🔴 Action needed
```  
**幻灯片2：收入结构图（Revenue Waterfall）**  
```
Starting MRR:     $___
+ New:            $___
+ Expansion:      $___
- Contraction:    $___
- Churn:          $___
= Ending MRR:     $___
```  
**幻灯片3：单位经济指标（Unit Economics）**  
```
CAC: $___  →  LTV: $___  →  LTV:CAC: ___x
Payback: ___ months
Blended vs top channel efficiency
```  

---

## 第六阶段：特定业务模型的指标（Phase 6: Model-Specific Metrics）  
### SaaS业务相关指标（SaaS Additions）  
```
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
  > 4.0 → Very healthy growth
  2.0-4.0 → Good
  1.0-2.0 → Sustainable but slow
  < 1.0 → Shrinking

Logo-to-Revenue Retention Gap:
  If logo retention 85% but revenue retention 95% → upsell compensates
  If logo retention 85% and revenue retention 85% → no expansion = problem

Expansion Revenue % = Expansion MRR / Total New MRR
  > 30% → Healthy at scale
  # Best SaaS: expansion > new revenue (Twilio was 170% NDR)
```  
### 市场平台相关指标（Marketplace Additions）  
```
GMV (Gross Merchandise Value) = Total value of transactions on platform
Take Rate = Platform Revenue / GMV
  5-15% → Typical for most marketplaces
  15-30% → Managed/full-service marketplaces
  
Supply-side metrics:
  supply_liquidity = listings_with_transaction / total_listings
  time_to_first_match = avg_days_from_listing_to_sale
  
Demand-side metrics:
  search_to_fill = completed_transactions / searches
  repeat_purchase_rate = returning_buyers / total_buyers
```  
### 消费者付费/免费增值服务相关指标（Consumer/PLG Additions）  
```
DAU/MAU Ratio:
  > 50% → Exceptional (messaging apps)
  25-50% → Strong habit (social, productivity)
  10-25% → Good (media, entertainment)
  < 10% → Weak engagement

Viral Coefficient (K-factor) = Invites_per_User × Conversion_Rate
  > 1.0 → Viral growth (each user brings >1 new user)
  0.5-1.0 → Amplified growth
  < 0.5 → Not viral — need paid acquisition

Free-to-Paid Conversion:
  PLG benchmark: 2-5% of free users convert
  Freemium benchmark: 1-3%
  Enterprise self-serve: 5-15%

Time to Value = Time from signup to "aha moment"
  # Reduce this aggressively — strongest lever for activation
```  

---

## 第七阶段：指标操纵的警示信号（Phase 7: Metric Manipulation Red Flags）  
**区分表面指标与真正有意义的指标**：  
| 应避免的虚假指标（Vanity Metrics） | 应关注的真实指标（Real Metrics） |  
| ---------------- | ------------------ |  
| 总注册用户数 | 激活用户数（完成关键操作的用户） |  
| 页面浏览量 | 实际参与互动的用户（停留时间超过2分钟或采取行动的用户） |  
| “潜在客户池” | 符合销售转化条件的潜在客户 |  
| 总收入 | 扣除退款和退款后的净收入 |  
| 总客户数 | 过去30天内登录过的活跃客户 |  
| 下载次数 | 每日活跃用户数/每月活跃用户数（WAU/MAU） |  
| “合作伙伴关系” | 来自合作伙伴的收入 |  
### 常见的指标操纵手段（Common Manipulation Tactics）**  
```
🚩 Counting annual contracts as MRR at signing (vs. monthly recognition)
🚩 Excluding "one-time" churns from churn rate
🚩 Using gross revenue instead of net
🚩 Measuring CAC without fully-loaded costs
🚩 Cherry-picking best cohort as "representative"
🚩 Counting reactivations as new customers
🚩 Using "committed ARR" (signed but not live)
🚩 Trailing-12-month NDR when recent cohorts are worse
```  

---

## 第八阶段：应对策略（Phase 8: Action Playbooks）  
### 当客户获取成本（CAC）过高时（When CAC is too high）  
```
1. Audit channel efficiency — kill bottom 20% channels
2. Improve activation rate (reduces wasted spend)
3. Increase conversion at each funnel stage (+10% each = compound effect)
4. Shift mix: more organic/PLG, less paid
5. Reduce sales cycle length (lower cost per deal)
6. Tighten ICP — stop selling to bad-fit customers
```  
### 当用户流失率（Churn）过高时（When Churn is too high）  
```
1. Segment: which customers churn? (Size, channel, use case)
2. Time: when do they churn? (Month 1-3 = onboarding, 6-12 = value, 12+ = competition)
3. Reason: exit survey + CS interviews (top 3 reasons)
4. Fix activation if month 1-3 churn
5. Fix value delivery if month 6-12 churn
6. Fix switching cost / competitive moat if 12+ churn
```  
### 当增长停滞时（When Growth Stalls）  
```
1. Check: is TAM exhausted in current segment? → Expand to adjacent
2. Check: conversion rates declining? → Product or message fatigue
3. Check: CAC rising with flat volume? → Channel saturation
4. Check: expansion revenue flat? → Packaging/pricing problem
5. Check: sales cycle lengthening? → Market conditions or competition
```  
### 在融资阶段（When raising capital）  
```
Metrics investors care about BY STAGE:

Pre-seed: Engagement, retention curves, market size
Seed: MoM growth (15%+), retention cohorts, early unit economics
Series A: $1M+ ARR, 3x+ YoY growth, LTV:CAC > 3, NDR > 100%
Series B: $5M+ ARR, path to Rule of 40, burn multiple < 2, sales efficiency
```  

---

## 常用命令（Quick Commands）：  
- “为[阶段][业务模型]的初创公司设置指标体系” → 完整的指标体系建议  
- “诊断[具体指标]” → 使用PULSE诊断框架  
- “为[月份]准备投资者更新报告” → 提供模板及指导  
- “对[数据]进行群体分析” → 分析用户留存曲线  
- “与基准数据进行对比” → 根据阶段特点分析差距  
- “为A/B轮融资准备哪些指标？” → 为投资者准备的检查清单  
- “根据[数据]计算单位经济指标” → 计算生命周期价值（LTV）、客户获取成本（CAC）、投资回收期  
- “检查警示信号” → 审查指标中的异常情况  
- “生成董事会汇报用的指标视图” → 生成适合展示的幻灯片内容  

---

## 特殊情况处理（Edge Cases）：  
### 多产品公司（Multi-Product Companies）  
需分别追踪每个产品线的指标，并进行综合分析。注意是否存在产品间的相互补贴现象（即一个产品的利润掩盖了另一个产品的亏损）。  
### 基于使用量的定价（Usage-Based Pricing）  
每月收入（MRR）是预估值，而非合同约定的金额。应追踪实际使用的资源与产生的收入。由于用户使用量会自然增长，新客户转化率（NDR）通常会较高——因此应与同类基于使用量的公司进行比较，而非基于座位数的公司。  
### 由于价格上涨导致的用户流失（Negative Churn due to Price Increases）  
如果新客户转化率（NDR）上升超过100%仅因价格上涨（而非自然增长），说明公司的运营模式存在问题。需区分价格驱动与使用量驱动的增长情况。  
### 非盈利阶段（Pre-Revenue）  
此时应重点追踪关键指标：激活率、用户活跃频率、净推荐值（NPS）、候补用户数量、自然流量以及用户价值实现时间。收入指标可以稍后再收集。  
### 季节性业务（Seasonal Businesses）  
使用同比（YoY）而非环比（MoM）进行数据分析。根据季节性规律调整群体分析方法，并建立季节性预测模型。  

---

*由AfrexAI开发——将数据转化为实际收益（Built by AfrexAI – Turning data into revenue.）*