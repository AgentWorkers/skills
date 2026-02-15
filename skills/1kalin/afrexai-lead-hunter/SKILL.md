---
name: afrexai-lead-hunter
description: "企业级B2B潜在客户生成、信息完善、评分以及自动化外联流程，专为AI代理设计。系统能够自动寻找理想的目标客户，利用经过验证的数据完善客户信息，根据您的业务指标（ICP）对客户进行评分，并生成个性化的营销策略。"
tags: [leads, sales, b2b, prospecting, enrichment, outreach, pipeline, crm, cold-email, icp]
author: AfrexAI
version: 1.0.0
license: MIT
---

# AfrexAI Lead Hunter Pro

> 将您的人工智能销售代理转变为一个完整的B2B销售开发工具：从发现潜在客户到跟进沟通，再到完成交易，全程无需人工干预。

---

## 架构

```
DEFINE ICP ──▶ DISCOVER ──▶ ENRICH ──▶ SCORE ──▶ SEGMENT ──▶ OUTREACH ──▶ CRM
    │              │            │          │          │            │          │
    ▼              ▼            ▼          ▼          ▼            ▼          ▼
 Persona      Multi-source  Email+Phone  ICP fit   Tier A/B/C  Sequences  Pipeline
 Builder      Web Research  Company Data  Intent    Campaigns   Templates  Tracking
```

---

## 第一阶段：定义理想客户画像（ICP）

在开始寻找潜在客户之前，首先要明确您要寻找的目标客户群体。请回答以下问题：

### 公司层面的ICP（Ideal Company Profile）
```yaml
# Copy and customize this ICP template
company:
  industries: [SaaS, fintech, legal-tech, prop-tech]
  employee_range: [50, 500]        # sweet spot for AI adoption
  revenue_range: [$5M, $100M]      # can afford $120K+ contracts
  funding_stage: [Series A, Series B, Series C]
  tech_signals:                     # tools that indicate AI readiness
    positive: [Salesforce, HubSpot, Snowflake, AWS, Python]
    negative: [no-website, wordpress-only]
  geography: [US, UK, Canada, Australia]
  pain_signals:                     # problems they're likely facing
    - "manual data entry"
    - "compliance overhead"
    - "scaling operations"
    - "document processing"
```

### 买家画像（Buyer Persona）
```yaml
persona:
  titles: [CEO, CTO, COO, VP Operations, Head of Innovation, Director of IT]
  seniority: [C-Suite, VP, Director]
  decision_authority: true          # can sign $50K+ without board approval
  linkedin_activity:                # signals they're actively looking
    - posts about AI/automation
    - comments on digital transformation content
    - recently changed roles (first 90 days = buying window)
  anti-signals:                     # skip these
    - "consultant" in title (not buyers)
    - company < 10 employees (no budget)
    - already has AI vendor (check for competitors in their stack)
```

### 评分标准（Scoring Criteria）
```yaml
scoring:
  icp_company_match: 30             # how well company matches
  icp_persona_match: 20             # right title + seniority
  intent_signals: 25                # actively looking for solutions
  engagement_recency: 15            # recent activity online
  timing_bonus: 10                  # new role, funding round, hiring
  
  thresholds:
    tier_a: 80                      # hot — outreach immediately
    tier_b: 60                      # warm — nurture sequence
    tier_c: 40                      # cool — add to newsletter
    disqualify: below 40            # don't waste time
```

---

## 第二阶段：多渠道信息收集

### 来源优先级矩阵（Source Priority Matrix）

| 来源 | 适合对象 | 搜索方法 | 数据质量 | 成本 |
|--------|----------|---------------|-------------|------|
| **网络搜索** | 任何行业 | `"[行业] companies" site:linkedin.com/company` | 高 | 免费 |
| **GitHub** | 开发工具公司、科技企业 | 搜索代码库、组织页面、贡献者资料 | 高 | 免费 |
| **产品发布信息** | 初创企业、SaaS公司 | 浏览新产品发布信息、点赞用户（他们可能是潜在买家） | 中等 | 免费 |
| **行业榜单** | 目标行业内的领先企业 | “2026年[行业]前50强企业”，Clutch、G2 | 高 | 免费 |
| **招聘网站** | 招聘活跃的公司 | 搜索包含“AI”或“自动化”关键词的职位信息 | 高 | 免费 |
| **Crunchbase** | 获得融资的初创企业 | 目标行业内的最新融资企业 | 高 | 免费/付费 |
| **会议演讲者** | 行业内的知名人士 | 从行业活动中获取演讲者名单 | 非常高 | 免费 |
| **播客嘉宾** | 有预算的思想领袖 | 搜索相关播客的文字记录 | 高 | 免费 |

### 信息收集模板

**通过业务痛点查找潜在客户：**
```
"[industry]" "manual process" OR "time-consuming" OR "looking for solutions" site:linkedin.com
```

**通过招聘活动寻找潜在客户（招聘活跃的企业通常有购买需求）：**
```
"[company type]" "hiring" "AI" OR "automation" OR "data" site:linkedin.com/jobs
```

**寻找最近获得融资的企业（资金充足）：**
```
"[industry]" "raises" OR "Series A" OR "funding" OR "investment" 2026
```

**寻找使用竞争对手产品的企业（适合推荐替代方案）：**
```
"[competitor tool]" "alternative" OR "switching from" OR "replaced"
```

**直接联系决策者：**
```
"[title]" "[industry]" "[city/region]" site:linkedin.com/in
```

### 信息收集工作流程（Discovery Workflow）
```
FOR each search query:
  1. Run web_search with the query
  2. Extract company names + URLs from results
  3. Deduplicate against existing leads
  4. For each NEW company:
     a. Visit company website → extract: industry, size estimate, tech signals
     b. Search "[company name] CEO" OR "[company name] founder" → get decision maker
     c. Search "[company name] funding" → get financial signals
     d. Create lead record (see schema below)
  5. Rate limit: 2-3 second delay between searches
```

---

## 第三阶段：数据补充（Enrichment）

对每个发现的潜在客户进行数据补充，确保信息的准确性：

### 公司信息补充 checklist
- [ ] **网站** — 加载公司主页，提取核心价值主张和技术栈（检查`<meta>`标签、JavaScript框架）
- [ ] **员工人数** — 从LinkedIn公司页面、Crunchbase或公司“关于”页面获取
- [ ] **收入预估** — 根据融资金额乘以3-5的倍数估算，或参考行业平均水平
- [ ] **技术栈** — 查看BuiltWith、Wappalyzer的数据，或招聘信息中的技术相关内容
- [ ] **最新动态** — 过去90天内的融资、新产品发布、高管变动、合作伙伴关系
- [ ] **业务痛点** — 招聘信息中提到的问题，或博客文章中讨论的挑战
- **竞争对手使用情况** — 该公司是否使用竞争对手的产品？使用的是哪家？（参考G2的评论和案例研究）

### 联系人信息补充 checklist
- [ ] **全名** — 从LinkedIn或公司页面获取名字和姓氏
- [ ] **职位** — 当前职位（确认与买家画像匹配）
- [ ] **电子邮件格式** — 分析公司常用的电子邮件格式（如first@、first.last@、firstlast@、f.last@）
- [ ] **电子邮件验证** — 用已知格式测试邮件地址，检查MX记录
- [ ] **LinkedIn链接** — 获取公司的LinkedIn个人资料链接
- [ ] **近期活动** — 过去30天内发布或分享的内容
- **共同联系人** — 您的人脉中是否有与该联系人关联的人？
- **兴趣领域** — 他们关注哪些主题？（用于个性化沟通）

### 电子邮件格式检测（Email Pattern Detection）
```
Common patterns (test in order of likelihood):
1. first.last@company.com     (most common, ~40%)
2. first@company.com          (startups, ~25%)
3. firstlast@company.com      (~15%)
4. flast@company.com           (~10%)
5. first_last@company.com     (~5%)
6. last.first@company.com     (~3%)
7. first.l@company.com        (~2%)

Verification approach:
- Check if company has public team page with email format
- Look for email in GitHub commits from company domain
- Check email format on Hunter.io or similar (if available)
- Search "[person name] email [company]" 
- Check their personal website/blog for contact
```

---

## 第四阶段：潜在客户评分算法

使用以下标准对每个潜在客户进行0-100分的评分：

### 公司评分（0-30分）

| 评分标准 | 分数 | 检查方法 |
|--------|--------|-------------|
| 行业与理想客户画像完全匹配 | +10 | 与ICP配置对比 |
| 员工人数在理想范围内 | +5 | 从LinkedIn或公司网站获取 |
| 收入在目标范围内 | +5 | 根据Crunchbase数据或预估 |
| 位于目标地理位置 | +3 | 从网站或LinkedIn获取 |
| 使用兼容的技术栈 | +4 | 从招聘信息或BuiltWith工具获取 |
| 当前没有使用竞争对手产品 | +3 | 通过调研和案例研究确认 |

### 买家画像评分（0-20分）

| 评分标准 | 分数 | 检查方法 |
|--------|--------|-------------|
| 职位与买家画像匹配 | +8 | 从LinkedIn获取 |
| 担任高管或副总裁级别 | +5 | 从LinkedIn获取 |
| 具有决策权 | +4 | 根据职位和公司规模判断 |
| 在LinkedIn上活跃（每月有发文） | +3 | 从LinkedIn活动记录判断 |

### 意图评分（0-25分）

| 评分标准 | 分数 | 检查方法 |
|--------|--------|-------------|
| 最近发布过与业务痛点相关的内容 | +8 | 从LinkedIn或Twitter获取 |
| 公司正在招聘您提供的职位 | +7 | 从招聘网站获取 |
| 参加过相关行业活动 | +5 | 从会议列表获取 |
| 下载过竞争对手的产品资料 | +3 | 难以验证，可忽略 |
| 搜索过相关解决方案 | +2 | 难以验证，可忽略 |

### 时间评分（0-15分）

| 评分标准 | 分数 | 检查方法 |
|--------|--------|-------------|
| 新上任（任职时间<90天） | +5 | 从LinkedIn获取任职日期 |
| 公司刚获得融资 | +4 | 从Crunchbase或新闻获取 |
| 季末（预算充足） | +3 | 根据日历判断 |
| 公司发展迅速（招聘活跃） | +3 | 从招聘信息数量判断 |

### 互动评分（0-10分）

| 评分标准 | 分数 | 检查方法 |
|--------|--------|-------------|
| 打开了之前的邮件 | +4 | 通过邮件跟踪系统确认 |
| 访问过您的网站 | +3 | 通过分析系统确认 |
| 与您在LinkedIn上建立了联系 | +2 | 从LinkedIn记录确认 |
| 由他人推荐 | +1 | 从CRM系统记录确认 |

---

## 第五阶段：客户分类与营销策略分配

### A级潜在客户（评分80-100分）—— 高价值潜在客户
```
Action: Immediate personalized outreach
Sequence: 5-touch hyper-personalized campaign
Timeline: Contact within 24 hours
Channel: Email → LinkedIn → Phone (if available)
Template: "CEO-to-CEO" or "Specific Pain" (see below)
```

### B级潜在客户（评分60-79分）—— 中等价值潜在客户
```
Action: Nurture sequence
Sequence: 7-touch value-first campaign  
Timeline: Start within 48 hours
Channel: Email → LinkedIn
Template: "Value Insight" or "Case Study" (see below)
```

### C级潜在客户（评分40-59分）—— 低价值潜在客户
```
Action: Add to newsletter + long-term nurture
Sequence: Monthly value content
Timeline: Bi-weekly touchpoints
Channel: Email only
Template: "Industry Report" or "Educational" (see below)
```

---

## 第六阶段：营销沟通模板

### 模板1：针对具体业务痛点的沟通策略（A级潜在客户）

**邮件1 — 第0天（吸引注意）**
```
Subject: [specific pain point] at [Company]?

Hi [First Name],

Noticed [Company] is [specific observation — hiring for X role / posted about Y challenge / using Z tool].

That usually means [pain point they're likely feeling].

We built [solution] that [specific result with number]. [Client name] cut their [metric] by [X%] in [timeframe].

Worth a 15-min call to see if it fits [Company]?

[Your name]
```

**邮件2 — 第3天（提供证据）**
```
Subject: Re: [original subject]

[First Name] — quick follow-up.

Here's exactly what we did for [similar company]: [1-sentence case study with specific numbers].

[Link to case study or calculator]

Happy to walk through how this maps to [Company].

[Your name]
```

**邮件3 — 第7天（深入探讨）**
```
Subject: [industry trend] + [Company]

[First Name],

[Industry trend or stat that's relevant]. Companies like [Company] are [what smart companies are doing about it].

We help [type of company] [specific outcome]. Takes about [timeframe] to see results.

Open to a quick chat this week?

[Your name]
```

**邮件4 — 第14天（结束沟通）**
```
Subject: Should I close your file?

[First Name],

I've reached out a few times — totally understand if the timing isn't right.

If [pain point] becomes a priority, here's a [free resource] that might help: [link]

Either way, I'll stop filling your inbox. Just reply "yes" if you'd like to chat sometime.

[Your name]
```

### 模板2：以价值为导向的沟通策略（B级潜在客户）

**邮件1 — 首先提供有价值的见解，而非直接推销产品**
```
Subject: [number] [industry] companies are doing [thing] wrong

Hi [First Name],

We analyzed [X] companies in [industry] and found that [surprising insight].

The ones getting it right are [what top performers do differently].

Put together a quick breakdown: [link to free resource/calculator]

Thought it'd be useful given what [Company] is building.

[Your name]
```

### 模板3：LinkedIn预热策略

**步骤1：查看他们的个人资料（触发通知）**
**步骤2（第2天）：对他们最近发布的帖子点赞/评论（真诚且非泛泛而谈）**
**步骤3（第4天）：发送联系请求，并附上说明：**
```
Hi [Name] — been following [Company]'s work in [space]. 
Particularly liked your take on [specific post topic]. 
Would love to connect.
```
**步骤4（收到回复后第7天）：发送有价值的信息（而非推销内容）：**
```
[Name] — saw you mentioned [challenge] in your recent post. 
We put together [free resource] that addresses exactly that. 
Thought you might find it useful: [link]
```

---

## 第七阶段：客户关系管理（CRM）与销售流程管理

### 潜在客户记录结构（Lead Record Schema）
```json
{
  "id": "lead-001",
  "created": "2026-02-13",
  "source": "web-search",
  
  "company": {
    "name": "Acme Corp",
    "website": "https://acme.com",
    "industry": "SaaS",
    "employees": 150,
    "revenue_est": "$20M",
    "funding": "Series B — $15M (2025)",
    "tech_stack": ["Salesforce", "AWS", "React"],
    "location": "San Francisco, CA"
  },
  
  "contact": {
    "first_name": "Jane",
    "last_name": "Smith",
    "title": "VP of Operations",
    "email": "jane.smith@acme.com",
    "email_verified": false,
    "linkedin": "https://linkedin.com/in/janesmith",
    "phone": null
  },
  
  "scoring": {
    "company_score": 25,
    "persona_score": 18,
    "intent_score": 15,
    "timing_score": 8,
    "engagement_score": 0,
    "total": 66,
    "tier": "B"
  },
  
  "enrichment": {
    "pain_signals": ["hiring 3 data analysts", "blog about manual reporting"],
    "recent_news": ["Raised Series B in Jan 2026"],
    "competitor_usage": "None detected",
    "content_interests": ["data automation", "operational efficiency"]
  },
  
  "outreach": {
    "status": "not_started",
    "sequence": "value-first",
    "emails_sent": 0,
    "last_contacted": null,
    "next_action": "2026-02-14",
    "replies": [],
    "notes": ""
  },
  
  "pipeline": {
    "stage": "prospect",
    "deal_value": null,
    "probability": 0,
    "next_step": "Initial outreach"
  }
}
```

### 销售流程阶段（Pipeline Stages）
```
PROSPECT → CONTACTED → REPLIED → MEETING_BOOKED → QUALIFIED → PROPOSAL → NEGOTIATION → CLOSED_WON / CLOSED_LOST
```

### 监控指标（Tracking Metrics）

每周监控以下指标以优化销售流程：
- **发现率**：每次搜索会话发现的潜在客户数量
- **数据补充完成率**：每个潜在客户的字段填写完成率
- **客户分类比例**：A级、B级、C级各占多少？
- **回复率**：收到的回复数/发送的邮件数（目标：5-15%）
- **会议转化率**：会议次数/收到的回复数（目标：30-50%）
- **成交率**：达成交易的潜在客户数/会议次数（目标：20-30%）
- **销售周期**：从发现潜在客户到完成交易的平均天数

---

## 第八阶段：自动化与日程安排

### 日常自动化流程（Daily Autopilot Routine）
```
MORNING (agent runs autonomously):
  1. Run 3-5 discovery searches (rotate queries)
  2. Enrich any un-enriched leads from yesterday
  3. Score new leads
  4. Send Day-N emails for active sequences
  5. Check for replies → flag for human review
  6. Update pipeline stages
  7. Report: "Found X leads, sent Y emails, Z replies"

WEEKLY:
  1. Review Tier C leads — any moved to B/A?
  2. Clean dead leads (no response after full sequence)
  3. Analyze response rates by template — A/B test
  4. Refresh ICP based on closed deals
  5. Add new search queries based on wins
```

### 与销售代理的集成（Agent Integration）
```
# In your agent's heartbeat or cron:
1. Load ICP config
2. Run discovery for 1 search query
3. Enrich top 5 new leads
4. Score all unscored leads
5. Queue outreach for Tier A leads
6. Log results to daily brief
```

---

## 输出格式

### CSV导出（Export Formats）
```csv
company,contact,title,email,linkedin,score,tier,industry,employees,pain_signal
Acme Corp,Jane Smith,VP Ops,jane@acme.com,linkedin.com/in/jane,66,B,SaaS,150,hiring analysts
```

### 周报模板（Weekly Report Template）
```markdown
# Lead Hunter Weekly Report — Week of [DATE]

## Pipeline Summary
- Total leads in system: [N]
- New leads this week: [N]  
- Tier A: [N] | Tier B: [N] | Tier C: [N]

## Outreach Performance
- Emails sent: [N]
- Reply rate: [X%]
- Meetings booked: [N]
- Pipeline value added: $[X]

## Top Leads This Week
1. [Company] — [Contact] — Score: [X] — [Why they're hot]
2. [Company] — [Contact] — Score: [X] — [Why they're hot]
3. [Company] — [Contact] — Score: [X] — [Why they're hot]

## Insights
- Best performing search query: [query]
- Best performing email template: [template]
- Recommendation: [action to take]
```

---

## 专业建议

1. **90天黄金期**：新上任的高管在入职前90天内购买产品的概率是平时的10倍。优先关注“新上任”这一信号。
2. **招聘活动 = 购买需求**：如果一家公司正在招聘您产品所替代的职位，说明他们有购买意愿且预算充足。这些是最高价值的潜在客户。
3. **竞争对手的客户**：搜索关于竞争对手的评论或投诉信息。不满意的客户最有可能更换产品。
4. **行业会议名单**：行业活动的演讲者和参与者名单非常有用。这些人通常对该领域非常关注。
5. **“回复任何信息”原则**：任何回复（即使表示“不感兴趣”）都很有价值。这可以确认邮件已送达且目标客户确实存在。请记录下来。
6. **个性化沟通 > 数量**：20封高度个性化的邮件比200封泛泛而谈的邮件效果更好。务必在邮件中提及潜在客户的特定需求。
7. **多渠道沟通**：不要只依赖与每个公司的单一联系人联系。寻找2-3位决策者，并从不同角度进行沟通。
8. **沟通时机很重要**：当地时间周二至周四上午8-10点是打开邮件的高峰期。避免周一和周五。

---

*由[AfrexAI](https://afrexai-cto.github.io/context-packs/)开发——真正能促成销售的AI销售工具。*