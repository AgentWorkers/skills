---
name: Event Planner Pro
description: 规划、执行并评估各类商业活动——包括会议、网络研讨会、工作坊、产品发布会、社交活动、贸易展览以及企业聚会。从活动构思到活动结束后的投资回报率（ROI）分析，全程负责活动的生命周期管理。
metadata: {"clawdbot":{"emoji":"🎪","os":["linux","darwin","win32"]}}
---
# Event Planner Pro 🎪

这是一个全面的活动策划与执行系统，适用于从小型研讨会到超过5000人的大型会议等各种类型的活动。系统采用商业级的方法论，提供模板、预算制定、时间线规划以及投资回报率（ROI）的评估工具。

---

## 第一阶段：活动策略与概念

### 快速活动评估

当接到活动策划任务时，需要收集以下信息：

```yaml
event_brief:
  name: ""
  type: ""  # conference | webinar | workshop | networking | trade_show | product_launch | corporate | fundraiser | retreat
  purpose: ""  # lead_gen | brand_awareness | education | community | sales | internal_alignment | celebration
  target_audience: ""
  expected_attendees: 0
  date_range: ""  # preferred dates or flexibility
  budget_range: ""  # total budget or per-attendee target
  format: ""  # in_person | virtual | hybrid
  success_metrics: []  # what does success look like?
  constraints: []  # venue locked, date fixed, sponsor requirements, etc.
```

### 活动类型决策矩阵

| 活动类型 | 适合对象 | 通常规模 | 准备时间 | 人均预算 |
|------|----------|-------------|-----------|--------------|
| 网络研讨会 | 招揽潜在客户、树立行业领导地位 | 50-500人 | 2-4周 | $5-20美元 |
| 研讨会 | 深度技能传授、提升品牌影响力 | 10-50人 | 4-8周 | $100-500美元 |
| 交流活动 | 建立人际关系、拓展社区 | 30-200人 | 3-6周 | $30-100美元 |
| 会议 | 增强品牌影响力、提供多主题内容 | 200-5000人以上 | 3-12个月 | $200-800美元 |
| 产品发布会 | 提升产品知名度、吸引媒体关注 | 50-500人 | 6-12周 | $150-1000美元 |
| 展览会（展位） | 提高行业曝光度、获取潜在客户 | 无固定人数 | 8-16周 | 总费用5000-50000美元 |
| 企业/内部活动 | 强化团队凝聚力、培训员工 | 20-500人 | 4-8周 | $100-400美元 |
| 筹款活动 | 招募捐款、培养捐赠者 | 50-500人 | 8-16周 | $150-500美元 |
| 露营活动 | 增强团队凝聚力、制定战略 | 10-50人 | 6-12周 | $500-2000美元 |

### 活动目的与形式匹配

- **招揽潜在客户** → 适合使用网络研讨会（初级营销渠道）+ 研讨会（高级营销渠道）
- **增强品牌影响力** → 适合举办会议或在其他活动中演讲
- **加速销售** → 适合安排小型晚餐会或圆桌会议（针对10-20名潜在客户）
- **建立社区** → 适合定期举办交流活动及年度峰会
- **教育培训** → 适合举办系列研讨会并提供证书
- **强化内部凝聚力** → 适合组织户外露营活动及季度内部会议

---

## 第二阶段：预算规划

### 预算模板

```yaml
event_budget:
  name: ""
  total_budget: 0
  contingency_pct: 15  # always include 15% buffer
  
  venue:
    rental: 0
    insurance: 0
    security: 0
    permits: 0
    subtotal: 0
  
  food_beverage:
    catering: 0
    beverages: 0
    special_dietary: 0
    service_staff: 0
    subtotal: 0
  
  technology:
    av_equipment: 0
    streaming_platform: 0  # for virtual/hybrid
    event_app: 0
    wifi_upgrade: 0
    recording: 0
    subtotal: 0
  
  marketing:
    design_branding: 0
    paid_ads: 0
    email_platform: 0
    printed_materials: 0
    signage: 0
    photography_video: 0
    subtotal: 0
  
  speakers:
    fees: 0
    travel: 0
    accommodation: 0
    gifts: 0
    subtotal: 0
  
  logistics:
    staff_travel: 0
    shipping: 0
    swag_gifts: 0
    badges_lanyards: 0
    decorations: 0
    transportation: 0
    subtotal: 0
  
  contingency: 0  # 15% of total
  grand_total: 0

  revenue:
    ticket_sales: 0
    sponsorships: 0
    exhibitor_fees: 0
    merchandise: 0
    total_revenue: 0
  
  net_cost: 0  # grand_total - total_revenue
  cost_per_attendee: 0
```

### 按活动类型分配预算的规则

| 活动类型 | 场地费用 | 餐饮费用 | 技术设备费用 | 营销费用 | 演讲者费用 | 物流费用 |
|------|-------|-----|------|-----------|----------|-----------|
| 会议 | 25% | 20% | 15% | 20% | 10% | 10% |
| 网络研讨会 | 0% | 0% | 40% | 35% | 15% | 10% |
| 研讨会 | 20% | 15% | 10% | 25% | 20% | 10% |
| 交流活动 | 30% | 30% | 5% | 20% | 5% | 10% |
| 产品发布会 | 20% | 15% | 20% | 25% | 5% | 15% |
| 展览会 | 40% | 10% | 15% | 20% | 0% | 15% |

### 预算紧张时的成本削减策略

1. **场地费用** → 优先考虑共享办公空间、大学礼堂或合作伙伴的办公场所。
2. **演讲者费用** → 对于小型活动，可以提供曝光机会或内容交换，而非直接支付费用。
3. **餐饮费用** → 选择提供早餐/午餐，避免提供晚餐；可以使用饮料券代替自由饮酒。
4. **营销费用** | 利用演讲者的受众资源，或与合作伙伴进行交叉推广。
5. **技术设备费用** | 对于参会人数少于100人的活动，使用免费的技术平台（如StreamYard、Zoom、Luma）。
6. **纪念品** | 提供电子形式的纪念品（如电子书、模板、折扣码），而非实体物品。

---

## 第三阶段：时间线与项目计划

### 主要时间线模板

根据活动类型调整准备时间。会议通常需要6-12个月；网络研讨会则需要2-4周。

```yaml
timeline:
  t_minus_6_months:
    - Define event concept, goals, success metrics
    - Set budget and get approval
    - Book venue (in-person) or select platform (virtual)
    - Identify keynote speakers, begin outreach
    - Create event brand (name, logo, color scheme, tagline)
    
  t_minus_4_months:
    - Confirm speakers and session topics
    - Launch event website/landing page
    - Open early-bird registration
    - Begin sponsor outreach (sponsorship deck ready)
    - Book AV, catering, photographer
    
  t_minus_2_months:
    - Finalize agenda and schedule
    - Launch marketing campaign (email, social, ads)
    - Send speaker prep kits (guidelines, templates, deadlines)
    - Confirm all vendor contracts
    - Set up registration/ticketing system
    - Plan networking activities
    
  t_minus_1_month:
    - Close early-bird pricing
    - Send attendee pre-event survey
    - Finalize run-of-show document
    - Brief all staff on roles and responsibilities
    - Test all technology (streaming, mics, slides)
    - Prepare attendee welcome materials
    
  t_minus_1_week:
    - Final headcount to caterer
    - Print badges, signage, materials
    - Load all presentations into master deck
    - Run full tech rehearsal
    - Send attendee reminder with logistics
    - Prepare emergency kit (adapters, tape, markers, batteries, meds)
    
  t_minus_1_day:
    - Venue walkthrough with team
    - Set up registration desk, signage, AV
    - Test wifi under load
    - Charge all devices
    - Pre-position water, snacks in speaker rooms
    - Team dinner / final briefing
    
  event_day:
    - Arrive 2 hours early
    - Registration desk open 1 hour before
    - Run-of-show doc in every staff member's hands
    - Photographer capturing key moments
    - Live social media coverage
    - Monitor and fix issues in real time
    - Collect feedback (paper cards or app)
    
  post_event:
    - day_1: Thank you emails to attendees, speakers, sponsors
    - day_2: Share photos and recording links
    - day_3: Send feedback survey
    - week_1: Analyze survey results, calculate ROI
    - week_2: Debrief with team, document lessons learned
    - week_3: Follow up on leads generated
    - month_1: Publish recap content (blog, video, social)
```

### 网络研讨会快速时间线（2-4周）

```yaml
webinar_timeline:
  week_1:
    - Define topic, title, speaker(s)
    - Create landing page with registration form
    - Write 3-email invite sequence
    - Schedule social posts (5-8 posts)
    - Set up streaming platform (test audio/video)
    
  week_2:
    - Send invite email #1 (announcement)
    - Speaker prep call (align on content, Q&A format)
    - Create slide deck template
    - Send invite email #2 (value hook)
    - Partner cross-promotion (ask speakers to share)
    
  week_3:
    - Slides finalized
    - Full dry run with speaker(s)
    - Send invite email #3 (urgency/last chance)
    - Prepare follow-up email sequence (recording, CTA)
    - Set up polls/Q&A in platform
    
  webinar_day:
    - Test 30 min before go-live
    - Start recording
    - Moderator manages Q&A
    - Drop CTA in chat at midpoint and end
    - Thank everyone, announce next event
    
  post_webinar:
    - Send recording within 24 hours
    - Send follow-up #1 (recording + resource) — day 1
    - Send follow-up #2 (CTA/offer) — day 3
    - Send follow-up #3 (case study/social proof) — day 7
    - Add registrants to nurture sequence
```

---

## 第四阶段：场地与供应商管理

### 场地选择评分标准（线下活动）

对每个场地进行1-5分的评估：

| 评估标准 | 权重 | 分数 | 加权得分 |
|-----------|--------|-------|----------|
| 容量是否足够（预留20%的缓冲空间） | 5 | /5 | /25 |
| 交通便利性（包括公共交通、停车和机场） | 4 | /5 | /20 |
| 是否配备先进的视听设备 | 4 | /5 | /20 |
| 无线网络覆盖情况（询问最大同时连接设备数量） | 4 | /5 | /20 |
| 餐饮服务选项（是否提供内部餐饮或灵活选择） | 3 | /5 | /15 |
| 是否有独立会议室 | 3 | /5 | /15 |
| 自然采光情况 | 2 | /5 | /10 |
| 场地氛围是否与活动主题相符 | 2 | /5 | /10 |
 | 取消/重新安排政策 | 3 | /5 | /15 |
| **总分** | | | **/150** |

**评分标准：**总分110分以上即可预订；80-109分需协商改进；低于80分需继续寻找其他场地。

### 场地合同检查清单

- 确认场地容量（包括座位、站立区域和教室式布局）
- 了解无线网络的具体参数（带宽、最大连接设备数量、密码分配方式）
- 检查视听设备（投影仪、屏幕、麦克风数量及无线使用情况）
- 电源设施（电源插座位置、延长线政策、备用发电机）
- 确认场地是否提供布置和拆除服务（通常需要2-4小时）
- 了解取消政策及不可抗力条款
- 了解餐饮服务的具体情况（是否提供独家服务或允许自带食物）
- 了解停车安排（停车位数量、验证方式及班车服务）
- 了解保险要求（通常需要购买活动责任保险）
- 了解场地是否有无障碍设施（如轮椅通道、电梯、洗手间）

### 供应商管理模板

```yaml
vendors:
  - name: ""
    type: ""  # catering | av | photography | streaming | decor | transport | security
    contact: ""
    phone: ""
    email: ""
    contract_signed: false
    deposit_paid: false
    deposit_amount: 0
    total_cost: 0
    payment_schedule: ""
    cancellation_policy: ""
    insurance_verified: false
    delivery_date: ""
    setup_time_needed: ""
    notes: ""
```

---

## 第五阶段：演讲者与内容管理

### 演讲者联系模板

```
Subject: Speaking at [Event Name] — [Date]

Hi [Name],

We're organizing [Event Name], a [type] event for [audience] on [date] in [location/virtual].

Your work on [specific topic/achievement] is exactly what our attendees need. We'd love you to deliver a [length]-minute [keynote/talk/workshop/panel] on [proposed topic].

What we offer:
- [Fee / travel + accommodation / exposure to X audience]
- Professional recording of your session
- Promotion to our [X]-person audience across [channels]

[X] attendees from companies like [notable names].

Interested? Happy to jump on a quick call this week.

Best,
[Name]
```

### 演讲者准备材料

在活动前4周发送给演讲者：

```yaml
speaker_kit:
  event_overview:
    name: ""
    date: ""
    venue: ""
    audience_profile: ""
    expected_attendance: 0
    
  session_details:
    title: ""
    format: ""  # keynote | breakout | workshop | panel | fireside
    duration_minutes: 0
    q_and_a_minutes: 0
    time_slot: ""
    room: ""
    
  content_guidelines:
    slide_template_url: ""  # branded template
    slide_deadline: ""  # 1 week before event
    max_slides: 0
    no_sales_pitch: true
    actionable_takeaways: 3  # minimum
    audience_level: ""  # beginner | intermediate | advanced | mixed
    
  logistics:
    arrival_time: ""
    tech_check_time: ""
    green_room_location: ""
    av_setup: ""  # what's provided (clicker, mic type, monitor)
    laptop_compatibility: ""  # HDMI, USB-C, bring own adapter
    recording_consent: true
    
  promotion:
    headshot_needed: true
    bio_word_limit: 100
    social_handles: ""
    promotional_posts_requested: 2  # minimum shares
```

### 议程设计原则

1. **合理安排活动节奏** — 休息后安排高互动性的环节，午餐后安排反思性环节。
2. **控制演讲时长** — 单次演讲时间不超过18分钟，以确保互动性（遵循TED演讲模式）。
3. **平衡主会场与分会场的时间分配** — 会议中主会场占比60%，分会场占比40%。
4. **设置交流环节** — 安排3次结构化的交流活动。
5. **精彩的开场和结束** — 最优秀的演讲者应负责开场和结束整个活动。
6. **预留缓冲时间** — 每个环节之间预留10分钟的时间，以便顺利过渡。
7. **避免连续安排多个演讲者** — 避免听众疲劳。

### 全天会议议程模板

```
08:00 - 08:45  Registration & Coffee ☕
08:45 - 09:00  Welcome & Housekeeping
09:00 - 09:30  Opening Keynote: [Big Name / Big Idea]
09:30 - 09:45  Transition + Networking Activity #1
09:45 - 10:15  Talk: [Topic A]
10:15 - 10:45  Talk: [Topic B]
10:45 - 11:15  Break + Expo / Sponsor Booths ☕
11:15 - 12:00  Workshop Track A | Workshop Track B | Workshop Track C
12:00 - 13:00  Lunch + Networking Activity #2 🍽️
13:00 - 13:30  Fireside Chat: [Industry Leader]
13:30 - 14:00  Talk: [Topic C]
14:00 - 14:30  Talk: [Topic D]
14:30 - 15:00  Break + Expo ☕
15:00 - 15:45  Panel: [Hot Topic]
15:45 - 16:15  Lightning Talks (5 min x 5 speakers)
16:15 - 16:45  Closing Keynote
16:45 - 17:00  Wrap-up & Announcements
17:00 - 19:00  Happy Hour / After-Party 🎉
```

---

## 第六阶段：注册与营销

### 注册定价策略

```yaml
pricing_tiers:
  super_early_bird:
    discount: 40%
    deadline: "T-3 months"
    purpose: "Validate demand, seed initial registrations"
    
  early_bird:
    discount: 20%
    deadline: "T-6 weeks"
    purpose: "Build momentum, create urgency"
    
  regular:
    discount: 0%
    deadline: "T-1 week"
    purpose: "Standard pricing"
    
  last_minute:
    premium: 10%  # optional
    deadline: "Day of"
    purpose: "Captures procrastinators"
    
  group_discount:
    threshold: 3  # tickets
    discount: 15%
    purpose: "Encourage team attendance"
    
  student_nonprofit:
    discount: 50%
    verification: "edu email or org verification"
```

### 营销活动时间线

```yaml
marketing_phases:
  awareness:  # T-8 to T-6 weeks
    - Launch event website/landing page
    - Announce on social media (3-5 posts)
    - Email blast to existing list
    - Speaker announcements (1 per week)
    - Partner cross-promotion begins
    
  consideration:  # T-6 to T-3 weeks
    - Share agenda/session details
    - Speaker spotlight posts (interviews, quotes)
    - Early testimonials from past events
    - Retargeting ads on registrants who didn't complete
    - Blog post: "X Reasons to Attend [Event]"
    
  urgency:  # T-3 weeks to T-1 week
    - "Early bird ending" campaign
    - Countdown posts
    - "Only X spots left" (if true)
    - Direct outreach to high-value prospects
    - Reminder email to registered (build excitement)
    
  final_push:  # T-1 week
    - "Last chance" email
    - Social proof: "X people already registered"
    - DM outreach to key targets
    - Logistics email to confirmed attendees
```

### 电子邮件发送流程（共6封）

1. **活动公告**（提前8周）：活动内容、时间、目的，同时邀请提前报名。
2. **演讲者介绍**（提前6周）：介绍2-3位演讲者，并展示他们的背景资料。
3. **议程发布**（提前4周）：公布完整议程，询问参与者对哪些环节感兴趣。
4. **提前报名截止**（提前3周）：告知剩余报名时间，并提醒价格上涨。
5. **最终信息**（提前1周）：提供活动详细信息、所需携带物品及注意事项。
6. **活动前一天**：再次提醒参与者，提供活动链接和停车/无线网络信息。

### 活动官网必备元素

- 清晰的活动名称和日期、地点。
- 一句话的价值主张：参与者能从活动中获得什么。
- 演讲者的头像和简短简介。
- 可展开的议程内容。
- 过往参与者的评价和参与企业的LOGO。
- 明确的定价信息和报名链接。
- 常见问题解答（包括停车、退款、着装要求、录像等相关信息）。
- 网站需支持移动设备访问。
- 设置倒计时功能。
- 可提供过往活动的录像（如适用）。

---

## 第七阶段：赞助合作

### 赞助层级结构

```yaml
sponsorship_tiers:
  title_sponsor:
    price: ""  # typically 40-60% of total sponsorship goal
    benefits:
      - Logo on all materials (event name: "Powered by [Sponsor]")
      - Keynote slot or fireside chat (10-15 min)
      - Premium booth location
      - Full attendee list (with consent)
      - 10 complimentary tickets
      - Logo on recording/replay
      - Social media mentions (10+)
      - Email feature
    limit: 1
    
  gold:
    price: ""
    benefits:
      - Logo on website and printed materials
      - Breakout session or workshop slot
      - Booth in expo area
      - 5 complimentary tickets
      - Social media mentions (5)
      - Logo on attendee email
    limit: 3
    
  silver:
    price: ""
    benefits:
      - Logo on website
      - Table in expo area
      - 3 complimentary tickets
      - Social media mention (2)
    limit: 5
    
  community:
    price: ""  # or in-kind
    benefits:
      - Logo on website
      - 2 complimentary tickets
      - Social mention (1)
    limit: 10
```

### 赞助商联系邮件

```
Subject: Sponsorship Opportunity — [Event Name] ([Date])

Hi [Name],

[Event Name] brings together [X] [audience type] on [date] in [location].

Last year: [X attendees], [X% decision-makers], [notable companies].

We have [tier] sponsorship packages from $[low] to $[high], including:
- [Top 3 benefits of relevant tier]

Our attendees match your ICP: [specific overlap].

Happy to send the full sponsorship deck. Quick 15 min this week?

Best,
[Name]
```

### 活动后的赞助回报包

在活动结束后2周内发送以下信息：
- 总参与人数及人群统计。
- 展位参观情况/分会场参与人数。
- 社交媒体上的曝光量和提及次数。
- 赞助商品牌的展示图片。
- 拥有同意权的潜在客户名单或扫描数据。
- 参与者的满意度评分。
- 感谢信及下一次活动的优惠信息。

---

## 第八阶段：活动当天执行

### 活动执行手册

这是最重要的文件，所有工作人员都需要一份。

```yaml
run_of_show:
  event: ""
  date: ""
  venue: ""
  
  team_contacts:
    event_lead: {name: "", phone: ""}
    av_tech: {name: "", phone: ""}
    registration: {name: "", phone: ""}
    catering: {name: "", phone: ""}
    venue_contact: {name: "", phone: ""}
    
  schedule:
    - time: "06:00"
      activity: "Team arrives, begin setup"
      owner: ""
      notes: ""
    - time: "07:00"
      activity: "AV check, mic test all rooms"
      owner: ""
      notes: ""
    # ... full schedule with owner and notes for every slot
    
  contingency:
    speaker_no_show: "Backup: [name] on standby. Extend Q&A. Panel becomes fireside."
    av_failure: "Backup laptop loaded. Mobile hotspot ready. Portable speaker in kit."
    low_attendance: "Close off sections. Rearrange to fill front. More interactive format."
    wifi_down: "Mobile hotspots x3. Offline slide copies. Apologize + offer recording."
    medical_emergency: "First aid kit at [location]. Nearest hospital: [name, address]. Call [emergency#]."
    weather_disruption: "Indoor backup plan. Communication plan for attendees."
```

### 应急物资清单

- 多个电源条和延长线。
- HDMI、USB-C、DisplayPort适配器。
- 备用笔记本电脑及所有演示文件。
- 移动无线热点设备（2-3个）。
- 铜线、胶带、双面胶带。
- 记号笔（用于白板和永久性书写）。
- 剪刀、美工刀。
- AA和AAA电池。
- 手机充电器（支持Lightning和USB-C接口）。
- 急救包。
- 口香糖、止痛药、洗手液。
- 打印好的参与者名单（作为注册信息的备用）。
- 现金（用于小费或紧急情况）。
- 备用徽章和挂绳。
- 蓝牙音箱（作为备用音频设备）。

### 交流活动组织技巧

- **结构化交流**：
  - **快速交流环节**：设置3分钟的轮换环节，使用提示卡（例如：“您本季度面临的最大挑战是什么？”）
  - **主题匹配的交流小组**：根据参与者兴趣分组。
  - **伙伴匹配**：在活动前为参与者配对，通过电子邮件互相介绍。
  - **专家咨询**：在休息时间安排专家在指定小组内回答问题。
  - **寻宝游戏**：通过 bingo 卡片让参与者互相认识。

---

## 第九阶段：虚拟/混合式活动

### 平台选择指南

| 平台 | 适用场景 | 最大参与人数 | 价格范围 |
|----------|----------|---------------|-------------|
| Zoom Webinar | 适合简单的网络研讨会 | 10,000人 | $79-6,490/年 |
| StreamYard | 适合多演讲者的活动，支持品牌推广 | 1,000人 | 免费至$99/月 |
| Hopin | 适合大型会议 | 100,000人 | 根据需求定制价格 |
| Luma | 适合社区活动，支持票务系统 | 无限制 | 免费至$59/月 |
| Airmeet | 适合以交流为目的的活动 | 10,000人 | $167/月 |
| Riverside | 适合高质量录制 | 适合8位演讲者的活动 | $24/月 |
| YouTube Live | 适合直播，不支持实时互动 | 无限制 | 免费 |

### 混合式活动的注意事项

- **虚拟活动不可忽视**：为虚拟环节设置专门的摄像角度和聊天主持人。
- **制定独立的虚拟议程**：除了直播现场活动外，还需安排虚拟问答和分会场环节。
- **进行两次技术测试**：在活动前同时测试现场和虚拟环境的连接情况。
- **必须安排聊天主持人**：负责监控虚拟聊天并解答问题。
- **提供即时录像**：确保虚拟参与者能快速获取录像。

### 提高虚拟活动参与度的技巧

- **每10分钟进行一次投票**：保持观众的参与度。
- **聊天提示**：在活动开始时提醒参与者在聊天区留言。
- **设置分会场**：每组4-6人，每次讨论10分钟。
- **设置实时问答环节**：预留活动最后的1/3时间用于问答。
- **加入互动元素**：通过积分奖励等方式提高参与度。
- **鼓励使用摄像头**：在研讨会上鼓励参与者开启摄像头。

---

## 第十阶段：活动后的分析与投资回报率（ROI）评估

### 活动后反馈调查

在活动结束后24小时内发送反馈调查，问卷不超过5分钟：

1. 整体满意度（1-10分）。
2. 哪个环节最有价值？（多选）
3. 哪个环节最不值得？（多选）
4. 你是否会向同事推荐这次活动？（1-10分）
5. 有哪些方面可以改进？
6. 下次活动希望包含哪些主题？
7. 你还会参加这次活动吗？（是/可能/不会）

### 投资回报率计算框架

```yaml
event_roi:
  costs:
    total_spend: 0
    staff_time_hours: 0
    staff_time_cost: 0  # hours × blended rate
    total_cost: 0  # spend + staff time
    
  direct_revenue:
    ticket_sales: 0
    sponsorship_revenue: 0
    merchandise: 0
    total_direct: 0
    
  pipeline_value:
    leads_generated: 0
    qualified_leads: 0
    average_deal_size: 0
    expected_close_rate: 0
    pipeline_value: 0  # qualified × deal_size
    expected_revenue: 0  # pipeline × close_rate
    
  brand_value:
    social_impressions: 0
    media_mentions: 0
    new_email_subscribers: 0
    content_assets_created: 0  # recordings, blogs, clips
    estimated_content_value: 0  # cost to create equivalent
    
  calculations:
    direct_roi_pct: 0  # (direct_revenue - total_cost) / total_cost × 100
    pipeline_roi_pct: 0  # (expected_revenue - total_cost) / total_cost × 100
    cost_per_lead: 0  # total_cost / leads_generated
    cost_per_attendee: 0  # total_cost / attendees
    nps_score: 0
    
  verdict: ""  # repeat | modify | kill
  # Repeat: ROI > 200% or NPS > 50
  # Modify: ROI 50-200% or NPS 20-50
  # Kill: ROI < 50% AND NPS < 20
```

### 活动后的内容推广策略

最大化活动的长尾价值：

- **活动后第1-2天**：发送感谢邮件和调查问卷，并附上活动照片。
- **活动后第3-5天**：发布活动录像链接（仅限注册用户）。
- **活动后第1周**：在博客上发布活动总结。
- **活动后第2周**：发布演讲者的精彩片段（30-60秒）。
- **活动后第3周**：发布完整的活动录像。
- **活动后第1个月**：整理活动内容的电子书或报告。
- **活动后第2个月**：发布参与者的成功案例。
- **持续推广**：在未来3-6个月内持续使用活动中的素材进行宣传。

## 第十一阶段：活动系列与规模化运营

### 建立定期活动品牌

- **统一活动名称**：例如“[品牌]峰会2026”、“[品牌]第14次交流活动”。
- **固定每月的活动时间**：例如每周四。
- **年度重点活动**：每年举办一次大型活动，其他小型活动为其配套。
- **内容循环利用**：每个活动产生的内容都可用于后续活动的宣传。
- **建立社区**：在活动期间及之后通过Slack/Discord等平台建立长期社区。
- **为老参与者提供优惠**：给予他们优先报名权和折扣。

### 规模化运营检查清单

- 为每个岗位制定详细的操作流程。
- 与供应商建立长期合作关系（重复合作可享受折扣）。
- 确保注册系统能够处理大量参与者。
- 建立志愿者和员工培训机制。
- 提前12个月开始筹备下一年的赞助流程。
- 整理以往活动的素材库。
- 根据实际数据优化预算模板。
- 随着活动次数的增加，不断提高客户满意度（NPS）。

---

## 第十二阶段：行业特定活动策划指南

### 技术/软件服务行业

- **活动重点**：产品演示、开发者研讨会、API黑客马拉松。
- **特色服务**：为每位参与者提供无线网络和电源；提供开发者专属纪念品（如贴纸、T恤）；提供现场编码演示。
- **赞助策略**：强调“让[技术]领域的开发者了解您的产品”。

### 专业服务行业（法律、咨询、金融）

- **活动重点**：提供继续教育学分、圆桌讨论、案例研究展示。
- **特色服务**：举办正式的交流活动；使用带有职位名称的徽章；提供纸质议程。
- **赞助策略**：突出您的公司在该领域的专业优势。

### 医疗行业

- **活动重点**：提供继续医学教育学分、合规性培训、患者结果数据分享。
- **特殊要求**：遵守严格的药品赞助规定；禁止赠送价值超过100美元的礼品。
- **赞助策略**：通过官方渠道推广您的服务。

### 建筑/制造业行业

- **活动重点**：现场参观、设备演示、安全培训、行业认证。
- **特色服务**：为现场参观提供必要的个人防护装备；鼓励采用现场实践的形式。
- **赞助策略**：向相关承包商和工程师推广您的产品和服务。

### 房地产行业

- **活动重点**：市场趋势分析、商业机会交流、房产参观。
- **特色服务**：适合举办晚间鸡尾酒会；提供详细的房产信息；安排小型圆桌会议（20-30人）。
- **赞助策略**：吸引房地产行业的投资者和开发商。

---

## 活动准备完成度评估

### 活动准备前评估（1-5分）

在继续进行活动之前，对以下各项进行评估：

| 评估项目 | 评分 |
|-----------|-------|
| 场地/平台已确认并测试完毕 | /5 |
| 演讲者已确定并提交演讲内容 | /5 |
| 注册系统已开放，营销活动已启动 | /5 |
| 预算已制定，未知费用低于10% | /5 |
| 活动执行手册已完成 | /5 |
| 团队已了解各自职责 | /5 |
| 应急预案已制定 | /5 |
| 技术测试已完成 | /5 |
| **总分** | **/40** |

**评分标准：**总分35分以上即可开始活动；25-34分需在本周内解决不足之处；低于25分需推迟或简化活动流程。

---

## 常用命令

- “为[目标受众]在[日期]策划一场[活动类型]活动”
- “为[参与人数]的[活动类型]活动制定预算”
- “为[活动日期]制定活动时间线”
- “为[活动时长]的[活动类型]活动设计议程”
- “给[演讲者姓名]发送关于[活动主题]的联络邮件”
- “为[活动]制作赞助资料”
- “为[活动]制定营销计划”
- “计算[活动]的投资回报率（已花费的成本与实际成果）”
- “为[活动]准备活动执行手册”
- “为[活动]制作活动后的反馈调查”
- “比较[场地A]和[场地B]”
- “在[时间范围]内策划一场[活动主题]的网络研讨会”