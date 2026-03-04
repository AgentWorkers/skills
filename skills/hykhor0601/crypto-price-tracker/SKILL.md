---
name: crypto-trading-assistant
description: 实时加密货币交易智能与投资组合跟踪功能。适用于监控加密货币价格、追踪以太坊持仓情况、计算杠杆使用情况、分析去中心化金融（DeFi）协议、设置价格警报，以及汇总加密货币市场新闻和情绪数据。
version: 1.0.0
metadata:
  openclaw:
    emoji: "₿"
    requires:
      anyBins: ["curl", "jq"]
    os: ["linux", "darwin", "win32"]
---
# 加密货币交易助手

实时提供加密货币交易信息、投资组合跟踪和市场分析功能，专为活跃的交易者设计，让他们无需离开终端即可快速获取比特币（BTC）、以太坊（ETH）及主要山寨币的行情数据。

## 使用场景

- 查看比特币、以太坊或任何加密货币的当前价格
- 通过实时价格更新跟踪投资组合价值
- 计算使用杠杆（2倍、3倍、5倍）时的盈亏情况
- 监控去中心化金融（DeFi）协议的总锁定价值（TVL）和收益率
- 设置价格警报以确定入场/出场时机
- 汇总加密货币新闻和市场情绪
- 分析链上指标（如交易手续费、市场情绪）
- 利用实时数据快速进行投资组合计算

## 快速价格查询

通过CryptoCompare API获取即时价格（无需API密钥）：

```bash
# Bitcoin price
curl -s "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD" | jq -r '.USD'
# Output: 67604.52

# Ethereum price
curl -s "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD" | jq -r '.USD'
# Output: 3234.56

# Multiple coins at once with full data
curl -s "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL&tsyms=USD" | jq '.RAW | to_entries | map({coin: .key, price: .value.USD.PRICE, change24h: .value.USD.CHANGEPCT24HOUR})'
# Shows price + 24h change for BTC, ETH, SOL
```

另一种数据来源（Blockchain.info）：

```bash
# All major coins from Blockchain.info
curl -s "https://blockchain.info/ticker" | jq -r 'to_entries[] | "\(.key): $\(.value.last)"'
# Shows all available currency pairs
```

## 投资组合跟踪

自动计算您的持仓价值：

```bash
# Single-line portfolio calculator
# Replace with your holdings
BTC_AMOUNT=0.5
ETH_AMOUNT=12.5
SOL_AMOUNT=250

# Get prices and calculate
BTC_PRICE=$(curl -s "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD" | jq -r '.USD')
ETH_PRICE=$(curl -s "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD" | jq -r '.USD')
SOL_PRICE=$(curl -s "https://min-api.cryptocompare.com/data/price?fsym=SOL&tsyms=USD" | jq -r '.USD')

BTC_VALUE=$(echo "$BTC_AMOUNT * $BTC_PRICE" | bc -l)
ETH_VALUE=$(echo "$ETH_AMOUNT * $ETH_PRICE" | bc -l)
SOL_VALUE=$(echo "$SOL_AMOUNT * $SOL_PRICE" | bc -l)
TOTAL=$(echo "$BTC_VALUE + $ETH_VALUE + $SOL_VALUE" | bc -l)

echo "Portfolio Value:"
echo "BTC: $BTC_AMOUNT × \$$BTC_PRICE = \$$(printf '%.2f' $BTC_VALUE)"
echo "ETH: $ETH_AMOUNT × \$$ETH_PRICE = \$$(printf '%.2f' $ETH_VALUE)"
echo "SOL: $SOL_AMOUNT × \$$SOL_PRICE = \$$(printf '%.2f' $SOL_VALUE)"
echo "---"
echo "Total: \$$(printf '%.2f' $TOTAL)"
```

## 杠杆计算器

计算使用杠杆时的盈亏情况：

```bash
# 3x leverage ETH position calculator
# Entry: $3000, Current: $3200, Position: $10,000, Leverage: 3x
ENTRY=3000
CURRENT=3200
POSITION=10000
LEVERAGE=3

echo "Position: \$${POSITION} @ ${LEVERAGE}x leverage on ETH" | awk -v entry=$ENTRY -v current=$CURRENT -v pos=$POSITION -v lev=$LEVERAGE '{
  price_change_pct = ((current - entry) / entry) * 100
  leveraged_return_pct = price_change_pct * lev
  profit = pos * (leveraged_return_pct / 100)
  liquidation_price = entry * (1 - (1 / lev) + 0.05)
  
  printf "Entry: $%.2f | Current: $%.2f (%.2f%%)
", entry, current, price_change_pct
  printf "Leveraged Return: %.2f%%
", leveraged_return_pct
  printf "Profit/Loss: $%.2f
", profit
  printf "Liquidation Price (~): $%.2f
", liquidation_price
}'
```

快速了解杠杆清算情况：

```bash
# Quick calculator for any leverage
ENTRY_PRICE=3000
LEVERAGE=3
LIQ_PRICE=$(echo "$ENTRY_PRICE * (1 - (1 / $LEVERAGE) + 0.05)" | bc -l)
echo "Entry: \$$ENTRY_PRICE | Leverage: ${LEVERAGE}x | Liquidation: \$$(printf '%.2f' $LIQ_PRICE)"
```

## 去中心化金融协议监控

监控主要DeFi协议的总锁定价值（TVL）：

```bash
# Top DeFi protocols by TVL
curl -s "https://api.llama.fi/protocols" | jq -r '.[:10] | .[] | "\(.name): $\(.tvl / 1e9 | floor)B"'
# Output: Lists top 10 protocols with TVL in billions

# Specific protocol (e.g., Uniswap)
curl -s "https://api.llama.fi/protocol/uniswap" | jq '{name: .name, tvl: .tvl, change_24h: .change_1d}'

# Track your favorite protocols
for protocol in uniswap aave lido curve; do
  echo -n "$protocol: "
  curl -s "https://api.llama.fi/protocol/$protocol" | jq -r '"\(.tvl / 1e9 | floor * 1)B TVL"'
done
```

## 设置价格警报

创建简单的价格警报系统：

```bash
# Bitcoin alert script (save as btc-alert.sh)
#!/bin/bash
TARGET_PRICE=70000
CURRENT=$(curl -s "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD" | jq -r '.USD')

if (( $(echo "$CURRENT > $TARGET_PRICE" | bc -l) )); then
  osascript -e "display notification "Bitcoin hit \$$CURRENT!" with title "Price Alert""
  # Or use: echo "BTC Alert: \$$CURRENT" | mail -s "Price Alert" you@email.com
fi
```

将警报脚本添加到crontab中以自动执行：

```bash
chmod +x btc-alert.sh
# Add to crontab (every 5 minutes)
*/5 * * * * /path/to/btc-alert.sh
```

## 市场情绪分析

比特币恐惧与贪婪指数：

```bash
# Current fear & greed
curl -s "https://api.alternative.me/fng/?limit=1" | jq -r '.data[0] | "Fear & Greed: \(.value)/100 (\(.value_classification))"'
# Output: Fear & Greed: 10/100 (Extreme Fear)

# 7-day history
curl -s "https://api.alternative.me/fng/?limit=7" | jq -r '.data[] | "\(.timestamp | strftime("%Y-%m-%d")): \(.value) (\(.value_classification))"'
```

## 多币种价格监控

实时监控多种加密货币的价格：

```bash
# Watch mode - updates every 10 seconds
watch -n 10 'curl -s "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,BNB&tsyms=USD" | jq -r ".RAW | to_entries[] | "\(.key): $\(.value.USD.PRICE | floor) (24h: \(.value.USD.CHANGEPCT24HOUR | floor)%)""'

# One-time check with formatted output
curl -s "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,BNB,ADA,XRP&tsyms=USD" | jq -r '.RAW | to_entries | sort_by(.value.USD.PRICE) | reverse | .[] | 
"\(.key): $\(.value.USD.PRICE | floor | tostring) | 24h: \(.value.USD.CHANGEPCT24HOUR | tonumber | floor | tostring)% | Vol: $\(.value.USD.VOLUME24HOUR / 1e6 | floor | tostring)M"'
```

## 历史价格数据

获取历史价格数据进行分析：

```bash
# Last 30 days daily close for BTC
curl -s "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=30" | jq -r '.Data.Data[] | "\(.time | strftime("%Y-%m-%d")): $\(.close | floor)"'

# Hourly prices for last 24 hours
curl -s "https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=24" | jq '.Data.Data | map(.close) | {min: min, max: max, avg: (add/length), current: .[-1]}'
```

## 常见加密货币及其API符号

CryptoCompare API支持的常见加密货币符号：

| 加密货币 | 符号 | 名称 |
|------|---------|---------|
| 比特币 | `BTC` | Bitcoin |
| 以太坊 | `ETH` | Ethereum |
| Solana | `SOL` | Solana |
| BNB | `BNB` | BNB |
| XRP | `XRP` | Ripple |
| Cardano | `ADA` | Cardano |
| Dogecoin | `DOGE` | Dogecoin |
| Polygon | `MATIC` | Polygon |
| Avalanche | `AVAX` | Avalanche |
| Chainlink | `LINK` | Chainlink |

## API使用限制与密钥

**免费API（无需密钥）**：
- CryptoCompare：每月10万次请求的免费额度（非常慷慨）
- DeFi Llama：无严格使用限制
- Alternative.me（恐惧与贪婪指数）：无使用限制
- Blockchain.info：无严格使用限制

**如需更多请求，请升级服务**：
- CryptoCompare Pro：无限请求，每月50美元（通常无需）

基本使用无需API密钥！

## 高级功能：价格变化追踪

跟踪价格随时间的变化情况：

```bash
# Save current prices to file
echo "$(date +%s),$(curl -s 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD' | jq -r '.USD')" >> btc_prices.log

# Calculate change from 1 hour ago (if you have hourly logs)
CURRENT=$(tail -1 btc_prices.log | cut -d',' -f2)
ONE_HOUR_AGO=$(tail -13 btc_prices.log | head -1 | cut -d',' -f2)
CHANGE=$(echo "scale=2; (($CURRENT - $ONE_HOUR_AGO) / $ONE_HOUR_AGO) * 100" | bc)
echo "1h change: $CHANGE%"
```

## 使用建议

- **CryptoCompare非常可靠**：免费额度每月可进行10万次请求，完全满足个人使用需求。基本请求无需API密钥。
- **务必计算清算价格**：使用杠杆时，清算通常发生在价格下跌约（100/杠杆百分比）时。请额外预留5%的缓冲空间以应对费用。3倍杠杆的情况下，价格下跌约28%时会发生清算。
- **先从小额交易开始测试**：在尝试使用3倍杠杆交易以太坊之前，先通过小额交易测试相关机制和风险。
- **保护你的资产**：将大额资金存放在硬件钱包（如Ledger、Trezor）中。交易所黑客攻击仍时有发生。
- **恐惧与贪婪指数具有反向指导作用**：当指数显示“极度贪婪”（>75）时，市场往往会出现调整；“极度恐惧”（<25）可能预示着买入机会。
- **自动化警报，避免盲目交易**：设置价格警报，遵循既定策略。
- **高收益率的DeFi项目风险较高**：高年化收益率（APY）往往伴随着高风险（如智能合约漏洞或不可持续的代币经济模型）。
- **关注TVL变化**：DeFi协议TVL的突然下降可能预示市场避险情绪或协议问题。注意每日TVL变化超过20%的情况。
- **杠杆会放大收益和损失**：3倍杠杆意味着收益和损失都会放大3倍。如果价格下跌10%，你的保证金将损失30%。请根据风险调整持仓规模。
- **使用`bc`命令进行计算**：`bc -l`命令能准确处理小数运算，对bash环境中的财务计算至关重要。

## 安全提示

本工具提供市场数据和计算功能，但**不构成财务建议**。加密货币交易风险极高且价格波动剧烈，您可能会损失全部投资。请务必：
- 自行进行充分研究（DYOR）
- 仅投资您能够承受的损失金额
- 在使用杠杆前了解其风险（清算可能迅速发生）
- 提防诈骗和网络钓鱼（验证URL，使用双重身份验证）
- 考虑所在地区的税收规定
- 从小额交易开始，逐步熟悉相关工具

---

**技能版本**：1.0.0  
**最后更新时间**：2026年3月  
**作者**：HY  
**许可证**：MIT  
**已测试的API**：CryptoCompare ✅ | DeFi Llama ✅ | Fear & Greed ✅