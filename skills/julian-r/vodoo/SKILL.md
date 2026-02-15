---
name: vodoo
description: 通过 vodoo CLI 查询和管理 Odoo ERP 数据（包括帮助台工单、项目、任务、CRM 潜在客户以及知识文章）
---

# Vodoo - Odoo 命令行工具 (Odoo CLI Tool)

使用 `uvx vodoo` 可通过 XML-RPC 与 Odoo 进行交互。无需安装，`uvx` 会直接执行该命令。

## 重要提示：务必使用 `--no-color` 选项

**请在每个 `vodoo` 命令后添加 `--no-color` 选项。** 这将禁用 ANSI 转义码，从而显著减少通信过程中使用的令牌（tokens）数量。

```bash
# Correct
uvx vodoo --no-color helpdesk list

# Wrong (wastes tokens on color codes)
uvx vodoo helpdesk list
```

## 命令概览

| 模块        | 模型        | 描述                          |
|-------------|------------|-------------------------------------------|
| `helpdesk`     | helpdesk.ticket | 支持工单                          |
| `project-task`   | project.task   | 项目任务                          |
| `project`     | project.project | 项目                            |
| `crm`      | crm.lead     | 客户线索与销售机会                    |
| `knowledge`    | knowledge.article | 知识库文章                        |
| `model`      | any        | 适用于任何模型的通用 CRUD 操作                |
| `security`    | -           | 用户与组管理                        |

## 支持工单 (Helpdesk Tickets)

```bash
# List tickets
uvx vodoo helpdesk list
uvx vodoo helpdesk list --stage "New"
uvx vodoo helpdesk list --limit 5

# Show ticket details
uvx vodoo helpdesk show 123

# Add comment (visible to customer)
uvx vodoo helpdesk comment 123 "Your issue has been resolved"

# Add internal note (not visible to customer)
uvx vodoo helpdesk note 123 "Escalated to dev team"

# Manage tags
uvx vodoo helpdesk tags                    # List available tags
uvx vodoo helpdesk tag 123 "urgent"        # Add tag to ticket

# View history and attachments
uvx vodoo helpdesk chatter 123             # Message history
uvx vodoo helpdesk attachments 123         # List attachments
uvx vodoo helpdesk download 456            # Download attachment by ID
uvx vodoo helpdesk download-all 123        # Download all attachments

# Update fields
uvx vodoo helpdesk fields                  # List available fields
uvx vodoo helpdesk fields 123              # Show field values for ticket
uvx vodoo helpdesk set 123 priority=3      # Set field value

# Attachments and URL
uvx vodoo helpdesk attach 123 report.pdf   # Attach file
uvx vodoo helpdesk url 123                 # Get web URL
```

## 项目任务 (Project Tasks)

```bash
# List tasks
uvx vodoo project-task list
uvx vodoo project-task list --project "Website Redesign"
uvx vodoo project-task list --stage "In Progress"

# Create task
uvx vodoo project-task create "Fix login bug" --project "Website"

# Show task details
uvx vodoo project-task show 456

# Comments and notes
uvx vodoo project-task comment 456 "Started working on this"
uvx vodoo project-task note 456 "Need clarification from client"

# Tags
uvx vodoo project-task tags
uvx vodoo project-task tag 456 "backend"
uvx vodoo project-task tag-create "new-tag"
uvx vodoo project-task tag-delete "old-tag"

# Attachments and history
uvx vodoo project-task chatter 456
uvx vodoo project-task attachments 456
uvx vodoo project-task attach 456 spec.pdf

# Fields and URL
uvx vodoo project-task fields
uvx vodoo project-task set 456 priority=1
uvx vodoo project-task url 456
```

## 项目 (Projects)

```bash
# List projects
uvx vodoo project list

# Show project details
uvx vodoo project show 789

# Comments and notes
uvx vodoo project comment 789 "Project kickoff complete"
uvx vodoo project note 789 "Budget approved"

# History and attachments
uvx vodoo project chatter 789
uvx vodoo project attachments 789
uvx vodoo project attach 789 contract.pdf

# Fields and stages
uvx vodoo project fields
uvx vodoo project set 789 description="Updated description"
uvx vodoo project stages              # List task stages
uvx vodoo project url 789
```

## 客户线索/销售机会 (CRM Leads/Opportunities)

```bash
# List leads
uvx vodoo crm list
uvx vodoo crm list --stage "Qualified"

# Show lead details
uvx vodoo crm show 321

# Comments and notes
uvx vodoo crm comment 321 "Follow-up scheduled"
uvx vodoo crm note 321 "Decision maker: John Smith"

# Tags
uvx vodoo crm tags
uvx vodoo crm tag 321 "hot-lead"

# History and attachments
uvx vodoo crm chatter 321
uvx vodoo crm attachments 321
uvx vodoo crm attach 321 proposal.pdf

# Fields and URL
uvx vodoo crm fields
uvx vodoo crm set 321 expected_revenue=50000
uvx vodoo crm url 321
```

## 知识库文章 (Knowledge Articles)

```bash
# List articles
uvx vodoo knowledge list

# Show article
uvx vodoo knowledge show 111

# Comments and notes
uvx vodoo knowledge comment 111 "Updated for v2.0"
uvx vodoo knowledge note 111 "Needs review"

# History and URL
uvx vodoo knowledge chatter 111
uvx vodoo knowledge attachments 111
uvx vodoo knowledge url 111
```

## 通用模型操作 (Generic Model Operations)

对于没有专门命令支持的 Odoo 模型，可以使用以下通用命令：

```bash
# Read records
uvx vodoo model read res.partner --domain "[('is_company', '=', True)]" --fields name,email
uvx vodoo model read res.partner --ids 1,2,3

# Create record
uvx vodoo model create res.partner name="ACME Corp" is_company=true

# Update record
uvx vodoo model update res.partner 123 phone="+1234567890"

# Delete record
uvx vodoo model delete res.partner 123

# Call model method
uvx vodoo model call res.partner 123 method_name
```

## 安全/用户管理 (Security / User Management)

```bash
# Create standard Vodoo security groups
uvx vodoo security create-groups

# Create API service account
uvx vodoo security create-user "api-bot" "api-bot@example.com"

# Assign user to Vodoo API groups
uvx vodoo security assign-bot 456

# Set/reset user password
uvx vodoo security set-password 456 "new-password"
```

## 常用选项

大多数命令支持以下选项：
- `--no-color`  - **必需**（用于 AI 应用场景，需紧跟在 `vodoo` 后使用）
- `--limit N`   - 限制返回结果的数量
- `--help`   - 显示命令帮助信息

## 字段更新 (Field Updates)

`set` 命令支持对数值字段进行以下操作：
- `field=value`   - 将字段值设置为指定值
- `field+=10`   - 将字段值增加 10
- `field-=5`   - 从字段值中减去 5
- `field*=2`   - 将字段值乘以 2
- `field/=2`   - 将字段值除以 2

## 使用技巧：
1. 始终使用 `--no-color` 选项（可避免不必要的 ANSI 转义码，从而节省通信资源）
2. 在更新字段值之前，使用 `fields` 命令查看可用的字段列表
3. 项目阶段的名称区分大小写，必须完全匹配
4. 如果知道模型的技术名称，`model` 命令可以访问该模型中的所有数据