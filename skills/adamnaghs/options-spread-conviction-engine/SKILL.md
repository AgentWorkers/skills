---
name: options-spread-conviction-engine
description: 多策略期权组合分析引擎，具备高度的量化严谨性。该引擎支持策略检测（基于VIX指数）、GARCH波动率预测、基于最大回撤限制的Kelly投资组合规模调整方法，以及滚动式回测（walk-forward backtesting）功能。它利用Ichimoku Kinko Hyo、RSI、MACD、Bollinger Bands等技术指标，以及对隐含波动率（IV）期限结构的分析，对垂直期权组合（如牛市看跌期权/看涨期权组合、熊市看涨期权/看跌期权组合）以及多腿期权策略（如铁秃鹰组合、蝴蝶式期权组合、日历式期权组合）进行评估。
version: 2.3.0
author: Leonardo Da Pinchy
metadata:
  openclaw:
    emoji: 📊
    requires:
      bins: ["python3"]
    install:
      - id: venv-setup
        kind: exec
        command: "cd {baseDir} && python3 scripts/setup-venv.sh"
        label: "Setup isolated Python environment with dependencies"
---

# 期权价差判断引擎

**利用技术指标和隐含波动率（IV）期限结构分析，对多种市场环境下的期权价差策略进行评分。**

## 安装

```bash
brew install jq
npm install yahoo-finance2
sudo ln -s /opt/homebrew/bin/yahoo-finance /usr/local/bin/yf
```

## 概述

该引擎可以分析任意股票，并对以下两类期权策略进行评分：

### 垂直价差（方向性策略）
| 策略 | 类型 | 基本原理 | 理想设置 |
|----------|------|------------|-------------|
| **看涨卖空** | 正值 | 均值回归 | 上涨趋势 + 过度卖空 |
| **看跌买入** | 正值 | 均值回归 | 下跌趋势 + 过度买入 |
| **看涨买入** | 负值 | 布朗带突破 | 强劲上涨动能 |
| **看跌卖空** | 负值 | 布朗带突破 | 强劲下跌动能 |

### 多腿策略（非方向性/Theta策略）
| 策略 | 类型 | 基本原理 | 理想设置 |
|----------|------|------------|-------------|
| **铁秃鹫** | 正值 | 高溢价卖出 | IV排名 >70，RSI中性，价格波动范围有限 |
| **蝴蝶式** | 负值 | 固定价格策略 | 布朗带挤压，RSI处于中间位置，ADX较低 |
| **日历价差** | 负值 | 利用IV期限结构差异（前端 > 后端） |

## 评分方法

### 垂直价差

不同策略的权重有所不同（正值 = 均值回归，负值 = 布朗带突破）：

#### 正值价差（看涨卖空，看跌买入）
| 指标 | 权重 | 作用 |
|-----------|--------|---------|
| 一目均衡线 | 25分 | 判断趋势结构和平衡状态 |
| RSI | 20分 | 进场时机（均值回归） |
| MACD | 15分 | 动能确认 |
| 布朗带 | 25分 | 波动性判断 |
| ADX | 15分 | 判断趋势强度 |

#### 负值价差（看涨买入，看跌卖空）
| 指标 | 权重 | 作用 |
|-----------|--------|---------|
| 一目均衡线 | 20分 | 判断趋势 |
| RSI | 10分 | 判断方向动能 |
| MACD | 30分 | 判断突破加速 |
| 布朗带 | 25分 | 波动带宽度变化 |
| ADX | 15分 | 判断趋势强度 |

### 多腿策略

#### 铁秃鹫（正值 / 价格波动范围有限）
| 组成部分 | 权重 | 原理 |
|-----------|--------|-----------|
| IV排名（BBW百分比） | 25分 | 高溢价时适合卖出 |
| RSI中性 | 20分 | 无方向性动能 |
| ADX波动范围有限 | 20分 | 趋势疲软 = 价格波动范围有限 |
| 价格位置 | 20分 | 价格位于波动范围内 = 安全边际 |
| MACD中性 | 15分 | 无方向性加速 |

**触发条件：**
- IV排名 > 70：高溢价环境 |
- RSI 40-60：动能中性 |
- ADX < 25：趋势疲软/无趋势 |
- 价格接近中间点：利润最大化区域

**执行价格选择：**
- 在价格下方1标准差处卖出看跌期权（卖空）
- 在价格下方2标准差处买入看跌期权（多头看跌）
- 在价格上方1标准差处卖出看涨期权（卖空）
- 在价格上方2标准差处买入看涨期权（多头看涨）

**输出结果：**
- 四个执行价格（看涨多头，看跌多头，看跌空头，看涨多头）
- 最大利润区域（卖空执行价格之间的范围）
- 翅部宽度

#### 蝴蝶式（负值 / 波动性压缩）
| 组成部分 | 权重 | 原理 |
|-----------|--------|-----------|
| 布朗带挤压 | 30分 | 波动性压缩 = 价格波动范围狭窄 |
| RSI中性 | 25分 | 价格处于平衡状态 |
| ADX疲软 | 20分 | 完全无方向性趋势 |
| 价格居中 | 15分 | 价格位于波动范围中心，利润最高 |
| MACD平缓 | 10分 | 无动能 |

**触发条件：**
- BBW百分比 < 25：挤压现象明显 |
- RSI 45-55：价格处于中间位置（比铁秃鹫策略更紧密的挤压）
- ADX < 20：趋势非常疲软 |
- MACD柱状图接近零 |
- 价格位于中间点（%B = 0.50）

**执行价格选择：**
- 在中间执行价格下方买入1个看涨期权（下翼）
- 在中间执行价格买入2个看涨期权（主体部分）
- 在中间执行价格上方买入1个看涨期权（上翼）

**输出结果：**
- 三个执行价格（下翼多头，中间空头，上翼多头）
- 最大利润价格（等于中间执行价格）
- 利润区域（大致的盈亏平衡点）

#### 日历价差（负值 / 利用IV期限结构差异）
| 组成部分 | 权重 | 原理 |
|-----------|--------|-----------|
| IV期限结构 | 30分 | 前端IV > 后端IV = 利用IV期限结构差异 |
| 价格稳定性 | 20分 | 价格接近执行价格 |
| RSI中性 | 20分 | 价格没有偏离执行价格 |
| ADX适中 | 15分 | 有一定结构，趋势不明显 |
| MACD中性 | 15分 | 无方向性加速 |

**数据来源：**
- 主要数据来源：Yahoo Finance的实时期权链隐含波动率（IV）
- 备用数据：历史波动率（10天与30天的对比）

**执行价格选择：**
- 平值执行价格（四舍五入到标准间隔）
- 前端到期日：最近的可用日期 |
- 后端到期日：前端到期日后25天以上

**输出结果：**
- 单个执行价格（两个腿）
- 前端和后端到期日 |
- IV差异百分比 |
- IV期限结构差异的描述

## 评分等级

| 评分 | 等级 | 行动 |
|-------|------|--------|
| 80-100 | 执行 | 信心度高 — 进入价差交易 |
| 60-79 | 准备 | 条件有利 — 调整交易规模 |
| 40-59 | 关注 | 有潜力 — 添加到观察列表 |
| 0-39 | 等待 | 条件不佳 — 避免/无需操作 |

## 使用方法

### 垂直价差

```bash
# Basic analysis (auto-detects best strategy)
conviction-engine AAPL

# Specific strategy
conviction-engine SPY --strategy bear_call
conviction-engine QQQ --strategy bull_call --period 2y
```

### 多腿策略

```bash
# Iron Condor — high IV, range-bound
conviction-engine SPY --strategy iron_condor

# Butterfly — volatility compression, pinning play
conviction-engine AAPL --strategy butterfly

# Calendar — inverted IV term structure, theta harvest
conviction-engine TSLA --strategy calendar
```

### 多个股票

```bash
conviction-engine AAPL MSFT GOOGL --strategy bull_put
conviction-engine SPY QQQ IWM --strategy iron_condor
```

### JSON输出（用于自动化）

```bash
conviction-engine TSLA --strategy butterfly --json
conviction-engine SPY --strategy calendar --json | jq '.[0].iv_term_structure'
```

### 完整期权策略

```bash
conviction-engine <ticker> [ticker...]
  --strategy {bull_put,bear_call,bull_call,bear_put,iron_condor,butterfly,calendar}
  --period {1y,2y,3y,5y}
  --interval {1h,1d,1wk}
  --json
```

## 示例输出

### 铁秃鹫策略

```
================================================================================
SPY — Iron Condor (Credit)
================================================================================
Price: $681.27 | Score: 31.8/100 → WAIT

[IV Rank +2.5/25]
  IV Rank (BBW proxy): 5% (VERY_LOW)
  BBW: 3.17 (1Y range: 2.37 - 18.13)
  Premiums are THIN — poor risk/reward for credit

Strikes:
  BUY  680.0P | SELL 685.0P
  SELL 695.0C | BUY  700.0C
  Max Profit Zone: $685.0 - $695.0
  Wing Width: $5.00
```

### 蝴蝶式策略

```
================================================================================
SPY — Long Butterfly (Debit)
================================================================================
Price: $681.27 | Score: 64.5/100 → PREPARE

[BB Squeeze +27.0/30]
  Bandwidth: 3.1701 (percentile: 21%)
  SQUEEZE ACTIVE — 19 consecutive bars

Strikes:
  BUY 1x 685.0C | SELL 2x 690.0C | BUY 1x 695.0C
  Max Profit Price: $690.0
  Profit Zone: ~$685.0 - $695.0
```

### 日历价差策略

```
================================================================================
SPY — Calendar Spread (Debit)
================================================================================
Price: $681.27 | Score: 67.2/100 → PREPARE

[IV Term Structure +30.0/30]
  Front IV: 27.5% | Back IV: 19.4%
  Differential: +41.7%
  INVERTED TERM STRUCTURE — calendar opportunity confirmed

Strikes:
  Strike: $680.0
  SELL 2026-02-13 | BUY 2026-03-13
  Theta Advantage: Front IV > Back IV by 41.7%
```

## IV排名估算

IV排名是通过**布隆带宽度（BBW）百分比**在252个交易日内估算的：

```
IV Rank ≈ (Current BBW - 52wk Low BBW) / (52wk High BBW - 52wk Low BBW) × 100
```

这种相关性已有充分文献支持：实际波动率（BBW）与隐含波动率排名之间的相关性约为0.7-0.8（Sinclair, "Volatility Trading", 2013）。

## IV期限结构

对于日历价差策略，该引擎会尝试从Yahoo Finance的期权链中获取实时平值隐含波动率。如果无法获取，则会使用历史波动率期限结构（10天与30天的对比）作为替代数据。

## 定量模块（v2.3.0）

该引擎现在包含四个定量模块，用于严格验证和优化策略：

### 1. 市场环境检测器（`regime_detector.py`）

使用VIX百分位数对市场环境进行分类：
- **危机状态**：VIX > 第80百分位数 — 适合卖出高溢价期权（铁秃鹫策略）
- **高波动性**：VIX在60-80百分位数之间 — 高隐含波动率有利于卖出期权价差 |
- **正常波动性**：VIX在40-60百分位数之间 — 所有策略均可行 |
- **低波动性**：VIX在20-40百分位数之间 — 低价期权适合卖出期权价差 |
- **繁荣状态**：VIX < 第20百分位数 — 动能持续，均值回归趋势显现

```bash
# Detect current regime
python3 scripts/regime_detector.py

# Get regime-adjusted weights for specific strategy
python3 scripts/regime_detector.py --strategy iron_condor --json
```

**集成：**
```python
from regime_detector import RegimeDetector

detector = RegimeDetector()
regime, confidence = detector.detect_regime()
weights = detector.get_regime_weights(regime)
adjusted_score, reasoning = detector.regime_aware_score(75, regime, 'bull_put')
```

### 2. 波动性预测器（`vol_forecaster.py`）

基于GARCH模型的实际波动率预测，结合VRP分析：
- 对历史回报数据拟合GARCH(1,1)模型 |
- 预测可实现的波动率 |
- 计算波动率风险溢价（IV - RV预测值） |
- 根据VRP结果调整策略决策

```bash
# Analyze AAPL volatility
python3 scripts/vol_forecaster.py AAPL

# Compare IV = 25% vs forecast RV
python3 scripts/vol_forecaster.py SPY --iv 0.25 --horizon 5
```

**解释：**
- VRP > 5%：适合卖出高溢价期权（正值价差策略） |
- VRP < -5%：适合买入高溢价期权（负值价差策略） |
- VRP接近0：波动性优势不明显，应关注方向性策略 |

**集成：**
```python
from vol_forecaster import VolatilityForecaster

forecaster = VolatilityForecaster("AAPL")
params = forecaster.fit_garch()  # Returns omega, alpha, beta
forecast = forecaster.forecast_vol(horizon=5)
vrp, strength, rec = forecaster.vol_risk_premium(iv=0.25, rv_forecast=forecast.annualized_vol)
adjusted_score, reasoning = forecaster.add_to_conviction(70, vrp_signal, 'bull_put')
```

### 3. 改进版Kelly法则定位器（`enhanced_kelly.py`）

考虑回撤限制和相关性的定位策略：
- 完整的Kelly法则计算 |
- 回撤限制：f_dd = f_kelly × (1 - 目标回撤 / 最大回撤) |
- 根据信心程度调整Kelly法则：
  - 90-100：使用半Kelly法则 |
  - 80-89：使用四分之一Kelly法则 |
  - 60-79：使用八分之一Kelly法则 |
  - <60：不进行交易 |

**集成：**
```bash
# Calculate position with $390 account
python3 scripts/enhanced_kelly.py --loss 80 --win 40 --pop 0.65 --conviction 85

# Include correlation with existing position
python3 scripts/enhanced_kelly.py --loss 80 --win 40 --pop 0.65 --conviction 85 --correlation 0.3
```

### 4. 回测验证器（`backtest-validator.py**

对策略评分进行前瞻性验证：
- 在整个股票市场中模拟历史交易 |
- 验证不同评分等级的表现 |
- 进行统计测试（t检验、方差分析） |
- 评分等级区分（0-1） |
- 提出权重调整建议

**输出指标：**
- 各评分等级的胜率 |
- 各等级的期望收益：(胜率 × 平均收益) - (亏损率 × 平均亏损) |
- 各等级的夏普比率 |
- 不同等级之间的差异显著性（P值） |

**集成：**
```python
from backtest_validator import BacktestValidator

validator = BacktestValidator(engine, "2022-01-01", "2024-01-01")
results_df = validator.run_walk_forward(["AAPL", "MSFT"], hold_days=5)
report = validator.validate_tiers(results_df)
print(f"Separation score: {report.tier_separation_score:.2f}")
print(f"EXECUTE vs WAIT p-value: {report.p_values['execute_vs_wait']:.4f}")
```

### 5. 定量集成模块（`quantitative_integration.py`**

整合所有定量模块的统一接口：

```bash
# Full quantitative analysis with regime and VRP
python3 scripts/quantitative_integration.py AAPL --regime-aware --vol-aware

# With Kelly sizing
python3 scripts/quantitative_integration.py SPY --regime-aware --pop 0.65 --max-loss 80 --win-amount 40

# Run backtest validation
python3 scripts/quantitative_integration.py --backtest SPY QQQ --start 2022-01-01 --end 2024-01-01
```

## 学术基础

- **一目均衡线** — 用于判断趋势结构（Hosoda, 1968） |
- **RSI** — 用于判断动能（Wilder, 1978） |
- **MACD** — 用于判断趋势动能（Appel, 1979） |
- **布隆带** — 用于判断波动性（Bollinger, 2001） |
- **IV排名/期限结构** — 用于分析期权市场微观结构（Sinclair, 2013） |

结合多种指标可以降低误判率（Pring, 2002; Murphy, 1999）。

## 架构

```
conviction-engine/
├── scripts/
│   ├── conviction-engine              # CLI wrapper (bash)
│   ├── spread_conviction_engine.py    # Core engine (vertical spreads)
│   ├── multi_leg_strategies.py        # Multi-leg extensions
│   ├── quantitative_integration.py    # Unified quantitative interface
│   ├── regime_detector.py             # VIX-based regime classification
│   ├── vol_forecaster.py              # GARCH volatility forecasting
│   ├── enhanced_kelly.py              # Drawdown-constrained Kelly sizing
│   ├── backtest_validator.py          # Walk-forward validation
│   ├── quant_scanner.py               # Quantitative options scanner
│   ├── market_scanner.py              # Technical market scanner
│   ├── calculator.py                  # Black-Scholes & POP calculator
│   ├── position_sizer.py              # Kelly position sizing
│   ├── chain_analyzer.py              # IV surface analyzer
│   ├── options_math.py                # Core mathematical models
│   └── setup-venv.sh                  # Environment setup
├── tests/                             # Unit tests
│   ├── test_regime_detector.py
│   ├── test_vol_forecaster.py
│   ├── test_enhanced_kelly.py
│   ├── test_backtest_validator.py
│   └── run_tests.py
└── SKILL.md                           # This documentation
```

### 模块分离

- **spread_conviction_engine.py**：处理垂直价差策略，提供通用数据获取和指标计算功能 |
- **multi_leg_strategies.py**：实现铁秃鹫、蝴蝶式、日历价差等多腿策略 |
- **quantitative_integration.py**：提供统一的接口，用于整合市场环境检测、波动性分析、Kelly法则定位和回测模块 |
- **regime_detector.py**：使用VIX百分位数进行市场环境分类 |
- **vol_forecaster.py**：基于GARCH模型的实际波动率预测 |
- **enhanced_kelly.py**：考虑回撤限制和相关性的定位策略 |
- **backtest-validator.py**：对策略评分进行前瞻性验证 |

这种模块分离有助于保持代码的清晰度和避免重复代码。

## 限制与假设

### IV数据
- **Yahoo Finance的局限性**：在市场关闭时间或交易量较低的股票上，期权链数据可能不可用 |
- **备用数据**：历史波动率数据虽然不如实时数据准确，但可以提供交易信号 |
- **IV排名**：通过布隆带宽度估算；实际IV排名需要期权链数据 |

### 执行价格选择
- **估算方法**：执行价格基于布隆带水平（1标准差/2标准差） |
- **四舍五入**：根据股票价格将执行价格四舍五入到标准期权间隔 |
- **无实时价格数据**：不获取实时期权溢价；执行价格选择基于结构，而非价值优化 |

### 数据质量
- 需要至少180个交易日的数据才能使用一目均衡线 |
- 多腿策略（尤其是日历价差策略）需要期权链数据 |
- 市场关闭时间后的数据分析可能导致数据质量下降 |

## 市场假设
- 假设市场处于正常波动状态（非极端波动情况） |
- 执行价格基于美国股票期权惯例 |
- 未针对期货、商品或非美国市场进行测试

## 系统要求

- Python 3.10及以上版本（Python 3.14及以上版本支持纯Python模式） |
- 需要隔离的虚拟环境（首次运行时会自动创建） |
- 需要互联网连接（用于从Yahoo Finance获取数据）

## 安装说明

```bash
clawhub install options-spread-conviction-engine
```

该工具会自动创建虚拟环境并安装以下库：
- pandas >= 2.0 |
- pandas_ta >= 0.4.0（Python 3.14及以上版本支持纯Python模式） |
- yfinance >= 1.0 |
- scipy, tqdm

**注意：** 在Python 3.14及以上版本中，该工具以纯Python模式运行，不使用numba库。虽然性能略有下降，但所有功能均能正常使用。

## 市场扫描工具

该工具包含两种不同的扫描工具，适用于不同的交易策略：

### 1. 技术扫描器（market_scanner.py）
- 使用技术指标（一目均衡线、RSI、MACD、布隆带）自动搜索高信心度的交易机会 |
- 支持扫描标准普尔500指数、纳斯达克100指数或自定义股票列表 |
- 过滤出信心等级≥80的策略 |
- 执行前会进行交易规模调整，确保符合账户限制。

#### 使用方法
```bash
# Scan S&P 500 for high-conviction technical setups
python3 scripts/market_scanner.py --universe sp500
```

### 2. 定量扫描器（quant_scanner.py）
- 该工具侧重于市场微观结构和概率分析，不使用技术指标 |
- **IV表面分析**：分析价格偏度和期限结构 |
- **蒙特卡洛模拟**：进行10,000次模拟以评估实际盈利概率 |
- **期望值优化**：寻找风险调整后的最高期望收益交易 |
- **账户限制**：考虑账户资金限制（最大风险为100美元）

#### 使用方法
```bash
# Maximize POP (Probability of Profit) for SPY
python3 scripts/quant_scanner.py SPY --mode pop

# High-expectancy (EV) plays with specific DTE
python3 scripts/quant_scanner.py AAPL TSLA --mode ev --min-dte 30
```

## 计算器与定位器

该工具包包含以下工具：

### calculator.py
- 使用Black-Scholes模型计算期权价格，支持以下类型：
- 单个期权：看涨期权、看跌期权 |
- 垂直价差：看涨买入、看跌卖出 |
- 多腿策略：铁秃鹫、蝴蝶式期权 |
- 计算期权希腊值（delta、gamma、theta、vega、rho） |
- 进行蒙特卡洛模拟

### position_sizer.py
- 根据Kelly法则调整交易规模，适用于小账户：
- 完整的Kelly法则和部分Kelly法则（默认为0.25） |
- 考虑账户资金限制 |
- 进行交易筛选和排名 |
- 提供执行价格调整建议

## 文件结构

- `scripts/conviction-engine`：主要的命令行接口 |
- `scripts/spread_conviction_engine.py`：核心的垂直价差策略模块 |
- `scripts/multi_leg_strategies.py`：多腿策略扩展模块（v2.0.0） |
- `scripts/market_scanner.py`：自动执行策略的扫描工具 |
- `scripts/calculator.py`：Black-Scholes定价、希腊值计算、蒙特卡洛模拟 |
- `scripts/position_sizer.py**：根据Kelly法则调整交易规模 |
- `scripts/setup-venv.sh`：环境设置脚本 |
- `data/sp500_tickers.txt`：标准普尔500指数成分股列表 |
- `data/ndx100_tickers.txt`：纳斯达克100指数成分股列表 |
- `assets/`：包含文档和示例代码

## 版本历史

- **v2.3.0**（2026-02-13）：增强定量分析功能 |
  - 引入市场环境检测器，基于VIX百分位数进行市场分类 |
  - 引入波动性预测器，结合VRP分析 |
  - 改进Kelly法则定位器，考虑回撤限制和相关性 |
  - 引入回测验证器，进行分级验证 |
  - 整合所有定量模块 |

- **v2.2.0**（2026-02-13）：完善Kelly法则定位器，包括全额/部分Kelly法则、利润计算和账户限制 |
- **v2.1.0**（2026-02-12）：新增市场扫描器和定位工具 |
- **v2.0.0**（2026-02-12）：新增多腿策略（铁秃鹫、蝴蝶式、日历价差） |
- **v1.2.1**（2026-02-09）：引入交易量调整和动态执行价格建议 |
- **v1.1.0**（2026-02-08）：引入多指标加权机制和多策略支持 |
- **v1.0.0**（2026-02-07）：初始版本，包含看涨卖空策略 |

## 许可证

MIT许可证 — 该工具属于OpenClaw金融工具包的一部分。