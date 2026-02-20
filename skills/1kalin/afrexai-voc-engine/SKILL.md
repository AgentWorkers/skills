---
name: afrexai-voc-engine
description: 完整的“客户之声”（Voice of Customer, VoC）系统——能够大规模地收集、分析并利用客户反馈。该系统涵盖了净推荐值（Net Promoter Score, NPS）、客户满意度（Customer Satisfaction Score, CSAT）、客户体验（Customer Experience Score, CES）的测量方法、客户访谈流程、反馈分类体系、功能请求的优先级排序、情感分析、闭环工作流程，以及基于客户反馈的产品决策机制。适用于构建反馈系统、开展客户访谈、评估客户满意度、分析功能请求、降低客户流失率（churn）或完善反馈循环等场景。相关关键词包括：“客户反馈”（customer feedback）、“客户之声”（voice of customer）、“净推荐值”（NPS）、“客户满意度”（CSAT）、“客户体验得分”（CES）、“功能请求”（feature requests）、“反馈系统”（feedback system）、“客户访谈”（customer interviews）、“满意度调查”（satisfaction survey）、“客户流失分析”（churn analysis）。
---
# 客户之声（VoC）引擎

这是一个完整的系统，用于收集、分析并利用客户反馈，以推动产品决策、降低客户流失率并增加收入。

---

## 第一阶段：VoC项目设计

### 项目简介

```yaml
voc_program:
  company: "[Company Name]"
  product: "[Product/Service]"
  stage: "[Pre-PMF | Growth | Scale | Enterprise]"
  customer_count: "[approximate]"
  current_nps: "[score or unknown]"
  current_churn: "[monthly % or unknown]"
  primary_goal: "[reduce churn | improve NPS | prioritize roadmap | find PMF]"
  
  segments:
    - name: "[Enterprise / SMB / Consumer]"
      size: "[count]"
      arr_contribution: "[%]"
      priority: "[1-3]"
    
  existing_channels:
    - "[list current feedback collection methods]"
  
  gaps:
    - "[what feedback are you NOT collecting?]"
```

### VoC成熟度评估

对您当前的项目进行评分（每个维度1-5分）：

| 维度 | 1（临时性） | 3（结构化） | 5（已制度化） |
|-----------|-----------|----------------|---------------------|
| **收集** | 零星、被动响应 | 多渠道、有一定规律性 | 自动化、多渠道、触发式收集 |
| **分析** | 仅阅读个别评论 | 标记和分类 | 定量分析主题、跟踪趋势 |
| **分发** | 仅限于支持团队 | 在会议中分享 | 实时仪表盘、自动路由 |
| **行动** | 偶尔修复问题 | 每季度提供输入 | 闭环管理，反馈驱动决策 |
| **衡量** | 无跟踪 | 无NPS或CSAT数据 | 全套指标、有基准测试 |

**评分说明：**
- 5-10分：需要基础建设——从第二阶段开始 |
- 11-18分：正在发展中——重点关注分析和分发 |
- 19-25分：已成熟——优化闭环管理和投资回报率（ROI）跟踪 |

---

## 第二阶段：反馈收集架构

### 渠道策略

围绕客户旅程设计反馈收集方式：

```yaml
collection_channels:
  # ALWAYS-ON (continuous)
  in_app_widget:
    placement: "[specific screens/moments]"
    trigger: "User-initiated (feedback button)"
    format: "Open text + optional category selector"
    volume: "High"
    quality: "Medium (context-rich but brief)"
    
  support_tickets:
    source: "[Intercom / Zendesk / Help Scout / email]"
    tagging: "Auto-tag feedback themes (see taxonomy)"
    volume: "High"
    quality: "High (real problems, real context)"
    
  feature_request_board:
    tool: "[Canny / ProductBoard / custom]"
    voting: true
    status_updates: true  # Close the loop!
    volume: "Medium"
    quality: "High (considered requests)"

  # PERIODIC (scheduled)
  nps_survey:
    frequency: "Quarterly"
    trigger: "Email to active users (>30 days tenure)"
    follow_up: "Open text for score explanation"
    segments: "[by plan tier, tenure, usage level]"
    
  csat_survey:
    trigger: "After key interactions (onboarding complete, support resolved, feature shipped)"
    format: "1-5 stars + optional comment"
    
  ces_survey:
    trigger: "After task completion (setup, first report, integration)"
    question: "How easy was it to [specific task]? (1-7)"
    
  # EVENT-DRIVEN (triggered)
  onboarding_check_in:
    trigger: "Day 7, Day 30, Day 90"
    format: "Short email survey (3 questions max)"
    
  cancellation_survey:
    trigger: "On churn/downgrade"
    format: "Required reason + optional comment"
    options:
      - "Too expensive"
      - "Missing features I need"
      - "Too complex / hard to use"
      - "Switched to competitor"
      - "No longer need this type of product"
      - "Poor support experience"
      - "Other: [free text]"
    
  win_loss_interview:
    trigger: "After closed-won or closed-lost deal"
    format: "15-min call or async survey"
    
  renewal_feedback:
    trigger: "30 days before renewal"
    format: "Health check + satisfaction + roadmap preview"
```

### 调查设计规则

1. **每份调查最多3个问题**（每增加一个问题，响应率下降20%）
2. **至少包含一个量化指标问题和一个开放性问题** |
3. **时机很重要**：在触发事件发生后的24小时内发送 |
4. **优先考虑移动端**：设计便于滑动浏览的调查问卷 |
5. **避免在客户情绪不佳时进行调查**：在负面支持体验后等待48小时 |
6. **频率限制**：每个用户每季度最多被调查一次（特殊事件除外） |
7. **务必解释原因**：使用“帮助我们改进[具体问题]”而非“请填写调查问卷” |

### 样本量计算器

| 客户基数 | 95%置信度，±5% | 90%置信度，±5% | 最小样本量 |
|--------------|---------------------|---------------------|----------------|
| 100 | 80 | 74 | 30 |
| 500 | 217 | 176 | 50 |
| 1,000 | 278 | 213 | 75 |
| 5,000 | 357 | 258 | 100 |
| 10,000+ | 370 | 264 | 150 |

**各渠道的预期响应率：**
- 应用内：10-15% |
- 电子邮件NPS：20-40% |
- 支持服务后的CSAT：15-25% |
- 客户流失调查：30-50%（建议至少80%的受访者参与） |

---

## 第三阶段：客户访谈方法

### 访谈类型

| 类型 | 时间 | 时长 | 样本量 | 目的 |
|------|------|----------|--------|------|
| **问题发现** | 在产品开发前 | 45-60分钟 | 8-12人 | 验证问题是否存在 |
| **可用性** | 在功能开发期间 | 30-45分钟 | 5-7人 | 测试假设 |
| **满意度** | 每季度进行 | 30分钟 | 每个群体5-8人 | 深度定性NPS调查 |
| **流失原因** | 客户取消服务后 | 15-20分钟 | 所有愿意参与的人 |
| **成交后** | 交易完成后 | 20-30分钟 | 每季度5人以上 | 收集销售流程反馈 |
| **战略咨询** | 每季度进行 | 60分钟 | 3-5位高级用户 | 共同制定产品路线图 |

### 访谈指南模板

```yaml
interview:
  type: "[Discovery / Satisfaction / Churn / Win-Loss]"
  participant: "[name, role, company, segment]"
  date: "[YYYY-MM-DD]"
  interviewer: "[name]"
  
  pre_interview:
    - Review account history (usage data, support tickets, NPS scores)
    - Check CRM for relationship context
    - Prepare 3 hypotheses to test
    
  warm_up: # 3-5 min
    - "Tell me about your role and what a typical week looks like."
    - "How long have you been using [product]?"
    - "[Acknowledge something specific about their usage]"
    
  context: # 5-10 min  
    - "What problem were you trying to solve when you found us?"
    - "What were you using before? What worked/didn't?"
    - "Walk me through how [product] fits into your workflow."
    
  core_exploration: # 15-20 min
    - "Walk me through the last time you used [specific feature]."
    - "What's the most valuable thing [product] does for you?"
    - "What's the most frustrating thing?"
    - "Tell me about a time [product] didn't work the way you expected."
    - "What workaround have you built because we're missing something?"
    
  outcome_assessment: # 5-10 min
    - "How do you measure the value you get from [product]?"
    - "What would happen if you lost access tomorrow?"
    - "On a scale of 1-10, how likely would you recommend us? Why that number?"
    
  future_vision: # 5 min
    - "If you had a magic wand, what would [product] do that it doesn't today?"
    - "What's changing in your world that we should know about?"
    
  close: # 2 min
    - "Anything I didn't ask that I should have?"
    - "Would you be open to joining our advisory group / beta testing?"
    - Thank + follow-up timeline
    
  post_interview:
    key_quotes: []
    surprises: []
    hypotheses_confirmed: []
    hypotheses_invalidated: []
    action_items: []
```

### 访谈技巧

**“妈妈测试”（Rob Fitzpatrick）：**
- 与客户谈论他们的生活，而不是你的想法 |
- 询问过去的实际情况，而非假设性问题 |
- 少说多听 |
- 错误做法：“你会使用具有X功能的产品吗？”（客户可能会出于礼貌回答“会”）
- 正确做法：“请告诉我你上次尝试使用X功能时的情况。”

**五问法（探究根本原因）：**
1. “这很令人沮丧。为什么这对你来说是个问题？” |
2. “这对你的工作有什么影响？” |
3. “如果这个问题发生，会怎样？” |
4. “你为什么无法解决它？” |
5. “如果我们解决了这个问题，什么会改变？” |

**沉默技巧：** 在客户回答后默默数到5。他们通常会在沉默中提供最有价值的见解。 |

### 访谈总结模板

每完成5次访谈后，进行总结：

```yaml
synthesis:
  batch: "[Interview batch name]"
  dates: "[range]"
  participants: "[count, segments]"
  
  themes:
    - theme: "[Name]"
      frequency: "[X of Y participants mentioned]"
      severity: "[Critical / High / Medium / Low]"
      representative_quotes:
        - "[exact quote]" — [participant type]
        - "[exact quote]" — [participant type]
      implications: "[what this means for product/business]"
      recommended_action: "[specific next step]"
      
  surprises:
    - "[Things you didn't expect]"
    
  segments_divergence:
    - "[Where different segments disagreed]"
    
  confidence_level: "[High / Medium / Low]"
  next_steps: []
```

---

## 第四阶段：反馈分类与归类

### 类别层次结构

```yaml
feedback_taxonomy:
  product:
    usability:
      - "Confusing UI / navigation"
      - "Feature hard to find"
      - "Too many steps to complete task"
      - "Mobile experience issues"
    functionality:
      - "Feature doesn't work as expected"
      - "Missing capability"
      - "Performance / speed"
      - "Integration issues"
    reliability:
      - "Bugs / errors"
      - "Data loss / corruption"
      - "Downtime / availability"
      
  experience:
    onboarding:
      - "Setup too complex"
      - "Documentation unclear"
      - "Time to value too long"
    support:
      - "Response time"
      - "Resolution quality"
      - "Self-service gaps"
    communication:
      - "Product updates unclear"
      - "Billing confusion"
      - "Status page / transparency"
      
  value:
    pricing:
      - "Too expensive"
      - "Wrong packaging / tiers"
      - "Hidden costs"
      - "Competitor cheaper"
    roi:
      - "Can't measure value"
      - "Not delivering promised results"
      - "Value decreased over time"
      
  strategic:
    market_fit:
      - "Wrong audience"
      - "Use case mismatch"
      - "Outgrew the product"
    competitive:
      - "Competitor has feature X"
      - "Switching to competitor"
      - "Industry trend we're missing"
```

### 情感评分

对每条反馈进行评分：

| 维度 | 分数范围 | 评分标准 |
|-----------|-------|-------|
| **情感** | -2至+2 | -2=愤怒，-1=沮丧，0=中立，+1=积极，+2=非常满意 |
| **紧急性** | 1-5 | 1=次要，3=重要，5=严重影响客户流失 |
| **提及频率** | 计数 | 有多少独特客户提到该问题 |
| **潜在收入影响** | （金额） | 提及该问题的客户的年收入（ARR） |
| **修复难度** | 低/中/高/非常困难 | 工程团队估计的修复难度 |

### 自动标签规则

在处理反馈时，自动应用标签：

```
IF contains("cancel", "churn", "leaving", "switching") → tag: churn_risk, urgency: 5
IF contains("bug", "error", "broken", "crash") → tag: bug_report, urgency: 4
IF contains("wish", "would be nice", "if only") → tag: feature_request, urgency: 2
IF contains("love", "amazing", "best") → tag: positive_signal, sentiment: +2
IF contains("competitor", "alternative", "other tool") → tag: competitive_intel
IF contains("price", "cost", "expensive", "cheaper") → tag: pricing_feedback
IF contains("confusing", "hard to", "can't figure") → tag: usability_issue, urgency: 3
```

---

## 第五阶段：指标体系

### NPS（净推荐值）

**问题：“你有多可能向同事推荐[产品]？”（0-10分）

**评分标准：**
- 0-6分：贬低者 |
- 7-8分：中立者 |
- 9-10分：推荐者 |
**NPS = （推荐者比例 - 贬低者比例）× 100%**

**行业基准：**
| 行业 | 较差 | 平均 | 良好 | 优秀 |
|----------|------|---------|------|-----------|
| SaaS B2B | <20% | 20-40% | 40-60% | 60%以上 |
| SaaS B2C | <10% | 10-30% | 30-50% | 50%以上 |
| 电子商务 | <20% | 20-40% | 40-60% | 60%以上 |
| 金融服务 | <10% | 10-30% | 30-50% | 50%以上 |
| 医疗科技 | <15% | 15-35% | 35-55% | 55%以上 |

**NPS后续问题（根据评分）：**
- 贬低者（0-6分）：“很遗憾听到这样的反馈。我们最需要改进什么？” |
- 中立者（7-8分）：“需要什么才能让我们的评分达到9或10分？” |
- 推荐者（9-10分）：“太好了！您最看重我们的哪些方面？”

**NPS行动规则：**
- 如果评分季度间下降超过10分，立即调查 |
- 来自企业客户的贬低者反馈，24小时内通知客户关系经理（CSM） |
- 推荐者反馈，7天内触发推荐/反馈收集/案例研究请求 |

### CSAT（客户满意度）

**问题：“您对[具体服务/产品]的满意度如何？”（1-5分）**

**评分标准：**（满意回答占比[4-5] / 总回答数）× 100%

**使用场景：** 在特定服务/产品使用后进行调查

### CES（客户努力度）

**问题：“完成[具体任务]的难度如何？”（1-7分，1=非常困难，7=非常容易）**

**评分标准：** 所有回答的平均值

**CES的重要性：** CES是预测客户未来购买行为的最强指标。高努力度的体验会导致96%的客户流失。

### 综合健康评分

结合各项指标评估VoC系统的整体健康状况：

```yaml
voc_health_score:
  nps:
    weight: 30
    score: "[0-100 normalized: (NPS + 100) / 2]"
  csat:
    weight: 20
    score: "[CSAT %]"
  ces:
    weight: 15
    score: "[(CES / 7) × 100]"
  feedback_volume:
    weight: 10
    score: "[trend: increasing = good]"
  response_rate:
    weight: 10
    score: "[survey response rate %]"
  closed_loop_rate:
    weight: 15
    score: "[% of feedback items with documented response/action]"
    
  total: "[weighted sum / 100]"
  grade: "[A: 80+, B: 65-79, C: 50-64, D: 35-49, F: <35]"
```

---

## 第六阶段：功能需求优先级排序

### RICE + VoC框架

对每个功能需求进行评分：

| 因素 | 计算公式 | 权重 |
|--------|---------|--------|
| **覆盖范围** | 每季度提出该需求的客户数量 | 25% |
| **影响** | 评分0.5（低），1（中等），2（高） | 25% |
| **可信度** | 对预估的信心程度（50-100%） | 20% |
| **开发难度** | 需要的人周数 | 15% |
| **收入影响** | 受影响客户的年收入（ARR） | 15% |

**RICE-V评分 = （覆盖范围 × 影响 × 可信度 × 收入影响） / 开发难度**

### 优先级决策树

```
1. Is this blocking revenue? (churn risk from top accounts)
   → YES: Fast-track (Sprint 1)
   → NO: Continue ↓

2. Does it affect >20% of customers?
   → YES: High priority (next quarter)
   → NO: Continue ↓

3. Is it from a strategic segment we're targeting?
   → YES: Medium-high priority
   → NO: Continue ↓

4. Does it align with product vision?
   → YES: Backlog with planned quarter
   → NO: Decline with explanation (close the loop!)
```

### 拒绝请求的流程

并非所有功能需求都应被实现。优雅地拒绝客户：

**模板：“感谢您的建议！我们已经收到[X]位客户的类似反馈。目前我们的产品路线图专注于[特定主题]，因为[原因]。我们计划在[时间范围]内不开发这个功能，但已将其记录下来。以下是我们正在开发的可能相关功能：[替代方案]。如果我们的计划发生变化，会更新此请求。”**

**拒绝的时机：**
- 该需求仅影响不到5%的客户 |
- 与产品愿景相冲突 |
- 通过集成或合作伙伴能更好地解决问题 |
- 功能与客户需求的成本效益比不佳 |
- 客户更适合使用其他产品 |

---

## 第七阶段：闭环工作流程

### 反馈循环（四个阶段）

```
COLLECT → ANALYZE → ACT → COMMUNICATE
    ↑                              |
    └──────────────────────────────┘
```

### 闭环响应模板

**感谢反馈（24小时内）：**
“感谢您分享这些反馈。我们已将其归类为[类别]，目前正由[产品/工程团队]审核。我们会及时告知您处理结果。”

**处理中：**
“关于[具体主题]的反馈更新——我们正在积极处理中，预计完成时间[时间范围]。以下是改进内容：[简要描述]。”

**已处理：**
“还记得您之前提到的[原始反馈]吗？我们已经修复了问题！以下是具体改进内容：[具体改进措施]。请试用后告诉我们您的感受。”

**拒绝反馈（参见上述“拒绝请求”模板）**

### 不同类型反馈的响应时间表

| 类型 | 感谢反馈 | 分类处理 | 解决/回复时间 |
|------|------------|--------|-----------------|
| 错误报告 | 4小时 | 24小时 | 根据严重程度 |
| 功能需求 | 48小时 | 1周 | 每季度审核 |
| 抱怨 | 4小时 | 24小时 | 72小时 |
| 赞扬 | 24小时 | 不适用 | 内部分享 |
| 客户流失反馈 | 24小时 | 48小时 | 1周 |
| NPS贬低者反馈 | 24小时 | 48小时 | 1周 |

### 闭环跟踪

```yaml
feedback_item:
  id: "FB-[YYYY]-[####]"
  source: "[channel]"
  customer: "[name, segment, ARR]"
  date_received: "[YYYY-MM-DD]"
  category: "[from taxonomy]"
  sentiment: "[-2 to +2]"
  urgency: "[1-5]"
  
  status: "[New | Acknowledged | Triaging | In Progress | Shipped | Declined | Won't Fix]"
  assigned_to: "[team/person]"
  
  date_acknowledged: "[YYYY-MM-DD]"
  date_resolved: "[YYYY-MM-DD]"
  resolution: "[what was done]"
  customer_notified: "[yes/no + date]"
  customer_satisfied: "[yes/no/unknown]"
  
  linked_items:
    jira: "[ticket ID]"
    roadmap: "[feature/initiative]"
    other_feedback: "[related FB IDs]"
```

---

## 第八阶段：VoC报告与仪表盘

### 每周VoC总结

```yaml
weekly_voc:
  period: "[week of YYYY-MM-DD]"
  
  volume:
    total_feedback: "[count]"
    by_channel:
      support: "[count]"
      in_app: "[count]"
      surveys: "[count]"
      interviews: "[count]"
    trend: "[↑/↓/→ vs last week]"
    
  metrics:
    nps: "[score] ([↑/↓] [X] from last period)"
    csat: "[%] ([↑/↓] [X]%)"
    ces: "[score] ([↑/↓])"
    
  top_themes:
    - theme: "[#1 theme]"
      mentions: "[count]"
      sentiment: "[avg]"
      revenue_at_risk: "[$]"
      action: "[what we're doing]"
    - theme: "[#2]"
      # ...
    - theme: "[#3]"
      # ...
      
  alerts:
    - "[Enterprise detractor: Company X, NPS dropped from 8 to 3]"
    - "[New theme emerging: Y mentioned by 5 customers this week]"
    
  closed_loop:
    items_received: "[count]"
    items_acknowledged: "[count] ([%])"
    items_resolved: "[count]"
    avg_resolution_time: "[days]"
    
  wins:
    - "[Positive feedback / testimonial / case study lead]"
```

### 每月VoC报告（供管理层参考）

**报告结构：**
1. **执行摘要** — 三个关键指标（NPS趋势、主要风险、主要机会）
2. **指标趋势** — NPS/CSAT/CES的月度及季度变化 |
3. **主题分析** — 最常见的5个主题及其频率、情感倾向、收入影响 |
4. **客户群体分析** — 不同客户群体的反馈模式 |
5. **竞争分析** | 客户对竞争对手的看法 |
6. **路线图对齐** | 反馈与当前产品路线图的对应关系 |
7. **行动事项** | 我们针对主要问题的应对措施 |
8. **闭环管理效果** | 已确认的反馈比例、解决比例、平均处理时间 |

### 每季度战略VoC评估

深入分析：
- **新客户群体**：他们的反馈模式是否不同？
- **客户群体分析**：哪些群体最满意/最不满意？
- **反馈高发环节**：在客户旅程的哪个环节反馈最多？
- **趋势分析**：哪些主题在增加/减少？
- **竞争态势**：我们在关键指标上是否领先/落后？
- **变更的ROI**：基于反馈做出的功能改进是否提升了指标？

---

## 第九阶段：基于VoC的产品决策

### 证据优先级排序

在做产品决策时，按以下优先级排序证据：

1. **行为数据**（客户实际行为）——使用情况分析、转化率、客户留存率 |
2. **客户真实需求**（他们愿意为哪些功能付费）——升级触发因素、定价实验 |
3. **定性访谈**（客户的深入反馈）——问题发现、满意度 |
4. **调查数据**（客户的反馈结果）——NPS、CSAT、功能需求 |
5. **支持问题**（客户的不满点） |
6. **功能需求**（客户明确提出的需求） |
7. **社交媒体/评论反馈**（客户对产品的评价） |

**决策规则：** 切勿仅依据第6-7类证据做出决策。务必结合第1-3类证据进行综合分析。

### 产品决策模板

```yaml
product_decision:
  what: "[Feature/change being considered]"
  
  voc_evidence:
    quantitative:
      customers_requesting: "[count]"
      arr_represented: "[$]"
      nps_impact: "[detractors mentioning this]"
      support_tickets: "[count related]"
    qualitative:
      interview_quotes:
        - "[quote]" — [segment]
      themes_connected: "[from taxonomy]"
    behavioral:
      usage_data: "[relevant metrics]"
      churn_correlation: "[if applicable]"
      
  decision: "[Build / Decline / Investigate further]"
  confidence: "[High / Medium / Low]"
  expected_impact:
    nps_change: "[estimated]"
    churn_reduction: "[estimated]"
    expansion_revenue: "[estimated]"
    
  success_metrics:
    - "[How we'll know this worked]"
  review_date: "[When to check impact]"
```

---

## 第十阶段：高级VoC策略

### 客户咨询委员会（CAB）

**组成：**
- 来自不同客户群体的8-12位客户 |
- 每季度召开90分钟会议 |
- 内容：60%讨论产品路线图，20%讨论行业趋势，20%建立合作关系 |
**激励措施：** 提前试用新功能、参与高层会议、对产品路线图有影响力 |

**选拔标准：**
- 代表目标客户群体 |
- 真正使用产品的用户（而非只是品牌代言人） |
- 能够提出建设性意见（而非单纯抱怨或盲目支持） |
- 使用场景多样化 |
- 愿意投入时间参与讨论 |

### 竞争对手反馈分析

当客户提到竞争对手时：

```yaml
competitive_mention:
  competitor: "[name]"
  context: "[switching to / comparing / switched from]"
  feature_gap: "[what competitor has that we don't]"
  our_advantage: "[what they like about us vs competitor]"
  customer_segment: "[type]"
  deal_size: "[$]"
  action: "[product response needed?]"
```

**季度跟踪：“竞争对手被提及的频率”——特定竞争对手被提及的次数增加可能预示着潜在问题。**

### 基于反馈的定价策略

客户反馈能揭示定价问题：

| 信号 | 含义 | 应对措施 |
|--------|---------|--------|
| “价格太高”（无具体原因） | 客户认为产品价值未体现 | 改进价值沟通 |
| “希望[功能X]包含在产品中” | 产品功能配置不合理 | 重新评估功能层级 |
| “竞争对手的产品更便宜” | 定价策略需要调整 | 进行竞争分析 |
| “我希望为[功能Y]支付更多费用” | 有扩展机会 | 测试高级功能或附加服务 |
| “不清楚自己购买的产品包含哪些功能” | 需明确产品价值 | 优化产品信息 |

### 多产品公司的VoC管理

如果公司有多个产品：
- 为每个产品单独统计NPS |
- 跨产品反馈分析：“希望[产品A]具备[产品B]的功能” |
- 统一客户反馈视图：汇总所有产品的反馈 |
- 跨产品销售线索：分析客户在不同产品间的反馈差异 |

### 产品上市前的VoC管理

对于客户数量少于50的公司：
- **每月与每位客户沟通**（20分钟） |
- **使用电子表格记录**：客户姓名、反馈内容、反馈主题、采取的措施 |
- **单一指标**：使用Sean Ellis测试法——“如果您不能再使用[产品A]，会有什么感受？”（如果超过40%的客户表示“非常失望”，则说明产品需要改进） |
- **每周更新反馈** | 保持紧密的反馈循环 |
- **无需进行大规模调查**：样本量太小 |

---

## 第十一阶段：特殊情况处理

### 负面反馈激增

- **不要恐慌**。检查原因：是偶发错误、系统变更还是普遍现象？
- **分类处理**：如果是个别客户的强烈反馈，还是多个客户的共同意见？
- **响应方式**：如果反馈在公开渠道（如社交媒体、评论区）被广泛传播，需公开回应；如果是技术问题，及时修复；如果是系统性问题，需解释变更原因。

### 反馈矛盾

- 不同客户群体有不同的需求：例如，A群体希望简单的产品，B群体希望功能强大 |
- **解决方式**：确定主要目标客户群体，为他们开发相应功能；为其他客户提供替代方案；考虑分层产品策略。

### 调查疲劳

- 如果响应率低于10%，说明客户可能对调查感到疲劳 |
- **调整策略**：减少调查频率、缩短调查时长、说明反馈的作用（例如“您提到的问题我们已经解决了”），并尝试更换调查渠道。

### 少数客户的强烈反馈

- 3位客户强烈要求某个功能，而300位客户实际使用另一个功能 |
- **决策原则**：不要仅依据投诉数量决策，要结合使用数据和收入数据综合考虑。

### 文化差异

- 不同地区的NPS评分可能有所不同（例如日本用户评分较低） |
- **调整策略**：根据地区差异调整评估标准。

### 免费用户的反馈

- 免费用户的反馈在优先级排序中的权重较低 |
- **但仍有价值**：有助于了解转化障碍、用户初始使用体验等问题 |
- **处理方式**：单独记录免费用户的反馈，重点关注可能影响转化的因素。

---

## 质量评估标准

对VoC系统的质量进行评分（0-100分）：

| 维度 | 权重 | 0-25 | 50 | 75 | 100 |
|-----------|--------|------|----|----|-----|
| **收集范围** | 单一渠道 | 3个渠道 | 5个及以上渠道 | 全生命周期覆盖 |
| **分析深度** | 评论阅读情况 | 是否分类分析 | 是否量化主题 | 是否具有预测性 |
| **响应时间** | 响应时间（周/天/小时） | 是否满足实时响应标准 |
| **闭环管理效率** | 20%以下 | 40-60% | 60-80% | 80%以上（包含满意度检查） |
| **决策影响力** | 是否对决策有实际影响 | 是否偶尔收到反馈 | 是否定期纳入决策流程 | 是否系统化影响决策 |
| **指标跟踪** | 是否有完整的指标体系 | 仅有无NPS数据 | 是否同时考虑NPS、CSAT和CES数据 | 是否包含全面指标 |
| **客户细分** | 是否按客户群体细分 | 是否按计划分层分析 | 是否提供个性化分析 |
| **ROI衡量** | 是否有明确的ROI衡量标准 | 仅凭主观感受 | 是否能量化功能影响 |

---

## 常用命令

使用以下命令来操作VoC系统：

1. **“设置VoC系统”** — 生成项目简介、收集渠道和首次调查问卷 |
2. **“设计NPS调查”** — 创建包含后续调查和分发计划的NPS调查问卷 |
3. **“准备客户访谈”** — 为特定客户或访谈类型生成访谈指南 |
4. **“分析反馈”** — 对反馈进行分类、评分、情感分析、标签设置并建议下一步行动 |
5. **“汇总访谈结果”** — 从多份访谈记录中生成综合分析报告 |
6. **“优先排序功能需求” ** 使用RICE-V评分方法进行优先级排序 |
7. **“生成VoC报告” ** 生成每周/每月/季度报告 |
8. **“评估VoC系统” ** 进行成熟度评估并提出改进建议 |
9. **“处理反馈” ** 为具体反馈生成合适的响应 |
10. **“与行业标准对比” ** 与行业基准进行对比分析 |
11. **“识别流失风险” ** 分析反馈中的流失风险信号 |
12. **“组建客户咨询委员会” ** 制定委员会组成标准、会议流程和议程 |

---

*由AfrexAI开发——将客户的声音转化为商业决策。*