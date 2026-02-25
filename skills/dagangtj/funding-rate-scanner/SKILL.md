---
name: funding-rate-scanner
version: 1.0.1
description: 扫描加密货币的融资费率，寻找套利机会。无需使用 API 密钥。
---
# 资金费率扫描器

扫描所有加密货币永续期期货的资金费率，寻找高收益的套利机会。

## 主要功能

- 扫描币安期货平台上的500多种加密货币
- 发现极低的资金费率（通过做多获利）
- 计算不同杠杆水平下的年化收益率
- 监测资金费率随时间的变化

## 使用方法

```bash
# Scan top opportunities
node scripts/scan.js

# Monitor specific coins
node scripts/monitor.js DUSK DASH AXS

# Get detailed analysis
node scripts/analyze.js DUSK
```

## 输出示例

```
=== Funding Rate Opportunities ===

Rank  Coin    Rate      Annual(5x)  Volume
1     DUSK    -0.38%    2071%       $30M
2     AXS     -0.12%    655%        $46M
3     DASH    -0.12%    649%        $50M

Next settlement: 03:00 UTC (2h away)
```

## 套利策略

当资金费率为负时，每8小时短仓向长仓支付费用：

1. 在资金费率极低的加密货币上开多仓
2. 每8小时收取一次费用（每天三次）
3. 设置止损以限制损失
4. 从资金费率和潜在的价格上涨中获利

## 风险提示

- 高杠杆意味着高风险
- 资金费率可能会发生变化
- 必须始终使用止损机制
- 只投资你能承受的损失金额