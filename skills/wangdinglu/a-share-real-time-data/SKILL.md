---
name: mootdx-china-stock-data
description: 通过 mootdx/TDX 协议获取中国 A 股市场的数据（包括条形图、实时报价以及逐笔交易记录）。适用于处理中国股票数据、mootdx 库、TDX 报价、日内分钟级数据、交易历史记录或实时 A 股市场数据时。
---

# Mootdx China A-Share Stock Data Client

这是一个基于 `mootdx` 库（TDX 协议）的封装层，用于获取中国 A 股市场的数据，包括 K 线图、实时报价以及逐笔交易记录。

## 安装

```bash
pip install mootdx
```

> `mootdx` 在内部依赖于 `tdxpy`，两者需要一起安装。

### 验证与演示

```bash
python scripts/setup_and_verify.py           # Install + verify + connectivity test
python scripts/setup_and_verify.py --check   # Verify only (skip install)
python scripts/setup_and_verify.py --demo    # Full API demo with real output
```

`--demo` 模式会测试所有的主要 API 并输出实时数据，可作为正确调用方式的参考。

## 关键注意事项：时间与时区

### 交易时间（北京时间，UTC+8）

| 交易时段 | 时间 |
|---------|------|
| 早晨 | 09:30 - 11:30 (120 分钟) |
| 午休时间 | 11:30 - 13:00 |
| 下午 | 13:00 - 15:00 (120 分钟) |
| **总计** | **每天 240 分钟的交易时间** |

### 交易时间绕过补丁

**问题**：`mootdx` / `tdxpy` 内置了 `time_frame()` 检查机制，会在非交易时段阻止 API 调用。在非北京时间时区的服务器上，即使在有效交易时段内也会出现此问题。

**解决方案**：对 `tdxpy.hq.time_frame` 进行修改，使其始终返回 `True`：

```python
import tdxpy.hq
tdxpy.hq.time_frame = lambda: True
```

该补丁会在 `MootdxClient.__init__()` 被自动应用。如果不使用此补丁，`transactions()` 和 `transaction()` 方法在非交易时段会返回空结果。

### 交易日历

在查询历史数据时，务必检查日期是否为交易日。非交易日（周末、节假日）没有数据。客户端使用 `TradingCalendarStrategy.is_trading_day(date_str)` 来判断交易日——你需要一个可用的交易日历服务。

### 日期/时间参数格式

| 参数 | 格式 | 示例 |
|-----------|--------|---------|
| `date` | `YYYYMMDD` | `"20250210"` |
| `time` | `HH:MM:SS` 或 `HH:MM` | `"10:30:00"` 或 `"10:30"` |

## 股票代码格式

`mootdx` 使用 **纯数字代码**（TDX 格式）。请按照以下规则进行转换：

| 标准格式 | TDX 格式 | 市场 |
|----------------|------------|--------|
| `000001.SZ` | `000001` | 深圳 |
| `600300.SH` | `600300` | 上海 |
| `300750.SZ` | `300750` | 深圳（创业板） |
| `688001.SH` | `688001` | 上海（STAR） |

**转换方法**：去掉 `.SH` / `.SZ` / `.BJ` 后缀。

> **重要提示**：`mootdx` 不支持北京证券交易所（`.BJ`）的股票。在调用相关接口前请先过滤掉这些股票。

## API 参考

### 1. 初始化客户端

```python
from mootdx.quotes import Quotes
client = Quotes.factory(market='std')
```

### 2. `get_bars()` — K 线图数据

获取历史或实时的 K 线图数据。

```python
await client.get_bars(
    stock_code="000001.SZ",   # Standard format (auto-converted)
    frequency=7,               # K-line period (see table below)
    offset=240,                # Number of bars to fetch
    date="20250210",           # Optional: specific date (YYYYMMDD)
    time="10:30:00",           # Optional: specific time (HH:MM:SS)
    filter_by_time=True        # Filter to closest bar matching time
)
```

**频率代码**：

| 代码 | 周期 |  
|------|--------|  
| 7   | 1 分钟的 K 线图 |  
| 8   | 1 分钟的 K 线图（备用格式）|  
| 4   | 日线图   |  
| 9   | 日线图（备用格式）|  

**返回格式**（字典列表）：

```python
{
    "stock_code": "000001.SZ",
    "datetime": "2025-02-10 10:30:00",
    "open": 12.50,
    "high": 12.65,
    "low": 12.45,
    "close": 12.60,
    "vol": 150000.0,
    "amount": 1890000.0
}
```

**起始位置计算**：对于历史数据，`start` 参数会根据当前时间与目标日期之间的交易分钟数（1 分钟 K 线图）或交易天数（日线图）来计算。计算时会考虑以下因素：
- 当前是否为交易日  
- 当前的交易时段（盘前/盘中/盘后）  
- 午休时间的间隔（11:30-13:00）

### 3. `get_realtime_quote()` — 单股实时报价

```python
await client.get_realtime_quote(stock_code="000001.SZ")
```

**返回值**（字典）：价格、开盘价（OHLC）、成交量、交易量以及完整的二级订单簿（5 个价格等级的买卖订单）：

```python
{
    "stock_code": "000001.SZ",
    "price": 12.60,
    "last_close": 12.50,
    "open": 12.45, "high": 12.65, "low": 12.40,
    "volume": 5000000, "amount": 63000000,
    "bid1": 12.59, "bid2": 12.58, ..., "bid5": 12.55,
    "ask1": 12.60, "ask2": 12.61, ..., "ask5": 12.65,
    "bid_vol1": 500, ..., "ask_vol5": 300,
    "pct_chg": 0.8
}
```

### 4. `get_realtime_quotes()` — 批量实时报价

提供批量处理的接口，比循环调用 `get_realtime_quote()` 更快。

```python
await client.get_realtime_quotes(["000001.SZ", "600300.SH", "300750.SZ"])
```

**返回值**（字典列表）：

```python
{
    "stock_code": "000001.SZ",
    "trade_date": "2025-02-10",
    "open": 12.45, "high": 12.65, "low": 12.40, "close": 12.60,
    "pre_close": 12.50,
    "change": 0.15,
    "pct_chg": 1.2048,
    "vol": 5000000.0,
    "amount": 63000000.0,
    "is_realtime": true
}
```

> `pctchg` 是根据 **当天的开盘价** 计算的，而非前一天的收盘价。

### 5. `get_batch_bars()` — 批量 K 线图数据

并行获取多只股票的 K 线图数据，并支持并发控制。

```python
await client.get_batch_bars(
    stock_codes=["000001.SZ", "600300.SH"],
    date="20250210",
    time="10:30:00",
    max_concurrent=10
)
```

**返回值**：`Dict[str, List[Dict]]` — `{stock_code: [bar_data, ...]}`

### 6. `get_transactions_history()` — 历史交易记录

获取指定历史日期的逐笔交易记录。

```python
await client.get_transactions_history(
    stock_code="000001.SZ",
    date="20250210",         # Required: YYYYMMDD
    start=0,
    offset=1000
)
```

**返回值**（字典列表）：

```python
{
    "stock_code": "000001.SZ",
    "time": "09:30:05",
    "price": 12.50,
    "vol": 100,
    "buyorsell": 0,          # 0=buy, 1=sell, 2=neutral
    "num": 5,                # Number of trades in this tick
    "volume": 100
}
```

### 7. `get_transactions_realtime()` — 实时逐笔交易数据

获取当天的实时逐笔交易数据。

```python
await client.get_transactions_realtime(
    stock_code="000001.SZ",
    start=0,
    offset=1000
)
```

返回格式与 `get_transactions_history()` 相同。

### 8. `get_transactions_with_fallback()` — 带有回退机制的实时数据

首先尝试获取实时数据，如果实时数据为空，则回退到当天的历史数据。

```python
await client.get_transactions_with_fallback(
    stock_code="000001.SZ",
    start=0, offset=1000,
    use_history_fallback=True
)
```

## 原始的 `mootdx` API（低级接口）

如果直接使用 `mootdx` 而不使用此封装层：

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')

# K-line bars
df = client.bars(symbol="000001", frequency=7, start=0, offset=240)

# Real-time quotes (supports list of symbols for batch)
df = client.quotes(symbol="000001")
df = client.quotes(symbol=["000001", "600300"])

# Historical transactions
df = client.transactions(symbol="000001", start=0, offset=1000, date="20250210")

# Real-time transactions
df = client.transaction(symbol="000001", start=0, offset=1000)
```

> 所有原始 API 都返回 **pandas DataFrame**。

## 常见问题

1. **非交易时段返回空结果**：请应用上述的 `time_frame` 补丁。
2. **北京证券交易所的股票**：不支持 `.BJ` 格式的股票代码，请在调用前过滤掉它们。
3. **请求速率限制**：默认的请求间隔为 0.005 秒；如果网络连接不稳定，请适当调整。
4. **周末/节假日查询**：在查询前务必验证日期是否为交易日。
5. **1 分钟 K 线图的起始时间计算**：需要考虑每天 240 分钟的交易时间以及午休时间的影响。

## 额外资源

- 有关详细的 API 方法签名和时间计算逻辑，请参阅 [api-reference.md](api-reference.md)。