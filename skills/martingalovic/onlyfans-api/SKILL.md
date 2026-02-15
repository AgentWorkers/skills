---
name: onlyfansapi-skill
description: >-
  Query OnlyFans data and analytics via the OnlyFansAPI.com platform. Get revenue
  summaries across all models, identify top-performing models, analyze
  Free Trial and Tracking Link conversion rates, compare link earnings, and much more!
  Use when users ask about anything related to OnlyFans.
compatibility: Requires curl, jq, and network access to app.onlyfansapi.com
metadata:
  author: OnlyFansAPI.com
  version: "1.0"
allowed-tools: Bash(curl:*) Bash(jq:*) Read
---

# OnlyFans API 技能

该技能用于查询 OnlyFansAPI.com 平台，以获取关于 OnlyFans 代理机构分析的数据，包括收入、模型表现以及链接转化指标等信息。

## 前提条件

用户必须设置环境变量 `ONLYFANSAPI_API_KEY`，并使用从 <https://app.onlyfansapi.com/api-keys> 获取的 API 密钥。如果未设置该密钥，请提醒用户：

```
Export your OnlyFansAPI key:
  export ONLYFANSAPI_API_KEY="your_api_key_here"
```

## API 基础信息

- **基础 URL：** `https://app.onlyfansapi.com`
- **认证头：** `Authorization: Bearer $ONLYFANSAPI_API_KEY`
- 所有日期均使用 URL 编码格式：`YYYY-MM-DD HH:MM:SS`
- 如果未指定具体时间，使用当天开始或结束的时间（对于日期范围）
- 分页：使用 `limit` 和 `offset` 查询参数。可以通过响应中的 `hasMore` 或 `_pagination.next_page` 来判断是否还有更多数据。
- 尽可能使用 `User-Agent`，其值为 `OnlyFansAPI-Skill`
- 尽量从端点的示例响应中推断数据结构。例如，`data.total.total` 表示收入的总金额。

## 工作流程

### 1. 获取过去 N 天内所有模型的收入

**步骤：**

1. **列出所有关联的账户：**

   ```bash
   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/accounts" | jq .
   ```

   每个账户对象包含 `"id"`（例如 `"acct_xxx"`）、`onlyfans_username` 和 `"display_name"`。

2. **获取每个账户的收入：**

   ```bash
   START=$(date -u -v-7d '+%Y-%m-%d+00%%3A00%%3A00')  # macOS
   # Linux: START=$(date -u -d '7 days ago' '+%Y-%m-%d+00%%3A00%%3A00')
   END=$(date -u '+%Y-%m-%d+23%%3A59%%3A59')

   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/{account_id}/statistics/statements/earnings?start_date=$START&end_date=$END&type=total" | jq .
   ```

   响应字段：
   - `data.total` — 净收入
   - `data.gross` — 总收入
   - `data.chartAmount` — 每日收入明细数组
   - `data.delta` — 与上一期的收入变化百分比

3. **汇总数据：** 显示每个模型的显示名称、用户名、净收入和总收入，并计算总和。

### 2. 哪个模型的表现最好

使用上述流程，按照 `data.total`（净收入）降序排列模型。收入最高的模型表现最佳。

（可选）还可以获取更详细的统计信息，例如订阅者数量、访问者统计以及帖子/消息的收入明细。

### 3. 哪个免费试用链接的转化率最高（订阅者 → 消费者）

1. **列出所有免费试用链接：**

   ```bash
   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/{account_id}/trial-links?limit=100&offset=0&sort=desc&field=subscribe_counts&synchronous=true" | jq .
   ```

   每个链接的关键响应字段：
   - `id`、`trialLinkName`、`url`
   - `claimCounts` — 提取试用权限的订阅者总数
   - `clicksCounts` — 点击次数
   - `revenue.total` — 该链接带来的总收入
   - `revenue.spendersCount` — 支付费用的订阅者数量
   - `revenue.revenuePerSubscriber` — 每位订阅者的平均收入

2. **计算转化率：**

   ```
   conversion_rate = spendersCount / claimCounts
   ```

   按转化率降序排列链接。

3. **以表格形式展示结果：** 包括链接名称、领取试用权限的订阅者数量、实际付费的订阅者数量、转化率以及总收入。

### 4. 哪个跟踪链接的转化率最高

1. **列出所有跟踪链接：**

   ```bash
   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/{account_id}/tracking-links?limit=100&offset=0&sort=desc&sortby=claims&synchronous=true" | jq .
   ```

   每个链接的关键响应字段：
   - `id`、`campaignName`、`campaignUrl`
   - `subscribersCount` — 通过该链接获得的订阅者总数
   - `clicksCount` — 点击次数
   - `revenue.total` — 总收入
   - `revenue.spendersCount` — 支付费用的订阅者数量
   - `revenue.revenuePerSubscriber` — 每位订阅者的平均收入
   - `revenue.revenuePerClick` — 每次点击的平均收入

2. **计算转化率：**

   ```
   conversion_rate = revenue.spendersCount / subscribersCount
   ```

3. **以表格形式展示结果：** 包括活动名称、订阅者数量、实际付费的订阅者数量、转化率以及总收入。

### 5. 哪个免费试用链接/跟踪链接带来的收入最高

使用上述相同的接口获取数据，按照 `revenue.total` 降序排列，展示收入最高的链接及其类型（免费试用/跟踪链接）、总收入以及订阅者/付费订阅者数量。

## 多账户（代理机构）查询

对于涉及所有模型的代理机构级查询，请始终执行以下步骤：

1. 首先通过 `GET /api/accounts` 获取所有账户信息。
2. 遍历每个账户并收集相关数据。
3. 对数据进行汇总，并以每个模型的明细形式展示结果。

## 收入类型过滤

在查询 `GET /api/{account}/statistics/statements/earnings` 时，`type` 参数可用于过滤收入类型：
- `total` — 所有收入总和
- `subscribes` — 订阅收入
- `tips` — 收到的小费
- `post` — 付费帖子收入
- `messages` — 付费消息收入
- `stream` — 流媒体收入

## 如有疑问

如果您不确定某个端点、参数、响应格式或如何使用 OnlyFans API 完成特定任务，请查阅官方文档 <https://docs.onlyfansapi.com>。该网站提供了所有可用端点的完整参考信息、指南和示例。在尝试之前，请务必先查看文档。

## 错误处理

- 如果未设置 `ONLYFANSAPI_API_KEY`，请停止操作并提示用户进行配置。
- 如果 API 调用返回非 200 状态码的响应，请显示错误信息和 HTTP 状态码。
- 如果 `_meta._rate_limits_remaining_minute` 或 `remaining_day` 为 0，请提醒用户注意使用率限制。
- 如果账户的 `"isAuthenticated"` 为 `false`，则表示需要重新认证。

## 输出格式

- 始终使用 markdown 表格格式展示数据，以便于阅读。
- 货币值保留两位小数。
- 在显示百分比（转化率、变化百分比）时，格式化为 `XX.X%`。
- 对于多模型汇总数据，应在表格底部添加一个 **总计** 行。