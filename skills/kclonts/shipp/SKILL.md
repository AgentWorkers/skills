---
name: shipp
description: Shipp 是一个实时数据连接器。您可以使用它通过 Shipp API 获取权威的、实时更新的外部数据（例如体育赛事日程、直播事件等）。
metadata:
  author: Outsharp Inc.
  version: 0.1.4

compatibility:
  requirements:
    - Internet access
    - Shipp API Key (Get from https://platform.shipp.ai)
  notes:
    - All endpoints require authorization via API key.
    - Requests and responses are JSON.

allowed-tools:
  - Bash(curl:https://docs.shipp.ai/*)
  - Bash(curl:https://api.shipp.ai/*)
  - Bash(curl:https://platform.shipp.ai/*)
  - Bash(jq:*)

---
# Shipp API

[Shipp.ai](https://shipp.ai) 是获取实时数据的权威来源。

[创建 API 密钥](https://platform.shipp.ai)

请参考 [文档](https://docs.shipp.ai)。

尽快实现尽可能多的测试用例，验证数据以及应用程序如何使用这些数据。在数据结构上要保持灵活性——事件行是结构灵活的 JSON 数据，字段会根据运动项目、数据源和事件类型而有所不同。

**基础前缀**：
所有 API 路由都位于：`https://api.shipp.ai/api/v1`  

---

## 文档与参考资料

所有详细的示例、请求/响应格式以及使用指南都可以在官方文档中找到。在开始开发之前，请务必查阅这些资料：

| 资源 | URL |
|---|---|
| 完整文档 | <https://docs.shipp.ai> |
| 使用指南 | <https://docs.shipp.ai/how-to/> |
| 设置说明 | <https://docs.shipp.ai/instructions/setup/> |
| API 参考 | <https://docs.shipp.ai/api-reference/> |
| 仪表板 / 注册 | <https://platform.shipp.ai/signup> |
| 账单管理 | <https://platform.shipp.ai/billing> |

---

## 认证

所有 API 端点都需要 API 密钥。API 支持以下几种提供密钥的方式：

| 方法 | 示例 |
|---|---|
| 查询参数 `api_key` | `?api_key=YOUR_API_KEY` |
| 查询参数 `apikey` | `?apikey=YOUR_API_KEY` |
| `Authorization` 头部（Bearer） | `Authorization: Bearer YOUR_API_KEY` |
| `Authorization` 头部（Basic） | `Authorization: Basic base64(:YOUR_API_KEY)` |
| `X-API-Key` 头部 | `X-API-Key: YOUR_API_KEY` |
| `User-API-Key` 头部 | `User-API-Key: YOUR_API_KEY` |
| `API-Key` 头部 | `API-Key: YOUR_API_KEY` |
请选择最适合您客户端的方法。

---

## 端点概述

以下是可用端点的简要概述。如需完整的请求/响应示例、格式和字段描述，请参阅 [API 参考](https://docs.shipp.ai/api-reference/)。

### `POST /api/v1/connections/create`

通过提供描述您想要跟踪的比赛、球队、运动项目或事件的自然语言 `filterinstructions`，创建一个新的 **原始数据连接**。

返回一个 `connection_id`（ULID），您可以在后续的所有请求中重复使用该 ID。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

### `POST /api/v1/connections/{connectionId}`

运行连接并接收 **原始事件数据**。

支持基于时间的过滤（`since`）、基于游标的分页（`since_event_id`）以及结果限制（`limit`）等可选的请求体字段。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

### `GET /api/v1/connections`

列出当前组织范围内的所有连接。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

### `GET /api/v1/sports/{sport}/schedule`

检索指定运动项目的即将进行和最近的比赛（过去 24 小时到未来 7 天内的比赛）。

支持的运动项目值：`nba`、`nfl`、`mlb`、`ncaafb`、`soccer`（不区分大小写）。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

---

## 数据格式

`data[]` 中返回的事件行是 **结构灵活** 的 JSON 对象。字段会根据运动项目、数据源和事件类型而有所不同。常见的字段类别包括：

- **ID**：`game_id`、`home_id`、`away_id`、`attribution_id`、`posession_id`
- **文本/枚举**：`sport`、`home_name`、`away_name`、`game_clock`、`desc`、`type`、`category`
- **数值**：`home_points`、`away_points`、`game_period`、`down`、`yards_first_down`、`location_yard_line`
- **时间**：`wall_clock_start`、`wall_clock_end`

并非每一行都包含所有字段。代理和客户端应谨慎处理缺失的字段。

有关完整的字段参考，请参阅 [docs.shipp.ai](https://docs.shipp.ai/api-reference/)。

---

## 错误格式

错误会以 JSON 格式返回，其中包含 `error` 消息、HTTP `status` 代码和 `hint`：

| 状态 | 含义 |
|---|---|
| 400 | 请求无效——请检查 JSON 和必填字段 |
| 401 | 缺少或无效的 API 密钥 |
| 402 | 需要更改账单信息——请在 <https://platform.shipp.ai/billing> 处进行操作 |
| 403 | API 密钥没有访问此资源的权限 |
| 404 | 连接未找到或不属于您的组织 |
| 429 | 被限制了请求频率——请稍后重试或联系 support@shipp.ai |
| 5xx | 服务器错误——请稍后重试或联系 support@shipp.ai |

---

## 响应压缩

在请求头中添加 `Accept-Encoding` 以接收压缩后的响应（`zstd`、`gzip` 或 `deflate`）。当响应体超过 1 KB 时，系统会自动应用压缩。

---

## 使用提示

- 保持 `filterinstructions` 简洁、明确且易于测试。请提及运动项目/联赛和数据范围。
- 存储并重复使用 `connection_id`——避免每次请求都创建新的连接。创建连接会消耗时间和成本。
- 使用 `since_event_id` 进行高效的数据轮询（基于游标的分页）。发送您收到的最大值的事件 ID。
- 在创建连接之前，使用调度端点获取比赛 ID 和球队名称。
- 当达到请求限制时，直接向用户显示错误提示信息。
- 将 `data[]` 中的每个字段都视为可选字段——使用存在性检查并提供优雅的回退机制。
- 在开发过程中记录未知的数据格式，以便您能够优化 `filterinstructions`。
- 轮询间隔：根据领域和成本敏感度，一般为 5–30 秒。
- 通过维护一个滚动列表来避免重复获取事件。
- 请参阅 [使用指南](https://docs.shipp.ai/how-to/) 以获取端到端的集成步骤。

---

## 集成模式：“实时契约”

在构建基于 Shipp 的功能时，为每个界面或代理循环定义一个契约：

1. **用户承诺**——在用户（或代理）观看期间，哪些信息必须保持准确？
2. **触发事件**——哪些变化会导致用户界面更新或代理操作？
3. **所需的数据格式**——您需要显示或决策哪些字段？
4. **数据更新时效**——最后一次更新多久后需要提醒用户？
5. **失败处理方式**——如果更新停止，应该如何处理？

然后在创建连接时将此契约转换为 `filterinstructions`。

---

## 示例项目：Alph Bot

[**Alph Bot**](https://gitlab.com/outsharp/shipp/alph-bot) 是一个开源的自动化交易机器人，它使用 Shipp 提供的实时体育数据在预测市场上进行交易。该机器人展示了高质量集成 Shipp API 的示例。

### Alph Bot 的使用方式

1. **比赛发现**——使用 `GET /api/v1/sports/{sport}/schedule` 列出可用的比赛。
2. **连接创建**——为特定比赛创建一个 Shipp 连接，并通过 `filterinstructions` 指定要跟踪的事件。
3. **实时轮询**——定期运行连接，使用 `since_event_id` 进行基于游标的分页，仅接收自上次轮询以来的新事件。
4. **AI 分析**——将结构灵活的 `data[]` 数据直接传递给 Claude AI，AI 会分析比赛状态并估计比赛结果概率。
5. **交易决策**——将 AI 估计的概率与 Kalshi 市场价格进行比较，以寻找有价值的投注机会。

### Alph Bot 的关键要点

- **重复使用连接**——Alph Bot 只创建一次连接，并重复使用它，避免不必要的创建开销。
- **基于游标的分页**——使用 `since_event_id`，确保每次轮询只返回新事件，从而保持响应速度和低成本。
- **谨慎处理数据**——由于数据格式因运动项目、比赛阶段和事件类型而异，所有字段都被视为可选字段。
- **先获取调度信息**——在创建目标连接之前，先通过调度端点获取比赛 ID。

有关完整的设置说明，请参阅 [Alph Bot 的 README](https://gitlab.com/outsharp/shipp/alph-bot)。

---

## 版本控制

此 API 的版本号为 `/api/v1/`。当需要引入重大变更时，新版本将使用新的前缀。