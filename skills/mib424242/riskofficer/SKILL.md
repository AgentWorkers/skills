---
name: riskofficer
description: Risk management and portfolio analytics: VaR, Monte Carlo, stress tests, Risk Parity and Calmar optimization. Run risk assessments, scenarios, and allocation optimization on virtual portfolios; no real broker orders.
metadata: {"openclaw":{"requires":{"env":["RISK_OFFICER_TOKEN"]},"primaryEnv":"RISK_OFFICER_TOKEN","emoji":"📊","homepage":"https://riskofficer.tech"}}
---

## RiskOfficer投资组合管理

该技能通过连接RiskOfficer API来管理投资组合并计算财务风险指标。

**所需环境变量：** `RISK_OFFICER_TOKEN`（在RiskOfficer应用程序的“设置”→“API密钥”中创建）。无需其他环境变量或二进制文件。

**来源：** 官方技能仓库：[github.com/mib424242/riskofficer-openclaw-skill](https://github.com/mib424242/riskofficer-openclaw-skill)；产品官网：[riskofficer.tech](https://riskofficer.tech)。该技能仅使用RiskOfficer应用程序生成的令牌，不会收集或存储任何凭证。

### 使用范围：** 仅用于分析和研究（虚拟投资组合）

**此技能中的所有投资组合数据和操作均发生在RiskOfficer的内部环境中。** 在这里创建、编辑或优化的投资组合均为**虚拟**投资组合，仅用于分析和研究。该助手可以：  
- **读取**您的投资组合信息（包括从经纪商同步的数据），显示持仓、历史记录和风险指标；  
- **创建和修改**虚拟/手动投资组合，并在RiskOfficer内部进行优化；  
- **对这些投资组合运行计算**（如VaR、蒙特卡洛模拟、压力测试）。

**该技能不会在您的经纪商账户中下达或执行任何真实交易指令。** 经纪商数据的同步仅用于分析；任何重新平衡或交易操作均由您在经纪商的应用程序或RiskOfficer的内部流程中完成，而非由助手执行。令牌仅用于访问RiskOfficer的API以进行这些分析和研究操作。

### 设置方法

1. 打开RiskOfficer应用程序 → “设置” → “API密钥”  
2. 创建一个名为“OpenClaw”的新令牌  
3. 设置环境变量：`RISK_OFFICER_TOKEN=ro_pat_...`  
**或配置在`~/.openclaw/openclaw.json`文件中：**  

### API基础URL  
（此处应填写RiskOfficer API的实际URL）

所有请求都需要包含`Authorization: Bearer ${RISK_OFFICER_TOKEN}`头。

---

## 可用命令

### 股票搜索

#### 搜索股票代码  
在创建或编辑任何投资组合之前，使用此功能来验证股票代码并获取其货币/交易所信息。当用户输入公司名称而非股票代码时也可使用此功能。  

**查询参数：**  
- `q`（可选）：搜索条件——按股票代码、名称或全称（不区分大小写）。省略此参数将获取按流行度排序的热门股票代码。  
- `limit`（可选，默认20条，最多50条）：返回结果的数量。  
- `include_prices`（可选，默认`false`）：是否包含`current_price`、`price_change_percent`、`price_change_absolute`、`price_date`。  
- `locale`（可选，默认`ru`）：`en`表示英文名称，`ru`表示俄文名称。  
- `exchange`（可选）：按交易所过滤——`MOEX`、`NYSE`、`NASDAQ`、`CRYPTO`。  

**返回结果：** `tickers`数组，每个元素包含：`ticker`、`name`、`full_name`、`instrument_type`、`currency`、`exchange`、`popularity_score`、`isin`。  

**股票类型：** `share`（股票）、`bond`（债券）、`etf`（交易所交易基金）、`futures`（期货）、`futures_continuous`（例如MOEX上的BR、SI）。  

**重要规则：**  
- 始终使用股票搜索功能将公司名称转换为股票代码（例如：“Apple” → “AAPL”，“Sberbank” → “SBER”）。  
- 在将股票添加到投资组合之前，请使用结果中的`currency`字段检查货币是否一致。  
- 对于MOEX期货，搜索“BR”或“SI”将返回连续合约（例如BRF6、SIM5），而非单个合约。  
- 如果用户询问“X的价格是多少？”，请设置`include_prices=true`以显示当前价格。  

#### 获取历史股票价格  
当用户询问特定资产的价格历史、图表数据或趋势时：  

**查询参数：**  
`tickers`（必填，用逗号分隔，最多50个），`days`（可选，默认7天，最多252个交易日）。  

**返回结果：** `data`对象，每个元素包含按股票代码键值的字段：  
- `prices`：`date`、`close`对象数组。  
- `current_price`、`price_change_percent`、`price_change_absolute`。  

---

### 投资组合管理

#### 列出投资组合  
当用户希望查看他们的投资组合或获取概览时：  

**查询参数：**  
`portfolio_type`（可选）：`"production"`（手动+真实经纪账户）、`"sandbox"`（仅限经纪商沙箱）、`"all"`（默认）。  

返回结果：包含`snapshot_id`、`name`、`total_value`、`currency`、`positions_count`、`broker`、`sandbox`、`active_snapshot_id`（UUID或null——如果设置了`active_snapshot_id`，则使用该历史快照而非最新快照）的投资组合数组。  

#### 获取投资组合详情  
当用户希望查看特定投资组合中的持仓情况时：  

**返回结果：**  
`name`、`total_value`、`currency`、`positions`（包含`ticker`、`quantity`、`current_price`、`value`、`weight`、`avg_price`的数组）。  

#### 获取投资组合历史  
当用户询问投资组合随时间的变化情况或希望浏览历史快照时：  

**查询参数：**  
`days`（可选，默认30天，范围1–365天）。  

**返回结果：** `snapshots`数组，每个元素包含：`snapshot_id`、`timestamp`、`total_value`、`positions_count`、`sync_source`、`type`（`aggregated`/`manual`/`broker`）、`name`、`broker`、`sandbox`。  

#### 获取投资组合差异（比较两个投资组合版本）  
当用户希望比较两个投资组合的状态（例如重新平衡前后或两个日期之间的差异）时：  

**返回结果：** `added`/`removed`/`modified`的持仓情况，以及`total_value_delta`。两个快照必须属于同一用户。  

#### 获取汇总投资组合  
当用户希望查看所有账户的总投资组合情况时：  

**查询参数：**  
- `type=production`：手动+真实经纪账户  
- `type=sandbox`：仅限经纪商沙箱  
- `type=all`：所有账户（默认）。  

**返回结果：**  
- `portfolio_positions`：合并后的所有持仓；  
- `portfolio.total_value`：以基础货币表示的总价值；  
- `portfolio.currency`：基础货币（`RUB`或`USD`）；  
- `portfolio.sources_count`：汇总的投资组合数量。  

**示例返回结果：**  
（此处应展示合并后的投资组合数据。）  

#### 更改基础货币（汇总投资组合）  
当用户希望以不同货币查看汇总投资组合时：  

**返回结果：**  
（此处应展示转换后的投资组合数据。）  

**支持的货币：** `RUB`、`USD`。更改基础货币后，汇总投资组合会自动重新计算。  

**用户示例指令：**  
- “以美元显示所有信息” → `base_currency: "USD"`  
- “转换为卢布” → `base_currency: "RUB"`  

#### 从汇总中排除/包含投资组合  
当用户希望从总计算中排除某个投资组合时：  

**用户示例指令：**  
- “从总金额中排除沙箱账户”  
- “从计算中移除演示账户”  

#### 创建手动投资组合  
当用户希望创建具有特定持仓的新投资组合时：  

**所需字段：**  
- `ticker`（必填）：股票代码。**务必先使用`/tickers/search`验证并检查货币。  
- `quantity`（必填）：股票数量。**负数表示空头持仓（例如`-20`表示持有20股空头）。  
- `avg_price`（可选）：用于跟踪盈亏的平均买入/入场价格。新投资组合中省略此参数时，使用当前市场价格；编辑时省略则继承自上一个快照。  

**查询参数：**  
`locale`（可选，默认`ru`）——影响资产名称的解析。  

**重要规则：**  
- 同一投资组合中的所有资产必须使用**相同货币**。  
- **RUB资产（MOEX）**：例如SBER、GAZP、LKOH、YNDX等；  
- **USD资产（NYSE/NASDAQ）**：例如AAPL、MSFT、GOOGL、TSLA等。  
**同一投资组合中不能混合不同货币！** 建议创建单独的投资组合。  

**空头持仓：**  
- 使用负数`quantity`表示空头持仓（例如`{"ticker": "GAZP", "quantity": -50}`）。  
- 支持在同一投资组合中同时持有多头和空头持仓（长多/短多投资组合）。  
- 在优化长多/短多投资组合时，使用`optimization_mode: "preserve_directions"`以保持空头持仓的方向。  

#### 更新投资组合（添加/删除持仓）  
当用户希望修改现有投资组合时：  
1. 获取当前持仓情况：  
（此处应展示当前持仓数据。）  
2. 用相同的名称和更新后的持仓列表重新提交请求：  
（此处应展示更新后的投资组合数据。）  

**重要提示：**  
- 在更新前务必向用户显示即将发生的变化并请求确认。除非明确指定，否则会保留`avg_price`。  

#### 删除手动投资组合  
当用户希望完全删除手动创建的投资组合时：  

**返回结果：**  
- 投资组合名称必须进行URL编码；  
- 该投资组合的所有快照将被归档（不可撤销）；  
- **删除前务必确认**——删除操作不可撤销；  
- 返回结果包括归档的快照数量、投资组合名称和提示信息。  

#### 删除经纪商投资组合快照  
当用户希望清除经纪商的投资组合历史记录而不断开连接时：  

**返回结果：**  
- `sandbox=true`表示沙箱投资组合，`sandbox=false`表示真实账户；  
- 仅归档快照；经纪商连接保持激活状态；  
- 下一次同步将创建新的快照；  
**删除前务必确认**。  

---

### 经纪商集成  

#### 列出连接的经纪商  
当用户询问他们的经纪商连接情况时：  

**返回结果：**  
（此处应列出所有连接的经纪商名称。）  

#### 列出可用的经纪商提供商  
当用户询问支持哪些经纪商时：  

**返回结果：**  
（此处应列出所有支持的经纪商名称。）  

#### 从经纪商同步投资组合  
当用户希望从连接的经纪商处刷新/更新投资组合时：  

**请求参数：**  
`{broker}`：例如`tinkoff`或`alfa`；  
`sandbox`：`false`表示真实账户，`true`表示Tinkoff沙箱账户。  

如果返回`400`且显示`missing_api_key`，则表示经纪商未连接。指导用户：  
1. 从https://www.tbank.ru/invest/settings/api/获取API令牌；  
2. 打开RiskOfficer应用程序 → “设置” → “经纪商” → “连接Tinkoff”；  
3. 粘贴令牌并完成连接。  

#### 断开经纪商连接  
当用户希望断开经纪商连接时：  

**返回结果：**  
- `sandbox=false`表示真实账户，`sandbox=true`表示沙箱账户；  
- 删除连接及其保存的API密钥；投资组合的快照历史记录将被保留；  
- 要删除快照历史记录，请先使用`DELETE /portfolio/broker/{broker}?sandbox=false`；  
**删除前务必确认**——重新连接需要使用移动应用程序。  

**两个删除端点的区别：**  
| 操作 | `DELETE /portfolio/broker/{id}` | `DELETE /brokers/connections/{id}` |
|--------|-------------------------------|----------------------------------|
| 删除快照 | ✅ 是（归档历史记录） | ❌ 否（不保留历史记录） |
| 删除连接 | ❌ 否 | ✅ 是 |
| 可以在不重新连接的情况下再次同步 | ✅ 是 | ❌ 否 |  

---

### 活动快照选择  

默认情况下，所有风险计算使用**最新**快照。您可以固定一个历史快照，以便针对过去的投资组合状态运行计算——这对于回测风险或比较“重新平衡前后的情况”非常有用。  

#### 设置活动快照  
当用户希望根据历史版本的投资组合运行风险计算时：  

**`portfolio_key`格式：**  
| 投资组合类型 | 格式 | 示例 |  
|---|---|---|  
| 汇总 | `aggregated` | `"aggregated"` |  
| 手动 | `manual:{name}` | `"manual:My Portfolio"` |  
| 真实经纪账户 | `broker:{broker_id}:false` | `"broker:tinkoff:false"` |  
| 经纪商沙箱 | `broker:{broker_id}:true` | `"broker:tinkoff:true"` |  

**工作流程：**  
1. `GET /portfolio/history?days=90` → 按日期选择快照；  
2. 使用选定的`snapshot_id`和`portfolio_key`通过`PATCH /portfolio/active-snapshot`设置活动快照；  
3. 运行VaR/蒙特卡洛模拟；  
4. 完成后重置（详见下文）。  

**在`/portfolios/list`中：** `active_snapshot_id`字段显示当前使用的快照（`null`表示使用最新快照）。  

#### 将活动快照重置为最新  
**用户示例指令：**  
- “计算一个月前的投资组合风险” → 设置活动快照；  
- “恢复到当前投资组合状态” → 删除活动快照。  

---

### 风险计算  

#### 计算VaR（免费）  
当用户请求计算风险、VaR或风险指标时：  

**参数：**  
- `method`：`"historical"`（默认，推荐）、`"parametric"`或`"garch"`；  
- `confidence`：置信水平，默认`0.95`（范围0.01–0.99）；  
- `horizon_days`：预测期限，默认`1`（范围1–30天）；  
- `force_recalc`（可选，默认`false`）：设置为`true`以绕过缓存并强制重新计算（当用户请求“重新计算”或“刷新”时使用）。  

**返回结果：**  
- 如果`reused_existing: true`且`status: "done"`，则结果已包含在响应中（`var_95`、`cvar_95`、`sharpe_ratio`），无需再次请求；  
- 否则，返回`calculation_id`并等待结果。  

**等待`status: "done"`后显示结果。**

#### 获取VaR/风险计算历史记录  
当用户请求过去的风险计算结果时：  

**查询参数：**  
`limit`（可选，默认50条，最多100条）。  

**返回结果：** `calculations`数组，每个元素包含`calculation_id`、`portfolio_snapshot_id`、`status`、`method`、`var_95`、`cvar_95`、`sharpe_ratio`、`created_at`、`completed_at`。  

#### 运行蒙特卡洛模拟（Quant功能，目前对所有用户免费）  
当用户请求进行蒙特卡洛模拟时：  

**参数：**  
- `simulations`：模拟路径的数量，默认`1000`（范围100–10000）；  
- `horizon_days`：预测期限，默认`365`（范围1–365天）；  
- `model`：`"gbm"`（几何布朗运动模型，推荐）或`"garch"`；  
- `confidence_levels`（可选）：百分位数数组，默认`[0.05, 0.50, 0.95]`；  
- `force_recalc`（可选，默认`false`）：绕过缓存。  

**请求路径：** `GET /api/v1/risk/monte-carlo/{simulation_id}`  

#### 运行压力测试（Quant功能，目前对所有用户免费）  
当用户请求进行压力测试时：  
首先获取可用的危机情景：  

**参数：**  
`crisis`：来自`/stress-test/crises`的危机情景ID（例如`covid_19`、`2008_crisis`）；  
然后运行模拟：  

**参数：**  
`simulations`：模拟路径的数量；  
`horizon_days`：预测期限；  
`model`：模拟模型；  
`force_recalc`：是否强制重新计算。  

**请求路径：** `GET /api/v1/risk/stress-test/{stress_test_id}`  

---

### 投资组合优化（Quant功能，目前对所有用户免费）  

#### 风险均衡优化  
当用户请求优化投资组合或平衡风险时：  

**`optimization_mode`：**  
- `"long_only"`：所有权重≥0（优化前将空头持仓转换为多头）；  
- `"preserve_directions"`：保持多头/空头的方向不变（默认）；  
- `"unconstrained"`：权重可以自由变化。  

**请求路径：** `GET /api/v1/portfolio/optimizations/{optimization_id}`  
**返回结果：** `GET /api/v1/portfolio/optimizations/{optimization_id}/result`  

**重要提示：**  
- 优化时，请使用`active_snapshot_id`或投资组合列表中的`snapshot_id`（如果设置了历史快照，则使用该快照）。  

#### 卡尔玛比率优化  
当用户请求最大化卡尔玛比率（CAGR / 最大回撤）时：  
**要求每个股票有200天以上的交易历史数据**（后台请求需要252天数据）。如果投资组合的历史数据不足，建议使用风险均衡优化。  

**请求路径：** `GET /api/v1portfolio/optimizations/{optimization_id}`（检查`optimization_type === "calmar_ratio"`）。  
**返回结果：** `GET /api/v1/portfolio/optimizations/{optimization_id}/result`——包含`current_metrics`和`optimized_metrics`（CAGR、最大回撤、卡尔玛比率）。  
**应用优化：** `POST /api/v1/portfolio/optimizations/{optimization_id}/apply`。  

**错误提示：**  
`INSUFFICIENT_HISTORY`：历史数据不足——提示需要200天以上的交易数据，并建议使用风险均衡优化。  

#### 应用优化结果  
**重要提示：**  
- 应始终向用户展示完整的重新平衡计划，并在应用前请求确认！  

**返回结果：** `new_snapshot_id`。优化结果只能应用一次。  

---

### 订阅状态  
> **注意：** Quant功能目前对所有用户免费。所有功能均可免费使用。  

**返回结果：**  
`has_subscription: true`。  

---

## 异步操作  
VaR、蒙特卡洛模拟、压力测试和优化操作均为**异步**。  

**请求模式：**  
1. 发送POST请求到相应端点以获取`calculation_id`/`simulation_id`/`optimization_id`；  
2. 每2–3秒轮询一次相应GET端点；  
3. 检查状态：  
  - `pending`或`processing`：继续轮询；  
  - `done`：显示结果；  
  - `failed`：显示错误信息。  

**典型处理时间：**  
| 操作 | 处理时间 |  
|-----------|-------------|  
| VaR | 3–10秒 |  
| 蒙特卡洛模拟 | 10–30秒 |  
| 压力测试 | 5–15秒 |  
| 优化 | 10–30秒 |  

**用户交互提示：**  
- 开始操作后立即显示“正在计算中”；  
- 如果轮询超过10秒，显示“仍在计算中，请稍候...”；  
- 始终显示最终结果或错误信息。  

---

## 重要规则  

0. **虚拟/分析用途：** 所有投资组合及操作（创建、优化、删除、同步）仅存在于RiskOfficer内部。该技能仅用于分析和研究，不会下达或执行真实经纪商订单。  
1. **单一货币规则（手动/经纪账户投资组合）：** 同一投资组合中的所有资产必须使用相同货币。例如不能将RUB资产（MOEX）与USD资产（NYSE/NASDAQ）混合；汇总投资组合是例外——它会自动使用CBR汇率进行转换。  
2. **空头持仓：** 负数`quantity`表示空头持仓。在优化长多/短多投资组合时，使用`optimization_mode: "preserve_directions"`以保持空头持仓的方向。  
3. **始终先搜索股票代码：** 在创建或编辑投资组合之前，使用`/tickers/search`验证股票代码并检查其货币。  
4. **确认操作：** 在更新/删除投资组合、应用优化或断开经纪商连接之前，务必向用户显示即将发生的变化并请求确认。这些操作可能是不可逆的。  
5. **异步操作：** VaR、蒙特卡洛模拟、压力测试和优化操作均为异步处理。结果通过轮询获取。  
6. **订阅：** 蒙特卡洛模拟、压力测试和优化功能目前免费；VaR功能始终免费。  
7. **经纪商集成：** 用户必须先通过RiskOfficer移动应用程序连接经纪商。无法通过聊天界面连接。  
8. **错误处理：**  
  - `401 Unauthorized`：令牌无效或已过期；用户需要重新生成令牌；  
  - `403 subscription_required`：需要Quant订阅（目前对所有用户免费）；  
  - `400 missing_api_key`：经纪商未通过应用程序连接；  
  - `400 currency_mismatch`：同一投资组合中混合了不同货币；  
  - `400 INSUFFICIENT_HISTORY`：历史数据不足（需要200天以上的交易数据）；建议使用风险均衡优化；  
  - `404 Not Found`：投资组合或快照未找到（可能已被删除）；  
  - `429 Too Many Requests`：达到请求限制；  
9. **活动快照：** 在运行计算时，`/portfolios/list`中的`active_snapshot_id`优先于`snapshot_id`。在调用优化函数时使用`active_snapshot_id || snapshot_id`。  

---

## 示例对话  

### 用户查看投资组合  
“显示我的投资组合” → `GET /portfolios/list`  
→ 以美观的格式显示投资组合的名称、总价值、持仓数量、货币和最后更新时间。  

### 用户查看所有账户的总金额  
“显示所有账户的总金额” → `GET /portfolio/aggregated?type=all`  
→ 显示合并后的总价值、持仓数量及来源；  
→ 注意其他货币的持仓会自动转换为美元显示。  

### 用户更改显示货币  
“以美元显示所有信息” → `PATCH /portfolio/{aggregated_id}/settings`，设置`{"base_currency": "USD"`；  
→ 重新获取`GET /portfolio/aggregated`；  
→ 以新货币显示投资组合。  

### 用户通过公司名称查询股票代码  
“将Sberbank添加到我的投资组合” / “Gazprom的代码是什么？” → `GET /tickers/search?q=Sberbank&locale=en`  
→ 找到股票代码`SBER`，货币`RUB`，交易所`MOEX`；  
→ 确认后创建/更新投资组合。  

### 用户查询股票价格  
“特斯拉的价格是多少？” → `GET /tickers/search?q=TSLA&include_prices=true`  
→ 显示`current_price`、`price_change_percent`和交易所信息。  

### 用户创建长多/短多投资组合  
“创建投资组合：持有100股SBER股票，卖出50股YNDX股票” →  
- 使用`/tickers/search`查询股票代码；  
- 确认股票代码和货币兼容后，使用`POST /portfolio/manual`创建投资组合：  
→ 显示创建的投资组合及其持仓情况。  

### 用户分析投资组合风险  
“我的投资组合有哪些风险？” → `GET /portfolios/list`找到投资组合；  
- 使用`POST /risk/calculate-var`进行风险计算；  
- 显示VaR、CVaR、波动率及各股票的风险贡献；  
- 如有必要，提供优化建议。  

### 用户请求卡尔玛比率优化  
“根据卡尔玛比率优化投资组合” → 获取`snapshot_id`；  
- 使用`POST /portfolio/{snapshot_id}/optimize-calmar`进行优化；  
- 如果历史数据不足，提示需要200天以上的交易数据，并建议使用风险均衡优化；  
- 显示优化结果（卡尔玛比率、CAGR、最大回撤）；  
- 提供重新平衡计划并请求确认。  

### 用户请求蒙特卡洛模拟  
“运行1年的蒙特卡洛模拟” → `POST /risk/monte-carlo`；  
- 设置参数：模拟路径数量、预测期限；  
- 显示模拟结果。  

### 用户请求压力测试  
“对我的投资组合进行压力测试” → 获取可用危机情景；  
- 选择危机情景后进行模拟；  
- 显示模拟结果。  

### 用户查询历史投资组合的风险  
“计算一个月前的投资组合风险” → `GET /portfolio/history?days=45`；  
- 选择相应的快照；  
- 使用`PATCH /portfolio/active-snapshot`设置活动快照；  
- 使用`POST /risk/calculate-var`进行计算；  
- 显示结果。  

### 用户尝试混合不同货币的投资组合  
“将Apple股票添加到我的RUB投资组合” → 发现股票代码不兼容（例如AAPL在NASDAQ市场）；  
- 提示只能使用相同货币的投资组合。  

### 用户比较两个投资组合  
“我的投资组合发生了哪些变化？” → 获取两个投资组合的快照；  
- 比较两个投资组合的持仓变化；  
- 显示变化情况和总价值差异。  

### 用户删除投资组合  
“删除我的测试投资组合” → 确认后删除投资组合；  
- 提示删除操作将永久删除所有相关快照；  
- 显示删除的快照数量。  

### 用户断开经纪商连接  
“断开Tinkoff连接” → 确认后删除连接；  
- 提示删除操作将删除Tinkoff账户的连接记录；  
- 显示是否继续；  
- 提示重新连接需要使用移动应用程序。