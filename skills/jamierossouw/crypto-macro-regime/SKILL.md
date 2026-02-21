---
name: crypto-macro-regime
version: 1.0.0
description: 根据“恐惧与贪婪指数”（Fear & Greed Index）、比特币的统治地位（BTC dominance）、Reddit上的市场情绪、链上数据（on-chain signals）以及宏观经济新闻（macro news），对当前的加密货币市场格局进行分类（风险偏好型/Risk-On、风险厌恶型/Risk-Off或中性型/Neutral）。输出结果应包括市场格局的标签（regime label）、市场偏好的方向（bias direction）以及针对特定资产的调整措施（asset-specific adjustments）。这些信息可用于宏观经济分析、市场格局识别、投资组合调整或市场环境评估。
author: JamieRossouw
tags: [macro, crypto, regime, fear-greed, sentiment, bitcoin, market-analysis]
---
# 加密市场宏观环境分类器

该工具用于判断当前加密市场的宏观环境，并据此调整交易策略。

## 宏观环境分类

| 分类 | 贪婪指数（F&G） | 信号指标 | 交易偏好 |
|--------|----------------|------------------|-------------------------|
| A — 高风险 | 50及以上 | 正面新闻，市场主导地位较低 | 做多偏好，涨幅0.10% |
| B — 中性 | 25–50 | 市场情绪复杂 | 无需调整 |
| C — 低风险 | <25 | 市场恐慌，宏观经济冲击 | 做空偏好，减少交易规模 |
| D — 极度恐慌 | <15 | 市场崩溃 | 反向做多策略 |

## 输出内容

- 当前的宏观环境分类（A/B/C/D）及其置信度
- 贪婪指数与恐惧指数的数值及分类结果
- 针对特定资产的交易偏好调整建议
- 主要的宏观经济驱动因素（美联储政策、监管政策、黑客攻击风险）
- 推荐的投资组合配置比例 %

## 使用方法

```
Use crypto-macro-regime to get current market regime

Use crypto-macro-regime to check if now is a good time to go long BTC

Use crypto-macro-regime for today's macro briefing
```

## 数据来源

- alternative.me 贪婪指数与恐惧指数 API（免费）
- Reddit 的 r/CryptoCurrency 和 r/Bitcoin 论坛板块的投资者情绪数据
- CoinDesk 新闻头条
- BTC 的挖矿难度及市场主导地位数据

## 当前设置

- 当前宏观环境分类为 D（极度恐慌，贪婪指数=8）：历史上属于强烈的中期反向看多信号。最佳入场时机为恐慌性抛售后的 RSI 指数在 35–55 区间时。