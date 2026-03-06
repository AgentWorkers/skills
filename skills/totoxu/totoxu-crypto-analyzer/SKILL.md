---
name: crypto-market-analyzer
description: 实时获取加密货币价格，并计算 BTC、ETH、SOL、BNB、XRP、DOGE 的技术指标（SMA、EMA、MACD、RSI、Bollinger Bands、ATR）。数据来源包括 Binance、CoinGecko、CoinCap、CryptoCompare。
version: 1.0.0
author: crypto-tools
requires:
  binaries:
    - python3
  env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
metadata:
  clawdbot:
    requires:
      env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
    files:
      - "scripts/*"
---
# 加密货币市场分析工具

该工具提供了两项核心功能，用于加密货币的分析：

1. **实时市场数据**：获取当前价格、24小时价格变化、交易量以及最高/最低价格。
2. **技术指标分析**：计算专业级别的技术指标，并提供交易信号。

## 支持的加密货币

BTC、ETH、SOL、BNB、XRP、DOGE

## 依赖库

该脚本需要 `requests` Python 库。如果尚未安装，请执行以下命令进行安装：

```bash
pip install requests
```

## 计费

该工具为付费服务。每次调用费用为 **0.001 美元**，通过 SkillPay 收费。请使用 `--user` 标志传递用户 ID 以完成计费。如果用户余额不足，脚本将返回一个 `payment_url`——请将此链接提供给用户。

---

## 命令 1：获取市场数据

**使用场景**：当用户询问当前加密货币价格、市场状况或需要实时价格数据时。

### 获取当前价格

```bash
python scripts/fetch_market.py --user 用户ID --coins BTC,ETH,SOL
```

**参数说明**：
- `--coins`（必选）：用逗号分隔的加密货币符号（例如 `BTC,ETH,SOL`）
- `--user`（必选）：用于计费的用户 ID
- `--test-mode`（可选）：测试模式下跳过计费

**输出格式（JSON）**：
```json
{
  "status": "success",
  "data": {
    "BTC": {
      "price": 95432.10,
      "change_24h": 2.35,
      "high_24h": 96000.00,
      "low_24h": 93800.50,
      "volume_24h": 28500000000,
      "source": "binance"
    },
    "coins_requested": ["BTC"],
    "timestamp": 1709654321
  },
  "timestamp": 1709654321
}
```

### 获取历史价格

```bash
python scripts/fetch_market.py --user 用户ID --coins BTC --historical --days 30
```

**附加参数**：
- `--historical`：启用历史数据模式
- `--days`（默认值：30）：要分析的历史天数

**输出内容**：包含每个时间段的 OHLCV 数据（开盘价、最高价、最低价、收盘价、交易量）。

---

## 命令 2：技术指标分析

**使用场景**：当用户询问技术分析、交易信号、趋势分析、支撑/阻力位，或是否应该买入/卖出某种加密货币时。

```bash
python scripts/calc_indicators.py --user 用户ID --coin BTC --days 30
```

**参数说明**：
- `--coin`（必选）：要分析的加密货币符号（例如 `BTC`）
- `--days`（默认值：30）：数据分析的天数
- `--user`（必选）：用于计费的用户 ID
- `--test-mode`（可选）：测试模式下跳过计费

**输出格式（JSON）**：
```json
{
  "status": "success",
  "coin": "BTC",
  "current_price": 95432.10,
  "moving_averages": {
    "sma_7": 94800.50,
    "sma_14": 93200.30,
    "sma_30": 91500.00,
    "ema_12": 94600.80,
    "ema_26": 93100.20
  },
  "macd": {
    "macd_line": 1500.60,
    "signal_line": 1200.30,
    "histogram": 300.30
  },
  "rsi_14": 62.5,
  "bollinger_bands": {
    "upper": 97000.00,
    "middle": 93200.00,
    "lower": 89400.00,
    "bandwidth": 8.15,
    "position": 0.79
  },
  "atr_14": 1850.30,
  "momentum": {
    "change_7d_pct": 3.25,
    "change_30d_pct": 8.50
  },
  "volatilitypct": 2.15,
  "support_resistance": {
    "support": 89400.00,
    "resistance": 97000.00
  },
  "signals": [
    "RSI leaning bullish",
    "MACD bullish crossover → BUY signal",
    "Uptrend: Price & SMA7 above SMA30"
  ],
  "signal_score": 45,
  "overall_assessment": "STRONG BUY"
}
```

## 解释输出结果

在向用户展示结果时，请重点关注以下内容：

### 对于市场数据：
- **价格** 和 **24小时价格变化** 是最关键的信息。
- 提及 **交易量** 以了解市场活跃程度。
- 如果 `24小时价格变化` 超过 ±5%，请特别说明。

### 对于技术分析：
- **overall_assessment** 提供整体分析结果（强烈买入 / 买入 / 中立 / 卖出 / 强烈卖出）。
- **signal_score** 的范围是 -100（极度看跌）到 +100（极度看涨）。
- **signals** 数组列出了做出该评估的具体原因。
- **RSI**：<30 表示超卖（买入机会），>70 表示超买（卖出机会）。
- **MACD 直方图**：>0 表示看涨动能，<0 表示看跌动能。
- **Bollinger Band 位置**：<0.1 表示接近支撑位，>0.9 表示接近阻力位。

### 重要免责声明：

请始终提醒用户，技术指标仅用于教育/分析目的，不构成财务建议。加密货币市场波动性极高。

## 错误处理

如果脚本返回错误，请检查：
1. **支付错误**：向用户提供 `payment_url` 以补充余额。
2. **数据源错误**：所有 API 都失败了；建议稍后重试。
3. **无效的加密货币**：支持的加密货币包括 BTC、ETH、SOL、BNB、XRP、DOGE。