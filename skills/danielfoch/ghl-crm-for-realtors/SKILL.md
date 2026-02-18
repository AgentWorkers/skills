---
name: ghl-crm-for-realtors
description: Use this skill for GoHighLevel CRM work for realtors: contact lookup and updates, opportunity/pipeline actions, conversation messaging, calendar slots, and workflow enrollment using GoHighLevel API v2.
---

# GHL CRM for Real Estate Agents

当用户需要在 GoHighLevel (GHL) 中实现房地产代理的 CRM 功能时，请使用此技能，包括跟进潜在客户、管理销售流程、预订预约以及处理消息工作流等操作。

## 所需环境

在运行脚本之前，请设置以下变量：

- `HIGHLEVEL_TOKEN`（私有集成令牌）
- `HIGHLEVEL_LOCATION_ID`（子账户的位置 ID）

可选的运行时变量：

- `PYTHONUNBUFFERED=1`

## 设置

如果用户请求连接或设置 GHL，请运行以下命令：

```bash
python3 scripts/setup-wizard.py
```

向导会验证凭据并测试 API 连接性。

## 主要脚本

使用辅助脚本执行直接操作：

```bash
python3 scripts/ghl-api.py <command> [args...]
```

房地产代理工作流的常用命令：

- `test_connection`  
- `search_contacts [query]`  
- `get_contact [contact_id]`  
- `create_contact [json]`  
- `update_contact [contact_id] [json]`  
- `list_opportunities`  
- `list_pipelines`  
- `list_conversations`  
- `send_message [contact_id] [message]`  
- `list_calendars`  
- `get_free_slots [calendar_id] [start_date] [end_date]`  
- `list_workflows`  
- `add_to_workflow [contact_id] [workflow_id]`  

## 面向房地产代理的实用脚本

### 新潜在客户处理

1. 使用 `search_contacts` 命令检查潜在客户是否存在重复记录。
2. 如果未找到潜在客户，使用 `create_contact` 命令创建新客户，并为其添加相应的标签（例如：`buyer`、`zillow`、`open-house`）。
3. 通过相应的接触点（contact endpoints）添加后续任务或备注。

### 销售流程管理

1. 使用 `list_opportunities` 命令查看当前活跃的潜在客户。
2. 通过 `ghl-api.py` 中提供的命令路径更新潜在客户的销售阶段。
3. 根据响应数据确认潜在客户的销售阶段和状态。

### 回访与沟通

1. 首先使用 `search_contacts` 或 `get_contact` 命令获取客户信息。
2. 使用 `send_message` 命令发送消息。
3. 通过 `list_conversations` 命令查看与客户的沟通记录。

### 预约协助

1. 使用 `list_calendars` 命令查看可用的日程安排。
2. 使用 `get_free_slots` 命令查询指定日期范围内的空闲时间。
3. 根据需要，通过脚本中的日历接口（calendar endpoints）创建预约。

## 安全规则

- 绝不要在聊天输出中显示或打印原始令牌。
- 当意图不明确时，优先进行信息读取操作，避免执行写入操作。
- 请从 GHL 的响应中验证客户或潜在客户的 ID，避免猜测。
- 如果 API 错误返回 401/403 状态码，立即停止操作，并请求用户提供正确的权限范围或令牌。

## 参考资料

仅在需要时加载以下文件：

- `references/contacts.md`  
- `references/opportunities.md`  
- `references/conversations.md`  
- `references/calendars.md`  
- `references/troubleshooting.md`