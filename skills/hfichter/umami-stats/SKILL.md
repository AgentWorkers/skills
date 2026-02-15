---
name: umami-stats
description: 通过环境提供的 API 密钥，使用 API 查询 Umami Cloud (v2) 的分析数据。当代理需要网站流量、页面信息、事件数据、会话记录、实时数据、报告或归因数据来进行分析、规划、实验或监控时，可以使用此功能。内容包括只读 API 查询模式、端点选择指南，以及可用于灵活请求不同端点和时间范围的可重用脚本。
---

# Umami 统计数据（只读 API 功能）

您可以将此功能用作数据访问层：获取 Umami 的分析数据，然后由代理决定后续的分析或策略。

## 所需的环境变量

- `UMAMI_API_KEY`（必需）
- `UMAMI_BASE_URL`（可选，默认值：`https://api.umami.is`）
- `UMAMI_WEBSITE_ID`（可选，默认网站）
- `UMAMI_DEPLOYMENT`（可选：`cloud` 或 `self-hosted`，默认值：`cloud`）

## API 路径规范

- **Umami Cloud：** `https://api.umami.is/v1/...`
- **自托管 Umami：** `https://<your-host>/api/...`

该脚本支持以下两种部署模式：
- `--deployment cloud` → 使用云服务模式（路径格式：`/v1/...` + `x-umami-api-key`）
- `--deployment self-hosted` → 使用自托管模式（路径格式：`/api/...` + `Authorization: Bearer ...`）

## 只读工作流程

1. 从文档或 `references/read-endpoints.md` 中选择相应的 API 端点。
2. 使用 `scripts/umami_query.py` 脚本，传入 API 端点和参数。
3. 可以使用预设参数（如 `today`、`last7d` 等），或自定义 `startAt`/`endAt` 来指定时间范围。
4. 分析返回的 JSON 数据以完成用户任务。

## 快速命令示例

```bash
# 1) List websites
python3 scripts/umami_query.py --endpoint /v1/websites

# 2) Website stats for last 7 days (default website from env)
python3 scripts/umami_query.py \
  --endpoint /v1/websites/{websiteId}/stats \
  --preset last7d

# 3) Top pages with explicit website id
python3 scripts/umami_query.py \
  --endpoint /v1/websites/{websiteId}/pageviews \
  --website-id "$UMAMI_WEBSITE_ID" \
  --preset last30d

# 4) Events series with custom window
python3 scripts/umami_query.py \
  --endpoint /v1/websites/{websiteId}/events/series \
  --param startAt=1738368000000 \
  --param endAt=1738972799000

# 5) Legacy path auto-mapping in cloud mode (/api/... -> /v1/...)
python3 scripts/umami_query.py --endpoint /api/websites/{websiteId}/stats --preset last7d

# 6) Self-hosted example (/v1/... auto-maps to /api/...)
python3 scripts/umami_query.py \
  --deployment self-hosted \
  --base-url "https://umami.example.com" \
  --endpoint /v1/websites/{websiteId}/stats \
  --preset last7d
```

## 常见的查询示例

- “本周的流量情况如何？”
- “过去 30 天内的热门页面”
- “显示注册点击事件的趋势”
- “比较本周和上周的数据”
- “提供原始的 Umami 数据以制定营销计划”

## 注意事项

- 所有请求均为只读操作（使用 `GET` 方法）。
- 为确保结果的可重复性，请指定明确的时间范围。
- 对于未知的 API 端点，请先查阅 `https://v2.umami.is/docs/api`，然后再使用脚本进行查询。
- 在云服务模式下，建议使用 `/v1/...` 的路径格式；在自托管模式下，使用 `/api/...` 的路径格式。
- 认证头的格式因部署模式而异：云服务模式使用 `x-umami-api-key`，自托管模式使用 `Authorization: Bearer ...`。
- 对于 `metrics` 类型的 API 端点，需要提供 `type` 参数；如果该参数被省略，脚本会自动设置为 `type=url`。
- 对于 `/v1/reports/*` 端点，如果提供了 `--website-id` 或 `UMAMI_WEBSITE_ID`，脚本会自动添加相应的网站 ID。
- 在 Umami Cloud 上，使用普通用户 API 密钥访问 `/v1/users/*` 端点时可能会收到 403 错误（这是许多账户的常见情况）。

## 相关资源

- API 端点映射：`references/read-endpoints.md`
- 查询辅助工具：`scripts/umami_query.py`