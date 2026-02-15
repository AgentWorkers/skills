---
name: riskofficer
description: 管理投资组合，计算风险指标（如 Value at Risk, VaR；蒙特卡洛模拟；压力测试），并利用风险均衡（Risk Parity）或卡尔玛比率（Calmar Ratio）来优化资产配置。
metadata: {"openclaw":{"requires":{"env":["RISK_OFFICER_TOKEN"]},"primaryEnv":"RISK_OFFICER_TOKEN","emoji":"📊","homepage":"https://riskofficer.tech"}}
---

## RiskOfficer投资组合管理

该功能通过RiskOfficer API来管理投资组合并计算风险。

### 设置

1. 打开RiskOfficer应用程序 → 设置 → API密钥
2. 为“OpenClaw”创建一个新的令牌
3. 设置环境变量：`RISK_OFFICER_TOKEN=ro_pat_...`

或者可以在`~/.openclaw/openclaw.json`中进行配置：
```json
{
  "skills": {
    "entries": {
      "riskofficer": {
        "enabled": true,
        "apiKey": "ro_pat_..."
      }
    }
  }
}
```

### API基础URL

```
https://api.riskofficer.tech/api/v1
```

所有请求都需要包含以下头部信息：`Authorization: Bearer ${RISK_OFFICER_TOKEN}`

---

## 可用的命令

### 投资组合管理

#### 列出投资组合
当用户希望查看他们的投资组合或投资组合概览时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/portfolios/list" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

响应中包含一个投资组合数组，其中包含：id、名称、总价值、货币、持仓数量、经纪商和沙箱（sandbox）信息。

#### 获取投资组合详情
当用户询问特定投资组合或想要查看持仓情况时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/portfolio/snapshot/{snapshot_id}" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

响应中包含：名称、总价值、货币以及持仓信息（数组，包含股票代码、数量、当前价格、价值和权重）。

#### 获取投资组合历史
当用户请求查看投资组合的历史变化或过去的快照列表时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/portfolio/history?days=30" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

**查询参数：**`days`（可选，默认为30天，范围1–365天）。响应中包含：`snapshots`数组，其中包含`snapshot_id`、`timestamp`、`total_value`、`positions_count`、`sync_source`、`type`（聚合/手动/经纪商）、`name`、`broker`、`sandbox`。

#### 获取快照差异（比较两个投资组合版本）
当用户想要比较两个投资组合的状态（例如再平衡前后的状态）时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/portfolio/snapshot/{snapshot_id}/diff?compare_to={other_snapshot_id}" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

响应中包含：新增/移除/修改的持仓情况以及`total_value_delta`。这两个快照必须都属于同一用户。

#### 获取汇总投资组合
当用户请求查看汇总投资组合、整体持仓情况或“全部合并显示”时：

**查询参数：**
- `type=production` — 手动 + 经纪商（sandbox=false）
- `type=sandbox` — 仅经纪商（sandbox=true）
- `type=all` — 全部（默认）

**响应：**
- `portfolio.positions` — 各投资组合中的所有持仓合并后的列表
- `portfolio.total_value` — 总价值（以基础货币表示）
- `portfolio(currency` — 基础货币（RUB或USD）
- `portfolio.sources_count` — 被汇总的投资组合数量

**示例响应：**
```json
{
  "portfolio": {
    "positions": [
      {"ticker": "SBER", "quantity": 150, "value": 42795, "sources": ["Т-Банк", "Manual"]},
      {"ticker": "AAPL", "quantity": 10, "value": 189500, "original_currency": "USD"}
    ],
    "total_value": 1500000,
    "currency": "RUB",
    "sources_count": 3
  },
  "snapshot_id": "uuid-of-aggregated"
}
```

**货币转换：**不同货币的持仓会自动根据当前汇率（RUB的CBR）转换为基础货币。

#### 更改基础货币（汇总投资组合）
当用户希望以不同货币查看汇总投资组合时：

```bash
curl -s -X PATCH "https://api.riskofficer.tech/api/v1/portfolio/{aggregated_snapshot_id}/settings" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"base_currency": "USD"}'
```

**支持的货币：**`RUB`、`USD`

更改后，汇总投资组合会自动重新计算。

**用户示例指令：**
- “以美元显示所有信息” → 将基础货币更改为USD
- “将投资组合转换为卢布” → 将基础货币更改为RUB

#### 从汇总中包含/排除投资组合
当用户希望从总计算中排除某个投资组合时：

```bash
curl -s -X PATCH "https://api.riskofficer.tech/api/v1/portfolio/{snapshot_id}/settings" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"include_in_aggregated": false}'
```

**使用场景：**
- “在总投资组合中不考虑沙箱投资组合” → 排除沙箱投资组合
- “从计算中移除演示投资组合” → 移除手动创建的投资组合

#### 创建手动投资组合
当用户希望创建具有特定持仓的新投资组合时：

```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/portfolio/manual" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Portfolio Name",
    "positions": [
      {"ticker": "SBER", "quantity": 100},
      {"ticker": "GAZP", "quantity": 50}
    ]
  }'
```

**重要规则 - 单一货币：**投资组合中的所有资产必须使用相同的货币。
- RUB资产：SBER、GAZP、LKOH、YNDX等
- USD资产：AAPL、MSFT、GOOGL等
不能混合使用！如果用户尝试混合货币，请解释并要求他们创建单独的投资组合。

#### 更新投资组合（添加/移除持仓）
当用户想要修改现有投资组合时：

1. 首先获取当前投资组合的名称：
```bash
curl -s "https://api.riskofficer.tech/api/v1/portfolio/snapshot/{snapshot_id}" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

2. 然后使用相同的名称创建一个新的快照：
```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/portfolio/manual" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<same name from step 1>",
    "positions": [<updated list of all positions>]
  }'
```

**重要提示：**在更新之前，务必向用户显示更改的内容并征求确认。

---

### 经纪商集成

#### 列出连接的经纪商
当用户询问连接的经纪商或经纪商的状态时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/brokers/connections" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

#### 从Tinkoff同步投资组合
当用户希望从Tinkoff同步/更新投资组合时（经纪商必须通过应用程序连接）：

```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/portfolio/proxy/broker/tinkoff/portfolio" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"sandbox": false}'
```

如果响应代码为400且包含`missing_api_key`，则表示经纪商未连接。请指导用户如何连接：
1. 从https://www.tbank.ru/invest/settings/api/获取API令牌
2. 打开RiskOfficer应用程序 → 设置 → 经纪商 → 连接Tinkoff
3. 粘贴令牌并完成连接

---

### 风险计算

#### 计算VaR（免费）
当用户请求计算风险、VaR或风险指标时：

```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/risk/calculate-var" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_snapshot_id": "{snapshot_id}",
    "method": "historical",
    "confidence": 0.95,
    "horizon_days": 1,
    "force_recalc": false
  }'
```

- **方法：**`historical`、`parametric`、`garch`
- `force_recalc`（可选，默认为false）：如果用户希望忽略缓存并重新计算（例如“重新计算VaR”或“刷新风险”），则设置`"force_recalc": true`。否则，即使价格未变化，API也可能返回缓存结果。

此操作会返回`calculation_id`。需要通过轮询获取结果：

```bash
curl -s "https://api.riskofficer.tech/api/v1/risk/calculation/{calculation_id}" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

等待`status`变为`done`后，再展示结果。如果POST响应中已经包含`status: "done"`以及`var_95`/`cvar_95`（缓存结果），则可以直接展示这些数据而无需轮询。

#### 获取VaR / 风险计算历史
当用户请求查看最近的风险计算结果、之前的VaR结果或“显示我的风险历史”时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/risk/history?limit=50" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

**查询参数：**`limit`（可选，默认为50条，最多100条）。

**响应：**`calculations`数组，其中包含`calculation_id`、`portfolio_snapshot_id`、`status`、`method`、`var_95`、`cvar_95`、`sharpe_ratio`、`created_at`、`completed_at`。这些信息可用于展示最近的VaR计算结果或让用户选择过去的计算结果。

#### 运行蒙特卡洛模拟（Quant功能 - 目前对所有用户免费）
当用户请求进行蒙特卡洛模拟时：

```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/risk/monte-carlo" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_snapshot_id": "{snapshot_id}",
    "simulations": 1000,
    "horizon_days": 365,
    "model": "gbm"
  }'
```

轮询：`GET /api/v1/risk/monte-carlo/{simulation_id}`

#### 运行压力测试（Quant功能 - 目前对所有用户免费）
当用户请求进行压力测试时：

首先，获取可用的危机情景：
```bash
curl -s "https://api.riskofficer.tech/api/v1/risk/stress-test/crises" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

然后运行压力测试：
```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/risk/stress-test" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_snapshot_id": "{snapshot_id}",
    "crisis": "covid_19"
  }'
```

轮询：`GET /api/v1/risk/stress-test/{stress_test_id}`

---

### 投资组合优化（Quant功能 - 目前对所有用户免费）

#### 风险均衡优化
当用户请求优化投资组合或平衡风险时：

```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/portfolio/{snapshot_id}/optimize" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "optimization_mode": "preserve_directions",
    "constraints": {
      "max_weight": 0.30,
      "min_weight": 0.02
    }
  }'
```

**模式：**
- `long_only`：所有持仓的权重均大于等于0
- `preserve_directions`：保持多头/空头的方向不变
- `unconstrained`：允许任何方向

轮询：`GET /api/v1/portfolio/optimizations/{optimization_id}`

结果：`GET /api/v1/portfolio/optimizations/{optimization_id}/result`

#### Calmar比率优化
当用户请求进行Calmar比率优化时，目标是最大化Calmar比率（CAGR / |Max Drawdown|）。**每个股票代码需要至少200天的交易历史数据**（后端请求需要252天的数据）。如果用户的交易历史数据不足，建议使用风险均衡优化。

```bash
curl -s -X POST "https://api.riskofficer.tech/api/v1/portfolio/{snapshot_id}/optimize-calmar" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "optimization_mode": "long_only",
    "constraints": {
      "max_weight": 0.50,
      "min_weight": 0.05,
      "min_expected_return": 0.0,
      "max_drawdown_limit": 0.15,
      "min_calmar_target": 0.5
    }
  }'
```

轮询：`GET /api/v1/portfolio/optimizations/{optimization_id}`（检查`optimization_type === "calmar_ratio"`）
结果：`GET /api/v1/portfolio/optimizations/{optimization_id}/result` — 包含`current_metrics`、`optimized_metrics`（cagr、max_drawdown、calmar_ratio）。
应用优化：`POST /api/v1/portfolio/optimizations/{optimization_id}/apply`。

**重要提示：**在应用优化之前，务必先展示再平衡计划并征求用户的明确确认！

---

### 订阅状态

> **注意：**Quant订阅功能目前对所有用户免费。所有功能均可免费使用。

#### 检查订阅状态
当需要检查用户是否拥有Quant订阅时：

```bash
curl -s "https://api.riskofficer.tech/api/v1/subscription/status" \
  -H "Authorization: Bearer ${RISK_OFFICER_TOKEN}"
```

目前所有用户的`has_subscription`字段都设置为`true`（免费 tier已启用）。

---

## 异步操作

VaR、蒙特卡洛模拟、压力测试和优化操作都是异步进行的。

**轮询流程：**
1. 调用POST接口以获取`calculation_id` / `simulation_id` / `optimization_id`
2. 每2-3秒轮询一次GET接口
3. 检查`status`字段：
   - `pending`或`processing` → 继续轮询
   - `done` → 显示结果
   - `failed` → 显示错误信息

**典型耗时：**
| 操作 | 典型耗时 |
|-----------|--------------|
| VaR | 3-10秒 |
| Monte Carlo | 10-30秒 |
| Stress Test | 5-15秒 |
| Optimization | 10-30秒 |

**用户反馈：**
- 开始操作后立即显示“计算中...”的消息
- 如果轮询超过10秒，更新为：“仍在计算中...请稍候”
- 完成后始终显示结果或错误信息

---

## 重要规则

1. **单一货币规则（手动/经纪商投资组合）：**每个投资组合中的资产必须使用相同的货币。例如，不能在同一投资组合中同时包含RUB资产（如SBER）和USD资产（如AAPL）。建议用户创建单独的投资组合。
2. **汇总投资组合：**汇总投资组合可以包含不同货币的资产——这些资产会自动根据CBR汇率转换为基础货币（RUB或USD）。
3. **订阅：**蒙特卡洛模拟、压力测试和优化功能目前对所有用户免费。VaR功能始终免费。
4. **经纪商集成：**用户必须先在RiskOfficer应用程序中连接经纪商。无法通过聊天界面进行连接（出于安全考虑）。
5. **确认：**在应用优化或进行重大投资组合更改之前，务必向用户展示更改内容并征求确认。
6. **异步操作：**VaR、蒙特卡洛模拟、压力测试和优化操作都是异步进行的。需要轮询以获取结果。
7. **错误处理：**
   - 401 Unauthorized → 令牌无效或过期，用户需要重新创建令牌
   - 403 subscription_required → 需要Quant订阅（目前对所有用户免费）
   - 400 missing_api_key → 经纪商未连接
   - 400 currency_mismatch → 资产货币不匹配

---

## 示例对话

### 用户请求投资组合概览
用户：“显示我的投资组合”
→ 调用`GET /portfolios/list`
→ 以美观的格式显示投资组合的名称、持仓数量和最新更新时间

### 用户请求汇总投资组合
用户：“全部合并显示” / “我的总投资额是多少？”
→ 调用`GET /portfolio/aggregated?type=all`
→ 显示总价值、合并后的所有持仓以及来源数量
→ 注意哪些持仓是从其他货币转换而来的

### 用户希望更改显示货币
用户：“以美元显示” / “切换到USD”
→ 调用`PATCH /portfolio/{aggregated_id}/settings`并设置`{"base_currency": "USD"}`
→ 再次调用`GET /portfolio/aggregated`
→ 以新的货币显示投资组合

### 用户希望分析风险
用户：“我的主要投资组合的风险是多少？”
→ 调用`GET /portfolios/list`找到相关投资组合
→ 调用`POST /risk/calculate-var`
→ 等待计算完成
→ 显示VaR、CVaR、波动率以及风险贡献
→ 如果风险不平衡，建议进行优化

### 用户请求Calmar比率优化
用户：“使用Calmar比率优化投资组合” / “优化投资组合”
→ 调用`GET /portfolios/list`或`GET /portfolio/optimizations`获取快照ID
→ 调用`POST /portfolio/{snapshot_id}/optimize-calmar`并设置优化模式和可选参数
→ 如果返回400 INSUFFICIENT_HISTORY，说明需要至少200天的交易历史数据，建议使用风险均衡优化
→ 轮询`GET /optimizations/{id}`直到状态变为`done`
→ 调用`GET /optimizations/{id}/result`查看优化前后的指标（Calmar比率、CAGR、最大回撤率）
→ 显示再平衡计划并征求用户的确认

### 用户尝试混合货币
用户：“将Apple股票添加到我的投资组合中”
→ 检查投资组合的货币（RUB）与Apple股票的货币（USD）是否匹配
→ 解释无法混合使用不同货币，并建议创建单独的USD投资组合

### 用户请求进行蒙特卡洛模拟或压力测试
用户：“运行蒙特卡洛模拟”
→ 调用`POST /risk/monte-carlo`并提供投资组合快照
→ 等待模拟结果并显示百分位数和预测数据

### 用户请求风险或VaR历史
用户：“显示我之前的VaR结果” / “之前的风险计算记录”
→ 调用`GET /risk/history?limit=50`
→ 显示最近的计算结果（包括计算方法、var_95、cvar_95、日期）

### 用户请求投资组合历史
用户：“我的投资组合发生了哪些变化？” / “投资组合的历史记录”
→ 调用`GET /portfolio/history?days=30`
→ 显示投资组合的历史快照（包括日期、总价值、持仓数量）

### 用户比较两个投资组合版本
用户：“比较我现在和上周的投资组合” / “我的投资组合发生了哪些变化？”
→ 从`GET /portfolio/history`获取两个快照ID
→ 调用`GET /portfolio/snapshot/{snapshot_id}/diff?compare_to={other_snapshot_id}`
→ 显示新增/移除/修改的持仓以及价值变化情况