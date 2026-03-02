---
name: edge
description: >
  **使用场景：**  
  当用户询问有关加密货币代币、交易、投资组合或价格警报的相关信息时使用。
---
# Edge

通过 `edge` MCP 服务器提供的工具：

- **search** — 按名称或地址查找代币
- **inspect** — 提供 9 种视图：token_overview、pair_metrics、token_holders、token_analytics、graduation、pair_overview、pair_candles、pair_swaps（token_holders 包含 sniper/insider 标志）
- **screen** — 按市值（mcap）、流动性、狙击者比例（sniper %）、内部人士比例（insider %）以及社交活跃度进行筛选
- **portfolio** — 查看持仓情况、交易历史、顶级交易者信息、钱包余额及原生货币余额
- **trade** — 下限订单、制定入场/出场策略、分析价格影响
- **alerts** — 支持订阅/轮询/取消订阅；支持通过 Webhook 接收警报

## 使用模式：

1. **先获取价格信息再下单**：执行 `inspect pair_metrics` → 计算目标价格 → 然后执行 `trade place`
2. **从代币到交易对**：执行 `inspect token_overview` 可获取 `pairAddress`
3. **链ID**：`"8453"` 代表 Base Chain；`"1"` 代表 Ethereum；`"42161"` 代表 Arbitrum
4. **警报设置**：首次订阅后，每轮更新时轮询一次；清理数据后取消订阅

[文档](https://docs.trade.edge/agents)