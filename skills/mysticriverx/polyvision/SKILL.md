---
name: polyvision
description: 分析 Polymarket 预测市场中的钱包：获取跟单交易评分（1-10 分）、盈亏情况、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、风险警示信号、头寸规模、市场类别表现、近期表现（7 天/30 天/90 天）、连续交易记录、各个未平仓头寸的入场价格和当前价格以及近期交易历史。此外，还可以通过每日排行榜发现优秀交易者、查看顶级交易者的热门投注策略，以及随机发现新的交易钱包。该工具可通过 MCP 服务器或 REST API 进行连接。适用于评估是否要跟单某个 Polymarket 交易者、对比多个钱包的表现、筛选出表现优异的交易者、检查钱包是否存在类似机器人的交易行为或隐藏的亏损风险、研究交易者的风险状况、查看近期的交易活动，或是寻找值得关注的新交易者。提供免费的 API 密钥，无每日使用限制，结果缓存时长为 6 小时。
homepage: https://polyvisionx.com
license: MIT
disable-model-invocation: true
metadata: {"clawdis":{"emoji":"📊","primaryEnv":"POLYVISION_API_KEY","requires":{"env":["POLYVISION_API_KEY"]}}}
---
# PolyVision — Polymarket钱包分析工具

PolyVision能够分析Polymarket预测市场中的钱包，并提供全面的交易报告：包括跟单交易评分（1-10分）、盈亏明细、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、持仓规模一致性、市场类别表现、近期表现（7天/30天/90天）、连续盈利/亏损情况、风险警示以及各个未平仓头寸的入场价和当前价。此外，它还提供每日顶尖交易者的排行榜、热门投注（来自顶尖交易者的最盈利未平仓头寸）以及随机精选的优秀交易者信息。你可以使用它来评估某个交易者是否适合跟单交易、比较多个钱包的表现、筛选出表现优秀的交易者、寻找当天的最佳投注策略，或者发现新的交易者进行关注。

## 使用场景
- 当用户提供Polymarket钱包地址（格式为0x...）时
- 当用户询问关于跟单交易、交易者评估或钱包评分的信息时
- 当用户想要比较不同交易者的表现或筛选出优秀交易者时
- 当用户想了解交易者的风险状况、风险警示或交易模式时
- 当用户想知道顶尖交易者的投注策略或当天的最佳未平仓头寸时
- 当用户希望发现或寻找新的Polymarket交易者进行关注时
- 当用户请求查看每日排行榜或顶尖交易者的排名时
- 当用户想查看交易者的未平仓头寸及其盈亏详情时
- 当用户想了解交易者的近期交易记录或最新活动时
- 当用户需要跟单交易策略建议或最佳设置时
- 当用户想了解适合跟单交易的风险评估标准或参数时

## 不适用场景
- 一般性的加密货币价格查询（非Polymarket特定内容）
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

注册一个免费的API密钥（无每日使用限制）：

```bash
curl -X POST https://api.polyvisionx.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "name": "My App"}'
```

收到密钥后，请将其存储起来——该密钥仅显示一次，之后无法重新获取。请将其设置为环境变量：

```bash
export POLYVISION_API_KEY="pv_live_abc123..."
```

## MCP工具参考

### `analyze_wallet`

执行全面的Polymarket钱包分析。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|--------|---------|-----------|
| `wallet_address` | 字符串 | 是 | — | Ethereum钱包地址（42个字符，以0x开头） |
| `mode` | 字符串 | 否 | `"quick"` | `"quick"`（约5秒）或 `"full"`（约30-60秒，包含交易时间数据） |

**返回值：** 包含盈亏情况、胜率、风险指标、交易类别、跟单交易评分（1-10分）、风险警示和使用信息的完整分析结果。分析结果会缓存6小时——缓存命中时响应速度极快。详细字段参考请参见`references/response-schemas.md`。

**耗时：** 快速模式约5秒，完整模式约30-60秒。缓存后的响应可立即获取。

### `get_score`

获取钱包的简洁跟单交易评分。与`analyze_wallet`共享相同的缓存。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|--------|---------|-----------|
| `wallet_address` | 字符串 | 是 | Ethereum钱包地址（42个字符，以0x开头） |

**返回值：** 评分（1-10分）、推荐等级（绿色/黄色/橙色/红色）、总盈亏、胜率、交易次数、夏普比率、风险警示以及使用信息。

**耗时：** 约5秒（如果已缓存则立即响应）。

### `get_hot_bets`

获取当天的热门投注策略。返回来自顶尖交易者的最盈利未平仓头寸，数据来源于每日策略报告。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|--------|---------|-----------|
| `limit` | 整数 | 否 | `20` | 返回的最大投注数量 |
| `sort_by` | 字符串 | 否 | `"rank"` | 默认值；或 `"pnl"` |

**返回值：** 包含扫描日期、热门投注总数及列表——每个投注策略包含交易者信息（钱包地址、用户名、评分、胜率）、市场详情（标题、标识符、价格、当前价格、当前价值）、盈亏情况（未实现盈亏、百分比）、解决时间信息（结束日期、解决前天数）、入场时间（入场日期、持有时间）以及Polymarket链接。详细字段参考请参见`references/response-schemas.md`。

### `get_leaderboard`

获取Polymarket交易者的每日排行榜前十名。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|--------|---------|-----------|
| `sort_by` | 字符串 | 否 | `"rank"` | 默认值；或 `"pnl"` |

**返回值：** 包含扫描日期、排行榜条目总数及列表——每个条目包含钱包地址、用户名、总盈亏、成交量、投资回报率（ROI%）、胜率、风险指标（夏普比率、最大回撤率、盈利因子）、跟单评分（1-10分）、推荐等级（绿色/黄色/橙色/红色）、风险警示、交易记录天数以及市场类别（政治、加密货币、体育等）。详细字段参考请参见`references/response-schemas.md`。

### `get_strategy`

获取预先计算好的跟单交易策略配置文件。返回3种风险等级（保守型、中等型、激进型）的策略配置，包含回测参数和预期指标，每日更新。

**参数：** 无

**返回值：** 包含扫描日期、策略配置文件总数及列表——每个配置文件包含参数（价格范围、最低评分、每日最大交易次数、最小交易规模、持仓规模方法）、回测结果（胜率、ROI、夏普比率、最大回撤率、盈利因子、每笔交易的预期价值、总盈亏）、成本调整后的结果以及通俗易懂的描述。详细字段参考请参见`references/response-schemas.md`。

### `get_recent_trades`

获取Polymarket钱包的近期交易记录。返回包含交易方向（买入/卖出）、交易规模、价格、市场标题和时间戳的交易历史。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|--------|---------|-----------|
| `wallet_address` | 字符串 | 是 | — | Ethereum钱包地址（42个字符，以0x开头） |
| `since` | 整数 | 否 | — | 时间戳——仅返回该时间之后的交易 |
| `limit` | 整数 | 否 | `50` | 返回的最大交易数量（1-100笔） |

**返回值：** 包含`wallet_address`、`since`、`count`以及`trades`列表——每个交易记录包含交易方向、交易规模、价格、时间戳、市场标题、结果、标识符和交易哈希。详细字段参考请参见`references/response-schemas.md`。

### `discover_wallet`

从精选的交易者池（250多个）中随机选择一个优秀交易者。每次调用都会返回一个随机钱包地址——可以使用`analyze_wallet`或`get_score`进一步分析该钱包。

**参数：** 无

**返回值：** `{ "wallet_address": "0x...", "pool_size": 250, "message": "..." }`

### `check_quota`

检查你的使用统计信息。此操作不会消耗配额。

**参数：** 无

**返回值：** `{ "used_today": <int>, "tier": "api" }`

API/MCP的使用没有每日使用限制——仅用于统计分析。

### `health`

检查系统运行状态。

**参数：** 无

**返回值：** `{ "status": "ok" }` 或 `{ "status": "degraded" }`

## 评分等级

| 评分等级 | 评分范围 | 推荐等级 | 含义 |
|---------|------------|----------------|---------|
| 绿色 | 8.0 – 10.0 | 非常优秀的交易者 | 持续盈利，风险管理良好，表现稳健 |
| 黄色 | 6.0 – 7.9 | 中等水平的交易者 | 表现尚可，但存在一些问题，需谨慎跟单 |
| 橙色 | 4.0 – 5.9 | 风险较高的交易者 | 表现不稳定，存在显著风险 |
| 红色 | 0.0 – 3.9 | 不建议跟单 | 表现极差，存在重大风险 |

## 决策参考表

| 用户需求 | 工具 | 使用模式 | 原因 |
|---------|--------|--------|-------------------|
| “我应该跟这个交易者吗？” | `get_score` | — | 通过评分和风险警示快速判断是否适合跟单 |
| “深入分析这个钱包” | `analyze_wallet` | `full` | 包含交易时间数据的全面分析 |
| “快速查看一个钱包” | `analyze_wallet` | `quick` | 不包含交易时间数据的快速分析 |
| “这个交易者的未平仓头寸是什么？” | `analyze_wallet` | `quick` | 分析结果中包含`open_positions_detail`字段 |
| “比较两个交易者” | `get_score` | — | 两侧对比评分以便快速比较 |
| “这个交易者主要关注哪些市场类别？” | `analyze_wallet` | `quick` | 分析结果中包含市场类别细分 |
| “当前哪些投注策略最盈利？” | `get_hot_bets` | — | 来自顶尖交易者的最盈利未平仓头寸 |
| “顶尖交易者正在做什么投注？” | `get_hot_bets` | `sort=`pnl | 按盈亏排序的热门投注 |
| “今天的顶尖交易者是谁？” | `get_leaderboard` | — | 每日排名前十的交易者 |
| “帮我找一个值得关注的交易者” | `discover_wallet` | — | 随机选择一个优秀交易者，然后使用`get_score`或`analyze_wallet`进一步分析 |
| “这个钱包最近做了哪些交易？” | `get_recent_trades` | — | 该钱包的近期交易记录 |
| “我应该使用哪种跟单策略？” | `get_strategy` | — | 三种风险等级的策略配置文件 |
| “哪种跟单策略最安全？” | `get_strategy` | — | 保守型策略，回撤率较低 |
| “发现新的交易者” | `discover_wallet` | — | 随机选择多个优秀交易者进行探索 |
| “系统是否正常运行？” | `health` | — | 系统状态检查 |
| “我进行了多少次分析？” | `check_quota` | — | 使用统计信息（无使用限制） |

## 风险警示说明

风险警示以字符串列表的形式返回。各警示的含义如下：

| 风险警示 | 触发条件 | 严重程度 |
|---------|----------------|-----------|
| 胜率过低 | 胜率低于40% | 高风险 |
| 单笔交易损失过大 | 单笔最大损失超过总盈亏的50% | 中等风险 |
| 总体亏损 | 净盈亏为负 | 高风险 |
| 交易记录较少 | 关闭的头寸少于10个 | 中等风险 |
| 长时间不活跃 | 30天内无交易 | 低风险 |
| 机器人交易行为 | 平均交易时长低于5分钟 | 高风险 |
| 交易频率过高 | 平均交易时长低于30分钟 | 中等风险 |
| 隐藏亏损 | 70%以上的未平仓头寸处于亏损状态 | 高风险 |
| 大量未平仓头寸处于亏损状态 | 50%以上的未平仓头寸处于亏损状态 | 中等风险 |
| 未发现重大风险警示 | 未发现异常交易模式 | 无风险 |

## REST API（备用选项）

对于无法使用MCP的客户端，所有工具都可以通过REST接口访问：`https://api.polyvisionx.com`。大多数接口需要使用Bearer令牌进行身份验证（部分接口除外）。

交互式文档和OpenAPI规范可访问以下地址：
- **Swagger UI：** `https://api.polyvisionx.com/docs`
- **OpenAPI JSON：** `https://api.polyvisionx.com/openapi.json`

| 接口 | 方法 | 说明 |
|---------|--------|-------------|
| `POST /v1/auth/register` | POST | 注册并获取API密钥（无需身份验证） |
| `GET /v1/auth/me` | GET | 获取当前用户信息和使用统计 |
| `GET /v1/analyze/{wallet_address}?mode=quick` | GET | 完整钱包分析（包含`open_positions_detail`） |
| `GET /v1/score/{wallet_address}` | GET | 简洁的跟单交易评分 |
| `GET /v1/hot-bets?page=0&limit=20&sort_by=rank` | GET | 当天的热门投注策略 |
| `GET /v1/leaderboard?sort_by=rank` | GET | 每日排行榜前十名 |
| `GET /v1/strategy` | GET | 预先计算好的跟单交易策略配置文件（3种风险等级） |
| `GET /v1/trades/{wallet_address}?since=&limit=50` | GET | 某钱包的近期交易记录 |
| `GET /v1/discover` | GET | 随机选择一个优秀交易者 |
| `GET /health` | GET | 系统健康检查（无需身份验证） |

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

### 示例：获取热门投注策略

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
|------|---------|-------------------|
| 400 | 非法钱包地址（必须是42个字符的十六进制地址） | 请检查地址格式 |
| 401 | API密钥无效或无效 | 请检查你的`POLYVISION_API_KEY`或重新注册 |
| 409 | 电子邮件已注册（仅限注册使用） | 使用现有密钥或使用其他电子邮件注册 |
| 429 | 使用频率受限 | 请稍后重试——Polymarket API可能存在使用限制 |
| 503 | 系统已满载（所有分析资源已占用） | 30-60秒后重试 |
| 502 | Polymarket API出现错误 | 请稍后重试——可能是Polymarket API暂时不可用 |
| 504 | 分析超时 | 请稍后重试——该钱包的交易记录可能过于复杂 |