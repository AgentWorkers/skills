---
name: crypto-regime-report
description: 使用 Supertrend 和 ADX 指标为加密货币永续合约生成市场分析报告。当用户请求市场状况检查、市场报告、趋势分析或定时的早晨/晚间加密货币更新时，可以使用该报告。报告内容包括价格走势、趋势方向/强度、资金费率、未平仓合约数量（open interest）、成交量分析以及可配置观察列表中各合约与 BTC 的相关性数据。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3", "curl", "uvx", "jq"]
---

# 加密货币市场状况报告

该工具使用技术指标生成加密货币永续期货的市场状况报告。

## 快速入门

```bash
# Run a daily regime report
python3 {baseDir}/scripts/regime_report.py

# Run a weekly regime report
python3 {baseDir}/scripts/regime_report.py --weekly
```

或者直接提问：“BTC的市场状况如何？”或“运行一份市场报告。”

---

## 报告内容

**价格与趋势：**
- 当前价格及24小时价格变化
- 市场状况分类（强涨/强跌、弱涨/弱跌、盘整）
- ADX值（趋势强度）
- 趋势方向（根据超级趋势判断为上涨/下跌）
- 与超级趋势线的偏离程度（百分比）

**成交量与流动性：**
- 成交量与20日均值的对比（百分比）
- 🔇 = 成交量低，🔊 = 成交量高

**永续期货数据：**
- 垂直保证金费率及其变化方向（↑↓→）
- 开仓量（当前值，单位：美元）
- 🔥 = 垂直保证金费率升高

**市场环境：**
- BTC与其他资产的相关性（0.0至1.0）
- 🔗 = 高相关性（> 0.7）

---

## 设置指南

### 1. 配置你的观察列表

**选项A：编辑默认配置**

编辑 `{baseDir}/references/config.json` 以自定义你的资产列表：

```json
{
  "watchlist": [
    {"symbol": "BTC", "name": "Bitcoin", "okx": "BTC-USDT-SWAP"},
    {"symbol": "ETH", "name": "Ethereum", "okx": "ETH-USDT-SWAP"}
  ],
  "indicators": {
    "supertrend": { "period": 10, "multiplier": 3 },
    "adx": { "period": 14, "strong_threshold": 25, "weak_threshold": 20 }
  }
}
```

**选项B：使用自定义配置文件**

示例配置文件位于 `{baseDir}/references/config.example.json` — 请根据需要复制并修改。

**配置字段：**
- `symbol` — 简短代码（用于显示）
- `name` — 完整名称（用于显示）
- `okx` — OKX上的永续期货代码（必须符合OKX的格式：`ASSET-USDT-SWAP`）

**查找OKX期货代码的方法：** 访问 [OKX市场页面](https://www.okx.com/markets) 或使用以下命令：
```bash
curl -s "https://www.okx.com/api/v5/public/instruments?instType=SWAP" | jq '.data[].instId'
```

### 2. 配置指标参数

在 `config.json` 中进行设置：

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `supertrend.period` | 10 | ATR计算的回顾周期 |
| `supertrend.multiplier` | 3.0 | 用于计算趋势带宽的ATR倍数 |
| `adx.period` | 14 | ADX计算的回顾周期 |
| `adx.strong_threshold` | 25 | 判断“强趋势”的ADX阈值 |
| `adx.weak_threshold` | 20 | 判断“弱趋势”的ADX阈值 |

### 3. 设置定期报告（可选）

使用OpenClaw的定时任务系统自动接收报告。

**通过CLI执行：**

```bash
# Morning report (6am PST)
openclaw cron add \
  --name "Morning Regime Report" \
  --schedule "0 6 * * *" \
  --timezone "America/Los_Angeles" \
  --message "Run the crypto regime morning report"

# Evening report (3pm PST)
openclaw cron add \
  --name "Evening Regime Report" \
  --schedule "0 15 * * *" \
  --timezone "America/Los_Angeles" \
  --message "Run the crypto regime evening report"

# Friday weekly summary (4pm PST)
openclaw cron add \
  --name "Friday Weekly Summary" \
  --schedule "0 16 * * 5" \
  --timezone "America/Los_Angeles" \
  --message "Run the crypto regime weekly report with --weekly flag"
```

**通过配置文件（`~/.openclaw/openclaw.json`）设置：**

```json5
{
  // ... other config ...
  "cron": {
    "jobs": [
      {
        "name": "Morning Regime Report",
        "schedule": { "kind": "cron", "expr": "0 6 * * *", "tz": "America/Los_Angeles" },
        "sessionTarget": "isolated",
        "payload": { "kind": "agentTurn", "message": "Run the crypto regime morning report and send it to Telegram" },
        "delivery": { "mode": "announce" }
      },
      {
        "name": "Evening Regime Report",
        "schedule": { "kind": "cron", "expr": "0 15 * * *", "tz": "America/Los_Angeles" },
        "sessionTarget": "isolated",
        "payload": { "kind": "agentTurn", "message": "Run the crypto regime evening report and send it to Telegram" },
        "delivery": { "mode": "announce" }
      },
      {
        "name": "Friday Weekly Summary",
        "schedule": { "kind": "cron", "expr": "0 16 * * 5", "tz": "America/Los_Angeles" },
        "sessionTarget": "isolated",
        "payload": { "kind": "agentTurn", "message": "Run the crypto regime weekly report with --weekly flag and send it to Telegram" },
        "delivery": { "mode": "announce" }
      }
    ]
  }
}
```

### 4. 测试报告功能

```bash
# Test daily report
python3 {baseDir}/scripts/regime_report.py

# Test weekly report
python3 {baseDir}/scripts/regime_report.py --weekly
```

---

## 功能说明

1. 从OKX获取观察列表中每个资产的OHLCV数据
2. 计算超级趋势以确定市场方向
3. 计算ADX值以衡量趋势强度
4. 获取当前的垂直保证金费率及开仓量
5. 生成格式化的报告，适用于通过Telegram发送

---

## 使用的指标

### 超级趋势（Supertrend，参数：10, 3）
- **周期（Period）**：10
- **倍数（Multiplier）**：3
- **上涨趋势（Bullish）**：价格高于超级趋势线
- **下跌趋势（Bearish）**：价格低于超级趋势线

### ADX（平均方向指数，Average Directional Index）
- **> 25**：强趋势（上涨或下跌）
- **20-25**：弱/中等趋势
- **< 20**：无明显趋势/盘整

## 市场状况分类

| 超级趋势（Supertrend） | ADX值 | 市场状况（Regime） |
|------------|-----|--------|
| 上涨趋势（Bullish） | > 25 | 强涨 |
| 上涨趋势（Bullish） | 20-25 | 弱涨 |
| 下跌趋势（Bearish） | > 25 | 强跌 |
| 下跌趋势（Bearish） | 20-25 | 弱跌 |
| 两者均不符合（Either） | < 20 | 盘整 |

---

## 数据来源

| 数据类型 | 来源 | 备注 |
|------|--------|-------|
| 日度OHLCV数据 | OKX API | 免费，无需密钥 |
| 周度OHLCV数据 | Yahoo Finance | 提供11年以上的历史数据，可作为OKX数据的备用来源 |
| 垂直保证金费率 | OKX API | 免费，无需密钥 |
| 开仓量 | OKX API | 免费，无需密钥 |

**OKX API接口：**
- OHLCV：`/api/v5/market/candles`
- 垂直保证金费率：`/api/v5/public/funding-rate`
- 开仓量：`/api/v5/public/open-interest`

---

## 相关资源

### 脚本（Scripts）：
- `regime_report.py` — 主脚本，用于获取数据并生成报告

### 参考文件（References）：
- `config.json` — 默认观察列表配置文件（可编辑以自定义）
- `config.example.json` — 可供参考的自定义配置文件