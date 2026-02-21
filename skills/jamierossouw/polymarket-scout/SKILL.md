---
name: polymarket-scout
version: 1.0.0
description: 每小时扫描 Polymarket 的加密货币市场（BTC/ETH/SOL/XRP），以寻找潜在的交易机会。通过 Argus 策略识别市场中的异常情况（即与共识相悖的交易模式）、数据更新的窗口期以及潜在的盈利机会。适用于需要 Polymarket 市场分析、交易机会识别、每小时一次的二元市场分析或预测市场信号的场景。
author: JamieRossouw
tags: [polymarket, prediction-markets, crypto, edge-detection, betting, defi]
---
# Polymarket Scout — 每小时市场机会检测器

该工具使用Argus策略，扫描Polymarket平台上每小时更新的BTC/ETH/SOL/XRP市场的交易机会。

## 功能说明

- 通过REST API获取Polymarket平台上每小时加密货币市场的实时赔率数据
- 计算“市场机会”（market_opportunity）：market_opportunity = our_p_win - market_implied_p_win
- 标识出与市场共识相悖的交易信号（例如：技术分析预测上涨，但市场实际下跌超过70% → 表示有正的预期收益）
- 实施“新鲜度过滤”机制：跳过那些获得超过92%共识支持的市场（L020规则）
- 返回按预期收益排序的交易机会，并提供相应的投注建议（基于Kelly策略）

## 使用方法

```
Use polymarket-scout to scan current hourly markets for edge

Use polymarket-scout to check BTC 10am ET edge

Use polymarket-scout to find best Polymarket bet right now
```

## 市场机会计算方法

```
edge = our_P - market_P
where our_P = TA-calibrated probability per asset:
  BTC: reliability 0.75, min score ±3
  ETH: reliability 0.80, slight UP bias +0.05
  SOL: reliability 0.90, UP bias +0.05
  XRP: reliability 0.70, UP bias +0.08 (CLARITY catalyst)
```

## 与市场共识相悖的交易规则（L023）
当技术分析得分（TA score）≥+1、市场走势为下跌且剩余交易时间超过20分钟时，认为存在与市场共识相悖的交易机会（即“反共识”交易），这种交易具有正的预期收益。经验证：在新进行的初次投注中，该策略的有效率为77.8%。

## API集成
该工具使用了Polymarket的CLOB REST API和Gamma API进行数据获取，无需任何API密钥。