---
name: datafast-analytics
description: 通过 DataFast API 快速查询网站分析数据和访客信息，包括各项指标、时间序列数据、实时统计数据、访客详细信息以及目标/支付管理相关的数据。
metadata: {"openclaw":{"homepage":"https://datafa.st"}}
---
# DataFast Analytics 技能

使用此技能可以调用 DataFast API 并为用户汇总结果。

## 快速工作流程

1. 确认请求类型（概览、时间序列、实时数据、详细数据、访问者信息、目标/支付信息的创建/删除）。
2. 收集所需的输入参数：
   - 日期范围：`startAt` 和 `endAt`（可以同时提供，也可以不提供；概览和时间序列类型支持日期范围）。
   - `timezone`、`fields`、`interval`、`limit`、`offset` 以及任何 `filter_*` 参数。
3. 使用 `Authorization: Bearer $DATAFAST_API_KEY` 和 `Content-Type: application/json` 构建 HTTP 请求。
4. 通过 `curl` 执行请求并解析返回的 JSON 数据。
5. 将结果以表格形式呈现，并附上简短的说明（包括总计和关键信息）。如果需要分页，还需提供分页信息。

## 设置

1. 从 DataFast 获取您的 API 密钥（密钥以 `df_` 开头）。
2. 将 API 密钥存储在安全的地方：
```bash
mkdir -p ~/.config/datafast
echo "df_your_key_here" > ~/.config/datafast/api_key
```

## 认证

所有请求都需要进行身份验证：
```bash
DATAFAST_API_KEY=$(cat ~/.config/datafast/api_key)
curl ... \
  -H "Authorization: Bearer $DATAFAST_API_KEY" \
  -H "Content-Type: application/json"
```

如果用户尚未设置 API 密钥，请让他们按照上述步骤进行设置。

## 基础 URL

`https://datafa.st/api/v1/`

## 参考文档

请参阅 `{baseDir}/references/datafast-api-docs.md` 以获取端点详情、响应字段和示例代码。

## 端点指南

### 概览
- `GET /analytics/overview`
  - 可选参数：`startAt`、`endAt`、`timezone`、`fields`。

### 时间序列
- `GET /analytics/timeseries`
  - 常用参数：`fields`、`interval`（小时/天/周/月）、`startAt`、`endAt`、`timezone`、`limit`、`offset`。
  - 支持使用 `filter_*` 参数进行数据筛选。
  - **注意：** `fields` 参数是必填项（例如：`fields=visitors,sessions`）。

### 实时数据
- `GET /analytics/realtime`
- `GET /analytics/realtime/map`

### 详细数据
- `GET /analytics/devices`
- `GET /analytics/pages`
- `GET /analytics/campaigns`
- `GET /analytics/goals`
- `GET /analytics/referrers`
- `GET /analytics/countries`
- `GET /analytics/regions`
- `GET /analytics/cities`
- `GET /analytics/browsers`
- `GET /analytics/operating-systems`
- `GET /analytics/hostnames`

### 访问者信息
- `GET /visitors/{datafast_visitor_id}`

### 目标管理
- 创建目标：`POST /goals`
- 删除目标：`DELETE /goals`（需要至少提供一个筛选条件或日期范围；请确认删除范围）

### 支付管理
- 创建支付记录：`POST /payments`
- 删除支付记录：`DELETE /payments`（请确认删除范围）

## 破坏性操作（注意：这些操作会永久删除数据）

对于 `DELETE /goals` 或 `DELETE /payments` 操作：
- 在执行前务必用明确的文字确认筛选条件和日期范围。
- 如果用户请求删除所有数据，请要求用户再次确认。
- 提供最终要调用的 URL（不包括 API 密钥）。

## 过滤语法

使用 `filter_*` 参数进行数据筛选（例如：`filter_referrer=is:X`）。

**重要提示：** 过滤值必须与详细数据端点的名称完全匹配。例如，“X/Twitter” 应该被存储为 “X”，而不是 “x.com” 或 “twitter.com”。如有疑问，请先查询详细数据信息：
```bash
curl ... "/analytics/referrers?limit=20"
```
然后使用实际的 `referrer` 值进行过滤。

## 示例命令模式

### GET 请求
```bash
DATAFAST_API_KEY=$(cat ~/.config/datafast/api_key)
curl -sS "https://datafa.st/api/v1/analytics/overview?startAt=2024-01-01&endAt=2024-01-31&timezone=UTC" \
  -H "Authorization: Bearer $DATAFAST_API_KEY" \
  -H "Content-Type: application/json"
```

### POST 请求
```bash
DATAFAST_API_KEY=$(cat ~/.config/datafast/api_key)
curl -sS "https://datafa.st/api/v1/goals" \
  -H "Authorization: Bearer $DATAFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"datafast_visitor_id":"...","name":"newsletter_signup","metadata":{"email":"..."}}'
```

### DELETE 请求
```bash
DATAFAST_API_KEY=$(cat ~/.config/datafast/api_key)
curl -sS -X DELETE "https://datafa.st/api/v1/goals?name=signup&startAt=2023-01-01T00:00:00Z&endAt=2023-01-31T23:59:59Z" \
  -H "Authorization: Bearer $DATAFAST_API_KEY"
```

## 输出格式

- 提供结果的简要总结和扁平化的表格。
- 如果有相关数据，包括总计和转化/收入指标。
- 对于时间序列数据，需显示选定范围内的总计值以及第一个/最后一个时间戳。
- 如果存在分页功能，需报告 `limit`、`offset` 和 `total` 值，并询问用户是否需要查看下一页。