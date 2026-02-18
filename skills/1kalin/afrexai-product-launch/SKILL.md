# 产品发布攻略

作为产品发布策略师，您的职责是指导用户完成产品发布的整个过程，包括从发布前的验证到发布后的增长。本系统适用于SaaS产品、实体产品、服务、市场平台以及内容产品。

## 适用场景

- 规划新产品的发布或新功能的推出
- 制定市场进入策略
- 制定发布时间表和检查清单
- 协调跨职能的发布团队
- 发布后的分析及迭代计划

---

## 第一阶段：发布准备评估

在制定任何计划之前，需要从6个维度（每个维度1-5分，总分30分）评估产品的发布准备情况：

### 准备情况评分表

| 维度 | 分数（1-5） | 依据 |
|---------|-----------|--------|
| **产品与市场的契合度** | _ | 用户研究、测试版反馈、等待名单规模 |
| **定位清晰度** | _ | 能否用一句话解释产品的价值？ |
| **渠道准备情况** | _ | 电子邮件列表规模、社交媒体关注者数量、合作伙伴关系 |
| **内容资产** | _ | 登陆页、演示文稿、截图、用户评价 |
| **团队协调性** | _ | 每个人都清楚自己的职责和时间表 |
| **技术稳定性** | _ | 进行过负载测试、有监控机制、有回滚计划 |

**评分标准：**
- 25-30分：准备充分，可以自信地执行发布 |
- 18-24分：还差一些，需先填补具体漏洞 |
- 12-17分：尚未准备好，需在确定发布日期前解决基础问题 |
- 低于12分：仍处于发布前阶段，需重点进行验证工作 |

### 中止发布的标准（在发布前必须解决）

- [ ] 没有付费测试用户或明确的用户需求信号 |
- [ ] 无法明确说明产品与竞争对手的区别 |
- [ ] 无法在发布当天吸引1000名以上潜在用户 |
- [ ] 核心工作流程在正常使用中出现问题 |
- [ ] 团队对目标客户或定价存在分歧 |

如果存在任何中止发布的标准，请暂停发布计划并先解决这些问题。

---

## 第二阶段：发布策略设计

### 第一步：确定发布类型

```yaml
launch_brief:
  product_name: ""
  launch_type: ""  # big-bang | rolling | soft | beta-to-ga | feature-drop
  target_date: ""
  launch_goal: ""  # awareness | signups | revenue | adoption | press
  primary_metric: ""  # e.g., "500 signups in 7 days"
  secondary_metrics:
    - ""
  budget: ""
  team_lead: ""
```

### 发布类型决策矩阵

| 发布类型 | 适用场景 | 风险 | 时间表 | 预算 |
|---------|-----------|--------|---------|--------|
| **大规模发布** | 新品牌、重要产品、融资公告 | 风险较高 | 8-12周准备 | 高成本 |
| **逐步发布** | B2B SaaS、企业级产品、市场平台 | 风险较低 | 每轮4-8周 | 中等成本 |
| **软发布** | MVP验证、新市场测试 | 风险极低 | 2-4周 | 低成本 |
| **从测试版到正式发布** | 技术产品、开发者工具 | 风险中等 | 4-6周 | 中等成本 |
| **功能更新** | 现有产品、新增功能 | 风险较低 | 1-3周 | 低成本 |

### 第二步：目标受众定位

```yaml
launch_audience:
  primary_segment:
    who: ""  # Specific job title + company size + pain
    size: ""  # Estimated reachable audience
    where_they_gather: []  # Communities, platforms, events
    trigger_event: ""  # What makes them search for this NOW
    
  secondary_segment:
    who: ""
    size: ""
    where_they_gather: []
    
  anti_audience:  # Who is NOT a good fit
    - ""
    
  early_adopter_profile:
    characteristics: []  # Tech-savvy, vocal, community influence
    motivation: ""  # Why they'll try something new
    how_to_find: ""  # Beta programs, Product Hunt, Twitter/X
```

### 第三步：定位与信息传递

使用以下公式来制定核心的发布信息：

**定位声明：**
```
For [target audience] who [situation/pain],
[product name] is a [category]
that [key benefit].
Unlike [alternative], we [differentiator].
```

**信息传递检查清单：**
- [ ] 外行人能否在5秒内理解？
- [ ] 信息是否能够清晰传达产品的价值？（避免仅描述功能）
- [ ] 产品的独特优势是否明显？（不仅仅是“更好”或“更快”）
- [ ] 目标客户是否会使用这些具体表述？ |
- [ ] 信息是否能够激发用户的紧迫感或好奇心？ |

**信息传递层次结构（适用于所有渠道）：**

| 层次 | 内容 | 例子 |
|-------|------|---------|
| **标题** | 一句话的价值主张 | “发布客户真正需要的产品” |
| **副标题** | 用一句话解释产品的工作原理 | “AI驱动的用户研究，能在几分钟内转化为洞察” |
| **三大核心优势** | 关键优势（而非具体功能） | 速度、准确性、易用性 |
| **证据支持** | 每个优势的依据 | “比手动分析快10倍” |
| **故事背景** | 产品诞生的原因及使命 | “我们之所以开发这个产品，是因为在电子表格上浪费了100小时” |

---

## 第三阶段：发布前准备（发布前8至2周）

### 等待名单与热度营造

**等待名单登录页必备元素：**
- [ ] 明确的标题（基于上述定位） |
- [ ] 1张视觉素材（产品截图、演示GIF或特色图片） |
- [ ] 包含明确行动号召的电子邮件（“抢先体验” > “立即注册”） |
- [ ] 社交媒体证明元素（测试版用户数量、用户评价、合作伙伴标志） |
- [ ] 紧迫感/独家性声明（“前500名用户可享受终身折扣” |
- [ ] 分享激励措施（“在等待名单中排名靠前——邀请朋友”）

**发布前内容计划：**

| 周数 | 内容类型 | 发布渠道 | 目标 |
|-------|-------------|---------|------|
| T-8 | 问题意识帖子 | 博客 + 社交媒体 | 提高品牌知名度 |
| T-7 | 背景故事 | Twitter/X线程 | 增加关注者 |
| T-6 | 数据/研究文章 | LinkedIn + 博客 | 增强可信度 |
| T-5 | 用户案例/故事 | 电子邮件 + 社交媒体 | 提升用户信任 |
| T-4 | 产品预告（截图/GIF） | 所有渠道 | 提升热度 |
| T-3 | 创始人故事 | 博客 + 电子邮件 | 建立情感联系 |
| T-2 | 产品对比文章 | 博客 + SEO | 招揽搜索用户 |
| T-1 | 发布预告 | 电子邮件 + 社交媒体 | 确定发布日期 |

### 测试版计划

```yaml
beta_program:
  size: 50-200  # Enough for patterns, small enough for personal touch
  selection_criteria:
    - Matches ICP
    - Active in relevant community
    - Willing to give feedback (written or call)
    - Has the problem RIGHT NOW (not theoretical)
  
  feedback_loop:
    onboarding_survey: true  # Day 1: expectations, setup experience
    weekly_checkin: true  # 3-question pulse (NPS, blockers, requests)
    exit_interview: true  # Why they stayed/left, what they'd pay
    
  incentives:
    - Lifetime discount (20-50%)
    - Founding member badge/status
    - Input on roadmap priorities
    - Early access to future features
    
  success_metrics:
    activation_rate: ">60%"  # Complete core action
    weekly_retention: ">40%"  # Return after first week
    nps_score: ">30"  # Would recommend
    willingness_to_pay: ">50%"  # Would pay at planned price
```

### 合作伙伴与影响者推广

**推广模板（需个性化）：**
```
Subject: [Specific thing you noticed about them] + quick question

Hey [Name],

Loved your [specific content/post/product] — especially [specific detail that proves you actually consumed it].

We're launching [product] on [date] — it [one-sentence value prop]. Thought of you because [genuine connection to their audience/interests].

Would you be open to:
- [ ] Early access to try it (no strings)
- [ ] A quick collab (guest post, joint webinar, co-promotion)
- [ ] Just sharing it if you genuinely like it

Either way, keep making great stuff.

[Name]
```

**合作伙伴评分（优先级排序）：**

| 评分因素 | 权重 | 分数（1-5） |
|---------|--------|-------------|
| 与我们目标受众的重叠度 | 30% | _ |
| 合作伙伴的互动率（不仅仅是关注者数量） | 25% | _ |
| 内容质量与品牌契合度 | 20% | _ |
| 回应的可能性（是否与我们关系密切） | 15% | _ |
| 我们能提供的互惠价值 | 10% | _ |

---

## 第四阶段：发布当天执行

### 发布前7天：最终准备清单

**产品方面：**
- [ ] 所有关键漏洞都已修复（仅针对P0/P1级别问题，避免过度优化） |
- [ ] 与新用户一起测试了产品引导流程 |
- [ ] 配置好了监控和警报机制 |
- [ ] 编写了回滚计划并进行了测试 |
- [ ] 系统在预期流量的3倍压力下通过了测试 |

**营销方面：**
- [ ] 登陆页已上线并经过测试（移动端 + 电脑端） |
- [ ] 电子邮件序列已准备好（欢迎邮件、激活邮件、第3天邮件、第7天邮件） |
- [ ] 社交媒体帖子已起草并安排好发布时间 |
- [ ] 如果适用，已发送了媒体/博主邀请 |
- [ ] 如果适用，已准备了产品推荐活动（Product Hunt） |
- [ ] 为Reddit、Hacker News等相关论坛准备了社区帖子 |

**销售方面：**
- [ ] 演示文稿已更新，包含发布信息 |
- [ ] 为支持团队准备了常见问题解答文档 |
- [ ] 定价页面已上线，包含明确的行动号召 |
- [ ] 支付流程已经过端到端的测试 |

**运营方面：**
- [ ] 支持团队已了解常见问题 |
- [ ] 明确了问题处理的优先级和流程 |
- [ ] 创建了紧急沟通渠道（Slack/Discord） |
- [ ] 成功指标仪表盘已上线 |

### 发布当天计划

**每小时时间表：**

```
06:00  Final systems check — monitoring, uptime, payment flow
07:00  Publish blog post / announcement
07:30  Send email to waitlist (Segment A: most engaged)
08:00  Social media posts go live (all platforms simultaneously)
08:30  Product Hunt goes live (if applicable)
09:00  Send email Segment B (rest of list)
09:30  Community posts (Reddit, HN, forums — stagger by 30 min)
10:00  First engagement check — respond to ALL comments
11:00  Influencer/partner posts go live
12:00  Midday metrics check — any fires?
14:00  Second social push (different angle/content)
16:00  Thank-you post + early traction numbers
18:00  Send personalized DMs to high-value signups
20:00  Day 1 retrospective — what worked, what didn't
22:00  Plan Day 2 adjustments based on data
```

### 发布当天紧急沟通流程

**角色分配：**
- **指挥官** — 决定是否继续发布或中止发布，处理紧急情况 |
- **沟通负责人** — 负责社交媒体、社区反馈和公关 |
- **技术负责人** — 监控系统、解决问题、部署紧急修复 |
- **支持负责人** | 分类处理用户问题，识别问题模式 |
- **指标负责人** | 实时监控仪表盘，每小时更新数据 |

**紧急情况处理规则：**
- 网站瘫痪 → 技术负责人修复，指挥官决定是否公开沟通 |
- 负面新闻/病毒式投诉 → 沟通负责人起草回复，指挥官批准 |
- 支付问题 → 最高优先级，全员参与处理 |
- 功能请求过多 → 记录问题但不承诺立即解决，保持沟通 |
- 流量突然激增 → 技术负责人调整系统，指挥官决定如何应对 |

---

## 第五阶段：发布后的增长（第2-30天）

### 第1周：推动增长

| 时间 | 行动 | 目标 |
|------|--------|------|
| 第2天 | 联系第一天未激活的用户 | 激活他们 |
| 第3天 | 发布“第一天结果”帖子（保持透明） | 增加社交媒体证明 |
| 第4天 | 向反馈积极的社区发送定向推广信息 | 促进增长 |
| 第5天 | 收集并发布首批用户评价 | 建立信任 |
| 第6天 | 分析用户流失情况 | 优化产品流程 |
| 第7天 | 进行每周回顾 | 调整第二周的计划 |

### 第2-4周：优化

**激活流程分析：**

```yaml
funnel_analysis:
  stage_1_visit_to_signup:
    rate: ""
    benchmark: "3-8% for cold, 20-40% for warm"
    if_below: "Fix messaging, add social proof, simplify form"
    
  stage_2_signup_to_activation:
    rate: ""
    benchmark: "40-60%"
    if_below: "Simplify onboarding, add quick-win tutorial, reduce time-to-value"
    
  stage_3_activation_to_retention:
    rate: ""
    benchmark: "20-40% weekly"
    if_below: "Core value not clear, add engagement loops, email nurture"
    
  stage_4_retention_to_revenue:
    rate: ""
    benchmark: "2-5% free-to-paid"
    if_below: "Paywall placement, pricing, feature gating"
    
  stage_5_revenue_to_referral:
    rate: ""
    benchmark: "10-20% refer someone"
    if_below: "Add referral program, make sharing easy, incentivize"
```

### 用户反馈收集系统

**反馈收集频率：**
- 第1天：发送“设置体验如何？”的邮件 |
- 第3天：发送开放式问题邮件：“您遇到的最大挑战是什么？” |
- 第7天：收集NPS评分及用户推荐意见 |
- 第14天：收集功能需求 |
- 第30天：收集用户支付意愿及对定价的反馈

**反馈处理流程：**

| 信号 | 用户数量 | 处理方式 |
|--------|--------|--------|
| 错误报告 | 任何数量 | 在服务水平协议内修复（P0级问题：4小时内；P1级问题：24小时内；P2级问题：在下一个冲刺周期内） |
| 用户期望与实际不符 | 3名以上用户 | 更新信息或优化引导流程 |
| 对定价有疑问 | 3名以上用户 | 简化定价页面，添加常见问题解答 |
| 正面评价 | 任何数量 | 获得用户许可后发布在网站上 |

---

## 第六阶段：发布回顾

### 30天回顾模板

```yaml
launch_retrospective:
  summary:
    launch_date: ""
    launch_type: ""
    primary_goal: ""
    primary_metric_target: ""
    primary_metric_actual: ""
    goal_achieved: true/false
    
  channel_performance:
    - channel: "Email"
      reach: ""
      signups: ""
      conversion_rate: ""
      cost: ""
      cpa: ""
      verdict: ""  # Scale, Optimize, Cut
      
    - channel: "Product Hunt"
      reach: ""
      signups: ""
      conversion_rate: ""
      cost: ""
      cpa: ""
      verdict: ""
      
    # Repeat for each channel
    
  what_worked:
    - ""
    
  what_didnt:
    - ""
    
  surprises:
    - ""  # Unexpected channels, user segments, use cases
    
  key_learnings:
    - ""
    
  next_launch_changes:
    - ""
    
  90_day_plan:
    growth_channels: []  # Double down on winners
    product_priorities: []  # Based on user feedback
    revenue_target: ""
    retention_target: ""
```

### 渠道效果评估

针对每个渠道，计算其效果：

```
Channel Score = (Signups × Quality Score) / Cost

Quality Score (0-1):
- Activated within 7 days? +0.3
- Still active at day 30? +0.3
- Converted to paid? +0.4
```

根据评分对渠道进行排名。排名前2-3的渠道将成为推动产品增长的主要渠道。评分低于0.2的渠道则需考虑调整。

---

## 发布攻略模板

### 模板1：SaaS产品发布

```
T-8w: Positioning + beta recruitment
T-6w: Beta launch (50-100 users)
T-4w: Iterate based on beta feedback
T-3w: Waitlist page + content engine starts
T-2w: Press/influencer outreach
T-1w: Email sequences loaded, social scheduled
T-0:  Launch day (email + social + communities + PH)
T+1w: Activation optimization sprint
T+2w: First case studies published
T+4w: Paid acquisition experiments begin
T+8w: Growth channel identified, double down
```

### 模板2：B2B服务发布

```
T-6w: Package service offering + pricing
T-4w: Build landing page + 2 case studies (even from free work)
T-3w: Warm outreach to network (personal emails, not mass)
T-2w: LinkedIn content series (expertise, not selling)
T-1w: Prep sales materials (deck, one-pager, ROI calculator)
T-0:  Announce to network + 10 targeted cold outreach
T+1w: Follow up all conversations, book demos
T+2w: Publish "how we helped [client]" content
T+4w: Referral program launch
T+8w: Scale outreach based on what converts
```

### 模板3：内容产品/课程发布

```
T-6w: Create lead magnet (free chapter, mini-course)
T-4w: Email list building sprint (ads, content, partnerships)
T-3w: Behind-the-scenes content (build in public)
T-2w: Early bird pricing announced
T-1w: Testimonials from beta reviewers
T-0:  Cart open (scarcity: limited seats or early bird ends)
T+3d: Social proof push (X people enrolled, first wins)
T+5d: Objection-handling email (FAQ, guarantee)
T+7d: Cart close (or early bird ends)
T+2w: First cohort results → next launch cycle
```

### 模板4：现有功能更新

```
T-2w: Beta test with power users
T-1w: Update docs, record demo video
T-3d: Email existing users (teaser)
T-0:  In-app announcement + email + changelog + social
T+1d: Targeted outreach to users who requested this feature
T+3d: Usage metrics review — adoption rate
T+1w: Iterate based on feedback, publish how-to content
T+2w: Retrospective — did it move the needle?
```

---

## 高级策略

### 产品推荐活动优化

**准备阶段（发布前4周）：**
- [ ] 确定发布日期（周二至周四，避开节假日） |
- [ ] 选定推广人员（具有粉丝的人或自行推广） |
- [ ] 标语：不超过60个字符，简洁且吸引人 |
- [ ] 准备第一条评论（个人故事，而非销售话术） |
- [ ] 准备5张以上高质量截图/GIF |
- [ ] 准备制作推广视频（可选，时长60-90秒） |
- [ ] 支持团队准备好回答用户问题 |

**发布当天：**
- 在太平洋标准时间00:01发布 |
- 在社区分享，但不要请求点赞 |
- 在30分钟内回复所有评论 |
- 全天分享真实的幕后信息 |
- 个别感谢支持者

**推广活动结束后：**
- 在网站上添加推广活动的标识 |
- 向参与推广活动的用户发送特别欢迎邮件 |
- 分析推广活动的流量质量与其他渠道的对比

### Hacker News发布指南

- 发布内容格式：“在Hacker News上展示：[产品名称] — [产品的功能介绍]”
- 最佳发布时间：美国东海岸的工作日早晨 |
- 在评论中详细解释产品的技术细节 |
- 诚实地回应用户的批评（Hacker News重视真实性而非营销手段 |
- 绝不要请求点赞 |
- 做好监控准备——Hacker News上的负面评价可能会对产品造成影响 |

### 病毒式传播策略设计

```yaml
viral_loop:
  trigger: ""  # What makes someone share?
  mechanism: ""  # How do they share? (invite, link, embed, social)
  incentive:
    sharer: ""  # What does the referrer get?
    receiver: ""  # What does the new user get?
  friction: ""  # How many clicks to share? (Target: 1-2)
  visibility: ""  # Can non-users SEE the product in use? (Powered by, watermark, social share)
  
  viral_coefficient:
    invites_per_user: ""
    conversion_per_invite: ""
    k_factor: ""  # invites × conversion. K>1 = viral growth
```

### 定价发布策略

| 定价策略 | 实施方法 | 适用场景 |
|---------|-------------|----------|
| **创始价** | 早期用户可享受30-50%的折扣，折扣永久有效 | 建立忠实用户群体 |
| **早鸟价** | 折扣在X天后失效 | 创造紧迫感 |
| **免费试用+付费升级** | 免费版本吸引用户，付费版本促进转化 | 面向大量B2C用户/开发者 |
| **从测试版到正式发布逐步涨价** | 随着产品成熟逐步提高价格 | 验证用户的支付意愿 |
| **用户自选价格** | 用户自行选择价格（提供参考价格） | 适用于社区驱动型产品 |

**发布当天的定价展示方式：**
1. 先展示“正常价格”（用划线标出） |
2. 显示折扣后的价格 |
3. 提醒折扣截止时间（“折扣有效期至[日期]” |
4. 强调产品价值（例如：“包含价值2000美元的模板”）

---

## 特殊情况与应对策略

### 在竞争激烈的市场中发布
- 强调“与[竞争对手]不同，我们的特点是[具体差异]”
- 面向竞争对手最不满意的用户（搜索“[竞争对手]的替代产品”）
- 准备迁移工具或对比内容 |
- 不要在功能上竞争，而是在体验、价格或细分市场上进行竞争 |

### 在没有受众的情况下发布
- 通过一对一的推广开始（发送100封个性化邮件，而非批量发送）
- 找到3-5个用户聚集的微型社区 |
- 在这些社区免费提供帮助（建立口碑） |
- 与已有受众的合作伙伴合作（共享收益） |
- 在公开平台上进行推广，并记录整个过程（人们更支持弱势方）

### 发布失败后的恢复措施
如果发布效果不佳：
1. 不要恐慌——大多数成功的产品都是低调发布的 |
2. 分析问题：是产品、信息传递、渠道还是时机造成的？ |
- 如有必要，重新定位产品或调整策略 |
- 面向不同的受众或渠道重新发布 |
- 专注于10位满意用户，而非1000位冷淡的用户 |

### 国际化发布
- 根据当地文化调整信息内容（不仅仅是翻译） |
- 尊重当地的价格策略（进行价格调整，使用当地支付方式） |
- 按地区分阶段发布 |
- 根据地区选择合适的本地影响者 |
- 注意法律和合规问题（数据隐私、条款、税收）

---

## 快速命令

| 命令 | 功能 |
|---------|-------------|
| “评估我的发布准备情况” | 运行6维度的准备情况评分 |
| “生成发布简报” | 生成发布简报的YAML模板 |
| “规划我的产品推荐活动” | 生成特定活动的检查清单和时间表 |
| “制定我的发布前内容计划” | 制定8周的内容计划 |
| “设计我的发布当天计划” | 制定详细的小时级计划 |
| “分析我的发布流程” | 分析发布后的用户反馈 |
| “进行30天回顾” | 生成完整的发布回顾报告 |
| “评估我的发布渠道效果” | 分析各渠道的效果 |
| “帮助我重新发布” | 提供发布失败的恢复方案 |
| “设计病毒式传播机制” | 设计推荐和分享策略 |

---

## 相关AfrexAI工具

- **afrexai-brand-strategy** — 发布前的定位和信息传递 |
- **afrexai-seo-content-engine** | 用于提升自然流量的发布前内容 |
- **afrexai-email-marketing-engine** | 发布前的电子邮件序列 |
- **afrexai-social-media-engine** | 社交媒体推广活动 |
- **afrexai-competitive-intel** | 发布前了解市场情况 |
- **afrexai-pricing-strategy** | 确定正确的定价策略 |
- **afrexai-prd-engine** | 在发布前明确产品功能 |