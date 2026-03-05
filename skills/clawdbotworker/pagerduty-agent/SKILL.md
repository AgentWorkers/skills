---
name: pagerduty-agent
description: "您可以直接从您的代理（agent）中管理PagerDuty事件、值班排班、服务以及维护窗口（maintenance windows）。"
version: 1.0.0
emoji: "🚨"
homepage: https://github.com/openclaw/skills
metadata:
  openclaw:
    requires:
      env:
        - PAGERDUTY_API_KEY
      bins:
        - node
      anyBins: []
    primaryEnv: PAGERDUTY_API_KEY
    always: false
    tags:
      - pagerduty
      - incidents
      - oncall
      - devops
      - observability
      - alerting
---
# PagerDuty Agent

> ⚠️ 本技能属于非官方社区开发，与PagerDuty, Inc. 无关联，也未获得其官方认可。

该技能可用于触发、确认和解决PagerDuty事件，查看当前值班人员信息，以及管理维护窗口状态，并检查服务运行状况——所有这些操作都无需离开您的工作流程。

## 设置

1. 生成一个PagerDuty API密钥：**进入PagerDuty → Integrations → API Access Keys → Create New API Key**

2. 导出所需的环境变量：

```bash
export PAGERDUTY_API_KEY="your-v2-api-key"
export PAGERDUTY_FROM_EMAIL="you@yourcompany.com"   # required for write operations
```

> `PAGERDUTY_FROM_EMAIL` 必须是您账户中有效PagerDuty用户的邮箱地址。所有POST/PUT请求都需要使用此邮箱地址。

## 使用方法

所有命令都是通过将 `{ command, params }` 形式的JSON对象传递给 `node pagerduty.js` 脚本来执行的。该技能会将处理结果以结构化JSON格式输出到标准输出（stdout）。

```bash
echo '{"command":"list_incidents","params":{"status":"triggered"}}' | node pagerduty.js
```

---

## 命令

### 事件管理

---

#### `trigger_incident`  
创建一个新的事件。

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `service_id` | 字符串 | ✓ | PagerDuty服务ID（例如：“P1ABCDE”） |  
| `title` | 字符串 | ✓ | 事件标题/摘要 |  
| `severity` | 字符串 | | 紧急程度（`critical`、`error`、`warning`、`info`） |  
| `body` | 字符串 | | 详细描述或运行手册相关内容 |  

**示例**  
```json
{
  "command": "trigger_incident",
  "params": {
    "service_id": "P1ABCDE",
    "title": "Database replication lag > 60s",
    "severity": "critical",
    "body": "Replica db-02 is 90s behind primary. Check pg_stat_replication."
  }
}
```

**响应**  
```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "triggered",
  "urgency": "high",
  "html_url": "https://your-subdomain.pagerduty.com/incidents/Q2W3E4R",
  "created_at": "2026-03-04T12:00:00Z",
  "service": { "id": "P1ABCDE", "name": "Production Database" }
}
```

---

#### `acknowledge_incident`  
确认事件，表示正在处理中。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `incident_id` | 字符串 | ✓ | PagerDuty事件ID |  

**示例**  
```json
{ "command": "acknowledge_incident", "params": { "incident_id": "Q2W3E4R" } }
```

**响应**  
```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "acknowledged",
  "acknowledged_at": "2026-03-04T12:03:00Z"
}
```

---

#### `resolve_incident`  
将事件标记为已解决。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
| `incident_id` | 字符串 | ✓ | PagerDuty事件ID |  

**示例**  
```json
{ "command": "resolve_incident", "params": { "incident_id": "Q2W3E4R" } }
```

**响应**  
```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "resolved",
  "resolved_at": "2026-03-04T12:45:00Z"
}
```

---

#### `list_incidents`  
列出所有事件，可按状态进行筛选。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `status` | 字符串 | | 状态（`triggered`、`acknowledged`、`resolved`） |  
| `limit` | 数字 | | 最大返回结果数量（默认为25） |  

**示例**  
```json
{
  "command": "list_incidents",
  "params": { "status": "triggered", "limit": 10 }
}
```

**响应**  
```json
{
  "total": 3,
  "limit": 10,
  "incidents": [
    {
      "id": "Q2W3E4R",
      "incident_number": 1042,
      "title": "Database replication lag > 60s",
      "status": "triggered",
      "urgency": "high",
      "created_at": "2026-03-04T12:00:00Z",
      "service": { "id": "P1ABCDE", "name": "Production Database" },
      "assigned_to": ["Alice Smith"]
    }
  ]
}
```

---

#### `get_incident`  
获取单个事件的详细信息。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `incident_id` | 字符串 | ✓ | PagerDuty事件ID |  

**示例**  
```json
{ "command": "get_incident", "params": { "incident_id": "Q2W3E4R" } }
```

**响应**  
```json
{
  "id": "Q2W3E4R",
  "incident_number": 1042,
  "title": "Database replication lag > 60s",
  "status": "acknowledged",
  "urgency": "high",
  "html_url": "https://your-subdomain.pagerduty.com/incidents/Q2W3E4R",
  "created_at": "2026-03-04T12:00:00Z",
  "last_status_change_at": "2026-03-04T12:03:00Z",
  "service": { "id": "P1ABCDE", "name": "Production Database" },
  "assigned_to": ["Alice Smith"],
  "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" },
  "body": "Replica db-02 is 90s behind primary. Check pg_stat_replication."
}
```

---

#### `add_incident_note`  
在事件的时间线上添加带时间戳的备注。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `incident_id` | 字符串 | ✓ | PagerDuty事件ID |  
| `content` | 字符串 | ✓ | 备注内容（支持Markdown格式） |  

**示例**  
```json
{
  "command": "add_incident_note",
  "params": {
    "incident_id": "Q2W3E4R",
    "content": "Root cause identified: checkpoint completion time spiked to 95%. Increased max_wal_size and restarting standby."
  }
}
```

**响应**  
```json
{
  "id": "NOTE123",
  "content": "Root cause identified...",
  "created_at": "2026-03-04T12:20:00Z",
  "user": "Alice Smith"
}
```

---

### 值班人员与排班管理

---

#### `get_oncall`  
列出当前值班的人员，可按排班计划进行筛选。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `schedule_id` | 字符串 | | 过滤条件：特定排班计划ID |  

**示例**  
```json
{ "command": "get_oncall", "params": { "schedule_id": "SCHED01" } }
```

**响应**  
```json
{
  "oncalls": [
    {
      "user": { "id": "UABC123", "name": "Alice Smith" },
      "schedule": { "id": "SCHED01", "name": "Primary On-Call" },
      "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" },
      "escalation_level": 1,
      "start": "2026-03-04T08:00:00Z",
      "end": "2026-03-11T08:00:00Z"
    }
  ]
}
```

---

#### `list_schedules`  
返回账户中的所有排班计划。  

**参数** — 无 |  
**示例**  
```json
{ "command": "list_schedules", "params": {} }
```

**响应**  
```json
{
  "total": 2,
  "schedules": [
    {
      "id": "SCHED01",
      "name": "Primary On-Call",
      "description": "Weekly rotation — eng team",
      "time_zone": "America/New_York",
      "html_url": "https://your-subdomain.pagerduty.com/schedules/SCHED01",
      "users": [
        { "id": "UABC123", "name": "Alice Smith" },
        { "id": "UDEF456", "name": "Bob Jones" }
      ]
    }
  ]
}
```

---

### 服务管理

---

#### `list_services`  
列出所有PagerDuty服务。  

**参数** — 无 |  
**示例**  
```json
{ "command": "list_services", "params": {} }
```

**响应**  
```json
{
  "total": 3,
  "services": [
    {
      "id": "P1ABCDE",
      "name": "Production Database",
      "description": "RDS Postgres cluster",
      "status": "active",
      "html_url": "https://your-subdomain.pagerduty.com/services/P1ABCDE",
      "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" }
    }
  ]
}
```

---

#### `get_service`  
获取单个服务的详细信息（包括其关联的集成组件）。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `service_id` | 字符串 | ✓ | PagerDuty服务ID |  

**示例**  
```json
{ "command": "get_service", "params": { "service_id": "P1ABCDE" } }
```

**响应**  
```json
{
  "id": "P1ABCDE",
  "name": "Production Database",
  "description": "RDS Postgres cluster",
  "status": "active",
  "html_url": "https://your-subdomain.pagerduty.com/services/P1ABCDE",
  "created_at": "2024-01-15T09:00:00Z",
  "escalation_policy": { "id": "P9XYZ12", "name": "Eng On-Call" },
  "integrations": [
    { "id": "INT001", "name": "Datadog" }
  ],
  "alert_grouping": "intelligent",
  "alert_grouping_timeout": 300
}
```

---

### 维护管理

---

#### `create_maintenance_window`  
将一个或多个服务设置为维护模式，以屏蔽警报。  

**参数**  
| 字段 | 类型 | 是否必填 | 说明 |  
|---|---|---|---|  
| `service_ids` | 字符串数组 | ✓ | 需要设置为维护状态的服务ID列表 |  
| `start_time` | 字符串 | ✓ | ISO 8601格式的开始时间（例如：“2026-03-04T22:00:00Z”） |  
| `end_time` | 字符串 | ✓ | ISO 8601格式的结束时间 |  
| `description` | 字符串 | | 维护原因 |  

**示例**  
```json
{
  "command": "create_maintenance_window",
  "params": {
    "service_ids": ["P1ABCDE", "P2FGHIJ"],
    "start_time": "2026-03-04T22:00:00Z",
    "end_time": "2026-03-05T00:00:00Z",
    "description": "Scheduled DB migration — expect brief connectivity drops"
  }
}
```

**响应**  
```json
{
  "id": "MW00123",
  "description": "Scheduled DB migration — expect brief connectivity drops",
  "start_time": "2026-03-04T22:00:00Z",
  "end_time": "2026-03-05T00:00:00Z",
  "html_url": "https://your-subdomain.pagerduty.com/maintenance_windows/MW00123",
  "services": [
    { "id": "P1ABCDE", "name": "Production Database" },
    { "id": "P2FGHIJ", "name": "API Gateway" }
  ]
}
```

---

#### `list_maintenance_windows`  
列出所有当前和即将进行的维护窗口。  

**参数** — 无 |  
**示例**  
```json
{ "command": "list_maintenance_windows", "params": {} }
```

**响应**  
```json
{
  "total": 1,
  "maintenance_windows": [
    {
      "id": "MW00123",
      "description": "Scheduled DB migration",
      "start_time": "2026-03-04T22:00:00Z",
      "end_time": "2026-03-05T00:00:00Z",
      "html_url": "https://your-subdomain.pagerduty.com/maintenance_windows/MW00123",
      "services": [
        { "id": "P1ABCDE", "name": "Production Database" }
      ]
    }
  ]
}
```

---

## 错误响应  
所有错误都会返回一个包含 `error` 键的JSON对象：  

```json
{ "error": "PAGERDUTY_API_KEY environment variable is not set" }
{ "error": "params.incident_id is required" }
{ "error": "Incident Not Found" }
```

## 提示  
- 在触发事件之前，请先使用 `list_services` 命令查询服务ID。  
- 在调用 `get_oncall` 命令之前，请使用 `list_schedules` 命令获取排班计划ID。  
- `severity` 的值 `critical` 和 `error` 对应PagerDuty的紧急程度 `urgency: high`；其他值对应 `urgency: low`。  
- `create_maintenance_window` 中的时间格式必须为ISO 8601 UTC字符串。  
- 所有写入操作（触发事件、确认事件、解决事件、添加备注、创建维护窗口）都需要使用 `PAGERDUTY_FROM_EMAIL`。