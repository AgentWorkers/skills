---
name: posthog
description: 通过 PostHog 的 REST API 与其进行分析交互。可以捕获事件、评估功能开关（feature flags）、使用 HogQL 查询数据、管理用户信息、查看洞察报告（insights）、管理仪表板（dashboards）、执行实验（experiments）、处理调查数据（surveys）、管理用户分组（cohorts）、添加注释（annotations）以及查看会话记录（session recordings）。当用户提到 “PostHog”、“PostHog API”、“PostHog 事件”、“PostHog 功能开关”、“PostHog 洞察报告”、“PostHog 查询”、“HogQL”、“PostHog 用户信息”、“PostHog 仪表板”、“PostHog 实验”、“PostHog 调查数据”、“PostHog 用户分组”、“PostHog 会话记录” 或 “PostHog 分析” 时，可以使用此功能。
metadata:
  env:
    - POSTHOG_API_KEY (required): "Personal API key — create at https://us.posthog.com/settings/user-api-keys"
    - POSTHOG_PROJECT_ID (required): "Project ID — find at https://us.posthog.com/settings/project#variables"
    - POSTHOG_PROJECT_API_KEY: "Project API key (for public capture/flags endpoints)"
    - POSTHOG_HOST: "API host (default: https://us.posthog.com)"
    - POSTHOG_INGEST_HOST: "Ingest host (default: https://us.i.posthog.com)"
---
# PostHog API 技能

通过 PostHog 的 REST API 与其进行交互。PostHog 提供两种类型的 API 端点：

- **公共端点**（仅支持 POST 请求，需要使用项目 API 密钥）：用于捕获事件、评估功能标志（无请求速率限制）。
- **私有端点**（需要使用个人 API 密钥）：支持查询操作以及对所有资源的创建、读取、更新和删除（CRUD）操作，但存在请求速率限制。

## 设置

1. 获取个人 API 密钥：[https://us.posthog.com/settings/user-api-keys](https://us.posthog.com/settings/user-api-keys)
2. 获取项目 ID：[https://us.posthog.com/settings/project#variables](https://us.posthog.com/settings/project#variables)
3. 设置环境变量：
   ```bash
   export POSTHOG_API_KEY="phx_..."
   export POSTHOG_PROJECT_ID="12345"
   export POSTHOG_PROJECT_API_KEY="phc_..."  # optional, for capture/flags
   # For EU Cloud:
   # export POSTHOG_HOST="https://eu.posthog.com"
   # export POSTHOG_INGEST_HOST="https://eu.i.posthog.com"
   ```
4. 验证 API 密钥的有效性：运行 `bash scripts/posthog.sh whoami`

## 辅助脚本

`scripts/posthog.sh` 脚本用于封装常见的 PostHog 操作。运行 `bash scripts/posthog.sh help` 可以查看完整的脚本用法。

### 示例

```bash
# Capture an event
bash scripts/posthog.sh capture "signup" "user_123" '{"plan":"pro"}'

# Evaluate feature flags
bash scripts/posthog.sh evaluate-flags "user_123"

# HogQL query — top events last 7 days
bash scripts/posthog.sh query "SELECT event, count() FROM events WHERE timestamp >= now() - INTERVAL 7 DAY GROUP BY event ORDER BY count() DESC LIMIT 20"

# List persons
bash scripts/posthog.sh list-persons 10 | jq '.results[] | {name, distinct_ids}'

# List feature flags
bash scripts/posthog.sh list-flags | jq '.results[] | {id, key, active}'

# Create a feature flag
echo '{"key":"new-dashboard","name":"New Dashboard","active":true,"filters":{"groups":[{"rollout_percentage":50}]}}' | \
  bash scripts/posthog.sh create-flag

# List dashboards
bash scripts/posthog.sh list-dashboards | jq '.results[] | {id, name}'
```

## 关键概念

### 两种 API 类型
- **公共端点**（`/i/v0/e/`, `/batch/`, `/flags`）：在请求体中包含项目 API 密钥，无需添加认证头，且无请求速率限制。
- **私有端点**（`/api/projects/:project_id/...`）：需要通过 `Authorization: Bearer` 指令携带个人 API 密钥，存在请求速率限制。

### HogQL 查询
查询端点（`POST /api/projects/:project_id/query/`）是提取数据的最强大工具，支持使用类似 SQL 的 HogQL 语法来操作 `events`、`persons`、`sessions`、`groups` 等数据表，以及数据仓库中的表。

在查询时务必指定时间范围，并使用 `LIMIT` 限制返回的数据量。对于大量数据导出，建议使用基于时间戳的分页方式。

### 请求速率限制（私有端点）
| 类型 | 限制 |
|------|-------|
| 分析数据（insights, persons, recordings） | 每分钟 240 次请求，每小时 1200 次请求 |
| 查询端点 | 每小时 2400 次请求 |
| 功能标志的本地评估 | 每分钟 600 次请求 |
| 其他 CRUD 操作 | 每分钟 480 次请求，每小时 4800 次请求 |

这些速率限制是针对整个组织而言的。如果达到请求限制，系统会自动暂停请求并提示用户重试。

### 域名
| 地区 | 公共端点 | 私有端点 |
|-------|--------|---------|
| 美国 | `us.i.posthog.com` | `us.posthog.com` |
| 欧洲 | `eu.i.posthog.com` | `eu.posthog.com` |

### 事件 API（已弃用）
`/api/projects/:project_id/events/` 端点已被弃用，建议使用 HogQL 查询或批量导出数据。

## 直接使用 curl 进行请求

```bash
# Private endpoint
curl -H "Authorization: Bearer $POSTHOG_API_KEY" \
  "$POSTHOG_HOST/api/projects/$POSTHOG_PROJECT_ID/feature_flags/"

# HogQL query
curl -H "Authorization: Bearer $POSTHOG_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST -d '{"query":{"kind":"HogQLQuery","query":"SELECT count() FROM events WHERE timestamp >= now() - INTERVAL 1 DAY"}}' \
  "$POSTHOG_HOST/api/projects/$POSTHOG_PROJECT_ID/query/"

# Capture event (public)
curl -H "Content-Type: application/json" \
  -X POST -d '{"api_key":"'$POSTHOG_PROJECT_API_KEY'","event":"test","distinct_id":"u1"}' \
  "$POSTHOG_INGEST_HOST/i/v0/e/"
```

## 完整的 API 参考文档

请参阅 [references/api-endpoints.md](references/api-endpoints.md)，以获取完整的 API 端点列表，包括参数、请求体格式、请求范围和响应格式等信息。

文档内容涵盖以下部分：
- 公共端点（事件捕获、批量处理、功能标志操作）
- 私有端点（用户信息、功能标志管理、数据分析、仪表盘、注释、用户群体分析、实验设计、调查问卷、操作记录、会话数据、用户信息、自定义字段定义）
- 查询 API（使用 HogQL 进行数据查询）