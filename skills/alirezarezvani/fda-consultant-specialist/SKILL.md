---
name: "fda-consultant-specialist"
description: FDA（美国食品药品监督管理局）医疗设备监管顾问，为医疗设备公司提供510(k)/PMA/De Novo申请流程的指导、QSR（21 CFR 820）合规性评估、HIPAA法规遵从性审核以及设备网络安全方面的咨询服务。当用户提及FDA提交、510(k)申请、PMA审批、De Novo流程、QSR要求、上市前审查、 predicate device（参考设备）、实质等同性评估、HIPAA相关医疗设备或FDA网络安全相关内容时，请参考该顾问的服务。
---
# FDA咨询专家

为医疗器械制造商提供FDA法规咨询服务，涵盖提交流程、质量体系法规（QSR）、HIPAA合规性以及设备网络安全要求。

## 目录

- [FDA提交路径选择](#fda-pathway-selection)
- [510(k)提交流程](#510k-submission-process)
- [QSR合规性](#qsr-compliance)
- [医疗器械的HIPAA合规性](#hipaa-for-medical-devices)
- [设备网络安全](#device-cybersecurity)
- [资源](#resources)

---

## FDA提交路径选择

根据设备分类和可用的Predicate来确定合适的FDA监管路径。

### 决策框架

```
Predicate device exists?
├── YES → Substantially equivalent?
│   ├── YES → 510(k) Pathway
│   │   ├── No design changes → Abbreviated 510(k)
│   │   ├── Manufacturing only → Special 510(k)
│   │   └── Design/performance → Traditional 510(k)
│   └── NO → PMA or De Novo
└── NO → Novel device?
    ├── Low-to-moderate risk → De Novo
    └── High risk (Class III) → PMA
```

### 路径比较

| 路径 | 使用时机 | 时间线 | 成本 |
|---------|-------------|----------|------|
| 510(k) 传统路径 | 存在Predicate，设计变更 | 90天 | $21,760 |
| 510(k) 特殊路径 | 仅涉及制造变更 | 30天 | $21,760 |
| 510(k) 缩略路径 | 遵循指南/标准 | 30天 | $21,760 |
| De Novo路径 | 新型设备，低至中等风险 | 150天 | $134,676 |
| PMA路径 | III类设备，无Predicate | 180天以上 | $425,000以上 |

### 提交前策略

1. 确定产品代码和分类
2. 在510(k)数据库中查找Predicate
3. 评估实质等同性的可行性
4. 为FDA准备Q-Sub问题
5. 如有需要，安排提交前会议

**参考：**请参阅[fda_submission_guide.md](references/fda_submission_guide.md)以获取路径决策矩阵和提交要求。

---

## 510(k)提交流程

### 工作流程

```
Phase 1: Planning
├── Step 1: Identify predicate device(s)
├── Step 2: Compare intended use and technology
├── Step 3: Determine testing requirements
└── Checkpoint: SE argument feasible?

Phase 2: Preparation
├── Step 4: Complete performance testing
├── Step 5: Prepare device description
├── Step 6: Document SE comparison
├── Step 7: Finalize labeling
└── Checkpoint: All required sections complete?

Phase 3: Submission
├── Step 8: Assemble submission package
├── Step 9: Submit via eSTAR
├── Step 10: Track acknowledgment
└── Checkpoint: Submission accepted?

Phase 4: Review
├── Step 11: Monitor review status
├── Step 12: Respond to AI requests
├── Step 13: Receive decision
└── Verification: SE letter received?
```

### 必需提交的文件（21 CFR 807.87）

| 文件 | 内容 |
|---------|---------|
| 封面信 | 提交类型、设备ID、联系方式 |
| 表格3514 | CDRH上市前审查封面页 |
| 设备描述 | 物理描述、工作原理 |
| 使用说明 | 表格3881、适用患者群体、使用环境 |
| 实质等同性比较 | 与Predicate的对比 |
| 性能测试 | 台架测试、生物相容性、电气安全 |
| 软件文档 | 风险等级、危险分析（IEC 62304） |
| 标签 | 使用说明书、包装标签、警告信息 |
| 510(k)提交摘要 | 提交内容的公开摘要 |

### 常见RTA问题

| 问题 | 预防措施 |
|-------|------------|
| 未支付用户费用 | 提交前核实费用支付情况 |
| 表格3514填写不完整 | 审查所有字段，确保签名完整 |
| 未找到Predicate | 在FDA数据库中确认K编号 |
| 实质等同性比较不充分 | 全面说明技术特性 |

---

## QSR合规性

医疗器械制造商需遵守的质量体系法规（21 CFR Part 820）要求。

### 关键子系统

| 条款 | 标题 | 重点 |
|---------|-------|-------|
| 820.20 | 管理责任 | 质量政策、组织结构、管理评审 |
| 820.30 | 设计控制 | 输入控制、输出控制、审查控制、验证控制 |
| 820.40 | 文件控制 | 批准控制、文件分发、变更控制 |
| 820.50 | 采购控制 | 供应商资质、采购数据 |
| 820.70 | 生产控制 | 过程验证、环境控制 |
| 820.100 | CAPA | 根本原因分析、纠正措施 |
| 820.181 | 设备主记录 | 规格要求、操作程序、验收标准 |

### 设计控制工作流程（820.30）

```
Step 1: Design Input
└── Capture user needs, intended use, regulatory requirements
    Verification: Inputs reviewed and approved?

Step 2: Design Output
└── Create specifications, drawings, software architecture
    Verification: Outputs traceable to inputs?

Step 3: Design Review
└── Conduct reviews at each phase milestone
    Verification: Review records with signatures?

Step 4: Design Verification
└── Perform testing against specifications
    Verification: All tests pass acceptance criteria?

Step 5: Design Validation
└── Confirm device meets user needs in actual use conditions
    Verification: Validation report approved?

Step 6: Design Transfer
└── Release to production with DMR complete
    Verification: Transfer checklist complete?
```

### CAPA流程（820.100）

1. **识别**：记录不符合项或潜在问题
2. **调查**：进行根本原因分析（5个“为什么”和鱼骨图）
3. **计划**：制定纠正/预防措施
4. **实施**：执行措施，更新文档
5. **验证**：确认措施已落实
6. **有效性**：监控问题是否再次发生（30-90天）
7. **关闭**：获得管理层批准并完成流程

**参考：**请参阅[qsr_compliance_requirements.md](references/qsr_compliance_requirements.md)以获取详细的QSR实施指南。

---

## 医疗器械的HIPAA合规性

针对创建、存储、传输或访问受保护健康信息（PHI）的医疗器械的HIPAA要求。

### 适用范围

| 设备类型 | 是否适用HIPAA |
|-------------|---------------|
| 独立诊断设备（无数据传输） | 不适用 |
| 传输患者数据的连接设备 | 适用 |
| 集成电子健康记录（EHR）的设备 | 适用 |
| 存储患者信息的健康应用程序 | 适用（仅限存储PHI的情况） |

### 必需的安全措施

```
Administrative (§164.308)
├── Security officer designation
├── Risk analysis and management
├── Workforce training
├── Incident response procedures
└── Business associate agreements

Physical (§164.310)
├── Facility access controls
├── Workstation security
└── Device disposal procedures

Technical (§164.312)
├── Access control (unique IDs, auto-logoff)
├── Audit controls (logging)
├── Integrity controls (checksums, hashes)
├── Authentication (MFA recommended)
└── Transmission security (TLS 1.2+)
```

### 风险评估步骤

1. 清理所有处理电子PHI的系统
2. 记录数据流（收集、存储、传输）
3. 识别威胁和漏洞
4. 评估风险的可能性和影响
5. 确定风险等级
6. 实施控制措施
7. 记录剩余风险

**参考：**请参阅[hipaa_compliance_framework.md](references/hipaa_compliance_framework.md)以获取实施检查清单和BAA模板。

---

## 设备网络安全

FDA对连接型医疗器械的网络安全要求。

### 上市前要求

| 要素 | 描述 |
|---------|-------------|
| 威胁模型 | STRIDE分析、攻击树、信任边界 |
| 安全控制 | 认证、加密、访问控制 |
| SBOM | 软件物料清单（CycloneDX或SPDX） |
| 安全测试 | 渗透测试、漏洞扫描 |
| 漏洞管理计划 | 漏洞披露流程、补丁管理 |

### 设备风险等级分类

**等级1（高风险）：**
- 连接到网络/互联网
- 网络安全事件可能导致患者受伤

**等级2（标准风险）：**
- 其他所有连接型设备

### 上市后义务

1. 监控NVD和ICS-CERT发布的漏洞信息
2. 评估漏洞对设备组件的影响
3. 开发并测试补丁
4. 与客户沟通
5. 按照FDA指南进行报告

### 协调漏洞披露

```
Researcher Report
    ↓
Acknowledgment (48 hours)
    ↓
Initial Assessment (5 days)
    ↓
Fix Development
    ↓
Coordinated Public Disclosure
```

**参考：**请参阅[device_cybersecurity_guidance.md](references/device_cybersecurity_guidance.md)以获取SBOM格式示例和威胁建模模板。

---

## 资源

### 脚本

| 脚本 | 用途 |
|--------|---------|
| `fda_submission_tracker.py` | 跟踪510(k)/PMA/De Novo提交的里程碑和时间线 |
| `qsr_compliance_checker.py | 根据项目文档评估21 CFR 820的合规性 |
| `hipaa_risk_assessment.py | 评估医疗器械软件中的HIPAA安全措施 |

### 参考资料

| 文件 | 内容 |
|------|---------|
| `fda_submission_guide.md` | 510(k)、De Novo、PMA提交要求和检查清单 |
| `qsr_compliance_requirements.md | 21 CFR 820实施指南及模板 |
| `hipaa_compliance_framework.md | HIPAA安全规则、BAA要求 |
| `device_cybersecurity_guidance.md | FDA网络安全要求、SBOM、威胁建模 |
| `fda_capa_requirements.md | CAPA流程、根本原因分析、有效性验证 |

### 使用示例

```bash
# Track FDA submission status
python scripts/fda_submission_tracker.py /path/to/project --type 510k

# Assess QSR compliance
python scripts/qsr_compliance_checker.py /path/to/project --section 820.30

# Run HIPAA risk assessment
python scripts/hipaa_risk_assessment.py /path/to/project --category technical
```