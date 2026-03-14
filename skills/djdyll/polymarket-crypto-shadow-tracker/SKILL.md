---
name: polymarket-crypto-shadow-tracker
description: 别再猜测哪种加密货币策略有效了。在 Polymarket 上同时测试所有策略（包括 BTC、ETH、XRP、SOL），覆盖不同的时间框架和阈值。然后根据实际数据（而非主观感觉）来选择最有效的策略，并将其投入实际交易中。这才是那些认真交易者所缺失的“回测功能”啊。
metadata:
  author: "DjDyll"
  version: "1.0.0"
  displayName: "Polymarket Crypto Shadow Tracker"
  difficulty: "intermediate"
---
# Polymarket 加密货币影子交易追踪器（Crypto Shadow Tracker）

每个策略在头脑中看起来都很不错，但实际应用前都需要先进行验证。这个工具允许你在 Polymarket 的加密快速市场中测试各种策略参数组合——无需承担任何资金风险——只有在数据证明策略有效时，才会正式推广该策略。

## 功能概述

1. **发现** 可用于交易的加密快速市场（通过 Simmer API 的 `get_fast_markets(asset=, window=)` 函数）。
2. **评估** 每个市场是否符合你的策略插件所设定的信号逻辑。
3. **记录** 每种策略组合的模拟交易结果——实际资金不会流入区块链。
4. **处理** 交易结果（通过相应的 API 端点）。
5. **根据胜率和预期收益对策略组合进行排名**，找出真正有效的策略。
6. **在策略满足统计标准时**，将其推广为正式使用的策略。

## 启动模板插件

随附的 `crypto_momentum_plugin.py` 是你的起点：只需将你的信号逻辑代码添加到其中，定义参数范围，其余工作都由该框架完成。

### 快速入门

```bash
# Shadow-trade BTC/ETH momentum variants
python shadow_tracker.py run -s crypto_momentum_plugin.py

# Resolve outcomes
python shadow_tracker.py resolve -s crypto_momentum_plugin.py

# Compare variants
python shadow_tracker.py stats -s crypto_momentum_plugin.py

# Find the best variant
python shadow_tracker.py promote -s crypto_momentum_plugin.py
```

### 自动运行模式

将 `SHADOW_crypto_PLUGIN` 设置为 `crypto_momentum_plugin.py`，然后直接运行程序，框架会自动执行 `run` 和 `resolve` 操作。

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|------|---------|---------|-------------|
| `max_trades_per_run` | `SHADOW_crypto_MAX_TRADES` | 每次运行最多记录的模拟交易数量 |
| `min_volume` | `SHADOW_crypto_MIN_VOLUME` | 24 小时最低交易量阈值 |
| `data_dir` | `SHADOW_DATA_DIR` | 交易日志存储目录 |
| `plugin` | `SHADOW_crypto_PLUGIN` | 策略插件的路径（必须以 `.py` 结尾） |

```bash
# View config
python shadow_tracker.py --config

# Update config
python shadow_tracker.py --set max_trades_per_run=20
```

## 编写自定义插件

你需要从 `shadow_plugin_base.py` 继承 `StrategyPlugin` 类，并根据需求实现具体功能。

```python
from shadow_plugin_base import StrategyPlugin, TradeSignal, ShadowTrade

class MyStrategy(StrategyPlugin):
    name = "my_crypto_strategy"
    default_params = {"coin": "BTC", "threshold": 0.05}
    param_grid = {"coin": ["BTC", "ETH"], "threshold": [0.03, 0.05, 0.08]}

    # Promotion thresholds
    min_n = 30
    min_wr = 0.58
    min_ev_delta = 0.02

    def get_markets(self, client=None):
        """Fetch markets. Use client.get_fast_markets() for crypto."""
        markets = client.get_fast_markets(asset="BTC", window="15m", limit=50)
        return [{"id": m.id, "price": m.current_probability, ...} for m in markets]

    def evaluate(self, market, params):
        """Return TradeSignal or None."""
        ...

    def is_win(self, trade, market=None):
        """Return True/False/None. Resolution also handled by framework."""
        ...
```

### 插件接口

| 方法 | 返回值 | 作用 |
|--------|---------|---------|
| `get_markets(client)` | `list[dict]` | 获取符合条件的市场列表 |
| `evaluate(market, params)` | `TradeSignal \| None` | 为指定的市场和参数组合生成交易信号 |
| `is_win(trade, market)` | `bool \| None` | 判断交易结果是否成功（若失败，框架会使用内置的 API 处理） |

### 快速市场的字段（来自 Simmer SDK）

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `m.id` | str | Simmer 平台的市场 ID |
| `m.question` | str | 市场的相关描述文本 |
| `m.current_probability` | float | 当前价格（0-1 表示价格高低） |
| `m.resolves_at` | str | 交易结果确定的 ISO 时间戳 |
| `m.is_live_now` | bool | 市场是否当前可交易 |
| `m.spread_cents` | float | 当前价差（以分为单位） |
| `m_external_price_yes` | float | 外部参考价格 |
| `m.liquidity_tier` | str | 市场的流动性等级 |

## 所需依赖

- `simmer-sdk`（可通过 pip 安装）
- 环境变量 `SIMMER_API_KEY`（用于访问 Simmer API）