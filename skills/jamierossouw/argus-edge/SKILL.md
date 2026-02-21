---
name: argus-edge
version: 1.0.0
description: Argus风格的预测市场边缘检测与投注策略：该策略通过分析技术分析（TA）所蕴含的概率与市场赔率来计算预期收益，利用Kelly准则来确定投注金额，并结合市场数据的新鲜度及共识信息来调整投注策略。在Polymarket平台上进行的新鲜数据测试中，该策略的胜率为77.8%。适用于预测市场投注、预期收益计算、策略制定或市场做市等场景。
author: JamieRossouw
tags: [polymarket, prediction-markets, edge, kelly, betting-strategy, ev, crypto]
---
# Argus Edge — 预测市场投注引擎

Argus策略的完整体系，用于在加密货币预测市场中发现并利用投资机会。

## 核心公式

```
Edge = our_P(win) - market_implied_P(win)
Bet when: edge ≥ 10% AND fresh market (<30 min old) AND TA score ≥ ±2
Kelly stake = (edge × bankroll) / odds
```

## 策略规则

### 新鲜度筛选
- 跳过共识度超过92%的市场（信号无效，L020）
- 优先考虑创建时间小于30分钟的市场（主要观察窗口）
- 主要投注的胜率（WR）为77.8%，而整体胜率为56.6%

### 反共识规则（L023）
- 技术分析（TA）得分 ≥+1 + 市场价格下跌幅度 >80% + 剩余时间 ≥20分钟 → 投注上涨（反共识策略具有正的预期价值，通过5倍以上的回报得到验证）

### 资产评估
| 资产 | 技术分析可靠性 | 偏好倾向 | 最低得分 |
|-------|---------------|------|-----------|
| BTC | 0.75 | 中立 | ±3 |
| ETH | 0.80 | 上涨趋势 +0.05 | ±2 |
| SOL | 0.90 | 上涨趋势 +0.05 | ±1 |
| XRP | 0.70 | 上涨趋势 +0.08 | ±2 |

## 使用方法

```
Use argus-edge to find the best Polymarket bet right now

Use argus-edge to calculate edge on BTC 11am ET market

Use argus-edge for full market scan with Kelly sizing
```

## 经过实战验证
该策略基于100多个Polymarket平台的实际投注案例得出，包含25条详细的操作指南（L001–L025）。