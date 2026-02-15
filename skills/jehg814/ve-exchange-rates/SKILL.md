---
name: ve-exchange-rates
description: 获取委内瑞拉的汇率信息：包括委内瑞拉玻利瓦尔（BCV）的官方汇率、币安（Binance）平台上的P2P交易中USDT的平均汇率，以及两者之间的差价。当用户询问委内瑞拉美元的汇率、货币兑换差价（brecha cambiaria）、BCV对USDT的汇率或委内瑞拉境内的其他货币兑换信息时，可以使用这些数据。
---

# ve-exchange-rates: 委内瑞拉汇率

获取委内瑞拉的当前汇率：
1. **Tasa BCV** - 委内瑞拉中央银行的官方汇率
2. **Tasa USDT Binance P2P** - 来自P2P市场的平均汇率
3. **Brecha cambiaria** - 官方汇率与平行市场汇率之间的差价

## 使用方法

运行脚本以获取当前汇率：

```bash
~/clawd/skills/ve-exchange-rates/scripts/get-rates.sh
```

## 输出结果

脚本将返回以下信息：
- BCV的官方汇率（Bs/USD）
- Binance P2P平台的USDT汇率（买入价/卖出价/平均价）
- BCV与P2P市场汇率之间的差价百分比

## 数据来源

- **BCV汇率**：来自tcambio.app或finanzasdigital.com
- **USDT P2P汇率**：来自Binance P2P平台的API（p2p.binance.com）

## 注意事项

- 汇率数据通过API实时获取
- BCV汇率每天更新一次
- P2P市场汇率会根据市场情况不断波动
- 该脚本使用jq工具进行JSON数据解析