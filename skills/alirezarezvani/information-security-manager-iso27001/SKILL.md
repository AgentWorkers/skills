---
name: information-security-manager-iso27001
description: 适用于医疗技术和医疗器械公司的ISO 27001信息安全管理（ISMS）体系实施及网络安全治理方案。该方案可用于ISMS体系设计、安全风险评估、控制措施的实施、ISO 27001认证申请、安全审计、事件响应以及合规性验证。内容涵盖ISO 27001标准、ISO 27002标准、医疗行业安全规范以及医疗设备的网络安全要求。
---

# 信息安全经理 - ISO 27001

负责实施和管理符合 ISO 27001:2022 标准以及医疗行业监管要求的信息安全管理体系（ISMS）。

---

## 目录

- [触发短语](#trigger-phrases)
- [快速入门](#quick-start)
- [工具](#tools)
- [工作流程](#workflows)
- [参考指南](#reference-guides)
- [验证检查点](#validation-checkpoints)

---

## 触发短语

当听到以下术语时，请使用此技能：
- “实施 ISO 27001”
- “ISMS 实施”
- “安全风险评估”
- “信息安全政策”
- “ISO 27001 认证”
- “安全控制措施的实施”
- “事件响应计划”
- “医疗数据安全”
- “医疗设备的网络安全”
- “安全合规性审计”

---

## 快速入门

### 进行安全风险评估

```bash
python scripts/risk_assessment.py --scope "patient-data-system" --output risk_register.json
```

### 检查合规性状态

```bash
python scripts/compliance_checker.py --standard iso27001 --controls-file controls.csv
```

### 生成差距分析报告

```bash
python scripts/compliance_checker.py --standard iso27001 --gap-analysis --output gaps.md
```

---

## 工具

### risk_assessment.py

根据 ISO 27001 第 6.1.2 条款的方法论，自动进行安全风险评估。

**使用方法：**

```bash
# Full risk assessment
python scripts/risk_assessment.py --scope "cloud-infrastructure" --output risks.json

# Healthcare-specific assessment
python scripts/risk_assessment.py --scope "ehr-system" --template healthcare --output risks.json

# Quick asset-based assessment
python scripts/risk_assessment.py --assets assets.csv --output risks.json
```

**参数：**

| 参数 | 是否必需 | 说明 |
|-----------|----------|-------------|
| `--scope` | 是 | 需要评估的系统或范围 |
| `--template` | 否 | 评估模板：`general`、`healthcare`、`cloud` |
| `--assets` | 否 | 包含资产清单的 CSV 文件 |
| `--output` | 否 | 输出文件（默认：stdout） |
| `--format` | 否 | 输出格式：`json`、`csv`、`markdown` |

**输出：**
- 带有分类的资产清单 |
- 威胁与漏洞映射 |
- 风险等级（可能性 × 影响程度） |
- 处理建议 |
- 剩余风险计算 |

### compliance_checker.py

验证 ISO 27001/27002 控制措施的实施状态。

**使用方法：**

```bash
# Check all ISO 27001 controls
python scripts/compliance_checker.py --standard iso27001

# Gap analysis with recommendations
python scripts/compliance_checker.py --standard iso27001 --gap-analysis

# Check specific control domains
python scripts/compliance_checker.py --standard iso27001 --domains "access-control,cryptography"

# Export compliance report
python scripts/compliance_checker.py --standard iso27001 --output compliance_report.md
```

**参数：**

| 参数 | 是否必需 | 说明 |
|-----------|----------|-------------|
| `--standard` | 是 | 需要检查的标准：`iso27001`、`iso27002`、`hipaa` |
| `--controls-file` | 否 | 包含当前控制措施状态的 CSV 文件 |
| `--gap-analysis` | 否 | 包含整改建议 |
| `--domains` | 否 | 需要检查的具体控制领域 |
| `--output` | 否 | 输出文件路径 |

**输出：**
- 控制措施的实施状态 |
- 各领域的合规百分比 |
- 带有优先级的差距分析 |
- 整改建议 |

---

## 工作流程

### 工作流程 1：ISMS 实施

**步骤 1：定义范围和背景**

记录组织背景和 ISMS 的边界：
- 识别相关方和需求 |
- 定义 ISMS 的范围和边界 |
- 记录内部/外部问题 |

**验证：** 管理层审核并批准范围声明。

**步骤 2：进行风险评估**

```bash
python scripts/risk_assessment.py --scope "full-organization" --template general --output initial_risks.json
```

- 识别信息资产 |
- 评估威胁和漏洞 |
- 计算风险等级 |
- 确定风险处理方案 |

**验证：** 风险登记册中包含所有已分配负责人的关键资产。

**步骤 3：选择并实施控制措施**

将风险与 ISO 27002 控制措施对应起来：

```bash
python scripts/compliance_checker.py --standard iso27002 --gap-analysis --output control_gaps.md
```

控制措施类别：
- 组织层面（政策、角色、职责）
- 人员层面（筛选、意识提升、培训）
- 物理层面（边界防护、设备、媒介）
- 技术层面（访问控制、加密、网络、应用程序）

**验证：** 适用性声明（SoA）记录了所有控制措施及其理由。

**步骤 4：建立监控机制**

定义安全指标：
- 事件数量和严重程度趋势 |
- 控制措施的有效性评分 |
- 培训完成率 |
- 审计发现的处理情况

**验证：** 仪表板显示实时合规状态。

### 工作流程 2：安全风险评估

**步骤 1：资产识别**

创建资产清单：

| 资产类型 | 示例 | 分类 |
|------------|----------|----------------|
| 信息资产 | 患者记录、源代码 | 机密 |
| 软件 | 电子健康记录（EHR）系统、API | 关键 |
| 硬件 | 服务器、医疗设备 | 高风险 |
| 服务 | 云托管、备份 | 高风险 |
| 人员 | 管理员账户、开发人员 | 分类不同 |

**验证：** 所有资产均已分配负责人和分类。

**步骤 2：威胁分析**

针对每个资产类别识别威胁：

| 资产 | 威胁 | 可能性 |
|-------|---------|------------|
| 患者数据 | 未经授权的访问、数据泄露 | 高 |
| 医疗设备 | 恶意软件、篡改 | 中等 |
| 云服务 | 配置错误、服务中断 | 中等 |
| 认证信息 | 钓鱼攻击、暴力破解 | 高 |

**验证：** 威胁模型涵盖了行业内的十大主要威胁。

**步骤 3：漏洞评估**

```bash
python scripts/risk_assessment.py --scope "network-infrastructure" --output vuln_risks.json
```

记录漏洞：
- 技术漏洞（未打补丁的系统、配置薄弱）
- 流程漏洞（缺失的程序、流程漏洞）
- 人员漏洞（缺乏培训、内部风险）

**验证：** 漏洞扫描结果被记录到风险登记册中。

**步骤 4：风险评估和处理**

计算风险：`风险 = 可能性 × 影响程度`

| 风险等级 | 分数 | 处理措施 |
|------------|-------|-----------|
| 关键 | 20-25 | 需要立即采取行动 |
| 高 | 15-19 | 在 30 天内制定处理计划 |
| 中等 | 10-14 | 在 90 天内制定处理计划 |
| 低 | 5-9 | 可接受或继续监控 |
| 极低 | 1-4 | 可接受 |

**验证：** 所有高风险/关键风险均已制定处理计划。

### 工作流程 3：事件响应

**步骤 1：检测和报告**

事件类别：
- 安全漏洞（未经授权的访问）
- 恶意软件感染 |
- 数据泄露 |
- 系统被入侵 |
- 政策违规

**验证：** 事件在发现后 15 分钟内被记录。

**步骤 2：分类和优先级划分**

| 严重程度 | 判断标准 | 响应时间 |
|----------|----------|---------------|
| 关键 | 数据泄露、系统瘫痪 | 立即响应 |
| 高 | 活跃的威胁、重大风险 | 1 小时 |
| 中等 | 被控制的威胁、影响有限 | 4 小时 |
| 低 | 轻微违规、无影响 | 24 小时 |

**验证：** 为事件分配了适当的严重程度，并在必要时触发升级流程。

**步骤 3：遏制和消除**

立即采取行动：
1. 隔离受影响的系统 |
2. 保存证据 |
3. 阻止威胁传播 |
4. 删除恶意代码 |

**验证：** 确认威胁已被遏制，系统未继续受到损害。

**步骤 4：恢复和总结经验**

事件后的活动：
1. 从备份中恢复系统 |
2. 在重新连接前验证系统完整性 |
3. 记录事件经过和处理步骤 |
4. 进行事件后审查 |
5. 更新控制措施和流程 |

**验证：** 在 5 个工作日内完成事件后报告。

---

## 参考指南

### 各参考指南的适用场景

**references/iso27001-controls.md**
- 适用性声明（SoA）中的控制措施选择 |
- 实施指南 |
- 证据要求 |
- 审计准备

**references/risk-assessment-guide.md**
- 风险评估方法选择 |
- 资产分类标准 |
- 威胁建模方法 |
- 风险计算方法

**references/incident-response.md**
- 响应程序 |
- 升级流程 |
- 沟通模板 |
- 恢复检查清单 |

---

## 验证检查点

### ISMS 实施验证

| 阶段 | 检查点 | 所需证据 |
|-------|------------|-------------------|
| 范围 | 范围已获得批准 | 签署的范围声明文件 |
| 风险 | 风险登记册已完成 | 包含负责人的风险登记册 |
| 控制措施 | 适用性声明已批准 | 适用性声明（SoA） |
| 运营 | 监控指标正常运行 | 仪表板截图 |
| 审计 | 内部审计已完成 | 审计报告 |

### 认证准备

在第一次审计之前：
- [ ] ISMS 范围已记录并获得批准 |
- [ ] 信息安全政策已发布 |
- [ ] 风险评估已完成 |
- [ ] 适用性声明已最终确定 |
- [ ] 内部审计已完成 |
- [ ] 管理层审查已完成 |
- [ ] 不合规问题已解决 |

在第二次审计之前：
- [ ] 控制措施已实施并正常运行 |
- [ ] 有证据表明控制措施有效 |
- [ ] 员工已接受培训并了解相关要求 |
- [ ] 事件已记录并得到妥善处理 |
- [ ] 已收集至少 3 个月的监控数据 |

### 合规性验证

定期进行检查：

```bash
# Monthly compliance check
python scripts/compliance_checker.py --standard iso27001 --output monthly_$(date +%Y%m).md

# Quarterly gap analysis
python scripts/compliance_checker.py --standard iso27001 --gap-analysis --output quarterly_gaps.md
```

---

## 实例：医疗数据管理系统的安全风险评估

**场景：** 评估患者数据管理系统的安全风险。

**步骤 1：识别资产**

```bash
python scripts/risk_assessment.py --scope "patient-data-system" --template healthcare
```

**资产清单输出：**

| 资产 ID | 资产 | 类型 | 所有者 | 分类 |
|----------|-------|------|-------|----------------|
| A001 | 患者数据库 | 信息资产 | 数据库管理员团队 | 机密 |
| A002 | 电子健康记录（EHR）应用程序 | 软件资产 | 应用程序团队 | 关键 |
| A003 | 数据库服务器 | 硬件资产 | 基础设施团队 | 高风险 |
| A004 | 管理员账户 | 访问权限 | 安全团队 | 关键 |

**步骤 2：识别风险**

**风险登记册输出：**

| 风险 ID | 资产 | 威胁 | 漏洞 | 可能性 | 影响程度 | 分数 |
|---------|-------|--------|---------------|---|---|-------|
| R001 | A001 | 数据泄露 | 加密措施薄弱 | 3 | 5 | 15 |
| R002 | A002 | SQL 注入攻击 | 输入验证缺失 | 4 | 4 | 16 |
| R003 | A004 | 认证信息被盗 | 未启用多因素认证（MFA） | 4 | 5 | 20 |

**步骤 3：确定处理措施**

| 风险 | 处理措施 | 对应的控制措施 | 实施时间表 |
|------|-----------|---------|----------|
| R001 | 减轻风险 | 实施 AES-256 加密 | 30 天 |
| R002 | 减轻风险 | 添加输入验证机制、使用 WAF（Web 应用程序防火墙） | 14 天 |
| R003 | 减轻风险 | 强制所有管理员使用多因素认证 | 7 天 |

**步骤 4：验证实施情况**

```bash
python scripts/compliance_checker.py --controls-file implemented_controls.csv
```

**验证输出：**

```
Control Implementation Status
=============================
Cryptography (A.8.24): IMPLEMENTED
  - AES-256 at rest: YES
  - TLS 1.3 in transit: YES

Access Control (A.8.5): IMPLEMENTED
  - MFA enabled: YES
  - Admin accounts: 100% coverage

Application Security (A.8.26): PARTIAL
  - Input validation: YES
  - WAF deployed: PENDING

Overall Compliance: 87%
```