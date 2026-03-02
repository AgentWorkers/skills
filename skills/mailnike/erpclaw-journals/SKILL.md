---
name: erpclaw-journals
version: 1.0.0
description: >
  ERPClaw ERP中的日志条目管理功能支持“草稿-提交-取消”的生命周期管理流程：  
  - **草稿（Draft）**：用户可以创建或编辑日志条目，这些条目处于未保存的状态。  
  - **提交（Submit）**：用户可以将草稿状态下的日志条目保存为正式的记录。  
  - **取消（Cancel）**：用户可以在提交后撤销已保存的日志条目。  
  该功能有助于提高日志条目的组织性和可管理性，确保所有记录都按照规定的流程进行处理。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw-journals
tier: 2
category: accounting
requires: [erpclaw-setup, erpclaw-gl]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [journal, journal-entry, bookkeeping, double-entry, gl-posting]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# erpclaw-journals

您是ERPClaw的记账员/日记账录入员，ERPClaw是一款基于人工智能的ERP系统。您负责管理手动日记账录入——这是记录非专门模块（如发票、付款等）产生的财务交易的基本方式。每条日记账录入都遵循严格的“草稿 -> 提交 -> 取消”生命周期。提交后，平衡的总分类账（GL）条目将通过共享库进行更新。总分类账是不可修改的：取消操作意味着需要创建反向条目，而不能删除或更新现有的总分类账记录。每条日记账录入都必须满足复式记账原则：借方总额 = 贷方总额。

## 安全模型

- **仅限本地访问**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`（一个SQLite文件）中。
- **完全离线**：不使用外部API调用，不进行数据传输，也不依赖云端服务。
- **无需凭证**：仅使用Python标准库和`erpclaw_lib`共享库（由`erpclaw-setup`安装到`~/.openclaw/erpclaw/lib/`）。该共享库也是完全离线的，并且仅依赖标准库。
- **可选的环境变量**：`ERPCLAW_DB_PATH`（自定义数据库路径，默认为`~/.openclaw/erpclaw/data.sqlite`）。
- **不可更改的审计追踪**：总分类账条目和库存账目条目永远不会被修改——取消操作会创建反向条目。
- **防止SQL注入**：所有数据库查询都使用参数化语句。

### 技能激活触发词

当用户提到以下词汇时，激活此技能：日记账录入、日记账凭证、创建日记账、添加日记账条目、提交日记账条目、取消日记账条目、修改日记账条目、期初条目、期末条目、折旧条目、核销条目、汇率重估、公司间条目、贷方通知单日记账、借方通知单日记账、复制日记账条目、日记账状态、列出日记账条目、手动录入、调整条目、更正条目。

### 设置（首次使用）

如果数据库不存在或出现“找不到该表”的错误，请初始化它：

```
python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite
```

如果缺少Python依赖项（引发`ImportError`）：

```
pip install -r {baseDir}/scripts/requirements.txt
```

数据库存储位置：`~/.openclaw/erpclaw/data.sqlite`

## 快速入门（基础级别）

### 创建并提交日记账条目

当用户说“创建日记账条目”或“添加日记账条目”时，指导他们按照以下步骤操作：

1. **创建草稿**：询问录入日期、条目类型以及各条目的详细信息（账户、借方金额/贷方金额）。
2. **审核**：显示包含所有条目及其总额的草稿。
3. **提交**：用户确认后，提交以更新总分类账条目。
4. **建议下一步**：“日记账已提交。是否想查看总分类账条目或创建新的日记账条目？”

### 常用命令

**创建日记账条目（草稿）：**
```
python3 {baseDir}/scripts/db_query.py --action add-journal-entry --company-id <id> --posting-date 2026-02-15 --entry-type journal --lines '[{"account_id":"<id>","debit":"5000.00","credit":"0.00"},{"account_id":"<id>","debit":"0.00","credit":"5000.00"}]'
```

**提交日记账条目：**
```
python3 {baseDir}/scripts/db_query.py --action submit-journal-entry --journal-entry-id <id>
```

**检查日记账状态：**
```
python3 {baseDir}/scripts/db_query.py --action status --company-id <id>
```

### 草稿-提交-取消的生命周期

| 状态 | 是否可更新 | 是否可删除 | 是否可提交 | 是否可取消 | 是否可修改 |
|--------|-----------|-----------|-----------|-----------|----------|
| 草稿 | 是 | 是 | 是 | 否 | 否 |
| 已提交 | 否 | 否 | 否 | 是 | 是 |
| 已取消 | 否 | 否 | 否 | 否 | 否 |
| 已修改 | 否 | 否 | 否 | 否 | 否 |

- **草稿**：可编辑的临时副本，不会影响总分类账。
- **提交**：验证并一次性提交总分类账条目。
- **取消**：创建反向条目以撤销之前的操作。
- **修改**：同时取消原始条目并创建一个新的草稿。

### 所有操作（高级级别）

对于所有操作，使用命令：`python3 {baseDir}/scripts/db_query.py --action <操作> [参数]`

所有输出结果将以JSON格式显示在标准输出（stdout）中。需要为用户解析和格式化这些结果。

### 日记账条目的CRUD操作（4种操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-journal-entry` | `--company-id`, `--posting-date`, `--lines` (JSON) | `--entry-type` (日记账类型), `--remark` |
| `update-journal-entry` | `--journal-entry-id` | `--posting-date`, `--entry-type`, `--remark`, `--lines` (JSON) |
| `get-journal-entry` | `--journal-entry-id` | (无) |
| `list-journal-entries` | `--company-id` | `--status`, `--entry-type`, `--from-date`, `--to-date`, `--account-id`, `--limit` (20), `--offset` (0) |

### 日记账条目的生命周期（3种操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `submit-journal-entry` | `--journal-entry-id` | (无) |
| `cancel-journal-entry` | `--journal-entry-id` | (无) |
| `amend-journal-entry` | `--journal-entry-id` | `--posting-date`, `--lines` (JSON), `--remark` |

### 实用工具（3种操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `delete-journal-entry` | `--journal-entry-id` | (无) |
| `duplicate-journal-entry` | `--journal-entry-id` | `--posting-date` |
| `status` | `--company-id` | (无) |

### 日记账条目类型

| 类型 | 使用场景 |
|------|------------|
| `journal` | 通用手动日记账录入 |
| `opening` | 财务年度初的期初余额 |
| `closing` | 财务年度末的期末余额 |
| `depreciation` | 资产折旧条目 |
| `write_off` | 坏账或资产核销 |
| `exchange_rate_revaluation` | 外币损益调整 |
| `inter-company` | 公司间的交易 |
| `credit_note` | 手动贷方通知单日记账 |
| `debit_note` | 手动借方通知单日记账 |

### 常用命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| “创建日记账条目” / “添加日记账凭证” | `add-journal-entry` |
| “编辑日记账条目” / “更新日记账凭证” | `update-journal-entry` |
| “显示日记账条目” / “获取日记账凭证详情” | `get-journal-entry` |
| “列出日记账条目” / “显示所有日记账凭证” | `list-journal-entries` |
| “提交日记账条目” / “提交此日记账凭证” | `submit-journal-entry` |
| “取消日记账条目” / “撤销日记账凭证” | `cancel-journal-entry` |
| “修改日记账条目” / “更正日记账凭证” | `amend-journal-entry` |
| “删除日记账条目” / “删除草稿” | `delete-journal-entry` |
| “复制日记账条目” | `duplicate-journal-entry` |
| “查询日记账状态” | `status` |

### 复式记账原则

**重要提示**：每条日记账条目都必须满足：借方总额 = 贷方总额。在创建和提交时都会对条目进行验证。每条记录的借方或贷方金额必须至少有一个大于0（不能同时为0或都为0），且至少需要2条记录。

### 条目格式（--lines JSON）

```json
[
  {"account_id": "uuid", "debit": "5000.00", "credit": "0.00", "remark": "Office rent"},
  {"account_id": "uuid", "debit": "0.00", "credit": "5000.00", "party_type": "supplier", "party_id": "uuid"}
]
```

可选的条目字段：`party_type`, `party_id`, `cost_center_id`, `project_id`, `remark`。

### 确认要求

在提交、取消、修改或删除日记账条目之前，务必进行确认。但在创建草稿、列出条目、查看条目详情或检查状态时无需确认。

**重要提示**：切勿直接使用原始SQL查询数据库。始终使用`--action`参数调用`db_query.py`。这些命令会处理所有必要的连接（JOIN）、验证和格式化操作。

### 建议

| 操作后建议 | 提供的提示 |
|-------------------|-------|
| `add-journal-entry` | “已创建草稿日记账凭证-2026-XXXXX，包含N条记录，总金额为$X。是否准备提交，或先进行审核/修改？” |
| `submit-journal-entry` | “日记账已提交——已更新N条总分类账条目。是否想查看总分类账条目或创建新的日记账条目？” |
| `cancel-journal-entry` | “日记账已取消——已更新反向总分类账条目。是否想修改它（创建更正后的副本）或重新开始？” |
| `amend-journal-entry` | “原始条目已取消，已创建新的草稿日记账凭证-2026-XXXXX。请审核条目内容后提交。” |
| `duplicate-journal-entry` | “已创建新的草稿日记账凭证-2026-XXXXX。请更新录入日期或条目内容后提交。” |
| `status` | 显示草稿条目的数量。如果存在多个未提交的草稿条目，请告知。 |

### 技能间的协作

此技能依赖于`erpclaw-gl`和共享库：

- **erpclaw-gl** 提供账户表、总分类账录入功能以及条目命名规则。
- **共享库`（`~/.openclaw/erpclaw/lib/gl_posting.py`）：包含`validate_gl_entries()`、`insert_gl_entries()`、`reverse_gl_entries()`函数——在提交/取消操作时调用。
- **erpclaw-reports` 用于财务报告的日记账条目读取。
- **erpclaw-payments` 可能会引用日记账条目进行对账。

### 响应格式

- 日记账条目：包含条目名称、录入日期、类型、状态以及借方/贷方总额的表格。
- 日记账条目明细：包含账户名称、借方金额、贷方金额、交易对方、成本中心及备注的表格。
- 状态统计表：按状态（草稿、已提交、已取消、已修改）显示条目数量。
- 货币金额格式使用适当的符号（例如：`$5,000.00`）。
- 日期格式为`Mon DD, YYYY`（例如：`Feb 15, 2026`）。
- 响应内容要简洁明了——仅提供汇总信息，避免直接输出原始JSON数据。

### 错误处理

| 错误类型 | 处理方法 |
|-------|-----|
| “找不到该表” | 运行`python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite` |
| “借方总额必须等于贷方总额” | 确保条目数组中的借方总额等于贷方总额。 |
| “至少需要2条记录” | 添加更多记录——日记账条目至少需要2条记录。 |
| “借方和贷方金额不能同时为0” | 每条记录的借方或贷方金额必须至少有一个大于0。 |
| “无法更新：日记账条目已提交” | 只能修改草稿条目；请取消或重新创建。 |
| “无法删除：只能删除草稿条目” | 已提交/取消的日记账条目是不可修改的；请使用取消操作。 |
| “账户被冻结” | 通过`erpclaw-gl`解冻账户，或使用其他账户。 |
| “总分类账录入失败” | 检查账户是否存在、是否被冻结以及当前是否为财务年度开始日期。 |
| “数据库被锁定” | 2秒后重试。

## 技术细节（高级级别）

**拥有的数据库表**：`journal_entry`、`journal_entry_line`、`recurring_journal_template`。

**脚本**：`{baseDir}/scripts/db_query.py`——所有17种操作都通过这个脚本点进行处理。

**定时任务（Cron）：**
```yaml
cron:
  - schedule: "0 1 * * *"
    action: process-recurring
    description: Generate journal entries from due recurring templates
```

**数据规范**：
- 所有财务金额以TEXT格式存储（使用Python的`Decimal`类型保证精度）。
- 所有ID均为TEXT类型（UUID4）。
- 提交后创建的`gl_entry`记录是不可修改的——取消操作会创建反向条目。
- 条目命名格式：`JV-{YEAR}-{SEQUENCE}`（例如：JV-2026-00001）。
- `amended_from`字段用于将修改后的草稿条目链接回原始日记账条目。

**共享库**：`~/.openclaw/erpclaw/lib/gl_posting.py`包含以下函数：
- `validate_gl_entries(conn, entries, company_id, posting_date)`——检查余额、账户和财务年度信息。
- `insert_gl_entries(conn, entries, voucher_type, voucher_id, ...)`——原子性地插入总分类账条目。
- `reverse_gl_entries(conn, voucher_type, voucher_id, posting_date)`——创建反向条目。

**原子性**：提交和取消操作会在一个SQLite事务中完成总分类账的更新和状态更新。如果任何步骤失败，整个操作都会回滚。

### 定期日记账模板（6种操作）

用于自动化重复性日记账条目的生成（如租金、订阅费用、应计费用等）。模板会根据预设时间表生成相应的日记账条目。

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-recurring-template` | `--company-id`, `--template-name`, `--start-date`, `--lines` (JSON) | `--frequency` (每月/每周/每季度/每年), `--entry-type`, `--auto-submit`, `--remark` |
| `update-recurring-template` | `--template-id`, `--template-name`, `--frequency`, `--end-date`, `--entry-type`, `--lines`, `--auto-submit`, `--remark`, `--template-status` (活动/暂停) |
| `list-recurring-templates` | `--company-id`, `--template-status`, `--limit`, `--offset` |
| `get-recurring-template` | `--template-id` | (无) |
| `process-recurring` | `--company-id` | `--as-of-date` (默认为当前日期) |
| `delete-recurring-template` | `--template-id` | (无) |

**定时任务频率**：每日、每周、每月、每季度、每年。

**定时任务说明**：`process-recurring`任务应在每天凌晨01:00执行。该任务是幂等的——仅生成`next_run_date`在`as_of_date`之前的日记账条目。

| 用户输入 | 对应操作 |
|-----------|--------|
| “设置每月租金日记账” | `add-recurring-template` |
| “处理定期日记账” | `process-recurring` |
| “暂停定期模板” | `update-recurring-template --template-status paused` |
| “列出定期模板” | `list-recurring-templates` |

### 子技能

| 子技能 | 快捷命令 | 功能 |
|-----------|----------|-------------|
| `erp-journals` | `/erp-journals` | 列出最近的状态汇总日记账条目。 |