---
name: greek-individual-taxes
description: 针对有雇用关系的希腊公民，提供全面的个人所得税申报处理服务。涵盖E1表格的填写、个人所得税的计算、税收减免的优化、房产税（ENFIA）的缴纳以及个人税务合规性的管理。该服务专为拥有工资收入、房产收入和投资收入的希腊纳税人设计。
version: 1.0.0
author: openclaw-greek-accounting
homepage: https://github.com/satoshistackalotto/openclaw-greek-accounting
tags: ["greek", "accounting", "individual-tax", "e1-form", "enfia"]
metadata: {"openclaw": {"requires": {"bins": ["jq"], "env": ["OPENCLAW_DATA_DIR"]}, "notes": "Instruction-only skill. Prepares E1 tax return data from local files. Does not submit to AADE directly — submission is handled by greek-compliance-aade skill with human approval."}}
---
# 希腊个人税务处理

该功能将 OpenClaw 转换为专门的希腊个人税务处理工具，用于处理希腊纳税居民的个人所得税申报表（E1 表格）、税收减免优化以及个人税务合规管理。

## 设置

```bash
export OPENCLAW_DATA_DIR="/data"
which jq || sudo apt install jq
```

无需外部凭证。该功能从本地文件中提取 E1 税务申报表数据。实际的税务申报工作由 `greek-compliance-aade` 功能负责，并需要人工审核。

## 核心理念

- **以雇员为中心**：专为工资收入者和员工（主要用户群体）优化设计
- **最大化税收减免**：识别并应用所有合法的税收减免和税收抵免项
- **合规优先**：确保遵守希腊个人税法及截止日期
- **家庭税务规划**：支持配偶和受抚养人的税收优化策略
- **财产税务管理**：处理 ENFIA 财产税和租金收入
- **投资收入处理**：处理股息、利息和资本利得

## 关键功能

### 1. 个人所得税（E1 表格）处理
- **工资收入**：工资、奖金、第 13/14 个月工资、加班费
- **职业收入**：自由职业收入、咨询服务、兼职职业服务
- **财产收入**：住宅和商业房产的租金收入
- **投资收入**：股息、利息、资本利得
- **养老金收入**：退休金和社会保险福利
- **其他收入**：版税、奖金、农业收入

### 2. 希腊税收减免与抵免优化
- **医疗费用**：医疗保健费用、药品费用、牙科费用、医疗设备费用
- **教育费用**：学费、书籍费用、教育材料费用
- **保险费用**：人寿保险、健康保险、财产保险费用
- **慈善捐赠**：向认可的希腊慈善组织进行的捐赠
- **能源效率抵免**：家庭装修费用、太阳能板安装、能源升级费用
- **家庭税收抵免**：配偶和受抚养人的税收抵免
- **残疾抵免**：为残疾个人或家庭成员提供的税收抵免

### 3. 财产税务管理（ENFIA）
- **主要住宅**：主要住宅的财产税计算和免税政策
- **次要房产**：度假屋、投资房产
- **商业房产**：商业房产的税务义务
- **财产税抵免**：保险折扣、能源效率改进带来的税收减免
- **地方财产税（TAP）**：地方财产税的协调管理
- **房产转让税**：房地产交易的税务管理

### 4. 个人税务合规管理
- **税务申报截止日期**：必须在 6 月 30 日之前提交 E1 表格
- **付款计划**：税务分期付款的规划与管理
- **文件收集**：收集所需的证书和支持文件
- **与 AADE 的集成**：通过 TAXIS 平台进行电子申报
- **审计准备**：个人税务审计的应对和文件准备
- **税务居民身份确定**：确定和规划税务居民身份

## 实施指南

### E1 表格处理架构

#### 收入类别及处理流程
```yaml
Employment_Income:
  salary_income:
    sources: ["Employer certificates", "Monthly payslips", "13th/14th payments"]
    tax_treatment: "Progressive rates 9%-44%"
    deductions: ["Social security contributions", "Professional expenses"]
    
  overtime_compensation:
    calculation: "Regular rate × overtime multiplier"
    tax_treatment: "Included in total employment income"
    limits: "Greek labor law overtime limits"
    
  bonuses_and_benefits:
    types: ["Performance bonuses", "Company car", "Meal allowances", "Housing benefits"]
    valuation: "Fair market value for benefits in kind"
    exemptions: ["Meal vouchers up to ‚¬5/day", "Transport allowances"]

Professional_Income:
  freelance_services:
    tax_treatment: "Progressive rates with professional expenses"
    expense_deductions: ["Office rent", "Equipment", "Professional development"]
    presumptive_taxation: "Available for specific professions"
    
  consulting_income:
    withholding_tax: "20% withheld by clients"
    annual_reconciliation: "Net additional tax or refund calculation"
    expense_tracking: "Business meal deductions (50%)", "Travel expenses"]

Property_Income:
  rental_income:
    tax_rates: 
      - up_to_12000: "15%"
      - from_12001_to_35000: "35%" 
      - over_35000: "45%"
    deductions: ["Property maintenance", "Management fees", "Insurance", "Depreciation"]
    
  airbnb_income:
    licensing_requirement: "Short-term rental license required"
    tax_treatment: "As rental income with limited deductions"
    vat_implications: "13% VAT if over ‚¬10,000 annually"

Investment_Income:
  dividend_income:
    greek_companies: "5% withholding tax (final)"
    foreign_dividends: "Progressive rates with foreign tax credit"
    
  interest_income:
    bank_deposits: "15% withholding tax (final)"
    bonds: "15% withholding tax or progressive rates (taxpayer choice)"
    
  capital_gains:
    status: "Suspended until December 31, 2026"
    real_estate: "Suspended for property sales"
    securities: "Suspended for stock sales"
```

#### 希腊税收减免系统
```yaml
Medical_Expenses:
  eligible_costs:
    - "Doctor visits and specialist consultations"
    - "Hospital expenses and surgery costs"  
    - "Prescription medications from pharmacies"
    - "Dental care and orthodontics"
    - "Medical equipment and devices"
    - "Physiotherapy and rehabilitation"
  
  limitations:
    annual_limit: "No maximum limit for medical expenses"
    supporting_documents: "Receipts with patient name and medical purpose"
    electronic_payments: "Additional 10% deduction for card/electronic payments"
    
Education_Expenses:
  eligible_institutions:
    - "Greek universities and technical schools"
    - "Recognized foreign universities"
    - "Private schools and tutoring centers"
    - "Language schools and certification programs"
  
  eligible_costs:
    - "Tuition fees and registration costs"
    - "Required textbooks and materials"
    - "Laboratory fees and equipment"
    - "Student housing (university dormitories)"
  
  limitations:
    per_child_limit: "No annual limit for education expenses"
    age_restrictions: "Generally up to age 24 for higher education"

Insurance_Premiums:
  life_insurance:
    annual_limit: "‚¬1,200 per person"
    eligible_policies: "Greek and EU insurance companies"
    
  health_insurance:
    annual_limit: "‚¬1,200 per person"  
    supplementary_coverage: "Private health insurance premiums"
    
  property_insurance:
    eligible: "Home insurance, fire insurance, earthquake insurance"
    enfia_discount: "20% ENFIA reduction for insured properties"

Charitable_Donations:
  eligible_organizations:
    - "Greek state and municipalities"
    - "Recognized charitable organizations"
    - "Churches and religious institutions"
    - "Educational institutions"
    - "Cultural organizations"
  
  limitations:
    maximum_deduction: "5% of total income or ‚¬2,000 (whichever is higher)"
    documentation: "Official donation receipts required"
```

### 税务计算引擎

#### 2026 年的累进税率
```yaml
Individual_Income_Tax_Brackets:
  bracket_1:
    income_range: "‚¬0 - ‚¬10,000"
    tax_rate: "9%"
    tax_amount: "‚¬0 - ‚¬900"
    
  bracket_2: 
    income_range: "‚¬10,001 - ‚¬20,000"
    tax_rate: "22%"
    tax_amount: "‚¬900 + 22% of excess over ‚¬10,000"
    
  bracket_3:
    income_range: "‚¬20,001 - ‚¬30,000" 
    tax_rate: "28%"
    tax_amount: "‚¬3,100 + 28% of excess over ‚¬20,000"
    
  bracket_4:
    income_range: "‚¬30,001 - ‚¬40,000"
    tax_rate: "36%"
    tax_amount: "‚¬5,900 + 36% of excess over ‚¬30,000"
    
  bracket_5:
    income_range: "‚¬40,001+"
    tax_rate: "44%"
    tax_amount: "‚¬9,500 + 44% of excess over ‚¬40,000"

Tax_Credits:
  basic_tax_credit: "‚¬2,100 per individual"
  spouse_credit: "‚¬2,100 (if spouse has no income)"
  dependent_children_credit: "‚¬777 per child"
  disability_credit: "Varies by disability percentage"
  low_income_credit: "Graduated reduction for income under ‚¬12,000"
  
Solidarity_Tax:
  threshold: "Income over ‚¬30,000"
  rates:
    - "‚¬30,001 - ‚¬40,000": "2.2%"  
    - "‚¬40,001 - ‚¬65,000": "5%"
    - "‚¬65,001 - ‚¬220,000": "6.5%"
    - "Over ‚¬220,000": "9%"
```

#### 税务计算工作流程
```python
def calculate_individual_tax(income_data, deductions, family_situation):
    """
    Calculate Greek individual income tax with optimization
    """
    # Step 1: Calculate total taxable income
    employment_income = sum(income_data['employment'])
    professional_income = sum(income_data['professional'])  
    property_income = calculate_rental_tax(income_data['property'])
    investment_income = sum(income_data['investment'])
    
    total_income = employment_income + professional_income + property_income + investment_income
    
    # Step 2: Apply deductions
    medical_deductions = min(deductions['medical'], total_income * 0.1)  # No limit
    education_deductions = deductions['education']  # No limit
    insurance_deductions = min(deductions['insurance'], 1200 * family_situation['family_members'])
    charity_deductions = min(deductions['charity'], max(total_income * 0.05, 2000))
    
    total_deductions = medical_deductions + education_deductions + insurance_deductions + charity_deductions
    taxable_income = max(0, total_income - total_deductions)
    
    # Step 3: Calculate progressive tax
    income_tax = calculate_progressive_tax(taxable_income)
    solidarity_tax = calculate_solidarity_tax(taxable_income)
    
    # Step 4: Apply tax credits  
    tax_credits = calculate_tax_credits(family_situation, taxable_income)
    
    net_tax = max(0, income_tax + solidarity_tax - tax_credits)
    
    return {
        'total_income': total_income,
        'taxable_income': taxable_income, 
        'total_deductions': total_deductions,
        'income_tax': income_tax,
        'solidarity_tax': solidarity_tax,
        'tax_credits': tax_credits,
        'net_tax': net_tax,
        'effective_rate': (net_tax / total_income) * 100 if total_income > 0 else 0
    }
```

## 工作流程模板

### 个人税务申报表准备

#### 文件收集阶段
```bash
#!/bin/bash
# Individual tax return document collection

# Employment income documents
openclaw individual collect-employment-docs --year 2025
  # - Employer certificates (Βεβαίπ°ση αποδοπ¡Ͻν)
  # - Social security contributions summary
  # - Withholding tax certificates

# Property income documents  
openclaw individual collect-property-docs --year 2025
  # - Rental agreements and income records
  # - Property expenses and maintenance receipts
  # - ENFIA property tax payments

# Investment income documents
openclaw individual collect-investment-docs --year 2025
  # - Bank interest statements
  # - Dividend certificates from Greek companies
  # - Foreign income documentation

# Deduction supporting documents
openclaw individual collect-deduction-docs --year 2025
  # - Medical expenses receipts (patient name required)
  # - Education expense receipts and certificates  
  # - Insurance premium payment receipts
  # - Charitable donation certificates
```

#### E1 表格准备流程
```bash
#!/bin/bash
# E1 form automated preparation

# Step 1: Income calculation and validation
openclaw individual calculate-income --taxpayer-id $AFM --year 2025

# Step 2: Deduction optimization
openclaw individual optimize-deductions --include-all-eligible --electronic-payment-bonus

# Step 3: Tax calculation with family optimization
openclaw individual calculate-tax --include-spouse --include-dependents

# Step 4: E1 form generation
openclaw individual generate-e1-form --year 2025 --validate-data

# Step 5: AADE TAXIS preparation  
openclaw individual prepare-taxis-submission --digital-signature-ready

# Step 6: Payment planning
openclaw individual plan-tax-payments --installments --due-dates
```

#### 家庭税务优化
```yaml
Family_Tax_Strategies:
  spouse_optimization:
    separate_returns:
      when_beneficial: "When spouse has significant deductible expenses"
      calculation: "Compare combined vs separate tax burden"
      
    joint_deduction_allocation:
      medical_expenses: "Allocate to higher-income spouse for better benefit"
      education_expenses: "Can be claimed by either parent"
      charitable_donations: "Optimize between spouses for maximum benefit"
      
  dependent_children:
    child_tax_credits: "‚¬777 per child under 18 or in education"
    education_expenses: "No limit on university tuition deductions"
    medical_expenses: "Include children's medical costs"
    
    age_transitions:
      - "Monitor when children turn 18 (affects tax credits)"
      - "Track university enrollment (extends education deductions)"
      - "Plan for children starting work (changes dependency status)"

  property_ownership_optimization:
    joint_ownership: "Split property income between spouses"
    primary_residence: "Optimize ENFIA exemptions and reductions"
    rental_properties: "Strategic allocation of rental income and expenses"
```

### 财产税务管理（ENFIA）

#### ENFIA 计算与优化
```yaml
ENFIA_Processing:
  primary_residence:
    base_calculation: "Based on objective property value and characteristics"
    exemptions:
      - "First ‚¬200,000 of single-person household value"
      - "Additional exemptions for large families"
      - "Disability exemptions for qualifying individuals"
    
    discounts:
      insurance_discount: "20% reduction for comprehensive property insurance"
      energy_efficiency: "Reductions for high energy rating properties"
      rural_properties: "50% reduction for properties in villages under 1,500 population"
      
  investment_properties:
    supplementary_tax: "Additional tax for total property value over ‚¬500,000"
    commercial_properties: "Different rates for business-use properties"
    rental_income_coordination: "ENFIA costs deductible from rental income"
    
  payment_scheduling:
    installment_options: "Up to 10 monthly installments"
    payment_methods: "Online, bank transfer, or cash at authorized locations"
    early_payment: "3% discount for full payment before April 30"
```

#### 地方税务协调
```yaml
Municipal_Property_Taxes:
  tap_coordination:
    collection_method: "Through electricity bills"
    rate_variation: "0.025%-0.035% by municipality"
    integration: "Coordinate with ENFIA for total property tax burden"
    
  waste_and_lighting:
    calculation_basis: "Property square meters × municipal rate"
    payment_frequency: "Annual via electricity bill"
    exemptions: "Limited exemptions for specific circumstances"
```

## 个人税务场景

### 场景 1：拥有房产的雇员
```yaml
Taxpayer_Profile:
  employment:
    annual_salary: "‚¬35,000"
    employer_withholding: "‚¬6,500"
    social_security: "‚¬4,200"
    
  property:
    primary_residence_value: "‚¬180,000"
    enfia_paid: "‚¬450"
    rental_property_income: "‚¬8,000"
    rental_expenses: "‚¬2,000"
    
  family:
    marital_status: "married"
    spouse_income: "‚¬0"
    dependent_children: 2
    
Tax_Calculation:
  total_income: "‚¬41,000" # ‚¬35,000 salary + ‚¬6,000 net rental
  deductions: "‚¬2,450" # ENFIA + rental expenses
  taxable_income: "‚¬38,550"
  
  income_tax: "‚¬8,398"
  solidarity_tax: "‚¬945" 
  tax_credits: "‚¬3,654" # Basic + spouse + 2 children
  
  gross_tax: "‚¬9,343"
  withholding_credit: "‚¬6,500"
  net_tax_due: "‚¬2,843"
  
Optimization_Opportunities:
  - "Ensure spouse claims any eligible deductions separately"
  - "Maximize children's education expense deductions"
  - "Consider property insurance for ENFIA discount"
  - "Track all rental property maintenance expenses"
```

### 场景 2：高收入专业人士
```yaml
Taxpayer_Profile:
  employment:
    annual_salary: "‚¬55,000"
    employer_withholding: "‚¬12,000"
    
  professional_income:
    consulting_fees: "‚¬25,000"
    withholding_tax: "‚¬5,000"
    business_expenses: "‚¬8,000"
    
  investments:
    dividend_income: "‚¬3,000" # 5% tax already paid
    bank_interest: "‚¬1,500" # 15% tax already paid
    
  family:
    marital_status: "single" 
    dependent_parents: 1
    
Tax_Calculation:
  total_income: "‚¬84,500"
  professional_net: "‚¬17,000" # ‚¬25,000 - ‚¬8,000 expenses
  taxable_income: "‚¬76,500"
  
  income_tax: "‚¬25,500"
  solidarity_tax: "‚¬3,082"
  tax_credits: "‚¬2,100" # Basic credit only
  
  gross_tax: "‚¬28,582"
  withholding_credits: "‚¬17,000" # Employment + professional + investment
  net_tax_due: "‚¬11,582"
  
Optimization_Strategies:
  - "Maximize business expense deductions"
  - "Consider retirement contributions for tax relief"
  - "Plan timing of professional income for tax efficiency"
  - "Explore dependent parent tax benefits"
```

## 与其他功能的集成

### 与邮件处理功能的集成
```bash
# Process tax-related emails automatically
openclaw individual process-tax-emails --year 2025
  # - Employer certificates received via email
  # - Bank statements and tax documents
  # - AADE notifications about individual tax matters

# Client communication for individual tax services
openclaw individual client-communications --auto-respond-greek
  # - Tax return completion confirmations
  # - Required document requests
  # - Payment reminder notifications
```

### 与 AADE 合规功能的集成
```bash
# E1 form submission through TAXIS
openclaw individual submit-e1-form --digital-signature --confirm-receipt

# Individual tax audit support
openclaw individual audit-preparation --year 2025 --gather-supporting-docs

# Deadline monitoring for individual tax obligations
openclaw individual monitor-deadlines --include-enfia --include-payments
```

### 与银行系统的集成
```bash
# Import bank statements for income verification
openclaw individual import-bank-data --verify-salary-deposits --track-investments

# Payment processing for tax obligations
openclaw individual process-tax-payments --schedule-installments --confirm-payments
```

## 高级功能

### 多年税务规划
```yaml
Tax_Planning_Strategies:
  income_timing:
    bonus_deferral: "Defer year-end bonuses to optimize tax brackets"
    consulting_income: "Time invoice payments across tax years"
    property_sales: "Plan property transactions during capital gains suspension"
    
  deduction_timing:
    medical_expenses: "Batch medical procedures in single tax year"
    education_payments: "Time tuition payments for maximum deduction"
    charitable_giving: "Optimize donation timing for tax efficiency"
    
  family_planning:
    marriage_timing: "Consider tax implications of marriage date"
    property_ownership: "Optimize property ownership between spouses"
    dependent_status: "Plan for children's changing tax status"
```

### 投资收入优化
```yaml
Investment_Tax_Strategies:
  dividend_optimization:
    greek_companies: "5% withholding is final - no additional tax"
    foreign_dividends: "Plan for foreign tax credit utilization"
    timing: "Coordinate dividend payments with other income"
    
  interest_income:
    bank_deposits: "15% withholding vs progressive rates analysis"
    bond_investments: "Choose optimal taxation method"
    foreign_accounts: "Ensure proper reporting and tax credit"
    
  capital_gains_suspension:
    real_estate: "Take advantage of suspension until Dec 2026"
    securities: "Strategic selling during suspension period"
    future_planning: "Prepare for potential reinstatement"
```

## 合规性与报告

### 与 AADE 的集成
```yaml
Electronic_Submission:
  e1_form_preparation:
    data_validation: "Comprehensive data accuracy checks"
    digital_signature: "Qualified electronic signature integration"
    submission_tracking: "Monitor submission status and confirmation"
    
  supporting_documents:
    electronic_receipts: "Preference for electronic documentation"
    document_scanning: "OCR processing for paper documents"
    cloud_storage: "Secure document archive with retention policies"
    
Tax_Authority_Communication:
  audit_requests: "Immediate alert system for individual audit notifications"
  clarification_requests: "Track and respond to AADE inquiries"
  payment_confirmations: "Verify tax payment processing and receipts"
```

### 记录保存
```yaml
Documentation_Requirements:
  income_records:
    retention_period: "5 years from tax year end"
    required_documents: ["Employer certificates", "Bank statements", "Investment records"]
    
  deduction_support:
    medical_expenses: "Receipts with patient name and medical purpose"
    education_costs: "Official educational institution receipts"
    charitable_donations: "Certificates from recognized organizations"
    
  property_documentation:
    enfia_calculations: "Property value assessments and tax calculations"
    rental_records: "Income and expense tracking for rental properties"
    maintenance_costs: "Receipts for property improvements and repairs"
```

## 成功指标

一个成功的希腊个人税务处理系统应达到以下目标：
- ✅ 100% 准确地准备和提交 E1 表格
- ✅ 最大限度地识别和应用法律规定的税收减免项
- ✅ 通过家庭税务规划实现最优的税收负担
- ✅ 完整地整合和优化 ENFIA 税务流程
- ✅ 在 6 月 30 日之前及时提交税务申报表
- ✅ 提供全面的审计记录和文件支持
- ✅ 与工资收入和投资收入来源实现有效集成
- ✅ 提供专业的希腊税务咨询和规划服务

请注意：该功能主要针对雇员群体设计，提供全面的个人税务管理服务，同时确保遵守希腊税法并实现最高的税收合规和优化标准。