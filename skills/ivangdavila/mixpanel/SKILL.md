---
name: Mixpanel
slug: mixpanel
version: 1.0.1
homepage: https://clawic.com/skills/mixpanel
description: 通过 REST API，您可以查询 Mixpanel 的分析数据，包括用户转化路径（funnels）、用户留存率（retention）、用户细分（segmentation）以及事件跟踪（event tracking）等详细信息。
changelog: Improved security docs and env var declarations.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["curl","jq"],"env":["MP_SERVICE_ACCOUNT","MP_SERVICE_SECRET","MP_PROJECT_ID"],"config":["~/mixpanel/"]},"primaryEnv":"MP_SERVICE_SECRET","os":["linux","darwin"]}}
---
## 设置

首次使用本技能时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

当用户需要 Mixpanel 的产品分析功能时，该技能可发挥作用。代理程序负责处理事件查询、渠道分析、用户留存分析、用户细分以及用户资料查询等任务。

## 架构

数据存储在 `~/mixpanel/` 目录下。具体存储结构请参考 `memory-template.md`。

```
~/mixpanel/
├── memory.md        # Projects, saved queries, insights
└── queries/         # Saved JQL queries
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 数据存储结构 | `memory-template.md` |

## 核心规则

### 1. 认证
需要使用 Mixpanel 的服务账户：

```bash
export MP_SERVICE_ACCOUNT="your-service-account"
export MP_SERVICE_SECRET="your-service-secret"
export MP_PROJECT_ID="123456"
```

在 Mixpanel 的“组织设置”（Organization Settings）中创建服务账户。

### 2. 使用查询 API 进行分析
使用查询 API（Query API）来获取数据洞察、分析渠道转化情况以及用户留存情况：

```bash
BASE="https://mixpanel.com/api/query"
AUTH=$(echo -n "$MP_SERVICE_ACCOUNT:$MP_SERVICE_SECRET" | base64)

# Insights query (event counts)
curl -s "$BASE/insights?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "event": ["Sign Up", "Purchase"],
      "type": "general",
      "unit": "day",
      "from_date": "2024-01-01",
      "to_date": "2024-01-31"
    }
  }' | jq
```

### 3. 渠道分析
```bash
curl -s "$BASE/funnels?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "events": [
        {"event": "Sign Up"},
        {"event": "Complete Onboarding"},
        {"event": "First Purchase"}
      ],
      "from_date": "2024-01-01",
      "to_date": "2024-01-31",
      "unit": "day"
    }
  }' | jq '.data.meta.overall'
```

### 4. 用户留存分析
```bash
curl -s "$BASE/retention?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "born_event": "Sign Up",
      "event": "App Open",
      "from_date": "2024-01-01",
      "to_date": "2024-01-31",
      "unit": "week",
      "retention_type": "birth"
    }
  }' | jq
```

### 5. 用户资料查询
```bash
curl -s "https://mixpanel.com/api/query/engage?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "filter_by_cohort": {"id": 12345},
    "output_properties": ["$email", "$name", "plan"]
  }' | jq
```

### 6. 导出原始事件数据
```bash
curl -s "https://data.mixpanel.com/api/2.0/export?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -d "from_date=2024-01-01" \
  -d "to_date=2024-01-07" \
  -d "event=[\"Purchase\"]"
```

### 7. 使用 JQL 进行复杂查询
```javascript
// Mixpanel JQL (JavaScript Query Language)
function main() {
  return Events({
    from_date: "2024-01-01",
    to_date: "2024-01-31",
    event_selectors: [{event: "Purchase"}]
  })
  .groupByUser(["properties.$city"], mixpanel.reducer.sum("properties.amount"))
  .groupBy(["key.$city"], mixpanel.reducer.avg("value"))
  .sortDesc("value")
  .take(10);
}
```

## 常见查询

| 目标 | API 端点 | 关键参数 |
|------|----------|------------|
| 事件数量 | `/insights` | event, type, unit, dates |
| 转化渠道分析 | `/funnels` | events array, dates |
| 用户留存分析 | `/retention` | born_event, event, unit |
| 用户细分 | `/engage` | filter_by_cohort, properties |
| 导出原始事件数据 | `/export` | dates, event filter |

## 注意事项

- **日期格式**：请使用 `YYYY-MM-DD`，而非时间戳。
- **项目 ID**：所有查询 API 请求都必须提供项目 ID。
- **请求限制**：免费账户每小时最多 60 次请求；建议批量处理查询。
- **JQL 超时**：超过 60 秒的查询会失败，可使用 `.take(N)` 来限制返回结果数量。

## 外部接口

| API 端点 | 发送的数据 | 用途 |
|----------|-----------|---------|
| `mixpanel.com/api/query/*` | 认证信息、项目 ID、查询参数 | 分析数据查询 |
| `data.mixpanel.com/api/2.0/*` | 认证信息、项目 ID、时间范围 | 原始数据导出 |

**其他数据不会被发送到外部。**

## 安全性与隐私

**发送到 Mixpanel 的数据（通过 HTTPS）：**
- 服务账户认证信息
- 查询参数（事件名称、时间范围、过滤条件）
- 项目 ID

**本地存储的数据：**
- 认证信息仅存储在环境变量中
- 查询结果缓存于 `~/mixpanel/` 目录下

**本技能不会：**
- 将认证信息存储在 `memory.md` 或任何文件中
- 将数据发送到除 `mixpanel.com` 以外的其他服务
- 修改用户的 Mixpanel 跟踪代码或 SDK

## 信任声明

使用本技能意味着会从 Mixpanel 获取分析数据。请确保您信任 Mixpanel 并愿意将其用于产品数据分析。

## 相关技能

如果用户同意，可以使用以下命令安装相关技能：
- `clawhub install <slug>`：安装多平台分析工具 `analytics`
- `clawhub install data-analysis`：安装数据处理工具
- `clawhub install api`：安装 REST API 相关工具

## 反馈

- 如果本技能对您有帮助，请给它打星（`clawhub star mixpanel`）
- 保持更新：使用 `clawhub sync` 命令获取最新信息