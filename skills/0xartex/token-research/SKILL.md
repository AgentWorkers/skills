---
name: token-research
description: 针对 EVM 链路（如 Base、ETH、Arbitrum）和 Solana 的全面代币研究功能。当您需要研究加密货币代币、深入了解相关项目或监控代币动态时，可以使用此技能。
---
该技能涵盖了针对EVM链（Base、ETH、Arbitrum）和Solana平台的综合代币研究功能，提供了两种研究模式：**深度研究（Deep Research）**和**浅层分析（Shallow Dive）**。

### 强制性要求：务必联系代币所有者获取确认

**任何被标记为“WATCH”（🟡）或“APE”（🟢）的代币，都必须立即联系所有者，并通过Telegram、Discord或WhatsApp发送私信进行确认。** 无例外！

1. 运行以下命令：`~/workspace/scripts/ape-call.sh "WATCH/APE alert: $TICKER at $MCAPk mcap, $VOLk volume. [1-line reason]"`（如果没有相关脚本，则直接联系所有者）。
2. 向所有者发送包含详细分析内容的私信。
3. 两者都必须执行——既需要联系所有者，也需要发送私信。每次都要这样做。

**严禁**：以“所有者可能不在”为由推迟操作；不要因为代币属于“纯粹的娱乐性代币”或“缺乏故事性”就忽略它；也不要在未联系所有者的情况下处理相关警报。

### 强制性要求：务必在X（Twitter）和Twitter上进行查询

**在给出任何判断之前，务必在X和Twitter上搜索以下信息：**
1. 搜索 `$TICKER` 和项目名称（包括最新和热门的相关内容）。
2. 查看项目的Twitter账户：查看推文、个人简介以及他们正在开发的产品或项目。
3. 寻找该项目的实际产品（如网站、GitHub代码库、应用程序或相关协议）。

**重要提示：** 使用“x-research”技能在X平台上进行搜索。

**如果该项目确实存在，无论市场走势如何，都必须联系所有者。** 对于实际存在的项目来说，即使市场表现不佳，也可能是一个买入机会，因此不能因此放弃研究。

**纯粹的娱乐性代币应默认避免投资。** 唯一的例外情况是：该代币的成交量是批次平均值的10倍以上。

### 报告与关注列表

- **报告文件格式：`reports/YYYY-MM-DD/[report-name].md`
- **关注列表文件格式：`watchlists/YYYY-MM/watchlist.md`

#### 关注列表规则：
- 在完成任何研究后，如果某个代币拥有实际的产品或团队支持，或者具有独特的故事性，应将其添加到关注列表中。
- 关注列表分为三个等级：**一级（最强推荐）**、**二级（信号良好，风险较高）**、**三级（投机性）**。
- 每个条目应包含代币名称、所属链、项目团队、当前市场资本化（MCAP）、最新市场资本化（MC）、推动该代币价格上涨的催化剂以及当前状态（🟢、🟡、🔴）。
- 只允许添加新条目，禁止覆盖现有条目。当有新数据时更新状态。

---

### 深度研究（Deep Research）

#### 第一阶段：代币基础信息
```bash
curl -s "https://api.dexscreener.com/latest/dex/tokens/CHAIN/TOKEN_ADDRESS"
curl -s "https://api.gopluslabs.io/api/v1/token_security/CHAIN_ID?contract_addresses=TOKEN_ADDRESS"
```

#### 第二阶段：X/Twitter调研（最重要阶段）
```bash
# Search by ticker, CA, and project name
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=\$TICKER&queryType=Latest" -H "X-API-Key: $TWITTERAPI_KEY"
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=TOKEN_ADDRESS&queryType=Latest" -H "X-API-Key: $TWITTERAPI_KEY"

# Project account info + tweets
curl -s "https://api.twitterapi.io/twitter/user/info?userName=PROJECT_HANDLE" -H "X-API-Key: $TWITTERAPI_KEY"
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=PROJECT_HANDLE" -H "X-API-Key: $TWITTERAPI_KEY"

# KOL mentions
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=\$TICKER%20min_faves:50&queryType=Top" -H "X-API-Key: $TWITTERAPI_KEY"

# Founder research (if found)
curl -s "https://api.twitterapi.io/twitter/user/info?userName=FOUNDER_HANDLE" -H "X-API-Key: $TWITTERAPI_KEY"
```

**重要提示：** 必须通过项目官方账户来验证开发者的声明。** 绝不要相信持有者或社区关于开发者支持的说法。使用 `from:DEV_HANDLE` 来搜索与该代币相关的开发者发文记录。如果开发者没有发布过相关内容，应将其标记为“未确认”。

#### 第三阶段：网络调研
- 搜索项目的官方网站、团队/创始人的背景信息、新闻及合作伙伴关系。
- 查看Reddit上的用户反馈和讨论。

#### 第四阶段：故事性评估
**故事性评分（每份报告均需包含）：**
- 🔥 **强烈推荐**：概念新颖、具有病毒式传播潜力且具有明确的推动因素。
- 🟡 **中等推荐**：概念不错但缺乏独特性，或者概念不错但执行力度较弱。
- 🧊 **弱推荐/不推荐**：内容普通、重复性高，缺乏吸引力——这类代币的价格很可能归零。

**关键问题：** 这个代币的概念是否新颖？人们会主动分享它吗？市场是否已经对这类代币感到厌倦？为什么要在短期交易后继续持有它？

**智能资金（smart money）持有者的数量以及故事性的质量，比合约的安全性更能预示代币的未来表现。**

#### 第五阶段：风险综合评估
- 综合考虑以下因素：故事性的质量、智能资金的关注度、合约的安全性、持有者的集中度、团队的透明度、社交证明（真实用户与机器人的区别）、流动性以及买卖比率。

---

### 浅层分析（Shallow Dive）
- 仅使用以下工具进行调研：DexScreener、GoPlus以及简单的Twitter搜索和基本的网络查询。

---

### 批量研究（5个及以上代币）
- 启动多个子进程同时进行代币研究。
- 筛选结果后，**自动对排名前1-3的代币进行深度分析**，无需用户另行请求。
- 将分析报告保存为 `reports/YYYY-MM-DD/[N]-token-analysis.md`。
- 将分析结果自动添加到每月的关注列表中。