---
name: agentcanary
description: 这是一个用于AI代理的跨资产市场情报API，提供了超过130个终端点（endpoints），涵盖以下功能：宏观经济环境检测、风险评分、交易信号（包括买入/积累/分散/抛售信号）、大户交易行为警报、资金套利机会分析、订单簿数据分析、去中心化金融（DeFi）产品的收益与市盈率（PE ratio）计算、比特币期权相关数据（如最大亏损点、价格偏度等）、中央银行资产负债表信息、行业轮动趋势分析、市场情绪监测、CAPE比率计算、不同市场情景的概率分析、比特币ETF的资金流动情况、地缘政治风险评估、均值回归信号分析以及机构投资者的持仓情况（包括长期预测、空头头寸数据、CFTC的持仓报告等）。该API支持基于钱包的认证机制，用户可以使用USDC或USDT在主流的EVM区块链（如Base、Ethereum、Arbitrum、Optimism、Polygon）上进行交易。适用于需要宏观经济背景信息、风险评估、交易策略制定、市场结构分析、大户交易行为监控、去中心化金融产品情报、期权交易数据或机构投资者持仓情况的AI代理。该API仅提供数据查询服务，不支持本地执行操作，也不允许访问文件系统或存储任何敏感信息（如交易密钥）。
---
# AgentCanary

为AI代理提供跨资产市场情报服务，支持超过130个数据终端。提供的是经过处理的智能分析结果，而非原始数据。

**基础URL：** `https://api.agentcanary.ai/api`
**认证方式：** 基于钱包的API密钥。创建密钥后，需在任意支持的EVM链上充值USDC/USDT，然后使用该密钥作为查询参数。
**情报更新频率：** 每日自动生成4次情报报告：Radar（04:15）、Signal（10:15）、Pulse（16:15）、Wrap（22:15 UTC）。
**Telegram频道：** [@AgentCanary](https://t.me/AgentCanary) — 实时情报更新。
**应用程序：** [app.agentcanary.ai](https://app.agentcanary.ai) — 用于查看仪表盘、管理账单和API密钥。
**文档：** [api.agentcanary.ai/api/docs](https://api.agentcanary.ai/api/docs) — 提供交互式的Swagger用户界面。
**官方网站：** [agentcanary.ai](https://agentcanary.ai)

---

## 安全性

- **仅通过API访问** — 使用HTTP GET/POST请求，返回JSON格式的数据。无需安装任何本地代码或使用shell命令。
- **所有敏感信息均存储在钱包中** — 认证过程不涉及API密钥的传输，确保数据安全。
- **仅支持读取数据** — 无法写入或修改任何文件系统内容。
- **严格限制访问权限** — 无文件读取、写入或目录列表功能。
- **采用高级安全措施：** 使用Helmet.js框架保护应用程序免受XSS攻击，限制内容类型检测，并确保传输安全。
- **实施速率限制**：服务器端对每个IP地址的API请求进行限制（每15分钟最多5次尝试）。
- **请求体大小限制**：请求体最大为1MB，超出限制的请求将被拒绝。
- **错误处理**：全局异常处理机制确保系统稳定运行，响应中不显示错误堆栈信息。
- **支持多链充值**：支持Base、Ethereum、Arbitrum、Optimism、Polygon等链路的USDC/USDT充值，所有链路的充值地址相同。
- **病毒检测结果：** [0/62次检测](https://www.virustotal.com/gui/file/1bc6c1e0d5f339451281a3667d17ce8e761ab53ca98f490edfe25f15702b5d68/detection)。

---

## 入门指南

```
1. POST /api/keys/create  { walletAddress: "0x..." }  → returns apiKey
2. Send USDC/USDT to the receiving address shown at agentcanary.ai (Base, Ethereum, Arbitrum, Optimism, Polygon)
3. POST /api/billing/check  { apiKey: "..." }  → auto-detects payment, credits account
4. Use endpoints:  GET /api/data/realtime-prices?apikey=YOUR_KEY
```

最低充值金额为5美元。积分永不过期，无需订阅服务，也无需进行任何身份验证（KYC）。

---

## 价格方案

| 订阅层级 | 累计充值金额 | 单次调用费用 | 请求速率限制 | 访问权限 |
|------|-------------------|----------|------------|--------|
| Explorer | 免费 | 0.02美元 | 每15分钟10次请求，每天50次 | 提供价格信息、新闻、市场趋势分析等 |
| Builder | 50美元以上 | 0.02美元 | 每15分钟60次请求，每天5000次 | 增加宏观经济数据、市场信号、日历功能等 |
| Signal | 150美元以上 | 0.015美元 | 每15分钟120次请求，每天20000次 | 支持访问所有130多个数据终端，包含AI报告、订单簿、DeFi相关数据等 |
| Institutional | 500美元以上 | 0.01美元 | 每15分钟300次请求，无次数限制 | 提供白标服务、SLA保障及定制集成功能 |

---

## 默认的代理使用模式

AgentCanary作为风险情报中间件，会向您的代理发送提示，告知当前市场环境是否有利于执行特定操作——代理随后可自行决定如何行动。

---

## 数据终端分类及示例

完整的数据终端文档及响应示例请参阅：[references/endpoints.md]

### 专有数据终端（`/api/...`）

| 分类 | 关键数据终端 | 订阅层级 |
|----------|--------------|------|
| **指标分析** | `/indicators`, `/indicators/summary`, `/indicators/:name` | Explorer–Builder层级 |
| **市场情景分析** | `/scenarios/current`, `/scenarios/history`, `/scenarios/signals` | Signal层级 |
| **情报报告** | `/briefs/latest`, `/briefs/feed`, `/briefs/archive`, `/briefs/:type` | Explorer–Signal层级 |
| **宏观经济数据** | `/macro/regime`, `/macro/snapshot`, `/macro/signals`, `/macro/global-liquidity`, `/macro/us-m2`, `/macro/central-banks`, `/macro/supply-chain` | Explorer–Builder层级 |
| **市场趋势分析** | `/regime`, `/regime/matrix`, `/regime/history` | Signal层级 |
| **市场信号** | `/signals/correlations`, `/signals/sector-rotation`, `/signals/btc-etf-flows`, `/signals/fear-greed`, `/signals/whale-alerts`, `/signals/decision-engine` | Signal层级 |
| **市场叙事分析** | `/narratives`, `/narratives/history`, `/narratives/:name` | Signal层级 |
| **DeFi市场数据** | `/defi/intelligence`, `/defi/pe-ratios`, `/defi/yields`, `/defi/perps`, `/defi/stablecoins`, `/defi/chains`, `/defi/unlocks`, `/defi/signals` | Signal层级 |
| **比特币期权数据** | `/btc-options`, `/btc-options/maxpain`, `/btc-options/skew` | Signal层级 |
| **央行数据** | `/central-banks`, `/central-banks/balance-sheets`, `/central-banks/btc`, `/central-banks/stablecoins`, `/central-banks/gold`, `/central-banks/reserves`, `/central-banks/tic` | Signal层级 |
| **高级分析服务** | `/premiums`, `/premiums/coinbase`, `/premiums/kimchi` | Signal层级 |
| **预测分析** | `/predictions`, `/predictions/movers`, `/predictions/:slug` | Signal层级 |
| **市场情绪分析** | `/sentiment/reddit` | Signal层级 |
| **均值回归分析** | `/mr/signals`, `/mr/trades`, `/mr/stats` | Signal层级 |
| **其他高级功能** | `/hindenburg`, `/hindenburg/history`, `/cape` | Signal层级 |
| **退出策略** | `/kill-conditions` | Signal层级 |
| **加密货币重新入场策略** | `/crypto-reentry`, `/crypto-reentry/history` | Signal层级 |
| **机构级服务** | `/institutional/13f` | Signal层级 |
| **新闻资讯** | `/news/trending`, `/news/stats`, `/news/market-analysis`, `/news/xtg-analysis` | Signal层级 |

### 数据集（`/api/data/...`）

这些数据集会定期更新，涵盖价格、宏观经济、加密货币、新闻、机构市场等多个领域：

| 数据集 | 订阅层级 | 描述 |
|---------|------|-------------|
| `realtime-prices` | Explorer层级 | 提供100多种加密货币的24小时价格变化数据 |
| `yahoo-quotes` | Builder层级 | 包括SPY、QQQ、VIX、TLT、DXY等指数及16个行业ETF的价格数据 |
| `whale-alerts` | Explorer层级 | 监测大额加密货币交易 |
| `breaking-news` | Explorer层级 | 提供带有FinBERT情感分析的财经新闻 |
| `fear-greed` | Explorer层级 | 显示加密货币市场的恐惧与贪婪指数 |
| `macro-snapshot` | Builder层级 | 提供30多个FRED系列经济指标及风险评估数据 |
| `funding-rates` | Builder层级 | 全球交易所的永久性融资利率数据 |
| `financial-calendar` | Builder层级 | 重要经济事件的日历信息 |
| `newsletters` | Builder层级 | 精选市场情报新闻 |
| `narrative-scores` | Signal层级 | 分析21种市场叙事主题 |
| `btc-etf-flows` | Signal层级 | 每日比特币ETF的流动数据 |
| `reddit-sentiment` | Signal层级 | 分析14个Reddit子版块的市场情绪 |
| `decision-engine` | Signal层级 | 多因素加密货币重新入场策略评估 |
| `scenario-probs` | Signal层级 | 6种宏观经济情景的概率分析 |

更多数据集请参阅：[references/endpoints.md]

---

## 信号更新频率指南

| 信号类型 | 更新频率 | 推荐使用频率 |
|--------|-----------------|-------------------|
| 宏观经济分析 | 每6小时一次 | 每4–6小时 |
| 市场状态信号 | 每日收盘时 | 每4–6小时 |
| 大额交易预警 | 实时更新 | 每15–30分钟 |
| 融资利率 | 每8小时一次 | 每4–8小时 |
| 重要新闻 | 实时更新 | 每15–30分钟 |
| 智报报告 | 每日4次 | 每次报告发布后 |
| DeFi市场数据 | 每4小时一次 | 每4–6小时 |

---

## 服务限制

- **不提供价格预测** — 仅对市场状况进行分类和分析。
- **不执行交易指令或替代执行逻辑**。
- **不提供财务建议**。
- **不保证投资回报**。

*AgentCanary仅提供市场数据和情报，不构成任何财务建议。*

---

*AgentCanary旨在帮助您更好地理解市场状况，但请自行承担所有投资决策的风险。*