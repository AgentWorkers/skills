---
name: askgina-polymarket
displayName: Polymarket via Gina
description: 您可以使用自己的代理在 Polymarket 上执行搜索、交易以及自动化任何策略的操作。
version: 0.1.0
metadata:
  tags: polymarket, prediction-markets, trading, betting, gina, mcp, ask gina, crypto, agent, agentic, bot, automated
authors:
  - Gina (@askginadotai)
---

# 通过Gina使用Polymarket

使用Gina与AI进行Polymarket交易——您可以从任何MCP客户端进行搜索、下注、跟踪持仓并自动化交易策略。

**服务器URL：** `https://askgina.ai/ai/predictions/mcp`

## 该功能的用途

### 搜索与发现

- 按主题、运动项目、关键词或日期搜索预测市场
- 使用SQL分析市场数据（按交易量、流动性、结束时间、类别筛选）
- 查找即将到期的市场（最后时刻的交易机会）
- 发现可设置自动化策略的重复性市场（支持BTC、ETH、SOL等，期限从5分钟到一个月不等）
- 浏览股票和指数预测市场（如AAPL、S&P 500、黄金）

### 交易

- 在Polymarket上下达市场订单和限价订单
- 跟踪您的持仓、盈亏情况以及胜率
- 查看和取消未完成的订单
- 从已完成的交易中提取收益

### 自动化

- 设置交易规则——自动执行交易或发送提醒
- 提供每日市场简报、赔率变动警报以及投资组合概览
- 设置完全自动化的交易策略，帮助您进行市场扫描、筛选、交易和记录

## 操作方式

只需输入自然语言指令即可，无需特殊语法。

| 功能 | 示例指令 |
|---------|----------------|
| **搜索市场** | `"明天NBA市场的预测结果"` `"美联储利率决策的赔率"` |
| **热门市场** | `"Polymarket上哪些市场最热门？"` `"交易量和流动性最高的市场"` |
| **加密货币价格** | `"BTC 15分钟内的涨跌"` `"ETH当前每小时的价格走势"` |
| **股票和指数** | `"AAPL每日涨跌"` `"S&P 500每日走势"` |
| **到期市场** | `"2小时后到期的市场"` `"今晚结束的NBA比赛"` |
| **下注** | `"下注10美元赌湖人队获胜"` `"购买50美元的‘Yes’选项"` |
| **限价订单** | `"以0.40或更高的价格买入‘Yes’选项"` `"避免滑点"` |
| **查看持仓** | `"显示我在Polymarket上的所有持仓"` `"我的盈亏情况是多少？"` |
| **业绩分析** | `"我的胜率是多少？"` `"查看我的交易历史"` |
| **管理订单** | `"显示我所有的未完成订单"` `"取消所有待处理的限价订单"` |
| **提取收益** | `"提取我的收益"` `"我可以兑换什么？"` |
| **数据分析** | `"将加密货币市场数据导入SQL"` `"执行查询"` |
| **自动化操作** | `"每天上午9点发送市场简报"` `"在赔率变动时提醒我"` |

## 快速入门

1. 将服务器URL添加到您的MCP客户端（如Claude Code、Codex、Cursor、Windsurf等）。
2. 打开浏览器登录Gina并批准访问权限。
3. 开始使用相关功能。

有关详细的客户端设置说明，请参阅[快速入门指南](https://docs.askgina.ai/predictions-mcp/quick-start)。

## 工作原理

- **认证**：采用OAuth 2.1协议及PKCE机制——由您的客户端自动处理，无需管理API密钥。
- **钱包**：通过[Privy](https://privy.io)实现自我托管，您拥有自己的密钥。
- **交易**：在Polymarket（基于Polygon网络和USDC）上直接执行交易。
- **交易费用**：Gina提供费用补贴以降低交易成本。
- **安全性**：大额交易在执行前需要明确确认。
- **自动化**：通过自然语言指令设置定期执行的交易规则或提醒。

## 安全须知

- 交易使用真实资金（Polymarket上的USDC）——确认前请务必仔细核对。
- 先尝试只读功能（如搜索、热门市场查询），再开始交易。
- 大额交易需要明确确认。
- 如果认证流程要求输入私钥，请**切勿继续操作**。

## 链接

- **应用程序**：https://askgina.ai
- **文档**：https://docs.askgina.ai
- **功能介绍**：https://docs.askgina.ai/predictions-mcp/features
- **客户端设置**：https://docs.askgina.ai/predictions-mcp/client-setup
- **故障排除**：https://docs.askgina.ai/predictions-mcp/troubleshooting
- **服务条款**：https://askgina.ai/terms-and-conditions
- **Twitter账号**：https://x.com/askginadotai