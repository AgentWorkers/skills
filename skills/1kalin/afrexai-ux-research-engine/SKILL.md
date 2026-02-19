---
name: afrexai-ux-research-engine
description: 完整的用户体验研究与设计系统——包括用户发现、角色建模、用户旅程分析、可用性测试、研究结果整合以及设计验证等功能。该系统完全独立运行，无需依赖任何外部组件或服务。
---
# 用户体验研究引擎 ⚡

一套完整的用户体验研究方法论——从问题发现到验证设计决策。无需脚本、API或依赖外部工具，完全依靠研究人员的专业技能。

---

## 第一阶段：研究规划

### 研究简报（YAML格式）

```yaml
project: "[Product/Feature Name]"
research_question: "[What do we need to learn?]"
business_context:
  objective: "[Business goal this research supports]"
  decision: "[What decision will this research inform?]"
  stakeholders: ["PM", "Design Lead", "Engineering"]
  deadline: "YYYY-MM-DD"
scope:
  product_area: "[Feature/flow being studied]"
  user_segment: "[Who are we studying?]"
  geographic: "[Regions/markets]"
methodology: "[See selection matrix below]"
sample_size: "[See calculator below]"
timeline:
  planning: "Week 1"
  recruiting: "Week 1-2"
  fieldwork: "Week 2-3"
  analysis: "Week 3-4"
  reporting: "Week 4"
budget:
  participant_incentives: "$X"
  tools: "$X"
  total: "$X"
success_criteria:
  - "[Specific insight we need]"
  - "[Confidence level required]"
  - "[Actionable output format]"
```

### 方法选择矩阵

| 方法 | 适用场景 | 样本量 | 时间 | 成本 | 可靠性 |
|--------|----------|-------------|------|------|------------|
| 用户访谈 | 深入了解用户“为什么”这样操作，探索未知问题 | 5-15人 | 2-4周 | 高（定性研究） |
| 可用性测试 | 发现交互问题，验证用户操作流程 | 每轮5-8人 | 1-2周 | 高（行为研究） |
| 调查 | 定量分析用户态度，衡量满意度 | 100-400人或更多 | 1-2周 | 高（统计分析） |
| 卡片分类法 | 分析信息架构和导航标签 | 15-30人（开放式问题），30人以上（封闭式问题） | 1周 | 中等 |
| 日记研究 | 长期观察用户行为和使用场景 | 10-15人 | 2-6周 | 高（纵向研究） |
| A/B测试 | 比较不同设计方案 | 每个方案1000人以上 | 1-4周 | 非常高 |
| 情境探究 | 了解用户在实际环境中的行为和工作流程 | 4-8人 | 2-3周 | 非常高 |
| 树状测试 | 在没有视觉设计的情况下验证信息架构 | 50人以上 | 1周 | 高 |
| 首次点击测试 | 测试导航效率 | 30-50人 | 1周 | 中等 |
| 概念测试 | 早期验证设计想法 | 8-15人 | 1-2周 | 中等 |
| 启发式评估 | 专家评估现有用户界面 | 3-5名评估者 | 2-3天 | 中等 |
| 竞品用户体验审计 | 了解市场标准 | 无固定样本量 | 1周 | 低-中等 |

### 决策树：选择哪种方法？

```
Do you know WHAT the problem is?
├── NO → Generative Research
│   ├── Need context? → Contextual Inquiry
│   ├── Need attitudes? → User Interviews
│   ├── Need behaviors over time? → Diary Study
│   └── Need broad patterns? → Survey (exploratory)
│
└── YES → Evaluative Research
    ├── Have a prototype/product?
    │   ├── YES → Usability Testing
    │   │   ├── Early concept → Concept Test (paper/low-fi)
    │   │   ├── Key flow → Task-based Usability Test
    │   │   └── Comparing options → A/B Test
    │   └── NO → 
    │       ├── Testing IA → Card Sort / Tree Test
    │       └── Testing content → First-Click Test
    └── Need expert opinion fast? → Heuristic Evaluation
```

### 样本量计算

**定性研究（访谈、可用性测试）：**
- 根据Nielsen的研究，5名用户可以发现约85%的可用性问题 |
- 为了确保调查结果的全面性，建议访谈8-12人 |
- 如果目标群体多样或研究领域复杂，建议访谈15人以上 |
- 规则：重复访谈直到听到相同的问题三次以上再停止

**定量研究（调查）：**
| 样本量 | 90%置信度 ±5% | 95%置信度 ±5% | 99%置信度 ±5% |
|------------|---------------------|---------------------|---------------------|
| 100人 | 74人 | 80人 | 87人 |
| 500人 | 176人 | 217人 | 285人 |
| 1,000人 | 214人 | 278人 | 399人 |
| 10,000人 | 264人 | 370人 | 622人 |
| 100,000人以上 | 271人 | 384人 | 660人 |

**A/B测试：**
- 根据最小可检测效应（MDE）计算样本量 |
- 如果MDE为5%，置信度为95%，每个方案需要约1,600人 |
- 如果MDE为2%，每个方案需要约10,000人 |
- 建议进行完整的测试周期（至少1周）

---

## 第二阶段：招募参与者

### 筛选问卷模板

```yaml
screener:
  title: "[Study Name] Participant Screener"
  target_profile:
    demographics:
      age_range: "[e.g., 25-45]"
      location: "[e.g., US-based]"
      language: "[e.g., English-fluent]"
    behavioral:
      product_usage: "[e.g., Uses [product] 3+ times/week]"
      experience_level: "[e.g., 1+ year with similar tools]"
      recent_activity: "[e.g., Made a purchase in last 30 days]"
    psychographic:
      decision_maker: "[e.g., Primary household purchaser]"
      tech_comfort: "[e.g., Comfortable with mobile apps]"
  
  screening_questions:
    - question: "How often do you use [product category]?"
      type: "single-select"
      options: ["Daily", "Weekly", "Monthly", "Rarely", "Never"]
      qualify: ["Daily", "Weekly"]
      disqualify: ["Never"]
    
    - question: "Which of these tools do you currently use?"
      type: "multi-select"
      options: ["Tool A", "Tool B", "Tool C", "None"]
      qualify_min: 1
      
    - question: "What is your primary role?"
      type: "single-select"
      options: ["Developer", "Designer", "PM", "Marketing", "Other"]
      qualify: ["Developer", "Designer", "PM"]
    
    - question: "Have you participated in a UX study in the last 6 months?"
      type: "single-select"
      options: ["Yes", "No"]
      disqualify: ["Yes"]  # Avoid professional participants
  
  anti-patterns:
    - "Works at a competitor or in UX research"
    - "Family/friends of team members"
    - "Participated in study for this product before"
  
  incentive: "$75 for 60-min session"
  
  recruiting_channels:
    - channel: "Existing user database"
      quality: "★★★★★"
      cost: "Free"
    - channel: "UserTesting.com / UserInterviews.com"
      quality: "★★★★"
      cost: "$50-150/participant"
    - channel: "Social media recruitment"
      quality: "★★★"
      cost: "Free-$$"
    - channel: "Craigslist / local posting"
      quality: "★★"
      cost: "$"
```

### 招募质量检查清单
- [ ] 筛选问卷没有引导性问题（避免明显的“正确”答案）
- [ ] 目标人群中包含不同类型的人选 |
- [ ] 来自同一招募渠道的参与者不超过20% |
- [ ] 至少有一名“边缘用户”（如高级用户、新用户或有特殊需求的用户） |
- [ ] 招募人数比实际需要多20%以应对可能的缺席情况 |
- [ ] 同意书已准备好并提前发送 |
- [ ] 已确认激励措施的发放方式 |

---

## 第三阶段：用户访谈

### 访谈指南模板

```markdown
# Interview Guide: [Study Name]
Duration: 60 minutes
Moderator: [Name]

## Setup (5 min)
- Thank participant, confirm recording consent
- "There are no right or wrong answers — we're learning from YOUR experience"
- "Feel free to be critical — honest feedback helps us improve"
- "I didn't design this, so you won't hurt my feelings"

## Warm-Up (5 min)
- "Tell me about your role and what a typical day looks like"
- "How does [product area] fit into your work?"

## Core Questions (35 min)

### Context & Current Behavior
1. "Walk me through the last time you [did the task we're studying]"
   - Probe: "What happened next?"
   - Probe: "How did that make you feel?"
   - Probe: "What would you have preferred to happen?"

2. "What tools/methods do you currently use for [task]?"
   - Probe: "What do you like about that approach?"
   - Probe: "What frustrates you?"
   - Probe: "How long have you been doing it this way?"

3. "Can you show me how you typically [task]?" (if remote: screen share)

### Pain Points & Needs
4. "What's the hardest part about [task]?"
   - Probe: "How often does that happen?"
   - Probe: "What do you do when that happens?"
   - Probe: "How much time/money does that cost you?"

5. "If you could wave a magic wand and change one thing about [experience], what would it be?"

6. "Tell me about a time when [process] went really wrong"
   - Probe: "What was the impact?"
   - Probe: "How was it resolved?"

### Mental Models
7. "How would you explain [concept] to a colleague?"
8. "What do you expect to happen when you [action]?"
9. "Where would you look for [information/feature]?"

### Priorities & Trade-offs
10. "If you had to choose between [speed vs accuracy / ease vs power], which matters more? Why?"

## Concept Reaction (10 min) — if applicable
- Show prototype/concept
- "What's your first impression?"
- "What would you use this for?"
- "What's missing?"
- "Would this replace what you currently use? Why/why not?"

## Wrap-Up (5 min)
- "Is there anything else about [topic] we should know?"
- "Who else should we talk to about this?"
- Thank participant, confirm incentive delivery
```

### 访谈质量规则
1. **80/20法则**：参与者说话80%，你提问20%
2. **不要问“你会使用这个功能吗？”**——人们无法预测未来的行为
3. **询问过去的行为**，而不是假设未来的情况
4. **跟随他们的思路**——当他们表现出兴趣时，进一步深入探讨
5. **沉默是一种技巧**——在他们回答后暂停5秒，他们会继续补充
6. **“请详细说说……”**——这是最有效的提问方式
7. **注意言行不一致的情况**——记录下言行不一致的地方
8. **全程录音**——至少录音，最好录像，并做好笔记

### 访谈记录模板（每次访谈使用）

```yaml
participant:
  id: "P01"
  date: "YYYY-MM-DD"
  demographics: "[age, role, experience level]"
  session_duration: "58 min"

key_quotes:
  - quote: "[Exact words]"
    timestamp: "12:34"
    context: "[What prompted this]"
    theme: "[Emerging theme tag]"

observations:
  behaviors:
    - "[What they DID, not what they said]"
  emotions:
    - "[Frustration when..., delight when..., confusion at...]"
  workarounds:
    - "[Creative solutions they've built]"

pain_points:
  - pain: "[Specific problem]"
    severity: "[1-5]"
    frequency: "[daily/weekly/monthly/rarely]"
    current_solution: "[How they cope]"
    
needs:
  - need: "[Unmet need identified]"
    type: "[functional/emotional/social]"
    evidence: "[Quote or behavior that reveals this]"

surprises:
  - "[Anything unexpected — these are gold]"

moderator_notes:
  - "[Post-session reflection, what to adjust for next interview]"
```

---

## 第四阶段：构建用户角色

### 数据驱动的用户角色模板

```yaml
persona:
  name: "[Realistic name — not cutesy]"
  photo: "[Representative stock photo description]"
  archetype: "[1-3 word label, e.g., 'The Overwhelmed Manager']"
  
  demographics:
    age: "[Range or specific]"
    role: "[Job title / life stage]"
    experience: "[Years with product/domain]"
    tech_proficiency: "[Novice / Intermediate / Advanced / Expert]"
    environment: "[Office / remote / mobile / field]"
  
  # MOST IMPORTANT SECTION
  goals:
    primary: "[The #1 thing they're trying to accomplish]"
    secondary:
      - "[Supporting goal]"
      - "[Supporting goal]"
    underlying: "[The emotional/social need behind the functional goal]"
  
  frustrations:
    - frustration: "[Specific pain point]"
      frequency: "[How often — from research data]"
      severity: "[1-5]"
      current_workaround: "[What they do today]"
      evidence: "[P03, P07, P11 mentioned this]"
  
  behaviors:
    usage_pattern: "[When, where, how often they engage]"
    decision_process: "[How they evaluate options]"
    information_sources: "[Where they learn / get help]"
    social_influence: "[Who influences their decisions]"
    key_workflows:
      - "[Task 1 — frequency — duration]"
      - "[Task 2 — frequency — duration]"
  
  mental_models:
    - "[How they think about [concept] — often surprising]"
    - "[Vocabulary they use — not our jargon]"
  
  motivations:
    gains: "[What success looks like to them]"
    fears: "[What failure looks like]"
    triggers: "[What prompts them to act]"
    barriers: "[What stops them from acting]"
  
  quotes:
    - "\"[Real quote from research that captures this persona]\""
    - "\"[Another revealing quote]\""
  
  design_implications:
    must_have:
      - "[Feature/quality this persona absolutely needs]"
    should_have:
      - "[Important but not dealbreaker]"
    must_avoid:
      - "[Things that will drive this persona away]"
    communication_style: "[How to talk to this persona]"
  
  data_sources:
    interviews: "[# of participants who map to this persona]"
    survey_segment: "[% of survey respondents]"
    analytics_cohort: "[Behavioral data that identifies this group]"
```

### 用户角色验证清单
- [ ] 基于真实的研究数据，而非猜测 |
- [ ] 代表有代表性的用户群体（而非个别极端案例） |
- [ ] 角色的目标明确，有助于设计 |
- [ ] 描述用户的困扰及其频率和严重程度 |
- [] 包含至少两条真实的用户反馈 |
- [ ] 设计建议具有可操作性 |
- [ ] 已经经过3名以上利益相关者的审查 |
- [ ] 与分析数据相互验证 |
- [ ] 该用户角色不能涵盖所有用户（好的用户角色应排除某些特定用户）

### 非目标用户角色（我们不针对的用户群体）

```yaml
anti_persona:
  name: "[Label]"
  description: "[Who this is]"
  why_excluded: "[Business reason — too small a segment, wrong market, etc.]"
  risk_if_included: "[What happens to the product if we try to serve them too]"
```

---

## 第五阶段：用户旅程映射

### 旅程地图模板

```yaml
journey_map:
  title: "[Persona] — [Goal/Scenario]"
  persona: "[Which persona]"
  scenario: "[Specific situation triggering this journey]"
  
  stages:
    - stage: "1. Awareness / Trigger"
      duration: "[Time in this stage]"
      goals: "[What they want to accomplish]"
      actions:
        - "[Step they take]"
        - "[Step they take]"
      touchpoints:
        - "[Where they interact — website, app, email, phone, in-person]"
      thoughts:
        - "\"[What they're thinking — from research]\""
      emotions:
        rating: 3  # 1=frustrated, 3=neutral, 5=delighted
        feeling: "[Curious but uncertain]"
      pain_points:
        - "[Problem encountered]"
      opportunities:
        - "[How we could improve this moment]"
    
    - stage: "2. Consideration / Research"
      # ... same structure
    
    - stage: "3. Decision / Sign-Up"
      # ... same structure
    
    - stage: "4. Onboarding / First Use"
      # ... same structure
    
    - stage: "5. Regular Use / Value Realization"
      # ... same structure
    
    - stage: "6. Expansion / Advocacy (or Churn)"
      # ... same structure
  
  moments_of_truth:
    - moment: "[Critical make-or-break interaction]"
      stage: "[Which stage]"
      current_experience: "[What happens now — score 1-5]"
      desired_experience: "[What should happen — score 1-5]"
      gap: "[Difference = priority]"
      
  service_blueprint_layer:  # Optional — behind-the-scenes
    - stage: "[Stage name]"
      frontstage: "[What user sees]"
      backstage: "[What team does]"
      support_systems: "[Tools/processes involved]"
      failure_points: "[Where things break down]"
```

### 情感曲线评分
在用户旅程中绘制情感变化：

```
5 ★ Delighted  ──────────╮          ╭──
4 ☺ Happy               │          │
3 😐 Neutral    ──╮      │    ╭─────╯
2 😟 Frustrated    │      │    │
1 😤 Angry         ╰──────╯────╯
                  Stage1  Stage2  Stage3  Stage4  Stage5
```

### 旅程地图质量规则
1. 基于研究结果，而非猜测（注明每个数据来源）
2. 每个用户角色对应一张地图（不要平均分配数据）
3. 包括功能性和情感性维度
4. 识别“关键时刻”——决定用户体验成败的2-3个交互点
5. 根据差距大小（期望与现状的差距）对改进机会进行优先级排序
6. 包含服务设计的背景信息/蓝图

---

## 第六阶段：可用性测试

### 测试计划模板

```yaml
usability_test:
  study_name: "[Name]"
  objective: "[What design question are we answering?]"
  
  format:
    type: "[Moderated / Unmoderated]"
    location: "[Remote / In-person / Lab]"
    device: "[Desktop / Mobile / Tablet / Cross-device]"
    duration: "60 min"
    recording: "[Screen + audio + face camera]"
  
  prototype:
    fidelity: "[Paper / Wireframe / Hi-fi / Live product]"
    tool: "[Figma / InVision / Live URL]"
    scope: "[Which flows are testable]"
    known_limitations: "[What won't work in the prototype]"
  
  participants:
    target: 5-8
    criteria: "[From screener — link to Phase 2]"
    incentive: "$75"
  
  tasks:
    - task_id: "T1"
      scenario: "You need to [context]. Using this app, [goal]."
      success_criteria: 
        - "[Specific completion definition]"
      time_limit: "5 min"
      priority: "critical"  # critical / important / nice-to-know
      metrics:
        - completion_rate
        - time_on_task
        - error_count
        - satisfaction_rating
    
    - task_id: "T2"
      scenario: "[Next task...]"
      # ... same structure
  
  post_task_questions:
    - "On a scale of 1-7, how easy was that? (SEQ)"
    - "What did you expect to happen when you [action]?"
    - "Was anything confusing?"
  
  post_test_questions:
    - "SUS (System Usability Scale) — 10 questions"
    - "What was the easiest part?"
    - "What was the most frustrating part?"
    - "Would you use this? Why/why not?"
    - "What's missing?"
```

### 任务编写规则
1. **提供背景信息**——给出具体的情境，而不是直接给出指令（例如：“你需要预订下周五去纽约的航班”）
2. **避免使用界面术语**——使用自然语言（如“查找”而非“导航到”，“购买”而非“加入购物车并结账”）
3. **设计真实的任务场景**——基于实际研究数据
4. **每个任务只有一个目标**——避免同时设置多个复杂任务
5. **从简单到复杂逐步设计任务**

### 严重性评分标准

| 严重程度 | 标签 | 定义 | 应对措施 |
|----------|-------|------------|--------|
| 0 | 没有问题 | 评估者意见不一致，实际没有问题 | 无需处理 |
| 1 | 仅是外观问题 | 虽然存在但不会影响任务完成 | 有时间可修复 |
| 2 | 轻微问题 | 会导致犹豫或效率降低 | 安排修复 |
| 3 | 严重问题 | 需要绕过现有流程 | 发布前必须修复 |
| 4 | 灾难性问题 | 完全无法完成任务 | 立即修复 |

### 可用性测试记录模板

```yaml
finding:
  id: "UF-001"
  title: "[Short descriptive title]"
  severity: 3  # 0-4
  frequency: "4/5 participants"
  task: "T2"
  
  observation: "[What happened — factual, behavioral]"
  evidence:
    - participant: "P01"
      behavior: "[What they did]"
      quote: "\"[What they said]\""
      timestamp: "14:22"
    - participant: "P03"
      behavior: "[What they did]"
  
  root_cause: "[Why this happened — mental model mismatch, visibility, feedback, etc.]"
  
  recommendation:
    change: "[Specific design change]"
    rationale: "[Why this will fix it]"
    effort: "[S/M/L]"
    impact: "[High/Medium/Low]"
    
  heuristic_violated: "[Which Nielsen heuristic, if applicable]"
```

### Nielsen的10条可用性启发式原则（快速参考）

| 编号 | 启发式原则 | 检查内容 |
|---|-----------|---------------|
| 1 | 系统状态的可见性 | 显示加载进度、进度条、确认信息 |
| 2 | 与现实世界一致 | 标签使用用户熟悉的语言，避免内部术语 |
| 3 | 用户控制与自由度 | 可以轻松撤销、返回、取消、退出 |
| 4 | 一致性与标准 | 相同的操作在不同地方产生相同的结果 |
| 5 | 错误预防 | 提供确认信息、限制措施、智能默认设置 |
| 6 | 识别易用性高于记忆 | 选项易于识别 |
| 7 | 灵活性与效率 | 专家能快速使用，新手也能轻松操作 |
| 8 | 美观性与简洁性 | 避免不必要的信息干扰 |
| 9 | 错误恢复 | 明确的错误提示和解决方案 |
| 10 | 帮助与文档 | 提供易于搜索的信息，内容聚焦任务 |

### 启发式评估评分表

对每个屏幕/流程的每个启发式原则进行1-5分的评分：

```yaml
heuristic_audit:
  screen: "[Screen/Flow name]"
  evaluator: "[Name]"
  date: "YYYY-MM-DD"
  
  scores:
    visibility_of_status: 4
    real_world_match: 3
    user_control: 2
    consistency: 4
    error_prevention: 3
    recognition_over_recall: 4
    flexibility_efficiency: 2
    aesthetic_minimal: 3
    error_recovery: 1
    help_documentation: 2
  
  total: 28  # out of 50
  grade: "C"  # A=45+, B=38+, C=28+, D=20+, F=<20
  
  critical_issues:
    - heuristic: "Error recovery"
      location: "[Where]"
      issue: "[What's wrong]"
      fix: "[Recommendation]"
```

---

## 第七阶段：研究总结

### 共情映射过程

1. **提取**：将所有观察结果、用户反馈和行为记录在单独的笔记中 |
2. **分组**：将相似的笔记归类（自下而上，而非自上而下）
3. **命名**：用参与者的语言为每个组命名 |
4. **分层**：将分组归纳为更广泛的主题 |
5. **排序**：根据出现频率和影响程度进行优先级排序

### 主题模板

```yaml
theme:
  name: "[Theme label — use participant language]"
  description: "[2-3 sentence summary]"
  
  evidence:
    participant_count: "8/12 participants"
    segments_affected: ["Persona A", "Persona B"]
    
    quotes:
      - participant: "P03"
        quote: "\"[Exact quote]\""
      - participant: "P07"
        quote: "\"[Exact quote]\""
    
    behaviors_observed:
      - "[What they did]"
      - "[Pattern across participants]"
    
    data_points:
      - "[Any quantitative support — survey %, analytics, etc.]"
  
  impact:
    on_users: "[How this affects their experience]"
    on_business: "[Revenue, retention, acquisition, support cost impact]"
    severity: "High"  # High / Medium / Low
  
  insight: "[The 'so what' — what does this mean for design?]"
  
  recommendations:
    - recommendation: "[Specific, actionable change]"
      effort: "M"
      impact: "High"
      confidence: "High"  # based on evidence strength
```

### 观点撰写公式

每个观点都必须包含以下要素：**观察结果 + 证据 + 影响 + 推荐措施**

> “用户始终[观察结果]——在[X/Y名参与者中观察到，有相关证据支持。这很重要，因为[影响]——对业务目标有影响。我们应该[推荐措施]。”

**不良的观点示例：“用户觉得导航界面混乱”**
**良好的观点示例：“12名参与者中有7人在30秒内找不到设置页面。4人在个人资料菜单中寻找，2人使用搜索功能，1人放弃。这对应了15%的支持请求（‘如何更改密码’）。将设置页面移到一级导航栏并添加搜索快捷键可以减少发现问题的时间，同时减少相关支持请求的数量。”

### 研究评分标准（0-100分）

| 维度 | 权重 | 评分标准 |
|-----------|--------|----------|
| 方法论严谨性 | 20% | 选择合适的方法，样本量充足，招募过程规范 |
| 数据质量 | 15% | 观察丰富，有真实的用户反馈和行为数据 |
| 分析深度 | 20% | 探究到根本原因，发现不同用户群体的共性 |
| 观点的可操作性 | 25% | 提出的建议具体、可实施，且经过优先级排序 |
| 表达清晰度 | 10% | 利益相关者无需解释就能理解并采取行动 |
| 与业务的关联 | 10% | 研究结果与业务指标和目标相关 |

**评分标准：**
- 90-100分：研究质量高，适合发表 |
- 75-89分：研究结果较为可靠，但存在方法论或分析上的不足 |
- 60-74分：研究尚可，但在方法论或分析上有一定缺陷 |
- 40-59分：研究质量较低，发现结果不够深入或缺乏支持 |
- 40分以下：需要重新进行研究，因为方法论存在严重问题 |

---

## 第八阶段：研究报告

### 执行摘要模板

---

## 第九阶段：设计验证

### 设计评审框架（CAMPS）

| 维度 | 需要询问的问题 |
|-----------|-----------------|
| **清晰度** | 用户能否在5秒内理解研究内容和操作步骤？ |
| **针对性** | 该设计是否解决了研究中发现的问题？是否针对目标用户群体？ |
| **心理模型** | 设计是否符合用户对任务的认知（基于访谈数据） |
| **优先级** | 视觉设计是否符合用户的任务优先级？ |
| **简洁性** | 是否可以去除某些元素而不影响功能？ |

### 原型评审清单

```yaml
design_review:
  screen: "[Screen name]"
  reviewer: "[Name]"
  date: "YYYY-MM-DD"
  
  research_alignment:
    - check: "Addresses top pain point from research"
      status: "✅ / ❌ / ⚠️"
      notes: "[Which finding this addresses]"
    - check: "Uses language from user interviews (not internal jargon)"
      status: "✅ / ❌ / ⚠️"
    - check: "Matches mental model revealed in research"
      status: "✅ / ❌ / ⚠️"
    - check: "Works for primary persona AND doesn't break for secondary"
      status: "✅ / ❌ / ⚠️"
  
  usability:
    - check: "Primary action is visually dominant"
      status: "✅ / ❌ / ⚠️"
    - check: "Error states designed and messaged"
      status: "✅ / ❌ / ⚠️"
    - check: "Empty states designed (first use, no data, no results)"
      status: "✅ / ❌ / ⚠️"
    - check: "Loading states designed"
      status: "✅ / ❌ / ⚠️"
    - check: "Edge cases handled (long text, missing data, permissions)"
      status: "✅ / ❌ / ⚠️"
  
  accessibility:
    - check: "Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)"
      status: "✅ / ❌ / ⚠️"
    - check: "Touch targets ≥44px"
      status: "✅ / ❌ / ⚠️"
    - check: "Information not conveyed by color alone"
      status: "✅ / ❌ / ⚠️"
    - check: "Logical reading/tab order"
      status: "✅ / ❌ / ⚠️"
    - check: "Alt text for meaningful images"
      status: "✅ / ❌ / ⚠️"
  
  overall_score: "[1-5]"
  ship_decision: "Ready / Needs changes / Needs testing / Needs research"
```

---

## 第十阶段：研究运营

### 研究资料库结构

```
research/
├── YYYY/
│   ├── Q1/
│   │   ├── [study-name]/
│   │   │   ├── plan.yaml          # Research brief
│   │   │   ├── screener.yaml      # Recruiting criteria
│   │   │   ├── guide.md           # Interview/test guide
│   │   │   ├── notes/             # Per-participant notes
│   │   │   │   ├── P01.yaml
│   │   │   │   └── P02.yaml
│   │   │   ├── synthesis/         # Themes, affinity maps
│   │   │   ├── personas/          # Updated personas
│   │   │   ├── journey-maps/      # Updated maps
│   │   │   ├── report.md          # Final report
│   │   │   └── recordings/        # Session recordings (link)
│   │   └── [next-study]/
│   └── Q2/
├── personas/                      # Master persona library
│   ├── persona-a.yaml
│   └── persona-b.yaml
├── journey-maps/                  # Master journey maps
├── insights-database.yaml         # Cross-study insight tracker
└── research-calendar.yaml         # Planned studies
```

### 跨研究项目洞察跟踪

```yaml
insights_database:
  - insight_id: "INS-001"
    theme: "[Category]"
    insight: "[The insight]"
    first_found: "2026-01-15"
    studies: ["Study A", "Study C", "Study F"]
    evidence_strength: "Strong"  # 3+ studies
    status: "Addressed"  # Open / In Progress / Addressed / Won't Fix
    design_response: "[What was done]"
    impact_measured: "[Before/after metric if available]"
```

### 研究效果追踪

| 指标 | 测量方法 | 目标 |
|--------|---------------|--------|
| 研究结果与实际功能的匹配度 | 2个季度内实施的建议比例 | >60% |
| 可用性测试前后的评分变化 | 改进后的SUS评分 | 提高10分 |
| 支持请求量减少 | 设计变更后的支持请求量 | 减少25% |
| 任务完成率 | 随时间变化的可用性测试成功率 | >85% |
| 任务完成时间 | 任务完成时间的趋势 | 逐渐减少 |
| 利益相关者的满意度 | 后期调查：“这项研究有多有用？” | >4/5 |

---

## 快速命令

| 命令 | 功能 |
|---------|-------------|
| “为[主题]规划一项研究” | 生成研究简报（YAML格式） |
| “为[目标受众]制作筛选问卷” | 生成筛选问卷 |
| “为[主题]生成访谈指南” | 生成访谈问题和结构 |
| “根据[数据/笔记]构建用户角色” | 生成用户角色信息 |
| “为[用户角色+目标]绘制旅程地图” | 生成旅程地图 |
| “为[原型]制定可用性测试计划” | 生成包含具体任务的测试计划 |
| “对[界面/流程]进行启发式评估” | 根据Nielsen的10条原则进行评分 |
| “从[研究]中总结观点” | 生成研究主题和发现 |
| “为[研究]撰写报告” | 生成执行摘要和建议 |
| “评估这项研究的质量” | 根据评分标准进行评价 |
| “根据研究结果评审设计” | 使用CAMPS框架进行评审 |
| “建立研究资料库” | 创建文件夹结构和模板 |

---

## 特殊情况处理

### 预算有限/无招募预算
- **游击式测试**：在咖啡店随机邀请用户（测试时间5分钟，请用户喝杯咖啡）
- **内部用户**：邀请不同部门的同事参与 |
- **社交媒体**：在相关社区发布招募信息寻找志愿者 |
- **现有用户**：通过电子邮件邀请用户参与研究 |

### 仅通过远程方式进行的研究
- **视频会议**：使用Zoom或Google Meet进行屏幕共享 |
- **异步收集数据**：使用Loom录制用户操作过程并收集书面反馈 |
- **无监督测试**：使用UserTesting.com、Maze、Lookback等工具 |
- **日记研究**：使用WhatsApp、Telegram等通讯应用进行日常交流

### 利益相关者的反对意见（“我们没有时间进行研究”）
- **最低要求**：5名用户，1周时间，3个关键发现 |
- **将研究与其他工作结合**：与现有的沟通渠道（如支持电话、销售演示）结合进行 |
- **强调研究的价值**：解释“提前了解这些问题比在产品发布后了解更有价值”
- **展示以往研究的回报**：例如减少支持请求量、提高转化率

### 研究结果冲突
- **检查样本构成**：不同用户群体可能有不同的需求 |
- **根据业务影响优先处理**：哪个用户群体的需求更紧急？ |
- **进行调查**：例如“60%的用户偏好A选项，40%偏好B选项** |
- **考虑同时满足两种需求**：逐步披露信息或进行个性化设计 |

### 国际化/跨文化研究
- **不仅仅是翻译**：需要对场景和语言进行本地化 |
- **考虑文化差异**：某些文化中用户可能不愿意提出批评 |
- **使用本地化的审核人员** |
- **调整激励措施**：根据当地文化进行调整 |
- **注意设计上的差异**：例如图标、颜色、阅读方向等 |

### 可访问性研究
- **招募有特殊需求的用户**（如视障用户、行动不便的用户、认知障碍用户） |
- **使用实际辅助技术进行测试** |
- **将这类用户纳入常规研究**：每项研究至少包括1名有特殊需求的用户 |
- **WCAG合规性测试**不能替代针对残障用户的研究

---

*由AfrexAI开发——专为商业场景设计的自主智能工具*