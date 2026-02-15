---
name: finance
description: 支持跟踪股票、ETFs、指数、加密货币（如支持的话）以及外汇货币对的数据。系统采用缓存机制，并提供备用数据源（provider fallbacks）以确保数据获取的稳定性和可靠性。
metadata: {"clawdbot":{"config":{"requiredEnv":["TWELVEDATA_API_KEY","ALPHAVANTAGE_API_KEY"],"stateDirs":[".cache/finance"],"example":"# Optional (only if you add a paid provider later)\n# export TWELVEDATA_API_KEY=\"...\"\n# export ALPHAVANTAGE_API_KEY=\"...\"\n"}}}
---

# 市场追踪技能

该技能可帮助您获取以下金融产品的**最新报价**和**历史数据**：
- 股票 / ETF / 指数（例如：AAPL, MSFT, ^GSPC, VOO）
- 外汇对（例如：USD/ZAR, EURUSD, GBP-JPY）
- 所选提供商支持的所有加密货币（尽力提供）

该技能针对以下场景进行了优化：
- 快速查询“当前价格”；
- 支持使用本地看盘列表进行轻量级追踪；
- 通过缓存机制避免请求频率限制。

## 使用场景
当用户提出以下问题时，请使用该技能：
- “___的最新价格是多少？”
- “追踪___和___，并显示每日变化情况。”
- “提供___的30天历史数据。”
- “将USD兑换成ZAR（或追踪USD/ZAR的汇率）。”
- “维护一个看盘列表并汇总表现。”

## 提供商策略（重要说明）
- **股票/ETF/指数**的默认提供商为Yahoo Finance（通过`yfinance`接口获取数据），无需密钥，但可能存在请求频率限制。
- **外汇**的默认提供商为ExchangeRate-API Open Access（无需密钥，数据每日更新）。
- 如果用户需要高频数据或大量交易品种，建议后续使用付费提供商。

详情及交易品种格式请参阅`providers.md`文件。

---

# 快速入门（使用方法）
这些脚本需要在终端中运行。您需要执行以下步骤：
1. 确保所有依赖项已安装；
2. 运行相关脚本；
3. 清晰地展示结果。

安装步骤：
- 对于Linux/macOS：`python -m venv .venv && source .venv/bin/activate`（Windows系统请使用相应命令）
- `pip install -r requirements.txt`

## 命令说明

### 1) 获取最新报价（股票/ETF/指数）
示例：
- `python scripts/market_quote.py AAPL`
- `python scripts/market_quote.py ^GSPC`
- `python scripts/market_quote.py VOO`

### 2) 获取最新外汇汇率
示例：
- `python scripts/market_quote.py USD/ZAR`
- `python scripts/market_quote.py EURUSD`
- `python scripts/market_quote.py GBP-JPY`

### 3) 获取历史数据（以CSV格式输出到标准输出）
示例：
- `python scripts/market_series.py AAPL --days 30`
- `python scripts/market_series.py USD/ZAR --days 30`

### 4) 管理看盘列表
- 添加交易品种：`python scripts/market_watchlist.py add AAPL MSFT USD/ZAR`
- 删除交易品种：`python scripts/market_watchlist.py remove MSFT`
- 查看看盘列表摘要：`python scripts/market_watchlist.py summary`

---

# 预期输出结果
- 对于报价：应包括价格、价格变化百分比、时间戳及数据来源，以及任何特殊说明（如“外汇数据每日更新”）。
- 对于历史数据：需确认数据范围、数据点数量，并展示部分数据预览（前几行或最后几行）。
- 如果遇到请求频率限制：需说明原因，并建议用户降低请求频率或更换提供商。

---

# 安全性与正确性注意事项
- 除非提供商确实提供实时数据，否则切勿声称数据为“实时”的。
- 必须对响应结果进行缓存，并限制重复请求的频率。
- 如果Yahoo Finance限制了请求频率，请建议用户使用付费提供商或延长数据缓存时间。

---