---
name: clawback
description: 通过自动化经纪商执行系统来镜像国会的股票交易行为，并实现风险管理。
version: 1.0.0
author: dayne
metadata:
  openclaw:
    requires:
      - python3
      - pdfplumber
      - selenium
      - yfinance
    config:
      - BROKER_API_KEY
      - BROKER_API_SECRET
      - BROKER_ACCOUNT_ID
    optional_config:
      - TELEGRAM_BOT_TOKEN
      - TELEGRAM_CHAT_ID
---

# ClawBack

**通过自动化经纪商执行功能，追踪国会议员的股票交易**

ClawBack 跟踪国会议员（众议院和参议院）披露的股票交易，并在您的经纪账户中执行相应的交易。该工具基于这样一个前提：由于信息优势，国会议员通常能够获得优于市场的投资回报。

## 主要功能

- **实时数据追踪**：从众议院书记员和参议院的官方电子文件（eFD）来源获取数据
- **自动化交易执行**：通过经纪商的 API 进行交易（包含 E*TRADE 适配器）
- **智能仓位管理**：根据您的账户规模自动调整交易量
- **动态止损机制**：锁定利润、限制损失
- **风险管理**：设置止损限额、防止连续亏损
- **Telegram 通知**：接收新交易和止损事件的提醒
- **回测引擎**：使用历史数据测试交易策略

## 性能（回测结果）

| 交易策略 | 胜率 | 收益率 | 夏普比率 |
|---------|--------|---------|---------|
| 延迟 3 天、持有 30 天 | 42.9% | +6.2% | 0.39 |
| 延迟 9 天、持有 90 天 | 57.1% | +4.7% | 0.22 |

根据 NBER 的研究，国会议员的年均投资回报比标准普尔 500 指数高出 47%。

## 快速入门

```bash
# Clone and setup
git clone https://github.com/openclaw/clawback
cd clawback
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure secrets
python3 src/config_loader.py setup

# Authenticate with broker
python3 src/main.py interactive
# Select option 1 to authenticate

# Set up automation
./scripts/setup_cron.sh
```

## 配置

ClawBack 从环境变量或 `config/secrets.json` 文件中读取配置信息：

```json
{
  "BROKER_API_KEY": "your-broker-api-key",
  "BROKER_API_SECRET": "your-broker-api-secret",
  "BROKER_ACCOUNT_ID": "your-account-id",
  "TELEGRAM_BOT_TOKEN": "optional-for-notifications",
  "TELEGRAM_CHAT_ID": "optional-for-notifications"
}
```

### 支持的经纪商

ClawBack 采用适配器模式与各种经纪商集成。每个经纪商都实现了 `broker_adapter.py` 中定义的通用接口：

| 经纪商 | 适配器 | 支持状态 |
|--------|---------|---------|
| E*TRADE | `etrade_adapter.py` | 已支持 |
| Schwab | `schwab_adapter.py` | 计划中 |
| Fidelity | `fidelity_adapter.py` | 计划中 |

要指定使用的经纪商，请在配置文件中设置 `broker.adapter`：

```json
{
  "broker": {
    "adapter": "etrade",
    "credentials": {
      "apiKey": "${BROKER_API_KEY}",
      "apiSecret": "${BROKER_API_SECRET}"
    }
  }
}
```

## 数据来源

所有数据均直接从官方政府渠道获取：

| 数据来源 | 数据类型 | 获取方式 |
|---------|---------|---------|
| 众议院书记员 | 众议院股票交易记录（PTR 文件） | PDF 文件解析 |
| 参议院电子文件（eFD） | 参议院股票交易记录（PTR 文件） | Selenium 爬虫技术 |

获取国会议员交易数据无需使用第三方 API。

## 交易策略设置

请编辑 `config/config.json` 文件以自定义交易策略：

```json
{
  "strategy": {
    "entryDelayDays": 3,
    "holdingPeriodDays": 30,
    "purchasesOnly": true,
    "minimumTradeSize": 50000
  },
  "riskManagement": {
    "positionStopLoss": 0.08,
    "trailingStopActivation": 0.10,
    "trailingStopPercent": 0.05,
    "maxDrawdown": 0.15
  }
}
```

## 命令行操作

```bash
# Interactive mode
python3 src/main.py interactive

# Single check cycle
python3 src/main.py run

# Scheduled trading
python3 src/main.py schedule 24

# Run backtest
python3 src/backtester.py
```

## 定时任务自动化

```bash
# Install cron jobs
./scripts/setup_cron.sh

# Manual runs
./scripts/run_bot.sh check    # Check for new trades
./scripts/run_bot.sh monitor  # Check stop-losses
./scripts/run_bot.sh full     # Both
```

## 系统架构

```
clawback/
├── src/
│   ├── main.py              # Main entry point
│   ├── congress_tracker.py  # Congressional data collection
│   ├── trade_engine.py      # Trade execution & risk management
│   ├── broker_adapter.py    # Abstract broker interface
│   ├── etrade_adapter.py    # E*TRADE broker implementation
│   ├── database.py          # SQLite state management
│   └── config_loader.py     # Configuration handling
├── config/
│   ├── config.json          # Main configuration
│   └── secrets.json         # API keys (git-ignored)
├── scripts/
│   ├── run_bot.sh           # Cron runner
│   └── setup_cron.sh        # Cron installer
└── data/
    └── trading.db           # SQLite database
```

## 风险声明

本软件仅用于教育目的。股票交易存在较高的风险，可能导致损失。过去国会议员的交易表现并不能保证未来的收益。作者并非财务顾问，使用本软件需自行承担风险。

## 许可证

采用 MIT 许可证——详见 LICENSE 文件

---

*专为 OpenClaw 社区开发*