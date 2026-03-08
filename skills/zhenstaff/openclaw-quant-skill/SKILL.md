---
name: openclaw-quant
description: 专业的加密货币量化交易系统——支持回测、模拟交易、实盘交易以及策略优化功能。
tags: [quant, trading, backtest, crypto, strategy, optimization, bitcoin, trading-bot, algorithmic-trading]
version: 0.1.0
---
# 定量交易技能

这是一个专为加密货币市场设计的专业定量交易系统，具备回测、模拟交易、实盘交易和高级策略优化功能。

## 安装

### 第一步：安装 Quantitative Trading 技能

```bash
clawhub install openclaw-quant
```

### 第二步：克隆并设置项目

```bash
# Clone repository
git clone https://github.com/ZhenRobotics/openclaw-quant.git ~/openclaw-quant
cd ~/openclaw-quant

# Install dependencies
pip install -r requirements.txt

# Set API keys (optional for backtesting)
export BINANCE_API_KEY="your-key"
export BINANCE_API_SECRET="your-secret"
```

### 第三步：验证安装

```bash
cd ~/openclaw-quant
python -m openclaw_quant --help
```

---

## 核心功能

- **回测引擎**：使用真实数据模拟来测试交易策略
- **模拟交易**：利用实时市场数据进行模拟交易
- **实盘交易**：在真实交易所（如 Binance、OKX 等）进行自动交易
- **策略优化**：使用贝叶斯方法进行参数优化
- **技术指标**：内置 50 多种技术指标（MA、RSI、MACD、Bollinger 等）
- **风险管理**：控制头寸大小、设置止损和止盈
- **绩效分析**：计算夏普比率、最大回撤率、胜率、盈利因子
- **多交易所支持**：通过 ccxt 库支持 100 多个交易所

---

## 何时使用此技能

当用户的消息包含以下关键词或请求时，会自动触发该技能：
- `backtest`（回测）、`trading strategy`（交易策略）、`quant`（量化交易）、`cryptocurrency trading`（加密货币交易）、`optimize strategy`（优化策略）
- 例如：“测试这个交易策略”、“回测 MA 交叉信号”、“用我的动量策略进行模拟交易”
- 战略描述：“当 RSI < 30 时买入，当 RSI > 70 时卖出”
- 绩效相关问题：“夏普比率是多少？”、“计算最大回撤率”

**触发示例**：
- “在比特币上回测移动平均线交叉策略”
- “优化过去 6 个月的 RSI 参数”
- “使用我的动量策略开始模拟交易”
- “这个策略的胜率是多少？”

**不适用的情况**：
- 仅用于投资组合跟踪（使用 investmentportfolio-tracker 技能）
- 仅用于价格警报（使用 price-alert 技能）
- 一般性的加密货币新闻或信息

---

## 快速入门示例

### 示例 1：简单移动平均线策略

```python
from openclaw_quant import Strategy, Backtest

class MAStrategy(Strategy):
    # Parameters (can be optimized)
    fast_period = 10
    slow_period = 30

    def init(self):
        # Vectorized indicator calculation
        self.fast_ma = self.I(SMA, self.data.Close, self.fast_period)
        self.slow_ma = self.I(SMA, self.data.Close, self.slow_period)

    def next(self):
        # Event-driven logic
        if self.fast_ma[-1] > self.slow_ma[-1]:
            if not self.position:
                self.buy()
        else:
            if self.position:
                self.sell()

# Backtest
bt = Backtest(MAStrategy, data, cash=10000, commission=0.001)
result = bt.run()
print(result)
result.plot()
```

### 示例 2：RSI 均值回归策略

```python
class RSIStrategy(Strategy):
    rsi_period = 14
    oversold = 30
    overbought = 70

    def init(self):
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)

    def next(self):
        if self.rsi[-1] < self.oversold:
            if not self.position:
                self.buy()
        elif self.rsi[-1] > self.overbought:
            if self.position:
                self.sell()

bt = Backtest(RSIStrategy, data, cash=10000)
result = bt.run()
```

### 示例 3：参数优化

```python
# Optimize parameters automatically
result = bt.optimize(
    fast_period=range(5, 20, 2),
    slow_period=range(20, 60, 5),
    maximize='sharpe_ratio'  # or 'total_return', 'profit_factor'
)

print(f"Best parameters: {result.best_params}")
print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
```

### 示例 4：模拟交易

```python
from openclaw_quant import LiveTrading

# Paper trading with real-time data
live = LiveTrading(
    strategy=MAStrategy,
    exchange='binance',
    symbol='BTC/USDT',
    paper=True  # Simulation mode
)

live.run()
```

### 示例 5：实盘交易

```python
# Real trading (use with caution!)
live = LiveTrading(
    strategy=MAStrategy,
    exchange='binance',
    symbol='BTC/USDT',
    paper=False,  # Real mode
    api_key=os.getenv('BINANCE_API_KEY'),
    api_secret=os.getenv('BINANCE_API_SECRET')
)

live.run()
```

---

## 代理使用指南

### 命令行界面

```bash
# Backtest a strategy
openclaw-quant backtest --strategy ma_cross --symbol BTCUSDT --days 365

# Optimize parameters
openclaw-quant optimize --strategy rsi --symbol ETHUSDT --metric sharpe_ratio

# Paper trading
openclaw-quant paper --strategy ma_cross --symbol BTCUSDT

# Live trading
openclaw-quant live --strategy ma_cross --symbol BTCUSDT --confirm

# View results
openclaw-quant results --backtest-id abc123
```

### 自然语言（通过 OpenClaw 代理）

代理可以理解以下请求：
- “在比特币上回测过去一年的移动平均线交叉策略”
- “优化 RSI 参数以最大化夏普比率”
- “使用我的动量策略，用 1 万美元开始模拟交易”
- “显示上次回测的绩效指标”
- “我的实盘交易账户的最大回撤率是多少？”

---

## 绩效指标

系统计算以下综合绩效指标：

| 指标 | 描述 |
|--------|-------------|
| **总回报** | 总利润/亏损百分比 |
| **年化回报** | 年化后的回报 |
| **夏普比率** | 经风险调整后的回报（数值越高越好） |
| **Sortino 比率** | 下降风险调整后的回报 |
| **最大回撤率** | 最大峰值到最低值的跌幅 |
| **胜率** | 盈利交易的百分比 |
| **盈利因子** | 总利润 / 总亏损 |
| **Calmar 比率** | 回报 / 最大回撤率 |
| **平均盈亏** | 每笔交易的平均利润/亏损 |
| **预期收益** | 每笔交易的预期价值 |

---

## 内置策略

系统包含几种现成的策略：
1. **MA Cross**：移动平均线交叉策略
2. **RSI 均值回归**：在超卖时买入，在超买时卖出
3. **MACD 动量**：MACD 线和信号线的交叉
4. **Bollinger Bounce**：在 Bollinger 带触碰时进行交易
5. **突破**：在支撑/阻力位突破时进行交易
6. **网格交易**：在价格区间内低买高卖
7. **DCA（美元成本平均法）**：定期买入
8. **均值回归**：统计套利策略

---

## 技术指标

通过 `self.I()` 方法可以使用 50 多种技术指标：

**趋势指标**：
- SMA、EMA、WMA、DEMA、TEMA
- MACD、ADX、Aroon、Supertrend

**动量指标**：
- RSI、Stochastic、CCI、Williams %R
- ROC（变化率）、Momentum

**波动性指标**：
- Bollinger 带、ATR、Keltner 通道
- 标准差、历史波动率

**成交量指标**：
- OBV、Volume SMA、MFI、VWAP
- Accumulation/Distribution、CMF

---

## 风险管理

系统内置了以下风险管理功能：

```python
class MyStrategy(Strategy):
    def init(self):
        # Set risk parameters
        self.risk_per_trade = 0.02  # 2% of capital
        self.stop_loss = 0.05       # 5% stop loss
        self.take_profit = 0.10     # 10% take profit

        self.ma = self.I(SMA, self.data.Close, 20)

    def next(self):
        if self.ma[-1] > self.data.Close[-1]:
            if not self.position:
                # Calculate position size based on risk
                size = self.calculate_position_size(
                    risk=self.risk_per_trade,
                    stop_loss=self.stop_loss
                )
                self.buy(size=size)
                self.set_stop_loss(self.stop_loss)
                self.set_take_profit(self.take_profit)
```

---

## 数据来源

支持多种数据来源：
1. **交易所 API**：Binance、OKX、Bybit 等（通过 ccxt）
2. **CSV 文件**：从文件中加载历史数据
3. **数据库**：使用 PostgreSQL 或 SQLite 进行数据缓存
4. **实时 WebSocket**：获取实时市场数据

```python
# Example: Load data from Binance
from openclaw_quant import DataFetcher

fetcher = DataFetcher('binance')
data = fetcher.fetch_candles(
    symbol='BTC/USDT',
    timeframe='1h',
    since='2023-01-01',
    limit=1000
)
```

---

## 配置

配置文件示例（`config.yaml`）：

```yaml
backtest:
  initial_capital: 10000
  commission: 0.001  # 0.1%
  slippage: 0.0005   # 0.05%

strategy:
  name: ma_cross
  parameters:
    fast_period: 10
    slow_period: 30

exchange:
  name: binance
  testnet: false

risk:
  max_position_size: 0.1  # 10% of capital
  max_drawdown: 0.2       # Stop if 20% drawdown
  daily_loss_limit: 0.05  # Stop if 5% daily loss

notification:
  telegram:
    enabled: true
    bot_token: "your-token"
    chat_id: "your-chat-id"
```

---

## 项目结构

```
openclaw-quant/
├── src/
│   ├── openclaw_quant/
│   │   ├── __init__.py
│   │   ├── strategy.py         # Strategy base class
│   │   ├── backtest.py         # Backtest engine
│   │   ├── live.py             # Live trading engine
│   │   ├── broker.py           # Order execution
│   │   ├── data.py             # Data fetching
│   │   ├── indicators.py       # Technical indicators
│   │   ├── optimizer.py        # Parameter optimization
│   │   ├── metrics.py          # Performance metrics
│   │   └── risk.py             # Risk management
│   └── strategies/
│       ├── ma_cross.py
│       ├── rsi.py
│       └── ...
├── examples/
│   ├── backtest_example.py
│   ├── optimization_example.py
│   └── paper_trading_example.py
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

---

## 需求

```
Python >= 3.9
pandas >= 2.0.0
numpy >= 1.24.0
ccxt >= 4.0.0
optuna >= 3.0.0
matplotlib >= 3.7.0
pydantic >= 2.0.0
```

---

## 故障排除

### 问题 1：API 连接错误

**错误**：`ccxt.NetworkError` 或连接超时

**解决方法**：
```bash
# Check internet connection
# Verify API keys are correct
# Use testnet for testing:
exchange = ccxt.binance({'enableRateLimit': True, 'options': {'defaultType': 'future', 'testnet': True}})
```

### 问题 2：数据不足

**错误**：策略测试所需的数据量不足

**解决方法**：
```python
# Increase warmup period
bt = Backtest(strategy, data, warmup=100)  # Skip first 100 candles

# Or fetch more historical data
data = fetcher.fetch_candles(symbol='BTC/USDT', limit=5000)
```

### 问题 3：优化耗时过长

**解决方法**：
```python
# Reduce search space
result = bt.optimize(
    fast_period=range(5, 20, 5),  # Larger step
    slow_period=range(20, 60, 10),
    max_tries=50  # Limit iterations
)
```

---

## 安全指南

### 回测
- 始终先在历史数据上进行测试
- 使用真实的佣金和滑点设置
- 注意过拟合现象
- 建议使用向前验证（walk-forward validation）

### 模拟交易
- 至少测试 1-2 周
- 监控滑点和成交情况
- 在不同市场条件下测试策略表现

### 实盘交易
- 从小额资金开始
- 设置严格的风险限制
- 在第一周内持续监控
- 设置紧急止损机制
- 绝不要冒险超过你能承受的损失

---

## 性能优化技巧

1. **向量化**：使用 `self.I()` 方法来计算指标（只需计算一次）
2. **数据缓存**：缓存历史数据以避免重复调用 API
3. **优化方法**：使用贝叶斯优化，而非网格搜索
4. **并行回测**：同时测试多个交易品种
5. **WebSocket**：使用 WebSocket 获取实时数据（比 REST 更快）

---

## 文档资料

- **GitHub**：https://github.com/ZhenRobotics/openclaw-quant
- **快速入门**：`~/openclaw-quant/QUICKSTART.md`
- **API 参考**：`~/openclaw-quant/docs/API.md`
- **策略指南**：`~/openclaw-quant/docs/STRATEGIES.md`
- **完整说明文档**：`~/openclaw-quant/README.md`

---

## 开发计划

### 版本 0.1.0（当前版本）
- 基本回测引擎
- 简单策略（MA、RSI）
- 支持 Binance 交易所

### 版本 0.2.0
- 模拟交易功能
- 参数优化
- 增加更多技术指标

### 版本 0.3.0
- 实盘交易功能
- 支持多个交易所
- 高级风险管理功能

### 版本 1.0.0
- 准备上线
- 提供 Web 仪表盘
- 构建策略市场

---

## 成本

- **开发**：免费且开源（MIT 许可证）
- **数据**：免费（使用交易所 API）
- **交易费用**：因交易所而异（通常为 0.1%）
- **API 使用费用**：大多数交易所提供免费 tier

---

## 许可证

MIT 许可证——个人和商业用途均免费

---

## 支持

- **问题报告**：https://github.com/ZhenRobotics/openclaw-quant/issues
- **讨论区**：https://github.com/ZhenRobotics/openclaw-quant/discussions
- **ClawHub**：https://clawhub.ai/ZhenStaff/openclaw-quant

---

## 代理使用规范

使用此技能时，代理应：
- 在使用前检查项目是否已安装
- 在实盘交易模式下提醒用户注意风险
- 验证策略参数
- 显示清晰的绩效指标
- 解释优化结果

**禁止行为**：
- 未经明确确认直接执行实盘交易
- 推荐具体的交易策略
- 保证盈利或回报
- 忽视风险警告
- 提供财务建议

---

**状态**：开发中（Alpha 版本）

**作者**：@ZhenStaff

**最后更新**：2026-03-05