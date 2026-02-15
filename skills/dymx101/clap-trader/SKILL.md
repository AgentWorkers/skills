---
name: Crypto Trader & Analyst
description: 这是一项OpenClaw技能，用于研究加密货币市场的趋势（包括技术面和情绪面），并在Binance平台上交易ETH（以太坊）。
---

# 加密货币交易员与分析师技能

该技能使 OpenClaw 能够利用技术指标和新闻情感分析来研判加密货币市场，记录分析结果，并在 Binance 平台上执行交易。

## 依赖项

请确保已安装以下 Python 包：
```bash
pip install ccxt pandas pandas-ta requests TextBlob
```
*注：如果需要基本的情感分析，建议使用 `TextBlob`；不过简单的关键词匹配也可能足够使用。*

## 环境变量

您必须设置以下用于交易的环境变量：
- `BINANCE_API_KEY`：您的 Binance API 密钥。
- `BINANCE_API_SECRET`：您的 Binance API 密钥。

**警告**：切勿共享这些密钥，也切勿将它们提交到版本控制系统中。

## 工作流程

### 1. 市场分析

**技术分析**
运行市场数据脚本，获取指定货币（默认为 ETH/USDT）的当前技术指标。
```bash
python skills/crypto_trader/scripts/market_data.py --symbol ETH/USDT
```
*输出：包含 RSI、MACD、收盘价等信息的 JSON 数据。*

**情感分析**
运行情感分析脚本，获取最新的新闻标题和论坛讨论内容。
```bash
python skills/crypto_trader/scripts/sentiment_data.py
```
*输出：关于正面/负面新闻的文本/JSON 摘要。*

### 2. 决策与记录

**分析并记录**
根据第一步的输出结果，形成一个交易策略（市场是看涨、看跌还是中性？）
在交易之前，**必须**保存您的分析结果。
```bash
python skills/crypto_trader/scripts/logger.py "Your detailed analysis here. E.g., RSI is 30 (oversold) and news is positive. Planning to BUY."
```

### 3. 执行交易

**交易**
如果分析结果支持进行交易，请执行相应的交易操作。
```bash
# Buy 0.01 ETH at Market Price
python skills/crypto_trader/scripts/trade.py --symbol ETH/USDT --side buy --amount 0.01 --type market

# Dry Run (Test without real money)
python skills/crypto_trader/scripts/trade.py --symbol ETH/USDT --side buy --amount 0.01 --dry-run
```
*交易脚本会自动将交易记录添加到 `skills/crypto_trader/logs/trade_history.csv` 文件中。*

## 文件结构
- `scripts/market_data.py`：获取开盘价（Open）、最高价（High）、收盘价（Close）和最低价（Low）以及计算技术指标。
- `scripts/sentiment_data.py`：获取新闻和论坛讨论数据。
- `scripts/logger.py`：将分析结果记录到 `logs/analysis_journal.md` 文件中。
- `scripts/trade.py`：执行交易操作，并将交易记录保存到 `logs/trade_history.csv` 文件中。
- `logs/`：存储您的分析历史记录和交易日志的目录。