---
name: stocks
description: 通过 Yahoo Finance，您可以使用 56 种以上的金融数据工具。这些工具可以自动获取股票价格、公司基本信息、收益数据、股息信息、期权信息、加密货币价格、外汇汇率、大宗商品价格以及相关新闻等内容。
---
# 股票技能

通过 Yahoo Finance 提供超过 56 种金融工具，包括股票价格、基本财务数据、收益信息、期权交易、加密货币、外汇、大宗商品以及相关新闻。

## 设置

从技能目录中运行脚本：

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

> **Windows:** 使用 `.venv\Scripts\python3` 而不是 `.venv/bin/python3`。

## 兼容多种操作系统 / 一次性设计（目标）
- 该技能设计为不依赖于具体的操作系统或执行环境。
- 首次使用时仅加载必要的数据，并采用一次性交互模式以确保可靠性。
- 基本使用方法请参考 `TOOLS.md` 文件以及 `SKILL.md` 正文中的“所有功能”列表。

## 引用/命令执行的可靠性（常见问题）
- 如果命令调用使用了复杂的 shell 引用语法，可能会在不同环境中出现错误。建议使用 here-doc 格式或小型辅助脚本来避免转义问题。
- **务必使用技能虚拟环境中的 Python 解释器来执行脚本。** 如果虚拟环境未激活，直接调用 `python3` 可能会使用错误的解释器，从而导致 `ModuleNotFoundError`。
- **执行命令时必须使用虚拟环境中的 Python 解释器的完整路径**，例如：
  `/home/openclaw/.openclaw/venv/stocks/bin/python3`
- 确保所有必要的包（如 `yfinance-ai` 所需的 `pydantic`）都已通过 `pip` 安装在该虚拟环境中：
  `/home/openclaw/.openclaw/venv/stocks/bin/pip install <package_name>`
- 使用 here-doc 的示例代码：

```bash
/home/openclaw/.openclaw/venv/stocks/bin/python3 - << 'PY'
import asyncio, sys
sys.path.insert(0, '.')
from yfinance_ai import Tools

t = Tools()
async def main():
    r = await t.get_key_ratios(ticker='UNH')
    print(r)
asyncio.run(main())
PY
```
- 如果内联脚本较为复杂，可以将相关代码封装到一个小的 Python 脚本文件中（例如放在 `scripts/` 目录下），然后通过虚拟环境中的 Python 解释器来执行该脚本。

## 代理快速启动

设置完成后，将以下模板复制到代理的 `TOOLS.md` 文件中（或框架要求注入到每个会话中的任何文件中）。这是最重要的步骤——只要代理能够识别正确的调用模式，该技能就能每次正常工作。

**请将 `SKILL_DIR` 替换为该技能目录的绝对路径**（例如包含 `scripts/` 和 `.venv/` 的目录）。

````markdown
# Stocks Skill

## Usage

```bash
cd SKILL_DIR/scripts && SKILL_DIR/.venv/bin/python3 -c "
import asyncio, sys
sys.path.insert(0, '.')
from yfinance_ai import Tools
t = Tools()
async def main():
    result = await t.METHOD(ARGS)
    print(result)
asyncio.run(main())
" 2>/dev/null
```

Replace METHOD(ARGS) with any call below. Suppress stderr (2>/dev/null) to hide warnings.

## Common Calls

| Need | Method |
|---|---|
| Stock price | `get_stock_price(ticker='AAPL')` |
| Key ratios (P/E, ROE, margins) | `get_key_ratios(ticker='AAPL')` |
| Company overview | `get_company_overview(ticker='AAPL')` |
| Full deep-dive | `get_complete_analysis(ticker='AAPL')` |
| Compare stocks | `compare_stocks(tickers='AAPL,MSFT,GOOGL')` |
| Crypto | `get_crypto_price(symbol='BTC')` |
| Forex | `get_forex_rate(pair='EURUSD')` |
| Commodities | `get_commodity_price(commodity='gold')` |
| News | `get_stock_news(ticker='AAPL')` |
| Market indices | `get_market_indices()` |
| Dividends | `get_dividends(ticker='AAPL')` |
| Earnings | `get_earnings_history(ticker='AAPL')` |
| Analyst recs | `get_analyst_recommendations(ticker='AAPL')` |
| Options chain | `get_options_chain(ticker='SPY')` |
| Market open/closed | `get_market_status()` |

## Routing

- Price / quote → `get_stock_price`
- Ratios / valuation → `get_key_ratios`
- "Tell me about" → `get_company_overview`
- Deep dive → `get_complete_analysis`
- Compare → `compare_stocks`
- Crypto → `get_crypto_price`
- Forex → `get_forex_rate`
- Commodities → `get_commodity_price`
- News → `get_stock_news`
````

---

## 所有功能

请参阅 `skill.json` 文件，了解超过 56 个功能的完整列表、参数以及触发关键词。功能类别包括：
- **报价**：`get_stock_price`, `get_stock_quote`, `get_fast_info`, `get_historical_data`
- **公司**：`get_company_info`, `get_company_overview`, `get_company_officers`
- **财务**：`get_income_statement`, `get_balance_sheet`, `get_cash_flow`, `get_key_ratios`, `get_financial_summary`
- **收益**：`get_earnings_history`, `get_earnings_dates`, `get_analyst_estimates`, `get_eps_trend`
- **分析师**：`get_analyst_recommendations`, `get_analyst_price_targets`, `get_upgrades_downgrades`
- **持股情况**：`get_institutional_holders`, `get_insider_transactions`, `get_major_holders`
- **股息**：`get_dividends`, `get_stock_splits`, `get_corporate_actions`
- **期权**：`get_options_chain`, `get_options_expirations`
- **市场**：`get_market_indices`, `get_sector_performance`, `get_market_status`
- **加密货币/外汇/大宗商品**：`get_crypto_price`, `get_forex_rate`, `get_commodity_price`
- **比较**：`compare_stocks`, `get_peer_comparison`, `get_historical_comparison`
- **新闻**：`get_stock_news`, `get_sec_filings`
- **工具**：`search_ticker`, `validate_ticker`, `run_self_test`

## 注意事项
- 数据来源于 Yahoo Finance，可能存在轻微的实时延迟。
- 所有功能都是异步的，由 `asyncio.run()` 装饰器处理异步执行。
- 该技能支持 Linux、macOS 和 Windows 系统（Windows 用户需调整虚拟环境的路径）。