# 📊 AI商业计划生成器 — 10分钟内即可完成、完全适合投资者的商业计划

**slug:** `ai-business-plan-generator`  
**类别:** 创业 / 商业策略  
**技术支持:** [Apify](https://www.apify.com?fpr=dx06p) + [InVideo AI](https://invideo.sjv.io/TBB) + Claude AI

> 输入您的商业想法，即可获得一份**完整且适合投资者的商业计划**：包含实时市场研究、竞争对手分析、财务预测以及演示文稿视频。这正是风险投资机构、银行或加速器所需要的所有信息。整个流程仅需10分钟。

---

## 💥 为什么这项技能在ClawHub上会大受欢迎

每位创业者、初创公司创始人、自由职业者或学生，在某个阶段都需要一份商业计划书。商业计划咨询公司的收费通常在**1,500美元至10,000美元**之间。然而，95%的提案因研究不充分或数据不真实而被拒绝。

这项技能能够以不到2美元的成本，生成一份**基于数据、结构严谨的商业计划书**：包含实时市场研究、真实的竞争对手信息以及合理的财务预测。

**自动化流程包括：**
- 🌍 从可靠来源抓取**实时市场数据**（总市场规模TAM、可服务市场SAM、潜在市场SOM）
- 🏆 分析**前五大竞争对手**（优势、劣势、定价策略、市场定位）
- 💰 建模**三年财务预测**（收入、成本、盈亏平衡点、资金消耗速度）
- 📋 生成**完整的商业计划书**（包含所有12个标准章节）
- 🎬 通过InVideo AI制作**60秒的演示文稿视频**（非常适合提交给加速器）
- 📊 编写**投资者专用的高层摘要**（风险投资机构会优先阅读的一页内容）

---

## 🛠️ 使用的工具

| 工具 | 功能 |
|---|---|
| [Apify](https://www.apify.com?fpr=dx06p) — 谷歌搜索爬虫 | 获取市场规模数据、行业报告、市场趋势 |
| [Apify](https://www.apify.com?fpr=dx06p) — 网站内容爬取工具 | 收集竞争对手的网站信息（定价、定位、功能） |
| [Apify](https://www.apify.com?fpr=dx06p) — LinkedIn公司信息爬取工具 | 获取竞争对手的团队规模、融资情况、发展动态 |
| [Apify](https://www.apify.com?fpr=dx06p) — 谷歌新闻爬虫 | 获取行业新闻、融资轮次信息 |
| [Apify](https://www.apify.com?fpr=dx06p) — Reddit爬虫 | 了解客户痛点及市场反馈 |
| [InVideo AI](https://invideo.sjv.io/TBB) | 根据商业计划书生成60秒的演示文稿视频 |
| Claude AI | 撰写所有12个章节的内容、进行财务建模、编写高层摘要 |

---

## ⚙️ 完整的工作流程

```
INPUT: Business idea + industry + target market + funding goal
        ↓
STEP 1 — Live Market Research
  └─ TAM / SAM / SOM from real industry data
  └─ Market growth rate & key trends
  └─ Regulatory environment & barriers to entry
        ↓
STEP 2 — Competitor Intelligence
  └─ Top 5 competitors: pricing, features, positioning
  └─ Their funding history & team size
  └─ Weaknesses = your opportunity gaps
        ↓
STEP 3 — Customer Validation Data
  └─ Reddit: real pain points from your target audience
  └─ Google trends: demand trajectory
  └─ Review mining: what customers hate about existing solutions
        ↓
STEP 4 — Claude AI Writes Full 12-Section Plan
  └─ Executive Summary
  └─ Company Description
  └─ Market Analysis
  └─ Competitive Analysis
  └─ Products & Services
  └─ Marketing & Sales Strategy
  └─ Operations Plan
  └─ Management Team
  └─ Financial Projections (3 years)
  └─ Funding Requirements
  └─ Risk Analysis
  └─ Exit Strategy
        ↓
STEP 5 — Financial Model Built
  └─ Revenue projections (3 scenarios: conservative / base / optimistic)
  └─ Cost structure & burn rate
  └─ Break-even analysis
  └─ Unit economics (CAC, LTV, payback period)
        ↓
STEP 6 — InVideo AI Produces Pitch Video
  └─ 60-second elevator pitch video
  └─ Problem → Solution → Market → Traction → Ask
  └─ Professional voiceover + visuals
  └─ Perfect for accelerator applications & investor emails
        ↓
OUTPUT: Full 12-section business plan + financial model + pitch video
```

---

## 📥 输入内容

```json
{
  "business": {
    "idea": "AI-powered meal planning app that generates weekly plans based on health goals, dietary restrictions, and local grocery prices",
    "industry": "Health Tech / FoodTech",
    "stage": "Pre-seed / Idea stage",
    "location": "United States",
    "target_market": "Health-conscious adults 25-45 with busy lifestyles"
  },
  "funding": {
    "amount_seeking": 500000,
    "type": "seed round",
    "use_of_funds": "Product development (60%), Marketing (25%), Operations (15%)"
  },
  "founders": {
    "team_size": 2,
    "background": "1 engineer, 1 nutritionist"
  },
  "production": {
    "invideo_api_key": "YOUR_INVIDEO_API_KEY",
    "pitch_video_style": "clean_professional"
  },
  "apify_token": "YOUR_APIFY_TOKEN"
}
```

---

## 📤 输出示例

```json
{
  "executive_summary": {
    "company": "NutriPlan AI",
    "tagline": "Eat smarter. Spend less. Live healthier.",
    "problem": "83% of Americans want to eat healthier but cite time and cost as the #1 barrier. Existing meal planning apps ignore local grocery prices and real dietary restrictions.",
    "solution": "NutriPlan AI generates fully personalized weekly meal plans in 60 seconds — synced with local grocery store prices, dietary needs, and health goals. Users save an average of $180/month on groceries.",
    "market": "TAM: $8.2B (digital health & nutrition apps). SAM: $1.4B (US meal planning market). SOM: $42M (Year 3 target).",
    "traction": "Pre-launch waitlist: 2,400 signups in 3 weeks via organic TikTok content.",
    "ask": "Raising $500K seed round to complete MVP and acquire first 10,000 paid users.",
    "funding_use": "Product development (60%), Performance marketing (25%), Operations (15%)"
  },
  "market_analysis": {
    "tam": "$8.2 billion — global digital health & nutrition app market",
    "sam": "$1.4 billion — US meal planning & nutrition software",
    "som": "$42 million — realistic 3-year addressable share",
    "growth_rate": "14.2% CAGR through 2028 (source: Grand View Research, scraped live)",
    "key_trends": [
      "AI personalization becoming expected standard in health apps",
      "Grocery inflation driving demand for budget-conscious meal planning",
      "Gen Z & Millennials spending 3x more on health apps vs 2020"
    ]
  },
  "competitive_analysis": {
    "competitors": [
      {
        "name": "Mealime",
        "pricing": "Free / $5.99/month",
        "strengths": "Clean UI, large recipe library",
        "weaknesses": "No grocery price integration, generic meal plans",
        "your_edge": "Real-time local grocery pricing + AI personalization"
      },
      {
        "name": "PlateJoy",
        "pricing": "$69/year",
        "strengths": "Detailed health questionnaire",
        "weaknesses": "Expensive, no budget optimization",
        "your_edge": "50% cheaper + budget-first approach"
      }
    ],
    "competitive_moat": "Proprietary grocery price API integration — competitors would need 12+ months to replicate"
  },
  "financial_projections": {
    "model": "SaaS subscription — $9.99/month or $79/year",
    "year_1": { "users": 8000, "mrr": "$52,000", "arr": "$624,000", "burn_rate": "$28,000/month" },
    "year_2": { "users": 31000, "mrr": "$198,000", "arr": "$2,376,000", "burn_rate": "$45,000/month" },
    "year_3": { "users": 89000, "mrr": "$580,000", "arr": "$6,960,000", "burn_rate": "$72,000/month" },
    "break_even": "Month 18",
    "unit_economics": {
      "cac": "$12 (organic-first strategy)",
      "ltv": "$127 (avg 12.7 month retention)",
      "ltv_cac_ratio": "10.6x",
      "payback_period": "1.8 months"
    }
  },
  "pitch_video": {
    "script": "Hook: 'What if eating healthy didn't mean spending hours planning or going broke at the grocery store?'\nProblem: '83% of Americans want to eat healthier. Most fail because it costs too much time and money.'\nSolution: 'NutriPlan AI generates your perfect weekly meal plan in 60 seconds — personalized to your goals and synced with your local grocery prices.'\nTraction: '2,400 people joined our waitlist in 3 weeks without a single paid ad.'\nAsk: 'We're raising $500K to bring this to 10,000 paid users. Join us.'\nCTA: 'Link in bio to learn more.'",
    "duration": "60s",
    "status": "produced",
    "video_file": "outputs/nutriplan_pitch_video.mp4"
  }
}
```

---

## 🧠 Claude AI的使用方法

```
You are a world-class startup advisor, business plan writer, and financial modeler.

LIVE MARKET DATA FROM SCRAPING:
{{market_research_data}}

COMPETITOR INTELLIGENCE:
{{competitor_data}}

CUSTOMER PAIN POINTS:
{{reddit_and_review_data}}

BUSINESS PROFILE:
- Idea: {{business_idea}}
- Industry: {{industry}}
- Stage: {{stage}}
- Target market: {{target_market}}
- Funding ask: ${{funding_amount}}
- Team: {{team_background}}

GENERATE A COMPLETE 12-SECTION BUSINESS PLAN:
1. Executive Summary (1 page — make every word count)
2. Company Description (mission, vision, legal structure)
3. Market Analysis (TAM/SAM/SOM with real data, CAGR, trends)
4. Competitive Analysis (5 competitors, feature matrix, your moat)
5. Products & Services (what you sell, how it works, IP/tech edge)
6. Marketing & Sales Strategy (channels, CAC targets, growth loops)
7. Operations Plan (tech stack, team structure, key processes)
8. Management Team (founder backgrounds, advisors, gaps)
9. Financial Projections (3-year P&L, monthly Year 1, unit economics)
10. Funding Requirements (amount, use of funds, milestones unlocked)
11. Risk Analysis (top 5 risks + mitigation strategies)
12. Exit Strategy (acquisition targets, IPO path, timeline)

FINANCIAL MODEL RULES:
- 3 scenarios: conservative (base -40%), base, optimistic (base +60%)
- Show monthly for Year 1, quarterly for Years 2-3
- Include CAC, LTV, LTV/CAC ratio, payback period
- Break-even month clearly stated

TONE: Professional. Data-backed. Confident but not delusional.
Investors have seen 10,000 plans — make this one feel grounded and real.
OUTPUT: Valid JSON only. No markdown. No preamble.
```

---

## 💰 成本估算

| 计划数量 | Apify费用 | InVideo费用 | 总费用 | 咨询费用 |
|---|---|---|---|---|
| 1份计划 + 视频 | 约0.50美元 | 约3美元 | 约3.50美元 | 1,500美元至10,000美元 |
| 5份计划 | 约2.50美元 | 约15美元 | 约17.50美元 | 7,500美元至50,000美元 |
| 20份计划 | 约10美元 | 约60美元 | 约70美元 | 30,000美元至200,000美元 |

> 💡 **在[Apify](https://www.apify.com?fpr=dx06p)上可免费开始使用——包含5个信用额度**  
> 🎬 **使用[InVideo AI](https://invideo.sjv.io/TBB)制作演示文稿视频——提供免费试用计划**

---

## 🔗 谁能从这项技能中获利

| 使用者 | 使用方式 | 收入来源 |
|---|---|---|
| **商业计划咨询师** | 每份计划收费500美元至2,000美元 | 每月收入10,000美元至40,000美元 |
| **初创公司创始人** | 通过完整的商业计划书吸引投资 | 可筹集50万美元至500万美元 |
| **MBA学生/教练** | 向同学或客户出售商业计划书 | 每份计划收费200美元至500美元 |
| **加速器/孵化器** | 大规模地为初创企业提供商业计划书 | 作为高级服务附加选项 |
| **小型企业贷款顾问** | 为贷款申请提供银行认可的商业计划书 | 每份计划收费300美元至800美元 |

---

## 📊 为什么这项技能能超越现有的解决方案

| 功能 | 传统商业计划服务（100美元） | 咨询服务（5,000美元） | **本技能** |
|---|---|---|---|
| 实时市场研究 | 无 | 有 | 有 |
| 真实竞争对手分析 | 无 | 有 | 有 |
| 人工智能撰写的文案 | 无 | 有 | 有 |
| 三情景财务预测 | 无 | 有 | 有 |
| 包含演示文稿视频 | 无 | 无 | 有 |
| 项目完成时间 | 3小时 | 2周 | 10分钟 |
| 成本 | 100美元 | 5,000美元 | 约3.50美元 |

---

## 🚀 三步设置流程

**步骤1 — 获取[Apify](https://www.apify.com?fpr=dx06p)的API令牌**  
前往：**设置 → 集成 → API令牌**

**步骤2 — 注册[InVideo AI](https://invideo.sjv.io/TBB)账户**  
前往：**设置 → API → 复制API密钥**

**步骤3 — 描述您的商业想法并开始操作**  
提供商业想法、所在行业及融资目标，10分钟内即可完成完整的商业计划书和演示文稿视频。

---

## ⚡ 为投资者准备的商业计划的实用建议

- **投资者首先会阅读高层摘要**——如果60秒内不能吸引他们的兴趣，其他内容就无关紧要了。
- **切勿虚构市场数据**——本技能会抓取真实数据，投资者会进行核实。
- **LTV/CAC比率至少要达到3倍**——低于这个比例，没有投资者会感兴趣。
- **清晰展示达到盈亏平衡点的路径**——明确指出“第18个月实现盈利”比“未来会盈利”更有说服力。
- **在邮件推广中使用演示文稿视频**——视频引言的回复率是文本的3倍。

---

## 🏷️ 相关标签

`商业计划` `初创企业` `投资者` `演示文稿` `融资` `Apify` `InVideo` `市场研究` `财务预测` `创业` `种子轮融资` `加速器`

---

*由[Apify](https://www.apify.com?fpr=dx06p) + [InVideo AI](https://invideo.sjv.io/TBB) + Claude AI提供技术支持*