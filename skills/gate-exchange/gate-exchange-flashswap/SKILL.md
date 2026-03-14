---
name: gate-exchange-flashswap
version: "2026.3.11-5"
updated: "2026-03-11"
description: >
  **Gate Flash Swap 查询技能**  
  该技能用于查询支持的货币对、验证闪汇（flash swap）限额、查看交易历史记录以及追踪特定交易。无论您需要查询闪汇货币对、检查闪汇限额、查看闪汇交易历史记录，还是查找特定的闪汇交易，都可以使用此技能。  
  **触发短语示例**：  
  - “flash swap pairs”（闪汇货币对）  
  - “flash swap orders”（闪汇交易）  
  - “flash swap limits”（闪汇限额）  
  - “query flash swap”（查询闪汇信息）  
  - “check swap amount”（检查闪汇金额）  
  - 任何与闪汇查询相关的请求。
---
# 门极闪速兑换查询（Gate Flash Swap Query）

## 通用规则
在继续之前，请阅读并遵守共享的运行时规则：
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

---

查询与门极闪速兑换相关的信息，包括支持的货币对列表、兑换金额限制、订单历史记录以及单个订单的详细信息。

## 触发条件
当用户的请求符合以下任何一种情况时，将激活此技能：
- 提到“闪速兑换”（flash swap），并伴随对货币对、限制、订单或历史记录的查询
- 询问哪些货币支持闪速兑换或即时兑换
- 询问最低/最高兑换金额或限制
- 请求查看闪速兑换订单历史记录或特定订单的详细信息
- 使用关键词：“闪速兑换”（flash swap）、“即时兑换”（instant swap）、“快速兑换”（quick exchange）、“兑换对”（swap pairs）、“兑换限制”（swap limits）

## 快速入门
常见的查询示例：
1. **列出支持的货币对**：“显示所有支持闪速兑换的货币对”
2. **检查兑换限制**：“我想将 BTC 兑换成 USDT，最低和最高金额是多少？”
3. **查看订单历史记录**：“显示我最近的闪速兑换订单”

## 领域知识
**闪速兑换**（Flash Swap）是由 Gate 提供的一种快速加密货币兑换服务。用户可以立即将一种加密货币兑换成另一种加密货币，而无需下订单并等待匹配。

**关键概念**：
- **货币对**（Currency Pair）：支持闪速兑换的兑换组合，例如 BTC_USDT 表示 BTC 和 USDT 之间的兑换
- **卖出货币**（Sell Currency）：用户支付的货币
- **买入货币**（Buy Currency）：用户收到的货币
- **最低卖出金额**（Sell Min/Max Amount）：单次兑换中允许卖出的最低和最高数量
- **最低买入金额**（Buy Min/Max Amount）：单次兑换中允许买入的最低和最高数量
- **订单状态**（Order Status）：`1` = 成功，`2` = 失败

**API 响应字段名称映射**：
API 返回驼峰式（camelCase）字段名称。提取数据时，请将其映射到以下对应字段：
| API 响应字段 | SKILL.md 字段 | 描述 |
|--------------------|----------------|-------------|
| `sellMinAmount` | sell_min_amount | 最低卖出数量 |
| `sellMaxAmount` | sell_max_amount | 最高卖出数量 |
| `buyMinAmount` | buy_min_amount | 最低买入数量 |
| `buyMaxAmount` | buy_max_amount | 最高买入数量 |
| `sellCurrency` | sell_currency | 卖出货币符号 |
| `buyCurrency` | buy_currency | 买入货币符号 |
| `sellAmount` | sell_amount | 实际卖出金额 |
| `buyAmount` | buy_amount | 实际买入金额 |
| `createTime` | create_time | 订单创建时间戳 |

**数据类型说明**：`order_id` 在 API 响应中以 **字符串**（string）形式返回，而不是整数。在从结果中提取时，请始终将其视为字符串。

## 工作流程
### 第一步：识别用户意图
分析用户的请求，以确定要执行哪种闪速兑换查询。

**意图分类**：
| 用户意图 | 操作 | 工具 |
|-------------|--------|------|
| 查询所有支持的闪速兑换货币对 / 检查哪些货币可以兑换 | 列出所有货币对 | `cex_fc_list_fc_currency_pairs` |
| 检查特定货币是否支持闪速兑换 / 检查最低/最高兑换限制 | 根据货币过滤货币对 | `cex_fc_list_fc_currency_pairs` |
| 查询闪速兑换订单列表 / 查看兑换历史记录 / 检查订单状态 | 列出订单 | `cex_fc_list_fc_orders` |
| 根据 ID 查询特定闪速兑换订单 / 跟踪订单详细信息 | 获取单个订单 | `cex_fc_get_fc_order` |

**需要提取的关键数据**：
- `intent`：`list_pairs` / `check_limits` / `list_orders` / `get_order`
- `parameters`：用户提到的任何过滤条件（货币、状态、订单 ID 等）

### 第二步：查询所有闪速兑换货币对（如果意图 = list_pairs）
调用 `cex_fc_list_fc_currency_pairs`，无需传入参数。

**注意**：此查询可能返回 34,000 多行结果。不要将整个列表直接显示给用户。相反：
1. 总结可用货币对的总数
2. 显示前 20 个货币对作为示例
3. 询问用户是否希望根据特定货币进行过滤以获得更精确的结果

**需要提取的关键数据**：
- `currency_pairs`：所有支持的闪速兑换交易货币对列表
- `sell_currency`：可卖出的货币
- `buy_currency`：可买入的货币
- 可用货币对的总数

### 第三步：验证货币支持情况并检查兑换限制（如果意图 = check_limits）
如果用户没有指定货币，请提示他们提供货币后再继续。可以推荐一些常见的货币（例如 BTC、ETH、USDT）作为示例。

调用 `cex_fc_list_fc_currency_pairs`，传入参数 `currency`（必需）：
- `currency`：要检查的货币符号，例如 "BTC"、"USDT"

**需要提取的关键数据**：
- `currency_pairs`：包含指定货币的货币对列表
- `sell_min_amount`：每次兑换的最低卖出数量
- `sell_max_amount`：每次兑换的最高卖出数量
- `buy_min_amount`：每次兑换的最低买入数量
- `buy_max_amount`：每次兑换的最高买入数量

如果返回的列表为空，说明指定的货币不支持闪速兑换。

### 第四步：查询闪速兑换订单历史记录（如果意图 = list_orders）
在调用 API 之前，验证提供的 `status` 参数。有效的值只有 `1`（成功）和 `2`（失败）。如果用户提供了其他值，告知他们状态参数只接受 `1` 或 `2`，然后不要调用 API。

调用 `cex_fc_list_fc_orders`，传入参数：
- `status`（可选，整数）：订单状态过滤器，`1` = 成功，`2` = 失败。调用前必须验证此参数——只接受 `1` 或 `2`
- `sell_currency`（可选，字符串）：按卖出货币过滤
- `buy_currency`（可选，字符串）：按买入货币过滤
- `limit`（可选，整数）：每页显示的记录数
- `page`（可选，整数）：页码

**需要提取的关键数据**：
- `orders`：闪速兑换订单列表
- `order_id`（字符串）：订单标识符
- `sell_currency` / `buy_currency`：涉及的货币
- `sell_amount` / `buy_amount`：交易金额
- `price`：兑换汇率
- `status`：订单状态（1=成功，2=失败）
- `create_time`：订单创建时间

### 第五步：查询单个闪速兑换订单的详细信息（如果意图 = get_order）
调用 `cex_fc_get_fc_order`，传入参数 `order_id`（必需）：
- `order_id`（字符串）：要查询的订单 ID

如果 API 返回 404 错误，说明该订单不存在。告知用户指定的订单 ID 未找到，并建议用户验证订单 ID 或先查询订单列表。

**需要提取的关键数据**：
- `order_id`（字符串）：订单标识符
- `sell_currency` / `buy_currency`：涉及的货币
- `sell_amount` / `buy_amount`：交易金额
- `price`：兑换汇率
- `status`：订单状态
- `create_time`：订单创建时间

### 第六步：格式化并呈现结果
根据用户的意图，使用适当的报告模板格式化查询结果并呈现给用户。

**需要提取的关键数据**：
- 根据查询类型生成的格式化报告

## 错误处理
| 错误情况 | 处理方式 |
|----------------|----------|
| MCP 服务连接失败 | 提示用户检查网络连接或 VPN 状态，建议稍后重试 |
| 未提供订单 ID | 提示用户提供订单 ID，或引导他们先使用订单列表查询 |
| 查询结果为空 | 明确告知用户未找到数据，建议调整过滤条件 |
| 货币不支持闪速兑换 | 告知用户指定的货币不支持闪速兑换 |
| 未指定用于检查限制的货币 | 提示用户在查询限制前指定货币（例如 BTC、ETH、USDT） |
| 状态值无效 | 状态参数只接受 `1`（成功）或 `2`（失败）。在调用 API 之前拒绝其他值，并告知用户有效选项 |
| 订单未找到（404） | 指定的 `order_id` 不存在。告知用户并建议验证订单 ID 或先查询订单列表 |
| 结果集过大（34,000 多行） | 不要显示整个列表。总结总数，显示 20 个货币对的示例，并建议按货币过滤 |
| 参数格式无效 | 提示用户正确的参数格式 |

## 安全规则
- 该技能仅执行查询操作；不执行任何订单放置或资金更改
- 不得在输出中暴露用户的 API 密钥、Secret 或其他敏感信息
- 查询结果中的金额应保持原样显示，不得修改

## 判断逻辑总结
| 条件 | 操作 | 工具 |
|-----------|--------|------|
| 用户询问支持哪些闪速兑换货币对 | 查询所有货币对 | `cex_fc_list_fc_currency_pairs` |
| 用户询问特定货币是否可以兑换 | 根据货币过滤货币对 | `cex_fc_list_fc_currency_pairs` |
| 用户询问最低/最高兑换金额或限制（指定了货币） | 根据货币过滤货币对并提取限制 | `cex_fc_list_fc_currency_pairs` |
| 用户询问兑换限制但未指定货币 | 提示用户先指定货币再继续 | — |
| 用户查询闪速兑换订单历史记录 | 查询订单列表 | `cex_fc_list_fc_orders` |
| 用户提供的状态值无效（非 1 或 2） | 拒绝请求并告知状态参数只接受 1 或 2 | — |
| 用户按状态/货币过滤订单 | 根据条件查询订单列表 | `cex_fc_list_fc_orders` |
| 用户根据 ID 查询特定订单 | 获取单个订单 | `cex_fc_get_fc_order` |
| API 返回 404 错误 | 告知用户订单不存在，建议验证订单 ID | — |
| 返回的货币对列表超过 34,000 行 | 总结数量，显示 20 个货币对的示例，并建议按货币过滤 | — |
| 查询订单详细信息时缺少 order_id | 提示用户提供 order_id | — |

## 报告模板
**时间戳格式**：以下所有 `{timestamp}` 占位符使用 ISO 8601 格式：`YYYY-MM-DD HH:mm:ss UTC`（例如 `2026-03-11 14:30:00 UTC`）。生成报告时使用当前时间。

### 闪速兑换货币对报告（Flash Swap Currency Pairs Report）
```markdown
## Gate Flash Swap Supported Pairs

**Query Time**: {timestamp}
**Filter**: {currency filter or "None"}

| Pair | Sell Currency | Buy Currency |
|------|---------------|--------------|
| {pair} | {sell_currency} | {buy_currency} |

Total: {total} pairs.
```

### 闪速兑换货币限制报告（Flash Swap Currency Limit Report）
```markdown
## Gate Flash Swap Limit Check

**Query Time**: {timestamp}
**Currency**: {currency}

| Pair | Sell Currency | Sell Min | Sell Max | Buy Currency | Buy Min | Buy Max |
|------|---------------|----------|----------|--------------|---------|---------|
| {pair} | {sell_currency} | {sell_min_amount} | {sell_max_amount} | {buy_currency} | {buy_min_amount} | {buy_max_amount} |

Total: {total} pairs available for {currency}.
```

### 闪速兑换订单列表报告（Flash Swap Order List Report）
```markdown
## Gate Flash Swap Order List

**Query Time**: {timestamp}
**Filters**: Status={status}, Sell Currency={sell_currency}, Buy Currency={buy_currency}

| Order ID | Sell | Sell Amount | Buy | Buy Amount | Status | Created At |
|----------|------|-------------|-----|------------|--------|------------|
| {order_id} | {sell_currency} | {sell_amount} | {buy_currency} | {buy_amount} | {status_text} | {create_time} |

Total: {total} records.
```

### 闪速兑换订单详细信息报告（Flash Swap Order Detail Report）
```markdown
## Gate Flash Swap Order Details

**Query Time**: {timestamp}

| Field | Value |
|-------|-------|
| Order ID | {order_id} |
| Sell Currency | {sell_currency} |
| Sell Amount | {sell_amount} |
| Buy Currency | {buy_currency} |
| Buy Amount | {buy_amount} |
| Exchange Rate | {price} |
| Order Status | {status_text} |
| Created At | {create_time} |
```