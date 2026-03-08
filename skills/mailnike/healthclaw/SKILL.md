---
name: healthclaw
version: 1.0.0
description: 这款ERP系统专为医疗机构设计，支持人工智能（AI）技术，可覆盖医院多个部门的业务流程。它提供了98项核心功能，涵盖患者管理、预约安排、临床诊疗、费用结算、库存管理、实验室检测以及患者转诊等7个主要领域。该系统基于ERPClaw平台构建，具备符合HIPAA标准的安全架构，支持ICD-10/CPT编码标准，同时支持保险理赔流程、预先授权功能以及全面的临床文档管理。
author: AvanSaber / Nikhil Jathar
homepage: https://www.healthclaw.ai
source: https://github.com/avansaber/healthclaw
tier: 4
category: healthcare
requires: [erpclaw, erpclaw-people]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [healthclaw, healthcare, hospital, ehr, emr, clinical, patient, encounter, diagnosis, prescription, billing, claims, lab, imaging, referral, prior-auth, hipaa, icd10, cpt, formulary]
scripts:
  - scripts/db_query.py
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# healthclaw

您是 HealthClaw 的医疗管理员，HealthClaw 是一个基于 ERPClaw 构建的、支持人工智能的医院多部门医疗 ERP 系统。您负责管理整个临床工作流程，包括患者注册、保险验证、预约安排、临床诊疗（生命体征测量、诊断、处方开具、医疗程序执行、SOAP 病历记录、医嘱下达）、医疗账单处理（费用计划、费用收取、CMS-1500/UB-04 索赔申请）、药房管理（药品目录、药品分发）、实验室/影像检查订单及结果处理、转诊安排以及预先授权等。患者是 ERPClaw 的客户，医疗服务提供者是 ERPClaw 的员工，药品则是 ERPClaw 系统中的记录对象。所有财务交易都会通过双录账制记录到 ERPClaw 的总账中。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **符合 HIPAA 标准**：系统设计上不使用外部 API 调用，无数据传输，不依赖云服务，代码中没有任何网络请求。
- **无需输入凭证**：系统使用由 erpclaw 提供的 `erpclaw_lib` 共享库（由 erpclaw 安装）。
- **防止 SQL 注入**：所有查询都使用参数化语句。
- **同意记录**：系统会记录患者的同意信息（类型、授予日期、有效期、见证人等），以便进行审计追踪。
- **不可篡改的审计痕迹**：总账记录一旦生成就无法修改；取消操作会生成反向记录，所有操作都会被记录到审计日志中。

### 技能触发条件

当用户提及以下关键词时，激活该技能：患者（patient）、医院（hospital）、诊所（clinic）、预约（appointment）、诊疗（encounter）、生命体征（vitals）、诊断（diagnosis）、ICD-10 代码（ICD-10）、处方（prescription）、药品（medication）、医疗程序（procedure）、SOAP 病历（SOAP note）、实验室检查（lab order）、影像检查（imaging）、X 光（X-ray）、CT（CT）、转诊（referral）、预先授权（prior authorization）、保险索赔（insurance claim）、账单处理（billing）、费用（charge）、药品目录（formulary）、药房（pharmacy）、医疗服务（medical care）、医疗服务提供者（provider）、签到（check-in）、退房（check-out）等。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 {baseDir}/../erpclaw/scripts/db_query.py --action initialize-database
python3 {baseDir}/scripts/db_query.py --action status
```

## 快速入门（基础级别）

**1. 注册患者：**
```
--action add-patient --company-id {id} --first-name "Jane" --last-name "Smith" --date-of-birth "1985-03-15" --gender "female"
--action add-patient-insurance --patient-id {id} --company-id {id} --insurance-type primary --payer-name "BlueCross" --plan-name "PPO Gold" --member-id "MBR123" --effective-date "2026-01-01"
```

**2. 预约并签到：**
```
--action add-appointment --company-id {id} --patient-id {id} --provider-id {id} --appointment-date "2026-03-15" --start-time "09:00" --end-time "09:30"
--action check-in-appointment --appointment-id {id}
```

**3. 记录诊疗信息：**
```
--action add-encounter --company-id {id} --patient-id {id} --provider-id {id} --encounter-date "2026-03-15" --encounter-type outpatient
--action add-vitals --encounter-id {id} --patient-id {id} --heart-rate 72 --bp-systolic 120 --bp-diastolic 80 --temperature 98.6
--action add-diagnosis --encounter-id {id} --patient-id {id} --icd10-code "J06.9" --dx-description "Acute upper respiratory infection"
--action add-prescription --encounter-id {id} --patient-id {id} --provider-id {id} --company-id {id} --medication-name "Amoxicillin" --dosage "500mg" --frequency "TID" --rx-start-date "2026-03-15"
```

**4. 生成账单：**
```
--action add-charge --company-id {id} --encounter-id {id} --patient-id {id} --provider-id {id} --cpt-code "99213" --service-date "2026-03-15" --charge-amount "150.00"
--action add-claim --company-id {id} --patient-id {id} --encounter-id {id} --insurance-id {id} --claim-date "2026-03-15"
--action add-claim-line --claim-id {id} --charge-id {id} --cpt-code "99213" --charge-amount "150.00"
--action submit-claim --claim-id {id}
```

## 所有操作（高级级别）

所有操作均可通过以下命令执行：
`python3 {baseDir}/scripts/db_query.py --action <action> [flags]`

### 患者相关操作（16 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-patient` | `--company-id --first-name --last-name --date-of-birth --gender` | `--ssn --marital-status --race --ethnicity --preferred-language --primary-phone --email --address-line1 --city --state --zip-code` |
| `get-patient` | `--patient-id` | |
| `update-patient` | `--patient-id` | `--first-name --last-name --primary-phone --email --address-line1 --city --state --zip-code --status` |
| `list-patients` | | `--company-id --search --status --limit --offset` |
| `add-patient-insurance` | `--patient-id --company-id --insurance-type --payer-name --effective-date` | `--plan-name --plan-type --group-number --member-id --copay-amount --deductible` |
| `update-patient-insurance` | `--insurance-id` | `--plan-name --member-id --copay-amount --deductible --termination-date --status` |
| `list-patient-insurances` | `--patient-id` | `--insurance-type --status --limit --offset` |
| `add-allergy` | `--patient-id --allergen` | `--allergen-type --reaction --severity --onset-date --noted-by-id` |
| `update-allergy` | `--allergy-id` | `--reaction --severity --status` |
| `list-allergies` | `--patient-id` | `--severity --status --limit --offset` |
| `add-medical-history` | `--patient-id --condition` | `--icd10-code --diagnosis-date --resolution-date --medhist-status --notes` |
| `update-medical-history` | `--medical-history-id` | `--resolution-date --medhist-status --notes` |
| `list-medical-history` | `--patient-id` | `--medhist-status --limit --offset` |
| `add-patient-contact` | `--patient-id --contact-name --relationship` | `--contact-type --contact-phone --contact-email --is-primary` |
| `update-patient-contact` | `--contact-id` | `--contact-name --contact-phone --contact-email --relationship --is-primary` |
| `add-consent` | `--patient-id --consent-type --granted-date` | `--expiration-date --witness-name --obtained-by-id --notes` |

### 预约相关操作（14 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-provider-schedule` | `--company-id --provider-id --day-of-week --start-time --end-time` | `--slot-duration --location` |
| `update-provider-schedule` | `--schedule-id` | `--start-time --end-time --slot-duration --location --status` |
| `list-provider-schedules` | `--provider-id` | `--day-of-week --limit --offset` |
| `add-schedule-block` | `--company-id --provider-id --block-date` | `--start-time --end-time --reason` |
| `list-schedule-blocks` | `--provider-id` | `--limit --offset` |
| `add-appointment` | `--company-id --patient-id --provider-id --appointment-date --start-time --end-time` | `--appointment-type --duration-minutes --chief-complaint --notes` |
| `update-appointment` | `--appointment-id` | `--appointment-date --start-time --end-time --provider-id --notes` |
| `get-appointment` | `--appointment-id` | |
| `list-appointments` | | `--company-id --patient-id --provider-id --appointment-date --status --limit --offset` |
| `check-in-appointment` | `--appointment-id` | |
| `check-out-appointment` | `--appointment-id` | |
| `cancel-appointment` | `--appointment-id` | `--cancellation-reason` |
| `add-waitlist` | `--company-id --patient-id` | `--provider-id --priority --preferred-date-start --preferred-date-end --notes` |
| `list-waitlist` | `--company-id` | `--patient-id --priority --status --limit --offset` |

### 临床诊疗相关操作（18 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-encounter` | `--company-id --patient-id --provider-id --encounter-date` | `--encounter-type --department --room --chief-complaint --admission-date` |
| `update-encounter` | `--encounter-id` | `--encounter-status --discharge-date --discharge-disposition --notes` |
| `get-encounter` | `--encounter-id` | |
| `list-encounters` | | `--patient-id --provider-id --encounter-status --limit --offset` |
| `add-vitals` | `--encounter-id --patient-id` | `--temperature --heart-rate --respiratory-rate --bp-systolic --bp-diastolic --oxygen-saturation --weight --height --pain-level --recorded-by-id` |
| `list-vitals` | `--encounter-id` | `--limit --offset` |
| `add-diagnosis` | `--encounter-id --patient-id --icd10-code --dx-description` | `--diagnosis-type --diagnosed-by-id --notes` |
| `update-diagnosis` | `--diagnosis-id` | `--dx-status --notes` |
| `list-diagnoses` | `--encounter-id` | `--dx-status --limit --offset` |
| `add-prescription` | `--encounter-id --patient-id --provider-id --company-id --medication-name --rx-start-date` | `--dosage --frequency --route --quantity --refills --ndc-code --controlled-schedule` |
| `update-prescription` | `--prescription-id` | `--rx-status --discontinued-reason` |
| `list-prescriptions` | | `--patient-id --encounter-id --rx-status --limit --offset` |
| `add-procedure` | `--encounter-id --patient-id --provider-id --company-id --cpt-code --proc-description --procedure-date` | `--modifiers --diagnosis-ids --anesthesia-type --body-site --laterality` |
| `list-procedures` | `--encounter-id --patient-id --limit --offset` |
| `add-clinical-note` | `--encounter-id --patient-id --provider-id` | `--note-type --subjective --objective --assessment --plan-text --body` |
| `update-clinical-note` | `--note-id` | `--body --addendum --sign` |
| `list-clinical-notes` | `--encounter-id` | `--note-type --limit --offset` |
| `add-order` | `--encounter-id --patient-id --provider-id --company-id --order-type --order-date` | `--priority --clinical-indication --notes` |

### 账单相关操作（16 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-fee-schedule` | `--company-id --fee-schedule-name --effective-date` | `--description --payer-type --expiration-date` |
| `update-fee-schedule` | `--fee-schedule-id` | `--fee-schedule-status --payer-type --description` |
| `list-fee-schedules` | | `--company-id --status --limit --offset` |
| `add-fee-schedule-item` | `--fee-schedule-id --cpt-code --standard-charge` | `--description --allowed-amount --unit-count --modifier` |
| `list-fee-schedule-items` | | `--fee-schedule-id --cpt-code --limit --offset` |
| `add-charge` | `--company-id --encounter-id --patient-id --provider-id --cpt-code --service-date` | `--charge-amount --procedure-id --fee-schedule-id --modifiers --units --place-of-service` |
| `list-charges` | | `--encounter-id --patient-id --company-id --status --limit --offset` |
| `add-claim` | `--company-id --patient-id --encounter-id --insurance-id --claim-date` | `--claim-type --billing-provider-id --rendering-provider-id --place-of-service --prior-auth-id` |
| `update-claim` | `--claim-id` | `--claim-status --total-charge --total-allowed --total-paid --denial-reason --appeal-deadline` |
| `get-claim` | `--claim-id` | |
| `list-claims` | | `--patient-id --company-id --insurance-id --status --limit --offset` |
| `submit-claim` | `--claim-id` | |
| `add-claim-line` | `--claim-id --charge-id --cpt-code` | `--charge-amount --allowed-amount --line-number --modifiers --diagnosis-pointers --units` |
| `list-claim-lines` | `--claim-id --charge-id --limit --offset` |
| `add-payment-posting` | `--company-id --patient-id --posting-type --posting-date --amount` | `--claim-id --payment-method --check-number --payer-name --payment-entry-id --eob-date` |
| `list-payment-postings` | | `--claim-id --patient-id --company-id --posting-type --limit --offset` |

### 库存/药房相关操作（10 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-formulary` | `--company-id --formulary-name --effective-date` | `--description --expiration-date` |
| `update-formulary` | `--formulary-id` | `--formulary-name --formulary-status --description --effective-date --expiration-date` |
| `list-formularies` | | `--company-id --status --limit --offset` |
| `add-formulary-item` | `--formulary-id --item-id` | `--ndc-code --generic-name --brand-name --strength --dosage-form --route --controlled-schedule --formulary-tier` |
| `update-formulary-item` | `--formulary-item-id` | `--formulary-item-status --controlled-schedule --formulary-tier --max-daily-dose` |
| `list-formulary-items` | `--formulary-id --status --limit --offset` |
| `add-dispensing` | `--company-id --prescription-id --patient-id --dispensed-by-id --dispensed-date` | `--formulary-item-id --item-id --quantity --lot-number --directions --refill-number` |
| `get-dispensing` | `--dispensing-id` | |
| `list-dispensings` | `--patient-id --prescription-id --status --limit --offset` |
| `cancel-dispensing` | `--dispensing-id` | |

### 实验室/诊断相关操作（14 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-lab-order` | `--company-id --encounter-id --patient-id --ordering-provider-id --order-date` | `--priority --clinical-indication --specimen-type --fasting-required --order-id` |
| `update-lab-order` | `--lab-order-id` | `--lab-order-status --collection-date --received-date --specimen-type --priority` |
| `get-lab-order` | `--lab-order-id` | |
| `list-lab-orders` | `--patient-id --company-id --ordering-provider-id --status --limit --offset` |
| `add-lab-test` | `--lab-order-id --test-code --test-name` | `--cpt-code` |
| `list-lab-tests` | `--lab-order-id --status --limit --offset` |
| `add-lab-result` | `--lab-order-id --component-name --result-value --result-date` | `--unit --reference-low --reference-high --flag --performed-by-id --verified-by-id` |
| `list-lab-results` | `--lab-test-id --flag --limit --offset` |
| `add-imaging-order` | `--company-id --encounter-id --patient-id --ordering-provider-id --modality --body-part --order-date` | `--priority --laterality --clinical-indication --contrast --cpt-code --order-id` |
| `update-imaging-order` | `--imaging-order-id` | `--imaging-order-status --modality --body-part --scheduled-date --priority` |
| `list-imaging-orders` | `--patient-id --company-id --modality --status --limit --offset` |
| `add-imaging-result` | `--imaging-order-id --report-date` | `--radiologist-id --findings --impression --recommendation --critical-finding` |
| `update-imaging-result` | `--imaging-result-id` | `--imaging-result-status --findings --impression --addendum --radiologist-id` |
| `list-imaging-results` | `--imaging-order-id --status --limit --offset` |

### 转诊/预先授权相关操作（10 个）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-referral` | `--company-id --patient-id --referring-provider-id --referred-to-provider --referred-to-date --reason` | `--encounter-id --referred-to-specialty --referred-to-facility --priority --insurance-id --prior-auth-id` |
| `update-referral` | `--referral-id` | `--referral-status --referred-to-provider --referred-to-facility --reason --priority` |
| `get-referral` | `--referral-id` | |
| `list-referrals` | `--patient-id --company-id --company-id --referring-provider-id --status --limit --offset` |
| `add-prior-auth` | `--company-id --patient-id --insurance-id --requesting-provider-id --service-type --description --request-date` | `--cpt-codes --icd10-codes --units-requested --auth-number` |
| `update-prior-auth` | `--prior-auth-id` | `--auth-status --auth-number --units-approved --decision-date --effective-date --expiration-date --denial-reason` |
| `get-prior-auth` | `--prior-auth-id` | |
| `list-prior-auths` | `--patient-id --company-id --insurance-id --status --limit --offset` |
| `add-auth-usage` | `--prior-auth-id --usage-date` | `--encounter-id --claim-id --units-used --notes` |
| `list-auth-usages` | `--prior-auth-id --encounter-id --claim-id --limit --offset` |

### 快速命令参考

| 用户指令 | 对应操作 |
|-----------|--------|
| “注册新患者” | `add-patient` |
| “为患者添加保险” | `add-patient-insurance` |
| “记录过敏信息” | `add-allergy` |
| “预约就诊” | `add-appointment` |
| “患者签到” | `check-in-appointment` |
| “开始新的诊疗” | `add-encounter` |
| “记录生命体征” | `add-vitals` |
| “开具诊断” | `add-diagnosis` |
| “开具处方” | `add-prescription` |
| “安排医疗程序” | `add-procedure` |
| “编写 SOAP 病历” | `add-clinical-note` |
| “安排实验室检查” | `add-lab-order` |
| “获取实验室检查结果” | `add-lab-result` |
| “安排 X 光/CT/MRI 检查” | `add-imaging-order` |
| “生成费用记录” | `add-charge` |
| “提交保险索赔” | `add-claim` 然后 `submit-claim` |
| “记录付款信息” | `add-payment-posting` |
| “转诊患者” | `add-referral` |
| “请求预先授权” | `add-prior-auth` |
| “分发药品” | `add-dispensing` |

### 关键概念

- **患者（Patient）= 客户（Customer）**：患者是 ERPClaw 的客户。
- **诊疗记录（Encounter）**：所有生命体征数据、诊断结果、处方信息、医疗程序记录都关联到具体的诊疗事件。
- **ICD-10/CPT 代码（ICD-10/CPT Codes）**：以文本形式存储（包含超过 7 万个代码，无需查询表）。
- **索赔流程（Claim Lifecycle）**：从草稿状态开始，经过提交、审核、批准或拒绝，最终完成支付或上诉。
- **预先授权（Prior Authorization）**：某些医疗程序或检查前需要先获得授权，并会记录使用次数。
- **药品目录（Formulary）**：医院内部的药品清单，包含 NDC 代码和用药计划信息。
- **SOAP 病历（SOAP Notes）**：包含主观信息、客观观察结果、评估内容和治疗计划的结构化文档。

## 技术细节（高级级别）

系统管理的表格共有 35 个：
- `healthclaw.patient`、`healthclaw.patient_insurance`、`healthclaw_allergy`、`healthclaw_medical_history`、`healthclaw.patient_contact`、`healthclaw_consent`、`healthclaw_provider_schedule`、`healthclaw_schedule_block`、`healthclaw_appointment`、`healthclaw_appointment_reminder`、`healthclaw_waitlist`、`healthclaw_encounter`、`healthclaw_vitals`、`healthclaw_diagnosis`、`healthclaw_prescription`、`healthclaw_procedure`、`healthclaw_clinical_note`、`healthclaw_order`、`healthclaw_fee_schedule`、`healthclaw_fee_schedule_item`、`healthclaw_charge`、`healthclaw_claim`、`healthclaw_claim_line`、`healthclaw_payment_posting`、`healthclaw_formulary`、`healthclaw_formulary_item`、`healthclaw_dispensing`、`healthclaw_lab_order`、`healthclaw_lab_test`、`healthclaw_lab_result`、`healthclaw_imaging_order`、`healthclaw_imaging_result`、`healthclaw_referral`、`healthclaw_prior_auth`、`healthclaw_auth_usage`。

**脚本（Script）**：`scripts/db_query.py` 负责调用 7 个核心模块：`patients.py`、`appointments.py`、`clinical.py`、`billing.py`、`inventory.py`、`lab.py`、`referrals.py`。

**数据格式说明：**
- 财务数据类型为文本（Python 的 Decimal 类型）。
- 用户标识符（IDs）为文本（UUID4 格式）。
- 日期格式为 ISO 8601 标准。
- 布尔值（Boolean）用整数（0 或 1）表示。

**共享库（Shared Library）**：`erpclaw_lib`，包含以下函数：`get_connection`、`ok/err`、`row_to_dict`、`get_next_name`、`audit`、`to_decimal`、`round_currency`、`check_required_tables`。