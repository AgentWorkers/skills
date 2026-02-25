---
name: Executive Coaching & Leadership Development Engine
description: 完整的执行教练系统——包括领导力评估、360度反馈、教练辅导活动、领导力发展计划、团队效能提升、高管形象塑造以及继任计划。该系统适用于领导力辅导、高管发展项目、团队建设、绩效提升以及职业转型等场景。
metadata:
  category: role
  skills: ["coaching", "leadership", "executive-development", "360-feedback", "team-effectiveness", "succession-planning", "executive-presence", "performance", "career-transition"]
---
# 执行教练与领导力发展引擎

这是一套完整的领导力辅导方法论，适用于各个层级的领导者——从初出茅庐的经理到高管团队。涵盖领导力评估、发展计划、辅导对话、团队效能、高管形象以及继任规划等方面。

---

## 第一阶段：领导力评估与基线

### 快速领导力健康检查 (/8)

每个维度的评分范围为0-2（0=薄弱，1=发展中，2=强大）：

| 维度 | 评分 | 依据 |
|---------|------|--------|
| 战略清晰度 |      | 能否在30秒内清晰阐述三年愿景？ |
| 决策速度 |      | 能否在合理时间内做出决策？ |
| 团队发展 |      | 直属下属是否得到成长并得到晋升？ |
| 沟通影响力 |      | 信息是否被立即理解并付诸行动？ |
| 自我意识 |      | 是否了解自己的盲点并主动管理？ |
| 结果交付 |      | 是否始终达到或超过目标？ |
| 利益相关者信任 |      | 在整个组织中有支持者吗？ |
| 能量管理 |      | 能够保持可持续的工作节奏，避免过度劳累？ |

**评分解读：**
- 14-16分：表现优异的领导者——专注于提升领导力与留下长期影响 |
- 10-13分：基础扎实——需要在2-3个领域进行针对性发展 |
- 6-9分：需要发展——需要系统的辅导支持 |
- 0-5分：情况危急——需要密集的支持 |

### 领导力评估简报

```yaml
leader_profile:
  name: ""
  role: ""
  level: "" # IC → Manager → Director → VP → C-Suite
  tenure_in_role: ""
  direct_reports: 0
  org_size: 0 # total people in their org
  
context:
  company_stage: "" # startup/growth/mature/turnaround
  industry: ""
  current_challenges: []
  recent_changes: [] # reorg, new boss, M&A, layoffs
  
assessment:
  strengths: # things they do well consistently
    - strength: ""
      evidence: ""
  development_areas: # things limiting their impact
    - area: ""
      impact: "" # how this shows up day-to-day
      root_cause: "" # underlying driver
  derailers: # behaviors that could end their career
    - behavior: ""
      trigger: "" # when it shows up
      risk_level: "" # low/medium/high/critical
      
leadership_style:
  primary: "" # visionary/coaching/affiliative/democratic/pacesetting/commanding
  secondary: ""
  overused: "" # style used too much
  underused: "" # style needed but avoided
  
stakeholder_perception:
  boss_view: ""
  peer_view: ""
  direct_report_view: ""
  cross_functional_view: ""
```

### 不同层级应关注的焦点

| 层级 | 主要关注点 | 次要关注点 | 需避免的误区 |
|--------|--------------|-----------------|---------------|
| 新经理 | 授权、反馈、一对一沟通 | 团队规范、招聘 | 代替管理者去做下属的工作 |
| 高级经理 | 战略规划、跨团队影响力 | 人才培养、绩效指标 | 过度管理经验丰富的下属 |
| 经理 | 组织架构设计、高管沟通 | 政治博弈、预算管理 | 过度参与具体执行 |
| 副总裁 | 愿景规划、企业文化 | 并购、利润与损失责任 | 试图管理所有团队 |
| 高管团队 | 企业战略、外部形象 | 董事会管理、继任规划 | 与团队脱节 |

---

## 第二阶段：360度反馈系统

### 360度反馈调查设计

**评分者选择规则：**
- 经理：1人（必填）
- 同事：3-5人（跨职能团队优先）
- 直属下属：如果人数少于8人，则全部参与；人数较多时随机抽取5-8人 |
- 上级：2-3人（可选，但能提供重要信息）
- 外部利益相关者：1-2人（客户、董事会成员、合作伙伴）
- 自我评估：必须包含

**核心能力评估问题（评分1-5分 + 开放式评论）**

```yaml
strategic_thinking:
  - "Sets clear direction that aligns with business strategy"
  - "Anticipates market/competitive changes and adapts"
  - "Makes sound decisions with incomplete information"
  - "Balances short-term execution with long-term vision"

people_leadership:
  - "Creates an environment where people do their best work"
  - "Develops talent — direct reports grow under their leadership"
  - "Gives honest, actionable feedback regularly"
  - "Builds diverse, high-performing teams"
  - "Handles conflict directly and constructively"

execution:
  - "Delivers results consistently"
  - "Sets clear priorities and says no to distractions"
  - "Removes obstacles for their team"
  - "Holds people accountable without micromanaging"

communication:
  - "Communicates clearly — messages are understood first time"
  - "Listens genuinely — people feel heard"
  - "Adapts communication style to the audience"
  - "Handles difficult conversations with courage and empathy"

influence:
  - "Builds strong relationships across the organization"
  - "Persuades through logic and empathy, not authority"
  - "Navigates organizational politics effectively"
  - "Represents their team's interests to leadership"

self_leadership:
  - "Shows self-awareness about strengths and limitations"
  - "Remains calm and composed under pressure"
  - "Admits mistakes and learns from them"
  - "Models the behaviors they expect from others"
```

**开放式问题（必填）：**
1. “这位领导者应该开始做什么？”
2. “这位领导者应该停止做什么？”
3. “这位领导者应该继续做什么？”
4. “他们作为领导者的最大优势是什么？”
5. “如果改变哪一点，会对他们产生最大的影响？”

### 360度反馈反馈总结框架

```yaml
debrief_structure:
  duration: "90 minutes"
  
  steps:
    1_self_assessment_first:
      - "Before showing results, ask: How do you think people perceive you?"
      - "Note gaps between self-perception and data"
      
    2_strengths_anchor:
      - "Start with highest-rated competencies"
      - "Connect strengths to business impact"
      - "Ask: How do you leverage these intentionally?"
      
    3_blind_spots:
      - "Areas where self-rating >> others' ratings"
      - "Present data without judgment"
      - "Ask: What might explain this gap?"
      
    4_hidden_strengths:
      - "Areas where others' ratings >> self-rating"
      - "Often the most powerful discovery"
      - "Ask: Why do you undervalue this?"
      
    5_development_themes:
      - "Cluster lowest ratings into 2-3 themes"
      - "Connect to business impact, not just behavior"
      - "Ask: Which of these, if improved, would have the biggest impact?"
      
    6_commitment:
      - "Select 1-2 focus areas maximum"
      - "Define specific behavioral changes"
      - "Identify accountability structure"

  rules:
    - "Never reveal individual rater responses"
    - "Present themes, not outliers"
    - "Let the leader draw conclusions before offering interpretation"
    - "Normalize emotional reactions — frustration, defensiveness, sadness are all normal"
    - "End with forward-looking energy, not backward-looking analysis"
```

---

## 第三阶段：辅导计划设计

### 辅导结构设计

```yaml
coaching_engagement:
  type: "" # developmental/performance/transition/onboarding/derailment
  duration: "" # typically 6-12 months
  frequency: "" # biweekly is standard, weekly for intensive
  session_length: "60 minutes" # 90 for first session
  
  goals: # max 3
    - goal: ""
      success_metric: "" # how we'll know it's working
      business_impact: "" # why this matters to the org
      timeline: ""
      
  stakeholders:
    sponsor: "" # usually the leader's boss
    hr_partner: ""
    check_in_cadence: "" # monthly/quarterly with sponsor
    
  boundaries:
    confidential: "Content of sessions is confidential"
    exceptions: "Safety concerns, ethics violations, or legal issues"
    sponsor_updates: "Themes and progress only, not specifics"
    
  success_criteria:
    leading_indicators: [] # behavioral changes visible in 30-60 days
    lagging_indicators: [] # business results visible in 90-180 days
    360_remeasure: "At 6 months — expecting 0.5+ point improvement on focus areas"
```

### 辅导类型决策矩阵

| 辅导类型 | 时长 | 触发条件 | 重点 | 强度 |
|--------|--------|---------|-------|-----------|
| 发展型辅导 | 6-12个月 | 高潜力员工 | 帮助其成长至更高层级 | 每两周一次 |
| 绩效辅导 | 3-6个月 | 存在绩效差距 | 解决具体问题 | 每周一次→每两周一次 |
| 转型辅导 | 3-6个月 | 新角色/新公司 | 加速适应 | 开始前90天每周一次 |
| 入职辅导 | 3个月 | 新高管入职 | 文化融合 | 每周一次 |
| 防止偏离轨道 | 3-6个月 | 面临职业危机 | 引导行为改变 | 每周一次 + 与利益相关者沟通 |

---

## 第四阶段：辅导对话技巧

### 辅导对话结构（60分钟）

```yaml
session_flow:
  check_in: # 5 min
    - "How are you arriving today? (energy/mindset)"
    - "What happened with your commitments from last session?"
    - "Score: Did you do what you said? (1-10)"
    
  agenda_setting: # 5 min
    - "What's most important for us to focus on today?"
    - "What would make this hour valuable?"
    - "If we could only solve one thing, what would it be?"
    
  exploration: # 30 min
    - "Deep dive into the topic"
    - "Use coaching models (GROW, CLEAR, etc.)"
    - "Challenge assumptions, reframe, explore options"
    
  action_planning: # 15 min
    - "What will you do differently?"
    - "What's the first step? By when?"
    - "What might get in the way?"
    - "Who else needs to be involved?"
    - "How will you know it's working?"
    
  reflection: # 5 min
    - "What was most useful about today's conversation?"
    - "What are you taking away?"
    - "Anything we need to revisit next time?"
```

### GROW模型（核心辅导框架）

```
G — Goal: "What do you want to achieve?"
  - "What does success look like specifically?"
  - "How will you know when you've reached it?"
  - "What's the timeline?"
  - "Is this within your control?"

R — Reality: "What's happening now?"
  - "What have you already tried?"
  - "What's working? What isn't?"
  - "On a scale of 1-10, where are you now?"
  - "What are you not seeing?"
  - "What would your team say about this?"

O — Options: "What could you do?"
  - "What are all the possible approaches?"
  - "What would you do if resources were unlimited?"
  - "What would [someone you admire] do?"
  - "What's the opposite of what you'd normally do?"
  - "What have you seen work in similar situations?"
  - "What if you did nothing?"

W — Will: "What will you do?"
  - "Which option resonates most?"
  - "On a scale of 1-10, how committed are you?"
  - "If less than 8, what would make it an 8?"
  - "What's the very first action?"
  - "When will you do it?"
  - "What support do you need?"
```

### 50个有效的辅导问题（按类别分类）

**自我意识：**
1. “人们与你互动时有什么感受？”
2. “你对自己有什么样的评价？”
3. “你最严厉的批评者会怎么说？其中有什么事实？”
4. “你在什么时候状态最佳？当时你在做什么？”
5. “你假装不知道什么？”
6. “你一直在重复什么模式？”
7. “如果你已经解决了这个问题，现在的你会怎么做？”

**决策能力：**
8. “在这种情况下，你会给别人什么建议？”
9. “不做决定会有什么后果？”
10. “最坏的情况会怎样？你能接受吗？”
11. “你在回避哪个决定？”
12. “如果必须在5分钟内做出决定，你会选择什么？”
13. “你的直觉告诉了你什么？你为什么不相信它？”

**勇气与行动：**
14. “你害怕发生什么？”
15. “你在回避什么样的对话？”
16. “如果你不怕，你会怎么做？”
17. “你能做的最小规模的尝试是什么？”
18. “今天就能实施的80%解决方案是什么？”
19. “如果你不这么做，你会后悔什么？”

**团队与关系：**
20. “你的团队需要你提供什么，但他们没有得到？”
21. “团队中谁遇到了困难，而你回避了与他们的对话？”
22. “你的直属下属会在背后怎么说你？”
23. “你在哪里进行救援，而不是帮助他们成长？”
24. “修复哪一种关系能带来最大的进步？”
25. “你还需要哪些资源来支持你的工作？”

**战略思维：**
26. “如果这件事做对了，其他事情会变得容易多少？”
27. “你应该停止做什么？”
28. “你在优化哪个指标上错了？”
29. “你的假设是什么？这些假设可能是错误的？”
30. “有什么事情你认为是正确的，但实际上可能并不正确？”

**能量与可持续性：**
31. “什么在消耗你的精力，你可以消除它？”
32. “你在什么情况下说了‘是’，但实际上意思是‘不’？”
33. “要以80%的精力持续工作需要什么？”
34. “你上次什么时候什么都没做？当时的感受如何？”
35. “什么能让你充满能量，但你却优先处理了其他事情？”

**成长与学习：**
36. “哪次失败让你学到了最多？”
37. “你忽略了哪些可能真实的反馈？”
38. “如果掌握了哪项技能，会改变你的发展轨迹？”
39. “你的自负在哪里阻碍了你？”
40. “现在你知道了什么，但一年前还不知道？”

**愿景与目标：**
41. “这个职位对你来说，除了薪水之外，还有什么意义？”
42 “你想在这个组织留下什么遗产？”
43 “五年后回顾时，你会为自己感到骄傲的是什么？”
44 “只有你能完成什么工作？”
45 “你有什么独特的优势，可以产生什么影响？”

**重新定义问题：**
46. “如果这个问题实际上是一个机会，会是什么样子？”
47 “如果这件事很容易解决，会是什么样子？”
48 “你为什么给它赋予了不必要的意义？”
49 “还有谁成功地处理过类似的情况？你可以从他们那里学到什么？”
50 “这种困难情况有什么积极的一面？”

### 高级辅导技巧

**谨慎地提出挑战：**
- 镜像反馈： “我注意到你说了X，但你的情绪下降了。背后是什么原因？”
- 直接提问： “我会直言不讳。数据显示的是Y。你怎么看？”
- 元分析： “我们已经连续三次讨论这个话题了。是什么让你停滞不前？”
- 假设提出： “我有一个想法。可以分享吗？[等待对方同意]”

**应对抗拒：**
- 命名抗拒： “我感觉到你有抗拒。抗拒的原因是什么？”
- 验证抗拒： “考虑到……，你有这样的感受是可以理解的。”
- 探索抗拒： “这种抗拒在保护你免受什么？”
- 利用抗拒： “为了继续前进，你需要什么条件？”

**沉默作为工具：**
- 在提出有力问题后，至少等待10秒
- 当对方说“我不知道”时，保持沉默——他们通常知道答案
- 在对方情绪激动时，给他们时间平静下来
- 当对方在处理情绪时，不要急于填补空白

**身体感知：**
- “当你提到某个话题时，你的身体有什么反应？”
- “你说出某个词时，你的情绪发生了什么变化？”
- “深呼吸一下。接下来会想到什么？”

---

## 第五阶段：领导力发展计划

### 发展计划模板

```yaml
leadership_development_plan:
  leader: ""
  date: ""
  review_date: "" # 90 days out
  
  vision:
    next_role: "" # where they're heading
    timeline: "" # realistic horizon
    gap_to_next_level: "" # biggest gap between now and next level
    
  focus_areas: # max 2-3
    - area: ""
      current_state: "" # specific behaviors today
      target_state: "" # specific behaviors in 6 months
      why_it_matters: "" # business impact
      
      development_actions:
        learn: # 10% — knowledge acquisition
          - action: ""
            resource: "" # book, course, podcast
            by_when: ""
            
        practice: # 70% — on-the-job application
          - action: "" # specific situation to practice in
            frequency: "" # daily/weekly
            success_look: "" # what good looks like
            
        connect: # 20% — feedback and relationships
          - action: "" # mentor, feedback partner, peer group
            who: ""
            cadence: ""
            
      progress_indicators:
        30_day: "" # leading indicator
        60_day: "" # early results
        90_day: "" # measurable outcome
        
  support_needed:
    from_manager: []
    from_hr: []
    from_coach: []
    stretch_assignments: []
    
  review_schedule:
    - date: "" # 30-day
      focus: "Are actions being taken? Early signals?"
    - date: "" # 60-day
      focus: "Behavioral changes visible? Adjust plan?"
    - date: "" # 90-day
      focus: "Results materializing? Set next phase?"
```

### 70-20-10%的发展行动库

**70% 在职经验：**
- 领导一个跨职能项目（超出自己的舒适区）
- 向更高级别的听众展示成果（董事会、高管团队、全体员工）
- 承担一个扭转局面的项目
- 全程管理危机或紧急情况
- 招聘并引导一位高级领导者
- 向同事或高级利益相关者提供尖锐的反馈
- 在外部场合执行战略
- 谈判重要的交易或供应商合同
- 管理超出当前职责范围的预算

**20% 关系拓展（增加曝光度）：**
- 跟随一位高管团队工作一周
- 寻找行业外的导师
- 加入同行学习小组
- 指导一位初级员工
- 得到一位“直言不讳”的反馈者
- 本季度建立3个新的跨职能关系
- 非正式地从5位利益相关者那里获取360度反馈
- 以观察者的身份参加董事会会议

**10% 正式学习（教育培训）：**
- 参加高管培训项目（2-5天）
- 使用领导力评估工具（如Hogan、StrengthsFinder、DISC、MBTI）
- 每季度阅读2本领导力相关书籍
- 参加行业领导力会议
- 学习与本职工作无关的技能（如财务人员学习技术相关知识）

---

## 第六阶段：高管形象塑造

### 高管形象框架（4个支柱）

```yaml
executive_presence:
  gravitas: # 67% of EP — the most important
    components:
      - confidence: "Projects calm certainty without arrogance"
      - decisiveness: "Makes calls and owns them"
      - composure: "Stays steady under pressure"
      - vision: "Connects today's work to tomorrow's destination"
      - authenticity: "Consistent in public and private"
    
    development:
      - "Practice the 3-second pause before responding"
      - "Prepare your 'point of view' on every topic before meetings"
      - "Use 'I believe...' and 'My recommendation is...' not 'I think maybe...'"
      - "When challenged, acknowledge the point, then restate your position"
      - "Own mistakes immediately: 'That was my call. Here's what I learned.'"
      
  communication: # 28% of EP
    components:
      - clarity: "Simple, jargon-free, structured"
      - storytelling: "Uses narrative to make data memorable"
      - listening: "Makes others feel genuinely heard"
      - adaptation: "Adjusts style for board vs team vs 1:1"
      - brevity: "Says more with fewer words"
    
    development:
      - "Structure every message: Point → Evidence → Implication → Action"
      - "Practice the 'one headline' test — can you say it in one sentence?"
      - "Record yourself presenting — watch once a month"
      - "Ask 2 questions for every 1 statement in meetings"
      - "Use silence intentionally — pause 3 seconds after key points"
      
  appearance: # 5% of EP — least important but still matters
    components:
      - dress: "Appropriate for context, slightly above the room"
      - energy: "Projects vitality and engagement"
      - body_language: "Open posture, appropriate eye contact"
      - environment: "Organized space, professional virtual setup"
    
    development:
      - "Match dress code to the audience, not your team"
      - "Stand or use a standing desk for important calls"
      - "Eliminate filler words (um, like, you know)"
      - "Video calls: camera at eye level, good lighting, clean background"
```

### 不同情境下的形象展示指南

**董事会演讲：**
- 以提出问题或建议的方式开始——董事会不喜欢隐晦的表达
- 演示时最多使用3张幻灯片
- 预先准备5个最棘手的问题并准备好答案
- 使用“我们”来描述团队成就，使用“我”来承担责任
- 结尾时说：“我需要你们……”

**危机沟通：**
- 速度优先于完美——即使信息不完整，也要在2小时内沟通
- 结构化表达： “我们知道什么。我们在做什么。我们何时会更新你们。”
- 承担责任： “我负责……”
- 绝不说“无可奉告”——说“我会在[时间]之前提供更多信息”
- 如有承诺，一定要跟进——信誉通过实际行动来建立

**困难对话：**
- 直接面对问题： “这是一个困难的话题。我之所以提出来，是因为我尊重你。”
- 使用SBI模型： 情境 → 行为 → 影响（而非个人品质）
- 在给出建议前，先了解对方的观点
- 结束时明确承诺： “我们同意做什么？”
- 48小时内跟进

---

## 第七阶段：团队效能

### 团队健康评估（Lencioni + Google的Project Aristotle方法）

```yaml
team_assessment:
  psychological_safety: # "Can I take risks without feeling insecure?"
    score: 0 # 1-10
    signals:
      healthy: ["People admit mistakes", "Questions are welcomed", "Dissent is voiced"]
      unhealthy: ["Silence in meetings", "Blame culture", "CYA behavior"]
    actions:
      - "Leader models vulnerability: 'I was wrong about...' / 'I don't know'"
      - "Explicitly reward risk-taking, even when it fails"
      - "Ask the quietest person in the room: 'What are we missing?'"
      
  trust: # "Do I believe my teammates have my back?"
    score: 0
    signals:
      healthy: ["Candid feedback", "Asking for help", "Giving benefit of doubt"]
      unhealthy: ["Political maneuvering", "Back-channel conversations", "Guarded language"]
    actions:
      - "Personal histories exercise: 5-min vulnerability sharing in team meeting"
      - "Replace 'Why did you...' with 'Help me understand...'"
      - "Create shared experiences outside work context"
      
  healthy_conflict: # "Do we debate ideas openly?"
    score: 0
    signals:
      healthy: ["Passionate debate about ideas", "Quick resolution", "No lingering resentment"]
      unhealthy: ["Artificial harmony", "Passive-aggressive", "Decisions reopened privately"]
    actions:
      - "Assign devil's advocate role in meetings"
      - "Mining for conflict: 'We agreed too fast. What are we not considering?'"
      - "Norm: 'Disagree and commit' — debate fully, then align"
      
  commitment: # "Do we align on decisions and priorities?"
    score: 0
    signals:
      healthy: ["Clear priorities", "Fast decisions", "Unified external message"]
      unhealthy: ["Ambiguity about direction", "Revisiting decisions", "Hedging"]
    actions:
      - "End every meeting with: 'What did we decide? Who owns what? By when?'"
      - "Cascading communication: within 24 hours, everyone tells their teams"
      - "Write decisions down — 'If it's not written, it wasn't decided'"
      
  accountability: # "Do we hold each other to standards?"
    score: 0
    signals:
      healthy: ["Peer feedback flows freely", "Standards are clear", "Underperformance addressed"]
      unhealthy: ["Leader is sole accountability enforcer", "Low performers protected", "Resentment from high performers"]
    actions:
      - "Publish team commitments — transparency creates accountability"
      - "Peer feedback rounds in retrospectives"
      - "Score as a team: 'How did WE do against our commitments this quarter?'"
      
  results_focus: # "Do we prioritize collective results over individual?"
    score: 0
    signals:
      healthy: ["Shared goals", "Celebrating team wins", "Helping across boundaries"]
      unhealthy: ["Fiefdoms", "Individual credit-seeking", "Silo mentality"]
    actions:
      - "Shared OKRs that require collaboration"
      - "Recognition: praise what helps the team, not just individual brilliance"
      - "Quarterly: 'What did WE achieve?' before 'What did I achieve?'"
```

### 团队外部培训（全天）

```yaml
team_offsite:
  pre_work:
    - "Anonymous pulse survey: 3 things working, 3 things not"
    - "Each person: 1-page 'State of my world' (priorities, blockers, requests)"
    - "Pre-read on strategic context"
    
  morning: # Connection + Retrospective
    - "09:00 Check-in: Personal + professional highlight since last offsite (10 min each)"
    - "10:00 Retrospective: What's working? What isn't? What should we change?"
    - "11:00 Team health assessment: Score and discuss each dimension"
    - "12:00 Lunch together (no laptops)"
    
  afternoon: # Strategy + Commitments
    - "13:30 Strategic context: Where is the business heading? What does it mean for us?"
    - "14:30 Priority alignment: What are our 3 must-win battles this quarter?"
    - "15:30 Working agreements: How do we want to work together? (revise/create)"
    - "16:30 Commitments: Each person — 'My commitment to this team'"
    - "17:00 Reflection + Close: 'One word for how you're leaving'"
    
  follow_up:
    - "Share notes within 48 hours"
    - "30-day check-in on commitments"
    - "Quarterly pulse survey to track health trends"
```

---

## 第八阶段：职业转型与高管入职辅导

### 新领导者的前90天计划

```yaml
transition_plan:
  first_30_days: # LEARN
    theme: "Listen and learn — resist the urge to change things"
    actions:
      - "Meet every direct report 1:1 (60 min each)"
      - "Meet every peer and key stakeholder (30 min each)"
      - "Meet skip-levels in small groups"
      - "Learn the business: financials, customers, products, competitive landscape"
      - "Identify 3 quick wins — things you can fix that build credibility"
      - "DO NOT reorganize, fire anyone, or change processes yet"
    questions_to_ask_everyone:
      - "What's working well that I should protect?"
      - "What's broken that needs fixing?"
      - "What would you do if you had my role?"
      - "What don't I know that I should?"
      - "What are you worried I might do?"
      
  days_31_60: # ALIGN
    theme: "Form your point of view and align with stakeholders"
    actions:
      - "Present your diagnosis to your boss: 'Here's what I've learned'"
      - "Draft strategic priorities (3 max)"
      - "Identify talent: A-players (invest), B-players (develop), wrong-seat (move)"
      - "Execute quick wins — build credibility through action"
      - "Establish your team rhythms (meetings, 1:1s, reporting)"
      
  days_61_90: # ACT
    theme: "Make your mark — implement first meaningful changes"
    actions:
      - "Communicate your strategic priorities to the team"
      - "Make necessary people decisions (role changes, hiring, performance conversations)"
      - "Launch 1 signature initiative that signals your direction"
      - "90-day review with boss: 'Here's what I've done, here's what's next'"
      - "Adjust development plan based on what you've learned"
      
  common_traps:
    - "Trap: Bringing your old playbook. Fix: This is a new context — diagnose first."
    - "Trap: Trying to please everyone. Fix: You can't — make the hard calls."
    - "Trap: Going too fast. Fix: Trust takes time. Earn it before spending it."
    - "Trap: Going too slow. Fix: If you haven't made a visible change by Day 60, you've waited too long."
    - "Trap: Ignoring the culture. Fix: How things get done matters as much as what gets done."
```

### 职业转型辅导（不同层级）

| 转型 | 关键思维转变 | 常见错误 |
|--------|-------------------|-------------------|
| 直属下属 → 经理 | “我的成功 = 他们的成功” | 专注于工作本身，忽视团队发展 |
| 经理 → 经理 | “通过管理者来管理团队” | 跳过中间层级，过度管理 |
| 经理 → 副总裁 | “只关注结果，忽略方法” | 过度参与战术决策 |
| 副总裁 → 高管团队 | “企业利益优先，部门利益其次” | 只为自己的部门发声 |
| 高管团队 → 首席执行官 | “你是企业的象征” | 低估个人行为的象征意义 |
| 企业高管 → 初创企业 | “边飞行边建造飞机” | 过度规划，等待完美信息 |

## 第九阶段：继任规划

### 继任准备评估

```yaml
succession_plan:
  critical_roles: # positions where vacancy = significant business risk
    - role: ""
      incumbent: ""
      flight_risk: "" # low/medium/high
      
      successors:
        ready_now: # could step in within 30 days
          - name: ""
            readiness: "" # percentage
            gaps: []
            development_plan: ""
            
        ready_1_2_years:
          - name: ""
            readiness: ""
            gaps: []
            development_plan: ""
            
        emergency_backup: # if incumbent leaves tomorrow
          name: ""
          plan: "" # what happens day 1

  bench_strength_score:
    roles_with_ready_now_successor: 0
    roles_with_1_2_year_successor: 0
    roles_with_no_successor: 0
    overall_readiness: "" # strong/adequate/at-risk/critical

  actions:
    - "Review succession plan quarterly"
    - "Give successors stretch assignments aligned to gaps"
    - "Cross-train across functions"
    - "Engage external search firms for critical roles with no internal successor"
```

### 9-box人才评估

```
                    Low Performance    Medium Performance    High Performance
High Potential    │ Potential Gem     │ High Potential       │ Star
                  │ Invest or move    │ Accelerate dev       │ Stretch & retain
                  │─────────────────── ──────────────────── ────────────────────
Medium Potential  │ Underperformer    │ Core Player          │ High Performer
                  │ PIP or redeploy   │ Develop in role      │ Expand scope
                  │─────────────────── ──────────────────── ────────────────────
Low Potential     │ Wrong Seat        │ Solid Contributor    │ Mastery Expert
                  │ Exit              │ Maintain             │ Leverage expertise
```

**评估规则：**
- 永远不要将超过20%的人评为“明星”——否则会导致评价膨胀
- “定位不当”的人需要在90天内采取行动——不要长期保留他们
- “潜力股”有最多6个月的时间来展示进步
- “核心成员”是团队的支柱——不要忽视他们的成长
- 每季度重新评估9-box评估结果，每年进行一次调整

---

## 第十阶段：辅导效果评估与投资回报

### 辅导效果仪表盘

```yaml
coaching_metrics:
  engagement_health:
    sessions_completed: 0
    sessions_cancelled: 0
    completion_rate: "" # target: >90%
    commitment_completion_rate: "" # actions taken / actions committed
    
  behavioral_change: # measured at 30/60/90 days
    self_reported_progress: "" # 1-10
    stakeholder_observed_change: "" # 1-10 (from sponsor/HR)
    360_score_change: "" # delta from baseline
    
  business_impact:
    team_engagement_delta: "" # survey score change
    retention_of_direct_reports: "" # 12-month retention rate
    team_performance_metrics: "" # revenue, NPS, delivery, etc.
    promotion_readiness: "" # is leader closer to next level?
    
  roi_calculation:
    coaching_investment: 0 # total cost (coach fee + leader time)
    value_created: 0 # estimated from retention + performance + averted risks
    roi_percentage: "" # (value - cost) / cost × 100
    
  qualitative:
    leader_testimonial: ""
    sponsor_assessment: ""
    most_significant_change: ""
```

### 投资回报证据类型

| 证据 | 测量方法 | 典型影响 |
|--------|------------|-------------------|
| 关键人才的保留 | 保留的直属下属数量与基线对比 | 每保留一人可节省5万至20万美元 |
| 决策速度加快 | 从发现问题到做出决策的时间 | 提高竞争力，加快市场响应速度 |
| 团队生产力 | 产出指标、工作效率、人均收入 | 通常可以提高10-30% |
| 减少冲突 | 用于处理人际问题的时间 | 每周节省2-5小时 |
| 改善利益相关者关系 | 客户满意度、360度反馈、导师评价 | 释放资源，消除障碍 |
| 继任准备情况 | 内部晋升率、人才储备 | 每避免一次外部招聘可节省10万美元以上 |

## 第十一阶段：复杂辅导场景

### 五种常见辅导挑战

**1. 抵抗型领导者（“我不需要辅导”）**
```
- Don't argue — meet them where they are
- Ask: "What would make this time worthwhile for you?"
- Reframe: "Think of this as a strategic thinking partner, not remediation"
- Find their motivation: "What would you like to be even better at?"
- Quick win: Solve one problem they care about → credibility earned
```

**2. 多话型领导者（会议中喋喋不休，缺乏深度）**
```
- Notice the pattern: "I notice we cover a lot of ground but don't go deep. What's that about?"
- Use structured tools: "Give me 3 bullet points, then we'll explore the most important one"
- Direct interrupt: "I want to stop you here because something important just came up"
- Assign reflective pre-work: "Come to our next session with one question you don't know the answer to"
```

**3. 完美主义型领导者（被标准束缚）**
```
- Normalize: "Your high standards got you here. AND they might be the ceiling now"
- Reframe: "What's the cost of waiting for perfect?"
- Experiment: "Ship one thing at 80% this week. Observe what happens"
- Identity work: "You ARE successful even when something isn't perfect"
- Track: Log the outcome of 80% efforts vs 100% efforts — data beats fear
```

**4. 过分讨好型领导者（避免冲突，过度承诺）**
```
- Name the pattern: "You seem to say yes to everything. What's driving that?"
- Explore the cost: "What are you sacrificing by never saying no?"
- Practice: Role-play declining a request — start with low-stakes
- Reframe: "Every yes to someone else is a no to something you care about"
- Assignment: Say no once this week. Report back on what happened (usually nothing bad)
```

**5. 优秀但行为不当的领导者（虽然成果显著，但方式不当）**
```
- Don't lead with behavior — lead with impact: "Your team's attrition is 2x the company average. What's your theory?"
- Connect to their goals: "You want to be VP. VPs need organizations that scale. People leave you."
- Specific incidents: "In the meeting Tuesday, when you said X, here's what happened..."
- Not optional: "This isn't about being nice. It's about whether you can lead at the next level"
- Consequences: "Without change, here's the likely outcome in 12 months..."
```

### 何时结束辅导关系

| 信号 | 应对措施 |
|--------|--------|
| 3-4次辅导后没有进展 | 直接沟通：“是什么阻碍了你的进步？” |
| 领导者未能履行承诺 | 重新协商或结束辅导关系——不要浪费时间 |
| 目标达成 | 庆祝并制定后续计划 |
| 辅导变成心理治疗 | 建议寻求专业帮助——这是辅导的界限 |
| 信任破裂（领导者撒谎或存在道德问题） | 直接处理——可能需要结束辅导关系 |
| 组织变动（重组、人员变动） | 重新评估辅导范围和目标 |

## 第十二阶段：辅导质量评估

### 100分制辅导质量评分标准

| 评估维度 | 权重 | 评分标准 |
|---------|--------|-------------------|
| 评估深度 | 15分 | 全面覆盖360度评估、自我评估和利益相关者反馈 |
| 目标明确性 | 15分 | 目标与业务影响紧密相关 |
| 对话质量 | 20分 | 问题具有挑战性，能引发深刻思考 |
| 发展计划 | 15分 | 包含明确的目标和里程碑 |
| 行为改变 | 15分 | 利益相关者报告有明显变化 |
| 利益相关者管理 | 10分 | 导师积极参与并保持一致 |
| 投资回报证据 | 10分 | 有量化的业务成果 |

**总分：/100**
- 90-100分：具有变革性的辅导效果 |
- 75-89分：效果显著，执行到位 |
- 60-74分：起步良好，需要进一步深化 |
- 60分以下：需要重新考虑辅导方法 |

### 常见辅导误区**

1. **过度提供建议** —— 只顾告诉对方答案，而不引导思考。
2. **关系变得像朋友** —— 辅导变成了闲聊。
3. **回避棘手问题** —— 回避真正需要解决的问题。
4. **比客户更努力** —— 如果你投入过多，可能说明方法有问题。
5 **确认偏误** —— 只听符合自己假设的信息。
6 **过度干预** —— 代替对方解决问题，而不是帮助他们成长。
7 **依赖工具** —— 依赖评估工具，而忽视真正的对话。
8 **忽视整体情况** —— 只关注个体，忽略其所处的环境。
9 **缺乏评估** —— 无法证明辅导效果。
10 **无止境的辅导** —— 辅导没有明确的结束点。

---

### 自然语言指令

该系统支持以下指令：
- “评估[领导者姓名]的领导力” → 运行第一阶段的评估
- “为[姓名]设计360度反馈调查” → 生成第二阶段的调查
- “安排辅导关系” → 设计第三阶段的辅导计划
- “就[主题]进行辅导” → 进行GROW模型辅导
- “为[姓名]制定发展计划” → 生成第五阶段的计划
- “帮助我提升高管形象” → 制定第六阶段的辅导计划
- “评估我的团队状况” → 进行第七阶段的团队评估
- “规划我的前90天” → 制定第八阶段的入职计划
- “制定继任计划” → 制定第九阶段的计划
- “评估辅导效果” → 运用第十阶段的评估工具
- “帮助我应对困难领导者” → 应对第十一阶段的挑战
- “评估这次辅导的效果” → 使用第十二阶段的评分标准