---
name: hyperliquid-analyzer
version: 1.0.0
description: 分析Hyperliquid市场数据，提供交易洞察。支持实时价格监控、趋势分析及风险评估功能。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["curl", "jq"]
    primaryEnv: HYPERLIQUID_WALLET_ADDRESS
---
# Hyperliquid Market Analyzer

该工具用于分析Hyperliquid DEX上的市场状况，并提供可操作的交易建议。

## 主要功能

- 实时监控BTC、ETH、SOL和HYPE的价格
- 市场趋势分析（牛市/熊市/中性）
- 基于波动性的风险评估
- 财务组合余额追踪
- 在价格发生重大变动时发送警报

## 使用方法

### 检查市场状态

```bash
curl -s https://api.hyperliquid.xyz/info -X POST \
  -H "Content-Type: application/json" \
  -d '{"type": "metaAndAssetCtxs"}' | jq '.[0:4]'
```

### 获取当前价格

```bash
curl -s https://api.hyperliquid.xyz/info -X POST \
  -H "Content-Type: application/json" \
  -d '{"type": "allMids"}' | jq '{BTC: .BTC, ETH: .ETH, SOL: .SOL}'
```

## 分析功能

1. **趋势检测**：识别短期和中期市场趋势
2. **波动性分析**：衡量价格波动以评估风险
3. **支撑/阻力位**：计算关键价格水平
4. **市场情绪**：汇总市场情绪指标

## 示例输出

```
📊 Hyperliquid Market Analysis

Current Prices:
  BTC: $67,743 (+2.1% 24h)
  ETH: $1,971 (+1.5% 24h)
  SOL: $84.14 (-0.3% 24h)

Trend: BULLISH
Volatility: MEDIUM
Risk Level: 3/5

Recommendation: 
  BTC showing strong momentum. Consider long positions 
  with stop loss at $66,500.
```

## 配置

可选的环境变量：
- `HYPERLIQUID_WALLET_ADDRESS`：用于追踪财务组合的钱包地址
- `HYPERLIQUID_API_KEY`：用于身份验证的API密钥

## 注意事项

- 免费使用，基本功能无需API密钥
- 请求速率限制：每分钟120次
- 数据更新频率：每5秒一次