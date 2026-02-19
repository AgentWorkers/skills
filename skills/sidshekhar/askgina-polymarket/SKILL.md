---
name: askgina-polymarket
displayName: Polymarket via Gina
description: Fast setup for Claw bots: paste your Gina MCP token and start trading Polymarket in minutes.
version: 0.1.2
metadata:
  tags: polymarket, prediction-markets, trading, betting, gina, mcp, ask gina, crypto, agent, agentic, bot, automated
authors:
  - Gina (@askginadotai)
---

# 通过Gina使用Polymarket

利用Gina与AI进行Polymarket交易——您可以从任何MCP客户端进行搜索、下注、跟踪持仓并自动化交易策略。

**服务器地址：** `https://askgina.ai/ai/predictions/mcp`

## 使用此功能的用途

### 搜索与发现

- 按主题、运动项目、关键词或日期搜索预测市场
- 使用SQL分析市场数据（按交易量、流动性、结束时间、类别筛选）
- 查找即将到期的市场（抓住最后时刻的交易机会）
- 发现可设置自动化策略的重复性市场（支持BTC、ETH、SOL等，期限从5分钟到一个月不等）
- 浏览股票和指数预测市场（如AAPL、S&P 500、黄金）

### 交易

- 在Polymarket上下达市场订单和限价订单
- 跟踪您的持仓、盈亏及胜率
- 查看和取消未完成的订单
- 从已结束的市场中提取收益

### 自动化

- 设置交易规则——自动执行交易或发送提醒
- 每日市场简报、赔率变动提醒、投资组合概览
- 设置完全自动化的交易策略，帮助您进行市场扫描、筛选、交易和记录

## 操作方式

只需输入自然语言指令即可，无需特殊语法。

| 功能 | 示例指令 |
|---------|----------------|
| **开始使用** | `"Gina能做什么？"` `"给我一些可以尝试的使用案例"` |
| **搜索市场** | `"明天的NBA市场"` `"联邦利率决策的赔率"` |
| **热门市场** | `"Polymarket上哪些市场最热门？"` `"交易量最大的市场"` |
| **加密货币价格** | `"BTC 15分钟内的涨跌"` `"ETH当前每小时的价格走势"` |
| **股票与指数** | `"AAPL每日涨跌"` `"S&P 500每日走势"` |
| **到期市场** | `"2小时后到期的市场"` `"今晚结束的NBA比赛"` |
| **下注** | `"下注10美元赌湖人队获胜"` `"购买50美元的‘Yes’选项"` |
| **限价订单** | `"以0.40或更高的价格买入‘Yes’"` `"避免滑点"` |
| **查看持仓** | `"显示我的Polymarket持仓"` `"我的盈亏是多少？"` |
| **业绩分析** | `"我的胜率是多少？"` `"查看我的交易历史"` |
| **管理订单** | `"显示我的未完成订单"` `"取消所有待处理的限价订单"` |
| **提取收益** | `"提取我的收益"` `"我可以兑换什么？"` |
| **数据分析** | `"将加密货币市场数据导入SQL"` `"运行查询"` |
| **自动化操作** | `"上午9点发送每日市场简报"` `"在赔率变动时提醒我"` |

## 快速入门

1. 登录[askgina.ai](https://askgina.ai)，然后打开**代理设置**（侧边栏或访问`https://askgina.ai/agent-setup`）。
2. 为您的令牌命名（例如：“OpenClaw on MacBook”），然后点击**生成令牌**。
3. 立即复制连接配置信息——令牌仅显示一次。
4. 将配置信息粘贴到您的MCP客户端中：

```json
{
  "mcpServers": {
    "gina-predictions": {
      "transport": "http",
      "url": "https://askgina.ai/ai/predictions/mcp",
      "headers": {
        "Authorization": "Bearer <PASTE_TOKEN_HERE>"
      }
    }
  }
}
```

5. 重启您的MCP客户端，然后输入：“Gina能做什么？”

有关详细的客户端设置说明，请参阅[快速入门指南](https://docs.askgina.ai/predictions-mcp/quick-start)。

## 工作原理

- **身份验证**：在`https://askgina.ai/agent-setup`生成长期有效的JWT令牌。令牌有效期为90天。您最多可以拥有5个有效令牌，并可通过代理设置页面随时撤销其中任何一个。
- **钱包**：通过[Privy](https://privy.io)实现自我托管——您拥有自己的密钥。
- **交易**：交易在Polymarket（基于Polygon网络和USDC）上执行。
- **交易费用**：Gina提供交易费用补贴。
- **安全性**：大额交易在执行前需要明确确认。
- **自动化**：通过自然语言设置定时任务（如市场简报、提醒等），可随时管理。

## 安全注意事项

- 将令牌视为私钥——切勿公开分享
- 交易使用真实资金（Polymarket上的USDC）——确认前请务必仔细核对
- 先尝试只读功能（如搜索、热门市场查询），再开始交易
- 大额交易需要明确确认
- 如果怀疑令牌被泄露，请立即通过代理设置页面撤销令牌
- 如果身份验证流程要求输入私钥，请**不要继续操作**

## 链接

- **应用程序**：https://askgina.ai
- **文档**：https://docs.askgina.ai
- **功能介绍**：https://docs.askgina.ai/predictions-mcp/features
- **客户端设置**：https://docs.askgina.ai/predictions-mcp/client-setup
- **故障排除**：https://docs.askgina.ai/predictions-mcp/troubleshooting
- **服务条款**：https://askgina.ai/terms-and-conditions
- **Twitter**：https://x.com/askginadotai