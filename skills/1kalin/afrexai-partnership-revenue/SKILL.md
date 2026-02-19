# 合作伙伴与渠道收入引擎

将简单的合作伙伴关系转变为一个系统的收入来源。这是一套完整的指南，涵盖了寻找、评估、构建、启动和扩展合作伙伴驱动的增长策略——无论您是建立集成合作伙伴关系、经销商渠道、联盟计划还是战略联盟。

---

## 第一阶段 — 合作伙伴策略与潜在合作伙伴（ICP）评估

在联系任何人之前，先明确理想合作伙伴的特征。

### 合作伙伴类型决策矩阵

| 合作类型 | 适用场景 | 收入模式 | 复杂度 | 收入实现时间 |
|------|-----------|---------------|------------|-----------------|
| **集成/技术** | 产品相互补充 | 收入分成 10-30% | 高 | 3-6个月 |
| **经销商/VAR** | 合作伙伴获得客户的信任 | 批发折扣 20-40% | 中等 | 1-3个月 |
| **推荐** | 低门槛的进入方式 | 每个潜在客户的费用或首笔交易的百分比 | 低 | 2-4周 |
| **联盟** | 大规模受众，数字产品 | 15-40% 的佣金 | 低 | 1-2周 |
| **联合销售** | 企业级交易，双方品牌都有帮助 | 收入分成根据贡献分配 | 高 | 3-6个月 |
| **白标/OEM** | 合作伙伴希望使用您的技术并加上自己的品牌 | 许可费 + 每个用户/使用量费用 | 非常高 | 6-12个月 |
| **联合营销** | 共享受众，内容协同 | 无直接收入（生成销售线索） | 低 | 2-4周 |
| **战略/合资** | 市场进入，新市场拓展 | 股权或利润分成 | 非常高 | 6-18个月 |

**选择规则：** 从推荐或联盟开始（快速见效，验证概念），然后逐步过渡到集成或经销商合作（产生实际收入），最后是战略合作伙伴关系。

### 理想合作伙伴画像（IPP）

```yaml
ideal_partner_profile:
  company:
    size: "50-500 employees"  # or revenue range
    stage: "Series B+ or profitable"
    geography: "US, UK, EU"
    industries: ["SaaS", "Professional Services"]
  
  audience_overlap:
    serves_our_icp: true  # Their customers = our target buyers
    complementary_not_competitive: true
    audience_size_minimum: 5000  # customers or active users
  
  capability:
    has_sales_team: true  # for reseller; optional for referral
    technical_integration_capacity: "medium"  # for tech partnerships
    marketing_team_exists: true  # for co-marketing
    partner_program_experience: "any"  # bonus if they've partnered before
  
  alignment:
    brand_quality: "matches or exceeds ours"
    values_compatible: true
    growth_trajectory: "stable or growing"
    executive_sponsorship_likely: true
  
  anti_signals:  # Disqualify if any are true
    - "Direct competitor or building competing feature"
    - "Declining revenue / layoffs > 20%"
    - "Known for partner-unfriendly behavior"
    - "Regulatory risk that could impact us"
    - "Single decision-maker who's leaving"
```

### 合作伙伴评分（0-100）

| 维度 | 权重 | 评分标准 |
|-----------|--------|---------------------|
| **受众匹配度** | 25% | 1=无重叠，3=部分重叠，5=完全匹配 |
| **收入潜力** | 25% | 1=<5K/年，3=25-50K/年，5=100K+/年 |
| **品牌契合度** | 15% | 1=风险品牌，3=中立，5=知名/可信 |
| **执行能力** | 20% | 1=无团队/资源，3=有一定能力，5=有专门的合作伙伴团队 |
| **战略价值** | 15% | 1=仅交易合作，3=市场洞察力，5=开辟新市场 |

**评分 = (受众×5 + 收入×5 + 品牌×3 + 执行×4 + 战略×3) = 最高100**

- **80-100：** 第一级别 — 优先支持，配备专职合作伙伴经理 |
- **60-79：** 第二级别 — 标准支持，季度评估 |
- **40-59：** 第三级别 — 自助资源，年度检查 |
- **<40：** 不符合标准 — 礼貌拒绝或延期考虑 |

---

## 第二阶段 — 合作伙伴发现与研究

### 8种发现合作伙伴的渠道（按质量排序）

1. **现有客户推荐** — “您使用哪些工具与我们的一样？” — 最可靠的信息来源 |
2. **集成市场分析** — 浏览 Zapier、HubSpot、Salesforce AppExchange 等平台，寻找相关工具 |
3. **竞争对手的合作伙伴页面** — 了解竞争对手的合作伙伴情况 |
4. **行业会议赞助商名单** — 投资于品牌曝光度的公司通常准备好合作 |
5. **LinkedIn Sales Navigator** — 按公司搜索，筛选标题中包含“合作伙伴关系”或“业务发展”的联系人 |
6. **G2/Capterra 类别关联** — 同一类别的客户也可能会购买这些供应商的产品 |
7. **风险投资组合重叠** | 共同的投资方通常鼓励合作伙伴关系 |
8. **主动联系** — 跟踪主动联系我们的人；表明有市场需求 |

### 研究简报模板

```yaml
partner_research:
  company: "Acme Corp"
  website: "https://acme.com"
  what_they_do: "Project management for construction firms"
  
  audience:
    customer_count: "~2,000 companies"
    target_segment: "Mid-market construction ($10M-$200M revenue)"
    geographic_focus: "US, expanding to UK"
    overlap_with_our_icp: "HIGH — 60% of their customers match our target"
  
  product:
    core_product: "Cloud PM platform"
    pricing: "$99-499/mo per company"
    integrations: ["QuickBooks", "Procore", "Slack"]
    api_available: true
    gaps_we_fill: "No AI automation, no document analysis"
  
  business:
    funding: "Series B, $40M raised"
    revenue_estimate: "$15M ARR"
    growth: "Growing ~40% YoY"
    team_size: 180
    partner_program_exists: false  # Opportunity to be first!
  
  key_people:
    partnership_lead: "Jane Smith, VP Business Development"
    product_lead: "Mike Johnson, CPO"
    ceo: "Sarah Williams"
    linkedin_urls:
      - "https://linkedin.com/in/janesmith"
      - "https://linkedin.com/in/mikejohnson"
  
  competitive_intel:
    partners_with: ["QuickBooks", "DocuSign"]
    missing_partners: "No AI/automation partner"
    competitor_partnerships: "Rival Corp partners with BuildBot AI"
  
  partnership_angle: "Integration: our AI reads their project docs, automates compliance checks"
  estimated_annual_value: "$75K (rev share on 200 conversions)"
  risk_factors: ["May build in-house", "CEO reportedly difficult"]
  
  outreach_strategy:
    warm_intro_available: "Yes — mutual investor, also customer X knows their VP"
    first_touch: "Warm intro via investor → meeting with VP BD"
    hook: "Their competitor already has AI partner; they're falling behind"
```

---

## 第三阶段 — 联系与初次会议

### 联系流程（3周内进行5次接触）

**第一次联系 — 第1天：热情介绍或发送冷邮件**

主题："{共同联系人} 建议我联系您 — {他们的公司} + {您的公司}" 

```
Hi {Name},

{Mutual connection} mentioned you're exploring ways to help {their customers} 
with {problem area}. We've been building {brief description} and {X} of our 
customers already use {their product} alongside ours.

Quick thought: a {partnership type} between us could help your customers 
{specific outcome — e.g., "cut compliance review time by 60%"} without you 
building anything new.

Worth a 20-minute call this week?

{Signature}
```

**第二次联系 — 第4天：提供额外价值**

```
Hi {Name},

Following up — I put together a quick analysis of how {their product} users 
could benefit from {your capability}. [Attach 1-pager or link]

The overlap between our customer bases is stronger than I expected — 
{specific data point}.

Happy to walk through it whenever works.
```

**第三次联系 — 第8天：展示社会认可度**

```
Quick update — {similar company} just launched a similar partnership with us 
and saw {metric — e.g., "23% increase in customer retention"} in the first 
quarter. 

Their {role} said: "{brief quote}."

Think this could work for {their company} too. Free Thursday?
```

**第四次联系 — 第14天：轻微提醒**

```
Hi {Name} — wanted to bump this up. We're formalizing our partner program 
this quarter and have {X} spots for launch partners who get priority 
integration support and co-marketing.

Should I include {their company}?
```

**第五次联系 — 第21天：结束联系**

```
Hi {Name} — I'll assume the timing isn't right. Totally understand.

If partnerships ever become a priority, we'd love to explore this. 
I'll check back in {timeframe — e.g., "Q3"}.

In the meantime, {useful resource — guide, report, or intro to someone helpful}.
```

### 初次会议议程（30分钟）

```
0-5 min:  Rapport + confirm agenda
5-10 min: THEM — their business, customers, growth priorities
10-15 min: US — brief overview, why we think there's a fit
15-20 min: THE OPPORTUNITY — specific partnership model, mutual benefits
20-25 min: LOGISTICS — next steps, who else should be involved
25-30 min: COMMITMENT — agree on timeline for follow-up/decision
```

**需要询问的问题：**
1. “本季度您最大的增长重点是什么？”
2. “您的客户目前是如何解决{我们解决的问题}的？”
3. “您之前有过合作伙伴关系吗？哪些方法有效/无效？”
4. “内部需要哪些部门批准合作？”
5. “什么会让您毫不犹豫地选择与我们合作？”

**初次会议中的警示信号：**
- 他们无法明确说明自己的客户群体 → 客户群体不明确 |
- 第一反应是“我们需要 legal 审批” → 说明流程繁琐 |
- 对您的产品不感兴趣 → 没有表现出真正的兴趣 |
- 立即询问“佣金是多少？” → 只关注交易利益 |

---

## 第四阶段 — 合作协议结构与商务条款

### 收入分成模式

| 模型 | 适用场景 | 典型范围 | 跟踪方法 |
|-------|----------|---------------|-----------------|
| **收入百分比** | 持续的 SaaS 推荐 | 12-24 个月内 MRR 的 15-30% | 使用 UTM 和推荐代码 |
| **每个潜在客户的固定费用** | 高量但质量较低的推荐 | 每个符合条件的潜在客户 50-500 美元 | 通过 CRM 追踪 |
| **每笔交易的固定费用** | 有明确转化事件的交易 | 每笔成交交易 500-5,000 美元 | 使用促销代码或 UTM |
| **分层佣金** | 激励交易量 | 1-10 符合条件的交易 15%，11-25 符合条件的交易 20%，26 符合条件的交易 25% | 通过仪表盘跟踪 |
| **收入分成（双方共同承担）** | 集成合作伙伴关系 | 双方各承担 10-20% | 基于 API 使用量 |
| **许可费** | 白标/OEM 合作 | 每个用户每月 X 美元 | 根据使用量计费 |
| **混合模式** | 复杂交易 | 基础费用 + 绩效奖金 | 综合跟踪 |

### 合作协议检查清单

```
MUST INCLUDE:
□ Partnership type and scope (what's included, what's excluded)
□ Revenue share / commission structure with payment terms
□ Attribution method and tracking technology
□ Minimum commitments (if any — e.g., X referrals/quarter to maintain tier)
□ Exclusivity terms (usually NON-exclusive; exclusive = premium tier only)
□ Term length and renewal (12 months auto-renew is standard)
□ Termination clause (30-60 days notice, what happens to in-flight deals)
□ IP and brand usage rights (logo, name, marketing materials)
□ Data sharing and privacy (what data is exchanged, GDPR/CCPA compliance)
□ SLAs for integration support or lead response time
□ Dispute resolution (mediation before litigation)
□ Non-compete / non-solicit (narrow and reasonable)
□ Confidentiality / NDA
□ Insurance requirements (if applicable)

NICE TO INCLUDE:
□ Joint marketing commitments (X co-branded pieces per quarter)
□ MDF (Market Development Funds) availability
□ Partner advisory board participation
□ Early access to product roadmap
□ Escalation contacts for both sides
```

---

## 第五阶段 — 合作伙伴支持与启动

### 合作伙伴入职检查清单（前14天）

```
DAY 1-3: SETUP
□ Signed agreement received and countersigned
□ Partner portal access provisioned
□ Referral/tracking link generated and tested
□ Partner contact added to CRM with "Partner" tag
□ Welcome email sent with all resources
□ Kick-off call scheduled

DAY 4-7: ENABLEMENT
□ Product deep-dive session (60 min — record it)
□ Sales enablement materials shared:
  - One-pager (partner version)
  - Battle card vs. competitors
  - Demo script / walkthrough
  - FAQ document (20+ common questions)
  - Pricing guide with partner-specific terms
□ Co-branded landing page live (if applicable)
□ Partner's team trained on positioning and qualification

DAY 8-14: ACTIVATION
□ First joint pipeline review
□ First co-marketing piece planned (webinar, blog, case study)
□ Partner makes first referral or introduction
□ Feedback collected on enablement materials
□ 14-day check-in call completed
□ Partner added to monthly partner newsletter
```

### 合作伙伴支持资料包

| 资料 | 用途 | 更新频率 |
|-------|---------|------------------|
| **合作伙伴概述手册** | 为合作伙伴的销售团队提供快速参考 | 每季度 |
| **竞争对比卡** | 与竞争对手的对比 | 每月 |
| **演示脚本** | 分步演示指南 | 每次产品发布时 |
| **常见问题解答** | 20个常见问题及解答 | 每月 |
| **案例研究** | 行业/用例展示 | 根据实际情况提供 |
| **邮件模板** | 预写好的介绍邮件 | 每季度 |
| **联合品牌资料包** | 用于潜在客户的联合演示 | 每个合作伙伴 |
| **集成指南** | 技术设置文档 | 每次产品发布时 |
| **投资回报率计算器** | 可共享的工具 | 每季度 |

### 启动计划

```
WEEK 1: Soft Launch
- Partner's internal team briefed
- Test referral flow end-to-end
- First 3-5 warm intros from partner's network

WEEK 2-3: Controlled Launch
- Co-branded announcement blog post
- Email to partner's customer base (segmented)
- Social media cross-promotion
- Webinar or live demo (target: 50+ registrants)

WEEK 4+: Full Launch
- Integration listed on both marketplaces
- Paid co-marketing (if budget allows)
- Case study from first joint customer
- Press release (if strategic partnership)
```

---

## 第六阶段 — 合作伙伴管理与增长

### 合作伙伴健康状况评分（0-100，每月评估）

| 指标 | 权重 | 评分标准 |
|--------|--------|---------|
| **推荐数量** | 25% | 1=0 个推荐，3=达到目标，5=超过目标2倍 |
| **潜在客户质量** | 20% | 1=转化率<10%，3=达到平均水平，5=超过平均水平2倍 |
| **参与度** | 20% | 1=不响应，3=参加季度会议，5=积极参与联合营销 |
| **产生的收入** | 25% | 1=每月收入<1K，3=达到预期，5=超过预期2倍 |
| **关系强度** | 10% | 1=仅一次接触，3=有多个利益相关者，5=有高层支持 |

**评分 = 各指标权重之和 × 4 = 最高100**

- **80-100：** 首选合作伙伴 — 提供额外支持，配备专职经理 |
- **60-79：** 表现良好 — 维持现有关系，寻找增长机会 |
- **40-59：** 需要关注 — 诊断问题，制定改进计划 |
- **<40：** 表现不佳 — 开诚布公地讨论，考虑结束合作 |

### 季度业务回顾（QBR）模板

```
## Partner QBR: {Partner Name} — {Quarter}

### Performance Summary
- Referrals sent: {X} (target: {Y})
- Deals closed: {X} (target: {Y})
- Revenue generated: ${X} (target: ${Y})
- Commission paid: ${X}
- Partner health score: {X}/100

### What Worked
- {Top performing initiative}
- {Successful co-marketing effort}

### What Didn't
- {Underperforming area}
- {Blocked initiative and why}

### Next Quarter Plan
- Revenue target: ${X} (+{Y}% growth)
- Key initiatives:
  1. {Initiative — owner — deadline}
  2. {Initiative — owner — deadline}
  3. {Initiative — owner — deadline}
- Co-marketing commitment: {X pieces}
- Enablement needs: {Training, new materials, etc.}

### Open Issues
- {Issue — owner — target resolution date}

### Executive Alignment
- {Any strategic changes to discuss}
```

### 合作伙伴生命周期阶段

```
PROSPECT → EVALUATING → ONBOARDING → RAMPING → PRODUCING → SCALING → STRATEGIC
   ↓          ↓            ↓            ↓           ↓          ↓          ↓
 Research   Pitch &     14-day       First 90    Steady     Expand     Deep
 & score    negotiate   checklist    days ramp   state      scope      collab
```

**各阶段的行动：**

| 阶段 | 关键行动 | 成功标准 | 典型时间 |
|-------|-----------|----------------|------------------|
| **潜在客户阶段** | 研究 + 评估 | 评分 >60 | 1-2周 |
| **评估阶段** | 演讲 + 谈判条款 | 签署协议 | 2-4周 |
| **入职阶段** | 提供支持 + 培训 | 完成14天的入职流程 | 2周 |
| **成长阶段** | 获得首批推荐 + 提供支持 | 完成首笔交易 | 30-90天 |
| **稳定阶段** | 保持推荐流量 | 每月达到目标 | 持续进行 |
| **扩展阶段** | 扩大合作范围 | 收入逐季度增长 | 6个月以上 |
| **战略阶段** | 合作合资，共同发展 | 建立高层合作关系 | 12个月以上 |

---

## 第七阶段 — 渠道计划设计

### 渠道计划层级

```yaml
partner_program:
  tiers:
    - name: "Referral Partner"
      requirements:
        annual_revenue: "$0+"
        certifications: 0
        quarterly_reviews: false
      benefits:
        commission: "15%"
        support: "Email only"
        marketing: "Listed in partner directory"
        training: "Self-serve portal"
        
    - name: "Silver Partner"
      requirements:
        annual_revenue: "$25K+"
        certifications: 1
        quarterly_reviews: true
      benefits:
        commission: "20%"
        support: "Dedicated Slack channel"
        marketing: "Co-branded landing page + 1 webinar/quarter"
        training: "Live training sessions"
        mdf: "$2,500/quarter"
        
    - name: "Gold Partner"
      requirements:
        annual_revenue: "$100K+"
        certifications: 2
        quarterly_reviews: true
      benefits:
        commission: "25%"
        support: "Dedicated partner manager"
        marketing: "Full co-marketing program"
        training: "Custom enablement"
        mdf: "$10,000/quarter"
        early_access: true
        advisory_board: true
        
    - name: "Platinum Partner"
      requirements:
        annual_revenue: "$250K+"
        certifications: 3
        quarterly_reviews: true
        executive_sponsor: true
      benefits:
        commission: "30%"
        support: "Named SE + partner manager"
        marketing: "Joint press releases + events"
        training: "On-site enablement"
        mdf: "$25,000/quarter"
        product_input: "Roadmap influence"
        exclusivity_option: true
```

### 合作伙伴认证计划

```
LEVEL 1 — Foundations (self-paced, 2 hours)
- Product overview and positioning
- Target customer profile
- Basic demo skills
- Quiz: 80% to pass

LEVEL 2 — Practitioner (instructor-led, half day)
- Advanced product deep-dive
- Objection handling workshop
- Live demo practice with feedback
- Role-play exercise: 3 scenarios

LEVEL 3 — Expert (hands-on, full day)
- Technical integration workshop
- Solution architecture for top use cases
- Co-selling methodology
- Build a custom demo
- Present to panel for certification
```

---

## 第八阶段 — 指标与报告

### 合作伙伴计划仪表盘

```yaml
weekly_metrics:
  pipeline:
    new_partner_leads: {X}
    partners_in_evaluation: {X}
    partners_onboarding: {X}
    active_partners: {X}
    churned_partners_this_month: {X}
  
  performance:
    total_referrals_this_week: {X}
    qualified_referrals: {X}
    deals_closed_via_partners: {X}
    partner_sourced_revenue: "${X}"
    commission_paid: "${X}"
    net_partner_revenue: "${X}"
  
  efficiency:
    partner_sourced_vs_direct_cac: "{X}% lower"
    partner_deal_close_rate: "{X}%"
    average_partner_deal_size: "${X}"
    time_to_first_referral: "{X} days"
    partner_activation_rate: "{X}%"  # % of signed partners who refer in 90 days
  
  health:
    avg_partner_health_score: "{X}/100"
    partners_at_risk: {X}
    nps_from_partners: {X}

monthly_review:
  - Top 5 partners by revenue
  - Bottom 5 active partners (intervention needed?)
  - New partners added vs churned
  - Partner-sourced % of total revenue (target: 20-30%)
  - Co-marketing ROI
  - Enablement material usage stats
```

### 关键指标

| 指标 | 较差 | 良好 | 优秀 |
|--------|------|------|-------|
| **合作伙伴激活率（90天内首次推荐）** | <30% | 50-70% | >70% |
| **合作伙伴带来的交易转化率** | <10% | 20-30% | >30% |
| **合作伙伴带来的客户获取成本（CAC）** | 相同或更低 | 20-40% |
| **合作伙伴带来的收入百分比** | <10% | 15-25% | >25% |
| **首次推荐的平均时间** | >90天 | 30-60天 | <30天 |
| **合作伙伴净推荐值（NPS）** | <30 | 40-60 | >60 |
| **佣金占合作伙伴收入的百分比** | >35% | 20-30% | <20% |
| **合作伙伴流失率（年度）** | >30% | 15-25% | <15% |

---

## 第九阶段 — 高级策略

### 联合销售策略（企业级交易）

### 联合销售规则：
- 由拥有更强现有关系的合作伙伴主导合作 |
- 在首次联合会议前明确收入分成 |
- 由一方负责管理交易，另一方提供支持 |
- 在交易期间每周召开联合会议 |
- 共享 CRM 或每周发送合作进度邮件 |

### 大规模的联盟计划

```yaml
affiliate_program:
  tracking: "First-click attribution, 90-day cookie"
  commission_structure:
    one_time: "30% of first payment"
    recurring: "20% for 12 months"
    
  tiers:
    starter: { monthly_sales: "0-5", commission: "20%" }
    pro: { monthly_sales: "6-20", commission: "25%" }
    elite: { monthly_sales: "21+", commission: "30%", bonus: "$500/mo" }
  
  assets_provided:
    - Banner ads (5 sizes)
    - Email swipe copy (5 variations)
    - Social media posts (10 templates)
    - Landing page (co-branded, personalized link)
    - Video testimonials for embedding
  
  rules:
    - No brand bidding on paid search
    - No coupon/deal sites without approval
    - Honest representation required
    - FTC disclosure mandatory
    
  payment: "Monthly, NET-30, minimum $100 payout"
  platform: "PartnerStack / FirstPromoter / custom"
```

### 合作伙伴生态系统加速器

### 加速生态系统发展的方法：
1. **合作伙伴市场** — 使客户能够自然发现合作伙伴 |
2. **集成模板** — 将集成时间从几个月缩短到几天 |
3. **合作伙伴 API** — 提供自助技术支持 |
4. **成功案例** — 每个成功案例能吸引2-3个新的合作伙伴 |
5. **合作伙伴活动** | 年度峰会，增强社区凝聚力 |

---

## 第十阶段 — 特殊情况与复杂问题处理

### 当合作伙伴表现不佳时

```
Step 1: Data review — is it volume, quality, or conversion?
Step 2: Honest conversation — "We committed to X referrals/quarter. 
        We're at Y. What's blocking you?"
Step 3: Enablement check — do they have what they need? Re-train if needed
Step 4: 30-day improvement plan with specific targets
Step 5: If no improvement → move to self-serve tier or mutual wind-down
```

### 当合作伙伴之间发生竞争时

- 按地区、行业或交易规模进行区分 |
- 采用“先注册交易”的规则（通过交易注册系统） |
- 规则透明，严格执行 |
- 如发生冲突：通过沟通解决，避免邮件争论 |

### 当合作伙伴要求独家合作时

- 仅针对特定地区或行业提供独家权，避免全球范围 |
- 设定最低收入要求（至少是非独家合作时的两倍） |
- 设定时间限制（12个月，每年重新评估） |
- 设定绩效条款：如果未达到目标，取消独家权 |

### 当您是较小的合作伙伴时

- 强调您能带来的独特价值（如专业领域知识、技术能力） |
- 提议试点合作（3个月，范围有限，有明确的成功指标） |
- 为合作伙伴提供便利（您负责集成和资料准备） |
- 找到公司内部的推动者（如获得销售指标减免、创新支持） |

### 国际合作伙伴关系

- 尊重当地商业习惯（不同文化的合作速度不同） |
- 合同中明确适用法律和货币 |
- 考虑在当地寻找合作伙伴以进入市场 |
- 考虑税务问题（跨境佣金的扣税） |
- 翻译关键的支持资料 |

### 如何终止合作关系

以下情况表明合作关系应终止：
- 合作伙伴主动将潜在客户推荐给竞争对手 |
- 对您的品牌造成负面影响 |
- 违反法律或合规规定 |
- 经过6个月以上努力仍无投资回报 |
- 关系变得对立 |

**优雅终止方式：** 提前30-60天通知，妥善处理现有合作项目，制定专业的过渡计划，为未来留有余地。

---

## 自然语言命令

```
"Research [company] as potential partner"
→ Builds full research brief from web data

"Score [company] as a partner"
→ Runs 5-dimension scoring, returns tier recommendation

"Draft outreach to [name] at [company] about [partnership type]"
→ Generates personalized 5-touch sequence

"Create partner agreement outline for [company] — [type] partnership"
→ Generates deal structure with commercial terms

"Build enablement kit for [partner name]"
→ Creates one-pager, FAQ, battle card, email templates

"Run QBR prep for [partner name]"
→ Pulls metrics, generates QBR document

"Partner health check — all active partners"
→ Scores all partners, flags at-risk, suggests actions

"Design partner program tiers"
→ Generates tier structure with requirements and benefits

"Calculate deal economics: [referrals/mo] referrals at [ACV] ACV, [rate]% commission"
→ Returns full economics including Partner LTV/CAC

"Compare partnership types for [goal]"
→ Decision matrix based on your specific situation

"Plan co-marketing campaign with [partner]"
→ Generates campaign plan with timeline and assets

"Draft partner newsletter for this month"
→ Compiles updates, wins, new resources for partner base
```

---

## ⚡ 升级建议

本指南提供了完整的合作伙伴管理方案。如需特定行业的合作策略、交易结构或针对不同行业的联系流程，请参考：

**[AfrexAI 专业包 — 47美元](https://afrexai-cto.github.io/context-packs/)**

- **SaaS 包** — 针对 SaaS 行业的合作伙伴策略和集成指南 |
- **专业服务包** — 推荐网络和分包商合作框架 |
- **制造行业包** — 分销商和供应链合作伙伴管理方法 |
- **建筑行业包** — 分包商和供应商的合作系统 |

## 🔗 AfrexAI 提供的更多免费工具

- `afrexai-lead-hunter` — 自动化潜在客户生成与信息优化 |
- `afrexai-sales-playbook` — 完整的 B2B 销售系统 |
- `afrexai-negotiation-mastery` — 交易谈判框架 |
- `afrexai-proposal-engine` — 胜利提案制定方法 |
- `afrexai-competitive-intel` — 竞争情报系统 |

**[查看所有 AfrexAI 工具 →](https://afrexai-cto.github.io/context-packs/)**