# 商业功能（Business Functions）

这些高级商业工作流程将多个MCP工具整合为可重用、可执行的技能，用于ERPNext系统。

## 概述

这些“技能”是预先定义的工作流程，以JSON文件的形式存储在`definitions/`目录中。每个技能包含以下内容：
- **触发条件（Triggers）**：用于激活该技能的自然语言指令或模式。
- **工具（Tools）**：按顺序执行的MCP工具。
- **输入参数（Input Parameters）**：必需或可选的输入数据。
- **工作流程步骤（Workflow Steps）**：包含变量替换的有序执行计划。
- **安全规则（Guardrails）**：确保技能安全执行的验证机制。
- **输出模板（Output Template）**：格式化的响应消息。

## 可用的技能

### 客户关系管理（CRM）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`create_customer`](definitions/create_customer.json) | 创建新客户（包含联系信息和地址）          | crm         |
| [`create_lead`](definitions/create_lead.json) | 注册新潜在客户                          | crm         |
| [`create_supplier`](definitions/create_supplier.json) | 添加新供应商                            | crm         |

### 销售（Sales）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`create_sales_order`](definitions/create_sales_order.json) | 创建销售订单                          | sales        |
| [`create_quotation`](definitions/create_quotation.json) | 创建销售报价                          | sales        |
| [`createinvoice`](definitions/createinvoice.json) | 生成销售发票                          | sales        |
| [`complete_sales_workflow`](definitions/complete_sales_workflow.json) | 完整的销售流程（报价 → 订单 → 发票 → 支付）     | sales        |

### 采购（Purchase）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`create_purchase_order`](definitions/create_purchase_order.json) | 创建采购订单                          | purchase      |
|                          |                                            |

### 库存（Inventory）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`create_item`](definitions/create_item.json) | 创建新库存项目                          | inventory     |
| [`stock_entry`](definitions/stock_entry.json) | 记录库存变动                          | inventory     |

### 项目（Project）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`create_project`](definitions/create_project.json) | 创建新项目                          | project       |
|                          |                                            |

### 财务（Financial）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`process_payment`](definitions/process_payment.json) | 处理付款记录                          | payments      |

### 实用工具（Utility）技能

| 技能          | 描述                                      | 类别        |
|-----------------|-----------------------------------------|------------|
| [`search_records`](definitions/search_records.json) | 在多种文档类型中搜索                          | utility      |
| [`bulk_operation`](definitions/bulk_operation.json) | 批量创建/更新/删除记录                    | utility      |
| [`generic_task`](definitions/generic_task.json) | 灵活的多步骤工作流程                        | utility      |

## 使用方法

### 加载技能

```python
from bc_skills import get_available_skills, load_skill

# List all available skills
skills = get_available_skills()
print(skills)  # ['create_customer', 'create_sales_order', ...]

# Load a specific skill
skill = load_skill("create_customer")
```

### 执行技能

```python
from bc_skills.loader import execute_skill

result = execute_skill(
    name="create_customer",
    context={
        "customer_name": "ACME Corp",
        "customer_type": "Company",
        "customer_group": "Commercial",
        "email": "contact@acme.com"
    },
    user="Administrator"
)

print(result)
```

### 触发条件示例

这些技能可以响应以下自然语言指令：

| 触发语句                | 对应技能                |
|-------------------|-------------------|
| “create customer”          | create_customer          |
| “add customer”          | create_customer          |
| “new customer”          | create_customer          |
| “complete sales workflow”     | complete_sales_workflow     |
| “full sales process”     | complete_sales_workflow     |
| “process order to payment”     | complete_sales_workflow     |
| “create sales order”     | create_sales_order       |
| “generate invoice”       | createinvoice         |

## 技能定义结构

```json
{
  "name": "skill_name",
  "version": "1.0.0",
  "description": "What the skill does",
  "author": "Business Claw Team",
  "category": "crm|sales|purchase|inventory|project|payments|utility",
  
  "triggers": [
    "trigger phrase 1",
    "trigger phrase 2"
  ],
  
  "tools": [
    {
      "name": "tool_name",
      "description": "What it does",
      "required": true
    }
  ],
  
  "input_schema": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string",
        "description": "Parameter description",
        "enum": ["option1", "option2"]
      }
    },
    "required": ["required_param"]
  },
  
  "workflow": {
    "steps": [
      {
        "step": "step_name",
        "tool": "tool_to_call",
        "arguments": {
          "doctype": "DocType",
          "data": {
            "field": "${variable}"
          }
        }
      }
    ]
  },
  
  "guardrails": {
    "rule_name": true
  },
  
  "output_template": "Formatted output {{variable}}"
}
```

## 变量替换

工作流程步骤支持从执行上下文中替换变量（例如：`${variable}`）。

```json
{
  "step": "create_order",
  "tool": "create_document",
  "arguments": {
    "doctype": "Sales Order",
    "data": {
      "customer": "${customer_id}",
      "items": "${items}"
    }
  }
}
```

## 创建自定义技能

1. 在`definitions/`目录下创建一个JSON文件。
2. 定义触发条件、使用的工具、输入参数以及工作流程。
3. 使用`SkillLoader`类加载并执行该技能。

示例自定义技能结构：

```json
{
  "name": "my_custom_skill",
  "version": "1.0.0",
  "description": "My custom workflow",
  "category": "utility",
  "triggers": ["my trigger"],
  "tools": [
    {"name": "get_doctype_meta", "required": true},
    {"name": "create_document", "required": true}
  ],
  "input_schema": {
    "type": "object",
    "properties": {
      "param1": {"type": "string"}
    },
    "required": ["param1"]
  },
  "workflow": {
    "steps": [
      {
        "step": "step1",
        "tool": "get_doctype_meta",
        "arguments": {"doctype": "Item"}
      }
    ]
  },
  "output_template": "Result: {{result}}"
}
```

## 系统架构

- `loader.py`：负责管理技能的加载和执行。
- `definitions/`：包含所有技能定义的JSON文件。
- 技能通过`ToolRouter`按顺序执行相应的MCP工具。
- 安全规则在技能执行前进行验证。

## 系统要求

- 需要Frappe/ERPNext环境。
- 需要`bc_mcp`模块来路由工具调用。
- 技能定义文件格式为JSON或YAML。

## 许可证

MIT许可证。