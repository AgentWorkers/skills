---
name: outlit-mcp
description: >
  **使用说明：**  
  当通过 MCP 工具（outlit_*）查询 Outlit 客户数据时，请使用此功能。该功能适用于以下场景：客户分析、收入指标监控、活动时间线追踪、客户群体分析、流失风险评估、针对分析数据的 SQL 查询，以及任何 Outlit 数据探索任务。
---
# Outlit MCP 服务器

通过 6 个 MCP 工具查询客户智能数据，这些工具涵盖了客户和用户信息、收入指标、活动时间线以及原始 SQL 分析功能。

## 快速入门

| 所需功能 | 对应工具 |
|---------------|------|
| 浏览/筛选客户 | `outlit_list_customers` |
| 浏览/筛选用户 | `outlit_list_users` |
| 单个客户详细信息 | `outlit_get_customer` |
| 客户活动历史记录 | `outlit_get_timeline` |
| 自定义分析/聚合 | `outlit_query`（SQL） |
| 查看表格和列 | `outlit_schema` |

**在编写 SQL 之前：**务必先调用 `outlit_schema` 以获取可用的表格和列信息。

### 常见用法

**查找高风险客户：**
```json
{
  "tool": "outlit_list_customers",
  "billingStatus": "PAYING",
  "noActivityInLast": "30d",
  "orderBy": "mrr_cents",
  "orderDirection": "desc"
}
```

**收入明细（SQL）：**
```json
{
  "tool": "outlit_query",
  "sql": "SELECT billing_status, count(*) as customers, sum(mrr_cents)/100 as mrr_dollars FROM customer_dimensions GROUP BY 1 ORDER BY 3 DESC"
}
```

---

## MCP 设置

### 获取 API 密钥

在 Outlit 仪表板（[app.outlit.ai](https://app.outlit.ai)）中，选择 **设置 > MCP 集成**。

### 自动检测设置

根据当前环境运行相应的设置命令：

1. **检查是否在 Claude Code 中运行** — 如果在 Claude Code 中运行（检查 `claude` CLI 是否可用），请运行：
   ```bash
   claude mcp add outlit https://mcp.outlit.ai/mcp -- --header "Authorization: Bearer API_KEY"
   ```

2. **检查项目中是否存在 `.cursor/mcp.json` 文件** — 如果存在，请将其添加到该文件中：
   ```json
   {
     "mcpServers": {
       "outlit": {
         "url": "https://mcp.outlit.ai/mcp",
         "headers": { "Authorization": "Bearer API_KEY" }
       }
     }
   }
   ```

3. **检查是否存在 Claude Desktop** — 如果在 macOS 的 `~/Library/Application Support/Claude/` 或 Windows 的 `%APPDATA%/Claude/` 目录下存在 `claude_desktop_config.json` 文件，请将其添加到该文件中：
   ```json
   {
     "mcpServers": {
       "outlit": {
         "url": "https://mcp.outlit.ai/mcp",
         "headers": { "Authorization": "Bearer API_KEY" }
       }
     }
   }
   ```

如果用户未提供 API 密钥，请向用户索取。请将 `API_KEY` 替换为实际的密钥。

### 验证连接

调用 `outlit_schema` 以确认连接是否正常工作。

---

## 工具参考

### `outlit_list_customers`

用于筛选和分页显示客户信息。

| 关键参数 | 参数值 |
|------------|--------|
| `billingStatus` | NONE, TRIALING, PAYING, CHURNED |
| `hasActivityInLast` / `noActivityInLast` | 7d, 14d, 30d, 90d（互斥） |
| `mrrAbove` / `mrrBelow` | 金额单位为分（10000 分 = 100 美元） |
| `search` | 客户名称或域名 |
| `orderBy` | 最后活动时间、首次访问时间、客户名称、收入金额（mrr_cents） |
| `limit` | 1-1000（默认：20） |
| `cursor` | 分页令牌 |

### `outlit_list_users`

用于筛选和分页显示用户信息。

| 关键参数 | 参数值 |
|------------|--------|
| `journeyStage` | DISCOVERED, SIGNED_UP, ACTIVATED, ENGAGED, INACTIVE |
| `customerId` | 按客户 ID 过滤 |
| `hasActivityInLast` / `noActivityInLast` | 活动时间范围（例如：7 天、24 小时）（互斥） |
| `search` | 电子邮件或名称 |
| `orderBy` | 最后活动时间、首次访问时间、电子邮件 |
| `limit` | 1-1000（默认：20） |
| `cursor` | 分页令牌 |

### `outlit_get_customer`

用于获取单个客户的详细信息。支持输入客户 ID、域名或名称。

| 关键参数 | 参数值 |
|------------|--------|
| `customer` | 客户 ID、域名或名称（必填） |
| `include` | `users`, `revenue`, `recentTimeline`, `behaviorMetrics` |
| `timeframe` | 7d, 14d, 30d, 90d（默认：30d） |

仅请求所需的字段——省略不需要的字段可以加快响应速度。

### `outlit_get_timeline`

用于查看客户的活动时间线。

| 关键参数 | 参数值 |
|------------|--------|
| `customer` | 客户 ID 或域名（必填） |
| `channels` | SDK, EMAIL, SLACK, CALL, CRM, BILLING, SUPPORT, INTERNAL |
| `eventTypes` | 按特定事件类型过滤 |
| `timeframe` | 7d, 14d, 30d, 90d, all（默认：30d） |
| `startDate` / `endDate` | ISO 8601 格式的时间范围（与 `timeframe` 参数互斥） |
| `limit` | 1-1000（默认：50） |
| `cursor` | 分页令牌 |

### `outlit_query`

用于对 ClickHouse 分析表执行原始 SQL 查询。**仅支持 SELECT 语句。**请参阅 [SQL 参考文档](references/sql-reference.md) 了解 ClickHouse 的语法和安全模型。

| 关键参数 | 参数值 |
|------------|--------|
| `sql` | SQL SELECT 查询语句（必填） |
| `limit` | 1-10000（默认：1000） |

可用表格：`events`, `customer_dimensions`, `user_dimensions`, `mrr_snapshots`。

### `outlit_schema`

用于查看所有表格及其列信息。无需参数即可调用；如需查看特定表格，可使用 `table: "events"`。在编写 SQL 之前务必先调用此函数。

---

## 数据模型

**计费状态：** NONE → TRIALING → PAYING → CHURNED

**客户状态：** DISCOVERED → SIGNED_UP → ACTIVATED → ENGAGED → INACTIVE

**数据格式：**
- 货币值以分为单位（100 分等于 1 美元）
- 时间戳采用 ISO 8601 格式
- ID 前缀为 `cust_`, `contact_`, `evt_`

**分页：**所有列表接口均使用基于游标的分页机制。在请求更多页面之前，请检查 `pagination.hasMore`。使用 `pagination.nextCursor` 作为 `cursor` 参数来获取下一页数据。

---

## 最佳实践

1. **在编写 SQL 之前先调用 `outlit_schema`** — 了解可用的列信息，避免猜测。
2. **使用专用工具进行单次查询** — 不要使用 SQL 来查询单个客户。
3. **在数据源处进行过滤** — 使用工具提供的参数和 WHERE 子句进行过滤，避免在获取数据后进行过滤操作。
4. **仅请求所需的字段** — 省略不需要的字段以加快响应速度。
5. **在 SQL 查询中添加时间过滤条件** — 使用 `WHERE occurred_at >= now() - INTERVAL N DAY`。
6. **将金额转换为美元** — 在显示前将分转换为美元。
7. **在 SQL 中使用 LIMIT 语句** — 限制结果集的大小，避免传输大量数据。

## 已知限制

1. **SQL 操作仅支持读取** — 不支持 INSERT、UPDATE、DELETE 操作。
2. **数据隔离** — 无法查询其他组织的数据。
3. **时间线查询需要指定客户** — 无法跨所有客户查询时间线数据。
4. **MRR 过滤操作在数据获取后进行** — 在处理大量数据时，`outlit_list_customers` 的性能可能会受到影响。
5. **事件查询需要时间过滤条件** — 未指定时间范围的查询会扫描所有数据。
6. **使用 ClickHouse 的语法** — 与 MySQL/PostgreSQL 的语法不同（请参阅 [SQL 参考文档](references/sql-reference.md)。

---

## 工具使用注意事项

| 工具 | 注意事项 |
|------|--------|
| `outlit_list_customers` | `hasActivityInLast` 和 `noActivityInLast` 是互斥的 |
| `outlit_list_customers` | `search` 仅支持搜索客户名称或域名 |
| `outlit_get_customer` | `behaviorMetrics` 的数据可能因时间范围不同而为空，请根据需要扩展查询内容 |
| `outlit_get_timeline` | `timeframe` 和 `startDate`/`endDate` 是互斥的 |
| `outlit_query` | 使用 ClickHouse 的日期格式：`now() - INTERVAL 30 DAY`，而非 `DATE_SUB()` |
| `outlit_query` | `properties` 列的数据类型为 JSON，请使用 `JSONExtractString(properties, 'key')` 进行提取 |

---

## 参考资料

| 参考文档 | 阅读说明 |
|-----------|--------------|
| [SQL 参考文档](references/sql-reference.md) | ClickHouse 语法、安全模型、查询模式 |
| [工作流程](references/workflows.md) | 多步骤分析：客户流失风险分析、收入报表、账户健康状况检查 |