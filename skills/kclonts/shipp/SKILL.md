---
name: shipp
description: Shipp 是一个实时数据连接器。您可以使用它通过 Shipp API 获取权威的、实时更新的外部数据（例如体育赛事日程、实时事件等信息）。
metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
  notes:
    - All endpoints require authorization via API key.
    - Requests and responses are JSON.

allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)

---
# Shipp API

[Shipp.ai](https://shipp.ai) 是获取实时数据的权威来源。

[创建 API 密钥](https://platform.shipp.ai)

请**经常**查阅本文档，并参考 API 及其[文档](https://docs.shipp.ai)。

尽快实现尽可能多的测试用例，验证数据以及应用程序如何使用这些数据。在数据结构上要保持灵活性。

**基础前缀：**
所有 API 路由均位于：`https://api.shipp.ai/api/v1` 下

---

## 文档与参考资料

所有详细的示例、请求/响应模式以及使用指南均可在官方文档中找到。在开发之前，请务必查阅这些资料：

| 资源 | URL |
|---|---|
| 完整文档 | <https://docs.shipp.ai> |
| 使用指南 | <https://docs.shipp.ai/how-to/> |
| 设置说明 | <https://docs.shipp.ai/instructions/setup/> |
| API 参考 | <https://docs.shipp.ai/api-reference/> |
| 仪表盘 / 注册 | <https://platform.shipp.ai/signup> |
| 账单管理 | <https://platform.shipp.ai/billing> |

---

## 认证

所有 API 端点都需要 API 密钥。API 支持多种提供密钥的方式：

| 方法 | 示例 |
|---|---|
| 查询参数 `api_key` | `?api_key=YOUR_API_KEY` |
| 查询参数 `apikey` | `?apikey=YOUR_API_KEY` |
| `Authorization` 标头 (Bearer) | `Authorization: Bearer YOUR_API_KEY` |
| `Authorization` 标头 (Basic) | `Authorization: Basic base64(:YOUR_API_KEY)` |
| `X-API-Key` 标头 | `X-API-Key: YOUR_API_KEY` |
| `User-API-Key` 标头 | `User-API-Key: YOUR_API_KEY` |
| `API-Key` 标头 | `API-Key: YOUR_API_KEY` |

请选择最适合您客户端的方法来传递 API 密钥。

---

## 端点概述

以下是可用端点的简要介绍。如需完整的请求/响应示例、模式及字段描述，请参阅[API 参考](https://docs.shipp.ai/api-reference/)。

### `POST /api/v1/connections/create`

通过提供描述您想要跟踪的游戏、球队、运动项目或事件的自然语言**过滤指令**，创建一个新的**原始数据连接**。

返回一个 `connection_id`（ULID），您可以在后续的所有请求中重复使用该 ID。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

### `POST /api/v1/connections/{connectionId}`

运行连接并接收**原始事件数据**。支持基于时间的过滤（`since`）、基于游标的分页（`since_event_id`）以及结果限制（`limit`）等选项。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

### `GET /api/v1/connections`

列出当前组织范围内的所有连接。

→ [完整文档与示例](https://docs_shipp.ai/api-reference/)

### `GET /api/v1/sports/{sport}/schedule`

检索指定运动项目的即将进行的比赛及最近的比赛（时间范围为过去 24 小时到未来 7 天）。

支持的运动项目名称：`nba`、`nfl`、`mlb`、`ncaafb`、`soccer`（不区分大小写）。

→ [完整文档与示例](https://docs.shipp.ai/api-reference/)

---

## 数据结构

返回的事件数据以 `data[]` 的形式呈现，这些数据是**结构灵活**的 JSON 对象。不同运动项目、数据源和事件类型的字段可能有所不同。常见的字段类别包括：

- **ID：** `game_id`、`home_id`、`away_id`、`attribution_id`、`posession_id`
- **文本/枚举类型：** `sport`、`home_name`、`away_name`、`game_clock`、`desc`、`type`、`category`
- **数值类型：** `home_points`、`away_points`、`game_period`、`down`、`yards_first_down`、`location_yard_line`
- **时间类型：** `wall_clock_start`、`wall_clock_end`

并非每一行数据都包含所有字段。开发人员和客户端应做好处理缺失字段的准备。

完整的字段列表请参阅[docs.shipp.ai](https://docs.shipp.ai/api-reference/)。

---

## 错误格式

错误信息会以 JSON 格式返回，其中包含 `error` 消息、HTTP 状态码以及相应的**提示**：

| 状态码 | 含义 |
|---|---|
| 400 | 请求无效 — 请检查 JSON 格式及必填字段 |
| 401 | API 密钥缺失或无效 |
| 402 | 需要更新账单信息 — 请在 <https://platform.shipp.ai/billing> 处操作 |
| 403 | API 密钥无权限访问该资源 |
| 404 | 连接未找到或不属于您的组织 |
| 429 | 超过请求限制 — 请稍后重试或联系 support@shipp.ai |
| 5xx | 服务器错误 — 请稍后重试或联系 support@shipp.ai |

---

## 响应压缩

在请求头中添加 `Accept-Encoding`，以接收压缩后的响应（支持 `zstd`、`gzip` 或 `deflate` 格式）。当响应体超过 1 KB 时，系统会自动进行压缩。

---

## 使用提示：

- 保持 `filterinstructions` 简洁、明确且易于测试。请注明要跟踪的运动项目/联赛及范围。
- 存储并重复使用 `connection_id`，避免每次请求都创建新的连接。
- 使用 `since_event_id` 进行高效的数据轮询（基于游标的分页）。
- 在创建连接之前，先使用 `schedule` 端点获取比赛 ID 和球队名称。
- 当达到请求限制时，直接向用户显示错误提示信息。
- 可参考[使用指南](https://docs.shipp.ai/how-to/)以获取端到端的集成步骤。

---

## 版本控制

本 API 的版本标识为 `/api/v1/`。当需要引入重大变更时，新版本将使用新的前缀进行区分。