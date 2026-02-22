# 投资分析与投资组合管理引擎

该工具提供完整的投资分析、投资组合构建、风险管理以及交易执行服务，支持股票、加密货币、ETF、债券等多种资产类型。完全独立于外部系统，仅依赖内置的智能算法。

## 快速健康检查（/8）

在进行任何投资活动之前，请先评估您的投资组合现状：

| 项目 | 是否健康 | 需要改进 |
|--------|---------|---------|
| 投资逻辑是否明确记录 | 有详细的分析且可验证 | “我认为价格会上涨” |
| 仓位大小是否计算合理 | 使用凯利公式或固定比例确定 | “我打算投入5000美元” |
| 是否设置了止损点 | 根据价格或逻辑触发 | 无退出计划 |
| 是否监控投资组合风险 | 总风险低于15% | 总风险未知 |
| 资产相关性是否检查 | 无超过40%的相关性 | 所有资产都属于同一领域 |
| 是否制定了再平衡计划 | 每月或根据阈值自动调整 | 从未进行过再平衡 |
| 是否考虑了税收影响 | 知道如何处理亏损和税收优惠 | 交易时未考虑税收因素 |
| 是否跟踪投资表现 | 与长期持有策略对比 | “我认为自己赚到了钱” |

得分：/8。低于5分，请在建立新仓位前先改进基本条件。

---

## 第一阶段：投资逻辑的制定

每个投资决策都基于明确的逻辑。没有逻辑，就没有交易。

### 投资逻辑简要模板

```yaml
thesis:
  ticker: "AAPL"
  asset_class: "equity"  # equity | crypto | etf | bond | commodity | real_estate
  date: "2026-02-22"
  
  # THE EDGE — why does this opportunity exist?
  edge:
    type: "mispricing"  # mispricing | catalyst | trend | mean_reversion | structural
    description: "Market pricing in worst-case regulation; actual impact is 5-10% revenue, not 30%"
    why_others_miss_it: "Headline risk scaring generalists; specialists still buying"
    
  # THESIS STATEMENT (one sentence)
  thesis_statement: "AAPL is undervalued by 20% due to regulatory FUD; earnings growth will re-rate within 2 quarters"
  
  # TIMEFRAME
  timeframe:
    horizon: "3-6 months"
    catalyst_date: "2026-04-15"  # earnings, FDA, macro event
    catalyst_type: "earnings_beat"
    
  # BULL / BASE / BEAR
  scenarios:
    bull:
      probability: 30
      target_price: 245
      thesis: "Regulation light + Services acceleration"
    base:
      probability: 50
      target_price: 215
      thesis: "Regulation moderate, priced in by Q3"
    bear:
      probability: 20
      target_price: 165
      thesis: "Full regulatory impact + macro downturn"
      
  # EXPECTED VALUE
  # EV = (P_bull × R_bull) + (P_base × R_base) + (P_bear × R_bear)
  current_price: 190
  expected_value: 213.5  # (0.3×245 + 0.5×215 + 0.2×165)
  ev_vs_current: "+12.4%"
  
  # INVALIDATION — when you're WRONG
  invalidation:
    price_stop: 175  # -7.9% from entry
    thesis_stop: "Revenue decline >10% YoY in any segment"
    time_stop: "No catalyst by 2026-07-01"
    
  # CONVICTION (1-5)
  conviction: 4
  conviction_factors:
    - "3 independent data sources confirm undervaluation"
    - "Insider buying last 90 days"
    - "Valuation below 5Y average on EV/EBITDA"
```

### 投资优势类型框架

| 投资优势类型 | 描述 | 验证方法 | 有效期 |
|-----------|-------------|-------------------|------------|
| 价格错估 | 市场对基本面的判断错误 | 基本面分析 + 模型验证 | 长期有效（数月） |
| 事件驱动 | 预计即将发生的事件 | 日历 + 概率分析 | 短期有效（事件触发） |
| 趋势跟随 | 市场趋势 + 价格走势 | 技术分析 | 中期有效（数周） |
| 均值回归 | 市场偏离正常范围 | Z分数 + 历史数据 | 中期有效 |
| 结构性机会 | 市场结构带来的机会 | 流量分析 | 长期有效 |

### 投资逻辑质量检查清单

- [ ] 投资逻辑表述清晰（而不仅仅是“价格便宜” |
- [ ] 多种投资策略（牛市/熊市）的概率之和为100% |
- [ ] 预期收益高于当前价格 |
- [ ] 至少有两个独立的数据来源 |
- [ ] 有明确的验证标准（价格 + 投资逻辑 + 时间） |
- [ ] 时间框架符合投资优势的特点 |
- [ ] 不是简单复制市场共识 |

---

## 第二阶段：基本面分析

### 股票分析框架

#### 估值指标（收集所有指标，并按行业加权）

```yaml
valuation:
  # Price Multiples
  pe_ratio: null          # Price / Earnings (TTM)
  forward_pe: null        # Price / Forward Earnings
  peg_ratio: null         # PE / Earnings Growth Rate
  ps_ratio: null          # Price / Sales
  pb_ratio: null          # Price / Book
  ev_ebitda: null         # Enterprise Value / EBITDA
  ev_revenue: null        # Enterprise Value / Revenue
  fcf_yield: null         # Free Cash Flow / Market Cap
  
  # Compare to:
  sector_median: null
  historical_5y_avg: null
  historical_range: [null, null]  # [low, high]
  
  # Verdict
  valuation_score: null   # 1-10 (1=very expensive, 10=very cheap)
  relative_to_sector: null  # premium | inline | discount
```

#### 财务健康状况评估表

| 指标 | 健康标准 | 警告标准 | 危险标准 |
|--------|---------|---------|---------|
| 盈利能力 | 毛利率 | >50% | 30-50% | <30% |
| 盈利能力 | 净利润率 | >15% | 5-15% | <5% |
| 盈利能力 | 净资产回报率 | >15% | 8-15% | <8% |
| 盈利能力 | 现金流量回报率 | >12% | 6-12% | <6% |
| 增长性 | 收入同比增长 | >15% | 5-15% | <5% |
| 增长性 | 每股收益同比增长 | >10% | 0-10% | 负增长 |
| 增长性 | 现金流量增长率 | >10% | 0-10% | 负增长 |
| 杠杆率 | 负债/股本 | <0.5 | 0.5-1.5 | >1.5 |
| 杠杆率 | 利息保障倍数 | >8倍 | 3-8倍 | <3倍 |
| 杠杆率 | 净债务/息税折旧摊销前利润 | <2倍 | 2-4倍 | >4倍 |
| 流动性 | 流动比率 | >1.5 | 1-1.5 | <1 |
| 流动性 | 速动比率 | >1.0 | 0.5-1 | <0.5 |
| 效率 | 资产周转率 | >0.8 | 0.4-0.8 | <0.4 |
| 效率 | 库存周转天数 | <60天 | 60-120天 | >120天 |
| 质量 | 现金流量/净利润 | >80% | 50-80% | <50% |
| 质量 | 应计账款比率 | <5% | 5-10% | >10% |

每个指标的得分范围为1-3分。总分超过36分表示投资逻辑较强；低于24分则应避免投资。

#### 垒护分析（0-25分）

| 垒护来源 | 得分 | 需要的证据 |
|--------|---------|-------------------|
| 网络效应 | | 用户使用该产品能增加其他用户的价值 |
| 转换成本 | | 用户难以更换产品（数据锁定、集成问题） |
| 成本优势 | | 相比竞争对手具有结构性成本优势 |
| 无形资产 | | 拥有品牌、专利或监管许可 |
| 规模经济 | | 市场仅支持少数竞争者 |

得分：/25。超过15分表示具有较强竞争力；8-15分表示竞争力一般；低于8分表示没有明显优势。

### 加密货币分析框架

```yaml
crypto_analysis:
  # Network Fundamentals
  network:
    daily_active_addresses: null
    transaction_volume_24h: null
    hash_rate_trend: null        # BTC/PoW
    staking_ratio: null          # PoS chains
    developer_activity: null     # GitHub commits 90d
    tvl: null                    # DeFi protocols
    tvl_trend_30d: null
    
  # Tokenomics
  tokenomics:
    supply_schedule: null        # inflationary | deflationary | fixed
    circulating_vs_total: null   # % circulating
    unlock_schedule: null        # upcoming unlocks
    concentration: null          # top 10 holders %
    
  # On-Chain Signals
  on_chain:
    exchange_reserves_trend: null  # decreasing = bullish
    whale_accumulation: null       # large wallet changes
    realized_profit_loss: null     # NUPL
    mvrv_ratio: null               # Market Value / Realized Value
    
  # Market Structure
  market:
    funding_rate: null           # perpetuals funding
    open_interest_trend: null
    spot_vs_derivatives_volume: null
    correlation_to_btc: null
    correlation_to_sp500: null
```

### 加密货币估值方法

| 估值方法 | 适用对象 | 公式 |
|--------|----------|---------|
| 股票市值与流量比率 | BTC | 价格 = 0.4 × 日交易量^3（实际数据验证） |
| NVT比率 | 主流加密货币 | 网络价值 / 日交易量 |
| TVL比率 | DeFi项目 | 市值 / 日交易量（低于1表示被低估） |
| 费用收入倍数 | 产生收入的加密货币 | 年化费用 |

---

## 第三阶段：技术分析

### 价格走势分析框架

```yaml
technical_analysis:
  ticker: "BTC-USD"
  timeframe: "daily"
  date: "2026-02-22"
  
  # TREND
  trend:
    primary: "uptrend"    # uptrend | downtrend | range
    higher_highs: true
    higher_lows: true
    above_200ma: true
    above_50ma: true
    ma_alignment: "bullish"  # 20 > 50 > 200 = bullish
    
  # KEY LEVELS
  levels:
    resistance: [105000, 110000, 120000]
    support: [95000, 88000, 80000]
    current_price: 98500
    distance_to_resistance: "+6.6%"
    distance_to_support: "-3.6%"
    
  # MOMENTUM
  momentum:
    rsi_14: 58           # <30 oversold, >70 overbought
    rsi_divergence: null # bullish_div | bearish_div | none
    macd_signal: "bullish"  # bullish | bearish | neutral
    macd_histogram_trend: "increasing"
    
  # VOLUME
  volume:
    vs_20d_avg: "+15%"
    trend: "increasing_on_up_days"  # confirms trend
    
  # PATTERN
  pattern:
    current: "ascending_triangle"
    reliability: "high"
    target: 112000
    invalidation: 93000
```

### 信号评分矩阵

| 因素 | 买信号（+） | 中性（0） | 卖信号（-） |
|--------|-------------|-------------|-------------|
| 趋势 | 200日均线以上，价格创新高 | 横盘整理 | 200日均线以下，价格创新低 |
| 动量 | 相对强弱指数（RSI）40-60且上升，MACD金叉 | 相对强弱指数（RSI）45-55且平盘 | 相对强弱指数（RSI）>75或下降 |
| 交易量 | 上涨时交易量增加 | 平均交易量 | 下跌时交易量增加 |
| 支撑/阻力 | 接近强支撑位 | 中等支撑位 | 接近强阻力位 |
| 形态 | 价格走势符合技术形态 | 无明显技术形态 | 价格走势相反 |

得分范围：-9至+9。得分高于+5表示强烈的买入信号；低于-5表示强烈的卖出信号。

---

## 第四阶段：仓位大小与风险管理

### 仓位大小规则（强制要求）

```yaml
risk_rules:
  # Per-Trade Risk
  max_risk_per_trade: 2%       # of total equity
  max_risk_aggressive: 3%      # only with 5/5 conviction
  
  # Portfolio Heat
  max_portfolio_heat: 15%      # total risk across all positions
  max_correlated_exposure: 25% # in correlated assets
  max_single_position: 10%     # of total equity
  
  # Position Size Formula
  # Position Size = (Account × Risk%) / (Entry - Stop Loss)
  # Example: ($100K × 2%) / ($190 - $175) = $2,000 / $15 = 133 shares
  
  # Kelly Criterion (optional, aggressive)
  # f* = (bp - q) / b
  # b = win/loss ratio, p = win probability, q = 1-p
  # ALWAYS use Half-Kelly or Quarter-Kelly (full Kelly = too aggressive)
```

### 仓位大小计算器

```
Account Equity:     $___________
Risk Per Trade:     ___% (max 2%)
Dollar Risk:        $___________  (equity × risk%)
Entry Price:        $___________
Stop Loss Price:    $___________
Risk Per Share:     $___________  (entry - stop)
Position Size:      ___________ shares (dollar risk / risk per share)
Position Value:     $___________  (shares × entry)
Portfolio Weight:   ___%          (position value / equity)

CHECK: Portfolio weight < 10%?  ☐ Yes ☐ No (reduce if no)
CHECK: Portfolio heat < 15%?    ☐ Yes ☐ No (reduce if no)
CHECK: Correlated exposure ok?  ☐ Yes ☐ No (reduce if no)
```

### 止损决策树

```
Is this a TREND trade?
├── YES → Trailing stop below swing low (ATR-based: 2× ATR)
│         Initial stop: Below last higher low
│         Trail: Move stop to below each new higher low
│
└── NO → Is this a CATALYST trade?
    ├── YES → Time-based + price stop
    │         Price: Below pre-catalyst support
    │         Time: Close if no move within 2 days post-catalyst
    │
    └── Is this a VALUE trade?
        ├── YES → Thesis invalidation stop
        │         Price: Below bear case scenario price
        │         Thesis: Close if fundamental thesis breaks
        │         Time: Close if no re-rating in stated timeframe
        │
        └── MEAN REVERSION → Tight stop
            Price: If moves further from mean (wider Z-score)
            Target: Mean / fair value level
```

### 风险管理原则

1. **没有计划就不要追加亏损** —— 追加亏损会导致账户亏损。只有在以下情况下才能追加仓位：投资逻辑仍然成立、价格达到预定水平且总仓位仍在风险范围内。
2. **迅速止损，让盈利部分继续增长** —— 目标是实现1:3的风险/回报比。
3. **禁止报复性交易** —— 亏损后等待24小时再交易。
4. **每日亏损限制** —— 账户回撤超过3%时停止当日交易。
5. **每周亏损限制** —— 每周回撤超过5%时减少仓位大小50%。
6. **每月亏损限制** —— 每月回撤超过10%时将全部资产转换为现金，并重新评估投资组合。
7. **相关性检查** —— 在建立新仓位前检查新资产与现有资产的相关性。
8. **黑天鹅事件** —— 如果任何资产在24小时内价格波动超过15%，立即重新评估所有仓位。

---

## 第五阶段：投资组合构建

### 资产配置框架

```yaml
portfolio:
  name: "Growth + Income"
  target_allocation:
    # Core (60-70% — low turnover)
    core:
      us_large_cap: 25%      # S&P 500 / quality growth
      international: 10%      # Developed markets
      fixed_income: 15%       # Bonds / treasuries
      bitcoin: 10%            # Digital gold thesis
      real_estate: 5%         # REITs
      
    # Satellite (20-30% — active management)
    satellite:
      growth_stocks: 15%      # Individual stock picks
      crypto_alts: 5%         # L1s, DeFi
      thematic: 5%            # AI, clean energy, etc.
      
    # Cash (5-15%)
    cash: 10%                 # Dry powder for opportunities
    
  # Rebalance Rules
  rebalance:
    method: "threshold"       # calendar | threshold | hybrid
    threshold: 5%             # Rebalance when drift >5% from target
    calendar_check: "monthly" # Review allocations monthly
    tax_aware: true           # Use new contributions to rebalance first
```

### 根据风险偏好配置投资组合

| 风险偏好 | 股票 | 债券 | 加密货币 | 其他资产 | 现金 | 预期回报 | 最大回撤 |
|---------|--------|-------|--------|------|------|----------------|--------------|
| 保守型 | 30% | 40% | 5% | 10% | 15% | 6-8% | -15% |
| 平衡型 | 50% | 20% | 10% | 10% | 10% | 8-12% | -25% |
| 成长型 | 60% | 10% | 15% | 10% | 5% | 12-18% | -35% |
| 进攻型 | 50% | 0% | 30% | 15% | 5% | 15-25% | -50% |
| 防守型 | 20% | 0% | 50% | 25% | 5% | 20-40% | -70% |

### 相关性矩阵模板

跟踪投资组合内资产之间的相关性。目标是不让任何两个资产的相关性超过20%，且总权重之和不超过20%。

```
         SPY    BTC    ETH    AAPL   MSFT   GLD    TLT
SPY      1.00
BTC      0.35   1.00
ETH      0.30   0.85   1.00
AAPL     0.82   0.25   0.20   1.00
MSFT     0.85   0.28   0.22   0.78   1.00
GLD     -0.10  -0.05  -0.08  -0.12  -0.10   1.00
TLT     -0.35  -0.15  -0.12  -0.30  -0.32   0.40   1.00
```

---

## 第六阶段：交易执行

### 交易记录模板

```yaml
trade:
  id: "T-2026-042"
  date_opened: "2026-02-22"
  date_closed: null
  
  # WHAT
  ticker: "BTC-USD"
  direction: "long"
  asset_class: "crypto"
  
  # SIZING
  entry_price: 98500
  position_size: 0.15  # BTC
  position_value: 14775
  portfolio_weight: "8.2%"
  
  # RISK
  stop_loss: 93000
  risk_amount: 825   # (98500-93000) × 0.15
  risk_percent: "0.82%"  # of portfolio
  
  # TARGETS
  target_1: 105000   # 50% of position
  target_2: 115000   # 30% of position
  target_3: 130000   # 20% of position (runner)
  risk_reward: "1:3.8"  # avg target vs risk
  
  # THESIS
  thesis: "BTC consolidating above 200MA, halving supply reduction, ETF inflows accelerating"
  edge_type: "trend + structural"
  conviction: 4
  
  # EXECUTION
  entry_type: "limit"  # market | limit | scaled
  scale_plan: null     # or: [{"price": 97000, "size": "50%"}, {"price": 95000, "size": "50%"}]
  
  # RESULT (fill on close)
  exit_price: null
  exit_reason: null    # target_hit | stop_hit | thesis_invalidated | time_stop | manual
  pnl_dollar: null
  pnl_percent: null
  r_multiple: null     # PnL / initial risk
  
  # REVIEW
  followed_plan: null  # yes | partially | no
  lessons: null
  mistakes: null
  grade: null          # A-F
```

### 交易前检查清单

- [ ] 投资逻辑明确记录，包括验证依据和时间框架 |
- [ ] 仓位大小计算合理（风险不超过2%，投资组合总权重的10%） |
- [ ] 设置了止损点（基于价格、投资逻辑和时间） |
- [ ] 设定了至少两个盈利目标 |
- [ ] 风险/回报比≥1:2（理想为1:3以上） |
- [ ] 投资组合风险低于15% |
- [ ] 检查相关性，避免过度集中投资 |
- [ ] 交易决策不受情绪影响（避免报复性交易、害怕错过机会或盲目跟风） |
- [ ] 已确认市场环境（无突发事件） |
- [ ] 确定了入场方式（市场价、限价单或分批入场）

### 订单类型选择

| 交易情况 | 选择订单类型 | 原因 |
|--------|-----------|-----|
| 确信度很高，希望立即买入 | 市场价 | 快速成交 |
| 交易条件良好，但不紧急 | 在支撑位设置限价单 | 更好的入场时机 |
| 确信度很高，希望分批买入 | 分批设置限价单 | 降低交易风险 |
| 突破行情 | 在阻力位以上设置止损限价单 | 确认突破后再入场 |
| 事件驱动的交易 | 在事件发生前设置限价单 | 在事件发生前建立仓位 |

---

## 第七阶段：投资组合表现跟踪

### 日报

```yaml
daily_dashboard:
  date: "2026-02-22"
  
  # PORTFOLIO SNAPSHOT
  portfolio:
    total_equity: null
    daily_pnl: null
    daily_pnl_percent: null
    weekly_pnl: null
    monthly_pnl: null
    ytd_pnl: null
    
  # POSITIONS
  open_positions: 0
  portfolio_heat: "0%"  # sum of all position risks
  cash_percent: "100%"
  
  # BENCHMARK
  benchmark:
    sp500_ytd: null
    btc_ytd: null
    portfolio_vs_sp500: null
    portfolio_vs_btc: null
    
  # ACTIVITY
  trades_today: 0
  alerts_triggered: []
```

### 表现指标（每周跟踪）

| 指标 | 计算公式 | 目标值 |
|--------|---------|--------|
| 胜率 | 胜利交易数 / 总交易数 | >50% |
| 平均收益 | 所有交易的平均收益倍数 | >1.5 |
| 盈利因子 | 总利润 / 总损失 | >2.0 |
| 期望值 | （胜率 × 平均收益） - （亏损率 × 平均损失） | 正值 |
| 最大回撤 | 从最高点到最低点的跌幅 | <15% |
 | 夏普比率 | （收益 - 无风险利率） / 标准差 | >1.5 |
| 萨尔蒂诺比率 | （收益 - 无风险利率） / 下跌幅度 | >2.0 |
| 卡尔马比率 | 年化收益 / 最大回撤 | >1.0 |

### 月度评估模板

```yaml
monthly_review:
  month: "2026-02"
  
  # PERFORMANCE
  portfolio_return: null
  benchmark_return: null  # vs S&P 500
  alpha: null             # portfolio - benchmark
  
  # TRADING STATS
  total_trades: 0
  winning_trades: 0
  losing_trades: 0
  win_rate: null
  average_winner: null
  average_loser: null
  largest_winner: null
  largest_loser: null
  profit_factor: null
  
  # RISK STATS
  max_drawdown: null
  avg_portfolio_heat: null
  risk_rule_violations: 0
  
  # BEHAVIOR ANALYSIS
  followed_plan_rate: null    # % of trades that followed the plan
  emotional_trades: 0          # trades driven by FOMO/revenge/boredom
  early_exits: 0               # cut winners short
  late_exits: 0                # held losers too long
  
  # TOP 3 LESSONS
  lessons:
    - null
    - null
    - null
    
  # ADJUSTMENTS FOR NEXT MONTH
  adjustments:
    - null
```

---

## 第八阶段：市场环境识别

### 市场环境框架

| 市场环境 | 特征 | 对应策略 | 仓位大小 |
|--------|----------------|----------|---------------|
| 牛市 | 200日均线上升，市场宽度大于60%，VIX指数低于20 | 跟随趋势，逢低买入 | 全额持仓 |
| 熊市 | 200日均线下降，市场宽度小于40%，VIX指数高于30 | 卖空或减少持仓 | 减少持仓 |
| 横盘/震荡市 | 200日均线持平，市场宽度在40-60%之间 | 均值回归策略，卖出高估值资产 | 减少持仓 |
| 高波动市 | VIX指数高于35%，市场波动剧烈 | 减少持仓或进行对冲 | 最小化持仓 |
| 欣喜市 | VIX指数低于12%，市场情绪极度乐观 | 收益最大化，适当对冲 | 逐步增加持仓 |
| 恐慌市 | VIX指数高于50%，市场出现恐慌 | 积累优质资产 | 逐步增加持仓 |

### 宏观经济指标（每周检查）

- [ ] 美联储利率及下一次会议安排 |
- [ ] 美国10年期国债收益率趋势 |
- [ ] 美元汇率（DXY）走势 |
- [ ] VIX指数水平 |
- [ ] 利率差（收窄/扩大） |
- [ ] 收益率曲线（倒挂/平坦/陡峭） |
- [ | 领先指标（改善/恶化） |
- [ | 全球流动性趋势（扩张/收缩） |
- [ | 行业轮动（风险偏好变化） |
- [ | 加密货币市场市值趋势 |

### 情绪指标

| 指标 | 极度恐惧（买入信号） | 中性 | 极度贪婪（卖出信号） |
|--------|-------------------|---------|---------------------|
| CNN恐惧与贪婪指数 | <20 | 40-60 | >80 |
| AAII牛熊指数 | >-30% | ±10% | >+30% |
| 看跌/看涨期权比率 | >1.2 | 0.7-0.9 | <0.5 |
| VIX期限结构 | 向后溢价 | 平价 | 倒向溢价 |
| 加密货币恐惧与贪婪指数 | <15 | 40-60 | >85 |
| BTC融资利率 | 非常低 | 中性 | >0.05 |

---

## 第九阶段：股息与收益分析

### 股息质量评分（0-100）

| 评分因素 | 权重 | 得分 |
|--------|--------|---------|
| 盈利率与行业平均水平 | 15 | 高于行业平均水平得15分，低于则按比例扣分 |
| 分红率 | 20 | 低于50%得20分，50-75%得15分，75-100%得15分，高于100%得0分 |
| 五年复合增长率 | 20 | 高于10%得20分，5-10%得15分，低于5%得10分 |
| 连续分红年份 | 15 | 连续五年以上得15分，否则得0分 |
| 现金流量覆盖率 | 15 | 现金流量/股息大于1.5得15分，1-1.5得10分，小于1得0分 |

得分：/100。得分高于75分表示是优质股息投资对象。低于40分表示股息收益存在风险。

### 收益投资组合构建

- **核心收益**（60%）：高股息股票、优质房地产投资信托（REITs） |
- **成长型收益**（25%）：高股息成长型股票 |
- **高收益**（15%）：高风险、高收益的债券或衍生品 |

---

## 第十阶段：税收优化

### 税收损失收割规则

1. **收割条件**：资产价格较买入成本下跌超过10%，且持有时间少于12个月。
2. **操作方法**：卖出资产后，立即买入相关性资产（但不得完全相同）。
3. **税务规则**：30天内不得回购同一资产。
4. **替换示例**：例如将SPY换成VOO，AAPL换成QQQ，BTC现货换成BTC期货ETF。
5. **跟踪记录**：累计损失可用于抵扣税收，同时可享受3000美元的税收减免。

### 持有期限优化

| 持有期限 | 美国税率 | 税收策略 |
|----------------|--------------|----------|
| <1年 | 普通税收（最高37%） | 仅适用于短期交易 |
| >1年 | 长期持有（0%/15%/20%） | 根据情况选择 |
| >5年 | 高税收优惠区域（QOZ） | 适用特定税收政策 |

### 税收效率账户配置

| 账户类型 | 适用情况 | 优势 |
|-------------|----------|-----|
| 应纳税账户 | 长期持有，适用资本利得税 | |
| 传统IRA/401(k)账户 | 债券、REITs等高股息资产 | 适用税收优惠 |
| Roth IRA账户 | 高成长型资产 | 享受免税优惠 |

---

## 第十一阶段：筛选与投资思路生成

### 股票筛选标准

**价值筛选**：
- 市盈率（P/E）低于行业平均水平 |
- 市净率（P/B）低于1.5 |
- 杠杆率（债务/股本）低于0.5 |
- 净资产回报率（ROE）高于12% |
- 连续五年现金流为正 |

**成长筛选**：
- 收入同比增长超过20% |
- 每股收益同比增长超过15% |
- 毛利率高于50% |
- 客户留存率高于110%（SaaS企业） |
- 年收入超过100亿美元 |

**股息筛选**：
- 股息率高于3% |
- 分红率低于60% |
- 分红增长率连续五年超过5% |
- 债务/息税折旧摊销前利润（DEBT/EBITDA）低于3%

**加密货币筛选**：
- 市值超过10亿美元 |
- 日交易量超过5000万美元 |
- 有活跃的开发团队（GitHub代码提交记录） |
- 不被前十大钱包持有超过90% |

### 研究资源（无需API）

| 来源 | 链接 | 适用范围 |
|--------|-----|----------|
| Yahoo Finance | finance.yahoo.com | 基本面数据、股票报价 |
| Finviz | finviz.com | 筛选工具、市场热度图 |
| Macrotrends | macrotrends.net | 历史财务数据 |
| CoinGecko | coingecko.com | 加密货币数据 |
| DeFiLlama | defillama.com | DeFi项目的数据和收益 |
| FRED | fred.stlouisfed.org | 宏观经济数据 |
| TradingView | tradingview.com | 图表和分析工具 |
| SEC EDGAR | sec.gov/edgar | 相关文件、内幕交易信息 |
| Glassnode | glassnode.com | 区块链数据 |

---

## 第十二阶段：高级策略

### 期权基础（用于对冲）

| 策略 | 适用情况 | 风险 | 收益 |
|----------|------|------|--------|
| 保护性看跌期权 | 持有股票，希望降低下跌风险 | 需支付期权费用 | 上限收益有限，但下行风险可控 |
| 对冲型看涨期权 | 持有股票，希望限制价格上涨 | 上限收益有上限，但需支付期权费用 |
| 现金担保看跌期权 | 希望以较低价格买入股票 | 需在指定价格买入期权 |
| 头寸对冲 | 希望同时限制价格上涨和下跌的风险 | 需支付期权费用 |

### 定期定额投资（DCA）框架

```yaml
dca_plan:
  asset: "BTC"
  frequency: "weekly"           # daily | weekly | biweekly | monthly
  amount: 250                   # per purchase
  day: "Monday"                 # specific day
  duration: "indefinite"        # or end date
  
  # SMART DCA (optional — buy more when cheap)
  smart_dca:
    enabled: true
    base_amount: 250
    multiplier_rules:
      - condition: "price < 200MA"
        multiplier: 1.5          # buy 50% more
      - condition: "RSI < 30"
        multiplier: 2.0          # double buy
      - condition: "price > 200MA × 1.5"
        multiplier: 0.5          # buy less in euphoria
```

### 再平衡决策树

```
Is any allocation >5% from target?
├── NO → No action needed. Check again next month.
│
└── YES → Is it a tax-advantaged account?
    ├── YES → Rebalance by selling overweight, buying underweight
    │
    └── NO (taxable) → Can you rebalance with new contributions?
        ├── YES → Direct new money to underweight positions
        │
        └── NO → Are there tax losses to harvest?
            ├── YES → Sell losers (harvest), redirect to underweight
            │
            └── NO → Is the drift >10%?
                ├── YES → Rebalance (accept tax hit for risk control)
                └── NO → Wait for next contribution or year-end
```

---

## 投资者心理规则

### 十种影响投资回报的认知偏差

| 偏差 | 陷阱 | 应对策略 |
|------|------|---------|
| 损失厌恶 | 持有亏损资产，不愿卖出盈利资产 | 设置止损点，机械执行交易 |
| 证实偏差 | 只关注支持投资逻辑的数据 | 主动寻找反驳证据 |
| 最新偏见 | 根据近期表现做出决策 | 查看长期数据（至少10年） |
| 锚定偏差 | 固定买入价格 | 关注当前价值，而非市场整体 |
| 怕错过机会（FOMO） | 追随市场趋势 | 坚持使用筛选标准 |
| 过度自信 | 在盈利后增加持仓 | 严格执行仓位大小规则 |
| 处置效应 | 过早卖出盈利资产 | 设置止损点，让盈利资产继续增长 |
| 群体行为 | 跟随大众买卖 | 采用反向投资策略 |
| 沉没成本偏差 | “已经持有很久，不能卖出” | 重新评估投资逻辑是否合理 |

### 交易心理检查清单（每日）

- [ ] 我是否保持冷静？（无愤怒、恐惧或过度兴奋） |
- [ ] 我是否按照计划交易？（不随意更改交易策略） |
- [ ] 我的交易是否在风险范围内？（检查投资组合风险） |
- [ ] 我是否进行了充分分析？（不根据直觉交易） |

---

## 质量评估（0-100）

| 评估维度 | 权重 | 评分标准 |
|--------|--------|----------|
| 投资逻辑质量 | 20分 | 投资逻辑清晰、有验证依据，时间框架合理 |
| 风险管理 | 25分 | 仓位大小合理，设置止损点，监控投资组合风险 |
| 分析深度 | 15分 | 充分考虑基本面、技术分析和宏观经济因素 |
| 执行能力 | 15分 | 严格执行入场和出场规则，选择合适的订单类型 |
| 记录保存 | 10分 | 保持交易记录，定期评估投资表现 |
| 心理素质 | 10分 | 控制情绪，意识到自身偏见，严格执行交易计划 |

得分：/100。得分高于80分表示投资流程专业且高效；低于50分表示投资决策缺乏专业性。

---

## 自然语言命令

| 命令 | 功能 |
|---------|--------|
| “分析[股票代码]” | 进行全面的基本面和技术分析 |
| “比较[股票代码1]和[股票代码2]” | 进行对比分析 |
| “为[股票代码]制定投资逻辑” | 生成投资逻辑模板 |
| “以[价格]买入[股票代码]” | 计算买入仓位大小并控制风险 |
| “检查投资组合健康状况” | 评估投资组合状况 |
| “进行月度评估” | 生成投资组合表现报告 |
| “筛选[价值/成长/股息/加密货币]资产” | 应用相应的筛选标准 |
| “当前市场环境如何？” | 评估市场环境 |
| “寻找税收优化机会” | 识别适合收割税收损失的资产 |
| “制定[资产]的定期定额投资计划” | 生成定期定额投资计划 |
| “分析[股票代码]的股息情况” | 进行股息质量评估 |
| “生成风险报告” | 提供投资组合风险和相关性分析 |

---

*由AfrexAI开发——将市场噪音转化为投资信号。* 🖤💛