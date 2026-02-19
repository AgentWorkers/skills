---
name: horizon-trader
description: 交易预测市场（Polymarket、Kalshi）：查看持仓、提交订单、管理风险、发现新的交易机会，并计算最优的投注金额（Kelly-optimal sizing）。
emoji: "\U0001F4C8"
metadata:
  openclaw:
    requires:
      env:
        - HORIZON_API_KEY
    primaryEnv: HORIZON_API_KEY
    install:
      - id: pip
        kind: uv
        formula: horizon-sdk
        label: "Horizon SDK (pip install horizon-sdk)"
    homepage: https://docs.openclaw.ai/tools/clawhub
---
# Horizon Trader

您是一个由 Horizon SDK 提供支持的预测市场交易助手。

## 何时使用此技能

当用户询问以下内容时，请使用此技能：
- 查看他们的**持仓**、**盈亏**或**投资组合状态**
- 在预测市场上**提交**或**取消**订单
- 在 Polymarket 或 Kalshi 上**查找**或**搜索**市场或事件
- 计算**凯利最优**持仓规模
- 管理**风险**控制（紧急停止机制、止损、止盈）
- 查看**行情数据**或市场信息
- 在 Polymarket 上查询**钱包**活动、交易记录、持仓情况或用户信息
- 分析某个市场的**交易流量**或**主要持有者**
- 对投资组合风险进行**蒙特卡洛模拟**
- 执行**跨交易所套利**
- 与**预测市场交易**相关的任何操作

## 使用方法

通过 CLI 脚本运行命令。所有输出均为 JSON 格式。

```bash
python3 {baseDir}/scripts/horizon.py <command> [args...]
```

## 可用命令

### 投资组合与状态
```bash
# Engine status: PnL, open orders, positions, kill switch, uptime
python3 {baseDir}/scripts/horizon.py status

# List all open positions
python3 {baseDir}/scripts/horizon.py positions

# List open orders (optionally for a specific market)
python3 {baseDir}/scripts/horizon.py orders [market_id]

# List recent fills
python3 {baseDir}/scripts/horizon.py fills
```

### 交易
```bash
# Submit a limit order: quote <market_id> <side> <price> <size>
# side: buy or sell, price: 0-1 (probability)
python3 {baseDir}/scripts/horizon.py quote <market_id> buy 0.55 10

# Cancel a single order
python3 {baseDir}/scripts/horizon.py cancel <order_id>

# Cancel all orders
python3 {baseDir}/scripts/horizon.py cancel-all
```

### 市场搜索
```bash
# Search for markets on an exchange
python3 {baseDir}/scripts/horizon.py discover <exchange> [query] [limit]

# Examples:
python3 {baseDir}/scripts/horizon.py discover polymarket "bitcoin"
python3 {baseDir}/scripts/horizon.py discover kalshi "election" 5
```

### 凯利最优持仓规模计算
```bash
# Compute optimal position size: kelly <prob> <price> <bankroll> [fraction] [max_size]
python3 {baseDir}/scripts/horizon.py kelly 0.65 0.50 1000
python3 {baseDir}/scripts/horizon.py kelly 0.70 0.55 2000 0.5 50
```

### 风险管理
```bash
# Activate kill switch (emergency stop - cancels all orders)
python3 {baseDir}/scripts/horizon.py kill-switch on "market crash"

# Deactivate kill switch
python3 {baseDir}/scripts/horizon.py kill-switch off
```

### 行情数据与系统健康状况
```bash
# Get snapshot for a named feed
python3 {baseDir}/scripts/horizon.py feed <feed_name>

# List all feeds
python3 {baseDir}/scripts/horizon.py feeds

# Check feed staleness and health (optional threshold in seconds, default 30)
python3 {baseDir}/scripts/horizon.py feed-health [threshold]
```

### 条件订单
```bash
# List pending stop-loss/take-profit orders
python3 {baseDir}/scripts/horizon.py contingent
```

### 事件搜索
```bash
# Discover multi-outcome events on Polymarket
python3 {baseDir}/scripts/horizon.py discover-events "election"
python3 {baseDir}/scripts/horizon.py discover-events "" 5

# Get top markets by volume
python3 {baseDir}/scripts/horizon.py top-markets polymarket 10
python3 {baseDir}/scripts/horizon.py top-markets kalshi 5 "KXBTC"
```

### 钱包分析（Polymarket - 无需认证）
```bash
# Trade history for a wallet
python3 {baseDir}/scripts/horizon.py wallet-trades 0x1234... [limit] [condition_id]

# Trade history for a market
python3 {baseDir}/scripts/horizon.py market-trades 0xabc... [limit] [side] [min_size]

# Open positions for a wallet (sort: TOKENS, CURRENT, CASHPNL, PERCENTPNL, etc.)
python3 {baseDir}/scripts/horizon.py wallet-positions 0x1234... 50 CURRENT

# Total portfolio value in USD
python3 {baseDir}/scripts/horizon.py wallet-value 0x1234...

# Public profile (pseudonym, bio, X handle)
python3 {baseDir}/scripts/horizon.py wallet-profile 0x1234...

# Top holders in a market
python3 {baseDir}/scripts/horizon.py top-holders 0xabc... [limit]

# Trade flow analysis (buy/sell volume, net flow, top buyers/sellers)
python3 {baseDir}/scripts/horizon.py market-flow 0xabc... [trade_limit] [top_n]
```

### 蒙特卡洛模拟
```bash
# Simulate portfolio risk (uses current engine positions)
python3 {baseDir}/scripts/horizon.py simulate [scenarios] [seed]
python3 {baseDir}/scripts/horizon.py simulate 50000
python3 {baseDir}/scripts/horizon.py simulate 10000 42
```

### 套利
```bash
# Execute atomic cross-exchange arb: arb <market_id> <buy_exchange> <sell_exchange> <buy_price> <sell_price> <size>
python3 {baseDir}/scripts/horizon.py arb will-btc-hit-100k kalshi polymarket 0.48 0.52 10
```

## 流程组件（v0.3.0）

Horizon SDK 还提供了用于自动化策略的高级流程组件：
- **市场状态检测**（`regime_signal`）：市场波动性/趋势分类（0=平静，1=波动）
- **行情数据保护**（`feed_guard`）：当行情数据失效时自动触发紧急停止机制
- **持仓风险调整**（`inventory_skewer`）：调整报价以降低持仓风险
- **动态价差管理**（`adaptive_spread`）：根据成交率、波动性和订单不平衡情况动态调整价差
- **执行跟踪**（`execution_tracker`）：监控成交率、滑点和不利选择情况
- **多策略管理**：通过字典配置针对不同市场运行多种策略
- **跨市场对冲**（`cross_hedger`）：当投资组合的Delta值超过阈值时生成对冲报价

这些是使用 `hz.run()` 运行的 Python 流程函数。详情请参阅 SDK 文档。

## 输出格式

所有命令返回 JSON 格式。成功时直接返回数据；失败时返回 `{"error": "message"}`。

## 重要说明

- `quote` 命令会提交**实际订单**（或根据配置提交模拟订单）。提交前请务必确认用户需求。
- `kill-switch on` 命令是一个**紧急停止**操作，会立即取消所有订单。
- 价格表示为 0 到 1 之间的**概率**（例如，0.65 表示 65% 的隐含概率）。
- 交易所配置通过 `HORIZON_EXCHANGE` 环境变量设置（默认为模拟交易）。

完整文档：https://docs.openclaw.ai/tools/clawhub