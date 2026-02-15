---
name: stock-market-pro
description: 由 Yahoo Finance (yfinance) 提供支持的股票分析功能：包括股票报价、基本财务数据、ASCII 图表（如 RSI、MACD、BB、VWAP、ATR 等指标），以及可选的网络插件（新闻功能、浏览器优先显示的选项/交互式界面）。
  Yahoo Finance (yfinance) powered stock analysis skill: quotes, fundamentals,
  ASCII trends, high-resolution charts (RSI/MACD/BB/VWAP/ATR), plus optional
  web add-ons (news + browser-first options/flow).
---
# Stock Market Pro

**Stock Market Pro** 是一个快速、以本地数据为主的市场研究工具包。它能够获取股票的价格和基本财务数据，生成包含技术指标（RSI、MACD、Bollinger Bands、VWAP、ATR）的图表，并生成包含摘要和高分辨率PNG图片的报告。此外，还提供可选的插件功能，如快速新闻链接扫描（使用DDG服务）以及以浏览器为中心的期权/市场动态查看功能（Unusual Whales）。

## 功能概述
- 获取 **实时报价**（价格及涨跌幅度）
- 汇总 **基本财务数据**（市值、市盈率、每股收益、净资产收益率）
- 以 **ASCII格式** 显示价格趋势（便于在终端上查看）
- 生成 **高分辨率PNG图表**，图表中可叠加显示多种技术指标
- 生成 **简洁的文本摘要** 并附带图表文件
- 通过DuckDuckGo搜索 **新闻链接**
- 以浏览器为中心查看 **期权/市场动态**（Unusual Whales数据）

---

## 命令（本地执行）
> 该工具使用 `uv run --script` 来处理依赖关系。如果尚未安装 `uv`，请从 [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv) 下载并安装。

### 1) 获取报价
```bash
uv run --script scripts/yf.py price TSLA
# shorthand
uv run --script scripts/yf.py TSLA
```

### 2) 查看基本财务数据
```bash
uv run --script scripts/yf.py fundamentals NVDA
```

### 3) 以ASCII格式显示价格趋势
```bash
uv run --script scripts/yf.py history AAPL 6mo
```

### 4) 生成高分辨率PNG图表
```bash
# candlestick (default)
uv run --script scripts/yf.py pro 000660.KS 6mo

# line chart
uv run --script scripts/yf.py pro 000660.KS 6mo line
```

#### 可选的技术指标
```bash
uv run --script scripts/yf.py pro TSLA 6mo --rsi --macd --bb
uv run --script scripts/yf.py pro TSLA 6mo --vwap --atr
```
- `--rsi`：RSI（14周期）
- `--macd`：MACD（12, 26, 9周期）
- `--bb`：Bollinger Bands（20, 2周期）
- `--vwap`：VWAP（选定时间范围内的累计加权平均价）
- `--atr`：ATR（14周期）

### 5) 生成一次性报告
- 打印简洁的文本摘要，并生成包含图表的PNG文件

```bash
uv run --script scripts/yf.py report 000660.KS 6mo
# output includes: CHART_PATH:/tmp/<...>.png
```

> 可以通过代理工作流程添加额外的网络插件（新闻/期权功能）。

---

## 网络插件（可选）

### A) 使用DuckDuckGo搜索新闻
该工具提供了一个辅助脚本 `scripts/ddg_search.py`。
- **依赖项**：[请参考此处](```bash
pip3 install -U ddgs
```)
- **使用方法**：[请参考此处](```bash
python3 scripts/news.py NVDA --max 8
# or
python3 scripts/ddg_search.py "NVDA earnings guidance" --kind news --max 8 --out md
```)

### B) 查看期权/市场动态（以浏览器为中心）
由于Unusual Whales网站可能会限制爬虫或无头浏览器的访问，建议直接在浏览器中打开相关页面并查看内容。
- **快速链接示例**：
  - `https://unusualwhales.com/stock/{TICKER}/overview`
  - `https://unusualwhales.com/live-options-flow?ticker_symbol={TICKER}`
  - `https://unusualwhales.com/stock/{TICKER}/options-flow-history`

---

## `yf.py` 命令行工具
`yf.py` 支持以下命令：
- `price`：获取股票价格
- `fundamentals`：查看基本财务数据
- `history`：查看历史数据
- `pro`：使用Stock Market Pro的核心功能
- `chart`：生成图表（别名）
- `report`：生成报告
- `option`：尝试获取期权信息（建议使用浏览器查看）

- **示例用法**：[请参考此处](```bash
python3 scripts/yf.py --help
```)

## 可支持的股票代码示例
- 美国股票：`AAPL`, `NVDA`, `TSLA`
- 韩国股票：`005930.KS`, `000660.KS`
- 加密货币：`BTC-USD`, `ETH-KRW`
- 外汇：`USDKRW=X`