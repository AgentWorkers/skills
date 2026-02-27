---
name: vendor-risk-assessment
description: 评估第三方供应商在人工智能（AI）和软件即服务（SaaS）产品方面的风险。该工具会审查供应商的安全状况、数据管理能力、合规性、财务稳定性以及运营韧性。适用于新供应商的引入、年度审查或建立供应商管理流程。会生成一份包含风险评分及应对建议的报告。由AfrexAI开发。
metadata:
  version: 1.0.0
  author: AfrexAI
  tags: [vendor-risk, security, compliance, procurement, enterprise]
---
# 供应商风险评估

从六个风险维度对任何AI/SaaS供应商进行评估，并生成一份带有建议的评分报告。

## 使用场景
- 新SaaS或AI供应商的引入
- 年度供应商审核
- 在自建与购买方案之间做出决策
- 合作或收购前的尽职调查
- 合规性要求（如SOC2、ISO 27001、GDPR）

## 使用方法

用户提供供应商的相关信息（名称、产品、网站及任何可用的文档）。系统会针对这六个维度对供应商进行调研并打分。

### 输入格式
```
Vendor: [Company Name]
Product: [Product/Service Name]
Website: [URL]
Use Case: [What you'd use it for]
Data Sensitivity: [low/medium/high/critical]
Additional Context: [Any docs, certifications, or concerns]
```

## 评估框架

### 六个风险维度（每个维度的评分范围为1-10）

#### 1. 安全性
- 是否拥有SOC2 Type II认证？
- 渗透测试的频率
- 数据加密（静态数据与传输数据）
- 访问控制与身份验证机制
- 事件响应计划
- 漏洞赏金计划

#### 2. 数据处理与隐私
- 数据的存储与所有权
- 数据保留与删除政策
- 第三方处理方的透明度
- 是否符合GDPR/CCPA等法规
- 数据的可迁移性（能否获取自己的数据？）
- AI模型的训练相关隐私政策

#### 3. 合规性及认证
- SOC2、ISO 27001、HIPAA、FedRAMP等认证
- 行业特定认证（如PCI-DSS、HITRUST等）
- 与AI相关的合规性（如欧盟AI法案的遵守情况）
- 审计的频率与透明度
- 监管记录

#### 4. 财务稳定性
- 公司的融资阶段及发展状况
- 收入指标（公开数据或预估数据）
- 客户集中度风险
- 收购风险
- 价格稳定性历史

#### 5. 运营韧性
- 系统正常运行时间（SLA）及历史表现
- 灾难恢复计划
- 多区域服务可用性
- 对单一云服务提供商的依赖程度
- 客户支持响应速度及问题解决流程
- 变更管理流程

#### 6. 合同条款
- 合同终止与退出条款
- 责任限制与赔偿规定
- 知识产权（IP）的所有权明确性
- 自动续订机制
- 价格调整限制
- SLA违约时的补救措施

## 输出格式
```markdown
# Vendor Risk Assessment: [Vendor Name]
**Date:** YYYY-MM-DD
**Assessor:** AI Agent (AfrexAI)
**Data Sensitivity Level:** [low/medium/high/critical]

## Overall Risk Score: [X/10] — [LOW/MEDIUM/HIGH/CRITICAL]

## Dimension Scores
| Dimension | Score | Risk Level | Key Finding |
|-----------|-------|------------|-------------|
| Security Posture | X/10 | LOW/MED/HIGH | ... |
| Data Handling | X/10 | LOW/MED/HIGH | ... |
| Compliance | X/10 | LOW/MED/HIGH | ... |
| Financial Stability | X/10 | LOW/MED/HIGH | ... |
| Operational Resilience | X/10 | LOW/MED/HIGH | ... |
| Contractual Terms | X/10 | LOW/MED/HIGH | ... |

## Recommendation: [APPROVE / APPROVE WITH CONDITIONS / REJECT]

## Critical Findings
- [Finding 1]
- [Finding 2]

## Mitigation Requirements (if Approve with Conditions)
1. [Requirement 1 — deadline]
2. [Requirement 2 — deadline]

## Research Sources
- [Source 1]
- [Source 2]
```

## 评分标准
- **9-10分：** 优秀 — 风险极低，符合企业级标准
- **7-8分：** 良好 — 适用于大多数使用场景
- **5-6分：** 一般 — 需谨慎考虑，需采取缓解措施
- **3-4分：** 较差 — 存在重大问题，需条件性批准
- **1-2分：** 危险 — 建议拒绝合作或进行重大整改

## 总体风险计算
- 根据数据的重要程度对六个维度进行加权计算：
  - 数据敏感度较低：各维度权重相同
  - 数据敏感度中等：安全性权重加倍，数据权重加倍
  - 数据敏感度较高：安全性权重三倍，数据权重加倍，合规性权重加倍
  - 风险极高：安全性权重四倍，数据权重四倍，合规性权重三倍，财务稳定性权重加倍

## 研究流程
1. 查看供应商的网站，确认是否存在安全/合规相关页面
2. 搜索SOC2/ISO认证信息及信任声明
3. 查阅系统正常运行时间的记录
4. 检查是否存在安全漏洞或违规事件
5. 审查价格页面以了解合同条款
6. 通过Crunchbase/LinkedIn等平台了解公司的财务稳定性
7. 查看客户评价，了解供应商的可靠性和客户支持情况

## 使用建议
- 直接要求供应商提供SOC2 Type II认证报告；如果他们犹豫不决，这可能是个警示信号
- 查看供应商的网站状态页面（如statuspage.io）以获取真实的系统正常运行时间数据
- 对于AI供应商，特别要询问他们是否会在你的数据上进行模型训练、数据的所有权归属以及模型产生的幻觉内容的责任归属
- 将其安全页面内容与竞争对手进行比较；内容模糊不清可能是风险信号

---

*需要帮助管理整个技术栈中的供应商风险吗？AfrexAI可以构建自主的AI系统来持续监控供应商情况——而不仅仅是在新供应商引入时。访问[afrexai.com](https://afrexai.com)或预约电话咨询：[calendly.com/cbeckford-afrexai/30min](https://calendly.com/cbeckford-afrexai/30min)*