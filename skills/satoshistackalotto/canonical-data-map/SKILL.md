---
name: canonical-data-map
description: OpenClaw希腊会计系统中所有路径、命名规范和数据格式的统一信息来源。参考文档。
version: 1.1.0
author: openclaw-greek-accounting
homepage: https://github.com/satoshistackalotto/openclaw-greek-accounting
tags: ["greek", "accounting", "data-map", "reference"]
metadata: {"openclaw": {"requires": {"bins": [], "env": ["OPENCLAW_DATA_DIR"]}}}
---
# 标准数据目录结构图  
## OpenClaw 希腊会计系统 — v1.1  

## 设置  

本文档为参考文档，定义了所有希腊会计系统组件所使用的目录结构和命名规范。无需任何二进制文件或认证信息。  

```bash
# Set the data directory (all skills read this)
export OPENCLAW_DATA_DIR="/data"

# Initialize the full directory structure
mkdir -p $OPENCLAW_DATA_DIR/{incoming/{invoices,receipts,statements,government},processing,clients,compliance/{vat,efka,mydata,e1,e3},banking/{imports/{alpha,nbg,eurobank,piraeus},processing,reconciliation},ocr/{incoming,output},reports,auth,system/{logs,process-locks},backups}
```  

本文档详细阐述了 OpenClaw 希腊会计系统的完整文件系统架构，是所有路径决策的权威依据。任何组件在未更新本文档版本的情况下，均不得创建新的顶级目录或违反此处规定的命名规则。  

**v1.1 更新内容：** 新增了 `/data/memory/` 目录，用于存储代理的临时记忆数据、故障日志、模式学习结果、GitHub 提交队列以及速率限制状态信息。该目录由 `memory-feedback` 组件（技能 19，第 4 阶段）负责管理。所有第 3B+ 阶段的组件都必须包含写入该目录的钩子函数（用于记录代理行为和故障信息）。  

---

## 根目录结构  

```
/data/
╔══ incoming/          # All raw input — documents arriving into the system
╔══ processing/        # Temporary working space — files mid-pipeline
╔══ clients/           # Canonical client records — the source of truth
╔══ compliance/        # Government filings and submissions
╔══ banking/           # Bank statement processing pipeline
╔══ ocr/               # OCR processing pipeline
╔══ efka/              # EFKA/social security processing pipeline
╔══ reports/           # Generated reports for human consumption
╔══ exports/           # Data exports leaving the system
╔══ imports/           # Bulk data imports entering the system
╔══ dashboard/         # Dashboard state, config, cache, history
╔══ auth/              # Authentication and access control
╔══ backups/           # Encrypted system backups
╔══ gdpr-exports/      # GDPR subject access request exports
╔══ memory/            # Agent episodic memory, failure logs, learning patterns, proposals
└══ system/            # System-level files: logs, schema versions, locks
```  

---

## 1. `/data/incoming/` — 输入数据  
所有进入系统的文件首先会被存储在此目录，无论其来源如何（电子邮件附件、手动上传、扫描文件或从银行下载的文件）。`/data/incoming/` 目录中的文件目前尚未被处理。  

**文件命名规则：**  
这些文件的名称可以是任意的；系统在处理前不会更改其原始名称，以保留审计追踪的依据。只有在文件被移动到 `/data/processing/` 目录时，系统才会为其分配一个标准的名称。  

---

## 2. `/data/processing/` — 处理中的文件  
该目录用于存储处理过程中的临时文件，这些文件可能尚未完成处理。其他组件不应将 `/data/processing/` 作为数据的最终来源；应始终从 `/data/clients/` 或 `/data/compliance/` 目录获取正式的数据。  

**清理策略：**  
当文件处理完成后，`/data/processing/` 目录中的文件会被删除或归档；这些文件不会被视为系统的正式记录。  

---

## 3. `/data/clients/` — 客户数据主目录  
这是所有客户数据的唯一权威存储位置。所有需要访问客户信息的组件都必须从这里读取数据。只有 `client-data-management` 组件可以向该目录写入数据。  

**文件格式规范：**  
文件名格式为 `EL` 加 9 位数字（例如：`EL123456789`），必须包含 `EL` 前缀；严禁使用仅包含 9 位数字的文件名。  

---

## 4. `/data/compliance/` — 政府文件存储目录  
该目录用于保存提交给政府机构的文件（格式为 XML 或 PDF）。文件的元数据（如文件路径）存储在 `/data/clients/{AFM}/compliance/filings.json` 中。  

**文件命名规则：**  
文件名格式为 `{AFM}_{period}_{type}.{ext}`，其中 `type` 和 `ext` 均为小写；日期格式遵循 ISO 标准（`YYYYMM` 或 `YYYYMMDD`）。  

---

## 5. `/data/banking/` — 银行对账单处理目录  
**注意：**  
早期版本中使用的 `/data/alpha-bank/`、`/data/nbg-statements/`、`/data/eurobank/`、`/data/piraeus-bank/` 目录已被弃用。所有银行相关文件现在都应通过 `/data/banking/imports/{bank}/` 进行导入。  

---

## 6. `/data/ocr/` — OCR 处理目录  
**注意：**  
早期版本中使用的 `/data/scanned-documents/` 目录已被弃用；所有扫描后的文件现在都应存储在 `/data/ocr/incoming/scanned/` 目录中。  

---

## 7. `/data/efka/` — EFKA 处理目录  
（该目录的具体内容在文档中未详细说明，保留原英文描述。）  

## 8. `/data/reports/` — 生成的报告  
这些报告可供人类阅读，属于输出结果，而非输入数据。  

**注意：**  
`/data/reports/monthly-expenses.json`（在技能 1 中使用）已被弃用；费用相关数据应存储在 `/data/clients/{AFM}/compliance/` 或通过 `/data/exports/` 导出。  

---

## 9. `/data/exports/` — 系统输出目录  
该目录用于生成供外部使用的文件（如 Excel 导出文件、CSV 格式的文件等）。  

---

## 10. `/data/imports/` — 批量数据导入目录  
该目录用于导入结构化的数据（如客户列表、员工名单等文件），而非原始文件（原始文件应存储在 `/data/incoming/` 目录）。  

---

## 11. `/data/dashboard/` — 仪表盘数据目录  
（该目录的具体内容在文档中未详细说明，保留原英文描述。）  

## 12. `/data/auth/` — 认证与访问控制相关数据  
（该目录的具体内容在文档中未详细说明。）  

## 13. `/data/backups/` — 加密备份目录  
**文件命名规则：**  
备份文件名中必须包含日期和时间信息；加密文件扩展名为 `.enc`。加密密钥存储在 `/data/` 目录之外。  

## 14. `/data/gdpr-exports/` — GDPR 相关数据导出目录  
（该目录的具体内容在文档中未详细说明。）  

## 15. `/data/system/` — 系统配置文件目录  
（该目录的具体内容在文档中未详细说明。）  

## 16. `/data/memory/` — 代理状态数据目录  
该目录用于存储代理的临时记忆数据、故障记录、模式学习结果、GitHub 提交队列以及速率限制状态信息。所有组件都可以通过钩子函数向该目录写入数据，但只有 `memory-feedback` 组件（技能 19）可以读取这些数据。  

**日志记录规则：**  
- 任何导致决策、产生输出或与政府系统交互的代理操作都会被记录。  
- 错误、数据读取错误、数据缺失或人工干预等情况也会被记录。  
- 日志中会包含“预期应发生的情况”（`what_should_have_happened`）字段。  
- 模式扫描任务每天在雅典时间 02:00 进行一次；工作时间除外。每天最多记录 3 条日志。  
- 每天最多提交 3 个 GitHub 提交请求（PR）。  

**存储限制（默认值）：**  
- 代理行为记录：最大 500 MB，90 天后自动归档  
- 故障记录：最大 200 MB  
- 模式学习数据：最大 50 MB  
- GitHub 提交请求：最大 50 MB  
- `/data/memory/` 目录总容量上限为 2 GB；当存储空间使用率达到 90% 时，系统会停止写入操作。  

**GitHub 集成规则：**  
当故障模式满足置信度阈值（≥0.85，且出现次数≥3 次）时，`memory-feedback` 组件会在 GitHub 上创建一个新的分支，并针对相关的 SKILL.md 文件提交合并请求。必须由人工审核并完成合并操作；代理组件严禁直接推送更改到主分支。被拒绝的合并请求会被记录在日志中，相同更改不会被再次提交。  

**速率限制机制：**  
内存操作和反射操作的令牌数量与会计操作分开分配；所有内存相关操作的每日令牌上限为 5,000 个。  

---

## 全局命名规范  

### 标识符格式  
| 标识符 | 格式 | 例 | 备注 |  
| --- | --- | --- | --- |  
| AFM（增值税识别码） | `EL` 加 9 位数字 | `EL123456789` | 必须以 `EL` 开头；禁止使用仅包含 9 位数字的格式。  
| EFKA 雇主 ID | 8 位数字 | `12345678` | 无前缀 |  
| GEMI（希腊税务识别码） | 9–12 位数字 | `012345678` | 可包含前导零 |  
| 联系人 ID | `C` 加 3 位数字 | `C001` | 按客户顺序生成 |  
| 文件 ID | `D` 加 6 位数字 | `D000123` | 全局唯一编号 |  
| 审计事件 ID | `AUD-{YYYYMMDD}-{6digits}` | `AUD-20260218-001234` |  
| 备份 ID | `{type}_{YYYYMMDD}_{HHMMSS}` | `clients_20260218_143022` |  
| 事件 ID | `EP-{YYYYMMDD}-{3digits}` | `EP-20260218-001` | 每日唯一编号 |  
| 故障 ID | `FAIL-{YYYYMMDD}-{3digits}` | `FAIL-20260218-003` | 每日唯一编号 |  
| 模式 ID | `PAT-{YYYYMMDD}-{3digits}` | `PAT-20260218-007` | 检测时生成 |  
| 更正 ID | `COR-{YYYYMMDD}-{3digits}` | `COR-20260218-001` | 人工分配 |  
| 会话 ID | `S{YYYYMMDD}-{3digits}` | `S20260218-001` | 每次会话唯一编号 |  

### 日期和时间格式  
| 使用场景 | 格式 | 例 | 备注 |  
| 文件名 | `YYYYMMDD` | `20260218` | 文件名中不含分隔符 |  
| 带时间戳的文件名 | `YYYYMMDD_HHMMSS` | `20260218_143022` |  
| 周期引用 | `YYYY-MM` | `2026-01` | 表示月份周期 |  
| JSON 格式的日期时间 | `YYYY-MM-DDTHH:MM:SSZ` | 存储时使用 UTC 格式 |  
| 用户显示格式 | `DD/MM/YYYY` | 希腊语日期格式 |  
| CLI 参数 `--date` | `YYYY-MM-DD` | CLI 参数使用 ISO 格式 |  
| CLI 参数 `--period` | `YYYY-MM` | `YYYY-MM` | 使用 ISO 格式 |  

### 货币单位  
- **JSON 存储格式**：数值类型，保留 2 位小数 | `12500.00` | 存储值中禁止使用 € 符号 |
- **文件名**：仅使用数字格式 | `12500` | 文件名中仅存储整数金额 |
- **用户显示格式**：`€XX,XXX.XX` | 使用欧盟标准的货币格式 |  
- **CLI 输出**：`EUR XX,XXX.XX` | 保证终端显示格式的准确性 |

### 文件命名规则  
文件名格式为 `{AFM}_{YYYY-MM}_{type}_{optional-detail}.{ext}`  
示例：  
- `EL123456789_2026-01_vat_return.xml`  
- `EL123456789_2026-2_reconciliation_report.pdf`  
- `EL123456789_2025_e1_form.xml`  
- `EL123456789_2026-2_payslip_nikos-papadopoulos.pdf`  

**命名规则：**  
- `type` 和 `detail` 部分使用小写  
- 部分之间使用连字符（禁止使用下划线）  
- 文件名中不允许出现空格  
- 文件名中禁止使用希腊字母；员工姓名需使用拉丁转写形式  
- 文件名中仅允许使用连字符和下划线  

### 员工姓名的文件名规范  
希腊姓名在文件名中需转换为 ASCII 小写格式，并使用连字符连接：  
- `Îίκος Παπαδόπουλος` → `nikos-papadopoulos`  
- `ΜαÏία Κωνσταντίνου` → `maria-konstantinou`  
- `ΔήμητÏα ΚαλαμαÏά` → `dimitra-kalamara`  

---

## 已弃用的路径  
以下路径仅存在于早期版本中，新版本中禁止使用；如果在现有代码中遇到这些路径，请将其视为指向标准路径的别名：  
| 已弃用路径 | 标准替换路径 |  
| --- | --- |  
| `/data/alpha-bank/` | `/data/banking/imports/alpha/` |  
| `/data/nbg-statements/` | `/data/banking/imports/nbg/` |  
| `/data/eurobank/` | `/data/banking/imports/eurobank/` |  
| `/data/piraeus-bank/` | `/data/banking/imports/piraeus/` |  
| `/data/bank-imports/` | `/data/banking/imports/` |  
| `/data/scanned-documents/` | `/data/ocr/incoming/scanned/` |  
| `/data/email-attachments` | `/data/incoming/`（用于分类文件） |  
| `/data/email-imports/` | `/data/incoming/` |  
| `/data/invoices` | `/data/incoming/invoices/`（原始文件）或 `/data/clients/{AFM}/documents/`（处理后的文件） |  
| `/data/processed/invoices/` | `/data/clients/{AFM}/documents/` + 注册表记录 |  
| `/data/processed/receipts/` | `/data/clients/{AFM}/documents/` + 注册表记录 |  
| `/data/processed/E1_2025.pdf` | `/data/compliance/e1/EL{AFM}_2025_e1_form.xml` |  
| `/data/processing/classification` | `/data/processing/classification/` |  
| `/data/processing/extraction` | `/data/processing/ocr/extracted/` |  
| `/data/processing/validation` | `/data/processing/ocr/validated/` |  
| `/data/reports/monthly-expenses.json` | `/data/clients/{AFM}/compliance/` 或 `/data/exports/` |  
| `/data/payroll/monthly.xlsx` | `/data/efka/payroll/input/` 或 `/data/clients/{AFM}/payroll/` |  
| `/data/export/accounting-software` | `/data/exports/accounting-software/` |  
| `/data/aade-downloads/` | `/data/incoming/government/` |  
| `/data/aade-outputs/` | `/data/reports/` 或 `/data/compliance/`（按类型分类） |  
| `/data/aade-processing/` | `/data/processing/compliance/` |  
| `/data/compliance-updates/` | `/data/incoming/government/` |  

## 各组件的职责  
以下表格说明了每个组件负责写入哪些顶级目录：  
| 目录 | 负责写入的组件 | 其他组件可读取的目录 |  
| --- | --- | --- |  
| `/data/incoming/` | `accounting-workflows` | 所有组件 |  
| `/data/processing/` | 处理数据的组件 | 该目录为临时存储区，非最终数据来源 |  
| `/data/clients/` | `client-data-management` | 所有组件（仅可读取） |  
| `/data/compliance/` | `greek-compliance-aade` | `aade-api-monitor`、`efka-api-integration`、`dashboard` |  
| `/data/banking/` | `greek-banking-integration` | `accounting-workflows`、`dashboard` |  
| `/data/ocr/` | `greek-document-ocr` | `accounting-workflows`、`greek-email-processor` |  
| `/data/efka/` | `efka-api-integration` | `greek-compliance-aade`、`dashboard` |  
| `/data/reports/` | `dashboard-greek-accounting` | 所有组件（可读取） |  
| `/data/reports/analytics/` | `analytics-and-advisory-intelligence` | `conversational-ai-assistant`、`dashboard-greek-accounting` |  
| `/data/reports/system/` | `system-integrity-and-backup` | `dashboard-greek-accounting`（可读取） |  
| `/data/clients/{AFM}/financial-statements/` | `greek-financial-statements` | `conversational-ai-assistant`、`client-communication-engine`、`analytics-and-advisory-intelligence` |  
| `/data/clients/{AFM}/correspondence/` | `client-communication-engine` | `conversational-ai-assistant`、`analytics-and-advisory-intelligence` |  
| `/data/processing/comms/` | `client-communication-engine` | 临时生成的草稿文件，发送后会被清除 |  
| `/data/backups/` | `system-integrity-and-backup` | 所有组件可通过元技能触发备份操作 |  
| `/data/system/integrity/` | `system-integrity-and-backup` | 所有组件可在写入文件时生成哈希值 |  
| `/data/exports/` | 任何使用 `--export` 参数的组件 | 外部接收者 |  
| `/data/imports/` | `client-data-management` | `efka-api-integration` |  
| `/data/dashboard/` | `dashboard-greek-accounting` | `user-authentication-system` |  
| `/data/auth/` | `user-authentication-system` | 所有组件（用于身份验证） |  
| `/data/gdpr-exports/` | `client-data-management` | 无 |  
| `/data/system/` | OpenClaw 系统 | 所有组件（可读取） |  
| `/data/memory/` | `memory-feedback`（技能 19） | 所有组件可写入数据；仅 `memory-feedback` 组件可读取数据用于分析 |  

## 所有组件的通用规则  
1. 在修改 `/data/` 目录下的结构之前，必须先更新本文档。  
2. 处理后的数据或正式数据严禁写入 `/data/processing/` 目录（该目录为临时存储区）。  
3. 客户数据必须存储在 `/data/clients/` 目录中；`client-data-management` 组件负责写入数据。  
4. 所有路径、文件名和 JSON 键中必须使用完整的 AFM 格式（`EL` 前缀 + 9 位数字）。  
5. 文件名和 JSON 数据中必须使用 ISO 日期格式（`YYYY-MM-DD` 或 `YYYYMMDD`）。  
6. 文件名和目录名中禁止使用希腊字母；JSON 数据中仅允许使用数字格式。  
7. JSON 数据中的货币值必须为数值类型（禁止使用 € 符号）。  
8. JSON 中的时间戳必须使用 UTC 格式；显示时需转换为希腊时间格式（`Europe/Athens`）。  
9. `/data/processing/` 目录中的数据为临时数据；其他组件不得将其视为数据的最终来源。  
10. 已弃用的路径仅限读取，禁止在新版本中创建新文件。  

## 统一的审计事件记录规范  
所有组件必须使用统一的 JSON 格式记录重要操作。审计事件会被写入 `/data/system/logs/audit/` 目录，作为监管检查的权威记录。  

**所有事件必须包含的字段：** `event_id`、`timestamp`、`skill`、`action`、`category`、`user.username`、`user.role`、`result`。  
**可选字段：`client`、`details`、`before_state`、`after_state`、`approval`、`data_classification`。**  

**事件分类示例：**  
- `governmentsubmission`：提交给 AADE、EFKA 或 myDATA 的文件  
- `data_modification`：创建、更新或删除客户记录  
- `access_event`：登录、登出、会话活动、访问拒绝  
- `document_processing`：OCR 处理、文件分类、数据提取、验证  
- `financial_output`：生成对账单、修改数据、创建报告  
- `communication`：发送给客户的通信文件  
- `system_operation`：备份操作、完整性检查、模式迁移  
- `security_event`：账户锁定、双因素认证失败、会话撤销、权限变更  

**存储要求：**  
审计日志按照希腊税法和欧盟法规（EU Regulation 2016/679）要求保存 10 年。  

## 加密要求  
在生产环境中，包含敏感数据的目录必须进行加密处理（符合 GDPR 规定，具体要求见希腊法律 4624/2019）。  

### 需要加密的目录  
| 目录 | 数据分类 | 加密要求 | 备注 |  
| --- | --- | --- | --- |  
| `/data/auth/` | 限制级数据 | **强制加密** | 包含凭证哈希值、会话数据、双因素认证密钥 |  
| `/data/clients/` | 机密数据 | **强制加密** | 包含财务记录和个人身份信息（如姓名、AFM、IBAN） |  
| `/data/compliance/` | 机密数据 | **强制加密** | 包含财务数据 |  
| `/data/efka/` | 机密数据 | **强制加密** | 包含员工个人信息和薪资信息 |  
| `/data/banking/` | 机密数据 | **建议加密** | 包含银行对账单和账户号码 |  
| `/data/backups/` | 机密数据 | **已加密** | 使用 AES-256 算法（由技能 17 负责加密） |  
| `/data/gdpr-exports/` | 机密数据 | **强制加密** | 包含用户访问请求相关数据 |  
| `/data/processing/` | 内部数据 | **可选加密** | 临时数据，处理完成后会被删除 |  
| `/data/reports/` | 内部数据 | **建议加密** | 可能包含客户财务摘要 |  
| `/data/system/` | 内部数据 | **可选加密** | 包含日志和操作数据 |  

### 数据分类标签  
存储在加密目录中的所有 JSON 数据记录都必须包含 `data_classification` 字段，有效值包括 `public`、`internal`、`confidential`、`restricted`。  
该字段有助于在 GDPR 数据泄露事件发生时快速确定数据泄露的类型（72 小时内必须上报）。  

## 专业责任免责声明模板  
系统生成的面向客户的文档必须包含此免责声明；生成客户可见输出的组件（技能 15、16、18）必须在输出文件中附加此声明。  

### 标准免责声明（希腊语/英语）  
（具体内容在文档中未提供。）  

### 使用规则  
- **财务报告**（技能 15）：PDF 文件的页脚中需同时包含希腊语和英语免责声明。  
- **客户通信文件**（技能 16）：电子邮件页脚中需包含希腊语免责声明。  
- **咨询报告**（技能 18）：内部报告中需包含英语免责声明；面向客户的文件中需包含希腊语免责声明。  
- **政府提交文件**：提交给 AADE/EFKA 的文件不包含免责声明（这些文件为正式提交文件，非咨询文件）。  

## 输入数据验证规则  
所有组件在处理数据前必须验证输入数据的合法性；无效数据必须被拒绝，并附带清晰的错误信息。  

### 其他验证规则  
（具体验证规则在文档中未详细说明。）