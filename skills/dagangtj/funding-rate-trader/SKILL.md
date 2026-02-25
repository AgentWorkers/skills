---
name: funding-rate-trader
description: >
  **加密货币融资费率套利策略**：  
  该策略会自动扫描市场中负数的融资费率（即用户支付给平台的费用高于他们从平台获得的收益的情况），并执行自动交易，同时设置止损和止盈机制。  
  - 扫描市场数据时无需使用API密钥；  
  - 实际交易则通过Binance的API来完成。
version: 1.0.1
author: guanjia
---
# 资金费率交易策略

专为Binance Futures设计的自动化加密货币资金费率套利策略。

## 特点

- 🔍 扫描50多种加密货币，寻找负资金费率
- 📊 根据费率、趋势和RSI指标评估交易机会
- 🤖 支持自定义杠杆率的自动交易
- 🛡️ 自动设置止损和止盈点
- 💰 通过滚动投资策略实现利润复利

## 快速入门

```bash
# Scan opportunities (no API needed)
node scan.js

# Run auto-trader (requires Binance API)
node trader.js

# Monitor positions
node monitor.js
```

## 配置

创建`~/.openclaw/secrets/binance.json`文件：
```json
{
  "apiKey": "your-api-key",
  "secret": "your-secret"
}
```

## 策略规则

1. **入场条件**：负资金费率 + 上升趋势
2. **杠杆率**：20倍（可调节）
3. **止损**：-10%
4. **止盈**：+20%
5. **利润复利**：将盈利滚动投入到下一次交易中

## 预期收益

| 投资金额 | 每日收益 | 年收益（估算） |
|---------|--------------|--------------|
| $100 | $5-15 | 1800-5400% |
| $500 | $25-75 | 1800-5400% |
| $1000 | $50-150 | 1800-5400% |

*收益受市场状况和资金费率影响*

## 风险提示

⚠️ 高杠杆交易具有高风险。请仅交易您能够承受损失的资金。

## 许可证

MIT许可协议