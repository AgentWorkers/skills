---
name: taco
description: "通过 API 与 Taco 加密货币交易平台进行交互。用户可以使用该 API 来执行以下操作：  
(1) 获取 Kline 图表/蜡烛图市场数据；  
(2) 查看账户余额和持仓情况；  
(3) 开立永续合约；  
(4) 关闭永续合约；  
(5) 更新现有持仓的止盈/止损设置；  
(6) 计算技术指标（EMA、MACD、RSI、ATR、Bollinger Bands、DonchianChannel）；  
(7) 执行任何与 Taco 平台相关的交易操作。  
支持的交易所包括：Binance、Hyper、Aster、Grvt、StandX、Lighter。"
---
# Taco交易平台

## 设置

配置信息存储在`~/.openclaw/workspace/taco/config.json`文件中。每个交易所都对应一个唯一的`trader_id`：

```json
{
  "user_id": "<taco user id>",
  "api_token": "<taco api key>",
  "trader_ids": {
    "StandX": "<trader id for StandX>",
    "Binance": "<trader id for Binance>",
    "Hyper": "<trader id for Hyper>",
    "Lighter": "<trader id for Lighter>",
    "Aster": "<trader id for Aster>",
    "Grvt": "<trader id for Grvt>"
  }
}
```

**关键概念：**交易所与`trader_id`之间存在一对一的绑定关系。在操作特定交易所时，命令行界面（CLI）会自动使用配置文件中对应的`trader_id`。请仅配置您实际使用的交易所。

**首次设置：**如果配置文件不存在，请用户提供他们的`user_id`、`api_token`以及每个交易所的`trader_id`，然后将该JSON文件写入`~/.openclaw/workspace/taco/config.json`（必要时创建相应的目录）。或者，您可以运行交互式的初始化命令：

```bash
$PYTHON scripts/taco_client.py init
```

**在调用任何API之前：**请检查`~/.openclaw/workspace/taco/config.json`文件是否存在。如果不存在，请先指导用户完成配置。

## Python要求

在运行任何命令之前，需要检测系统中是否安装了Python 3：

```bash
command -v python3 || command -v python
```

- 如果系统安装了`python3`，则使用`python3`（并使用`pip3`来安装第三方包）；
- 如果系统仅安装了`python`，请通过`python --version`确认其版本是否为Python 3；如果是Python 2.x，则视为未安装Python 3；
- 如果系统中没有Python 3，请用户先安装Python 3后再继续操作。

接下来，请检查`requests`包是否可用：执行`$PYTHON -c "import requests"`。如果无法导入`requests`，则需要使用`pip3 install requests`（如果系统中只有`pip`，则使用`pip install requests`）。

**在以下所有示例中，`$PYTHON`代表系统检测到的Python版本。**请将检测结果保存在会话中，并在后续的所有调用中重复使用该值。

## 使用方法

在`scripts/taco_client.py`文件中运行CLI客户端（该文件位于当前技能目录的相对路径下）。该脚本需要`requests` Python包。配置文件默认位于`~/.openclaw/workspace/taco/config.json`（可以通过`--config <path>`参数进行自定义）。

### 获取K线数据（无需认证）

```bash
$PYTHON scripts/taco_client.py kline \
  --symbol BTCUSDT --interval 1h --exchange Binance
```

可选参数：
- `--start-time <unix_ms>`：开始时间（以微秒为单位）
- `--end-time <unix_ms>`：结束时间（以微秒为单位）
- 每次请求最多返回100条K线数据

支持的时间间隔：`1m`、`3m`、`5m`、`15m`、`30m`、`1h`、`2h`、`4h`、`6h`、`8h`、`12h`、`1d`、`3d`、`1w`、`1M`

### 检查账户信息

```bash
$PYTHON scripts/taco_client.py account --exchange Binance
```

返回指定交易所的交易者的可用余额、总资产、已使用保证金以及未平仓头寸信息。

### 开仓

```bash
$PYTHON scripts/taco_client.py open \
  --exchange Binance --symbol BTCUSDT --notional 100 --long --leverage 3 \
  --sl-price 80000 --tp-price 100000
```

- 使用`--long`参数表示开多仓；省略该参数表示开空仓
- `--sl-price`和`--tp-price`为可选参数
- `--leverage`的默认值为1.0

### 平仓

```bash
$PYTHON scripts/taco_client.py close \
  --exchange Binance --symbol BTCUSDT --notional 100 --long
```

- 使用`--long`参数表示平多仓；省略该参数表示平空仓

### 更新止盈/止损价格

```bash
# Update take-profit price
$PYTHON scripts/taco_client.py update-tp-sl \
  --exchange Binance --symbol BTCUSDT --price 100000 --take-profit

# Update stop-loss price
$PYTHON scripts/taco_client.py update-tp-sl \
  --exchange Binance --symbol BTCUSDT --price 80000
```

- 使用`--take-profit`参数更新止盈价格；省略该参数表示不更新止盈价格
- `--price`参数表示新的触发价格

### 计算技术指标（无需认证）

该功能会获取K线数据并计算技术指标。支持的指标类型包括：`EMA`、`MACD`、`RSI`、`ATR`、`BollingerBands`、`DonchianChannel`。

```bash
# EMA (Exponential Moving Average)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type EMA --period 20

# MACD (Moving Average Convergence Divergence)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type MACD \
  --fast 12 --slow 26 --signal 9

# RSI (Relative Strength Index)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 4h --type RSI --period 14

# ATR (Average True Range)
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1d --type ATR --period 14

# Bollinger Bands
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type BollingerBands \
  --period 20 --std-dev 2.0

# Donchian Channel
$PYTHON scripts/taco_client.py indicator \
  --exchange Binance --symbol BTCUSDT --interval 1h --type DonchianChannel --period 20
```

参数说明：
- `--type`：必需参数，可选值为`EMA`、`MACD`、`RSI`、`ATR`、`BollingerBands`、`DonchianChannel`之一
- `--period`：指标的计算周期（默认值因指标类型而异：EMA=20、RSI=14、ATR=14、BollingerBands=20、DonchianChannel=20）
- `--fast`、`--slow`、`--signal`：MACD指标特有的参数（默认值分别为12、26、9）
- `--std-dev`：BollingerBand的标准差倍数（默认值：2.0）
- `--limit N`：仅显示最后N个计算结果（默认值：显示所有结果）
- `--start-time`、`--end-time`：可选参数，与获取K线数据的时间范围相同

## 支持的交易所

`Binance`、`Hyper`、`Aster`、`Grvt`、`StandX`、`Lighter`

## API详细信息

有关完整的API端点文档和响应格式，请参阅[references/api-references.md]。