# 面试架构师

这是一个完整的招聘面试系统，涵盖了从职位评分卡设计到结构化问题库、现场评估标准、面试小组协调以及最终录用决策的全过程。该系统通过基于证据的框架来消除主观的招聘判断，从而预测候选人在工作中的表现。

## 快速入门

告诉我您的需求：
- “为[职位]设计面试流程” → 提供完整的面试计划（评分卡 + 问题 + 评估标准）
- “为[职位]创建评分卡” → 明确A级候选人的标准及可衡量的成果
- “为[技能/能力]生成问题” → 生成针对性的问题库
- “为[职位]设计带回家的任务” → 设计包含评估标准的技术评估任务
- “评估这名候选人” → 进行结构化的面试总结并给出评分
- “审核我们的面试流程” → 检查是否存在偏见并评估流程的有效性

---

## 第一阶段：职位评分卡（在评估之前先明确标准）

**规则：在确定“优秀”的标准之前，切勿查看候选人的简历。**

### 评分卡模板

```yaml
scorecard:
  role: "[Title]"
  level: "[Junior/Mid/Senior/Staff/Principal/Director/VP]"
  team: "[Team name]"
  hiring_manager: "[Name]"
  created: "YYYY-MM-DD"

  mission:
    statement: "[One sentence: why does this role exist?]"
    success_metric: "[How we'll know this hire was successful in 12 months]"

  outcomes:
    # 3-5 specific, measurable results expected in first 12 months
    - outcome: "[e.g., Reduce deployment time from 45min to <10min]"
      measure: "[Metric: deployment duration, measured via CI/CD logs]"
      timeline: "Q1-Q2"
      priority: "critical"

    - outcome: "[e.g., Ship v2 API with 99.9% uptime]"
      measure: "[Uptime %, error rate, customer adoption]"
      timeline: "Q2-Q3"
      priority: "critical"

    - outcome: "[e.g., Mentor 2 junior engineers to mid-level competency]"
      measure: "[Promotion readiness assessment, PR quality metrics]"
      timeline: "Q3-Q4"
      priority: "important"

  competencies:
    technical:
      must_have:
        - name: "[e.g., System design]"
          level: "[Novice/Competent/Proficient/Expert]"
          evidence: "[What demonstrates this: e.g., designed systems handling 10K+ RPS]"
        - name: "[e.g., TypeScript/React]"
          level: "Proficient"
          evidence: "[Shipped production TS/React apps, not just tutorials]"
      nice_to_have:
        - name: "[e.g., Kubernetes]"
          level: "Competent"

    behavioral:
      must_have:
        - name: "Ownership"
          definition: "Takes responsibility for outcomes, not just tasks. Doesn't wait to be told."
          anti_pattern: "Says 'that's not my job' or 'I was told to do X'"
        - name: "Communication"
          definition: "Explains complex ideas simply. Writes clear docs. Raises issues early."
          anti_pattern: "Surprises stakeholders. Can't explain their own work."
        - name: "Growth mindset"
          definition: "Seeks feedback. Admits mistakes. Improves from failure."
          anti_pattern: "Defensive about criticism. Repeats same mistakes."
      nice_to_have:
        - name: "[e.g., Cross-functional leadership]"

    cultural:
      values_alignment:
        - "[Company value 1: what this looks like in practice]"
        - "[Company value 2: what this looks like in practice]"
      anti_signals:
        - "[Red flag behavior 1]"
        - "[Red flag behavior 2]"

  compensation:
    band: "[min - max]"
    equity: "[range if applicable]"
    flexibility: "[What's negotiable]"

  deal_breakers:
    # Hard no's — instant disqualification
    - "[e.g., Cannot start within 4 weeks]"
    - "[e.g., No experience with production systems at scale]"
    - "[e.g., Requires >30% above band]"
```

### 评分卡质量检查

在继续之前，请确认以下内容：
- [ ] 使命宣言是一句话（而非一段长文）
- [ ] 每个评估结果都有具体的数字或指标（而非模糊的描述，如“需要改进”或“有帮助”）
- [ ] 能力区分了必备项和可选项
- [ ] 对每种行为能力都定义了反模式（即不良行为）
- [ ] 决定性因素是客观的（而非主观感受）
- [ ] 评分等级符合市场标准（可参考Glassdoor等平台的数据）

---

## 第二阶段：面试流程设计

### 面试流程模板

```yaml
interview_loop:
  role: "[from scorecard]"
  total_duration: "[X hours across Y sessions]"
  
  stages:
    - stage: "Resume Screen"
      duration: "5-10 min"
      who: "Recruiter or hiring manager"
      evaluates: ["deal_breakers", "basic_qualification"]
      pass_rate_target: "30-40%"
      
    - stage: "Phone Screen"
      duration: "30 min"
      who: "Hiring manager"
      evaluates: ["communication", "motivation", "outcome_1_capability"]
      format: "Structured conversation"
      pass_rate_target: "50%"
      
    - stage: "Technical Assessment"
      duration: "60-90 min"
      who: "Senior engineer"
      evaluates: ["technical_competencies"]
      format: "Live coding OR take-home (see Phase 4)"
      pass_rate_target: "40-50%"
      
    - stage: "System Design"
      duration: "45-60 min"
      who: "Staff+ engineer"
      evaluates: ["system_design", "trade_off_thinking", "communication"]
      format: "Whiteboard/collaborative design"
      pass_rate_target: "50%"
      applies_to: "Senior+ only"
      
    - stage: "Behavioral Deep-Dive"
      duration: "45-60 min"
      who: "Hiring manager + cross-functional partner"
      evaluates: ["behavioral_competencies", "cultural_values"]
      format: "STAR-based structured interview"
      pass_rate_target: "60%"
      
    - stage: "Team Fit / Reverse Interview"
      duration: "30 min"
      who: "2-3 potential teammates"
      evaluates: ["collaboration_style", "candidate_questions"]
      format: "Informal but structured"
      pass_rate_target: "80%"
      
    - stage: "Hiring Manager Final"
      duration: "30 min"
      who: "Hiring manager"
      evaluates: ["remaining_concerns", "motivation", "offer_readiness"]
      format: "Conversation"

  timeline:
    screen_to_onsite: "< 5 business days"
    onsite_to_decision: "< 2 business days"
    decision_to_offer: "< 1 business day"
    total_process: "< 3 weeks"
```

### 根据职位级别调整面试流程

| 职位级别 | 可省略的环节 | 需添加的环节 | 重点关注的内容 |
|---------|-------------|----------------|-------------------|
| 初级（0-2年经验） | 系统设计 | 代码协作、学习能力 | 更注重潜力而非经验 |
| 中级（2-5年经验） | — | — | 平衡执行能力和成长潜力 |
| 高级（5-8年经验） | — | 架构讨论 | 影响力、责任心、指导能力 |
| 主管级（8年以上经验） | 基本编码能力 | 设计文档审查、战略规划能力 | 影响力和技术视野 |
| 经理级 | 基本编码能力 | 战略规划展示 | 对组织的影响 |
| 总监级及以上 | 所有核心技术能力 | 组织管理和领导力展示 | 对业务的影响 |

---

## 第三阶段：问题库

### 行为问题（STAR格式）

**对于以下每个问题：**
- 首先提出核心问题
- 然后追问：“请具体描述你是如何做的”
- 接着追问：“具体的结果是什么？”
- 注意：避免模糊的回答，以及使用“我们”而非“我”这样的表述，同时要确认候选人能否回忆起具体细节

#### 责任感与主动性

```
Q: "Tell me about a time you identified a problem no one asked you to fix, and you fixed it anyway."
  Probe: "How did you discover it? What did you do first? What was the outcome?"
  Green signal: Specific problem, proactive action, measurable impact
  Red flag: Can't recall an example, or problem was trivial

Q: "Describe a project that failed or didn't meet expectations. What was your role?"
  Probe: "What would you do differently? What did you learn?"
  Green signal: Owns their part, specific lessons, changed behavior afterward
  Red flag: Blames others, no learning, defensive

Q: "Tell me about the last time you disagreed with your manager's technical decision."
  Probe: "How did you raise it? What happened? Would you do it differently?"
  Green signal: Respectful pushback with data, compromise or acceptance
  Red flag: Never disagrees, or went around manager, or still bitter
```

#### 沟通与协作

```
Q: "Describe the most complex technical concept you had to explain to a non-technical audience."
  Probe: "How did you know they understood? What would you change?"
  Green signal: Adapts language, checks understanding, uses analogies
  Red flag: Talks down, uses jargon anyway, frustrated by the need

Q: "Tell me about a cross-team project that had conflicting priorities."
  Probe: "How did you align the teams? What trade-offs were made?"
  Green signal: Proactive communication, documented agreements, escalated appropriately
  Red flag: Waited for someone else to resolve, or steamrolled

Q: "Give me an example of written communication that had significant impact."
  Probe: "What was the context? Who was the audience? What resulted?"
  Green signal: Design doc, RFC, post-mortem that changed decisions
  Red flag: Can't think of one, or only Slack messages
```

#### 技术卓越性

```
Q: "What's the best piece of code or system you've built? Walk me through it."
  Probe: "What trade-offs did you make? What would you change now?"
  Green signal: Deep understanding, clear trade-off reasoning, honest about flaws
  Red flag: Can't go deep, no awareness of trade-offs

Q: "Tell me about a production incident you were involved in resolving."
  Probe: "How did you diagnose it? What was root cause? What prevented recurrence?"
  Green signal: Systematic debugging, root cause fix (not band-aid), prevention measures
  Red flag: Only applied quick fix, blamed infrastructure, no follow-up

Q: "Describe a time you had to make a technical decision with incomplete information."
  Probe: "What did you know? What didn't you know? How did you decide?"
  Green signal: Explicit about unknowns, gathered what they could, made reversible decision
  Red flag: Paralyzed, or overconfident without data
```

#### 领导力与指导能力（针对高级职位）

```
Q: "Tell me about someone you helped grow significantly in their career."
  Probe: "What did you specifically do? How did you know it was working?"
  Green signal: Specific actions (pair programming, stretch assignments, feedback), measurable growth
  Red flag: "I told them what to do" or can't name anyone

Q: "Describe a technical strategy or vision you set for your team."
  Probe: "How did you get buy-in? How did you measure progress?"
  Green signal: Clear rationale, stakeholder alignment, adapted based on feedback
  Red flag: Top-down mandate, or never set direction

Q: "Tell me about a time you had to say no to a stakeholder or product request."
  Probe: "How did you explain it? What was the outcome?"
  Green signal: Data-driven reasoning, offered alternatives, maintained relationship
  Red flag: Just said no, or always says yes
```

### 面试中的简历验证问题（压力测试）

针对简历中的亮点，设计相应的验证问题：

```
Pattern: "[Impressive claim on resume]"
→ "Walk me through [specific project]. What was the state when you joined?"
→ "What was YOUR specific contribution vs the team's?"
→ "What was the hardest technical problem YOU solved?"
→ "If I called your manager from that time, what would they say was your biggest weakness?"

Pattern: "Led team of X"
→ "How many people reported to you directly?"
→ "Name someone you had to give tough feedback to. What happened?"
→ "Who was the weakest performer? What did you do about it?"

Pattern: "Improved X by Y%"
→ "What was the baseline measurement? How did you measure it?"
→ "What was it before you started? After? How long did it take?"
→ "What else changed during that period that could explain the improvement?"

Pattern: "Short tenure (< 1 year)"
→ "Walk me through your decision to leave [company]."
→ "What would your manager there say about your departure?"
→ "What did you learn from that experience?"

Pattern: "Gap in employment"
→ Ask once, move on. Don't dwell. Valid reasons: health, family, travel, learning, job market.
→ Red flag only if: story keeps changing, or they're evasive about a very long gap
```

### 未来模拟问题（预测候选人表现）

根据实际职位的要求，设计模拟场景的问题：

```
Template:
"In this role, one of your first challenges will be [outcome from scorecard].
The current situation is [honest context]. 
Walk me through how you'd approach this in your first [timeframe]."

Example (Senior Backend):
"Our API currently handles 2K RPS but we need to scale to 50K by Q3.
The codebase is a 3-year-old Node.js monolith with PostgreSQL.
Budget for infrastructure is $10K/mo. Team is 4 engineers including you.
How would you approach this?"

Probe sequence:
1. "What would you do in week 1?" (Information gathering)
2. "What data would you need?" (Analytical thinking)
3. "What are the biggest risks?" (Risk awareness)
4. "If [constraint changes], how does your approach change?" (Adaptability)
5. "How would you communicate progress to stakeholders?" (Communication)

Scoring:
5 — Structured approach, asks clarifying questions, identifies trade-offs, realistic timeline
4 — Good approach with minor gaps
3 — Reasonable but generic, doesn't probe assumptions
2 — Jumps to solution without understanding problem
1 — No coherent approach, or unrealistic
```

---

## 第四阶段：技术评估

### 现场编码评估

```yaml
coding_assessment:
  duration: "60 min"
  structure:
    warm_up: "5 min — environment setup, introduce the problem"
    problem_1: "20 min — core implementation"
    problem_2: "25 min — extension or new problem"
    debrief: "10 min — trade-offs discussion"

  problem_design_rules:
    - Solvable in the time limit (test it yourself first — halve your time)
    - Multiple valid approaches (no single "right answer")
    - Extension points for stronger candidates
    - Relevant to actual work (not algorithm puzzles unless role requires it)
    - Candidate chooses their language
    - Provide starter code / boilerplate to reduce setup time

  evaluation_rubric:
    problem_solving:
      5: "Breaks down problem, considers edge cases upfront, efficient approach"
      3: "Gets to solution but misses edge cases or takes indirect path"
      1: "Struggles to break down problem, no clear approach"
    
    code_quality:
      5: "Clean, readable, well-named, handles errors, testable"
      3: "Works but messy, some error handling, reasonable naming"
      1: "Barely works, no error handling, unclear naming"
    
    communication:
      5: "Thinks aloud, explains trade-offs, asks clarifying questions"
      3: "Some explanation, responds to prompts"
      1: "Silent, defensive about suggestions, doesn't explain reasoning"
    
    testing_awareness:
      5: "Writes tests unprompted, considers edge cases, talks about test strategy"
      3: "Writes tests when prompted, covers happy path"
      1: "No testing consideration"
    
    speed_and_fluency:
      5: "Fast, clearly experienced, language/tooling fluent"
      3: "Reasonable pace, occasional lookups"
      1: "Very slow, struggles with syntax/tooling"

  do_not:
    - Ask trick questions or gotchas
    - Time pressure beyond reasonable
    - Penalize for looking things up
    - Judge IDE/editor choice
    - Ask questions that require proprietary knowledge
```

### 带回家的任务评估

```yaml
take_home:
  time_limit: "3-4 hours (honor system, state clearly)"
  deadline: "5-7 days from send"
  
  problem_design:
    - Real-world scenario (not academic)
    - Clear requirements with defined scope
    - Extension section for candidates who want to show more
    - Starter repo with CI, linting, test framework pre-configured
    
  deliverables:
    required:
      - Working solution
      - Tests (at minimum: happy path + 2 edge cases)
      - README explaining approach, trade-offs, what you'd improve
    optional:
      - Architecture diagram
      - Performance analysis
      - Additional features from extension section
  
  evaluation_rubric:
    functionality: "30% — Does it work? Edge cases handled?"
    code_quality: "25% — Clean, readable, maintainable, well-structured"
    testing: "20% — Coverage, meaningful tests, edge cases"
    documentation: "15% — README quality, trade-off explanations"
    extras: "10% — Extension features, thoughtful additions"

  anti_gaming:
    - Check git history (single mega-commit = suspicious)
    - Ask about implementation details in follow-up interview
    - Vary the problem slightly across candidates
    - Time the follow-up discussion: over-engineered solutions + can't explain = red flag
```

### 系统设计评估（针对高级职位）

```yaml
system_design:
  duration: "45-60 min"
  structure:
    requirements: "10 min — clarify scope, constraints, scale"
    high_level: "15 min — components, data flow, API design"
    deep_dive: "15 min — pick 1-2 areas to go deep"
    trade_offs: "10 min — discuss alternatives, failure modes"
    extensions: "5 min — how would this evolve?"

  evaluation:
    requirements_gathering:
      5: "Asks about scale, users, latency requirements, budget before designing"
      3: "Some clarifying questions but misses key constraints"
      1: "Jumps straight to drawing boxes"
    
    high_level_design:
      5: "Clear components with well-defined boundaries, data flows make sense"
      3: "Reasonable architecture but some unclear responsibilities"
      1: "Vague boxes with arrows, can't explain data flow"
    
    depth:
      5: "Deep knowledge in chosen area, considers failure modes, cites real experience"
      3: "Good knowledge but stays surface level"
      1: "Can't go deep on any component"
    
    trade_off_awareness:
      5: "Explicitly names trade-offs, compares alternatives, knows when each fits"
      3: "Acknowledges trade-offs when prompted"
      1: "Presents one approach as the only option"
    
    scalability:
      5: "Considers growth path, bottleneck identification, realistic scaling strategy"
      3: "Basic scaling awareness"
      1: "No consideration of scale or unrealistic assumptions"
```

---

## 第五阶段：评估与决策

### 面试官个人评分卡

```yaml
interviewer_scorecard:
  candidate: "[name]"
  interviewer: "[name]"
  stage: "[which interview]"
  date: "YYYY-MM-DD"
  
  # Score BEFORE reading other interviewers' feedback
  overall: 1-5  # 1=Strong No, 2=Lean No, 3=Neutral, 4=Lean Yes, 5=Strong Yes
  
  competency_scores:
    - competency: "[from scorecard]"
      score: 1-5
      evidence: "[Specific quote or behavior observed]"
      
    - competency: "[from scorecard]"
      score: 1-5
      evidence: "[Specific quote or behavior observed]"
  
  green_signals:
    - "[Specific positive indicator with evidence]"
    
  red_flags:
    - "[Specific concern with evidence]"
    
  questions_for_next_interviewer:
    - "[What to probe further]"

  # IMPORTANT: Submit before debrief. Do not change after discussion.
```

### 面试总结流程

```
1. BEFORE debrief:
   - All interviewers submit scorecards independently
   - Hiring manager collects but does NOT share scores

2. DEBRIEF structure (30-45 min):
   a. Each interviewer states their overall vote FIRST (no explanation yet)
      → This prevents anchoring bias from persuasive speakers
   
   b. Lowest scorer goes first (explain concerns)
      → Prevents positive bias from drowning out concerns
   
   c. Highest scorer responds
   
   d. Open discussion — focus on EVIDENCE not feelings
      → "They seemed smart" is not evidence
      → "They designed a cache invalidation strategy that handled..." IS evidence
   
   e. Address conflicting signals:
      → If strong yes + strong no on same competency, that's the discussion
      → Resolve with: "What specific behavior did you observe?"
   
   f. Final vote (all interviewers):
      → Strong Hire / Hire / No Hire / Strong No Hire
      → Any "Strong No Hire" triggers discussion but NOT automatic rejection
      → Hiring manager makes final call but must document reasoning

3. AFTER debrief:
   - Decision recorded with reasoning
   - Feedback compiled for candidate (regardless of outcome)
   - Action items assigned (offer prep or rejection with feedback)
```

### 评分决策矩阵

```
Strong Hire (all 4-5):
  → Make offer within 24 hours
  → Expedite process — strong candidates have multiple offers

Hire (mix of 3-5, no 1s):
  → Make offer within 48 hours
  → Address any 3-scores with targeted onboarding plan

Borderline (mix of 2-4):
  → Additional data needed — one more focused interview on weak areas
  → Set a deadline: if still borderline after additional data → No Hire
  → "When in doubt, don't hire" — the cost of a bad hire > cost of continuing search

No Hire (any 1, or multiple 2s):
  → Decline with specific, constructive feedback
  → Document clearly for future reference (candidate may reapply)

Strong No Hire (multiple 1s or deal breaker):
  → Immediate decline
  → Review: did we miss this in screening? Fix the funnel.
```

---

## 第六阶段：偏见缓解

### 面试前的偏见检查

```
Before each interview, remind yourself:
□ I will evaluate against the SCORECARD, not my "gut feeling"
□ I will give the same weight to disconfirming evidence as confirming
□ I will not let one great/terrible answer color the entire evaluation
□ I will not compare this candidate to the last one — compare to the scorecard
□ I will note specific behaviors, not general impressions
□ I will not evaluate "culture fit" as "would I have a beer with them"
```

### 常见的招聘偏见

| 偏见类型 | 表现形式 | 缓解方法 |
|---------|------------------|-------------------|
| **光环效应** | 仅因编码能力强就认为其他方面也强 | 独立评估每个能力 |
| ** horns效应** | 因沟通能力弱就认为技术能力也弱 | 同样独立评估每个能力 |
| **相似性偏见** | 因候选人与面试官相似就给予较高评价 | 根据评分卡进行评估 |
| **锚定效应** | 第一印象影响后续评价 | 在所有问题结束后再给出评分 |
| **确认偏误** | 仅看到积极方面就给予高评价 | 主动寻找相反的证据 |
| **对比效应** | 在遇到表现不佳的候选人后，对其他候选人评价偏高 | 与评分卡对比进行评估 |
| **近期偏见** | 只记得候选人的最后回答 | 面试过程中详细记录所有信息 |
| **归因错误** | 将成功归因于个人能力，将失败归因于环境 | 深入探究原因：“哪里出了问题？什么起到了帮助作用？” |
| **宽容偏见** | 为避免冲突而给予较高评分 | 强制使用1-5分的评分标准 |
| **紧迫偏见** | 因急需人才而降低评分标准 | 延长评估时间，避免仓促决策 |

### 结构化面试规则

1. **同一职位使用相同的问题** — 所有候选人都会被问到相同的核心问题
2. **立即评分** — 在与任何人讨论之前完成评分
3. **仅基于事实** — 每个评分都需要具体的观察依据
4. **多元化的面试小组** — 至少有一名来自不同团队或背景的面试官
5. **匿名化简历筛选** — 在初步筛选时隐藏姓名、学校和公司名称（如果可能的话）
6. **避免引导性问题** — 如“你可能在X方面很出色，对吧？”这样的问题
7. **设定时间限制** — 所有候选人的面试时间相同（不要根据直觉缩短或延长）

---

## 第七阶段：候选人反馈

### 每个阶段后的沟通模板

**在每个环节结束后24小时内：**

```
ADVANCING:
"Hi [name], thank you for your time today. We enjoyed our conversation about [specific topic]. 
We'd like to move forward with [next stage]. [Interviewer name] will be speaking with you 
about [topic]. Available times: [options]. 
Any questions before then? — [recruiter name]"

REJECTION (after phone screen):
"Hi [name], thank you for taking the time to speak with us about [role].
After careful consideration, we've decided not to move forward at this stage.
[One specific, constructive piece of feedback if appropriate].
We'll keep your information on file and may reach out for future opportunities that 
align more closely. Wishing you the best in your search. — [name]"

REJECTION (after onsite):
"Hi [name], thank you for investing [X hours] in our interview process.
We were impressed by [specific positive], but ultimately decided to move forward 
with a candidate whose [specific competency] more closely matches our current needs.
Feedback: [1-2 specific, actionable items].
We genuinely appreciated your time and would welcome a future conversation 
if circumstances change. — [hiring manager name]"

OFFER (verbal, then written within 24h):
"Hi [name], I'm excited to share that we'd like to offer you the [role] position.
We were particularly impressed by [specific evidence from interviews].
Here's what we're proposing: [comp summary]. I'll send the formal offer letter 
within 24 hours. Do you have any initial questions? — [hiring manager]"
```

### 候选人反馈评分卡

每次招聘完成后（以及每季度对所有候选人进行评估）：

| 评估维度 | 目标值 | 评估方法 |
|---------|----------------|-------------------|
| 面试安排时间 | 各环节之间间隔不超过48小时 | 通过ATS系统记录 |
| 面试官的准备情况 | 面试前是否完全阅读了评分卡 | 面试后通过调查问卷收集 |
| 反馈的及时性 | 在24小时内回复 | 通过ATS系统记录 |
| 反馈的质量 | 具体且具有可操作性 | 通过候选人调查问卷收集 |
| 总体体验 | 评分4分以上 | 通过候选人调查问卷收集（包括所有候选人） |
| 录用率 | 超过80% | 通过ATS系统记录 |

---

## 第八阶段：流程审核与改进

### 季度招聘回顾

```yaml
quarterly_review:
  period: "Q[N] YYYY"
  
  funnel_metrics:
    applications: N
    screens_passed: N  # → Screen pass rate
    onsites: N         # → Onsite conversion rate  
    offers: N          # → Offer rate
    accepts: N         # → Acceptance rate
    
  quality_metrics:
    ninety_day_retention: "X%"
    manager_satisfaction_90d: "X/5"
    time_to_productivity: "X weeks"
    regretted_attrition_1yr: "X%"
    
  process_metrics:
    time_to_fill: "X days (target: <30)"
    time_in_stage:
      screen: "X days"
      onsite: "X days"  
      decision: "X days"
      offer: "X days"
    interviewer_calibration: "score variance across interviewers"
    
  actions:
    - "[Improvement 1 based on metrics]"
    - "[Improvement 2]"
```

### 问题库的有效性跟踪

对于问题库中的每个问题，记录其实际使用情况：

```yaml
question_effectiveness:
  question: "[question text]"
  times_asked: N
  
  signal_quality:
    strong_differentiator: N  # Times this question clearly separated strong/weak
    no_signal: N              # Times everyone answered similarly
    confusing: N              # Times candidates misunderstood
    
  # If no_signal > 50% → Replace the question
  # If confusing > 20% → Reword the question
  # If strong_differentiator > 70% → Keep and promote
```

### 面试官的培训与校准

```
Monthly: Compare interviewer scores across candidates
- Interviewer A averages 4.2, Interviewer B averages 2.8 → calibration needed
- Run calibration session: review same candidate, discuss scoring differences
- Goal: interviewers should be within 0.5 points on average for same candidates

Training for new interviewers:
1. Shadow 3 interviews (observe, don't participate)
2. Reverse shadow 2 interviews (conduct, observed by experienced interviewer)
3. Solo with debrief for 3 interviews
4. Full autonomy after calibration check
```

---

## 特殊情况处理

### 内部候选人
- 使用与外部候选人相同的评分卡（确保公平）
- 采用不同的问题策略：关注候选人未来的发展潜力而非过去的表现（因为您已经了解他们的过去经历）
- 如果候选人未被录用：由经理亲自提供反馈，并制定再应聘的计划和时间表
- 绝不要承诺给予内部候选人特殊待遇

### 高层职位招聘
- 增加推荐信审核（5份以上，包括非正式渠道的推荐信）
- 组织高管团队聚餐（旨在了解企业文化而非评估候选人）
- 在最后阶段要求候选人展示90天内的工作成果
- 使用专业招聘机构寻找候选人，但内部负责最终的评估

### 大量招聘（10个以上相同职位）
- 规范所有流程：使用相同的问题、相同的评估标准、相同的顺序
- 使用结构化的评分表，避免自由形式的记录
- 每周进行团队间的评分校准
- 考虑在初期阶段使用集体评估中心
- 监控不同招聘经理之间的评分差异（差异应保持较低）

### 远程/异步面试
- 在面试前测试技术环境（面试过程中不要进行）
- 保持双方摄像头开启（非语言信号也很重要）
- 在获得候选人同意的情况下进行录音（用于后续校准）
- 对于时区有差异的候选人，优先安排带回家的任务而非现场编码测试
- 注意：不要因为背景噪音、口音或非英语母语等因素而降低评分

### 重新加入公司的员工
- 将他们视为新候选人对待（情况可能已经发生变化）
- 跳过基本的公司知识问题
- 重点关注他们离职的原因、离职后的变化以及他们在其他公司的经历
- 检查他们离开后的团队/职位是否有所变化；现任团队是否希望他们回归

### 给出反offer时的注意事项
- 如果候选人收到反offer：
  - 不要惊慌，确保您的报价已经足够吸引人
  - “我们根据该职位的价值给出了最好的报价。如果您愿意加入，我们非常欢迎您，但如果您决定留下，我们也理解。”
  - 统计数据显示：80%接受反offer的人在18个月内会离开
  - 如果他们选择留下，尊重他们的决定，并保持沟通渠道畅通

---

## 自然语言指令与操作对应关系

| 命令 | 操作内容 |
|---------|-------------------|
| “为[职位]设计面试流程” | 设计完整的面试流程（包括评分卡、结构、问题及评估标准） |
| “为[职位]创建评分卡” | 为该职位制定明确的评价标准和可衡量的成果 |
| “为[能力]生成问题” | 为该能力生成STAR格式的问题及相应的追问 |
| “为[职位]设计带回家的任务” | 设计包含评估标准和防止作弊措施的任务 |
| “为[职位级别]设计系统设计面试” | 设计相应的面试流程和评估标准 |
| “评估候选人[姓名]” | 进行结构化的面试总结并给出评分 |
| “为[职位]设计电话筛选环节” | 设计30分钟的电话筛选环节，并设定通过/未通过的标准 |
| “撰写拒绝通知” | 撰写具体且建设性的拒绝通知 |
| “审核我们的面试流程” | 对整个流程进行全面的审核并提供改进建议 |
| “校准面试官” | 组织面试官的培训，确保评分标准的一致性 |
| “为[职位/公司阶段]设计面试流程” | 根据初创公司/成长型企业/大型企业的特点调整面试流程 |
| “为[职位]生成推荐信问题” | 设计结构化的推荐信询问指南 |