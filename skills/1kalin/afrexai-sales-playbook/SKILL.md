---
name: afrexai-sales-playbook
version: 1.0.0
description: "完整的B2B销售系统——从潜在客户的发现（ICP）到交易的最终达成。该系统涵盖发现潜在客户的方法、处理客户异议的流程、销售管道管理、销售预测以及加速交易成交的功能，适用于所有B2B企业。"
author: afrexai
tags: sales, b2b, pipeline, crm, deals, closing, objections, forecasting, revenue
---
# B2B销售手册 ⚡

**一套用于执行可复制、可扩展的B2B销售操作的完整系统。**

这不是一个CRM包装工具，也不是一个模板集合。这是一套完整的销售方法论——从识别理想客户到完成交易并扩展业务关系。

---

## 第一阶段：理想客户画像（ICP）与销售区域规划

### ICP定义模板
```yaml
icp:
  company:
    industry: [SaaS, Fintech, Healthcare, etc.]
    size_employees: [50-500]
    size_revenue: [$5M-$50M ARR]
    geography: [US, UK, DACH, etc.]
    tech_stack: [signals they use tools you integrate with]
    growth_stage: [Series A-C, post-PMF, scaling]
    
  pain_indicators:  # Observable signals, not assumptions
    - hiring_for: [roles that signal the pain you solve]
    - tech_adoption: [recently adopted X tool = need for Y]
    - org_changes: [new VP of X = budget for initiatives]
    - regulatory: [upcoming compliance deadline]
    - public_statements: [earnings call mentions, press releases]
    
  buyer_personas:
    economic_buyer:  # Signs the check
      title_patterns: [VP Sales, CRO, CEO]
      cares_about: [revenue growth, cost reduction, competitive advantage]
      speaks_in: [ROI, board metrics, market share]
      
    champion:  # Fights for you internally
      title_patterns: [Director, Head of, Senior Manager]
      cares_about: [team productivity, career advancement, solving daily pain]
      speaks_in: [workflow, efficiency, team capacity]
      
    technical_evaluator:  # Validates feasibility
      title_patterns: [Engineering Manager, Architect, IT Director]
      cares_about: [integration, security, maintenance burden]
      speaks_in: [APIs, uptime, migration effort]
      
    end_user:  # Uses it daily
      title_patterns: [Individual contributors]
      cares_about: [ease of use, time saved, fewer context switches]
      
  anti-signals:  # DO NOT pursue
    - company_size_under: 20  # too small, long sales cycle for low ACV
    - no_budget_indicator: [startup pre-revenue, recent layoffs >30%]
    - tech_mismatch: [on-prem only, legacy stack incompatible]
    - cultural: [committee-driven decisions with 6+ stakeholders at low ACV]
```

### 销售区域规划

**客户分级：**

| 级别 | 判断标准 | 客户数量 | 时间分配 | 联系频率 |
|------|----------|----------|-----------------|-----------------|
| **一级** | 完全符合ICP标准且有明显的业务痛点 | 20-30个客户 | 50%的时间 | 每周2-3次 |
| **二级** | 符合ICP标准但暂无明显业务痛点 | 50-80个客户 | 30%的时间 | 每周1次 |
| **三级** | 部分符合ICP标准，值得持续关注 | 100-200个客户 | 15%的时间 | 每月2次 |
| **新客户** | 任何符合条件的新客户 | 变动 | 5%的时间 | 1小时内回复 |

**每月销售区域回顾：**
1. 重新评估所有一级客户——是否有客户降级为二级？
2. 在二级客户中寻找新的业务线索——是否有客户升级为一级？
3. 将三级客户中90天内无任何互动的客户移除名单。
4. 从潜在客户中添加新客户。
5. 计算销售区域的覆盖率：（有互动的客户数量 / 总客户数量）——一级客户的覆盖率应超过80%。

---

## 第二阶段：潜在客户开发与主动联系

### 多渠道联系流程框架

**原则：**没有任何单一渠道是有效的。需要综合使用多种渠道。

**标准的一级客户开发流程（14天）：**

| 第一天 | 渠道 | 行动 | 目标 |
|-----|---------|--------|------|
| 1 | 电子邮件 | 发送个性化的冷邮件（参见下方模板） | 期望客户打开邮件并回复 |
| 1 | LinkedIn | 查看客户资料并添加好友（在好友请求信息中不推销产品） | 建立初步联系 |
| 3 | 电子邮件 | 发送附加价值的邮件（如文章、见解或数据） | 展示专业能力 |
| 5 | LinkedIn | 在客户的最新帖子下留言（真诚的，不要推销产品） | 增进熟悉感 |
| 7 | 电话 | 进行冷电话沟通（参见下方脚本） | 进行实时交流 |
| 7 | 电子邮件 | 发送语音邮件跟进 | 加强联系 |
| 10 | LinkedIn | 发送邮件提醒之前的沟通内容 | 促使客户再次回应 |
| 14 | 电话 | 最后一次尝试 | 最后一次联系 |

**流程规则：**
- 一旦客户回复（无论是正面还是负面），立即停止当前流程。
- 每天不要向同一客户发送超过一封邮件。
- 个性化内容必须涉及具体信息（如他们的公司、职位或近期动态）。
- 如果客户打开邮件但未回复三次，尝试通过电话联系。
- 如果在整个流程结束后客户仍无任何互动，将客户降级为三级，并在90天后重新尝试。

### 冷邮件模板

**模板1：基于触发事件的邮件**
```
Subject: [Trigger event] → quick thought

[First name],

Saw [specific trigger — new hire, funding, product launch, earnings mention].

When [companies in their situation] hit this stage, [specific problem] usually becomes the bottleneck — [data point or example].

[One sentence on how you solve this, tied to the trigger.]

Worth a 15-min call to see if this applies to [company]?

[Your name]
```

**模板2：基于同行推荐的邮件**
```
Subject: How [similar company] solved [problem]

[First name],

[Similar company in their industry] was dealing with [specific problem] — [quantify: X hours/week, $Y lost, Z% error rate].

They [brief result: cut X by 40%, saved $Y/month, shipped Z days faster].

Happy to share what they did differently — no pitch, just the playbook.

15 min this week?

[Your name]
```

**模板3：结束联系的邮件**
```
Subject: Closing the loop

[First name],

I've reached out a few times about [problem/topic] — I'll assume the timing isn't right.

If [problem] becomes a priority later, I'm here. 

Deleting your reminder from my CRM now.

[Your name]
```

**为什么结束联系的邮件有效：**回复率可达30-40%。人们会对失去机会感到不安。“删除您的提醒”会让他们担心失去联系机会。

### 冷电话脚本

**开场白（前10秒决定成败）：**
```
"Hi [Name], this is [You] from [Company]. 
Did I catch you at an okay time?"

[If yes:]
"I'll be brief. I noticed [trigger/signal] and wanted to ask —
are you currently dealing with [specific problem]?"

[If they confirm the problem:]
"Got it. What's that costing you right now — in time, money, or headaches?"

[Let them talk. Take notes. Ask follow-up questions.]

"That's exactly what we help with. [One sentence proof point.]
Would it make sense to set up 20 minutes this week to dig into this properly?"
```

**常见的客户回应及应对策略：**

| 客户回应 | 你的回应 |
|----------|---------|
| “不感兴趣” | “完全理解——请问是因为[问题]不是优先事项，还是您已经解决了这个问题？” |
| “请给我发封邮件” | “很乐意帮忙——具体需要哪些信息？这样我就不会浪费您的时间了。” |
| “我们已经有解决方案了” | “很好——效果如何？我接触的大多数公司都有相应的解决方案，但在[具体方面]仍有不足。” |
| “时机不好” | “什么时候比较合适？我可以为您安排一个提醒时间。” |
| “您是怎么得到我的电话号码的？” | “通过LinkedIn或您的网站。我知道冷电话不太愉快——我会尽量控制在2分钟内结束通话。” |

---

## 第三阶段：深入挖掘——最重要的会议

### MEDDPICC评估框架

对每个评估要素打分1-3分（1=未知，2=部分了解，3=完全确认）：
```yaml
deal_qualification:
  metrics:  # Quantifiable impact they care about
    score: [1-3]
    detail: "[What numbers matter? Revenue increase, cost reduction, time saved?]"
    source: "[Who told you? Validated how?]"
    
  economic_buyer:  # Person with budget authority
    score: [1-3]
    name: "[Name and title]"
    access: "[Have you spoken to them directly?]"
    priority: "[Is this in their top 3 priorities?]"
    
  decision_criteria:  # How they'll evaluate options
    score: [1-3]
    technical: "[Integration, security, performance requirements]"
    business: "[ROI threshold, payback period, risk tolerance]"
    political: "[Internal politics, competing priorities]"
    
  decision_process:  # How they'll make the decision
    score: [1-3]
    steps: "[What happens between now and signed contract?]"
    timeline: "[When do they need to decide? Hard deadline?]"
    stakeholders: "[Who's involved? Who has veto power?]"
    
  paper_process:  # Legal/procurement steps
    score: [1-3]
    procurement: "[Standard terms or custom negotiation?]"
    legal_review: "[How long does legal take? Past precedent?]"
    security_review: "[Required? How long?]"
    
  identified_pain:  # The problem driving this
    score: [1-3]
    pain: "[What hurts? What breaks?]"
    impact: "[Cost of inaction — quantified]"
    urgency: "[Why now? What happens if they wait?]"
    
  champion:  # Your internal advocate
    score: [1-3]
    name: "[Who is it?]"
    motivation: "[Why do THEY personally care?]"
    power: "[Can they influence the economic buyer?]"
    coached: "[Have you prepped them for internal selling?]"
    
  competition:  # What you're up against
    score: [1-3]
    competitors: "[Named competitors in the evaluation]"
    status_quo: "[Doing nothing is always a competitor]"
    differentiation: "[Why you win against each]"
    
  total_score: "[X/24]"
  # 20-24 = Strong deal, forecast confidently
  # 15-19 = Gaps to fill, work the unknowns
  # 10-14 = At risk, needs significant work
  # <10 = Unqualified, don't invest time
```

### 按类别划分的深入挖掘问题

**了解现状：**
1. 请详细说明[流程]目前是如何运作的。
2. 使用了哪些工具或系统？
3. 有多少人参与这个流程？
4. 这个流程已经存在多久了？

**发现痛点：**
5. 这个流程在哪里出问题？
6. 如果问题没有解决，会有什么后果？（请给出具体数字）
7. 这个问题多久发生一次？
8. 您尝试过哪些解决方法？
9. 为什么那些方法没有效果？

**分析影响：**
10. 如果这个问题在接下来的6个月内没有解决，会发生什么？
11. 这会对[他们的老板/团队/公司]产生什么影响？
12. 不采取任何行动的成本是多少？（迫使他们量化成本）
13. 还有哪些其他计划依赖于这个问题的解决？

**需求与收益分析（让客户自己描述解决方案）：**
14. 如果您能实现神奇的转变，会是什么样子？
15. 如果[问题]得到解决，对您的团队会有什么好处？
16. 如果[具体指标]得到改善，会带来什么结果？
17. [他们的老板]会对这些结果有何反应？

**了解购买流程：**
18. 除了您之外，还有谁需要参与决策？
19. 之前购买类似软件时发生了什么？
20. 是否有预算安排，或者需要获得批准？
21. 实现这个目标的理想时间表是什么？
22. 什么会阻碍交易的完成？

### 深入挖掘会议结构（30分钟）

| 阶段 | 时间 | 你的行动 |
|---------|------|-------------|
| 开场 | 2分钟 | 确认会议议程，设定预期，获得提问许可 |
| 了解现状 | 5分钟 | 询问相关问题，了解他们的实际情况 |
| 发现痛点 | 10分钟 | 询问问题，深入探讨1-2个痛点 |
| 展示未来愿景 | 5分钟 | 询问需求与收益相关的问题，描绘未来的状态 |
| 明确流程 | 5分钟 | 了解决策流程、时间表和相关方 |
| 下一步行动 | 3分钟 | 确定具体的下一步行动及时间安排 |

**黄金法则：**讲话时间控制在30%以内。如果讲话时间过长，就是在推销产品，而不是在挖掘客户需求。**

---

## 第四阶段：产品演示与展示

**问题-解决方案-验证框架**

**永远不要演示功能，而是展示实际效果。**

**流程：**
1. **反映他们的痛点**（2分钟）——“您提到[在挖掘阶段发现的具体痛点]。这会给他们带来多大的损失：[量化损失]。**
2. **展示解决方案**（15分钟）——使用他们的实际数据、术语和工作流程来演示解决方案。
3. **验证效果**（5分钟）——展示类似公司的案例研究，展示实施前的情况和实施后的效果。
4. **解决潜在风险**（3分钟）——提前提出他们尚未提出的主要担忧。
5 **下一步行动**（2分钟）——在会议结束时，一定要确定下一步的具体行动。

### 演示时的禁忌行为

| 不要做 | 应该做 |
|----------|---------------|
| 展示所有功能 | 只展示与他们痛点相关的内容 |
| 从“让我分享屏幕”开始 | 从“让我回顾您刚才说的内容”开始 |
| 说“我们还提供……” | 说“您提到了[痛点]——这是具体的解决方案” |
| 向整个团队演示 | 先向关键决策者演示，然后再进行集体讨论 |
| 演示时间过长 | 提前5分钟结束演示——时间越短越能体现专业性 |
| 演示结束后发送录像 | 发送一份包含具体投资回报的总结邮件 |

### 双方行动计划（MAP）

演示结束后，与潜在客户共同制定一份文档：
```yaml
mutual_action_plan:
  deal: "[Company Name] + [Your Company]"
  target_go_live: "[Date]"
  
  steps:
    - step: "Technical deep-dive with engineering team"
      owner: "[Prospect technical contact]"
      date: "[Date]"
      status: pending
      
    - step: "Security review / questionnaire"
      owner: "[You — send completed questionnaire]"
      date: "[Date]"
      status: pending
      
    - step: "Business case presentation to [Economic Buyer]"
      owner: "[Champion + You]"
      date: "[Date]"
      status: pending
      
    - step: "Proposal / pricing review"
      owner: "[You]"
      date: "[Date]"
      status: pending
      
    - step: "Legal / contract review"
      owner: "[Prospect legal]"
      date: "[Date]"
      status: pending
      
    - step: "Signature"
      owner: "[Economic Buyer]"
      date: "[Date]"
      status: pending
      
    - step: "Kickoff call"
      owner: "[Your CS team]"
      date: "[Date]"
      status: pending
```

**为什么MAP有效：**共同承担责任，明确时间表。关键决策者可以利用这份文档推动内部进展。当讨论陷入僵局时，你可以参考这份文档。

---

## 第五阶段：处理客户异议

**LAER框架**

每个异议都遵循以下模式：

1. **倾听**——让他们把话说完，不要打断，点头表示理解。
2. **确认**——“这是一个合理的担忧” / “我明白了”（不要说“我理解但是……”）
3. **深入探究**——“请帮我弄清楚——这是[具体问题]，还是更普遍的问题？”（诊断真正的异议）
4. **回应**——针对真正的担忧进行回应，而不仅仅是表面的问题。

### 处理不同类型异议的策略

**价格异议：**

| 异议 | 真实含义 | 回应 |
|-----------|-------------|----------|
| “太贵了” | 他们还没有看到产品的价值 | “与什么相比？请告诉我您所衡量的标准是什么？”然后重新强调不采取行动的后果。 |
| “能打折吗？” | 测试你的信心 | “我们的定价反映了我们提供的价值。[公司X]获得了[Y]的结果，投资回报是[Z]倍。您觉得哪里不对吗？” |
| “我们没有预算” | 要么他们不是决策者，要么他们不是优先考虑的对象 | “这是时间问题，还是[问题]在这个季度不是优先事项？”如果是优先事项：“预算重新安排后，我们可以计划一下吗？” |
| “竞争对手的价格更便宜” | 他们可能在利用你压价，或者他们真的对价格敏感 | “他们可能确实如此。问题是[缺失的功能]在12个月内会让他们花费多少成本？我可以帮您计算一下。” |

**时间异议：**

| 异议 | 真实含义 | 回应 |
|-----------|-------------|----------|
| “现在不行，也许下个季度吧” | 没有紧迫感 | “下个季度情况会怎样变化？如果[问题]每个月花费[X]，那么到下个季度会变成[3X]。” |
| “我们正在做另一个项目” | 真正忙，或者是在拖延 | “完全理解。[项目]什么时候结束？我们现在就确定一个时间吧。” |
| “我们需要考虑一下” | 他们还没有表达出真正的担忧 | “当然可以。您具体需要考虑什么？我现在就可以帮忙解决。” |

**权限异议：**

| 异议 | 真实含义 | 回应 |
|-----------|-------------|----------|
| “我需要跟我的老板商量” | 你没有直接与决策者沟通 | “当然可以。他们最关心的问题是什么？我们一起准备一下。”然后问：“如果我参与讨论会有帮助吗？” |
| “我们的委员会需要决定” | 这是一个涉及多个决策者的决策 | “委员会里有哪些人？每个人最关心什么？让我们确保提案能满足他们的需求。” |

**现状异议：**

| 异议 | 真实含义 | 回应 |
|-----------|-------------|----------|
| “我们现有的方案就很好” | 害怕改变大于对改进的渴望 | “您使用这个方案已经有多久了？从那以后您的业务发生了什么变化？我接触的大多数公司在达到[他们的增长阶段]时都会更换方案。” |
| “我们自己开发的” | 对内部解决方案感到自豪 | “这很棒。但是维护成本是多少？我接触的团队中，大多数工程师把[X]%的时间都花在维护上，而不是开发新功能。” |

**“反向质疑”技巧**

**当客户不断提出异议时，可以这样回应：**
> “听起来这个方案可能不适合您。我们是不是应该直接结束这次讨论？”
这样做有两个效果：
1. 减轻他们的压力——他们就不会再辩解了。
2. 迫使他们要么同意（你节省了时间），要么自己说服自己这个方案确实适合他们。

---

## 第六阶段：成交与谈判

### 何时提出成交请求

**口头表达：**
- “实施过程会是怎样的？”
- “价格是多少？”
- “我们可以做一次试用吗？”
- “合同的有效期是多久？”
- “我们什么时候可以开始？”

**行为表现：**
- 他们向你介绍其他相关方
- 他们请求推荐人
- 他们分享内部文件或需求
- 回应速度加快
- 他们开始使用“我们”和“什么时候”这样的表达

### 成交技巧

**1. 总结式成交法**
```
"So to recap — [problem] is costing you [X/month], you need a solution 
by [date] for [reason], and [your product] addresses [their top 3 criteria]. 
Shall I send the agreement?"
```

**2. 下一步行动法**
```
"Based on everything we've discussed, the next step would be 
[specific action — contract review, pilot setup, intro to CS]. 
Should I kick that off?"
```

**3. 假设成交法**
```
"Great — I'll have the proposal over by end of day. 
Would you prefer monthly or annual billing?"
```

**4. 对犹豫不决的客户的成交策略**
```
"Tell you what — let's do a 14-day pilot with [specific use case]. 
You'll see [expected result] in the first week. 
If it doesn't deliver, no hard feelings. Fair?"
```

### 谈判规则**

1. **永远不要对自己不利地谈判。**如果他们要求打折，询问他们愿意放弃什么（比如更长的试用期、提供案例研究、推荐人、更快签署合同等）。
2. **要有所交换，不要轻易让步。**每次让步都必须得到相应的回报。
3. **从较高的价格开始谈判。**先提出你的最高价格，这会设定谈判的范围。
4. **沉默就是力量。**说出价格后，停止讲话，让他们先回应。
5. **明确你的底线。**在谈判之前，先设定你的最低价格。低于这个价格就放弃交易。
6. **提供附加价值，而不是直接降价。**可以提供一个月的免费试用期、额外培训或高级支持，但不要直接降价。
7. **设定截止日期。**“这个价格的有效期限是[日期]”或“这个季度我还有两个培训名额。”

### 折扣决策树
```
Prospect asks for discount
├── Do they have budget? 
│   ├── YES → Don't discount. Anchor to value.
│   └── NO → Is the deal strategic (logo, case study, expansion potential)?
│       ├── YES → Offer trade: discount for [annual commit / case study / referral]
│       └── NO → Walk away or defer to next quarter
├── Is this a competitive situation?
│   ├── YES → Don't discount on price. Win on value + risk reduction.
│   └── NO → They're testing. Hold firm. "Our pricing reflects..."
└── Final rule: NEVER discount more than 20% on any deal. 
    Below that, you're training them to negotiate hard every renewal.
```

---

## 第七阶段：销售流程管理

### 销售流程阶段与退出标准

| 阶段 | 定义 | 退出标准 | 成交概率 |
|-------|-----------|---------------|-------------|
| **潜在客户开发** | 初始联系，尚未安排会议 | 会议已经安排 | 5% |
| **深入挖掘** | 第一次会议已经举行 | 痛点得到确认，客户符合ICP标准 | 15% |
| **评估** | 正在评估中，已经进行了产品演示 | 确定了关键决策者，了解了决策标准 | 30% |
**提案阶段** | 提案或价格已经发送 | 预算已经确定，决策流程已经明确 | 50% |
| **谈判阶段** | 正在讨论条款 | 客户已经口头同意，法律或采购流程已经开始 | 75% |
| **成交阶段** | 合同已经签署 | ✅ 收入已经确认 | 100% |
| **失败阶段** | 交易失败 | 记录失败原因，确定下一步行动 | 0% |

**阶段管理规则：**
- 任何交易在一个阶段停留的时间不得超过该阶段平均时间的两倍。
- 每个交易都必须有明确的下一步行动和时间安排。
- 如果一个交易14天内没有任何进展，就需要重新评估。
- 根据客户的行动来更新销售流程的阶段，而不是根据你的行动（你发送提案并不意味着交易进入了下一个阶段）。

### 每周销售流程回顾模板
```yaml
pipeline_review:
  date: "[YYYY-MM-DD]"
  
  summary:
    total_pipeline: "$[X]"
    weighted_pipeline: "$[X]"
    new_this_week: [X deals, $Y]
    advanced_this_week: [X deals moved forward]
    closed_won: [X deals, $Y]
    closed_lost: [X deals, $Y — reasons]
    slipped: [X deals pushed from this month]
    
  deals_to_review:  # Top 10 by size
    - company: "[Name]"
      value: "$[X]"
      stage: "[Stage]"
      age_in_stage: "[X days]"
      next_step: "[Action]"
      risk: "[red/yellow/green]"
      risk_reason: "[Why]"
      
  actions:
    - "[Deal]: [Specific action to take this week]"
    
  pipeline_health:
    coverage_ratio: "[X]x"  # Pipeline / Quota — target 3-4x
    avg_deal_size: "$[X]"
    avg_sales_cycle: "[X days]"
    win_rate: "[X%]"
    stage_conversion:
      discovery_to_eval: "[X%]"
      eval_to_proposal: "[X%]"
      proposal_to_closed: "[X%]"
```

### 预测分类

| 分类 | 定义 | 规则 |
|----------|-----------|-------|
| **肯定会成交** | 在这个周期内一定会成交 | 客户已经口头同意，合同已经签订，没有障碍 |
| **最佳情况** | 在这个周期内有很高的成交可能性 | 关键决策者正在推动，决策流程正在进行中，存在一定的风险 |
| **待成交** | 可能在这个周期内成交，但还需要进一步工作 | 处在评估阶段，尚未进入提案阶段 |
| **可能性较低** | 在这个周期内成交的可能性较小，但仍有机会 | 处在早期阶段，客户符合ICP标准，但时间表不确定 |

**预测准确性规则：**你的预测成交数量应该与实际成交数量相差不超过10%。如果预测持续偏离实际情况，说明你的客户评估方法有问题。**

---

## 第八阶段：加速交易进程的策略

### 当交易陷入僵局时的诊断检查清单
```
Deal is stalled. Ask yourself:

1. [ ] Do I have a champion? (If no → find one or walk away)
2. [ ] Have I talked to the economic buyer? (If no → get access)
3. [ ] Is there a compelling event / deadline? (If no → create urgency)
4. [ ] Do they understand the cost of doing nothing? (If no → quantify it)
5. [ ] Are there unresolved objections? (If yes → LAER them)
6. [ ] Is there a competitor blocking? (If yes → differentiate or reframe)
7. [ ] Is my champion still engaged? (If no → re-engage with new value)
8. [ ] Have I multi-threaded? (If no → engage other stakeholders)
```

### 多线程销售策略

**规则：**在任何交易中，不能只依赖一个联系人。如果你的关键决策者离开、生病或休假，交易就很可能会失败。

**根据交易金额确定最低联系人数量：**
- 交易金额<25,000美元 → 2名联系人（关键决策者 + 经济买家）
- 25,000美元至100,000美元 → 3-4名联系人（关键决策者、经济买家、技术评估员、最终用户）
- 100,000美元以上 → 5名以上联系人（增加采购人员、法律人员、高层支持人员）

### 创造紧迫感的策略（道德原则）

| 方法 | 方法 | 适用情况 |
|-----------|-----|-------------|
| **延迟的成本** | “如果这个问题不解决，每个月会让你损失[X]美元。到下个季度这个损失会变成[X]美元。” | 当他们没有明确的时间表时使用 |
| **资源限制** | “这个季度我们要接待3位新客户。之后下一个接待时间就是[日期]。” | 当情况属实时使用（切勿撒谎） |
| **价格时间限制** | “当前价格的有效期限是[日期]。** | 当价格有变动时使用 |
| **竞争对手的威胁** | “你的竞争对手[公司名称]刚刚与我们签约。” | 当这种情况属实且相关时使用 |
| **法规截止日期** | “[法规]将在[日期]生效。你需要[X]周的时间来准备。” | 当合规性是一个问题时使用 |

## 第九阶段：售后与业务扩展

### 与客户成功团队的交接
```yaml
deal_handoff:
  company: "[Name]"
  closed_date: "[Date]"
  contract_value: "$[X] / [term]"
  
  key_contacts:
    - name: "[Champion]"
      role: "[Title]"
      communication_preference: "[email/slack/phone]"
      personality: "[detail-oriented/big picture/hands-on]"
      
    - name: "[Executive Sponsor]"
      role: "[Title]"
      engagement_level: "[high/medium/low]"
      success_metrics: "[What they told you success looks like]"
      
  context:
    pain_points_solved: "[List from discovery]"
    promised_outcomes: "[Specific commitments made during sales]"
    known_risks: "[Anything that could cause churn]"
    expansion_opportunity: "[What else they could buy]"
    competitor_considered: "[Who else they evaluated and why they chose you]"
    
  implementation:
    priority_use_cases: "[What to set up first]"
    technical_requirements: "[Integrations, SSO, data migration]"
    timeline_expectations: "[What you committed to]"
    
  DO_NOT:
    - "[Any sensitive topics to avoid]"
    - "[Things that were contentious during sales]"
```

### 业务扩展策略

**何时进行追加销售：**
- 客户的使用量达到当前等级/上限的80%以上 |
- 客户询问更高级别的功能 |
- 新团队或部门希望加入 |
- 客户达到某个里程碑（例如团队规模扩大、进入新市场）

**扩展销售时的注意事项：**
```
"I noticed [specific usage signal]. That usually means [outcome they care about] 
is going well. 

Other companies at your stage typically [expand to X / add Y] to [benefit].
Would it make sense to explore that?"
```

**何时不应进行追加销售：**
- 客户仍有未解决的支持问题 |
- 在交易后的前60天内 |
- 客户处于流失风险中 |
- 没有数据表明客户会从扩展服务中获益 |

## 第十阶段：指标与自我改进

### 活动指标（领先指标）

| 指标 | 目标值 | 重要性 |
|--------|--------|---------------|
| 每天发送的邮件数量 | 30-50封 | 用于生成销售线索 |
| 每天拨打的电话数量 | 15-25通 | 用于生成销售线索 |
| 每周安排的会议数量 | 8-12次 | 用于转化销售线索 |
| 每周进行的挖掘电话数量 | 5-8次 | 用于评估潜在客户 |
| 每周发送的提案数量 | 2-3份 | 用于促成成交 |
| 每周进行的演示数量 | 3-5次 | 用于推进销售流程 |

### 结果指标（滞后指标）

| 指标 | 计算公式 | 合理范围 |
|--------|---------|---------------|
| 成交率 | 成交数量 / （成交数量 + 失败数量） | 20-35% |
| 平均交易金额 | 总收入 / 成交数量 | 趋势上升 |
| 销售周期 | 从首次联系到成交的平均时间 | 趋势下降 |
| 销售线索转化率 | 开启的销售线索数量 / 总销售线索数量 | >50% |
| 会议数量与销售线索的比例 | 开启的销售线索数量 / （发送的邮件数量 + 打电话的数量） | >50% |
| 会议数量与潜在客户数量的比例 | 潜在客户数量 / 会议数量 | >50% |
| 预测准确性 | 实际成交数量 / 预测成交数量 | >90% |

### 成交/失败分析模板
```yaml
deal_analysis:
  company: "[Name]"
  outcome: "[Won/Lost]"
  value: "$[X]"
  cycle_length: "[X days]"
  
  won_because:  # or lost_because
    - "[Primary reason]"
    - "[Secondary reason]"
    
  competitor: "[Who they went with / considered]"
  
  what_worked:
    - "[Specific thing that moved the deal forward]"
    
  what_didnt:
    - "[Specific mistake or gap]"
    
  lesson:
    - "[What to do differently next time]"
    
  process_score:  # Self-assessment
    prospecting: [1-5]
    discovery: [1-5]
    demo: [1-5]
    objection_handling: [1-5]
    closing: [1-5]
    relationship: [1-5]
```

### 每月自我评估问题

1. 我的成交率趋势如何？（是在提高、持平还是下降？）
2. 交易失败的主要原因在哪里？（哪个阶段的问题导致失败率最高？）
3. 我是否在联系正确的人？（我联系的对象是否是决策者？）
4. 我的交易金额是在增加还是减少？ |
5. 我在处理哪种类型的异议时最薄弱？ |
6. 哪种销售渠道的转化效果最好？ |
7. 我是否在把时间花在正确的客户上？（80%的交易是否来自20%的有效客户？）
8. 从上一次失败中我学到了什么？ |

---

## 自动化命令

| 命令 | 功能 |
|---------|-------------|
| “生成我的理想客户画像” | 根据ICP定义模板生成客户画像 |
| “为[公司]生成销售流程” | 根据已知信息生成个性化的多渠道销售流程 |
| “为[公司]准备挖掘阶段所需的问题” | 根据客户情况生成相应的挖掘问题 |
| “评估这个交易是否符合标准” | 使用MEDDPICC评估框架进行评估 |
| “帮助我处理这个异议” | 提供相关的应对策略和练习机会 |
| “查看我的销售流程” | 生成每周的销售流程回顾报告 |
| “分析我为什么失败” | 对最近的失败案例进行成交/失败分析 |
| “预测这个季度的成交情况” | 将交易分类为肯定会成交、最佳情况、待成交或可能性较低的情况 |
| “为[公司]准备提案” | 根据挖掘结果生成提案 |
| “在[会议类型]后发送跟进邮件” | 根据会议内容生成合适的跟进邮件 |
| “指导我如何处理[会议记录/对话内容]” | 分析销售对话并提供反馈 |
| “指导我如何完成[公司的成交]” | 评估交易情况并推荐成交策略 |