---
name: crypto-regime-report
description: 使用 Supertrend 和 ADX 指标为加密货币永续合约生成市场分析报告。当用户请求市场状况检查、市场报告、趋势分析或定时的早晨/晚上加密货币更新时，可使用该功能。报告内容包括价格走势、趋势方向/强度、资金费率以及可配置关注列表中的未平仓合约数量。
---

# 加密资产市场状况报告

本工具使用技术指标生成加密资产永续期期货的市场状况报告。

## 快速入门

```bash
# Run a daily regime report
python3 {baseDir}/scripts/regime_report.py

# Run a weekly regime report
python3 {baseDir}/scripts/regime_report.py --weekly
```

或者直接询问：“BTC的市场状况如何？”或“运行一份市场报告。”

---

## 设置指南

### 1. 配置您的观察列表

**选项 A：编辑默认配置**

编辑 `{baseDir}/references/config.json` 以自定义您的资产列表：

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

示例配置文件位于 `{baseDir}/references/config.example.json` — 根据需要复制并修改该文件。

**配置字段：**
- `symbol` — 简称（用于显示）
- `name` — 全名（用于显示）
- `okx` — OKX 上的资产代码（必须符合 OKX 的格式：`ASSET-USDT-SWAP`）

**查找 OKX 资产代码的方法：** 访问 [OKX 市场页面](https://www.okx.com/markets) 或使用以下命令：
```bash
curl -s "https://www.okx.com/api/v5/public/instruments?instType=SWAP" | jq '.data[].instId'
```

### 2. 配置指标参数

在 `config.json` 中进行设置：

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `supertrend.period` | 10 | ATR 计算的回顾周期 |
| `supertrend.multiplier` | 3.0 | 用于计算趋势带宽的 ATR 乘数 |
| `adx-period` | 14 | ADX 的回顾周期 |
| `adx.strong_threshold` | 25 | 表示“强趋势”的 ADX 水平 |
| `adx.weak_threshold` | 20 | 表示“弱趋势”的 ADX 水平 |

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
2. 计算 Supertrend 指标以确定趋势方向
3. 计算 ADX 指标以衡量趋势强度
4. 获取当前的融资利率和未平仓合约数量
5. 生成适合通过 Telegram 发送的格式化报告

---

## 指标说明

### Supertrend（10, 3）
- **周期：** 10
- **乘数：** 3
- **牛市：** 价格高于 Supertrend 线
- **熊市：** 价格低于 Supertrend 线

### ADX（平均方向指数）
- **> 25：** 强趋势（牛市或熊市）
- **20-25：** 弱/中等趋势
- **< 20：** 无明确趋势 / 横盘整理

## 市场状况分类

| Supertrend | ADX | 市场状况 |
|------------|-----|--------|
| 牛市 | > 25 | 强牛市 |
| 牛市 | 20-25 | 弱牛市 |
| 熊市 | > 25 | 强熊市 |
| 熊市 | 20-25 | 弱熊市 |
| 两者均不符合 | < 20 | 横盘整理 |

---

## 数据来源

| 数据类型 | 来源 | 备注 |
|------|--------|-------|
| 日度 OHLCV | OKX API | 免费，无需密钥 |
| 周度 OHLCV | Yahoo Finance | 提供 11 年以上的历史数据，可作为 OKX 的备用数据源 |
| 融资利率 | OKX API | 免费，无需密钥 |
| 未平仓合约数量 | OKX API | 免费，无需密钥 |

**OKX API 端点：**
- OHLCV：`/api/v5/market/candles`
- 融资利率：`/api/v5/public/funding-rate`
- 未平仓合约数量：`/api/v5/public/open-interest`

---

## 资源

### 脚本：
- `regime_report.py` — 主脚本，用于获取数据并生成报告

### 参考文件：
- `config.json` — 默认的观察列表配置（可编辑以自定义）
- `config.example.json` — 可供参考的自定义配置文件