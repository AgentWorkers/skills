---
name: client-project-manager
description: 管理自由职业者客户、项目、发票以及沟通记录。适用于跟踪客户的工作进度、生成发票、发送更新信息、管理截止日期，或组织自由职业者的业务运营。
argument-hint: "[action] [client-or-project]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# 客户项目经理

这是一个功能齐全的Freelance业务管理系统，能够通过一个统一的界面来管理客户、项目、截止日期、交付物、发票以及沟通记录。

## 使用方法

```
/client-project-manager add client "Acme Corp" --contact "jane@acme.com" --rate "$100/hr"
/client-project-manager add project "Website Redesign" --client "Acme Corp" --deadline "2026-03-15" --budget "$5000"
/client-project-manager status
/client-project-manager update "Website Redesign" --progress 60 --note "Homepage mockup approved"
/client-project-manager invoice "Acme Corp" --project "Website Redesign"
/client-project-manager weekly-update "Acme Corp"
/client-project-manager dashboard
```

## 数据存储

所有数据都以JSON格式存储在`./freelance-data/`目录下：

```
freelance-data/
  clients.json        # Client CRM data
  projects.json       # Active and completed projects
  time-log.json       # Time tracking entries
  invoices/           # Generated invoices
  updates/            # Client update emails
```

如果该目录不存在，请在首次使用时创建它。如果文件已经存在，请先读取这些文件并保留所有现有数据。

## 命令

### `add client`  
向CRM系统中添加一个新的客户。

```
/client-project-manager add client "[Name]" --contact "[email]" --rate "[rate]" --notes "[notes]"
```

数据存储位置：`clients.json`  
```json
{
  "id": "client-uuid",
  "name": "Acme Corp",
  "contact_email": "jane@acme.com",
  "default_rate": "$100/hr",
  "notes": "Prefers Slack for communication",
  "projects": [],
  "total_billed": 0,
  "total_paid": 0,
  "created": "2026-02-13",
  "status": "active"
}
```

### `add project`  
在某个客户名下添加一个新的项目。

```
/client-project-manager add project "[Name]" --client "[Client]" --deadline "[date]" --budget "[amount]" --deliverables "[list]"
```

数据存储位置：`projects.json`  
```json
{
  "id": "project-uuid",
  "name": "Website Redesign",
  "client_id": "client-uuid",
  "client_name": "Acme Corp",
  "status": "active",
  "progress": 0,
  "budget": 5000,
  "billed": 0,
  "deadline": "2026-03-15",
  "created": "2026-02-13",
  "deliverables": [
    { "name": "Homepage mockup", "status": "pending", "due": "2026-02-20" },
    { "name": "Inner pages", "status": "pending", "due": "2026-03-01" },
    { "name": "Development", "status": "pending", "due": "2026-03-10" },
    { "name": "Launch", "status": "pending", "due": "2026-03-15" }
  ],
  "notes": [],
  "time_entries": []
}
```

### `log time`  
记录在项目上花费的工作时间。

```
/client-project-manager log time "[Project]" --hours [X] --description "[what you did]"
```

数据存储位置：`time-log.json`  
```json
{
  "id": "entry-uuid",
  "project_id": "project-uuid",
  "client_id": "client-uuid",
  "date": "2026-02-13",
  "hours": 3.5,
  "rate": 100,
  "amount": 350,
  "description": "Built responsive navigation and hero section"
}
```

### `update`  
更新项目进度并添加备注。

```
/client-project-manager update "[Project]" --progress [0-100] --note "[update]" --deliverable "[name]" --status "[done|in-progress|pending]"
```

### `status`  
显示所有活跃项目的当前状态。

输出格式：  
```
╔══════════════════════════════════════════════════════════════╗
║                    FREELANCE DASHBOARD                       ║
╠══════════════════════════════════════════════════════════════╣

📊 Active Projects: 3
💰 Outstanding Invoices: $2,500
⏰ Hours This Week: 22.5
📅 Next Deadline: Website Redesign (Acme Corp) — Mar 15

──────────────────────────────────────────────────────────────
PROJECT: Website Redesign
CLIENT: Acme Corp | DEADLINE: Mar 15, 2026
PROGRESS: ████████████░░░░░░░░ 60%
BUDGET: $3,000 / $5,000 billed
DELIVERABLES:
  ✅ Homepage mockup (Feb 20) — DONE
  🔄 Inner pages (Mar 1) — IN PROGRESS
  ⬜ Development (Mar 10) — PENDING
  ⬜ Launch (Mar 15) — PENDING
──────────────────────────────────────────────────────────────
```

### `invoice`  
为某个客户生成专业的发票。

```
/client-project-manager invoice "[Client]" --project "[Project]" --period "[start] to [end]"
```

发票文件将以Markdown和HTML格式生成，并保存在`freelance-data/invoices/`目录下：  
**发票内容**：  
```
INVOICE #[INV-YYYY-NNN]
Date: [today]
Due: [today + 14 days]

FROM:
[Your name/business — read from freelance-data/config.json if exists]

TO:
[Client name]
[Client contact]

PROJECT: [Project name]
PERIOD: [Date range]

| Date | Description | Hours | Rate | Amount |
|------|-------------|-------|------|--------|
| ... time entries from period ... |

                              Subtotal: $X,XXX.XX
                              Tax (0%): $0.00
                              TOTAL DUE: $X,XXX.XX

Payment Terms: Net 14
Payment Methods: [from config.json or "Bank Transfer / PayPal"]

Thank you for your business.
```

文件名示例：`freelance-data/invoices/INV-2026-001-acme-corp.md` 和 `freelance-data/invoices/INV-2026-001-acme-corp.html`

### `weekly-update`  
生成一份专业的每周客户更新邮件。

```
/client-project-manager weekly-update "[Client]"
```

读取客户的项目信息、最近的工作记录和备注，然后生成相应的更新邮件。

```
Subject: Weekly Update — [Project Name] — Week of [date]

Hi [Contact first name],

Here's your weekly update on [Project Name]:

**This Week:**
- [Completed deliverables and progress]
- [Key decisions made]
- [Hours worked: X.X]

**Next Week:**
- [Planned deliverables]
- [Any blockers or decisions needed from client]

**Project Status:**
- Progress: XX%
- Budget used: $X,XXX / $X,XXX
- On track for [deadline]: ✅ Yes / ⚠️ At risk / ❌ Behind

[Any questions or items needing client input]

Best,
[Your name]
```

邮件内容将保存在`freelance-data/updates/`目录中，可供复制和粘贴使用。

### `payment-reminder`  
为逾期未付的发票生成礼貌的付款提醒。

```
/client-project-manager payment-reminder "[Client]"
```

检查所有逾期未付的发票：
- 逾期1-7天：发送温和的提醒  
- 逾期8-14天：发送正式但专业的跟进通知  
- 逾期15天及以上：发送最终通知并提及滞纳金

### `dashboard`  
展示全面的业务概览。

```
╔══════════════════════════════════════════════════════════════╗
║                  MONTHLY BUSINESS REPORT                     ║
╠══════════════════════════════════════════════════════════════╣

💰 Revenue This Month:     $4,250
💰 Revenue Last Month:     $3,800  (↑ 12%)
📊 Active Projects:        3
✅ Completed This Month:   1
⏰ Hours Billed:           42.5
💵 Effective Hourly Rate:  $100/hr
📋 Outstanding Invoices:   $2,500 (2 invoices)
⚠️  Overdue Invoices:      $0

TOP CLIENTS (by revenue):
  1. Acme Corp        $2,500  (59%)
  2. StartupXYZ       $1,250  (29%)
  3. LocalBiz         $500    (12%)

UPCOMING DEADLINES:
  Feb 20 — Homepage mockup (Acme Corp)
  Mar 01 — Content strategy (StartupXYZ)
  Mar 15 — Website launch (Acme Corp)
```

### `config`  
设置发票和沟通相关的基本配置信息。

```
/client-project-manager config --name "Your Name" --business "Your Business LLC" --email "you@email.com" --payment "PayPal: you@email.com / Bank: routing XXX"
```

配置信息将保存在`freelance-data/config.json`文件中。

## 数据完整性规则

1. **切勿覆盖现有数据**——始终先读取现有数据，再进行修改后再写入。
2. **务必备份数据**——在任何写入操作之前，先检查数据是否存在且格式正确（JSON格式）。
3. **使用UUID生成唯一标识符**：例如 `client-[timestamp]`、`project-[timestamp]`。
4. **日期格式**——始终使用ISO 8601格式（`YYYY-MM-DD`）。
5. **货币单位**——以数字形式存储货币，显示时使用 `$` 标记。