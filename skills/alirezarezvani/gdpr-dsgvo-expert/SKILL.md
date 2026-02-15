---
name: gdpr-dsgvo-expert
description: GDPR与德国数据保护法（DSGVO）合规性自动化工具：  
该工具能够自动扫描代码库以识别潜在的隐私风险，生成数据保护影响评估（DPIA）报告，并追踪数据主体提出的权利请求。适用于GDPR合规性评估、隐私审计、数据保护规划、DPIA报告的生成以及数据主体权利的管理工作。
---

# GDPR/DSGVO 专家

提供符合欧盟通用数据保护条例（GDPR）和德国《联邦数据保护法》（BDSG）要求的工具和指导。

---

## 目录

- [工具](#tools)
  - [GDPR 合规性检查器](#gdpr-compliance-checker)
  - [数据保护影响评估（DPIA）生成器](#dpia-generator)
  - [数据主体权利追踪器](#data-subject-rights-tracker)
- [参考指南](#reference-guides)
- [工作流程](#workflows)

---

## 工具

### GDPR 合规性检查器

扫描代码库，查找潜在的 GDPR 合规性问题，包括个人数据的使用情况以及可能存在风险的做法。

```bash
# Scan a project directory
python scripts/gdpr_compliance_checker.py /path/to/project

# JSON output for CI/CD integration
python scripts/gdpr_compliance_checker.py . --json --output report.json
```

**检测内容：**
- 个人数据（电子邮件、电话号码、IP 地址）
- 特殊类别数据（健康信息、生物识别数据、宗教信仰）
- 财务数据（信用卡信息、IBAN）
- 高风险代码实践：
  - 记录个人数据
- 缺乏同意机制
- 数据保留期限不明确
- 敏感数据未加密
- 禁用了数据删除功能

**输出结果：**
- 合规性评分（0-100 分）
- 风险等级（严重、较高、中等）
- 带有 GDPR 条文引用的优先处理建议

---

### 数据保护影响评估（DPIA）生成器

根据第 35 条的要求生成数据保护影响评估文档。

```bash
# Get input template
python scripts/dpia_generator.py --template > input.json

# Generate DPIA report
python scripts/dpia_generator.py --input input.json --output dpia_report.md
```

**功能：**
- 自动评估 DPIA 风险等级
- 根据数据处理特点识别风险
- 生成法律依据相关文件
- 提出风险缓解建议
- 生成 Markdown 格式的报告

**触发 DPIA 评估的情况：**
- 系统性监控（第 35(3)(c) 条）
- 大规模处理特殊类别数据（第 35(3)(b) 条）
- 自动化决策（第 35(3)(a) 条）
- 符合 WP29 高风险标准的情况

---

### 数据主体权利追踪器

管理根据 GDPR 第 15-22 条规定的数据主体权利请求。

```bash
# Add new request
python scripts/data_subject_rights_tracker.py add \
  --type access --subject "John Doe" --email "john@example.com"

# List all requests
python scripts/data_subject_rights_tracker.py list

# Update status
python scripts/data_subject_rights_tracker.py status --id DSR-202601-0001 --update verified

# Generate compliance report
python scripts/data_subject_rights_tracker.py report --output compliance.json

# Generate response template
python scripts/data_subject_rights_tracker.py template --id DSR-202601-0001
```

**支持的数据主体权利：**

| 权利 | 条文 | 截止期限 |
|-------|---------|----------|
| 查阅权 | 第 15 条 | 30 天 |
| 更正权 | 第 16 条 | 30 天 |
- 删除权 | 第 17 条 | 30 天 |
- 限制处理权 | 第 18 条 | 30 天 |
- 数据迁移权 | 第 20 条 | 30 天 |
- 拒绝处理权 | 第 21 条 | 30 天 |
- 对自动化决策的反对权 | 第 22 条 | 30 天 |

**功能：**
- 跟踪截止日期并发送逾期提醒
- 身份验证流程
- 生成回复模板
- 提供合规性报告

---

## 参考指南

### GDPR 合规性指南
`references/gdpr_compliance_guide.md`

提供全面的实施指南，涵盖以下内容：
- 数据处理的合法依据（第 6 条）
- 特殊类别数据的处理要求（第 9 条）
- 数据主体权利的实施
- 责任要求（第 30 条）
- 数据跨境传输（第五章）
- 数据泄露通知（第 33-34 条）

### 德国《联邦数据保护法》（BDSG）要求
`references/german_bdsg_requirements.md`

德国特有的要求包括：
- 需要任命数据保护官（DPO）的门槛（BDSG 第 38 条——员工人数超过 20 人）
- 雇佣数据处理相关要求（BDSG 第 26 条）
- 视频监控规则（BDSG 第 4 条）
- 信用评分相关要求（BDSG 第 31 条）
- 各州的数据保护法规
- 工会参与决策的权利

### 数据保护影响评估（DPIA）方法论
`references/dpia_methodology.md`

数据保护影响评估的步骤：
- 风险评估标准
- WP29 高风险指标
- 风险评估方法
- 风险缓解措施
- 数据保护官与监管机构的沟通流程
- 模板和检查清单

---

## 工作流程

### 工作流程 1：新数据处理活动的评估

```
Step 1: Run compliance checker on codebase
        → python scripts/gdpr_compliance_checker.py /path/to/code

Step 2: Review findings and compliance score
        → Address critical and high issues

Step 3: Determine if DPIA required
        → Check references/dpia_methodology.md threshold criteria

Step 4: If DPIA required, generate assessment
        → python scripts/dpia_generator.py --template > input.json
        → Fill in processing details
        → python scripts/dpia_generator.py --input input.json --output dpia.md

Step 5: Document in records of processing activities
```

### 工作流程 2：处理数据主体请求

```
Step 1: Log request in tracker
        → python scripts/data_subject_rights_tracker.py add --type [type] ...

Step 2: Verify identity (proportionate measures)
        → python scripts/data_subject_rights_tracker.py status --id [ID] --update verified

Step 3: Gather data from systems
        → python scripts/data_subject_rights_tracker.py status --id [ID] --update in_progress

Step 4: Generate response
        → python scripts/data_subject_rights_tracker.py template --id [ID]

Step 5: Send response and complete
        → python scripts/data_subject_rights_tracker.py status --id [ID] --update completed

Step 6: Monitor compliance
        → python scripts/data_subject_rights_tracker.py report
```

### 工作流程 3：德国《联邦数据保护法》合规性检查

```
Step 1: Determine if DPO required
        → 20+ employees processing personal data automatically
        → OR processing requires DPIA
        → OR business involves data transfer/market research

Step 2: If employees involved, review § 26 BDSG
        → Document legal basis for employee data
        → Check works council requirements

Step 3: If video surveillance, comply with § 4 BDSG
        → Install signage
        → Document necessity
        → Limit retention

Step 4: Register DPO with supervisory authority
        → See references/german_bdsg_requirements.md for authority list
```

---

## 关键的 GDPR 概念

### 合法依据（第 6 条）

- **同意**：用于营销、发送新闻通讯、进行分析，必须基于自愿、明确且充分告知的原则
- **合同**：用于订单履行、服务提供
- **法律义务**：如税务记录、劳动法相关处理
- **合法利益**：用于预防欺诈、保障安全（需进行利益平衡测试）

### 特殊类别数据（第 9 条）

处理特殊类别数据时必须获得明确同意，或符合第 9(2) 条的例外情况：
- 健康数据
- 生物识别数据
- 种族/民族背景
- 政治观点
- 宗教信仰
- 工会会员身份
- 基因数据
- 性取向

### 数据主体权利

所有权利必须在 **30 天内**得到履行（复杂请求可延长至 90 天）：
- **查阅权**：提供数据副本和处理信息
- **更正权**：纠正错误数据
- **删除权**：删除数据（法律义务除外）
- **限制处理权**：在问题解决期间限制数据处理
- **数据迁移权**：以机器可读格式提供数据
- **拒绝处理权**：基于合法利益停止数据处理

### 德国《联邦数据保护法》的额外规定

| 条款 | 关键要求 | 详细说明 |
|-------|--------------|-----------------|
| 数据保护官任命门槛 | 第 38 条 | 员工人数超过 20 人时必须任命数据保护官 |
| 雇佣数据处理 | 第 26 条 | 详细的员工数据处理规定 |
- 视频监控 | 第 4 条 | 视频监控的设置和比例原则 |
- 信用评分 | 第 31 条 | 算法的可解释性要求 |