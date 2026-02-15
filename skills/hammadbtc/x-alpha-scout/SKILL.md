---
name: x-alpha-scout
description: 这是一个用于监控加密货币和NFT在X（Twitter）上的动态的alpha版本工具。适用场景如下：  
(1) 用户需要每日获取相关动态报告；  
(2) 需要分析特定代币/NFT项目在X上的用户情绪（即用户对项目的看法和讨论）。  
GitHub地址：github.com/hammad-btc/alpha-scout-skill
---

# X Alpha Scout

这是为您的代理设计的X/Twitter监控工具。它提供两项主要功能：每日报告和按需分析。

## 先决条件

**环境变量：**
```bash
export X_AUTH_TOKEN="your_twitter_auth_token"
export X_CT0="your_twitter_ct0_cookie"
```

**验证：**
```bash
bird whoami --auth-token "$X_AUTH_TOKEN" --ct0 "$X_CT0"
```

---

## 功能1：每日Alpha报告（自动在UTC 00:00生成）

**用户操作：** “运行每日Alpha报告” 或 “获取今天的报告”

**系统操作：**

```bash
# Scan for overnight alpha
bird search "(buying OR bought OR aping OR loading up) (ticker OR token OR \$)" -n 25
bird search "(minting OR mint OR free mint) NFT" -n 20
bird search "(just launched OR stealth launch) token" -n 15
bird search "(gem OR undervalued OR 100x) crypto" --min-likes 10 -n 15
```

**报告生成格式：**

```markdown
# 🦅 Alpha Report — Feb 10, 2026

### 1. Good Morning
[Simple greeting]

### 2. Crypto Market Update
- BTC: $[price] ([+/-]% 24h)
- ETH: $[price] ([+/-]% 24h)
- SOL: $[price] ([+/-]% 24h)
- Fear & Greed Index: [value] ([Extreme Fear/Fear/Neutral/Greed/Extreme Greed])

### 3. News of the Day
- [Major Web3 announcement](https://x.com/...) — Brief summary
- [Regulation/news affecting market](https://x.com/...) — Brief summary
- [Any market-moving world news](https://x.com/...) — Brief summary

### 4. Crypto Twitter (CT)
- Main narrative: [What's the hot topic today?]
- Key trends: [New meta, drama, or shifts]
- Notable accounts: [Who's driving conversation]

### 5. NFTs Market Update
**ETH Eco:** [2-3 sentence paragraph on top ETH ecosystem updates — NFTs, tokens, protocols. Skip if nothing significant.]

**Bitcoin Eco:** [2-3 sentence paragraph on top Bitcoin/Ordinals market. Skip if nothing significant.]

**Sol Eco:** [2-3 sentence paragraph on top Solana ecosystem — NFTs, DeFi, memes. Skip if nothing significant.]

**Notable Mints:**
- Minting Today: [@account1](https://x.com/account1) [@account2](https://x.com/account2) [@account3](https://x.com/account3) (only good, hyped drops — embed X profile links)
- Upcoming Mints: [@account4](https://x.com/account4) [@account5](https://x.com/account5) (worth keeping an eye on — embed X profile links)

If none worth mentioning, say "No major mints detected."

### 6. Alpha from Reputable Figures:
- Top calls: [What are reputable accounts buying/minting? Include @username]
- High-conviction signals: [Who's aping what with size/proof — include @username]
- WL opportunities: [Any good drops they mentioned — include @username]
- Emerging narratives: [New meta or trend being discussed — include @username]
- Notable exits/warnings: [Who's selling or warning about what — include @username]

### 7. Extra / Warnings
- [Any red flags or opportunities noticed]
- [Personal observations]

---
*Report time: 00:00 UTC | NFA/DYOR*
```

**报告发送方式：** 通过用户指定的渠道（Discord、Telegram等）发送报告

---

## 功能2：按需分析

**用户操作：** “你对$PEPEAI有什么看法？” 或 “分析FomoBears NFT”

**系统操作：**

```bash
# Deep scan this specific asset
bird search "$PEPEAI" -n 30
bird search "$PEPEAI (gem OR scam OR rug OR buy)" -n 20
```

**分析收集到的推文：**
1. **统计情绪倾向：** 看涨 vs 看跌 vs 中立
2. **识别观点强烈的用户：** 显示他们的持仓规模、钱包截图以及相关讨论帖
3. **检查高信誉度的用户：** 他们是否是可靠的预测者
4. **查找风险信号：** 检查是否存在合约问题、使用重复的用户名或匿名团队

**分析结果生成格式：**

```
📊 CT Sentiments:
[4-5 line summary based on top 20-30 recent tweets about the asset. What are people saying? Any patterns? Hype or concern? Specific details about the project/token/NFT]
📈 Overall: [Bullish/Bearish/Neutral] (assessment at end of CT Sentiments section)

🐋 Takes of High-Rep Accounts:
[@Influencer1: "quote or summary of their take" — Bullish]
[@Influencer2: "quote or summary of their take" — Bearish]
[Or: No noticeable activity detected from high-rep accounts — Bearish]

⚠️ Red Flags:
[Any contract issues, anon team, copycat name, LP not locked, etc. Or: None detected]

📊 Score: XX/100

✅ Verdict: [High/Medium/Low confidence — Bullish/Neutral/Bearish]

⚡ NFA / DYOR
```

**数据收集方式：**
```bash
# Get general sentiment tweets
bird search "$TICKER" -n 30

# Get high-rep account takes specifically
bird search "$TICKER (from:DegenKing OR from:AlphaKing OR from:CryptoGem)" -n 20
# Add more KOLs as needed
```

**评分标准：**
- **90-100分：** 看涨情绪占主导，高信誉度用户多数，无风险信号
- **70-89分：** 看涨情绪中等，部分高信誉度用户参与预测，存在小问题
- **50-69分：** 情绪复杂/中立，无明显趋势或高信誉度用户保持沉默
- **30-49分：** 看跌信号明显，存在风险信号或高信誉度用户发出警告
- **0-29分：** 看跌情绪强烈，存在多个风险信号，建议避免投资

---

## 信号评分标准

**CT情绪评分（0-100分）：**
- **80-100分：** 看涨情绪占主导，高信誉度用户多数，无风险信号
- **50-79分：** 情绪复杂或中等，需要进一步研究
- **<50分：** 看跌情绪占主导或存在多个风险信号

**重点关注词汇：**
- **看涨信号：** “gem”（优质资产）、“undervalued”（被低估）、“loading up”（正在买入）、“next 100x”（未来价值将增长100倍）
- **看跌信号：** “rug”（骗局）、“avoid”（避免投资）、“dumping”（抛售）
- **观点强烈的用户特征：** 提供具体投资金额（如“买入了5000美元”）、钱包截图、详细讨论帖
- **风险信号：** 合同未验证、锁定机制缺失、使用重复的用户名、团队完全匿名

---

## 快速命令

| 功能 | 命令 |
|------|---------|
| 生成每日报告 | 运行过去24小时的扫描并整理主要预测结果 |
| 分析资产 | `bird search "$TICKER" -n 30` | （搜索指定股票/代币的推文） |
| 检查特定用户 | `bird search "from:username" -n 20` | （搜索特定用户的推文） |
| 查找NFT发行信息 | `bird search "free mint OR minting now NFT" -n 15` | （搜索免费的或正在发行的NFT） |

---

**示例操作：**

**用户操作：** “获取我的Alpha报告”

**系统操作：** 运行每日扫描 → 整理主要预测结果 → 格式化报告 → 通过指定渠道发送

**用户操作：** “$MOONSHOT的情况如何？”

**系统操作：** 搜索关于$MOONSHOT的推文（30条） → 分析情绪倾向 → 检查风险信号 → 提供分析报告（包含评分、结论及风险提示）

**用户操作：** “@DegenKing可靠吗？”

**系统操作：** 搜索用户@DegenKing的推文 → 评估其预测能力：** “以提供有根据的预测而闻名，近期表现稳定” 或 “近期预测结果参差不齐，建议核实后再投资”

---

*专为代理经济设计。本工具提供未经验证的分析结果（NFA）。请自行判断风险。* 🦅