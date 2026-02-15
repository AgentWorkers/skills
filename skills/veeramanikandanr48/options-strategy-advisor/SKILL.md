---
name: options-strategy-advisor
description: 期权交易策略分析与模拟工具。该工具利用Black-Scholes模型提供理论定价，支持希腊字母（Greeks）的计算，能够模拟交易策略的盈亏情况，并提供风险管理建议。适用于用户需要分析期权交易策略、执行保护性看涨期权（covered calls）、保护性看跌期权（protective puts）、期权组合（spreads）、铁秃鹫期权（iron condors）、基于公司收益的期权交易策略（earnings plays）或进行期权风险管理的情况。工具涵盖波动率分析、头寸规模调整以及基于公司收益的策略推荐，同时注重教育性内容，并提供实际的交易模拟功能。
---

# 期权策略顾问

## 概述

该技能利用理论定价模型提供全面的期权策略分析和教育服务，帮助交易者理解、分析并模拟期权策略，而无需订阅实时市场数据。

**核心功能：**
- **布莱克-斯科尔斯定价模型**：计算理论期权价格及希腊值（Greeks）
- **策略模拟**：分析主要期权策略的盈亏情况
- **收益策略**：结合收益日历预测收益前的波动性
- **风险管理**：确定头寸规模、控制希腊值风险、分析最大盈亏
- **教育重点**：详细解释策略及风险指标

**数据来源：**
- FMP API：股票价格、历史波动性、股息、收益日期
- 用户输入：隐含波动率（IV）、无风险利率
- 理论模型：用于定价的布莱克-斯科尔斯模型及希腊值计算

## 适用场景

当用户有以下需求时，可使用该技能：
- 询问期权策略（例如：“什么是覆盖式看涨期权？”、“铁秃鹰策略是如何运作的？”）
- 想模拟策略的盈亏情况（例如：“我在MSFT的100美元/105美元看涨期权组合中的最大利润是多少？”）
- 需要分析希腊值（例如：“我的Delta风险是多少？”）
- 询问收益策略（例如：“在收益公布前应该买入跨式期权吗？”）
- 需要头寸规模建议（例如：“我应该交易多少份合约？”）
- 询问波动性情况（例如：“当前的隐含波动率高吗？”

**示例请求：**
- “分析AAPL的覆盖式看涨期权”
- “MSFT的100美元/105美元看涨期权组合的盈亏情况是多少？”
- “在NVDA收益公布前应该买入跨式期权吗？”
- “计算我的铁秃鹰策略的希腊值”
- “比较保护性看跌期权和覆盖式看涨期权在下行风险保护方面的优势”

## 支持的期权策略

### 收益策略
1. **覆盖式看涨期权**：持有股票并卖出看涨期权（产生收入，限制上行风险）
2. **现金担保看跌期权**：用现金购买看跌期权（收取期权费，有意愿买入股票）
3. **低成本覆盖式看涨期权**：买入长期看涨期权（LEAPS）并卖出短期看涨期权（资本效率较高）

### 保护策略
4. **保护性看跌期权**：持有股票并买入看跌期权（提供保险，限制下行风险）
5. **领口策略**：持有股票并卖出看涨期权的同时买入看跌期权（同时限制上行和下行风险）

### 方向性策略
6. **看涨期权组合**：买入低执行价格的看涨期权并卖出高执行价格的看涨期权（多头策略，风险有限）
7. **看涨期权差价**：卖出高执行价格的看跌期权并买入低执行价格的看跌期权（多头策略，获得信用收益）
8. **看跌期权组合**：卖出低执行价格的看跌期权并买入高执行价格的看跌期权（多头策略，获得信用收益）
9. **看跌期权差价**：买入高执行价格的看跌期权并卖出低执行价格的看跌期权（多头策略，风险有限）

### 波动性策略
10. **长跨式期权**：买入平价看涨期权和平价看跌期权（无论价格涨跌都有收益）
11. **长挤压期权**：买入虚值看涨期权和平价看跌期权（比长跨式期权成本更低，但需要更大的价格波动）
12. **短跨式期权**：卖出平价看涨期权和平价看跌期权（在价格无波动时获利，但风险无限）
13. **短挤压期权**：卖出虚值看涨期权和平价看跌期权（在价格无波动时获利，但需要更大的价格波动范围）

### 区间限制策略
14. **铁秃鹰策略**：卖出看涨期权差价并买入看跌期权差价（从价格区间波动中获利）
15. **铁蝴蝶策略**：卖出平价看涨期权组合并买入虚值看涨期权组合（从价格区间紧密时获利）

### 高级策略
16. **日历差价**：卖出短期期权并买入长期期权（从时间衰减中获利）
17. **对角差价**：使用不同执行价格的日历差价（结合方向性和时间衰减）
18. **比率差价**：在某一腿上使用更多合约的不对称差价

## 分析流程

### 第一步：收集输入数据

**用户需要提供的信息：**
- 股票代码
- 策略类型
- 执行价格
- 到期日期
- 头寸规模（合约数量）

**用户可选提供的信息：**
- 隐含波动率（IV）：如果未提供，则使用历史波动率
- 无风险利率：默认为当前3个月国债利率（截至2025年为约5.3%）

**从FMP API获取的数据：**
- 当前股票价格
- 历史价格（用于计算历史波动率）
- 股息收益率
- 即将到来的收益日期（用于收益策略分析）

**示例用户输入：**
```
Ticker: AAPL
Strategy: Bull Call Spread
Long Strike: $180
Short Strike: $185
Expiration: 30 days
Contracts: 10
IV: 25% (or use HV if not provided)
```

### 第二步：计算历史波动率（如果未提供隐含波动率）

**目标：**根据历史价格走势估算波动率。

**方法：**
```python
# Fetch 90 days of price data
prices = get_historical_prices("AAPL", days=90)

# Calculate daily returns
returns = np.log(prices / prices.shift(1))

# Annualized volatility
HV = returns.std() * np.sqrt(252)  # 252 trading days
```

**输出结果：**
- 历史波动率（年化百分比）
- 提示用户：“历史波动率为24.5%，建议使用当前市场隐含波动率以获得更准确的结果”

**用户可覆盖的信息：**
- 从经纪平台（如ThinkorSwim、TastyTrade等）获取隐含波动率
- 脚本支持`--iv 28.0`参数进行手动设置

### 第三步：使用布莱克-斯科尔斯模型定价期权

**布莱克-斯科尔斯模型：**

适用于欧式期权：
```
Call Price = S * N(d1) - K * e^(-r*T) * N(d2)
Put Price = K * e^(-r*T) * N(-d2) - S * N(-d1)

Where:
d1 = [ln(S/K) + (r + σ²/2) * T] / (σ * √T)
d2 = d1 - σ * √T

S = Current stock price
K = Strike price
r = Risk-free rate
T = Time to expiration (years)
σ = Volatility (IV or HV)
N() = Cumulative standard normal distribution
```

**调整因素：**
- 从股票价格中减去股息的现值（适用于看涨期权）
- 美式期权：使用近似值或注明“此模型适用于欧式期权，可能低估美式期权的价格”

**Python实现代码：**
```python
from scipy.stats import norm
import numpy as np

def black_scholes_call(S, K, T, r, sigma, q=0):
    """
    S: Stock price
    K: Strike price
    T: Time to expiration (years)
    r: Risk-free rate
    sigma: Volatility
    q: Dividend yield
    """
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    call_price = S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    put_price = K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)
    return put_price
```

**每条期权腿的输出结果：**
- 理论价格
- 提示：“市场价格可能因买卖价差及美式期权与欧式期权的差异而有所不同”

### 第四步：计算希腊值

**希腊值**用于衡量期权价格对各种因素的敏感度：

**Delta（Δ）**：股票价格每变动1美元时期权价格的变化幅度
```python
def delta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.cdf(d1)

def delta_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * (norm.cdf(d1) - 1)
```

**Gamma（Γ）**：股票价格每变动1美元时Delta的变化幅度
```python
def gamma(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
```

**Theta（Θ）**：期权价格每天的变化幅度（时间衰减）
```python
def theta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    theta = (-S*norm.pdf(d1)*sigma*np.exp(-q*T)/(2*np.sqrt(T))
             - r*K*np.exp(-r*T)*norm.cdf(d2)
             + q*S*norm.cdf(d1)*np.exp(-q*T))

    return theta / 365  # Per day
```

**Vega（ν）**：波动率每变动1%时期权价格的变化幅度
```python
def vega(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S * np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T) / 100  # Per 1%
```

**Rho（ρ）**：利率每变动1%时期权价格的变化幅度
```python
def rho_call(S, K, T, r, sigma, q=0):
    d2 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T)) - sigma*np.sqrt(T)
    return K * T * np.exp(-r*T) * norm.cdf(d2) / 100  # Per 1%
```

**组合头寸的希腊值：**

对于包含多条腿的策略，将所有腿的希腊值相加：
```python
# Example: Bull Call Spread
# Long 1x $180 call
# Short 1x $185 call

delta_position = (1 * delta_long) + (-1 * delta_short)
gamma_position = (1 * gamma_long) + (-1 * gamma_short)
theta_position = (1 * theta_long) + (-1 * theta_short)
vega_position = (1 * vega_long) + (-1 * vega_short)
```

**希腊值的解释：**

| 希腊值 | 含义 | 举例 |
|-------|---------|---------|
| Delta | 方向性风险 | Δ = 0.50 → 股票价格上涨1美元时获利50美元 |
| Gamma | Delta的变化率 | Γ = 0.05 → 股票价格上涨1美元时Delta增加0.05 |
| Theta | 时间衰减 | Θ = -5 → 随时间流逝每天损失5美元 |
| Vega | 波动率敏感度 | ν = 10 → 波动率增加1%时获利10美元 |
| Rho | 利率敏感度 | ρ = 2 → 利率上升1%时获利2美元 |

### 第五步：模拟策略盈亏

**目标：**计算到期时在不同股票价格下的盈亏情况。

**方法：**

生成股票价格范围（例如，当前价格的±30%）：
```python
current_price = 180
price_range = np.linspace(current_price * 0.7, current_price * 1.3, 100)
```

对于每个价格点，计算盈亏情况：
```python
def calculate_pnl(strategy, stock_price_at_expiration):
    pnl = 0

    for leg in strategy.legs:
        if leg.type == 'call':
            intrinsic_value = max(0, stock_price_at_expiration - leg.strike)
        else:  # put
            intrinsic_value = max(0, leg.strike - stock_price_at_expiration)

        if leg.position == 'long':
            pnl += (intrinsic_value - leg.premium_paid) * 100  # Per contract
        else:  # short
            pnl += (leg.premium_received - intrinsic_value) * 100

    return pnl * num_contracts
```

**关键指标：**
- **最大利润**：可能的最高盈亏
- **最大损失**：可能的最低盈亏
- **盈亏平衡点**：盈亏为0的股票价格
- **盈利概率**：盈利的价格区间占比（简化计算）

**示例输出：**
```
Bull Call Spread: $180/$185 on AAPL (30 DTE, 10 contracts)

Current Price: $180.00
Net Debit: $2.50 per spread ($2,500 total)

Max Profit: $2,500 (at $185+)
Max Loss: -$2,500 (at $180-)
Breakeven: $182.50
Risk/Reward: 1:1

Probability Profit: ~55% (if stock stays above $182.50)
```

### 第六步：生成盈亏图表（ASCII艺术形式）

**以ASCII艺术形式展示不同股票价格下的盈亏情况：**

```python
def generate_pnl_diagram(price_range, pnl_values, current_price, width=60, height=15):
    """Generate ASCII P/L diagram"""

    # Normalize to chart dimensions
    max_pnl = max(pnl_values)
    min_pnl = min(pnl_values)

    lines = []
    lines.append(f"\nP/L Diagram: {strategy_name}")
    lines.append("-" * width)

    # Y-axis levels
    levels = np.linspace(max_pnl, min_pnl, height)

    for level in levels:
        if abs(level) < (max_pnl - min_pnl) * 0.05:
            label = f"    0 |"  # Zero line
        else:
            label = f"{level:6.0f} |"

        row = label
        for i in range(width - len(label)):
            idx = int(i / (width - len(label)) * len(price_range))
            pnl = pnl_values[idx]
            price = price_range[idx]

            # Determine character
            if abs(pnl - level) < (max_pnl - min_pnl) / height:
                if pnl > 0:
                    char = '█'  # Profit
                elif pnl < 0:
                    char = '░'  # Loss
                else:
                    char = '─'  # Breakeven
            elif abs(level) < (max_pnl - min_pnl) * 0.05:
                char = '─'  # Zero line
            elif abs(price - current_price) < (price_range[-1] - price_range[0]) * 0.02:
                char = '│'  # Current price line
            else:
                char = ' '

            row += char

        lines.append(row)

    lines.append(" " * 6 + "|" + "-" * (width - 6))
    lines.append(" " * 6 + f"${price_range[0]:.0f}" + " " * (width - 20) + f"${price_range[-1]:.0f}")
    lines.append(" " * (width // 2 - 5) + "Stock Price")

    return "\n".join(lines)
```

**示例输出：**
```
P/L Diagram: Bull Call Spread $180/$185
------------------------------------------------------------
 +2500 |                               ████████████████████
       |                         ██████
       |                   ██████
       |             ██████
     0 |       ──────
       | ░░░░░░
       |░░░░░░
 -2500 |░░░░░
      |____________________________________________________________
       $126                  $180                   $234
                          Stock Price

Legend: █ Profit  ░ Loss  ── Breakeven  │ Current Price
```

### 第七步：针对特定策略提供指导

根据策略类型提供定制化的建议：

**覆盖式看涨期权：**
```
Income Strategy: Generate premium while capping upside

Setup:
- Own 100 shares of AAPL @ $180
- Sell 1x $185 call (30 DTE) for $3.50

Max Profit: $850 (Stock at $185+ = $5 stock gain + $3.50 premium)
Max Loss: Unlimited downside (stock ownership)
Breakeven: $176.50 (Cost basis - premium received)

Greeks:
- Delta: -0.30 (reduces stock delta from 1.00 to 0.70)
- Theta: +$8/day (time decay benefit)

Assignment Risk: If AAPL > $185 at expiration, shares called away

When to Use:
- Neutral to slightly bullish
- Want income in sideways market
- Willing to sell stock at $185

Exit Plan:
- Buy back call if stock rallies strongly (preserve upside)
- Let expire if stock stays below $185
- Roll to next month if want to keep shares
```

**保护性看跌期权：**
```
Insurance Strategy: Limit downside while keeping upside

Setup:
- Own 100 shares of AAPL @ $180
- Buy 1x $175 put (30 DTE) for $2.00

Max Profit: Unlimited (stock can rise infinitely)
Max Loss: -$7 per share = ($5 stock loss + $2 premium)
Breakeven: $182 (Cost basis + premium paid)

Greeks:
- Delta: +0.80 (stock delta 1.00 - put delta 0.20)
- Theta: -$6/day (time decay cost)

Protection: Guaranteed to sell at $175, no matter how far stock falls

When to Use:
- Own stock, worried about short-term drop
- Earnings coming up, want protection
- Alternative to stop-loss (can't be stopped out)

Cost: "Insurance premium" - typically 1-3% of stock value

Exit Plan:
- Let expire worthless if stock rises (cost of insurance)
- Exercise put if stock falls below $175
- Sell put if stock drops but want to keep shares
```

**铁秃鹰策略：**
```
Range-Bound Strategy: Profit from low volatility

Setup (example on AAPL @ $180):
- Sell $175 put for $1.50
- Buy $170 put for $0.50
- Sell $185 call for $1.50
- Buy $190 call for $0.50

Net Credit: $2.00 ($200 per iron condor)

Max Profit: $200 (if stock stays between $175-$185)
Max Loss: $300 (if stock moves outside $170-$190)
Breakevens: $173 and $187
Profit Range: $175 to $185 (58% probability)

Greeks:
- Delta: ~0 (market neutral)
- Theta: +$15/day (time decay benefit)
- Vega: -$25 (short volatility)

When to Use:
- Expect low volatility, range-bound movement
- After big move, think consolidation
- High IV environment (sell expensive options)

Risk: Unlimited if one side tested
- Use stop loss at 2x credit received (exit at -$400)

Adjustments:
- If tested on one side, roll that side out in time
- Close early at 50% max profit to reduce tail risk
```

### 第八步：收益策略分析

**与收益日历集成：**

当用户询问收益策略时，获取收益日期：
```python
from earnings_calendar import get_next_earnings_date

earnings_date = get_next_earnings_date("AAPL")
days_to_earnings = (earnings_date - today).days
```

**收益前的策略：**
- **长跨式/挤压期权组合**：
```
Setup (AAPL @ $180, earnings in 7 days):
- Buy $180 call for $5.00
- Buy $180 put for $4.50
- Total Cost: $9.50

Thesis: Expect big move (>5%) but unsure of direction

Breakevens: $170.50 and $189.50
Profit if: Stock moves >$9.50 in either direction

Greeks:
- Delta: ~0 (neutral)
- Vega: +$50 (long volatility)
- Theta: -$25/day (time decay hurts)

IV Crush Risk: ⚠️ CRITICAL
- Pre-earnings IV: 40% (elevated)
- Post-earnings IV: 25% (typical)
- IV drop: -15 points = -$750 loss even if stock doesn't move!

Analysis:
- Implied Move: √(DTE/365) × IV × Stock Price
  = √(7/365) × 0.40 × 180 = ±$10.50
- Breakeven Move Needed: ±$9.50
- Probability Profit: ~30-40% (implied move > breakeven move)

Recommendation:
✅ Consider if you expect >10% move (larger than implied)
❌ Avoid if expect normal ~5% earnings move (IV crush will hurt)

Alternative: Buy further OTM strikes to reduce cost
- $175/$185 strangle cost $4.00 (need >$8 move, but cheaper)
```

**短铁秃鹰策略：**
```
Setup (AAPL @ $180, earnings in 7 days):
- Sell $170/$175 put spread for $2.00
- Sell $185/$190 call spread for $2.00
- Net Credit: $4.00

Thesis: Expect stock to stay range-bound ($175-$185)

Profit Zone: $175 to $185
Max Profit: $400
Max Loss: $100

IV Crush Benefit: ✅
- Short high IV before earnings
- IV drops after earnings → profit on vega
- Even if stock moves slightly, IV drop helps

Greeks:
- Delta: ~0 (market neutral)
- Vega: -$40 (short volatility - good here!)
- Theta: +$20/day

Recommendation:
✅ Good if expect normal earnings reaction (<8% move)
✅ Benefit from IV crush regardless of direction
⚠️ Risk if stock gaps outside range (>10% move)

Exit Plan:
- Close next day if IV crushed (capture profit early)
- Use stop loss if one side tested (-2x credit)
```

### 第九步：风险管理指导

**头寸规模确定：**
```
Account Size: $50,000
Risk Tolerance: 2% per trade = $1,000 max risk

Iron Condor Example:
- Max loss per spread: $300
- Max contracts: $1,000 / $300 = 3 contracts
- Actual position: 3 iron condors

Bull Call Spread Example:
- Debit paid: $2.50 per spread
- Max contracts: $1,000 / $250 = 4 contracts
- Actual position: 4 spreads
```

**投资组合希腊值管理：**
```
Portfolio Guidelines:
- Delta: -10 to +10 (mostly neutral)
- Theta: Positive preferred (seller advantage)
- Vega: Monitor if >$500 (IV risk)

Current Portfolio:
- Delta: +5 (slightly bullish)
- Theta: +$150/day (collecting $150 daily)
- Vega: -$300 (short volatility)

Interpretation:
✅ Neutral delta (safe)
✅ Positive theta (time working for you)
⚠️ Short vega: If IV spikes, lose $300 per 1% IV increase
→ Reduce short premium positions if VIX rising
```

**调整与退出策略：**
```
Exit Rules by Strategy:

Covered Call:
- Profit: 50-75% of max profit
- Loss: Stock drops >5%, buy back call to preserve upside
- Time: 7-10 DTE, roll to avoid assignment

Spreads:
- Profit: 50% of max profit (close early, reduce tail risk)
- Loss: 2x debit paid (cut losses early)
- Time: 21 DTE, close or roll (avoid gamma risk)

Iron Condor:
- Profit: 50% of credit (close early common)
- Loss: One side tested, 2x credit lost
- Adjustment: Roll tested side out in time

Straddle/Strangle:
- Profit: Stock moved >breakeven, close immediately
- Loss: Theta eating position, stock not moving
- Time: Day after earnings (if earnings play)
```

## 输出格式

**策略分析报告模板：**
```markdown
# Options Strategy Analysis: [Strategy Name]

**Symbol:** [TICKER]
**Strategy:** [Strategy Type]
**Expiration:** [Date] ([DTE] days)
**Contracts:** [Number]

---

## Strategy Setup

### Leg Details
| Leg | Type | Strike | Price | Position | Quantity |
|-----|------|--------|-------|----------|----------|
| 1 | Call | $180 | $5.00 | Long | 1 |
| 2 | Call | $185 | $2.50 | Short | 1 |

**Net Debit/Credit:** $2.50 debit ($250 total for 1 spread)

---

## Profit/Loss Analysis

**Max Profit:** $250 (at $185+)
**Max Loss:** -$250 (at $180-)
**Breakeven:** $182.50
**Risk/Reward Ratio:** 1:1

**Probability Analysis:**
- Probability of Profit: ~55% (stock above $182.50)
- Expected Value: $25 (simplified)

---

## P/L Diagram

[ASCII art diagram here]

---

## Greeks Analysis

### Position Greeks (1 spread)
- **Delta:** +0.20 (gains $20 if stock +$1)
- **Gamma:** +0.03 (delta increases by 0.03 if stock +$1)
- **Theta:** -$5/day (loses $5 per day from time decay)
- **Vega:** +$8 (gains $8 if IV increases 1%)

### Interpretation
- **Directional Bias:** Slightly bullish (positive delta)
- **Time Decay:** Working against you (negative theta)
- **Volatility:** Benefits from IV increase (positive vega)

---

## Risk Assessment

### Maximum Risk
**Scenario:** Stock falls below $180
**Max Loss:** -$250 (100% of premium paid)
**% of Account:** 0.5% (if $50k account)

### Assignment Risk
**Early Assignment:** Low (calls have time value)
**At Expiration:** Manage positions if in-the-money

---

## Trade Management

### Entry
✅ Enter if: [Conditions]
- Stock price $178-$182
- IV below 30%
- >21 DTE

### Profit Taking
- **Target 1:** 50% profit ($125) - Close half
- **Target 2:** 75% profit ($187.50) - Close all

### Stop Loss
- **Trigger:** Stock falls below $177 (-$150 loss)
- **Action:** Close position immediately

### Adjustments
- If stock rallies to $184, consider rolling short call higher
- If stock drops to $179, add second spread at $175/$180

---

## Suitability

### When to Use This Strategy
✅ Moderately bullish on AAPL
✅ Expect upside to $185-$190
✅ Want defined risk
✅ 21-45 DTE timeframe

### When to Avoid
❌ Very bullish (buy stock or long call instead)
❌ High IV environment (wait for IV to drop)
❌ Earnings in <7 days (IV crush risk)

---

## Alternatives Comparison

| Strategy | Max Profit | Max Loss | Complexity | When Better |
|----------|-----------|----------|------------|-------------|
| Bull Call Spread | $250 | -$250 | Medium | Moderately bullish |
| Long Call | Unlimited | -$500 | Low | Very bullish |
| Covered Call | $850 | Unlimited | Medium | Own stock already |
| Bull Put Spread | $300 | -$200 | Medium | Want credit spread |

**Recommendation:** Bull call spread is good balance of risk/reward for moderate bullish thesis.

---

*Disclaimer: This is theoretical analysis using Black-Scholes pricing. Actual market prices may differ. Trade at your own risk. Options are complex instruments with significant loss potential.*
```

**文件命名规则：**
```
options_analysis_[TICKER]_[STRATEGY]_[DATE].md
```

**示例文件名：**options_analysis_AAPL_BullCallSpread_2025-11-08.md**

## 关键原则

### 理论定价的局限性

**用户应了解的内容：**
1. **布莱克-斯科尔斯模型的假设：**
   - 仅适用于欧式期权（不可提前行权）
   - 假设波动率恒定（实际波动率会变化）
   - 假设交易成本为零
   - 假设市场持续交易

**理论与实际操作的差异：**
   - 买卖价差：实际交易成本高于理论计算
   - 美式期权：可以提前行权（尤其是实值期权）
   - 流动性：部分期权市场流动性较低
   - 股息：股息支付日会影响期权价格

**最佳实践：**
   - 将该工具作为学习工具和对比分析工具使用
   - 在交易前获取经纪商提供的实际报价
   - 理论价格约为中间市场价格
   - 考虑佣金和滑点的影响

### 波动率管理建议

**历史波动率与隐含波动率：**

**隐含波动率的百分位数：**

用户提供当前隐含波动率，我们计算其百分位数：
```python
# Fetch 1-year HV data
historical_hvs = calculate_hv_series(prices_1yr, window=30)

# Calculate IV percentile
iv_percentile = percentileofscore(historical_hvs, current_iv)

if iv_percentile > 75:
    guidance = "High IV - consider selling premium (credit spreads, iron condors)"
elif iv_percentile < 25:
    guidance = "Low IV - consider buying options (long calls/puts, debit spreads)"
else:
    guidance = "Normal IV - any strategy appropriate"
```

## 与其他技能的集成

**收益日历：**
- 自动获取收益日期
- 建议相应的收益策略
- 计算距离收益日的天数（DTE对隐含波动率至关重要）
- 警示隐含波动率剧烈变化的风险

**技术分析师的注意事项：**
- 使用支撑/阻力位选择执行价格
- 进行趋势分析以确定方向性策略的时机
- 判断跨式/挤压期权的交易时机

**美国股票分析：**
- 对于长期策略（如LEAPS期权），进行基本面分析
- 考虑股息收益率对覆盖式看涨/看跌期权的影响
- 分析收益质量以制定策略

**风险提示：**
- 高波动率风险：优先选择保护性看跌期权
- 低波动率环境：适合采用多头策略
- 高风险环境：避免买入高溢价期权（因为Theta值会导致损失）

**投资组合管理者：**
- 监控期权头寸与股票头寸的表现
- 统计整个投资组合的希腊值
- 将期权作为股票头寸的对冲工具

## 重要说明**

- **所有分析结果以英文呈现**
- **教育重点**：策略解释清晰易懂
- **理论定价**：使用布莱克-斯科尔斯模型进行近似计算
- **隐含波动率由用户输入**：可选，默认使用历史波动率
- **无需实时数据**：FMP免费版本即可满足需求
- **依赖库：** Python 3.8+、numpy、scipy、pandas

## 常见使用场景**

- **学习期权策略**
- **分析特定交易**
- **制定收益策略**
- **检查投资组合的希腊值**

## 故障排除**

**问题1：无法获取隐含波动率**
  - 解决方案：使用历史波动率作为替代，并告知用户
  - 请求用户从经纪平台获取隐含波动率

**问题2：期权价格为负数**
  - 解决方案：检查输入数据（执行价格与股票价格是否正确）
  - 深度实值期权可能导致计算异常

**问题3：希腊值计算结果不正确**
  - 解决方案：核实输入数据（执行价格、波动率、利率等参数）
  - 确认使用的是年化值还是日波动率

**问题4：策略过于复杂**
  - 解决方案：将策略拆分为多个部分分别分析
  - 参考相关资料了解策略细节

## 参考资源**

- `references/strategies_guide.md`：包含17种以上期权策略的详细说明
- `references/greeks_explained.md`：深入解释希腊值的含义
- `references/volatility_guide.md`：介绍隐含波动率与实际波动率的区别及交易时机

**脚本：**
- `scripts/black_scholes.py`：用于期权定价和希腊值计算
- `scripts/strategy_analyzer.py`：用于策略模拟
- `scripts/earnings_strategy.py`：用于特定收益情况的分析

**外部资源：**
- 期权策略手册：https://www.optionsplaybook.com/
- CBOE教育资源：https://www.cboe.com/education/
- 布莱克-斯科尔斯计算器：多种在线工具可用于验证计算结果

---

**版本：** 1.0
**最后更新时间：** 2025-11-08
**依赖库：** Python 3.8+、numpy、scipy、pandas
**使用的API：** FMP API（免费版本即可满足需求）