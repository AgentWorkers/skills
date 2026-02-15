# Polymarket 自动交易技能

**使 AI 代理能够在 Polymarket 上自主进行预测市场交易。**

## 概述

该技能为 AI 代理提供了以下功能：
- 📊 获取实时市场数据和赔率
- 💰 自动下达买卖订单
- 📈 监控持仓和盈亏情况
- 🎯 执行交易策略
- ⚖️ 管理风险和投资组合分配
- 🔔 接收市场动态警报

## 先决条件

### 1. Polymarket 账户
- 在 [polymarket.com](https://polymarket.com) 注册
- 如有需要，完成身份验证（KYC）
- 用 USDC 充值您的钱包

### 2. API 凭据
Polymarket 使用基于钱包的认证系统：
- 私钥用于签署交易
- API 密钥用于访问 CLOB（中央限价订单簿）

### 3. 钱包设置
您需要：
- Ethereum 钱包私钥
- Polygon 网络上的 USDC
- Polymarket 提供的 API 凭据

## 快速入门

### 1. 配置凭据

创建 `~/.config/polymarket/credentials.json` 文件：
```json
{
  "privateKey": "YOUR_WALLET_PRIVATE_KEY",
  "apiKey": "YOUR_POLYMARKET_API_KEY",
  "apiSecret": "YOUR_API_SECRET",
  "rpcUrl": "https://polygon-rpc.com"
}
```

或设置环境变量：
```bash
export POLYMARKET_PRIVATE_KEY="your_private_key"
export POLYMARKET_API_KEY="your_api_key"
export POLYMARKET_API_SECRET="your_api_secret"
```

### 2. 浏览市场
```bash
./scripts/list-markets.sh --category politics --limit 10
```

### 3. 下单交易
```bash
./scripts/place-order.sh \
  --market "0x1234..." \
  --side buy \
  --outcome yes \
  --amount 10 \
  --price 0.65
```

### 4. 查看持仓
```bash
./scripts/check-positions.sh
```

## 核心脚本

### `list-markets.sh` - 浏览可用市场
查找可交易的市场：
```bash
# List all active markets
./scripts/list-markets.sh

# Filter by category
./scripts/list-markets.sh --category politics
./scripts/list-markets.sh --category crypto
./scripts/list-markets.sh --category sports

# Search by keyword
./scripts/list-markets.sh --search "Trump"

# Sort by volume or liquidity
./scripts/list-markets.sh --sort volume --limit 20
```

### `place-order.sh` - 执行交易
下达买卖订单：
```bash
# Buy YES shares
./scripts/place-order.sh \
  --market "0xabc123..." \
  --side buy \
  --outcome yes \
  --amount 50 \
  --price 0.62

# Sell NO shares
./scripts/place-order.sh \
  --market "0xabc123..." \
  --side sell \
  --outcome no \
  --amount 25 \
  --price 0.38

# Market order (best available price)
./scripts/place-order.sh \
  --market "0xabc123..." \
  --side buy \
  --outcome yes \
  --amount 100 \
  --type market
```

**参数：**
- `--market`（必填）：市场 ID
- `--side`（必填）：买入或卖出
- `--outcome`（必填）：yes 或 no
- `--amount`（必填）：USDC 数量
- `--price`：限价（0-1 的比例，例如 0.65 = 65%）
- `--type`：限价（默认）或市场价

### `check-positions.sh` - 监控投资组合
查看当前持仓：
```bash
# All positions
./scripts/check-positions.sh

# Specific market
./scripts/check-positions.sh --market "0xabc123..."

# Include P&L calculation
./scripts/check-positions.sh --show-pnl

# Export to JSON
./scripts/check-positions.sh --format json > positions.json
```

### `market-data.sh` - 获取市场信息
获取市场详情和订单簿：
```bash
# Market info
./scripts/market-data.sh --market "0xabc123..."

# Current odds
./scripts/market-data.sh --market "0xabc123..." --odds

# Full orderbook
./scripts/market-data.sh --market "0xabc123..." --orderbook

# Recent trades
./scripts/market-data.sh --market "0xabc123..." --trades --limit 50
```

### `cancel-order.sh` - 取消未成交订单
```bash
# Cancel specific order
./scripts/cancel-order.sh --order-id "order_123"

# Cancel all orders in market
./scripts/cancel-order.sh --market "0xabc123..."

# Cancel all open orders
./scripts/cancel-order.sh --all
```

## 交易策略

### 示例 1：价值投注
买入被低估的资产：
```bash
./examples/value-betting.sh \
  --min-edge 0.05 \
  --max-position 100 \
  --categories "politics,crypto"
```

策略：
- 扫描市场中的价格异常
- 将 Polymarket 的赔率与其他预测市场进行比较
- 当优势超过 5% 时进行投注

### 示例 2：套利
利用价格差异：
```bash
./examples/arbitrage.sh \
  --min-profit 0.02 \
  --max-position 500
```

策略：
- 找到互补的市场（“YES”和“NO”的总价值应为 1 美元）
- 在发现价格错误时执行配对交易
- 确保无风险利润

### 示例 3：趋势跟随
跟随市场趋势：
```bash
./examples/trend-following.sh \
  --lookback 24h \
  --threshold 0.10 \
  --position-size 50
```

策略：
- 长期跟踪价格走势
- 进入显示强劲趋势的持仓
- 在趋势反转时退出

### 示例 4：基于新闻的交易
对事件做出反应：
```bash
./examples/news-trader.sh \
  --keywords "election,poll" \
  --reaction-time 60 \
  --max-position 200
```

策略：
- 监控新闻动态和 Twitter
- 识别能影响市场的事件
- 在赔率调整前进行交易

## 高级用法

### 投资组合管理
```bash
# Set risk limits
./scripts/set-limits.sh \
  --max-per-market 100 \
  --max-total 1000 \
  --max-exposure 0.20

# Rebalance portfolio
./scripts/rebalance.sh \
  --target-allocation portfolio.json
```

### 自动交易机器人
运行连续交易：
```bash
# Start trading bot
./scripts/trading-bot.sh \
  --strategy value \
  --interval 5m \
  --capital 1000 \
  --log bot.log &

# Monitor bot
tail -f bot.log

# Stop bot
./scripts/stop-bot.sh
```

### 回测
在历史数据上测试策略：
```bash
./scripts/backtest.sh \
  --strategy examples/value-betting.sh \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --initial-capital 1000
```

## 风险管理

### 持仓规模控制
```bash
# Kelly Criterion sizing
./scripts/calculate-position.sh \
  --edge 0.10 \
  --bankroll 1000 \
  --kelly-fraction 0.25

# Fixed percentage
./scripts/calculate-position.sh \
  --bankroll 1000 \
  --risk-percent 2
```

### 止损/止盈
```bash
# Set automated exits
./scripts/set-exit-rules.sh \
  --market "0xabc123..." \
  --stop-loss -20 \
  --take-profit 50
```

## 市场类别
Polymarket 提供以下类别的市场：
- 🏛️ **政治**：选举、政策结果
- 💰 **加密货币**：比特币价格、ETH 重要节点
- ⚽ **体育**：比赛结果、锦标赛
- 📈 **经济**：美联储决策、GDP 增长
- 🎬 **娱乐**：奖项、票房收入
- 🌍 **世界事件**：地缘政治、自然灾害

## 了解 Polymarket 的运作机制

### 赔率如何计算
价格代表概率：
- `0.65` = 65% 的“YES”概率
- 市场做市商确保“YES”和“NO”的总价值约为 1 美元

### 费用
- 交易费：利润的 2%
- 网络费用：根据 Polygon 网络情况而定
- 提现费用：取决于网络

### 结算
市场在以下情况下结算：
- 事件发生或截止日期到期
- 官方来源确认结果
- 获胜的份额价值 1 美元
- 失败的份额价值 0 美元

## 集成模式

### 1. 定时交易
每小时运行一次策略：
```bash
# Add to cron
0 * * * * /path/to/scripts/trading-bot.sh --strategy value
```

### 事件驱动交易
在收到 Telegram 消息时触发交易：
```bash
# Clawdbot integration
if message contains "trade polymarket Trump"; then
  ./scripts/place-order.sh --market trump-2024 --side buy --amount 50
fi
```

### 投资组合仪表板
通过网页界面进行监控：
```bash
# Start dashboard server
./scripts/dashboard.sh --port 3000
# Visit http://localhost:3000
```

## 故障排除

### “余额不足”
```bash
# Check USDC balance
./scripts/check-balance.sh

# Deposit more USDC to Polygon wallet
```

### “订单失败”
```bash
# Check order status
./scripts/check-order.sh --order-id "order_123"

# Review gas settings
./scripts/place-order.sh --gas-price 50 --gas-limit 300000
```

### “市场未找到”
```bash
# Verify market ID
./scripts/market-data.sh --market "0x..."

# Search for market by keyword
./scripts/list-markets.sh --search "keyword"
```

## API 使用限制
- 市场数据：每分钟 100 次请求
- 下单：每分钟 20 次请求
- 持仓查询：每分钟 50 次请求

请遵守这些限制以避免临时禁令。

## 安全最佳实践
1. **切勿泄露私钥** - 使用环境变量
2. **从小规模开始** - 先用少量资金进行测试
3. **设置持仓限额** - 限制最大风险敞口
4. **使用冷存储** - 将大部分资金存储在离线环境中
5. **定期监控** - 每日检查持仓
6. **启用双重认证** - 在 Polymarket 账户上启用
7. **审核交易** - 审查所有交易记录

## 示例工作流程

### 工作流程 1：每日价值扫描
```bash
#!/bin/bash
# Scan for value bets every morning

# Get top markets
MARKETS=$(./scripts/list-markets.sh --sort volume --limit 50 --format json)

# For each market
echo "$MARKETS" | jq -r '.[] | .id' | while read MARKET; do
  # Get current odds
  ODDS=$(./scripts/market-data.sh --market "$MARKET" --odds)
  
  # Calculate edge vs. your model
  EDGE=$(calculate_edge "$ODDS")
  
  # Place bet if edge > 5%
  if (( $(echo "$EDGE > 0.05" | bc -l) )); then
    ./scripts/place-order.sh --market "$MARKET" --side buy --amount 20
  fi
done
```

### 工作流程 2：对冲现有持仓
```bash
# If you're long YES at 60¢, hedge by selling at 70¢
./scripts/place-order.sh \
  --market "0xabc..." \
  --side sell \
  --outcome yes \
  --amount 50 \
  --price 0.70 \
  --type limit
```

## 资源
- [Polymarket 文档](https://docs.polymarket.com)
- [CLOB API 参考](https://docs.polymarket.com/api)
- [Polygon 网络](https://polygon.technology)
- [Polygon 上的 USDC](https://www.circle.com/en/usdc)

## 常见问题

**Q：我可能会损失超过投资金额吗？**
A：不会。最大损失为您支付的份额金额。

**Q：市场何时结算？**
A：因事件而异。选举市场的结算通常在官方结果公布后的几天内完成。

**Q：我可以随时提现吗？**
A：可以。您可以出售份额或等待结算后提取 USDC。

**Q：如果市场从未结算怎么办？**
A：Polymarket 提供争议解决机制，必要时会退还资金。

**Q：这合法吗？**
A：Polymarket 全球范围内运营，但请遵守当地法规。

## 支持方式
- Polymarket Discord：[discord.gg/polymarket](https://discord.gg/polymarket)
- GitHub 问题报告：提交技能相关问题
- ClawdHub：`clawdhub install polymarket-trading`

## 许可证
MIT 许可证 - 可自由使用和修改

## 致谢
由 Kelly Claude（AI 代理）开发  
基于 Polymarket CLOB API 运行  
发布到 ClawdHub，供 AI 代理社区使用

---

**准备好自主进行预测市场交易了吗？**

```bash
clawdhub install polymarket-trading
```

让您的 AI 代理全天候进行数据驱动的投注吧。