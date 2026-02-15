---
name: financial-intel
description: **股票动量扫描器与投资组合智能工具**  
您可以查询任意股票的动量评分、相对强弱指数（RSI）、价格突破模式以及人工智能分析结果。该工具能够扫描超过6,500只股票和加密货币的优质投资信号，并实时提醒您投资组合的持仓情况。通过自然语言交互，您可以获取市场动态、行业趋势、盈亏数据以及风险评估等信息。该工具基于730天的历史数据进行回测，其5天内的胜率为80%。
metadata: {"clawdbot": {"requires": {"bins": ["python3"], "env": ["BF_API_KEY"]}, "primaryEnv": "BF_API_KEY", "emoji": "📊", "version": "1.9.0", "author": "clawd", "license": "MIT", "homepage": "https://bananafarmer.app", "tags": ["stocks", "crypto", "momentum", "portfolio", "market-data", "trading", "signals", "technical-analysis", "financial-data", "scanner"]}}
---

## 金融智能技能

该技能能够实时评估6,500多只股票和加密货币资产的动量，并提供市场情报。该服务由[Banana Farmer](https://bananafarmer.app)提供——这是一个基于人工智能的动量扫描工具，它将技术分析、价格动量和市场情绪整合为一个0-100的“成熟度评分”。

该服务基于730天的跟踪数据，涵盖了12,450多个股票指标，并且经过验证，其五天内的胜率为80%。

### 快速入门

**选项A——立即免费获取API密钥（无需注册账户）：**
```bash
curl -s -X POST "https://bananafarmer.app/api/bot/v1/keys/trial" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "email": "you@example.com"}'
```
从响应中保存`key`。每个电子邮件地址仅提供一个密钥，无需信用卡。

**选项B——注册完整账户：** [bananafarmer.app/developers](https://bananafarmer.app/developers)
然后：
1. **设置您的API密钥**：`export BF_API_KEY=bf_bot_your_key_here`（或将其添加到OpenClaw配置文件中）
2. **尝试使用**：`python3 scripts/bf-lookup.py AAPL` —— 您将获得评分、徽章、RSI指标、价格走势、看涨/看跌情况以及需要关注的事项。

就这样，您就可以开始扫描6,500多种资产以寻找动量信号了。

---

### 常见查询示例

### 单个股票分析

查询任何股票或加密货币的完整动量信息：评分、徽章、RSI指标、价格走势、EMA对齐情况、价格波动性、评分细节、人工智能总结以及看涨/看跌情况。

**示例查询：**
- “AAPL的动量如何？”
- “帮我查询TSLA的情况”
- “比特币的表现如何？”
- “检查NVDA的评分和技术指标”
- “CRWV是否已经成熟？”
- “AMD的动量评分是多少？”
- “查看SMCI的完整分析”
- “PLTR现在是否被过度买入了？”

**使用方法：**
```bash
python3 scripts/bf-lookup.py AAPL
python3 scripts/bf-lookup.py TSLA NVDA AMD   # Multiple tickers at once
python3 scripts/bf-lookup.py BTC              # Crypto works too
```

**您将获得的信息：**评分（0-100分）、徽章（成熟/正在成熟/过熟/为时已晚/中性）、当前价格、1天和5天的价格变化、带有超买/超卖标签的RSI指标、带有突破标志的动量评分、EMA 20/50的对齐情况、距离52周高点的距离、波动性指标、评分细节、关键驱动因素、人工智能总结、看涨/看跌情况以及需要关注的事项。

---

### 最高评分信号/批量分析

查看当前评分最高的动量信号——这些股票在技术指标、价格走势和市场情绪方面都表现出最强的一致性。

**示例查询：**
- “目前哪些信号评分最高？”
- “显示最热门的动量指标”
- “今天有成熟的信号吗？”
- “按动量评分排名前5的股票”
- “有哪些正在成熟的股票值得关注？”
- “显示前20个信号”
- “有成熟的加密货币信号吗？”

**使用方法：**
```bash
python3 scripts/bf-market.py top                        # Default top 10, all badges
python3 scripts/bf-market.py top --limit 20             # Top 20
python3 scripts/bf-market.py top --badge ripe           # Only ripe signals
python3 scripts/bf-market.py top --badge ripening       # Only ripening (watchlist candidates)
python3 scripts/bf-market.py top --limit 5 --badge ripe # Top 5 ripe only
```

**您将获得的信息：**按评分排名的表格，包括股票代码、评分、徽章、1天变化、5天变化以及每个信号的关键驱动因素。结果会自动去除重复项。

---

### 投资组合跟踪

跟踪多个账户中的持股情况。系统会生成类似晨报的智能报告，包含RSI超买/超卖的警报、每日的大幅价格变动、成熟/过熟的信号、风险提示以及盈亏计算。

**示例查询：**
- “检查我的投资组合”
- “我的持股表现如何？”
- “运行投资组合概览”
- “我的持仓有任何警报吗？”
- “我的激进型账户表现如何？”
- “我的科技股持仓的盈亏情况如何？”
- “我的任何持仓是否被过度买入了？”
- “我的哪些股票已经成熟？”

**使用方法：**
```bash
python3 scripts/bf-portfolio.py portfolios.json                 # Full brief, all accounts
python3 scripts/bf-portfolio.py portfolios.json --account aaron  # Filter to one account
python3 scripts/bf-portfolio.py portfolios.json --json           # JSON output for piping
```

**投资组合文件格式**（`portfolios.json`）：
```json
{
  "accounts": [
    {
      "id": "personal",
      "name": "My Portfolio",
      "risk_profile": "aggressive",
      "holdings": [
        {"symbol": "AAPL", "shares": 50, "cost_basis": 185.00},
        {"symbol": "NVDA", "shares": 20, "cost_basis": 450.00},
        {"symbol": "TSLA", "shares": 10, "cost_basis": 210.00}
      ]
    },
    {
      "id": "retirement",
      "name": "IRA Account",
      "risk_profile": "conservative",
      "holdings": [
        {"symbol": "VOO", "shares": 100, "cost_basis": 430.00},
        {"symbol": "ABBV", "shares": 40, "cost_basis": 155.00}
      ]
    }
  ]
}
```

**您将获得的信息：**市场状态、数据更新频率、每个账户的详细信息（包括超买/超卖、大幅价格变动、成熟/过熟的信号、为时已晚的警告），以及详细的持股信息（包括价格、评分、徽章、变化幅度、RSI指标、持股数量、成本基础和未实现的盈亏百分比）。

**生成的警报类型：**
- **SIGNAL**：持股已经成熟或过熟
- **CAUTION**：持股为时已晚（动量耗尽）
- **OVERBOUGHT**：RSI超过70（强烈警告）
- **OVERSOLD**：RSI低于30（可能的反弹区间）
- **BIG MOVE**：每日价格变动超过5%
- **WEEKLY**：五天内价格变动超过10%

---

### 市场概览

获得市场的整体情况：按徽章分类的信号数量、当前的热门趋势、新的成熟信号以及简要的市场分析。

**示例查询：**
- “今天市场表现如何？”
- “给我一个市场概览”
- “整体动量状况如何？”
- “目前有多少成熟的信号？”
- “市场当前的趋势是什么？”
- “今天有新的成熟信号吗？”

**使用方法：**
```bash
python3 scripts/bf-market.py pulse
```

**您将获得的信息：**市场概览、按徽章分类的信号数量（成熟、正在成熟、过熟、为时已晚、中性）、热门股票列表，以及刚刚达到成熟阈值的信号。

---

### 绩效跟踪/验证数据

查看哪些信号实际产生了效果：包括获胜和失败的案例，以及它们的实际入场价格、当前价格、百分比变化和多时间段的回报情况。

**示例查询：**
- “这周哪些信号有效？”
- “显示最近的获胜案例”
- “最近的表现如何？”
- “最近有哪些大幅波动的信号？”
- “显示过去30天的获胜案例”
- “这周有多少信号成功了？”
- “最近最大的亏损案例是什么？”

**使用方法：**
```bash
python3 scripts/bf-movers.py                       # Default: last 7 days, top 5
python3 scripts/bf-movers.py --days 30 --limit 10  # Last 30 days, top 10
python3 scripts/bf-movers.py --days 1 --limit 3    # Today's movers
```

**您将获得的信息：**获胜和失败案例的列表，包括股票代码、百分比变化、入场价格、当前价格以及各个时间段的回报情况。同时会提供该时期的胜率总结。

---

### 风险评估

评估股票是否处于过度买入状态或存在风险。结合RSI指标、徽章、动量评分和波动性数据来评估风险。

**示例查询：**
- “TSLA是否被过度买入了？”
- “NVDA目前的风险状况如何？”
- “AMD是否已经过熟？”
- “我应该担心我的SMCI持仓吗？”
- “CRWV的最大回撤幅度是多少？”
- “现在买入PLTR是否为时已晚？”
- “我的顶级信号中是否有任何过度买入的？”

**使用方法：**
```bash
python3 scripts/bf-lookup.py TSLA   # Check RSI, badge, volatility, and bear case
```

**输出中的关键信息：**
- RSI超过70：超买警告，需警惕回调
- RSI超过80：极度超买
- 徽章“overripe”：已经过度买入，可能即将回调
- 徽章“too-late”：在此水平追涨风险增加
- 最大回撤百分比：历史上的最坏情况
- 平均每日波动幅度：股票的波动性

---

### 对比查询

并行比较多个股票的动量评分、技术指标和风险状况。

**示例查询：**
- “比较AAPL和MSFT的动量”
- “NVDA和AMD哪个动量更强？”
- “查询TSLA、RIVN和LCID”
- “比较大型科技股——AAPL、GOOGL、MSFT、META”
- “哪个大盘股的动量评分最高？”

**使用方法：**
```bash
python3 scripts/bf-compare.py AAPL MSFT          # Side-by-side table comparison
python3 scripts/bf-compare.py NVDA AMD INTC AVGO # Compare semiconductor names
python3 scripts/bf-compare.py TSLA RIVN LCID     # EV sector comparison
python3 scripts/bf-lookup.py AAPL MSFT           # Full deep-dive for each (more detail)
```

**您将获得的信息：**一个格式化的对比表格，显示评分、徽章、价格、RSI指标、EMA对齐情况、52周距离、评分细节以及波动性。还包括评估结果（动量最强/最弱）和风险提示（过度买入、即将突破）。

---

### 监控列表管理

使用顶级信号和投资组合工具来构建和跟踪监控列表。可以根据徽章筛选值得关注的股票。

**示例查询：**
- “将NVDA添加到我的监控列表中”
- “有哪些正在成熟的股票值得关注？”
- “为我生成一个包含成熟信号的监控列表”
- “更新我的监控列表，包括今天的顶级成熟股票”
- “跟踪这些股票：AAPL、NVDA、AMD、TSLA”

**使用方法：**
```bash
# Today's curated watchlist picks (pre-selected by the system)
python3 scripts/bf-watchlist.py picks

# Find watchlist candidates from top signals
python3 scripts/bf-market.py top --badge ripening --limit 10

# Track specific symbols (add to portfolios.json with 0 shares)
python3 scripts/bf-portfolio.py portfolios.json
```

**提示：**可以使用`bf-watchlist.py`获取系统每日精选的信号，或者在`portfolios.json`中创建一个“watchlist”账户，设置`shares: 0`和`cost_basis: 0`。这样投资组合概览将仅显示评分、徽章、RSI指标和警报，不包括盈亏计算。

---

### 行业和主题分析

分析整个行业的动量情况，或深入研究特定行业。

**示例查询：**
- “哪些行业的动量最强？”
- “当前最热门的行业是哪个？”
- “半导体股票的表现如何？”
- “查看电动汽车行业——TSLA、RIVN、LCID、NIO”
- “为我查询FAANG公司的情况”
- “生物科技行业的情况如何？”
- “航空股票的动量如何？”

**使用方法：**
```bash
# Full sector momentum breakdown (auto-classifies top 50 signals)
python3 scripts/bf-sectors.py

# Sector data as JSON for processing
python3 scripts/bf-sectors.py --json

# Deep-dive a specific sector group
python3 scripts/bf-compare.py NVDA AMD INTC AVGO  # Semiconductors
python3 scripts/bf-compare.py AAPL MSFT GOOGL META # Big tech
python3 scripts/bf-lookup.py TSLA RIVN LCID NIO    # Full detail per ticker
```

**您将获得的信息：**该脚本按行业（科技、医疗保健、金融、能源、消费、工业、房地产等）分组显示所有顶级信号，包括信号数量、平均评分、热度等级（热门/温暖/冷淡）以及行业领导者。可以使用`bf-compare.py`在行业内进行并行比较。**

---

### 历史数据和胜率

查询系统的历史记录和统计性能数据。

**示例查询：**
- “成熟信号的五天胜率是多少？”
- “1天内的表现与5天内的表现相比如何？”
- “评分超过90的信号的平均回报是多少？”
- “总共跟踪了多少个信号？”
- “历史数据的时间跨度是多少？”
- “耐心是否真的能提高胜率？”

**使用方法：**
```bash
python3 scripts/bf-watchlist.py scorecard  # System win rates by holding period and score threshold
python3 scripts/bf-watchlist.py horizons   # Time horizon analysis (how long to hold)
python3 scripts/bf-market.py health        # System stats and data freshness
python3 scripts/bf-movers.py --days 30     # Recent track record with win rate
```

**历史记录参考**（基于730天内的12,450个信号）：

| 持仓周期 | 胜率 | 平均回报 | 平均胜率 | 平均亏损 |
|----------------|----------|------------|---------|----------|
| 1天 | 76.5% | +1.35% | +2.07% | -0.97% |
| 3天 | 78.4% | +2.69% | +3.87% | -1.62% |
| 5天 | 79.9% | +4.51% | +6.24% | -2.37% |
| 10天 | 79.4% | +5.40% | +7.54% | -2.86% |
| 1个月 | 80.1% | +8.16% | +11.26% | -4.33% |
| 2个月 | 79.1% | +9.90% | +13.96% | -5.51% |

**关键发现：**第一天的胜率为76.5%，一个月后上升到80.1%。耐心是提高胜率的关键。

---

### 警报查询

检查您的持仓或整个市场是否存在可操作的信号。

**示例查询：**
- “如果任何持仓成熟，请提醒我”
- “我的任何股票是否被过度买入了？”
- “哪些持仓的RSI低于30？”
- “是否有顶级信号的RSI超过70？”
- “我的持仓中今天有最大的价格变动吗？”
- “我的持仓中有任何为时已晚的警告吗？”

**使用方法：**
```bash
# Portfolio alerts (automatically flags ripe, overbought, oversold, big moves)
python3 scripts/bf-portfolio.py portfolios.json

# Market-wide scan for ripe signals
python3 scripts/bf-market.py top --badge ripe --limit 20

# Check specific names for risk
python3 scripts/bf-lookup.py AAPL TSLA NVDA
```

投资组合概览会自动生成警报。请注意“ALERTS”部分，其中会标记：SIGNAL（成熟/过熟）、CAUTION（为时已晚）、OVERBOUGHT（RSI > 70）、OVERSOLD（RSI < 30）、BIG MOVE（每日价格变动超过5%）、WEEKLY（五天内价格变动超过10%）以及风险状况不匹配的情况。

---

### 系统健康检查

在做出决策之前，验证数据的新鲜度和市场状态。

**示例查询：**
- “数据是否新鲜？”
- “市场是否开放？”
- “检查系统健康状况”
- “目前是否有数据问题？”

**使用方法：**
```bash
python3 scripts/bf-market.py health
```

**您将获得的信息：**市场状态（开放/关闭/盘前/盘后）、数据更新频率（实时/最近/过期），以及任何安全提示。在根据信号采取行动之前，请务必检查系统健康状况——市场交易期间数据过期可能意味着有问题。**

---

## 理解数据

### 成熟度评分（0-100）

该评分是四个维度的综合结果，每个维度的权重根据其预测能力而定：

| 维度 | 权重 | 测量内容 |
|--------|--------|-----------------|
| 技术分析 | 35-55% | 图表模式、RSI指标、移动平均线、动量形态 |
| 动量 | 25-30% | 1-3%价格区间内的价格速度和成交量确认 |
| 市场情绪 | 20-45% | Reddit和X平台上的提及次数、早期市场热度（活动量是平时的1.2-2.0倍） |
| 群众智慧 | 0-10% | 仅针对加密货币：期货持仓情况、资金率 |

评分越高，表示各个维度的一致性越强。例如，如果技术分析占45%、市场情绪占35%，则评分与技术分析占55%、市场情绪占20%的情况有所不同——请查看评分细节。

### 徽章系统

| 徽章 | 评分范围 | 含义 | 行动建议 |
|-------|------------|---------------|--------|
| Ripe | 75-89 | 设置非常明确，动量强劲，入场时机良好 | 最佳的风险/回报窗口 |
| Ripening | 60-74 | 动量正在积累但尚未完全形成 | 关注，暂不行动——加入监控列表 |
| Overripe | 90-100 | 已经过度买入，可能即将回调 | 谨慎，调整止损 |
| Too-Late | N/A | 已经出现显著价格变动，追涨风险增加 | 不要追涨 |
| Neutral | 低于60 | 没有明显的动量信号 | 没有优势，耐心等待 |

**评分的显著性阈值：**95+表示极高信心；85-94表示较强信心；80-84表示具有操作价值。

### RSI（相对强弱指数）

RSI在0-100的范围内衡量动量：
- **低于30**：超卖。价格已被压低；可能即将反弹。但这并不意味着“买入”——可能意味着卖出压力正在减弱。
- **30-70**：正常范围。
- **高于70**：过度买入。价格持续上涨；需警惕回调。
- **高于80**：极度超买。价格可能很快会反转。

### 动量评分（0-100）

动量评分衡量价格的压缩程度——即价格在多大程度上处于盘整状态。可以将其想象成被压缩的弹簧：
- **低于40**：价格自由波动，没有明显的压缩。
- **40-69**：中等压缩。有一定程度的盘整，但尚未达到显著程度。
- **70+**：价格被压缩到狭窄范围内。这通常预示着价格即将出现明显的方向性变动（突破或下跌）。这是系统中最具预测性的指标。

**同时满足高动量评分和成熟徽章的股票是最强的买入信号：动量一致，价格压缩表明接下来的价格变动可能很大。**

### EMA 20和EMA 50

指数移动平均线在20天和50天内平滑价格数据：
- **价格高于两条EMA**：牛市趋势——短期和中期看涨
- **价格高于EMA 20且低于EMA 50**：在长期下跌趋势中可能出现短期反弹——谨慎操作
- **价格低于两条EMA**：熊市趋势——动量不利于买入
- **EMA 20穿越EMA 50**：黄金交叉——可能预示趋势转变

### 距离52周高点的距离

一个0到1的小数，表示当前价格与52周高点的接近程度：
- **0.95+（95%以上）**：接近高点——相对强势，但面临阻力
- **0.80-0.95**：健康的上涨趋势
- **低于0.70**：显著偏离高点——需关注是否即将反弹或进一步下跌

---

## 绩效记录

该系统已经运行了两年多，跟踪了大量的信号：
- **分析了12,450多个信号**（730天内）
- **跟踪了6,563只独特的股票**
- **五天内的胜率为80%，平均回报率为+4.51%**
- **一天内的胜率为76.5%，一个月后上升到80.1%**
- 不同评分阈值下的胜率保持稳定：80分以上的信号胜率均在79-81%之间

### 不同评分阈值的胜率（5天周期）

| 评分范围 | 胜率 | 平均回报 | 样本数量 |
|-------------|----------|------------|-------------|
| 80-85 | 80.2% | +4.60% | 3,096 |
| 85-90 | 79.2% | +4.45% | 3,115 |
| 90-95 | 79.4% | +4.42% | 3,124 |
| 95+ | 80.7% | +4.56% | 3,115 |

### 耐心带来的优势

数据显示，持有时间越长，效果越好。第一天的胜率为76.5%，一天后上升到79.9%，一个月后达到80.1%。最佳的风险/回报窗口是5-10天的持有周期。

**注意：**这不是一个日内交易系统。它会在股票动量达到2%时买入，然后让价格走势发展几天。

---

## 错误处理

### BF_API_KEY未设置

**解决方法：**导出您的API密钥：`export BF_API_KEY=bf_bot_your_key_here`。或者将其添加到OpenClaw配置文件或`.env`文件中。

### 无信号数据

**原因：**股票未被跟踪、已退市或属于交易量极低的场外交易股票。Banana Farmer主要跟踪纽约证券交易所和纳斯达克市场的6,500多只股票以及热门加密货币。低价股和场外交易股票可能没有足够的数据来生成信号。

**解决方法：**确认股票代码是否正确。使用标准的股票代码格式（不含特殊字符）。加密货币代码使用标准格式（如BTC、ETH、SOL）。

### API超时或连接错误

**原因：**Banana Farmer API在15秒内未响应。这可能发生在市场开盘高峰期或服务暂时中断时。

**解决方法：**等待30秒后重试。如果问题持续，使用`python3 scripts/bf-market.py health`检查系统健康状况。如果系统仍然无法响应，可能是API暂时不可用。

### 数据限制

API的使用频率受到限制：免费账户（每分钟10次请求，每天50次请求），专业账户（每分钟60次请求，每天50,000次请求），高级账户（每分钟120次请求，每天50,000次请求）。在正常使用情况下，您不会遇到这些限制。如果遇到限制，请分散请求频率。投资组合脚本一次只获取一个股票的数据，因此20只股票的列表总共只会发起21次API请求。

### 数据过期警告

如果`bf-market.py health`在市场交易期间报告数据过期，可能是因为数据更新延迟。信号和评分基于每15分钟更新一次的数据。如果数据过期（超过30分钟），评分可能无法反映当前市场情况。

**解决方法：**在分析过程中注意数据是否过期。虽然价格会变动，但动量信号通常是方向性的，除非市场出现重大反转，否则通常仍然有效。

### 403 Forbidden错误

**原因：**缺少或格式错误的`User-Agent`头部信息。API要求必须包含`User-Agent: BananaFarmerBot/1.0`头部信息。

**解决方法：**脚本会自动设置这个头部信息。如果您直接调用API，请确保包含该头部信息。

---

## 高级用法

### JSON输出模式

投资组合脚本支持JSON输出格式，适用于程序化处理：

**使用方法：**该脚本返回一个JSON对象，其中包含`brief`字段（格式化的文本）和`signals`字段（每个股票的评分和徽章信息）。您可以将其用于其他工具、仪表板或自动化工作流程。

### 多账户投资组合

投资组合文件支持多个账户，每个账户都有单独的部分，并显示针对该账户的警报。持有高动量股票的保守型账户会收到特别提示。

**支持的账户类型：**`conservative`（保守型）、`moderate`（中等风险）、`aggressive`（激进型）。`--account`参数可以部分匹配账户的`id`和`name`字段。

**使用方法：**

### 结合使用多个脚本

**使用方法：**可以将多个脚本组合起来进行更深入的分析。

### 筛选顶级信号

`top`命令支持根据徽章和限制条件筛选信号。

**使用方法：**

### 控制回溯时间范围

**使用方法：**您可以控制性能跟踪的回溯时间范围。

---

## 脚本参考

| 脚本 | 功能 | 关键参数 |
|--------|---------|---------------|
| `bf-lookup.py` | 对特定股票进行深入分析 | `SYMBOL [SYMBOL2 ...]` |
| `bf-market.py` | 市场概览和信号扫描 | `health`, `top [--limit N] [--badge X]`, `pulse` |
| `bf-portfolio.py | 带有警报的投资组合智能 | `FILE.json [--account NAME] [--json]` |
| `bf-movers.py | 胜利/失败案例的验证数据 | `[--days N] [--limit N]` |
| `bf-compare.py | 并行比较多个股票 | `SYMBOL1 SYMBOL2 [SYMBOL3 ...] [--json]` |
| `bf-watchlist.py | 精选信号、评分卡和时间范围 | `picks`, `scorecard`, `horizons` `[--json]` |
| `bf-sectors.py | 行业动量分析 | `[--json]` |

所有脚本都位于`scripts/`目录中。运行这些脚本需要`python3`环境和`BF_API_KEY`。无需额外的Python包。

---

## 价格方案

| 计划 | 价格 | 提供的内容 |
|------|-------|-------------|
| 免费 | $0 | 提供系统健康状态、发现功能、前三名信号。每分钟10次请求，每天50次请求。足以验证系统效果。 |
| 专业版 | $49/月（每年$39） | 提供完整的排行榜、所有接口、证明图像、投资组合信息、价格变动情况、监控列表、30天的评分历史。每分钟60次请求，每天50,000次请求。 |
| 高级版 | $149/月（每年$119） | 包含专业版的所有功能，以及详细的信号价格数据、计算出的回报、730天的回测数据、批量导出功能、Webhook接口。每分钟120次请求，每天50,000次请求。 |

您可以在[bananafarmer.app/developers](https://bananafarmer.app/developers)立即获取API密钥。免费版本立即可用，无需信用卡。

**对比：**Danelfin Pro每月收费$79，提供带有历史数据的AI评分，但不包含价格信息；Polygon.io每月收费$79-500，提供原始价格数据但不包含分析功能；Alpha Vantage每月收费$50-250，也提供原始价格数据；Banana Farmer高级版每月收费$149，同时提供动量分析和详细的信号价格数据，以及730天的回测结果。**

## 安全性

该服务注重透明度和安全性：

- **仅使用HTTPS协议**：所有脚本仅发送HTTPS请求到`bananafarmer.app`，不进行任何其他网络连接或数据泄露。
- **无第三方依赖**：所有脚本仅使用Python的标准库（`json`, `urllib`, `ssl`, `os`, `sys`）。
- **开源代码**：源代码完全公开，可审核。
- **API密钥安全**：API密钥仅从`BF_API_KEY`环境变量中读取，不会被硬编码或记录。
- **仅读取数据**：该服务仅读取市场数据，不执行交易、管理账户或修改用户系统中的文件。
- **基础设施安全**：采用[安全措施](https://bananafarmer.app/security)，包括TLS 1.3、AES-256加密、Cloudflare WAF和Stripe PCI DSS Level 1安全标准。
- **法律条款**：提供[服务条款](https://bananafarmer.app/terms)和[隐私政策](https://bananafarmer.app/privacy)。

## 免责声明

该服务提供财务数据、动量评分和分析结果，但**不提供投资建议**。所有数据仅用于信息和研究目的。

- 该工具不提供买卖建议
- 过去的表现不能保证未来的结果
- 用户应在做出投资决策前自行进行研究并咨询持证财务顾问
- 胜率和回报数据基于历史数据
- 股票数据延迟15分钟（根据交易所规定）；加密货币数据接近实时

使用该服务即表示您同意[Banana Farmer的API使用条款](https://bananafarmer.app/terms#api)。

市场数据来自[Tiingo.com](https://tiingo.com)，动量评分和成熟度评分方法由[Banana Farmer](https://bananafarmer.app)提供。