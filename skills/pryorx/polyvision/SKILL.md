---
name: polyvision
description: 分析 Polymarket 预测市场钱包的信息：获取跟单交易评分（1-10 分）、盈亏情况、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、风险警示信号、持仓规模、市场类别表现、近期表现（7 天/30 天/90 天），以及交易连贯性分析。支持通过 MCP 服务器或 REST API 进行数据查询。该工具可用于评估是否应跟单某个 Polymarket 交易者、对比多个钱包的表现、筛选表现优异的交易者、检查钱包是否存在类似机器人的交易模式或隐藏的亏损风险，或在跟随其交易策略前了解其风险状况。提供免费的 API 密钥，无每日使用限制，结果缓存时长为 6 小时。
homepage: https://polyvisionx.com
license: MIT
disable-model-invocation: true
metadata: {"clawdis":{"emoji":"📊","primaryEnv":"POLYVISION_API_KEY","requires":{"env":["POLYVISION_API_KEY"]}}}
---

# PolyVision — Polymarket钱包分析工具

PolyVision能够分析Polymarket预测市场中的钱包，并提供全面的交易评估报告：包括跟单交易评分（1-10分）、盈亏明细、胜率、风险指标（夏普比率、索蒂诺比率、最大回撤率）、持仓规模的一致性、市场类别表现、近期表现（7天/30天/90天）、连续交易记录以及潜在的风险警示。您可以使用该工具来评估某个交易者是否适合跟单交易、比较多个钱包的表现，或者筛选出表现优秀的交易者。

## 使用场景
- 用户提供了Polymarket钱包地址（格式为0x...）
- 用户询问关于跟单交易、交易者评估或钱包评分的信息
- 用户希望比较不同交易者的表现或筛选出表现优异的交易者
- 用户想了解交易者的风险状况、潜在风险或交易模式

## 不适用场景
- 一般性的加密货币价格查询（非Polymarket相关）
- 下单或执行交易操作（PolyVision仅提供分析功能）
- 非Polymarket钱包的查询（如Ethereum DeFi、NFT等）

## 设置：建议使用MCP服务器

请将以下配置添加到您的MCP客户端配置文件中（例如`claude_desktop_config.json`、Cursor、Windsurf）：

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

您可以免费注册一个API密钥（无每日使用限制）：

```bash
curl -X POST https://api.polyvisionx.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "name": "My App"}'
```

系统会返回一个API密钥。请注意：该密钥仅显示一次，之后无法再次获取。请将其设置为环境变量：

```bash
export POLYVISION_API_KEY="pv_live_abc123..."
```

## MCP工具参考

### `analyze_wallet`

执行全面的Polymarket钱包分析：
- **参数** | **类型** | **是否必需** | **默认值** | **说明** |
| --- | --- | --- | --- | --- |
| `wallet_address` | `string` | 是 | — | Ethereum钱包地址（42个字符，以`0x`开头） |
| `mode` | `string` | 否 | `"quick"` | `"quick"`（约5秒）或`"full"`（约30-60秒，包含交易时间数据） |

**返回结果**：包含盈亏明细、胜率、风险指标、交易类别、跟单交易评分（1-10分）、风险警示和使用情况的完整分析数据。分析结果会缓存6小时，缓存命中时可立即获取结果。详细字段参考请参见`references/response-schemas.md`。

**耗时**：快速模式约5秒，完整模式约30-60秒。缓存后的结果可立即获取。

### `get_score`

获取钱包的跟单交易评分：
- **参数** | **类型** | **是否必需** | **说明** |
| --- | --- | --- | --- |
| `wallet_address` | `string` | 是 | Ethereum钱包地址（42个字符，以`0x`开头） |

**返回结果**：评分（1-10分）、推荐等级（绿色/黄色/橙色/红色）、总盈亏、胜率、交易次数、夏普比率、风险警示以及使用情况。

**耗时**：约5秒；如果数据已缓存，则可立即获取结果。

### `check_quota`

查看您的使用统计信息。此操作不会消耗任何配额。

**返回结果**：`{"used_today": <int>, "tier": "api" }`

API/MCP的使用没有每日使用限制，所有数据仅用于分析目的。

### `health`

检查系统运行状态。

**返回结果**：`{"status": "ok" }` 或 `{"status": "degraded" }`

### `regenerate_key`

重新生成您的API密钥。旧密钥将立即失效。

**返回结果**：`{"api_key": "pv_live_...", "key_prefix": "pv_live_...", "message": "..." }`

新密钥仅显示一次，请立即更新您的配置文件。

### `deactivate_key`

永久停用您的API密钥。此操作不可逆，如需更换密钥，请使用`regenerate_key`。

**返回结果**：`{"success": true, "message": "API key deactivated. All future requests with this key will be rejected." }`

## 评分等级

| 评分等级 | 评分范围 | 推荐建议 | 含义 |
| --- | --- | --- | --- |
| 绿色 | 8.0 – 10.0 | 表现优异 | 持续盈利，风险管理良好，有良好的交易记录 |
| 黄色 | 6.0 – 7.9 | 表现中等 | 有一定问题，需谨慎操作 |
| 橙色 | 4.0 – 5.9 | 风险较高 | 交易结果不稳定，存在显著风险 |
| 红色 | 0.0 – 3.9 | 不建议跟单 | 表现糟糕，存在重大风险 |

## 决策参考

| 用户需求 | 工具 | 模式 | 原因 |
| --- | --- | --- | --- |
| “我应该跟单这个交易者吗？” | `get_score` | — | 提供简单的评分和风险警示 |
| “深入分析这个钱包” | `analyze_wallet` | `full` | 包含交易时间数据的全面分析 |
| “快速查看钱包情况” | `analyze_wallet` | `quick` | 不包含交易时间数据的快速分析 |
| “比较两个交易者” | `get_score`（多次调用） | 便于快速对比两个交易者的评分 |
| “这个交易者主要关注哪些市场类别？” | `analyze_wallet` | `quick` | 分析中包含市场类别信息 |
| “系统是否正常运行？” | `health` | — | 检查系统状态 |
| “我进行了多少次分析？” | `check_quota` | | 查看使用统计信息（无使用限制） |

## 风险警示说明

风险警示以字符串列表的形式返回。各警示的含义如下：
- **低胜率**：胜率低于40% | 风险较高 |
- **单笔大额亏损**：单笔最大亏损超过总盈亏的50% | 中等风险 |
- **整体亏损**：净盈亏为负 | 高风险 |
- **交易记录不足**：已平仓的交易数量少于10笔 | 中等风险 |
- **长期不活跃**：30天内无交易 | 低风险 |
- **交易频率过高**：单笔交易平均持续时间少于5分钟 | 高风险 |
- **交易速度过快**：单笔交易平均持续时间少于30分钟 | 中等风险 |
- **隐藏亏损**：70%以上的未平仓交易处于亏损状态 | 高风险 |
- **多数未平仓交易处于亏损状态**：50%以上的未平仓交易处于亏损状态 | 中等风险 |
- **未发现重大风险警示**：未发现异常交易模式 | 无风险 |

## REST API（备用方案）

对于无法使用MCP的工具，所有功能都可以通过REST接口访问：`https://api.polyvisionx.com`。大多数接口需要使用Bearer令牌进行身份验证（部分接口除外）。

交互式文档和OpenAPI规范请参考：
- **Swagger UI**：`https://api.polyvisionx.com/docs`
- **OpenAPI JSON**：`https://api.polyvisionx.com/openapi.json`

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `POST /v1/auth/register` | 注册并获取API密钥（无需认证） |
| `GET /v1/auth/me` | 获取当前用户信息和使用统计 |
| `POST /v1/auth/regenerate` | 重新生成API密钥 |
| `POST /v1/auth/deactivate` | 停用API密钥 |
| `GET /v1/analyze/{wallet_address}?mode=quick` | 执行全面钱包分析 |
| `GET /v1/score/{wallet_address}` | 获取简洁的跟单交易评分 |
| `GET /health` | 检查系统运行状态（无需认证） |

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

## 错误代码

| 代码 | 含义 | 处理方式 |
| --- | --- | --- |
| 400 | 钱包地址无效（必须是42个字符的十六进制地址，以`0x`开头） | 请检查地址格式 |
| 401 | API密钥无效或已停用 | 请检查您的`POLYVISION_API_KEY`或重新注册 |
| 409 | 该邮箱已注册（仅限注册） | 使用现有密钥或使用其他邮箱注册 |
| 429 | 使用频率受限 | 请稍后重试（Polymarket API有使用频率限制） |
| 503 | 系统已满载（所有分析资源已占用） | 30-60秒后重试 |
| 504 | 分析超时 | 可能是因为钱包的交易记录过多，请稍后重试 |