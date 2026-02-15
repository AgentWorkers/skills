---
name: servicenow-agent
description: 仅限读取的 CLI 访问权限，用于 ServiceNow 的表（Table）、附件（Attachment）、聚合数据（Aggregate）以及服务目录（Service Catalog）相关 API；支持模式检查（schema inspection）和历史记录查询（history retrieval，仅限读取操作）。
read_when:
  - Need to read ServiceNow Table API records
  - Need to query a table or fetch a record by sys_id
  - Need to download attachment content or metadata
  - Need aggregate statistics or service catalog variables
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["node"]}}}
---

# ServiceNow 表格 API（仅限读取）

使用此技能通过 Table API 从 ServiceNow 读取数据。请勿创建、更新或删除记录。

## 配置

在当前文件夹中的 `.env` 文件中设置以下环境变量：

- `SERVICENOW_DOMAIN`：实例域名，例如 `myinstance.service-now.com`
- `SERVICENOW_USERNAME`：用于基本身份验证的用户名
- `SERVICENOW_PASSWORD`：用于基本身份验证的密码

如果您的域名已经包含 `https://`，则直接使用该域名。否则，请求应发送到：

```
https://$SERVICENOW_DOMAIN
```

## 允许的操作：仅限 GET 请求

仅使用以下文件中的 GET 端点：

- `openapi.yaml`：用于 Table API
- `references/attachment.yaml`：用于附件 API
- `references/aggregate-api.yaml`：用于聚合 API
- `references/service-catalog-api.yaml`：用于服务目录 API

### 列出记录
- `GET /api/now/table/{tableName}`

### 通过 sys_id 获取记录
- `GET /api/now/table/{tableName}/{sys_id}`

请勿使用 POST、PUT、PATCH 或 DELETE 操作。

## Table API 的常见查询参数

- `sysparm_query`：编码后的查询条件，例如 `active=true^priority=1`
- `sysparm_fields`：以逗号分隔的字段名称，用于返回数据
- `sysparm_limit`：限制返回的记录数量，以减少数据量
- `sysparm_display_value`：设置为 `true`、`false` 或 `all`，以决定是否显示字段值
- `sysparm Exclude_reference_link`：设置为 `true` 可以避免显示引用链接

有关参数的完整列表，请参阅 `openapi.yaml`。

## 命令行界面 (CLI)

使用提供的 CLI 进行所有读取操作。CLI 会从 `.env` 文件中自动获取身份验证信息，您也可以通过命令行参数进行自定义。

### 命令说明

- `list table`：列出指定表格中的所有记录
- `get table sys_id`：根据 sys_id 获取单条记录
- `batch file.json`：一次性执行多个读取请求
- `attach`：读取附件及其内容
- `stats table`：汇总相关统计数据
- `schema table`：列出表格的有效字段名称和类型
- `history table`：根据 sys_id 获取完整的评论和工作日志记录
- `sc`：用于访问服务目录的 GET 端点

### 身份验证参数

- `--domain`：指定实例域名
- `--username`：指定用户名
- `--password`：指定密码

### 查询参数

可以使用以下参数作为 `--sysparm_` 命令行参数：

- `--sysparm_query`
- `--sysparm_fields`
- `--sysparm_limit`
- `--sysparm_display_value`
- `--sysparm Exclude_reference_link`
- `--sysparm_suppress_pagination_header`
- `--sysparm_view`
- `--sysparm_query_category`
- `--sysparm_query_no_domain`
- `--sysparm_no_count`

### 附件 API 参数

- `--sysparm_query`
- `--sysparm_suppress_pagination_header`
- `--sysparm_limit`
- `--sysparm_query_category`

### 聚合 API 参数

- `--sysparm_query`
- `--sysparm_avg_fields`
- `--sysparm_count`
- `--sysparm_min_fields`
- `--sysparm_max_fields`
- `--sysparm_sum_fields`
- `--sysparm_group_by`
- `--sysparm_order_by`
- `--sysparm_having`
- `--sysparm_display_value`
- `--sysparm_query_category`

### 服务目录 API 参数

- `--sysparm_view`
- `--sysparm_limit`
- `--sysparm_text`
- `--sysparm_offset`
- `--sysparm_category`
- `--sysparm_type`
- `--sysparm_catalog`
- `--sysparm_top_level_only`
- `--record_id`
- `--template_id`
- `--mode`

### 输出格式

- `--pretty`：以美观的 JSON 格式输出结果
- `--out <path>`：将附件内容保存到指定文件路径

### 示例

- 列出最近的事件：```bash
node cli.mjs list incident --sysparm_limit 5 --sysparm_fields number,short_description,priority,sys_id
```

- 使用过滤器进行查询：```bash
node cli.mjs list cmdb_ci --sysparm_query "operational_status=1^install_status=1" --sysparm_limit 10
```

- 获取单条记录：```bash
node cli.mjs get incident <sys_id> --sysparm_fields number,short_description,opened_at
```

- 动态修改身份验证信息：```bash
node cli.mjs list incident --domain myinstance.service-now.com --username admin --password "***" --sysparm_limit 3
```

- 读取附件元数据并下载附件：```bash
node cli.mjs attach list --sysparm_query "table_name=incident" --sysparm_limit 5
node cli.mjs attach file <sys_id> --out /tmp/attachment.bin
```

- 汇总统计数据：```bash
node cli.mjs stats incident --sysparm_query "active=true^priority=1" --sysparm_count true
```

- 仅限读取服务目录数据：```bash
node cli.mjs sc catalogs --sysparm_text "laptop" --sysparm_limit 5
node cli.mjs sc items --sysparm_text "mac" --sysparm_limit 5
node cli.mjs sc item <sys_id>
node cli.mjs sc item-variables <sys_id>
```

### 服务目录的 GET 端点（仅限读取）

- `cart`
- `delivery-address user_id`
- `validate-categories`
- `on-change-choices entity_id`
- `catalogs`
- `catalog sys_id`
- `catalog-categories sys_id`
- `category sys_id`
- `items`
- `item sys_id`
- `item-variables sys_id`
- `item-delegation item_sys_id user_sys_id`
- `producer-record producer_id record_id`
- `record-wizard record_id wizard_id`
- `generate-stage-pool quantity`
- `step-configs`
- `wishlist`
- `wishlist-item cart_item_id`
- `wizard sys_id`

### 检查表格结构

如果您不确定字段名称，可以使用此命令：```bash
node cli.mjs schema incident
```

### 读取工单历史记录

此命令用于读取工单的完整对话记录，而不仅仅是当前状态：```bash
node cli.mjs history incident <sys_id>
```

### 专家预设文件

在 `specialists/` 目录下创建 JSON 预设文件，以一次性执行多个读取操作：

- `specialists/incidents.json`：用于检查 `incident` 表的结构：
  每个条目支持 `sysparm_` 参数以及其他相关参数。
  - `name`：批量输出中的标签
  - `table`：目标表格名称
  - `sys_id`：可选的记录 ID（用于获取单条记录）

运行批量预设文件：```bash
node cli.mjs batch specialists/incidents.json --pretty
```

## 输出格式

Table API 默认返回 JSON 格式的数据。结果将显示在 `result` 变量中。

## 注意事项

- 使用 `sysparm_limit` 限制返回的数据量，以避免传输大量数据。
- 使用 `sysparm_fields` 仅返回必要的字段，以减少数据大小。
- 本技能仅支持读取操作，不支持写入操作。

## 代理工具包功能概述

- `list` 和 `get`：用于查看记录的当前状态。
- `attach`：用于查看文件和截图。
- `stats`：用于显示统计信息和汇总数据。
- `sc`：用于获取所需的字段信息。
- `schema`：用于检查数据库结构，帮助识别错误。
- `history`：用于查看工单的完整对话记录。

## 注意事项（重要）

- 服务目录 API 的返回结果可能为空数组，具体取决于目录内容和搜索条件——请尝试使用更具体的查询条件（如 `--sysparm_text`），或增加 `--sysparm_limit` 的值。
- `sysparm_display_value` 默认设置为 `true`，以便以用户友好的格式显示字段值（例如显示用户名而非系统 ID）。如需原始系统 ID，可设置 `--sysparm_display_value false`。
- 对于代理发起的查询，请设置较小的 `--sysparm_limit` 值，以避免数据量过大导致超时。建议使用 `stats` 功能进行计数或汇总操作，而不是下载大量数据。
- 关于附件：元数据可通过 `attach list`/`attach get` 获取；使用 `attach file <sys_id> --out <path>` 下载附件内容以供本地分析。
- 在读取未知表格之前，建议先使用 `schema` 命令检查表格结构。
- `history` 命令用于获取日志记录（评论/工作日志），有助于查看工单的完整对话记录。
- 使用 `--pretty` 选项可让 JSON 输出更易于阅读，并帮助代理总结结果。

## 推荐的批量预设文件

以下是一些常用的批量预设文件，位于 `specialists/` 目录下，可加速常见的读取操作：

1) `specialists/inspect_incident_schema.json`：用于检查 `incident` 表的结构：
  ```json
[
  {
    "name": "schema-incident",
    "table": "sys_dictionary",
    "sysparm_query": "name=incident^elementISNOTEMPTY",
    "sysparm_fields": "element,column_label,internal_type,reference",
    "sysparm_limit": 500
  }
]
```

2) `specialists/incident_history_template.json`：用于查看工单的历史记录（运行前请将 `<SYS_ID>` 替换为目标记录 ID）：
  ```json
[
  {
    "name": "incident-history",
    "table": "sys_journal_field",
    "sysparm_query": "name=incident^element_id=<SYS_ID>",
    "sysparm_fields": "value,element,sys_created_on,sys_created_by",
    "sysparm_order_by": "sys_created_on",
    "sysparm_limit": 500
  }
]
```

3) `specialists/attachments_incident.json`：用于获取 `incident` 表中的最近附件：
  ```json
[
  {
    "name": "recent-incident-attachments",
    "table": "attachment",
    "sysparm_query": "table_name=incident",
    "sysparm_fields": "sys_id,file_name,content_type,table_sys_id,sys_created_on",
    "sysparm_limit": 20
  }
]
```

使用方法：

- 检查表格结构：`node cli.mjs batch specialists/inspect_incident_schema.json --pretty`
- 查看历史记录：将 `<SYS_ID>` 替换为目标记录 ID，然后运行 `node cli.mjs batch specialists/incident_history_template.json --pretty`（或 `node cli.mjs history incident <SYS_ID> --pretty`）
- 下载附件：`node cli.mjs batch specialists/attachments_incident.json --pretty`，接着使用 `node cli.mjs attach file <sys_id> --out /tmp/file` 下载附件文件。

这些预设文件仅支持读取操作，并设置了合理的限制。如需其他预设文件（例如查看仪表板数据、最近更改记录或升级信息），可随时提出请求。