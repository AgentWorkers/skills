---
name: chairman-daily-brief
description: 专为上市公司董事长提供的专属晨间和晚间简报服务。每日从高管决策的角度提供简报，内容包括股价走势、行业政策动态、竞争对手分析、资本市场情绪以及监管公告提醒。晨间简报重点关注市场开盘前的市场展望和风险预警；晚间简报则侧重于市场收盘后的分析及次日策略规划。数据来源于多个QVeris信息源。
  Exclusive morning and evening briefing skill for listed company chairmen. 
  Provides daily briefings from an executive decision-making perspective,
  covering stock price movements, industry policy updates, competitor intelligence,
  capital market sentiment, and regulatory announcement alerts. 
  Morning briefings focus on pre-market outlook and risk warnings;
  evening briefings emphasize post-market review and next-day strategies.
  Data aggregated from multiple QVeris sources.
env:
  - QVERIS_API_KEY
requirements:
  env_vars:
    - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
runtime:
  language: nodejs
  node: ">=18"
install:
  mechanism: local-skill-execution
  external_installer: false
  package_manager_required: false
persistence:
  writes_within_skill_dir:
    - config/companies.json
    - config/watchlist.json
    - .evolution/tool-evolution.json
  writes_outside_skill_dir: false
security:
  full_content_file_url:
    enabled: true
    allowed_hosts:
      - qveris.ai
    protocol: https
network:
  outbound_hosts:
    - qveris.ai
metadata:
  openclaw:
    requires:
      env: ["QVERIS_API_KEY"]
    primaryEnv: "QVERIS_API_KEY"
    homepage: https://qveris.ai
auto_invoke: true
source: https://qveris.ai
examples:
  - "Generate morning report: focus on 600519.SS Moutai"
  - "Chairman evening report: generate closing briefing for 0700.HK Tencent"
  - "Morning brief: BYD and new energy vehicle industry"
  - "Generate morning report, focus on competitor CATL"
  - "Evening report: summarize today's dynamics of three listed companies I follow"
---
# 董事长每日简报

这是一个专为上市公司董事长设计的每日市场简报系统，从战略决策的角度提供高管级别的市场情报。

## 核心价值主张

与普通的投资者市场监控工具不同，本系统是从**董事长的决策视角**出发的：

- **股票走势 → 影响分析**：不仅关注股价的涨跌，还分析其对融资、并购和股东关系的影响；
- **行业政策 → 战略机遇**：实时捕捉监管变化带来的商业机会或风险；
- **竞争对手 → 对标分析**：评估主要竞争对手的动向对公司的影响；
- **市场情绪 → 资本策略**：根据投资者情绪为公司的资本运作提供时机建议；
- **公告提醒 → 合规警告**：及时提醒监管公告和重大事件。

## 早晨简报 vs 傍晚简报

### 早晨简报 — 上午7:00-9:00（盘前）

**目标**：在开盘前为董事长提供全面的市场信息，帮助其做好当天的准备

**内容模块**：
1. **隔夜全球市场**：美国股市、港股和A50期货对当日开盘的影响；
2. **宏观政策速递**：隔夜发布的行业政策和监管动态；
3. **公司盘前展望**：盘前的价格预期、关键价位、潜在的波动因素；
4. **行业动态**：行业内其他公司的重大进展及行业指数表现；
5. **竞争情报**：主要竞争对手的最新动态及应对建议；
6. **风险提示**：需要关注的风险点；
7. **今日重点**：会议安排、公告提醒、投资者活动信息。

### 傍晚简报 — 下午3:30-6:00（盘后）

**目标**：回顾当天的市场表现，并规划明天的战略

**内容模块**：
1. **市场收盘总结**：市场趋势、行业表现、公司股价表现；
2. **交易分析**：交易量、资金流动情况（如适用）；
3. **今日公告**：公司及竞争对手的重要公告摘要；
4. **媒体监测**：媒体报道、分析师观点、社交媒体情绪；
5. **机构活动**：研究报告评级变化、目标价调整、大宗交易情况；
6. **政策解读**：今日发布的政策对公司的影响分析；
7. **明日战略建议**：根据当天的市场情况制定应对策略。

## 数据来源

通过QVeris聚合的多源数据：

- **市场数据**：THS iFinD、Alpha Vantage、Yahoo Finance；
- **财经新闻**：Caidazi News、THS Finance、East Money；
- **研究报告**：Caidazi Reports、分析师评级；
- **政策公告**：交易所公告、中国证监会发布的信息、行业协会通知；
- **社交媒体**：X/Twitter上的舆论动态、Xueqiu论坛的讨论热度；
- **宏观数据**：经济数据、行业统计数据。

## 使用方式

### 生成早晨报告

```bash
# Single company morning report
node scripts/chairman_daily.mjs morning --symbol 600519.SS --company "Kweichow Moutai"

# Multi-company morning report (portfolio view)
node scripts/chairman_daily.mjs morning --watchlist holdings

# With industry focus
node scripts/chairman_daily.mjs morning --symbol 002594.SZ --industry "New Energy Vehicles"
```

### 生成傍晚报告

```bash
# Single company evening report
node scripts/chairman_daily.mjs evening --symbol 0700.HK --company "Tencent Holdings"

# Full review (with competitor analysis)
node scripts/chairman_daily.mjs evening --symbol 000858.SZ --competitors 000568.SZ,000596.SZ

# Summary mode (key information only)
node scripts/chairman_daily.mjs evening --symbol AAPL --format summary
```

### 管理观察列表

```bash
# Add company to watchlist
node scripts/chairman_daily.mjs watch --action add --symbol 600519.SS --company "Kweichow Moutai" --role self

# Add competitor
node scripts/chairman_daily.mjs watch --action add --symbol 002594.SZ --company "BYD" --role competitor --peer-group "New Energy Vehicles"

# View watchlist
node scripts/chairman_daily.mjs watch --action list

# Remove from watchlist
node scripts/chairman_daily.mjs watch --action remove --symbol 600519.SS
```

### OpenClaw定时任务设置

```bash
# Morning briefing schedule (weekdays 8:00 AM)
openclaw cron add \
  --name "Chairman Morning Brief" \
  --cron "0 8 * * 1-5" \
  --tz Asia/Shanghai \
  --session isolated \
  --message "Run chairman-daily-brief to generate morning report: node scripts/chairman_daily.mjs morning --watchlist holdings" \
  --channel feishu \
  --to <chat-id>

# Evening briefing schedule (weekdays 3:35 PM)
openclaw cron add \
  --name "Chairman Evening Brief" \
  --cron "35 15 * * 1-5" \
  --tz Asia/Shanghai \
  --session isolated \
  --message "Run chairman-daily-brief to generate evening report: node scripts/chairman_daily.mjs evening --watchlist holdings" \
  --channel feishu \
  --to <chat-id>
```

## 输出格式

### 早晨报告示例

```markdown
# 📊 Chairman Morning Brief — Kweichow Moutai (600519.SH)
📅 March 4, 2026 Tuesday 08:00

---

## 🌍 Overnight Global Markets
| Market | Close | Change | A-Share Impact |
|--------|-------|--------|----------------|
| Dow Jones | 43,850 | +0.5% | Positive |
| NASDAQ | 18,920 | +1.2% | Positive |
| Hang Seng | 23,450 | -0.3% | Slightly Negative |
| A50 Futures | 13,280 | +0.4% | Positive Opening Expected |

**Commentary**: US tech stocks rebounded strongly, boosting sentiment for A-share growth stocks. A50 futures rose slightly, indicating a stable opening for Moutai today.

---

## 📰 Macro Policy Express
🔔 **New Baijiu Industry Regulations** — State Administration for Market Regulation released draft "Baijiu Labeling and Identification Management Measures", imposing stricter requirements on marketing communications for high-end baijiu.
- **Impact Assessment**: Neutral to slightly negative, may affect marketing investments in the short term
- **Response Recommendation**: Review advertising compliance in advance, prepare investor communication talking points

---

## 📈 Company Pre-Market Outlook
| Indicator | Value | Expectation |
|-----------|-------|-------------|
| Previous Close | 1,580 CNY | - |
| Pre-Market Sentiment | Neutral | Slightly higher opening expected |
| Key Resistance | 1,600 CNY | Breakthrough requires volume |
| Key Support | 1,550 CNY | Strong support |

**Today's Focus Points**:
- Any institutional research report releases
- Northbound capital flow
- Dealer channel sales data rumors

---

## 🏭 Industry Radar
| Company | Development | Impact |
|---------|-------------|--------|
| Wuliangye | Released annual report preview, net profit +12% | Industry prosperity confirmed |
| Luzhou Laojiao | Announced 5% price increase | Industry pricing power solidified |

---

## 🎯 Competitive Intelligence
**Wuliangye (000858.SZ)** — Annual report exceeded expectations
- **Key Points**: Q4 revenue accelerated, high-end product mix improved
- **Impact on Moutai**: Intensified industry competition, need to monitor own market share
- **Recommendation**: Accelerate direct sales channel development, improve consumer reach efficiency

---

## ⚠️ Risk Alerts
1. **Policy Risk**: Baijiu industry regulations tightening, monitor subsequent detailed rules
2. **Valuation Risk**: Current PE 28x, above historical average, requires continued earnings growth support
3. **Foreign Outflow**: Northbound capital net selling for 3 consecutive days, monitor sustainability

---

## 📅 Today's Focus
- 09:30 National Bureau of Statistics releases February CPI data
- 10:00 Company IR quarterly communication meeting
- 14:00 Industry association symposium (Chairman attending)

---
*Data Sources: QVeris | THS iFinD, Caidazi, THS Finance*
```

### 傍晚报告示例

```markdown
# 🌙 Chairman Evening Report — Tencent Holdings (0700.HK)
📅 March 4, 2026 Tuesday 18:00

---

## 📊 Market Close Overview
| Indicator | Value | Change |
|-----------|-------|--------|
| Close Price | 485.00 HKD | +2.5% |
| Volume | 12.5M shares | +15% volume |
| Turnover | 6.06B HKD | - |
| Market Cap | 4.62T HKD | - |

**Market Comparison**: Hang Seng +0.8%, Tencent outperformed by 1.7 percentage points

---

## 💰 Trading Analysis
- **Capital Flow**: Northbound net buy 850M HKD
- **Main Force**: Large order net inflow 520M HKD
- **Dragon Tiger List**: Not listed

---

## 📢 Today's Announcements
**Company Announcements**:
- No major announcements

**Industry Announcements**:
- NetEase released Q4 earnings, gaming business exceeded expectations
- Regulator released new batch of game license approvals

---

## 📰 Media Monitoring
**Media Coverage**:
- Bloomberg: Tencent accelerates AI business layout, competing with OpenAI
- Caixin: WeChat Video Channel commercialization accelerates, ad revenue expectations raised

**Analyst Views**:
- Goldman Sachs: Maintains "Buy" rating, target price 520 HKD (+7%)
- Morgan Stanley: Upgrades to "Overweight", optimistic on cloud business turnaround

**Social Media Sentiment**: Positive (72% positive, 18% neutral, 10% negative)

---

## 🏦 Institutional Activity
| Institution | Rating Change | Target Price | Commentary |
|-------------|---------------|--------------|------------|
| Goldman Sachs | Maintain Buy | 520 HKD | AI business catalyst |
| Morgan Stanley | Upgrade to Overweight | 510 HKD | Cloud business turnaround |
| UBS | Maintain Neutral | 480 HKD | Fair valuation |

**Block Trades**: No block trades today

---

## 📋 Policy Interpretation
**Game License Approval Normalization**
- **Policy Content**: New batch of game licenses released today, Tencent approved for 2 titles
- **Impact Analysis**: Industry policy environment continues to improve, positive for gaming business growth
- **Strategic Significance**: Paves the way for subsequent new game launches

---

## 🎯 Tomorrow's Strategy Recommendations
**Based on today's market, recommend focusing on**:

1. **Investor Communication**: Utilize today's stock price rise window to communicate with institutional investors at appropriate times
2. **Buyback Pace**: If stock price pulls back below 480, consider accelerating buyback pace
3. **M&A Timing**: Positive market sentiment, can monitor potential M&A targets
4. **Risk Hedging**: Recommend moderate derivatives allocation to hedge short-term volatility

**Key Level Monitoring**:
- Break 490 → Opens upside to 520
- Fall below 475 → Triggers technical adjustment

---
*Data Sources: QVeris | THS iFinD, Caidazi, X Sentiment*
```

## 工具链路由

本系统通过`references/tool-chains.json`文件定义数据获取的优先级和路由规则：

```json
{
  "morning_brief": {
    "market_overview": ["ths_ifind.global_market", "alpha_vantage.market_status"],
    "policy_news": ["caidazi.news.query", "caidazi.report.query"],
    "company_quote": ["ths_ifind.real_time_quotation"],
    "industry_data": ["ths_ifind.industry_index", "caidazi.sector_analysis"],
    "sentiment": ["qveris_social.x_domain_hot_topics"]
  },
  "evening_brief": {
    "company_quote": ["ths_ifind.real_time_quotation", "ths_ifind.history_quotation"],
    "announcements": ["caidazi.news.query", "exchange_announcements"],
    "research": ["caidazi.report.query", "alpha_news_sentiment"],
    "fund_flow": ["ths_ifind.capital_flow", "ths_ifind.dragon_tiger"]
  }
}
```

## 安全与隐私

- 仅使用`QVERIS_API_KEY`，不存储其他凭证；
- 仅调用`qveris.ai` API；
- 数据本地存储仅限于技能目录内的配置文件；
- 研究报告仅供参考，不构成投资建议。

## 更新记录

- v1.0.0：初始版本，支持基本的早晨/傍晚简报功能；
- v1.1.0：新增竞争对手分析模块；
- v1.2.0：新增政策解读和风险提示模块；
- v1.3.0：完成全部内容的英文本地化。