---
name: binance-watchlist
version: 1.0.0
description: 使用多指标技术分析（TA）评分方法，扫描整个币安（Binance）的现货观察列表。返回按信号强度排序的交易机会。无需API密钥（使用公开数据）。适用于币安的扫描、观察列表筛选、信号排名，或当前寻找最佳交易策略。
author: JamieRossouw
tags: [binance, watchlist, crypto, trading, ta, signals, scanner]
---# Binance 监控列表扫描器

该工具每个周期会扫描 20 对 Binance 的现货交易对，并根据技术分析（TA）信号的强度对它们进行排序。

## 默认监控列表
BTC、ETH、SOL、XRP、TRX、DOGE、ADA、AVAX、BNB、LINK、LTC、SUI、ARB、OP、NEAR、DOT、ATOM、UNI、MATIC

## 使用的指标
RSI（14）、MACD（12/26/9）、EMA 交叉（9/21）、Bollinger Bands（20）、OBV 发散度、StochRSI（14）

## 输出结果
机会的排名列表：
```
🔥 TOP SIGNALS RIGHT NOW
+4 ARB/USDT | RSI=38 | MACD cross | OBV rising | $0.82
+3 LINK/USDT | RSI=42 | EMA bull cross | $14.20
+2 SOL/USDT | RSI=55 | BB support | $86.50
-3 ETH/USDT | RSI=79 | Overbought | $1,990
-4 XRP/USDT | RSI=83 | MACD death cross | $1.45
```

## 使用方法
```
Use binance-watchlist to find the best trade setup right now

Use binance-watchlist to scan all 20 pairs and rank signals

Use binance-watchlist for the top 3 buy opportunities
```

## 扫描速度
完整扫描整个监控列表大约需要 30 秒。无需 API 密钥。