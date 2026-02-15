---
name: afrexai-competitive-intel
description: 完整的竞争情报系统——包括市场分析、产品拆解、价格信息、盈亏分析、竞争态势图以及战略监控功能。其覆盖范围远超单纯的搜索引擎优化（SEO），能够全面呈现企业的商业环境。
---

# 竞争情报引擎

这是一个全面的系统，用于了解、跟踪并超越竞争对手。涵盖市场分析、产品研究、价格策略、销售分析以及持续监控等功能。

## 使用场景

- 进入新市场或推出新产品时
- 由于竞争对手的原因失去交易，需要了解原因时
- 进行季度战略评估时
- 制定定价策略时（新产品或价格调整）
- 销售团队需要准备应对竞争对手的论据时
- 对目标公司或收购方进行尽职调查时
- 为投资者准备演示材料时（展示对市场情况的了解）
- 根据竞争对手的不足制定内容策略时

---

## 第一阶段：市场分析

### 1.1 竞争对手识别

将每个竞争对手分为四个层级：

| 层级 | 定义 | 例子 | 监控频率 |
|------|-----------|---------|---------------------|
| **直接竞争对手** | 提供相同产品、面向相同客户群 | 最接近的竞争对手 | 每周 |
| **相关竞争对手** | 提供不同产品、但目标客户群重叠 | 扩展到您所在领域的平台 | 每两周 |
| **间接竞争对手** | 解决相同问题但采用不同方案 | 用电子表格替代您的SaaS产品 | 每月 |
| **新兴竞争对手** | 处于早期阶段、具有相似愿景 | 与您同领域的初创公司 | 每月 |

### 发现竞争对手的方法

系统地搜索以下信息来源：

1. **Google**：输入“[您的行业]软件/工具/服务” —— 记录排名前10的搜索结果（自然搜索+广告）
2. **G2/Capterra/TrustRadius**：进入您的行业页面 —— 根据评分记录排名前10的产品 |
3. **Product Hunt**：搜索您的关键词 —— 按投票数排序 |
4. **Crunchbase**：搜索您的行业 —— 筛选已获得融资的公司 |
5. **LinkedIn**：查看“[竞争对手名称]”的公司页面 —— 关注员工数量的变化 |
6. **Reddit/HN**：搜索“[竞争对手名称]的替代品”或“[行业]推荐”
7. **客户访谈**：询问“您还评估过哪些竞争对手？” |
8. **失败的交易记录**：分析哪些交易被竞争对手夺走以及原因是什么？

### 市场分析 YAML

```yaml
market_map:
  category: "[Your Category]"
  date: "YYYY-MM-DD"
  total_addressable_market: "$XB"
  
  competitors:
    - name: "Competitor A"
      tier: "direct"
      website: "https://..."
      founded: 2019
      funding: "$50M Series B"
      estimated_revenue: "$10-20M ARR"
      employee_count: 150
      employee_trend: "growing"  # growing | stable | shrinking
      hq: "San Francisco, CA"
      key_customers: ["Customer 1", "Customer 2"]
      primary_market: "mid-market"  # smb | mid-market | enterprise
      positioning: "All-in-one platform for X"
      strengths: ["Feature A", "Strong brand"]
      weaknesses: ["Expensive", "Slow support"]
      threat_level: "high"  # low | medium | high | critical
      notes: ""
```

---

## 第二阶段：产品分析

### 2.1 功能对比

为每个直接竞争对手制作功能对比表：

```yaml
feature_matrix:
  last_updated: "YYYY-MM-DD"
  
  categories:
    - name: "Core Features"
      features:
        - name: "Feature X"
          us: "full"       # none | partial | full | superior
          competitor_a: "full"
          competitor_b: "partial"
          weight: 5        # 1-5 importance to buyer
          notes: "We have deeper customization"
          
        - name: "Feature Y"
          us: "none"
          competitor_a: "full"
          competitor_b: "full"
          weight: 3
          notes: "On our roadmap for Q3"
    
    - name: "Integrations"
      features:
        - name: "Salesforce"
          us: "full"
          competitor_a: "partial"
          weight: 4
```

### 2.2 产品分析模板

对每个主要竞争对手进行结构化的产品分析：

```markdown
## [Competitor Name] Product Teardown
**Date:** YYYY-MM-DD
**Analyst:** [name]

### First Impressions (0-5 min)
- Homepage messaging: What problem do they lead with?
- Sign-up friction: How many steps? What info required?
- Time to value: How fast can you DO something?
- Design quality: Modern, dated, cluttered, clean?

### Onboarding (5-30 min)
- Guided tour? Checklist? Video? Nothing?
- Sample data provided? Sandbox mode?
- How quickly did you feel competent?
- What confused you?

### Core Workflow
- Complete their primary use case end-to-end
- Note: steps required, clicks per task, speed, error handling
- Screenshot key screens

### Differentiators
- What can they do that we can't? (be honest)
- What's their "magic moment"?
- What do their happiest customers praise? (check G2 reviews)

### Weaknesses
- Where did you get stuck?
- What felt missing or half-baked?
- What do their angriest customers complain about? (check G2 1-2 star reviews)

### Pricing vs Value
- What plan would a typical customer need?
- Price per user/month at that tier?
- Any hidden costs (implementation, support, integrations)?
- Free trial? Freemium? Money-back guarantee?

### Technical Assessment
- Stack: (check Wappalyzer, BuiltWith, job postings)
- API: Public? REST/GraphQL? Rate limits? Docs quality?
- Mobile: Native app? Responsive web? PWA?
- Performance: Page load speed, UI responsiveness
- Uptime: Status page? Historical incidents?
```

### 2.3 用户体验评分标准

对每个竞争对手的产品进行评分（每个维度0-10分）：

| 维度 | 评估内容 | 权重 |
|-----------|-----------------|--------|
| **易用性** | 达到初始使用价值所需的时间、上手难度 | 15% |
| **核心用户体验** | 主要工作流程的效率、直观性 | 25% |
| **功能深度** | 是否涵盖边缘情况、高级用户的需求 | 20% |
| **可靠性** | 运行时间、遇到的错误、错误处理 | 15% |
| **集成能力** | 生态系统的广度、API的质量 | 10% |
| **支持服务** | 响应时间、服务质量、自助服务资源 | 10% |
| **移动端支持** | 移动端的体验、功能是否齐全 | 5% |
| **总分 = 各维度得分之和。在竞争对手之间进行比较。**

---

## 第三阶段：价格策略

### 3.1 价格对比表

```yaml
pricing_intel:
  date: "YYYY-MM-DD"
  
  competitors:
    - name: "Us"
      model: "per-seat"  # per-seat | usage | flat | hybrid | freemium
      entry_price: "$29/user/mo"
      mid_price: "$79/user/mo"
      enterprise_price: "Custom"
      free_tier: true
      free_limits: "5 users, 1000 records"
      annual_discount: "20%"
      contract_required: false
      implementation_fee: "$0"
      hidden_costs: []
      
    - name: "Competitor A"
      model: "per-seat"
      entry_price: "$49/user/mo"
      mid_price: "$99/user/mo"
      enterprise_price: "Custom ($150+/user)"
      free_tier: false
      annual_discount: "15%"
      contract_required: true  # annual minimum
      implementation_fee: "$5,000"
      hidden_costs: ["API access on enterprise only", "SSO $50/user extra"]
```

### 3.2 定价策略分析

回答以下问题：

1. **我们的定位在哪里？** 在价格（低→高）和功能深度（基础→高级）的二维坐标系中定位所有竞争对手 |
2. **谁的价格最低？** 对于10个用户？50个用户？200个用户？（价格通常会随着用户数量的变化而变化） |
3. **总拥有成本**：包括实施成本、培训费用、迁移费用和隐藏费用 |
4. **性价比**：与每个竞争对手相比，功能与价格的比例 |
5. **价格趋势**：竞争对手是否在涨价？（可以通过Wayback Machine查看历史价格变化）
6. **折扣政策**：他们在交易中是否提供大幅折扣？（询问销售团队，或查看G2上的用户评价）

### 3.3 定价策略建议

根据分析结果，选择以下策略之一：

| 策略 | 适用场景 | 风险 |
|----------|------------|------|
| **高端策略** | 产品明显优于竞争对手且品牌知名度高 | 可能会失去对价格敏感的客户 |
| **价格平价策略** | 产品相似时，在其他方面竞争 | 可能导致价格战 |
| **渗透策略** | 新进入者，需要快速获取市场份额 | 可能被认为产品质量较低 |
| **价值策略** | 以更低的价格提供更好的产品 | 如果成本上升，可能会影响利润率 |
| **细分市场策略** | 面向特定细分市场的竞争对手 | 目标客户群较小 |

---

## 第四阶段：销售分析

### 4.1 销售分析模板

为每个直接竞争对手创建一份销售分析报告：

```markdown
# 🏆 Battlecard: Us vs [Competitor]
**Last Updated:** YYYY-MM-DD | **Confidence:** High/Medium/Low

## Quick Stats
| Metric | Us | Them |
|--------|-----|------|
| Founded | | |
| Funding | | |
| Est. Revenue | | |
| Employees | | |
| G2 Rating | | |
| Gartner Position | | |

## Their Pitch (in their words)
"[Their homepage headline or elevator pitch]"

## Why Customers Choose Us Over Them
1. **[Reason 1]**: [Specific proof point — customer quote, metric, demo moment]
2. **[Reason 2]**: [Specific proof point]
3. **[Reason 3]**: [Specific proof point]

## Why Customers Choose Them Over Us (be honest)
1. **[Reason 1]**: [And how to counter it]
2. **[Reason 2]**: [And how to counter it]

## Landmines to Plant 🧨
Questions to ask the prospect that expose competitor weaknesses:
1. "Ask them how they handle [weakness area] — you'll find it requires [workaround]"
2. "Request a demo of [specific feature] — it's not as deep as it looks"
3. "Ask about [hidden cost] — it's not on the pricing page"

## Objection Handling

**"[Competitor] is cheaper"**
> Response: "At first glance, yes. But when you factor in [hidden cost 1], [hidden cost 2], and [limitation requiring workaround], the total cost is actually [higher/comparable]. Plus, [our unique value] saves you [X hours/dollars] per [period]."

**"[Competitor] has [feature we lack]"**
> Response: "[Acknowledge honestly]. Here's why our customers find that [our approach] actually works better for [their use case]: [specific reasoning]. [Customer name] evaluated both and chose us specifically because [reason]."

**"We're already using [Competitor]"**
> Response: "That makes sense — they're solid at [genuine strength]. The customers who switch to us typically hit a wall with [specific limitation]. Are you experiencing [common pain point with that competitor]?"

## Trap Plays (When to Walk Away)
- If prospect needs [specific capability we truly lack], acknowledge it honestly
- If they're deeply embedded in [competitor ecosystem], switching cost may be too high
- If deal size is below $[X], cost of competing isn't worth it

## Win Stories
- **[Customer A]**: Switched from [Competitor] because [reason]. Result: [metric improvement]
- **[Customer B]**: Evaluated both, chose us because [reason]. Quote: "[testimonial]"

## Recent Intel
- [Date]: [Competitor] announced [product change/funding/hire]
- [Date]: [Customer feedback about competitor]
```

### 4.2 快速应对策略

为销售团队提供日常使用的应对策略矩阵：

| 常见反对意见 | 短暂回应 | 证据 |
|-----------|---------------|-------------|
| “太贵了” | [重新阐述产品价值] | [投资回报率数据或客户评价] |
| “从未听说过你们” | [提供社交证明] | [客户推荐或G2排名] |
| “缺少[某功能]” | [提供替代方案或产品路线图] | [临时解决方案或实施时间表] |
| “对现有工具很满意” | [提出引导性问题] | [现有工具的常见问题] |
| “需要企业级功能” | [说明我们提供的企业级功能] | [企业客户案例] |

---

## 第五阶段：胜负分析

### 5.1 胜败分析框架

在每次重大交易（无论胜负）后，记录相关数据：

```yaml
win_loss:
  deal: "[Company Name]"
  date: "YYYY-MM-DD"
  outcome: "won"  # won | lost | no-decision
  deal_size: "$X ARR"
  sales_cycle_days: 45
  competitors_evaluated: ["Competitor A", "Competitor B"]
  
  decision_factors:
    - factor: "Ease of use"
      importance: 5  # 1-5
      our_score: 4   # 1-5
      winner_score: 3
      notes: "Demo experience was decisive"
      
    - factor: "Price"
      importance: 4
      our_score: 3
      winner_score: 4
      notes: "We were 20% more expensive but justified by ROI"
      
    - factor: "Integration with Salesforce"
      importance: 5
      our_score: 5
      winner_score: 2
      notes: "They required middleware; we're native"
  
  champion: "VP of Sales"
  decision_maker: "CRO"
  buying_trigger: "Previous tool couldn't scale past 50 users"
  
  key_quote: "Your Salesforce integration sealed the deal"
  
  lessons:
    - "Lead with integration story for Salesforce-heavy orgs"
    - "ROI calculator was critical for justifying premium price"
```

### 5.2 胜败趋势仪表盘

定期（每季度）跟踪胜负情况：

```markdown
## Q[X] Win/Loss Summary

### Win Rate by Competitor
| Competitor | Wins | Losses | Win Rate | Trend |
|-----------|------|--------|----------|-------|
| Competitor A | 12 | 8 | 60% | ↑ (was 50%) |
| Competitor B | 5 | 15 | 25% | ↓ (was 35%) |
| No competition | 20 | 3 | 87% | → |

### Top Win Reasons (ranked by frequency)
1. Ease of use (mentioned in 65% of wins)
2. Integration depth (55%)
3. Customer support (40%)

### Top Loss Reasons (ranked by frequency)
1. Price (mentioned in 70% of losses)
2. Missing [specific feature] (45%)
3. Incumbent relationship (30%)

### Action Items from This Quarter's Losses
1. [Feature gap] → Product team building for Q[X+1]
2. [Price objection] → New ROI calculator + case study
3. [Competitor strength] → Invest in [counter-strategy]
```

---

## 第六阶段：持续监控

### 6.1 竞争对手动态监控

为每个直接竞争对手设置监控机制：

| 监控指标 | 来源 | 监控频率 | 关注内容 |
|--------|--------|-----------|-----------------|
| **产品更新** | 对方的更新日志/博客 | 每周 | 新功能、功能淘汰 |
| **价格变化** | 官方价格页面或Wayback Machine | 每月 | 价格变动、新的价格层级、产品模式变化 |
| **招聘动态** | LinkedIn上的招聘信息 | 每两周 | 工程团队扩张可能意味着新产品发布；销售增长可能预示着业务扩张 |
| **融资动态** | Crunchbase、TechCrunch | 实时更新 | 新轮融资可能预示着扩张计划 |
| **领导层变动** | LinkedIn、新闻报道 | 实时更新 | 新CEO或首席运营官的任命可能预示着战略调整 |
| **用户评价** | G2、Capterra | 每月 | 用户情绪变化、常见问题 |
| **内容发布** | 对方的博客、社交媒体 | 每周 | 发布的内容、市场定位的变化 |
| **客户动态** | 新闻稿、案例研究 | 每月 | 新客户、目标行业 |
| **社区动态** | Reddit、HackerNews、Twitter | 每周 | 客户反馈、评价、功能需求 |

### 6.2 周报模板

```markdown
## Competitive Intel Brief — Week of [Date]

### 🔴 Critical (action needed)
- [Competitor X] launched [feature] that directly competes with our [feature]
  - Impact: [assessment]
  - Recommended response: [action]

### 🟡 Notable (monitor)
- [Competitor Y] raised Series C ($40M) — expect aggressive hiring/marketing
- [Competitor Z] changed pricing model from per-seat to usage-based

### 🟢 Informational
- [Competitor X] published blog post about [topic]
- [Competitor Y] hiring 3 new enterprise AEs in EMEA

### Win/Loss This Week
- Won [Deal] vs [Competitor] — reason: [X]
- Lost [Deal] to [Competitor] — reason: [X]
```

### 6.3 季度竞争分析议程

1. **市场分析更新**（15分钟）：是否有新进入者？是否有竞争对手退出市场？市场层级是否有变化？
2. **功能差距分析**（20分钟）：竞争对手发布了哪些新功能？我们应该如何应对？
3. **胜负趋势分析**（15分钟）：我们的市场份额是在增加还是减少？相对于哪些竞争对手？
4. **价格检查**（10分钟）：是否有价格变动？我们的定位是否仍然合适？
5. **销售分析报告更新**（15分钟）：更新所有活跃的销售分析报告 |
6. **战略决策**（15分钟）：根据所有收集到的信息，我们应该优先投资哪些方面？

---

## 第七阶段：战略框架

### 7.1 竞争优势评估

评估您自己的竞争优势以及每个竞争对手的竞争优势（1-5分）：

| 竞争优势类型 | 描述 | 我们 | 竞争对手A | 竞争对手B |
|-----------|------------|-----|--------|--------|
| **网络效应** | 用户越多，产品体验越好 | | | |
| **转换成本** | 随着用户数量增加，离开现有平台的成本越高 | | | |
| **数据优势** | 独有的数据有助于提升产品体验 | | | |
| **品牌优势** | 品牌知名度、客户信任 | | | |
| **规模经济** | 规模带来的成本优势 | | | |
| **法规优势** | 许可证、认证、合规性要求 | | | |
| **技术优势** | 专利、专有技术、技术速度 | | | |
| **生态系统优势** | 集成能力、合作伙伴关系、市场地位 | | | |

**总竞争优势得分 = 各项优势得分之和。得分越高，越难以被取代。**

### 7.2 竞争对手反应预测

对于每个主要竞争对手的动向，预测他们可能采取的应对策略：

```markdown
**If we [action]...**
- Competitor A will likely: [response] because [reasoning]
- Competitor B will likely: [response] because [reasoning]
- Timeline: [how fast they'll respond]
- Our counter-move: [what we do next]
```

### 7.3 蓝海市场机会

在分析所有竞争对手后，寻找以下机会：

1. **未被充分服务的市场细分**：被所有人忽视的客户群体（市场规模太小？过于细分？过于复杂？）
2. **未被满足的需求**：客户实际需要的功能或能力 |
3 **体验差距**：现有产品在这些方面的不足 |
4 **商业模式创新**：是否可以通过不同的收费方式获得竞争优势？（按使用量收费？按结果收费？）
5 **渠道覆盖差距**：哪些客户群体尚未被触及？（垂直社区、特定地区、语言）

---

## 特殊情况与高级技巧

### 隐形竞争对手
- 监控您所在领域的专利申请（使用Google Patents）
- 关注YC/TechStars等创业大赛上的行业新进入者展示 |
- 在大型科技公司的招聘信息中搜索与您的行业相关的职位信息（可能预示着内部研发）

### 国际竞争对手
- 用目标语言搜索相关产品 |
- 查看当地的评价网站（Capterra提供按国家分类的信息）
- 不同市场可能有不同的市场领导者——按地区划分进行分析

### 平台相关风险
- 如果您基于某个平台（如Salesforce、Shopify等）开发产品，需监控该平台本身的动态 |
- 平台经常推出新的插件或功能 |
- 关注该平台在您所在领域的收购情况

### 竞争情报收集的道德规范
- ✅ 使用公开信息（网站、新闻报道、招聘信息、用户评价、专利）
- ✅ 收集关于竞争对手的客户反馈（通过胜负分析）
- ✅ 参加产品试用和演示活动（正常注册即可）
- ❌ 使用虚假身份获取受限内容 |
- ❌ 为获取情报而挖走竞争对手的员工 |
- ❌ 访问机密文件 |
- ❌ 对受保护的代码进行逆向工程

---

## 自然语言命令

| 命令 | 功能 |
|---------|-------------|
| “绘制我的竞争格局” | 完整的市场分析（第一阶段） |
| “分析[竞争对手]的产品” | 产品详细分析（第二阶段） |
| “与[竞争对手]比较价格” | 价格策略分析（第三阶段） |
| “为[竞争对手]制作销售分析报告” | 销售分析报告（第四阶段） |
| “分析我们的胜负数据” | 胜败模式分析（第五阶段） |
| “生成每周竞争报告” | 持续监控的总结（第六阶段） |
| “评估我们的竞争优势” | 战略分析（第七阶段） |
| “寻找蓝海市场机会” | 市场机会分析（第七阶段） |
| “针对[竞争对手的动向应如何应对？” | 竞争策略建议（第七阶段） |
| “进行全面竞争分析” | 所有阶段的综合报告 |