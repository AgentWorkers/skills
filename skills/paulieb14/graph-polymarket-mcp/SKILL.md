---
name: graph-polymarket-mcp
description: 通过 The Graph 查询 Polymarket 预测市场数据——提供 20 种工具，用于查看市场统计数据、交易者的盈亏情况、持仓信息、订单簿交易记录、未平仓合约数量、订单状态以及交易者资料。
metadata:
  {"openclaw": {"requires": {"bins": ["node"], "env": ["GRAPH_API_KEY"]}, "primaryEnv": "GRAPH_API_KEY", "homepage": "https://github.com/PaulieB14/graph-polymarket-mcp"}}
---
# Graph Polymarket MCP

通过 The Graph 的子图查询 Polymarket 的预测市场数据，包括市场统计信息、交易者的盈亏情况、持仓信息、订单簿交易记录、未平仓合约数量（open interest）、交易结果状态以及交易者资料。

## 工具

- **list_subgraphs**：列出所有可用的 Polymarket 子图及其描述和关键实体。
- **get_subgraph_schema**：获取特定子图的完整 GraphQL 架构。
- **query_subgraph**：对任何子图执行自定义的 GraphQL 查询。
- **get_market_data**：获取市场/条件数据及其结果状态。
- **get_global_stats**：平台统计信息：市场数量、交易量、费用等。
- **get_account_pnl**：交易者的盈亏情况及其绩效指标（胜率、盈利因子、最大回撤率）。
- **get_top_traders**：根据盈亏、胜率、交易量或盈利因子对交易者进行排名。
- **get_daily_stats**：每日交易量、费用、交易者数量及市场活动情况。
- **get_market_positions**：获取特定结果代币的顶级持有者及其盈亏情况。
- **get_user_positions**：获取用户的当前代币持仓情况。
- **get_recent_activity**：最近的分割、合并和赎回操作记录。
- **get_orderbook_trades**：获取最近的订单成交记录（支持做市商/撮合商过滤）。
- **get_market_open_interest**：根据锁定在 USDC 中的合约数量对市场进行排名。
- **get_oi_history**：特定市场的每小时未平仓合约数量快照。
- **get_global_open_interest**：整个平台的未平仓合约总数及市场数量。
- **get_market_resolution**：UMA 预言机交易结果状态（支持过滤）。
- **get_disputed_markets**：在预言机交易过程中存在争议的市场。
- **get_market_revisions**：市场交易结果相关的管理员干预和更新记录。
- **get_trader_profile**：完整的交易者资料：首次出现时间、CTF（Create Trade Event）事件、USDC 流动情况。
- **get_trader_usdc_flows**：交易者的 USDC 存款/提取历史记录（支持方向过滤）。

## 要求

- **运行环境**：Node.js >= 18（通过 `npx` 命令执行）。
- **环境变量**：
  - `GRAPH_API_KEY`（必填）：来自 [The Graph Studio](https://thegraph.com/studio/) 的免费 API 密钥。用于通过 The Graph Gateway 查询 8 个 Polymarket 子图。查询次数计入该密钥的使用量（免费 tier：每月 100,000 次查询）。

## 安装

```bash
GRAPH_API_KEY=your-key npx graph-polymarket-mcp
```

## 网络与数据行为

- 所有工具调用都会使用您的 API 密钥通过 The Graph Gateway (`gateway.thegraph.com`) 发送 GraphQL 请求。
- 共查询 8 个子图：Main、Beefy P&L、Slimmed P&L、Activity、Orderbook、Open Interest、Resolution 和 Traders（这些子图的 IPFS 哈希值已内置在服务器中）。
- 不使用本地数据库或持久化存储。
- SSE 传输方式（`--http` / `--http-only`）会在端口 3851 上启动本地 HTTP 服务器（可通过 `MCP_HTTP_PORT` 环境变量进行配置）。

## 使用场景

- 获取 Polymarket 平台的实时统计信息、交易量和市场排名。
- 分析交易者的盈亏情况、绩效指标及排名情况。
- 跟踪未平仓合约数量趋势和市场持仓情况。
- 监控市场交易结果的状态及存在争议的市场。
- 查询订单簿交易记录和持仓管理事件。
- 对 8 个专门的 Polymarket 子图执行自定义的 GraphQL 查询。