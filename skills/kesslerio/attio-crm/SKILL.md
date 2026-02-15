---
name: attio
description: 管理 Attio CRM 的记录（包括公司、人员、交易、任务和备注）。支持搜索、创建、更新记录以及管理交易流程。
metadata: {"moltbot":{"emoji":"📇","requires":{"bins":["attio"],"env":["ATTIO_ACCESS_TOKEN"]}}}
---

# Attio CRM

## 快速命令

```bash
# Search for records
attio search companies "Acme"
attio search deals "Enterprise"
attio search people "John"

# Get record details by ID
attio get companies "record-uuid"
attio get deals "record-uuid"

# Add a note to a record
attio note companies "record-uuid" "Title" "Note content here"

# List notes on a record
attio notes companies "record-uuid"

# See available fields for a record type
attio fields companies
attio fields deals

# Get select field options (e.g., deal stages)
attio options deals stage
```

## 重要规则

1. **先查看字段信息** - 在更新记录之前，运行 `attio fields <type>` 命令。
2. **检查下拉选项** - 对于下拉菜单，运行 `attio options <type> <field>` 命令来查看可用选项。
3. **使用内部字段名称** - 选择字段时应使用其内部名称，而非显示标签。
4. **不确定时使用备注** - 将非结构化数据保存在备注中，而非记录字段中。
5. **正确格式化数据** - 数字格式为 `85`，数组格式为 `["Value"]`，布尔值格式为 `true/false`。

## 工作流程参考

根据需要加载以下参考资料：
- **公司工作流程** - `references/company_workflows.md`
- **交易工作流程** - `references/deal_workflows.md`
- **字段指南** - `references/field_guide.md`

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `attio search <type> "<query>"` | 搜索记录 |
| `attio get <type> <id>` | 获取记录详情 |
| `attio update <type> <id> record_data="{...}'` | 更新记录 |
| `attio create <type> record_data="{...}'` | 创建记录 |
| `attio delete <type> <id>` | 删除记录 |
| `attio note <type> <id> "<title>" "<content>"` | 添加备注 |
| `attio notes <type> <id>` | 列出所有备注 |
| `attio fields <type>` | 列出可用字段 |
| `attio options <type> <field>` | 查看字段的下拉选项 |

**记录类型：** `companies`、`people`、`deals`、`tasks`

## 常见工作流程

### 查找公司信息
```bash
attio search companies "Acme Corp"
```

### 获取交易详情
```bash
attio get deals "deal-uuid-here"
```

### 为公司添加会议备注
```bash
attio note companies "company-uuid" "Meeting Notes" "Discussed pricing. Follow up next week."
```

### 在更新前检查交易阶段
```bash
attio options deals stage
```

### 更新交易阶段
```bash
attio update deals "deal-uuid" record_data='{"stage":"negotiation"}'
```

## 流程阶段

**切勿硬编码阶段名称。** 必须先进行检查：
```bash
attio options deals stage
```

请使用字段的内部名称（例如 `negotiation`），而非显示标签（例如 “Negotiation”）。