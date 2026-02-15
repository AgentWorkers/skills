---
name: stock-market-pro
description: 这是一款专业的股票价格跟踪、基本面分析及财务报告工具，支持全球市场（如美国、韩国等）、加密货币和外汇市场，并提供实时数据。主要功能包括：  
(1) 实时报价；  
(2) 估值指标（市盈率 PE、每股收益 EPS、净资产收益率 ROE）；  
(3) 盈利预测日历及市场共识；  
(4) 高质量的蜡烛图和折线图，附带技术指标（5/20/60日均线）。
---

# Stock Market Pro

这是一款基于雅虎财经（Yahoo Finance）数据的专业级金融分析工具。

## 核心功能

### 1. 实时报价 (`price`)
获取即时价格更新及每日价格范围。
```bash
uv run --script scripts/yf price [TICKER]
```

### 2. 专业图表 (`pro`)
生成包含成交量和移动平均线的高分辨率PNG图表。
- **蜡烛图**: `uv run --script scripts/yf pro [股票代码] [时间周期]`
- **折线图**: `uv run --script scripts/yf pro [股票代码] [时间周期] line`
- **时间周期**: `1个月`, `3个月`, `6个月`, `1年`, `5年`, `最长` 等

### 3. 基本面分析 (`fundamentals`)
深入分析公司估值：市值、市盈率（PE）、每股收益（EPS）、股本回报率（ROE）和利润率。
```bash
uv run --script scripts/yf fundamentals [TICKER]
```

### 4. 盈利与预测 (`earnings`)
查看即将发布的盈利报告日期及市场共识（预期收入/每股收益）。

### 5. 历史趋势 (`history`)
以终端友好的ASCII图表形式查看最近10天的市场趋势。

## 股票代码示例
- **美国股票**: `AAPL`, `NVDA`, `TSLA`
- **韩国股票**: `005930.KS`（三星电子），`000660.KS`（SK海力士）
- **加密货币**: `BTC-USD`, `ETH-KRW`

## 技术说明
- **开发语言**: Python 3.11+，使用 `yfinance`, `mplfinance`, `rich` 库
- **主要优势**: 无需API密钥。通过 `uv` 自动处理所有依赖关系。

---

*中文说明：这是一款具备实时股价查询、财务指标分析及专业图表生成功能的综合股票分析工具。*