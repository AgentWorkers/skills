---
name: polyvision
description: 分析 Polymarket 预测市场中的钱包：获取跟单交易评分（1-10 分）、盈亏情况、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、风险警示信号、头寸规模、市场类别表现、近期表现（7天/30天/90天）、连续盈利/亏损情况，以及各个未平仓头寸的入场价和当前价格。此外，还可以通过每日排行榜发现顶尖交易者、了解顶级交易者的热门投注策略，或随机发现新的交易账户。该工具支持通过 MCP 服务器或 REST API 进行数据交互。适用于评估是否应跟随某个 Polymarket 交易者的交易策略、对比多个钱包的表现、筛选表现优异的交易账户、检查交易账户是否存在类似机器人的交易行为或隐藏的亏损风险、研究交易者的风险特征、查找当天的最佳投注机会，或发现值得关注的新交易者。提供免费 API 密钥，无每日使用限制，结果数据可缓存 6 小时。
homepage: https://polyvisionx.com
license: MIT
disable-model-invocation: true
metadata: {"clawdis":{"emoji":"📊","primaryEnv":"POLYVISION_API_KEY","requires":{"env":["POLYVISION_API_KEY"]}}}
---
# PolyVision — Polymarket钱包分析工具

PolyVision能够分析Polymarket预测市场的钱包，并提供全面的交易报告：包括复制交易评分（1-10分）、盈亏明细、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、持仓规模的一致性、市场类别表现、近期表现（7天/30天/90天）、连续盈利情况、风险警示以及各个未平仓头寸的入场价和当前价。此外，它还提供每日排名前10的交易者排行榜、热门投注（来自顶尖交易者的最盈利未平仓头寸），以及随机精选的优秀交易者信息。你可以使用它来评估某个交易者是否适合复制交易、比较多个钱包、筛选优秀交易者、寻找当天的最佳投注策略，或者发现新的交易者进行关注。

## 使用场景
- 用户提到某个Polymarket钱包地址（格式为0x...）
- 用户询问关于复制交易、交易者评估或钱包评分的信息
- 用户希望比较不同交易者的表现或筛选优秀交易者
- 用户想了解交易者的风险状况、风险警示或交易模式
- 用户想了解顶尖交易者的投注策略或当天的最佳未平仓头寸
- 用户希望发现或寻找新的Polymarket交易者进行关注
- 用户想查看每日排行榜或顶尖交易者的排名
- 用户想查看交易者的未平仓头寸及其盈亏详情
- 用户需要复制交易策略的建议或最佳设置
- 用户想了解适合复制交易的risk profile或参数设置

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

执行全面的Polymarket钱包分析：
| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `wallet_address` | 字符串 | 是 | — | Ethereum钱包地址（42个字符，以`0x`开头） |
| `mode` | 字符串 | 否 | `"quick"` | `"quick"`（约5秒）或"`full"`（约30-60秒，包含交易时间数据） |

**返回结果**：包含盈亏情况、胜率、风险指标、类别、复制交易评分（1-10分）、风险警示和使用信息的完整分析结果。分析结果会缓存6小时——缓存命中时响应速度很快。详细字段参考请参见`references/response-schemas.md`。

**耗时**：快速模式约5秒，完整模式约30-60秒。缓存后的响应会立即返回。

### `get_score`

获取钱包的简化复制交易评分。与`analyze_wallet`共享相同的缓存。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|------|---------|-------------|
| `wallet_address` | 字符串 | 是 | Ethereum钱包地址（42个字符，以`0x`开头） |

**返回结果**：评分（1-10分）、推荐等级（绿色/黄色/橙色/红色）、总盈亏、胜率、交易次数、夏普比率、风险警示以及使用信息。

**耗时**：约5秒（如果数据已缓存，则立即返回）。

### `get_hot_bets`

获取当天顶尖交易者的热门投注策略。返回来自排名前10的交易者的最盈利未平仓头寸，数据来源于每日策略报告。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `limit` | 整数 | 否 | `20` | 返回的投注策略数量上限 |
| `sort_by` | 字符串 | 否 | `"rank"` | 默认按排名排序；或`"pnl"`按盈亏排序 |

**返回结果**：包含扫描日期、热门投注策略的数量和列表——每个策略包含交易者信息（钱包地址、用户名、评分、胜率）、市场详情（标题、slug、结果）、价格信息（入场价、当前价、当前价值）、盈亏情况（未实现盈亏、百分比）、解决日期、距离解决的天数、入场时间（入场日期、持有时间）以及Polymarket链接。详细字段参考请参见`references/response-schemas.md`。

### `get_leaderboard`

获取每日排名前10的Polymarket交易者排行榜。数据每日同步更新。

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `sort_by` | 字符串 | 否 | `"rank"` | 默认按排名排序；或`"pnl"`按盈亏排序 |

**返回结果**：包含扫描日期、排行榜条目数量和列表——每个条目包含钱包地址、用户名、总盈亏、交易量、ROI百分比、胜率、风险指标（夏普比率、最大回撤率、盈利因子）、复制交易评分（1-10分）、推荐等级（绿色/黄色/橙色/红色）、风险警示、交易记录天数以及市场类别（政治、加密货币、体育等）。详细字段参考请参见`references/response-schemas.md`。

### `get_strategy`

获取预先计算好的复制交易策略配置。返回3种风险等级（保守型、中等型、激进型）的策略配置，包含回测参数和预期指标，每日更新。

**参数**：无

**返回结果**：包含扫描日期、策略配置数量和列表——每个配置包含参数（价格范围、最低评分、每日最大交易次数、最小交易规模、持仓规模方法）、回测结果（胜率、ROI、夏普比率、最大回撤率、盈利因子、每笔交易的EV值、总盈亏）、成本调整后的结果以及通俗易懂的描述。详细字段参考请参见`references/response-schemas.md`。

### `discover_wallet`

从精选的交易者池（250个以上）中随机选择一个优秀交易者。每次调用会返回一个随机钱包地址——可以使用`analyze_wallet`或`get_score`进一步分析该钱包。

**参数**：无

**返回结果**：`{"wallet_address": "0x...", "pool_size": 250, "message": "..."}`

### `check_quota`

查看你的使用统计信息。此操作不会消耗任何配额。

**参数**：无

**返回结果**：`{"used_today": <int>, "tier": "api"}`

API/MCP的使用没有每日使用限制——仅用于统计分析。

### `health`

检查系统运行状态。

**参数**：无

**返回结果**：`{"status": "ok"}` 或 `{"status": "degraded"}`

### `regenerate_key`

重新生成你的API密钥。旧密钥将立即失效。

**参数**：无

**返回结果**：`{"api_key": "pv_live_...", "key_prefix": "pv_live_...", "message": "..."}`

新密钥仅显示一次。请立即更新你的配置。

### `deactivate_key`

永久停用你的API密钥。此操作不可逆——如需替换密钥，请使用`regenerate_key`。

**参数**：无

**返回结果**：`{"success": true, "message": "API密钥已被停用。使用此密钥的所有未来请求都将被拒绝。"}`

## 评分等级

| 评分等级 | 评分范围 | 推荐等级 | 含义 |
|---------|------------|----------------|---------|
| 绿色 | 8.0 – 10.0 | 非常优秀的交易者 | 持续盈利，风险管理良好，表现稳定 |
| 黄色 | 6.0 – 7.9 | 中等水平的交易者 | 表现尚可，但存在一些问题，需谨慎操作 |
| 橙色 | 4.0 – 5.9 | 风险较高的交易者 | 成绩参差不齐，存在显著风险 |
| 红色 | 0.0 – 3.9 | 不建议复制交易 | 表现较差，存在重大风险 |

## 决策参考表

| 用户需求 | 工具 | 模式 | 使用理由 |
|---------|------|------|---------|
| “我应该复制这个交易者的策略吗？” | `get_score` | — | 通过评分和风险警示快速判断是否适合复制 |
| “深入分析这个钱包” | `analyze_wallet` | `full` | 包含交易时间数据的全面分析 |
| “快速查看一个钱包的情况” | `analyze_wallet` | `quick` | 不包含交易时间数据的快速分析 |
| “这个交易者的未平仓头寸是什么？” | `analyze_wallet` | `quick` | 分析结果中包含`open_positions_detail` |
| “比较两个交易者的表现” | `get_score` | — | 两侧对比评分以便快速比较 |
| “这个交易者主要关注哪些市场类别？” | `analyze_wallet` | `quick` | 分析结果中包含市场类别分布 |
| “目前最好的投注策略是什么？” | `get_hot_bets` | — | 当天顶尖交易者的最盈利未平仓头寸 |
| “顶尖交易者在做什么样的投注？” | `get_hot_bets` | `sort=`pnl | 按盈亏排序的热门投注 |
| “今天的顶尖交易者是谁？” | `get_leaderboard` | — | 每日排名前10的交易者 |
| “帮我找一个值得跟随的交易者” | `discover_wallet` | — | 随机选择一个优秀交易者，然后使用`get_score`或`analyze_wallet`进一步分析 |
| “我应该使用哪种复制交易策略？” | `get_strategy` | — | 3种风险等级的策略配置 |
| “最安全的复制交易方式是什么？” | `get_strategy` | — | 保守型策略，回撤率较低 |
| “发现新的交易者” | `discover_wallet` | — | 随机选择多个优秀交易者进行探索 |
| “系统是否正常运行？” | `health` | — | 系统状态检查 |
| “我进行了多少次分析？” | `check_quota` | — | 使用统计信息（无使用限制） |

## 风险警示说明

风险警示以字符串列表的形式返回。各警示的含义如下：

| 风险警示 | 触发条件 | 严重程度 |
|---------|---------|----------|
| 胜率过低 | 胜率低于40% | 高风险 |
| 单笔交易损失过大 | 单笔最大损失超过总盈亏的50% | 中等风险 |
| 总体亏损 | 净盈亏为负 | 高风险 |
| 交易记录较少 | 关闭的头寸少于10个 | 中等风险 |
| 长时间不活跃 | 30天内无交易 | 低风险 |
| 交易频率过高 | 平均交易时长低于5分钟 | 中等风险 |
| 隐藏亏损 | 70%以上的未平仓头寸处于亏损状态 | 高风险 |
| 大多数未平仓头寸处于亏损状态 | 50%以上的未平仓头寸处于亏损状态 | 中等风险 |
| 未发现重大风险警示 | 未发现异常交易模式 | 无风险 |

## REST API（备用选项）

对于无法使用MCP的客户端，所有工具都可以通过REST接口访问：`https://api.polyvisionx.com`。大多数接口需要使用Bearer令牌进行身份验证（部分接口除外）。

交互式文档和OpenAPI规范可在以下地址获取：
- **Swagger UI:** `https://api.polyvisionx.com/docs`
- **OpenAPI JSON:** `https://api.polyvisionx.com/openapi.json`

| 接口 | 方法 | 说明 |
|---------|--------|-------------|
| `POST /v1/auth/register` | POST | 注册并获取API密钥（无需认证） |
| `GET /v1/auth/me` | GET | 获取当前用户信息和使用统计 |
| `POST /v1/auth/regenerate` | POST | 重新生成API密钥 |
| `POST /v1/auth/deactivate` | POST | 停用API密钥 |
| `GET /v1/analyze/{wallet_address}?mode=quick` | GET | 完整钱包分析（包含`open_positions_detail`） |
| `GET /v1/score/{wallet_address}` | GET | 简化版的复制交易评分 |
| `GET /v1/hot-bets?page=0&limit=20&sort_by=rank` | GET | 当天顶尖交易者的热门投注策略 |
| `GET /v1/leaderboard?sort_by=rank` | GET | 每日排名前10的交易者排行榜 |
| `GET /v1/strategy` | GET | 预先计算好的复制交易策略配置（3种风险等级） |
| `GET /v1/discover` | GET | 随机选择一个优秀交易者 |
| `GET /health` | GET | 系统健康检查（无需认证） |

### 示例：分析一个钱包
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

### 示例：获取策略配置
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

| 代码 | 含义 | 处理方法 |
|------|---------|----------|
| 400 | 非法钱包地址（必须是42个字符的十六进制地址，以`0x`开头） | 请检查地址格式 |
| 401 | API密钥无效或无效 | 请检查你的`POLYVISION_API_KEY`或重新注册 |
| 409 | 电子邮件已注册（仅限注册使用） | 使用现有密钥或使用其他电子邮件注册 |
| 429 | 使用频率受限 | 请稍后重试——Polymarket API有使用频率限制 |
| 503 | 系统已满载（所有分析资源已占用） | 30-60秒后重试 |
| 504 | 分析超时 | 请稍后重试——该钱包可能有大量历史数据需要分析 |