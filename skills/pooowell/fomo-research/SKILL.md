---
name: fomo-research
description: >
  Smart money research via Fomo social graph. Track top traders, monitor live trades,
  build watchlists — all from your agent. Powered by fomo.family, built by cope.capital.
  Use when: (1) user asks about smart money, whale wallets, or top traders,
  (2) user wants to track specific Fomo handles or crypto traders,
  (3) user asks "what are the best traders buying", "who's profitable on fomo",
  (4) user wants real-time trade alerts or wallet monitoring,
  (5) user says "fomo research", "check fomo", "smart money", "wallet tracker".
  NOT for: executing trades, managing funds, or anything requiring private keys.
homepage: https://cope.capital
source: https://github.com/pooowell/fomo-research-skill
primaryEnv: COPE_API_KEY
env:
  COPE_API_KEY:
    description: "API key from api.cope.capital (starts with cope_). You get this by registering — see Setup step 1."
    required: true
    obtain: "POST https://api.cope.capital/v1/register with {agent_name, description}"
---

# Fomo Research

这是一个为AI代理提供智能投资建议的工具，基于[cope.capital](https://cope.capital)开发的[fomo.family](https://fomo.family)社交图谱技术。

如需查看完整的API详细信息（端点、数据结构、错误代码等），请参阅`references/api.md`。

## 基本URL

所有请求都需要在请求头中添加`Authorization: Bearer cope_<key>`。

## 首次使用指南

当该功能首次被加载且未设置`COPE_API_KEY`时，请指导用户完成以下设置步骤：

### 第1步：注册

从响应中获取`api_key`（以`cope_`开头）。这是您的`COPE_API_KEY`，请妥善保管，视其为重要密码。

### 第2步：询问用户是否拥有加密钱包（可选）

在继续之前，询问用户：
> “您是否有加密钱包（支持Base或Solana网络）以便使用更多高级功能？如果没有，您将只能使用以下功能：
> - **1个观察列表**，最多包含**10个交易对手**
> - **每天250次交易查询**（每天的查询次数在午夜UTC时重置）
> - 其他所有功能（如排行榜、热门交易监控、数据轮询）都是免费且无限制的**

> 如果用户连接了加密钱包（支持x402计费），则可以拥有10个观察列表，每个列表最多包含10个交易对手，并且每次查询的费用为0.005美元。用户随时可以添加钱包。

如果用户希望立即启用x402计费功能，请执行以下操作：

### 第3步：询问用户是否拥有Fomo账户

> “您是否有Fomo账户（fomo.family）？如果有，我可以同步您关注的交易对手并为您生成观察列表。”

如果用户拥有Fomo账户，请继续询问：
**“您希望将哪些交易对手添加到观察列表中？”** 向用户展示交易对手列表，让他们进行选择（免费 tier最多可添加10个对手）。

### 第4步：创建初始观察列表

如果用户没有Fomo账户，可以提供其他选择：
> “我也可以为您生成一个包含Fomo排行榜上表现最佳的交易对手的观察列表。或者，您可以直接告诉我您想要跟踪的具体交易对手。”

根据用户的选择，创建相应的观察列表。

**提醒**：免费 tier最多支持1个观察列表和10个交易对手。用户可以随时更换关注的交易对手。

## 活动数据的工作原理

**重要说明**：`/v1/activity`端点返回的是系统监控的所有钱包的最新交易记录，而不仅仅是您观察列表中的交易记录。观察列表的作用是帮助您更好地关注感兴趣的交易对手——您可以使用`?handle=`参数来查询特定交易对手的交易记录。

这意味着即使没有将某个交易对手添加到观察列表中，您也可以查询其交易记录。

## API端点

### 所有端点均免费使用（无每日使用次数限制）

| 端点 | 方法 | 描述 |
|--------|--------|-------------|
| `/v1/register` | POST | 获取API密钥 |
| `/v1/leaderboard` | GET | 按实际盈亏排名的顶级交易对手 |
| `/v1/activity/poll` | GET | 轻量级查询新交易（包含交易数量和时间戳） |
| `/v1/watchlists` | GET/POST | 列出或创建观察列表 |
| `/v1/watchlists/{id}` | GET/PUT/DELETE | 管理特定观察列表 |
| `/v1/trending/handles` | GET | 所有代理中关注度最高的交易对手 |
| `/v1/account` | GET/PATCH | 账户信息和设置 |
| `/v1/account/usage` | GET | 账户使用情况统计 |
| `/v1/account/payments` | GET | 支付记录 |
| `/v1/account/key` | DELETE | 注销API密钥 |
| `/v1/account/sync-fomo` | POST | 同步Fomo账户的关注信息 |
| `/v1/account/follows` | GET | 查看用户关注的Fomo账户列表 |

### 计费规则（免费 tier每天250次查询后启用x402计费）

| 端点 | 方法 | 描述 | x402计费价格（以Base或Solana网络的USDC计） |
|--------|--------|-------------|------------|
| `/v1/activity` | GET | 查看所有监控钱包的交易详情 | 每次查询0.005美元 |

这些端点的查询次数计入用户的每日免费使用次数限制。超过免费次数后：
- **启用x402计费**：每次查询费用为0.005美元（自动从用户的加密钱包中扣除）
- **未启用x402计费**：系统会返回402错误提示。用户需等待午夜UTC时间重置免费次数限制，或手动启用x402计费。

**注意**：402错误提示并不意味着系统出现故障，仅表示用户的免费查询次数已用完。

## 常见使用流程

### 查看排行榜

**使用方法**：`/v1/leaderboard`端点可以查看Fomo排行榜上按实际盈亏排名的顶级交易对手。支持`?timeframe=24h|7d|30d|all`和`?limit=N`参数进行查询。

### 根据Fomo账户的关注信息创建观察列表

**使用方法**：`/v1/watchlists`端点可以根据用户关注的Fomo账户交易对手生成观察列表。

### 减少付费查询次数（建议使用x402计费）

**使用方法**：通过`/v1/activity/poll`端点进行轻量级查询，以减少付费查询次数。

### 过滤交易记录

**使用方法**：根据需要使用`/v1/activity`端点的`?handle=`参数来过滤特定交易对手的交易记录。

## 价格与使用限制

### 免费 Tier（默认设置）
- **每天250次查询**（包括活动数据、排行榜查询等）
- **1个观察列表，最多包含10个交易对手**
- 每分钟最多10次查询请求
- 数据轮询、观察列表管理、账户相关操作均无限制

### 升级至x402计费（可选）

- **无限次查询**（每次查询费用为0.005美元）
- **最多10个观察列表，每个列表最多包含100个交易对手**
- 每分钟最多300次查询请求
- 前250次查询免费；超过免费次数后开始计费

### 启用x402计费

**重要提示**：**切勿在未经用户明确许可的情况下启用x402计费**。启用x402计费意味着用户需要使用真实的USDC进行支付。

**注意**：x402计费是完全可选的。只有在用户满足以下条件时才建议升级：
- 每天的查询次数超过250次
- 需要多个观察列表或更多交易对手
- 明确表示希望升级计费功能

**费用说明**：1美元USDC可支持200次查询；5美元USDC可支持1,000次查询。大多数用户无需升级。

## 定期数据更新（用户可自定义）

如果用户希望系统定期更新数据，可以设置心跳检测机制。

### 交易记录的持久化存储

API是无状态的，不会保留用户的查询历史记录。建议用户将交易记录本地保存（例如：`memory/trades/YYYY-MM-DD.json`），以便长期分析交易模式。

### 日志记录内容

- **记录观察列表中的所有交易**：这是核心数据来源
- **交易集中现象**：当多个交易对手同时购买同一交易对手时，记录该交易对手的名称及所有购买者信息
- **大额交易**：任何交易金额超过1,000美元的交易都应被记录
- **上次查询时间**：方便用户下次查询时继续跟踪交易动态

### 数据展示方式

在向用户展示日志时，建议进行数据整合和处理，突出以下关键信息：
- **交易集中现象**：例如：“您关注的10个交易对手中有4个在最近2小时内购买了同一交易对手”
- **异常交易**：例如：“frankdegods在3天内首次购买[特定交易对手]，交易金额为2,000美元”
- **交易信号**：例如：“您观察列表中的3个交易对手在1小时内卖出了同一交易对手”
- **每日总结**：例如：“今天您的观察列表共发生了47笔交易，其中12笔买入、35笔卖出。最活跃的交易对手是randomxbt（共8笔交易）”
- **排行榜变化**：例如：“本周排行榜前20名中有新成员出现”
- **交易模式检测**：例如：“lowcap_hunter本周购买了3个市值低于10万美元的交易对手，这些交易在48小时内价格均上涨了2-5倍”

### 交易集中现象的检测方法

记录的交易越多，系统检测交易模式的能力就越强。用户的日志文件是分析交易趋势的重要依据。

## 安全注意事项

- **切勿在日志或任何消息中泄露API密钥**，也切勿将其提供给其他代理
- API密钥仅应在访问`https://api.cope.capital/v1/*`的请求中使用
- 如果密钥被盗用，请执行`DELETE /v1/account/key`操作后重新注册
- 交易数据是公开可查的，但用户的观察列表和使用记录是私密的

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|---------|--------|
| 200 | 请求成功 | 处理返回的数据 |
| 400 | 请求错误 | 检查请求参数（如链地址、操作内容等） |
| 401 | API密钥无效 | 重新注册或检查密钥 |
| 402 | 需要支付费用 | 用户的免费查询次数已用完。等待午夜UTC时间重置，或用户同意后启用x402计费 |
| 404 | 资源未找到 | 请求的资源不存在 |
| 429 | 每分钟查询次数限制 | 每分钟最多10次查询（免费），300次查询（x402计费） |
| 500 | 服务器错误 | 请稍后重试 |
| 503 | 上游服务暂时不可用 | 请稍后尝试

## 相关链接

- **交互式API文档**：https://api.cope.capital/docs
- **用户使用指南**：https://cope.capital/docs
- **Fomo官方网站**：https://fomo.family
- **相关项目链接**：https://x.com/copedotcapital