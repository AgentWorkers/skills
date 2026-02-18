---
name: servicenow
emoji: 🔧
description: "将您的 AI 代理连接到 ServiceNow —— 使用 Table API 和 Stats API 在任何表中查询、创建、更新和管理记录。支持完整的 CRUD 操作（创建、读取、更新、删除），以及聚合分析（COUNT/AVG/MIN/MAX/SUM）、模式查询（schema introspection）和附件管理功能。该解决方案专为 ITSM（IT 服务管理）、ITOM（IT 运维管理）和 CMDB（配置管理数据库）工作流程设计，适用于处理事件（incidents）、变更（changes）、问题（problems）、配置项（configuration items）、知识文章（knowledge articles）等数据。"
author: "OnlyFlows (onlyflowstech)"
homepage: "https://onlyflows.tech"
license: MIT
tags:
  - servicenow
  - itsm
  - itom
  - cmdb
  - snow
  - table-api
  - incidents
  - changes
  - problems
  - configuration-items
  - knowledge-base
  - service-management
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["curl", "jq"], "env": ["SN_INSTANCE", "SN_USER", "SN_PASSWORD"] }
      }
  }
---
# ServiceNow 技能

通过 REST Table API 查询和管理任何 ServiceNow 实例中的记录。

## 设置

为你的 ServiceNow 实例设置环境变量：

```bash
export SN_INSTANCE="https://yourinstance.service-now.com"
export SN_USER="your_username"
export SN_PASSWORD="your_password"
```

以下所有工具都会使用 `scripts/sn.sh` 脚本，该脚本会读取这些环境变量。

## 工具

### sn_query — 查询任意表格

```bash
bash scripts/sn.sh query <table> [options]
```

选项：
- `--query "<encoded_query>"` — ServiceNow 编码查询（例如：`active=true^priority=1`）
- `--fields "<field1,field2>"` — 需要返回的字段（用逗号分隔）
- `--limit <n>` — 最大记录数（默认为 20）
- `--offset <n>` — 分页偏移量
- `--orderby "<field>"` — 排序字段（以 `-` 为前缀表示降序）
- `--display <true|false|all>` — 显示值模式

示例：

```bash
# List open P1 incidents
bash scripts/sn.sh query incident --query "active=true^priority=1" --fields "number,short_description,state,assigned_to" --limit 10

# All users in IT department
bash scripts/sn.sh query sys_user --query "department=IT" --fields "user_name,email,name"

# Recent change requests
bash scripts/sn.sh query change_request --query "sys_created_on>=2024-01-01" --orderby "-sys_created_on" --limit 5
```

### sn_get — 通过 sys_id 获取单条记录

```bash
bash scripts/sn.sh get <table> <sys_id> [options]
```

选项：
- `--fields "<field1,field2>"` — 需要返回的字段
- `--display <true|false|all>` — 显示值模式

示例：

```bash
bash scripts/sn.sh get incident abc123def456 --fields "number,short_description,state,assigned_to" --display true
```

### sn_create — 创建一条记录

```bash
bash scripts/sn.sh create <table> '<json_fields>'
```

示例：

```bash
bash scripts/sn.sh create incident '{"short_description":"Server down","urgency":"1","impact":"1","assignment_group":"Service Desk"}'
```

### sn_update — 更新一条记录

```bash
bash scripts/sn.sh update <table> <sys_id> '<json_fields>'
```

示例：

```bash
bash scripts/sn.sh update incident abc123def456 '{"state":"6","close_code":"Solved (Permanently)","close_notes":"Restarted service"}'
```

### sn_delete — 删除一条记录

```bash
bash scripts/sn.sh delete <table> <sys_id> --confirm
```

必须使用 `--confirm` 选项以防止意外删除。

### sn_aggregate — 聚合查询

```bash
bash scripts/sn.sh aggregate <table> --type <TYPE> [options]
```

聚合类型：`COUNT`、`AVG`、`MIN`、`MAX`、`SUM`

选项：
- `--type <TYPE>` — 聚合类型（必选）
- `--query "<encoded_query>"` — 过滤记录
- `--field "<field>"` — 聚合字段（对于 AVG/MIN/MAX/SUM 是必选的）
- `--group-by "<field>"` — 按字段分组结果
- `--display <true|false|all>` — 显示值模式

示例：

```bash
# Count open incidents by priority
bash scripts/sn.sh aggregate incident --type COUNT --query "active=true" --group-by "priority"

# Average reassignment count
bash scripts/sn.sh aggregate incident --type AVG --field "reassignment_count" --query "active=true"
```

### sn_schema — 获取表格结构

```bash
bash scripts/sn.sh schema <table> [--fields-only]
```

返回字段名称、类型、最大长度、必填标志、引用目标以及可选值。

使用 `--fields-only` 可以获取简化的字段列表。

### sn_batch — 批量更新或删除记录

```bash
bash scripts/sn.sh batch <table> --query "<encoded_query>" --action <update|delete> [--fields '{"field":"value"}'] [--limit 200] [--confirm]
```

对符合查询条件的所有记录执行批量更新或删除操作。默认以 **干运行模式** 运行——仅显示匹配的记录数量而不进行实际操作。传递 `--confirm` 选项即可执行操作。

选项：
- `--query "<encoded_query>"` — 需要操作的记录过滤条件（必选）
- `--action <update|delete>` — 执行的操作（必选）
- `--fields '<json>'` — 每条记录要设置的 JSON 字段（更新操作时必选）
- `--limit <n>` — 每次操作影响的最大记录数（默认为 200，上限为 10000）
- `--dry-run` — 仅显示匹配记录数量，不进行任何操作（默认行为）
- `--confirm` — 真正执行操作（禁用干运行模式）

示例：

```bash
# Dry run: see how many resolved incidents older than 90 days would be affected
bash scripts/sn.sh batch incident --query "state=6^sys_updated_on<javascript:gs.daysAgo(90)" --action update

# Bulk close resolved incidents (actually execute)
bash scripts/sn.sh batch incident --query "state=6^sys_updated_on<javascript:gs.daysAgo(90)" --action update --fields '{"state":"7","close_code":"Solved (Permanently)","close_notes":"Auto-closed by batch"}' --confirm

# Dry run: count orphaned test records
bash scripts/sn.sh batch u_test_table --query "u_status=abandoned" --action delete

# Delete orphaned records (actually execute)
bash scripts/sn.sh batch u_test_table --query "u_status=abandoned" --action delete --limit 50 --confirm
```

输出（JSON 总结）：
```json
{"action":"update","table":"incident","matched":47,"processed":47,"failed":0}
```

### sn_health — 实例健康检查

```bash
bash scripts/sn.sh health [--check <all|version|nodes|jobs|semaphores|stats>]
```

从多个维度检查 ServiceNow 实例的健康状况。默认选项是 `--check all`，会执行所有检查。

检查内容：
- **version** — 实例构建版本、创建日期和标签（来自 sys_properties）
- **nodes** — 集群节点状态（在线/离线）（来自 sys_cluster_state）
- **jobs** — 停滞/逾期的计划任务（来自 sys_trigger，状态为 ready，next_action 超过 30 分钟）
- **semaphores** — 活动信号量（潜在的锁）（来自 sysSemaphore）
- **stats** — 快速仪表盘：活跃事件、未解决的问题、待处理的问题

示例：

```bash
# Full health check
bash scripts/sn.sh health

# Just check version
bash scripts/sn.sh health --check version

# Check for stuck jobs
bash scripts/sn.sh health --check jobs

# Quick incident/change/problem dashboard
bash scripts/sn.sh health --check stats
```

输出（JSON）：
```json
{
  "instance": "https://yourinstance.service-now.com",
  "timestamp": "2026-02-16T13:30:00Z",
  "version": {"build": "...", "build_date": "...", "build_tag": "..."},
  "nodes": [{"node_id": "...", "status": "online", "system_id": "..."}],
  "jobs": {"stuck": 0, "overdue": []},
  "semaphores": {"active": 2, "list": []},
  "stats": {"incidents_active": 54, "p1_open": 3, "changes_active": 12, "problems_open": 8}
}
```

### sn_attach — 管理附件

```bash
# List attachments on a record
bash scripts/sn.sh attach list <table> <sys_id>

# Download an attachment
bash scripts/sn.sh attach download <attachment_sys_id> <output_path>

# Upload an attachment
bash scripts/sn.sh attach upload <table> <sys_id> <file_path> [content_type]
```

## 常用表格

| 表格 | 描述 |
|-------|-------------|
| `incident` | 事件 |
| `change_request` | 变更请求 |
| `problem` | 问题 |
| `sc_req_item` | 请求项（RITMs） |
| `sc_request` | 请求 |
| `sys_user` | 用户 |
| `sys_user_group` | 组 |
| `cmdb_ci` | 配置项 |
| `cmdb_ci_server` | 服务器 |
| `kb_knowledge` | 知识库文章 |
| `task` | 任务（事件/变更/问题的父级） |
| `sys_choice` | 选择列表值 |

## 编码查询语法

ServiceNow 编码查询使用 `^` 表示 AND，`^OR` 表示 OR：

- `active=true^priority=1` — 状态为活动且优先级为 1
- `active=true^ORactive=false` — 状态为活动或非活动
- `short_descriptionLIKEserver` — 包含 “server” 字符串
- `sys_created_on>=2024-01-01` — 创建时间在 2024-01-01 之后
- `assigned_toISEMPTY` — 未分配给任何人
- `stateIN1,2,3` — 状态为 1、2 或 3
- `caller_id.name=John Smith` — 通过引用链查找相关记录

## 注意事项

- 所有 API 调用都使用 Basic Auth，认证凭据为 `SN_USER` / `SN_PASSWORD`
- 默认结果限制为 20 条记录；可以使用 `--limit` 选项进行调整
- 使用 `--display true` 可以获取人类可读的字段值，而不是 sys_id
- 脚本会自动检测 `SN_INSTANCE` 是否包含协议前缀