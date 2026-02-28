---
name: nautilus-trader
description: NautilusTrader 是一个用于策略开发和实时交易的算法交易平台。适用于构建交易策略、回测，或将其部署到 Hyperliquid 平台。
version: "2.0.0"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---
# Nautilus Trader 技能

提供全面的 NautilusTrader 开发支持，包括与 Hyperliquid 主网的完整集成以及用于实时交易的 SDK 修补程序。

---

## 概述

本技能涵盖以下内容：

- 使用 NautilusTrader 开发交易策略
- 使用 Parquet 数据目录进行回测
- 在 Hyperliquid 主网上进行实时交易
- 适用于 Hyperliquid 价格精度要求的 SDK 修补程序

### 适用场景

- 使用 NautilusTrader 构建交易策略
- 使用历史数据进行回测
- 将策略部署到 Hyperliquid 主网
- 调试 NautilusTrader 适配器的问题
- 使用多时间框架（MTF）指标

---

## 先决条件

### 核心依赖项

```bash
# NautilusTrader (backtesting + live trading framework)
pip install nautilus_trader

# Hyperliquid SDK (for live trading patch)
pip install hyperliquid-python-sdk eth-account python-dotenv

# Data handling
pip install pandas numpy
```

### 验证安装

```python
import nautilus_trader
print(f"Nautilus Trader: {nautilus_trader.__version__}")
# Tested with v1.222.0
```

### 环境变量

创建一个 `.env` 文件以存储 Hyperliquid 的凭据：

```bash
HYPERLIQUID_PK=your_private_key_without_0x_prefix
HYPERLIQUID_VAULT=0xYourVaultAddressHere
```

---

## 快速入门

### 1. 应用 Hyperliquid 修补程序（用于实时交易）

```python
# CRITICAL: Import patch BEFORE Nautilus Trader
import hyperliquid_patch

# Then import Nautilus normally
from nautilus_trader.adapters.hyperliquid import HYPERLIQUID
from nautilus_trader.live.node import TradingNode
```

### 2. 基本策略模板

```python
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.identifiers import InstrumentId
from decimal import Decimal

class MyStrategyConfig(StrategyConfig):
    instrument_id: str
    bar_type: str
    trade_size: Decimal = Decimal("0.1")

class MyStrategy(Strategy):
    def __init__(self, config: MyStrategyConfig):
        super().__init__(config)
        self.instrument_id = InstrumentId.from_str(config.instrument_id)
        self.bar_type = BarType.from_str(config.bar_type)
        self.trade_size = config.trade_size

    def on_start(self):
        self.instrument = self.cache.instrument(self.instrument_id)
        self.subscribe_bars(self.bar_type)

    def on_bar(self, bar: Bar):
        # Your strategy logic here
        pass

    def on_stop(self):
        self.close_all_positions(self.instrument_id)
```

---

## 策略开发

### Heiken Ashi 指标

```python
from nautilus_trader.indicators.base.indicator import Indicator
from nautilus_trader.model.data import Bar

class HeikenAshi(Indicator):
    """Heiken Ashi candle smoothing indicator."""

    def __init__(self):
        super().__init__([])
        self.ha_open = 0.0
        self.ha_close = 0.0
        self.ha_high = 0.0
        self.ha_low = 0.0
        self._prev_ha_open = None
        self._prev_ha_close = None
        self.initialized = False

    def handle_bar(self, bar: Bar) -> None:
        o, h, l, c = float(bar.open), float(bar.high), float(bar.low), float(bar.close)

        self.ha_close = (o + h + l + c) / 4

        if self._prev_ha_open is None:
            self.ha_open = (o + c) / 2
        else:
            self.ha_open = (self._prev_ha_open + self._prev_ha_close) / 2

        self.ha_high = max(h, self.ha_open, self.ha_close)
        self.ha_low = min(l, self.ha_open, self.ha_close)

        self._prev_ha_open = self.ha_open
        self._prev_ha_close = self.ha_close
        self.initialized = True

    @property
    def is_bullish(self) -> bool:
        return self.ha_close > self.ha_open

    @property
    def is_bearish(self) -> bool:
        return self.ha_close < self.ha_open

    def reset(self) -> None:
        self._prev_ha_open = None
        self._prev_ha_close = None
        self.initialized = False
```

### 多时间框架 EMA 策略

有关完整的 MTF EMA + Heiken Ashi 策略实现，请参阅 `references/hyperliquid.md`。

**关键概念：**

- **HTF（更高时间框架）**：通过 EMA 交叉确定趋势方向
- **LTF（更低时间框架）**：通过 Heiken Ashi 信号确定入场时机
- **入场**：当 Heiken Ashi 的颜色发生变化时
- **出场**：当 Heiken Ashi 的颜色反转时

---

## 回测

### 引擎设置

```python
from nautilus_trader.backtest.engine import BacktestEngine, BacktestEngineConfig
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from decimal import Decimal

def run_backtest():
    config = BacktestEngineConfig(
        trader_id="BACKTESTER-001",
        logging_level="INFO",
    )
    engine = BacktestEngine(config=config)

    # Add venue
    engine.add_venue(
        venue=Venue("HYPERLIQUID"),
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USD,
        starting_balances=[Money(100_000, USD)],
    )

    # Load data from catalog
    catalog = ParquetDataCatalog("./data_catalog")

    instruments = catalog.instruments()
    for instrument in instruments:
        engine.add_instrument(instrument)

    bars = catalog.bars()
    engine.add_data(bars)

    # Add strategy
    strategy = MyStrategy(config=MyStrategyConfig(
        instrument_id="SOL-USD.HYPERLIQUID",
        bar_type="SOL-USD.HYPERLIQUID-5-MINUTE-LAST-EXTERNAL",
        trade_size=Decimal("1.0"),
    ))
    engine.add_strategy(strategy)

    # Run
    engine.run()

    # Results
    print(engine.trader.generate_account_report(Venue("HYPERLIQUID")))
    print(engine.trader.generate_order_fills_report())
    print(engine.trader.generate_positions_report())

    engine.dispose()
```

### 数据目录

有关数据目录操作的详细信息，请参阅 `references/backtesting.md` 和 `references/data.md`：

- `ParquetDataCatalog`：查询和管理 Parquet 数据文件
- `BarDataWrangler`：将 pandas 数据帧转换为 Nautilus 条形图对象
- `write_data()`：将数据持久化到目录
- `query()`：使用时间过滤器检索数据

---

## 在 Hyperliquid 上进行实时交易

### 节点配置

```python
import os
from dotenv import load_dotenv

load_dotenv()

# CRITICAL: Apply patch BEFORE Nautilus imports
import hyperliquid_patch

from nautilus_trader.adapters.hyperliquid import (
    HYPERLIQUID,
    HyperliquidDataClientConfig,
    HyperliquidExecClientConfig,
)
from nautilus_trader.live.node import TradingNode, TradingNodeConfig
from nautilus_trader.config import LiveDataEngineConfig, LiveExecEngineConfig

def main():
    node_config = TradingNodeConfig(
        trader_id="LIVE-001",
        data_engine=LiveDataEngineConfig(),
        exec_engine=LiveExecEngineConfig(),
    )

    node = TradingNode(config=node_config)

    data_config = HyperliquidDataClientConfig(
        wallet_address=os.getenv("HYPERLIQUID_VAULT"),
        is_testnet=False,
    )

    exec_config = HyperliquidExecClientConfig(
        wallet_address=os.getenv("HYPERLIQUID_VAULT"),
        private_key=os.getenv("HYPERLIQUID_PK"),
        is_testnet=False,
    )

    node.build()

    # Add your strategy
    strategy = MyStrategy(config=my_config)
    node.trader.add_strategy(strategy)

    node.run()

if __name__ == "__main__":
    main()
```

### 设置杠杆（一次性设置）

```python
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account import Account
import os

private_key = os.getenv("HYPERLIQUID_PK")
if not private_key.startswith("0x"):
    private_key = "0x" + private_key

account = Account.from_key(private_key)
exchange = Exchange(account, constants.MAINNET_API_URL)

# Set 10x leverage for SOL (cross margin)
exchange.update_leverage(10, "SOL", is_cross=True)
```

### 网络延迟

为了获得最佳性能，请部署在 AWS ap-northeast-1（东京）：

- 对 Hyperliquid CloudFront 的 ping 响应时间约为 1ms
- API 延迟约为 28ms

---

## Hyperliquid SDK 修补程序

### 问题

Nautilus Trader v1.222.0 的 Hyperliquid 适配器存在以下问题：

1. Rust HTTP 客户端的序列化导致类型不匹配
2. 价格精度超过了 Hyperliquid 的 5 位有效数字限制

### 解决方案

使用官方的 Hyperliquid Python SDK 来绕过有问题的适配器。修补程序文件位于 `references/hyperliquid_patch.py`。

### 价格精度规则

Hyperliquid 要求所有价格最多保留 5 位有效数字：

| 价格       | 是否有效 | 有效位数 |
|-----------|--------|----------|
| $139.05     | 是     | 5        |
| $139.054    | 否     | 6        |
| $1.2345     | 是     | 5        |
| $1.23456    | 否     | 6        |
| $12345     | 是     | 5        |
| $123456    | 否     | 6        |

### 使用方法

```python
# CRITICAL: Import patch BEFORE any Nautilus imports
import hyperliquid_patch

# Then import Nautilus normally
from nautilus_trader.adapters.hyperliquid import HYPERLIQUID
```

该修补程序在导入时自动应用，并处理以下内容：

- 将价格格式化为 5 位有效数字
- 买入时向上取整，卖出时向下取整（确保成交）
- 基于 SDK 的订单提交绕过 Rust 客户端

### 已验证的有效性

已在 Hyperliquid 主网（2025-01-12）上进行了测试：

```
SELL 0.72 SOL @ $143.38 - FILLED
BUY 0.71 SOL @ $143.39 - FILLED
```

---

## 配置

### 文件结构

```
your_trading_project/
├── .env                        # Credentials (gitignored)
├── hyperliquid_patch.py        # SDK patch for live trading
├── heiken_ashi.py              # Heiken Ashi indicator
├── my_strategy.py              # Strategy implementation
├── backtest.py                 # Backtest runner
├── live.py                     # Live trading runner
└── data_catalog/               # Parquet data for backtesting
```

### 条形图类型格式

```
{symbol}.{venue}-{step}-{aggregation}-{price_type}-{source}

Examples:
SOL-USD.HYPERLIQUID-1-HOUR-LAST-EXTERNAL
SOL-USD.HYPERLIQUID-5-MINUTE-LAST-EXTERNAL
BTC-USD.HYPERLIQUID-15-MINUTE-LAST-EXTERNAL
```

---

## 故障排除

### 订单被拒绝：价格无效

确保价格最多保留 5 位有效数字。使用修补程序中的 `format_price_5_sigfigs()` 函数。

### 连接错误

1. 检查 `.env` 文件中的 `HYPERLIQUID_PK` 和 `HYPERLIQUID_VAULT` 是否正确
2. 验证私钥格式（是否带有 `0x` 前缀）
3. 确认金库地址是否正确

### 修补程序未应用

确保 `import hyperliquid_patch` 在导入任何 Nautilus 模块之前执行。

### 回测中数据缺失

1. 验证数据目录路径是否存在
2. 检查数据与策略配置中的工具ID是否匹配
3. 确保条形图类型格式正确

### 未平仓的头寸

检查净结算账户的出场订单是否设置了 `reduce_only=True`

---

## 参考文件

详细文档位于 `references/` 目录下：

| 文件          | 说明                        |
|--------------|---------------------------|
| `hyperliquid.md`    | 完整的 Hyperliquid 集成指南            |
| `hyperliquid_patch.py` | SDK 修补程序的源代码                |
| `strategies.md`    | 交易策略和示例                    |
| `backtesting.md`    | 数据目录和回测 API                   |
| `data.md`      | 数据处理和整理                    |
| `getting_started.md` | NautilusTrader 基础知识                |
| `concepts.md`    | 核心概念和架构                    |
| `api.md`      | 完整的 API 参考                    |

需要详细信息时，可以使用 `view` 命令查看相应的参考文件。