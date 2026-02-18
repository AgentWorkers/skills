---
name: Email Marketing Engine
description: 完整的电子邮件营销系统——包括邮件送达率优化、邮件列表构建、发送序列管理、冷启动营销（即针对新用户的推广活动）、自动化营销流程、数据分析以及收入提升功能。该系统完全不依赖任何第三方服务或库。
metadata:
  category: marketing
  skills: ["email", "marketing", "newsletters", "cold-email", "outreach", "sequences", "deliverability", "automation", "lead-generation", "drip-campaigns"]
---
# 邮件营销引擎

这是一套完整的邮件营销构建、运行和优化方法论，涵盖了从域名设置到收入归因的整个流程。内容包括生命周期邮件（新闻通讯、新用户欢迎邮件、客户保留邮件）以及冷拓展邮件（潜在客户开发邮件、个性化邮件、跟进邮件）。无需使用API密钥或付费工具。

---

## 第一阶段：基础设施与邮件送达率

### 域名认证检查清单

在发送任何一封邮件之前，请完成以下所有步骤：

```yaml
domain_auth:
  spf:
    record: "v=spf1 include:_spf.google.com include:[esp-domain] ~all"
    check: "nslookup -type=txt yourdomain.com"
    status: pending  # pending | configured | verified
  dkim:
    selector: "google"  # or ESP-specific
    key_length: 2048  # minimum
    status: pending
  dmarc:
    policy: "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; pct=100"
    progression: "none → quarantine → reject (over 4 weeks)"
    status: pending
  bimi:
    logo_format: "SVG Tiny 1.2"
    vmc_certificate: false  # optional but increases trust
  reverse_dns: pending
  custom_return_path: pending
```

### 域名预热计划

如果是新域名或新IP地址，请严格遵循以下计划：

| 周数 | 每日发送量 | 目标受众 | 内容类型 |
|------|-------------|-----------------|--------------|
| 1     | 20-50封       | 已知活跃联系人      | 个性化、高价值内容     |
| 2     | 50-150封       | 新订阅者       | 欢迎邮件 + 最佳内容    |
| 3     | 150-500封       | 活跃用户（30天内打开邮件） | 多种类型内容     |
| 4     | 500-1500封       | 更广泛的活跃用户群   | 定期发送的邮件     |
| 5     | 1500-5000封       | 全部活跃用户     | 正常发送       |
| 6及以上 | 每周增加20%     | 除不活跃用户外的全部用户 | 所有类型的邮件     |

**预热规则：**
- 首先发送到Gmail/Outlook邮箱（这些邮箱的过滤规则最严格，因此反馈最准确）；
- 在预热期间收集用户回复——提出问题、请求反馈；
- 如果任何阶段的退信率超过3%，立即停止发送并清理邮件列表；
- 在预热期间每天监控Google Postmaster Tools的统计数据；
- 严禁跳过任何一周的发送——从垃圾邮件标记中恢复需要3-6个月的时间。

### 发件人信誉监控

每周检查以下内容：

```yaml
reputation_dashboard:
  google_postmaster:
    domain_reputation: high  # high | medium | low | bad
    spam_rate: 0.02%  # must stay under 0.1%
    authentication: pass
    encryption: tls
  blacklists:
    check_url: "https://mxtoolbox.com/blacklists.aspx"
    listed_on: []  # any listing = immediate action
  bounce_tracking:
    hard_bounces: 0.3%  # remove immediately, never re-send
    soft_bounces: 1.2%  # retry 3x, then suppress
    complaint_rate: 0.04%  # above 0.1% = emergency
  inbox_placement:
    gmail: 94%
    outlook: 91%
    yahoo: 88%
    corporate: 85%
```

**如果信誉下降时的紧急应对措施：**
1. 立即将发送量减少75%；
2. 仅向最活跃的用户群（7天内打开过邮件的用户）发送邮件；
3. 暂停所有冷拓展和促销活动；
4. 审查最近5次发送的邮件内容；
5. 检查是否有用户因误入垃圾邮件陷阱而退信；
6. 在2-4周内逐步恢复发送。

---

## 第二阶段：邮件列表的构建与管理

### 列表增长策略

**按质量排序的有机增长方法：**

| 方法        | 质量        | 发送量      | 设置难度        |
|------------|------------|-----------|-------------------|
| 内容升级（文章内嵌入） | ★★★★★     | 中等        | 中等            |
| 网络研讨会/活动注册 | ★★★★★     | 低-中等      | 高              |
| 免费工具/计算器   | ★★★★☆     | 高          | 高              |
| 新闻通讯推荐计划 | ★★★★☆     | 中等        | 中等            |
| 离开网站时的弹窗提示 | ★★★☆☆     | 高          | 低              |
| 社交媒体个人资料链接 | ★★★☆☆     | 低          | 低              |
| 合作营销交换   | ★★★☆☆     | 中等        | 中等            |
| 付费白皮书/报告   | ★★★☆☆     | 中等        | 中等            |
| 比赛/赠品活动   | ★★☆☆☆     | 高          | 中等            |
| 购买邮件列表   | ☆☆☆☆☆     | 高          | 低              |

**切勿购买邮件列表。** 购买的邮件列表可能包含垃圾邮件陷阱，会降低邮件送达率，并违反GDPR/CAN-SPAM法规。这种“捷径”带来的成本远高于有机增长的方式。

### 吸引潜在客户的框架

每个用户注册都需要一个令人信服的理由：

```yaml
lead_magnet:
  name: "[Specific Outcome] [Format]"
  format: checklist | template | calculator | swipe_file | mini_course | report
  promise: "What specific result will they get?"
  time_to_value: "< 5 minutes"  # faster = higher conversion
  quality_bar: "Would someone pay $20 for this?"
  delivery: immediate  # never gate behind "check your email in 24h"
  
  # Opt-in page elements
  headline: "[Number] [Outcome] without [Pain]"
  subhead: "One specific proof point or social proof"
  bullet_1: "Specific benefit with number"
  bullet_2: "Addresses main objection"
  bullet_3: "Speed/ease promise"
  form_fields: [email]  # name optional, more fields = lower conversion
  cta_button: "Get the [Format]"  # never "Submit"
  social_proof: "[X] people downloaded this week"
```

### 用户细分架构

**核心用户细分（最低要求）：**

```yaml
segments:
  lifecycle:
    - new_subscriber:
        definition: "Joined < 14 days ago"
        treatment: "Welcome sequence, daily for 2 weeks"
    - active:
        definition: "Opened or clicked in last 30 days"
        treatment: "Full campaigns, all content types"
    - cooling:
        definition: "No opens 30-60 days"
        treatment: "Reduced frequency, best content only"
    - dormant:
        definition: "No opens 60-90 days"
        treatment: "Re-engagement sequence"
    - dead:
        definition: "No opens > 90 days, re-engagement failed"
        treatment: "Remove from list (improves deliverability)"
    - customer:
        definition: "Has purchased"
        treatment: "Retention, upsell, referral"
    - vip:
        definition: "Top 10% by engagement OR revenue"
        treatment: "Early access, exclusives, personal touch"
  
  behavioral:
    - clicked_pricing: "Sales-ready, trigger demo offer"
    - downloaded_resource: "Interested in [topic], nurture there"
    - visited_3x_week: "High intent, accelerate sequence"
    - opened_not_clicked: "Subject works, content needs help"
    - clicked_not_converted: "Interest without action, address objection"
  
  demographic:
    - by_role: "[CEO, VP, Manager, IC]"
    - by_company_size: "[1-10, 11-50, 51-200, 201-1000, 1000+]"
    - by_industry: "[SaaS, Ecommerce, Finance, Healthcare, etc.]"
```

### 邮件列表维护规则

每月执行以下操作：

```
List Hygiene Checklist:
□ Remove all hard bounces (immediately, never re-add)
□ Suppress soft bounces with 3+ consecutive failures
□ Remove spam complainers (permanent suppress)
□ Flag role addresses (info@, admin@, support@) — lower priority
□ Identify spam traps (sudden old-domain bounces)
□ Run email verification on new imports (NeverBounce, ZeroBounce)
□ Sunset dormant subscribers (90 days no engagement)
□ Merge duplicates (same email, different entries)
□ Update preference center opt-outs
□ Document list size change: [before] → [after] = [% change]
```

---

## 第三阶段：邮件发送序列与活动设计

### 欢迎邮件序列（7封邮件，14天内发送）

这是你编写过的最重要的邮件序列：

```yaml
welcome_sequence:
  email_1:
    timing: "Immediate (within 60 seconds)"
    subject: "Here's your [lead magnet] + a quick question"
    goal: "Deliver value, set expectations, get a reply"
    structure:
      - deliver_lead_magnet: "Direct download link, no hoops"
      - set_expectations: "Here's what you'll get from me and how often"
      - personal_question: "What's your biggest challenge with [topic]?"
      - ps: "Reply to this email — I read every response"
    why: "First email gets 50-80% open rate. Replies train inbox placement."
    
  email_2:
    timing: "Day 1 (24 hours)"
    subject: "The [thing] that changed everything for me"
    goal: "Build connection through story + deliver quick win"
    structure:
      - origin_story: "Why I care about [topic] (brief, 3-4 sentences)"
      - quick_win: "One actionable tip they can use in 5 minutes"
      - result: "What happened when I/client did this"
    
  email_3:
    timing: "Day 3"
    subject: "[Number] mistakes killing your [desired outcome]"
    goal: "Educate + position expertise"
    structure:
      - mistakes_list: "3-5 common mistakes with brief explanations"
      - reframe: "Why most advice about this is wrong"
      - bridge: "What to do instead (high-level)"
    
  email_4:
    timing: "Day 5"
    subject: "How [client/case study] achieved [specific result]"
    goal: "Social proof + belief building"
    structure:
      - situation: "Where they started (relatable)"
      - action: "What they did (your method)"
      - result: "Specific numbers and outcomes"
      - takeaway: "One thing the reader can apply today"
    
  email_5:
    timing: "Day 7"
    subject: "The complete guide to [core topic]"
    goal: "Deliver highest-value free content"
    structure:
      - comprehensive_resource: "Best blog post, guide, or video"
      - framework: "Your unique approach/methodology"
      - depth: "Go deeper than competitors dare"
    
  email_6:
    timing: "Day 10"
    subject: "Why most [people] fail at [goal] (and how to avoid it)"
    goal: "Address objections before selling"
    structure:
      - common_objections: "The 3 reasons people hesitate"
      - reframe_each: "Why each objection is actually a feature"
      - bridge_to_offer: "Subtle transition toward solution"
    
  email_7:
    timing: "Day 14"
    subject: "Quick question about [their goal]"
    goal: "Soft CTA — consultation, product, or next step"
    structure:
      - summary: "Quick recap of value delivered so far"
      - offer: "Clear, specific next step with benefit"
      - urgency: "Genuine reason to act now (not fake scarcity)"
      - ps: "Easy alternative if they're not ready"
```

### 冷拓展邮件序列（5封邮件，21天内发送）

针对还不了解你的潜在客户：

```yaml
cold_outreach:
  principles:
    - "Research before writing — generic = spam"
    - "One ask per email — never multiple CTAs"
    - "Under 125 words — busy people skim"
    - "No HTML, no images — plain text performs 2x better"
    - "Personalize first 2 lines or don't send"
    - "Never lie about prior relationship ('We met at...' when you didn't)"

  email_1:
    timing: "Day 0"
    subject: "[First name], quick question about [their specific initiative]"
    template: |
      Hi [Name],

      Saw [specific thing — blog post, LinkedIn update, company news, job posting].
      [One sentence connecting their situation to your value prop].

      We helped [similar company] [specific result with numbers].

      Worth a 15-min call to see if this applies to [their company]?

      [Your name]
    personalization_checklist:
      - "Reference something specific to THEM (not their industry)"
      - "Mention a trigger event (hiring, funding, product launch)"
      - "Name a competitor or peer who got results"
    
  email_2:
    timing: "Day 3"
    subject: "Re: [original subject]"
    template: |
      Hi [Name],

      Quick follow-up — wanted to share [relevant resource/case study]
      that shows how [peer company] solved [the problem you help with].

      [One-line insight from the resource]

      Would this be relevant for [their company]?

      [Your name]
    note: "Add value, don't just 'bump' — bumps are lazy"
    
  email_3:
    timing: "Day 7"
    subject: "[Their company] + [your solution area]"
    template: |
      Hi [Name],

      [One specific observation about their business/website/product].
      [What this typically means / costs them].

      If you're seeing the same thing, I have 2-3 ideas that took
      [similar company] from [before] to [after].

      Open to hearing them?

      [Your name]
    note: "Show you've done homework — specific observation > generic pitch"
    
  email_4:
    timing: "Day 14"
    subject: "Should I close the loop?"
    template: |
      Hi [Name],

      I've reached out a few times — totally understand if the
      timing isn't right.

      If [problem you solve] isn't a priority right now, no worries.
      But if it is, I'd love 15 minutes to share what's working
      for [industry] companies like [their company].

      Either way, just let me know and I'll update my notes.

      [Your name]
    note: "Give them an easy out — reduces guilt, increases replies"
    
  email_5:
    timing: "Day 21"
    subject: "Closing the file on [their company]"
    template: |
      Hi [Name],

      Looks like [solving X] isn't a priority right now — totally get it.

      I'll close out my notes on [their company]. If things change
      down the road, here's my calendar link: [link]

      Wishing you and the team a great [quarter/year].

      [Your name]
    note: "Breakup email — often gets the highest reply rate (20-30%)"
```

### 个性化框架

不要仅仅使用 `{first_name}`（用户的名字）来进行个性化邮件内容：

```yaml
personalization_levels:
  level_1_basic:  # minimum viable
    - first_name
    - company_name
    - industry
    impact: "5-10% lift in opens"
    
  level_2_contextual:  # good
    - role/title reference
    - company size tier messaging
    - industry-specific pain points
    - geographic reference
    impact: "15-25% lift in opens and clicks"
    
  level_3_behavioral:  # great
    - reference their recent action (download, page visit, event)
    - mention content they engaged with
    - tailor offer to demonstrated interest
    impact: "30-50% lift in conversions"
    
  level_4_research:  # cold outreach only
    - reference specific blog post/interview they wrote
    - mention recent company news (funding, launch, hire)
    - note a competitor move affecting them
    - connect to LinkedIn post or tweet they shared
    impact: "2-5x reply rate vs. generic"
```

### 重新激活用户序列（3封邮件）

针对30-90天内未打开邮件的订阅者：

```yaml
re_engagement:
  email_1:
    timing: "Day 0 (triggered at 60 days no open)"
    subject: "Still interested in [topic]?"
    content: |
      We noticed you haven't opened our emails in a while.
      No hard feelings — priorities change.
      
      Here's what you missed: [link to best content from last 60 days]
      
      Want to stay on the list? Just click here: [re-confirm link]
      
      If not, we'll automatically remove you in 14 days.
      Either way, no spam — that's a promise.
      
  email_2:
    timing: "Day 7"
    subject: "Last chance: [special offer or best content piece]"
    content: "Offer genuine incentive — exclusive content, discount, or early access"
    
  email_3:
    timing: "Day 14"
    subject: "Goodbye (for now)"
    content: |
      We're removing you from our email list to keep things clean.
      
      If you ever want back in: [subscribe link]
      
      Thanks for being here — hope we helped along the way.
    
    action: "Auto-suppress after send. NEVER re-add without explicit re-opt-in."
```

---

## 第四阶段：邮件类型与模板设计

### 新闻通讯模板设计

```yaml
newsletter:
  frequency: weekly | biweekly  # pick one and be consistent
  best_day: "Tuesday-Thursday, 9-11 AM recipient timezone"
  
  structure:
    hook: "Opening line — personal, topical, or contrarian (2 sentences max)"
    main_content:
      format: "1 deep piece OR 3-5 curated pieces with commentary"
      rule: "80% education, 20% promotion maximum"
      voice: "Write like you're emailing a smart friend"
    cta: "One clear ask — reply, click, share, or buy"
    ps: "Secondary link, personal note, or teaser for next issue"
  
  subject_line_formulas:
    curiosity: "[Number] things I learned about [topic] this week"
    utility: "How to [achieve X] without [pain Y]"
    contrarian: "Stop [common advice] — here's what works instead"
    news: "[Topic] just changed — here's what it means for you"
    personal: "I made a mistake with [topic] (here's what happened)"
  
  metrics_targets:
    open_rate: "> 35% (engaged list), > 20% (broad)"
    click_rate: "> 3%"
    reply_rate: "> 0.5%"
    unsubscribe: "< 0.3% per send"
```

### 促销活动邮件模板设计

```yaml
promotional:
  pre_launch:  # 3-7 days before
    email_1: "Tease — 'Something's coming for [audience]'"
    email_2: "Behind-the-scenes — why we built this"
    
  launch:  # Day of
    email_1: "Announcement — what it is, who it's for, how to get it"
    email_2: "Social proof — early results, testimonials"
    
  follow_up:  # 3-7 days after
    email_1: "FAQ — address top objections"
    email_2: "Case study — detailed success story"
    email_3: "Last chance — genuine deadline or limit"
    
  rules:
    - "Never fake scarcity — if it's evergreen, don't say 'limited time'"
    - "Segment: don't pitch customers what they already own"
    - "Track revenue per email, not just clicks"
    - "3 promotional emails per month maximum (ratio to value emails)"
```

### 交易邮件优化

大多数公司都未能充分利用交易邮件（打开率通常低于70%）：

```yaml
transactional_upgrades:
  order_confirmation:
    must_have: "Order details, delivery estimate"
    add: "Onboarding tip, complementary product, referral ask"
    
  shipping_notification:
    must_have: "Tracking link, delivery date"
    add: "Setup guide, community invite, content recommendation"
    
  receipt:
    must_have: "Amount, description, support contact"
    add: "Usage tips, upgrade path, review request (after delivery)"
    
  password_reset:
    must_have: "Reset link, security note"
    add: "Account security tips, feature reminder"
    
  rule: "Transactional emails MUST remain primarily transactional. Marketing content should be secondary and relevant."
```

---

## 第五阶段：A/B测试与优化

### 测试流程

```yaml
ab_testing:
  minimum_sample: 1000  # per variant for statistical significance
  confidence_level: 95%  # don't declare winners below this
  
  priority_order:  # test in this order for maximum impact
    1: "Subject line (biggest lever — 30-50% impact on opens)"
    2: "Send time (10-20% impact)"
    3: "From name (15-25% impact — personal name vs brand)"
    4: "CTA copy and placement (20-40% impact on clicks)"
    5: "Email length (varies wildly by audience)"
    6: "Plain text vs HTML"
    7: "Personalization depth"
    8: "Preheader text"
  
  methodology:
    split: "20% test / 80% winner (for subject lines)"
    duration: "Wait minimum 4 hours before declaring winner"
    isolation: "Change ONE variable per test"
    documentation: "Log every test result — institutional knowledge"
  
  test_log_template:
    date: "YYYY-MM-DD"
    variable: "Subject line | Send time | CTA | etc."
    variant_a: "Description"
    variant_b: "Description"
    sample_size: "N per variant"
    metric: "Open rate | Click rate | Conversion"
    result_a: "X%"
    result_b: "Y%"
    winner: "A | B | No significant difference"
    confidence: "95%+"
    learning: "What we now know"
    next_test: "What to test based on this result"
```

### 主题行评分

在发送邮件之前，对每个主题行进行评分：

```yaml
subject_line_rubric:
  length:
    score: 0-2
    criteria:
      2: "30-50 characters (optimal mobile display)"
      1: "50-70 characters (acceptable)"
      0: "> 70 characters (truncated on most devices)"
      
  specificity:
    score: 0-2
    criteria:
      2: "Contains a specific number, name, or outcome"
      1: "Somewhat specific"
      0: "Vague or generic"
      
  curiosity_gap:
    score: 0-2
    criteria:
      2: "Creates genuine curiosity without being clickbait"
      1: "Mildly interesting"
      0: "No reason to open"
      
  relevance:
    score: 0-2
    criteria:
      2: "Directly addresses recipient's known interest/pain"
      1: "Generally relevant to audience"
      0: "Could be for anyone"
      
  spam_risk:
    score: 0-2
    criteria:
      2: "No spam triggers, natural language"
      1: "Minor risk factors (emoji, question mark)"
      0: "ALL CAPS, exclamation!!!, 'Free', 'Act now'"
      
  total: "/10 — don't send below 7"
```

### 邮件正文评分

```yaml
email_quality_rubric:
  clarity:
    weight: 25
    criteria:
      25: "One clear message, one CTA, instantly understood"
      15: "Clear but slightly unfocused"
      5: "Multiple messages competing for attention"
      
  value:
    weight: 25
    criteria:
      25: "Reader gains actionable insight or clear benefit"
      15: "Somewhat useful"
      5: "Self-serving with no reader benefit"
      
  voice:
    weight: 20
    criteria:
      20: "Sounds like a human wrote it to one person"
      12: "Professional but slightly generic"
      4: "Corporate-speak, AI-obvious, or template-y"
      
  structure:
    weight: 15
    criteria:
      15: "Scannable: short paragraphs, bold key points, bullets"
      9: "Readable but dense"
      3: "Wall of text, no formatting"
      
  mobile:
    weight: 15
    criteria:
      15: "Single column, large CTA, < 300 words, images optional"
      9: "Mostly mobile-friendly"
      3: "Multi-column, tiny links, image-heavy"
      
  total: "/100 — don't send below 70"
```

---

## 第六阶段：冷拓展系统

### 潜在客户研究模板

在发送任何一封冷拓展邮件之前，请先进行以下研究：

```yaml
prospect_research:
  person:
    full_name: ""
    title: ""
    linkedin_url: ""
    recent_post_or_article: ""
    career_trajectory: ""  # where they came from
    mutual_connections: ""
    
  company:
    name: ""
    website: ""
    industry: ""
    employee_count: ""
    recent_news: ""  # funding, launches, hires, awards
    tech_stack: ""  # BuiltWith, Wappalyzer
    job_postings: ""  # what they're hiring for = priorities
    
  trigger_events:  # why NOW is the right time
    - "New funding round"
    - "New executive hire"
    - "Product launch"
    - "Competitor move"
    - "Industry regulation change"
    - "Job posting related to your solution"
    - "Negative review/complaint about current tool"
    
  connection_points:  # personalization hooks
    - "Shared background/school/employer"
    - "Content they published"
    - "Conference they spoke at"
    - "Mutual connection"
    - "Specific challenge visible from outside"
```

### 冷拓展邮件的发送规则

冷拓展邮件的发送规则与常规营销邮件不同：

```yaml
cold_email_rules:
  domain:
    - "Use a separate domain for cold outreach (not your main domain)"
    - "Set up: outreach.yourdomain.com or yourdomain.co"
    - "Full SPF/DKIM/DMARC on the outreach domain"
    - "Warm up for minimum 2 weeks before sending"
    
  volume:
    - "Maximum 50 cold emails per day per inbox"
    - "Use multiple inboxes to scale (5 inboxes = 250/day)"
    - "Spread sends throughout the day (not all at once)"
    - "Randomize send times ±15 minutes"
    
  content:
    - "Plain text only — no HTML, no images, no tracking pixels"
    - "Under 125 words (3-4 short paragraphs)"
    - "No more than 1 link per email"
    - "Avoid spam trigger words (free, guaranteed, act now, limited)"
    - "Include physical address and opt-out mechanism"
    
  list:
    - "Verify every email address before sending (< 3% bounce)"
    - "Never send to catch-all domains without verification"
    - "Remove any email that bounces immediately"
    - "Respect unsubscribe within 24 hours"
```

### 回复处理框架

```yaml
reply_handling:
  positive:
    signals: ["interested", "tell me more", "let's talk", "send info"]
    response_time: "< 1 hour during business hours"
    action: |
      1. Thank them specifically for what they said
      2. Answer any questions in the reply
      3. Propose 2-3 specific meeting times
      4. Keep it short — they said yes, don't oversell
      
  objection:
    signals: ["too expensive", "not now", "using competitor", "not interested"]
    response_time: "< 4 hours"
    action: |
      1. Acknowledge their concern genuinely
      2. Address the specific objection (not a generic rebuttal)
      3. Offer lighter alternative (case study, free resource)
      4. Leave door open: "If things change, I'm here"
      
  referral:
    signals: ["talk to [name]", "not the right person", "try [department]"]
    action: |
      1. Thank them warmly
      2. Ask: "Would you mind making an intro, or should I reach out directly and mention you?"
      3. Reference the referral in new outreach
      
  negative:
    signals: ["remove me", "stop emailing", "spam", "unsubscribe"]
    action: "Immediately suppress. Reply with brief apology. Never re-add."
```

---

## 第七阶段：自动化与工作流程

### 邮件自动化流程图

```yaml
automations:
  # Acquisition
  lead_magnet_download:
    trigger: "Form submission"
    action: "Deliver asset → Start welcome sequence → Tag by lead magnet topic"
    
  webinar_registration:
    trigger: "Registration"
    action: "Confirmation → 3 reminder emails → Post-event replay + offer"
    
  # Activation
  trial_signup:
    trigger: "Account created"
    sequence:
      day_0: "Welcome + first action to take"
      day_1: "Quick win tutorial"
      day_3: "Feature highlight relevant to their use case"
      day_5: "Case study from similar company"
      day_7: "Check-in: 'How's it going?'"
      day_10: "Advanced feature + upgrade nudge"
      day_13: "Trial ending reminder + offer"
      day_14: "Last day — decision time"
    
  # Revenue
  abandoned_cart:
    trigger: "Cart created, no purchase in 1 hour"
    sequence:
      1_hour: "Forgot something? [Cart contents]"
      24_hours: "Still thinking about it? [Social proof]"
      72_hours: "Last chance + incentive (if margin allows)"
    recovery_rate_target: "5-15%"
    
  # Retention
  post_purchase:
    trigger: "Purchase completed"
    sequence:
      immediate: "Order confirmation + onboarding"
      day_3: "Setup tips + quick win"
      day_14: "Check-in + feature discovery"
      day_30: "Usage milestone celebration"
      day_60: "Case study request or testimonial ask"
      day_90: "Upsell/cross-sell relevant product"
    
  # Win-back
  churn_risk:
    trigger: "No login in 14 days (SaaS) or no purchase in 60 days (ecomm)"
    sequence:
      day_0: "We miss you — here's what's new"
      day_7: "Special offer to come back"
      day_14: "Cancellation survey + last offer"
    
  # Expansion
  nps_follow_up:
    trigger: "NPS score submitted"
    action:
      promoter_9_10: "Ask for review/referral + referral incentive"
      passive_7_8: "Ask what would make it a 10"
      detractor_0_6: "Personal outreach from CS + escalation"
```

### 发送时间优化

```yaml
send_time_strategy:
  b2b:
    best: "Tuesday-Thursday, 9:00-11:00 AM recipient timezone"
    good: "Monday 10AM, Friday 9AM"
    avoid: "Friday afternoon, weekends, holidays"
    
  b2c:
    best: "Saturday 10AM, Sunday 6PM, Tuesday 8PM"
    good: "Weekday evenings 6-9PM"
    avoid: "Weekday mornings (competing with work email)"
    
  cold_outreach:
    best: "Tuesday-Thursday, 7:00-8:00 AM (before inbox floods)"
    good: "Monday 7AM, Thursday 4PM"
    avoid: "Weekends, lunch hour, Friday PM"
    
  advanced:
    - "Use ESP's send-time optimization if available"
    - "Test YOUR audience — benchmarks are averages, not your data"
    - "Consider timezone — segment by geography for large lists"
    - "Account for industry patterns (retail ≠ enterprise ≠ healthcare)"
```

---

## 第八阶段：数据分析与收入归因

### 邮件营销仪表盘

每周跟踪以下数据：

```yaml
dashboard:
  growth:
    list_size: 0
    new_subscribers_this_week: 0
    unsubscribes_this_week: 0
    net_growth_rate: "0%"
    
  engagement:
    avg_open_rate: "0%"
    avg_click_rate: "0%"
    avg_reply_rate: "0%"
    click_to_open_rate: "0%"  # clicks / opens — measures content quality
    
  health:
    bounce_rate: "0%"
    spam_complaint_rate: "0%"
    list_churn_rate: "0%"  # (unsubs + bounces + complaints) / list size
    deliverability_rate: "0%"
    
  revenue:
    email_attributed_revenue: "$0"
    revenue_per_subscriber: "$0"
    revenue_per_email_sent: "$0"
    conversion_rate: "0%"
    
  cold_outreach:
    emails_sent: 0
    open_rate: "0%"
    reply_rate: "0%"
    positive_reply_rate: "0%"
    meetings_booked: 0
    pipeline_generated: "$0"
```

### 收入归因模型

```yaml
attribution:
  last_touch:
    description: "Credit to last email before conversion"
    use_when: "Simple tracking, small list, direct sales"
    
  first_touch:
    description: "Credit to email that acquired the subscriber"
    use_when: "Measuring list-building ROI"
    
  linear:
    description: "Equal credit to all emails in journey"
    use_when: "Understanding full funnel contribution"
    
  time_decay:
    description: "More credit to emails closer to conversion"
    use_when: "Mature program with long sales cycles"
    
  calculation: |
    Email ROI = (Revenue attributed to email - Email costs) / Email costs × 100
    
    Email costs include:
    - ESP subscription
    - Email verification tools
    - Content creation time (hourly rate × hours)
    - Design/template costs
    
    Industry benchmark: $36-42 return per $1 spent
    Healthy program: > $20 per $1
    Needs work: < $10 per $1
```

### 每周回顾模板

```
## Email Marketing Weekly Review — [Date]

### Growth
- List size: [N] ([+/-X] from last week, [Y%] growth)
- Top acquisition source: [source] ([N] new subs)
- Churn: [N] unsubscribes + [N] bounces = [X%] churn rate

### Campaign Performance
| Campaign | Sent | Opens | Clicks | Unsubs | Revenue |
|----------|------|-------|--------|--------|---------|
| [name]   | [N]  | [X%]  | [X%]   | [N]    | $[X]    |

### Cold Outreach
- Sent: [N] | Opens: [X%] | Replies: [N] ([X%])
- Positive replies: [N] | Meetings booked: [N]
- Pipeline generated: $[X]

### A/B Test Results
- Test: [variable] — [A] vs [B]
- Winner: [variant] by [X%] ([confidence]% confidence)
- Learning: [insight]

### Health Check
- Deliverability: [X%] | Spam rate: [X%] | Blacklists: [clean/listed]
- Domain reputation: [high/medium/low]

### Next Week
- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Test to run]
```

---

## 第九阶段：合规性与法律遵从

### 各地区的合规性检查清单

```yaml
compliance:
  can_spam_us:
    - "Include physical mailing address"
    - "Clear 'From' name — no deceptive headers"
    - "Subject line must reflect content"
    - "Identify as ad if promotional"
    - "One-click unsubscribe link in every email"
    - "Honor unsubscribe within 10 business days"
    - "No harvested or purchased emails"
    penalty: "Up to $51,744 per email violation"
    
  gdpr_eu_uk:
    - "Explicit opt-in consent (no pre-checked boxes)"
    - "Record consent: who, when, what, how"
    - "Right to be forgotten — delete on request within 30 days"
    - "Data portability — export subscriber data on request"
    - "Privacy policy link accessible"
    - "Legitimate interest for B2B cold outreach (document your basis)"
    - "Data Processing Agreement with ESP"
    penalty: "Up to €20M or 4% of annual revenue"
    
  casl_canada:
    - "Express consent required (implied consent expires after 2 years)"
    - "Sender identification + physical address"
    - "Unsubscribe processed within 10 business days"
    - "Record of consent for all recipients"
    penalty: "Up to $10M per violation"
    
  cold_email_specific:
    - "Separate domain from marketing (protect main domain)"
    - "Physical address in signature"
    - "Unsubscribe mechanism in every email"
    - "Legitimate business reason for contact"
    - "No misleading subject lines"
    - "Respect 'do not contact' requests permanently"
```

---

## 特殊情况与高级策略

### 多语言邮件处理
- 按语言偏好对用户进行细分，切勿自动翻译后发送；
- 主题行在不同语言中可能表现不佳——应为每种语言单独编写；
- 不同文化对邮件的形式、幽默感、直接性及图片使用有不同的要求；
- 各国的法律要求不同——请遵守当地法规。

### 邮件与短信的整合
- 使用邮件发送内容或教育性信息，使用短信发送紧急提醒；
- 绝不要同时通过两种渠道发送相同的内容；
- 短信的订阅需要用户另行同意——不要默认用户已同意；
- 使用邮件传达故事性内容，短信触发用户行动。

### B2B与B2C营销的区别
- B2B：邮件序列较长，需要更多教育性内容，工作日发送，附上案例研究；
- B2C：邮件较短，更具情感性，适合在周末发送，需要提供社交证明和紧迫感；
- B2B：决策涉及多个利益相关者——邮件内容需便于转发；
- B2C：决策基于个人需求和紧迫感；
- B2B：邮件内容需有助于促成决策；
- B2C：邮件内容需激发用户的即时需求。

### 大规模邮件列表迁移
- 如果更换邮件服务提供商（ESP），请导出所有数据：订阅者信息、标签、互动历史；
- 从新的ESP开始重新发送邮件——不要在第一天就向整个列表发送邮件；
- 从最活跃的用户群开始发送，逐步扩大发送范围（2-4周内）；
- 在新平台首次发送前更新DNS记录。

### 大量邮件发送（每次活动5万封以上）
- 需要专用IP地址（共享IP地址会增加风险）；
- 控制发送频率：每小时1000-2000封，以避免触发过滤规则；
- 监控种子用户列表在不同邮件服务提供商处的收件箱显示情况；
- 为交易邮件和营销邮件使用不同的IP地址。

---

## 自然语言处理相关命令

```
"Set up email authentication for [domain]" → Generate DNS records
"Build a welcome sequence for [business/product]" → 7-email sequence
"Write a cold email for [prospect] at [company]" → Research + personalized email
"Score this subject line: [text]" → Subject line rubric evaluation
"Review this email for quality" → Email copy scoring rubric
"Create a lead magnet for [topic/audience]" → Lead magnet framework
"Audit my email list health" → List hygiene checklist
"Build an abandoned cart sequence" → 3-email recovery flow
"Plan my A/B test for [campaign]" → Testing protocol
"Generate my weekly email report" → Dashboard template
"Check compliance for [region]" → Region-specific checklist
"Create a re-engagement campaign" → 3-email win-back sequence
```