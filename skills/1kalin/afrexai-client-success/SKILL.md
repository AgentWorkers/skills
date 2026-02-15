# 客户留存与收入增长——一套完整的留存操作系统

将客户转化为长期的收入来源。这不仅仅是一些建议，而是一套完整的操作系统，其中包含了评分模型、模板、操作手册和自动化方案，适用于任何B2B或B2C订阅业务。

## 适用场景

- 全面设计或审计您的客户留存策略
- 客户出现流失迹象，需要采取干预措施
- 建立有效的入职流程（前90天）
- 从现有账户中规划收入增长
- 进行季度业务回顾（QBR）
- 分析客户留存数据并找出流失原因
- 为流失用户制定重新激活计划
- 建立客户健康评分系统
- 防止非自愿流失（如支付失败）

## 不适用场景

- 获取全新的客户（使用潜在客户开发/外展技巧）
- 一次性产品销售，没有重复购买行为
- 客户确实不合适——礼貌地放弃他们

---

## 第一阶段：客户健康评分（您的早期预警系统）

在开始任何行动之前，首先建立客户健康评分。没有评分系统，您将毫无头绪——只能对流失做出反应，而无法预防它。

### 健康评分模型（0-100分）

每周对每个账户进行评分。尽可能实现自动化。

```yaml
health_score:
  dimensions:
    usage:
      weight: 30
      signals:
        - login_frequency_vs_baseline: # % of their normal
            90-100%: 10
            70-89%: 7
            50-69%: 4
            below_50%: 1
        - core_feature_adoption: # % of key features used
            4+_features: 10
            3_features: 7
            2_features: 4
            1_or_fewer: 1
        - depth_of_usage: # power user vs surface
            advanced_features: 10
            intermediate: 6
            basic_only: 3
    
    engagement:
      weight: 25
      signals:
        - response_time_to_comms: # avg days to reply
            same_day: 10
            1-2_days: 7
            3-5_days: 4
            5+_days_or_no_reply: 1
        - attends_check_ins: # QBR/call attendance
            always: 10
            usually: 7
            sometimes: 4
            never: 1
        - proactive_requests: # they ask for more
            monthly: 10
            quarterly: 6
            rarely: 3
            never: 1
    
    financial:
      weight: 20
      signals:
        - payment_history: # last 6 months
            always_on_time: 10
            1_late: 7
            2+_late: 3
            failed_payment_unresolved: 0
        - contract_value_trend:
            expanding: 10
            stable: 6
            contracting: 2
        - billing_page_visits: # in last 30 days
            none: 10
            1-2: 6  # curious
            3+: 2   # shopping to leave
    
    relationship:
      weight: 15
      signals:
        - champion_status: # your internal advocate
            strong_champion: 10
            moderate: 6
            weak_or_unknown: 3
            champion_left_company: 0
        - stakeholder_breadth: # contacts you have
            3+_contacts: 10
            2_contacts: 6
            single_threaded: 2
        - sentiment_last_interaction:
            positive: 10
            neutral: 6
            negative: 2
    
    outcome:
      weight: 10
      signals:
        - achieving_stated_goals: # their original objectives
            exceeding: 10
            on_track: 7
            behind: 3
            unclear_goals: 2
        - roi_demonstrated:
            clear_positive_roi: 10
            probable_roi: 6
            unclear: 3
            negative: 0

  risk_tiers:
    healthy: 75-100    # green — nurture & expand
    monitor: 50-74     # yellow — proactive outreach
    at_risk: 25-49     # orange — intervention required
    critical: 0-24     # red — save or graceful exit
```

### 自动健康警报

| 评分变化 | 应对措施 |
|---|---|
| 评分下降15分以上 | 立即联系客户——情况发生了变化 |
| 进入“风险”等级 | 触发挽救计划（第五阶段） |
| 进入“危急”等级 | 在24小时内上报给创始人/CEO |
| 从较低等级提升到“健康”等级 | 发送祝贺信息并讨论进一步合作 |
| 关键联系人离职 | 紧急：在48小时内寻找新的关键联系人 |

---

## 第二阶段：入职流程（0-90天）——留存的基础

**超过20%的自愿流失案例源于糟糕的入职体验**（Recurly研究）。最初的90天决定了后续900天的客户留存情况。

### 每日入职框架

```yaml
onboarding_playbook:
  day_0:
    - welcome_message: |
        Personal, not templated. Reference their specific goals from the sales process.
        Include: what happens next, timeline, who they'll work with, how to reach you.
    - access_setup: Grant all necessary access, tools, integrations
    - kickoff_call: 30 min — align on goals, success metrics, communication cadence
    - document: Record their stated goals and success criteria in CRM
  
  day_1-3:
    - quick_win: Deliver ONE visible result ASAP
    - examples:
        - SaaS: first workflow automated
        - Agency: first deliverable draft
        - Consulting: first insight or recommendation
    - why: Quick wins create commitment bias — they've now seen value
  
  day_7:
    - check_in_1: |
        "How's everything going? Any questions or blockers?"
        Goal: surface confusion early. Don't wait for them to complain.
    - share_progress: Show what's been done, even if small
  
  day_14:
    - first_result: Share measurable outcome with numbers
    - format: "[Metric] went from [X] to [Y] — here's what that means for you"
    - ask: "Is this aligned with what you expected?"
  
  day_30:
    - milestone_review:
        - Show ROI calculation
        - Confirm success metrics are being hit
        - Discuss next 60 days
        - Introduce expansion possibilities (plant seeds, don't sell)
    - document: Update CRM with 30-day health assessment
  
  day_60:
    - deeper_review:
        - Feature adoption check — are they using everything available?
        - Identify unused capabilities and train on them
        - Stakeholder expansion — meet other team members who should be involved
  
  day_90:
    - graduation:
        - Full QBR format (see Phase 4)
        - Transition from "onboarding" to "ongoing" cadence
        - Set annual goals
        - If health score is green: discuss year 1 roadmap
        - If yellow/orange: intervention before it becomes a habit
```

### 入职评分标准（0-100分）

评估您的入职流程：

| 评估维度 | 权重 | 10分 | 5分 | 1分 |
|---|---|---|---|---|
| 达到首次价值的时间 | 25分 | < 3天 | 1-2周 | > 2周 |
| 客户所需投入的努力 | 20分 | 几乎不需要（您全包了） | 中等 | 需要大量投入 |
| 个性化程度 | 15分 | 完全根据客户需求定制 | 半定制 | 通用 |
| 沟通清晰度 | 15分 | 主动沟通，有明确的时间表 | 被动回应 | 令人困惑 |
| 快速看到成果 | 15分 | 第一周内能看到可衡量的成果 | 进展模糊 | 没有成果 |
| 文档资料 | 10分 | 提供完整的知识库/指南 | 仅有基本文档 | 没有文档 |

**目标：80分以上。** 低于60分意味着您的入职流程存在严重问题。

---

## 第三阶段：持续的价值提供（每月验证）

客户流失的原因不是因为服务停止了，而是因为他们**忘记了服务的存在**。

### 月度价值报告模板

```markdown
# [Month] Performance Report — [Client Name]

## Key Metrics
| Metric | This Month | Last Month | Change |
|--------|-----------|------------|--------|
| [Primary KPI] | [value] | [value] | [+/-]% |
| [Secondary KPI] | [value] | [value] | [+/-]% |
| [Tertiary KPI] | [value] | [value] | [+/-]% |

## What We Did
- [Specific action 1 with result]
- [Specific action 2 with result]
- [Optimization or improvement made]

## ROI Summary
- Your investment: $[monthly cost]
- Value delivered: $[quantified value]
- ROI: [X]x return

## What's Next
- [Planned improvement 1]
- [Planned improvement 2]

## Quick Question
[One specific question to keep dialogue open]
```

### 价值报告规则

1. **每月必发**——自动化数据收集
2. **仅提供真实数据**——避免含糊的“一切顺利”的说法
3. **展示趋势**——按月显示数据变化
4. **每份报告都以一个问题结尾**——保持沟通的双向性
5. **突出一个积极的改进点**——即使客户没有主动询问，也要展示您的努力
6. **报告控制在一页以内**——高管们时间宝贵，不会阅读冗长的报告

---

## 第四阶段：季度业务回顾（QBR）

季度业务回顾是提高客户留存效率的最佳方式。良好的QBR不仅能防止流失，还能发现增长机会，并加深与客户的关系。

### QBR议程模板（45-60分钟）

```yaml
qbr_agenda:
  1_celebrate_wins: # 10 min
    - "Here's what we've accomplished together this quarter"
    - Show 3-5 headline metrics with trends
    - Tie results to their original goals
    - Ask: "Does this match your perception?"
  
  2_deep_dive: # 15 min
    - One area of focus (their choice or your recommendation)
    - Bring analysis they haven't seen
    - Benchmark against industry if possible
    - "Here's what we've learned and what it means"
  
  3_feedback_loop: # 10 min
    - "What's working well?" (reinforce, don't skip this)
    - "What could we do better?" (write it down visibly)
    - "Has anything changed in your business we should know about?"
    - Listen for churn signals (see list below)
  
  4_roadmap: # 10 min
    - What's planned for next quarter
    - Any new capabilities or features relevant to them
    - Tie roadmap items to their stated needs
  
  5_expansion: # 5 min
    - "Based on your growth, here's where we could help more"
    - Present ONE expansion idea (not three — focused)
    - Frame as: "Other clients in your situation have found X valuable"
    - No pressure — plant the seed
  
  6_next_steps: # 5 min
    - Summarize action items (yours and theirs)
    - Confirm next QBR date
    - Send written summary within 24 hours
```

### QBR评分（对账户进行1-5分评估）

| 评估维度 | 5分（优秀） | 3分（一般） | 1分（危险） |
|---|---|---|---|
| 目标达成情况 | 超额完成所有目标 | 部分达成 | 大部分未达成 |
| 客户参与度 | 主动、热情 | 被动回应 | 无互动 |
| 关系深度 | 与高管保持多渠道联系 | 仅通过一次联系 | 联系中断 |
| 增长迹象 | 客户询问更多服务 | 愿意讨论扩展方案 | 减少服务范围 |
| 支付情况 | 按时支付，持续增长 | 稳定 | 支付延迟，对费用有疑问 |

**评分20-25分：**有增长潜力——推动追加销售
**评分15-19分：**状况良好——保持现有联系
**评分10-14分：**有流失风险——增加联系频率**
**评分5-9分：**情况危急——立即启动挽救计划**

---

## 第五阶段：流失预防与挽救计划

### 14种流失信号（按严重程度排序）

| 编号 | 信号 | 严重程度 | 应对时间 |
|---|---|---|---|
| 1 | 数据导出请求 | 🔴 危急 | 当天处理 |
| 2 | 询问取消条款 | 🔴 危急 | 当天处理 |
| 关键联系人离职 | 🔴 危急 | 48小时内处理 |
| 支付失败（第二次尝试） | 🔴 危急 | 当天处理 |
| 使用量下降50%以上 | 🟠 高风险 | 3天内处理 |
| 停止回复消息 | 🟠 高风险 | 1周内处理 |
| 错过2次以上预约的回访 | 🟠 高风险 | 1周内处理 |
| 谈话中提到竞争对手 | 🟡 中等风险 | 下一次联系时处理 |
| 内部宣布预算调整 | 🟡 中等风险 | 1周内处理 |
| 关键利益相关者变更 | 🟡 中等风险 | 2周内处理 |
| 请求减少服务范围/等级 | 🟡 中等风险 | 下一次联系时处理 |
| 支持工单激增后不再回复 | 🟡 中等风险 | 1周内处理 |
| 访问账单页面次数增加 | 🟡 中等风险 | 下一次联系时处理 |
| 沟通得分连续3周下降 | 🟡 中等风险 | 2周内处理 |

### 拯救计划（5个阶段）

```yaml
save_playbook:
  stage_1_detect:
    trigger: Health score enters "at-risk" OR churn signal detected
    action: |
      Internal alert to account owner + manager.
      Pull full account history: usage, payments, last interactions, open issues.
      Prepare value summary (total ROI delivered to date).
  
  stage_2_reach_out:
    timing: Within response time for the signal severity
    approach: |
      Personal, NOT templated. From a human, not "the team."
      "Hi [Name], I noticed [specific observation]. Wanted to check in — 
      is everything going well with [specific thing]?"
      DO NOT: mention churn, be defensive, or offer discounts preemptively.
    channel: Match their preferred channel (email, call, Slack, etc.)
  
  stage_3_listen:
    goal: Understand the real reason, not the surface excuse
    common_real_reasons:
      - "Not seeing value" → ROI not demonstrated clearly enough
      - "Too expensive" → Value perception gap (or genuine budget cut)
      - "Switched to competitor" → Feature/price gap you didn't know about
      - "Champion left" → Relationship wasn't broad enough
      - "Don't use it enough" → Adoption/training gap
      - "Priorities changed" → Their business shifted
    technique: |
      Ask "What would need to change for this to work for you?" 
      NOT "What's wrong?" (defensive) or "What can we do?" (desperate)
  
  stage_4_intervene:
    options_by_reason:
      not_seeing_value:
        - Emergency value review — show ROI with hard numbers
        - Offer dedicated optimization session
        - Set new, measurable goals with 30-day checkpoint
      too_expensive:
        - Tier adjustment (downgrade > cancel)
        - Pause option (1-2 months, hold their data/setup)
        - Annual discount if they commit
        - LAST RESORT: temporary price reduction with expiry
      low_usage:
        - Personalized training session
        - Assign an onboarding buddy
        - Simplify their setup (reduce complexity)
      champion_left:
        - Request intro to successor within 48 hours
        - Prepare "new stakeholder briefing" with full history + ROI
        - Offer fresh kickoff call with new contact
      competitor:
        - Understand specific features/price they're comparing
        - Build competitive comparison (honest, not FUD)
        - If you genuinely can't compete: let them go gracefully
  
  stage_5_outcome:
    saved:
      - Document what worked → update playbook
      - Set 30/60/90 day health checkpoints
      - Address root cause permanently (don't just bandage)
    churned:
      - Exit interview: "What could we have done differently?"
      - Leave door open: "We're here if things change"
      - Add to reactivation pipeline (see Phase 7)
      - Analyze: was this predictable? Update health score model
```

### 暂停 vs. 取消策略

**在接受取消之前，始终提供暂停选项。**

| 情况 | 提供的选项 | 条件 |
|---|---|---|
| 预算削减（临时） | 暂停1-3个月 | 保留数据，价格不变，随时可恢复 |
| 使用量低（季节性） | 降级为维护级服务 | 减少服务范围，降低价格 |
| 团队变动 | 暂停1个月 | 新团队准备就绪后提供免费重新入职服务 |
| “不是优先事项” | 暂停服务，并每月进行一次回访 | 发送邮件：“准备好恢复服务了吗？”

**暂停的有效性：**40-60%的暂停账户会重新激活。而取消服务的账户中，没有一个会主动回归。**

---

## 第六阶段：收入增长（无需新增客户）

**顶尖的B2B SaaS公司30-50%的新收入来自现有客户。**通过现有客户实现增长比新增客户更便宜、更快捷、更可靠。

### 5个增长触发因素

| 触发因素 | 信号 | 应对方法 |
|---|---|---|
| 使用量达到上限 | “您发展迅速——这里是如何扩大服务范围的” |
| 客户提到新的需求 | “我们也提供相关服务——想快速演示一下吗？” |
| 团队扩张 | 新员工入职/部门增加 | “您的团队扩大了——需要增加服务吗？” |
| 达成重要里程碑 | “恭喜您达成[里程碑]！处于您这个阶段的客户通常能从[服务]中受益” |
| 合同续签临近 | “在续签前，让我们看看有什么变化以及您可能需要什么” |

### 价格策略与增长

```yaml
expansion_pricing:
  anchor_to_value:
    - "This feature generates $X/month for similar clients"
    - "At your current volume, the upgrade pays for itself in [N] weeks"
  
  bundle_discount:
    - Package 2-3 add-ons at 15-20% less than individual prices
    - "Most clients at your stage add [X] and [Y] together"
  
  annual_commit:
    - 15-20% discount for annual payment
    - Position as: "Lock in this rate before our next price increase"
    - Only offer when health score is green (don't reward at-risk with discounts)
  
  land_and_expand:
    - Start small, prove value, grow scope
    - "Let's pilot this with one team for 30 days, then expand"
    - Lower risk = higher conversion
  
  never_do:
    - Discount to save a churning client (trains them to threaten churn)
    - Bundle everything together (leaves no expansion room)
    - Surprise price increases without added value
```

### 净收入留存（NRR）计算

```
NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR × 100

Example:
  Starting MRR: $50,000
  Expansion (upsells): +$8,000
  Contraction (downgrades): -$2,000
  Churn: -$3,000
  
  NRR = ($50,000 + $8,000 - $2,000 - $3,000) / $50,000 × 100 = 106%

Target NRR by segment:
  SMB: 90-100% (some churn is normal)
  Mid-Market: 100-110%
  Enterprise: 110-130%
  Best in class: 130%+ (Snowflake, Twilio at scale)
```

---

## 第七阶段：重新激活（挽回流失客户）

### 重新激活的时间顺序

```yaml
reactivation_sequence:
  day_7:
    subject: "We saved your setup"
    tone: Soft, no pressure
    message: |
      Hey [Name], your [data/setup/config] is still here. 
      If anything changes, you can pick up right where you left off.
    cta: "Reactivate in one click"
  
  day_30:
    subject: "Here's what you're missing"
    tone: Value-focused
    message: |
      Since you left, we've added [new feature/improvement].
      Clients like you are seeing [specific result].
    cta: "See what's new"
    incentive: None yet
  
  day_60:
    subject: "[Name], quick question"
    tone: Personal, curious
    message: |
      I've been wondering — did you find a solution for [their original problem]?
      If not, I'd love to show you how [specific improvement] addresses 
      exactly what wasn't working before.
    cta: "15-min call"
    incentive: Optional — free month or reduced rate for 3 months
  
  day_90:
    subject: "Last one from me"
    tone: Respectful closure
    message: |
      I won't keep emailing — I know your inbox is busy.
      If you ever want to revisit [problem we solve], we'll be here.
      Your data is saved for another 90 days.
    cta: "Reactivate anytime"
    incentive: Best offer (30% off for 3 months, or free month)
  
  day_180:
    subject: "Your data is expiring"
    tone: Factual, urgency
    message: |
      Your [data/setup] will be deleted in 30 days per our retention policy.
      Want to keep it? Reactivate or export before [date].
    cta: "Save my data" / "Export"
```

### 重新激活效果评估指标

| 指标 | 优秀 | 良好 | 最佳 |
|---|---|---|---|
| 总体挽回率 | 5-10% | 10-15% | 15-25% |
| 7-30天内的重新激活率 | 3-5% | 5-8% | 8-12% |
| 激励措施转化效果 | 达到基线的2倍 | 3倍 | 4倍 |
| 重新激活客户的留存率（6个月） | 50% | 65% | 80% |

---

## 第八阶段：非自愿流失的预防（支付问题）

**30-40%的流失是非自愿的**——原因可能是支付失败、卡片过期或账单错误。这些都是可以避免的收入损失。

### 支付问题处理流程

```yaml
payment_recovery:
  attempt_1_failed:
    action: Retry payment in 24 hours (automatic)
    notification: None (many are temporary holds)
  
  attempt_2_failed:
    action: Retry in 48 hours
    notification: |
      Friendly email: "Heads up — your payment didn't go through. 
      This usually happens when a card expires or has a temporary hold.
      Update your payment method here: [link]"
    tone: Helpful, not threatening
  
  attempt_3_failed:
    action: Retry in 72 hours
    notification: |
      More urgent: "Your account is at risk of interruption. 
      We don't want you to lose access to [specific value they use].
      Takes 30 seconds to update: [link]"
    add: In-app banner if applicable
  
  day_10:
    action: Final retry
    notification: |
      "Last attempt before we pause your account. 
      Your [data/setup/progress] is safe — just update payment to continue."
    escalation: Personal email from account manager for high-value accounts
  
  day_14:
    action: Pause account (don't delete)
    notification: |
      "Your account is paused. Everything is saved.
      Reactivate anytime: [link]"
    retention: Hold data for 90 days minimum
```

### 卡片更新优化

- **到期前提醒：**在卡片到期前30天发送邮件：“您的[XXXX]卡片下个月到期。现在更新以避免中断。”
- **多种支付方式：**允许使用备用卡片
- **智能重试机制：**在发薪日（1日和15日）自动重试支付
- **账户更新服务：**使用Stripe/支付处理器自动更新过期卡片

---

## 第九阶段：差异化留存策略

不同的客户需要不同的策略。

### 根据收入等级

```yaml
retention_by_tier:
  enterprise: # >$5,000/mo
    cadence: Weekly touchpoint, monthly deep dive, quarterly QBR
    team: Dedicated CSM + executive sponsor
    expansion: Custom solutions, multi-year deals
    save_budget: Up to 25% discount for 6 months
    
  mid_market: # $500-5,000/mo
    cadence: Bi-weekly check-in, quarterly QBR
    team: Shared CSM (1:20 ratio)
    expansion: Tier upgrades, add-on features
    save_budget: Up to 15% discount for 3 months
    
  smb: # <$500/mo
    cadence: Monthly automated report, quarterly email check-in
    team: Tech touch (automated) + pooled support
    expansion: Annual commit discount, referral program
    save_budget: Pause option only (no discounts at this tier)
    
  free_trial:
    cadence: Day 1, 3, 7, 10, 13 (end of trial)
    team: Automated sequences + sales for high-intent
    conversion: Demo offer at day 7, discount at day 12
```

### 根据客户生命周期阶段

| 阶段 | 重点 | 关键指标 | 应对措施 |
|---|---|---|---|
| 0-30天 | 激活服务 | 达到首次使用时间 | 加快入职流程 |
| 30-90天 | 培养使用习惯 | 每周检查活跃度 | 发现新功能 |
| 90-180天 | 深化客户关系 | 扩展服务范围 | 提供培训、进行季度业务回顾 |
| 180-365天 | 提升客户忠诚度 | 开展推荐计划、撰写案例研究 |

---

## 第十阶段：指标仪表盘

### 每周留存情况仪表盘

```yaml
weekly_dashboard:
  headline_metrics:
    - gross_churn_rate: "% of MRR lost to cancellations"
    - net_churn_rate: "Gross churn minus expansion revenue"
    - nrr: "Net Revenue Retention — THE number that matters"
    - logo_churn: "% of customers lost (not weighted by revenue)"
  
  health_distribution:
    - healthy_accounts: "[count] ([%]) — $[MRR]"
    - monitor_accounts: "[count] ([%]) — $[MRR]"
    - at_risk_accounts: "[count] ([%]) — $[MRR]"
    - critical_accounts: "[count] ([%]) — $[MRR]"
  
  pipeline:
    - expansion_pipeline: "$[amount] in active upsell conversations"
    - renewals_next_30_days: "[count] accounts, $[MRR] at stake"
    - saves_this_week: "[count] interventions, [count] saved, $[MRR] recovered"
  
  cohort_snapshot:
    - latest_cohort_d30: "[%] — trending [up/down] vs prior cohort"
    - best_cohort: "[month] at [%] — analyze why"
    - worst_cohort: "[month] at [%] — analyze why"
```

### 每月高管总结模板

```markdown
# Retention Report — [Month Year]

## Headline
- NRR: [X]% ([up/down] from [last month]%)
- Gross churn: [X]% ($[amount])
- Expansion: $[amount] ([count] accounts upgraded)
- Net change: [+/-]$[amount] MRR from existing clients

## Wins
- [Specific save story with numbers]
- [Expansion win with numbers]

## Risks
- [X] accounts in critical health ([total MRR at risk])
- Top risk: [Account name] — [reason] — [plan]

## Actions for Next Month
1. [Specific action with owner and deadline]
2. [Specific action with owner and deadline]
```

---

## 各行业客户留存率基准

| 行业 | 月流失率 | 优秀 | 最佳 |
|---|---|---|---|
| B2B SaaS（中小企业） | < 5% | < 3% | < 2% |
| B2B SaaS（企业级） | < 2% | < 1% | < 0.5% |
| B2C订阅服务 | < 7% | < 5% | < 3% |
| 代理/咨询公司 | < 8% | < 5% | < 3% |
| 电子商务（订阅服务） | < 10% | < 7% | < 5% |
| 健身/健康行业 | < 12% | < 8% | < 5% |

---

## 10个常见的导致收入流失的错误

1. **没有客户健康评分**——在流失发生后才发现问题
2. **单渠道沟通**——一旦失去一个联系人，就失去了这个客户
3. **通用化的入职流程**——对每月收费100美元和10,000美元的客户使用相同的流程
4. **不提供月度价值报告**——客户会忘记您的存在
5. **被动式的季度业务回顾**——只在续签时才联系客户（太晚）
6. **为了节省成本而打折**——这会让学生习惯通过威胁来争取折扣
7. **忽视非自愿流失**——30-40%的流失是可以预防的（如支付问题）
8. **没有重新激活机制**——流失的客户会永远失去
9. **对所有流失情况一视同仁**——自愿流失和非自愿流失、高价值客户与低价值客户需要不同的应对策略
10. **只关注流失数量，不关注收入**——失去10个小客户与失去一个大客户的影响截然不同

---

## 自然语言命令

| 命令 | 功能 |
|---|---|
| “[客户名称]的评分” | 计算特定客户的健康评分 |
| “[客户]的入职检查清单” | 生成个性化的90天入职计划 |
| “[客户]的QBR准备” | 根据其指标和讨论点制定QBR议程 |
| “流失风险报告” | 按健康等级列出所有客户并推荐应对措施 |
| “[客户]的月度报告” | 生成包含指标的报告 |
| “[客户]的挽救计划” | 诊断流失原因并推荐干预措施 |
| “增长机会” | 列出有追加销售潜力的健康客户 |
| “重新激活名单” | 显示适合重新激活的客户 |
| “本月净收入留存” | 计算净收入留存率 |
| “支付失败” | 列出有支付问题的客户及其恢复状态 |