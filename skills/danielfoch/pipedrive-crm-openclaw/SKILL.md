---
name: pipedrive-crm-openclaw
description: 使用 OpenClaw 和 API v1 管理 Pipedrive CRM，包括人员、组织、交易、潜在客户、活动、备注、销售流程以及自定义端点操作。当用户希望通过 API 而非 Pipedrive 界面来执行 CRM 操作时，可以使用此功能。
---
# Pipedrive CRM for OpenClaw

使用此技能通过API调用在Pipedrive中执行日常CRM操作，包括CRUD（创建、读取、更新、删除）、搜索、管道状态转移、活动记录以及任何不支持的操作（通过原始端点请求实现）。

## 所需环境

设置一种认证模式：

- `PIPEDRIVE_API_TOKEN`：用于API令牌认证（最简单的方式）
- `PIPEDRIVE_ACCESS_TOKEN`：用于OAuth bearer认证

设置基础路由：

- `PIPEDRIVE COMPANY_DOMAIN`（例如：`acme`，对应`https://acme.pipedrive.com`）

可选参数：

- `PIPEDRIVE_API_BASE`：用于覆盖完整的API基础URL（默认值为`https://<company>.pipedrive.com/api/v1`）
- `PIPEDRIVE_TIMEOUT`：请求超时时间（以秒为单位，默认为30秒）

## 设置

如果用户请求连接或验证凭据，请执行以下代码：

```bash
python3 skills/pipedrive-crm-openclaw/scripts/setup-wizard.py
```

## 主脚本

运行以下脚本：

```bash
python3 skills/pipedrive-crm-openclaw/scripts/pipedrive-api.py <command> [args]
```

核心命令：

- `test_connection`：测试连接是否正常
- `list <entity> [--start N] [--limit N]`：列出指定实体的记录（可选参数：`--start`和`--limit`用于分页）
- `get <entity> <id>`：获取指定实体的详细信息
- `create <entity> <json_payload>`：创建新的实体
- `update <entity> <id> <json_payload> [--method PUT|PATCH]`：更新指定实体的信息
- `delete <entity> <id>`：删除指定实体
- `search <entity> <term> [--limit N] [--fields csv] [--exact-match]`：搜索指定实体（可选参数：`--fields`用于指定搜索字段，`--exact-match`用于精确匹配）
- `move_deal_stage <deal_id> <stage_id> [--status open|won|lost|deleted]`：转移交易阶段
- `add_note <content> [--deal-id ID] [--person-id ID] [--org-id ID] [--lead-id UUID]`：添加备注
- `request <METHOD> <path> [--query '{...}'] [--body '{...}']`：发送自定义请求（`<METHOD>`表示请求方法，`<path>`表示请求路径，`--query`和`--body`用于传递请求参数）

支持的实体类型：

- `persons`（人员）
- `organizations`（组织）
- `deals`（交易）
- `leads`（潜在客户）
- `activities`（活动记录）
- `notes`（备注）
- `products`（产品）
- `users`（用户）
- `pipelines`（销售管道）
- `stages`（交易阶段）

## 实用OpenClaw脚本示例

### 潜在客户获取与资格评估

1. 使用`search persons "name or email"`搜索人员信息并去重。
2. 如果未找到匹配项，使用`create persons '{...}'`创建新人员。
3. 使用`create deals '{...}'`创建新交易，并将其与相关人员/组织关联。
4. 使用`add_note "summary" --deal-id <id>`为交易添加备注以保留上下文信息。

### 销售管道管理

1. 使用`list deals`列出所有交易，并通过`request`查询进行筛选。
2. 使用`move_deal_stage <deal_id> <stage_id>`转移交易阶段。
3. 使用`create activities '{...}'为交易创建后续跟进活动。

### 日常跟进流程

1. 使用`list activities`列出所有活动记录。
2. 完成活动后，使用`update activities <id> '{"done":1}'`更新活动状态。
3. 使用`add_note`记录相关交互信息。

## 安全规则

- 绝不要在聊天输出中显示原始API令牌。
- 当用户意图不明确时，先阅读API响应再执行操作。
- 在执行任何可能修改数据的操作之前，请验证API响应中的ID。
- 如果收到`401`或`403`错误响应，请停止操作并请求用户重新提供正确的凭据或权限范围。
- 对于尚未通过辅助命令封装的API端点，请使用`request`直接发送请求。

## 参考资料

根据需要加载以下文档：

- `references/entity-playbooks.md`
- `references/pipedrive-v1-notes.md`