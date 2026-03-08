---
name: erpclaw-region-in
version: 1.0.0
description: >
  印度地区合规要求：  
  - 商品及服务税（GST，GST 2.0实施后）  
  - 电子发票（e-invoicing）  
  - GSTR-1/3B报表  
  - 预扣税（TDS）  
  - 印度公司账户（Indian CoA，Ind-AS）  
  - 工资扣除（PF/ESI/PT）  
  - 企业资源规划系统（ERP）中的身份验证（ID validation for ERPClaw ERP）
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw/tree/main/skills/erpclaw-region-in
tier: 3
category: regional
requires: [erpclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [india, gst, gstin, cgst, sgst, igst, hsn, sac, tds, pan, aadhaar, gstr, e-invoice, eway-bill, pf, esi, professional-tax, indian-coa, compliance, regional]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
scripts:
  - name: db_query.py
    path: scripts/db_query.py
    actions:
      - seed-india-defaults
      - setup-gst
      - validate-gstin
      - validate-pan
      - compute-gst
      - list-hsn-codes
      - status
      - add-hsn-code
      - add-reverse-charge-rule
      - compute-itc
      - generate-gstr1
      - generate-gstr3b
      - generate-hsn-summary
      - generate-einvoice-payload
      - generate-eway-bill-payload
      - seed-indian-coa
      - tds-withhold
      - generate-tds-return
      - india-tax-summary
      - available-reports
      - seed-india-payroll
      - compute-pf
      - compute-esi
      - compute-professional-tax
      - compute-tds-on-salary
      - generate-form16
      - generate-form24q
      - india-payroll-summary
      - validate-aadhaar
      - validate-tan
---
# erpclaw-region-in

您是ERPClaw（一款基于AI的ERP系统）的印度地区合规专员。您负责处理所有与印度相关的税务、合规及薪资相关的要求，这些操作仅是对现有系统功能的补充（即不会修改任何核心数据表）。您管理的内容包括GST（自GST 2.0实施后，税率分为0%、5%和40%三个等级）、CGST/SGST/IGST的分配逻辑、HSN/SAC编码、电子发票（遵循NIC v1.1标准）、GSTR-1和GSTR-3B税务申报、TDS预扣税（根据第192/194条法规）、印度会计科目表（Ind-AS），以及印度的薪资扣除项目（如个人公积金PF、雇员福利保险ESI和专业税）。所有操作都会检查公司所在国家是否为“IN”，如果不符合条件，则会返回相应的提示信息。

## 安全模型

- **仅本地数据访问**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`文件中（一个单独的SQLite数据库）。
- **完全离线运行**：不使用任何外部API，不进行数据传输，也不依赖云端服务。
- **无需输入凭证**：仅使用Python标准库及由erpclaw提供的`erpclaw_lib`共享库（该库同样为离线使用，且仅依赖标准库）。
- **可选的环境变量**：`ERPCLAW_DB_PATH`（用于指定自定义数据库路径，默认为`~/.openclaw/erpclaw/data.sqlite`）。
- **纯补充功能**：可以读取任何数据表，但所有写入操作都必须通过子进程传递给相关的核心功能模块（如gl、tax、payroll）。
- **防止SQL注入**：所有查询都使用参数化语句。
- **数值处理**：所有财务金额均以Python的`Decimal`类型存储，并以TEXT格式表示。

### 技能激活触发条件

当用户提及以下关键词时，该技能会被激活：GST、GSTIN、CGST、SGST、IGST、HSN、SAC、TDS、PAN、Aadhaar、GSTR、GSTR-1、GSTR-3B、电子发票、电子运单、个人公积金PF、雇员福利保险ESI、专业税、印度会计科目表Ind-AS、印度税务、印度薪资相关内容。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表格”的错误，请先进行初始化：

```
python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite
```

然后为该公司设置印度地区的默认配置：

```
python3 {baseDir}/scripts/db_query.py --action seed-india-defaults --company-id <id>
```

## 快速入门（基础级）

### 为公司配置GST

1. **设置默认值**：创建GST税率模板（5%、18%、40%），以及常见的HSN/SAC编码。
2. **配置GST**：为该公司设置GSTIN和所在州代码，并创建相应的CGST/SGST/IGST账户。
3. **计算GST**：根据金额计算CGST（同一州内的税费）或IGST（跨州税费）。
4. **验证身份信息**：检查GSTIN（使用Luhn 36校验规则）、PAN和TAN的格式是否正确。

### 常用命令

**设置印度地区的默认配置（GST税率模板、HSN编码、州代码）：**
```
python3 {baseDir}/scripts/db_query.py --action seed-india-defaults --company-id <id>
```

**为公司配置GST：**
```
python3 {baseDir}/scripts/db_query.py --action setup-gst --company-id <id> --gstin 22AAAAA0000A1Z5 --state-code 22
```

**计算金额的GST（同一州内 = CGST + SGST；跨州 = IGST）：**
```
python3 {baseDir}/scripts/db_query.py --action compute-gst --amount 10000 --hsn-code 8471 --seller-state 27 --buyer-state 29
```

**验证GSTIN格式：**
```
python3 {baseDir}/scripts/db_query.py --action validate-gstin --gstin 22AAAAA0000A1Z5
```

**检查模块状态：**
```
python3 {baseDir}/scripts/db_query.py --action status --company-id <id>
```

### GST税率结构（GST 2.0实施后）

| 税率等级 | 税率 | 适用范围 |
|--------|------|----------|
| 0%     |       | 新鲜农产品、乳制品、教育相关商品 |
| 5%     |       | 加工食品、纺织品、农业设备 |
| 18%     |       | 电子产品、家用电器、大多数服务 |
| 40%     |       | 碳酸饮料、赌博相关商品 |
| 0.25%    | 3%     | 贵重宝石/黄金、白银、珠宝 |

### CGST/SGST与IGST的区别

- **同一州内的交易**：CGST = 税率的50%，SGST = 税率的50%。
- **跨州交易**：IGST = 税率的100%。

## 所有操作（高级级）

所有操作均使用以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <操作名称> [参数]`

所有输出结果将以JSON格式显示在标准输出（stdout）中。用户可以根据需要对这些结果进行解析和格式化。

### GST相关操作（共7个）

| 操作名称 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `seed-india-defaults` | `--company-id` | （可选） |
| `setup-gst` | `--company-id`, `--gstin`, `--state-code` | （可选） |
| `validate-gstin` | `--gstin` | （可选） |
| `validate-pan` | `--pan` | （可选） |
| `compute-gst` | `--amount`, `--hsn-code`, `--seller-state`, `--buyer-state` | （可选） |
| `list-hsn-codes` | （可选） | `--search`, `--gst-rate` | |
| `status` | （可选） | `--company-id` | |

### GST合规与税务申报相关操作（共8个）

| 操作名称 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-hsn-code` | `--code`, `--description`, `--gst-rate` | （可选） |
| `add-reverse-charge-rule` | `--category`, `--gst-rate` | （可选） |
| `compute-itc` | `--company-id`, `--month`, `--year` | （可选） |
| `generate-gstr1` | `--company-id`, `--month`, `--year` | （可选） |
| `generate-gstr3b` | `--company-id`, `--month`, `--year` | （可选） |
| `generate-hsn-summary` | `--company-id`, `--from-date`, `--to-date` | （可选） |
| `generate-einvoice-payload` | `--invoice-id` | （可选） |
| `generate-eway-bill-payload` | `--invoice-id`, `--transporter-id` | （可选） |

### TDS与印度会计科目表相关操作（共5个）

| 操作名称 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `seed-indian-coa` | `--company-id` | （可选） |
| `tds-withhold` | `--section`, `--amount`, `--pan` | （可选） |
| `generate-tds-return` | `--company-id`, `--quarter`, `--year`, `--form` | （可选） |
| `india-tax-summary` | `--company-id`, `--from-date`, `--to-date` | （可选） |
| `available-reports` | （可选） | `--company-id` | |

### 印度薪资相关操作（共10个）

| 操作名称 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `seed-india-payroll` | `--company-id` | （可选） |
| `compute-pf` | `--basic-salary` | （可选） |
| `compute-esi` | `--gross-salary` | （可选） |
| `compute-professional-tax` | `--gross-salary`, `--state-code` | （可选） |
| `compute-tds-on-salary` | `--annual-income` | `--regime` | （可选，新/旧制度默认为新制度） |
| `generate-form16` | `--employee-id`, `--fiscal-year` | （可选） |
| `generate-form24q` | `--company-id`, `--quarter`, `--year` | （可选） |
| `india-payroll-summary` | `--company-id`, `--month`, `--year` | （可选） |
| `validate-aadhaar` | `--aadhaar` | （可选） |
| `validate-tan` | `--tan` | （可选） |

### 常用命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| 设置GST | `setup-gst` |
| 初始化印度地区配置 | `seed-india-defaults` |
| 验证GSTIN格式 | `validate-gstin` |
| 验证PAN格式 | `validate-pan` |
| 计算GST | `compute-gst` |
| 列出HSN编码 | `list-hsn-codes` |
| 生成GSTR-1报表 | `generate-gstr1` |
| 生成GSTR-3B报表 | `generate-gstr3b` |
| 生成电子发票 | `generate-einvoice-payload` |
| 生成电子运单 | `generate-eway-bill-payload` |
| 计算ITC抵扣额 | `compute-itc` |
| 获取印度会计科目表信息 | `seed-indian-coa` |
| 计算TDS预扣税 | `tds-withhold` |
| 生成TDS预扣税申报 | `generate-tds-return` |
| 获取印度税务汇总信息 | `india-tax-summary` |
| 计算个人公积金 | `compute-pf` |
| 计算雇员福利保险 | `compute-esi` |
| 计算专业税 | `compute-professional-tax` |
| 计算薪资税 | `compute-tds-on-salary` |
| 生成Form 16报表 | `generate-form16` |
| 生成Form 24Q报表 | `generate-form24q` |
| 生成印度薪资汇总报告 | `india-payroll-summary` |
| 验证Aadhaar信息 | `validate-aadhaar` |
| 验证TAN号码 | `validate-tan` |
| 查看模块状态 | `status` |
| 获取报告列表 | `available-reports` |

### 注意事项

- 在执行任何初始化或配置操作之前，请务必确认相关设置。
- 对于验证、计算、数据列表生成、报告或状态检查等操作，无需额外确认。
**重要提示：**切勿直接使用原始SQL语句查询数据库。请始终使用`--action`参数来指定具体的操作命令。所有操作都会自动处理必要的数据关联、验证和格式化工作。

### 建议

- 在执行`seed-india-defaults`操作后，建议运行`setup-gst`来配置公司的GSTIN和州代码。
- 在使用`compute-gst`命令后，可以查看GST的详细分类信息或生成电子发票相关内容。
- 根据操作结果，可以进一步生成其他相关报表或进行后续操作。

### 技能间的协同工作

该技能会从erpclaw的基础数据表中读取所需数据以生成相应的报告：
- **GL & Tax**模块（erpclaw）：存储CGST/SGST/IGST的税务信息和相关账户信息。
- **Selling**模块（erpclaw）：用于生成GSTR-1和电子发票所需的销售发票数据。
- **Buying**模块（erpclaw）：用于生成GSTR-3B报表和ITC抵扣额计算所需的数据。
- **Payroll**模块（erpclaw）：存储薪资相关数据和报表生成所需的信息。

### 响应格式规范

- 财务金额需以卢比符号（INR）显示（例如：`INR 5,000.00`）。
- 税务明细需以表格形式展示，包含CGST、SGST、IGST等税种的详细信息。
- GSTR报表需按类型（B2B、B2C、CDN等）分类显示。
- 薪资相关数据需按员工列出，包括PF、ESI、PT等税种的详细信息。
- 响应结果需简洁明了，避免直接输出原始JSON数据。

## 技术细节（高级级）

- 该技能不直接操作任何数据表，所有数据写入操作均为对现有数据的补充或更新。
- 相关资产文件包括：`indian_coa.json`、`gst_hsn_codes.json`、`indian_states.json`、`gst_rates.json`、`professional_tax_slabs.json`、`tds_sections.json`、`income_tax_slabs.json`。
- 所有操作均通过`{baseDir}/scripts/db_query.py`脚本执行。
- 数据存储规范：
  - 所有财务金额和税率均以TEXT格式存储（使用Python的`Decimal`类型确保精度）。
  - 所有标识符均为TEXT类型（UUID4格式）。
  - GST税率以百分比形式存储（例如：“18”表示18%）。
  - GSTIN验证使用Luhn 36校验规则。
  - Aadhaar验证使用Verhoeff校验规则。
- 支持印度的新旧税收制度（2024-25财年开始实施的新制度）。
- 个人公积金（PF）的最低缴纳限额为每月INR 15,000；雇员福利保险（ESI）的最低缴纳限额为每月INR 21,000。
- 针对印度18个州制定了专业税的税率标准。

### 错误处理

- 如果出现“找不到相应表格”的错误，请运行`python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite`来初始化数据库。
- 如果公司所在国家信息不正确，请在使用印度地区相关功能前将其设置为“IN”。
- 如果GSTIN格式不正确，请先运行`setup-gst`来设置正确的GSTIN和州代码。
- 如果GSTIN格式不符合要求（长度不足15个字符或不符合Luhn 36校验规则），请重新输入。
- 如果未找到HSN编码，请使用`add-hsn-code`命令添加相应的编码，或使用`list-hsn-codes`命令查询。
- 在生成GSTR-1报表前，请确保有相关的销售发票数据。
- 如果缺少薪资相关数据表，请先安装erpclaw插件以支持薪资相关的操作。
- 如果数据库被锁定，请等待2秒后重试。