---
name: askgina-polymarket
displayName: Polymarket via Gina
description: Fast setup for Claw bots: paste your Gina MCP token and start trading Polymarket in minutes.
version: 0.1.1
metadata:
  tags: polymarket, prediction-markets, trading, betting, gina, mcp, ask gina, crypto, agent, agentic, bot, automated
authors:
  - Gina (@askginadotai)
---

# 通过Gina使用Polymarket

使用AI进行Polymarket交易——从任何MCP客户端搜索、下注、跟踪持仓并自动化交易策略。

**服务器地址：** `https://askgina.ai/ai/predictions/mcp`

## 使用此功能的用途

### 搜索与发现

- 按主题、运动项目、关键词或日期搜索预测市场
- 使用SQL分析市场数据（按交易量、流动性、结束时间、类别筛选）
- 查找即将到期的市场（最后时刻的交易机会）
- 发现可设置自动化策略的重复性市场（BTC、ETH、SOL——期限从5分钟到一个月不等）
- 浏览股票和指数预测市场（AAPL、S&P 500、黄金）

### 交易

- 在Polymarket上下达市价单和限价单
- 跟踪您的持仓、盈亏和胜率
- 查看和取消未成交的订单
- 从已结算的市场中提取收益

### 自动化

- 设置交易规则——安排自动化的交易或提醒任务
- 每日市场简报、赔率变动提醒、投资组合概览
- 设置完全自动化的交易策略，负责市场扫描、筛选、交易和记录

## 操作方式

只需输入自然语言指令即可，无需特殊语法。

| 功能 | 示例指令 |
|---------|----------------|
| **搜索市场** | `"搜索明天的NBA市场"` `"查询美联储利率决策的赔率"` |
| **热门市场** | `"Polymarket上有哪些热门市场？"` `"交易量最大的市场有哪些？"` |
| **加密货币价格** | `"查询BTC 15分钟内的涨跌情况"` `"查询ETH当前的每小时涨跌情况"` |
| **股票和指数** | `"查询AAPL的每日涨跌情况"` `"查询S&P 500的每日走势"` |
| **到期市场** | `"查询2小时后到期的市场"` `"查询今晚结束的NBA比赛"` |
| **下注** | `"下注10美元赌湖人队获胜"` `"购买50美元的‘Yes’选项"` |
| **限价单** | `"以0.40或更高的价格买入‘Yes’选项"` `"避免滑点"` |
| **查看持仓** | `"显示我的Polymarket持仓"` `"我的盈亏是多少？"` |
| **性能分析** | `"我的胜率是多少？"` `"查看我的交易历史"` |
| **管理订单** | `"显示我的未成交订单"` `"取消所有待定的限价单"` |
| **提取收益** | `"提取我的收益"` `"我可以提取哪些收益？"` |
| **数据分析** | `"将加密货币市场数据导入SQL"` `"运行查询"` |
| **自动化** | `"安排每天上午9点的市场简报"` `"在赔率变动时提醒我"` |

## 快速入门

1. 在[askgina.ai](https://askgina.ai)登录并打开**代理设置**（侧边栏或`https://askgina.ai/agent-setup`）。
2. 为您的令牌命名（例如：“MacBook上的OpenClaw”），然后点击**生成令牌**。
3. 立即复制连接配置——令牌仅显示一次。
4. 将配置粘贴到您的MCP客户端中：

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

5. 重新启动您的MCP客户端，然后输入：“搜索Polymarket上的NBA市场”。

有关详细的客户端设置说明，请参阅[快速入门指南](https://docs.askgina.ai/predictions-mcp/quick-start)。

## 工作原理

- **认证**：在`https://askgina.ai/agent-setup`生成长期有效的JWT令牌。令牌有效期为90天。您最多可以拥有5个有效令牌，并可通过代理设置页面随时撤销任何令牌。
- **钱包**：通过[Privy](https://privy.io)实现自我托管。您拥有自己的密钥。
- **交易**：在Polymarket（Polygon / USDC）上执行交易。
- **手续费**：Gina提供手续费补贴以帮助覆盖交易费用。
- **安全性**：大额交易在执行前需要明确确认。
- **自动化**：通过自然语言设置定时任务（市场简报、提醒等），随时可进行管理。

## 安全须知

- 将令牌视为私钥——切勿公开分享
- 交易使用真实资金（Polygon上的USDC）——确认前请务必仔细核对
- 先从只读操作（搜索、热门市场）开始，再尝试交易
- 大额交易需要明确确认
- 如果怀疑令牌被泄露，请立即撤销令牌（通过代理设置页面）
- 如果认证流程要求输入私钥，请**不要继续操作**

## 链接

- **应用程序**：https://askgina.ai
- **文档**：https://docs.askgina.ai
- **功能**：https://docs.askgina.ai/predictions-mcp/features
- **客户端设置**：https://docs.askgina.ai/predictions-mcp/client-setup
- **故障排除**：https://docs.askgina.ai/predictions-mcp/troubleshooting
- **服务条款**：https://askgina.ai/terms-and-conditions
- **Twitter**：https://x.com/askginadotai