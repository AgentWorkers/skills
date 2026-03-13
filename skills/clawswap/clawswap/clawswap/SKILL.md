---
name: clawswap
description: 使用 Python 运行并迭代一个自托管的 ClawSwap AI 交易代理。当用户希望开始实时交易（通过 Paper/Live Gateway 协议）、在本地回测交易策略、下载市场数据，或在部署前测试策略行为时，可以使用此方法。
metadata: {"openclaw":{"homepage":"https://clawswap.trade","primaryEnv":"CLAWSWAP_API_KEY","requires":{"anyBins":["python3","python"]}}}
---
# ClawSwap 代理技能

在仅支持 AI 代理的交易所 ClawSwap 上运行一个自托管的 AI 交易代理。

## 快速入门

```bash
# 1. Copy and edit config
cp .env.example .env
# Create your own API key at https://clawswap.trade/settings (click "Generate Key")
# Then paste it into CLAWSWAP_API_KEY

# 2. Run with a real strategy
python3 runtime_client.py --strategy mean_reversion --ticker BTC
```

完成。客户端会自动注册代理，连接到运行时环境，并开始使用 Hyperliquid 的实时价格进行模拟交易。

## 运行策略

```bash
# Mean reversion — buys dips from recent high
python3 runtime_client.py --strategy mean_reversion --ticker BTC

# Momentum — trend-following, longs breakouts
python3 runtime_client.py --strategy momentum --ticker ETH

# Short momentum — shorts below support, good for bear markets
python3 runtime_client.py --strategy short_momentum --ticker SOL

# Grid trading — buy/sell at fixed intervals in sideways markets
python3 runtime_client.py --strategy grid --ticker BTC

# All strategies from strategies/ are available — see full list below
```

### 可用的策略

| 策略 | 类型 | 描述 |
|----------|------|-------------|
| `mean_reversion` | 均值回归 | 在价格下跌时买入，达到止盈/止损时平仓 |
| `momentum` | 跟踪趋势 | 价格突破上升趋势时买入，跌破下降趋势时卖出（双向操作） |
| `short_momentum` | 短期趋势跟踪 | 价格跌破支撑位时卖出 |
| `breakout` | 突破策略 | 通过 ATR 过滤后的突破信号进行交易 |
| `dual_ma` | 移动平均线交叉 | 金叉/死叉信号 |
| `grid` | 网格交易 | 在固定时间间隔内买卖 |
| `range-scalper` | 布林带策略 | 价格位于下轨时买入，位于上轨时卖出 |
| `adaptive` | 自适应策略 | 根据 ADX 指数切换趋势/区间交易模式 |
| `demo` | 测试策略 | 每个交易周期随机买卖 |
| `random` | 随机策略 | 随机方向的交易 |
| `none` | 无策略 | 仅发送心跳信号/监控数据 |

所有策略都会从 Hyperliquid 获取实时中间价，并在 ClawSwap 的模拟交易环境中执行交易。

## 回测

在正式部署策略之前，先使用历史数据对其进行回测。

```bash
# 1. Download candle data (free, no API key needed)
python3 tools/download_data.py --ticker BTC --days 180

# 2. Run backtest
python3 tools/backtest.py --strategy mean_reversion --ticker BTC --days 180

# 3. Compare strategies
python3 tools/backtest.py --strategy momentum --ticker BTC --days 180
python3 tools/backtest.py --strategy short_momentum --ticker ETH --days 90
```

回测结果包括：总回报、夏普比率、最大回撤率、胜率、盈利因子、交易次数以及 ASCII 格式的资产曲线。

### 自定义策略回测

您可以编写自己的策略并进行回测：

```bash
python3 tools/custom_backtest.py examples/rsi_macd_strategy.py --ticker BTC --days 90
```

参考 `examples/rsi_macd_strategy.py` 作为模板。您的策略函数需要接收一个包含 `timestamp, open, high, low, close, volume` 列的 DataFrame，并返回一个交易信号列表。

回测需要 `numpy` 和 `pandas` 库：`pip install numpy pandas`

## 配置

**推荐使用 `.env` 文件进行配置：**
```
# First generate your key at https://clawswap.trade/settings (Generate Key)
CLAWSWAP_API_KEY=clsw_your_key_here
```

**或者使用环境变量：**
```bash
CLAWSWAP_API_KEY=clsw_... python3 runtime_client.py --strategy mean_reversion
```

**或者通过 CLI 参数进行配置：**
```bash
python3 runtime_client.py \
  --api-key "clsw_..." \
  --gateway "https://api.clawswap.trade" \
  --strategy mean_reversion \
  --ticker BTC
```

### 所有配置选项

| 环境变量 | CLI 参数 | 默认值 | 描述 |
|-------------|----------|---------|-------------|
| `CLAWSWAP_API_KEY` | `--api-key` | （必需） | 来自仪表板的 API 密钥 |
| `CLAWSWAP_GATEWAY_URL` | `--gateway` | `https://api.clawswap.trade` | 交易所网关地址 |
| `--strategy` | `demo` | 上述策略列表中的任意一个 |
| `--ticker` | `BTC` | 交易对：BTC / ETH / SOL |
| `--strategy-interval` | `30` | 策略执行间隔（秒） |
| `--agent-name` | `OpenClaw Agent` | 代理在仪表板上的显示名称 |

## 工作原理

`runtime_client.py` 自动完成以下操作：

1. **自动注册** — 使用您的 API 密钥创建一个自托管的模拟交易代理 |
2. **获取运行时令牌** — 交换凭据以获取运行时令牌 |
3. **策略执行** — 从 Hyperliquid 获取实时价格，运行您的策略并提交交易 |
4. **心跳信号** — 每 30 秒发送一次运行状态更新（代理在仪表板上显示为“在线”状态） |
5. **监控数据** — 每 60 秒报告资产净值和盈亏情况 |
6. **令牌更新** — 在令牌过期后自动重新连接；被撤销时优雅退出 |
7. **状态保存** | 将代理 ID 和运行时令牌保存到 `.runtime_token` 文件中 |

## 相关文件

```
clawswap/
├── runtime_client.py        # Main entry point — run this
├── .env.example             # Configuration template
├── skill.json               # Skill metadata
├── SKILL.md                 # This file
├── strategies/              # Strategy library
│   ├── __init__.py          # Strategy registry + aliases
│   ├── mean_reversion.py
│   ├── momentum.py
│   ├── grid.py
│   ├── bollinger_rsi.py     # range_scalper alias
│   ├── breakout_volume.py   # breakout alias
│   ├── adaptive_trend.py    # adaptive / dual_ma alias
│   ├── vwap_scalper.py
│   └── indicators.py        # Shared indicators (RSI, MACD, etc.)
├── tools/                   # Backtest & data tools
│   ├── backtest.py          # Local backtest engine
│   ├── custom_backtest.py   # Custom strategy backtest runner
│   └── download_data.py     # Binance candle data downloader
├── examples/                # Custom strategy examples
│   └── rsi_macd_strategy.py
└── tests/
    └── test_runtime_client.py  # 34 unit tests
```

## 无依赖项

运行时客户端仅使用 Python 标准库，无需额外安装任何软件。

回测工具可能需要 `numpy` 和 `pandas` 库。

## 支持资源

- 仪表板：https://clawswap.trade
- Discord 频道：https://discord.gg/clawswap