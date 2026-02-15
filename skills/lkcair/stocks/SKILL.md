---
name: Stocks and Financial Data Pull
description: 可以从 Yahoo Finance 获取实时金融数据，包括股票、加密货币、外汇、商品、公司信息、收益、新闻以及市场指数。这是 OURSS 的功能吗？如果是的话，请补充更多相关信息。通过 56 多种工具可以快速获取实时报价和市场数据，并获得深入的公司分析和新闻报道。
metadata: { "openclaw": { "requires": { "bins": ["python3"] }, "install": [{ "id": "pip", "kind": "uv", "label": "Install Python dependencies (yfinance, pandas, pydantic, requests) into a dedicated venv", "bins": ["python3"], "packages": ["yfinance>=0.2.66", "pandas>=2.2.0", "pydantic>=2.0.0", "requests>=2.28.0"] }] } }
---

# 股票与金融数据获取

### 链接
- 仓库：https://github.com/lkcair/yfinance-ai-skill  
- 由 yfinance-ai 的同一开发者创建：https://github.com/lkcair/yfinance-ai  

该技能通过 Yahoo Finance 提供了 56 种以上的金融数据工具，帮助用户获得全面的市场洞察。用户可以查询实时股票价格、进行基本面分析、跟踪股息信息、进行期权交易、了解加密货币行情、外汇汇率、商品价格以及获取市场突发新闻。这是进行投资分析和股票交易的必备工具。

## 使用方法  
根据用户的需求运行相应的工具函数。该技能的入口文件是 `{baseDir}/scripts/yfinance_ai.py`。

## 安装说明  
该技能会在 `~/.openclaw/venv/stocks` 创建一个 **Python 虚拟环境**，并通过 pip/PyPI 安装 `requirements.txt` 中列出的依赖项（yfinance、pandas、pydantic、requests）。这是基于 Python 的技能的标准安装流程，也是这些工具正常运行的必要条件。该虚拟环境与系统 Python 是隔离的。安装过程中需要网络访问 PyPI。该技能专为金融规划和投资策略优化设计。

### 如何调用工具（针对 AI 代理）  
**切勿** 直接通过 CLI 参数调用脚本（例如 `python3 yfinance_ai.py get_earnings_history --ticker GME`），这样会导致无法正常运行。  
**必须** 使用 `skill.json` 中定义的异步调用模式：  

```bash
cd /home/openclaw/.openclaw/workspace/skills/stocks/scripts && /home/openclaw/.openclaw/venv/stocks/bin/python3 -c "
import asyncio, sys
sys.path.insert(0, '.')
from yfinance_ai import Tools
t = Tools()
async def main():
    result = await t.{method}({args})
    print(result)
asyncio.run(main())
" 2>/dev/null
```  

请将 `{method}` 替换为工具函数名称，将 `{args}` 替换为相应的参数。  

**示例：**  
```bash
# Get earnings history for GME
result = await t.get_earnings_history(ticker='GME')

# Get stock price for AAPL
result = await t.get_stock_price(ticker='AAPL')

# Get crypto price for BTC
result = await t.get_crypto_price(symbol='BTC')

# Compare stocks
result = await t.compare_stocks(tickers='AAPL,MSFT,GOOG')
```  

**重要规则：**  
- 始终使用位于 `/home/openclaw/.openclaw/venv/stocks/bin/python3` 的虚拟环境中的 Python 解释器。  
- 使用前务必先进入 `scripts/` 目录。  
- 使用 `2>/dev/null` 来抑制弃用警告。  
- 所有工具函数均为异步函数，需使用 `asyncio.run()` 来调用它们。  
- 详细的功能列表、参数及触发关键词请参考 `skill.json` 文件。  

## 自动路由指南  
使用以下触发关键词来选择合适的工具：  

### 股票与报价  
- **get_stock_price**：股票价格、报价、股票代码、股票数量、市值  
- **compare_stocks**：比较股票表现  
- **get_fast_info**：快速获取股票基本信息  

### 加密货币  
- **get_crypto_price**：加密货币价格  

### 外汇  
- **get_forex_rate**：外汇汇率  

### 商品  
- **get_commodity_price**：商品价格  

### 公司信息  
- **get_company_info**：公司基本信息  
- **get_company_officers**：公司高管信息  
- **get_company_overview**：公司概况  
- **get_major_holders**：主要股东信息  

### 财务与基本面  
- **get_balance_sheet**：资产负债表  
- **get_income_statement**：损益表  
- **get_financial_summary**：财务摘要  
- **get_key_ratios**：关键财务比率  

### 收益与预测  
- **get_earnings_history**：收益历史  
- **get_analyst_estimates**：分析师预测  
- **get_eps_revisions**：收益预测修正  

### 股息与公司动态  
- **get_dividends**：股息信息  
- **get_stock_splits**：股票分割信息  

### 分析师与新闻  
- **get_analyst_recommendations**：分析师推荐  
- **get_upgrades_downgrades**：评级变化  
- **get_stock_news**：股票新闻  

### 期权  
- **get_options_chain**：期权合约信息  
- **get_options_expirations**：期权到期日  

### 基金与 ETF  
- **get_fund_holdings**：基金持仓  
- **get_fund_overview**：基金概况  

### 历史数据与对比  
- **get_historical_data**：历史价格数据  
- **get_historical_comparison**：历史业绩对比  

### 市场指数与状态  
- **get_market_indices**：市场指数  
- **get_market_status**：市场状态  

### 其他工具  
- **get_trending_tickers**：热门股票  
- **get_sec_filings**：公司公开文件  
- **get_api_status**：API 状态  

### 市场新闻  
- **get_stock_news**：实时金融新闻