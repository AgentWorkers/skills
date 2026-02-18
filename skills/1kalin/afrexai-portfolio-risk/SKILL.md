# 投资组合风险分析器

这是一个完整的投资组合风险管理系统，能够分析投资组合中的各个资产、计算风险指标、进行压力测试、优化资产配置，并生成机构级别的风险报告——所有这些功能均无需依赖外部API。

---

## 1. 投资组合导入

当用户分享他们的投资组合（包括持有的资产、股票代码及持有数量）时，请按照以下格式组织数据：

```yaml
portfolio:
  name: "User Portfolio"
  currency: USD
  as_of: "2026-02-15"
  positions:
    - ticker: AAPL
      shares: 50
      avg_cost: 185.00
      current_price: 228.50  # Look up via web search
      asset_class: US_EQUITY
      sector: Technology
    - ticker: BTC
      units: 0.5
      avg_cost: 42000
      current_price: 97500
      asset_class: CRYPTO
      sector: Digital Assets
    - ticker: VOO
      shares: 100
      avg_cost: 410.00
      current_price: 535.00
      asset_class: US_EQUITY_ETF
      sector: Broad Market
  cash:
    amount: 15000
    currency: USD
```

### 价格查询
对于每个资产，使用网络搜索来获取当前价格：
- 股票：`[股票代码] 当前股价`
- 加密货币：`[加密货币代码] 当前价格（美元）`
- 记录查询来源和时间戳

### 投资组合汇总表

| 资产 | 持有股数 | 成本基础 | 当前价值 | 权重 | 盈亏 | 盈亏百分比 |
|----------|--------|-----------|---------------|--------|-----|-------|
| AAPL | 50 | $9,250 | $11,425 | 18.2% | +$2,175 | +23.5% |
| ... | ... | ... | ... | ... | ... |
| **总计** | | **$XX,XXX** | **$XX,XXX** | **100%** | **±$X,XXX** | **±X.X%** |

---

## 2. 风险指标计算器

针对每次投资组合分析，计算以下所有风险指标：

### 2.1 集中风险

```
Position Concentration:
- Any single position >20% of portfolio = HIGH RISK ⚠️
- Any single position >10% = MODERATE RISK
- Top 3 positions >50% = CONCENTRATED

Sector Concentration:
- Any sector >30% = OVERWEIGHT
- Count unique sectors — fewer than 4 = UNDER-DIVERSIFIED

Asset Class Breakdown:
- Equities: X%
- Fixed Income: X%
- Crypto: X%
- Cash: X%
- Alternatives: X%
```

### 2.2 风险价值（VaR）——参数法

在给定的置信水平下，计算最大预期损失：

```
Daily VaR Calculation:
1. Look up each position's historical volatility (annualized)
   - Use web search: "[TICKER] historical volatility 30 day"
   - Typical ranges: Large cap stocks 15-25%, Crypto 50-80%, Bonds 5-10%

2. Convert to daily volatility:
   Daily Vol = Annual Vol / √252

3. Position VaR (95% confidence):
   Position VaR = Position Value × Daily Vol × 1.645

4. Position VaR (99% confidence):
   Position VaR = Position Value × Daily Vol × 2.326

5. Portfolio VaR (simplified — assumes correlation ≈ 0.5 for stocks):
   Portfolio VaR ≈ √(Σ(Position VaR²) + 2×0.5×Σ(VaR_i × VaR_j))

Report:
- 1-Day 95% VaR: $X,XXX (X.X% of portfolio)
- 1-Day 99% VaR: $X,XXX (X.X% of portfolio)
- 10-Day 95% VaR: $X,XXX (= 1-Day VaR × √10)
- Monthly 95% VaR: $X,XXX (= 1-Day VaR × √21)
```

### 2.3 最大回撤估计

```
Based on asset class historical max drawdowns:
- US Large Cap: -50% (2008-09), typical correction -20%
- US Small Cap: -55%, typical correction -25%
- International Equity: -55%, typical -25%
- Emerging Markets: -65%, typical -30%
- Investment Grade Bonds: -15%, typical -5%
- High Yield Bonds: -30%, typical -10%
- REITs: -70%, typical -25%
- Crypto (BTC): -85%, typical -50%
- Gold: -45%, typical -15%
- Cash: 0%

Portfolio Max Drawdown Estimate:
= Σ(Position Weight × Asset Class Max Drawdown)

Report:
- Estimated worst-case drawdown: -$XX,XXX (XX.X%)
- Estimated typical correction: -$XX,XXX (XX.X%)
- Recovery time estimate: X-X months (based on historical averages)
```

### 2.4 贝塔系数与市场敏感性

```
For each equity position:
- Look up beta via web search: "[TICKER] beta"
- Portfolio Beta = Σ(Position Weight × Position Beta)

Interpretation:
- Beta > 1.2: Portfolio is AGGRESSIVE (amplifies market moves)
- Beta 0.8-1.2: Portfolio is NEUTRAL
- Beta < 0.8: Portfolio is DEFENSIVE
- Negative beta positions: HEDGE value

Market Impact:
- If S&P 500 drops 10%, portfolio expected to move: Beta × -10%
```

### 2.5 夏普比率估计

```
Portfolio Expected Return = Σ(Weight × Expected Return)
Where Expected Return by asset class:
- US Large Cap: 8-10% annually
- US Small Cap: 9-11%
- International Developed: 6-8%
- Emerging Markets: 8-12%
- Investment Grade Bonds: 4-5%
- High Yield: 6-7%
- Crypto: highly variable (use 0% for conservative estimate)
- REITs: 7-9%
- Cash: current money market rate (~4.5%)

Risk-Free Rate: current 3-month T-bill rate (search if needed)

Sharpe Ratio = (Portfolio Expected Return - Risk-Free Rate) / Portfolio Volatility

Rating:
- > 1.0: EXCELLENT risk-adjusted returns
- 0.5-1.0: GOOD
- 0-0.5: MEDIOCRE — consider rebalancing
- < 0: POOR — return doesn't justify risk
```

### 2.6 收益分析

```
For dividend-paying positions:
- Look up dividend yield: "[TICKER] dividend yield"
- Annual Income = Shares × Annual Dividend per Share
- Portfolio Yield = Total Annual Dividends / Portfolio Value

Report:
- Monthly estimated income: $XXX
- Annual estimated income: $X,XXX
- Yield on cost: X.X%
- Current yield: X.X%
```

---

## 3. 压力测试

对投资组合运行各种压力测试场景，并报告测试结果：

### 3.1 标准压力测试场景

```yaml
scenarios:
  market_crash_2008:
    name: "2008 Financial Crisis"
    impacts:
      US_EQUITY: -0.50
      INTL_EQUITY: -0.55
      EMERGING: -0.60
      BONDS: +0.05
      HIGH_YIELD: -0.30
      REITS: -0.70
      CRYPTO: -0.80  # projected based on risk profile
      GOLD: +0.10
      CASH: 0

  covid_crash_2020:
    name: "COVID-19 Crash (Feb-Mar 2020)"
    impacts:
      US_EQUITY: -0.34
      INTL_EQUITY: -0.35
      EMERGING: -0.35
      BONDS: +0.03
      HIGH_YIELD: -0.20
      REITS: -0.40
      CRYPTO: -0.50
      GOLD: -0.05
      CASH: 0

  dot_com_2000:
    name: "Dot-Com Bust (2000-2002)"
    impacts:
      US_EQUITY: -0.45
      TECH: -0.75  # Apply to technology sector specifically
      INTL_EQUITY: -0.40
      BONDS: +0.15
      CASH: 0

  rate_hike_shock:
    name: "Rapid Rate Hike (+300bps)"
    impacts:
      US_EQUITY: -0.15
      BONDS: -0.15
      HIGH_YIELD: -0.10
      REITS: -0.25
      CRYPTO: -0.20
      GOLD: -0.10
      CASH: +0.01  # higher yields

  inflation_surge:
    name: "Stagflation (persistent 8%+ inflation)"
    impacts:
      US_EQUITY: -0.20
      BONDS: -0.20
      CRYPTO: -0.10  # debatable hedge
      GOLD: +0.15
      REITS: -0.05
      COMMODITIES: +0.20
      CASH: -0.03  # real value erosion

  crypto_winter:
    name: "Crypto Winter (80% drawdown)"
    impacts:
      CRYPTO: -0.80
      US_EQUITY: -0.05  # minor contagion
```

### 3.2 压力测试报告格式

对于每个测试场景，生成相应的报告：

```
📉 SCENARIO: [Name]

| Position | Current Value | Stressed Value | Loss |
|----------|--------------|----------------|------|
| AAPL     | $11,425      | $5,713         | -$5,712 |
| ...      | ...          | ...            | ...  |
| TOTAL    | $XX,XXX      | $XX,XXX        | -$XX,XXX (-XX.X%) |

Could you survive this? [YES/NO based on cash reserves and income needs]
Recovery estimate: X-X months
```

### 3.3 自定义压力测试场景

如果用户指出了特定的风险点，可以构建相应的自定义测试场景：

```
User: "What if tech crashes 40% but bonds rally?"
→ Build custom impact map, apply to portfolio, report results
```

---

## 4. 投资组合优化

### 4.1 当前资产配置评估

```
Compare current allocation to standard models:

AGGRESSIVE (Age <35, high risk tolerance):
  Equities: 80-90%, Bonds: 5-10%, Alternatives: 5-10%, Cash: 2-5%

GROWTH (Age 35-50):
  Equities: 60-75%, Bonds: 15-25%, Alternatives: 5-10%, Cash: 5%

BALANCED (Age 50-60):
  Equities: 40-60%, Bonds: 30-40%, Alternatives: 5-10%, Cash: 5-10%

CONSERVATIVE (Age 60+, income focus):
  Equities: 20-40%, Bonds: 40-50%, Alternatives: 5%, Cash: 10-20%

Current allocation matches: [MODEL] profile
Recommended adjustments: [specific moves]
```

### 4.2 风险均衡分析

```
Risk Parity Target: Each asset class contributes EQUAL risk to portfolio

Steps:
1. Calculate each position's risk contribution:
   Risk Contribution = Weight × Volatility × Correlation_with_portfolio

2. For equal risk contribution:
   Target Weight_i = (1/Vol_i) / Σ(1/Vol_j)

3. Report:
   Current vs Risk-Parity weights
   Trades needed to rebalance
   Expected impact on Sharpe Ratio
```

### 4.3 重新平衡建议

```
Check rebalancing triggers:
- Any position drifted >5% from target? → REBALANCE
- Any asset class drifted >10% from target? → REBALANCE
- Last rebalance >6 months ago? → REVIEW

Rebalancing Method:
1. Calculate target weights
2. Calculate current weights
3. Determine trades needed (minimize transactions)
4. Tax-lot optimization: sell highest-cost lots first (minimize tax)
5. Consider wash sale rules if harvesting losses

Output trade list:
| Action | Ticker | Shares | Est. Value | Reason |
|--------|--------|--------|-----------|--------|
| SELL   | AAPL   | 15     | $3,428    | Overweight tech |
| BUY    | BND    | 25     | $1,850    | Underweight bonds |
```

### 4.4 相关性分析

```
Assess diversification quality:

HIGH correlation pairs (>0.7) — these DON'T diversify each other:
- Tech stocks with each other
- US equity ETFs with each other
- High yield bonds with equities

LOW correlation pairs (<0.3) — TRUE diversifiers:
- Stocks vs Treasury bonds
- US vs Gold
- Equities vs Managed Futures

NEGATIVE correlation — HEDGES:
- Long equity + Put options
- Stocks + VIX products
- Growth + Value in some regimes

Grade portfolio diversification: A/B/C/D/F
```

---

## 5. 风险评分（0-100）

生成一个综合风险评分：

```yaml
risk_scorecard:
  concentration_risk:
    weight: 20
    score: X  # 100 = well diversified, 0 = single stock
    details: "Top position is X%, X sectors represented"

  volatility_risk:
    weight: 20
    score: X  # 100 = low vol, 0 = extremely volatile
    details: "Portfolio annualized vol: X%"

  drawdown_risk:
    weight: 20
    score: X  # 100 = minimal drawdown exposure, 0 = could lose 50%+
    details: "Max estimated drawdown: X%"

  liquidity_risk:
    weight: 15
    score: X  # 100 = all highly liquid, 0 = illiquid positions
    details: "X% in liquid large-cap, X% in illiquid"

  income_resilience:
    weight: 10
    score: X  # 100 = strong income, 0 = no yield
    details: "Portfolio yield: X%, X% from reliable dividend payers"

  market_sensitivity:
    weight: 15
    score: X  # 100 = low beta/defensive, 0 = highly aggressive
    details: "Portfolio beta: X.XX"

  overall_score: X/100
  rating: "[CONSERVATIVE|MODERATE|AGGRESSIVE|SPECULATIVE]"
  recommendation: "[Key action item]"
```

### 评分解读：
- 80-100：风险保护良好，但可能过于保守（不适合追求高增长）
- 60-79：风险管理较为稳健，有改进空间
- 40-59：风险水平适中，但仍存在显著风险
- 20-39：风险较高，建议重新平衡资产配置
- 0-19：风险极高，需要立即采取行动

---

## 6. 监控与警报

### 日常检查模板（用于定时任务）

```
For each portfolio position:
1. Check price vs previous close (web search)
2. Flag if any position moved >3% in a day
3. Flag if any position hit stop-loss level
4. Check for earnings/events in next 7 days

Alert Thresholds:
- Single position -5% in a day → ALERT
- Portfolio -3% in a day → ALERT
- Position hits 52-week low → WATCH
- VIX > 25 → ELEVATED CAUTION
- VIX > 35 → HIGH ALERT — review hedges
```

### 周度审查模板

```markdown
## Portfolio Weekly Review — [Date]

### Performance
- Portfolio value: $XX,XXX (±X.X% week)
- Best performer: [TICKER] +X.X%
- Worst performer: [TICKER] -X.X%
- vs S&P 500: [outperformed/underperformed] by X.X%

### Risk Changes
- VaR change: $X,XXX → $X,XXX
- Any new concentration issues? [Y/N]
- Rebalancing needed? [Y/N]

### Upcoming Events
- Earnings: [tickers and dates]
- Ex-dividend dates: [tickers and dates]
- Fed/macro events: [list]

### Action Items
1. [Specific recommendation]
2. [Specific recommendation]
```

---

## 7. 税务损失收割工具

```
For each position with unrealized losses:
1. Calculate unrealized loss: (Current Price - Avg Cost) × Shares
2. Check if loss >$500 (worth harvesting)
3. Identify tax-efficient replacement:
   - Same sector ETF (avoids wash sale)
   - Similar factor exposure
   - Hold replacement 31+ days before switching back

Report:
| Ticker | Unrealized Loss | Replacement | Wash Sale Clear Date |
|--------|----------------|-------------|---------------------|
| XYZ    | -$2,500        | Similar ETF | [date + 31 days]   |

Estimated tax savings: $X,XXX (at X% marginal rate)
```

---

## 8. 特殊资产类别

### 加密货币投资组合风险

- 加密货币特有的风险指标：
  - 比特币主导地位与市场相关性
  - 交易所风险（中心化存储与去中心化存储）
  - DeFi投资的相关性风险
  - 稳定币的暴露风险及脱钩风险
  - 持币/收益的税务影响

### 房地产投资（REITs/实物资产）

- 自由现金流收益率与股息收益率
- 利率敏感性
- 地理分布集中度
- 资产类型多样性（住宅/商业/工业）

### 期权投资

如果投资组合包含期权：
- Delta风险（期权对标的股票价格的影响）
- Theta风险（期权时间价值衰减）
- 隐含波动率与历史波动率对比
- 最大损失估算
- 平值价格计算

---

## 9. 报告生成

### 完整风险报告（按需生成）

生成一份可导出为PDF的Markdown报告：

```markdown
# Portfolio Risk Report
## Prepared: [Date]
## Portfolio: [Name]

### Executive Summary
[2-3 sentence overview: total value, risk rating, top recommendation]

### 1. Holdings Summary
[Position table from Section 1]

### 2. Risk Metrics
[All calculations from Section 2]

### 3. Stress Test Results
[All scenarios from Section 3]

### 4. Optimization Recommendations
[From Section 4]

### 5. Risk Scorecard
[From Section 5]

### 6. Action Plan
[Prioritized list of recommended changes]

### Disclaimer
This analysis is for informational purposes only and does not constitute
financial advice. Past performance and historical data do not guarantee
future results. Consult a qualified financial advisor before making
investment decisions.
```

---

## 10. 快速命令

支持以下自然语言指令：

| 用户指令 | 执行操作 |
|-----------|--------|
| “分析我的投资组合” | 执行第1-5节的分析 |
| “我的风险状况如何？” | 显示风险评分（第5节） |
| “对我的投资组合进行压力测试” | 运行所有压力测试场景（第3节） |
| “如果市场崩盘会怎样？” | 模拟2008年金融危机和COVID-19疫情的影响 |
| “如何重新平衡资产？” | 根据第4节建议进行资产调整 |
| “进行税务损失收割” | 使用第7节工具进行税务损失评估 |
| “进行每周审查” | 生成每周审查报告 |
| “添加[资产]” | 更新投资组合数据并重新计算风险指标 |
| “移除[资产]” | 更新投资组合数据并重新计算风险指标 |
| “我的风险价值是多少？” | 计算风险价值（第2.2节） |
| “与标普500指数对比” | 进行基准对比 |
| “我的投资组合多元化程度如何？” | 分析资产集中度与相关性 |
| “我的夏普比率是多少？” | 计算夏普比率（第2.5节） |
| “为[股票代码]设置价格警报” | 将该股票加入监控列表（第6节） |

---

## 特殊情况处理

### 小型投资组合（<1万美元）

- 跳过风险价值（VaR）的计算（对于小额投资意义不大）
- 重点关注资产集中风险和资金使用效率
- 建议采用指数投资策略

### 单一股票投资组合（例如公司限制性股票）

- 必须标记极端集中的风险
- 建议使用保护性策略（如看跌期权+看涨期权组合）
- 对内部人士提供10b5-1计划的相关提醒
- 计算每季度应增加的资产多样性

### 加密货币占比较高（>50%）

- 特别关注加密货币市场的不利因素
- 强调交易所对手方风险
- 建议提高冷存储比例
- 注意DeFi/质押操作的税务复杂性

### 国际投资组合

- 考虑货币风险
- 国家风险溢价
- 分红所得的预扣税影响
- ADR（美国存托凭证）与本地股票的区别

### 杠杆投资（保证金/期权）

- 计算保证金追加价格
- 在2倍最大回撤情况下进行压力测试
- 如果保证金使用率超过50%，发出警报
- 模拟强制清算情景

### 退休账户（IRA/401(k)）

- 享受不同的税收优惠政策（无需进行税务损失收割）
- 了解传统IRA的RMD（最低提取要求）
- 分析Roth账户的转换机会
- 考虑临近退休者的投资回报序列风险