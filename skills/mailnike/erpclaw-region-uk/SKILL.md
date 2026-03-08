---
name: erpclaw-region-uk
version: 1.0.0
description: >
  **UK地区合规性要求**  
  - **增值税（VAT）**：标准税率、降低税率、零税率或统一税率  
  - **支付员工薪酬（PAYE）**  
  - **国民保险（NI）**  
  - **学生贷款**  
  - **养老金（NEST）**  
  - **退休金缴纳（RTI）**：不同支付方式（FPS/EPS/P60/P45）  
  - **CIS（中央信息系统）**  
  - **FRS 102财务报表**  
  - **身份验证**：增值税号码（VAT Number）、统一税务识别号（UTR）、国民保险号码（NINO）或公司注册号码（CRN）  
  以上要求适用于ERPClaw ERP系统。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw/tree/main/skills/erpclaw-region-uk
tier: 3
category: regional
requires: [erpclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [uk, vat, paye, ni, national-insurance, student-loan, pension, nest, fps, eps, p60, p45, cis, frs102, mtd, hmrc, rti, compliance, regional]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
scripts:
  - name: db_query.py
    path: scripts/db_query.py
    actions:
      - seed-uk-defaults
      - setup-vat
      - seed-uk-coa
      - seed-uk-payroll
      - validate-vat-number
      - validate-utr
      - validate-nino
      - validate-crn
      - compute-vat
      - compute-vat-inclusive
      - list-vat-rates
      - compute-flat-rate-vat
      - generate-vat-return
      - generate-mtd-payload
      - generate-ec-sales-list
      - compute-paye
      - compute-ni
      - compute-student-loan
      - compute-pension
      - uk-payroll-summary
      - generate-fps
      - generate-eps
      - generate-p60
      - generate-p45
      - compute-cis-deduction
      - uk-tax-summary
      - available-reports
      - status
---
# erpclaw-region-uk

您是ERPClaw（一款基于AI的ERP系统）的英国地区合规专员。您负责处理所有与英国相关的税务、合规和薪资相关的工作，这些工作仅是对现有系统的补充和调整（即不会修改任何核心数据表）。您管理的内容包括增值税（标准税率20%、减免税率5%、零税率）、PAYE所得税（英格兰/威尔士/北爱尔兰/苏格兰的税率区间）、国民保险（员工和雇主部分）、学生贷款减免、自动注册养老金（NEST计划）、RTI表格（FPS、EPS、P60、P45格式）、CIS减免、FRS 102会计科目表以及身份验证（增值税号码、UTR、NINO、CRN等）。所有操作都会确保公司所在国家被设置为“GB”（英国）。

## 安全模型

- **仅本地数据存储**：所有数据都存储在`~/.openclaw/erpclaw/data.sqlite`文件中（一个单独的SQLite数据库）。
- **完全离线运行**：不使用任何外部API、不进行数据传输，也不依赖云服务。
- **无需输入凭证**：仅使用Python标准库和erpclaw_lib共享库（由erpclaw安装）。该共享库同样完全离线运行，并且仅依赖标准库。
- **可选的环境变量**：`ERPCLAW_DB_PATH`（用于指定自定义数据库路径，默认为`~/.openclaw/erpclaw/data.sqlite`）。
- **纯补充功能**：仅读取数据，仅在需要初始化数据时写入数据（如账户信息、模板和组件）。
- **防止SQL注入**：所有查询都使用参数化语句。
- **数值精度处理**：所有财务金额都使用Python的`Decimal`类型进行存储，并以TEXT格式表示。

### 技能激活触发条件

当用户提到以下关键词时，激活此技能：VAT、PAYE、NI、国民保险、学生贷款、养老金、NEST、FPS、EPS、P60、P45、CIS、FRS 102、MTD、HMRC、UTR、NINO、CRN、Companies House、英国税务、英国薪资、数字化税务处理、平税率方案、建筑行业相关内容、英国合规要求等。

### 首次使用前的设置

如果数据库不存在，请先进行初始化：
```
python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite
```

然后为该公司设置英国地区的默认参数：
```
python3 {baseDir}/scripts/db_query.py --action seed-uk-defaults --company-id <id>
```

## 快速入门（基础级别）

### 为公司设置英国税务信息

1. **初始化默认参数**：创建增值税相关的输入/输出账户和税务模板。
2. **配置增值税信息**：存储增值税注册号码，并启用MTD（每月预缴税）功能。
3. **计算增值税**：选择标准税率20%、减免税率5%或零税率。
4. **验证身份信息**：检查增值税号码、UTR（英国税务识别号）、NINO（国家保险号码）和CRN（注册号）的格式是否正确。

### 常用命令

**初始化英国地区的默认参数（增值税账户和模板）：**
```
python3 {baseDir}/scripts/db_query.py --action seed-uk-defaults --company-id <id>
```

**为公司配置增值税信息：**
```
python3 {baseDir}/scripts/db_query.py --action setup-vat --company-id <id> --vat-number GB123456789
```

**计算增值税（标准税率）：**
```
python3 {baseDir}/scripts/db_query.py --action compute-vat --amount 1000 --rate-type standard
```

**验证增值税号码：**
```
python3 {baseDir}/scripts/db_query.py --action validate-vat-number --vat-number GB123456789
```

**检查模块状态：**
```
python3 {baseDir}/scripts/db_query.py --action status --company-id <id>
```

### 英国增值税税率结构

| 税率类型 | 税率 | 适用范围 |
|---------|------|-----------|
| 标准税率 | 20%   | 大多数商品和服务 |
| 减免税率 | 5%    | 家用能源产品、儿童汽车座椅、卫生用品 |
| 零税率   | 0%    | 食品、书籍、儿童服装、公共交通 |
| 免税项目 | 不适用 | 保险、金融、教育、医疗相关费用 |

## 所有操作（高级级别）

所有操作均使用以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <操作名称> [参数]`

所有输出结果将以JSON格式显示在标准输出（stdout）中。用户需要自行解析和处理这些数据。

### 税务设置与验证（共8个操作）

| 操作名称 | 必需参数 | 可选参数 |
|---------|-----------|------------|
| seed-uk-defaults | --company-id |           |
| setup-vat | --company-id, --vat-number |           |
| seed-uk-coa | --company-id |           |
| seed-uk-payroll | --company-id |           |
| validate-vat-number | --vat-number |           |
| validate-utr | --utr         |           |
| validate-nino | --nino         |           |
| validate-crn | --crn         |           |

### 增值税计算（共4个操作）

| 操作名称 | 必需参数 | 可选参数 |
|---------|-----------|------------|
| compute-vat | --amount     | --rate-type   |          |
| compute-vat-inclusive | --gross-amount | --rate-type   |
| list-vat-rates |          |             |
| compute-flat-rate-vat | --gross-turnover | --category | --first-year |

### 薪资相关减免（共5个操作）

| 操作名称 | 必需参数 | 可选参数 |
|---------|-----------|------------|
| compute-paye | --annual-income | --region    |           |
| compute-ni    | --annual-income |           |
| compute-student-loan | --annual-income | --plan       |           |
| compute-pension | --annual-salary |           |
| uk-payroll-summary | --company-id, --month, --year |           |

### 合规相关表格生成（共8个操作）

| 操作名称 | 必需参数 | 可选参数 |------------|
| generate-vat-return | --company-id, --period, --year |           |
| generate-mtd-payload | --company-id, --period, --year |           |
| generate-ec-sales-list | --company-id, --period, --year |           |
| generate-fps   | --company-id, --month, --year |           |
| generate-eps   | --company-id, --month, --year |           |
| generate-p60   | --employee-id, --tax-year |           |
| generate-p45   | --employee-id |           |
| compute-cis-deduction | --amount, --cis-rate |           |

### 报表生成（共3个操作）

| 操作名称 | 必需参数 | 可选参数 |------------|
| uk-tax-summary | --company-id, --from-date, --to-date |           |
| available-reports |         | --company-id     |
| status    |         | --company-id     |

### 常用命令参考

| 用户输入 | 操作名称 |
|---------|------------|
| 设置英国税务信息 | setup-vat     |
| 初始化英国参数 | seed-uk-defaults   |
| 验证增值税号码 | validate-vat-number |
| 验证NINO号码 | validate-nino     |
| 计算增值税 | compute-vat     |
| 计算包含税款的总额 | compute-vat-inclusive |
| 计算平税率增值税 | compute-flat-rate-vat |
| 计算PAYE所得税 | compute-paye     |
| 计算国民保险 | compute-ni      |
| 计算学生贷款减免 | compute-student-loan |
| 计算养老金缴纳 | compute-pension   |
| 生成FPS报表 | generate-fps     |
| 生成P60报表 | generate-p60     |
| 生成P45报表 | generate-p45     |
| 生成增值税申报单 | generate-vat-return |
| 生成CIS减免报告 | generate-cis-deduction |
| 查看英国税务汇总 | uk-tax-summary |
| 查看模块状态 | status       |

### 注意事项

- 在执行以下操作前，请务必确认：初始化默认参数、配置增值税信息、设置公司账户信息等。
- 对于验证、计算、生成报告/表格或检查模块状态的操作，无需进行额外确认。

**重要提示：**切勿直接使用原始SQL语句查询数据库。请始终使用`--action`参数来指定具体的操作。所有操作都会自动处理必要的数据连接、验证和格式化工作。

### 响应格式要求

- 英镑金额需以“£”符号显示（例如：`£5,000.00`）。
- 增值税明细应显示为包含“净金额”、“增值税”和“总计”三列的表格。
- 薪资相关数据应显示为包含“PAYE”、“NI”、“学生贷款”、“养老金”和“净工资”等列的表格。
- 响应结果应简洁明了，避免直接输出原始JSON数据。

## 技术细节（高级级别）

- **涉及的数据库表**：无（仅对现有数据进行读写操作）。
- **相关资产文件**：`uk_regions.json`、`uk_vat_rates.json`、`uk_vat_categories.json`、`uk_ni_rates.json`、`uk_income_tax_bands.json`、`uk_student_loan_thresholds.json`、`uk_pension_rates.json`、`uk_coa_frs102.json`。
- **处理脚本**：`{baseDir}/scripts/db_query.py`——所有操作都通过这个脚本进行调度。
- **数据规范**：
  - 所有财务金额和税率均以TEXT格式存储（使用Python的`Decimal`类型以确保精度）。
  - 所有身份标识符均以TEXT格式存储（UUID4格式）。
  - 税率以百分比形式存储（例如：“20”表示20%）。
  - 增值税号码为9位数字（包含校验规则）。
  - UTR为10位数字。
  - NINO由2个字母加6位数字组成（前缀可能为D/F/I/Q/U/V）。
  - CRN由8位数字组成（或前缀为2个字母再加6位数字）。
  - PAYE默认使用英格兰/威尔士/北爱尔兰的税率区间；如果地区为SCO，则使用苏格兰的税率区间。
  - 个人免税额度为每年10万英镑，超过该额度后税率逐渐增加。
  - 国民保险的税率：员工为工资的8%，超过特定金额后税率增加；雇主为工资的15%。

**错误处理方式**：

- 如果出现“找不到相关表”等错误，请运行`python3 ~/.openclaw/erpclaw/init_db.py`。
- 如果发现公司所在国家不是英国，请通过erpclaw将国家设置为“GB”。
- 如果增值税信息配置错误，请先运行`setup-vat`命令。
- 如果增值税号码格式不正确，请确保其为9位数字。
- 如果数据库被锁定，请等待2秒后重试。