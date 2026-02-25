---
name: fear-and-greed
description: 访问 Alternative.me 的 Crypto Fear & Greed Index（加密货币恐惧与贪婪指数）。利用该工具来作为你的市场情绪分析基准，判断整个零售市场是处于极度恐惧状态（存在投降风险）还是极度贪婪状态（存在泡沫破裂/调整风险）。
homepage: https://alternative.me/crypto/fear-and-greed-index/
metadata:
  {
    "openclaw": {
      "emoji": "😨",
      "requires": {},
    },
  }
---
# 加密恐惧与贪婪指数 API

您可以使用免费的 Alternative.me API 来获取全球加密货币市场的情绪基准。

## API 端点

基础 URL：`https://api.alternative.me/fng/`

该 API 不需要任何身份验证或 API 密钥。

### 获取当前情绪指数

获取最新的每日恐惧与贪婪指数（0-100 分数 + 分类标签）：

```bash
curl -s "https://api.alternative.me/fng/?limit=1"
```

返回的 JSON 结构包含：
- `value`：0-100 的数值分数。
- `value_classification`：文本标签（例如：“极度恐惧”、“恐惧”、“贪婪”、“极度贪婪”）。
- `timestamp`：数据点的 Unix 时间戳。

## 常见使用场景

### 情绪基准的参考
在对新闻标题或链上数据流进行定性情绪分析时，首先获取恐惧与贪婪指数，以便为您关于散户心理的假设提供参考。

1. 如果 `value` < 25（极度恐惧）：市场对看跌因素非常敏感，价格可能被人为压低。
2. 如果 `value` > 75（极度贪婪）：市场情绪高涨，投资者忽视风险，存在突然抛售或价格回调的高风险。