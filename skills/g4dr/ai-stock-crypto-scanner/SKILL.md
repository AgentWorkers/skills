# 💹 AI股票与加密货币市场扫描器 — 在众人之前发现投资机会

**技能名称：** AI股票-加密货币扫描器  
**类别：** 金融 / 交易智能  
**技术支持：** [Apify](https://www.apify.com?fpr=dx06p) + [3Commas](https://3commas.io/?utm_source=referral&utm_medium=cabinet&c=SKL) + [InVideo AI](https://invideo.sjv.io/TBB) + Claude AI  

> 输入您的关注列表或市场板块，即可获得一份 **全面的市场分析报告**：包括价格走势分析、从Reddit和Twitter抓取的情绪数据、内部消息的检测结果、AI生成的投资机会评分，以及通过3Commas自动部署的交易机器人。所有这些功能均可一次性完成。  

---

## 💥 为何该技能在ClawHub上会大受欢迎  

每位散户投资者、加密货币爱好者及金融从业者都在不断寻找下一个投资机会——在他们错过最佳时机之前。专业对冲基金会在Bloomberg终端和情绪分析工具上花费数百万美元。而这项技能仅需不到2美元，就能提供同样的市场分析服务。  

**目标用户：** 日内交易者、波段交易者、加密货币投资者、去中心化金融（DeFi）爱好者、金融顾问、金融科技初创企业以及交易教育工作者。全球范围内，这类用户数量达数亿人。  

**自动化功能包括：**  
- 📊 实时抓取股票和加密货币的价格变动信号  
- 🐦 监控Reddit（WallStreetBets、r/CryptoCurrency）及Twitter/X上的情绪波动  
- 📰 检测新闻事件（如公司财报、合作公告、监管政策变化）  
- 🐋 识别大额资金转移（即“鲸鱼交易”）及异常交易量  
- 🤖 根据AI信号通过[3Commas](https://3commas.io/?utm_source=referral&utm_medium=cabinet&c=SKL)自动部署交易机器人  
- 🎬 通过[InVideo AI](https://invideo.sjv.io/TBB)制作每日市场简报视频  
- 📋 提供带有入场/出场建议的投资机会列表  

> ⚠️ **免责声明：** 本技能提供的市场分析仅用于信息参考，不构成任何投资建议。交易前请务必自行进行充分研究。  

---

## 🛠️ 使用的工具  

| 工具 | 功能 |  
|---|---|
| [Apify](https://www.apify.com?fpr=dx06p) | 获取股票和加密货币的价格数据、成交量及市值变化 |
| [Apify](https://www.apify.com?fpr=dx06p) | 从Reddit（WallStreetBets、r/CryptoCurrency）抓取情绪数据 |
| [Apify](https://www.apify.com?fpr=dx06p) | 从Twitter/X抓取热门话题及影响者相关内容 |
| [Apify](https://www.apify.com?fpr=dx06p) | 获取财经新闻（如公司财报、合作公告等） |
| [Apify](https://www.apify.com?fpr=dx06p) | 从CoinGecko获取加密货币价格数据及交易量变化 |
| [3Commas](https://3commas.io/?utm_source=referral&utm_medium=cabinet&c=SKL) | 根据AI信号自动执行交易操作 |
| [InVideo AI](https://invideo.sjv.io/TBB) | 制作每日60秒市场简报视频 |
| Claude AI | 信号评分、投资机会排序、风险分析 |

---

## ⚙️ 完整工作流程  

```
INPUT: Watchlist (tickers/coins) + sector + risk profile + trading style
        ↓
STEP 1 — Price Action & Volume Analysis
  └─ % change (1h / 24h / 7d / 30d)
  └─ Volume spike detection (3x+ average = signal)
  └─ Support & resistance levels
  └─ RSI, MACD signals (overbought/oversold)
        ↓
STEP 2 — Sentiment Scan (Reddit + Twitter/X)
  └─ Mention volume surge (10x+ normal = crowd forming)
  └─ Sentiment score: bullish / neutral / bearish / panic
  └─ Key influencer mentions detected
  └─ Viral posts & threads about this asset
        ↓
STEP 3 — News Catalyst Detection
  └─ Earnings reports (beat / miss / upcoming)
  └─ Partnership announcements
  └─ Regulatory news (positive or negative)
  └─ Insider buying/selling signals
        ↓
STEP 4 — Whale & On-Chain Signals (Crypto)
  └─ Large wallet transfers detected
  └─ Exchange inflows/outflows
  └─ New whale accumulation patterns
        ↓
STEP 5 — AI Opportunity Scoring (0–100)
  └─ Combines: price momentum + sentiment + news + volume
  └─ Risk-adjusted score based on your profile
  └─ Label: 🔥 Strong Signal / ⚡ Watch / ❄️ Avoid
        ↓
STEP 6 — 3Commas Bot Deployment
  └─ Auto-configure DCA bot for top opportunities
  └─ Set entry, take profit & stop loss based on AI signals
  └─ Risk-capped per your profile settings
        ↓
STEP 7 — InVideo AI Produces Daily Briefing Video
  └─ 60-second "Markets Today" summary video
  └─ Top 3 opportunities + 1 risk to watch
  └─ Perfect for YouTube Shorts, TikTok, newsletter
        ↓
OUTPUT: Ranked opportunity report + bot configs + daily briefing video
```  

---

## 📥 输入内容  

```json
{
  "watchlist": {
    "stocks": ["NVDA", "TSLA", "PLTR", "SMCI"],
    "crypto": ["BTC", "ETH", "SOL", "PEPE"],
    "sectors": ["AI & semiconductors", "DeFi", "memecoins"]
  },
  "trader_profile": {
    "style": "swing trader",
    "risk_level": "medium",
    "capital_per_trade": 1000,
    "holding_period": "3-14 days",
    "exchanges": ["Binance", "Coinbase"]
  },
  "alerts": {
    "sentiment_surge_threshold": "5x normal mention volume",
    "volume_spike_threshold": "3x 30-day average",
    "price_change_alert": "5%+ in 4 hours"
  },
  "automation": {
    "threecommas_api_key": "YOUR_3COMMAS_API_KEY",
    "auto_deploy_bots": true,
    "max_concurrent_bots": 3,
    "invideo_api_key": "YOUR_INVIDEO_API_KEY"
  },
  "apify_token": "YOUR_APIFY_TOKEN"
}
```  

---

## 📤 输出示例  

```json
{
  "scan_summary": {
    "date": "2026-03-03",
    "assets_scanned": 8,
    "strong_signals": 2,
    "watch_list": 3,
    "avoid": 3,
    "market_sentiment": "⚡ Cautiously Bullish — crypto momentum building, stocks mixed"
  },
  "opportunities": [
    {
      "rank": 1,
      "asset": "SOL (Solana)",
      "type": "Crypto",
      "opportunity_score": 91,
      "signal_label": "🔥 Strong Signal",
      "price_data": {
        "current_price": "$148.20",
        "change_24h": "+8.4%",
        "change_7d": "+22.1%",
        "volume_spike": "4.2x 30-day average",
        "rsi_14": 62,
        "rsi_signal": "Bullish — not yet overbought"
      },
      "sentiment": {
        "reddit_mentions_24h": 4847,
        "vs_7day_avg": "+380%",
        "sentiment_score": "82% Bullish",
        "top_reddit_post": "r/CryptoCurrency: 'Solana ETF filing confirmed — this changes everything' (12K upvotes)",
        "twitter_mentions_24h": 28400,
        "key_influencer": "@CryptoKaleo mentioned SOL as his top pick for Q1"
      },
      "news_catalysts": [
        "🟢 Solana ETF filing submitted to SEC — first major catalyst in 6 months",
        "🟢 Visa partnership expansion announced — real-world adoption signal",
        "⚪ Minor network outage 48 hours ago — resolved, no lasting impact"
      ],
      "whale_signals": {
        "large_transfers": "3 wallets moved 50K+ SOL to cold storage in last 12 hours",
        "exchange_flow": "Net outflow from exchanges (-$42M) — accumulation signal",
        "verdict": "🐋 Whales accumulating — bullish"
      },
      "ai_analysis": "SOL is showing a rare confluence of 4 bullish signals simultaneously: volume spike, sentiment surge, positive news catalyst, and whale accumulation. The ETF news is the primary driver. Risk: if SEC rejects, expect 20-30% correction. Risk/reward favors entry at current levels for swing traders.",
      "suggested_trade": {
        "entry_zone": "$144–$150",
        "take_profit_1": "$168 (+13%)",
        "take_profit_2": "$195 (+31%)",
        "stop_loss": "$132 (-11%)",
        "risk_reward_ratio": "2.8:1",
        "position_size": "$1,000 (per your risk profile)"
      },
      "threecommas_bot": {
        "type": "DCA Bot",
        "status": "deployed",
        "config": {
          "base_order": "$400",
          "safety_orders": 3,
          "safety_order_size": "$200",
          "take_profit": "13%",
          "stop_loss": "11%",
          "start_condition": "Price drops to $144"
        }
      }
    },
    {
      "rank": 2,
      "asset": "NVDA (Nvidia)",
      "type": "Stock",
      "opportunity_score": 84,
      "signal_label": "🔥 Strong Signal",
      "price_data": {
        "current_price": "$892.40",
        "change_24h": "+3.2%",
        "volume_spike": "2.8x average"
      },
      "news_catalysts": [
        "🟢 Earnings report in 6 days — consensus expects 40% YoY growth",
        "🟢 New AI chip partnership with Microsoft announced"
      ],
      "ai_analysis": "Pre-earnings momentum with strong institutional buying. High conviction swing trade opportunity into earnings. Consider reducing position after earnings announcement regardless of outcome.",
      "suggested_trade": {
        "entry_zone": "$880–$900",
        "take_profit_1": "$950 (+6.5%)",
        "stop_loss": "$850 (-4.7%)",
        "risk_reward_ratio": "1.4:1"
      }
    }
  ],
  "risk_warnings": [
    {
      "asset": "PEPE",
      "signal": "❄️ Avoid",
      "reason": "Negative sentiment surge — 67% bearish mentions. Whale dumping detected. 3 influencers called exit.",
      "action": "Do not enter. If holding, consider reducing exposure."
    }
  ],
  "daily_briefing_video": {
    "script": "Markets today — March 3rd 2026. Two strong signals on our radar. Solana is up 8% on ETF filing news with whale accumulation confirming the move. Nvidia approaching earnings with institutional momentum. Our AI scanner scores both as high conviction opportunities. One to avoid: PEPE showing whale distribution signals. Full analysis in the report. Trade smart.",
    "duration": "60s",
    "status": "produced",
    "video_file": "outputs/market_briefing_march03.mp4"
  }
}
```  

---

## 🧠 Claude AI使用指南  

```
You are a world-class quantitative analyst and trading intelligence specialist.

PRICE & VOLUME DATA:
{{price_action_data}}

SENTIMENT DATA (Reddit + Twitter):
{{sentiment_data}}

NEWS CATALYSTS:
{{news_data}}

WHALE/ON-CHAIN DATA:
{{onchain_data}}

TRADER PROFILE:
- Style: {{trading_style}}
- Risk level: {{risk_level}}
- Capital per trade: ${{capital}}
- Holding period: {{holding_period}}

FOR EACH ASSET GENERATE:
1. Opportunity score (0–100) combining:
   - Price momentum (25%)
   - Volume signal (20%)
   - Sentiment score (25%)
   - News catalyst strength (20%)
   - Whale/institutional signal (10%)
2. Signal label: Strong Signal / Watch / Avoid
3. Plain-English AI analysis (3-4 sentences, no jargon)
4. Suggested trade: entry zone, 2 take profit levels, stop loss, R/R ratio
5. 3Commas bot config for top 2 signals only
6. 60-second daily briefing video script

RISK RULES:
- Never suggest more than 10% portfolio in single trade
- Flag any asset with negative news + falling volume as Avoid
- Always include stop loss — no exceptions

DISCLAIMER: Include in every response that this is for informational
purposes only and does not constitute financial advice.

OUTPUT: Valid JSON only. No markdown. No preamble.
```  

---

## 💰 成本估算  

| 扫描次数 | Apify费用 | InVideo费用 | 总费用 | 相当于专业工具的费用（每月） |
|---|---|---|---|---|
| 每日扫描1次 | 约0.40美元 | 约3美元 | 约3.40美元 | Bloomberg：每月2,000美元 |
| 每周扫描7次 | 约2.80美元 | 约21美元 | 约23.80美元 | 情绪分析工具：每月500美元 |
| 每月扫描30次 | 约12美元 | 约90美元 | 约102美元 | 每月节省2,400美元 |

> 💡 **立即在[Apify](https://www.apify.com?fpr=dx06p)免费试用** — 免费提供5个API信用额度  
> 🤖 **使用[3Commas](https://3commas.io/?utm_source=referral&utm_medium=cabinet&c=SKL)自动化交易** — 提供免费试用计划  
> 🎬 **使用[InVideo AI](https://invideo.sjv.io/TBB)制作每日简报** — 提供免费试用计划  

---

## 🔗 谁能从这项技能中获益最多？  

| 用户 | 使用方式 | 价值 |  
|---|---|---|
| **散户投资者** | 每日使用AI进行市场扫描后再进行交易 | 更好的入场时机 |
| **加密货币投资者** | 在价格波动前识别大额资金转移及情绪变化 | 提前获取投资机会 |
| **金融内容创作者** | 为YouTube/TikTok观众制作每日市场简报视频 | 通过交易内容盈利 |
| **交易教育者** | 向学生提供每周市场分析报告 | 为高级课程增加附加价值 |
| **金融科技初创企业** | 为市场分析产品提供技术支持 | 实现B2B SaaS收入 |
| **金融顾问** | 用AI辅助分析市场情绪 | 每周节省超过5小时的工作时间 |

---

## 📊 为何这项技能能替代每月2,000美元以上的专业工具？  

| 功能 | Bloomberg终端 | 情绪分析工具（每月500美元） | 本技能 |  
|---|---|---|---|
| 价格和成交量数据 | ✅ | ✅ | ✅ |
| Reddit情绪分析 | ❌ | ✅ | ✅ |
| Twitter/X情绪分析 | ❌ | ✅ | ✅ |
| AI投资机会评分 | ❌ | ❌ | ✅ |
| 自动交易机器人 | ❌ | ❌ | ✅ |
| 每日市场简报 | ❌ | ❌ | ✅ |
| 入场/出场建议 | ❌ | ❌ | ✅ |
| 每月费用 | 每月2,000美元以上 | 每月500美元 | 每月约102美元 |

---

## 🚀 三步设置流程  

**步骤1：** 获取[Apify](https://www.apify.com?fpr=dx06p)的API密钥  
前往：**设置 → 集成 → API密钥**  

**步骤2：** 连接[3Commas](https://3commas.io/?utm_source=referral&utm_medium=cabinet&c=SKL)  
创建免费账户 → 进入：**我的账户 → API → 生成密钥**  

**步骤3：** 注册[InVideo AI](https://invideo.sjv.io/TBB)账户  
前往：**设置 → API → 复制您的API密钥**  

---

## ⚡ 使用本技能的进阶交易技巧  

- **切勿仅凭情绪数据交易** — 始终等待价格确认后再入场  
- **成交量激增与情绪波动同时出现时，是最佳入场信号**  
- **将3Commas交易机器人设置在周日晚上** — 周一市场波动较快  
- **每日市场简报视频是TikTok上的最佳交易素材** — 每日发布，积累观众  
- **务必遵守止损规则** — 机器人会自动执行，切勿手动更改  

> ⚠️ **重要提示：** 过去的表现并不能保证未来的结果。本工具仅用于市场研究，切勿投资超出您的承受能力。  

---

## 🏷️ 相关标签  

`交易` `加密货币` `股票` `市场扫描器` `情绪分析` `Apify` `3Commas` `InVideo` `交易机器人` `比特币` `去中心化金融` `金融`  

---

*由[Apify](https://www.apify.com?fpr=dx06p) + [3Commas](https://3commas.io/?utm_source=referral&utm_medium=cabinet&c=SKL) + [InVideo AI](https://invideo.sjv.io/TBB) + Claude AI提供技术支持*