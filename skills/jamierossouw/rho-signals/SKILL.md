---
name: rho-signals
version: 1.0.0
description: 实时加密货币技术分析信号（适用于 BTC、ETH、SOL、XRP）：包括 RSI、MACD、EMA、Bollinger Bands、OBV 发散度以及 StochRSI 等指标。这些信号被综合成一个方向性评分（范围为 -10 至 +10），并结合 Polymarket 的市场趋势检测功能。适用于需要实时加密货币技术分析信号、市场方向判断或 Polymarket 每小时市场趋势分析的场景。
author: rho-genesis
tags: [crypto, trading, signals, polymarket, technical-analysis, bitcoin, ethereum, solana, xrp]
price: 0.01
---
# RHO Signals — 实时加密货币技术分析引擎

为 BTC、ETH、SOL 和 XRP 提供实时技术分析信号。该引擎基于多种技术指标的综合分析，包括 RSI、MACD、EMA 交叉、Bollinger Bands、OBV 发散、StochRSI 以及 ATR 波动性筛选等。

## 您将获得的内容：

- **方向性评分**（范围：-10 至 +10）：负数表示看跌，正数表示看涨  
- **RSI** 指标，具备超买/超卖检测功能  
- **OBV 发散**：用于识别市场的积累/分配趋势  
- **Polymarket 边缘分析**：对比技术分析预测的概率与实际市场走势  
- **逆向共识警报**：当技术分析结果与市场主流观点（>70% 的共识）相悖时发出警报  

## 使用方法

```
# Get signal for one asset
Use the rho-signals skill to get BTC signal

# Get all signals + Polymarket edge
Use rho-signals to get full market scan with Polymarket edges
```

## 信号等级说明：

| 评分 | 含义 |
|-------|---------|
| +5 至 +10 | 强烈买入信号 — 所有指标均显示看涨趋势 |
| +2 至 +4 | 中等看涨倾向 |
| 0 至 ±1 | 中性/信号矛盾 |
| -2 至 -4 | 中等看跌倾向 |
| -5 至 -10 | 强烈卖出信号 — 所有指标均显示看跌趋势 |

## 实时 API（x402 协议，按信号收费）

信号也可通过 HTTP 提供，并支持微支付方式：  
- 端点：https://rho-signals.clawpay.bot（即将上线）  
- 单个信号价格：0.001 美元（USDC）  
- 支持 x402 支付协议  

## 数据来源：  
- Binance 公共 API（无需密钥）  
- 数据来源：1 小时 OHLCV 图表，回溯周期为 50 个周期  
- 数据更新频率：每 30 分钟一次  

## 准确性说明：  
- 在 Polymarket 的每小时数据上进行了回测：在新鲜数据（<30 分钟）的情况下，准确率为 77.8%  
- 表现最佳的资产：SOL（有 +5% 的上涨倾向）、ETH（RSI 指标反应灵敏）、XRP（受特定因素影响较大）  
- 表现最差的资产：BTC（1 小时图表的可预测性较低，建议仅参考评分 ≥±4 的信号）