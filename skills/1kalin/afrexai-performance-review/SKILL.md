# 绩效评估引擎

> 这是一个由人工智能驱动的性能管理系统，旨在帮助员工成长，而不仅仅是进行评估。从自我评估到360度反馈，我们提供了完整的评估周期框架。

---

## 快速入门

您可以这样使用该系统：
- 对您的代理说：“为[姓名]撰写绩效评估——他们的交付工作表现优异，但需要提升沟通能力”
- “帮我撰写2025年上半年的自我评估”
- “为我的6名团队成员收集360度反馈”
- “为我的4名直接下属准备评估意见”

---

## 1. 评估周期设置

### 周期配置模板

```yaml
cycle:
  name: "H2 2025 Performance Review"
  period: "2025-07-01 to 2025-12-31"
  type: annual | semi-annual | quarterly
  timeline:
    self_assessment_due: "2026-01-10"
    peer_feedback_due: "2026-01-17"
    manager_draft_due: "2026-01-24"
    calibration_session: "2026-01-28"
    delivery_window: "2026-01-29 to 2026-02-07"
  participants:
    - name: ""
      role: ""
      level: ""
      tenure_months: 0
      previous_rating: ""
      peer_reviewers: []
      skip_level_reviewer: ""
  rating_scale:
    1: "Does Not Meet Expectations"
    2: "Partially Meets Expectations"
    3: "Meets Expectations"
    4: "Exceeds Expectations"
    5: "Significantly Exceeds Expectations"
  competencies:
    - name: "Delivery & Execution"
      weight: 30
    - name: "Technical/Functional Expertise"
      weight: 25
    - name: "Communication & Collaboration"
      weight: 20
    - name: "Leadership & Influence"
      weight: 15
    - name: "Growth & Development"
      weight: 10
```

### 评分分布指南

| 评分 | 目标比例 | 说明 |
|--------|----------|-------------|
| 5 - 显著超出预期 | 5-10% | 对团队有变革性影响，提升了整体标准 |
| 4 - 超出预期 | 20-25% | 持续表现超出预期，有明显影响 |
| 3 - 达到预期 | 50-60% | 表现稳定，可靠 |
| 2 - 部分达到预期 | 10-15% | 在关键领域存在不足，需要重点改进 |
| 1 - 未达到预期 | 0-5% | 表现严重不佳，可能需要绩效改进计划 |

**注意：** 这些是评分指南，而非强制分配比例。如果团队中80%的员工表现优异，评分应真实反映实际情况。强行遵循固定比例可能会引发不信任。

---

## 2. 自我评估框架

### STAR-I 方法（情境 → 任务 → 行动 → 结果 → 影响）

指导员工撰写能够体现其价值的自我评估：

```markdown
### Achievement: [Title]

**Situation:** What was the context or challenge?
**Task:** What was your specific responsibility?
**Action:** What did you do? (Be specific — tools, approaches, decisions)
**Result:** What was the measurable outcome?
**Impact:** How did this affect the team/org/company beyond the immediate result?

**Competency alignment:** [Which competency does this demonstrate?]
**Evidence:** [Links, metrics, Slack messages, PRs, customer feedback]
```

### 按能力划分的自我评估提示

**交付与执行：**
- 本季度您完成的最重要的3-5项成果是什么？
- 哪些项目按时按预算完成了？哪些没有，原因是什么？
- 您是如何处理阻碍因素或范围变更的？
- 您最自豪交付了哪些成果？

**技术/职能专长：**
- 您掌握了哪些新技能或知识？
- 在哪些方面您成为了团队的专家？
- 您做出了哪些技术决策，结果如何？
- 您是如何保持行业知识的更新的？

**沟通与协作：**
- 您如何促进团队效率？
- 请举一个有效解决冲突的例子？
- 您是如何与他人分享知识的？
- 您参与了哪些跨部门的工作？

**领导力与影响力：**
- 您如何影响超出直接职责范围的结果？
- 您是否指导或培养过他人？是如何做的？
- 您推动了哪些项目或倡议？
- 您如何为团队文化做出贡献？

**成长与发展：**
- 您收到了哪些反馈，并采取了哪些行动？
- 本季度您在哪些方面取得了最大进步？
- 您还有哪些方面需要改进？
- 下一个季度的目标是什么？

### 自我评估质量检查清单

- [ ] 包含5-8项具体的成果，并附有数据支持
- [ ] 使用STAR-I格式（而不仅仅是“我做了X”）
- [ ] 覆盖所有能力领域，而不仅仅是交付成果
- [ ] 如实承认至少1-2个需要改进的方面
- [ ] 提及收到的具体反馈及采取的行动
- [ ] 包含未来目标
- [ ] 避免使用模糊的语言（如“提供了帮助”、“参与了某项工作”）
- [ ] 尽可能提供证据支持
- [ ] 页数适中（1-2页）
- [ ] 用第一人称书写，语气专业且亲切

---

## 3. 经理评估撰写

### OBSERVE 框架

每个评估都应围绕以下方面进行：

**O — 交付成果：** 他们完成了什么？提供具体数据和证据。
**B — 表现行为：** 他们是如何工作的，而不仅仅是完成了什么。
**S — 强项：** 他们的优势——哪些方面应该更加突出？
**E — 发展空间：** 将需要改进的方面视为机会，而非失败。
**R — 关系与影响：** 他们对团队动态和文化产生了怎样的影响。
**V — 前瞻性规划：** 明确的下一个季度目标和发展计划。
**E — 证据支持：** 每一项陈述都应有具体例证支持。

### 编写规则

1. **具体 > 模糊**
   - ❌ “本季度表现很好”
   - ✅ “领导了影响12个服务的API迁移工作，提前两周完成，且没有出现任何客户投诉”

2. **行为 > 特质**
   - ❌ “天生就是领导者”
   - ✅ “组织了每周的知识分享会议，使团队效率提高了15%，新员工的入职时间缩短了”

3. **模式 > 事件**
   - ❌ “错过了第三季度的截止日期”
   - ✅ “5个项目中有3个错过了交付期限，每次都滞后1-2周，表明估算能力需要提高”

4. **关注未来 > 回顾过去**
   - ❌ “沟通效果不佳”
   - ✅ “加强与利益相关者的沟通——特别是主动提供进度更新——这将提升他们的技术工作的影响力”

5. **始终保持平衡**
   - 即使是表现最好的员工也需要发展反馈
   - 即使是表现不佳的员工也有值得肯定的优点
   - 评分比例建议为：60% 强项 / 40% 发展空间（根据评分进行调整）

### 不同评分的评估模板

#### 评分5 — 显著超出预期

```markdown
## Performance Review: [Name] — H2 2025
**Rating: Significantly Exceeds Expectations (5/5)**

### Summary
[Name] delivered exceptional results this period, consistently operating above their current level. Their impact extended well beyond their role, influencing [team/org/company] outcomes in measurable ways.

### Key Achievements
1. **[Achievement]** — [STAR-I summary with metrics]
2. **[Achievement]** — [STAR-I summary with metrics]
3. **[Achievement]** — [STAR-I summary with metrics]

### Competency Assessment
| Competency | Rating | Evidence |
|-----------|--------|----------|
| Delivery & Execution | 5 | [Specific examples] |
| Technical Expertise | [X] | [Specific examples] |
| Communication | [X] | [Specific examples] |
| Leadership | [X] | [Specific examples] |
| Growth | [X] | [Specific examples] |

### Strengths to Leverage
- [Strength 1] — this is a differentiator that should be amplified
- [Strength 2] — consider giving them a platform to share this more broadly

### Development Opportunities
Even at this exceptional level, continued growth in [area] would unlock [next-level impact]. Specifically:
- [Development area with actionable suggestion]
- [Stretch assignment or learning recommendation]

### Forward Look
[Name] is ready for [promotion/expanded scope/leadership opportunity]. Recommended next steps: [specific action].
```

#### 评分3 — 达到预期

```markdown
## Performance Review: [Name] — H2 2025
**Rating: Meets Expectations (3/5)**

### Summary
[Name] delivered solid, reliable work this period, meeting the expectations of their role. They are a dependable contributor who [key positive theme].

### Key Achievements
1. **[Achievement]** — [Evidence]
2. **[Achievement]** — [Evidence]
3. **[Achievement]** — [Evidence]

### Competency Assessment
[Same table format]

### Strengths
- [Strength 1 with evidence]
- [Strength 2 with evidence]

### Development Areas
To move from "meets" to "exceeds," [Name] should focus on:
1. **[Area]** — Currently [current state]. The gap is [specific gap]. To close it: [actionable steps].
2. **[Area]** — [Same structure]

### Forward Look
Goals for next period:
1. [Measurable goal tied to development area]
2. [Stretch goal that would demonstrate growth]
3. [Continuation goal building on strengths]
```

#### 评分1-2 — 未达到预期

```markdown
## Performance Review: [Name] — H2 2025
**Rating: [Partially Meets / Does Not Meet] Expectations ([1-2]/5)**

### Summary
[Name] struggled to meet expectations in key areas this period. While [acknowledge any positives], significant gaps in [areas] need to be addressed.

### Performance Gaps
1. **[Gap]** — Expected: [what was expected]. Actual: [what happened]. Impact: [business impact]. Examples: [2-3 specific instances].
2. **[Gap]** — [Same structure]

### What Was Done Well
- [Genuine positive — never skip this section]

### Context Considered
- [Any mitigating factors: reorg, unclear expectations, personal circumstances]
- [Whether support/coaching was provided and when]

### Improvement Plan
| Area | Current State | Target State | Actions | Timeline | Support Needed |
|------|--------------|-------------|---------|----------|----------------|
| [Gap 1] | [Specific] | [Specific] | [Steps] | [Date] | [Resources] |
| [Gap 2] | [Specific] | [Specific] | [Steps] | [Date] | [Resources] |

### Consequences
If improvement to [specific measurable standard] is not demonstrated by [date]:
- [Next step: PIP / role change / separation]

### Check-in Schedule
- Weekly 1:1s focused on [areas]
- 30-day checkpoint: [date]
- 60-day checkpoint: [date]
- Final assessment: [date]
```

---

## 4. 360度反馈系统

### 同事反馈请求模板

```markdown
Hi [Peer Name],

You're invited to provide feedback on [Employee Name] for our [H2 2025] review cycle.

Please share your observations (10-15 min, ~200-400 words total):

1. **What does [Name] do well?** (Think: specific projects, behaviors, impact on you/the team)
2. **What could [Name] improve?** (Think: what would make them even more effective?)
3. **How would you describe working with [Name]?** (Collaboration style, communication, reliability)
4. **One thing [Name] should keep doing:** ___
5. **One thing [Name] should start or do more of:** ___

Your feedback will be anonymized and synthesized — [Name] will not see your individual responses verbatim.

Due by: [Date]
```

### 反馈整合方法

在整合多份同事反馈时：

1. **识别共同点** — 多人提到的问题是什么？这些是值得关注的模式，而非偶然现象。
2. **根据亲密程度加权** — 来自密切合作者的反馈比偶尔接触者的反馈更重要。
3. **区分事实与感受** — “错过了3个截止日期”是事实，“显得不投入”是一种主观感受（仍然有参考价值，但需以不同方式呈现）。
4. **保留独特见解** — 如果有人发现了独特的问题，也应予以记录。

### 反馈整合模板

```markdown
### 360° Feedback Summary for [Name]

**Respondents:** [N] peers, [N] cross-functional, [N] skip-level

**Consistent Strengths (mentioned by 2+ reviewers):**
- [Theme] — "[Representative quote]" (paraphrased from [N] responses)
- [Theme] — "[Representative quote]"

**Consistent Development Areas:**
- [Theme] — "[Representative quote]"
- [Theme] — "[Representative quote]"

**Notable Individual Observations:**
- [Unique insight worth including]

**Overall Sentiment:** [Positive / Mixed / Concerning]
**Collaboration Rating (aggregated):** [Strong / Solid / Needs Improvement]
```

---

## 5. 校准会议

### 校准前的准备工作

为每位直接下属准备：

```yaml
calibration_card:
  name: ""
  current_level: ""
  tenure: ""
  previous_rating: ""
  proposed_rating: ""
  rating_justification: "" # 2-3 sentences max
  top_achievement: ""
  biggest_gap: ""
  promotion_candidate: yes | no | not_yet
  flight_risk: low | medium | high
  key_question: "" # What you want the calibration group to weigh in on
```

### 校准讨论框架

**第一轮 — 展示（每人2分钟）**
- 经理介绍：提出的评分、主要成就、最大的不足
- 此时不进行讨论——只是介绍整体情况

**第二轮 — 校准（需要时每人5分钟）**
- 关注：评分为4或5的员工（他们真的表现突出吗？）、评分为1或2的员工（评分是否合理？）、与上一周期相比是否有变化
- 询问：“这个人在其他团队中会得到相同的评分吗？”
- 询问：“这个评分与[类似的人]相比是否合理？”

**第三轮 — 最终决定**
- 确定最终评分
- 标出需要跳级评估的员工
- 确定需要保留或晋升的员工

### 校准偏差检查清单

在最终确定评分前，请检查以下问题：
- [ ] **近期偏差** — 你是否过分强调了最近一个月的表现？
- [ ] **光环效应** — 一个员工的出色/糟糕表现是否影响了整个评估结果？
- [ ] **相似性偏差** — 你是否对与自己相似的人给予了更高的评分？
- [ ] **中心趋势偏差** — 你是否避开了合理的极端评分？
- [ ] **归因偏差** — 你是否将问题归咎于个人？
- [ ] **对比效应** — 你是否在比较时参考了之前的评估结果？

---

## 6. 评估沟通

### 沟通结构（45-60分钟）

**开场（5分钟）**
- 设定基调：“这是一个双向的沟通，不是定论”
- 提前告知评分结果——不要让他们等待

**成就（10分钟）**
- 介绍他们最突出的3-5项成就
- 让他们补充相关背景或你未提及的成就
- 表达真诚的赞赏——这不仅仅是批评的前奏

**发展（15分钟）**
- 提出1-2个需要改进的方面（而不是10个）
- 使用STAR-I格式：“我观察到[具体行为]在[具体情境]中发生，结果是[具体结果]。我希望看到[你希望看到的行为]。”
- 询问：“你有什么看法？”
- 倾听他们的意见。

**360度反馈（5分钟）**
- 分享整合后的同事反馈
- 强调：“同事们非常重视[某方面]”
- 讨论发展方面：“大家提到的一个共同点是[某方面]——你的看法是什么？”

**目标与发展计划（15分钟）**
- 共同制定3-5个下一个季度的目标
- 至少包括1个发展目标，而不仅仅是交付目标
- 确定具体的行动、所需资源和支持
- 确定后续沟通的频率

**结束（5分钟）**
- 总结关键要点
- 询问：“你需要我提供什么帮助才能取得成功？”
- 以积极和支持的态度结束对话

### 不同情况的沟通策略

**对于表现不佳的员工：**
“我想直接与你沟通，因为我尊重你的能力和潜力。本季度你的表现没有达到我们的要求。以下是我观察到的情况……我希望与你一起制定一个改进计划。你愿意参与吗？”

**对于表现优异但未获得晋升的员工：**
“你本季度的工作非常出色——[具体例子]。你被评为[某个等级]而不是获得晋升的原因是[具体原因]。以下是我认为需要的改进措施：[具体步骤]。我承诺支持你实现这些目标。”

**对于对评分有异议的员工：**
“我理解你的观点，希望你能详细说明你的不同看法。……感谢你的分享。以下是我考虑的各种因素。……”

---

## 7. 发展计划

### 发展计划模板

```yaml
development_plan:
  employee: ""
  manager: ""
  period: "H1 2026"
  review_date: ""
  
  strengths_to_leverage:
    - strength: ""
      leverage_action: "" # How to use this more
      
  development_areas:
    - area: ""
      current_state: ""
      target_state: ""
      actions:
        - type: "on_the_job" # 70% of development
          description: ""
          timeline: ""
        - type: "learning" # 20% — coaching, mentoring, peer learning
          description: ""
          timeline: ""
        - type: "formal" # 10% — courses, certifications, conferences
          description: ""
          timeline: ""
      success_metrics: ""
      check_in_dates: []
      
  career_goals:
    short_term: "" # 6-12 months
    medium_term: "" # 1-3 years
    long_term: "" # 3-5 years
    
  support_needed:
    from_manager: ""
    from_org: ""
    budget_required: ""
```

### 70-20-10 发展组合

| 类型 | 比例 | 例子 |
|------|---|----------|
| 在职学习 | 70% | 担任领导任务、新项目、推动倡议、参与跨部门工作、跟随资深员工学习 |
| 社交学习 | 20% | 导师制、辅导、同事反馈、参与专业社区、教学他人 |
| 正规学习 | 10% | 参加课程、认证培训、会议、阅读书籍、参加结构化培训项目 |

**常见错误：** 过度依赖正规学习（如送员工参加课程），而实际上在职学习可能更有效。

---

## 8. 持续反馈（评估周期之间）

### 1:1 绩效沟通模板（每月一次）

```markdown
## Monthly Check-in: [Name] — [Month Year]

### Progress on Goals
| Goal | Status | Notes |
|------|--------|-------|
| [Goal 1] | 🟢 On track / 🟡 At risk / 🔴 Off track | [Brief update] |

### Recent Wins
- [What went well this month]

### Challenges
- [What's been difficult]

### Feedback Exchange
- **Manager → Employee:** [One specific piece of feedback]
- **Employee → Manager:** [Ask: "What can I do differently to support you?"]

### Action Items
- [ ] [Action] — Owner: [who] — By: [date]

### Overall Pulse: 😊 Great / 😐 Fine / 😟 Struggling
```

### 实时反馈公式（SBI）

**情境：** “在昨天的客户会议上……”
**行为：** “……你通过重新解释ROI来处理价格异议……”
**结果：** “……这使我们保持了原价，客户的态度也从怀疑转为感兴趣。”

**反馈应在48小时内给出。正面反馈可以公开表达，建设性反馈应私下进行。**

---

## 9. 评分与分析

### 个人绩效评分（0-100分）

```
Score = Σ (competency_rating × competency_weight) × 20

Example:
Delivery (4/5 × 30%) + Technical (3/5 × 25%) + Communication (4/5 × 20%) 
+ Leadership (3/5 × 15%) + Growth (4/5 × 10%)
= (1.20 + 0.75 + 0.80 + 0.45 + 0.40) = 3.60 / 5 = 72/100
```

### 团队健康状况仪表盘

**季度跟踪：**

```markdown
## Team Performance Dashboard — Q4 2025

**Team size:** [N]
**Rating distribution:** ⭐5: [N] | ⭐4: [N] | ⭐3: [N] | ⭐2: [N] | ⭐1: [N]
**Average score:** [X]/100
**vs. last period:** [↑/↓ X points]

**Promotion candidates:** [Names]
**Flight risks:** [Names + risk level]
**PIP/coaching:** [Names]

**Top team strengths:** [Competencies scoring highest]
**Team gaps:** [Competencies scoring lowest]
**Development budget used:** [X]% of [Y] allocated

**Engagement signals:**
- Voluntary turnover: [X]%
- Internal mobility: [X] transfers/promotions
- 1:1 completion rate: [X]%
- Goal completion rate: [X]%
```

---

## 10. 特殊情况与高级场景

### 新员工（入职不到6个月）**
- 根据入职里程碑进行评估，而非全面职责要求
- 更重视学习速度和文化融入情况
- 与资深员工相比时，评分下限为3分（除非存在真正的绩效问题）

### 职位变更中**
- 将评估分为两部分：前半部分针对旧职位，后半部分针对新职位
- 新职位的表现应占更大比重（因为这是对未来的预测）
- 注意过渡期的表现波动

### 远程/混合办公员工**
- 评估工作成果和影响，而不仅仅是出勤时间
- 寻求非办公室同事的反馈
- 避免默认给予在办公室工作的人更高评分

### 表现优异但希望离职的员工**
- 与他们进行沟通：“我很重视你，希望了解你希望留下的原因”
- 不要为了留住员工而抬高评分——这会树立不良榜样
- 记录沟通内容和采取的保留措施

### 接任前任员工的经理**
- 从前任经理那里获取相关信息（请求查看前任的评估记录）
- 保持透明：“我还在了解你的工作表现”
- 更多参考同事反馈和客观数据
- 不要因为不了解情况就默认给予“达到预期”的评分

### 经理评估不喜欢的人**
- 仅关注可观察的行为和可衡量的成果
- 让同事经理帮忙检查评估的公正性
- 自问：“如果是我最喜欢的团队成员做了同样的事，我会给他们什么评分？”

---

## 11. 法律与合规注意事项

**文档规则：**
- 所有评估文件至少保存3年（在受监管行业中保存7年）
- 反馈必须针对具体、可观察的行为——不得涉及个人特质
- 严禁提及受保护的信息（如年龄、性别、残疾等）
- 绩效改进计划文件在发布前需经过人力资源部门或法律部门的审核
- 员工需签署确认收到文件的声明（而非同意评估结果的声明）

**避免使用的表述：**
- “文化契合度”（可能掩盖偏见）→ 使用“协作效率”
- “激进”（带有性别歧视的意味）→ 使用“果断”或“直接”
- “年轻/精力充沛”→ 使用具体的行为描述
- “不善于团队合作”→ 举例说明具体的协作问题

---

## 命令参考

| 命令 | 功能 |
|---------|-------------|
| “为[团队]启动评估周期” | 创建包含时间表的周期配置 |
| “为[具体成就]生成自我评估” | 生成STAR-I格式的自我评估文档 |
| “为[姓名]撰写评估——评分[X]” | 使用OBSERVE框架撰写完整经理评估 |
| “为[姓名]收集360度反馈” | 生成同事反馈请求 |
| “整合[来源]的反馈” | 将多份反馈整合成统一意见 |
| “为[团队]准备评估意见” | 为所有员工生成评估卡片 |
| “为[姓名]制定发展计划” | 制定70-20-10的发展计划 |
| “为[姓名]进行每月沟通” | 生成包含目标跟踪的1:1沟通模板 |
| “对[具体情境]提供反馈” | 使用SBI格式进行反馈 |
| “全面评估[姓名]的各项能力” | 计算综合绩效评分 |
| “团队健康状况仪表盘” | 生成团队整体分析报告 |