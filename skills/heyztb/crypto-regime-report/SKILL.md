---
name: crypto-regime-report
description: 使用 Supertrend 和 ADX 指标为加密货币永续合约生成市场分析报告。当用户请求市场状况检查、市场报告、趋势分析或定时的早晨/晚间加密货币更新时，可使用该报告。报告内容包括价格走势、趋势方向/强度、资金费率、未平仓合约量（open interest）、成交量分析以及可配置观察列表中的 BTC 相关性数据。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3", "curl"]
---
# 加密货币市场状况报告

该脚本使用技术指标为加密货币的永续期货生成市场状况报告。

## 快速入门

```bash
# Run a daily regime report
python3 {baseDir}/scripts/regime_report.py

# Run a weekly regime report
python3 {baseDir}/scripts/regime_report.py --weekly
```

或者直接询问：“BTC的市场状况如何？”或“运行一份市场报告。”

**注意：** 脚本会将格式化后的报告输出到标准输出（stdout）。代理程序负责报告的传递（例如，通过 Telegram 发送或显示在聊天界面中）。

---

## 报告内容

**价格与趋势：**
- 当前价格及24小时价格变化
- 市场状况分类（强涨/强跌、弱涨/弱跌、盘整）
- ADX 值（趋势强度）
- 趋势方向（根据 Supertrend 判断为上涨或下跌）
- 与 Supertrend 线的距离（百分比）

**成交量与流动性：**
- 成交量与20天平均值的对比（百分比）
- 🔇 = 低成交量，🔊 = 高成交量

**永续期货数据：**
- 基金费率及费率变化方向（↑↓→）
- 开仓量（当前值，单位：美元）
- 🔥 = 基金费率上升

**市场环境：**
- BTC 与其他资产的相关性（0.0 至 1.0）
- 🔗 = 高相关性（> 0.7）

---

## 设置指南

### 1. 配置你的观察列表

**选项 A：编辑默认配置**

编辑 `{baseDir}/references/config.json` 以自定义资产列表：

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

**选项 B：使用自定义配置文件**

```bash
# Via environment variable (must be relative path within skill directory)
REGIME_CONFIG=references/my-config.json python3 {baseDir}/scripts/regime_report.py
```

**安全提示：** 为保障安全，配置文件的路径仅限于技能目录内。不允许使用绝对路径或路径遍历（例如 `../`）。

示例配置文件位于 `{baseDir}/references/config.example.json` — 请根据需要复制并修改。

**配置字段：**
- `symbol` — 简称代码（用于显示）
- `name` — 完整名称（用于显示）
- `okx` — OKX 的永续期货代码（必须符合 OKX 的格式：`ASSET-USDT-SWAP`）

**查找 OKX 代码的方法：** 访问 [OKX 市场页面](https://www.okx.com/markets) 或使用以下命令：
```bash
curl -s "https://www.okx.com/api/v5/public/instruments?instType=SWAP"
# Optionally pipe through jq to filter: | jq '.data[].instId'
```

### 2. 配置指标参数

在 `config.json` 中进行设置：

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `supertrend.period` | 10 | ATR 计算的回顾周期 |
| `supertrend.multiplier` | 3.0 | 用于计算趋势带宽的 ATR 倍数 |
| `adx.period` | 14 | ADX 的回顾周期 |
| `adx.strong_threshold` | 25 | 判断“强趋势”的 ADX 水平 |
| `adx.weak_threshold` | 20 | 判断“弱趋势”的 ADX 水平 |

### 3. 设置定期报告（可选）

使用 OpenClaw 的 cron 系统自动接收报告。

**通过 CLI：**

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

**通过配置文件（`~/.openclaw/openclaw.json`）：**

```json5
{
  // ... other config ...
  "cron": {
    "jobs": [
      {
        "name": "Morning Regime Report",
        "schedule": { "kind": "cron", "expr": "0 6 * * *", "tz": "America/Los_Angeles" },
        "sessionTarget": "isolated",
        "payload": { "kind": "agentTurn", "message": "Run the crypto regime morning report" },
        "delivery": { "mode": "announce" }
      },
      {
        "name": "Evening Regime Report",
        "schedule": { "kind": "cron", "expr": "0 15 * * *", "tz": "America/Los_Angeles" },
        "sessionTarget": "isolated",
        "payload": { "kind": "agentTurn", "message": "Run the crypto regime evening report" },
        "delivery": { "mode": "announce" }
      },
      {
        "name": "Friday Weekly Summary",
        "schedule": { "kind": "cron", "expr": "0 16 * * 5", "tz": "America/Los_Angeles" },
        "sessionTarget": "isolated",
        "payload": { "kind": "agentTurn", "message": "Run the crypto regime weekly report with --weekly flag" },
        "delivery": { "mode": "announce" }
      }
    ]
  }
}
```

### 4. 测试报告

```bash
# Test daily report
python3 {baseDir}/scripts/regime_report.py

# Test weekly report
python3 {baseDir}/scripts/regime_report.py --weekly
```

---

## 功能说明

1. 从 OKX 获取观察列表中每个资产的 OHLCV 数据
2. 计算 Supertrend 以确定趋势方向
3. 计算 ADX 以衡量趋势强度
4. 获取当前的基金费率及开仓量
5. 生成适合通过 Telegram 发送的格式化报告

---

## 使用的指标

### Supertrend（10, 3）
- **周期：** 10
- **倍数：** 3
- **上涨趋势：** 价格高于 Supertrend 线
- **下跌趋势：** 价格低于 Supertrend 线

### ADX（平均方向指数）
- **> 25：** 强趋势（上涨或下跌）
- **20-25：** 弱/中等趋势
- **< 20：** 无明确趋势 / 盘整

## 市场状况分类

| Supertrend | ADX | 市场状况 |
|------------|-----|--------|
| 上涨 | > 25 | 强涨 |
| 上涨 | 20-25 | 弱涨 |
| 下跌 | > 25 | 强跌 |
| 下跌 | 20-25 | 弱跌 |
| 两者之一 | < 20 | 盘整 |

---

## 数据来源

| 数据类型 | 来源 | 备注 |
|------|--------|-------|
| 日度 OHLCV | OKX API | 免费，无需密钥 |
| 周度 OHLCV | Yahoo Finance | 提供超过11年的历史数据，作为 OKX 的备用数据源 |
| 基金费率 | OKX API | 免费，无需密钥 |
| 开仓量 | OKX API | 免费，无需密钥 |

**OKX API 端点：**
- OHLCV：`/api/v5/market/candles`
- 基金费率：`/api/v5/public/funding-rate`
- 开仓量：`/api/v5/public/open-interest`

---

## 资源

### scripts/
- `regime_report.py` — 主脚本，用于获取数据并生成报告

### references/
- `config.json` — 默认观察列表配置（可编辑以自定义）
- `config.example.json` — 可供参考的自定义配置文件