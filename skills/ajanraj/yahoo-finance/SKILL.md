---
name: yahoo-finance
description: 使用 Yahoo Finance 获取股票价格、报价、基本财务数据、收益信息、期权信息、股息信息以及分析师评级。该功能依赖于 yfinance 库，无需 API 密钥。
---

# Yahoo Finance CLI

这是一个Python命令行工具（CLI），用于通过yfinance库从Yahoo Finance获取全面的股票数据。

## 系统要求

- Python 3.11或更高版本
- uv（用于管理内联脚本的依赖关系）

## 安装uv

该工具需要`uv`这个高效的Python包管理器。请检查是否已安装：

```bash
uv --version
```

如果尚未安装，请使用以下方法之一进行安装：

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### macOS（使用Homebrew）
```bash
brew install uv
```

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 使用pip（适用于所有平台）
```bash
pip install uv
```

安装完成后，请重启终端或运行以下命令：
```bash
source ~/.bashrc  # or ~/.zshrc on macOS
```

## 使用方法

`yf`脚本使用了PEP 723规范的内联脚本元数据，因此在首次运行时会自动安装所有依赖关系（包括yfinance和rich库）。后续运行将直接使用已缓存的依赖关系，无需重新安装。

## 常用命令

### 查看股票价格（快速查询）
```bash
yf AAPL              # shorthand for price
yf price AAPL
```

### 查看股票详细报价
```bash
yf quote MSFT
```

### 查看公司基本信息
```bash
yf fundamentals NVDA
```
显示：市盈率（PE ratio）、每股收益（EPS）、市值（market cap）、利润率（margins）、净资产收益率（ROE/ROA）以及分析师预测。

### 查看公司收益信息
```bash
yf earnings TSLA
```
显示：下次收益公布日期、每股收益预估值以及历史收益数据。

### 查看公司概况
```bash
yf profile GOOGL
```
显示：所属行业、员工人数、官方网站、公司地址及业务描述。

### 查看股息信息
```bash
yf dividends KO
```
显示：股息率/收益率（dividend rate/yield）、除权日（ex-date）、股息支付比例（payout ratio）以及最近的股息发放记录。

### 查看分析师评级
```bash
yf ratings AAPL
```
显示：分析师的买入/持有/卖出建议（buy/hold/sell recommendations）、平均评级以及最近的评级变化。

### 查看期权信息
```bash
yf options SPY
```
显示：平值附近的看涨/看跌期权（near-the-money calls/puts），包括执行价格（strike price）、买卖价（bid/ask price）、成交量（volume）、期权合约总量（OI）以及隐含波动率（IV）。

### 查看股票历史数据
```bash
yf history GOOGL 1mo     # 1 month history
yf history TSLA 1y       # 1 year
yf history BTC-USD 5d    # 5 days
```
可选时间范围：1天、5天、1个月、3个月、6个月、1年、2年、5年、10年、截至当前日期（ytd）或全部历史数据。

### 进行股票比较
```bash
yf compare AAPL,MSFT,GOOGL
yf compare RELIANCE.NS,TCS.NS,INFY.NS
```
可以同时查看多只股票的价格、价格变化幅度以及市值等信息。

### 进行股票搜索
```bash
yf search "reliance industries"
yf search "bitcoin"
yf search "s&p 500 etf"
```

## 股票代码格式示例

- **美国股票**：AAPL, MSFT, GOOGL, TSLA
- **印度NSE股票**：RELIANCE.NS, TCS.NS, INFY.NS
- **印度BSE股票**：RELIANCE.BO, TCS.BO
- **加密货币**：BTC-USD, ETH-USD
- **外汇货币对**：EURUSD=X, GBPUSD=X
- **交易所交易基金（ETFs）**：SPY, QQQ, VOO

## 使用示例

```bash
# Quick price check
yf AAPL

# Get valuation metrics
yf fundamentals NVDA

# Next earnings date + history
yf earnings TSLA

# Options chain for SPY
yf options SPY

# Compare tech giants
yf compare AAPL,MSFT,GOOGL,META,AMZN

# Find Indian stocks
yf search "infosys"

# Dividend info for Coca-Cola
yf dividends KO

# Analyst ratings for Apple
yf ratings AAPL
```

## 常见问题解决方法

- **“command not found: uv”**：请按照上述说明重新安装uv。
- **请求速率限制/连接错误**：Yahoo Finance可能会对大量请求进行限制。请稍等几分钟后再尝试。
- **某些股票的数据无法获取**：请使用`yf search "股票代码"`确认该股票是否存在；部分数据（如期权、股息信息）可能不适用于所有股票。

## 技术说明

- 该工具依赖`uv`来管理内联脚本的依赖关系，并使用PEP 723规范进行元数据管理。
- `rich`库提供了格式化良好的表格数据。
- 首次运行时会将所有依赖关系安装到`uv`的缓存中，后续运行将直接使用缓存数据，无需重新安装。
- 该工具能够优雅地处理NaN或None值，并提供相应的默认处理方式。