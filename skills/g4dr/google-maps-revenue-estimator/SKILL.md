# 📍 谷歌地图收入估算器 — 在联系任何本地企业之前，准确了解其盈利情况

---

## 📋 ClawHub 信息

**slug:** `google-maps-revenue-estimator`

**显示名称:** **谷歌地图收入估算器 — 在联系任何本地企业之前，准确了解其盈利情况**

**更新日志:** `v1.0.0 — 从谷歌地图中抓取各类企业和位置的资料，根据评论数量、评分、客流量信号及行业基准估算每家企业的月收入，根据企业规模和增长潜力对其进行评分，并通过 InVideo AI 生成基于收入的营销素材及本地市场机会视频。由 Apify、InVideo AI 和 Claude AI 提供支持。`

**标签:** **谷歌地图** **本地企业** **收入估算** **B2B 销售** **Apify** **InVideo** **潜在客户生成** **销售智能** **代理** **主动联系** **小型企业** **客流量**

---

**类别:** 销售智能 / 本地潜在客户生成  
**技术支持:** [Apify](https://www.apify.com?fpr=dx06p) + [InVideo AI](https://invideo.sjv.io/TBB) + Claude AI

> 输入任何企业类别和城市，即可获取地图上每家企业的**预估月收入**（按收入从高到低排序）。在打电话之前，先了解对方的预算情况，从而有针对性地推销产品，更快地达成交易。

---

## 💥 为什么这个技能会在 ClawHub 上大受欢迎

“谷歌地图 B2B 金矿”已经是 ClawHub 上浏览量最高的技能之一（449 次浏览），而这个技能更是将其提升到了一个全新的高度。

掌握企业名单非常有用。在拨打电话之前，就能知道哪些企业每月盈利 8 万美元，哪些仅盈利 8,000 美元，这简直是一种强大的能力。

每个代理、自由职业者、SaaS 代表和服务型企业都曾浪费大量时间去联系那些没有预算的企业。这个技能能让你在花费一分钱进行营销之前，就准确判断出哪些企业有资金实力以及具体金额。

**目标受众:** 网页设计机构、SEO 机构、营销顾问、支付处理服务商、POS 经销商、会计师、保险经纪人、软件销售代表——任何向本地企业销售产品或服务的人。

**自动化功能包括：**
- 通过谷歌地图抓取**所有企业**的详细信息
- 根据评论数量、评分和客流量信号估算每家企业的**月收入**
- 按**预估收入**对企业进行排名，优先联系高收入企业
- 识别**增长信号**（企业是在扩张还是萎缩）
- 生成**基于收入的营销素材**（例如：“您的企业每月收入约为 X 美元，以下是增长方案”）
- 通过 [InVideo AI](https://invideo.sjv.io/TBB) 制作**本地市场机会视频**

---

## 🛠️ 使用的工具

| 工具 | 功能 |
|---|---|
| [Apify](https://www.apify.com?fpr=dx06p) — 谷歌地图数据抓取工具 | 获取各类企业和城市的所有信息（评论、评分、营业时间、网站内容） |
| [Apify](https://www.apify.com?fpr=dx06p) — 谷歌搜索数据抓取工具 | 获取企业的 SEO 状况、广告支出情况、品牌提及次数 |
| [Apify](https://www.apify.com?fpr=dx06p) — 网站内容爬取工具 | 获取价格页面、团队规模、服务范围等收入相关数据 |
| [Apify](https://www.apify.com?fpr=dx06p) — Instagram 数据抓取工具 | 获取企业的社交媒体关注者数量、发布频率及推广内容 |
| [Apify](https://www.apify.com?fpr=dx06p) — Facebook 数据抓取工具 | 判断企业是否投放了付费广告（预算信号） |
| [InVideo AI](https://invideo.sjv.io/TBB) | 生成基于收入的本地市场机会视频 |
| Claude AI | 收入建模、增长潜力评估、个性化营销策略制定 |

---

## ⚙️ 收入估算模型

该技能使用了一个基于行业基准数据训练的**七信号收入估算模型**：

```
SIGNAL 1 — Review Velocity
  └─ Reviews per month = proxy for customer volume
  └─ e.g. Restaurant: 20 reviews/month × avg ticket $35 × 30 = ~$21,000/month

SIGNAL 2 — Rating Quality
  └─ 4.5★+ with high volume = premium pricing power
  └─ 3.8★ with low volume = budget segment

SIGNAL 3 — Google Maps Category & Hours
  └─ Category benchmarks: restaurant vs law firm vs gym — different revenue profiles
  └─ Hours open × estimated hourly throughput = volume proxy

SIGNAL 4 — Website Presence & Quality
  └─ Premium website + booking system = established business with real revenue
  └─ No website or basic template = micro-business

SIGNAL 5 — Social Media Activity
  └─ Active Instagram with 2K+ followers + regular posts = marketing budget exists
  └─ Running Facebook ads = confirmed marketing spend

SIGNAL 6 — Team Size Signals
  └─ "Meet the team" page with 10+ staff = $500K+ annual revenue likely
  └─ Solo operator signals = micro-business tier

SIGNAL 7 — Location & Premises
  └─ Central location in premium area = higher revenue tier
  └─ Multiple locations = confirmed scale

COMBINED → Revenue tier estimate with confidence score
```

---

## ⚙️ 完整工作流程

```
INPUT: Business category + city + your service offer
        ↓
STEP 1 — Full Map Scrape
  └─ Every business in category within radius
  └─ Extract: name, address, phone, website, rating, review count, hours
        ↓
STEP 2 — Revenue Signal Collection
  └─ Review velocity (reviews per month)
  └─ Website quality score
  └─ Social media presence + ad signals
  └─ Team size indicators
        ↓
STEP 3 — Revenue Estimation
  └─ Apply 7-signal model per business
  └─ Output: estimated monthly revenue range
  └─ Confidence score per estimate
        ↓
STEP 4 — Growth Signal Detection
  └─ Review count growing month-over-month? (expanding)
  └─ Recently started running ads? (investing in growth)
  └─ New location opened? (scaling)
  └─ Rating improving? (fixing problems = reinvesting)
        ↓
STEP 5 — Prospect Scoring
  └─ Revenue tier: Whale ($100K+/mo) / Solid ($20-100K) / Small ($5-20K) / Skip (<$5K)
  └─ Growth signal: Scaling / Stable / Declining
  └─ Budget likelihood: High / Medium / Low
        ↓
STEP 6 — Claude AI Writes Revenue-Led Outreach
  └─ Opens with their estimated revenue figure
  └─ Shows % improvement your service delivers
  └─ Positions ROI in their own revenue terms
        ↓
STEP 7 — InVideo AI Produces Market Video
  └─ "The revenue landscape of [category] in [city]"
  └─ Key stats: average revenue, who's growing, who's not
  └─ Perfect opener for cold email or LinkedIn outreach
        ↓
OUTPUT: Ranked business list by revenue + outreach per business + market video
```

---

## 📥 输入内容

```json
{
  "targeting": {
    "category": "dental practices",
    "city": "Chicago, Illinois",
    "radius_km": 20,
    "exclude_chains": true,
    "min_reviews": 15
  },
  "your_service": {
    "type": "digital marketing agency",
    "offer": "Google Ads + SEO package for dental practices",
    "result": "Average client adds 40 new patients per month",
    "price": "$1,500/month"
  },
  "targeting_filters": {
    "revenue_tiers": ["Whale", "Solid"],
    "growth_signals": ["Scaling", "Stable"],
    "skip_if": ["running google ads already", "chain/franchise"]
  },
  "max_results": 80,
  "production": {
    "invideo_api_key": "YOUR_INVIDEO_API_KEY"
  },
  "apify_token": "YOUR_APIFY_TOKEN"
}
```

---

## 📤 输出示例

```json
{
  "market_overview": {
    "city": "Chicago, IL",
    "category": "Dental Practices",
    "businesses_scanned": 312,
    "revenue_distribution": {
      "whales_100k_plus": 18,
      "solid_20k_100k": 94,
      "small_5k_20k": 143,
      "skip_under_5k": 57
    },
    "total_estimated_monthly_revenue_in_market": "$42.8M",
    "avg_monthly_revenue_per_practice": "$137,200",
    "top_growth_signal": "34 practices started running Google Ads in last 90 days — market is getting competitive"
  },
  "top_prospects": [
    {
      "rank": 1,
      "revenue_tier": "🐋 WHALE",
      "prospect_score": 94,
      "business": {
        "name": "Lakefront Dental Group",
        "address": "840 N Michigan Ave, Chicago IL",
        "phone": "(312) 440-8820",
        "website": "lakefrontdental.com",
        "google_rating": 4.8,
        "review_count": 847,
        "reviews_last_30d": 23
      },
      "revenue_estimate": {
        "monthly_revenue_range": "$180,000 – $240,000/month",
        "confidence": "High (82%)",
        "model_signals": {
          "review_velocity": "23 reviews/month × avg dental ticket $780 = high volume practice",
          "website_quality": "Premium custom site with online booking — significant tech investment",
          "team_size": "11 dentists listed on team page",
          "location": "Prime Michigan Ave location — premium rent = premium revenue",
          "ads_detected": "Not currently running Google Ads — opportunity"
        }
      },
      "growth_signals": [
        "Review count up 34% in last 6 months",
        "Added 2 new dentists to team page recently",
        "Recently launched Invisalign service — expanding service range"
      ],
      "budget_likelihood": "Very High — $200K/month practice can easily justify $1,500/month marketing",
      "decision_maker": {
        "likely_title": "Practice Owner / Office Manager",
        "best_approach": "Call during 9–10am Tuesday–Thursday",
        "phone": "(312) 440-8820"
      },
      "outreach": {
        "email_subject": "Lakefront Dental — 40 new patients/month from Google Ads (you're not running any yet)",
        "email_body": "Hi Lakefront Dental team,\n\nI ran a quick analysis of dental practices on Michigan Ave and noticed something: Lakefront Dental is one of the highest-rated practices in Chicago (4.8★ from 847 reviews) but you're not running any Google Ads.\n\nYour competitors 3 blocks away are spending $2,000–$4,000/month on ads to capture patients who search 'dentist Chicago' — and those patients never find you organically.\n\nWe work exclusively with dental practices. Our average client adds 40 new patients per month from Google Ads. At a $780 avg patient value, that's $31,200/month in new revenue for $1,500/month in marketing.\n\nWould a 15-minute call this week make sense?\n\n[Your name] | [Agency]",
        "cold_call_opener": "Hi, I'm calling for the practice owner — I noticed Lakefront Dental has 847 Google reviews and a 4.8 rating, but you're not running any Google Ads. I work with dental practices specifically and I wanted to share what that's likely costing you in missed patients each month."
      }
    },
    {
      "rank": 2,
      "revenue_tier": "🐋 WHALE",
      "prospect_score": 89,
      "business": {
        "name": "Chicago Smile Design",
        "estimated_monthly_revenue": "$140,000 – $190,000/month",
        "key_signal": "Running Facebook ads but no Google Ads — channel gap opportunity"
      },
      "outreach": {
        "email_subject": "You're running Facebook ads but missing 3x the patients on Google",
        "email_body": "Hi Chicago Smile Design — I can see you're already investing in Facebook ads (smart). But Google Search captures patients at the exact moment they're searching for a dentist — 3x higher intent than social. You're currently invisible there. We fix that. 40 new patients/month average. Worth a call?"
      }
    }
  ],
  "market_video": {
    "script": "312 dental practices in Chicago. The average practice makes $137,000 a month. 18 of them make over $180,000. And only 34 of those 312 are running Google Ads right now. That means 278 high-revenue dental practices in this city are invisible to patients searching online. I analyzed every single one. Here are the 18 with the biggest budget and the biggest gap.",
    "duration": "60s",
    "status": "produced"
  }
}
```

---

## 🧠 Claude AI 使用提示

```
You are a world-class B2B sales intelligence analyst specializing in local business revenue modeling.

SCRAPED BUSINESS DATA: {{google_maps_website_social_data}}
AD SIGNAL DATA: {{facebook_google_ads_detection}}
INDUSTRY BENCHMARKS: {{category_revenue_benchmarks}}

YOUR SERVICE:
- Type: {{service_type}}
- Offer: {{offer}}
- Result: {{result}}
- Price: ${{price}}/month

TARGET:
- Category: {{category}}
- City: {{city}}

FOR EACH BUSINESS:
1. Revenue estimate using 7-signal model:
   - Review velocity × category avg ticket
   - Website quality tier
   - Team size signals
   - Location premium
   - Ad spend detection
   - Social following
   - Hours + category benchmark
   Output: monthly revenue range + confidence %

2. Revenue tier:
   - 🐋 Whale: $100K+/month
   - ✅ Solid: $20K–$100K/month
   - 🟡 Small: $5K–$20K/month
   - ⬇️ Skip: under $5K/month

3. Growth signals (specific, not generic):
   - Mention exact signals detected

4. Budget likelihood for YOUR price point:
   - Calculate as % of estimated revenue
   - Under 2% of revenue = easy yes
   - 2–5% = normal sales cycle
   - Over 5% = harder sell

5. Revenue-led outreach:
   - Email: open with their revenue estimate OR the gap it creates
   - Cold call opener: reference a specific signal
   - Subject line must include a number

6. 60-second market overview video script:
   - Lead with the total market revenue figure
   - Reveal the opportunity gap
   - End with the prospect count

GOLDEN RULE: Outreach must reference THEIR specific revenue signal.
"You have 847 reviews" beats "I noticed you have good reviews."

OUTPUT: Valid JSON only. No markdown. No preamble.
```

---

## 💰 成本估算

| 扫描数量 | Apify 成本 | InVideo 成本 | 总成本 | 提供的价值 |
|---|---|---|---|---|
| 100 家企业 | 约 0.50 美元 | 约 3 美元 | 约 3.50 美元 | 提供排名后的收入地图 |
| 500 家企业 | 约 2 美元 | 约 3 美元 | 约 5 美元 | 提供整个城市的收入分析 |
| 5 个城市（针对代理机构） | 约 10 美元 | 约 15 美元 | 提供整个月的销售线索 |
| 每周监控 | 每周约 2 美元 | 每月约 3 美元 | 提供持续更新的潜在客户信息 |

> 💡 **在 [Apify](https://www.apify.com?fpr=dx06p) 上可免费试用（包含 5 个信用额度）**  
> **使用 [InVideo AI](https://invideo.sjv.io/TBB) 制作市场视频**  

---

## 🔗 收入机会

| 用户 | 使用方式 | 收入提升效果 |
|---|---|---|
| **营销机构** | 仅联系月收入超过 10 万美元的企业 | 销售成交率提高 3 倍 |
| **SaaS 销售代表** | 首先瞄准高收入企业，忽略小企业 | 每笔交易的收入提升 5 倍 |
| **自由职业者** | 在报价前了解客户预算 | 再也不会低估客户预算 |
| **支付处理服务商** | 找到值得合作的优质商户 | 提高交易金额 |
| **企业经纪人** | 在接触前评估潜在客户 | 提供有数据支持的报价建议 |

---

## 📊 为什么这个工具比普通的地图抓取工具更优秀

| 功能 | 普通地图抓取工具 | Hunter.io | **谷歌地图收入估算器** |
|---|---|---|---|
| 联系信息提取 | ✅ | ✅ | ✅ |
| 收入估算 | ❌ | ❌ | ✅ |
| 预算可能性评分 | ❌ | ❌ | ✅ |
| 增长信号检测 | ❌ | ❌ | ✅ |
| 基于收入的营销策略 | ❌ | ❌ | ✅ |
| 市场概览视频 | ❌ | ❌ | ✅ |
| 成本 | 每月 49 美元 | 每月 49 美元 | 每次生成视频约 5 美元 |

---

## 🚀 三步设置流程

**步骤 1 — 获取 [Apify](https://www.apify.com?fpr=dx06p) 的 API 令牌**  
前往：**设置 → 集成 → API 令牌**

**步骤 2 — 注册 [InVideo AI](https://invideo.sjv.io/TBB) 账户**  
前往：**设置 → API → 复制 API 密钥**

**步骤 3 — 输入企业类别和城市并运行脚本**  
输入企业类型和位置，几分钟内即可获得完整的收入地图。

---

## ⚡ 专业提示

- **始终优先联系高收入企业** — 一家每月收入 10 万美元的企业价值相当于 20 家小企业的收入总和 |
- “您没有在谷歌上投放广告”是联系本地企业的最佳开场白 |
- **评论数量是评估收入的最佳指标** — 每月 20 条评论意味着每月有 20 笔以上的实际交易 |
- **市场视频能提升可信度** — “我分析了 [城市] 中的每个 [行业]，证明您是专家” |
- **预算可能性低于收入的 2% 的企业最容易成交** — 在这种情况下，预算差异对他们来说可以忽略不计 |

---

*由 [Apify](https://www.apify.com?fpr=dx06p) + [InVideo AI](https://invideo.sjv.io/TBB) + Claude AI 提供支持*