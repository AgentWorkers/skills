---
name: Customer Success Engine
description: 完整的客户成功、客户留存以及收入增长管理系统。该系统可用于防止客户流失（churn prevention）、客户健康状况评估（health scoring）、新客户入职流程优化（onboarding optimization）、季度业务回顾（QBR）准备、业务拓展策略制定（expansion playbooks）、客户挽回活动（win-back campaigns）以及客户服务团队（CS team）的日常运营。
metadata:
  category: business
  skills: ["customer-success", "retention", "churn", "expansion", "onboarding", "health-score", "nrr"]
---
# 客户成功引擎

这是一个全面的系统，旨在防止客户流失、推动业务扩展，并将客户转化为产品倡导者。该系统涵盖了从客户入职到续订及业务增长的整个生命周期。

---

## 第一阶段：客户健康状况评估

### 健康状况评分模型（0-100分）

根据关键指标构建综合评分，并根据您的商业模式进行权重调整。

**评分要素：**

| 维度 | 权重 | 指标 | 评分标准 |
|---------|--------|---------|---------|
| 产品使用情况 | 30% | 日活跃用户（DAU）/月活跃用户（MAU）比例、功能覆盖率、核心操作的频率 | 日活跃用户/月活跃用户比例 < 20% = 0-3分；20-40% = 4-6分；> 40% = 7-10分 |
| 参与度 | 20% | 登录趋势（上升/平稳/下降）、支持工单数量、社区活跃度 | 下降 = 0-3分；平稳 = 4-6分；上升 = 7-10分 |
| 客户关系 | 15% | 是否指定了产品倡导者、是否有高层管理人员支持、多渠道沟通机制 | 无倡导者 = 0-3分；仅有倡导者 = 4-6分；多渠道沟通 = 7-10分 |
| 成果 | 20% | 是否跟踪了既定目标、是否有投资回报（ROI）记录、是否达到了成功里程碑 | 未达成任何目标 = 0-3分；部分达成 = 4-6分；全部达成 = 7-10分 |
| 财务状况 | 15% | 支付历史、合同价值趋势、业务扩展迹象 | 迟延支付 = 0-3分；按时支付 = 4-6分；业务扩展 = 7-10分 |

**健康状况等级：**

| 评分 | 等级 | 颜色 | 应采取的行动 |
|-------|------|-------|--------|
| 80-100 | 迅速发展 | 🟢 绿色 | 推动业务扩展、邀请客户成为倡导者 |
| 60-79 | 健康 | 🟡 黄色 | 监控客户状况、提供支持、准备升级服务 |
| 40-59 | 处于风险中 | 🟠 橙色 | 在48小时内制定干预计划 |
| 0-39 | 危急 | 🔴 红色 | 立即向高层汇报，制定紧急挽救计划 |

### 健康状况评分的YAML模板

```yaml
customer_health:
  account: "[Company Name]"
  arr: 0
  tier: "enterprise|mid-market|smb"
  csm: "[CSM Name]"
  renewal_date: "YYYY-MM-DD"
  scores:
    product_usage:
      score: 0  # 0-10
      dau_mau_ratio: 0.0
      core_actions_weekly: 0
      features_adopted: 0  # out of total available
      trend: "up|flat|down"
    engagement:
      score: 0
      login_trend: "up|flat|down"
      support_tickets_30d: 0
      last_proactive_contact: "YYYY-MM-DD"
      community_active: false
    relationship:
      score: 0
      champion: "[Name, Title]"
      exec_sponsor: "[Name, Title]"
      contacts_count: 0
      last_exec_touch: "YYYY-MM-DD"
    outcomes:
      score: 0
      goals_defined: 0
      goals_achieved: 0
      roi_documented: false
      last_success_milestone: ""
    financial:
      score: 0
      payment_status: "current|late|delinquent"
      expansion_signals: []
      contraction_risk: false
  composite_score: 0  # Weighted calculation
  tier: "thriving|healthy|at-risk|critical"
  last_updated: "YYYY-MM-DD"
```

---

## 第二阶段：入职引导（前90天）

前90天决定了客户是否会持续使用产品或在未来选择流失。

### 首次产生价值的时间（TTFV）框架

**目标：**尽快让每位客户体验到产品的“顿悟时刻”。

**步骤1 — 按客户群体定义“顿悟时刻”：**

| 客户群体 | “顿悟时刻” | 目标TTFV（时间） |
|---------|-----------|-------------|
| 企业级客户 | 首个工作流程自动化且团队采纳 | 30天 |
| 中端市场客户 | 核心用例上线且有3名用户使用 | 14天 |
| 中小企业（SMB） | 完成首次产生价值的操作 | 24小时 |
| 自助服务客户 | 完成核心操作 | 10分钟 |

**步骤2 — 入职引导里程碑：**

```
Week 1: Technical Setup
  □ Account provisioned and configured
  □ Integration(s) connected
  □ Admin trained on core settings
  □ Success plan created (goals, timeline, stakeholders)
  □ Kickoff call completed — attendees: champion + exec sponsor

Week 2-3: Core Adoption
  □ Primary use case configured
  □ First 5 users activated
  □ Core workflow running
  □ Quick win documented and shared with sponsor

Week 4-6: Expansion Adoption
  □ Second use case identified and configured
  □ 80% of licensed users active
  □ Self-service resources shared (docs, videos, community)
  □ 30-day check-in: review progress vs success plan

Week 7-12: Optimization
  □ Advanced features introduced
  □ Workflow optimization session
  □ ROI calculation (first draft)
  □ 90-day review: success plan scorecard, next quarter goals
```

### 入职引导期间的风险信号

如果在入职引导期间出现以下任何情况，请立即标记：

| 信号 | 严重程度 | 应对措施 |
|--------|----------|----------|
| 产品倡导者离职 | 🔴 紧急 | 在48小时内寻找新的倡导者，重新建立与高层的沟通 |
| 第3天后仍未登录 | 🟠 高风险 | 通过电话（而非邮件）进行个人联系 |
| 集成失败 | 🟠 高风险 | 升级至工程团队，提供临时解决方案 |
| 启动会议延迟超过1周 | 🟡 中等风险 | 内部升级，提供灵活的会议安排 |
| 第30天内用户激活率低于50% | 🟡 中等风险 | 开展用户激活活动（培训、提供激励） |
| 未确定高层支持者 | 🟡 中等风险 | 请求倡导者推荐他们的经理 |

### 成功计划模板

```yaml
success_plan:
  account: "[Company Name]"
  created: "YYYY-MM-DD"
  owner: "[CSM Name]"
  stakeholders:
    champion: { name: "", title: "", email: "" }
    exec_sponsor: { name: "", title: "", email: "" }
    technical_lead: { name: "", title: "", email: "" }
  business_objectives:
    - objective: "[What they want to achieve]"
      metric: "[How we'll measure it]"
      baseline: "[Current state]"
      target: "[Goal state]"
      timeline: "[By when]"
  use_cases:
    - name: "[Use case]"
      status: "not-started|in-progress|live|optimizing"
      go_live_date: "YYYY-MM-DD"
  milestones:
    - name: "Technical Setup Complete"
      target_date: "YYYY-MM-DD"
      status: "pending|complete|at-risk"
    - name: "First Value Delivered"
      target_date: ""
      status: ""
    - name: "Full Adoption"
      target_date: ""
      status: ""
  risks:
    - risk: ""
      mitigation: ""
      owner: ""
  next_review: "YYYY-MM-DD"
```

---

## 第三阶段：持续互动与客户生命周期管理

### 不同等级的客户互动频率

| 等级 | 同步会议 | 异步检查 | 定期业务回顾（QBR） | 高层沟通 |
|------|--------------|-----------------|------|-----------------|
| 企业级客户（年收入超过10万美元） | 每两周一次 | 每周一次 | 每季度一次 | 每季度一次 |
| 中端市场客户（年收入2.5万至10万美元） | 每月一次 | 每两周一次 | 每半年一次 | 每半年一次 |
| 中小企业（年收入5000美元至2.5万美元） | 每季度一次 | 每月一次 | 每年一次 | 无 |
| 自助服务客户（年收入低于5000美元） | 无（被动响应） | 自动化处理 | 无 | 无 |

### 不同健康等级的客户互动策略

**🟢 迅速发展（健康状况80-100分）：**
- 分享产品路线图预览（让他们感觉自己是产品内部团队的一员）
- 请求案例研究/推荐信/推荐人
- 介绍业务扩展机会
- 邀请客户加入测试计划和顾问委员会
- 请求在G2/Capterra平台上进行评价

**🟡 健康（健康状况60-79分）：**
- 主动分享最佳实践
- 对未使用的功能开展采用活动
- 安排优化工作坊
- 更新和审查成功计划的目标
- 加强多渠道沟通（与更多利益相关者联系）

**🟠 处于风险中（健康状况40-59分）：**
- 需要在48小时内制定干预计划
- 分析根本原因：是产品问题、人员问题还是流程问题？
- 高层之间进行沟通
- 提供专门的客服支持或现场访问
- 制定30天的恢复计划，并设置每周检查点

### 不同健康等级的定期业务回顾（QBR）邮件序列

**当功能采用率低于50%时触发的激活提醒序列：**

```
Day 0: "You're missing out on [Feature] — here's what teams like yours do with it"
Day 3: "[Customer Name] saved 10 hours/week using [Feature] — quick setup guide"
Day 7: "Want a 15-min walkthrough of [Feature]? Here's my calendar link"
Day 14: [If no action] Flag for CSM personal outreach
```

## 第四阶段：流失预防

### 早期预警系统

**在客户流失前60-90天检测到的关键指标：**

| 指标 | 检测方法 | 提前时间 |
|-----------|-----------------|-----------|
| 月度使用量下降超过30% | 自动监控 | 90天 |
| 产品倡导者更换工作 | 通过LinkedIn监控、邮件回复率分析 | 60-90天 |
| 支持工单数量激增后骤减 | 工单趋势分析 | 60天 |
| 访问计费页面但未升级 | 产品分析 | 45天 |
| 客户评估竞争对手产品 | 网络流量、销售情报 | 30-60天 |
| 请求数据导出 | 产品分析 | 30天 |
| 合同未续订的迹象 | 采购流程延迟、法律问题 | 30-45天 |
| 团队成员离职 | 许可证/使用席位变更 | 30天 |

### 流失原因分类

对每个流失案例进行分类，以便分析原因：

| 类别 | 子原因 | 是否可预防？ |
|----------|-------------|-------------|
| 产品问题 | 缺少功能、用户体验差、性能问题 | ✅ 部分可预防 |
| 价值问题 | 未实现投资回报、使用场景错误、过度销售 | ✅ 可预防 |
| 客户关系问题 | 产品倡导者离职、客服体验差、信任破裂 | ✅ 可预防 |
| 财务问题 | 预算削减、并购、破产、价格过高 | ⚠️ 有时不可预防 |
| 竞争问题 | 客户转向竞争对手、内部开发替代方案 | ✅ 部分可预防 |
| 战略问题 | 业务方向调整、部门关闭、优先级降低 | ❌ 很少见 |

### 根据流失原因制定的挽救措施

**产品问题：**
- 向产品团队报告对收入的影响（年经常性收入ARR受威胁）
- 提供临时解决方案或专业服务来弥补差距
- 分享产品路线图及交付时间表
- 如果新功能将在90天内推出，提供折扣优惠

**价值问题未实现：**
- 重新引导客户：制定新的成功计划、设定新目标、提供新的培训
- 指派资深客服人员或解决方案架构师
- 提供“价值冲刺”服务——为期30天的密集培训，以证明投资回报
- 每周记录快速成果，并与高层沟通

**产品倡导者离职：**
- 在48小时内确定新的主要联系人
- 提供“新客户关系建立”会议
- 重新建立与高层的沟通
- 提供新的业务案例文档供新倡导者使用

**价格问题：**
- 在未获得回报之前，切勿打折（例如多年订阅客户、请求案例研究或推荐）
- 重新调整合同：移除未使用的功能/席位、调整合同规模
- 提供付款条款（例如将季度付款改为年度付款）
- 展示投资回报：「您目前支付X美元，但可以带来Y美元的价值」

**竞争对手威胁：**
- 发布竞争对手的产品对比资料
- 利用与竞争对手的关系进行沟通
- 利用高层之间的联系
- 分析切换成本

---

## 第五阶段：业务扩展与收入增长

### 净收入留存率（NRR）框架

**不同客户群体的目标NRR：**

| 客户群体 | 良好 | 优秀 | 世界级 |
|---------|------|-------|-------------|
| 企业级SaaS | 110% | 120% | 130%以上 |
| 中端市场SaaS | 105% | 110% | 120%以上 |
| 中小企业SaaS | 95% | 100% | 110%以上 |

**NRR公式：**（起始年经常性收入MRR + 扩展收入 - 流失收入）/ 起始年经常性收入MRR × 100%

### 业务扩展信号

注意这些购买信号：

| 信号 | 重要性 | 应采取的行动 |
|--------|----------|------|
| 使用量达到上限 | 🔥 高风险 | 主动提议升级 |
| 新团队/部门询问产品相关信息 | 🔥 高风险 | 安排产品介绍会议 |
| 请求高级功能 | 🔥 高风险 | 展示高级功能的试用方案 |
| 公司宣布融资轮次或业务扩展 | 🟡 中等风险 | 表示祝贺，并提供支持 |
| 产品倡导者获得晋升 | 🟡 中等风险 | 表示祝贺，并提供进一步的支持 |

### 业务扩展策略

**席位扩展：**
1. 每月监控席位使用情况
2. 当席位使用率超过80%时：「您即将达到容量上限——这里有优惠方案」
3. 提供批量折扣，鼓励长期订阅 |
4. 分享采用成功的案例：「您团队的使用情况在我们客户中排名前10%」

**等级升级：**
1. 确定哪些高级功能符合他们的需求
2. 运行“高级功能试用”活动——提供14天的试用机会 |
3. 计算升级的投资回报：「功能X将为您的团队节省Y小时的工作时间」
4. 提供升级方案：在续订时优惠，或在中期进行升级

**交叉销售（新产品）：**
1. 分析客户的技术栈，找出需求缺口
2. 提供相关案例研究进行介绍
3. 提供试用服务：「30天的概念验证，无需立即承诺」
4. 组合定价：「产品B的价格比单独购买便宜20%」

**新部门拓展：**
1. 询问产品倡导者：「还有哪些部门面临类似挑战？」
2. 为新部门提供免费的工作坊 |
3. 为新的产品倡导者提供内部演示材料 |
4. 为新部门制定新的成功计划和新的客户关系管理策略 |

---

## 第六阶段：定期业务回顾（QBR）

### 定期业务回顾（QBR）结构（60分钟）

```
1. Business Context (10 min)
   - Customer shares business updates, priorities, challenges
   - CS listens — do NOT present slides first

2. Value Delivered (15 min)
   - Usage dashboard: adoption, engagement, trends
   - ROI recap: goals set → outcomes achieved → dollar impact
   - Success stories: specific wins this quarter
   - Comparison: "Here's how you compare to peers in your industry"

3. Roadmap & Innovation (10 min)
   - Product roadmap aligned to THEIR priorities
   - Early access / beta opportunities
   - Industry trends and best practices

4. Success Plan Review (15 min)
   - Score previous quarter's goals
   - Set next quarter's objectives
   - Identify blockers and resource needs
   - Assign owners and timelines

5. Strategic Discussion (10 min)
   - "What keeps you up at night?"
   - "Where is the business heading in the next 12 months?"
   - Expansion opportunities (based on their strategy)
   - Introduce new stakeholders if relationship gaps exist
```

### QBR准备 checklist

```
□ Pull 90-day usage data and create dashboard
□ Calculate ROI / value delivered (specific numbers)
□ Review health score trend (improving? declining?)
□ Check open support tickets — resolve before QBR
□ Review success plan — score each goal
□ Draft next quarter objectives (aligned to their business)
□ Prepare 1-2 expansion recommendations with ROI projections
□ Identify who should attend (their side + yours)
□ Send pre-read agenda 5 days before
□ Prepare competitive intel (in case competitors come up)
```

### QBR后的跟进模板

```
Subject: [Company] + [Your Company] — Q[X] Review Recap & Next Steps

Hi [Name],

Thank you for a productive review today. Here's a summary:

**What We Achieved in Q[X]:**
- [Goal 1]: [Result + metric]
- [Goal 2]: [Result + metric]
- [Goal 3]: [Result + metric]

**Q[X+1] Objectives:**
1. [Objective] — Owner: [Name], Target: [Date]
2. [Objective] — Owner: [Name], Target: [Date]
3. [Objective] — Owner: [Name], Target: [Date]

**Action Items:**
- [ ] [Action] — [Owner] by [Date]
- [ ] [Action] — [Owner] by [Date]

**Next QBR:** [Date]

Looking forward to another strong quarter together.

[Name]
```

## 第七阶段：挽回流失客户的活动

### 持续流失客户的挽回时机

| 自流失后时间 | 推广方式 | 成功率 |
|-----------------|----------|-------------|
| 0-30天 | 发送“我们想念您”的邮件，并说明流失原因 | 15-25% |
| 30-90天 | 发送产品更新信息和改进成果 | 10-15% |
| 90-180天 | 发送重大产品更新信息和特别优惠 | 5-10% |
| 180-365天 | 进行年度回顾和案例研究 | 2-5% |
| 超过365天 | 从活跃客户名单中移除 | <2% |

### 持续流失客户的挽回邮件序列

**流失后第7天的邮件：**
```
Subject: We fixed [their specific issue]

Hi [Name],

I know [specific churn reason] was frustrating. I wanted you to know we've [specific improvement].

[If product: "Here's what changed: [feature/fix description]"]
[If value: "We've redesigned onboarding to get to value in [X days]"]
[If price: "We have new plans that might work better for your budget"]

No pressure — but if you'd like to take another look, I'm here.

[Name]
```

**流失后第30天的邮件：**
```
Subject: [Their industry] companies are seeing [specific result]

Hi [Name],

Since we last spoke, [similar company] achieved [specific metric] using [product].

We've shipped [X] improvements in the past month, including:
- [Improvement 1]
- [Improvement 2]

Would a quick catch-up be useful? Happy to show what's new.

[Name]
```

**仅在重大产品更新后的第90天发送的邮件：**
```
Subject: [Product] [Version] — built with your feedback

Hi [Name],

We just launched [major feature/version] and your feedback directly influenced it.

[1-2 sentence description of what's new and why it matters to them]

I'd love to give you a private preview. Want to jump on a 15-minute call this week?

[Name]
```

## 第八阶段：客户服务指标仪表盘

### 每周客户服务指标

```yaml
cs_dashboard:
  week: "YYYY-WXX"
  portfolio:
    total_accounts: 0
    total_arr: 0
    health_distribution:
      green: { count: 0, arr: 0 }
      yellow: { count: 0, arr: 0 }
      orange: { count: 0, arr: 0 }
      red: { count: 0, arr: 0 }
  retention:
    gross_retention_rate: 0.0  # Target: >90%
    net_retention_rate: 0.0    # Target: >110%
    logo_retention_rate: 0.0   # Target: >85%
    arr_churned_mtd: 0
    arr_contracted_mtd: 0
  expansion:
    arr_expanded_mtd: 0
    expansion_pipeline: 0
    upsell_conversations: 0
    expansion_rate: 0.0  # Target: >15% annually
  engagement:
    avg_health_score: 0      # Target: >70
    health_score_trend: "up|flat|down"
    qbrs_completed: 0
    nps_score: 0             # Target: >50
    csat_score: 0.0          # Target: >4.5/5
  onboarding:
    active_onboardings: 0
    avg_ttfv_days: 0         # Target: <14 for MM, <30 for Ent
    onboarding_completion_rate: 0.0  # Target: >90%
  renewals:
    upcoming_30d: { count: 0, arr: 0 }
    upcoming_60d: { count: 0, arr: 0 }
    upcoming_90d: { count: 0, arr: 0 }
    on_track: 0
    at_risk: 0
```

### 每月需要审查的问题：

1. 哪些账户的健康状况从绿色降级为黄色或更差？原因是什么？
2. 哪些账户的健康状况有所改善？采取了哪些措施？
3. 本月流失的主要原因是什么？这种趋势是否持续？
4. 我们在排名前10的客户中是否实现了多渠道沟通？
5. 下一季度有哪些业务扩展计划？
6. 哪些客户服务经理负责的风险客户较多？
7. 定期业务回顾是否带来了可衡量的行为改变？
8. 哪些产品反馈需要上报给产品团队？

---

## 第九阶段：客户群体分析与留存策略

### 构建客户留存群体表格

按客户注册月份（或合同开始时间）进行跟踪，并定期评估。

**SaaS产品客户留存群体示例：**

```
              Month 0  Month 1  Month 2  Month 3  Month 6  Month 12
Jan cohort    100%     92%      87%      84%      78%      68%
Feb cohort    100%     94%      90%      88%      82%      —
Mar cohort    100%     91%      85%      —        —        —
```

**需要关注的重点：**
- **垂直提升：**新客户群体的留存情况是否更好？（产品/入职引导流程是否有效）
- **流失率急剧下降的原因：**在哪里？（第1-2个月可能是入职引导问题；第6-12个月可能是价值/续订问题）
- **表现最佳的客户群体：**哪些群体留存率最高？不同群体之间有何差异？（营销渠道、销售代表、入职引导流程的变化）
- **收入留存与客户保留的关系：**即使流失客户数量增加，收入是否仍保持稳定？（业务扩展是否起到了抵消作用）

### 客户参与度与留存率的关联分析

| 客户参与度 | 参与频率 | 留存预测 | 应采取的行动 |
|-----------------|----------|---------------------|--------|
| 高频用户 | 每天使用多个功能、创建内容 | 留存率超过95% | 推广计划、推动业务扩展 |
| 定期用户 | 每周使用3-4次核心功能 | 留存率85-95% | 推广产品功能、优化使用体验 |
| 偶尔使用用户 | 每周使用1-2次核心功能 | 留存率60-80% | 重新开展互动活动 |
| 低频用户 | 每周使用次数少于1次或完全不使用 | 留存率20-40% | 需要紧急干预 |
| 完全不活跃的用户 | 超过30天无任何活动 | 留存率低于20% | 需要采取挽回措施 |

## 第十阶段：个性化留存策略

### 根据客户类型制定不同的留存策略

**按企业规模划分：**
- 企业级客户：注重客户关系、高层支持、专属客户服务经理、定制化集成服务 |
- 中端市场客户：注重业务流程、可扩展的沟通方式、共享客户服务资源 |
- 中小企业客户：注重产品体验、提供自助服务、自动化沟通机制 |

**根据客户成熟度划分：**
- 第1年：重点关注入职引导、首次产生价值、快速实现成果 |
- 第2年：优化产品使用、推动业务扩展、深化集成 |
- 第3年及以上：建立战略合作伙伴关系、高层支持、整合平台资源 |

### 客户顾问委员会（CAB）

**结构：**
- 由8-12位客户组成，涵盖不同类型和行业 |
- 每季度举行一次虚拟会议（90分钟）+ 每年一次面对面会议 |
| 主要议题：产品路线图建议、市场趋势、同行交流 |
| 激励措施：提前体验新产品功能、直接与产品团队沟通、获得认可 |

**选拔标准：**
- 健康状况评分超过70分 |
- 使用产品超过6个月 |
- 愿意提供坦诚的反馈 |
- 代表具有代表性的客户群体或使用场景 |

### 客户声音（VoC）收集计划

**收集方式：**
1. 客户满意度调查（NPS）：每季度一次（关注客户关系）+ 交互后的调查 |
2. 客服满意度调查：在提供支持后、入职引导后、定期业务回顾后 |
3. 应用内反馈：收集功能需求、错误报告、满意度调查 |
4. 沟通后的访谈：在决策后30天内进行 |
5. 客户流失后的访谈：在决策后30天内进行 |
6. 客户顾问委员会：定期召开反馈会议 |

**行动方案：**
- 评分0-6分（负面评价）：在24小时内进行个人沟通，分析根本原因并制定恢复计划 |
- 评分7-8分（中性评价）：后续发送改进调查、提供功能使用指南 |
- 评分9-10分（正面评价）：表示感谢，请求客户提供评价/推荐/案例研究 |

### 多产品客户的成功管理

当客户使用多个产品时：
- 综合评估各产品的健康状况（根据每个产品的年收入ARR贡献进行加权）
- 指定一名客户服务经理作为主要联系人，根据需要安排产品专家支持 |
- 对于使用多个产品的客户：「由于您使用了产品A，因此您也可以使用产品B」 |
- 组合进行定期业务回顾：一次性的全面评估 |

---

## 特殊情况处理

### 合并与收购

- 客户被收购：这是一个扩展业务的机会（新增用户/部门） |
- 被收购方：存在风险——新管理层可能会更换供应商。需提前行动：与新管理层沟通、重新证明产品价值、做好应对准备 |
- 被收购方：主动沟通、确保服务连续性、提供留存激励措施 |

### 季节性业务

- 根据预期使用量变化调整健康状况评分（不要将季节性使用量下降视为流失风险） |
- 在旺季前加强客户互动 |
- 定期业务回顾的时间安排应与业务高峰期相匹配 |

### 产品倡导者疲劳问题

- 如果产品倡导者在内部推广产品但缺乏支持，提供帮助：提供内部演示材料、投资回报报告和高层总结文件 |
- 减轻他们的负担：为他们的团队提供管理培训、自助服务资源 |
- 公开表彰他们的成果（如获得认可），以提高他们的内部影响力 |

### 经济低迷时期

- 主动沟通：「我们知道您的预算紧张——让我们一起分析您的投资回报」 |
- 提供合适的合同条款、付款灵活性、投资回报分析 |
- 强调节省成本的优势：「使用我们的服务可以节省多少费用」

### 客户服务接触方式的调整

- 根据客户的使用情况调整服务等级：
  - 降低服务等级时：清晰沟通变化内容 |
  - 提供自助服务工具包，替代传统的客户服务会议 |
  - 设置自动化的健康状况监控机制，并设置升级触发条件 |
  - 在调整服务等级时提供沟通支持 |

---

## 常用命令

使用以下命令与系统交互：

1. **“[账户]的评分”** — 计算该账户的健康状况评分 |
2. **[账户]的入职引导计划”** — 生成该账户的90天入职引导计划 |
3. **[账户]的定期业务回顾准备”** — 生成定期业务回顾的议程、数据总结和推荐措施 |
4. **[账户]的流失风险”** — 分析关键指标并生成风险评估 |
5. **[账户]的扩展机会”** — 识别并评估扩展策略 |
6. **[账户]的挽回计划”** — 根据流失原因生成挽回计划 |
7. **[账户]的续订准备”** — 生成续订时间表、风险评估和沟通内容 |
8. **[账户]的产品组合回顾”** — 生成所有跟踪账户的每周客户服务指标仪表盘 |
9. **[账户]的留存群体分析”** — 根据客户数据构建留存群体表格 |
10. **[账户]的成功计划”** — 生成或更新该账户的成功计划，包括目标和里程碑 |
11. **[账户]的挽回措施”** — 为高风险客户生成干预计划 |
12. **[账户]的净收入留存报告”** — 计算包含扩展影响的净收入留存率