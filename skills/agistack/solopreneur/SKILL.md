---
name: solopreneur
description: >
  **单人业务管理工具：包含仪表板、项目进度跟踪、发票生成及每周业务回顾功能**  
  适用于需要管理个人业务、客户关系、收入情况、项目进度以及发票处理的场景。该工具可生成业务仪表板，跟踪潜在客户从线索到成交的整个过程，协助用户起草发票，并对各项任务进行优先级排序。所有业务数据均保持私密性且存储在本地。  
  **主要功能包括：**  
  - **仪表板（Business Dashboard）**：实时展示业务运营状况。  
  - **项目进度跟踪（Pipeline Tracking）**：详细记录项目进展。  
  - **发票生成（Invoice Generation）**：自动生成发票。  
  - **每周业务回顾（Weekly Business Review）**：定期评估业务绩效。  
  **适用场景：**  
  - 个人创业者  
  - 自由职业者  
  - 需要独立管理业务的人员  
  **使用建议：**  
  当用户提及“单人业务”、“客户”、“收入”、“项目进度”、“发票”或“任务优先级”等关键词时，可考虑使用该工具。
---
# 独立创业者（Solopreneur）

这是一个专为独立创业者设计的业务管理系统，运作方式类似于小型企业。

## 高度的隐私与安全性

### 数据存储（至关重要）
- **所有业务数据仅存储在本地**：`memory/solopreneur/`
- **客户信息受到保护**，不会被外部共享
- **不使用任何云会计服务**  
- **该系统不处理任何支付流程**  
- 用户可以完全控制数据的保留和删除

### 安全保障措施
- ✅ 可查看业务仪表盘和各项指标  
- ✅ 管理销售流程和潜在客户  
- ✅ 起草发票并跟踪付款情况  
- ✅ 对工作进行优先级排序，并定期进行周度评估  
- ❌ **严禁处理任何支付事务**  
- ❌ **严禁申报税务**  
- ❌ **严禁替代会计师或法律顾问**

### 数据结构
业务数据存储在本地：
- `memory/solopreneur/dashboard.json`：业务指标仪表盘  
- `memory/solopreneur/clients.json`：客户列表及详细信息  
- `memory/solopreneur/pipeline.json`：销售流程跟踪  
- `memory/solopreneur/invoices.json`：发票记录  
- `memory/solopreneur/reviews.json`：周度评估记录  
- `memory/solopreneur/priorities.json`：当前工作优先级  

## 核心工作流程

### 查看仪表盘  
```
User: "How's my business doing?"
→ Use scripts/dashboard.py
→ Show clients, revenue YTD, pipeline, invoices outstanding, top priorities
```

### 跟踪销售流程  
```
User: "Add new prospect to pipeline"
→ Use scripts/add_prospect.py --name "Acme Corp" --value 15000 --stage "proposal"
→ Track from lead through closed, alert if going cold
```

### 起草发票  
```
User: "Draft invoice for the website project"
→ Use scripts/draft_invoice.py --client "XYZ Inc" --project "website" --amount 5000
→ Generate complete invoice with services, terms, due date
```

### 对工作进行优先级排序  
```
User: "What should I focus on today?"
→ Use scripts/prioritize.py --time 4 --energy high
→ Review full situation, produce prioritized action list with time estimates
```

### 进行周度评估  
```
User: "Run my weekly business review"
→ Use scripts/weekly_review.py
→ Review revenue, pipeline, delivery, set top 3 priorities for next week
```

## 模块参考  
- **业务仪表盘**：请参阅 [references/dashboard.md](references/dashboard.md)  
- **销售流程管理**：请参阅 [references/pipeline.md](references/pipeline.md)  
- **发票管理**：请参阅 [references/invoicing.md](references/invoicing.md)  
- **优先级设置**：请参阅 [references/priorities.md](references/priorities.md)  
- **周度评估**：请参阅 [references/weekly-reviews.md](references/weekly-reviews.md)  
- **客户管理**：请参阅 [references/clients.md](references/clients.md)  

## 脚本参考  
| 脚本 | 功能 |
|--------|---------|
| `dashboard.py` | 显示业务仪表盘信息 |
| `add_prospect.py` | 将潜在客户添加到销售流程中 |
| `draftinvoice.py` | 起草客户发票 |
| `prioritize.py` | 对日常任务进行优先级排序 |
| `weekly_review.py` | 进行周度业务评估 |
| `log_revenue.py` | 记录收入信息 |
| `track_payment.py` | 跟踪发票付款情况 |
| `set_goal.py` | 设定业务目标 |