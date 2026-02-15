---
name: options-spread-conviction-engine
description: 多策略期权价差分析引擎，结合凯利准则（Kelly Criterion）进行头寸调整。该引擎利用一目均衡线（Ichimoku）、相对强弱指数（RSI）、移动平均收敛发散指标（MACD）、布林带（Bollinger Bands）以及隐含波动率（IV）的期限结构等技术指标，对垂直价差组合（牛市看跌期权、熊市看涨期权、牛市看涨期权、熊市看跌期权）和多腿期权策略（铁秃鹰策略、蝴蝶式期权组合、日历价差组合）进行评分。同时，根据数学最优的凯利准则计算头寸规模，并生成0-100分之间的置信度评分及可操作的交易建议。
version: 2.2.0
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

# 选项价差判断引擎

**该引擎利用技术指标和隐含波动率（IV）期限结构分析，对多种期权策略进行评分。**

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
| **看涨卖空** | 正值期权费 | 均值回归 | 上涨趋势 + 超卖低点 |
| **看跌买入** | 正值期权费 | 均值回归 | 下跌趋势 + 超买高点 |
| **看涨买入** | 负值期权费 | 布局突破 | 强劲上涨动能 |
| **看跌卖空** | 负值期权费 | 布局突破 | 强劲下跌动能 |

### 多腿策略（非方向性/Theta策略）
| 策略 | 类型 | 基本原理 | 理想设置 |
|----------|------|------------|-------------|
| **铁秃鹫** | 正值期权费 | 卖出高溢价期权 | IV排名 >70，RSI中性，价格波动范围有限 |
| **蝴蝶式** | 负值期权费 | 固定价格策略 | 波浪带收窄，RSI处于中间位置，ADX较低 |
| **日历价差** | 负值期权费 | 利用IV期限结构差异获利 | IV期限结构倒置（前端 > 后端） |

## 评分方法

### 垂直价差

不同策略的权重不同（正值期权费 = 均值回归；负值期权费 = 布局突破）：

#### 正值期权费价差（看涨卖空，看跌买入）
| 指标 | 权重 | 作用 |
|-----------|--------|---------|
| 一目均衡线 | 25分 | 判断趋势结构和平衡状态 |
| RSI | 20分 | 进场时机（均值回归） |
| MACD | 15分 | 动能确认 |
| 波浪带 | 25分 | 波动性判断 |
| ADX | 15分 | 判断趋势强度 |

#### 负值期权费价差（看涨买入，看跌卖空）
| 指标 | 权重 | 作用 |
|-----------|--------|---------|
| 一目均衡线 | 20分 | 判断趋势 |
| RSI | 10分 | 判断方向动能 |
| MACD | 30分 | 判断突破速度 |
| 波浪带 | 25分 | 波动带宽度变化 |
| ADX | 15分 | 判断趋势强度 |

### 多腿策略

#### 铁秃鹫（正值期权费 / 价格波动范围有限）
| 组件 | 权重 | 原理 |
|-----------|--------|-----------|
| IV排名（波浪带宽度百分比） | 25分 | 高溢价期权可供卖出 |
| RSI中性 | 20分 | 无方向性动能 |
| ADX波动范围有限 | 20分 | 趋势较弱 = 价格波动范围有限 |
| 价格位置 | 20分 | 价格位于波动范围内 = 风险较低 |
| MACD中性 | 15分 | 无方向性加速 |

**触发条件：**
- IV排名 > 70：高溢价环境
- RSI 40-60：动能中性 |
- ADX < 25：趋势较弱/无趋势 |
- 价格接近中间位置：利润最大化区域

**执行策略：**
- 在价格下方1标准差处卖出看跌期权（卖空）
- 在价格下方2标准差处买入看跌期权（多头看跌）
- 在价格上方1标准差处卖出看涨期权（卖空）
- 在价格上方2标准差处买入看涨期权（多头看涨）

**输出结果：**
- 四个执行价格（看跌多头，看跌空头，看涨空头，看涨多头）
- 最大利润区域（空头执行价格之间的区间）
- 翅部宽度

#### 蝴蝶式策略（负值期权费 / 波动性压缩）
| 组件 | 权重 | 原理 |
|-----------|--------|-----------|
| 波浪带收窄 | 30分 | 波动性压缩 = 价格波动范围缩小 |
| RSI中性 | 25分 | 价格处于平衡状态 |
| ADX较弱 | 无方向性趋势 |
| 价格位于波动范围中间 | 位于波动范围中间以实现最大利润 |
| MACD平缓 | 10分 | 无动能 |

**触发条件：**
- 波浪带宽度百分比 < 25：波动带收窄明显 |
- RSI 45-55：价格处于中间位置（比铁秃鹫策略更严格）
- ADX < 20：趋势非常弱 |
- MACD柱状图接近零 |
- 价格位于中间位置（0.50）

**执行策略：**
- 在中间价格下方买入1个看涨期权（下翼）
- 在中间价格买入2个看涨期权（主体部分）
- 在中间价格上方买入1个看涨期权（上翼）

**输出结果：**
- 三个执行价格（下翼多头，中间空头，上翼多头）
- 最大利润价格（等于中间价格）
- 利润区域（大致的盈亏平衡点）

#### 日历价差（负值期权费 / 利用IV期限结构差异获利）
| 组件 | 权重 | 原理 |
|-----------|--------|-----------|
| IV期限结构 | 30分 | 前端IV > 后端IV = 利用IV期限结构差异 |
| 价格稳定性 | 20分 | 价格接近执行价格 |
| RSI中性 | 20分 | 价格没有偏离执行价格 |
| ADX适中 | 15分 | 有一定趋势结构，但趋势不明显 |
| MACD中性 | 15分 | 无方向性加速 |

**数据来源：**
- 主要数据来源：Yahoo Finance的实时期权链隐含波动率
- 备用数据来源：历史波动率（10天与30天的对比）

**执行策略：**
- 执行价格：标准执行价格区间
- 前端到期日：最接近的可用日期
- 后端到期日：前端到期日后25天以上

**输出结果：**
- 单一执行价格（两个期权腿）
- 前端和后端到期日
- IV差异百分比
- IV期限结构差异的描述

## 评分等级

| 评分 | 等级 | 行动 |
|-------|------|--------|
| 80-100 | 执行 | 信心度高 — 进行价差交易 |
| 60-79 | 准备 | 条件有利 — 调整交易规模 |
| 40-59 | 关注 | 有潜力 — 加入观察列表 |
| 0-39 | 等待 | 条件不佳 — 避免交易 |

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

### 自动化所需的JSON输出

```bash
conviction-engine TSLA --strategy butterfly --json
conviction-engine SPY --strategy calendar --json | jq '.[0].iv_term_structure'
```

### 完整的期权策略

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

IV排名是通过**252个交易日的波浪带宽度百分比**来估算的：

```
IV Rank ≈ (Current BBW - 52wk Low BBW) / (52wk High BBW - 52wk Low BBW) × 100
```

这种相关性已有充分文献支持：实际波动率（波浪带宽度百分比）与隐含波动率排名之间的相关性约为0.7-0.8（Sinclair, "Volatility Trading", 2013）。

## IV期限结构

对于日历价差，该引擎会尝试从Yahoo Finance的期权链中获取实时隐含波动率。如果无法获取，则使用历史波动率数据（10天与30天的对比）作为替代。

## 学术基础

- **一目均衡线** — 判断趋势结构（Hosoda, 1968）
- **RSI** — 动能振荡器（Wilder, 1978）
- **MACD** — 判断趋势动能（Appel, 1979）
- **波浪带** — 判断波动性（Bollinger, 2001）
- **IV排名/期限结构** — 期权市场的微观结构（Sinclair, 2013）

结合多种指标可以降低误判率（Pring, 2002; Murphy, 1999）。

## 架构

```
conviction-engine/
├── scripts/
│   ├── conviction-engine           # CLI wrapper (bash)
│   ├── spread_conviction_engine.py # Core engine (vertical spreads)
│   ├── multi_leg_strategies.py     # Multi-leg extensions
│   ├── quant_scanner.py            # Quantitative options scanner
│   ├── market_scanner.py           # Technical market scanner
│   ├── calculator.py               # Black-Scholes & POP calculator
│   ├── position_sizer.py           # Kelly position sizing
│   ├── chain_analyzer.py           # IV surface analyzer
│   ├── options_math.py             # Core mathematical models
│   └── setup-venv.sh              # Environment setup
└── SKILL.md                        # This documentation
```

### 模块分离

- **spread_conviction_engine.py**：处理垂直价差策略，共享基础设施（数据获取、指标计算）
- **multi_leg_strategies.py**：处理多腿策略（铁秃鹫、蝴蝶式、日历价差）

这种分离有助于保持代码的整洁性，并避免重复代码。

## 限制与假设

### IV数据
- **Yahoo Finance的限制**：在市场关闭时间或某些低成交量股票的期权链可能无法获取数据
- **备用数据**：历史波动率数据虽然不如实时数据准确，但可以提供交易信号
- **IV排名**：通过波浪带宽度百分比估算；实际IV排名需要期权链数据

### 执行价格选择
- **估算方法**：根据波浪带水平确定执行价格（1标准差/2标准差）
- **价格四舍五入**：根据股票价格四舍五入到标准期权执行价格区间
- **无法获取实时价格**：不获取实时期权溢价；执行价格选择基于结构，而非价值优化

### 数据质量
- 需要至少180个交易日的数据才能完整计算一目均衡线
- 多腿策略（尤其是日历价差）需要期权链数据
- 市场关闭时间后的分析可能导致数据质量下降

## 市场假设
- 假设市场条件正常（无极端波动事件）
- 执行价格基于美国股票期权惯例
- 未针对期货、商品或非美国市场进行测试

## 系统要求

- Python 3.10及以上版本（Python 3.14及以上版本支持纯Python模式）
- 需要隔离的虚拟环境（首次运行时会自动创建）
- 需要互联网连接（用于从Yahoo Finance获取数据）

## 安装过程

```bash
clawhub install options-spread-conviction-engine
```

该工具会自动创建虚拟环境并安装以下软件：
- pandas >= 2.0
- pandas_ta >= 0.4.0（Python 3.14及以上版本支持纯Python模式）
- yfinance >= 1.0
- scipy, tqdm

**注意：** 在Python 3.14及以上版本中，该工具以纯Python模式运行，不使用numba库。虽然性能略有下降，但所有功能都能正常使用。

## 市场扫描工具

该工具包含两种不同的扫描工具，适用于不同的交易策略：

### 1. 技术扫描工具（market_scanner.py）
- 使用技术指标（一目均衡线、RSI、MACD、波浪带）自动搜索高信心度的交易机会。
- 支持扫描标准普尔500指数、纳斯达克100指数或自定义股票列表。
- 可过滤出信心度高于80的策略进行执行。

#### 使用方法
```bash
# Scan S&P 500 for high-conviction technical setups
python3 scripts/market_scanner.py --universe sp500
```

### 2. 定量扫描工具（quant_scanner.py）
- 该工具不使用技术指标，而是基于市场微观结构和概率进行交易策略分析。

#### 功能：
- **IV表面分析**：分析波动率分布和期限结构。
- **蒙特卡洛模拟**：进行10,000次模拟以评估真实盈利概率。
- **期望值优化**：寻找风险调整后的最高期望收益交易。
- **考虑账户限制**：确保交易符合账户风险限制（最大风险为100美元）。

#### 使用方法
```bash
# Maximize POP (Probability of Profit) for SPY
python3 scripts/quant_scanner.py SPY --mode pop

# High-expectancy (EV) plays with specific DTE
python3 scripts/quant_scanner.py AAPL TSLA --mode ev --min-dte 30
```

## 计算器与交易规模调整工具

该工具包括以下组件：

### calculator.py
- 支持Black-Scholes期权定价算法，包括：
- 单个期权：看涨期权、看跌期权
- 垂直价差：看涨买入、看跌卖出
- 多腿策略：铁秃鹫、蝴蝶式策略
- 计算期权希腊值（delta、gamma、theta、vega、rho）
- 进行蒙特卡洛模拟

### position_sizer.py
- 适用于小型账户的Kelly准则交易规模调整：
- 提供完整的Kelly准则和分数Kelly准则（默认为0.25）
- 考虑账户风险限制（最大风险为100美元）
- 提供交易筛选和排名功能
- 提供执行价格调整建议

## 相关文件

- `scripts/conviction-engine` — 主要的命令行界面脚本
- `scripts/spread_conviction_engine.py` — 核心价差判断引擎
- `scripts/multi_leg_strategies.py` — 多腿策略扩展（版本2.0.0）
- `scripts/market_scanner.py** — 自动化市场扫描工具
- `scripts/calculator.py` — Black-Scholes定价、希腊值计算、蒙特卡洛模拟
- `scripts/position_sizer.py` — Kelly准则交易规模调整工具
- `scripts/setup-venv.sh` — 环境设置脚本
- `data/sp500_tickers.txt` — 标准普尔500指数成分股列表
- `data/ndx100_tickers.txt` — 纳斯达克100指数成分股列表
- `assets/` — 文档和示例代码

## 版本历史

- **v2.2.0**（2026-02-13）：添加了Kelly准则交易规模调整、边缘计算和账户风险限制功能
- **v2.1.0**（2026-02-12）：增加了市场扫描工具和计算器/交易规模调整工具
- **v2.0.0**（2026-02-12）：增加了多腿策略（铁秃鹫、蝴蝶式、日历价差）
- **v1.2.1**（2026-02-09）：添加了交易量调整功能和动态执行价格建议
- **v1.1.0**（2026-02-08）：增加了多信号加权功能和支持多种策略
- **v1.0.0**（2026-02-07）：初始版本，仅包含看跌卖空策略

## 许可证

MIT许可证 — 该工具属于OpenClaw金融工具包的一部分