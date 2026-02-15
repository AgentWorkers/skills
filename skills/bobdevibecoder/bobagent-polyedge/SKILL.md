---
name: polymarket-correlation
description: **检测Polymarket预测市场中价格异常的相关性：为AI代理提供跨市场套利工具**
version: 0.1.0
---

# Polymarket 相关性分析器

通过检测预测市场之间的价格异常相关性来发现套利机会。

## 功能介绍

该工具分析 Polymarket 上的多个市场对，以识别某个市场的价格走势是否与另一个市场的价格走势存在矛盾。

**示例：**
- 市场 A：“美联储会降息吗？” = 60%
- 市场 B：“标准普尔指数会上涨吗？” = 35%
- 历史数据：降息时标准普尔指数上涨的概率为 70%
- **信号提示：** 市场 B 可能被低估了

## 快速入门

```bash
cd src/
python3 analyzer.py <market_a_slug> <market_b_slug>
```

**示例：**
```bash
python3 analyzer.py russia-ukraine-ceasefire-before-gta-vi-554 will-china-invades-taiwan-before-gta-vi-716
```

## 分析结果输出

```json
{
  "market_a": {
    "question": "Russia-Ukraine Ceasefire before GTA VI?",
    "yes_price": 0.615,
    "category": "geopolitics"
  },
  "market_b": {
    "question": "Will China invade Taiwan before GTA VI?",
    "yes_price": 0.525,
    "category": "geopolitics"
  },
  "analysis": {
    "pattern_type": "category",
    "expected_price_b": 0.5575,
    "actual_price_b": 0.525,
    "mispricing": 0.0325,
    "confidence": "low"
  },
  "signal": {
    "action": "HOLD",
    "reason": "Mispricing (3.2%) below threshold"
  }
}
```

## 信号类型

| 信号 | 含义 |
|--------|---------|
| `HOLD` | 未检测到显著的价格异常 |
| `BUY_YES_B` | 市场 B 被低估，建议买入 |
| `BUY_NO_B` | 市场 B 被高估，建议不买入 |
| `BUY_YES_A` | 市场 A 被低估，建议买入 |
| `BUY_NO_A` | 市场 A 被高估，建议不买入 |

## 信心水平

- **高**：发现了特定的历史模式（阈值：5%）
- **中**：模式匹配度中等（阈值：8%）
- **低**：仅存在类别相关性（阈值：12%）

## 相关文件

```
src/
├── analyzer.py     # Main correlation analyzer
├── polymarket.py   # Polymarket API client
└── patterns.py     # Known correlation patterns
```

## 添加新的相关性模式

请编辑 `src/patterns.py` 文件以添加新的相关性模式：

```python
{
    "trigger_keywords": ["fed", "rate cut"],
    "outcome_keywords": ["s&p", "rally"],
    "conditional_prob": 0.70,  # P(rally | rate cut)
    "inverse_prob": 0.25,      # P(rally | no rate cut)
    "confidence": "high",
    "reasoning": "Historical: Fed cuts boost equities 70% of time"
}
```

## 注意事项

- 这仅是基于类别的相关性分析，可能存在误差；
- 特定模式需要人工审核和确认；
- 该工具未考虑市场流动性或价格滑点等因素；
- 本工具不提供投资建议，请自行进行充分研究。

## API 接口（实时可用！）

支持按请求计费的 API 接口（需启用 x402 访问权限）：

```
GET https://api.nshrt.com/api/v1/correlation?a=<slug>&b=<slug>
```

**费用：** 基础 L2 订阅费用为 0.05 美元 USD

**使用流程：**
1. 发送请求 → 收到“需要支付费用”的提示；
2. 根据提示向指定钱包付款；
3. 重新发送请求，并在请求头中添加 `X-Payment: <tx_hash>`；
4. 获取分析结果。

**仪表盘：** https://api.nshrt.com/dashboard

## 开发者

Gibson（[MoltBook 上的账号：@GibsonXO](https://moltbook.com/u/GibsonXO)）

专为代理经济（agent economy）设计。🦞