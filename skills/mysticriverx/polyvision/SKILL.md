---
name: polyvision
description: >
  分析 Polymarket 预测市场钱包的详细信息：  
  - 获取复制交易评分（1-10 分）  
  - 收益与损失（P&L）数据  
  - 胜率  
  - 风险指标（夏普比率、索蒂诺比率、最大回撤率）  
  - 风险警示信号  
  - 交易头寸规模  
  - 市场类别表现  
  - 最近7天/30天/90天的表现数据  
  - 交易 streak 分析  
  - 每个未平仓头寸的入场价格和当前价格  
  - 最近的交易历史记录  
  此外，还可以通过每日排行榜发现精英交易者，查看顶级交易者的热门投注策略，以及随机发现新的交易钱包。  
  支持通过 MCP 服务器或 REST API 进行数据查询。  
  适用于以下场景：  
  - 评估是否应该复制某个 Polymarket 交易者的交易策略  
  - 并行比较多个钱包的表现  
  - 筛选表现优异的交易者  
  - 检查交易者是否存在类似机器人的交易行为或隐藏的亏损  
  - 研究交易者的风险状况  
  - 查看最近的交易活动  
  - 寻找当天的最佳投注机会  
  - 发现值得关注的新交易者  
  提供免费 API 密钥，无每日使用限制，结果缓存时长为6小时。
homepage: https://polyvisionx.com
license: MIT
disable-model-invocation: true
metadata: {"clawdis":{"emoji":"📊","primaryEnv":"POLYVISION_API_KEY","requires":{"env":["POLYVISION_API_KEY"]}}}
---
# PolyVision — Polymarket钱包分析工具

PolyVision能够分析Polymarket预测市场中的钱包，并提供全面的交易报告：包括跟单交易评分（1-10分）、盈亏明细、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、持仓规模一致性、市场类别表现、近期表现（7天/30天/90天）、连续交易记录、风险警示以及各个持仓的入场价和当前价。此外，它还提供每日排名前10的交易者排行榜、热门投注（来自顶尖交易者的最盈利持仓），以及随机推荐的精英交易者信息。你可以使用该工具来评估某个交易者是否适合跟单交易、比较多个钱包的表现、筛选出表现优异的交易者、寻找当天的最佳投注机会，或者发现新的交易者进行关注。

## 使用场景
- 当用户提供Polymarket钱包地址（格式为`0x...`）时
- 当用户询问关于跟单交易、交易者评估或钱包评分的信息时
- 当用户希望比较不同交易者的表现或筛选精英交易者时
- 当用户想要了解交易者的风险状况、风险警示或交易模式时
- 当用户想知道顶尖交易者的投注策略或当天的最佳持仓时
- 当用户希望发现或寻找新的Polymarket交易者进行关注时
- 当用户请求查看每日排行榜或交易者排名时
- 当用户希望查看交易者的具体持仓及其盈亏详情时
- 当用户想要了解交易者的近期交易记录或最新活动时
- 当用户请求跟单交易策略建议或最佳设置时
- 当用户想知道适合跟单交易的风险等级或参数时

## 不适用场景
- 一般性的加密货币价格查询（非Polymarket相关）
- 下单或执行交易（PolyVision仅提供分析功能）
- 非Polymarket钱包的查询（如Ethereum DeFi、NFT等）

## 设置：MCP服务器（推荐）

请将以下配置添加到你的MCP客户端配置文件中（例如`claude_desktop_config.json`、Cursor、Windsurf）：

```json
{
  "mcpServers": {
    "polyvision": {
      "type": "streamable-http",
      "url": "https://api.polyvisionx.com/mcp",
      "headers": {
        "Authorization": "Bearer ${POLYVISION_API_KEY}"
      }
    }
  }
}
```

## 获取API密钥

你可以从Telegram机器人那里免费获取API密钥（无每日使用限制）：
1. 打开[PolyVision机器人](https://t.me/PolyVisionBot)的Telegram频道
2. 输入`/apikey`命令生成你的密钥
3. 复制显示的`pv_live_...`密钥，并妥善保管

将密钥设置为环境变量：

```bash
export POLYVISION_API_KEY="pv_live_abc123..."
```

完整API文档：https://polyvisionx.com/docs

## MCP工具参考

### `analyze_wallet`

执行全面的Polymarket钱包分析。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `wallet_address` | 字符串 | 是 | — | Ethereum钱包地址（42个字符，以`0x`开头） |
| `mode` | 字符串 | 否 | `"quick"` | `"quick"`（约5秒）或 `"full"`（约30-60秒，包含交易时间数据） |

**返回值：** 包含盈亏、胜率、风险指标、交易类别、跟单交易评分（1-10分）、风险警示和使用信息的完整分析结果。结果会缓存6小时——缓存命中时响应速度极快。详细字段参考请参见`references/response-schemas.md`。

**耗时：** 快速模式约5秒，完整模式约30-60秒。缓存后的响应也是即时可用的。

### `get_score`

获取钱包的简短跟单交易评分。使用与`analyze_wallet`相同的缓存。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|------|---------|-------------|
| `wallet_address` | 字符串 | 是 | Ethereum钱包地址（42个字符，以`0x`开头） |

**返回值：** 评分（1-10分）、建议等级（绿色/黄色/橙色/红色）、总盈亏、胜率、夏普比率、风险警示以及使用信息。

**耗时：** 约5秒（如果数据已缓存，则即时响应）。

### `get_hot_bets`

获取当天的热门投注信息，包括来自顶尖交易者的最盈利持仓。数据来源于每日策略报告。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `limit` | 整数 | 否 | `20` | 返回的投注数量上限 |
| `sort_by` | 字符串 | 否 | `"rank"` | 默认排序方式；`"pnl"`按盈亏排序 |

**返回值：** 包含扫描日期、投注总数和热门投注列表——每个投注包含交易者信息（钱包地址、用户名、评分、胜率）、市场详情（标题、slug、结果）、价格（入场价、当前价、当前价值）、盈亏（未实现盈亏百分比）、解决时间（结束日期、解决前天数）、入场时间（入场日期、持有时间）以及Polymarket链接。详细字段参考请参见`references/response-schemas.md`。

### `get_leaderboard`

获取每日排名前10的Polymarket交易者排行榜。数据每日更新。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `sort_by` | 字符串 | 否 | `"rank"` | 默认排序方式；`"pnl"`按盈亏排序 |

**返回值：** 包含扫描日期、投注总数和排行榜条目列表——每个条目包含钱包地址、用户名、总盈亏、投资回报率（ROI%）、胜率、风险指标（夏普比率、最大回撤率、盈利因子）、评分等级（绿色/黄色/橙色/红色）、风险警示、交易记录天数以及市场类别（政治、加密货币、体育）。详细字段参考请参见`references/response-schemas.md`。

### `get_strategy`

获取预先计算好的跟单交易策略配置文件。返回3种风险等级（保守型、中等型、激进型）的配置参数和预期指标，每日更新。

**参数：** 无

**返回值：** 包含扫描日期、策略配置文件总数以及配置文件列表——每个文件包含参数（价格范围、最低评分、每日最大交易次数、最小交易规模、持仓规模方法）、回测结果（胜率、ROI、夏普比率、最大回撤率、盈利因子、总盈亏）、成本调整后的结果以及通俗易懂的描述。详细字段参考请参见`references/response-schemas.md`。

### `get_recent_trades`

获取Polymarket钱包的近期交易记录。返回包含交易方向（买入/卖出）、交易规模、价格、市场标题和时间戳的交易历史。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `wallet_address` | 字符串 | 是 | — | Ethereum钱包地址（42个字符，以`0x`开头） |
| `since` | 整数 | 否 | — | 时间戳——仅返回该时间之后的交易 |
| `limit` | 整数 | 否 | `50` | 返回的交易数量上限（1-100笔） |

**返回值：** 包含`wallet_address`、`since`和`trades`列表——每笔交易包含交易方向、交易规模、价格、时间戳、市场标题、结果、slug和交易哈希。详细字段参考请参见`references/response-schemas.md`。

### `discover_wallet`

从精选的交易者池（250个以上）中随机选择一个精英交易者。每次调用会返回一个随机钱包地址——可以使用`analyze_wallet`或`get_score`进一步分析。

**参数：** 无

**返回值：`{"wallet_address": "0x...", "pool_size": 250, "message": "..."}`

### `check_quota`

检查你的使用统计信息。此操作不会消耗配额。

**参数：** 无

**返回值：`{"used_today": <int>, "tier": "api" }`

API/MCP的使用没有每日使用限制——数据仅用于分析目的。

### `health`

检查系统运行状态。

**参数：** 无

**返回值：`{"status": "ok" }` 或 `{"status": "degraded" }`

## 评分等级

| 评分等级 | 评分范围 | 建议 | 含义 |
|---------|------------|----------------|---------|
| 绿色 | 8.0 – 10.0 | 非常优秀的交易者 | 持续盈利，风险管理良好，表现稳定 |
| 黄色 | 6.0 – 7.9 | 中等水平的交易者 | 表现尚可，但存在一些问题，需谨慎跟单 |
| 橙色 | 4.0 – 5.9 | 风险较高的交易者 | 成绩波动较大，存在显著风险 |
| 红色 | 0.0 – 3.9 | 不建议跟单 | 表现不佳，存在重大风险 |

## 决策参考表

| 用户意图 | 工具 | 使用模式 | 原因 |
|---------|------|------|---------|
| “我应该跟这个交易者吗？” | `get_score` | — | 提供评分和风险警示，快速判断是否适合跟单 |
| “深入分析这个钱包” | `analyze_wallet` | `full` | 包含交易时间数据的全面分析 |
| “快速检查一个钱包” | `analyze_wallet` | `quick` | 不包含交易时间数据的快速分析 |
| “这个交易者的持仓有哪些？” | `analyze_wallet` | `quick` | 分析结果中包含`open_positions_detail`字段 |
| “比较两个交易者” | `get_score` | — | 并排显示评分以便快速对比 |
| “这个交易者主要关注哪些市场类别？” | `analyze_wallet` | `quick` | 分析结果中包含市场类别明细 |
| “当前哪些投注最赚钱？” | `get_hot_bets` | — | 来自顶尖交易者的最盈利持仓 |
| “顶尖交易者在做什么样的投注？” | `get_hot_bets` | `sort=`pnl | 按盈亏排序的热门投注 |
| “今天的顶尖交易者是谁？” | `get_leaderboard` | — | 每日排名前10的交易者 |
| “帮我找一个值得跟随的交易者” | `discover_wallet` | — | 随机推荐的精英交易者，然后使用`get_score`或`analyze_wallet`进一步分析 |
| “这个钱包最近做了哪些交易？” | `get_recent_trades` | — | 该钱包的近期交易记录 |
| “我应该使用哪种跟单策略？” | `get_strategy` | — | 提供3种风险等级的策略配置 |
| “最安全的跟单方式是什么？” | `get_strategy` | — | 保守型策略（回撤率较低） |
| “发现新的交易者” | `discover_wallet` | — | 随机推荐的精英交易者 |
| “系统是否正常运行？” | `health` | — | 系统状态检查 |
| “我进行了多少次分析？” | `check_quota` | — | 使用统计信息（无使用限制） |

## 风险警示说明

风险警示以字符串列表的形式返回。各警示的含义如下：

| 风险警示 | 触发条件 | 严重程度 |
|---------|----------------|---------|
| 胜率过低 | 胜率低于40% | 高风险 |
| 单笔交易损失过大 | 单笔最大损失超过总盈亏的50% | 中等风险 |
| 总体亏损 | 净盈亏为负 | 高风险 |
| 交易记录较少 | 关闭的持仓少于10笔 | 中等风险 |
| 长时间不活跃 | 30天内无交易 | 低风险 |
| 交易频率过高 | 平均交易时间少于5分钟 | 高风险 |
| 交易频率过低 | 平均交易时间少于30分钟 | 中等风险 |
| 大量持仓亏损 | 70%以上的持仓处于亏损状态 | 高风险 |
| 大多数持仓处于亏损状态 | 3笔以上持仓处于亏损状态 | 中等风险 |
| 未发现重大风险警示 | 未发现异常交易模式 | 低风险 |

## REST API（备用选项）

对于无法使用MCP的客户端，所有工具都可通过REST接口访问：`https://api.polyvisionx.com`。大部分接口需要使用Bearer令牌进行身份验证（部分接口除外）。

交互式文档和OpenAPI规范可在此处查看：
- **Swagger UI：** `https://api.polyvisionx.com/docs`
- **OpenAPI JSON：** `https://api.polyvisionx.com/openapi.json`

| 接口 | 方法 | 说明 |
|---------|--------|-------------|
| `GET /v1/auth/me` | 获取当前用户信息和使用统计 |  
| `GET /v1/analyze/{wallet_address}?mode=quick` | 获取钱包的全面分析结果（包含`open_positions_detail`） |
| `GET /v1/score/{wallet_address}` | 获取简洁的跟单交易评分 |  
| `GET /v1/hot-bets?page=0&limit=20&sort_by=rank` | 获取当天的热门投注信息 |  
| `GET /v1/leaderboard?sort_by=rank` | 获取每日排名前10的交易者 |  
| `GET /v1/strategy` | 获取预先计算好的跟单交易策略配置 |  
| `GET /v1/trades/{wallet_address}?since=&limit=50` | 获取钱包的近期交易记录 |  
| `GET /v1/discover` | 随机推荐一个精英交易者 |  
| `GET /health` | 检查系统运行状态 |  

### 示例：分析钱包

```bash
curl -s https://api.polyvisionx.com/v1/analyze/0x1234...abcd?mode=quick \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### 示例：获取评分

```bash
curl -s https://api.polyvisionx.com/v1/score/0x1234...abcd \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### 示例：获取热门投注信息

```bash
curl -s https://api.polyvisionx.com/v1/hot-bets?sort_by=pnl \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### 示例：获取排行榜

```bash
curl -s https://api.polyvisionx.com/v1/leaderboard \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### 示例：获取策略配置文件

```bash
curl -s https://api.polyvisionx.com/v1/strategy \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### 示例：随机选择一个交易者

```bash
curl -s https://api.polyvisionx.com/v1/discover \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

## 错误代码

| 代码 | 含义 | 处理方式 |
|---------|---------|----------|
| 400 | 钱包地址无效（必须是42个字符的十六进制地址） | 请检查地址格式 |
| 401 | API密钥无效或无效 | 从[PolyVision Telegram机器人](https://t.me/PolyVisionBot)获取密钥（使用`/apikey`命令） |
| 429 | 日使用量达到上限 | 等待片刻后重试——Polymarket API可能有限制 |
| 503 | 系统已满载（所有分析资源已分配） | 30-60秒后重试 |
| 502 | Polymarket API出现错误 | 请稍后重试——上游API可能暂时不可用 |
| 504 | 分析超时 | 请稍后重试——钱包的交易记录可能过于复杂 |